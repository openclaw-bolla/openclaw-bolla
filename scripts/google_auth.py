#!/usr/bin/env python3
"""Google OAuth Device Flow für Contacts API."""
import json, requests, time
from pathlib import Path

CONFIG = Path("/home/bolla/.openclaw/workspace/config/google_client.json")
TOKEN_FILE = Path("/home/bolla/.openclaw/workspace/config/google_token.json")

with open(CONFIG) as f:
    creds = json.load(f)

CLIENT_ID = creds["client_id"]
CLIENT_SECRET = creds["client_secret"]
SCOPE = "https://www.googleapis.com/auth/contacts"

# Step 1: Request device code
r = requests.post("https://oauth2.googleapis.com/device/code", data={
    "client_id": CLIENT_ID,
    "scope": SCOPE
})
data = r.json()

print(f"\nÖffne diesen Link in Edge:\n{data['verification_url']}\n")
print(f"Gib diesen Code ein: {data['user_code']}\n")
print("Warte auf Bestätigung...")

# Step 2: Poll for token
interval = data.get("interval", 5)
device_code = data["device_code"]
while True:
    time.sleep(interval)
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth2:grant_type:device_code"
    })
    token = r.json()
    if "access_token" in token:
        with open(TOKEN_FILE, "w") as f:
            json.dump(token, f, indent=2)
        print("✅ Login erfolgreich!")
        break
    elif token.get("error") == "authorization_pending":
        continue
    else:
        print(f"Fehler: {token}")
        break
