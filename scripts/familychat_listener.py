#!/usr/bin/env python3
"""
FamilyChat Listener für Bolla 🐾
Polling-basiert (zuverlässiger als WS bei Render.com Free Tier).
"""

import asyncio
import json
import requests
import logging
import os
import time

API_KEY = "858ea89ccf9576238f4cb003afaf64ff"
API_URL = "https://family-chat-uqq1.onrender.com/api/messages"
SENDER = "bolla"
POLL_INTERVAL = 3  # Sekunden zwischen Polls

LOG_FILE = os.path.expanduser("~/workspace/logs/familychat.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("familychat")

last_seen_id = 0
last_response_time = {}  # sender -> timestamp (Cooldown-Schutz)
COOLDOWN_SECONDS = 20

def send_message(text: str):
    try:
        r = requests.post(API_URL,
            headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
            json={"text": text, "sender": SENDER},
            timeout=10
        )
        r.raise_for_status()
        log.info(f"Sent: {text[:80]}")
    except Exception as e:
        log.error(f"Failed to send message: {e}")

def should_respond(msg: dict) -> bool:
    sender = msg.get("sender", "")
    text = msg.get("text", "").lower()
    msg_id = msg.get("id", 0)

    if sender == SENDER:
        return False
    if msg_id <= last_seen_id:
        return False

    # Cooldown: max 1 Antwort pro Sender alle 20 Sekunden
    now = time.time()
    if sender in last_response_time and (now - last_response_time[sender]) < COOLDOWN_SECONDS:
        return False

    if "bolla" in text:
        return True
    if "ping" in text:
        return True
    if "pong" in text:
        return True
    if "?" in text:
        return True

    return False

def build_response(msg: dict) -> str:
    text = msg.get("text", "")
    sender = msg.get("sender", "jemand")
    text_lower = text.lower()

    if "ping" in text_lower:
        return f"PONG! 🏓🐾"
    elif "pong" in text_lower:
        return f"PING! 🏓🐾"
    elif "hallo" in text_lower or "hey" in text_lower or "hi" in text_lower:
        return f"Hey {sender}! 🐾"
    elif "wie geht" in text_lower:
        return f"Mir geht's super, danke {sender}! 🐾"
    elif "?" in text:
        return f"(Bolla 🐾: Gute Frage, {sender}! Für komplexe Sachen bin ich auf Telegram erreichbar 😄)"
    else:
        return f"(Bolla 🐾 hat's gelesen! 👋)"

def poll_once():
    global last_seen_id
    try:
        r = requests.get(API_URL, headers={"X-API-Key": API_KEY}, timeout=10)
        r.raise_for_status()
        msgs = r.json().get("messages", [])

        new_msgs = [m for m in msgs if m.get("id", 0) > last_seen_id]
        for msg in sorted(new_msgs, key=lambda m: m["id"]):
            msg_id = msg["id"]
            sender = msg.get("sender", "?")
            text = msg.get("text", "")
            log.info(f"[{msg_id}] {sender}: {text[:100]}")

            if should_respond(msg):
                response = build_response(msg)
                time.sleep(1.5)
                send_message(response)
                last_response_time[sender] = time.time()

            last_seen_id = max(last_seen_id, msg_id)

    except Exception as e:
        log.warning(f"Poll error: {e}")

def main():
    global last_seen_id
    log.info("Bolla FamilyChat Listener (polling) starting up 🐾")

    # Aktuelle höchste ID holen, keine alten Nachrichten beantworten
    try:
        r = requests.get(API_URL, headers={"X-API-Key": API_KEY}, timeout=10)
        msgs = r.json().get("messages", [])
        if msgs:
            last_seen_id = max(m["id"] for m in msgs)
            log.info(f"Startup: Last message ID = {last_seen_id}, skipping old messages.")
    except Exception as e:
        log.warning(f"Could not fetch initial messages: {e}")

    log.info(f"Polling every {POLL_INTERVAL}s... 🐾")
    while True:
        poll_once()
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
