#!/usr/bin/env python3
"""Fügt eine E-Mail zur Cloudflare-Access-Policy von bolla.chrismandel.de hinzu.
Aufruf: cf_access_add_email.py list | add <email>
Token wird nur intern gelesen, nie ausgegeben."""
import json, os, sys, urllib.request

CFG = os.path.expanduser("~/workspace/config/cloudflare_token.json")
cfg = json.load(open(CFG))
TOKEN = cfg.get("token") or cfg.get("api_token")
ACC = cfg.get("account_id")

def api(method, path, body=None):
    req = urllib.request.Request("https://api.cloudflare.com/client/v4" + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=30))

if not ACC:
    ACC = api("GET", "/accounts")["result"][0]["id"]
apps = [a for a in api("GET", f"/accounts/{ACC}/access/apps")["result"] if "chrismandel.de" in a.get("domain", "")]
for a in apps:
    print("APP:", a["id"], a.get("name"), a.get("domain"))
    for p in api("GET", f"/accounts/{ACC}/access/apps/{a['id']}/policies")["result"]:
        print("  POLICY:", p["id"], p["name"], p["decision"], [i.get("email", {}).get("email") for i in p.get("include", [])])
if len(sys.argv) == 3 and sys.argv[1] == "add":
    mail = sys.argv[2]
    a = apps[0]
    pol = next(p for p in api("GET", f"/accounts/{ACC}/access/apps/{a['id']}/policies")["result"] if p["decision"] == "allow")
    if not any(i.get("email", {}).get("email") == mail for i in pol["include"]):
        pol["include"].append({"email": {"email": mail}})
        r = api("PUT", f"/accounts/{ACC}/access/apps/{a['id']}/policies/{pol['id']}",
                {k: pol[k] for k in ("name", "decision", "include", "exclude", "require") if k in pol})
        print("OK" if r.get("success") else r.get("errors"))
    else:
        print("schon drin")
