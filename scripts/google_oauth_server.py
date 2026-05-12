#!/usr/bin/env python3
import json, urllib.parse, http.server, threading, requests, time
from pathlib import Path

CONFIG = Path("/home/bolla/workspace/config/google_client.json")
TOKEN_FILE = Path("/home/bolla/workspace/config/google_gmail_drive_token.json")
creds = json.loads(CONFIG.read_text())
auth_code = None

class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        p = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        auth_code = p.get("code", [None])[0]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h2>OK - Fenster schliessen</h2>")
    def log_message(self, *a): pass

srv = http.server.HTTPServer(("0.0.0.0", 8765), H)
th = threading.Thread(target=srv.serve_forever)
th.daemon = True
th.start()
print("SERVER LAEUFT - Link in Edge oeffnen!")

for _ in range(300):
    if auth_code: break
    time.sleep(1)
srv.shutdown()

if not auth_code:
    print("TIMEOUT")
else:
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "code": auth_code,
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "redirect_uri": "http://localhost:8765",
        "grant_type": "authorization_code",
    })
    t = r.json()
    if "access_token" in t:
        t["account"] = creds["account"]
        TOKEN_FILE.write_text(json.dumps(t, indent=2))
        print("TOKEN_OK")
    else:
        print("FEHLER:", t)
