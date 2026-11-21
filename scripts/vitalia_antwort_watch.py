#!/usr/bin/env python3
"""Wartet auf Antwort von Anne Herrmann (Vitalia) auf die Mail vom 21.11.2026 (Beitragspause).
Meldet in MP-Jobs (aktion) und beendet sich. Max. 14 Tage, Check alle 15 Min."""
import sys, time, json, urllib.request, urllib.parse
sys.path.insert(0, "/home/bolla/workspace/scripts")
from outlook_oauth2 import refresh_access_token
from job_status import mc_meldung

AB = "2026-11-21T19:00:00Z"
ENDE = time.time() + 14 * 86400
JOB = "vitalia_antwort_watch"

while time.time() < ENDE:
    try:
        t = refresh_access_token()
        f = urllib.parse.quote(f"from/emailAddress/address eq 'anne.herrmann@vitaliagesundheitszentrum.de' and receivedDateTime ge {AB}")
        url = f"https://graph.microsoft.com/v1.0/me/messages?$filter={f}&$top=5&$select=subject,receivedDateTime,bodyPreview"
        r = urllib.request.Request(url, headers={"Authorization": "Bearer " + t})
        v = json.load(urllib.request.urlopen(r))["value"]
        if v:
            m = v[0]
            mc_meldung(JOB, "📩 Vitalia: Anne hat geantwortet", f"Antwort zur Beitragspause da ({m['receivedDateTime'][:16]}): {m['bodyPreview'][:400]}", "aktion")
            break
    except Exception as e:
        print("Fehler", repr(e), flush=True)
    time.sleep(900)
