import json, requests

tok = json.load(open("/home/bolla/workspace/config/cloudflare_token.json"))["api_token"]
H = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
ACC = "fdb35536a858c7fac78778c57625cd70"
ZONE = "d3cac22140736d264c6b3e7e475cfe30"
base = "https://api.cloudflare.com/client/v4"

# 1) Alte Web-Records (root + www, A/AAAA) löschen — Mail/Tunnel/ftp bleiben unberührt
recs = requests.get(f"{base}/zones/{ZONE}/dns_records", headers=H, params={"per_page": 100}, timeout=15).json()["result"]
kill = [r for r in recs if r["type"] in ("A", "AAAA") and r["name"] in ("chrismandel.de", "www.chrismandel.de")]
for r in kill:
    rid = r["id"]
    d = requests.delete(f"{base}/zones/{ZONE}/dns_records/{rid}", headers=H, timeout=15).json()
    print(("geloescht " if d.get("success") else "FEHLER   "), r["type"], r["name"], "->", r["content"])

# 2) Custom Domains ans Pages-Projekt haengen
for dom in ("chrismandel.de", "www.chrismandel.de"):
    a = requests.post(f"{base}/accounts/{ACC}/pages/projects/chrismandel/domains", headers=H, json={"name": dom}, timeout=20).json()
    status = (a.get("result") or {}).get("status") or json.dumps(a.get("errors"), ensure_ascii=False)
    print(("Domain+ " if a.get("success") else "Domain? "), dom, "|", status)

# 3) Sicherstellen, dass ein (proxied) CNAME auf pages.dev existiert (root via Flattening)
recs = requests.get(f"{base}/zones/{ZONE}/dns_records", headers=H, params={"per_page": 100}, timeout=15).json()["result"]
have = {(r["name"], r["type"]) for r in recs}
for name in ("chrismandel.de", "www.chrismandel.de"):
    if (name, "CNAME") in have or (name, "A") in have or (name, "AAAA") in have:
        print("DNS ok   ", name, "(Record vorhanden)")
        continue
    c = requests.post(f"{base}/zones/{ZONE}/dns_records", headers=H,
                      json={"type": "CNAME", "name": name, "content": "chrismandel.pages.dev", "proxied": True}, timeout=15).json()
    print(("CNAME+   " if c.get("success") else "CNAME?  "), name, "->", "chrismandel.pages.dev",
          "" if c.get("success") else json.dumps(c.get("errors"), ensure_ascii=False))
