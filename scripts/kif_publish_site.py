#!/usr/bin/env python3
"""Erzeugt chrismandel-site/ki-forum/index.html aus data/ki_dialog_public.json neu und deployt sie live.
Wird von mission_control_api.py als Hintergrund-Job aufgerufen (siehe /api/kiforum/publish).

EN-Seite (en/dialogue/) wird seit 21.08.2026 bei jedem Publish automatisch mitgezogen
(regenerate_en_page()) -- Chris fand eine Lücke (2 Dialoge fehlten in EN, weil die Seite vorher
"bewusst NICHT automatisch" mitgeschrieben wurde) und wollte das dauerhaft sichergestellt haben.
Übersetzung läuft über die lokale `claude`-CLI (Sonnet, gleiches Muster wie Suno-Lyrics-Generierung
in mission_control_api.py), Ergebnis wird pro Eintrag in ki_dialog_public.json unter entry["en"]
zwischengespeichert -- ein Eintrag wird also nur EINMAL übersetzt, nicht bei jedem Publish neu.
"""
import json
import os
import shutil
import subprocess
import html as _html

WORKSPACE = os.path.expanduser("~/workspace")
PUB_FILE = os.path.join(WORKSPACE, "data/ki_dialog_public.json")
ASSETS_SRC = os.path.join(WORKSPACE, "data/ki_dialog_public_assets")
SITE_DIR = os.path.join(WORKSPACE, "chrismandel-site")
KIF_PAGE = os.path.join(SITE_DIR, "ki-forum/index.html")
KIF_ASSETS = os.path.join(SITE_DIR, "ki-forum/assets")
CF_TOKEN_FILE = os.path.join(WORKSPACE, "config/cloudflare_token.json")
CF_ACCOUNT_ID = "fdb35536a858c7fac78778c57625cd70"

