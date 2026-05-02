#!/usr/bin/env python3
"""Schickt alle 3 Tage eine Telegram-Erinnerung: Reiseempfehlung in MC aktualisieren."""
import json, os, requests
from datetime import datetime
from pathlib import Path

WORKSPACE = os.path.expanduser("~/workspace")
TRAVEL_FILE = Path(WORKSPACE) / "cache/travel.json"
CFG_FILE = Path(WORKSPACE) / "config/telegram_bot.json"

cfg = json.loads(CFG_FILE.read_text())
TOKEN = cfg["bot_token"]
CHRIS = cfg["chris_id"]

travel = json.loads(TRAVEL_FILE.read_text()) if TRAVEL_FILE.exists() else {}
urlaube = travel.get("urlaube", [])

if not urlaube:
    exit(0)

u = urlaube[0]
von = datetime.fromisoformat(u["von"])
days_left = (von - datetime.now()).days

if days_left < 0:
    exit(0)

# Alter der letzten Empfehlung prüfen
akt = u.get("pauschal", {}).get("aktualisiert")
if akt:
    age_days = (datetime.now() - datetime.fromisoformat(akt)).days
    if age_days < 3:
        exit(0)

msg = (
    f"✈️ *Reiseplaner Update fällig!*\n\n"
    f"Der Sommer-Badeurlaub ist in *{days_left} Tagen* "
    f"({von.strftime('%d.%m.%Y')}).\n\n"
    f"Bitte Bolla nach neuen Reiseempfehlungen fragen:\n"
    f"→ Mission Control → Projekte → Urlaubsplanung\n\n"
    f"_Schreib mir: 'Such beste Pauschalreise für Sommer 2026'_"
)

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHRIS, "text": msg, "parse_mode": "Markdown"},
    timeout=10
)
print("Reminder sent")
