#!/usr/bin/env python3
"""Löscht benannte Kontakte in BEIDEN Systemen (Gmail + Outlook),
damit der bidirektionale Sync sie nicht zurückholt.
DRY-RUN per Default; mit 'apply' wird gelöscht."""
import json, sys, requests
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
MS_TOKEN_FILE = WORKSPACE / "config/ms_token.json"
GOOGLE_TOKEN_FILE = WORKSPACE / "config/google_token.json"
GOOGLE_CLIENT_FILE = WORKSPACE / "config/google_client.json"
MS_CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"
APPLY = len(sys.argv) > 1 and sys.argv[1] == "apply"

TARGETS = ["Kaminholz Bollow", "Frau Brunhilde Albiez", "Nele Fuß"]

def get_ms_token():
    data = json.loads(MS_TOKEN_FILE.read_text())
    r = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data={
        "client_id": MS_CLIENT_ID, "grant_type": "refresh_token",
        "refresh_token": data["refresh_token"],
        "scope": "https://graph.microsoft.com/Contacts.ReadWrite offline_access"})
    t = r.json()
    if "refresh_token" in t:
        data.update(t); MS_TOKEN_FILE.write_text(json.dumps(data, indent=2))
    return t["access_token"]

def get_google_token():
    data = json.loads(GOOGLE_TOKEN_FILE.read_text())
    client = json.loads(GOOGLE_CLIENT_FILE.read_text())
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "refresh_token": data["refresh_token"], "client_id": client["client_id"],
        "client_secret": client["client_secret"], "grant_type": "refresh_token"})
    new = r.json()
    if "access_token" in new:
        data["access_token"] = new["access_token"]; GOOGLE_TOKEN_FILE.write_text(json.dumps(data, indent=2))
    return data["access_token"]

def ms_delete(token):
    h = {"Authorization": f"Bearer {token}"}; out=[]
    url=("https://graph.microsoft.com/v1.0/me/contacts?$top=100&$select=id,displayName")
    contacts=[]
    while url:
        d=requests.get(url,headers=h).json(); contacts.extend(d.get("value",[]))
        url=d.get("@odata.nextLink")
    for c in contacts:
        if c["displayName"] in TARGETS:
            out.append(f"  OUTLOOK 🗑️ {c['displayName']} ({c['id'][:18]}…)")
            if APPLY:
                r=requests.delete(f"https://graph.microsoft.com/v1.0/me/contacts/{c['id']}",headers=h)
                if r.status_code not in (200,204): out.append(f"     FEHLER {r.status_code}")
    return out

def google_delete(token):
    h = {"Authorization": f"Bearer {token}"}; out=[]
    contacts=[]; page=None
    while True:
        params={"personFields":"names","pageSize":200}
        if page: params["pageToken"]=page
        d=requests.get("https://people.googleapis.com/v1/people/me/connections",headers=h,params=params).json()
        contacts.extend(d.get("connections",[])); page=d.get("nextPageToken")
        if not page: break
    for c in contacts:
        names=c.get("names",[]); dn=names[0].get("displayName","") if names else ""
        if dn in TARGETS:
            rn=c["resourceName"]
            out.append(f"  GMAIL   🗑️ {dn} ({rn})")
            if APPLY:
                r=requests.delete(f"https://people.googleapis.com/v1/{rn}:deleteContact",headers=h)
                if r.status_code not in (200,204): out.append(f"     FEHLER {r.status_code}: {r.text[:100]}")
    return out

def main():
    log=[]
    log+=google_delete(get_google_token())
    log+=ms_delete(get_ms_token())
    print("\n".join(log) if log else "  (nichts gefunden)")
    print("\n>>> "+("GELÖSCHT" if APPLY else "DRY-RUN"))

if __name__=="__main__":
    main()
