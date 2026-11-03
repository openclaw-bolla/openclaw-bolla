#!/usr/bin/env python3
"""
KDP-Veröffentlichen-Reminder (wiederkehrend bis erledigt)
Erinnert Chris ab dem 20.06.2026 per Telegram, die zwei KDP-Bücher (DE+EN)
zu veröffentlichen, sobald Amazons Bankprüfung durch ist.
Feuert alle 2 Tage erneut (Amazon mailt das Ende der Bankprüfung meist NICHT),
bis Chris stoppt ("done") oder das Sicherheitslimit erreicht ist.
Datums-Check (nicht uhrzeitgebunden) → übersteht ausgeschalteten Rechner.

Stoppen: config/kdp_publish_reminder_state.json -> "done": true setzen
(oder Bolla sagen "AURORA ist veröffentlicht").

Cron: 0 9 * * * python3 /home/bolla/workspace/scripts/kdp_publish_reminder.py
"""
import json, urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/kdp_publish_reminder_state.json")
FIRE_FROM = date(2026, 6, 20)
INTERVAL_DAYS = 2          # alle 2 Tage erneut
MAX_REMINDERS = 7          # Sicherheitsnetz: nach ~14 Tagen Ruhe

def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id":CHRIS,"text":text,"parse_mode":"Markdown",
                         "disable_web_page_preview":True}).encode(),
        headers={"Content-Type":"application/json"}), timeout=20)

def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    if st.get("done"):
        return
    today = date.today()
    if today < FIRE_FROM:
        return
    count = st.get("count", 0)
    if count >= MAX_REMINDERS:
        return
    last = st.get("last_sent")
    if last:
        if (today - date.fromisoformat(last)).days < INTERVAL_DAYS:
            return
    n = count + 1
    tg("⏰ *KDP-Erinnerung* (Stupser " + str(n) + "/" + str(MAX_REMINDERS) + ")\n\n"
       "Schau mal, ob Amazons Bankprüfung jetzt durch ist:\n\n"
       "👉 [KDP-Bücherregal](https://kdp.amazon.com) → AURORA-Entwurf öffnen → "
       "bis Seite *„Preisgestaltung\"* durchklicken → ist *„Kindle eBook veröffentlichen\"* "
       "nicht mehr ausgegraut? Dann bei **beiden** Büchern (🇩🇪 + 🇬🇧) veröffentlichen! 📚\n\n"
       "Noch grau → kein Problem, ich melde mich in 2 Tagen wieder.\n"
       "_Erledigt? Sag Bolla „AURORA ist veröffentlicht\", dann ist Ruhe._ 🐾")
    st["count"] = n
    st["last_sent"] = today.isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print(f"Reminder {n}/{MAX_REMINDERS} gesendet")

if __name__ == "__main__":
    main()
