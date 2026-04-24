#!/usr/bin/env python3
"""
Findet Dateien aus Eigene Aufnahmen_Backup die bereits irgendwo in OneDrive existieren (Hash-Vergleich).
"""
import hashlib, os, json
from pathlib import Path

BACKUP   = Path("/mnt/d/OneDrive/Bilder/Eigene Aufnahmen_Backup")
ONEDRIVE = Path("/mnt/d/OneDrive")
RESULT   = Path("/tmp/ea_duplicates.json")
EXTS     = {'.jpg', '.jpeg', '.png', '.mp4', '.JPG', '.JPEG', '.PNG', '.MP4'}

def file_hash(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

print("Schritt 1: Hashes der organisierten Fotos berechnen...")
backup_hashes = {}
for f in BACKUP.rglob("*"):
    if f.is_file() and f.suffix in EXTS:
        backup_hashes[file_hash(f)] = f

print(f"  {len(backup_hashes)} Dateien in Eigene Aufnahmen_Backup")

print("\nSchritt 2: Hashes aller OneDrive-Fotos berechnen (dauert ~10 Minuten)...")
onedrive_hashes = {}
count = 0
for f in ONEDRIVE.rglob("*"):
    if not f.is_file(): continue
    if f.suffix not in EXTS: continue
    # Eigene Aufnahmen Ordner überspringen
    parts = f.parts
    if any("Eigene Aufnahmen" in p for p in parts): continue
    try:
        h = file_hash(f)
        onedrive_hashes[h] = f
        count += 1
        if count % 1000 == 0:
            print(f"  {count} Dateien verarbeitet...")
    except Exception:
        pass

print(f"  {count} Dateien in OneDrive (ohne Eigene Aufnahmen)")

print("\nSchritt 3: Vergleiche...")
duplicates = []
for h, backup_file in backup_hashes.items():
    if h in onedrive_hashes:
        duplicates.append({
            "backup": str(backup_file.relative_to(BACKUP)),
            "existing": str(onedrive_hashes[h].relative_to(ONEDRIVE))
        })

RESULT.write_text(json.dumps(duplicates, indent=2, ensure_ascii=False))

print(f"\n{'═'*55}")
print(f"✓ Fertig!")
print(f"  Bereits in OneDrive vorhanden: {len(duplicates)}/{len(backup_hashes)}")
print(f"  Ergebnis: {RESULT}")
print(f"{'═'*55}")

if duplicates:
    print("\nBeispiele:")
    for d in duplicates[:10]:
        print(f"  {d['backup']}")
        print(f"    → bereits in: {d['existing']}")
