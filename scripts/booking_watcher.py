#!/usr/bin/env python3
"""
Booking-Wächter  🏨🐾
Scannt ernstmandel@outlook.de (Graph) nach Booking.com-Buchungsbestätigungen,
parst Hotel / Ort / Check-in / Check-out / Storno-Frist / Buchungsnummer,
ordnet die Buchung automatisch der passenden Reise-Etappe zu (Ortsabgleich
gegen SR_ROUTE in index.html), trägt sie über die MC-API in den Reiseplaner ein,
legt einen Storno-Kalendertermin an und meldet alles per Telegram.

Etappen = einzige Quelle: SR_ROUTE in mission-control/index.html (kein Drift).
Nicht zuordenbare Buchungen → Telegram-Hinweis "bitte manuell zuordnen".
Bestehende Etappen-Hotels werden NIE stumm überschrieben (nur gemeldet).

Cron:  7 */2 * * *  python3 /home/bolla/workspace/scripts/booking_watcher.py
Test:  python3 booking_watcher.py --test   (parst, schreibt NICHT, kein Telegram)
"""
import json, re, sys, urllib.parse, urllib.request
from pathlib import Path
from datetime import datetime, timedelta

WS      = Path("/home/bolla/workspace")
CFG     = WS / "config"
INDEX   = WS / "mission-control" / "index.html"
STATE   = CFG / "booking_watcher_state.json"
MC_API  = "http://127.0.0.1:18790"
TEST    = "--test" in sys.argv

TG    = json.loads((CFG / "telegram_bot.json").read_text())
OAUTH = json.loads((CFG / "outlook_oauth2.json").read_text())
TOKF  = CFG / "outlook_token.json"

MONATE = {  # deutsche Monatskürzel & -namen → Nummer
    "jan": 1, "feb": 2, "mrz": 3, "mär": 3, "apr": 4, "mai": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dez": 12,
    "januar": 1, "februar": 2, "märz": 3, "april": 4, "juni": 6, "juli": 7,
    "august": 8, "september": 9, "oktober": 10, "november": 11, "dezember": 12,
}


# ───────────────────────── Infrastruktur ─────────────────────────
def tg(text):
    if TEST:
        print("[telegram]\n" + text + "\n")
        return
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{TG['bot_token']}/sendMessage",
            data=json.dumps({"chat_id": TG["chris_id"], "text": text,
                             "parse_mode": "Markdown", "disable_web_page_preview": True}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e:
        print("tg err", e)


def token():
    tok = json.loads(TOKF.read_text())
    data = urllib.parse.urlencode({
        "client_id": OAUTH["client_id"], "client_secret": OAUTH["client_secret"],
        "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
        "scope": "Mail.ReadWrite offline_access"}).encode()
    new = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
        data=data, method="POST")).read())
    tok.update(new); TOKF.write_text(json.dumps(tok, indent=2)); TOKF.chmod(0o600)
    return new["access_token"]


def mc_post(path, payload):
    """POST an die lokale Mission-Control-API (Speichern / Kalender)."""
    if TEST:
        print(f"[mc-api {path}] {json.dumps(payload, ensure_ascii=False)}")
        return {"ok": True, "_test": True}
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            MC_API + path, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"}, method="POST"), timeout=25)
        return json.loads(r.read())
    except Exception as e:
        return {"ok": False, "error": str(e)}


# Nachbarorte / alternative Schreibweisen je Etappe (booking.com nennt oft den
# Nachbarort statt des Etappennamens). Keyed nach SR_ROUTE-id. Name selbst ist
# immer implizit dabei — hier nur die Zusätze.
ALIASES = {
    "bb":   ["baden baden"],
    "gen":  [],
    "fd":   ["baiersbronn", "loßburg", "lossburg", "pfalzgrafenweiler"],
    "tri":  ["schonach", "schönwald", "schoenwald"],
    "titi": ["titisee-neustadt", "neustadt", "hinterzarten", "saig", "lenzkirch",
             "schluchsee", "feldberg", "breitnau"],
    "fel":  ["feldberg", "todtnau", "bärental", "baerental"],
    "fre":  ["freiburg im breisgau", "breisgau", "umkirch", "gundelfingen",
             "merzhausen", "kirchzarten", "horben"],
    "kon":  ["constance", "kreuzlingen", "allensbach", "reichenau"],
    "mai":  ["insel mainau"],
    "mee":  ["uhldingen", "uhldingen-mühlhofen", "unteruhldingen", "hagnau",
             "stetten", "daisendorf"],
    "uel":  ["überlingen am bodensee", "ueberlingen", "owingen"],
    "fn":   ["friedrichshafen am bodensee", "fischbach", "immenstaad", "eriskirch"],
    "lin":  ["lindau (bodensee)", "lindau bodensee", "wasserburg", "bad schachen",
             "weißensberg", "weissensberg", "bodolz", "nonnenhorn"],
    "bre":  ["lochau", "hard", "hörbranz", "hoerbranz", "wolfurt", "lauterach"],
}


