#!/usr/bin/env python3
"""
Release Watcher — prüft ob Chris' Songs live sind.
Primär: Spotify API (braucht Premium). Fallback: iTunes API.
"""
import json
import os
import requests
import time
from datetime import datetime

CONFIG_DIR = "/home/bolla/workspace/config"
CREDENTIALS_FILE = f"{CONFIG_DIR}/spotify_credentials.json"
KNOWN_TRACKS_FILE = f"{CONFIG_DIR}/spotify_known_tracks.json"
TELEGRAM_CONFIG = f"{CONFIG_DIR}/telegram_bot.json"
LOG_FILE = "/home/bolla/workspace/logs/spotify_watcher.log"

RELEASED_DIR = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_RouteNote/released"


def get_tracklist():
    """Liest alle eingereichten Songs aus dem released/-Ordner."""
    if not os.path.isdir(RELEASED_DIR):
        return []
    return sorted([
        f.replace("_320.mp3", "")
        for f in os.listdir(RELEASED_DIR)
        if f.endswith("_320.mp3")
    ])


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")


def send_telegram(bot_token, chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
        timeout=10
    )


def is_our_artist(name):
    return "stingingwallofsounds" in name.lower().replace(" ", "")


# --- Spotify ---

def get_spotify_token(client_id, client_secret):
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
        timeout=10
    )
    r.raise_for_status()
    return r.json().get("access_token")


def search_spotify(token, artist_name):
    r = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": f"artist:{artist_name}", "type": "track", "limit": 50, "market": "DE"},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15
    )
    if r.status_code == 403:
        return None, "premium_required"
    r.raise_for_status()
    found = {}
    for t in r.json().get("tracks", {}).get("items", []):
        artists = [a["name"] for a in t.get("artists", [])]
        if any(is_our_artist(a) for a in artists):
            found[t["id"]] = {
                "name": t["name"],
                "artist": ", ".join(artists),
                "album": t["album"]["name"],
                "release_date": t["album"].get("release_date", ""),
                "spotify_url": t["external_urls"].get("spotify", ""),
                "source": "spotify"
            }
    return found, None


# --- iTunes Fallback ---

def search_itunes():
    found = {}
    for variant in ["Stinging Wall Of Sounds", "StingingWallOfSounds"]:
        r = requests.get(
            "https://itunes.apple.com/search",
            params={"term": variant, "entity": "song", "limit": 200, "country": "DE"},
            timeout=15
        )
        r.raise_for_status()
        for t in r.json().get("results", []):
            if is_our_artist(t.get("artistName", "")):
                tid = str(t["trackId"])
                found[tid] = {
                    "name": t["trackName"],
                    "artist": t.get("artistName", ""),
                    "album": t.get("collectionName", ""),
                    "release_date": t.get("releaseDate", "")[:10],
                    "spotify_url": t.get("trackViewUrl", ""),
                    "source": "itunes"
                }
        time.sleep(0.5)
    return found


def main():
    with open(TELEGRAM_CONFIG) as f:
        tg = json.load(f)
    with open(CREDENTIALS_FILE) as f:
        creds = json.load(f)
    bot_token = tg["bot_token"]
    chat_id = tg["group_chat_id"]

    if os.path.exists(KNOWN_TRACKS_FILE):
        with open(KNOWN_TRACKS_FILE) as f:
            known = json.load(f)
    else:
        known = {"tracks": {}}

    known_ids = set(known.get("tracks", {}).keys())

    try:
        current = None
        source = "itunes"

        # Spotify versuchen
        try:
            token = get_spotify_token(creds["client_id"], creds["client_secret"])
            result, err = search_spotify(token, "StingingWallOfSounds")
            if err == "premium_required":
                log("Spotify API noch nicht freigeschaltet, nutze iTunes")
            else:
                current = result
                source = "spotify"
        except Exception as e:
            log(f"Spotify Fehler: {e}, nutze iTunes")

        if current is None:
            current = search_itunes()

        new_ids = set(current.keys()) - known_ids
        new_found = [current[tid] for tid in new_ids]

        tracklist = get_tracklist()

        if new_found:
            lines = [f"🎵 <b>{len(new_found)} Song(s) jetzt live!</b>\n"]
            for t in new_found:
                label = "Spotify" if t["source"] == "spotify" else "Apple Music"
                lines.append(f"• <b>{t['name']}</b> ({t['release_date']})\n  {label}: {t['spotify_url']}")
                log(f"LIVE: {t['name']} ({t['release_date']}) via {source}")
            send_telegram(bot_token, chat_id, "\n".join(lines))
        else:
            log(f"Check via {source}. Live: {len(current)}/{len(tracklist)}, ausstehend: {len(tracklist)-len(current)}")

        known["tracks"] = current
        known["last_check"] = datetime.now().isoformat()
        known["last_source"] = source
        with open(KNOWN_TRACKS_FILE, "w") as f:
            json.dump(known, f, indent=2, ensure_ascii=False)

    except Exception as e:
        log(f"FEHLER: {e}")


if __name__ == "__main__":
    main()
