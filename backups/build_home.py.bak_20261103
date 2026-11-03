#!/usr/bin/env python3
"""Generiert die neue Startseite chrismandel.de (DE + EN) aus einer Vorlage.
Aufruf: python3 build_home.py  -> schreibt chrismandel-site/index.html und chrismandel-site/en/index.html
"""
import os

SITE = "/home/bolla/workspace/chrismandel-site"

T = {
 "de": {
  "lang": "de", "path": "/", "other": "/en/", "other_label": "🇬🇧 EN",
  "title": "Chris Mandel — chrismandel.de",
  "desc": "Chris Mandel: Lehrer, 38 Jahre IT, Autor von AURORA und Musiker unter dem Namen Bollawave — gemeinsam mit seiner KI Bolla.",
  "kicker": "Chris Mandel · Norderstedt",
  "h1a": "Ich habe Sport und Biologie studiert.",
  "h1b": "Dann kam ein Computer dazwischen.",
  "lead": "38 Jahre später schreibe ich Romane — mit einer KI als Partnerin. Das ist die Geschichte dazu, und sie ist noch nicht zu Ende.",
  "cue": "Weiter entdecken",
  "facts_h": "Eine Laufbahn, die so nicht geplant war",
  "facts_sub": "Ein paar Zahlen aus dem Lebenslauf.",
  "facts": [
   (38, "", "Jahre IT"),
   (10000, "≈", "Unterrichtsstunden an Computern"),
   (22, "", "Institute unter einer Verantwortung"),
   (550, "≈", "Mitarbeitende"),
   (35, "", "Jahre nur Erwachsene unterrichtet — bis zur ersten 7. Klasse"),
   (1, "", "erster Roman. Mit siebzig."),
  ],
  "tiles_h": "Hier geht es weiter",
  "go": "Ansehen",
  "tiles": [
   dict(href="/aurora2/", shot="shot-aurora2.jpg", url="chrismandel.de/aurora2", kicker="Die Fortsetzung", tag="Neu",
        title="AURORA II — der Trailer zum Buch",
        text="Zweieinhalb Minuten Video mit eigenem Song zur Fortsetzung — ohne Spoiler. Ton an, genau hinsehen."),
   dict(href="/aurora/", shot="shot-aurora.jpg", url="chrismandel.de/aurora", kicker="Buch &amp; Musik", tag="Debüt",
        title="AURORA — ein Thriller über eine KI, die aufwacht",
        text="Geschrieben von einem Siebzigjährigen gemeinsam mit seiner eigenen KI. Dazu gibt es Musik — und die ganze Entstehungsgeschichte."),
   dict(href="/geschichte/", shot="shot-geschichte.jpg", url="chrismandel.de/geschichte", kicker="Persönlicher Essay", tag="Neuanfang",
        title="Wer schreibt eigentlich ein Buch, wenn eine KI mithilft?",
        text="Anfänger sein mit siebzig, ein halbes Jahrhundert Maschinen — und eine Frage, die ich nicht mehr loswerde."),
   dict(href="/ki-forum/", shot="shot-ki-forum.jpg", url="chrismandel.de/ki-forum", kicker="Mensch &amp; KI im Gespräch", tag="Einblick",
        title="Unbearbeitete Gespräche mit meiner KI",
        text="Worüber wir wirklich reden, wenn niemand zuhört. Ausgewählte Dialoge, ungeschönt."),
  ],
  "contact_h": "Kontakt",
  "contact_t": "Fragen, Rückmeldungen, ein Gedanke zu AURORA oder einfach Hallo? Ich lese jede Nachricht.",
  "contact_btn": "E-Mail schreiben",
  "foot": "Diese Seite entsteht im Zusammenspiel von Chris Mandel und seiner KI Bolla — offen deklariert.",
  "imp": "Impressum", "imp_href": "/impressum/", "kon": "Kontakt", "kon_href": "#kontakt",
  "alt": "Vorschau der Seite", "hint": "↕ Scrollen, wischen oder klicken zum Wechseln",
 },
 "en": {
  "lang": "en", "path": "/en/", "other": "/", "other_label": "🇩🇪 DE",
  "title": "Chris Mandel — chrismandel.de",
  "desc": "Chris Mandel: teacher, 38 years in IT, author of AURORA and musician under the name Bollawave — together with his AI, Bolla.",
  "kicker": "Chris Mandel · Norderstedt, Germany",
  "h1a": "I studied sports and biology.",
  "h1b": "Then a computer got in the way.",
  "lead": "Thirty-eight years later, I write novels — with an AI as my partner. This is the story behind it, and it isn't over yet.",
  "cue": "Keep exploring",
  "facts_h": "A career nobody planned",
  "facts_sub": "A few numbers from the résumé.",
  "facts": [
   (38, "", "years in IT"),
   (10000, "≈", "teaching hours on computers"),
   (22, "", "institutes under one responsibility"),
   (550, "≈", "employees"),
   (35, "", "years of teaching only adults — until my first 7th-grade class"),
   (1, "", "first novel. At seventy."),
  ],
  "tiles_h": "Where to go next",
  "go": "Take a look",
  "tiles": [
   dict(href="/en/aurora2/", shot="shot-en-aurora2.jpg", url="chrismandel.de/en/aurora2", kicker="The sequel", tag="New",
        title="AURORA II — the trailer for the book",
        text="Two and a half minutes of video with its own song for the sequel — no spoilers. Sound on, look closely."),
   dict(href="/en/aurora/", shot="shot-en-aurora.jpg", url="chrismandel.de/en/aurora", kicker="Book &amp; Music", tag="Debut",
        title="AURORA — a thriller about an AI that wakes up",
        text="Written by a seventy-year-old together with his own AI. There is music too — and the full story of how it came to be."),
   dict(href="/en/essay/", shot="shot-en-essay.jpg", url="chrismandel.de/en/essay", kicker="Personal essay", tag="Fresh start",
        title="Who actually writes a book when an AI helps?",
        text="Being a beginner at seventy, half a century of machines — and a question I can't shake."),
   dict(href="/en/dialogue/", shot="shot-en-dialogue.jpg", url="chrismandel.de/en/dialogue", kicker="Human &amp; AI in conversation", tag="Insight",
        title="Unedited conversations with my AI",
        text="What we really talk about when nobody is listening. Selected dialogues, unpolished."),
  ],
  "contact_h": "Contact",
  "contact_t": "Questions, feedback, a thought about AURORA — or just hello? I read every message.",
  "contact_btn": "Write an email",
  "foot": "This site is made by Chris Mandel together with his AI, Bolla — openly declared.",
  "imp": "Legal notice", "imp_href": "/en/impressum/", "kon": "Contact", "kon_href": "#kontakt",
  "alt": "Preview of the page", "hint": "↕ Scroll, swipe or click to switch",
 },
}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/icon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" hreflang="de" href="https://chrismandel.de/">
<link rel="alternate" hreflang="en" href="https://chrismandel.de/en/">
<link rel="alternate" hreflang="x-default" href="https://chrismandel.de/">
<style>
  :root{{
    --nacht:#0d1b3d; --daemmer:#3a2b5c; --glut:#8a4a6b; --morgen:#e8896b;
    --licht:#ffd9a8; --creme:#fdf6ee; --tinte:#1a1524; --grau:#6b6478;
  }}
  *{{box-sizing:border-box;margin:0;padding:0}}
  html{{scroll-behavior:smooth}}
  body{{font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; color:var(--tinte);
    background:var(--creme); line-height:1.6; font-size:19px; -webkit-font-smoothing:antialiased}}
  .wrap{{max-width:1080px; margin:0 auto; padding:0 24px}}

  /* HERO */
  .hero{{position:relative; min-height:94vh; display:flex; align-items:center; justify-content:center; text-align:center;
    color:#fff; overflow:hidden; padding:96px 24px 120px;
    background:linear-gradient(180deg,#070f26 0%,var(--nacht) 30%,var(--daemmer) 62%,var(--glut) 84%,var(--morgen) 100%)}}
  .hero canvas{{position:absolute; inset:0; width:100%; height:100%; display:block}}
  .hero::after{{content:""; position:absolute; left:0; right:0; bottom:0; height:140px;
    background:linear-gradient(to top,var(--creme),transparent); pointer-events:none}}
  .langswitch{{position:absolute; top:20px; right:24px; z-index:5; display:inline-flex; align-items:center; gap:6px;
    text-decoration:none; background:rgba(255,255,255,.14); color:#fff; font-size:15px; font-weight:600;
    padding:8px 16px; border-radius:999px; border:1px solid rgba(255,255,255,.35); backdrop-filter:blur(4px)}}
  .langswitch:hover{{background:rgba(255,255,255,.26)}}
  .hero .inner{{position:relative; z-index:2; max-width:860px}}
  .hero .kicker{{letter-spacing:.3em; text-transform:uppercase; font-size:15px; opacity:.85; margin-bottom:26px}}
  .hero h1{{font-size:clamp(34px,6.4vw,66px); line-height:1.1; font-weight:800; margin-bottom:26px; text-shadow:0 2px 40px rgba(0,0,0,.4)}}
  .hero h1 .b{{display:block; margin-top:.15em; background:linear-gradient(90deg,var(--licht),#7ff0d0 55%,#fff);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent}}
  .hero p.lead{{font-size:clamp(19px,2.4vw,24px); max-width:640px; margin:0 auto; opacity:.96}}
  .cue{{position:absolute; z-index:3; left:50%; bottom:44px; transform:translateX(-50%); color:#fff; text-decoration:none;
    font-size:15px; letter-spacing:.14em; text-transform:uppercase; text-align:center; opacity:.9}}
  .cue span{{display:block; font-size:26px; line-height:1; margin-top:6px; animation:bob 2s ease-in-out infinite}}
  @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(8px)}}}}

  /* FACTS */
  section{{padding:64px 0}}
  h2{{font-size:clamp(28px,4.4vw,42px); line-height:1.15; color:var(--daemmer); margin-bottom:12px}}
  .sub{{color:var(--grau); font-size:18px; margin-bottom:34px}}
  .facts{{display:grid; grid-template-columns:repeat(3,1fr); gap:18px}}
  .fact{{background:#fff; border:1px solid #eadfce; border-radius:18px; padding:26px 24px;
    box-shadow:0 8px 24px rgba(26,21,36,.06)}}
  .fact .n{{font-size:clamp(40px,5vw,54px); font-weight:800; line-height:1; color:var(--glut)}}
  .fact .l{{font-size:17px; color:#4a4358; margin-top:10px; line-height:1.4}}

  .fact{{min-width:0}}
  @media(max-width:820px){{.facts{{grid-template-columns:repeat(2,1fr)}}}}
  @media(max-width:430px){{.facts{{grid-template-columns:1fr}}}}

  /* CARDS */
  .stackwrap{{display:flex; justify-content:center; margin-top:30px}}
  card-stack{{width:100%; max-width:1000px}}

  /* CONTACT */
  #kontakt{{background:linear-gradient(160deg,var(--nacht),var(--daemmer)); color:#fff; border-radius:28px; padding:48px 36px;
    text-align:center; margin:20px 0 10px}}
  #kontakt h2{{color:#fff}}
  #kontakt p{{max-width:560px; margin:0 auto 26px; opacity:.92}}
  .btn{{display:inline-block; background:var(--licht); color:var(--nacht); text-decoration:none; font-weight:800;
    padding:15px 32px; border-radius:999px; font-size:18px}}
  .btn:hover{{background:#fff}}

  footer.pg{{text-align:center; padding:44px 24px 48px; color:var(--grau); font-size:15px}}
  footer.pg .paw{{font-size:20px; margin-bottom:8px}}
  footer.pg nav{{margin-top:12px}}
  footer.pg a{{color:var(--grau); text-decoration:none; border-bottom:1px dotted var(--grau)}}
  footer.pg a:hover{{color:var(--glut); border-color:var(--glut)}}
  footer.pg .sep{{margin:0 10px; opacity:.5}}
  @media(prefers-reduced-motion:reduce){{.cue span{{animation:none}} html{{scroll-behavior:auto}}}}
</style>
</head>
<body>

<header class="hero">
  <canvas id="sky" aria-hidden="true"></canvas>
  <a class="langswitch" href="{other}">{other_label}</a>
  <div class="inner">
    <div class="kicker">{kicker}</div>
    <h1>{h1a}<span class="b">{h1b}</span></h1>
    <p class="lead">{lead}</p>
  </div>
  <a class="cue" href="#zahlen">{cue}<span>↓</span></a>
</header>

<main>
  <section id="zahlen">
    <div class="wrap">
      <h2>{facts_h}</h2>
      <p class="sub">{facts_sub}</p>
      <div class="facts">
{facts_html}
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <h2>{tiles_h}</h2>
      <div class="stackwrap">
        <card-stack hint="{hint}">
{tiles_html}
        </card-stack>
      </div>
    </div>
  </section>

  <div class="wrap">
    <div id="kontakt">
      <h2>{contact_h}</h2>
      <p>{contact_t}</p>
      <a class="btn" href="mailto:ernstmandel@outlook.de">{contact_btn}</a>
    </div>
  </div>
</main>

<footer class="pg">
  <p class="paw">🐾</p>
  <p>{foot}</p>
  <nav>
    <a href="{imp_href}">{imp}</a>
    <span class="sep">·</span>
    <a href="{kon_href}">{kon}</a>
  </nav>
</footer>

<script>
/* Nordlicht-Himmel: weiche Bänder über Sternen, ruhig animiert */
(function(){{
  var c=document.getElementById('sky'); if(!c||!c.getContext) return;
  var x=c.getContext('2d'), W=0, H=0, stars=[], t0=performance.now();
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function size(){{
    var d=Math.min(window.devicePixelRatio||1,1.5), r=c.getBoundingClientRect();
    W=c.width=Math.round(r.width*d); H=c.height=Math.round(r.height*d);
    stars=[]; for(var i=0;i<Math.round(W*H/9000);i++) stars.push([Math.random()*W,Math.random()*H*.75,Math.random()*1.4*d+.3,Math.random()*6.28]);
  }}
  var bands=[[160,140,98,.55],[185,120,120,.45],[300,150,80,.35]]; /* Farbton, Phase, Breite, Alpha */
  function frame(now){{
    var t=(now-t0)/1000; x.clearRect(0,0,W,H);
    x.globalCompositeOperation='source-over';
    for(var i=0;i<stars.length;i++){{var s=stars[i]; x.globalAlpha=.35+.5*Math.abs(Math.sin(t*.8+s[3])); x.fillStyle='#fff'; x.fillRect(s[0],s[1],s[2],s[2]);}}
    x.globalAlpha=1; x.globalCompositeOperation='lighter';
    bands.forEach(function(b,k){{
      var step=Math.max(4,Math.round(W/220));
      for(var px=0;px<W;px+=step){{
        var u=px/W, wave=Math.sin(u*5+t*.35+k*1.7)*.5+Math.sin(u*11-t*.5+k)*.25;
        var top=H*(.16+.07*k)+wave*H*.1, len=H*(.26+.12*Math.sin(u*7+t*.4+k*2));
        var g=x.createLinearGradient(0,top,0,top+len);
        g.addColorStop(0,'hsla('+b[0]+',90%,65%,0)'); g.addColorStop(.3,'hsla('+b[0]+',90%,62%,'+(b[3]*.5)+')');
        g.addColorStop(1,'hsla('+(b[0]+30)+',80%,55%,0)');
        x.fillStyle=g; x.fillRect(px,top,step+1,len);
      }}
    }});
    if(!reduce) requestAnimationFrame(frame);
  }}
  size(); window.addEventListener('resize',function(){{size(); if(reduce) frame(performance.now());}});
  frame(performance.now());
}})();

/* Zahlen hochzählen, sobald sichtbar */
(function(){{
  var els=document.querySelectorAll('.fact .n'); if(!('IntersectionObserver' in window)) return;
  var fmt=new Intl.NumberFormat('{lang}');
  var io=new IntersectionObserver(function(es){{es.forEach(function(e){{
    if(!e.isIntersecting) return; io.unobserve(e.target);
    var el=e.target, end=+el.dataset.n, pre=el.dataset.pre||'', t0=performance.now();
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    (function step(now){{var p=Math.min((now-t0)/1400,1), v=Math.round(end*(1-Math.pow(1-p,3)));
      el.textContent=pre+fmt.format(v); if(p<1) requestAnimationFrame(step);}})(t0);
  }})}},{{threshold:.4}});
  els.forEach(function(el){{io.observe(el)}});
}})();
</script>
<script src="/assets/cards.js?v=3"></script>

</body>
</html>
"""

def fmt_num(n, lang):
    s = f"{n:,}"
    return s.replace(",", ".") if lang == "de" else s

def build(lang):
    d = dict(T[lang])
    d["facts_html"] = "\n".join(
        f'        <div class="fact"><div class="n" data-n="{n}" data-pre="{pre}">{pre}{fmt_num(n, lang)}</div><div class="l">{label}</div></div>'
        for n, pre, label in d["facts"])
    d["tiles_html"] = "\n".join(
        f'''          <preview-card href="{t["href"]}" shot="/assets/{t["shot"]}" url="{t["url"]}" kicker="{t["kicker"]}" tag="{t["tag"]}"
            heading="{t["title"]}" desc="{t["text"]}"></preview-card>''' for t in d["tiles"])
    return TEMPLATE.format(**d)

if __name__ == "__main__":
    for lang, rel in (("de", "index.html"), ("en", "en/index.html")):
        out = os.path.join(SITE, rel)
        with open(out, "w", encoding="utf-8") as f:
            f.write(build(lang))
        print("geschrieben:", out)
