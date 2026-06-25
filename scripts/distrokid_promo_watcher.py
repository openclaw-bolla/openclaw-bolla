#!/usr/bin/env python3
"""
DistroKid Promo-Card Watcher für Chris Mandel.

Erkennt neue DistroKid-Promo-Card-Mails ("Here's a photo of ..."), erzeugt
posting-fertiges Material auf dem Desktop und meldet per Telegram:
  - Promo-Card-Bild (JPG, 1080x1920)
  - TikTok-Video (12s MP4 aus dem Standbild — TikTok-Desktop nimmt nur Video)
  - Caption als .txt (NUR der einfügbare Text, inkl. Hashtags + HyperFollow-Link)

Aufruf:
  python3 distrokid_promo_watcher.py          # normaler Lauf (Cron)
  python3 distrokid_promo_watcher.py --test    # nur erkennen/anzeigen, keine Seiteneffekte
  python3 distrokid_promo_watcher.py --seed     # vorhandene Promo-Mails als "erledigt" markieren (kein Posten)
"""
import json, urllib.request, urllib.parse, base64, re, subprocess, sys, os
from pathlib import Path

# Helfer aus dem bestehenden Mail-Skript wiederverwenden (Token, Telegram, GRAPH)
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
_spec = importlib.util.spec_from_file_location("m2c", str(Path(__file__).parent / "mail_to_calendar.py"))
m2c = importlib.util.module_from_spec(_spec)
try:
    _spec.loader.exec_module(m2c)
except SystemExit:
    pass

DESKTOPS      = ["/mnt/d/OneDrive/Desktop", "/mnt/c/Users/ernst/Desktop"]
PROCESSED     = Path("/home/bolla/workspace/state/distrokid_promo_processed.json")
ARTIST_SLUG   = "bollawave"   # DistroKid-Künstlername (HyperFollow-URL)

def load_processed():
    try: return set(json.loads(PROCESSED.read_text()))
    except Exception: return set()

def save_processed(s):
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED.write_text(json.dumps(sorted(s), indent=2))

def graph_search(tok, term, select, top=10):
    q = urllib.parse.quote(f'"{term}"')
    url = m2c.GRAPH + f'/messages?$search={q}&$select={select}&$top={top}'
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}", "ConsistencyLevel": "eventual"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("value", [])

def slugify(name):
    s = name.lower()
    repl = {"ä":"ae","ö":"oe","ü":"ue","ß":"ss"}
    for k,v in repl.items(): s = s.replace(k,v)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def safe_filename(name):
    return re.sub(r'[<>:"/\\|?*]+', "", name).strip()

def find_promo_mails(tok):
    """Promo-Card-Mails finden (Betreff: Here's a photo of "X")."""
    out = []
    for m in graph_search(tok, "photo of", "id,subject,from", top=15):
        subj = m.get("subject", "")
        frm  = m.get("from", {}).get("emailAddress", {}).get("address", "").lower()
        if "distrokid" not in frm: continue
        if "photo of" not in subj.lower(): continue
        mt = re.search(r'of\s+["“”\'„](.+?)["“”\'"]', subj)
        if not mt: continue
        out.append({"id": m["id"], "subject": subj, "release": mt.group(1).strip()})
    return out

def find_hyperfollow(tok, release_slug):
    for m in graph_search(tok, "hyperfollow", "body", top=10):
        html = m.get("body", {}).get("content", "")
        for u in re.findall(r'https?://[^\s"\'<>]+hyperfollow[^\s"\'<>]+', html):
            if release_slug in u.lower():
                return u.split("?")[0]
    return None

def download_promo_image(tok, msg_id, dest_path):
    url = m2c.GRAPH + f'/messages/{msg_id}/attachments'
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {tok}"})
    att = json.loads(urllib.request.urlopen(req, timeout=30).read())
    for a in att.get("value", []):
        ct = a.get("contentType", "")
        if a.get("contentBytes") and ("image" in ct):
            open(dest_path, "wb").write(base64.b64decode(a["contentBytes"]))
            return True
    return False

