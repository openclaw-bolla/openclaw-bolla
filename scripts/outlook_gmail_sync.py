#!/usr/bin/env python3
"""
Bidirektionaler Outlook ↔ Gmail Kontakt-Sync (inkl. Fotos)
- Outlook → Gmail: Kontakte + Fotos übertragen
- Gmail → Outlook: Neue Kontakte + Fotos zurück übertragen
- Match über E-Mail oder Name
"""

import json, requests, time, base64, sys
from pathlib import Path

WORKSPACE = Path("/home/bolla/workspace")
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
        "scope": "https://graph.microsoft.com/Contacts.ReadWrite offline_access"
    })
    token = r.json()
    if "access_token" not in token:
        raise RuntimeError(f"MS Token Fehler: {token}")
    # Save refreshed token
    if "refresh_token" in token:
        data.update(token)
        MS_TOKEN_FILE.write_text(json.dumps(data, indent=2))
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
    url = ("https://graph.microsoft.com/v1.0/me/contacts?$top=100"
           "&$select=id,displayName,givenName,surname,emailAddresses,mobilePhone,"
           "homePhones,businessPhones,birthday,personalNotes,companyName,jobTitle")
    while url:
        r = requests.get(url, headers=headers)
        data = r.json()
        contacts.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return contacts

# ── Outlook Kontaktfoto lesen ──────────────────────────────────────────────────
def get_outlook_photo(token, contact_id):
    """Gibt Foto als bytes zurück oder None."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}/photo/$value",
        headers=headers
    )
    if r.status_code == 200:
        return r.content
    return None

# ── Outlook Kontaktfoto setzen ─────────────────────────────────────────────────
def set_outlook_photo(token, contact_id, photo_bytes):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "image/jpeg"
    }
    r = requests.put(
        f"https://graph.microsoft.com/v1.0/me/contacts/{contact_id}/photo/$value",
        headers=headers,
        data=photo_bytes
    )
    return r.status_code in (200, 204)

# ── Google Kontakte lesen ──────────────────────────────────────────────────────
def get_google_contacts(token):
    headers = {"Authorization": f"Bearer {token}"}
    contacts = []
    page_token = None
    while True:
        params = {
            "personFields": "names,emailAddresses,phoneNumbers,biographies,birthdays,photos,organizations",
            "pageSize": 100
        }
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

# ── Google Kontaktfoto lesen ───────────────────────────────────────────────────
def get_google_photo_url(google_contact):
    """Gibt die Foto-URL zurück oder None (ignoriert Default-Fotos)."""
    for photo in google_contact.get("photos", []):
        if photo.get("metadata", {}).get("source", {}).get("type") == "CONTACT":
            url = photo.get("url")
            if url and "default" not in url.lower():
                return url
    return None

def download_google_photo(token, url):
    """Lädt ein Google-Kontaktfoto herunter."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.content
    return None

# ── Google Kontaktfoto setzen ──────────────────────────────────────────────────
def set_google_photo(token, resource_name, photo_bytes):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"photoBytes": base64.b64encode(photo_bytes).decode("utf-8")}
    r = requests.patch(
        f"https://people.googleapis.com/v1/{resource_name}:updateContactPhoto",
        headers=headers, json=body
    )
    return r.status_code == 200

# ── Outlook → Google Body bauen ────────────────────────────────────────────────
def outlook_to_google_body(contact):
    name = contact.get("displayName", "")
    given = contact.get("givenName", "")
    family = contact.get("surname", "")
    emails = [e["address"] for e in contact.get("emailAddresses", []) if e.get("address")]
    phones = []
    for p in [contact.get("mobilePhone"), *contact.get("homePhones", []), *contact.get("businessPhones", [])]:
        if p:
            phones.append(p)
    birthday = contact.get("birthday")
    notes = contact.get("personalNotes", "")
    company = contact.get("companyName", "")
    title = contact.get("jobTitle", "")

    body = {"names": [{"displayName": name, "givenName": given, "familyName": family}]}
    if emails:
        body["emailAddresses"] = [{"value": e} for e in emails]
    if phones:
        body["phoneNumbers"] = [{"value": p} for p in phones]
    if notes:
        body["biographies"] = [{"value": notes, "contentType": "TEXT_PLAIN"}]
    if company or title:
        body["organizations"] = [{"name": company or "", "title": title or ""}]
    if birthday:
        try:
            parts = birthday.split("T")[0].split("-")
            year = int(parts[0]) if int(parts[0]) > 1 else None
            body["birthdays"] = [{"date": {
                "year": year or 0, "month": int(parts[1]), "day": int(parts[2])
            }}]
        except:
            pass
    return body

