#!/usr/bin/env python3
"""
Outlook Spam Watcher - ernstmandel@outlook.de
- Löscht Mails mit [*** SPAM ***] im Betreff (Posteingang + alle Ordner)
- Läuft alle 15 Minuten
- Nutzt Microsoft Graph API (Token aus ms_token.json)
"""

import json
import logging
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path("/home/bolla/.openclaw/workspace")
TOKEN_FILE = WORKSPACE / "config/ms_token.json"
LOG_FILE = WORKSPACE / "logs/outlook_spam_watcher.log"
CHECK_INTERVAL = 15 * 60  # 15 Minuten
SPAM_MARKER = "[*** SPAM ***]"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("outlook_spam_watcher")


def load_token() -> str:
    with open(TOKEN_FILE) as f:
        data = json.load(f)
    return data["access_token"]


def graph_get(token: str, url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        log.error(f"GET {url} → {e.code}: {body[:200]}")
        return {}


def graph_delete(token: str, url: str) -> bool:
    req = urllib.request.Request(
        url,
        method="DELETE",
        headers={"Authorization": f"Bearer {token}"}
    )
    try:
        with urllib.request.urlopen(req) as r:
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        log.error(f"DELETE {url} → {e.code}: {body[:200]}")
        return False


def delete_spam_outlook():
    token = load_token()

    # Suche nach Mails mit SPAM-Marker im Betreff (alle Ordner via search)
    # Graph API: /me/messages?$filter=contains(subject,'[*** SPAM ***]')
    # URL-encode the filter
    marker_escaped = SPAM_MARKER.replace("[", "%5B").replace("]", "%5D").replace("*", "%2A").replace(" ", "%20")
    url = f"https://graph.microsoft.com/v1.0/me/messages?$filter=contains(subject,'{marker_escaped}')&$select=id,subject,receivedDateTime&$top=50"

    result = graph_get(token, url)
    messages = result.get("value", [])

    if not messages:
        log.info("Kein Spam gefunden.")
        return

    log.info(f"🗑️  {len(messages)} Spam-Mail(s) gefunden, lösche...")
    deleted = 0
    for msg in messages:
        msg_id = msg["id"]
        subject = msg.get("subject", "?")
        delete_url = f"https://graph.microsoft.com/v1.0/me/messages/{msg_id}"
        if graph_delete(token, delete_url):
            log.info(f"  ✅ Gelöscht: {subject[:80]}")
            deleted += 1
        else:
            log.warning(f"  ❌ Fehler beim Löschen: {subject[:80]}")

    log.info(f"Fertig: {deleted}/{len(messages)} Spam-Mails gelöscht.")


def main():
    log.info("=" * 60)
    log.info("Outlook Spam Watcher gestartet")
    log.info(f"Konto: ernstmandel@outlook.de")
    log.info(f"Marker: {SPAM_MARKER}")
    log.info(f"Überprüfe alle {CHECK_INTERVAL // 60} Minuten")
    log.info("=" * 60)

    while True:
        try:
            delete_spam_outlook()
        except Exception as e:
            log.error(f"Fehler: {e}", exc_info=True)
        log.info(f"Nächste Prüfung in {CHECK_INTERVAL // 60} Minuten.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
