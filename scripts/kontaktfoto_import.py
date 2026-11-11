#!/usr/bin/env python3
"""Kontaktfotos aus OneDrive/Bilder/Kontaktbilder in Outlook-Kontakte setzen.
Regel: Dateiname (ohne Endung, ohne ' - Kopie') = Anzeigename des Kontakts ("Vorname Nachname" oder "Nachname Vorname"). Nur eindeutige Treffer.
DRY-RUN default; 'apply' schreibt (Backup der alten Fotos vorher nach backups/kontaktfotos_<ts>/). Danach Gmail-Sync: outlook_gmail_sync.py.
Renates Kontakte werden nie angefasst (nur ms_token = Chris)."""
import os, re, sys, io, time, unicodedata, importlib.util
from PIL import Image, ImageOps
spec = importlib.util.spec_from_file_location("s", "/home/bolla/workspace/scripts/outlook_gmail_sync.py"); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"
DIR = "/mnt/d/OneDrive/Bilder/Kontaktbilder"
norm = lambda x: "".join(sorted(re.sub(r"[^a-zäöüß ]", "", unicodedata.normalize("NFC", x.lower())).split()))
t = s.get_ms_token(); cs = s.get_outlook_contacts(t)
idx = {}
for c in cs: idx.setdefault(norm(c["displayName"]), []).append(c)
bk = f"/home/bolla/workspace/backups/kontaktfotos_{time.strftime('%Y%m%d_%H%M')}"
done = 0
for f in sorted(os.listdir(DIR)):
    if not f.lower().endswith((".jpg", ".jpeg", ".png")): continue
    stem = re.sub(r"\s*-\s*kopie|\s*\(\d+\)", "", os.path.splitext(f)[0], flags=re.I)
    m = idx.get(norm(stem), [])
    if len(m) != 1: continue
    c = m[0]; print(("SETZE " if APPLY else "würde setzen: ") + f, "->", c["displayName"])
    if not APPLY: continue
    os.makedirs(bk, exist_ok=True)
    old = s.get_outlook_photo(t, c["id"])
    if old: open(f"{bk}/{c['id'][-12:].replace('/','_')}.jpg", "wb").write(old)
    im = ImageOps.exif_transpose(Image.open(os.path.join(DIR, f))).convert("RGB"); im.thumbnail((720, 720)); b = io.BytesIO(); im.save(b, "JPEG", quality=90)
    s.set_outlook_photo(t, c["id"], b.getvalue()); done += 1
print("fertig:", done if APPLY else "Dry-Run")
