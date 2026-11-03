#!/usr/bin/env python3
"""
Google-Play-Books Konto-Richtlinienprüfung-Reminder (wiederkehrend bis erledigt)

Stand 24.06.2026: Bankkonto bestätigt ✅. Letzter Blocker fürs Live-Gehen ist
Googles Konto-Richtlinienprüfung ("vorläufige Richtlinienüberprüfung",
gelber Banner im Buchkatalog) — kann bis zu 30 Tage dauern (ab ~23.06.,
also spätestens ~23.07.2026). Bücher stehen solange auf "Kontoüberprüfung
steht aus", Bearbeitungen (z.B. Preis) sind gesperrt.

Erinnert ab 08.07.2026 (nach ~2 Wochen) per Telegram, alle 4 Tage, bis Chris
stoppt. Datums-Check (nicht uhrzeitgebunden) -> übersteht aus-PC.

Wenn die Prüfung durch ist:
  1. AURORA DE + EN gehen live
  2. DE-Preis auf glatte 4,99 EUR setzen (war auf 5,34 gesperrt)
  3. Bolla: Store-Links erfassen + Google Play als 7. Kanal in Checkliste

Stoppen: config/gplay_policy_reminder_state.json -> "done": true
(oder Bolla sagen "Google Play ist live" / "Richtlinienpruefung ist durch").

Cron: 0 9 * * * python3 /home/bolla/workspace/scripts/gplay_policy_reminder.py
"""
import json, urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/gplay_policy_reminder_state.json")
FIRE_FROM = date(2026, 7, 8)    # ~2 Wochen nach Konto-Anlage (23.06.); Prüfung kann früher durch sein
INTERVAL_DAYS = 4
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
    tg("⏰ *Google Play — Richtlinienprüfung durch?* (Stupser " + str(n) + "/" + str(MAX_REMINDERS) + ")\n\n"
       "Schau mal ins [Partner Center](https://play.google.com/books/publish) → *Buchkatalog*:\n"
       "Ist der *gelbe Banner* (\"vorläufige Richtlinienüberprüfung\") weg und stehen AURORA "
       "*DE + EN* auf *live/aktiv* statt \"Kontoüberprüfung steht aus\"?\n\n"
       "✅ *Ja, durch!* → zwei Handgriffe:\n"
       "   1. AURORA *DE* Preis von krummen *5,34 €* auf glatte *4,99 €* (EUR direkt, nicht aus USD rechnen).\n"
       "   2. Sag Bolla *„Google Play ist live\"* → ich erfasse die Store-Links + häng Google Play als 7. Kanal in die AURORA-Checkliste.\n"
       "❌ *Noch nicht* → alles ok, läuft bis zu 30 Tage (~23.07.). Ich melde mich in 4 Tagen wieder.\n\n"
       "_Ruhe ist, sobald du sagst „Google Play ist live\"._ 🐾")
    st["count"] = n
    st["last_sent"] = today.isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print(f"Reminder {n}/{MAX_REMINDERS} gesendet")

if __name__ == "__main__":
    main()
