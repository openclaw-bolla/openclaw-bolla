#!/usr/bin/env python3
"""
Allianz-Zahnzusatz-Fall Reni (AK-0576988791): Postfach-Wächter.
Sucht neue Allianz-Mails (Ellermann/Easterling/Allianz-PKV) zum Fall, sichert sie als .eml im Fallordner
und meldet per Telegram. Meldet einmalig, wenn bis 12.11.2026 keine Antwort da ist.
Cron: 15 8 * * * python3 /home/bolla/workspace/scripts/ellermann_watch.py >> /home/bolla/workspace/logs/ellermann_watch.log 2>&1
"""
import json
import requests
from datetime import datetime
from pathlib import Path
from outlook_oauth2 import refresh_access_token

OUT = Path("/mnt/d/OneDrive/Eigene Dateien/Reni/Gesundheit - TK/Allianz Zahnzusatz Mailverkehr")
STATE = Path("/home/bolla/workspace/data/ellermann_watch.json")
SEIT = "2026-10-29T16:20:00Z"  # Klarstellungsmail gesendet
FRIST = "2026-11-12"
cfg = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())


def telegram(text):
    requests.post(f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
                  data={"chat_id": cfg["chris_id"], "text": text}, timeout=20)


st = json.loads(STATE.read_text()) if STATE.exists() else {"gesehen": [], "frist_gemeldet": False}
H = {"Authorization": f"Bearer {refresh_access_token()}"}
neu = {}
for q in ["ellermann", "easterling", "AK-0576988791", "Zahnersatz"]:
    r = requests.get("https://graph.microsoft.com/v1.0/me/messages", headers=H, timeout=60,
                     params={"$search": f'"{q}"', "$top": "50", "$select": "id,subject,receivedDateTime,from"})
    r.raise_for_status()
    for m in r.json().get("value", []):
        a = m["from"]["emailAddress"]["address"].lower()
        if m["receivedDateTime"] > SEIT and a.endswith("allianz.de") and m["id"] not in st["gesehen"]:
            neu[m["id"]] = m

for m in sorted(neu.values(), key=lambda m: m["receivedDateTime"]):
    raw = requests.get(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}/$value", headers=H, timeout=120).content
    frm = m["from"]["emailAddress"]["address"].split("@")[0]
    n = len(list(OUT.glob("*.eml"))) + 1
    fn = f"{n:02d}_{m['receivedDateTime'][:16].replace('-', '').replace(':', '').replace('T', '_')}_{frm}.eml"
    (OUT / fn).write_bytes(raw)
    st["gesehen"].append(m["id"])
    telegram(f"📬 Allianz-Zahnfall Reni: neue Mail von {frm}\nBetreff: {m['subject']}\nGesichert: {fn}\nBolla bei 'moin' ansprechen, dann werte ich sie aus.")
    print(datetime.now(), "neu:", fn)

if not st["gesehen"] and not st["frist_gemeldet"] and datetime.now().strftime("%Y-%m-%d") >= FRIST:
    telegram("⏰ Allianz-Zahnfall Reni: seit 29.10. keine Antwort von Frau Ellermann (14 Tage). Nächster Schritt: Nachfassen / Allianz-Beschwerde / Ombudsmann. Bolla bei 'moin' ansprechen.")
    st["frist_gemeldet"] = True

STATE.write_text(json.dumps(st, indent=1))
print(datetime.now(), "ok, neu:", len(neu))
