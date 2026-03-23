#!/usr/bin/env python3
"""
Token Watcher - Anthropic API Key Auto-Updater
Überwacht E-Mails von robinmandel@outlook.de alle 8 Stunden,
extrahiert den Anthropic Claude Token, aktualisiert die Konfiguration
und startet den OpenClaw Gateway neu.
"""

import json
import logging
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import requests

# ── Konfiguration ──────────────────────────────────────────────────────────────
WORKSPACE = Path("/home/bolla/.openclaw/workspace")
TOKEN_FILE = WORKSPACE / "config/ms_token.json"
AUTH_PROFILES = Path("/home/bolla/.openclaw/agents/main/agent/auth-profiles.json")
LOG_FILE = WORKSPACE / "logs/token_watcher.log"
STATE_FILE = WORKSPACE / "config/token_watcher_state.json"

CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"
SENDER_FILTER = "robinmandel@outlook.de"
CHECK_INTERVAL = 15 * 60  # 15 Minuten

# Regex für Anthropic API Keys (sk-ant-... oder sk-ant-oat01-...)
ANTHROPIC_TOKEN_RE = re.compile(r'sk-ant-[A-Za-z0-9_\-]{20,}')

# ── Logging Setup ──────────────────────────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("token_watcher")


# ── Microsoft Graph Token Management ──────────────────────────────────────────
def refresh_ms_token() -> str:
    """Refresht den Microsoft Graph Access Token und gibt ihn zurück."""
    with open(TOKEN_FILE) as f:
        token_data = json.load(f)

    r = requests.post(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        data={
            "client_id": CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"],
            "scope": "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.Send https://graph.microsoft.com/Mail.ReadWrite offline_access"
        }
    )

    if r.status_code != 200:
        raise RuntimeError(f"Token Refresh fehlgeschlagen: {r.status_code} {r.text}")

    new_token = r.json()
    with open(TOKEN_FILE, "w") as f:
        json.dump(new_token, f, indent=2)

    log.info("Microsoft Token erfolgreich erneuert.")
    return new_token["access_token"]


def get_ms_token() -> str:
    """Gibt einen gültigen Access Token zurück (refresht bei Bedarf)."""
    try:
        with open(TOKEN_FILE) as f:
            token_data = json.load(f)
        # Immer refreshen um sicherzustellen dass der Token frisch ist
        return refresh_ms_token()
    except Exception as e:
        log.error(f"Fehler beim Token-Refresh: {e}")
        raise


# ── E-Mail Suche ───────────────────────────────────────────────────────────────
def find_token_emails(access_token: str) -> list[dict]:
    """Sucht E-Mails von Robin mit einem Anthropic Token."""
    headers = {"Authorization": f"Bearer {access_token}"}

    # Letzte 20 Mails holen, lokal nach Absender filtern
    # Hinweis: $orderby ohne $filter wirft InefficientFilter → weglassen
    url = (
        "https://graph.microsoft.com/v1.0/me/messages"
        "?$top=20"
        "&$select=id,subject,body,receivedDateTime,from"
    )

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise RuntimeError(f"Mail-Abfrage fehlgeschlagen: {r.status_code} {r.text}")

    # Nach Datum sortieren — älteste zuerst, damit der neueste Token zuletzt gesetzt wird
    messages = sorted(
        r.json().get("value", []),
        key=lambda m: m.get("receivedDateTime", ""),
    )
    token_mails = []

    for msg in messages:
        sender = msg.get("from", {}).get("emailAddress", {}).get("address", "").lower()
        if sender != SENDER_FILTER.lower():
            continue
        body = msg.get("body", {}).get("content", "")
        # HTML-Tags entfernen für saubere Regex-Suche
        body_clean = re.sub(r'<[^>]+>', ' ', body)
        tokens = ANTHROPIC_TOKEN_RE.findall(body_clean)
        if tokens:
            msg["_extracted_tokens"] = tokens
            token_mails.append(msg)

    return token_mails


