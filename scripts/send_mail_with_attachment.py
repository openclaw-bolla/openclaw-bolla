#!/usr/bin/env python3
"""
HTML-Mail mit Dateianhang über MS Graph, Absender ernstmandel@outlook.de
(outlook_token.json, Scope inkl. Mail.Send). Nutzt createUploadSession,
damit auch Anhänge >3MB zuverlässig gehen.

Nutzung:
  python3 send_mail_with_attachment.py --to X --subject Y --bodyfile body.html --attach /pfad/datei.epub
"""
import argparse
import mimetypes
import os
import sys

import requests
from outlook_oauth2 import refresh_access_token

GRAPH = "https://graph.microsoft.com/v1.0"
CHUNK_SIZE = 320 * 1024 * 8  # 2.5MB, Vielfaches von 320KiB (MS-Vorgabe)


def send_with_attachment(token, to, subject, body_html, file_path):
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 1. Draft anlegen
    msg = {
        "subject": subject,
        "body": {"contentType": "HTML", "content": body_html},
        "toRecipients": [{"emailAddress": {"address": to}}],
    }
    r = requests.post(f"{GRAPH}/me/messages", headers=h, json=msg)
    if r.status_code != 201:
        raise RuntimeError(f"Draft-Fehler {r.status_code}: {r.text[:300]}")
    msg_id = r.json()["id"]

    # 2. Upload-Session für Anhang
    size = os.path.getsize(file_path)
    name = os.path.basename(file_path)
    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    session_body = {
        "AttachmentItem": {
            "attachmentType": "file",
            "name": name,
            "size": size,
            "contentType": content_type,
        }
    }
    r = requests.post(
        f"{GRAPH}/me/messages/{msg_id}/attachments/createUploadSession",
        headers=h,
        json=session_body,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"Upload-Session-Fehler {r.status_code}: {r.text[:300]}")
    upload_url = r.json()["uploadUrl"]

    with open(file_path, "rb") as f:
        start = 0
        while start < size:
            chunk = f.read(CHUNK_SIZE)
            end = start + len(chunk) - 1
            up_headers = {
                "Content-Length": str(len(chunk)),
                "Content-Range": f"bytes {start}-{end}/{size}",
            }
            resp = requests.put(upload_url, headers=up_headers, data=chunk)
            if resp.status_code not in (200, 201, 202):
                raise RuntimeError(f"Chunk-Upload-Fehler {resp.status_code}: {resp.text[:300]}")
            start += len(chunk)
            print(f"  Upload {min(start, size)}/{size} Bytes...")

    # 3. Senden
    r = requests.post(f"{GRAPH}/me/messages/{msg_id}/send", headers=h)
    if r.status_code != 202:
        raise RuntimeError(f"Send-Fehler {r.status_code}: {r.text[:300]}")
    print(f"✓ Mail an {to} mit Anhang '{name}' gesendet (Betreff: {subject}).")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--to", required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--bodyfile", required=True)
    p.add_argument("--attach", required=True)
    a = p.parse_args()
    body_html = open(a.bodyfile, encoding="utf-8").read()
    if not os.path.isfile(a.attach):
        sys.exit(f"Datei nicht gefunden: {a.attach}")
    token = refresh_access_token()
    send_with_attachment(token, a.to, a.subject, body_html, a.attach)
