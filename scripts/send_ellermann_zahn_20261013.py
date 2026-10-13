#!/usr/bin/env python3
"""Mail an Frau Ellermann (Allianz): Zahnarztrechnung Reni, 0 € erstattet. Freigabe Chris 13.10.2026.
Absender ernstmandel@outlook.de, Official-Signatur, 3 PNG-Anhänge."""
import base64, requests
from outlook_oauth2 import refresh_access_token

sig = open("/mnt/c/Users/ernst/AppData/Roaming/Microsoft/Signatures/Official (ernstmandel@outlook.de).htm", encoding="utf-8-sig").read()
sig = sig.replace('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />', '')
body = """<div style="font-family:Aptos,Calibri,sans-serif;font-size:12pt">
<p>Sehr geehrte Frau Ellermann,</p>
<p>für meine Frau Renate Mandel (geb. 24.10.1965) habe ich eine Zahnarztrechnung zur Erstattung über ihre Zahnzusatzversicherung eingereicht. Als Ergebnis wurde mir eine Erstattung von 0&nbsp;€ mitgeteilt, und ich verstehe nicht, warum.</p>
<p><b>Versicherungsnummer: AK-0576988791</b></p>
<p>Die Rechnung:<br>
– Zahnärztin Andrea Dingeldey, Norderstedt (abgerechnet über die Health AG)<br>
– Rechnungs-Nr. 536505638 vom 01.10.2026<br>
– Behandlungen am 08.09. und 23.09.2026 (u.&nbsp;a. Vollkrone)<br>
– Rechnungsbetrag 613,16&nbsp;€ (nach Abzug des Festzuschusses)</p>
<p>Sie hatten meiner Frau am 31.08.2026 geschrieben, dass die Zahnzusatzversicherung bei Kronen 70&nbsp;% der verbleibenden Kosten übernimmt und wir die Rechnung nach der Behandlung einfach einreichen können. Umso mehr überrascht mich die Erstattung von 0&nbsp;€.</p>
<p>Ich habe die Rechnung über die Allianz Gesundheits-App eingereicht, und zwar über meinen Zugang bei meiner Krankenversicherung, da Renis Zusatzversicherung dort mit eingebunden ist. Vielleicht wurde die Einreichung dadurch fehlerhaft zugeordnet oder hätte anders erfolgen müssen.</p>
<p>Könnten Sie bitte prüfen, woran es liegt, und mir sagen, was ich tun muss, damit die Rechnung korrekt bearbeitet wird? Die Rechnung (3 Seiten) hängt dieser Mail an.</p>
<p>Vielen Dank für Ihre Hilfe!</p>
</div>
""" + sig

base = "/home/bolla/workspace/scratch/ellermann_zahn/"
files = [("document_1791387637705.png", "Rechnung_536505638_Seite_1_von_3.png"),
         ("document_1791387652301.png", "Rechnung_536505638_Seite_2_von_3.png"),
         ("document_1791387664116.png", "Rechnung_536505638_Seite_3_von_3.png")]
atts = [{"@odata.type": "#microsoft.graph.fileAttachment", "name": n, "contentType": "image/png",
         "contentBytes": base64.b64encode(open(base + f, "rb").read()).decode()} for f, n in files]
msg = {"message": {"subject": "Zahnarztrechnung Renate Mandel – Erstattung 0 € bei eingereichter Rechnung",
                   "body": {"contentType": "HTML", "content": body},
                   "toRecipients": [{"emailAddress": {"address": "saskia.ellermann@allianz.de"}}],
                   "attachments": atts}, "saveToSentItems": True}
t = refresh_access_token()
r = requests.post("https://graph.microsoft.com/v1.0/me/sendMail",
                  headers={"Authorization": f"Bearer {t}", "Content-Type": "application/json"}, json=msg)
print("Status:", r.status_code, r.text[:300])
