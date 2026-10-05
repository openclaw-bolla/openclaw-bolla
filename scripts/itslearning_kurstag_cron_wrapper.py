#!/usr/bin/env python3
"""Cron-Wrapper: startet itslearning_post_kurstag.py und meldet das Ergebnis per Telegram
(Regel: Cron-Jobs melden immer, ob vollzogen - siehe [[feedback_cron_nur_nach_freigabe_mit_rueckmeldung]])."""
import json, subprocess, sys, urllib.request

SCRIPT = "/home/bolla/workspace/scripts/itslearning_post_kurstag.py"
CFG = json.load(open("/home/bolla/workspace/config/telegram_bot.json"))


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
        data=json.dumps({"chat_id": CFG["chris_id"], "text": text}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


try:
    r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, timeout=3000)
    out = r.stdout + r.stderr
    print(out)
    summ = out.split("=== ZUSAMMENFASSUNG ===")[-1].strip() if "=== ZUSAMMENFASSUNG ===" in out else out[-600:]
    lines = [l for l in summ.splitlines() if ":" in l]
    ok = r.returncode == 0 and len(lines) >= 4 and all(l.strip().endswith(": OK") for l in lines)
    tg(("✅ itslearning Kurstag 4 (II-Kurse): PDF + Praktikum + Mitteilung in allen 4 Kursen gepostet 🐾\n" if ok else
        "⚠️ itslearning Kurstag 4 (II-Kurse) NICHT sauber durch:\n") + summ[:900])
except Exception as e:
    tg(f"⚠️ itslearning Kurstag 4 Cron: Abbruch {e!r}"[:900])