def delete_email(access_token: str, message_id: str):
    """Löscht eine E-Mail via Graph API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.delete(
        f"https://graph.microsoft.com/v1.0/me/messages/{message_id}",
        headers=headers
    )
    if r.status_code == 204:
        log.info(f"E-Mail {message_id[:20]}... gelöscht.")
    else:
        log.warning(f"E-Mail löschen fehlgeschlagen: {r.status_code} {r.text}")


# ── Token Update ───────────────────────────────────────────────────────────────
def update_anthropic_token(new_token: str):
    """Ersetzt den Anthropic Token in auth-profiles.json (alle anthropic-Profile)."""
    with open(AUTH_PROFILES) as f:
        profiles = json.load(f)

    updated = []
    for profile_name, profile in profiles.get("profiles", {}).items():
        if profile.get("provider") == "anthropic":
            old = profile.get("token", "")[:20] + "..."
            profile["token"] = new_token
            updated.append(f"{profile_name} (war: {old})")

    with open(AUTH_PROFILES, "w") as f:
        json.dump(profiles, f, indent=2)

    for info in updated:
        log.info(f"Anthropic Token aktualisiert: {info} → Neu: {new_token[:20]}...")

    if not updated:
        log.warning("Kein anthropic-Profil in auth-profiles.json gefunden!")


# ── Gateway Neustart ───────────────────────────────────────────────────────────
def restart_gateway():
    """Startet den OpenClaw Gateway neu."""
    log.info("Starte OpenClaw Gateway neu...")
    env = os.environ.copy()
    env["PATH"] = env.get("PATH", "") + ":/home/bolla/.npm-global/bin"
    try:
        result = subprocess.run(
            ["openclaw", "gateway", "restart"],
            capture_output=True, text=True, timeout=30, env=env
        )
        if result.returncode == 0:
            log.info("Gateway erfolgreich neu gestartet.")
        else:
            log.warning(f"Gateway Neustart: {result.stdout} {result.stderr}")
    except subprocess.TimeoutExpired:
        log.error("Gateway Neustart Timeout!")
    except Exception as e:
        log.error(f"Gateway Neustart fehlgeschlagen: {e}")


# ── State Management ──────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_check": 0, "processed_mail_ids": []}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ── Hauptschleife ──────────────────────────────────────────────────────────────
def check_once():
    """Führt eine einzelne Überprüfung durch."""
    state = load_state()
    processed_ids = set(state.get("processed_mail_ids", []))

    log.info("Prüfe E-Mails von Robin...")
    access_token = get_ms_token()
    mails = find_token_emails(access_token)

    if not mails:
        log.info("Keine E-Mails mit Anthropic Token gefunden.")
        return

    for mail in mails:
        mail_id = mail["id"]
        if mail_id in processed_ids:
            log.info(f"Mail bereits verarbeitet, überspringe.")
            continue

        subject = mail.get("subject", "(kein Betreff)")
        tokens = mail["_extracted_tokens"]
        new_token = tokens[0]  # Ersten gefundenen Token nehmen

        log.info(f"Token gefunden in Mail: '{subject}'")
        log.info(f"Neuer Token: {new_token[:25]}...")

        # Token aktualisieren
        update_anthropic_token(new_token)

        # Mail löschen
        delete_email(access_token, mail_id)

        # Gateway neu starten
        restart_gateway()

        # Als verarbeitet markieren
        processed_ids.add(mail_id)
        log.info("✅ Token erfolgreich aktualisiert!")

    # State speichern (max 100 IDs behalten)
    state["last_check"] = int(time.time())
    state["processed_mail_ids"] = list(processed_ids)[-100:]
    save_state(state)


def main():
    interval_min = CHECK_INTERVAL // 60
    log.info("=" * 60)
    log.info("Token Watcher gestartet")
    log.info(f"Überprüfe alle {interval_min} Minuten")
    log.info(f"Überwache E-Mails von: {SENDER_FILTER}")
    log.info("=" * 60)

    while True:
        try:
            check_once()
        except Exception as e:
            log.error(f"Fehler beim Check: {e}", exc_info=True)

        log.info(f"Nächste Prüfung in {interval_min} Minuten.")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
