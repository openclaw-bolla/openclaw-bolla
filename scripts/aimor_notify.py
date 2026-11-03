#!/usr/bin/env python3
"""
Aimor Foto-Push Vorab-Benachrichtigung
Läuft täglich auf Tage 28-31 — sendet Telegram nur wenn morgen der 1. ist.
Cron: 0 20 28-31 * * python3 /home/bolla/workspace/scripts/aimor_notify.py
"""

import json
import os
import requests
from datetime import date, timedelta
from pathlib import Path

# Nur ausführen wenn morgen der 1. ist
tomorrow = date.today() + timedelta(days=1)
if tomorrow.day != 1:
    raise SystemExit(0)

cfg = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT_TOKEN = cfg["bot_token"]
CHRIS_ID  = cfg["chris_id"]

config_path = Path.home() / ".aimor_config"
photo_folder = "/mnt/d/OneDrive/Mandels"
if config_path.exists():
    for line in config_path.read_text().splitlines():
        if line.startswith("photo_folder="):
            photo_folder = line.partition("=")[2].strip()

monat = tomorrow.strftime("%B %Y").replace(
    "January","Januar").replace("February","Februar").replace("March","März"
    ).replace("April","April").replace("May","Mai").replace("June","Juni"
    ).replace("July","Juli").replace("August","August").replace("September","September"
    ).replace("October","Oktober").replace("November","November").replace("December","Dezember")

text = (
    f"📸 *Aimor Foto-Push morgen früh!*\n\n"
    f"Morgen ({tomorrow.strftime('%d.%m.')}) um 08:00 Uhr schicke ich automatisch "
    f"50 neue Fotos auf den Rahmen.\n\n"
    f"📁 Aktueller Ordner: `{photo_folder}`\n\n"
    f"Falls du einen anderen Ordner willst (z.B. Urlaub-Fotos), "
    f"trag ihn in `~/.aimor\\_config` ein:\n"
    f"`photo\\_folder=/mnt/d/OneDrive/DeinOrdner`\n\n"
    f"Oder sag mir einfach Bescheid 🐾"
)

import sys; sys.path.insert(0, "/home/bolla/workspace/scripts"); from job_status import mc_meldung
mc_meldung("aimor-notify", "Aimor: Fotoauswahl zum Monatsersten", text)  # Chris 03.11.2026: kein Telegram mehr
print("MC-Meldung eingetragen")
