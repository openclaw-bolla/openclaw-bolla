#!/usr/bin/env python3
"""Einmal-Skript: Mail an Buhl (Ticket #BD-26-1176980), TR-Depot trotz LetsTrade Kernel 5.2.2.208."""
import json, smtplib, ssl, imaplib, time
from email.message import EmailMessage
from pathlib import Path

CFG = json.loads(Path("/home/bolla/workspace/config/wtnet_account.json").read_text())
TO = "finanz@buhl-data.com"
SUBJECT = "Ticket #BD-26-1176980 – Trade Republic: Depot-Abruf scheitert trotz LetsTrade Kernel 5.2.2.208"
BODY = """Sehr geehrte Damen und Herren,

vielen Dank für Ihre Nachricht vom 13.10.2026 zum Abruf der Trade Republic.

Ich habe das LetsTrade-Update (LT5PreRelease.exe) wie beschrieben als Administrator ausgeführt. Unter Hilfe > Info > LetsTrade zeigt WISO Mein Geld Professional 365 jetzt:

- LetsTrade Kernel: 5.2.2.208
- Banking Kernel: 2.6.013.9578
- DDBAC.Net / DDBAC.Net Screenparser: 5.11.25.0
- Screenparser Framework: 2.0.0.0
- Screenparser Plugins: 4.5.0

Ergebnis: Das Trade-Republic-Verrechnungskonto lässt sich wieder abrufen. Das Wertpapierdepot (Depotstatusabfrage) funktioniert weiterhin nicht. Es erscheint unverändert die Meldung: "Bei der Verarbeitung Ihres Auftrags ist leider ein Fehler aufgetreten. Bitte wiederholen Sie die gewünschte Aktion zu einem späteren Zeitpunkt. Mindestens ein Fehler ist aufgetreten."

Das Problem besteht seit Anfang August 2026. Bitte geben Sie die Angelegenheit an die Entwicklungsabteilung zurück. Falls Logdateien benötigt werden, teilen Sie mir bitte mit, wie ich diese erzeugen und senden soll.

Vielen Dank und freundliche Grüße
Chris Mandel
Kundennummer 3279697
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
