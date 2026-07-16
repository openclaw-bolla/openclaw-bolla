#!/usr/bin/env python3
"""
SMTP-Sender für Renate Mandel (renatemandel@wtnet.de, wilhelm.tel).

Zugangsdaten liegen in config/reni_smtp.json (chmod 600), Passwort wird
NIE im Code oder Chat gespeichert — nur per --setpass verdeckt eingegeben.

Nutzung:
  python3 reni_mail.py --setpass                 # Passwort verdeckt setzen
  python3 reni_mail.py --to X --subject Y --body Z
"""
import argparse, imaplib, json, os, smtplib, ssl, getpass, stat
from email.message import EmailMessage
from pathlib import Path

CFG = Path("/home/bolla/workspace/config/reni_smtp.json")
DEFAULTS = {"email": "renatemandel@wtnet.de", "smtp": "mail.wtnet.de", "port": 465,
            "imap": "mail.wtnet.de", "imap_port": 993, "sent_folder": "Gesendet", "password": ""}


def load():
    if CFG.exists():
        d = DEFAULTS | json.loads(CFG.read_text())
    else:
        d = dict(DEFAULTS)
    return d


def save(d):
    CFG.write_text(json.dumps(d, indent=2, ensure_ascii=False))
    os.chmod(CFG, stat.S_IRUSR | stat.S_IWUSR)  # 600


def setpass():
    d = load()
    pw = getpass.getpass(f"Passwort für {d['email']}: ")
    if not pw:
        print("Abgebrochen (leer).")
        return
    d["password"] = pw
    save(d)
    print(f"✓ Passwort gespeichert in {CFG} (chmod 600).")


def send_mail(to, subject, body):
    d = load()
    if not d.get("password"):
        raise SystemExit("Kein Passwort gesetzt — erst:  python3 reni_mail.py --setpass")
    msg = EmailMessage()
    msg["From"] = d["email"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(d["smtp"], d["port"], context=ctx) as s:
        s.login(d["email"], d["password"])
        s.send_message(msg)
    print(f"✓ Mail von {d['email']} an {to} gesendet.")

    try:
        with imaplib.IMAP4_SSL(d["imap"], d["imap_port"]) as m:
            m.login(d["email"], d["password"])
            m.append(d["sent_folder"], "\\Seen", imaplib.Time2Internaldate(__import__("time").time()),
                     msg.as_bytes())
        print(f"✓ Kopie in {d['sent_folder']} abgelegt.")
    except Exception as e:
        print(f"⚠ Kopie konnte nicht in {d['sent_folder']} abgelegt werden: {e}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--setpass", action="store_true")
    p.add_argument("--to", default="")
    p.add_argument("--subject", default="")
    p.add_argument("--body", default="")
    a = p.parse_args()
    if a.setpass:
        setpass()
    elif a.to:
        send_mail(a.to, a.subject, a.body)
    else:
        print("Nutze --setpass  ODER  --to/--subject/--body")
