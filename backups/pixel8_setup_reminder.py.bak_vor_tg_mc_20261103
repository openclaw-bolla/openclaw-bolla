#!/usr/bin/env python3
"""Pixel-8-Einrichtungs-Reminder (Chris 21.09.2026: 'aktiv daran erinnern', Einrichtung Mi 23./Do 24.09.).
Datumsbasiert, jede Stufe feuert genau EINMAL (State). Cron: 0 15,18 * * *  (uebersteht ausgeschalteten Rechner).
Stoppen: config/pixel8_setup_reminder_state.json -> "p8_done": true.  Plan/Notizen: [[project_pixel8_p20_ersatz]]"""
import json, urllib.request
from pathlib import Path
from datetime import datetime

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
STATE = Path("/home/bolla/workspace/config/pixel8_setup_reminder_state.json")

def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                         "disable_web_page_preview": True}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)

STEPS = [  # (ab Datum, ab Stunde, Key, Text)
 ("2026-09-22", 18, "prep",
  "📱 *Pixel 8 — kleine Vorbereitung* (2 Min)\n\n"
  "Das P8 kommt Mi/Do. Bitte bereitlegen:\n"
  "1️⃣ *Echte Karten:* Deutsche Bank Card Plus, Allianz Privatschutzcard, Gesundheitskarte, Rusta- und Lindt-Kundenkarte (falls Wallet sie nicht selbst mitbringt)\n"
  "2️⃣ Duo bleibt an und geladen (für Bank-Freigaben & IONOS-Login)\n"
  "3️⃣ Wenn das P8 da ist: sag \"p8 ist da\" — dann gehen wir Schritt für Schritt vor, *als Erstes Akku-Check*. 🐾"),
 ("2026-09-23", 15, "day1",
  "📱 *Pixel 8 — heute ist Einrichtungstag?* 🔋\n\n"
  "Wenn das P8 da ist: sag \"p8 ist da\". Ich führe dich Schritt für Schritt: *1. Akku ≥ 80 % prüfen* (vor allem anderen!), "
  "2. Einrichtung mit Kopieren vom Duo (Renate-Konto mit; nur Dateimanager+ & YourPass abwählen, Spiele/Xbox bleiben), 3. Konten/Authenticator/IONOS, "
  "4. Wallet: Deutsche Bank Card Plus + Allianz/Gesundheitskarte/Rusta/Lindt, 5. pushTAN + BestSign als Backup, 6. mmp/mmc-Links + App-Ordner selbst neu anlegen, 7. SIM zuletzt. 🐾"),
 ("2026-09-24", 15, "day2",
  "📱 *Pixel 8 — Nachfrage* Ist das P8 schon eingerichtet? Falls nicht: sag \"p8 ist da\", ich mache mit dir alles Schritt für Schritt "
  "(Start immer mit dem Akku-Check). Wenn's schon durch ist, sag \"p8 fertig\", dann stelle ich die Erinnerungen ab. 🐾"),
]

def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {}
    if st.get("p8_done"):
        return
    now = datetime.now()
    for d, h, key, text in STEPS:
        if st.get(key):
            continue
        y, m, dd = map(int, d.split("-"))
        if (now.year, now.month, now.day) > (y, m, dd) or ((now.year, now.month, now.day) == (y, m, dd) and now.hour >= h):
            # nur die zeitlich passende, aktuellste faellige Stufe senden (keine Nachholflut)
            later_due = any(
                (not st.get(k2)) and ((now.year, now.month, now.day) > tuple(map(int, d2.split("-"))) or
                ((now.year, now.month, now.day) == tuple(map(int, d2.split("-"))) and now.hour >= h2))
                for d2, h2, k2, _ in STEPS if d2 > d)
            st[key] = now.isoformat(timespec="minutes")
            if not later_due:
                tg(text)
                print("Pixel8-Reminder gesendet:", key)
            STATE.write_text(json.dumps(st, indent=2))
            return

if __name__ == "__main__":
    main()
