#!/usr/bin/env python3
"""Verschiebt Aldi-Nord-Newsletter aus dem Posteingang nach Ablage/Archiv/Angebote —
Workaround dafür, dass Microsoft Graph bei privaten Outlook.de-Konten keine
serverseitigen Mail-Regeln per API erlaubt (nur bei Firmenkonten). Läuft alle 2h
per Cron, damit die Mail archiviert ist, bevor sie im Posteingang gelöscht wird
(Grund für den bisher verpassten wöchentlichen Angebots-Scan)."""
import json, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from mission_control_api import get_token

ANGEBOTE_FOLDER_FILE = Path("/home/bolla/workspace/config/aldi_archive_folder.json")
ALDI_SENDERS = ["aldi-nord.de", "aldi.de", "aldi-nord.com"]

def graph(path, token, method="GET", body=None):
    req = urllib.request.Request(
        f"https://graph.microsoft.com/v1.0{path}",
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read()) if r.length != 0 else {}

def run():
    token = get_token()
    angebote_id = json.loads(ANGEBOTE_FOLDER_FILE.read_text())["id"]

    moved = 0
    for sender in ALDI_SENDERS:
        d = graph(f'/me/mailFolders/inbox/messages?$search="from:{sender}"&$top=25&$select=id,subject', token)
        for m in d.get("value", []):
            graph(f"/me/messages/{m['id']}/move", token, method="POST", body={"destinationId": angebote_id})
            print(f"Verschoben: {m.get('subject','')[:60]}")
            moved += 1
    print(f"Fertig — {moved} Mail(s) nach Ablage/Archiv/Angebote verschoben.")

if __name__ == "__main__":
    run()
