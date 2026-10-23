#!/usr/bin/env python3
"""Mail an Tesla-Support: Konto-E-Mail-Adresse ändern (freigegeben von Chris 23.10.2026)."""
import sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import send_mail

TO = "EMEA-AT-ContactTeslaSupport@tesla.com"
SUBJECT = "Änderung der E-Mail-Adresse meines Tesla-Kontos (Ladeservice)"
BODY = """Sehr geehrtes Tesla-Support-Team,

ich nutze mein Tesla-Konto ausschließlich zum Laden meines Elektroautos (VW ID.3) über die Tesla-App. Die Anmelde-Adresse des Kontos lautet chrismandel@hotmail.com. Dieses Postfach existiert nicht mehr. Deshalb kann ich keine Bestätigungs- oder Sicherheitscodes empfangen. Die Adresse selbst ändern kann ich nicht.

Bitte ändern Sie die mit dem Konto verknüpfte E-Mail-Adresse auf:

ernstmandel@outlook.de

Zur Identifikation: Name Chris Mandel, bisherige Adresse chrismandel@hotmail.com. Falls Sie weitere Angaben oder Nachweise brauchen, melde ich mich gern.

Vielen Dank und freundliche Grüße
Chris Mandel
"""

if __name__ == "__main__":
    send_mail(TO, SUBJECT, BODY)
    print("gesendet")
