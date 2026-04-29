#!/usr/bin/env python3
"""
Mail → Kalender Automatisierung für Chris Mandel
Liest E-Mails (Outlook + IMAP), erkennt Termine per Claude, trägt in Outlook-Kalender ein.
"""
import json, urllib.request, urllib.parse, time, re, sys
import imaplib, email as email_lib
from email.header import decode_header as hdr_decode
from email.utils import parsedate_to_datetime
from pathlib import Path
from datetime import datetime, timedelta, timezone

# ── Config ────────────────────────────────────────────────────────────────────
HOME_ADDRESS   = "Buchenweg 67a, 22846 Norderstedt"
TOKEN_FILE     = Path("/home/bolla/workspace/config/outlook_token.json")
OAUTH_CFG      = Path("/home/bolla/workspace/config/outlook_oauth2.json")
IMAP_CFG       = Path("/home/bolla/workspace/config/wtnet_account.json")
TG_CFG         = Path("/home/bolla/workspace/config/telegram_bot.json")
PROCESSED_FILE = Path("/home/bolla/workspace/logs/mail_calendar_processed.json")
GRAPH          = "https://graph.microsoft.com/v1.0/me"

CATEGORIES = {
    "Event":      "preset23",  # Oper, Konzert, Theater, Veranstaltung
    "Termin":     "preset1",   # Allgemeine Termine
    "Arzt":       "preset3",   # Arzt, Krankenhaus, medizinisch
    "Lessing I":  "preset4",   # Schule Lessing Klasse I
    "Lessing II": "preset21",  # Schule Lessing Klasse II
    "Handwerker": "preset14",  # Handwerker, Reparatur, Monteur
    "Ferien":     "preset8",   # Schulferien
    "Urlaub":     "preset6",   # Urlaub, Reise
    "Wichtig":    "preset24",  # Wichtige Termine
    "Geburtstag": "preset20",  # Geburtstage
    "Feiertag":   "preset7",   # Feiertage
}

TRAVEL_TIMES = {
    "norderstedt": 10,
    "hamburg":     35,
    "default":     60,
}

# ── Auth ──────────────────────────────────────────────────────────────────────
def get_token():
    cfg = json.loads(OAUTH_CFG.read_text())
    tok = json.loads(TOKEN_FILE.read_text())
    data = urllib.parse.urlencode({
        'client_id':     cfg['client_id'],
        'refresh_token': tok['refresh_token'],
        'grant_type':    'refresh_token',
        'scope':         'Mail.ReadWrite Mail.Send Calendars.ReadWrite Contacts.ReadWrite Tasks.ReadWrite',
    }).encode()
    req = urllib.request.Request(
        'https://login.microsoftonline.com/consumers/oauth2/v2.0/token',
        data=data, method='POST')
    with urllib.request.urlopen(req) as r:
        new_tok = json.loads(r.read())
    tok.update(new_tok)
    TOKEN_FILE.write_text(json.dumps(tok, indent=2))
    TOKEN_FILE.chmod(0o600)
    return new_tok['access_token']

