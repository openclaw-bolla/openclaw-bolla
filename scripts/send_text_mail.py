#!/usr/bin/env python3
"""
Einfacher Text-Mail-Versand über MS Graph, Absender ernstmandel@outlook.de
(outlook_token.json, Scope inkl. Mail.Send). Reine Textmail, kein Anhang.

Nutzung:
  python3 send_text_mail.py --to X --subject Y --bodyfile /pfad/body.txt
  python3 send_text_mail.py --to X --subject Y --body "Text..."
"""
import argparse, requests
from outlook_oauth2 import refresh_access_token

GRAPH = "https://graph.microsoft.com/v1.0"


def send_text(token, to, subject, body):
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    msg = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to}}],
        },
        "saveToSentItems": True,
    }
    r = requests.post(f"{GRAPH}/me/sendMail", headers=h, json=msg)
    if r.status_code != 202:
        raise RuntimeError(f"Send-Fehler {r.status_code}: {r.text[:300]}")
    print(f"✓ Mail an {to} gesendet (Betreff: {subject}).")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--to", required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--body", default="")
    p.add_argument("--bodyfile", default="")
    a = p.parse_args()
    body = open(a.bodyfile, encoding="utf-8").read() if a.bodyfile else a.body
    token = refresh_access_token()
    send_text(token, a.to, a.subject, body)
