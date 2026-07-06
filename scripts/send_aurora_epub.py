#!/usr/bin/env python3
"""Sendet das/die AURORA-EPUB(s) mit kurzer Begleitmail per Microsoft Graph.
Absender: ernstmandel@outlook.de (outlook_token.json). Für Rezensions-/Freiexemplare
an Marketing-Kontakte, die das Buch angefragt haben.

Nutzung:
  python3 send_aurora_epub.py --to EMPFAENGER --lang de|en|both [--subject "..."]
"""
import sys, json, argparse, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from outlook_oauth2 import refresh_access_token

GRAPH = "https://graph.microsoft.com/v1.0"
CHUNK = 1310720  # 1.25 MiB
EPUB_DE = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA/2_eBook/AURORA_deutsch.epub"
EPUB_EN = "/mnt/d/OneDrive/Dokumente/Bolla/AURORA/2_eBook/AURORA_english.epub"

BODY_DE = """Hallo,

vielen Dank für Ihr Interesse an „AURORA“! Im Anhang finden Sie das Buch als E-Book (EPUB), das sich in allen gängigen Leseprogrammen öffnen lässt.

Über eine Erwähnung oder eine kurze Rückmeldung freue ich mich sehr – es besteht aber keinerlei Verpflichtung. Bei Fragen zur Entstehungsgeschichte (Mensch + KI) stehe ich gern zur Verfügung.

Herzliche Grüße
Chris Mandel
Autor von „AURORA“ · https://www.amazon.de/dp/B0H6JD2KDJ
"""

BODY_EN = """Hello,

thank you for your interest in "AURORA"! Please find the book attached as an e-book (EPUB), which opens in all common reading apps.

I'd be glad about a mention or any feedback — but there's no obligation at all. Happy to answer any questions about the origin story (human + AI).

Best regards,
Chris Mandel
Author of "AURORA" · https://www.amazon.com/dp/B0H6JQK6JQ
"""

def create_draft(token, to, subject, body):
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    msg = {"subject": subject, "body": {"contentType": "Text", "content": body},
           "toRecipients": [{"emailAddress": {"address": to}}]}
    r = requests.post(f"{GRAPH}/me/messages", headers=h, json=msg)
    r.raise_for_status()
    return r.json()["id"]

def attach(token, mid, path):
    p = Path(path); data = p.read_bytes(); size = len(data)
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    item = {"AttachmentItem": {"attachmentType": "file", "name": p.name, "size": size}}
    r = requests.post(f"{GRAPH}/me/messages/{mid}/attachments/createUploadSession", headers=h, json=item)
    r.raise_for_status(); url = r.json()["uploadUrl"]
    start = 0
    while start < size:
        end = min(start + CHUNK, size) - 1
        chunk = data[start:end+1]
        rr = requests.put(url, headers={"Content-Length": str(len(chunk)),
             "Content-Range": f"bytes {start}-{end}/{size}"}, data=chunk)
        if rr.status_code not in (200, 201, 202):
            raise RuntimeError(f"Upload-Fehler {rr.status_code}: {rr.text[:200]}")
        start = end + 1

def send(token, mid):
    r = requests.post(f"{GRAPH}/me/messages/{mid}/send",
                      headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 202:
        raise RuntimeError(f"Send-Fehler {r.status_code}: {r.text[:200]}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--lang", choices=["de", "en", "both"], default="both")
    ap.add_argument("--subject", default="")
    a = ap.parse_args()
    if a.lang == "de":
        body, files, subj = BODY_DE, [EPUB_DE], a.subject or "AURORA – Ihr Rezensionsexemplar (EPUB)"
    elif a.lang == "en":
        body, files, subj = BODY_EN, [EPUB_EN], a.subject or "AURORA — your review copy (EPUB)"
    else:
        body, files, subj = BODY_EN, [EPUB_EN, EPUB_DE], a.subject or "AURORA — your review copy (EPUB, English & German)"
    token = refresh_access_token()
    mid = create_draft(token, a.to, subj, body)
    for f in files:
        attach(token, mid, f); print(f"  angehängt: {Path(f).name}")
    send(token, mid)
    print(f"✓ AURORA-EPUB ({a.lang}) an {a.to} gesendet.")
