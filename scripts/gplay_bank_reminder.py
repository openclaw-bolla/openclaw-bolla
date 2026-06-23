#!/usr/bin/env python3
"""
Google-Play-Books Bankbestätigung-Reminder (wiederkehrend bis erledigt)
Google sendet nach Eingabe der Bankdaten (23.06.2026) eine Mini-Testzahlung
(paar Cent) aufs Deutsche-Bank-Konto. Chris muss den genauen Betrag im
Google Play Partner Center eingeben, um das Konto zu bestätigen.

Erinnert ab 27.06.2026 (nach ~3 Arbeitstagen) per Telegram, alle 2 Tage,
bis Chris stoppt. Datums-Check (nicht uhrzeitgebunden) → übersteht aus-PC.

Stoppen: config/gplay_bank_reminder_state.json -> "done": true
(oder Bolla sagen "Google-Play-Bank ist bestätigt").

Cron: 0 9 * * * python3 /home/bolla/workspace/scripts/gplay_bank_reminder.py
"""
import json, urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/gplay_bank_reminder_state.json")
FIRE_FROM = date(2026, 6, 27)   # ~3 Arbeitstage nach Bankdaten-Eingabe (23.06.)
INTERVAL_DAYS = 2
MAX_REMINDERS = 5

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
    if last and (today - date.fromisoformat(last)).days < INTERVAL_DAYS:
        return
    n = count + 1
    tg("⏰ *Google-Play-Bank prüfen* (Stupser " + str(n) + "/" + str(MAX_REMINDERS) + ")\n\n"
       "Schau mal auf deinen *Deutsche-Bank*-Kontoauszug — ist eine "
       "Mini-Testzahlung von *GOOGLE* (paar Cent) eingegangen?\n\n"
       "✅ *Ja* → Betrag merken → [Partner Center](https://play.google.com/books/publish) → "
       "Zahlungscenter → Bankkonto *bestätigen* → Betrag eingeben. Dann sind Auszahlungen scharf.\n"
       "❌ *Noch nicht* → kein Problem, ich melde mich in 2 Tagen wieder.\n\n"
       "💶 *Wenn du eh im Partner Center bist:* AURORA *DE* steht auf krummen "
       "*5,34 €* — beim DE-Eintrag den EUR-Preis direkt auf *4,99 €* setzen "
       "(rund + passt zur EN-Ausgabe 4,69 €).\n\n"
       "_Erledigt? Sag Bolla „Google-Play-Bank ist bestätigt\", dann ist Ruhe._ 🐾")
    st["count"] = n
    st["last_sent"] = today.isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print(f"Reminder {n}/{MAX_REMINDERS} gesendet")

if __name__ == "__main__":
    main()
