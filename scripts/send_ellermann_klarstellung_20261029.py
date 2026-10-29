#!/usr/bin/env python3
"""Klarstellungsmail an Frau Ellermann (Allianz): Falschauskunft 31.08. statt Kulanz. ENTWURF 29.10.2026, nur nach Freigabe von Chris ausführen.
ENTWURF 29.10.2026 - erst nach Freigabe von Chris ausfuehren (!python3 ...). Absender ernstmandel@outlook.de, Official-Signatur,
Anhang: Leistungsabrechnung der Allianz vom 28.10.2026."""
import base64, requests
from outlook_oauth2 import refresh_access_token

sig = open("/mnt/c/Users/ernst/AppData/Roaming/Microsoft/Signatures/Official (ernstmandel@outlook.de).htm", encoding="utf-8-sig").read()
sig = sig.replace('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />', '')
body = """<div style="font-family:Aptos,Calibri,sans-serif;font-size:12pt">
<p>Sehr geehrte Frau Ellermann,</p>
<p>ich muss meine Mail von heute ergänzen und in einem Punkt klarstellen: Das Wort „Kulanz" war nicht passend, und meine Frau und ich sehen es anders.</p>
<p>Am 28.08.2026 hat meine Frau Ihnen den Kostenvoranschlag der Zahnärztin und den erhöhten TK-Zuschuss geschickt und ausdrücklich um eine <b>Zusage der Kostenübernahme</b> durch die Allianz gebeten. Sie haben am 31.08. geantwortet, die Bearbeitung von Heil- und Kostenplänen dauere aktuell sehr lange, die Zahnzusatzversicherung übernehme „grundsätzlich 70&nbsp;% der verbleibenden Kosten bei Kronen", und wir könnten nach der Behandlung einfach die Rechnung einreichen.</p>
<p>Auf diese Auskunft haben wir uns verlassen. Sie enthielt keinen Hinweis, dass eine verbindliche Zusage nur über einen von der Allianz geprüften Heil- und Kostenplan möglich ist und dass die tatsächliche Erstattung davon abhängt, wie die GKV-Leistung angerechnet wird und bis zu welchem Steigerungssatz der Tarif leistet. Ihr Vorgänger, Herr Krämer, hat von mir bei Zahnersatz immer einen Kostenvoranschlag verlangt, bevor es eine feste Aussage gab. Mit einem geprüften Plan hätten wir den Erstattungsbetrag vorher gekannt und mit der Zahnärztin den Steigerungssatz besprechen können.</p>
<p>Tatsächlich erhalten wir 241,74&nbsp;€. Nach Ihrer Aussage („70&nbsp;% der verbleibenden Kosten") wären es 361,62&nbsp;€ gewesen, also <b>119,88&nbsp;€ mehr</b>. Wir sehen darin eine unvollständige Auskunft Ihrer Agentur und bitten um eine schriftliche Stellungnahme, wie Sie damit umgehen möchten, und um den Ausgleich dieser Differenz.</p>
<p>Meine Frage zum Tarifwechsel aus der Mail von heute bleibt unabhängig davon bestehen.</p>
<p>Mit freundlichen Grüßen</p>
</div>
""" + sig

pdf = "/mnt/d/OneDrive/Eigene Dateien/Reni/Gesundheit - TK/Leistungsabrechnung_AK2026-71439981_2026-10-28.pdf"
atts = [{"@odata.type": "#microsoft.graph.fileAttachment", "name": "Leistungsabrechnung_AK2026-71439981_2026-10-28.pdf",
         "contentType": "application/pdf",
         "contentBytes": base64.b64encode(open(pdf, "rb").read()).decode()}]
msg = {"message": {"subject": "AW: Zahnersatz Renate Mandel – Klarstellung zur Auskunft vom 31.08.2026 (AK-0576988791)",
                   "body": {"contentType": "HTML", "content": body},
                   "toRecipients": [{"emailAddress": {"address": "saskia.ellermann@allianz.de"}}],
                   "attachments": atts}, "saveToSentItems": True}
t = refresh_access_token()
r = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                  headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}, json=msg)
print("Status:", r.status_code, r.text[:300])