def load_etappen():
    """Etappen (id, name) direkt aus SR_ROUTE in index.html — keine Doppelpflege."""
    txt = INDEX.read_text(encoding="utf-8")
    blk = re.search(r"const SR_ROUTE\s*=\s*\[(.*?)\n\];", txt, re.S)
    src = blk.group(1) if blk else txt
    out = []
    for m in re.finditer(r"id:'([^']+)',\s*name:'([^']+)'", src):
        out.append({"id": m.group(1), "name": m.group(2)})
    return out


# ───────────────────────── Parsing ─────────────────────────
def html_to_text(html):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&nbsp;", " ", t)
    t = re.sub(r"&amp;", "&", t)
    t = re.sub(r"&[a-zA-Z#0-9]+;", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def _date(d, mon, y):
    mon = MONATE.get(mon.lower().rstrip("."))
    if not mon:
        return None
    try:
        return datetime(int(y), mon, int(d)).date()
    except ValueError:
        return None


def parse_booking(subject, text):
    """Liefert dict mit hotel, ort, checkin, checkout, stornofrist (alle YYYY-MM-DD),
    buchungsnr — oder None, wenn es keine echte Bestätigung ist."""
    low = text.lower()
    # echte Bestätigung muss An-/Abreise enthalten
    if not (("anreise" in low or "check-in" in low) and ("abreise" in low or "check-out" in low)):
        return None

    res = {"hotel": "", "ort": "", "checkin": "", "checkout": "",
           "stornofrist": "", "buchungsnr": ""}

    # Hotelname: aus Subject ("…bestätigt: Hotel X" / "Hotel X: Buchung …")
    m = re.search(r"best[äa]tigt:\s*(.+)$", subject, re.I)
    mu = re.search(r"in der Unterkunft\s+(.+)$", subject, re.I)  # "aktualisierte/neue Buchung in der Unterkunft X"
    if m:
        res["hotel"] = m.group(1).strip()
    elif mu:
        res["hotel"] = mu.group(1).strip()
    else:
        res["hotel"] = re.split(r":\s*Buchung|\s*:\s*Buchung| via Booking", subject)[0].strip()
    res["hotel"] = re.sub(r"^[^\w]+", "", res["hotel"]).strip()

    # Buchungsnummer
    m = re.search(r"Buchung(?:snummer)?[:\s]+([\d][\d-]{6,})", subject + " " + text)
    if m:
        res["buchungsnr"] = m.group(1)

    # Check-in / Check-out  ("Anreise Mi 25 Mrz 2026" / "Anreise Samstag, 25. Juli 2026")
    # \D{0,20} überspringt den ausgeschriebenen Wochentag samt Komma vor dem Tag.
    ci = re.search(r"Anreise\D{0,20}?(\d{1,2})\.?\s+([A-Za-zäöüÄÖÜ]+)\.?\s+(\d{4})", text)
    co = re.search(r"Abreise\D{0,20}?(\d{1,2})\.?\s+([A-Za-zäöüÄÖÜ]+)\.?\s+(\d{4})", text)
    # Fallback: "Check-in TT.MM.JJJJ"
    if not ci:
        ci2 = re.search(r"Check-?in\D{0,6}(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
        ci = ("num", ci2) if ci2 else None
    if not co:
        co2 = re.search(r"Check-?out\D{0,6}(\d{1,2})\.(\d{1,2})\.(\d{4})", text)
        co = ("num", co2) if co2 else None

    def resolve(m):
        if m is None:
            return None
        if isinstance(m, tuple):  # numerisches Format
            g = m[1]
            try:
                return datetime(int(g.group(3)), int(g.group(2)), int(g.group(1))).date()
            except ValueError:
                return None
        return _date(m.group(1), m.group(2), m.group(3))

    d_ci, d_co = resolve(ci), resolve(co)
    if d_ci:
        res["checkin"] = d_ci.isoformat()
    if d_co:
        res["checkout"] = d_co.isoformat()

    # Storno-Frist
    # (a) absolutes Datum:  "kostenlos … bis TT.MM.JJJJ"
    m = re.search(r"kostenlos\D{0,40}?bis\D{0,15}?(\d{1,2})\.(\d{1,2})\.(\d{4})", text, re.I)
    if m:
        try:
            res["stornofrist"] = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1))).date().isoformat()
        except ValueError:
            pass
    # (b) "X Tage vor Anreise/Check-in"  → checkin − X
    if not res["stornofrist"] and d_ci:
        m = re.search(r"(\d+)\s*Tag\D{0,30}?(?:vor)\D{0,30}?(?:Anreise|Check-?in)", text, re.I)
        if not m:  # auch umgekehrte Reihenfolge / nahe "stornier"/"kostenlos"
            win = re.search(r"(?:kostenlos|stornier)\w*(.{0,120})", text, re.I)
            if win:
                mm = re.search(r"(\d+)\s*Tag", win.group(1))
                if mm:
                    m = mm
        if m:
            res["stornofrist"] = (d_ci - timedelta(days=int(m.group(1)))).isoformat()

    # Ort: aus Adresse — zwei Layouts:
    #  (a) "PLZ , Stadt , Bundesland , Deutschland"  (Bestätigungs-Mail)
    #  (b) "Straße , Stadt , PLZ , Deutschland"       (aktualisierte Buchung)
    m = re.search(r"\b\d{4,5}\b\s*,\s*([A-Za-zäöüÄÖÜß.\- ]{2,40}?)\s*,\s*[A-Za-zäöüÄÖÜß.\- ]{3,40}\s*,\s*(?:Deutschland|Österreich|Schweiz)", text)
    if not m:
        m = re.search(r",\s*([A-Za-zäöüÄÖÜß.\- ]{2,40}?)\s*,\s*\d{4,5}\s*,\s*(?:Deutschland|Österreich|Schweiz)", text)
    if m:
        res["ort"] = m.group(1).strip()
    return res


