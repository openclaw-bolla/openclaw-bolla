#!/usr/bin/env python3
"""
Bolla Telegram Bot 🐾
Lauscht in der Familiengruppe und antwortet via Claude Code.
Reagiert auf Erwähnungen von "bolla" oder direkte Antworten auf Bolla-Nachrichten.
"""

import json
import logging
import os
import subprocess
import requests
import time

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "telegram_bot.json")
with open(CONFIG_FILE) as f:
    _cfg = json.load(f)

BOT_TOKEN = _cfg["bot_token"]
GROUP_CHAT_ID = _cfg["group_chat_id"]
CHRIS_ID = _cfg["chris_id"]
BOT_ID = _cfg["bot_id"]

LOG_FILE = os.path.expanduser("~/workspace/logs/telegram_bot.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("telegram_bot")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def get_updates(offset=None):
    params = {"timeout": 30, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(f"{API}/getUpdates", params=params, timeout=35)
        return r.json().get("result", [])
    except Exception as e:
        log.error(f"getUpdates Fehler: {e}")
        return []


def send_message(chat_id, text, reply_to=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_to:
        data["reply_to_message_id"] = reply_to
    try:
        r = requests.post(f"{API}/sendMessage", json=data, timeout=10)
        return r.json()
    except Exception as e:
        log.error(f"sendMessage Fehler: {e}")
        return None


def ask_claude(message, sender_name):
    """Fragt Claude Code und gibt die Antwort zurück."""
    prompt = f"[Telegram-Nachricht von {sender_name}]: {message}"
    cmd = ["claude", "-p", "--output-format", "json", prompt]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120,
            cwd=os.path.expanduser("~/workspace")
        )
        if result.returncode != 0:
            log.error(f"Claude Fehler: {result.stderr[:200]}")
            return None
        data = json.loads(result.stdout)
        return data.get("result", "")
    except subprocess.TimeoutExpired:
        return "Sorry, das hat zu lange gedauert — versuch's nochmal! 🐾"
    except Exception as e:
        log.error(f"Claude Fehler: {e}")
        return None


def should_respond(msg):
    """Prüft ob Bolla auf diese Nachricht reagieren soll."""
    text = msg.get("text", "").lower()

    # In der Familiengruppe: immer antworten
    if msg.get("chat", {}).get("id") == GROUP_CHAT_ID:
        return True

    # Direktnachrichten: immer antworten
    if msg.get("chat", {}).get("type") == "private":
        return True

    # Andere Gruppen: nur bei Erwähnung oder Antwort
    reply = msg.get("reply_to_message", {})
    if reply.get("from", {}).get("id") == BOT_ID:
        return True
    if "bolla" in text:
        return True

    return False


def main():
    log.info("Bolla Telegram Bot gestartet 🐾")
    send_message(GROUP_CHAT_ID, "Bolla ist wieder da! 🐾")

    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message")
            if not msg or not msg.get("text"):
                continue

            sender = msg.get("from", {})
            sender_name = sender.get("first_name", "Jemand")
            sender_id = sender.get("id", 0)
            text = msg["text"]
            chat_id = msg["chat"]["id"]
            msg_id = msg["message_id"]

            # Eigene Nachrichten ignorieren
            if sender_id == BOT_ID:
                continue

            log.info(f"[{sender_name}]: {text[:100]}")

            if should_respond(msg):
                log.info(f"Antworte auf: {text[:80]}")
                # "Tippt..." Indikator
                requests.post(f"{API}/sendChatAction",
                              json={"chat_id": chat_id, "action": "typing"})

                reply = ask_claude(text, sender_name)
                if reply:
                    send_message(chat_id, reply, reply_to=msg_id)
                else:
                    send_message(chat_id, "Da ging was schief — bin aber da! 🐾", reply_to=msg_id)


if __name__ == "__main__":
    main()
