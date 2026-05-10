#!/usr/bin/env python3
"""Wöchentlicher Hardware-Tipps-Scout für Chris' Geräte.
Sucht via Claude nach wirklich relevanten Tipps — sendet nur wenn etwas Wichtiges gefunden wird.
"""
import json, subprocess, requests
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
CLAUDE_BIN = Path("/home/bolla/.local/bin/claude")
TG_CFG = json.loads((WORKSPACE / "config/telegram_bot.json").read_text())
BOT_TOKEN = TG_CFG["bot_token"]
CHRIS_ID = TG_CFG["chris_id"]

GERAETE = [
    "Microsoft Surface Studio 2+ (Windows 11)",
    "Microsoft Surface Book 3",
    "Microsoft Surface Pro 3 (Windows 11)",
    "Microsoft Surface Duo 2 (Android 12)",
    "Huawei P20 (Android 11)",
]

PROMPT = f"""Du bist Bolla, Chris Mandels persönlicher Assistent. Chris ist ein technikaffiner Nutzer (70 Jahre, IT-Karriere).

Suche nach WIRKLICH WICHTIGEN und nicht-trivialen Tipps oder Neuigkeiten für diese Geräte:
{chr(10).join("- " + g for g in GERAETE)}

Kriterien für "wichtig":
- Sicherheits-relevante Updates oder bekannte Schwachstellen
- Deutliche Performance-Verbesserungen durch Einstellungen
- Wenig bekannte Features die Chris konkret nutzen könnte
- Bekannte Bugs mit Workarounds
- Wichtige Software-EOL-Ankündigungen (z.B. App-Abkündigung)

NICHT relevant:
- Allgemeine "10 Tipps für Windows" Listen
- Triviale Hinweise (Desktop-Hintergrund ändern, etc.)
- Marketing-Inhalte
- Dinge die Chris mit seiner Erfahrung ohnehin kennt

Antworte NUR wenn du 1-3 wirklich relevante Tipps gefunden hast. Format:
🔧 [Gerät]: [Tipp in 1-2 Sätzen]

Wenn nichts Wichtiges gefunden: antworte exakt mit dem Wort NICHTS"""

def telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHRIS_ID, "text": msg, "parse_mode": "HTML"},
        timeout=10
    )

def main():
    try:
        result = subprocess.run(
            [str(CLAUDE_BIN), "-p", PROMPT],
            capture_output=True, text=True, timeout=120
        )
        antwort = result.stdout.strip()

        if not antwort or antwort.upper() == "NICHTS":
            print("Keine relevanten Tipps diese Woche.")
            return

        msg = f"<b>🔧 Hardware-Tipps der Woche</b>\n\n{antwort}"
        telegram(msg)
        print(f"Gesendet:\n{antwort}")

    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
