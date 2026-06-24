#!/usr/bin/env python3
"""
Spotify-API-Zugriffs-Wächter (temporär).
Neue Spotify-Apps werden erst nach Stunden für Daten-Calls freigeschaltet
("Active premium subscription required for the owner of the app").
Dieser Check testet alle paar Stunden, ob der Zugriff offen ist, und meldet
GENAU EINMAL via Telegram, sobald es klappt. Danach bleibt er still.

Cron: 0 */2 * * * python3 /home/bolla/workspace/scripts/spotify_access_check.py
Wenn freigeschaltet, kann dieser Cron entfernt werden (der eigentliche
spotify_watcher nutzt die Credentials dann automatisch).
"""
import json
import os
import requests

CONFIG_DIR = "/home/bolla/workspace/config"
CREDENTIALS_FILE = f"{CONFIG_DIR}/spotify_credentials.json"
TELEGRAM_CONFIG = f"{CONFIG_DIR}/telegram_bot.json"
STATE_FILE = "/home/bolla/workspace/data/.spotify_access_ok"


def telegram(text):
    tg = json.loads(open(TELEGRAM_CONFIG).read())
    requests.post(
        f"https://api.telegram.org/bot{tg['bot_token']}/sendMessage",
        json={"chat_id": tg["chris_id"], "text": text, "parse_mode": "Markdown"},
        timeout=10,
    )


def main():
    if os.path.exists(STATE_FILE):
        return  # schon gemeldet, nichts mehr zu tun
    if not os.path.exists(CREDENTIALS_FILE):
        return
    c = json.loads(open(CREDENTIALS_FILE).read())
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(c["client_id"], c["client_secret"]), timeout=10,
    )
    if r.status_code != 200:
        return
    tok = r.json().get("access_token")
    s = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": "Bollawave", "type": "artist", "limit": 1},
        headers={"Authorization": f"Bearer {tok}"}, timeout=15,
    )
    if s.status_code == 200:
        open(STATE_FILE, "w").write("ok")
        telegram("✅ *Spotify-API-Zugriff ist jetzt frei!*\n"
                 "Das Bollawave-Tracking läuft ab sofort auch direkt über Spotify "
                 "(nicht nur Apple). Der Zugriffs-Wächter kann jetzt raus.")


if __name__ == "__main__":
    main()
