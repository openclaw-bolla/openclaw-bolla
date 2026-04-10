#!/usr/bin/env python3
"""
Spam Watcher — Löscht [*** SPAM ***] Mails in beiden Postfächern.
- Outlook (ernstmandel@outlook.de) via Microsoft Graph API
- wtnet (chrismandel@wtnet.de) via IMAP
Wird alle 15 Minuten per Cron ausgeführt.
"""

import imaplib
import json
import logging
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path("/home/bolla/.openclaw/workspace")
MS_TOKEN_FILE = WORKSPACE / "config/ms_token.json"
WTNET_CONFIG = WORKSPACE / "config/wtnet_account.json"
LOG_FILE = WORKSPACE / "logs/spam_watcher.log"
CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"

SPAM_PATTERNS = [
    "[*** SPAM ***]",
    "[**SPAM**]",
    "[SPAM]",
]

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("spam_watcher")


# ── Outlook (Microsoft Graph) ────────────────────────────────────────────────

def refresh_ms_token() -> str:
    """Refresht den Microsoft Graph Access Token."""
    with open(MS_TOKEN_FILE) as f:
        token_data = json.load(f)

    data = (
        f"client_id={CLIENT_ID}"
        f"&grant_type=refresh_token"
        f"&refresh_token={token_data['refresh_token']}"
        f"&scope=https://graph.microsoft.com/Mail.Read"
        f"%20https://graph.microsoft.com/Mail.ReadWrite"
        f"%20offline_access"
    ).encode()

    req = urllib.request.Request(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        data=data,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as r:
        new_token = json.loads(r.read())

    with open(MS_TOKEN_FILE, "w") as f:
        json.dump(new_token, f, indent=2)

    return new_token["access_token"]


def graph_get(token: str, url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log.error(f"GET {url} → {e.code}: {e.read().decode()[:200]}")
        return {}


def graph_delete(token: str, url: str) -> bool:
    req = urllib.request.Request(url, method="DELETE", headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return True
    except urllib.error.HTTPError as e:
        log.error(f"DELETE → {e.code}: {e.read().decode()[:200]}")
        return False


def is_spam(subject: str) -> bool:
    s = subject.upper()
    return any(p.upper() in s for p in SPAM_PATTERNS) or "*** SPAM" in s or "SPAM ***" in s


def clean_outlook():
    """Löscht Spam in Outlook (alle Ordner)."""
    log.info("[Outlook] Prüfe ernstmandel@outlook.de...")
    token = refresh_ms_token()

    # Alle Ordner holen
    folders = graph_get(token, "https://graph.microsoft.com/v1.0/me/mailFolders?$top=50")
    skip = {"Deleted Items", "Gesendete Elemente", "Sent Items", "Drafts", "Entwürfe", "Outbox"}
    total = 0

    for folder in folders.get("value", []):
        fname = folder.get("displayName", "")
        if fname in skip:
            continue
        fid = folder["id"]
        url = f"https://graph.microsoft.com/v1.0/me/mailFolders/{fid}/messages?$select=id,subject&$top=50"

        while url:
            data = graph_get(token, url)
            for mail in data.get("value", []):
                subject = mail.get("subject") or ""
                if is_spam(subject):
                    if graph_delete(token, f"https://graph.microsoft.com/v1.0/me/messages/{mail['id']}"):
                        log.info(f"  🗑️  [{fname}] {subject[:70]}")
                        total += 1
            url = data.get("@odata.nextLink")

    if total:
        log.info(f"[Outlook] ✅ {total} Spam-Mail(s) gelöscht.")
    else:
        log.info("[Outlook] Kein Spam.")


# ── wtnet (IMAP) ─────────────────────────────────────────────────────────────

def clean_wtnet():
    """Löscht Spam in wtnet Postfach."""
    log.info("[wtnet] Prüfe chrismandel@wtnet.de...")
    with open(WTNET_CONFIG) as f:
        cfg = json.load(f)

    try:
        m = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
        m.login(cfg["email"], cfg["password"])
        m.select("INBOX")

        status, data = m.search(None, "SUBJECT", '"SPAM"')
        ids = data[0].split()

        if ids:
            log.info(f"[wtnet] 🗑️  {len(ids)} Spam-Mail(s) gefunden, lösche...")
            for mid in ids:
                m.store(mid, "+FLAGS", "\\Deleted")
            m.expunge()
            log.info(f"[wtnet] ✅ {len(ids)} Spam-Mail(s) gelöscht.")
        else:
            log.info("[wtnet] Kein Spam.")

        m.logout()
    except Exception as e:
        log.error(f"[wtnet] Fehler: {e}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    log.info("─" * 50)
    log.info("Spam Watcher gestartet")

    try:
        clean_outlook()
    except Exception as e:
        log.error(f"[Outlook] Fehler: {e}", exc_info=True)

    try:
        clean_wtnet()
    except Exception as e:
        log.error(f"[wtnet] Fehler: {e}", exc_info=True)

    log.info("Spam Watcher fertig.")


if __name__ == "__main__":
    main()
