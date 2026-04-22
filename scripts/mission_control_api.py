#!/usr/bin/env python3
"""
Mission Control API Server
Liefert Kalender, E-Mail und andere Daten an Mission Control (localhost:18790)
"""

import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

WORKSPACE = os.path.expanduser("~/workspace")
TOKEN_FILE = os.path.join(WORKSPACE, "config/ms_token.json")
AZURE_SPEECH_FILE = os.path.join(WORKSPACE, "config/azure_speech.json")


def azure_speech_config():
    """Lädt Azure Speech Config. None wenn nicht konfiguriert."""
    try:
        with open(AZURE_SPEECH_FILE) as f:
            cfg = json.load(f)
        if not cfg.get("key") or cfg["key"].startswith("REPLACE_"):
            return None
        return cfg
    except Exception:
        return None

GEMINI_API_FILE = os.path.join(WORKSPACE, "config/gemini_api.json")


def gemini_api_key():
    try:
        with open(GEMINI_API_FILE) as f:
            cfg = json.load(f)
        key = cfg.get("api_key", "")
        if not key or key.startswith("REPLACE_"):
            return None
        return key
    except Exception:
        return None


BILDGEN_LIMIT = 100
_bildgen_counter = {"date": "", "count": 0}

def bildgen_check_limit():
    today = datetime.now().strftime("%Y-%m-%d")
    if _bildgen_counter["date"] != today:
        _bildgen_counter["date"] = today
        _bildgen_counter["count"] = 0
    if _bildgen_counter["count"] >= BILDGEN_LIMIT:
        return False, f"Tageslimit von {BILDGEN_LIMIT} Bildern erreicht. Morgen wieder möglich."
    return True, None

def bildgen_generate(prompt, model="gemini-2.5-flash-image", aspect_ratio="1:1",
                     input_image_b64=None, input_mime_type="image/png"):
    import urllib.request, urllib.error, base64
    key = gemini_api_key()
    if not key:
        return None, "Kein Gemini API-Key konfiguriert. Bitte in config/gemini_api.json eintragen."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    parts = []
    if input_image_b64:
        parts.append({"inlineData": {"mimeType": input_mime_type, "data": input_image_b64}})
    parts.append({"text": prompt})
    gen_cfg = {"responseModalities": ["TEXT", "IMAGE"]}
    if not input_image_b64:
        gen_cfg["imageConfig"] = {"aspectRatio": aspect_ratio}
    payload = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": gen_cfg
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                  headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")
        try:
            msg = json.loads(msg).get("error", {}).get("message", msg)
        except Exception:
            pass
        return None, f"API-Fehler: {msg}"
    except Exception as e:
        return None, str(e)
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            img_b64 = part["inlineData"]["data"]
            mime = part["inlineData"].get("mimeType", "image/png")
            return img_b64, mime
    return None, "Kein Bild in der API-Antwort erhalten."


CLIENT_ID = "9e5f94bc-e8a4-4e73-b8be-63364c29d753"

_lms_host_cache = None
def lms_base_url():
    """Findet LM Studio auf dem Windows-Host (WSL2-Default-Gateway), Port 1234."""
    global _lms_host_cache
    if _lms_host_cache is None:
        try:
            with open("/proc/net/route") as f:
                for line in f.readlines()[1:]:
                    parts = line.split()
                    if parts[1] == "00000000":
                        ip = ".".join(str(int(parts[2][i:i+2], 16)) for i in (6, 4, 2, 0))
                        _lms_host_cache = ip
                        break
        except Exception:
            _lms_host_cache = "172.20.96.1"
    return f"http://{_lms_host_cache}:1234"

def get_token():
    """Gibt einen gültigen MS Graph Access Token zurück (refresht bei Bedarf)."""
    try:
        with open(TOKEN_FILE) as f:
            token_data = json.load(f)

        # Immer refreshen — Access Tokens laufen schnell ab
        import urllib.request, urllib.parse
        data = urllib.parse.urlencode({
            "client_id": CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"],
            "scope": "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.ReadWrite https://graph.microsoft.com/Calendars.Read https://graph.microsoft.com/Contacts.Read offline_access"
        }).encode()
        req = urllib.request.Request(
            "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            data=data, method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            new_token = json.loads(r.read())
        with open(TOKEN_FILE, "w") as f:
            json.dump(new_token, f, indent=2)
        return new_token["access_token"]
    except Exception as e:
        print(f"Token error: {e}")
        # Fallback: alten Token versuchen
        try:
            with open(TOKEN_FILE) as f:
                return json.load(f).get("access_token")
        except:
            return None

def graph_get(path):
    import urllib.request, urllib.parse
    token = get_token()
    if not token:
        return None
    # URL-Teile splitten und Query-Parameter korrekt encodieren
    if '?' in path:
        base, query = path.split('?', 1)
        # Query-Parameter einzeln URL-encodieren (Leerzeichen → %20)
        encoded_query = urllib.parse.quote(query, safe='=&$,/')
        full_url = f"https://graph.microsoft.com/v1.0{base}?{encoded_query}"
    else:
        full_url = f"https://graph.microsoft.com/v1.0{path}"
    req = urllib.request.Request(
        full_url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"Graph error {path}: {e}")
        return None

PRESET_COLORS = {
    "preset0":  "229,57,53",    # Rot
    "preset1":  "230,81,0",     # Orange
    "preset2":  "121,85,72",    # Braun
    "preset3":  "249,168,37",   # Gelb
    "preset4":  "67,160,71",    # Grün
    "preset5":  "0,172,193",    # Türkis
    "preset6":  "142,155,0",    # Olive
    "preset7":  "30,136,229",   # Blau
    "preset8":  "94,53,177",    # Lila
    "preset9":  "194,24,91",    # Cranberry/Pink
    "preset10": "84,110,122",   # Stahl
    "preset11": "55,71,79",     # Dunkelstahl
    "preset12": "117,117,117",  # Grau
    "preset13": "66,66,66",     # Dunkelgrau
    "preset14": "33,33,33",     # Schwarz
    "preset15": "183,28,28",    # Dunkelrot
    "preset16": "191,54,12",    # Dunkelorange
    "preset17": "78,52,46",     # Dunkelbraun
    "preset18": "245,127,23",   # Dunkelgelb
    "preset19": "27,94,32",     # Dunkelgrün
    "preset20": "0,96,100",     # Dunkeltürkis
    "preset21": "130,119,23",   # Dunkelolive
    "preset22": "13,71,161",    # Dunkelblau
    "preset23": "74,20,140",    # Dunkellila
    "preset24": "136,14,79",    # Dunkelcranberry
    "none":     "120,144,156",  # Fallback Grau
}

def get_category_colors():
    data = graph_get("/me/outlook/masterCategories")
    if not data:
        return {}
    result = {}
    for cat in data.get("value", []):
        name = cat.get("displayName", "")
        preset = cat.get("color", "none")
        result[name] = PRESET_COLORS.get(preset, PRESET_COLORS["none"])
    return result

def get_calendar():
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=30)
    start_str = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    cat_colors = get_category_colors()

    data = graph_get(
        f"/me/calendarView?startDateTime={start_str}&endDateTime={end_str}"
        f"&$orderby=start/dateTime&$top=20"
        f"&$select=subject,start,end,categories,location"
    )
    if not data:
        return []

    events = []
    for ev in data.get("value", []):
        start_raw = ev.get("start", {}).get("dateTime", "")
        try:
            import zoneinfo
            berlin = zoneinfo.ZoneInfo("Europe/Berlin")
            dt_utc = datetime.fromisoformat(start_raw).replace(tzinfo=timezone.utc)
            dt_local = dt_utc.astimezone(berlin)
            date_str = dt_local.strftime("%d.%m.")
            time_str = dt_local.strftime("%H:%M")
            weekday = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"][dt_local.weekday()]
        except:
            date_str = start_raw[:10]
            time_str = ""
            weekday = ""

        cats = ev.get("categories", [])
        cat = cats[0] if cats else ""
        rgb = cat_colors.get(cat, PRESET_COLORS["none"])

        events.append({
            "title": ev.get("subject", ""),
            "date": date_str,
            "time": time_str,
            "weekday": weekday,
            "category": cat,
            "color": rgb,
            "location": ev.get("location", {}).get("displayName", "")
        })

    return events

