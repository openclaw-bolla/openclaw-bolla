#!/usr/bin/env python3
"""
Räumt D:\\OneDrive\\Bilder\\Handy-Clip\\ auf: Dateien älter als 14 Tage werden
gelöscht. Die Fotos dort sind nur eine Durchlaufstation für den ADB->Windows-
Zwischenablage-Weg (Original bleibt auf dem Handy) — kein Verlust bei Löschung.

Cron: 0 8 * * *  (täglich morgens)
Log:  logs/handy_clip_cleanup.log
"""
from pathlib import Path
from datetime import datetime, timedelta

CLIP_DIR = Path("/mnt/d/OneDrive/Bilder/Handy-Clip")
RETENTION_DAYS = 14

def main():
    if not CLIP_DIR.exists():
        return
    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    deleted = []
    for f in CLIP_DIR.iterdir():
        if not f.is_file():
            continue
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            deleted.append(f.name)
            f.unlink()
    if deleted:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] gelöscht ({len(deleted)}): {', '.join(deleted)}")

if __name__ == "__main__":
    main()
