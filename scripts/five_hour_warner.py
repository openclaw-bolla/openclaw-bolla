#!/usr/bin/env python3
"""
5h-Fenster-Warner: warnt Chris per Telegram, BEVOR das 5h-Limit zuschlaegt,
statt dass Prompts stumm ins Leere laufen ("5h-Falle", 14.09.2026).

Liest /api/claudequota (kein Token-Verbrauch), schickt ab SCHWELLE% einmalig
pro Reset-Fenster eine Warnung. State-Datei verhindert Spam; sobald der
Reset-Zeitstempel sich aendert (neues Fenster), darf wieder gewarnt werden.

Cron: */5 * * * * python3 /home/bolla/workspace/scripts/five_hour_warner.py
"""
import json
import urllib.request
from pathlib import Path

MC_API = "http://127.0.0.1:18790/api/claudequota"
TG_CFG = Path("/home/bolla/workspace/config/telegram_bot.json")
STATE = Path("/home/bolla/workspace/config/five_hour_warner_state.json")
SCHWELLE = 90


def telegram(msg):
    cfg = json.loads(TG_CFG.read_text())
    import urllib.parse
    data = urllib.parse.urlencode({
        "chat_id": cfg["chris_id"], "text": msg, "parse_mode": "HTML",
    }).encode()
    urllib.request.urlopen(
        f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
        data=data, timeout=10)


def main():
    try:
        with urllib.request.urlopen(MC_API, timeout=10) as r:
            q = json.loads(r.read())
    except Exception:
        return  # MC-Server nicht erreichbar - naechster Lauf in 5 Min

    pct = q.get("five_hour_pct", 0)
    reset_label = q.get("five_hour_reset_label", "?")

    state = json.loads(STATE.read_text()) if STATE.exists() else {}

    if pct < SCHWELLE:
        # Fenster wieder frisch (Reset war) -> Warn-Sperre aufheben
        if state.get("warned_for_reset"):
            state["warned_for_reset"] = None
            STATE.write_text(json.dumps(state, indent=2))
        return

    if state.get("warned_for_reset") == reset_label:
        return  # fuer dieses Fenster schon gewarnt

    telegram(
        f"⚠️ <b>5h-Kontingent bei {pct}%</b>\n\n"
        f"Reset: {reset_label}\n"
        f"Was dir wichtig ist, jetzt noch schnell anstoßen — danach laufen "
        f"Anfragen erstmal ins Leere, bis das Fenster wieder frei ist. 🐾"
    )
    state["warned_for_reset"] = reset_label
    STATE.write_text(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()
