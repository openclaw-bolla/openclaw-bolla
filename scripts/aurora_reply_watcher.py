#!/usr/bin/env python3
"""
AURORA-Antwort-Wächter
Prüft ernstmandel@outlook.de (Graph) auf ANTWORTEN der angeschriebenen
Marketing-Kontakte (AURORA-Sichtbarkeit) und meldet via Telegram.
Setzt zusätzlich im MP-Projekt-Board (data/board.json) bei der passenden
Aktion das Flag "reply": true + Datum → Board zeigt ein "✉️ Antwort!"-Badge.

Auto-Replies / Out-of-Office werden erkannt und NICHT gemeldet.

Cron: */30 * * * * python3 /home/bolla/workspace/scripts/aurora_reply_watcher.py
"""
import json, urllib.parse, urllib.request
from pathlib import Path

CFGDIR = Path("/home/bolla/workspace/config")
DATADIR = Path("/home/bolla/workspace/data")
TG = json.loads((CFGDIR/"telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
OAUTH = json.loads((CFGDIR/"outlook_oauth2.json").read_text())
TOKF  = CFGDIR/"outlook_token.json"
STATE = CFGDIR/"aurora_reply_watcher_state.json"
BOARD = DATADIR/"board.json"

# Angeschriebene Kontakte: Match-Key (Domain ODER exakte Adresse) -> Anzeigename
SENDERS = {
    "epv.de":               "Ethik Digital",
    "womeninairobotics.de": "Women in AI & Robotics",
    "sheconomy.media":      "Sheconomy",
    "montrealethics.ai":    "Montreal AI Ethics",
    "diversityinai@gmail.com": "Women in AI Ethics",
    "cheyenne@maivenscommunity.com": "M(AI)VENS Buchclub",
    "sarbecker@deloitte.de": "Dr. Sarah J. Becker (Deloitte)",
    "speaking@vanessacann.com": "Vanessa Cann (Accenture)",
}
AUTOREPLY = ["this is an automated", "automatic reply", "out of office",
             "auto-reply", "automatische antwort", "abwesenheit",
             "your message has been received", "we have received your"]

def tg(text):
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{BOT}/sendMessage",
            data=json.dumps({"chat_id":CHRIS,"text":text,"parse_mode":"Markdown",
                             "disable_web_page_preview":True}).encode(),
            headers={"Content-Type":"application/json"}), timeout=20)
    except Exception as e:
        print("tg err", e)

def token():
    cfg, tok = OAUTH, json.loads(TOKF.read_text())
    data = urllib.parse.urlencode({'client_id':cfg['client_id'],'client_secret':cfg['client_secret'],
        'refresh_token':tok['refresh_token'],'grant_type':'refresh_token',
        'scope':'Mail.ReadWrite offline_access'}).encode()
    new = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://login.microsoftonline.com/consumers/oauth2/v2.0/token', data=data, method='POST')).read())
    tok.update(new); TOKF.write_text(json.dumps(tok, indent=2)); TOKF.chmod(0o600)
    return new['access_token']

def load_state():
    return json.loads(STATE.read_text()) if STATE.exists() else {"seen": []}

def match_sender(frm):
    """Gibt (match_key, anzeigename) zurück, wenn die Absenderadresse zu einem Kontakt passt."""
    frm = (frm or "").lower()
    # exakte Adresse zuerst (z.B. gmail), dann Domain-Suffix
    for key, name in SENDERS.items():
        if "@" in key:
            if frm == key:
                return key, name
        else:
            if frm.endswith("@" + key) or frm.endswith("." + key):
                return key, name
    return None, None

def mark_board_reply(match_key, date_str):
    """Setzt bei der Aktion mit passendem 'match' das reply-Flag im Board."""
    try:
        data = json.loads(BOARD.read_text())
    except Exception:
        return
    changed = False
    for proj in data.get("projects", []):
        for act in proj.get("actions", []):
            if act.get("match") == match_key and not act.get("reply"):
                act["reply"] = True
                act["reply_date"] = date_str
                changed = True
    if changed:
        BOARD.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    st = load_state()
    seen = set(st.get("seen", []))
    at = token()
    qs = urllib.parse.urlencode({'$top':'30','$orderby':'receivedDateTime desc',
                                 '$select':'id,subject,from,receivedDateTime,bodyPreview'})
    url = "https://graph.microsoft.com/v1.0/me/messages?"+qs
    res = json.loads(urllib.request.urlopen(urllib.request.Request(
        url, headers={"Authorization":f"Bearer {at}"})).read())
    hits = 0
    for m in res.get("value", []):
        mid = m["id"]
        if mid in seen:
            continue
        frm = (m.get("from",{}).get("emailAddress",{}).get("address","") or "").lower()
        key, name = match_sender(frm)
        seen.add(mid)  # immer merken, damit nicht doppelt geprüft wird
        if not key:
            continue
        body = (m.get("bodyPreview") or "").lower()
        if any(p in body for p in AUTOREPLY):
            continue  # Auto-Reply/OOO ignorieren
        subj = m.get("subject") or "(kein Betreff)"
        when = (m.get("receivedDateTime") or "")[:16].replace("T", " ")
        hits += 1
        mark_board_reply(key, when[:10])
        tg(f"📬 *AURORA-Antwort!* — *{name}*\n\n*{subj}*\nvon `{frm}`\n{when}\n\n"
           f"→ Bei Interesse EPUB senden:\n`python3 ~/workspace/scripts/send_aurora_epub.py --to {frm} --lang both`\n\n"
           f"Board zeigt jetzt ✉️ bei diesem Kanal. 🐾")
    st["seen"] = list(seen)[-400:]
    STATE.write_text(json.dumps(st, indent=2))
    if hits:
        print(f"{hits} AURORA-Antwort(en) gemeldet")
    else:
        print("keine neuen Antworten")

if __name__ == "__main__":
    main()
