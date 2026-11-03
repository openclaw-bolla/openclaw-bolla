#!/usr/bin/env python3
"""
Suno Oster-Songs Reminder (saisonal, ab 01.02.2027)
3 Oster-Songs im Suno_DistroKid-Ordner nennen Klassen-Kürzel (7A/7B/7C) im Text
→ für anonymen Künstler-Release unpassend. Chris will sie vor Ostern 2027
allgemeiner neu generieren (ohne Klassen-Kürzel) und dann bei DistroKid hochladen.
Ostersonntag 2027 = 28.03. → Erinnerung mit ~8 Wochen Vorlauf ab 01.02.2027.

Erinnert ab 01.02.2027 per Telegram, alle 3 Tage, bis Chris stoppt.
Datums-Check (nicht uhrzeitgebunden) → übersteht aus-PC.
Stoppen: config/suno_ostern_reminder_state.json -> "done": true
(oder Bolla sagen "Oster-Songs sind erledigt").
Memory: project_suno_saison_songs.md

Cron: 0 9 * * * python3 /home/bolla/workspace/scripts/suno_ostern_reminder.py
"""
import json, urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/suno_ostern_reminder_state.json")
FIRE_FROM = date(2027, 2, 1)    # ~8 Wochen vor Ostersonntag 28.03.2027
INTERVAL_DAYS = 3
MAX_REMINDERS = 6

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
    tg("🐣 *Suno Oster-Songs neu machen* (Stupser " + str(n) + "/" + str(MAX_REMINDERS) + ")\n\n"
       "Ostersonntag ist am *28.03.2027* — Zeit, die 3 Oster-Songs *allgemeiner* "
       "neu zu generieren (ohne Klassen-Kürzel 7A/7B/7C), dann ab zu DistroKid:\n\n"
       "• *Bunny Hop Hustle* (hatte 7b)\n"
       "• *Der verrückte Hasenhüpfer* (hatte 7b)\n"
       "• *Hoppin' Into Easter* (hatte 7C)\n\n"
       "Vorlauf einplanen: Neugenerierung + DistroKid-Review dauert.\n"
       "_Erledigt? Sag Bolla „Oster-Songs sind erledigt\", dann ist Ruhe._ 🐾")
    st["count"] = n
    st["last_sent"] = today.isoformat()
    STATE.write_text(json.dumps(st, indent=2))

if __name__ == "__main__":
    main()
