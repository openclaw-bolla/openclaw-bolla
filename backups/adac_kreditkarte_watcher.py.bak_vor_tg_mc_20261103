#!/usr/bin/env python3
"""
ADAC-Kreditkarte-Kontaktformular-Wächter
Prüft ernstmandel@outlook.de (Graph) auf Antwort zur Kontaktformular-Anfrage vom
13.07.2026 ("Ist die ADAC-Kreditkarte an die Mitgliedschaft gekoppelt?").
Meldet eine echte Antwort per Telegram und ist damit erledigt.
Kommt nach 10 Tagen keine Antwort, gibt es (anders als beim Mitgliedschafts-
Wächter) KEINE automatische Nachfass-Mail — für die Kreditkarte existiert keine
offizielle E-Mail-Adresse, nur Formular/Telefon/Post. Stattdessen ein
Telegram-Hinweis, das Formular erneut auszufüllen oder anzurufen (089 76 76 17 50).

Cron: 0 */4 * * * python3 /home/bolla/workspace/scripts/adac_kreditkarte_watcher.py
"""
import imaplib, json, urllib.parse, urllib.request
from datetime import datetime, timezone
from email.header import decode_header, make_header
from pathlib import Path

CFGDIR = Path("/home/bolla/workspace/config")
TG = json.loads((CFGDIR / "telegram_bot.json").read_text())
BOT, CHRIS = TG["bot_token"], TG["chris_id"]
OAUTH = json.loads((CFGDIR / "outlook_oauth2.json").read_text())
TOKF = CFGDIR / "outlook_token.json"
WTNET_CONFIG = CFGDIR / "wtnet_account.json"
STATE = CFGDIR / "adac_kreditkarte_watcher_state.json"

SENT_DATE = "2026-07-13"
NUDGE_AFTER_DAYS = 10
SENDER_MARKERS = ["adac-kreditkarte.de", "solarisgroup.com", "solarisbank.de"]
AUTOREPLY = ["this is an automated", "automatic reply", "out of office",
             "auto-reply", "automatische antwort", "abwesenheit",
             "empfangsbestätigung", "elektronisch generiert",
             "kommen unaufgefordert auf sie zu", "ihre anfrage ist bei uns eingegangen",
             "wir haben ihre anfrage erhalten"]


def tg(text):
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{BOT}/sendMessage",
            data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                              "disable_web_page_preview": True}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e:
        print("tg err", e)


def read_token():
    cfg, tok = OAUTH, json.loads(TOKF.read_text())
    data = urllib.parse.urlencode({'client_id': cfg['client_id'], 'client_secret': cfg['client_secret'],
                                    'refresh_token': tok['refresh_token'], 'grant_type': 'refresh_token',
                                    'scope': 'Mail.ReadWrite offline_access'}).encode()
    new = json.loads(urllib.request.urlopen(urllib.request.Request(
        'https://login.microsoftonline.com/consumers/oauth2/v2.0/token', data=data, method='POST')).read())
    tok.update(new)
    TOKF.write_text(json.dumps(tok, indent=2))
    TOKF.chmod(0o600)
    return new['access_token']


def check_wtnet(seen):
    """Prüft chrismandel@wtnet.de per IMAP — Chris' eigene ADAC-Anfrage lief über dieses Konto,
    nicht über Outlook, deshalb muss dieses Postfach gleichwertig mitgeprüft werden."""
    cfg = json.loads(WTNET_CONFIG.read_text())
    m = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
    m.login(cfg["email"], cfg["password"])
    m.select("INBOX")
    status, data = m.search(None, "ALL")
    ids = data[0].split()

    for mid in ids[-100:]:
        key = f"wtnet:{mid.decode()}"
        if key in seen:
            continue
        seen.add(key)
        t, d = m.fetch(mid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])")
        if not d or not d[0]:
            continue
        raw = d[0][1].decode("utf-8", "replace")
        subject, sender = "", ""
        for line in raw.splitlines():
            low = line.lower()
            if low.startswith("subject:"):
                try:
                    subject = str(make_header(decode_header(line[8:].strip())))
                except Exception:
                    subject = line[8:].strip()
            elif low.startswith("from:"):
                try:
                    sender = str(make_header(decode_header(line[5:].strip())))
                except Exception:
                    sender = line[5:].strip()
        if not any(s in sender.lower() for s in SENDER_MARKERS):
            continue
        body_low = subject.lower()
        if any(p in body_low for p in AUTOREPLY):
            continue
        t2, d2 = m.fetch(mid, "(BODY.PEEK[TEXT])")
        preview = ""
        if d2 and d2[0]:
            preview = d2[0][1].decode("utf-8", "replace")[:400]
        m.logout()
        return subject, sender, preview
    m.logout()
    return None


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"seen": [], "done": False, "nudged": False}


def save_state(st):
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    STATE.chmod(0o600)


def main():
    st = load_state()
    if st.get("done"):
        print("bereits erledigt")
        return

    seen = set(st.get("seen", []))
    at = read_token()
    qs = urllib.parse.urlencode({'$top': '30', '$orderby': 'receivedDateTime desc',
                                  '$select': 'id,subject,from,receivedDateTime,bodyPreview'})
    url = "https://graph.microsoft.com/v1.0/me/messages?" + qs
    res = json.loads(urllib.request.urlopen(urllib.request.Request(
        url, headers={"Authorization": f"Bearer {at}"})).read())

    found = False
    for m in res.get("value", []):
        mid = m["id"]
        if mid in seen:
            continue
        seen.add(mid)
        frm = (m.get("from", {}).get("emailAddress", {}).get("address", "") or "").lower()
        if not any(s in frm for s in SENDER_MARKERS):
            continue
        subj = m.get("subject") or "(kein Betreff)"
        body = (m.get("bodyPreview") or "").lower()
        if any(p in body for p in AUTOREPLY) or any(p in subj.lower() for p in AUTOREPLY):
            continue
        when = (m.get("receivedDateTime") or "")[:16].replace("T", " ")
        preview = m.get("bodyPreview") or ""
        tg(f"📬 *ADAC-Kreditkarte hat geantwortet!* (Outlook)\n\n*{subj}*\nvon `{frm}`, {when}\n\n{preview[:400]}\n\n"
           f"Frage zur Kopplung Mitgliedschaft/Karte damit beantwortet. 🐾")
        st["done"] = True
        found = True
        break

    if not found:
        try:
            hit = check_wtnet(seen)
        except Exception as e:
            hit = None
            print("wtnet-Fehler:", e)
        if hit:
            subj, frm, preview = hit
            tg(f"📬 *ADAC-Kreditkarte hat geantwortet!* (wtnet)\n\n*{subj}*\nvon `{frm}`\n\n{preview}\n\n"
               f"Frage zur Kopplung Mitgliedschaft/Karte damit beantwortet. 🐾")
            st["done"] = True
            found = True

    st["seen"] = list(seen)[-300:]

    if not found and not st.get("done"):
        sent_dt = datetime.strptime(SENT_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - sent_dt).days
        if days >= NUDGE_AFTER_DAYS and not st.get("nudged"):
            st["nudged"] = True
            tg(f"🤔 Keine Antwort auf die ADAC-Kreditkarte-Anfrage nach {days} Tagen. "
               f"Für die Karte gibt's keine E-Mail-Adresse zum automatischen Nachfassen — "
               f"am besten kurz anrufen: 089 76 76 17 50, oder das Formular nochmal ausfüllen.")

    save_state(st)
    print("erledigt" if st.get("done") else "läuft weiter")


if __name__ == "__main__":
    main()
