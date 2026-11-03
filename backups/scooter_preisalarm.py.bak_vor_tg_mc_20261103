#!/usr/bin/env python3
"""
E-Scooter Preisalarm: ePowerFun ePF-2 PRO 653W + 490W (jeweils Wechselakku)
Liest den Preis von der Herstellerseite, speichert den Verlauf und meldet
per Telegram NUR bei neuem Tiefstpreis (und einmalig, wenn das Auslesen 3x
hintereinander scheitert).
Cron: 0 8 * * 1,3,5 python3 /home/bolla/workspace/scripts/scooter_preisalarm.py >> /home/bolla/workspace/logs/scooter_preisalarm.log 2>&1
"""

import json
import re
import requests
from datetime import datetime
from pathlib import Path

PRODUKTE = {
    "653W": "https://epowerfun.de/ePF-2-PRO-653W-Wechselakku/112005",
    "490W": "https://epowerfun.de/ePF-2-PRO-490W-Wechselakku/112004",
}
STATE = Path("/home/bolla/workspace/data/scooter_preisalarm.json")
cfg = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())


def telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
        data={"chat_id": cfg["chris_id"], "text": text}, timeout=20)


def hole_preis(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    r.raise_for_status()
    m = re.search(r'itemprop="price"\s+content="([\d.,]+)"', r.text)
    if not m:
        raise ValueError("Preisfeld nicht gefunden")
    return float(m.group(1).replace(",", "."))


alle = json.loads(STATE.read_text()) if STATE.exists() else {}
if "verlauf" in alle:  # altes Format (nur 653W) -> migrieren
    alle = {"653W": alle}
jetzt = datetime.now().strftime("%Y-%m-%d %H:%M")

for name, url in PRODUKTE.items():
    state = alle.setdefault(name, {"verlauf": [], "tiefstpreis": None, "fehler": 0})
    try:
        preis = hole_preis(url)
    except Exception as e:
        state["fehler"] += 1
        print(f"{jetzt} {name} FEHLER ({state['fehler']}x): {e}")
        if state["fehler"] == 3:
            telegram(f"⚠️ Scooter-Preisalarm ({name}): Preis konnte 3x nacheinander nicht gelesen werden (Seite geändert?). Bolla muss nachsehen.")
        continue
    state["fehler"] = 0
    alt = state["tiefstpreis"]
    state["verlauf"].append({"zeit": jetzt, "preis": preis})
    print(f"{jetzt} {name} Preis {preis:.2f} € (bisheriger Tiefstpreis: {alt})")
    if alt is None:
        state["tiefstpreis"] = preis  # Startwert, keine Meldung
    elif preis < alt:
        state["tiefstpreis"] = preis
        telegram(f"🛴 Neuer Tiefstpreis: ePF-2 PRO {name} (Wechselakku) jetzt {preis:.2f} € (vorher {alt:.2f} €)\n{url}")

STATE.write_text(json.dumps(alle, ensure_ascii=False, indent=1))
