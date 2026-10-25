#!/usr/bin/env python3
"""Newsletter-Scanner: checkt Aldi Nord, Penny, Lidl, Edeka, Rewe, Famila auf Watchlist-Artikel."""
import json, os, re, subprocess, sys, urllib.request, urllib.parse
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent))

WORKSPACE      = os.environ.get("BOLLA_WORKSPACE", os.path.expanduser("~/workspace"))
WATCHLIST_FILE   = Path(WORKSPACE) / "config" / "newsletter_watchlist.json"
RESULTS_FILE     = Path(WORKSPACE) / "cache"  / "newsletter_results.json"
ALDI_OFFERS_FILE = Path(WORKSPACE) / "cache"  / "aldi_offers.json"

STORES = [
    {"name": "Aldi Nord", "color": "#1565C0", "text": "#fff",
     "senders": ["aldi-nord.de", "aldi.de", "aldi-nord.com"]},
    {"name": "Penny",     "color": "#e30613", "text": "#fff",
     "senders": ["penny.de", "newsletter.penny.de", "penny-markt.de"]},
    {"name": "Lidl",      "color": "#FFD100", "text": "#0050AA",
     "senders": ["newsletter.lidl.de", "lidl-newsletter.de", "lidl.de"]},
    {"name": "Edeka",     "color": "#e2001a", "text": "#fff",
     "senders": ["edeka.de", "newsletter.edeka.de", "edeka-minden-hannover.de", "mailing.edeka.de"]},
    {"name": "Rewe",      "color": "#cc0000", "text": "#fff",
     "senders": ["rewe.de", "newsletter.rewe.de", "mailing.rewe.de", "rewe-group.com"]},
    {"name": "Famila",    "color": "#e8000d", "text": "#fff",
     "senders": ["famila.de", "famila-nordost.de", "newsletter.famila.de", "famila-handelsmarkt.de"]},
]

# Transaktionsdomains (Shop-Systeme, keine Newsletter)
TRANSACTIONAL_SENDER_DOMAINS = [
    "lidl-shop.de", "aldi-onlineshop.de", "penny-shop.de",
    "orders.", "rechnung.", "noreply.", "no-reply.",
]

# Transaktionsbetreff — nur anwenden wenn Sender KEINE bekannte Newsletter-Domain ist
TRANSACTIONAL_SUBJECTS = [
    "rechnung", "bestellung", "bestelleingang", "bestellbestätigung",
    "lieferung", "sendungsverfolgung", "tracking", "zahlung",
    "passwort", "kontoerstellung", "registrier",
]

def strip_html(html):
    # Soft-Hyphens, Zero-Width-Chars, HTML-Entities entfernen
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL)
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', ' ', html)
    html = html.replace('­', '').replace('‌', '').replace('​', '')
    html = re.sub(r'&nbsp;', ' ', html)
    html = re.sub(r'&#\d+;', ' ', html)
    html = re.sub(r'&[a-z]+;', ' ', html)
    return re.sub(r'\s+', ' ', html).strip()

def is_transactional(sender, subject):
    s_low = sender.lower()
    # Bekannte Transaktionsdomains immer raus
    if any(d in s_low for d in TRANSACTIONAL_SENDER_DOMAINS):
        return True
    # Newsletter-Domains nie rausfiltern (egal was im Betreff steht)
    if any(d in s_low for d in ["newsletter.", "vorteil", "angebot", "prospekt", "info@"]):
        return False
    # Sonst Betreff prüfen
    return any(k in subject.lower() for k in TRANSACTIONAL_SUBJECTS)

def match_store(sender):
    s = sender.lower()
    for store in STORES:
        if any(k in s for k in store["senders"]):
            return store
    return None

