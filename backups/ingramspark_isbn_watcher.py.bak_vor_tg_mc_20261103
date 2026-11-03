#!/usr/bin/env python3
"""
IngramSpark Gratis-ISBN-Wächter (für Ausländer/Nicht-US)
Prüft monatlich, ob IngramSpark kostenlose ISBNs auch außerhalb der USA anbietet.

Stand 24.06.2026: Gratis-ISBNs nur für US-Selfpublisher. Auf der Seite steht:
"While free ISBNs are only available in the U.S. for now, we're working around
the clock to make free ISBNs available to our global community."

Logik: Solange das Sentinel "only available in the u.s. for now" auf der Seite
steht, ist alles beim Alten -> still. Verschwindet es ODER taucht ein Hinweis
auf internationale Gratis-ISBNs auf -> Telegram-Alarm an Chris.

Chris wollte dranbleiben statt aufzugeben ("noch nicht so schnell aufgeben" 😉).

Cron: 0 9 3 * * python3 /home/bolla/workspace/scripts/ingramspark_isbn_watcher.py
"""

import json
import re
import sys
from pathlib import Path
import requests

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT_TOKEN = CFG["bot_token"]
CHRIS_ID = CFG["chris_id"]

STATE_PATH = Path("/home/bolla/workspace/config/ingramspark_isbn_state.json")
URLS = [
    "https://www.ingramspark.com/free-isbns",
    "https://www.ingramspark.com/faqs",
]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

# Sentinel = solange DAS noch da steht, ist Gratis-ISBN weiter US-only.
# Robust: NUR auf das Verschwinden dieses Satzes reagieren. Keine "Hoffnungs-
# Regex" mehr — die hat versehentlich den Wunschsatz "...to our global
# community" als Treffer gewertet (Fehlalarm 24.06.2026).
SENTINEL = "only available in the u.s. for now"


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
    return {"alerted": False, "last_status": "us_only"}


def save_state(s):
    STATE_PATH.write_text(json.dumps(s, indent=2, ensure_ascii=False))


def fetch_text(url):
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    # grob entmarkupen + Whitespace normalisieren
    txt = re.sub(r"<[^>]+>", " ", r.text)
    txt = re.sub(r"\s+", " ", txt).lower()
    return txt


def main():
    state = load_state()

    sentinel_seen = False
    fetch_ok = False
    for url in URLS:
        try:
            txt = fetch_text(url)
            fetch_ok = True
            if SENTINEL in txt:
                sentinel_seen = True
        except Exception as e:
            print(f"Fetch-Fehler {url}: {e}", file=sys.stderr)

    if not fetch_ok:
        # Seiten nicht erreichbar -> still, nächsten Monat wieder
        print("Keine Seite erreichbar, übersprungen.")
        return

    # Änderung erkannt: Sentinel-Satz verschwunden.
    changed = not sentinel_seen

    if changed and not state.get("alerted"):
        detail = ("\n\nDer bisherige Satz 'only available in the U.S. for now' "
                  "steht nicht mehr auf der Seite — könnte heißen, die Sperre fällt.")
        tg("📚 *IngramSpark-ISBN-Update!*\n\n"
           "Es sieht so aus, als hätte sich die Gratis-ISBN-Regel für "
           "Nicht-US-Autoren geändert! 🎉" + detail + "\n\n"
           "👉 Bitte prüfen: https://www.ingramspark.com/free-isbns\n"
           "(Du wolltest da dranbleiben — hier ist dein Signal. 🐾)")
        state["alerted"] = True
        state["last_status"] = "changed"
        save_state(state)
        print("ALERT gesendet — Policy könnte sich geändert haben.")
    elif not changed:
        # alles beim Alten -> ggf. Reset, falls vorher fälschlich alarmiert
        if state.get("last_status") != "us_only":
            state["last_status"] = "us_only"
            state["alerted"] = False
            save_state(state)
        print("Unverändert: Gratis-ISBN weiterhin nur US. Still.")
    else:
        print("Änderung bereits gemeldet, kein erneuter Alarm.")


if __name__ == "__main__":
    main()
