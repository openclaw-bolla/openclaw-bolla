#!/usr/bin/env python3
"""Mail an Frau Ellermann (Allianz): Kulanzbitte zur Zahnersatz-Erstattung Reni (241,74 EUR) + Frage Tarifwechsel.
ENTWURF 29.10.2026 - erst nach Freigabe von Chris ausfuehren (!python3 ...). Absender ernstmandel@outlook.de, Official-Signatur,
Anhang: Leistungsabrechnung der Allianz vom 28.10.2026."""
import base64, requests
from outlook_oauth2 import refresh_access_token

sig = open("/mnt/c/Users/ernst/AppData/Roaming/Microsoft/Signatures/Official (ernstmandel@outlook.de).htm", encoding="utf-8-sig").read()
sig = sig.replace('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />', '')
body = """<div style="font-family:Aptos,Calibri,sans-serif;font-size:12pt">
<p>Sehr geehrte Frau Ellermann,</p>
<p>die Zahnarztrechnung meiner Frau Renate Mandel (Vers.-Nr. AK-0576988791) wurde von der Allianz jetzt abgerechnet, vielen Dank für Ihre Unterstützung dabei. Die Abrechnung vom 28.10.2026 (Bearbeitungs-Nr. AK2026-71439981) hängt an.</p>
<p><b>Ergebnis:</b> Bei einer Rechnung von 1.012,78&nbsp;€ (davon 399,62&nbsp;€ TK-Festzuschuss) wurden 241,74&nbsp;€ erstattet. Mir ist inzwischen klar, wie die Allianz gerechnet hat: 70&nbsp;% der erstattungsfähigen 916,22&nbsp;€ unter Anrechnung der GKV-Leistung, und 96,56&nbsp;€ wurden gekürzt, weil das Honorar über dem 3,5-fachen GOZ-Satz lag. Das entspricht dem Tarifwortlaut, den Sie mir am 24.08. geschrieben hatten.</p>
<p>Wir hatten allerdings mit mehr gerechnet. Ihre Mail an meine Frau vom 31.08. lautete: <i>„Grundsätzlich übernimmt Ihre Zahnzusatzversicherung 70&nbsp;% der verbleibenden Kosten bei Kronen."</i> Das haben wir so verstanden, dass 70&nbsp;% der Kosten übernommen werden, die nach dem TK-Zuschuss bei uns bleiben, also etwa 360&nbsp;€ statt der erstatteten 242&nbsp;€. Vielleicht war die Formulierung nur verkürzt gemeint. Für unsere Planung war sie aber entscheidend.</p>
<p>Deshalb meine Bitte: Könnten Sie prüfen, ob die Allianz hier aus Kulanz noch etwas nachlegen kann, weil die Zusage vom 31.08. missverständlich war? Wenn das nicht möglich ist, verstehe ich das, und ich wäre Ihnen für eine kurze Rückmeldung dankbar.</p>
<p>Außerdem würde mich der Tarifwechsel interessieren, den Sie am 24.08. erwähnt haben (Zahnreinigung, Zahnbehandlung, Wurzelbehandlung, 3D-Scan). Könnten Sie mir dazu das aktuelle Angebot noch einmal schicken, mit den Wartezeiten und dem Beitrag? Dann entscheiden wir in Ruhe.</p>
<p>Vielen Dank und freundliche Grüße</p>
</div>
""" + sig

pdf = "/mnt/d/OneDrive/Eigene Dateien/Reni/Gesundheit - TK/Leistungsabrechnung_AK2026-71439981_2026-10-28.pdf"
atts = [{"@odata.type": "#microsoft.graph.fileAttachment", "name": "Leistungsabrechnung_AK2026-71439981_2026-10-28.pdf",
         "contentType": "application/pdf",
         "contentBytes": base64.b64encode(open(pdf, "rb").read()).decode()}]
msg = {"message": {"subject": "Zahnersatz Renate Mandel – Erstattung 241,74 € und Bitte um Kulanz (AK-0576988791)",
                   "body": {"contentType": "HTML", "content": body},
                   "toRecipients": [{"emailAddress": {"address": "saskia.ellermann@allianz.de"}}],
                   "attachments": atts}, "saveToSentItems": True}
t = refresh_access_token()
r = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                  headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}, json=msg)
print("Status:", r.status_code, r.text[:300])