SPAM_SUBJECT = ["newsletter", "unsubscribe", "abbestellen", "rabatt", "sonderangebot",
                "gutschein", "gewinnspiel", "angebot des tages", "% off", "% rabatt",
                "jetzt kaufen", "nur heute", "limited offer", "act now"]
SPAM_SENDER  = ["newsletter", "noreply", "no-reply", "donotreply", "mailer-daemon",
                "marketing@", "notification@", "bounce@", "alerts@", "info@newsletter"]

def _is_spam(subject, from_email):
    s = subject.lower()
    e = from_email.lower()
    return any(k in s for k in SPAM_SUBJECT) or any(k in e for k in SPAM_SENDER)

def _parse_graph_mail(m, account="Outlook"):
    received = m.get("receivedDateTime", "")
    try:
        dt = datetime.fromisoformat(received.replace("Z", "+00:00"))
        dt_local = dt.astimezone(timezone(timedelta(hours=2)))
        date_str = dt_local.strftime("%d.%m. %H:%M")
        is_today = dt_local.date() == datetime.now(timezone(timedelta(hours=2))).date()
    except:
        date_str = received[:16]
        is_today = False
    return {
        "account": account,
        "from": m.get("from", {}).get("emailAddress", {}).get("name", "Unbekannt"),
        "from_email": m.get("from", {}).get("emailAddress", {}).get("address", ""),
        "subject": m.get("subject", "(kein Betreff)"),
        "date": date_str,
        "is_today": is_today,
        "preview": m.get("bodyPreview", "")[:100]
    }

def get_emails_outlook():
    """Holt ungelesene Mails von ernstmandel@outlook.de via Graph API."""
    data = graph_get(
        "/me/mailFolders/inbox/messages?$filter=isRead%20eq%20false"
        "&$top=10"
        "&$select=subject,from,receivedDateTime,isRead,bodyPreview"
    )
    if not data:
        return []
    msgs = []
    for m in data.get("value", []):
        entry = _parse_graph_mail(m)
        if not _is_spam(entry["subject"], entry["from_email"]):
            msgs.append(entry)
    return msgs

def get_emails_recent_outlook():
    """Holt die letzten 5 empfangenen Mails (unabhängig vom Lesestatus), Spam gefiltert."""
    data = graph_get(
        "/me/mailFolders/inbox/messages"
        "?$top=15"
        "&$select=subject,from,receivedDateTime,isRead,bodyPreview"
    )
    if not data:
        return []
    msgs = []
    for m in data.get("value", []):
        entry = _parse_graph_mail(m)
        if not _is_spam(entry["subject"], entry["from_email"]):
            msgs.append(entry)
        if len(msgs) >= 5:
            break
    return msgs

def get_emails_sent_outlook():
    """Holt die letzten 5 gesendeten Mails."""
    data = graph_get(
        "/me/mailFolders/sentitems/messages"
        "?$top=5"
        "&$select=subject,toRecipients,sentDateTime,bodyPreview"
    )
    if not data:
        return []
    msgs = []
    for m in data.get("value", []):
        sent = m.get("sentDateTime", "")
        try:
            dt = datetime.fromisoformat(sent.replace("Z", "+00:00"))
            dt_local = dt.astimezone(timezone(timedelta(hours=2)))
            date_str = dt_local.strftime("%d.%m. %H:%M")
        except:
            date_str = sent[:16]
        recipients = m.get("toRecipients", [])
        to_name = recipients[0].get("emailAddress", {}).get("name", "Unbekannt") if recipients else "Unbekannt"
        msgs.append({
            "to": to_name,
            "subject": m.get("subject", "(kein Betreff)"),
            "date": date_str,
        })
    return msgs


def get_emails_wtnet():
    """Holt ungelesene Mails von chrismandel@wtnet.de via IMAP."""
    import imaplib, email as email_lib
    from email.header import decode_header

    try:
        wtnet_cfg = os.path.join(WORKSPACE, "config/wtnet_account.json")
        with open(wtnet_cfg) as f:
            cfg = json.load(f)

        mail = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
        mail.login(cfg["email"], cfg["password"])
        mail.select("INBOX")

        _, msg_ids = mail.search(None, "UNSEEN")
        ids = msg_ids[0].split()
        msgs = []

        for mid in reversed(ids[-10:]):  # max 10, neueste zuerst
            _, data = mail.fetch(mid, "(RFC822)")
            raw = data[0][1]
            msg = email_lib.message_from_bytes(raw)

            # Betreff dekodieren
            subj_raw = msg.get("Subject", "(kein Betreff)")
            subj_parts = decode_header(subj_raw)
            subj = ""
            for part, enc in subj_parts:
                if isinstance(part, bytes):
                    subj += part.decode(enc or "utf-8", errors="replace")
                else:
                    subj += part

            # Absender dekodieren
            from_raw = msg.get("From", "Unbekannt")
            from_parts = decode_header(from_raw)
            from_str = ""
            for part, enc in from_parts:
                if isinstance(part, bytes):
                    from_str += part.decode(enc or "utf-8", errors="replace")
                else:
                    from_str += part
            # Nur Name ohne E-Mail-Adresse
            from_name = from_str.split("<")[0].strip().strip('"')

            # Datum
            date_raw = msg.get("Date", "")
            try:
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(date_raw)
                dt_local = dt.astimezone(timezone(timedelta(hours=2)))
                date_str = dt_local.strftime("%d.%m. %H:%M")
            except:
                date_str = date_raw[:16]

            # Spam überspringen
            if "*** SPAM" in subj.upper() or "[SPAM]" in subj.upper():
                continue

            msgs.append({
                "account": "wtnet",
                "from": from_name or "Unbekannt",
                "from_email": cfg["email"],
                "subject": subj,
                "date": date_str,
                "preview": ""
            })

        mail.logout()
        return msgs

    except Exception as e:
        print(f"wtnet IMAP Fehler: {e}")
        return []


def get_emails():
    """Kombiniert Outlook + wtnet Mails."""
    outlook  = get_emails_outlook()
    wtnet    = get_emails_wtnet()
    recent   = get_emails_recent_outlook()
    sent     = get_emails_sent_outlook()

    all_msgs = outlook + wtnet
    return {
        "count": len(all_msgs),
        "messages": all_msgs,
        "recent": recent,
        "sent": sent,
        "accounts": [
            {"name": "Outlook", "count": len(outlook)},
            {"name": "wtnet",   "count": len(wtnet)}
        ]
    }