def match_etappe(booking, etappen):
    """Findet die Etappe per Ortsabgleich (Stadt → Etappenname). None bei Mehrdeutig/keine."""
    cand = []
    ort = (booking.get("ort") or "").lower()
    hotel = (booking.get("hotel") or "").lower()
    for e in etappen:
        terms = [e["name"].lower()] + ALIASES.get(e["id"], [])
        hit = False
        for t in terms:
            # Etappenname/Alias kommt in der Stadt vor (Titisee ⊂ "Titisee-Neustadt")
            # oder die Stadt ist (Teil von) Name/Alias
            if ort and (t in ort or ort in t):
                hit = True; break
            if hotel and t in hotel:  # Notnagel: Ort steckt im Hotelnamen
                hit = True; break
        if hit:
            cand.append(e)
    uniq = {e["id"]: e for e in cand}
    return list(uniq.values())[0] if len(uniq) == 1 else None


# ───────────────────────── Hauptlauf ─────────────────────────
def main():
    st = json.loads(STATE.read_text()) if STATE.exists() else {"seen_mids": [], "bookings": []}
    seen_mids = set(st.get("seen_mids", []))
    # Dedup pro Aufenthalt (Ort+Check-in+Check-out) — Buchung kommt in mehreren Mails
    # mit unterschiedlichen Nummern, deshalb NICHT über die Nummer deduplizieren.
    def bkey(b):
        return f"{(b.get('ort') or '').lower()}|{b.get('checkin')}|{b.get('checkout')}"
    done_keys = {bkey(b) for b in st.get("bookings", [])}
    etappen = load_etappen()

    at = token()
    qs = urllib.parse.urlencode({"$top": "40", "$orderby": "receivedDateTime desc",
                                 "$select": "id,subject,from,receivedDateTime,body"})
    res = json.loads(urllib.request.urlopen(urllib.request.Request(
        "https://graph.microsoft.com/v1.0/me/messages?" + qs,
        headers={"Authorization": f"Bearer {at}"})).read())

    neu = 0
    for m in res.get("value", []):
        mid = m["id"]
        if mid in seen_mids:
            continue
        frm = (m.get("from", {}).get("emailAddress", {}).get("address", "") or "").lower()
        subj = m.get("subject") or ""
        if "booking.com" not in frm:
            continue
        text = html_to_text(m.get("body", {}).get("content", ""))
        b = parse_booking(subj, text)
        seen_mids.add(mid)
        if not b:
            continue
        if bkey(b) in done_keys:
            continue  # dieser Aufenthalt schon verarbeitet (mehrere Mails pro Buchung)
        done_keys.add(bkey(b))

        e = match_etappe(b, etappen)
        neu += 1
        if TEST:
            print(f"── {subj[:60]}")
            print(f"   Hotel:   {b['hotel']}\n   Ort:     {b['ort']}")
            print(f"   Check-in:{b['checkin']}  Check-out:{b['checkout']}  Storno:{b['stornofrist']}")
            print(f"   Buchung: {b['buchungsnr']}  →  Etappe: {e['name'] if e else '— NICHT zugeordnet —'}\n")

        if not e:
            tg(f"🏨 *Neue Booking-Buchung — konnte ich nicht zuordnen*\n\n"
               f"*{b['hotel'] or subj}*\n📍 {b['ort'] or '?'}\n"
               f"📅 {b['checkin']} → {b['checkout']}\n"
               f"⏰ Storno frei bis: {b['stornofrist'] or '?'}\n\n"
               f"_Bitte in MP → Reiseplaner manuell der richtigen Etappe zuordnen._ 🐾")
            st.setdefault("bookings", []).append({**b, "etappe": None})
            continue

        # Schon ein (anderes) Hotel an dieser Etappe? → nicht überschreiben, nur melden
        existing = ""
        rd = WS / "data" / "reise_notizen.json"
        if rd.exists():
            try:
                existing = (json.loads(rd.read_text()).get(e["id"], {}) or {}).get("unterkunft_name", "")
            except Exception:
                existing = ""
        if existing and existing.strip().lower() != (b["hotel"] or "").strip().lower():
            tg(f"⚠️ *Booking-Konflikt — Etappe {e['name']}*\n\n"
               f"Dort steht schon: *{existing}*\nNeue Buchung: *{b['hotel']}*\n"
               f"📅 {b['checkin']} → {b['checkout']}\n\n"
               f"_Ich habe nichts überschrieben — bitte in MP prüfen._ 🐾")
            st.setdefault("bookings", []).append({**b, "etappe": e["id"], "konflikt": True})
            continue

        # Eintragen + Storno-Kalender
        mc_post("/api/reise-notizen", {
            "id": e["id"], "unterkunft_name": b["hotel"],
            "checkin": b["checkin"], "checkout": b["checkout"],
            "stornofrist": b["stornofrist"]})
        cal = ""
        if b["stornofrist"]:
            r = mc_post("/api/reise-calendar-storno", {
                "station": e["name"], "unterkunft_name": b["hotel"], "stornofrist": b["stornofrist"]})
            cal = "📅 Storno im Kalender (Erinnerung 2 Tg. vorher)\n" if r.get("ok") else ""
        st.setdefault("bookings", []).append({**b, "etappe": e["id"]})
        tg(f"✅ *Buchung zugeordnet → Etappe {e['name']}*\n\n"
           f"🏨 *{b['hotel']}*\n📅 {b['checkin']} → {b['checkout']}\n"
           f"⏰ Storno frei bis: *{b['stornofrist'] or '—'}*\n{cal}\n"
           f"_Eingetragen im Reiseplaner._ 🐾")

    st["seen_mids"] = list(seen_mids)[-400:]
    if not TEST:
        STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    print(f"{neu} neue Buchung(en) verarbeitet." + (" [TEST]" if TEST else ""))


if __name__ == "__main__":
    main()
