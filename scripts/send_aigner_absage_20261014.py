#!/usr/bin/env python3
"""Höfliche Absage an Aigner Immobilien (Etagenwohnung Obermenzing) – von Chris am 14.10.2026 freigegeben."""
import html, requests
from outlook_oauth2 import refresh_access_token
TEXT = """Sehr geehrte Frau Becker, sehr geehrte Damen und Herren,

herzlichen Dank für Ihr schnelles Angebot und die Mühe, die Sie sich für uns gemacht haben. Das hat uns sehr gefreut.

Die Wohnung in Obermenzing ist leider nicht ganz das Richtige für uns. Wir sind dafür schon etwas zu alt 😉: Eine Etagenwohnung kommt für uns nicht mehr in Frage, wir suchen ein Penthouse bzw. eine Wohnung in der obersten Etage mit Südterrasse, und ein Aufzug im Haus ist uns wichtig.

Falls Sie einmal etwas in dieser Art hereinbekommen, melden Sie sich gern bei uns. Unser Suchzeitraum beginnt erst ab Herbst 2027, es eilt also nicht.

Wir wünschen Ihnen weiterhin viel Erfolg und grüßen herzlich

Chris und Renate Mandel"""
body = "<div style='font-family:Aptos,Calibri,sans-serif;font-size:11pt'>" + "<br>".join(html.escape(TEXT).split("\n")) + "</div>"
msg = {"message": {"subject": "RE: Aigner Immobilien - Ihre Anfrage - Etagenwohnung - Obermenzing",
       "body": {"contentType": "HTML", "content": body},
       "toRecipients": [{"emailAddress": {"address": "info@aigner-immobilien.de"}}]}, "saveToSentItems": True}
r = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                  headers={"Authorization": "Bearer " + refresh_access_token()}, json=msg)
print(r.status_code, r.text[:200])
