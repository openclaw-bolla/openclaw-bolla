#!/usr/bin/env python3
"""Einmal-Skript: Nachfass-Mail an Buhl (Ticket #BD-26-1176980) von chrismandel@wtnet.de,
Multipart HTML+Text mit Official-Signatur, Kopie nach 'Gesendet' abgelegt."""
import json, smtplib, ssl, imaplib, time
from email.message import EmailMessage
from pathlib import Path

CFG = json.loads(Path("/home/bolla/workspace/config/wtnet_account.json").read_text())

TO = "finanz@buhl-data.com"
SUBJECT = "Ticket #BD-26-1176980 – Trade-Republic-Wertpapierdepot: aktueller Stand?"

TEXT_BODY = """Sehr geehrte Damen und Herren,

ich melde mich zum oben genannten Ticket. Auf meine Nachfrage vom 04.09.2026 hatte ich noch keine Rückmeldung erhalten. Das Trade-Republic-Wertpapierdepot lässt sich in WISO Mein Geld Professional 365 weiterhin nicht synchronisieren – nach wie vor mit der Meldung „die Bank arbeitet an einer Lösung". Verrechnungskonto und ADAC-Kreditkarten-Konto laufen unverändert sauber.

Das Problem besteht nun seit Anfang August, also seit rund sieben Wochen. Können Sie mir bitte einen aktuellen Stand zur Anpassung der Screenparser-Schnittstelle mitteilen – insbesondere, ob inzwischen eine Zeitschiene absehbar ist, oder ob weiterhin auf eine Lösung seitens Trade Republic gewartet wird?

Vielen Dank und freundliche Grüße
Chris Mandel
Buchenweg 67a
22846 Norderstedt
______________________________________
tel 040 30852883
mobil +49 178 6801513
email ernstmandel@outlook.de
web chrismandel.de
"""

TEXT_PARA = "<br>".join(
    "Sehr geehrte Damen und Herren,".split("\n")
)

HTML_BODY = """<html><body style="font-family:Aptos,Arial,sans-serif; font-size:12pt; color:black">
<p>Sehr geehrte Damen und Herren,</p>
<p>ich melde mich zum oben genannten Ticket. Auf meine Nachfrage vom 04.09.2026 hatte ich noch keine Rückmeldung erhalten. Das Trade-Republic-Wertpapierdepot lässt sich in WISO Mein Geld Professional 365 weiterhin nicht synchronisieren &ndash; nach wie vor mit der Meldung &bdquo;die Bank arbeitet an einer L&ouml;sung&ldquo;. Verrechnungskonto und ADAC-Kreditkarten-Konto laufen unver&auml;ndert sauber.</p>
<p>Das Problem besteht nun seit Anfang August, also seit rund sieben Wochen. K&ouml;nnen Sie mir bitte einen aktuellen Stand zur Anpassung der Screenparser-Schnittstelle mitteilen &ndash; insbesondere, ob inzwischen eine Zeitschiene absehbar ist, oder ob weiterhin auf eine L&ouml;sung seitens Trade Republic gewartet wird?</p>
<div>
<p style="margin:0cm; font-family:Aptos,sans-serif"><span style="font-size:12pt; color:black">Mit freundlichen Gr&uuml;&szlig;en</span></p>
<p style="margin:0cm; font-family:Aptos,sans-serif; font-size:12pt"><span style="color:rgb(195,151,29)"><b><i>Chris Mandel<br>
</i></b></span><span style="font-size:11pt; color:black">Buchenweg 67a<br>
22846 Norderstedt<br>
______________________________________<br>
</span><span style="font-size:11pt; color:rgb(195,151,29)"><b>tel </b></span><span style="font-size:11pt; color:black">040 30852883<br>
</span><span style="font-size:11pt; color:rgb(195,151,29)"><b>mobil </b></span><span style="font-size:11pt; color:black">+49 178 6801513<br>
</span><span style="font-size:11pt; color:rgb(195,151,29)"><b>email </b></span><span style="font-size:11pt; color:black">ernstmandel@outlook.de<br>
</span><span style="font-size:11pt; color:rgb(195,151,29)"><b>web </b></span><span style="font-size:11pt; color:black">chrismandel.de</span></p>
</div>
</body></html>"""


def main():
    msg = EmailMessage()
    msg["From"] = CFG["email"]
    msg["To"] = TO
    msg["Subject"] = SUBJECT
    msg.set_content(TEXT_BODY)
    msg.add_alternative(HTML_BODY, subtype="html")

    ctx = ssl.create_default_context()
    with smtplib.SMTP(CFG["smtp_host"], CFG["smtp_port"]) as s:
        s.starttls(context=ctx)
        s.login(CFG["email"], CFG["password"])
        s.send_message(msg)
    print(f"OK gesendet von {CFG['email']} an {TO}")

    try:
        with imaplib.IMAP4_SSL(CFG["imap_host"], CFG["imap_port"]) as m:
            m.login(CFG["email"], CFG["password"])
            m.append("Gesendet", "\\Seen", imaplib.Time2Internaldate(time.time()), msg.as_bytes())
        print("OK Kopie in Gesendet abgelegt")
    except Exception as e:
        print(f"WARN Kopie in Gesendet fehlgeschlagen: {e}")


if __name__ == "__main__":
    main()
