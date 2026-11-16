#!/usr/bin/env python3
"""Einmal-Skript: Mail an Buhl (Ticket #BD-26-1176980), TR-Depot + Verrechnungskonto, ohne Signatur."""
import json, smtplib, ssl, imaplib, time
from email.message import EmailMessage
from pathlib import Path

CFG = json.loads(Path("/home/bolla/workspace/config/wtnet_account.json").read_text())
TO = "finanz@buhl-data.com"
SUBJECT = "Ticket #BD-26-1176980 – Trade Republic: Depot weiterhin ohne Synchronisierung, jetzt auch Verrechnungskonto betroffen"
BODY = """Sehr geehrte Damen und Herren,

ich melde mich erneut zum oben genannten Ticket. Das Trade-Republic-Wertpapierdepot lässt sich in WISO Mein Geld Professional 365 weiterhin nicht synchronisieren.

Zusätzlich hat sich die Lage verschlechtert: Auch das Trade-Republic-Verrechnungskonto, das bisher einwandfrei lief, lässt sich jetzt nicht mehr abrufen. Damit ist der Trade-Republic-Zugang insgesamt nicht mehr nutzbar.

Das Problem besteht inzwischen seit Anfang August, also seit rund zehn Wochen, und hat sich seit Ihrem Update der Onlinebanking-Schnittstelle (LetsTrade) nur verschlechtert. Bitte teilen Sie mir mit, ob die Ursache bei Ihnen bereits bekannt ist und wann mit einer Lösung zu rechnen ist.

Falls Sie Logdateien oder weitere Angaben von mir benötigen, schicke ich sie gern.

Vielen Dank und freundliche Grüße
Chris Mandel
"""
msg = EmailMessage()
msg["From"] = CFG["email"]; msg["To"] = TO; msg["Subject"] = SUBJECT
msg.set_content(BODY)
with smtplib.SMTP(CFG["smtp_host"], CFG["smtp_port"]) as s:
    s.starttls(context=ssl.create_default_context())
    s.login(CFG["email"], CFG["password"]); s.send_message(msg)
print(f"OK gesendet von {CFG['email']} an {TO}")
try:
    with imaplib.IMAP4_SSL(CFG["imap_host"], CFG["imap_port"]) as m:
        m.login(CFG["email"], CFG["password"])
        m.append("Gesendet", "\\Seen", imaplib.Time2Internaldate(time.time()), msg.as_bytes())
    print("OK Kopie in Gesendet")
except Exception as e:
    print(f"WARN Kopie fehlgeschlagen: {e}")
