#!/usr/bin/env python3
"""
Outlook Backup - ernstmandel@outlook.de
- Sichert Kalender (alle), Kontakte (inkl. Fotos) als JSON + Bilder
- Ablage: /home/bolla/.openclaw/workspace/backups/
- Wird wöchentlich per Cron oder manuell aufgerufen
"""

import json
import base64
import logging
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/home/bolla/.openclaw/workspace")
TOKEN_FILE = WORKSPACE / "config/ms_token.json"
BACKUP_DIR = WORKSPACE / "backups"
LOG_FILE = WORKSPACE / "logs/outlook_backup.log"

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("outlook_backup")


def load_token() -> str:
    with open(TOKEN_FILE) as f:
        return json.load(f)["access_token"]


def graph_get(token: str, url: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        log.error(f"GET {url} → {e.code}")
        return {}


def graph_get_binary(token: str, url: str) -> bytes:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.read()
    except urllib.error.HTTPError:
        return b""


def backup_calendars(token: str, backup_path: Path):
    """Sichert alle Kalender mit allen Events."""
    log.info("📅 Sichere Kalender...")
    cals = graph_get(token, "https://graph.microsoft.com/v1.0/me/calendars")
    all_calendars = []

    for c in cals.get("value", []):
        cal_id = c["id"]
        cal_name = c["name"]
        
        # Alle Events holen (paginiert)
        events = []
        url = f"https://graph.microsoft.com/v1.0/me/calendars/{cal_id}/events?$top=200"
        while url:
            result = graph_get(token, url)
            events.extend(result.get("value", []))
            url = result.get("@odata.nextLink")

        cal_data = {
            "calendar": c,
            "events": events,
            "event_count": len(events)
        }
        all_calendars.append(cal_data)
        log.info(f"  {cal_name}: {len(events)} Events")

    cal_file = backup_path / "calendars.json"
    with open(cal_file, "w", encoding="utf-8") as f:
        json.dump(all_calendars, f, ensure_ascii=False, indent=2)
    log.info(f"✅ Kalender gesichert: {cal_file}")
    return sum(c["event_count"] for c in all_calendars)


def backup_contacts(token: str, backup_path: Path):
    """Sichert alle Kontakte inkl. Fotos."""
    log.info("👤 Sichere Kontakte...")
    
    # Alle Kontakte holen (paginiert)
    contacts = []
    url = "https://graph.microsoft.com/v1.0/me/contacts?$top=200"
    while url:
        result = graph_get(token, url)
        contacts.extend(result.get("value", []))
        url = result.get("@odata.nextLink")

    log.info(f"  {len(contacts)} Kontakte gefunden")

    # Fotos herunterladen
    photos_dir = backup_path / "contact_photos"
    photos_dir.mkdir(exist_ok=True)
    photo_count = 0

    for contact in contacts:
        contact_id = contact.get("id", "")
        display_name = contact.get("displayName", "unbekannt")
        
        # Foto abrufen
        photo_data = graph_get_binary(
            token,
            f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}/photo/$value"
        )
        
        if photo_data:
            # Foto als Datei speichern
            safe_name = "".join(c for c in display_name if c.isalnum() or c in " -_").strip()[:50]
            photo_file = photos_dir / f"{safe_name}_{contact_id[:8]}.jpg"
            with open(photo_file, "wb") as f:
                f.write(photo_data)
            
            # Base64 im Kontakt-JSON speichern
            contact["_photo_base64"] = base64.b64encode(photo_data).decode("ascii")
            contact["_photo_file"] = str(photo_file.name)
            photo_count += 1

    # Kontakte als JSON speichern
    contacts_file = backup_path / "contacts.json"
    with open(contacts_file, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)
    
    log.info(f"✅ Kontakte gesichert: {contacts_file}")
    log.info(f"  📸 {photo_count} Kontaktfotos gesichert")
    return len(contacts), photo_count


def main():
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M")
    backup_path = BACKUP_DIR / f"outlook-{timestamp}"
    backup_path.mkdir(parents=True, exist_ok=True)

    log.info("=" * 60)
    log.info(f"Outlook Backup gestartet: {timestamp}")
    log.info(f"Ziel: {backup_path}")
    log.info("=" * 60)

    token = load_token()

    event_count = backup_calendars(token, backup_path)
    contact_count, photo_count = backup_contacts(token, backup_path)

    # Summary
    summary = {
        "timestamp": timestamp,
        "account": "ernstmandel@outlook.de",
        "events_total": event_count,
        "contacts_total": contact_count,
        "contact_photos": photo_count,
        "backup_path": str(backup_path)
    }
    with open(backup_path / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    log.info("=" * 60)
    log.info(f"✅ Backup komplett!")
    log.info(f"  📅 {event_count} Kalendereinträge")
    log.info(f"  👤 {contact_count} Kontakte")
    log.info(f"  📸 {photo_count} Fotos")
    log.info(f"  📁 {backup_path}")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
