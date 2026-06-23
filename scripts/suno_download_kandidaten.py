#!/usr/bin/env python3
"""Lädt die MP3s (+Cover) der DistroKid-Kandidaten nach Suno_DistroKid/.
Bevorzugt vorhandene 320kbps aus dem alten released/-Ordner, sonst frischer
Download von der Suno-CDN. Dedupliziert nach Titel, mit Blocklist."""
import json, os, re, subprocess, shutil

WS = "/home/bolla/workspace"
OUT = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid"
RELEASED = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_RouteNote/released"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"

buckets = json.load(open(f"{WS}/data/suno_filter_result.json"))
kand = buckets["kandidat"]

# Finale Fehltreffer raus (Namen/Geburtstag/Artefakt durchgerutscht)
BLOCK = {
    "🎶🍪 „in der weihnachtskinderküche“",   # Enkelnamen — NIE
    "péter's anthem", "the world sings your name today 🎹🌤️",
    "“the world sings your name today 🎹🌤️”",
    "untitled project [01:10 - 02:00]", "heute ist der tag, den alle lieben,",
}
def norm(t): return re.sub(r"\s+"," ",t.strip().lower())
def safe(t):
    t = re.sub(r'[\\/:*?"<>|\n\r]+'," ", t).strip()
    t = re.sub(r"\s+"," ", t)
    return t[:90] or "untitled"

# Released-Index: Titel(lower) -> Pfad der _320.mp3
rel_idx = {}
if os.path.isdir(RELEASED):
    for f in os.listdir(RELEASED):
        if f.lower().endswith("_320.mp3"):
            rel_idx[norm(f[:-8])] = os.path.join(RELEASED, f)

os.makedirs(OUT, exist_ok=True)
seen, todo = set(), []
for s in kand:
    n = norm(s["title"])
    if n in BLOCK or n in seen or n == "(ohne titel)":
        continue
    seen.add(n); todo.append(s)

print(f"{len(todo)} eindeutige Kandidaten → {OUT}\n")
ok_copy = ok_dl = fail = 0
for s in todo:
    base = safe(s["title"])
    dest = os.path.join(OUT, base + ".mp3")
    n = norm(s["title"])
    # 1) Vorhandene 320er bevorzugen
    src320 = rel_idx.get(n)
    if src320 and os.path.exists(src320):
        shutil.copy2(src320, dest)
        cov = src320.replace("_320.mp3","_cover.jpg")
        if os.path.exists(cov): shutil.copy2(cov, os.path.join(OUT, base+".jpg"))
        print(f"  ✔ [320 kopiert] {base}"); ok_copy += 1; continue
    # 2) Frisch von Suno-CDN
    url = s.get("audio_url")
    if not url:
        print(f"  ✖ keine URL: {base}"); fail += 1; continue
    r = subprocess.run(["curl","-sL","-A",UA,"-o",dest,url], capture_output=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 100_000:
        print(f"  ⬇ [frisch] {base}  ({os.path.getsize(dest)//1024} KB)"); ok_dl += 1
        img = s.get("image_url")
        if img: subprocess.run(["curl","-sL","-A",UA,"-o",os.path.join(OUT,base+".jpg"),img], capture_output=True)
    else:
        if os.path.exists(dest): os.remove(dest)
        print(f"  ✖ Download-Fehler: {base}"); fail += 1

print(f"\nFertig. {ok_copy} aus 320-Bestand kopiert, {ok_dl} frisch geladen, {fail} Fehler.")
print(f"Ordner: {OUT}")
