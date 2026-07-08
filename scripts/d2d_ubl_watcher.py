#!/usr/bin/env python3
"""
D2D-Universal-Link-Wächter (Amazon/Apple/Kobo etc. hinter books2read.com/u/...)
Prüft wöchentlich per JSON-API, ob die AURORA-Universal-Links echte Store-
Verknüpfungen haben.

Stand 09.07.2026: Erst über HTML-Scraping geprüft — das war unzuverlässig,
weil die Store-Icons per JS nachgeladen werden und der Text "Add additional
Stores" IMMER auf der Seite steht (auch mit Stores drin) -> false negative.
Jetzt auf die echte API umgestellt: /links/api/ubls/<slug>/stores/public/
liefert eine JSON-Liste, leer = keine Stores hinterlegt.

Amazon taucht hier NIE automatisch auf (D2D vertreibt nicht zu Amazon,
Chris nutzt dafür separat KDP direkt) - das ist normal, kein Fehler.

Logik: Liste leer -> still. Liste nicht leer und noch nicht gemeldet ->
Telegram-Alarm mit Store-Liste.

Cron: 0 9 * * 1 python3 /home/bolla/workspace/scripts/d2d_ubl_watcher.py
"""

import json
import sys
from pathlib import Path
import requests

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT_TOKEN = CFG["bot_token"]
CHRIS_ID = CFG["chris_id"]

STATE_PATH = Path("/home/bolla/workspace/config/d2d_ubl_state.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

LINKS = {
    "EN": "4A9A6o",
    "DE": "bz0nwj",
}
API = "https://books2read.com/links/api/ubls/{slug}/stores/public/"


def tg(text):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                      json={"chat_id": CHRIS_ID, "text": text, "parse_mode": "Markdown",
                            "disable_web_page_preview": True},
                      timeout=20)
    except Exception as e:
        print("Telegram-Fehler:", e)


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}


def save_state(s):
    STATE_PATH.write_text(json.dumps(s, indent=2, ensure_ascii=False))


def main():
    state = load_state()

    for lang, slug in LINKS.items():
        key = lang.lower()
        st = state.get(key, {"alerted": False, "last_count": 0})

        try:
            r = requests.get(API.format(slug=slug), headers=UA, timeout=30)
            r.raise_for_status()
            stores = r.json()
        except Exception as e:
            print(f"Fetch-Fehler {lang} ({slug}): {e}", file=sys.stderr)
            continue

        names = sorted({s.get("app_name", "?") for s in stores})
        count = len(names)

        if count > 0 and not st.get("alerted"):
            tg(f"📚 *D2D-Link-Update ({lang})!*\n\n"
               f"Der Universal-Link für die {lang}-Ausgabe hat jetzt {count} "
               f"echte Store-Links! 🎉\n\n" + "\n".join(f"• {n}" for n in names) +
               f"\n\n👉 https://books2read.com/u/{slug}\n"
               f"(Amazon fehlt hier normal — läuft separat über KDP. 🐾)")
            st["alerted"] = True
            print(f"{lang}: ALERT gesendet — {count} Stores gefunden.")
        elif count == 0:
            if st.get("last_count") != 0:
                st["alerted"] = False
            print(f"{lang}: unverändert, weiterhin keine Stores hinterlegt.")
        else:
            print(f"{lang}: {count} Stores, bereits gemeldet.")

        st["last_count"] = count
        state[key] = st

    save_state(state)


if __name__ == "__main__":
    main()
