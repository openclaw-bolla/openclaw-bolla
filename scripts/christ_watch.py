#!/usr/bin/env python3
"""
Christ Juweliere Hamburg: Wächter für die Antwort auf unsere Zertifikats-Anfrage (gesendet 07.11.2026
an hamburg225@christ.de, Kauf 22.10.2026, Kundennr. 5000984789).
Sucht Mails von *@christ.de (NICHT mailings.christ.de = Newsletter/CLUB), sichert sie als .eml und
meldet per MC-Job. Meldet einmalig, wenn bis 14.11.2026 keine Antwort da ist.
Aufruf (derzeit manuell / bei 'moin'): python3 /home/bolla/workspace/scripts/christ_watch.py
"""
import json, sys, requests
from datetime import datetime
from pathlib import Path
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
from job_status import mc_meldung

OUT = Path("/mnt/d/OneDrive/Eigene Dateien/Rechnungen/Christ Schmuck 22.10.2026")
STATE = Path("/home/bolla/workspace/data/christ_watch.json")
SEIT = "2026-11-07T00:00:00Z"
FRIST = "2026-11-14"


def meld(text):
    return mc_meldung("christ-watch", "Christ Schmuck: Zertifikat-Anfrage", text)


OUT.mkdir(parents=True, exist_ok=True)
st = json.loads(STATE.read_text()) if STATE.exists() else {"gesehen": [], "frist_gemeldet": False}
H = {"Authorization": f"Bearer {refresh_access_token()}"}
neu = {}
for q in ["christ.de", "Kundennummer 5000984789", "Zertifikat"]:
    r = requests.get("https://graph.microsoft.com/v1.0/me/messages", headers=H, timeout=60,
                     params={"$search": f'"{q}"', "$top": "50", "$select": "id,subject,receivedDateTime,from"})
    r.raise_for_status()
    for m in r.json().get("value", []):
        a = m["from"]["emailAddress"]["address"].lower()
        if (m["receivedDateTime"] > SEIT and a.endswith("christ.de") and "mailings" not in a
                and m["id"] not in st["gesehen"]):
            neu[m["id"]] = m

for m in sorted(neu.values(), key=lambda m: m["receivedDateTime"]):
    raw = requests.get(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}/$value", headers=H, timeout=120).content
    frm = m["from"]["emailAddress"]["address"].split("@")[0]
    n = len(list(OUT.glob("*.eml"))) + 1
    fn = f"{n:02d}_{m['receivedDateTime'][:16].replace('-', '').replace(':', '').replace('T', '_')}_{frm}.eml"
    (OUT / fn).write_bytes(raw)
    st["gesehen"].append(m["id"])
    meld(f"📬 Antwort von Christ ({frm}): {m['subject']}\nGesichert: {fn}\nBolla bei 'moin' ansprechen, dann werte ich sie aus.")
    print(datetime.now(), "neu:", fn)

if not st["gesehen"] and not st["frist_gemeldet"] and datetime.now().strftime("%Y-%m-%d") >= FRIST:
    meld("⏰ Christ Hamburg: seit 07.11. keine Antwort auf die Zertifikats-Anfrage (7 Tage). "
         "Nächster Schritt: Nachfassen per Mail oder Anruf Filiale 040/330415. Bolla bei 'moin' ansprechen.")
    st["frist_gemeldet"] = True

STATE.write_text(json.dumps(st, indent=1))
print(datetime.now(), "ok, neu:", len(neu))
