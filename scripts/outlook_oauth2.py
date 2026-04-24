#!/usr/bin/env python3
"""
Outlook OAuth2 Mail-Sender für Bolla.
Erstes Mal: python3 outlook_oauth2.py --setup
Danach:     python3 outlook_oauth2.py --to "..." --subject "..." --body "..."
"""
import json, sys, urllib.request, urllib.parse, argparse, webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

CFG_FILE   = Path("/home/bolla/workspace/config/outlook_oauth2.json")
TOKEN_FILE = Path("/home/bolla/workspace/config/outlook_token.json")
GRAPH_URL  = "https://graph.microsoft.com/v1.0/me/sendMail"
TOKEN_URL  = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
AUTH_URL   = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
REDIRECT   = "http://localhost:8765"
SCOPE      = "Mail.Send offline_access"

def load_cfg():
    return json.loads(CFG_FILE.read_text())

def save_token(data):
    TOKEN_FILE.write_text(json.dumps(data, indent=2))
    TOKEN_FILE.chmod(0o600)

def load_token():
    return json.loads(TOKEN_FILE.read_text())

def refresh_access_token():
    cfg = load_cfg()
    tok = load_token()
    data = urllib.parse.urlencode({
        "client_id":     cfg["client_id"],
        "client_secret": cfg["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type":    "refresh_token",
        "scope":         SCOPE,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
    with urllib.request.urlopen(req) as r:
        new_tok = json.loads(r.read())
    tok.update(new_tok)
    save_token(tok)
    return tok["access_token"]

def setup():
    cfg = load_cfg()
    auth_params = urllib.parse.urlencode({
        "client_id":     cfg["client_id"],
        "response_type": "code",
        "redirect_uri":  REDIRECT,
        "scope":         SCOPE,
        "response_mode": "query",
    })
    url = f"{AUTH_URL}?{auth_params}"

    auth_code = [None]

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if "code" in params:
                auth_code[0] = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<h2>Fertig! Du kannst dieses Fenster schliessen.</h2>")
            else:
                self.send_response(400)
                self.end_headers()
        def log_message(self, *args): pass

    server = HTTPServer(("localhost", 8765), Handler)
    t = Thread(target=lambda: server.handle_request())
    t.start()

    print(f"\nBitte diesen Link im Browser öffnen:\n{url}\n")
    webbrowser.open(url)

    t.join(timeout=120)
    server.server_close()

    if not auth_code[0]:
        print("Fehler: Kein Auth-Code erhalten.")
        sys.exit(1)

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
    save_token(tok)
    print("✓ Token gespeichert. Bolla kann jetzt Mails versenden!")

def send_mail(to, subject, body):
    access_token = refresh_access_token()
    payload = json.dumps({
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to}}]
        }
    }).encode()
    req = urllib.request.Request(GRAPH_URL, data=payload, method="POST", headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type":  "application/json"
    })
    with urllib.request.urlopen(req) as r:
        if r.status == 202:
            print(f"✓ Mail an {to} gesendet.")
        else:
            print(f"Fehler: {r.status}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup",   action="store_true")
    parser.add_argument("--to",      default="")
    parser.add_argument("--subject", default="")
    parser.add_argument("--body",    default="")
    args = parser.parse_args()

    if args.setup:
        setup()
    elif args.to:
        send_mail(args.to, args.subject, args.body)
    else:
        print("Nutze --setup oder --to/--subject/--body")
