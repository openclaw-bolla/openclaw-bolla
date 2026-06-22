#!/usr/bin/env python3
"""
capabilities_drift.py — Periodische Überprüfung "was Bolla kann".

Erstellt einen Fingerprint der aktuellen Fähigkeiten:
  - MP-Seiten   (id="page-XXX" in index.html)
  - Cron-Jobs   (aktive Skripte/Endpunkte aus crontab)
Vergleicht mit dem letzten Snapshot und meldet per Telegram, wenn
Fähigkeiten dazugekommen oder weggefallen sind. Günstig, kein KI-Call.

Cron: 10 10 * * 1  (Montags 10:10)
"""
import json, re, subprocess, requests
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
INDEX_HTML = WORKSPACE / "mission-control/index.html"
SNAPSHOT = WORKSPACE / "state/capabilities_snapshot.json"

TG_CFG = json.loads((WORKSPACE / "config/telegram_bot.json").read_text())
BOT_TOKEN = TG_CFG["bot_token"]
CHRIS_ID = TG_CFG["chris_id"]


def telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHRIS_ID, "text": msg, "parse_mode": "HTML"},
        timeout=10,
    )


def current_capabilities():
    """Sammelt den Ist-Zustand der Bolla-Fähigkeiten."""
    # 1) MP-Seiten
    html = INDEX_HTML.read_text(encoding="utf-8")
    pages = sorted(set(re.findall(r'id="page-([a-z0-9-]+)"', html)))

    # 2) Cron-Jobs: Skript-Basenamen + /api/-Endpunkte
    try:
        cron = subprocess.run(["crontab", "-l"], capture_output=True, text=True, timeout=10).stdout
    except Exception:
        cron = ""
    crons = set()
    for line in cron.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for m in re.findall(r'([A-Za-z0-9_./-]+\.(?:py|sh))', line):
            crons.add(Path(m).name)
        for m in re.findall(r'/api/[a-z0-9/_-]+', line):
            crons.add(m)
    return {"pages": pages, "crons": sorted(crons)}


def diff_lists(old, new):
    o, n = set(old), set(new)
    return sorted(n - o), sorted(o - n)  # added, removed


def main():
    now = current_capabilities()

    if not SNAPSHOT.exists():
        SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT.write_text(json.dumps(now, ensure_ascii=False, indent=2))
        telegram(
            "🐾 <b>Fähigkeiten-Check eingerichtet</b>\n"
            f"Baseline angelegt: {len(now['pages'])} MP-Seiten, "
            f"{len(now['crons'])} automatische Jobs.\n"
            "Ab jetzt melde ich montags, wenn sich was ändert."
        )
        return

    old = json.loads(SNAPSHOT.read_text())
    p_add, p_rem = diff_lists(old.get("pages", []), now["pages"])
    c_add, c_rem = diff_lists(old.get("crons", []), now["crons"])

    if not any([p_add, p_rem, c_add, c_rem]):
        print("Keine Änderung an Bolla-Fähigkeiten.")
        return

    parts = ["🐾 <b>Bolla-Fähigkeiten haben sich geändert</b>"]
    if p_add:
        parts.append("🆕 Neue MP-Seiten: " + ", ".join(p_add))
    if p_rem:
        parts.append("➖ Entfernte MP-Seiten: " + ", ".join(p_rem))
    if c_add:
        parts.append("🆕 Neue Jobs: " + ", ".join(c_add))
    if c_rem:
        parts.append("➖ Entfallene Jobs: " + ", ".join(c_rem))
    parts.append("\n👉 Bitte die Übersicht „Was Bolla kann“ im System-Überblick prüfen.")
    telegram("\n".join(parts))

    SNAPSHOT.write_text(json.dumps(now, ensure_ascii=False, indent=2))
    print("Drift gemeldet + Snapshot aktualisiert.")


if __name__ == "__main__":
    main()
