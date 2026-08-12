#!/usr/bin/env python3
"""
Wiederkehrender Reminder: KI-Tool-Verfügbarkeit für Praktika gegenchecken.
MS ändert Copilot/Bing Image Creator/Designer laufend (Login-Pflicht, Kontingente) - siehe
[[feedback_praktikum_geraete_check]], ausgelöst durch den Copilot-Bildgenerierungs-Ausfall vom
12.08.2026. Erinnert Chris alle 14 Tage per Telegram, kurz zu testen, was aktuell an den
Schulgeräten (Win11-PCs / Win10-Laptops mit Office 2010) ohne Schüler-Account funktioniert -
bevor das nächste bildlastige Praktikum gebaut wird.

Rein zeitbasiert, kein technischer Verfügbarkeits-Check (MS bietet dafür keine verlässliche API) -
das ist bewusst eine Erinnerung an Chris, selbst kurz zu testen, keine Automatisierung des Tests.

Cron: 0 8 * * 2 python3 /home/bolla/workspace/scripts/praktikum_geraete_check_reminder.py
(nur Di morgens geprüft - Chris' Korrektur 12.08.2026: Do macht keinen Sinn, Di reicht -
feuert aber nur, wenn INTERVAL_DAYS seit dem letzten Mal um sind)
"""
import json
from pathlib import Path
from datetime import date
import urllib.request

CFGDIR = Path("/home/bolla/workspace/config")
TG = json.loads((CFGDIR / "telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
STATE = CFGDIR / "praktikum_geraete_check_reminder_state.json"
INTERVAL_DAYS = 14


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                         "disable_web_page_preview": True}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    last = st.get("last_sent")
    today = date.today()
    if last:
        days_since = (today - date.fromisoformat(last)).days
        if days_since < INTERVAL_DAYS:
            return
    tg("🖥️ *Praktikum-Geräte-Check* (alle 14 Tage)\n\n"
       "MS ändert Copilot/Designer/Bing Image Creator laufend (Login-Pflicht, Kontingente). "
       "Falls demnächst ein neues bildlastiges Praktikum ansteht: kurz an PC (Win11) und Laptop "
       "(Win10, Office 2010) testen, was aktuell ohne Schüler-Account funktioniert, dann sag mir "
       "kurz Bescheid, ich pass die Praktikums-HTML entsprechend an. 🐾")
    st["last_sent"] = today.isoformat()
    STATE.write_text(json.dumps(st, indent=2))
    print("Praktikum-Geraete-Check-Reminder gesendet")


if __name__ == "__main__":
    main()
