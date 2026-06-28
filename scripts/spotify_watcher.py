#!/usr/bin/env python3
"""
Bollawave Release-Watcher — prüft, ob die Singles live sind, meldet via Telegram.
Apple/iTunes-API (gratis, ohne Auth) läuft IMMER. Spotify zusätzlich, FALLS
config/spotify_credentials.json existiert (kostenlose Spotify-Developer-App:
client_id + client_secret). Ohne Credentials einfach nur Apple — kein Crash.

Artist: Bollawave (Suno→DistroKid Cleanstart). Stoppt nicht von selbst —
meldet jeden NEU entdeckten Track einmal.
Cron: 0 */6 * * * python3 /home/bolla/workspace/scripts/spotify_watcher.py
"""
import json
import os
import requests
from datetime import datetime

CONFIG_DIR = "/home/bolla/workspace/config"
CREDENTIALS_FILE = f"{CONFIG_DIR}/spotify_credentials.json"      # optional
KNOWN_TRACKS_FILE = f"{CONFIG_DIR}/bollawave_known_tracks.json"
TELEGRAM_CONFIG = f"{CONFIG_DIR}/telegram_bot.json"
LOG_FILE = "/home/bolla/workspace/logs/spotify_watcher.log"
TRACKS_DIR = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid/Cleanstart_8"

ARTIST = "Bollawave"


def get_tracklist():
    if not os.path.isdir(TRACKS_DIR):
        return []
    return sorted(f.rsplit(".", 1)[0] for f in os.listdir(TRACKS_DIR) if f.endswith(".mp3"))


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def send_telegram(bot_token, chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML",
              "disable_web_page_preview": True},
        timeout=10,
    )


def is_our_artist(name):
    return "bollawave" in (name or "").lower().replace(" ", "")


# --- Spotify (optional) ---
def search_spotify(client_id, client_secret):
    r = requests.post("https://accounts.spotify.com/api/token",
                      data={"grant_type": "client_credentials"},
                      auth=(client_id, client_secret), timeout=10)
    r.raise_for_status()
    token = r.json().get("access_token")
    # limit max 10: diese App (Client-Credentials ohne Extended Quota) liefert ab limit>10
    # "400 Invalid limit". Apple/iTunes (limit=200) ist eh der Hauptweg; Spotify nur Bonus.
    r = requests.get("https://api.spotify.com/v1/search",
                     params={"q": f'artist:{ARTIST}', "type": "track", "limit": 10, "market": "DE"},
                     headers={"Authorization": f"Bearer {token}"}, timeout=15)
    r.raise_for_status()
    found = {}
    for t in r.json().get("tracks", {}).get("items", []):
        artists = [a["name"] for a in t.get("artists", [])]
        if any(is_our_artist(a) for a in artists):
            found["sp_" + t["id"]] = {
                "name": t["name"], "release_date": t["album"].get("release_date", ""),
                "url": t["external_urls"].get("spotify", ""), "source": "Spotify"}
    return found


# --- Apple/iTunes (gratis, immer) ---
def search_itunes():
    found = {}
    r = requests.get("https://itunes.apple.com/search",
                     params={"term": ARTIST, "entity": "song", "limit": 200, "country": "DE"},
                     timeout=15)
    r.raise_for_status()
    for t in r.json().get("results", []):
        if is_our_artist(t.get("artistName", "")):
            found["it_" + str(t["trackId"])] = {
                "name": t["trackName"], "release_date": t.get("releaseDate", "")[:10],
                "url": t.get("trackViewUrl", ""), "source": "Apple Music"}
    return found


def main():
    tg = json.loads(open(TELEGRAM_CONFIG).read())
    bot_token, chat_id = tg["bot_token"], tg["chris_id"]

    known = json.loads(open(KNOWN_TRACKS_FILE).read()) if os.path.exists(KNOWN_TRACKS_FILE) else {"tracks": {}}
    known_ids = set(known.get("tracks", {}).keys())

    current, sources = {}, []
    try:
        current.update(search_itunes()); sources.append("Apple")
    except Exception as e:
        log(f"iTunes Fehler: {e}")
    if os.path.exists(CREDENTIALS_FILE):
        try:
            c = json.loads(open(CREDENTIALS_FILE).read())
            current.update(search_spotify(c["client_id"], c["client_secret"])); sources.append("Spotify")
        except Exception as e:
            log(f"Spotify Fehler: {e}")

    new = [current[k] for k in (set(current) - known_ids)]
    tracklist = get_tracklist()
    if new:
        lines = [f"🎵 <b>Bollawave: {len(new)} Song(s) jetzt LIVE!</b>\n"]
        for t in new:
            lines.append(f"• <b>{t['name']}</b> ({t['release_date']})\n  {t['source']}: {t['url']}")
            log(f"LIVE: {t['name']} via {t['source']}")
        send_telegram(bot_token, chat_id, "\n".join(lines))
    else:
        log(f"Check via {'+'.join(sources) or 'nichts'}. Live: {len(current)}/{len(tracklist)}")

    known["tracks"] = current
    known["last_check"] = datetime.now().isoformat()
    json.dump(known, open(KNOWN_TRACKS_FILE, "w"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
