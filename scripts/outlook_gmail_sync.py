#!/usr/bin/env python3
"""
Outlook → Gmail Kontakt-Sync
Liest alle Kontakte aus Outlook (Microsoft Graph) und überträgt sie nach Gmail (Google People API).
Bereits vorhandene Kontakte werden aktualisiert, neue werden angelegt.
"""

import json, requests, time
from pathlib import Path

WORKSPACE = Path("/home/bolla/.openclaw/workspace")
MS_TOKEN_FILE = WORKSPACE / "config/ms_token.json"
GOOGLE_TOKEN_FILE = WORKSPACE / "config/google_token.json"
GOOGLE_CLIENT_FILE = WORKSPACE / "config/google_client.json"
MS_CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"

# ── Microsoft Token ────────────────────────────────────────────────────────────
def get_ms_token():
    data = json.loads(MS_TOKEN_FILE.read_text())
    r = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data={
        "client_id": MS_CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": data["refresh_token"],
        "scope": "https://graph.microsoft.com/Contacts.Read offline_access"
    })
    token = r.json()
    if "access_token" not in token:
        raise RuntimeError(f"MS Token Fehler: {token}")
    return token["access_token"]

# ── Google Token ───────────────────────────────────────────────────────────────
def get_google_token():
    data = json.loads(GOOGLE_TOKEN_FILE.read_text())
    client = json.loads(GOOGLE_CLIENT_FILE.read_text())
    if "refresh_token" in data:
        r = requests.post("https://oauth2.googleapis.com/token", data={
            "refresh_token": data["refresh_token"],
            "client_id": client["client_id"],
            "client_secret": client["client_secret"],
            "grant_type": "refresh_token"
        })
        new = r.json()
        if "access_token" in new:
            data["access_token"] = new["access_token"]
            GOOGLE_TOKEN_FILE.write_text(json.dumps(data, indent=2))
    return data["access_token"]

# ── Outlook Kontakte lesen ─────────────────────────────────────────────────────
def get_outlook_contacts(token):
    headers = {"Authorization": f"Bearer {token}"}
    contacts = []
    url = "https://graph.microsoft.com/v1.0/me/contacts?$top=100&$select=displayName,emailAddresses,mobilePhone,homePhones,businessPhones,birthday,personalNotes"
    while url:
        r = requests.get(url, headers=headers)
        data = r.json()
        contacts.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return contacts

# ── Google Kontakte lesen ──────────────────────────────────────────────────────
def get_google_contacts(token):
    headers = {"Authorization": f"Bearer {token}"}
    contacts = []
    page_token = None
    while True:
        params = {"personFields": "names,emailAddresses,phoneNumbers,biographies,birthdays", "pageSize": 100}
        if page_token:
            params["pageToken"] = page_token
        r = requests.get("https://people.googleapis.com/v1/people/me/connections",
                         headers=headers, params=params)
        data = r.json()
        contacts.extend(data.get("connections", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return contacts

# ── Kontakt in Google anlegen/aktualisieren ────────────────────────────────────
def upsert_google_contact(token, outlook_contact, existing_map):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    name = outlook_contact.get("displayName", "")
    emails = [e["address"] for e in outlook_contact.get("emailAddresses", []) if e.get("address")]
    phones = []
    for p in [outlook_contact.get("mobilePhone"), *outlook_contact.get("homePhones", []), *outlook_contact.get("businessPhones", [])]:
        if p:
            phones.append(p)
    birthday = outlook_contact.get("birthday")
    notes = outlook_contact.get("personalNotes", "")

    # Google Person Body aufbauen
    body = {"names": [{"displayName": name, "unstructuredName": name}]}
    if emails:
        body["emailAddresses"] = [{"value": e} for e in emails]
    if phones:
        body["phoneNumbers"] = [{"value": p} for p in phones]
    if notes:
        body["biographies"] = [{"value": notes, "contentType": "TEXT_PLAIN"}]
    if birthday:
        try:
            # Format: 1970-01-01T00:00:00Z oder 0001-12-21T...
            parts = birthday.split("T")[0].split("-")
            year = int(parts[0]) if int(parts[0]) > 1 else None
            body["birthdays"] = [{"date": {
                "year": year or 0,
                "month": int(parts[1]),
                "day": int(parts[2])
            }}]
        except:
            pass

    # Existiert der Kontakt schon in Google? (Match über E-Mail oder Name)
    resource_name = None
    etag = None
    for email in emails:
        if email.lower() in existing_map:
            resource_name, etag = existing_map[email.lower()]
            break
    if not resource_name and name.lower() in existing_map:
        resource_name, etag = existing_map[name.lower()]

    if resource_name:
        # Update — etag muss mitgeschickt werden
        body["etag"] = etag
        r = requests.patch(
            f"https://people.googleapis.com/v1/{resource_name}:updateContact",
            headers=headers,
            params={"updatePersonFields": "names,emailAddresses,phoneNumbers,biographies,birthdays"},
            json=body
        )
        return "updated" if r.status_code == 200 else f"error_update:{r.status_code}"
    else:
        # Neu anlegen
        r = requests.post("https://people.googleapis.com/v1/people:createContact",
                          headers=headers, json=body)
        return "created" if r.status_code == 200 else f"error_create:{r.status_code}"

# ── Hauptprogramm ──────────────────────────────────────────────────────────────
def main():
    print("Starte Outlook → Gmail Sync...")
    
    ms_token = get_ms_token()
    google_token = get_google_token()
    
    print("Lade Outlook-Kontakte...")
    outlook_contacts = get_outlook_contacts(ms_token)
    print(f"  {len(outlook_contacts)} Kontakte in Outlook gefunden")
    
    print("Lade Gmail-Kontakte...")
    google_contacts = get_google_contacts(google_token)
    print(f"  {len(google_contacts)} Kontakte in Gmail gefunden")
    
    # Index aufbauen: E-Mail/Name → (resourceName, etag)
    existing_map = {}
    for c in google_contacts:
        rn = c.get("resourceName")
        etag = c.get("etag", "")
        for e in c.get("emailAddresses", []):
            existing_map[e.get("value", "").lower()] = (rn, etag)
        for n in c.get("names", []):
            existing_map[n.get("displayName", "").lower()] = (rn, etag)
    
    # Sync
    created = updated = errors = 0
    for i, contact in enumerate(outlook_contacts):
        name = contact.get("displayName", "?")
        result = upsert_google_contact(google_token, contact, existing_map)
        if result == "created":
            created += 1
            print(f"  + {name}")
        elif result == "updated":
            updated += 1
        else:
            errors += 1
            print(f"  ⚠️ {name}: {result}")
        time.sleep(0.1)  # Rate Limit schonen
    
    print(f"\n✅ Sync abgeschlossen!")
    print(f"   Neu angelegt: {created}")
    print(f"   Aktualisiert: {updated}")
    print(f"   Fehler: {errors}")

if __name__ == "__main__":
    main()
