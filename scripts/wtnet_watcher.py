#!/usr/bin/env python3
"""
wtnet Watcher - chrismandel@wtnet.de
- Löscht Spam-Mails ([*** SPAM ***]) alle 15 Minuten
- Läuft parallel zum Token Watcher
"""

import imaplib
import json
import logging
import sys
import time
from email.header import decode_header
from pathlib import Path

WORKSPACE = Path("/home/bolla/.openclaw/workspace")
CONFIG_FILE = WORKSPACE / "config/wtnet_account.json"
LOG_FILE = WORKSPACE / "logs/wtnet_watcher.log"
CHECK_INTERVAL = 15 * 60  # 15 Minuten

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("wtnet_watcher")


def load_config() -> dict:
    with open(CONFIG_FILE) as f:
        return json.load(f)


def delete_spam(cfg: dict):
    """Löscht alle [*** SPAM ***] Mails im Posteingang."""
    try:
        m = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
        m.login(cfg["email"], cfg["password"])
        m.select("INBOX")

        status, data = m.search(None, "SUBJECT", '"SPAM"')
        ids = data[0].split()

        if not ids:
            log.info("Kein Spam gefunden.")
        else:
            log.info(f"🗑️  {len(ids)} Spam-Mail(s) gefunden, lösche...")
            for mid in ids:
                m.store(mid, "+FLAGS", "\\Deleted")
            m.expunge()
            log.info(f"✅ {len(ids)} Spam-Mail(s) gelöscht.")

        m.logout()
    except Exception as e:
        log.error(f"Fehler beim Spam-Löschen: {e}")


def check_once():
    cfg = load_config()
    delete_spam(cfg)


def main():
    log.info("=" * 60)
    log.info("wtnet Watcher gestartet")
    log.info(f"Konto: {load_config()['email']}")
    log.info(f"Überprüfe alle {CHECK_INTERVAL // 60} Minuten")
    log.info("=" * 60)

    while True:
        try:
            check_once()
        except Exception as e:
            log.error(f"Fehler: {e}", exc_info=True)
        log.info(f"Nächste Prüfung in {CHECK_INTERVAL // 60} Minuten.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
