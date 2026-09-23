import json, os, sys, urllib.request, urllib.parse
from pathlib import Path

WORKSPACE = os.path.expanduser("~/workspace")

def graph_calendar_token():
    cfg  = json.loads(Path(os.path.join(WORKSPACE, "config/outlook_oauth2.json")).read_text())
    tokf = os.path.join(WORKSPACE, "config/outlook_token.json")
    tok  = json.loads(Path(tokf).read_text())
    data = urllib.parse.urlencode({
        "client_id": cfg["client_id"], "client_secret": cfg["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
        "scope": "Mail.ReadWrite Mail.Send Calendars.ReadWrite Contacts.ReadWrite Tasks.ReadWrite offline_access",
    }).encode()
    req = urllib.request.Request("https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
                                 data=data, method="POST")
    with urllib.request.urlopen(req, timeout=20) as r:
        new = json.loads(r.read())
    tok.update(new)
    Path(tokf).write_text(json.dumps(tok))
    return new["access_token"]

token = graph_calendar_token()
qs = urllib.parse.urlencode({"startDateTime": "2026-09-24T00:00:00", "endDateTime": "2026-09-25T00:00:00",
                              "$select": "id,subject,start,end,location,bodyPreview,createdDateTime", "$top": "50"})
req = urllib.request.Request("https://graph.microsoft.com/v1.0/me/calendarView?" + qs,
        headers={"Authorization": f"Bearer {token}", "Prefer": 'outlook.timezone="Europe/Berlin"'})
with urllib.request.urlopen(req, timeout=20) as r:
    data = json.loads(r.read())

for ev in data.get("value", []):
    if "giovanni" in ev.get("subject","").lower():
        print(json.dumps({
            "id": ev["id"], "subject": ev["subject"],
            "start": ev["start"], "end": ev["end"],
            "location": ev.get("location",{}).get("displayName"),
            "created": ev.get("createdDateTime"),
            "bodyPreview": ev.get("bodyPreview","")[:200],
        }, ensure_ascii=False))
