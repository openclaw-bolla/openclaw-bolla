#!/usr/bin/env python3
"""
KDP-Veröffentlichen-Reminder (einmalig)
Erinnert Chris ab dem 20.06.2026 per Telegram, die zwei KDP-Bücher (DE+EN)
zu veröffentlichen, sobald Amazons Bankprüfung durch ist. Feuert nur EINMAL.
Datums-Check (nicht uhrzeitgebunden) → übersteht ausgeschalteten Rechner.

Cron: 0 9 * * * python3 /home/bolla/workspace/scripts/kdp_publish_reminder.py
"""
import json, urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/kdp_publish_reminder_state.json")
FIRE_FROM = date(2026, 6, 20)

def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id":CHRIS,"text":text,"parse_mode":"Markdown",
                         "disable_web_page_preview":True}).encode(),
        headers={"Content-Type":"application/json"}), timeout=20)

def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {"done": False}
    if st.get("done"):
        return
    if date.today() < FIRE_FROM:
        return
    tg("⏰ *KDP-Erinnerung*\n\n"
       "Amazons Bankprüfung sollte jetzt durch sein (gestartet ~17.06., bis 3 Tage).\n\n"
       "👉 Geh ins [KDP-Bücherregal](https://kdp.amazon.com) und prüfe, ob der "
       "*„Kindle eBook veröffentlichen\"*-Button bei den **beiden** AURORA-Büchern "
       "(🇩🇪 + 🇬🇧) jetzt aktiv ist. Wenn ja: bei beiden veröffentlichen! 📚\n\n"
       "Falls noch ausgegraut → einfach morgen nochmal. 🐾")
    st["done"] = True
    STATE.write_text(json.dumps(st, indent=2))
    print("Reminder gesendet")

if __name__ == "__main__":
    main()