# ── Google → Outlook Body bauen ────────────────────────────────────────────────
def google_to_outlook_body(contact):
    body = {}
    names = contact.get("names", [{}])
    if names:
        body["displayName"] = names[0].get("displayName", "")
        body["givenName"] = names[0].get("givenName", "")
        body["surname"] = names[0].get("familyName", "")
    
    emails = contact.get("emailAddresses", [])
    if emails:
        body["emailAddresses"] = [{"address": e["value"], "name": e.get("type", "")} for e in emails]
    
    phones = contact.get("phoneNumbers", [])
    if phones:
        # Erste Nummer als mobilePhone
        body["mobilePhone"] = phones[0].get("value", "")
        if len(phones) > 1:
            body["homePhones"] = [p["value"] for p in phones[1:]]
    
    bios = contact.get("biographies", [])
    if bios:
        body["personalNotes"] = bios[0].get("value", "")
    
    orgs = contact.get("organizations", [])
    if orgs:
        body["companyName"] = orgs[0].get("name", "")
        body["jobTitle"] = orgs[0].get("title", "")
    
    birthdays = contact.get("birthdays", [])
    if birthdays:
        d = birthdays[0].get("date", {})
        if d.get("month") and d.get("day"):
            year = d.get("year", 0) or 1
            body["birthday"] = f"{year:04d}-{d['month']:02d}-{d['day']:02d}T00:00:00Z"
    
    return body

# ── Index aufbauen ─────────────────────────────────────────────────────────────
def name_key(s):
    """Normalisierter Namens-Schlüssel: lowercase, Tokens sortiert.
    So matchen 'Ingrid Lieb' und 'Lieb Ingrid' aufeinander (sonst Dubletten,
    wenn ein System Vorname-Nachname und das andere Nachname-Vorname führt)."""
    return " ".join(sorted(s.lower().split()))

def build_google_index(contacts):
    """E-Mail/Name → (resourceName, etag)"""
    idx = {}
    for c in contacts:
        rn = c.get("resourceName")
        etag = c.get("etag", "")
        for e in c.get("emailAddresses", []):
            idx[e.get("value", "").lower()] = (rn, etag)
        for n in c.get("names", []):
            dn = n.get("displayName", "").lower()
            if dn:
                idx[dn] = (rn, etag)
                idx[name_key(dn)] = (rn, etag)
    return idx

def build_outlook_index(contacts):
    """E-Mail/Name → contact dict"""
    idx = {}
    for c in contacts:
        for e in c.get("emailAddresses", []):
            idx[e.get("address", "").lower()] = c
        dn = c.get("displayName", "").lower()
        if dn:
            idx[dn] = c
            idx[name_key(dn)] = c
    return idx

# ── Sync Outlook → Gmail ──────────────────────────────────────────────────────
def sync_outlook_to_gmail(ms_token, g_token, outlook_contacts, google_index):
    print("\n═══ Outlook → Gmail ═══")
    created = updated = photos_synced = errors = 0

    for contact in outlook_contacts:
        name = contact.get("displayName", "?")
        emails = [e["address"].lower() for e in contact.get("emailAddresses", []) if e.get("address")]
        body = outlook_to_google_body(contact)
        
        # Match finden
        resource_name = etag = None
        for email in emails:
            if email in google_index:
                resource_name, etag = google_index[email]
                break
        if not resource_name and name.lower() in google_index:
            resource_name, etag = google_index[name.lower()]
        if not resource_name and name_key(name) in google_index:
            resource_name, etag = google_index[name_key(name)]

        headers = {"Authorization": f"Bearer {g_token}", "Content-Type": "application/json"}

        if resource_name:
            body["etag"] = etag
            r = requests.patch(
                f"https://people.googleapis.com/v1/{resource_name}:updateContact",
                headers=headers,
                params={"updatePersonFields": "names,emailAddresses,phoneNumbers,biographies,birthdays,organizations"},
                json=body
            )
            if r.status_code == 200:
                updated += 1
                # Foto sync
                photo = get_outlook_photo(ms_token, contact["id"])
                if photo:
                    if set_google_photo(g_token, resource_name, photo):
                        photos_synced += 1
                time.sleep(0.1)
            else:
                errors += 1
                print(f"  ⚠️ Update {name}: {r.status_code}")
        else:
            r = requests.post("https://people.googleapis.com/v1/people:createContact",
                              headers=headers, json=body)
            if r.status_code == 200:
                created += 1
                new_rn = r.json().get("resourceName")
                print(f"  + {name}")
                # Foto sync
                photo = get_outlook_photo(ms_token, contact["id"])
                if photo and new_rn:
                    if set_google_photo(g_token, new_rn, photo):
                        photos_synced += 1
                time.sleep(0.1)
            else:
                errors += 1
                print(f"  ⚠️ Create {name}: {r.status_code}")
        time.sleep(0.1)

    print(f"  → Neu: {created}, Aktualisiert: {updated}, Fotos: {photos_synced}, Fehler: {errors}")
    return created, updated, photos_synced, errors

