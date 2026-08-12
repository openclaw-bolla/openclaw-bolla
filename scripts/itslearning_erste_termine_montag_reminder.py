#!/usr/bin/env python3
"""
itslearning "Eure ersten Termine"-Reminder (einmalig)
Chris wollte die fertig geprüfte "Eure ersten Termine"-Mitteilung (alle 8 Kurse, korrekte I/II-
Termine, siehe scripts/itslearning_post_erste_termine.py) nicht sofort (12.08.2026), sondern erst
am Montag 17.08.2026 selbst einstellen lassen. Erinnert ihn ab diesem Datum per Telegram.

Datums-basiert (uebersteht ausgeschalteten Rechner). Cron laeuft mehrmals morgens, das Script
feuert aber genau EINMAL (State -> done).

Cron: 0 7-11 * * * python3 /home/bolla/workspace/scripts/itslearning_erste_termine_montag_reminder.py
Stoppen/Erledigt: config/itslearning_erste_termine_montag_reminder_state.json -> "done": true
"""
import json
from pathlib import Path
from datetime import date
import urllib.request

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/itslearning_erste_termine_montag_reminder_state.json")
FIRE_FROM = date(2026, 8, 17)


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
    tg("🗓️ *itslearning — Montag ist da* ⏰\n\n"
       "Du wolltest heute die \"Eure ersten Termine\"-Mitteilung selbst einstellen lassen — Texte "
       "sind fertig und korrekt (I- und II-Kurse mit ihren jeweils eigenen Terminen). Sag einfach "
       "Bescheid, dann poste ich sie in alle 8 Kurse. 🐾")
    st["done"] = True
    st["sent_on"] = date.today().isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print("itslearning-Erste-Termine-Montag-Reminder gesendet")


if __name__ == "__main__":
    main()
