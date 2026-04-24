#!/usr/bin/env python3
"""
Eigene Aufnahmen Organizer
Backup → Duplikate löschen → Gemini Vision Analyse → Umbenennen + Sortieren
"""
import os, json, shutil, base64, time, hashlib, re, io
from pathlib import Path
import urllib.request, urllib.parse
from PIL import Image

SOURCE     = Path("/mnt/d/OneDrive/Bilder/Eigene Aufnahmen")
BACKUP     = Path("/mnt/d/OneDrive/Bilder/Eigene Aufnahmen_Backup")
PROGRESS   = Path("/home/bolla/workspace/logs/ea_progress.json")
GEMINI_CFG = Path("/home/bolla/workspace/config/gemini_api_free.json")
MODEL      = "gemini-2.0-flash"
IMG_EXTS   = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
VID_EXTS   = {'.mp4', '.MP4'}
MAX_IMG_PX = 1600   # Resize auf max. diese Breite/Höhe vor dem Senden
DELAY      = 4.0    # Sekunden zwischen API-Calls (15 RPM Free Tier)

FOLDERS = [
    "Familie", "Robin", "Robin BeReal", "Renate",
    "Stephanie und Familie", "Anne",
    "Natur und Landschaft", "Essen und Trinken",
    "Reisen und Ausflüge", "Events und Feiern",
    "Tiere", "Schule und Arbeit", "Sonstiges"
]

PROMPT_TEMPLATE = """Analysiere dieses Bild{video_hint}.

Bekannte Personen die erscheinen könnten:
- Renate: Ehefrau, ca. 60 Jahre, weiblich
- Robin: Sohn, ca. 26 Jahre, männlicher Student
- Stephanie: Tochter, ca. 38 Jahre, weiblich
- Daniel (Dani): Schwiegersohn, ca. 59 Jahre, männlich
- Anne (Ann-Kristin): Tochter, ca. 35 Jahre, weiblich
- Emma: Enkelin, ca. 8 Jahre
- Mia: Enkelin, ca. 4 Jahre
- Marie & Anton: Zwillinge, ca. 1 Jahr

Antworte NUR als reines JSON ohne Markdown:
{{
  "name": "kurzer_dateiname",
  "ordner": "ordnername",
  "personen": ["name1", "name2"]
}}

Regeln:
- name: Kleinbuchstaben, Unterstriche statt Leerzeichen, keine Umlaute (ae/oe/ue/ss), kein Datum, maximal 4 Wörter
- ordner muss einer aus dieser Liste sein: {folders}
- BeReal-Screenshot von Robin (zwei Kameras gleichzeitig sichtbar) → "Robin BeReal"
- Nur Robin sichtbar (kein BeReal) → "Robin"
- Nur Renate → "Renate"
- Nur Anne (evtl. mit unbekanntem Mann) → "Anne"
- Stephanie, Daniel, Emma, Mia, Marie oder Anton → "Stephanie und Familie"
- Mehrere Familienmitglieder zusammen → "Familie"
- Essen, Getränke, Restaurant → "Essen und Trinken"
- Natur, Landschaft, Architektur, Stadtansicht → "Natur und Landschaft"
- Urlaub, Reise, Ausflug → "Reisen und Ausflüge"
- Party, Feier, Fest, Konzert → "Events und Feiern"
- Tiere, Haustiere → "Tiere"
- Schule, Unterricht, Büro, Arbeit → "Schule und Arbeit"
- Alles andere → "Sonstiges"
"""

# ─── Hilfsfunktionen ──────────────────────────────────────────────────────────

def gemini_key():
    return json.loads(GEMINI_CFG.read_text())["api_key"]

