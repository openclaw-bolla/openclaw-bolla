#!/usr/bin/env python3
"""
KDP-Mail-Wächter
Prüft ernstmandel@outlook.de (Graph) auf neue KDP/Kindle-Publishing-Mails
(Buch ist live / Aktion nötig / Zahlungs- bzw. Kontostatus) und meldet via Telegram.
Hinweis: Bankprüfung-Abschluss mailt KDP i.d.R. NICHT — Button wird still aktiv.

Cron: 0 */4 * * * python3 /home/bolla/workspace/scripts/kdp_mail_watcher.py
"""
import json, urllib.parse, urllib.request
from pathlib import Path

CFGDIR = Path("/home/bolla/workspace/config")
TG = json.loads((CFGDIR/"telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
OAUTH = json.loads((CFGDIR/"outlook_oauth2.json").read_text())
TOKF  = CFGDIR/"outlook_token.json"
STATE = CFGDIR/"kdp_mail_watcher_state.json"

# Schlüsselwörter, die eine Mail als KDP-relevant markieren (Subject, lower)
KW = ["kdp", "kindle direct", "ihr ebook", "your ebook", "is live", "ist jetzt",
      "veröffentlicht", "published", "is now available", "im kindle", "kindle store",
      "kindle-shop", "blocked", "abgelehnt", "rejected", "action required",
      "maßnahme erforderlich", "review", "überprüfung deines", "payment", "auszahlung"]
# Absender, die immer durchgehen
SENDER_OK = ["kdp.amazon", "kdp@amazon"]
# harte Ausschlüsse (Shopping/Bestellungen), damit keine Fehlalarme
BLOCK = ["bestellung", "widerruf", "lieferung", "zahlungserinnerung", "retoure", "rücksende"]
# Absender, die NIE als KDP durchgehen duerfen, auch wenn "amazon" im From-Header steckt
# (Riverty nutzt "Amazon@riverty.com" fuer Inkasso-Mails im Kieselerde-Fall, siehe
# [[project_riverty_kieselerde]] - Fehlalarm am 12.08.2026 entdeckt: "Bitte ueberweisen Sie
# umgehend! - Amazon Payments Europe SCA" wurde als KDP-Mail gemeldet, obwohl 13 Tage alt und
# laengst bekannt)
SENDER_BLOCK = ["riverty.com"]
# Auto-Reply-/Eingangsbestätigungs-Marker (im bodyPreview) — NICHT melden, nur als gesehen merken
AUTOREPLY = ["your message has been received", "this is an automated", "automatic reply",
             "out of office", "auto-reply", "automatische antwort", "experiencing a delay"]

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

def main():
    st = load_state()
    # WICHTIG: seen als LISTE (chronologische Reihenfolge) fuehren, kein set() mehr — ein set()
    # hat keine feste Iterationsreihenfolge, dadurch flogen beim Kappen auf 300 Eintraege
    # zufaellige (auch juengst gesehene) IDs raus statt der aeltesten, was am 12.08.2026 zu
    # einem Fehlalarm fuehrte (13 Tage alte Riverty-Mail wurde erneut als "neu" gemeldet).
    seen_list = list(dict.fromkeys(st.get("seen", [])))  # Reihenfolge erhalten, Duplikate weg
    seen = set(seen_list)
    at = token()
    qs = urllib.parse.urlencode({'$top':'25','$orderby':'receivedDateTime desc',
                                 '$select':'id,subject,from,receivedDateTime,webLink,bodyPreview'})
    url = "https://graph.microsoft.com/v1.0/me/messages?"+qs
    res = json.loads(urllib.request.urlopen(urllib.request.Request(
        url, headers={"Authorization":f"Bearer {at}"})).read())
    new_ids = []
    for m in res.get("value", []):
        mid = m["id"]
        if mid in seen:
            continue
        subj = (m.get("subject") or "")
        sl = subj.lower()
        frm = (m.get("from",{}).get("emailAddress",{}).get("address","") or "").lower()
        sender_hit = any(s in frm for s in SENDER_OK)
        sender_blocked = any(s in frm for s in SENDER_BLOCK)
        kw_hit = any(k in sl for k in KW)
        blocked = any(b in sl for b in BLOCK)
        body = (m.get("bodyPreview") or "").lower()
        is_autoreply = any(p in body for p in AUTOREPLY)
        # relevant: bekannter Absender ODER (Keyword UND nicht Shopping-Block, nur Amazon)
        # — aber NIE Auto-Replies/Eingangsbestätigungen und NIE geblockte Absender (Riverty etc.)
        if (sender_hit or (kw_hit and not blocked and "amazon" in frm)) and not is_autoreply and not sender_blocked:
            new_ids.append(mid)
            tg(f"📧 *KDP-Mail eingetroffen!*\n\n*{subj}*\nvon `{frm}`\n{m['receivedDateTime'][:16]}\n\n"
               f"→ Auf [kdp.amazon.com](https://kdp.amazon.com) prüfen. 🐾")
        # immer als gesehen markieren (auch irrelevante/geblockte), damit wir nicht jedes Mal
        # alles neu pruefen — als LISTE anhaengen (chronologisch), nicht set.add(), damit das
        # Kappen unten deterministisch die AELTESTEN entfernt.
        seen.add(mid)
        seen_list.append(mid)
    st["seen"] = seen_list[-300:]
    STATE.write_text(json.dumps(st, indent=2))
    if new_ids:
        print(f"{len(new_ids)} neue KDP-Mail(s) gemeldet")

if __name__ == "__main__":
    main()