def make_video(img_path, mp4_path):
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img_path, "-t", "12", "-r", "30",
           "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black",
           "-movflags", "+faststart", mp4_path]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180).returncode == 0

def build_caption(release, hyperfollow):
    slug = slugify(release)
    link = f"\n👉 Überall hören: {hyperfollow}\n(Spotify · Apple Music · YouTube)" if hyperfollow else ""
    return (f'🎵 Neuer Song ist live: „{release}"!{link}\n\n'
            f'🤖 Hinweis: KI-unterstützt produziert (Suno).\n\n'
            f'#distrokid #{slug} #neuersong #newrelease #spotify #applemusic #kimusik #aimusic')

def active_desktops():
    return [d for d in DESKTOPS if os.path.isdir(d)]

def process(test=False, seed=False):
    tok = m2c.get_token()
    processed = load_processed()
    mails = find_promo_mails(tok)
    if not mails:
        print("Keine Promo-Card-Mails gefunden."); return
    for mail in mails:
        new = mail["id"] not in processed
        print(f"{'NEU ' if new else 'alt '}| {mail['release']} | {mail['subject']}")
        if not new: continue
        if seed:
            processed.add(mail["id"]); continue
        if test:
            slug = slugify(mail["release"])
            hf = find_hyperfollow(tok, slug)
            print(f"   slug={slug}  hyperfollow={hf}")
            continue
        # echter Lauf
        desks = active_desktops()
        if not desks:
            print("   ⚠ Kein Desktop erreichbar — überspringe (nicht als erledigt markiert)"); continue
        rel = mail["release"]; fn = safe_filename(rel); slug = slugify(rel)
        img_name = f"DistroKid_PromoCard_{fn}.jpg"
        mp4_name = f"{fn}_TikTok-Video.mp4"
        txt_name = f"{fn}_Caption.txt"
        primary = desks[0]
        img_path = os.path.join(primary, img_name)
        if not download_promo_image(tok, mail["id"], img_path):
            print("   ⚠ Kein Bildanhang gefunden — überspringe"); continue
        hf = find_hyperfollow(tok, slug)
        mp4_path = os.path.join(primary, mp4_name)
        vid_ok = make_video(img_path, mp4_path)
        open(os.path.join(primary, txt_name), "w").write(build_caption(rel, hf))
        # auf weitere Desktops spiegeln
        for d in desks[1:]:
            try:
                open(os.path.join(d, img_name), "wb").write(open(img_path, "rb").read())
                if vid_ok: open(os.path.join(d, mp4_name), "wb").write(open(mp4_path, "rb").read())
                open(os.path.join(d, txt_name), "w").write(build_caption(rel, hf))
            except Exception: pass
        msg = (f"🎵 <b>Neue DistroKid Promo Card: „{rel}“</b>\n\n"
               f"Auf dem Desktop liegt jetzt bereit:\n"
               f"• 🖼️ Promo-Card-Bild\n"
               f"• 🎬 TikTok-Video (12s){' ⚠ Video fehlgeschlagen' if not vid_ok else ''}\n"
               f"• 📄 Caption-Textdatei (mit #distrokid + KI-Hinweis"
               f"{' + HyperFollow-Link' if hf else ''})\n\n"
               f"➡️ TikTok: Video hochladen · Insta: Bild posten.\n"
               f"Beschreibung aus der .txt einfügen, KI-Label aktivieren, posten. 🐾")
        try: m2c.telegram(msg)
        except Exception as e: print("   ⚠ Telegram-Fehler:", e)
        processed.add(mail["id"])
        print(f"   ✓ Material erzeugt + Telegram gesendet ({rel})")
    save_processed(processed)

if __name__ == "__main__":
    process(test="--test" in sys.argv, seed="--seed" in sys.argv)
