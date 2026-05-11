#!/usr/bin/env python3
"""
RouteNote Released-Watcher
Prüft ob neue Dateien im released/-Ordner aufgetaucht sind und benachrichtigt Chris per Telegram.
Cron: */10 * * * * /usr/bin/python3 /home/bolla/workspace/scripts/routenote_watcher.py
"""

import json
import os
import requests
from pathlib import Path

RELEASED_DIR = Path("/mnt/d/OneDrive/Dokumente/Bolla/Suno_RouteNote/released")
STATE_FILE = Path("/home/bolla/workspace/data/routenote_released.json")
cfg = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT_TOKEN = cfg["bot_token"]
CHRIS_ID = cfg["chris_id"]

def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHRIS_ID, "text": text, "parse_mode": "Markdown"},
        timeout=10
    )

STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
known = set(json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else [])

current = set()
if RELEASED_DIR.exists():
    for f in RELEASED_DIR.iterdir():
        if f.suffix.lower() in (".mp3", ".jpg"):
            current.add(f.name)

new_files = current - known
if new_files:
    mp3s = sorted(f for f in new_files if f.endswith(".mp3"))
    for mp3 in mp3s:
        song = mp3.replace("_320.mp3", "")
        send(f"🎵 *RouteNote — Song released!*\n\n✅ _{song}_ wurde in den `released/`-Ordner verschoben.\n\nVergiss nicht ihn bei RouteNote einzureichen falls noch nicht erledigt!")

STATE_FILE.write_text(json.dumps(sorted(current)))
