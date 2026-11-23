#!/usr/bin/env python3
"""Beschwerde an Allianz (krankenversicherung@allianz.de), cc Ellermann. Freigabe Chris 23.11.2026. Absender ernstmandel@outlook.de."""
import base64, os, sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
import requests
from outlook_oauth2 import refresh_access_token

sig = open("/mnt/c/Users/ernst/AppData/Roaming/Microsoft/Signatures/Official (ernstmandel@outlook.de).htm", encoding="utf-8-sig").read()
sig = sig.replace('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />', '')
body = """<div style="font-family:Aptos,Calibri,sans-serif;font-size:12pt">
<p>Sehr geehrte Damen und Herren,</p>
<p>anbei erhalten Sie meine Beschwerde über die Beratung der Generalvertretung Saskia Ellermann-Vitsos (Waldenbuch) zum Zahnersatz meiner Frau Renate Mandel (Vers.-Nr. AK-0576988791, Tarif ZahnPlus ZP02, Bearbeitungs-Nr. AK2026-71439981).</p>
<p>Kurz zusammengefasst: Die Agentur hat uns am 31.08.2026 schriftlich mitgeteilt, es würden „grundsätzlich 70&nbsp;% der verbleibenden Kosten bei Kronen" übernommen, wir könnten einfach die Rechnung einreichen. Auf einen geprüften Heil- und Kostenplan wurde nicht hingewiesen. Erstattet wurden 241,74&nbsp;€ statt der nach dieser Auskunft zu erwartenden 361,62&nbsp;€. Die Differenz beträgt 119,88&nbsp;€. Die Leistungsabrechnung selbst greifen wir nicht an.</p>
<p>Ich bitte um Eingangsbestätigung, Prüfung und schriftliche Antwort innerhalb der auf Ihrer Internetseite genannten 5 Arbeitstage. Die Agentur setze ich zur Kenntnis in Kopie.</p>
<p>Mit freundlichen Grüßen</p>
</div>
""" + sig

D = "/mnt/d/OneDrive/Eigene Dateien/Reni/Gesundheit - TK/"
M = D + "Allianz Zahnzusatz Mailverkehr/"
files = [
 ("/mnt/c/Users/ernst/AppData/Local/Temp/bz/Beschwerde_Allianz_Mandel_2026-11-23.pdf", "Beschwerde_Allianz_Mandel_2026-11-23.pdf", "application/pdf"),
 (D + "Leistungsabrechnung_AK2026-71439981_2026-10-28.pdf", "Leistungsabrechnung_AK2026-71439981_2026-10-28.pdf", "application/pdf"),
 (D + "Zuschuss TK.pdf", "Zuschuss_TK.pdf", "application/pdf"),
 (M + "11_20260831_0637_saskia.ellermann.eml", "Auskunft_Ellermann_2026-08-31.eml", "message/rfc822"),
 (M + "07_20260825_1034_kontakt.eml", "Kostenvoranschlag_2026-08-25.eml", "message/rfc822"),
 (M + "15_20261029_1608_Chris.eml", "Mail_2026-10-29_1608.eml", "message/rfc822"),
 (M + "16_20261029_1620_Chris.eml", "Mail_2026-10-29_1620_Klarstellung.eml", "message/rfc822"),
 (M + "17_20261120_1453_saskia.ellermann.eml", "Antwort_Ellermann_2026-11-20.eml", "message/rfc822"),
 (M + "2026-11-21_Meine-Allianz_Antwort_Easterling.txt", "Antwort_Easterling_Meine_Allianz_2026-11-21.txt", "text/plain"),
]
for n in sorted(os.listdir(M)):
    if n.startswith("Rechnung_Dingeldey") and n.endswith(".png"):
        files.append((M + n, n, "image/png"))

t = refresh_access_token()
H = {"Authorization": f"Bearer {t}", "Content-Type": "application/json"}
draft = {"subject": "Beschwerde über die Beratung der Agentur Ellermann-Vitsos – Zahnersatz Renate Mandel (AK-0576988791 / AK2026-71439981)",
         "body": {"contentType": "HTML", "content": body},
         "toRecipients": [{"emailAddress": {"address": "krankenversicherung@allianz.de"}}],
         "ccRecipients": [{"emailAddress": {"address": "saskia.ellermann@allianz.de"}}]}
r = requests.post("https://graph.microsoft.com/v1.0/me/messages", headers=H, json=draft)
print("Draft:", r.status_code); r.raise_for_status()
mid = r.json()["id"]
for p, name, ct in files:
    a = {"@odata.type": "#microsoft.graph.fileAttachment", "name": name, "contentType": ct,
         "contentBytes": base64.b64encode(open(p, "rb").read()).decode()}
    ra = requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mid}/attachments", headers=H, json=a)
    print("Anhang", name, ra.status_code)
    if ra.status_code >= 300:
        print(ra.text[:300]); sys.exit("Abbruch vor Versand (Draft bleibt im Entwurfsordner)")
rs = requests.post(f"https://graph.microsoft.com/v1.0/me/messages/{mid}/send", headers=H)
print("Send:", rs.status_code, rs.text[:200])
