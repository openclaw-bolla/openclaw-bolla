#!/usr/bin/env python3
"""
itslearning Geburtstagssong-Namen-Reminder (woechentlich, jeden Montag)
Chris' Auftrag 28.09.2026: jeden Montag erinnern, dass er die 2 Schuelernamen fuer Mittwoch und
2 fuer Donnerstag liefern soll (Geburtstagssong-Automatisierung, siehe
[[project_itslearning_automation]] / scripts/itslearning_send_private_song.py) - aber NUR wenn
in dieser Woche ueberhaupt Schule ist (nicht in den Ferien). Schulwochen-Check laeuft ueber
data/schuljahr2627.json (termine[] hat echte Datumsangaben, Ferien sind dort schon rausgerechnet).

Feuert wirklich nur EINMAL pro Kalenderwoche (State speichert die ISO-Kalenderwoche), auch wenn
der Cron mehrfach morgens laeuft (Reboot-Sicherheit, wie bei den anderen itslearning-Remindern).

Cron: 0 7-11 * * 1 python3 /home/bolla/workspace/scripts/itslearning_geburtstagssong_namen_montag_reminder.py
"""
import json
from pathlib import Path
from datetime import date, timedelta
import urllib.request

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/itslearning_geburtstagssong_namen_montag_reminder_state.json")
SCHULJAHR = Path("/home/bolla/workspace/data/schuljahr2627.json")


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                         "disable_web_page_preview": True}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


def ist_schulwoche(mittwoch, donnerstag):
    """Prueft, ob fuer Mittwoch oder Donnerstag dieser Woche ein echter Unterrichtstermin
    existiert (Ferien sind in termine[] schon rausgerechnet)."""
    termine = json.loads(SCHULJAHR.read_text(encoding="utf-8"))["termine"]
    daten = {t["datum"] for t in termine}
    return mittwoch.isoformat() in daten or donnerstag.isoformat() in daten


def main():
    heute = date.today()
    kw = heute.isocalendar()[1]
    jahr = heute.isocalendar()[0]
    kw_key = f"{jahr}-KW{kw:02d}"

    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    if st.get("last_sent_kw") == kw_key:
        return

    mittwoch = heute + timedelta(days=(2 - heute.weekday()))
    donnerstag = heute + timedelta(days=(3 - heute.weekday()))

    if not ist_schulwoche(mittwoch, donnerstag):
        return

    tg("🎂 *Geburtstagssong — Namen für diese Woche?*\n\n"
       f"Wer ist dran? Bitte 2 Namen für Mittwoch ({mittwoch.strftime('%d.%m.')}) und "
       f"2 Namen für Donnerstag ({donnerstag.strftime('%d.%m.')}) — dann kümmere ich mich "
       "wie besprochen nachmittags um die itslearning-Nachrichten. 🐾")
    st["last_sent_kw"] = kw_key
    STATE.write_text(json.dumps(st, indent=2))
    print("Geburtstagssong-Namen-Montag-Reminder gesendet fuer", kw_key)


if __name__ == "__main__":
    main()
