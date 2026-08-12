#!/usr/bin/env python3
"""
itslearning "Eure nächsten Termine"-Reminder (einmalig)
Erinnert Chris ab dem 02.09.2026 (ca. 1 Woche Vorlauf, Chris' Grundsatz "immer fruehzeitig
ankuendigen" - siehe [[feedback_itslearning_termine_fruehzeitig]]) per Telegram daran, die
naechste Runde der "Eure naechsten Termine"-Mitteilung (Format siehe
[[project_itslearning_automation]]) in allen 8 EDV-Kursen zu posten - Block Gruppe I endet
09./10.09.2026, danach startet Gruppe II.

Datums-basiert (uebersteht ausgeschalteten Rechner). Cron laeuft mehrmals
morgens, das Script feuert aber genau EINMAL (State -> done).

Cron: 0 7-11 * * * python3 /home/bolla/workspace/scripts/itslearning_naechste_termine_reminder.py
Stoppen/Erledigt: config/itslearning_naechste_termine_reminder_state.json -> "done": true
"""
import json
from pathlib import Path
from datetime import date
import urllib.request

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/itslearning_naechste_termine_reminder_state.json")
FIRE_FROM = date(2026, 9, 2)


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
    tg("🗓️ *itslearning — Gruppenwechsel steht an* ⏰\n\n"
       "Der erste Block (Gruppe I) läuft bis 09./10.09. — Zeit für *\"Eure nächsten Termine\"* "
       "in allen 8 EDV-Kursen (7a/7b/7c/7d, je I+II), mit den Terminen der jetzt startenden "
       "Gruppe II. Sag einfach Bescheid, dann bau ich die Texte + poste sie. 🐾")
    st["done"] = True
    st["sent_on"] = date.today().isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print("itslearning-Naechste-Termine-Reminder gesendet")


if __name__ == "__main__":
    main()