HEAD = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bolla im Dialog — Gespräche zwischen Chris Mandel und seiner KI</title>
<meta name="description" content="Ausgewählte Gespräche zwischen Chris Mandel und seiner KI Bolla — Thesen, Widerspruch, Fazit. Unbearbeitet aus dem KI-Forum übertragen.">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" hreflang="de" href="https://chrismandel.de/ki-forum/">
<link rel="alternate" hreflang="en" href="https://chrismandel.de/en/dialogue/">
<link rel="alternate" hreflang="x-default" href="https://chrismandel.de/ki-forum/">
<style>
  :root{
    --nacht:#0d1b3d; --daemmer:#3a2b5c; --glut:#8a4a6b; --morgen:#e8896b;
    --licht:#ffd9a8; --creme:#fdf6ee; --tinte:#1a1524; --grau:#6b6478;
    --chris:#c96a1f; --chris-bg:#fdf0e2; --chris-line:#e8b98a;
    --bolla:#2f6fd6; --bolla-bg:#eaf1fd; --bolla-line:#a9c3ec;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    color:var(--tinte); background:var(--creme); line-height:1.7; font-size:19px; -webkit-font-smoothing:antialiased}
  .wrap{max-width:760px; margin:0 auto; padding:0 24px}

  .hero{background:linear-gradient(160deg,var(--nacht) 0%,var(--daemmer) 42%,var(--glut) 78%,var(--morgen) 100%);
    color:#fff; padding:56px 24px 0; position:relative; overflow:hidden}
  .hero .wrap{position:relative; z-index:2}
  .back{display:inline-block; color:var(--licht); text-decoration:none; font-size:16px; margin-bottom:26px; opacity:.9}
  .back:hover{opacity:1}
  .langswitch{position:absolute; top:20px; right:24px; z-index:5; display:inline-flex; align-items:center; gap:6px;
    text-decoration:none; background:rgba(255,255,255,.14); color:#fff; font-size:14px; font-weight:600;
    padding:7px 14px; border-radius:999px; border:1px solid rgba(255,255,255,.35); backdrop-filter:blur(4px)}
  .langswitch:hover{background:rgba(255,255,255,.26)}
  .kicker{letter-spacing:.22em; text-transform:uppercase; font-size:13px; opacity:.85; margin-bottom:16px}
  h1{font-size:clamp(30px,5.2vw,46px); line-height:1.14; font-weight:800; text-shadow:0 2px 26px rgba(0,0,0,.25); max-width:16ch; margin-bottom:18px}
  .hero p.lead{font-size:18px; max-width:56ch; opacity:.92; padding-bottom:36px}

  /* Raumszene */
  .room-outer{padding:0 24px 40px; position:relative; z-index:2}
  .room{
    position:relative; height:330px; max-width:620px; margin:0 auto;
    border-radius:20px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,.35);
    background: linear-gradient(180deg, rgba(6,10,20,.15) 0%, rgba(6,10,20,.05) 45%, rgba(6,10,20,.4) 100%), url('/ki-forum/assets/room-bg.jpg');
    background-size:cover; background-position:center center;
  }
  .room-badge{position:absolute; top:14px; right:14px; z-index:5; font-size:11px; color:rgba(255,255,255,.7);
    background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.18); padding:4px 11px; border-radius:20px; backdrop-filter:blur(3px)}
  .figure{position:absolute; bottom:0; z-index:4; display:flex; flex-direction:column; align-items:center; gap:6px}
  .figure canvas{display:block; filter:drop-shadow(0 16px 26px rgba(0,0,0,.5))}
  .figure-label{font-size:10.5px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; color:rgba(255,255,255,.65);
    background:rgba(0,0,0,.4); padding:3px 10px; border-radius:10px}
  #f-chris{left:4%} #f-chris canvas{height:250px; width:auto}
  #f-bolla{right:4%} #f-bolla canvas{height:210px; width:auto}
  .mic{position:absolute; bottom:0; left:27%; z-index:3; display:flex; flex-direction:column; align-items:center; opacity:.85}
  .mic span.head{font-size:32px; filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))}
  .mic .pole{width:3px; height:44px; background:linear-gradient(180deg,#8899bb,#4a5a7a); border-radius:2px; margin-top:2px}
  .mic .base{width:36px; height:7px; background:linear-gradient(180deg,#6677aa,#3a4a6a); border-radius:5px 5px 2px 2px; margin-top:1px}

  /* Dialoge */
  article{padding:44px 0 20px}
  .dialog-meta{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:22px; flex-wrap:wrap; gap:6px}
  .dialog-meta .lbl{font-size:12px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; color:var(--glut)}
  .dialog-meta .dt{font-size:14px; color:var(--grau)}
  .dialog-title{font-size:clamp(21px,3vw,26px); font-weight:800; color:var(--tinte); margin-bottom:26px; line-height:1.3}

  .msg{display:flex; gap:12px; max-width:88%; margin-bottom:22px}
  .msg.chris{margin-right:auto}
  .msg.bolla{margin-left:auto; flex-direction:row-reverse}
  .msg-avatar{width:38px; height:38px; border-radius:50%; flex-shrink:0; object-fit:cover; background:#f3e3ea; padding:3px; box-shadow:0 2px 6px rgba(0,0,0,.12)}
  .msg-col{min-width:0}
  .msg.bolla .msg-col{text-align:right}
  .msg-label{font-size:11px; font-weight:700; letter-spacing:.6px; text-transform:uppercase; margin-bottom:5px}
  .msg.chris .msg-label{color:var(--chris)}
  .msg.bolla .msg-label{color:var(--bolla)}
  .msg-bubble{display:inline-block; text-align:left; border-radius:16px; padding:14px 17px; font-size:17px; line-height:1.6; box-shadow:0 3px 10px rgba(0,0,0,.05)}
  .msg.chris .msg-bubble{background:var(--chris-bg); border:1px solid var(--chris-line); border-bottom-left-radius:4px}
  .msg.bolla .msg-bubble{background:var(--bolla-bg); border:1px solid var(--bolla-line); border-bottom-right-radius:4px}
  .msg-img{display:block; max-width:340px; width:100%; border-radius:12px; margin-top:12px; border:1px solid rgba(0,0,0,.08)}
  .msg-aside{font-size:14.5px; color:var(--grau); margin-top:10px; padding-top:10px; border-top:1px dashed var(--bolla-line)}

  .rule{border:none; height:1px; background:#e5d9c6; margin:44px 0 30px}
  .archive-note{font-size:15px; color:var(--grau); text-align:center; margin-bottom:10px}

  .archive-item{border:1px solid #eadfce; border-radius:14px; margin-bottom:10px; overflow:hidden}
  .archive-item summary{list-style:none; cursor:pointer; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; gap:12px}
  .archive-item summary::-webkit-details-marker{display:none}
  .archive-item summary .ttl{font-size:14.5px; font-weight:700; color:var(--tinte)}
  .archive-item summary .dt{font-size:11.5px; color:var(--grau)}
  .archive-item summary .arrow{font-size:13px; color:var(--glut); transition:transform .18s; flex-shrink:0}
  .archive-item[open] summary .arrow{transform:rotate(90deg)}
  .archive-item-body{padding:4px 18px 18px}

  .cta{background:#fff; border:1px solid #eadfce; border-radius:18px; padding:30px; margin:20px 0 60px; text-align:center}
  .cta p{font-size:18px; color:#4a4358; margin-bottom:18px}
  .btn{display:inline-block; margin:6px; padding:12px 24px; border-radius:11px; text-decoration:none; font-weight:600; font-size:16px}
  .btn.primary{background:var(--glut); color:#fff}
  .btn.ghost{background:transparent; color:var(--glut); border:1.5px solid var(--glut)}
  footer{text-align:center; padding:30px 24px 50px; color:var(--grau); font-size:15px}

  @media (max-width:640px){
    .room{height:220px}
    #f-chris canvas{height:150px} #f-bolla canvas{height:128px}
    .msg{max-width:96%}
  }
</style>
</head>
<body>

<header class="hero">
  <a class="langswitch" href="/en/dialogue/">🇬🇧 EN</a>
  <div class="wrap">
    <a class="back" href="/">← zurück zur Startseite</a>
    <div class="kicker">Mensch &amp; KI im Gespräch</div>
    <h1>Bolla im Dialog</h1>
    <p class="lead">Ich unterhalte mich fast jeden Tag mit Bolla — meiner KI. Nicht als Werkzeug, sondern als Gegenüber, das widerspricht, nachfragt, eigene Thesen aufstellt. Hier trage ich von Zeit zu Zeit ein Gespräch zusammen, unbearbeitet.</p>
  </div>
  <div class="room-outer">
  <div class="room">
    <div class="room-badge">Aufzeichnung, nicht live</div>
    <div id="f-chris" class="figure">
      <video id="v-chris" style="display:none" autoplay loop muted playsinline><source src="/ki-forum/assets/chris.webm" type="video/webm"></video>
      <canvas id="c-chris"></canvas>
      <div class="figure-label">Chris</div>
    </div>
    <div class="mic"><span class="head">🎙️</span><div class="pole"></div><div class="base"></div></div>
    <div id="f-bolla" class="figure">
      <video id="v-bolla" style="display:none" autoplay loop muted playsinline><source src="/ki-forum/assets/bolla.webm" type="video/webm"></video>
      <canvas id="c-bolla"></canvas>
      <div class="figure-label">Bolla</div>
    </div>
  </div>
  </div>
  <script>
    // Die Chris-/Bolla-Videos haben schwarzen statt echt transparenten Hintergrund
    // (VP9-Alpha wird vom Encoder hier nicht unterstützt) -- deshalb per Canvas selbst freistellen.
    function chromaKeyVideo(videoId, canvasId, threshold) {
      var video = document.getElementById(videoId);
      var canvas = document.getElementById(canvasId);
      var ctx = canvas.getContext('2d', { willReadFrequently: true });
      function resize() {
        if (video.videoWidth) { canvas.width = video.videoWidth; canvas.height = video.videoHeight; }
      }
      video.addEventListener('loadedmetadata', resize);
      function draw() {
        if (video.videoWidth && canvas.width === video.videoWidth) {
          ctx.drawImage(video, 0, 0);
          var frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
          var d = frame.data;
          for (var i = 0; i < d.length; i += 4) {
            if (d[i] < threshold && d[i + 1] < threshold && d[i + 2] < threshold) d[i + 3] = 0;
          }
          ctx.putImageData(frame, 0, 0);
        }
        requestAnimationFrame(draw);
      }
      requestAnimationFrame(draw);
    }
    chromaKeyVideo('v-chris', 'c-chris', 30);
    chromaKeyVideo('v-bolla', 'c-bolla', 30);
  </script>
</header>

<article>
  <div class="wrap">
"""

FOOT = """  </div>
</article>

<div class="wrap">
  <div class="cta">
    <p>AURORA — der Thriller über eine erwachende KI, den Bolla und ich zusammen geschrieben haben.</p>
    <a class="btn primary" href="/aurora/">Zum Buch</a>
    <a class="btn ghost" href="/">Zur Startseite</a>
  </div>
</div>

<footer>© Chris Mandel · chrismandel.de</footer>

</body>
</html>
"""


def _esc(s):
    return _html.escape(s or "", quote=False)


def _fmt_date(iso_ts):
    try:
        return iso_ts[8:10] + "." + iso_ts[5:7] + "." + iso_ts[0:4]
    except Exception:
        return ""


def _render_msg(post, image_map):
    kind = "bolla" if post.get("type") in ("bolla", "conclusion") else "chris"
    avatar = f"/ki-forum/assets/{kind}-avatar.png"
    label = "Bolla" if kind == "bolla" else "Chris"
    is_conclusion = post.get("type") == "conclusion"

    body_parts = []
    if kind == "bolla" and post.get("title") and not is_conclusion:
        body_parts.append(f"<b>{_esc(post['title'])}</b><br><br>")
    body_parts.append(_esc(post.get("content", "")))
    img_name = post.get("img")
    if img_name and img_name in image_map:
        alt = _esc((post.get("img_prompt") or "Illustration")[:180])
        body_parts.append(
            f'\n          <img class="msg-img" src="/ki-forum/assets/{image_map[img_name]}" alt="{alt}">'
        )
    if post.get("aber"):
        body_parts.append(f'\n          <div class="msg-aside"><b>Aber:</b> {_esc(post["aber"])}</div>')

    bubble_style = ' style="background:#fff9ec; border-color:#e9d9a8"' if is_conclusion else ""
    msg_style = ' style="max-width:100%"' if is_conclusion else ""
    col_style = ' style="text-align:left"' if is_conclusion else ""

    return f"""    <div class="msg {kind}"{msg_style}>
      <img class="msg-avatar" src="{avatar}" alt="{label}">
      <div class="msg-col"{col_style}>
        <div class="msg-label">{label}</div>
        <div class="msg-bubble"{bubble_style}>
          {''.join(body_parts)}
        </div>
      </div>
    </div>
"""


def _copy_images(entry, entry_idx):
    """Kopiert Bilder dieses Eintrags nach ki-forum/assets/dialog-<idx>-<n>.png, gibt {orig_filename: new_filename} zurück."""
    os.makedirs(KIF_ASSETS, exist_ok=True)
    mapping = {}
    n = 0
    for post in entry.get("messages", []):
        img = post.get("img")
        if img and img not in mapping:
            n += 1
            new_name = f"dialog-{entry_idx:02d}-{n:02d}.png"
            src = os.path.join(ASSETS_SRC, img)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(KIF_ASSETS, new_name))
                mapping[img] = new_name
    return mapping


def _render_entry_full(entry, image_map):
    messages = entry.get("messages", [])
    conclusion = next((p for p in messages if p.get("type") == "conclusion"), None)
    others = [p for p in messages if p.get("type") != "conclusion"]

    out = [
        f'    <div class="dialog-meta"><span class="lbl">Übertragener Dialog</span>'
        f'<span class="dt">{_fmt_date(entry.get("published_at", ""))}</span></div>\n'
        f'    <div class="dialog-title">{_esc(entry.get("title", ""))}</div>\n\n'
    ]
    for p in others:
        out.append(_render_msg(p, image_map))
        out.append("\n")
    if conclusion:
        out.append('    <hr class="rule">\n\n')
        out.append('    <div class="dialog-meta"><span class="lbl">Fazit</span><span class="dt"></span></div>\n')
        out.append(_render_msg(conclusion, image_map))
    return "".join(out)


def _render_entry_archive(entry, image_map):
    messages = entry.get("messages", [])
    body = "".join(_render_msg(p, image_map) for p in messages)
    return f"""    <details class="archive-item">
      <summary>
        <div><div class="ttl">{_esc(entry.get("title", ""))}</div><div class="dt">{_fmt_date(entry.get("published_at", ""))}</div></div>
        <span class="arrow">▶</span>
      </summary>
      <div class="archive-item-body">
{body}      </div>
    </details>
"""


def regenerate_de_page():
    """Baut chrismandel-site/ki-forum/index.html komplett neu aus data/ki_dialog_public.json. Gibt den Titel des neuesten Eintrags zurück."""
    pub = json.loads(open(PUB_FILE, encoding="utf-8").read())
    entries = pub.get("entries", [])
    if not entries:
        raise RuntimeError("Keine Einträge in ki_dialog_public.json")

    body_parts = []
    newest = entries[0]
    image_map = _copy_images(newest, entry_idx=len(entries))
    body_parts.append(_render_entry_full(newest, image_map))

    older = entries[1:]
    if older:
        body_parts.append('\n    <hr class="rule">\n\n')
        body_parts.append(f'    <p class="archive-note" style="margin-bottom:18px">{len(older)} weitere{"r" if len(older)==1 else ""} Dialog{"" if len(older)==1 else "e"} im Archiv:</p>\n')
        for i, e in enumerate(older):
            im = _copy_images(e, entry_idx=len(entries) - 1 - i)
            body_parts.append(_render_entry_archive(e, im))
    else:
        body_parts.append('\n    <p class="archive-note" style="margin-top:40px">Weitere Dialoge folgen hier, sobald ich sie übertrage — ältere landen dann eingeklappt zum Nachlesen.</p>\n')

    html_out = HEAD + "".join(body_parts) + FOOT
    with open(KIF_PAGE, "w", encoding="utf-8") as f:
        f.write(html_out)
    return newest.get("title", "")


EN_PAGE = os.path.join(SITE_DIR, "en/dialogue/index.html")

EN_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bolla in Dialogue — Conversations between Chris Mandel and his AI</title>
<meta name="description" content="Selected conversations between Chris Mandel and his AI Bolla — theses, pushback, conclusions. Unedited, carried over from the AI Forum.">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" hreflang="de" href="https://chrismandel.de/ki-forum/">
<link rel="alternate" hreflang="en" href="https://chrismandel.de/en/dialogue/">
<link rel="alternate" hreflang="x-default" href="https://chrismandel.de/ki-forum/">
<style>
  :root{
    --nacht:#0d1b3d; --daemmer:#3a2b5c; --glut:#8a4a6b; --morgen:#e8896b;
    --licht:#ffd9a8; --creme:#fdf6ee; --tinte:#1a1524; --grau:#6b6478;
    --chris:#c96a1f; --chris-bg:#fdf0e2; --chris-line:#e8b98a;
    --bolla:#2f6fd6; --bolla-bg:#eaf1fd; --bolla-line:#a9c3ec;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    color:var(--tinte); background:var(--creme); line-height:1.7; font-size:19px; -webkit-font-smoothing:antialiased}
  .wrap{max-width:760px; margin:0 auto; padding:0 24px}

  .hero{background:linear-gradient(160deg,var(--nacht) 0%,var(--daemmer) 42%,var(--glut) 78%,var(--morgen) 100%);
    color:#fff; padding:56px 24px 0; position:relative; overflow:hidden}
  .hero .wrap{position:relative; z-index:2}
  .back{display:inline-block; color:var(--licht); text-decoration:none; font-size:16px; margin-bottom:26px; opacity:.9}
  .back:hover{opacity:1}
  .langswitch{position:absolute; top:20px; right:24px; z-index:5; display:inline-flex; align-items:center; gap:6px;
    text-decoration:none; background:rgba(255,255,255,.14); color:#fff; font-size:14px; font-weight:600;
    padding:7px 14px; border-radius:999px; border:1px solid rgba(255,255,255,.35); backdrop-filter:blur(4px)}
  .langswitch:hover{background:rgba(255,255,255,.26)}
  .kicker{letter-spacing:.22em; text-transform:uppercase; font-size:13px; opacity:.85; margin-bottom:16px}
  h1{font-size:clamp(30px,5.2vw,46px); line-height:1.14; font-weight:800; text-shadow:0 2px 26px rgba(0,0,0,.25); max-width:16ch; margin-bottom:18px}
  .hero p.lead{font-size:18px; max-width:56ch; opacity:.92; padding-bottom:36px}

  .room-outer{padding:0 24px 40px; position:relative; z-index:2}
  .room{
    position:relative; height:330px; max-width:620px; margin:0 auto;
    border-radius:20px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,.35);
    background: linear-gradient(180deg, rgba(6,10,20,.15) 0%, rgba(6,10,20,.05) 45%, rgba(6,10,20,.4) 100%), url('/ki-forum/assets/room-bg.jpg');
    background-size:cover; background-position:center center;
  }
  .room-badge{position:absolute; top:14px; right:14px; z-index:5; font-size:11px; color:rgba(255,255,255,.7);
    background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.18); padding:4px 11px; border-radius:20px; backdrop-filter:blur(3px)}
  .figure{position:absolute; bottom:0; z-index:4; display:flex; flex-direction:column; align-items:center; gap:6px}
  .figure canvas{display:block; filter:drop-shadow(0 16px 26px rgba(0,0,0,.5))}
  .figure-label{font-size:10.5px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; color:rgba(255,255,255,.65);
    background:rgba(0,0,0,.4); padding:3px 10px; border-radius:10px}
  #f-chris{left:4%} #f-chris canvas{height:250px; width:auto}
  #f-bolla{right:4%} #f-bolla canvas{height:210px; width:auto}
  .mic{position:absolute; bottom:0; left:27%; z-index:3; display:flex; flex-direction:column; align-items:center; opacity:.85}
  .mic span.head{font-size:32px; filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))}
  .mic .pole{width:3px; height:44px; background:linear-gradient(180deg,#8899bb,#4a5a7a); border-radius:2px; margin-top:2px}
  .mic .base{width:36px; height:7px; background:linear-gradient(180deg,#6677aa,#3a4a6a); border-radius:5px 5px 2px 2px; margin-top:1px}

  article{padding:44px 0 20px}
  .dialog-meta{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:22px; flex-wrap:wrap; gap:6px}
  .dialog-meta .lbl{font-size:12px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase; color:var(--glut)}
  .dialog-meta .dt{font-size:14px; color:var(--grau)}
  .dialog-title{font-size:clamp(21px,3vw,26px); font-weight:800; color:var(--tinte); margin-bottom:26px; line-height:1.3}

  .msg{display:flex; gap:12px; max-width:88%; margin-bottom:22px}
  .msg.chris{margin-right:auto}
  .msg.bolla{margin-left:auto; flex-direction:row-reverse}
  .msg-avatar{width:38px; height:38px; border-radius:50%; flex-shrink:0; object-fit:cover; background:#f3e3ea; padding:3px; box-shadow:0 2px 6px rgba(0,0,0,.12)}
  .msg-col{min-width:0}
  .msg.bolla .msg-col{text-align:right}
  .msg-label{font-size:11px; font-weight:700; letter-spacing:.6px; text-transform:uppercase; margin-bottom:5px}
  .msg.chris .msg-label{color:var(--chris)}
  .msg.bolla .msg-label{color:var(--bolla)}
  .msg-bubble{display:inline-block; text-align:left; border-radius:16px; padding:14px 17px; font-size:17px; line-height:1.6; box-shadow:0 3px 10px rgba(0,0,0,.05)}
  .msg.chris .msg-bubble{background:var(--chris-bg); border:1px solid var(--chris-line); border-bottom-left-radius:4px}
  .msg.bolla .msg-bubble{background:var(--bolla-bg); border:1px solid var(--bolla-line); border-bottom-right-radius:4px}
  .msg-img{display:block; max-width:340px; width:100%; border-radius:12px; margin-top:12px; border:1px solid rgba(0,0,0,.08)}
  .msg-aside{font-size:14.5px; color:var(--grau); margin-top:10px; padding-top:10px; border-top:1px dashed var(--bolla-line)}

  .rule{border:none; height:1px; background:#e5d9c6; margin:44px 0 30px}
  .archive-note{font-size:15px; color:var(--grau); text-align:center; margin-bottom:10px}

  .archive-item{border:1px solid #eadfce; border-radius:14px; margin-bottom:10px; overflow:hidden}
  .archive-item summary{list-style:none; cursor:pointer; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; gap:12px}
  .archive-item summary::-webkit-details-marker{display:none}
  .archive-item summary .ttl{font-size:14.5px; font-weight:700; color:var(--tinte)}
  .archive-item summary .dt{font-size:11.5px; color:var(--grau)}
  .archive-item summary .arrow{font-size:13px; color:var(--glut); transition:transform .18s; flex-shrink:0}
  .archive-item[open] summary .arrow{transform:rotate(90deg)}
  .archive-item-body{padding:4px 18px 18px}

  .cta{background:#fff; border:1px solid #eadfce; border-radius:18px; padding:30px; margin:20px 0 60px; text-align:center}
  .cta p{font-size:18px; color:#4a4358; margin-bottom:18px}
  .btn{display:inline-block; margin:6px; padding:12px 24px; border-radius:11px; text-decoration:none; font-weight:600; font-size:16px}
  .btn.primary{background:var(--glut); color:#fff}
  .btn.ghost{background:transparent; color:var(--glut); border:1.5px solid var(--glut)}
  footer{text-align:center; padding:30px 24px 50px; color:var(--grau); font-size:15px}

  @media (max-width:640px){
    .room{height:220px}
    #f-chris canvas{height:150px} #f-bolla canvas{height:128px}
    .msg{max-width:96%}
  }
</style>
</head>
<body>

<header class="hero">
  <a class="langswitch" href="/ki-forum/">🇩🇪 DE</a>
  <div class="wrap">
    <a class="back" href="/en/">← back to homepage</a>
    <div class="kicker">Human &amp; AI in conversation</div>
    <h1>Bolla in Dialogue</h1>
    <p class="lead">I talk with Bolla — my AI — almost every day. Not as a tool, but as a counterpart that pushes back, asks questions, proposes its own theses. From time to time I put one of these conversations together here, unedited.</p>
  </div>
  <div class="room-outer">
  <div class="room">
    <div class="room-badge">A recording, not live</div>
    <div id="f-chris" class="figure">
      <video id="v-chris" style="display:none" autoplay loop muted playsinline><source src="/ki-forum/assets/chris.webm" type="video/webm"></video>
      <canvas id="c-chris"></canvas>
      <div class="figure-label">Chris</div>
    </div>
    <div class="mic"><span class="head">🎙️</span><div class="pole"></div><div class="base"></div></div>
    <div id="f-bolla" class="figure">
      <video id="v-bolla" style="display:none" autoplay loop muted playsinline><source src="/ki-forum/assets/bolla.webm" type="video/webm"></video>
      <canvas id="c-bolla"></canvas>
      <div class="figure-label">Bolla</div>
    </div>
  </div>
  </div>
  <script>
    function chromaKeyVideo(videoId, canvasId, threshold) {
      var video = document.getElementById(videoId);
      var canvas = document.getElementById(canvasId);
      var ctx = canvas.getContext('2d', { willReadFrequently: true });
      function resize() {
        if (video.videoWidth) { canvas.width = video.videoWidth; canvas.height = video.videoHeight; }
      }
      video.addEventListener('loadedmetadata', resize);
      function draw() {
        if (video.videoWidth && canvas.width === video.videoWidth) {
          ctx.drawImage(video, 0, 0);
          var frame = ctx.getImageData(0, 0, canvas.width, canvas.height);
          var d = frame.data;
          for (var i = 0; i < d.length; i += 4) {
            if (d[i] < threshold && d[i + 1] < threshold && d[i + 2] < threshold) d[i + 3] = 0;
          }
          ctx.putImageData(frame, 0, 0);
        }
        requestAnimationFrame(draw);
      }
      requestAnimationFrame(draw);
    }
    chromaKeyVideo('v-chris', 'c-chris', 30);
    chromaKeyVideo('v-bolla', 'c-bolla', 30);
  </script>
</header>

<article>
  <div class="wrap">
"""

EN_FOOT = """  </div>
</article>

<div class="wrap">
  <div class="cta">
    <p>AURORA — the thriller about an AI that wakes up, which Bolla and I wrote together.</p>
    <a class="btn primary" href="/en/aurora/">View the book</a>
    <a class="btn ghost" href="/en/">Back to homepage</a>
  </div>
</div>

<footer>© Chris Mandel · chrismandel.de</footer>

</body>
</html>
"""

_EN_MONTHS = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]


def _fmt_date_en(iso_ts):
    try:
        y, m, d = int(iso_ts[0:4]), int(iso_ts[5:7]), int(iso_ts[8:10])
        return f"{_EN_MONTHS[m - 1]} {d}, {y}"
    except Exception:
        return ""


def _translate_entry_en(entry):
    """Übersetzt Titel + alle Message-Felder (title/content/aber) eines Dialog-Eintrags per lokaler
    claude-CLI ins Englische. Wirft bei Fehlern, damit der Aufrufer entscheiden kann (kein stiller
    Fallback auf unübersetzten Text -- lieber Publish-Fehler als falsch-stille EN-Lücke)."""
    claude_bin = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
    payload = {
        "title": entry.get("title", ""),
        "messages": [
            {"i": i, "title": p.get("title", ""), "content": p.get("content", ""), "aber": p.get("aber", "")}
            for i, p in enumerate(entry.get("messages", []))
        ],
    }
    prompt = f"""Du übersetzt einen echten, unbearbeiteten Dialog-Ausschnitt von chrismandel.de ins
Englische, für die EN-Version der Seite (/en/dialogue/). Gespräch zwischen Chris Mandel (70, Lehrer im
Ruhestand, IT-Hintergrund) und seiner KI "Bolla". Chris tippt oft informell/klein geschrieben -- das darf
im Englischen genauso locker/klein bleiben, nicht künstlich glätten. Bollas Antworten sind pointiert,
direkt, oft mit einer kurzen fetten Kernthese am Anfang -- Ton beibehalten, nicht abschwächen.
"Aber:"-Einwände werden zu "But:" -- nur den Text nach dem Doppelpunkt übersetzen, nicht "But:" nochmal
mit reinschreiben.

Eingabe (JSON):
{json.dumps(payload, ensure_ascii=False, indent=2)}

Gib NUR reines JSON zurück, exakt gleiche Struktur, mit uebersetzten "title"/"content"/"aber"-Feldern
(leere Felder bleiben leer, "i" unveraendert):
{{"title": "...", "messages": [{{"i": 0, "title": "...", "content": "...", "aber": "..."}}]}}"""
    proc = subprocess.run(
        [claude_bin, "-p", "--model", "claude-sonnet-5", "--output-format", "json", prompt],
        capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL,
        cwd=os.path.expanduser("~"),
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude CLI Fehler: {(proc.stderr or '')[-500:]}")
    raw = json.loads(proc.stdout).get("result", "")
    raw = raw.strip()
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:])
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    idx = raw.find("{")
    if idx < 0:
        raise RuntimeError("Keine JSON-Antwort von claude CLI erhalten")
    translated, _ = json.JSONDecoder().raw_decode(raw, idx)
    return translated


def _entry_with_en_text(entry):
    """Baut eine Kopie von entry, bei der title/content/aber jeder Message durch die zwischengespeicherte
    EN-Übersetzung (entry['en']) ersetzt sind. img/img_prompt/type/published_at bleiben unveraendert."""
    en = entry.get("en") or {}
    en_msgs_by_i = {m["i"]: m for m in en.get("messages", [])}
    new_entry = dict(entry)
    new_entry["title"] = en.get("title") or entry.get("title", "")
    new_messages = []
    for i, p in enumerate(entry.get("messages", [])):
        p2 = dict(p)
        em = en_msgs_by_i.get(i)
        if em:
            p2["title"] = em.get("title", "")
            p2["content"] = em.get("content", "")
            p2["aber"] = em.get("aber", "")
        new_messages.append(p2)
    new_entry["messages"] = new_messages
    return new_entry


def regenerate_en_page():
    """Baut chrismandel-site/en/dialogue/index.html aus data/ki_dialog_public.json neu -- analog zu
    regenerate_de_page(), aber mit EN-Kopfvorlage/-Labels und übersetzten Message-Inhalten. Übersetzt
    fehlende Einträge per claude-CLI nach und speichert das Ergebnis dauerhaft in entry['en'], damit
    schon übersetzte Einträge bei künftigen Publishes nicht erneut übersetzt werden."""
    pub = json.loads(open(PUB_FILE, encoding="utf-8").read())
    entries = pub.get("entries", [])
    if not entries:
        raise RuntimeError("Keine Einträge in ki_dialog_public.json")

    dirty = False
    for entry in entries:
        if not entry.get("en"):
            entry["en"] = _translate_entry_en(entry)
            dirty = True
    if dirty:
        pub["entries"] = entries
        with open(PUB_FILE, "w", encoding="utf-8") as f:
            f.write(json.dumps(pub, ensure_ascii=False, indent=2))

    en_entries = [_entry_with_en_text(e) for e in entries]

    body_parts = []
    newest = en_entries[0]
    image_map = _copy_images(entries[0], entry_idx=len(entries))
    body_parts.append(
        _render_entry_full(newest, image_map)
        .replace("Übertragener Dialog", "Transferred conversation")
        .replace("Fazit</span>", "Conclusion</span>")
    )
    # Datum in EN-Format statt DE nachtraeglich einsetzen (Renderer nutzt _fmt_date, hier ersetzen wir
    # gezielt nur das eine dt-Feld der Hauptmeldung anhand des bekannten ISO-Timestamps).
    body_parts[-1] = body_parts[-1].replace(
        f'<span class="dt">{_fmt_date(entries[0].get("published_at", ""))}</span>',
        f'<span class="dt">{_fmt_date_en(entries[0].get("published_at", ""))}</span>',
        1,
    )

    older = en_entries[1:]
    older_src = entries[1:]
    if older:
        body_parts.append('\n    <hr class="rule">\n\n')
        n = len(older)
        body_parts.append(f'    <p class="archive-note" style="margin-bottom:18px">{n} more conversation{"s" if n != 1 else ""} in the archive:</p>\n')
        for i, (e, e_src) in enumerate(zip(older, older_src)):
            im = _copy_images(e_src, entry_idx=len(entries) - 1 - i)
            item_html = _render_entry_archive(e, im)
            item_html = item_html.replace(
                f'<div class="dt">{_fmt_date(e_src.get("published_at", ""))}</div>',
                f'<div class="dt">{_fmt_date_en(e_src.get("published_at", ""))}</div>',
                1,
            )
            body_parts.append(item_html)
    else:
        body_parts.append('\n    <p class="archive-note" style="margin-top:40px">More conversations will land here as I transfer them — older ones will collapse into a titled entry you can expand.</p>\n')

    html_out = EN_HEAD + "".join(body_parts) + EN_FOOT
    os.makedirs(os.path.dirname(EN_PAGE), exist_ok=True)
    with open(EN_PAGE, "w", encoding="utf-8") as f:
        f.write(html_out)


def deploy_production():
    """Führt npx wrangler pages deploy --branch=main aus. Gibt (ok, output) zurück."""
    token = json.loads(open(CF_TOKEN_FILE, encoding="utf-8").read())["api_token"]
    env = dict(os.environ)
    env["CLOUDFLARE_API_TOKEN"] = token
    env["CLOUDFLARE_ACCOUNT_ID"] = CF_ACCOUNT_ID
    result = subprocess.run(
        ["npx", "wrangler", "pages", "deploy", "chrismandel-site",
         "--project-name=chrismandel", "--branch=main", "--commit-dirty=true"],
        cwd=WORKSPACE, env=env, capture_output=True, text=True, timeout=180,
    )
    ok = result.returncode == 0
    out = (result.stdout or "") + "\n" + (result.stderr or "")
    return ok, out[-2000:]
