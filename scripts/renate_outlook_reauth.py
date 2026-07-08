#!/usr/bin/env python3
"""
Outlook OAuth2 Reauth für renatemandel@outlook.de (separates Postfach, Booking.com-Konto).
Speichert NICHT in outlook_token.json (Chris' eigenes Konto), sondern in
config/renate_outlook_token.json — beide Konten laufen unabhängig nebeneinander.
Starten: python3 renate_outlook_reauth.py
"""
import json, urllib.request, urllib.parse, subprocess, sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

CFG_FILE   = Path("/home/bolla/workspace/config/outlook_oauth2.json")
TOKEN_FILE = Path("/home/bolla/workspace/config/renate_outlook_token.json")
TOKEN_URL  = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
AUTH_URL   = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
REDIRECT   = "http://localhost:8765"
SCOPE      = "Mail.ReadWrite Calendars.ReadWrite Contacts.Read offline_access"

def main():
    cfg = json.loads(CFG_FILE.read_text())
    auth_params = urllib.parse.urlencode({
        "client_id":     cfg["client_id"],
        "response_type": "code",
        "redirect_uri":  REDIRECT,
        "scope":         SCOPE,
        "response_mode": "query",
        "prompt":        "select_account",
    })
    url = f"{AUTH_URL}?{auth_params}"

    auth_code = [None]

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" in params:
                auth_code[0] = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<h2>&#10003; Fertig! Du kannst dieses Fenster schliessen.</h2>")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"<h2>Fehler: Kein Code erhalten.</h2>")
        def log_message(self, *args): pass

    server = HTTPServer(("0.0.0.0", 8765), Handler)
    t = Thread(target=lambda: server.handle_request(), daemon=True)
    t.start()

    clip = "/mnt/c/Windows/System32/clip.exe"
    subprocess.run([clip], input=url.encode(), check=True)
    print("\n" + "="*60)
    print("URL wurde in die Zwischenablage kopiert!")
    print("Bitte in Edge einfügen und mit renatemandel@outlook.de anmelden.")
    print("="*60 + "\n")
    print(f"URL (falls nötig):\n{url}\n")
    print("Warte auf Weiterleitung... (max. 3 Minuten)")

    t.join(timeout=180)
    server.server_close()

    if not auth_code[0]:
        print("Fehler: Kein Auth-Code empfangen. Script neu starten.")
        sys.exit(1)

    print("Code empfangen, tausche gegen Token...")

    data = urllib.parse.urlencode({
        "client_id":     cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "code":          auth_code[0],
        "redirect_uri":  REDIRECT,
        "grant_type":    "authorization_code",
        "scope":         SCOPE,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    with urllib.request.urlopen(req) as r:
        tok = json.loads(r.read())

    TOKEN_FILE.write_text(json.dumps(tok, indent=2))
    TOKEN_FILE.chmod(0o600)

    print("\n✓ Token gespeichert unter config/renate_outlook_token.json!")
    print(f"  access_token gültig für {tok.get('expires_in', '?')} Sekunden")
    print(f"  Refresh-Token: {'vorhanden' if 'refresh_token' in tok else 'FEHLT!'}")

if __name__ == "__main__":
    main()