def file_hash(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def img_to_b64(path: Path) -> tuple[str, str]:
    """Liest Bild, resized wenn nötig, gibt (base64, mime) zurück"""
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        if max(img.size) > MAX_IMG_PX:
            img.thumbnail((MAX_IMG_PX, MAX_IMG_PX), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        return base64.b64encode(buf.getvalue()).decode(), "image/jpeg"
    except Exception:
        raw = path.read_bytes()
        return base64.b64encode(raw).decode(), "image/jpeg"

def video_thumbnail_b64(path: Path) -> tuple[str, str] | None:
    """Extrahiert ersten Frame via ffmpeg"""
    import subprocess, tempfile
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", str(path), "-vframes", "1", "-q:v", "2", tmp_path],
            capture_output=True, timeout=30
        )
        if result.returncode == 0 and Path(tmp_path).exists():
            b64, mime = img_to_b64(Path(tmp_path))
            Path(tmp_path).unlink(missing_ok=True)
            return b64, mime
    except Exception:
        pass
    return None

def remove_duplicates():
    print("\n── Duplikate entfernen ──")
    deleted = 0
    for f in list(SOURCE.iterdir()):
        if f.is_file() and " - Kopie" in f.name:
            f.unlink(); deleted += 1
            print(f"  Kopie: {f.name}")
    hashes = {}
    for f in sorted(SOURCE.iterdir()):
        if not f.is_file(): continue
        if f.suffix.lower() not in IMG_EXTS | VID_EXTS: continue
        h = file_hash(f)
        if h in hashes:
            print(f"  Duplikat: {f.name}  (={hashes[h].name})")
            f.unlink(); deleted += 1
        else:
            hashes[h] = f
    print(f"  → {deleted} Dateien gelöscht\n")

def analyze(fp: Path, key: str) -> dict:
    is_video = fp.suffix.lower() in VID_EXTS
    if is_video:
        result = video_thumbnail_b64(fp)
    else:
        result = img_to_b64(fp)

    if not result:
        return {"name": "unbekannt", "ordner": "Sonstiges", "personen": []}

    b64_data, mime = result
    prompt = PROMPT_TEMPLATE.format(
        video_hint=" (Videoframe/Platzhalter)" if is_video else "",
        folders=", ".join(f'"{f}"' for f in FOLDERS)
    )
    payload = json.dumps({"contents": [{"parts": [
        {"text": prompt},
        {"inline_data": {"mime_type": mime, "data": b64_data}}
    ]}]}).encode()

    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{MODEL}:generateContent?key={key}")

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=payload, method="POST",
                                          headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                resp = json.loads(r.read())
            text = resp["candidates"][0]["content"]["parts"][0]["text"].strip()
            if "```" in text:
                parts = text.split("```")
                text = parts[1] if len(parts) > 1 else parts[0]
                if text.startswith("json"):
                    text = text[4:]
            data = json.loads(text.strip())
            if data.get("ordner") not in FOLDERS:
                data["ordner"] = "Sonstiges"
            # Name bereinigen
            name = re.sub(r'[^\w_-]', '', data.get("name", "bild")).strip('_') or "bild"
            data["name"] = name[:60]
            return data
        except Exception as e:
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
            else:
                print(f"  API-Fehler: {e}")
                return {"name": re.sub(r'[^\w]', '_', fp.stem)[:30], "ordner": "Sonstiges", "personen": []}

def unique_name(base: str, folder: Path, ext: str) -> str:
    name = f"{base}{ext.lower()}"
    if not (folder / name).exists():
        return name
    i = 2
    while (folder / f"{base}_{i:02d}{ext.lower()}").exists():
        i += 1
    return f"{base}_{i:02d}{ext.lower()}"

# ─── Hauptprogramm ────────────────────────────────────────────────────────────

def main():
    print("═" * 55)
    print("  Eigene Aufnahmen Organizer  🐾")
    print("═" * 55)

    # 1. Backup
    if BACKUP.exists():
        print(f"\n✓ Backup bereits vorhanden: {BACKUP.name}")
    else:
        print(f"\nErstelle Backup (bitte warten)...")
        shutil.copytree(SOURCE, BACKUP)
        print(f"✓ Backup fertig: {BACKUP}")

    # 2. Duplikate
    remove_duplicates()

    # 3. Unterordner anlegen
    for fn in FOLDERS:
        (SOURCE / fn).mkdir(exist_ok=True)

    # 4. Fortschritt laden
    progress = {}
    if PROGRESS.exists():
        try:
            progress = json.loads(PROGRESS.read_text())
            print(f"Fortschritt geladen: {len(progress)} bereits erledigt\n")
        except Exception:
            pass

    # 5. Dateien sammeln
    files = sorted([
        f for f in SOURCE.iterdir()
        if f.is_file()
        and f.suffix.lower() in IMG_EXTS | VID_EXTS
    ])

    total = len(files)
    print(f"── Verarbeite {total} Dateien (~{round(total * DELAY / 60)} Minuten) ──\n")

    key = gemini_key()
    moved = errors = skipped = 0
    start = time.time()

    for i, fp in enumerate(files, 1):
        if fp.name in progress:
            skipped += 1
            continue

        elapsed = time.time() - start
        remaining = (total - i) * DELAY
        print(f"[{i:3d}/{total}] {fp.name[:45]:<45}", end=" ", flush=True)

        result = analyze(fp, key)
        target_dir = SOURCE / result["ordner"]
        target_dir.mkdir(exist_ok=True)
        new_name = unique_name(result["name"], target_dir, fp.suffix)

        try:
            shutil.move(str(fp), str(target_dir / new_name))
            persons = ", ".join(result.get("personen", [])) or "–"
            print(f"→ {result['ordner']}/{new_name}")
            progress[fp.name] = {"new": new_name, "ordner": result["ordner"], "personen": result.get("personen", [])}
            PROGRESS.write_text(json.dumps(progress, indent=2, ensure_ascii=False))
            moved += 1
        except Exception as e:
            print(f"  MOVE FEHLER: {e}")
            errors += 1

        time.sleep(DELAY)

    # 6. Sauber machen
    for f in SOURCE.iterdir():
        if f.is_file() and f.name.lower() in {"desktop.ini", "thumbs.db"}:
            f.unlink()

    elapsed_total = round((time.time() - start) / 60, 1)
    print(f"\n{'═' * 55}")
    print(f"✓ Fertig in {elapsed_total} Minuten!")
    print(f"  Verschoben/umbenannt : {moved}")
    print(f"  Übersprungen (vorher): {skipped}")
    print(f"  Fehler               : {errors}")
    print(f"  Backup               : {BACKUP}")
    print(f"  Log                  : {PROGRESS}")
    print("═" * 55)

if __name__ == "__main__":
    main()