# ── Sync Gmail → Outlook ──────────────────────────────────────────────────────
def sync_gmail_to_outlook(ms_token, g_token, google_contacts, outlook_index):
    print("\n═══ Gmail → Outlook ═══")
    created = updated = photos_synced = errors = 0
    headers_ms = {"Authorization": f"Bearer {ms_token}", "Content-Type": "application/json"}

    for contact in google_contacts:
        names = contact.get("names", [{}])
        name = names[0].get("displayName", "?") if names else "?"
        emails = [e.get("value", "").lower() for e in contact.get("emailAddresses", []) if e.get("value")]

        # Match finden
        outlook_match = None
        for email in emails:
            if email in outlook_index:
                outlook_match = outlook_index[email]
                break
        if not outlook_match and name.lower() in outlook_index:
            outlook_match = outlook_index[name.lower()]
        if not outlook_match and name_key(name) in outlook_index:
            outlook_match = outlook_index[name_key(name)]

        if outlook_match:
            # Bereits in Outlook → Foto sync (Gmail → Outlook) falls Outlook kein Foto hat
            outlook_id = outlook_match["id"]
            existing_photo = get_outlook_photo(ms_token, outlook_id)
            if not existing_photo:
                photo_url = get_google_photo_url(contact)
                if photo_url:
                    photo = download_google_photo(g_token, photo_url)
                    if photo and set_outlook_photo(ms_token, outlook_id, photo):
                        photos_synced += 1
            updated += 1
            time.sleep(0.1)
        else:
            # Neu in Gmail → in Outlook anlegen
            body = google_to_outlook_body(contact)
            if not body.get("displayName"):
                continue  # Kein Name, überspringen
            r = requests.post(
                "https://graph.microsoft.com/v1.0/me/contacts",
                headers=headers_ms,
                json=body
            )
            if r.status_code == 201:
                created += 1
                new_id = r.json().get("id")
                print(f"  + {name}")
                # Foto sync
                photo_url = get_google_photo_url(contact)
                if photo_url and new_id:
                    photo = download_google_photo(g_token, photo_url)
                    if photo and set_outlook_photo(ms_token, new_id, photo):
                        photos_synced += 1
                time.sleep(0.1)
            else:
                errors += 1
                print(f"  ⚠️ Create {name}: {r.status_code}")
            time.sleep(0.1)

    print(f"  → Neu: {created}, Geprüft: {updated}, Fotos: {photos_synced}, Fehler: {errors}")
    return created, updated, photos_synced, errors

# ── Hauptprogramm ──────────────────────────────────────────────────────────────
def main():
    print("═" * 50)
    print("Outlook ↔ Gmail Kontakt-Sync (bidirektional)")
    print("═" * 50)

    ms_token = get_ms_token()
    g_token = get_google_token()

    print("\nLade Kontakte...")
    outlook_contacts = get_outlook_contacts(ms_token)
    print(f"  Outlook: {len(outlook_contacts)} Kontakte")

    google_contacts = get_google_contacts(g_token)
    print(f"  Gmail:   {len(google_contacts)} Kontakte")

    # Indices aufbauen
    google_index = build_google_index(google_contacts)
    outlook_index = build_outlook_index(outlook_contacts)

    # Sync in beide Richtungen
    o2g = sync_outlook_to_gmail(ms_token, g_token, outlook_contacts, google_index)
    g2o = sync_gmail_to_outlook(ms_token, g_token, google_contacts, outlook_index)

    print("\n" + "═" * 50)
    print("✅ Sync abgeschlossen!")
    print(f"  Outlook → Gmail: {o2g[0]} neu, {o2g[1]} aktualisiert, {o2g[2]} Fotos")
    print(f"  Gmail → Outlook: {g2o[0]} neu, {g2o[1]} geprüft, {g2o[2]} Fotos")
    total_errors = o2g[3] + g2o[3]
    if total_errors:
        print(f"  ⚠️ {total_errors} Fehler insgesamt")
    print("═" * 50)

if __name__ == "__main__":
    main()