def get_birthdays():
    """Nächste Geburtstage aus Outlook-Kontakten."""
    from datetime import datetime
    import urllib.request
    token = get_token()
    if not token:
        return []
    
    today = datetime.now()
    contacts = []
    url = "https://graph.microsoft.com/v1.0/me/contacts?$select=displayName,birthday&$top=200"
    
    while url:
        data = graph_get(url.replace("https://graph.microsoft.com/v1.0", ""))
        if not data:
            break
        for c in data.get("value", []):
            bd = c.get("birthday")
            if not bd:
                continue
            try:
                dt = datetime.fromisoformat(bd[:10])
                next_bd = dt.replace(year=today.year)
                if next_bd.date() < today.date():
                    next_bd = next_bd.replace(year=today.year + 1)
                days_until = (next_bd.date() - today.date()).days
                birth_year = dt.year
                age = None if birth_year < 1900 else next_bd.year - birth_year
                contacts.append({
                    "days": days_until,
                    "name": c["displayName"],
                    "date": dt.strftime("%d.%m."),
                    "age": age,
                    "today": days_until == 0
                })
            except:
                pass
        url = data.get("@odata.nextLink")
    
    # Duplikate entfernen: gleiche Namen-Tokens + gleicher Geburtstag = Duplikat
    seen = set()
    unique = []
    for c in sorted(contacts, key=lambda x: x["days"]):
        # Name in Tokens aufteilen, sortieren und als Key nutzen
        name_tokens = frozenset(c["name"].lower().split())
        key = (name_tokens, c["date"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    
    return unique[:10]  # Nächste 10


def get_photo_of_day():
    """Holt ein zufälliges Foto aus OneDrive-Reiseordnern."""
    import random
    from datetime import date

    REISE_ORDNER = [
        "Ägypten 99", "Andalusien 2008", "Berlin", "Bormio 2001",
        "Côte d'Azur", "Damüls 2026", "Dänemark 2021", "Florida 2005",
        "Grindelwald 2000", "Harz 2024", "Hong Kong 1999", "Ischgl 2022",
        "Italien 2014", "Kreta 2012", "Kreuzfahrt 2025", "Kroatien 2018",
        "Malediven 2000", "Mallorca 2015", "New York 2000", "Norwegen 2005",
        "Norwegen 2007", "Paris 2002", "Prag 2015", "Rhodos 2020",
        "Sizilien 2013", "Sölden 2023", "Sylt 2012", "Thailand 2022",
        "Teneriffa 2011", "Venedig 2002", "Wien 2003", "Zillertal 2024",
        "Schladming 2024", "USA 2019", "Natur"
    ]

    # Täglich gleicher Ordner (per Datum-Seed)
    random.seed(date.today().toordinal())
    ordner = random.choice(REISE_ORDNER)

    try:
        # Fotos im Ordner holen (Leerzeichen URL-encoden)
        import urllib.parse
        ordner_enc = urllib.parse.quote(ordner)
        data = graph_get(f"/me/drive/root:/{ordner_enc}:/children?$select=name,id,file&$top=100")
        if not data:
            return None

        fotos = [
            item for item in data.get("value", [])
            if "file" in item and item["file"].get("mimeType", "").startswith("image")
        ]
        if not fotos:
            return None

        # 3 verschiedene zufällige Fotos
        auswahl = random.sample(fotos, min(3, len(fotos)))
        results = []
        for foto in auswahl:
            thumb = graph_get(f"/me/drive/items/{foto['id']}/thumbnails/0/large")
            if thumb and "url" in thumb:
                results.append({"url": thumb["url"], "name": foto["name"]})

        if not results:
            return None

        return {
            "photos": results,
            "album": ordner,
            "total_photos": len(fotos)
        }
    except Exception as e:
        print(f"Foto des Tages Fehler: {e}")
        return None


def get_robin_info():
    """Robin-Panel: Standort, Reise-Info, letzte Nachrichten."""
    from datetime import datetime
    today = datetime.now()
    
    # Famulatur Tansania: 01.08. - 08.09.2026
    tansania_start = datetime(2026, 8, 1)
    tansania_end   = datetime(2026, 9, 8)
    
    if today < tansania_start:
        days_until = (tansania_start - today).days
        location = "Ulm"
        location_detail = "Universität Ulm — 10. Semester Medizin"
        status = "studiert"
        travel_info = {
            "event": "Famulatur Tansania",
            "start": "01.08.2026",
            "end": "08.09.2026",
            "days_until": days_until,
            "flight": "Istanbul (RGXQU8)",
            "active": False
        }
        lat, lng = 48.4011, 9.9876  # Ulm
    elif today <= tansania_end:
        days_in = (today - tansania_start).days + 1
        location = "Tansania"
        location_detail = f"Famulatur — Tag {days_in} von 38"
        status = "auf Famulatur"
        travel_info = {
            "event": "Famulatur Tansania",
            "start": "01.08.2026",
            "end": "08.09.2026",
            "days_until": 0,
            "flight": "Istanbul (RGXQU8)",
            "active": True,
            "days_in": days_in
        }
        lat, lng = -6.369, 34.889  # Tansania (Mitte)
    else:
        location = "Ulm"
        location_detail = "Universität Ulm — Doktorarbeit"
        status = "schreibt Doktorarbeit"
        travel_info = None
        lat, lng = 48.4011, 9.9876
    
    return {
        "name": "Robin Mandel",
        "status": status,
        "location": location,
        "location_detail": location_detail,
        "lat": lat,
        "lng": lng,
        "travel": travel_info,
        "email": "robinmandel@outlook.de",
        "study": "Medizin, 10. Semester, Uni Ulm",
        "jarvis": "@RobinMandels_Jarvis_bot"
    }


def get_redesigns_meta():
    meta_path = os.path.expanduser("~/workspace/mission-control/redesign-meta.json")
    if not os.path.exists(meta_path):
        return {"date": None, "design1": None, "design2": None}
    with open(meta_path, encoding="utf-8") as f:
        return json.load(f)


def get_sysinfo():
    import subprocess, shutil

    # RAM
    with open('/proc/meminfo') as f:
        mem = {}
        for line in f:
            k, v = line.split(':', 1)
            mem[k.strip()] = int(v.strip().split()[0])
    ram_total = mem['MemTotal'] // 1024
    ram_free = (mem['MemAvailable']) // 1024
    ram_used = ram_total - ram_free
    ram_pct = int(ram_used / ram_total * 100)

    # Disk C:
    disk = os.statvfs('/mnt/c')
    disk_total = disk.f_blocks * disk.f_frsize // (1024**3)
    disk_free = disk.f_bavail * disk.f_frsize // (1024**3)
    disk_used = disk_total - disk_free
    disk_pct = int(disk_used / disk_total * 100)

    # Uptime
    with open('/proc/uptime') as f:
        secs = float(f.read().split()[0])
    h = int(secs // 3600)
    m = int((secs % 3600) // 60)
    uptime = f"{h}h {m}m" if h > 0 else f"{m}m"

    # Claude Code Status (ersetzt OpenClaw Gateway)
    gw_status = 'claude-code'

    # Git status
    git_info = {"commit": "unbekannt", "branch": "main", "dirty": 0, "last_push": ""}
    try:
        log = subprocess.run(
            ['git', '-C', WORKSPACE, 'log', '--oneline', '-1', '--format=%h|%s|%cr'],
            capture_output=True, text=True, timeout=5
        )
        if log.returncode == 0 and log.stdout.strip():
            parts = log.stdout.strip().split('|')
            git_info["commit"] = parts[0] if len(parts) > 0 else ''
            git_info["message"] = parts[1] if len(parts) > 1 else ''
            git_info["age"] = parts[2] if len(parts) > 2 else ''
        
        status = subprocess.run(
            ['git', '-C', WORKSPACE, 'status', '--short'],
            capture_output=True, text=True, timeout=5
        )
        git_info["dirty"] = len([l for l in status.stdout.strip().splitlines() if l.strip()])
        
        # Remote URL
        remote = subprocess.run(
            ['git', '-C', WORKSPACE, 'remote', 'get-url', 'origin'],
            capture_output=True, text=True, timeout=5
        )
        if remote.returncode == 0:
            url = remote.stdout.strip()
            git_info["repo"] = url.replace('https://github.com/', '').replace('.git', '')
    except Exception as e:
        git_info["error"] = str(e)

    return {
        "ram": {"used_mb": ram_used, "total_mb": ram_total, "pct": ram_pct},
        "disk": {"used_gb": disk_used, "total_gb": disk_total, "pct": disk_pct, "free_gb": disk_free},
        "uptime": uptime,
        "gateway": gw_status,
        "git": git_info
    }


def get_book_health():
    import subprocess, base64, json as _json
    ps = (
        "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8;"
        "$cpu=(Get-WmiObject Win32_Processor).LoadPercentage;"
        "$os=Get-WmiObject Win32_OperatingSystem;"
        "$rT=[math]::Round($os.TotalVisibleMemorySize/1KB,0);"
        "$rF=[math]::Round($os.FreePhysicalMemory/1KB,0);"
        "$dk=Get-WmiObject Win32_LogicalDisk -Filter \"DeviceID='C:'\";"
        "$dT=[math]::Round($dk.Size/1GB,0);"
        "$dF=[math]::Round($dk.FreeSpace/1GB,0);"
        "$bs=Get-WmiObject -Namespace root/wmi -Class BatteryStatus;"
        "$b1=$bs|?{$_.InstanceName -like '*1_0'};"
        "$b2=$bs|?{$_.InstanceName -like '*2_0'};"
        "$fc=(Get-WmiObject -Namespace root/wmi -Class BatteryFullChargedCapacity|?{$_.InstanceName -like '*2_0'}).FullChargedCapacity;"
        "$up=(Get-Date)-(Get-CimInstance Win32_OperatingSystem).LastBootUpTime;"
        "@{cpu=$cpu;ramUsed=($rT-$rF);ramTotal=$rT;diskTotal=$dT;diskFree=$dF;"
        "bat1=if($b1){$b1.RemainingCapacity}else{-1};"
        "bat2=if($b2 -and $fc -gt 0){[math]::Round($b2.RemainingCapacity/$fc*100,0)}else{-1};"
        "bat2Charging=if($b2){[bool]$b2.Charging}else{$false};"
        "uptime=\"$([math]::Floor($up.TotalHours))h $($up.Minutes)m\"}|ConvertTo-Json"
    )
    enc = base64.b64encode(ps.encode('utf-16-le')).decode()
    try:
        r = subprocess.run(
            ['ssh', '-p', '2222', '-i', '/home/bolla/.ssh/id_ed25519',
             '-o', 'ConnectTimeout=5', '-o', 'StrictHostKeyChecking=no',
             'ernst@localhost', f'powershell -EncodedCommand {enc}'],
            capture_output=True, timeout=12
        )
        stdout = r.stdout.decode('utf-8', errors='replace') if r.stdout else ''
        if r.returncode == 0 and stdout.strip():
            d = _json.loads(stdout)
            d['online'] = True
            return d
    except Exception:
        pass
    return {'online': False}


def get_studio_health():
    import subprocess, time as _t
    with open('/proc/meminfo') as f:
        mem = {k.strip(): int(v.strip().split()[0])
               for line in f for k, v in [line.split(':', 1)]}
    ram_total = mem['MemTotal'] // 1024
    ram_used = ram_total - mem['MemAvailable'] // 1024
    disk = os.statvfs('/mnt/c')
    disk_total = disk.f_blocks * disk.f_frsize // (1024**3)
    disk_free = disk.f_bavail * disk.f_frsize // (1024**3)
    with open('/proc/uptime') as f:
        secs = float(f.read().split()[0])
    uptime = f"{int(secs//3600)}h {int((secs%3600)//60)}m"
    def svc(name):
        return bool(subprocess.run(['pgrep', '-f', name],
                                   capture_output=True).returncode == 0)
    return {
        'online': True,
        'ramUsed': ram_used, 'ramTotal': ram_total,
        'diskTotal': disk_total, 'diskFree': disk_free,
        'uptime': uptime,
        'mcServer': svc('mission_control_api'),
        'cloudflared': svc('cloudflared'),
        'telegramBot': svc('telegram_bot'),
    }


def do_book_action(action):
    import subprocess, base64
    if action == 'check':
        return get_book_health()
    if action == 'reboot':
        ps = 'Restart-Computer -Force'
        enc = base64.b64encode(ps.encode('utf-16-le')).decode()
        subprocess.run(
            ['ssh', '-p', '2222', '-i', '/home/bolla/.ssh/id_ed25519',
             '-o', 'ConnectTimeout=5', '-o', 'StrictHostKeyChecking=no',
             'ernst@localhost', f'powershell -EncodedCommand {enc}'],
            timeout=10
        )
        return {'ok': True, 'msg': 'Neustart gesendet'}
    if action == 'restart_tunnel':
        ps = ('Stop-Process -Name ssh -Force -ErrorAction SilentlyContinue;'
              'Start-Sleep 2;'
              'Start-Process powershell -ArgumentList "-WindowStyle Hidden -File C:\\\\Users\\\\ernst\\\\surface_book_tunnel.ps1" -WindowStyle Hidden')
        enc = base64.b64encode(ps.encode('utf-16-le')).decode()
        subprocess.run(
            ['ssh', '-p', '2222', '-i', '/home/bolla/.ssh/id_ed25519',
             '-o', 'ConnectTimeout=5', '-o', 'StrictHostKeyChecking=no',
             'ernst@localhost', f'powershell -EncodedCommand {enc}'],
            timeout=10
        )
        return {'ok': True, 'msg': 'Tunnel-Neustart gesendet'}
    return {'error': 'Unbekannte Aktion'}


def do_studio_action(action):
    import subprocess
    if action == 'restart_mc':
        subprocess.Popen(['pkill', '-f', 'mission_control_api'])
        return {'ok': True, 'msg': 'MC-Server wird neu gestartet...'}
    if action == 'restart_cloudflared':
        subprocess.run(['pkill', '-f', 'cloudflared'], capture_output=True)
        subprocess.Popen(['/home/bolla/.local/bin/cloudflared', 'tunnel', 'run', 'bolla-mc'])
        return {'ok': True, 'msg': 'Cloudflared neu gestartet'}
    if action == 'git_push':
        r = subprocess.run(
            ['git', '-C', WORKSPACE, 'add', '-A'],
            capture_output=True, text=True, timeout=15
        )
        r2 = subprocess.run(
            ['git', '-C', WORKSPACE, 'commit', '-m', 'auto: MC git push'],
            capture_output=True, text=True, timeout=15
        )
        r3 = subprocess.run(
            ['git', '-C', WORKSPACE, 'push'],
            capture_output=True, text=True, timeout=30
        )
        return {'ok': r3.returncode == 0, 'msg': r3.stdout.strip() or r3.stderr.strip() or 'Push abgeschlossen'}
    return {'error': 'Unbekannte Aktion'}


_token_cache = {"ts": 0, "data": None}
_halfday_cache = {"ts": 0, "data": None}

def get_token_halfdays(days=7):
    import time as _t
    if _halfday_cache["data"] and _t.time() - _halfday_cache["ts"] < 120:
        return _halfday_cache["data"]

    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo("Europe/Berlin")
    except Exception:
        tz = timezone.utc

    now_local = datetime.now(timezone.utc).astimezone(tz)
    cutoff = now_local - timedelta(days=days)
    buckets = {}
    proj_dir = "/home/bolla/.claude/projects"
    try:
        for root, _dirs, files in os.walk(proj_dir):
            for fn in files:
                if not fn.endswith(".jsonl"):
                    continue
                try:
                    with open(os.path.join(root, fn), encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            try:
                                d = json.loads(line)
                            except Exception:
                                continue
                            msg = d.get("message")
                            if not isinstance(msg, dict):
                                continue
                            u = msg.get("usage")
                            if not isinstance(u, dict):
                                continue
                            ts = d.get("timestamp", "")
                            if not isinstance(ts, str):
                                continue
                            try:
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                            except Exception:
                                continue
                            local = dt.astimezone(tz)
                            if local < cutoff:
                                continue
                            date_str = local.strftime("%Y-%m-%d")
                            half = "AM" if local.hour < 12 else "PM"
                            key = (date_str, half)
                            b = buckets.setdefault(key, {"input":0,"output":0,"cache_read":0,"cache_creation":0})
                            b["input"] += u.get("input_tokens", 0) or 0
                            b["output"] += u.get("output_tokens", 0) or 0
                            b["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
                            b["cache_creation"] += u.get("cache_creation_input_tokens", 0) or 0
                except Exception:
                    continue
    except Exception as e:
        print(f"halfday error: {e}")

    result = []
    for i in range(days - 1, -1, -1):
        day = now_local - timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        weekday = ["Mo","Di","Mi","Do","Fr","Sa","So"][day.weekday()]
        for half in ["AM", "PM"]:
            b = buckets.get((date_str, half), {"input":0,"output":0,"cache_read":0,"cache_creation":0})
            result.append({
                "date": date_str,
                "weekday": weekday,
                "label": f"{weekday} {day.strftime('%d.%m.')}",
                "half": half,
                "input": b["input"],
                "output": b["output"],
                "cache_read": b["cache_read"],
                "cache_creation": b["cache_creation"],
                "total_in": b["input"] + b["cache_read"] + b["cache_creation"],
                "total_out": b["output"]
            })
    data = {"halfdays": result, "days": days}
    _halfday_cache["data"] = data
    _halfday_cache["ts"] = _t.time()
    return data


def get_token_usage():
    """Summiert Claude-Code Token-Verbrauch aus den Session-JSONL-Dateien."""
    import time as _t
    if _token_cache["data"] and _t.time() - _token_cache["ts"] < 60:
        return _token_cache["data"]

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    t_in = t_out = t_cr = t_ce = 0
    a_in = a_out = a_cr = a_ce = 0
    latest_ts = ""
    latest_model = ""
    proj_dir = "/home/bolla/.claude/projects"
    try:
        for root, _dirs, files in os.walk(proj_dir):
            for fn in files:
                if not fn.endswith(".jsonl"):
                    continue
                try:
                    with open(os.path.join(root, fn), encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            try:
                                d = json.loads(line)
                            except Exception:
                                continue
                            msg = d.get("message")
                            if not isinstance(msg, dict):
                                continue
                            ts = d.get("timestamp", "")
                            mdl = msg.get("model")
                            if isinstance(mdl, str) and mdl and isinstance(ts, str) and ts > latest_ts:
                                latest_ts = ts
                                latest_model = mdl
                            u = msg.get("usage")
                            if not isinstance(u, dict):
                                continue
                            inp = u.get("input_tokens", 0) or 0
                            out = u.get("output_tokens", 0) or 0
                            cr = u.get("cache_read_input_tokens", 0) or 0
                            ce = u.get("cache_creation_input_tokens", 0) or 0
                            a_in += inp; a_out += out; a_cr += cr; a_ce += ce
                            if isinstance(ts, str) and ts.startswith(today):
                                t_in += inp; t_out += out; t_cr += cr; t_ce += ce
                except Exception:
                    continue
    except Exception as e:
        print(f"tokenusage error: {e}")

    def _pretty(m):
        if not m:
            return "Claude"
        p = m.split("-")
        if len(p) >= 4 and p[0] == "claude":
            return f"Claude {p[1].capitalize()} {p[2]}.{p[3]}"
        return m

    data = {
        "model": f"{_pretty(latest_model)} (Max Plan)",
        "today": {"input": t_in, "output": t_out, "cache_read": t_cr, "cache_creation": t_ce},
        "total": {"input": a_in, "output": a_out, "cache_read": a_cr, "cache_creation": a_ce},
        "note": "Max Plan — keine Kosten"
    }
    _token_cache["ts"] = _t.time()
    _token_cache["data"] = data
    return data


def bolla_chat_stream(message, session_id=None, image_b64=None):
    """Streamt Claude-Code-Events als Generator. Jeder yield ist ein JSON-Objekt."""
    import subprocess, tempfile, base64, shutil
    claude_bin = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
    cmd = [claude_bin, "-p", "--output-format", "stream-json", "--verbose"]
    if session_id:
        cmd.extend(["--resume", session_id])

    tmp_path = None
    if image_b64:
        try:
            img_data = base64.b64decode(image_b64)
            tmp = tempfile.NamedTemporaryFile(suffix=".png", prefix="bolla_img_", delete=False)
            tmp.write(img_data)
            tmp.close()
            tmp_path = tmp.name
            message = f"Schau dir das Bild an: {tmp_path}\n\n{message}" if message else f"Beschreibe was du in diesem Bild siehst: {tmp_path}"
        except Exception as e:
            print(f"Bild-Fehler: {e}")

    cmd.append(message)
    proc = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=os.path.expanduser("~"),
        )
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                yield {"type": "raw", "text": line}
        proc.wait(timeout=5)
        if proc.returncode != 0:
            err = proc.stderr.read() if proc.stderr else ""
            yield {"type": "error", "error": err.strip() or f"Exit {proc.returncode}"}
    except Exception as e:
        yield {"type": "error", "error": str(e)}
    finally:
        if proc and proc.poll() is None:
            proc.kill()
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except:
                pass


def azure_list_voices():
    """Holt die Stimmen-Liste von Azure."""
    cfg = azure_speech_config()
    if not cfg:
        return {"error": "Azure Speech nicht konfiguriert. Key in config/azure_speech.json eintragen."}
    import urllib.request
    url = f"https://{cfg['region']}.tts.speech.microsoft.com/cognitiveservices/voices/list"
    req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": cfg["key"]})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            voices = json.loads(r.read())
        # Filtern: nur DE + EN, neural, kompakte Form
        filtered = [
            {
                "name": v["ShortName"],
                "display": v.get("LocalName", v["ShortName"]),
                "locale": v["Locale"],
                "gender": v["Gender"],
                "styles": v.get("StyleList", []),
            }
            for v in voices
            if v.get("VoiceType") == "Neural" and (v["Locale"].startswith("de-") or v["Locale"].startswith("en-"))
        ]
        filtered.sort(key=lambda x: (not x["locale"].startswith("de-"), x["locale"], x["name"]))
        return {"voices": filtered, "default": cfg.get("default_voice", "de-DE-SeraphinaMultilingualNeural")}
    except Exception as e:
        return {"error": str(e)}


def azure_tts(text, voice, rate_percent=0):
    """Synthetisiert Text → MP3-Bytes. Gibt (bytes, error) zurück."""
    cfg = azure_speech_config()
    if not cfg:
        return None, "Azure Speech nicht konfiguriert"
    import urllib.request
    # SSML escapen
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    rate_sign = "+" if rate_percent >= 0 else ""
    locale = "-".join(voice.split("-")[:2]) if "-" in voice else "de-DE"
    ssml = (
        f"<speak version='1.0' xml:lang='{locale}'>"
        f"<voice name='{voice}'>"
        f"<prosody rate='{rate_sign}{int(rate_percent)}%'>{esc(text)}</prosody>"
        f"</voice></speak>"
    )
    url = f"https://{cfg['region']}.tts.speech.microsoft.com/cognitiveservices/v1"
    req = urllib.request.Request(
        url,
        data=ssml.encode("utf-8"),
        headers={
            "Ocp-Apim-Subscription-Key": cfg["key"],
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "bolla-mission-control",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read(), None
    except Exception as e:
        return None, str(e)


# ============ ADB / SURFACE ============
def _adb_run(args, timeout=15):
    import subprocess
    try:
        r = subprocess.run(["adb"] + list(args), capture_output=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace").strip()
    except subprocess.TimeoutExpired:
        return -1, b"", "Timeout — Gerät nicht erreichbar?"
    except FileNotFoundError:
        return -2, b"", "adb nicht installiert"

def adb_devices():
    rc, out, err = _adb_run(["devices"], timeout=5)
    if rc < 0:
        return {"devices": [], "error": err}
    devices = []
    for line in out.decode("utf-8", "replace").splitlines()[1:]:
        parts = line.strip().split()
        if len(parts) >= 2:
            devices.append({"id": parts[0], "state": parts[1]})
    return {"devices": devices, "error": None if rc == 0 else (err or "Fehler")}

def adb_packages(filter_str="", kind="all"):
    args = ["shell", "pm", "list", "packages"]
    if kind == "user":
        args.append("-3")
    elif kind == "system":
        args.append("-s")
    rc, out, err = _adb_run(args, timeout=15)
    if rc != 0:
        return {"packages": [], "error": err or "adb-Fehler"}
    pkgs = []
    f = (filter_str or "").lower().strip()
    for line in out.decode("utf-8", "replace").splitlines():
        line = line.strip()
        if line.startswith("package:"):
            name = line[8:]
            if not f or f in name.lower():
                pkgs.append(name)
    pkgs.sort()
    return {"packages": pkgs, "count": len(pkgs), "error": None}

def adb_connect(host):
    host = (host or "").strip()
    if not host or " " in host or "\n" in host:
        return {"ok": False, "error": "Ungültige Adresse"}
    rc, out, err = _adb_run(["connect", host], timeout=10)
    msg = (out.decode("utf-8", "replace") + " " + err).strip()
    ok = rc == 0 and ("connected" in msg.lower() or "already" in msg.lower())
    return {"ok": ok, "message": msg, "error": None if ok else (msg or "Verbindung fehlgeschlagen")}

def adb_disconnect(host=""):
    args = ["disconnect"]
    if host:
        args.append(host)
    rc, out, err = _adb_run(args, timeout=5)
    return {"ok": rc == 0, "message": (out.decode("utf-8","replace") + " " + err).strip()}

def adb_screenshot():
    rc, png, err = _adb_run(["exec-out", "screencap", "-p"], timeout=15)
    if rc != 0 or not png:
        return None, err or "Screenshot fehlgeschlagen"
    return png, None

def adb_push(filename, remote_dir, data_bytes):
    import tempfile
    filename = (filename or "").strip()
    remote_dir = (remote_dir or "").strip()
    if not filename or "/" in filename or "\\" in filename or "\0" in filename:
        return {"ok": False, "error": "Ungültiger Dateiname"}
    if not remote_dir or "\n" in remote_dir or "\0" in remote_dir:
        return {"ok": False, "error": "Ungültiger Zielpfad"}
    if not data_bytes:
        return {"ok": False, "error": "Keine Daten"}
    with tempfile.NamedTemporaryFile(delete=False, suffix="_" + filename) as tf:
        tf.write(data_bytes)
        local = tf.name
    try:
        remote = remote_dir.rstrip("/") + "/" + filename
        rc, out, err = _adb_run(["push", local, remote], timeout=300)
        if rc != 0:
            return {"ok": False, "error": err or "Push fehlgeschlagen"}
        return {"ok": True, "message": f"→ {remote} ({len(data_bytes)} Bytes)", "bytes": len(data_bytes)}
    finally:
        try: os.unlink(local)
        except Exception: pass

def adb_ls(path="/storage/emulated/0"):
    import shlex
    path = (path or "/storage/emulated/0").strip() or "/"
    if any(c in path for c in "\n\r\0"):
        return {"error": "Ungültiger Pfad"}
    rc, out, err = _adb_run(["shell", f"ls -laL {shlex.quote(path)} 2>/dev/null || ls -la {shlex.quote(path)}"], timeout=15)
    if rc != 0:
        return {"error": err or "Pfad nicht lesbar"}
    entries = []
    for line in out.decode("utf-8", "replace").splitlines():
        line = line.rstrip()
        if not line or line.startswith("total "):
            continue
        parts = line.split(None, 7)
        if len(parts) < 8:
            continue
        perms = parts[0]
        raw_name = parts[7]
        # Broken symlinks (l?????????) haben nur 7 Felder vor dem Namen statt 8
        if raw_name.startswith("-> ") and len(parts) > 6:
            name = parts[6]
        else:
            name = raw_name.split(" -> ", 1)[0]
        if name in (".", "..", ""):
            continue
        # Unleserliche Einträge überspringen
        if perms.startswith("?") or "?" in perms[:10] and perms.count("?") > 3:
            continue
        if perms.startswith("d"):
            kind = "dir"
        elif perms.startswith("l"):
            kind = "link"
        else:
            kind = "file"
        try:
            size = int(parts[4])
        except Exception:
            size = 0
        entries.append({"name": name, "type": kind, "size": size})
    entries.sort(key=lambda e: (e["type"] == "file", e["name"].lower()))
    normalized = path.rstrip("/") or "/"
    if normalized == "/":
        parent = None
    else:
        parent = "/".join(normalized.split("/")[:-1]) or "/"
    return {"path": normalized, "parent": parent, "entries": entries, "error": None}

def adb_info(kind="device"):
    kind = (kind or "device").strip().lower()
    if kind == "device":
        rc, out, err = _adb_run([
            "shell", "sh", "-c",
            "echo MODEL=$(getprop ro.product.model); "
            "echo MANUFACTURER=$(getprop ro.product.manufacturer); "
            "echo ANDROID=$(getprop ro.build.version.release); "
            "echo SDK=$(getprop ro.build.version.sdk); "
            "echo SIZE=$(wm size 2>/dev/null | grep -oE '[0-9]+x[0-9]+' | head -1)"
        ], timeout=10)
        if rc != 0:
            return {"error": err or "adb-Fehler"}
        props = {}
        for line in out.decode("utf-8", "replace").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                props[k.strip()] = v.strip()
        return {"kind": "device", "props": props, "error": None}
    if kind == "battery":
        rc, out, err = _adb_run(["shell", "dumpsys", "battery"], timeout=10)
        if rc != 0:
            return {"error": err or "adb-Fehler"}
        props = {}
        for line in out.decode("utf-8", "replace").splitlines():
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                props[k.strip().replace(" ", "_")] = v.strip()
        status_map = {"1":"Unbekannt","2":"Lädt","3":"Entlädt","4":"Nicht lädt","5":"Voll"}
        if "status" in props:
            props["status_text"] = status_map.get(props["status"], props["status"])
        return {"kind": "battery", "props": props, "error": None}
    if kind == "foreground":
        rc, out, err = _adb_run(["shell", "dumpsys", "activity", "activities"], timeout=10)
        if rc != 0:
            return {"error": err or "adb-Fehler"}
        import re
        text = out.decode("utf-8", "replace")
        for pattern in (r'mResumedActivity[^\n]*\{[^}]*\s+(\S+)/(\S+)', r'topResumedActivity[^\n]*\{[^}]*\s+(\S+)/(\S+)'):
            m = re.search(pattern, text)
            if m:
                pkg, act = m.group(1), m.group(2)
                if act.startswith("."):
                    act = pkg + act
                return {"kind": "foreground", "package": pkg, "activity": act, "error": None}
        return {"error": "Keine aktive App erkennbar"}
    return {"error": f"Unbekannter Info-Typ: {kind}"}

def adb_pull(remote):
    import tempfile
    remote = (remote or "").strip()
    if not remote or "\0" in remote or "\n" in remote:
        return None, "Ungültiger Pfad"
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        local = tf.name
    try:
        rc, _, err = _adb_run(["pull", remote, local], timeout=120)
        if rc != 0:
            return None, err or "Pull fehlgeschlagen"
        with open(local, "rb") as f:
            data = f.read()
        return data, None
    finally:
        try: os.unlink(local)
        except Exception: pass


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silent

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Type", "application/json; charset=utf-8")

    def _send_json(self, data, status=200):
        self.send_response(status)
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

    def _proxy_lms(self, method, body_bytes=None):
        import urllib.request, urllib.error
        target = lms_base_url() + self.path[len("/api/lms"):]
        req = urllib.request.Request(target, data=body_bytes, method=method)
        if body_bytes is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
                self.send_response(r.status)
                ct = r.headers.get("Content-Type", "application/json")
                self.send_header("Content-Type", ct)
                self._cors_headers()
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.URLError as e:
            self._send_json({"error": f"LM Studio nicht erreichbar: {e}"}, status=502)

    def do_GET(self):
        try:
            if self.path.startswith("/api/lms/"):
                self._proxy_lms("GET")
                return

            if self.path in ("/", "/index.html"):
                html_path = os.path.expanduser("~/workspace/mission-control/index.html")
                with open(html_path, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            # ===== MOBILE / PWA (MC Chris) =====
            MOBILE_STATIC = {
                "/m":                        ("mobile.html",            "text/html; charset=utf-8", "no-store"),
                "/mobile.html":              ("mobile.html",            "text/html; charset=utf-8", "no-store"),
                "/manifest.webmanifest":     ("manifest.webmanifest",   "application/manifest+json", "max-age=3600"),
                "/sw.js":                    ("sw.js",                  "application/javascript", "no-store"),
                "/mc-icon-192.png":          ("mc-icon-192.png",        "image/png", "max-age=604800"),
                "/mc-icon-512.png":          ("mc-icon-512.png",        "image/png", "max-age=604800"),
                "/mc-apple-touch.png":       ("mc-apple-touch.png",     "image/png", "max-age=604800"),
                "/redesign-aurora.html":     ("redesign-aurora.html",   "text/html; charset=utf-8", "no-store"),
                "/redesign-cyber.html":      ("redesign-cyber.html",    "text/html; charset=utf-8", "no-store"),
                "/redesign-1.html":          ("redesign-1.html",        "text/html; charset=utf-8", "no-store"),
                "/redesign-2.html":          ("redesign-2.html",        "text/html; charset=utf-8", "no-store"),
            }
            if self.path in MOBILE_STATIC:
                fname, ctype, cache = MOBILE_STATIC[self.path]
                fpath = os.path.expanduser(f"~/workspace/mission-control/{fname}")
                with open(fpath, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Cache-Control", cache)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/favicon.ico":
                ico_path = os.path.expanduser("~/workspace/mission-control/favicon.ico")
                with open(ico_path, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/x-icon")
                self.send_header("Cache-Control", "max-age=86400")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/api/bolla/avatar":
                avatar_path = os.path.expanduser("~/workspace/bolla_avatar.png")
                with open(avatar_path, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Disposition", 'attachment; filename="bolla_avatar.png"')
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/api/bolla/voices":
                self._send_json(azure_list_voices())
                return

            if self.path == "/api/adb/devices":
                self._send_json(adb_devices())
                return

            if self.path.startswith("/api/adb/packages"):
                import urllib.parse as _up
                qs = _up.urlparse(self.path).query
                params = dict(_up.parse_qsl(qs))
                self._send_json(adb_packages(params.get("filter", ""), params.get("kind", "all")))
                return

            if self.path.startswith("/api/adb/info"):
                import urllib.parse as _up
                qs = _up.urlparse(self.path).query
                params = dict(_up.parse_qsl(qs))
                self._send_json(adb_info(params.get("kind", "device")))
                return

            if self.path.startswith("/api/adb/ls"):
                import urllib.parse as _up
                qs = _up.urlparse(self.path).query
                params = dict(_up.parse_qsl(qs))
                self._send_json(adb_ls(params.get("path", "/storage/emulated/0")))
                return

            simple = {
                "/api/calendar": get_calendar,
                "/api/email": get_emails,
                "/api/photo": lambda: get_photo_of_day() or {},
                "/api/birthdays": get_birthdays,
                "/api/robin": get_robin_info,
                "/api/sysinfo": get_sysinfo,
                "/api/surfaces/book": get_book_health,
                "/api/surfaces/studio": get_studio_health,
                "/api/tokenusage": get_token_usage,
                "/api/tokenusage/history": get_token_halfdays,
                "/api/status": lambda: {"ok": True, "ts": datetime.now().isoformat()},
                "/api/redesigns-meta": get_redesigns_meta,
            }
            if self.path in simple:
                self._send_json(simple[self.path]())
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"GET Error: {tb}")
            try:
                self._send_json({"error": str(e)}, status=500)
            except Exception:
                pass

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b""
        except Exception:
            raw = b""

        if self.path.startswith("/api/lms/"):
            try:
                self._proxy_lms("POST", raw)
            except Exception as e:
                tb = traceback.format_exc()
                print(f"LMS proxy error: {tb}")
                try:
                    self._send_json({"error": str(e)}, status=500)
                except Exception:
                    pass
            return

        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            body = {}

        try:
            if self.path == "/api/bolla/chat":
                self._handle_bolla_stream(body)
            elif self.path == "/api/bolla/tts":
                self._handle_tts(body)
            elif self.path == "/api/surfaces/book/action":
                self._send_json(do_book_action(body.get("action", "")))
            elif self.path == "/api/surfaces/studio/action":
                self._send_json(do_studio_action(body.get("action", "")))
            elif self.path == "/api/adb/connect":
                self._send_json(adb_connect(body.get("host", "")))
            elif self.path == "/api/adb/disconnect":
                self._send_json(adb_disconnect(body.get("host", "")))
            elif self.path == "/api/adb/screenshot":
                png, err = adb_screenshot()
                if err or not png:
                    self._send_json({"error": err or "Screenshot fehlgeschlagen"}, status=500)
                    return
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(png)))
                self.end_headers()
                self.wfile.write(png)
            elif self.path == "/api/adb/push":
                import base64
                try:
                    data = base64.b64decode(body.get("data_b64", ""))
                except Exception:
                    self._send_json({"ok": False, "error": "Ungültige Datei-Daten"}, status=400)
                    return
                self._send_json(adb_push(body.get("filename", ""), body.get("remote_dir", "/sdcard/"), data))
            elif self.path == "/api/adb/pull":
                remote = body.get("remote", "")
                data, err = adb_pull(remote)
                if err or data is None:
                    self._send_json({"error": err or "Pull fehlgeschlagen"}, status=500)
                    return
                fname = os.path.basename(remote) or "download"
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            elif self.path == "/api/bildgen":
                prompt = body.get("prompt", "").strip()
                if not prompt:
                    self._send_json({"error": "Kein Prompt angegeben"}, status=400)
                    return
                ok, limit_err = bildgen_check_limit()
                if not ok:
                    self._send_json({"error": limit_err}, status=429)
                    return
                model = body.get("model", "gemini-2.5-flash-image")
                aspect = body.get("aspect_ratio", "1:1")
                in_img  = body.get("input_image_b64")
                in_mime = body.get("input_mime_type", "image/png")
                img_b64, mime_or_err = bildgen_generate(prompt, model, aspect, in_img, in_mime)
                if img_b64 is None:
                    self._send_json({"error": mime_or_err}, status=500)
                else:
                    _bildgen_counter["count"] += 1
                    remaining = BILDGEN_LIMIT - _bildgen_counter["count"]
                    self._send_json({"image_b64": img_b64, "mime_type": mime_or_err, "remaining": remaining})
            elif self.path == "/api/suno/generate":
                name = body.get("name", "").strip()
                klasse = body.get("klasse", "").strip()
                alter = body.get("alter", "").strip()
                geburtstag = body.get("geburtstag", "").strip()
                sprache = body.get("sprache", "de")
                hit = body.get("hit", "").strip()
                feedback = body.get("feedback", "").strip()
                if not name:
                    self._send_json({"error": "Name fehlt"}, status=400)
                    return
                if sprache == "de":
                    lang_inst = "auf Deutsch"
                else:
                    lang_inst = ("in English. IMPORTANT: Before writing the lyrics, analyze the name and find the single best "
                                 "English phonetic spelling that makes an English AI singer pronounce it exactly like a German "
                                 "speaker would. Rules: (1) Use hyphenated syllables if the name has multiple syllables "
                                 "(e.g. 'Jette' → 'Yet-teh', 'Jan' → 'Yahn', 'Jens' → 'Yens', 'Grete' → 'Greh-teh', "
                                 "'Heinz' → 'Hynts'). (2) Every syllable must be pronounceable by an English singer. "
                                 "(3) Use 'eh' for short German e, 'ah' for long German a, 'oo' for German u, 'y' for German j. "
                                 "(4) Replace EVERY occurrence of the name in the lyrics with this phonetic spelling. "
                                 "(5) Do NOT use parenthetical hints or footnotes — only the phonetic spelling in the text.")
                hit_inst = f"Orientiere dich am Stil und der Struktur des Songs '{hit}'." if hit else ""
                feedback_inst = f"Verbessere folgendes gegenüber der letzten Version: {feedback}" if feedback else ""
                prompt = f"""Du bist ein professioneller Songwriter für Suno AI. Erstelle einen Geburtstagssong {lang_inst}.

Schüler/in: {name}
Klasse: {klasse}
Alter: {alter}
Geburtstag: {geburtstag}
{hit_inst}
{feedback_inst}

Pflichtinhalte im Liedtext:
- Name des Schülers / der Schülerin mehrfach nennen
- Lessing-Gymnasium erwähnen
- Computerkurs bei Herrn Mandel erwähnen

Struktur: [Intro], [Verse 1], [Chorus], [Verse 2], [Chorus], [Bridge], [Outro]

Gib deine Antwort als JSON zurück (kein Markdown, nur reines JSON):
{{
  "title": "kreativer Songtitel mit passenden Emojis — verwende im Titel immer die ORIGINAL-Schreibweise des Namens, nicht die phonetische",
  "lyrics": "vollständiger Liedtext mit Struktur-Tags",
  "style": "Suno style prompt auf Englisch, professionell, 15-25 Wörter, mit Tempo, Instrumente, Stimmung, Genre"
}}"""
                import subprocess, shutil
                claude_bin = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
                result = subprocess.run(
                    [claude_bin, "-p", "--output-format", "json", prompt],
                    capture_output=True, text=True, timeout=120,
                    cwd=os.path.expanduser("~")
                )
                if result.returncode != 0:
                    self._send_json({"error": result.stderr[:200]}, status=500)
                    return
                raw = json.loads(result.stdout).get("result", "")
                raw = raw.strip()
                if raw.startswith("```"):
                    raw = "\n".join(raw.split("\n")[1:])
                if raw.endswith("```"):
                    raw = raw.rsplit("```", 1)[0]
                song_data = json.loads(raw.strip())
                if sprache == "de" and "style" in song_data:
                    song_data["style"] = song_data["style"].rstrip(", ") + ", german lyrics"
                if sprache != "de" and name and "title" in song_data:
                    # Ensure original name spelling in title (not phonetic)
                    import re as _re
                    phonetic = _re.sub(r'[^a-zA-Z]', '', name.lower())
                    song_data["title"] = name + " — " + song_data["title"] if name.lower() not in song_data["title"].lower() else song_data["title"]
                if sprache == "de":
                    parts = ["Happy Birthday", name]
                    if alter: parts.append(alter)
                    if geburtstag:
                        gb = geburtstag.strip().rstrip(".")
                        segments = [s for s in gb.split(".") if s]
                        if len(segments) == 2:
                            gb = gb.rstrip(".") + ".26"
                        parts.append(gb)
                    song_data["title"] = " ".join(parts)
                self._send_json(song_data)
            else:
                self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            tb = traceback.format_exc()
            print(f"POST Error: {tb}")
            try:
                self._send_json({"error": str(e)}, status=500)
            except Exception:
                pass

    def _handle_bolla_stream(self, body):
        msg = body.get("message", "").strip()
        if not msg and not body.get("image"):
            self._send_json({"error": "Keine Nachricht"}, status=400)
            return
        sid = body.get("session_id")
        img = body.get("image")

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        try:
            for event in bolla_chat_stream(msg, sid, image_b64=img):
                line = json.dumps(event, ensure_ascii=False) + "\n"
                self.wfile.write(line.encode("utf-8"))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:
            try:
                err = json.dumps({"type": "error", "error": str(e)}) + "\n"
                self.wfile.write(err.encode())
                self.wfile.flush()
            except Exception:
                pass

    def _handle_tts(self, body):
        text = (body.get("text") or "").strip()
        if not text:
            self._send_json({"error": "Kein Text"}, status=400)
            return
        voice = body.get("voice") or "de-DE-SeraphinaMultilingualNeural"
        try:
            rate = int(body.get("rate", 0))
        except (TypeError, ValueError):
            rate = 0
        rate = max(-50, min(100, rate))

        # Text kürzen zur Sicherheit (Azure-Limit ist hoch, aber 2000 reicht für Sprachausgabe)
        if len(text) > 2000:
            text = text[:2000] + "..."

        audio, err = azure_tts(text, voice, rate)
        if err or not audio:
            self._send_json({"error": err or "TTS fehlgeschlagen"}, status=500)
            return
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Type", "audio/mpeg")
        self.send_header("Content-Length", str(len(audio)))
        self.end_headers()
        self.wfile.write(audio)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()


if __name__ == "__main__":
    port = 18790
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Mission Control API läuft auf http://127.0.0.1:{port}")
    server.serve_forever()
