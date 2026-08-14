#!/usr/bin/env python3
"""Sendet EPUB(s) per Microsoft Graph (Upload-Session, >3MB-fähig) an Send-to-Kindle.
Absender: ernstmandel@outlook.de (outlook_token.json, Scope inkl. Mail.ReadWrite).
"""
import sys, json, requests
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from outlook_oauth2 import refresh_access_token

GRAPH = "https://graph.microsoft.com/v1.0"
KINDLE = "ernstmandel_MnAuOy@kindle.com"
CHUNK = 1310720  # 1.25 MiB (Vielfaches von 320 KiB)

def send_epub(token, path, subject):
    p = Path(path); data = p.read_bytes(); size = len(data)
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    # 1) Draft erstellen
    msg = {"subject": subject, "body": {"contentType": "Text", "content": ""},
           "toRecipients": [{"emailAddress": {"address": KINDLE}}]}
    r = requests.post(f"{GRAPH}/me/messages", headers=h, json=msg)
    r.raise_for_status(); mid = r.json()["id"]
    # 2) Upload-Session für Anhang
    item = {"AttachmentItem": {"attachmentType": "file", "name": p.name, "size": size}}
    r = requests.post(f"{GRAPH}/me/messages/{mid}/attachments/createUploadSession", headers=h, json=item)
    r.raise_for_status(); url = r.json()["uploadUrl"]
    # 3) chunked PUT
    start = 0
    while start < size:
        end = min(start + CHUNK, size) - 1
        chunk = data[start:end+1]
        rr = requests.put(url, headers={
            "Content-Length": str(len(chunk)),
            "Content-Range": f"bytes {start}-{end}/{size}",
        }, data=chunk)
        if rr.status_code not in (200, 201, 202):
            raise RuntimeError(f"Upload-Fehler {rr.status_code}: {rr.text[:200]}")
        start = end + 1
    # 4) senden
    r = requests.post(f"{GRAPH}/me/messages/{mid}/send", headers=h)
    if r.status_code != 202:
        raise RuntimeError(f"Send-Fehler {r.status_code}: {r.text[:200]}")
    print(f"  ✓ '{p.name}' ({size/1024/1024:.2f} MB) an {KINDLE} gesendet.")

if __name__ == "__main__":
    token = refresh_access_token()
    jobs = [
        ("/mnt/d/OneDrive/Dokumente/Bolla/AURORA/2_eBook/AURORA_deutsch.epub", "AURORA (deutsch)"),
        ("/mnt/d/OneDrive/Dokumente/Bolla/AURORA/2_eBook/AURORA_english.epub", "AURORA (English)"),
    ]
    for path, subj in jobs:
        send_epub(token, path, subj)
    print("Fertig. Amazon schickt gleich je eine Verifikations-Mail an ernstmandel@outlook.de.")
