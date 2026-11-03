#!/usr/bin/env python3
"""Prüft ob die neue Kindle-App für Windows 11 verfügbar ist.
Amazon kündigt die alte Kindle for PC App zum 30.06.2026 ab.
"""
import json, subprocess, requests
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
CLAUDE_BIN = Path("/home/bolla/.local/bin/claude")
TG_CFG = json.loads((WORKSPACE / "config/telegram_bot.json").read_text())
BOT_TOKEN = TG_CFG["bot_token"]
CHRIS_ID = TG_CFG["chris_id"]
STATE_FILE = WORKSPACE / "config/kindle_check_state.json"

PROMPT = """Suche nach aktuellen Informationen zur neuen Kindle-App für Windows 11.

Hintergrund: Amazon hat angekündigt, die klassische "Kindle for PC"-App (Desktop-Installer)
zum 30. Juni 2026 einzustellen. Es soll eine neue Kindle-App über den Microsoft Store kommen.

Frage: Ist die neue Kindle-App für Windows 11 im Microsoft Store bereits verfügbar?
Gibt es ein konkretes Veröffentlichungsdatum?

Antworte in einem dieser Formate:
- VERFÜGBAR: [kurze Beschreibung wie man sie bekommt]
- DATUM: [bekanntes Veröffentlichungsdatum]
- NOCH_NICHT: [kurze aktuelle Info zum Status]"""

def telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHRIS_ID, "text": msg, "parse_mode": "HTML"},
        timeout=10
    )

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"gemeldet": False, "letzter_status": ""}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def main():
    state = load_state()

    if state.get("gemeldet"):
        print("Bereits als verfügbar gemeldet — kein weiterer Check nötig.")
        return

    try:
        result = subprocess.run(
            [str(CLAUDE_BIN), "-p", PROMPT],
            capture_output=True, text=True, timeout=120
        )
        antwort = result.stdout.strip()
        print(f"Antwort: {antwort}")

        if antwort.startswith("VERFÜGBAR:"):
            info = antwort.replace("VERFÜGBAR:", "").strip()
            telegram(
                f"📚 <b>Neue Kindle-App für Windows 11 ist da!</b>\n\n"
                f"{info}\n\n"
                f"Die alte Kindle for PC App wird am 30.06.2026 abgekündigt."
            )
            state["gemeldet"] = True
            state["letzter_status"] = antwort
            save_state(state)

        elif antwort.startswith("DATUM:"):
            datum = antwort.replace("DATUM:", "").strip()
            if datum != state.get("letzter_status", ""):
                telegram(f"📚 <b>Neue Kindle-App für Windows 11 — Termin bekannt:</b>\n\n{datum}")
                state["letzter_status"] = datum
                save_state(state)

        else:
            print("Noch nicht verfügbar — kein Telegram nötig.")

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
