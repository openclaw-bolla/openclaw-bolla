#!/usr/bin/env python3
"""
itslearning Kurstag-2-Freigabe-Reminder (einmalig)
Chris wollte die vorbereiteten (noch nicht veroeffentlichten) Kurstag-2-Mitteilungen fuer
7a/7b/7c/7d I nicht sofort, sondern am Montag 24.08.2026 selbst pruefen/freigeben. Erinnert
ihn ab diesem Datum per Telegram. Vorschau liegt unter
/mnt/d/OneDrive/Desktop/itslearning Kurstag 2 - Vorschau/

Datums-basiert (uebersteht ausgeschalteten Rechner). Cron laeuft mehrmals morgens, das Script
feuert aber genau EINMAL (State -> done).

Cron: 0 7-11 * * * python3 /home/bolla/workspace/scripts/itslearning_kurstag2_freigabe_montag_reminder.py
Stoppen/Erledigt: config/itslearning_kurstag2_freigabe_montag_reminder_state.json -> "done": true
"""
import json
from pathlib import Path
from datetime import date
import urllib.request

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/itslearning_kurstag2_freigabe_montag_reminder_state.json")
FIRE_FROM = date(2026, 8, 24)


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                         "disable_web_page_preview": True}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    if st.get("done"):
        return
    if date.today() < FIRE_FROM:
        return
    tg("🗓️ *itslearning Kurstag 2 — Freigabe* ⏰\n\n"
       "Die Mitteilungen für 7a/7b/7c/7d I (Schüler + Eltern getrennt) sind fertig vorbereitet, "
       "aber noch nicht veröffentlicht. Vorschau liegt auf deinem Desktop im Ordner "
       "\"itslearning Kurstag 2 - Vorschau\". Sag Bescheid, dann poste ich live. 🐾")
    st["done"] = True
    st["sent_on"] = date.today().isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print("itslearning-Kurstag2-Freigabe-Montag-Reminder gesendet")


if __name__ == "__main__":
    main()