def graph_get(path):
    from mission_control_api import get_token as _get
    token = _get()
    req = urllib.request.Request(
        f"https://graph.microsoft.com/v1.0{path}",
        headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

def fetch_outlook_newsletters(days=8):
    """Holt Angebots-Newsletter der letzten `days` Tage aus allen Outlook-Ordnern."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen, mails = set(), []
    for store in STORES:
        for sender_kw in store["senders"]:
            try:
                d = graph_get(f"/me/messages?$search=\"from:{sender_kw}\"&$top=10"
                              f"&$select=subject,from,receivedDateTime,body,id")
            except Exception as e:
                print(f"Outlook Fehler ({sender_kw}): {e}")
                continue
            for m in d.get("value", []):
                mid = m.get("id","")
                if mid in seen:
                    continue
                seen.add(mid)
                subj = m.get("subject","")
                sender_addr = m.get("from",{}).get("emailAddress",{}).get("address","")
                if is_transactional(sender_addr, subj):
                    print(f"  Überspringe Transaktionsmail: {subj[:50]}")
                    continue
                body_html = m.get("body", {}).get("content", "")
                body = strip_html(body_html)
                if len(body.strip()) < 50:
                    continue
                mails.append({
                    "store": store, "subject": subj,
                    "sender": m.get("from",{}).get("emailAddress",{}).get("address",""),
                    "date": m.get("receivedDateTime","")[:10],
                    "body": body[:5000],
                })
    return mails

def fetch_wtnet_newsletters(days=8):
    """Holt Angebots-Newsletter aus allen wtnet-Ordnern."""
    import imaplib, email as email_lib
    from email.header import decode_header
    mails = []
    try:
        cfg = json.loads(Path(WORKSPACE, "config/wtnet_account.json").read_text())
        imap = imaplib.IMAP4_SSL(cfg["imap_host"], cfg["imap_port"])
        imap.login(cfg["email"], cfg["password"])
        since = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")

        # Alle relevanten Ordner scannen
        scan_folders = ["INBOX", "Junk-E-Mail", "Spam"]
        for folder in scan_folders:
            try:
                rv, _ = imap.select(f'"{folder}"', readonly=True)
                if rv != "OK":
                    continue
            except Exception:
                continue
            _, data = imap.uid("search", None, f'SINCE {since}')
            uids = data[0].split()
            for uid in uids:
                try:
                    _, raw = imap.uid("fetch", uid, "(RFC822)")
                    msg = email_lib.message_from_bytes(raw[0][1])
                    from_raw = decode_header(msg.get("From",""))[0]
                    sender = (from_raw[0].decode(from_raw[1] or "utf-8", errors="replace")
                              if isinstance(from_raw[0], bytes) else from_raw[0]).lower()
                    store = match_store(sender)
                    if not store:
                        continue
                    subj_raw = decode_header(msg.get("Subject",""))[0]
                    subj = (subj_raw[0].decode(subj_raw[1] or "utf-8", errors="replace")
                            if isinstance(subj_raw[0], bytes) else subj_raw[0])
                    if is_transactional(sender, subj):
                        continue
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            ct = part.get_content_type()
                            if ct == "text/html":
                                body = strip_html(part.get_payload(decode=True).decode("utf-8", errors="replace"))
                                break
                            if ct == "text/plain" and not body:
                                body = part.get_payload(decode=True).decode("utf-8", errors="replace")
                    else:
                        body = strip_html(msg.get_payload(decode=True).decode("utf-8", errors="replace"))
                    if len(body.strip()) < 50:
                        continue
                    mails.append({"store": store, "subject": subj, "sender": sender,
                                  "date": msg.get("Date","")[:16], "body": body[:5000]})
                except Exception as e:
                    print(f"wtnet Mail-Fehler: {e}")
        imap.logout()
    except Exception as e:
        print(f"wtnet Fehler: {e}")
    return mails

def analyse_mail(mail, watchlist):
    """Lässt Claude Angebote aus dem Newsletter extrahieren."""
    if not watchlist:
        return []
    terms = ", ".join(watchlist)
    prompt = f"""Du analysierst einen Supermarkt-Newsletter auf bestimmte Artikel.

Store: {mail['store']['name']}
Betreff: {mail['subject']}
Datum: {mail['date']}

Newsletter-Inhalt:
{mail['body']}

Gesuchte Artikel (Suchbegriffe): {terms}

Prüfe ob einer dieser Begriffe oder inhaltlich ähnliche Artikel im Newsletter vorkommen (z.B. "Pilze" trifft auch "Champignons", "Waldpilze" etc.).

Antworte NUR mit einem JSON-Array. Für jeden Treffer ein Objekt:
[{{"artikel": "genauer Artikelname aus dem Prospekt", "preis": "z.B. 1,99 €", "gueltig_von": "TT.MM.", "gueltig_bis": "TT.MM.", "hinweis": "kurze Zusatzinfo oder leer"}}]

Wenn nichts gefunden: []
Kein Text außerhalb des JSON-Arrays."""
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, timeout=90)
        text = r.stdout.strip()
        print(f"  Claude Antwort: {text[:200]}")
        match = re.search(r'\[.*?\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except Exception as e:
        print(f"Claude Fehler: {e}")
        return []

def extract_aldi_offers(mail):
    """Lässt Claude ALLE Produkte (nicht nur Watchlist-Treffer) aus einem Aldi-Nord-Newsletter
    strukturiert extrahieren, damit sie in der Angebots-Suche durchsuchbar sind
    (Aldi taucht bei marktguru.de nicht auf — eigene Datenquelle nötig)."""
    prompt = f"""Du extrahierst ALLE beworbenen Produkte mit Preis aus einem Aldi-Nord-Newsletter für eine durchsuchbare Angebotsliste.

Betreff: {mail['subject']}
Datum: {mail['date']}

Newsletter-Inhalt:
{mail['body']}

Antworte NUR mit einem JSON-Array, ein Objekt pro Produkt:
[{{"name": "Produktname", "brand": "Marke falls erkennbar, sonst leer", "price": 1.99, "old_price": null, "valid_from": "TT.MM.", "valid_to": "TT.MM."}}]

Preise als Zahl mit Punkt (z.B. 2.49), kein Währungszeichen, kein Komma. "old_price" nur setzen wenn ein Streichpreis genannt wird, sonst null. Nur Produkte mit erkennbarem Preis aufnehmen. Kein Text außerhalb des JSON-Arrays."""
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, timeout=90)
        text = r.stdout.strip()
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except Exception as e:
        print(f"Claude Fehler (Aldi-Vollextraktion): {e}")
        return []

def update_aldi_offers_cache(mails):
    """Sucht die (neueste) Aldi-Nord-Mail unter den gefundenen Newslettern und extrahiert
    daraus die komplette Angebotsliste in cache/aldi_offers.json."""
    aldi_mails = [m for m in mails if m["store"]["name"] == "Aldi Nord"]
    if not aldi_mails:
        return
    aldi_mails.sort(key=lambda m: m["date"], reverse=True)
    newest = aldi_mails[0]
    print(f"Aldi-Vollextraktion: {newest['subject'][:55]}…")
    offers = extract_aldi_offers(newest)
    ALDI_OFFERS_FILE.write_text(json.dumps({
        "scanned_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "source_subject": newest["subject"],
        "source_date": newest["date"],
        "offers": offers,
    }, ensure_ascii=False, indent=2))
    print(f"Aldi-Cache aktualisiert: {len(offers)} Artikel.")

def run_scan():
    watchlist = json.loads(WATCHLIST_FILE.read_text()) if WATCHLIST_FILE.exists() else []
    mails = fetch_outlook_newsletters() + fetch_wtnet_newsletters()
    print(f"\n{len(mails)} Angebots-Newsletter gefunden:")
    for m in mails:
        print(f"  [{m['store']['name']}] {m['subject'][:55]}")

    update_aldi_offers_cache(mails)

    if not watchlist:
        print("Watchlist leer — kein Abgleich nötig.")
        results = []
    else:
        print(f"\nAnalysiere auf: {watchlist}\n")
        results = []
        for mail in mails:
            print(f"Prüfe: {mail['subject'][:50]}…")
            hits = analyse_mail(mail, watchlist)
            for h in hits:
                results.append({
                    "store":       mail["store"]["name"],
                    "color":       mail["store"]["color"],
                    "text_color":  mail["store"].get("text", "#fff"),
                    "artikel":     h.get("artikel", ""),
                    "preis":       h.get("preis", ""),
                    "gueltig_von": h.get("gueltig_von", ""),
                    "gueltig_bis": h.get("gueltig_bis", ""),
                    "hinweis":     h.get("hinweis", ""),
                    "mail_date":   mail["date"],
                    "subject":     mail["subject"],
                })
    RESULTS_FILE.write_text(json.dumps({
        "scanned_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "results": results
    }, ensure_ascii=False, indent=2))
    print(f"\nFertig — {len(results)} Treffer gespeichert.")

if __name__ == "__main__":
    run_scan()
