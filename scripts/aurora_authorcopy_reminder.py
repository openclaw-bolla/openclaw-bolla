#!/usr/bin/env python3
"""
AURORA Autorenexemplar-Reminder (einmalig)
Erinnert Chris ab dem 25.06.2026 morgens per Telegram, nochmal nach dem
Amazon.de-Marktplatz im KDP-Autorenexemplar-Bestellprozess zu schauen —
am 24.06. fehlte .de noch (Taschenbuch gerade erst live, Marktplatz-Liste
hinkte hinterher).

Datums-basiert (übersteht ausgeschalteten Rechner). Cron läuft mehrmals
morgens, das Script feuert aber genau EINMAL (State -> done).

Cron: 0 7-11 * * * python3 /home/bolla/workspace/scripts/aurora_authorcopy_reminder.py
Stoppen/Erledigt: config/aurora_authorcopy_reminder_state.json -> "done": true
"""
import json, urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/aurora_authorcopy_reminder_state.json")
FIRE_FROM = date(2026, 6, 25)

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
    if date.today() < FIRE_FROM:
        return
    tg("📚 *AURORA — Autorenexemplar* ⏰\n\n"
       "Gestern fehlte *Amazon.de* noch im Marktplatz-Dropdown. Heute sollte's da sein!\n\n"
       "👉 [KDP-Bücherregal](https://kdp.amazon.com) → Taschenbuch 🇩🇪 → „…\" → "
       "*Autorenexemplar bestellen* → Marktplatz **Amazon.de** wählen → Menge *1*.\n\n"
       "Dein Preis: *≈ 6,11 €* Druckkosten + Versand. Erst das eine Probe-Exemplar "
       "prüfen, dann die Geschenke für die Kinder nachordern. 🎁\n\n"
       "_Falls .de immer noch fehlt: einfach Bescheid sagen, dann nehmen wir Amazon.fr/.it (EU-Druck, Euro)._ 🐾")
    st["done"] = True
    st["sent_on"] = date.today().isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print("Autorenexemplar-Reminder gesendet")

if __name__ == "__main__":
    main()