def graph_get(path, token):
    url = f"{GRAPH}{path}".replace(" ", "%20")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def graph_post(path, body, token, method="POST"):
    data = json.dumps(body).encode()
    req = urllib.request.Request(f"{GRAPH}{path}", data=data, method=method,
              headers={"Authorization": f"Bearer {token}",
                       "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        try: return json.loads(r.read())
        except: return {}

# ── Telegram ──────────────────────────────────────────────────────────────────
def telegram(msg):
    cfg = json.loads(TG_CFG.read_text())
    data = urllib.parse.urlencode({
        "chat_id": cfg["chris_id"],
        "text": msg, "parse_mode": "HTML"
    }).encode()
    urllib.request.urlopen(
        f"https://api.telegram.org/bot{cfg['bot_token']}/sendMessage",
        data=data, timeout=10)

# ── Claude ────────────────────────────────────────────────────────────────────
def analyze_email(subject, body, sender, date_received):
    import subprocess
    today = datetime.now().strftime("%d.%m.%Y")

    prompt = f"""Analysiere diese E-Mail und prüfe ob sie einen Termin/Event enthält.
Heute ist {today}. Heimatadresse: {HOME_ADDRESS}.

E-Mail:
Von: {sender}
Datum empfangen: {date_received}
Betreff: {subject}
Inhalt: {body[:2000]}

Antworte NUR als reines JSON ohne Markdown:
{{
  "hat_termin": true,
  "titel": "Kurzer Kalender-Titel",
  "datum": "YYYY-MM-DD oder null",
  "uhrzeit_start": "HH:MM oder null",
  "uhrzeit_ende": "HH:MM oder null",
  "dauer_minuten": 90,
  "ort": "Veranstaltungsort oder null",
  "ort_stadt": "Stadtname oder null",
  "kategorie": "Event|Termin|Arzt|Handwerker|Urlaub|Ferien|Wichtig|Geburtstag|Feiertag|Lessing I|Lessing II",
  "anfahrt_minuten": 35,
  "konfidenz": "hoch|mittel|niedrig",
  "begruendung": "Kurze Erklärung"
}}

Regeln:
- Nur echte Termine (mit Datum/Uhrzeit), keine Newsletter
- Anfahrtszeit: Norderstedt=10min, Hamburg=35min, andere Stadt=60min, unbekannt=45min
- Dauer schätzen: Oper=150min, Konzert=120min, Theater=120min, Arzt=45min, Handwerker=120min
- Kategorie "Event" für: Oper, Konzert, Theater, Festival, Veranstaltung
- konfidenz "niedrig" wenn Datum unklar oder kein eindeutiger Termin"""

    result = subprocess.run(
        ["/home/bolla/.local/bin/claude", "-p", prompt],
        capture_output=True, text=True, timeout=60
    )
    text = result.stdout.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"): text = text[4:]
    return json.loads(text.strip())

# ── Kalender ──────────────────────────────────────────────────────────────────
def check_duplicate(date_str, titel, token):
    start = f"{date_str}T00:00:00"
    end   = f"{date_str}T23:59:59"
    data = graph_get(
        f"/calendar/calendarView?startDateTime={start}&endDateTime={end}"
        f"&$select=subject,start&$top=50", token)
    existing = [e["subject"].lower() for e in data.get("value", [])]
    titel_lower = titel.lower()
    return any(titel_lower in e or e in titel_lower for e in existing)

def create_event(info, token):
    datum = info["datum"]
    start_h, start_m = map(int, (info.get("uhrzeit_start") or "09:00").split(":"))
    dauer = info.get("dauer_minuten", 60)
    anfahrt = info.get("anfahrt_minuten", 45)

    ev_start = datetime(
        *[int(x) for x in datum.split("-")], start_h, start_m,
        tzinfo=timezone(timedelta(hours=2)))
    event_start = ev_start - timedelta(minutes=anfahrt)
    event_end   = ev_start + timedelta(minutes=dauer + anfahrt)

    ort = info.get("ort") or ""
    kat = info.get("kategorie", "Termin")
    if kat not in CATEGORIES: kat = "Termin"

    body_text = (f"📍 {ort}\n" if ort else "") + \
                f"🚗 Anfahrt: ~{anfahrt} Min\n" + \
                f"⏱ Dauer: ~{dauer} Min\n" + \
                f"🏠 Rückfahrt: ~{anfahrt} Min\n" + \
                f"📧 Automatisch aus E-Mail erstellt von Bolla"

    event = {
        "subject": info["titel"],
        "start": {"dateTime": event_start.isoformat(), "timeZone": "Europe/Berlin"},
        "end":   {"dateTime": event_end.isoformat(),   "timeZone": "Europe/Berlin"},
        "location": {"displayName": ort},
        "body": {"contentType": "Text", "content": body_text},
        "categories": [kat]
    }
    result = graph_post("/calendar/events", event, token)
    return result.get("id") is not None or result.get("subject") is not None

# ── Mails holen ───────────────────────────────────────────────────────────────
def get_emails_since(days, token):
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    skip = {"Deleted Items", "Gelöschte Elemente", "Junk Email", "Junk-E-Mail",
            "Drafts", "Entwürfe", "Sent Items", "Gesendete Elemente",
            "Outbox", "RSS-Feeds", "Scheduled"}
    emails = []

    def fetch_folder(fid, fname):
        try:
            url = (f"/mailFolders/{fid}/messages"
                   f"?$filter=receivedDateTime%20ge%20{since}"
                   f"&$select=id,subject,from,receivedDateTime,body"
                   f"&$top=50&$orderby=receivedDateTime%20desc")
            msgs = graph_get(url, token)
            for m in msgs.get("value", []):
                m["_folder"] = fname
                emails.append(m)
        except Exception as e:
            print(f"   ⚠ Ordner {fname}: {e}")
        time.sleep(0.3)
        # Unterordner durchsuchen
        try:
            children = graph_get(f"/mailFolders/{fid}/childFolders?$top=50", token).get("value", [])
            for child in children:
                cname = child["displayName"]
                if cname in skip: continue
                fetch_folder(child["id"], f"{fname}/{cname}")
                time.sleep(0.2)
        except Exception:
            pass

    folders = graph_get("/mailFolders?$top=50", token).get("value", [])
    for folder in folders:
        fname = folder["displayName"]
        if fname in skip: continue
        fetch_folder(folder["id"], fname)

    return emails

# ── IMAP Mails holen ──────────────────────────────────────────────────────────
def _imap_utf7_decode(s):
    import base64
    result, i = [], 0
    while i < len(s):
        if s[i] == "&":
            j = s.index("-", i + 1)
            if j == i + 1:
                result.append("&")
            else:
                b64 = s[i+1:j].replace(",", "/")
                result.append(base64.b64decode(b64 + "==").decode("utf-16-be"))
            i = j + 1
        else:
            result.append(s[i])
            i += 1
    return "".join(result)

def get_emails_imap(days):
    if not IMAP_CFG.exists():
        return []
    cfg = json.loads(IMAP_CFG.read_text())
    # Einzel-Objekt oder Liste unterstützen
    accounts = cfg if isinstance(cfg, list) else [cfg]
    since_str = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
    skip_folders = {"sent", "drafts", "trash", "junk", "spam", "gesendet",
                    "entwürfe", "papierkorb", "outbox", "gelöscht"}
    all_emails = []

    for acc in accounts:
        host = acc.get("imap_server") or acc.get("imap_host", "")
        user = acc.get("username") or acc.get("email", "")
        try:
            with imaplib.IMAP4_SSL(host, acc.get("imap_port", 993)) as imap:
                imap.login(user, acc["password"])
                _, folder_list = imap.list()
                for folder_data in (folder_list or []):
                    raw = folder_data.decode(errors="replace")
                    parts = raw.split('"')
                    # Quoted name: (...) "/" "Name" → 5 parts, name is parts[-2]
                    # Unquoted name: (...) "/" Name → 3 parts, name is parts[-1].strip()
                    if len(parts) >= 5:
                        fname_raw = parts[-2]
                    else:
                        fname_raw = parts[-1].strip()
                    try:
                        fname = _imap_utf7_decode(fname_raw)
                    except Exception:
                        fname = fname_raw
                    if any(s in fname.lower() for s in skip_folders):
                        continue
                    try:
                        imap.select(f'"{fname_raw}"', readonly=True)
                        _, ids = imap.search(None, f'SINCE {since_str}')
                        for mid in (ids[0].split() if ids[0] else [])[-50:]:
                            _, msg_data = imap.fetch(mid, "(RFC822)")
                            if not msg_data or not msg_data[0]:
                                continue
                            msg = email_lib.message_from_bytes(msg_data[0][1])

                            subj_parts = hdr_decode(msg.get("Subject", ""))
                            subject = "".join(
                                p.decode(enc or "utf-8", errors="replace") if isinstance(p, bytes) else p
                                for p, enc in subj_parts
                            )
                            sender = msg.get("From", "")
                            try:
                                recv_dt = parsedate_to_datetime(msg.get("Date", "")).isoformat()
                            except Exception:
                                recv_dt = ""

                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    ct = part.get_content_type()
                                    if ct == "text/plain":
                                        body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                                        break
                                    elif ct == "text/html" and not body:
                                        body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                            else:
                                payload = msg.get_payload(decode=True)
                                if payload:
                                    body = payload.decode("utf-8", errors="replace")

                            uid = f"imap_{user}_{msg.get('Message-ID', mid.decode())}"
                            all_emails.append({
                                "id": uid,
                                "subject": subject,
                                "from": {"emailAddress": {"address": sender}},
                                "receivedDateTime": recv_dt,
                                "body": {"content": body, "contentType": "Text"},
                                "_folder": f"[{user}] {fname}",
                                "_source": "imap",
                                "_account": user,
                            })
                    except Exception:
                        pass
        except Exception as e:
            print(f"   ⚠ IMAP {acc.get('email','?')}: {e}")

    return all_emails

# ── Hauptprogramm ─────────────────────────────────────────────────────────────
def main():
    initial_run = "--initial" in sys.argv
    days = 90 if initial_run else 1

    print(f"{'='*55}")
    print(f"  Mail → Kalender  {'(Erstlauf: 90 Tage)' if initial_run else '(täglich)'}")
    print(f"{'='*55}\n")

    token = get_token()

    # Bereits verarbeitete Mails laden
    processed = {}
    if PROCESSED_FILE.exists():
        try: processed = json.loads(PROCESSED_FILE.read_text())
        except: pass

    emails = get_emails_since(days, token)
    imap_emails = get_emails_imap(days)
    emails += imap_emails
    print(f"E-Mails gefunden: {len(emails)} (Outlook: {len(emails)-len(imap_emails)}, IMAP: {len(imap_emails)})\n")

    added = skipped = uncertain = 0

    for mail in emails:
        mid = mail["id"]
        if mid in processed:
            continue

        subject  = mail.get("subject", "")
        sender   = mail.get("from", {}).get("emailAddress", {}).get("address", "")
        received = mail.get("receivedDateTime", "")
        body     = mail.get("body", {}).get("content", "")
        # Style-Blöcke und HTML-Tags entfernen
        body = re.sub(r'<style[^>]*>.*?</style>', ' ', body, flags=re.DOTALL)
        body = re.sub(r'<[^>]+>', ' ', body)
        body = re.sub(r'\s+', ' ', body).strip()

        print(f"📧 {subject[:60]}")

        # Offensichtliche Newsletter/Spam vorab rausfiltern
        skip_keywords = ["lotto", "gewinnzahl", "newsletter", "angebot", "bestpreis",
                         "spielquittung", "werbung", "unsubscribe", "abbestellen",
                         "microsoft-konto", "neue anmeldung", "neue apps", "sicherheit",
                         "konto erkannt", "verbunden", "immobilien", "eigentumswohnung",
                         "wohnung gesucht", "maklerbericht", "tracking", "versandbestätigung",
                         "rechnung", "invoice", "ihre bestellung", "ihr auftrag",
                         "password", "passwort", "spam", "phishing"]
        # Nur analysieren wenn Termin-Signalwörter vorhanden
        termin_keywords = ["termin", "einladung", "veranstaltung", "konzert", "oper",
                           "theater", "ticket", "reservierung", "buchung", "appointment",
                           "meeting", "treffen", "besuch", "feier", "party", "event",
                           "beginn", "uhr", "datum", "handwerker", "monteur", "lieferung",
                           "arzttermin", "praxis", "klinik", "impfung", "untersuchung",
                           "reise", "flug", "hotel", "urlaub", "ausflug"]
        has_skip = any(kw in subject.lower() or kw in sender.lower() for kw in skip_keywords)
        has_termin = any(kw in subject.lower() or kw in sender.lower() or kw in body[:2000].lower() for kw in termin_keywords)
        if has_skip or not has_termin:
            reason = "Newsletter/Werbung" if has_skip else "Kein Termin-Signal"
            print(f"   → {reason} übersprungen\n")
            processed[mid] = "skip_newsletter"
            PROCESSED_FILE.write_text(json.dumps(processed, indent=2))
            continue

        try:
            for attempt in range(3):
                try:
                    info = analyze_email(subject, body, sender, received)
                    break
                except Exception as e:
                    if "429" in str(e) and attempt < 2:
                        print(f"   ⏳ Rate-Limit, warte 30s...")
                        time.sleep(30)
                    else:
                        raise
            time.sleep(5)
        except Exception as e:
            print(f"   ⚠ Analyse-Fehler: {e}")
            processed[mid] = "error"
            continue

        if not info.get("hat_termin") or not info.get("datum"):
            print(f"   → Kein Termin\n")
            processed[mid] = "no_event"
            PROCESSED_FILE.write_text(json.dumps(processed, indent=2))
            continue

        titel    = info["titel"]
        datum    = info["datum"]
        konfidenz = info.get("konfidenz", "niedrig")

        print(f"   📅 {titel} am {datum} — Konfidenz: {konfidenz}")

        # Vergangene Termine überspringen
        try:
            event_date = datetime(*[int(x) for x in datum.split("-")], tzinfo=timezone.utc)
            if event_date < datetime.now(timezone.utc) - timedelta(days=2):
                print(f"   ⏪ Termin liegt in der Vergangenheit → übersprungen\n")
                processed[mid] = "past"
                PROCESSED_FILE.write_text(json.dumps(processed, indent=2))
                continue
        except Exception:
            pass

        # Duplikat-Check
        if check_duplicate(datum, titel, token):
            print(f"   ✓ Bereits im Kalender\n")
            processed[mid] = "duplicate"
            PROCESSED_FILE.write_text(json.dumps(processed, indent=2))
            skipped += 1
            continue

        if konfidenz == "hoch":
            ok = create_event(info, token)
            if ok:
                print(f"   ✅ Eingetragen: {titel}\n")
                processed[mid] = "added"
                added += 1
                telegram(f"📅 <b>Kalender-Eintrag erstellt:</b>\n"
                         f"<b>{titel}</b>\n"
                         f"📆 {datum}  ⏰ {info.get('uhrzeit_start','?')}\n"
                         f"📍 {info.get('ort','')}\n"
                         f"🏷 {info.get('kategorie','')}")
            else:
                print(f"   ⚠ Fehler beim Eintragen\n")
                processed[mid] = "error"
        else:
            print(f"   ❓ Unsicher → Telegram\n")
            telegram(f"❓ <b>Kalender-Rückfrage:</b>\n"
                     f"<b>{titel}</b>\n"
                     f"📆 {datum}  ⏰ {info.get('uhrzeit_start','?')}\n"
                     f"📍 {info.get('ort','')}\n"
                     f"🏷 {info.get('kategorie','')}\n"
                     f"Konfidenz: {konfidenz}\n"
                     f"Begründung: {info.get('begruendung','')}\n\n"
                     f"Antwort: /ka_ja oder /ka_nein (kommt bald)")
            processed[mid] = "pending"
            uncertain += 1

        PROCESSED_FILE.write_text(json.dumps(processed, indent=2))

    print(f"\n{'='*55}")
    print(f"✓ Eingetragen: {added} | Übersprungen: {skipped} | Rückfrage: {uncertain}")
    print(f"{'='*55}")

if __name__ == "__main__":
    main()
