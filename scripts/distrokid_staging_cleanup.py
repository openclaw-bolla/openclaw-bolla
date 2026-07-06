#!/usr/bin/env python3
"""
DistroKid-Staging-Aufräumer (feste Regel, Chris 06.07.2026):
Sobald ein Song laut Release-Kalender online ist (done:true), wandert sein
Desktop-Staging-Ordner automatisch ins Backup-Archiv — so bleibt
Desktop/DistroKid/ immer aufgeräumt, ohne dass jemand dran denken muss.

Cron: 45 9 * * *  (täglich, kurz nach dem Release-Reminder um 9:30)
Log:  logs/distrokid_staging_cleanup.log
"""
import json, re, shutil
from pathlib import Path
from datetime import datetime

DK_DIR   = Path("/mnt/d/OneDrive/Desktop/DistroKid")
ARCHIVE  = Path("/home/bolla/workspace/backups/distrokid_desktop_archiv")
SCHED    = Path("/home/bolla/workspace/config/bollawave_release_schedule.json")
TGCFG    = Path("/home/bolla/workspace/config/telegram_bot.json")

def norm(s):
    """Titel/Ordnernamen vergleichbar machen: klein, nur Buchstaben/Ziffern."""
    return re.sub(r"[^a-z0-9äöüß]", "", (s or "").lower())

def telegram(text):
    try:
        import urllib.request, urllib.parse
        cfg = json.loads(TGCFG.read_text())
        url = f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": cfg["chris_id"], "text": text}).encode()
        urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=15)
    except Exception:
        pass

def main():
    if not DK_DIR.exists():
        return
    sched = json.loads(SCHED.read_text(encoding="utf-8"))
    done_norms = {norm(s.get("title", "")) for s in sched.get("singles", []) if s.get("done")}
    if not done_norms:
        return
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    moved = []
    for folder in DK_DIR.iterdir():
        if not folder.is_dir():
            continue
        if norm(folder.name) in done_norms:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            dest = ARCHIVE / f"{folder.name}_{ts}"
            shutil.move(str(folder), str(dest))
            moved.append(folder.name)
            print(f"[{ts}] archiviert: {folder.name} → {dest}")
    if moved:
        telegram("🧹 DistroKid aufgeräumt: " + ", ".join(moved) +
                 " (online → Staging ins Backup-Archiv verschoben).")

if __name__ == "__main__":
    main()
