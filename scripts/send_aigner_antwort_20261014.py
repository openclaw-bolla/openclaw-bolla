"""Antwort an Aigner Immobilien (Fr. Becker). Freigabe Chris 14.10.2026 (mit Festnetz 040-30852883)."""
import json, requests, sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
H = {"Authorization": "Bearer " + refresh_access_token()}
msgs = requests.get("https://graph.microsoft.com/v1.0/me/messages?$top=50&$orderby=receivedDateTime desc"
                    "&$select=id,subject,from,receivedDateTime", headers=H).json()["value"]
m = next(x for x in msgs if x.get("from") and x["from"]["emailAddress"]["address"].lower() == "info@aigner-immobilien.de")
text = """Sehr geehrte Frau Becker,

vielen Dank für Ihre Rückmeldung.

Unsere Kontaktdaten:
Chris und Renate Mandel
Buchenweg 67a
22846 Norderstedt
Telefon: 040 - 30 85 28 83
E-Mail: ernstmandel@outlook.de

Unsere Preisvorstellung liegt zwischen 750.000 und 1.250.000 €.

Wie erwähnt, eilt es nicht: Wir suchen frühestens ab Herbst 2027, möglicherweise auch erst ab Herbst 2028.

Mit freundlichen Grüßen
Chris & Renate Mandel"""
r = requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{m['id']}/reply",
                  headers={**H, "Content-Type": "application/json"}, json={"comment": text})
print("Status:", r.status_code, r.text[:200])
if r.status_code == 202:
    p = "/home/bolla/workspace/data/makler_status.json"
    d = json.load(open(p))
    for rg in d["regionen"]:
        for mk in rg["makler"]:
            if (mk.get("email") or "").lower() == "info@aigner-immobilien.de":
                d["statuses"][mk["id"]] = {"status": "feedback_erhalten",
                    "notiz": "14.10.2026: Kontaktdaten (inkl. Festnetz auf Chris' Wunsch) + Preisrahmen an Fr. Becker geschickt", "datum": "14.10.2026"}
                print("Status gesetzt:", mk["id"])
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
