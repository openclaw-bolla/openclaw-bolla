"""Antwort an Loeger Immobilien (Tutzing): Anschrift + Kaufpreisvorstellung. Freigabe Chris 14.10.2026."""
import json, requests
from outlook_oauth2 import refresh_access_token
H = {"Authorization": "Bearer " + refresh_access_token()}
msgs = requests.get("https://graph.microsoft.com/v1.0/me/messages?$top=50&$orderby=receivedDateTime desc"
                    "&$select=id,subject,from,receivedDateTime", headers=H).json()["value"]
m = next(x for x in msgs if x.get("from") and x["from"]["emailAddress"]["address"].lower() == "info@loeger.de")
text = """Sehr geehrte Frau Löger-Hohenwarter,

vielen Dank für Ihre schnelle Antwort und das Angebot, ein Suchprofil für uns zu erstellen.

Unsere Anschrift:
Chris und Renate Mandel
Buchenweg 67a
22846 Norderstedt

Unsere Kaufpreisvorstellung liegt zwischen 750.000 und 1.250.000 €.

Wie erwähnt, eilt es nicht: Wir suchen frühestens ab Herbst 2027, möglicherweise auch erst ab Herbst 2028.

Mit freundlichen Grüßen
Chris & Renate Mandel
ernstmandel@outlook.de"""
r = requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}/reply",
                  headers={**H, "Content-Type": "application/json"}, json={"comment": text})
print("Status:", r.status_code, r.text[:200])
if r.status_code == 202:
    d = json.load(open("/home/bolla/workspace/data/makler_status.json"))
    for rg in d["regionen"]:
        for mk in rg["makler"]:
            if (mk.get("email") or "").lower() == "info@loeger.de":
                d["statuses"][mk["id"]] = {"status": "feedback_erhalten",
                    "notiz": "14.10.2026: Anschrift + Kaufpreis 750–1.250 Tsd € an Fr. Löger-Hohenwarter geschickt; wartet auf Suchprofil", "datum": "14.10.2026"}
    json.dump(d, open("/home/bolla/workspace/data/makler_status.json", "w"), ensure_ascii=False, indent=2)
