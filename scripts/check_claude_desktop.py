#!/usr/bin/env python3
"""
Prüft ob die Claude Code Desktop App für Windows verfügbar ist.
Wenn ja: Mail an Chris, dann Cronjob entfernen.
Läuft 1x täglich per Cron.
"""

import json
import logging
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE = Path("/home/bolla/.openclaw/workspace")
TOKEN_FILE = WORKSPACE / "config/ms_token.json"
STATE_FILE = WORKSPACE / "config/claude_desktop_check.json"
LOG_FILE = WORKSPACE / "logs/claude_desktop_check.log"
CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"

CHECK_URL = "https://claude.ai/api/desktop/win32/x64/setup/latest/redirect"
MIN_SIZE = 10_000_000  # Echte App sollte >10 MB sein

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("claude_desktop_check")


def refresh_token() -> str:
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": token_data["refresh_token"],
        "scope": "https://graph.microsoft.com/Mail.Send https://graph.microsoft.com/Mail.ReadWrite offline_access"
    }).encode()
    import urllib.parse
    req = urllib.request.Request(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        data=data, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        new_token = json.loads(r.read())
    with open(TOKEN_FILE, "w") as f:
        json.dump(new_token, f, indent=2)
    return new_token["access_token"]


def send_mail(token: str):
    mail = {
        "message": {
            "subject": "🐾 Claude Code Desktop App ist da!",
            "body": {
                "contentType": "HTML",
                "content": (
                    "<h2>🐾 Gute Nachricht, Chris!</h2>"
                    "<p>Die <b>Claude Code Desktop App</b> für Windows ist jetzt verfügbar!</p>"
                    "<p>Du kannst sie hier herunterladen:</p>"
                    f'<p><a href="{CHECK_URL}">Claude Code Desktop App downloaden</a></p>'
                    "<p>Nach der Installation mit deinem <b>Max Plan Konto</b> anmelden — "
                    "und Bolla ist direkt da. 🐾</p>"
                    "<p>Liebe Grüße,<br>Bolla</p>"
                )
            },
            "toRecipients": [
                {"emailAddress": {"address": "ernstmandel@outlook.de", "name": "Chris Mandel"}}
            ]
        },
        "saveToSentItems": True
    }
    data = json.dumps(mail).encode()
    req = urllib.request.Request(
        "https://graph.microsoft.com/v1.0/me/sendMail",
        data=data, method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        pass
    log.info("✅ Mail an Chris gesendet!")


def check_size() -> int:
    """Prüft die Dateigröße des Downloads (ohne komplett herunterzuladen)."""
    try:
        req = urllib.request.Request(CHECK_URL, method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req, timeout=15) as r:
            size = int(r.headers.get("Content-Length", 0))
            return size
    except Exception as e:
        # Manche Server blocken HEAD, dann GET mit Range
        try:
            req = urllib.request.Request(CHECK_URL)
            req.add_header("User-Agent", "Mozilla/5.0")
            req.add_header("Range", "bytes=0-0")
            with urllib.request.urlopen(req, timeout=15) as r:
                cr = r.headers.get("Content-Range", "")
                if "/" in cr:
                    return int(cr.split("/")[1])
        except:
            pass
        log.warning(f"Größe nicht ermittelbar: {e}")
        return 0


def main():
    # Schon benachrichtigt?
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            state = json.load(f)
        if state.get("notified"):
            log.info("Bereits benachrichtigt — überspringe.")
            return

    log.info("Prüfe Claude Code Desktop App...")
    size = check_size()
    log.info(f"Download-Größe: {size:,} Bytes")

    if size >= MIN_SIZE:
        log.info(f"🎉 App ist da! ({size:,} Bytes > {MIN_SIZE:,})")
        try:
            import urllib.parse
            token = refresh_token()
            send_mail(token)
        except Exception as e:
            log.error(f"Mail senden fehlgeschlagen: {e}")
            return

        # Als erledigt markieren
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w") as f:
            json.dump({"notified": True, "size": size}, f, indent=2)
        log.info("Check abgeschlossen — wird nicht mehr wiederholt.")
    else:
        log.info(f"Noch nicht verfügbar (nur {size:,} Bytes). Nächster Check morgen.")


if __name__ == "__main__":
    main()
