#!/usr/bin/env python3
"""Neue Kontaktbilder aus OneDrive/Bilder/Kontaktbilder automatisch einbauen ("kontaktbilder neu").
- nur NEUE/geänderte Dateien (Stand in kontaktfoto_state.json)
- Zuordnung: exakter Name > Alias (kontaktfoto_alias.json) > eindeutiger Vorname/Nachname-Treffer; mehrdeutig -> nur melden
- Zuschnitt quadratisch: manuelle Box (alias.json 'crops') > genau 1 Gesicht (OpenCV) > Mitte; mehrere Gesichter -> nur melden
- Backup altes Foto -> backups/kontaktfotos_<ts>/, setzt Outlook (Chris) + Google-Foto direkt (kein Vollsync nötig)
Aufruf: kontaktfoto_neu.py [dry]"""
import os, re, sys, io, json, time, unicodedata, importlib.util
import cv2, numpy as np
from PIL import Image, ImageOps
D = "/home/bolla/workspace/scripts/"
spec = importlib.util.spec_from_file_location("s", D + "outlook_gmail_sync.py"); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
DRY = len(sys.argv) > 1 and sys.argv[1] == "dry"
DIR = "/mnt/d/OneDrive/Bilder/Kontaktbilder"
STATE = D + "kontaktfoto_state.json"; ALIAS = D + "kontaktfoto_alias.json"
state = json.load(open(STATE)) if os.path.exists(STATE) else None
alias = json.load(open(ALIAS)) if os.path.exists(ALIAS) else {"alias": {}, "crops": {}}
norm = lambda x: "".join(sorted(re.sub(r"[^a-zäöüß ]", "", unicodedata.normalize("NFC", x.lower())).split()))
sig = lambda f: f"{os.path.getmtime(os.path.join(DIR,f)):.0f}:{os.path.getsize(os.path.join(DIR,f))}"
files = [f for f in sorted(os.listdir(DIR)) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
if state is None:  # Erstlauf: alles Vorhandene gilt als erledigt
    json.dump({f: sig(f) for f in files}, open(STATE, "w"), indent=1); print("Erstlauf: Stand gespeichert"); sys.exit()
new = [f for f in files if state.get(f) != sig(f)]
if not new: print("Keine neuen Kontaktbilder."); sys.exit()
t = s.get_ms_token(); cs = s.get_outlook_contacts(t)
def match(stem):
    n = norm(stem); ex = [c for c in cs if norm(c["displayName"]) == n]
    if len(ex) == 1: return ex[0], "Name"
    a = alias["alias"].get(stem.lower())
    if a:
        ex = [c for c in cs if norm(c["displayName"]) == norm(a)]
        if len(ex) == 1: return ex[0], "Alias"
    tok = stem.lower().split()
    if len(tok) == 1:
        ex = [c for c in cs if tok[0] in (c["displayName"].lower().split())]
        if len(ex) == 1: return ex[0], "Vorname"
        return None, f"mehrdeutig/keiner ({len(ex)}): " + ", ".join(c["displayName"] for c in ex[:6])
    return None, "kein Treffer"
def crop(im, f):
    box = alias["crops"].get(f)
    if box: return im.crop(tuple(box)), "manuell"
    w, h = im.size
    if w == h: return im, "quadratisch"
    g = cv2.cvtColor(np.array(im.copy().resize((w*800//max(w,h), h*800//max(w,h)))), cv2.COLOR_RGB2GRAY); k = max(w,h)/800
    fc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(g, 1.1, 6, minSize=(40, 40))
    if len(fc) > 1: return None, f"{len(fc)} Gesichter – bitte sagen wer / Zuschnitt angeben"
    s_ = min(w, h)
    if len(fc) == 1:
        x, y, fw, fh = [v*k for v in fc[0]]; cx, cy = x+fw/2, y+fh/2; s_ = min(s_, max(fw*2.6, 1)) if fw*2.6 > 300 else s_
    else: cx, cy = w/2, h/2
    x0 = int(min(max(cx-s_/2, 0), w-s_)); y0 = int(min(max(cy-s_/2, 0), h-s_))
    return im.crop((x0, y0, x0+int(s_), y0+int(s_))), "Gesicht" if len(fc) else "Mitte"
bk = f"/home/bolla/workspace/backups/kontaktfotos_{time.strftime('%Y%m%d_%H%M')}_neu"
gtoken = None; gidx = None; ok = []
for f in new:
    stem = re.sub(r"\s*-\s*kopie|\s*\(\d+\)", "", os.path.splitext(f)[0], flags=re.I)
    c, how = match(stem)
    if not c: print(f"⚠️ {f}: {how} – nicht gesetzt"); continue
    im = ImageOps.exif_transpose(Image.open(os.path.join(DIR, f))).convert("RGB")
    im2, cr = crop(im, f)
    if im2 is None: print(f"⚠️ {f}: {cr}"); continue
    print(f"{'würde setzen' if DRY else 'SETZE'}: {f} -> {c['displayName']} (Zuordnung {how}, Zuschnitt {cr})")
    if DRY: continue
    os.makedirs(bk, exist_ok=True)
    old = s.get_outlook_photo(t, c["id"])
    if old: open(f"{bk}/{c['id'][-12:].replace('/','_')}.jpg", "wb").write(old)
    im2.thumbnail((720, 720)); b = io.BytesIO(); im2.save(b, "JPEG", quality=90); data = b.getvalue()
    s.set_outlook_photo(t, c["id"], data)
    if gtoken is None: gtoken = s.get_google_token(); gidx = s.build_google_index(s.get_google_contacts(gtoken))
    g = gidx.get(c["displayName"].lower()) or gidx.get(s.name_key(c["displayName"]))
    print("   Google:", "ok" if g and s.set_google_photo(gtoken, g[0], data) else "NICHT gesetzt")
    state[f] = sig(f); ok.append(f)
if not DRY:
    for f in new:
        if f in ok: state[f] = sig(f)
    json.dump(state, open(STATE, "w"), indent=1)
print("fertig:", len(ok) if not DRY else "Dry-Run")
