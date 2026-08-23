#!/usr/bin/env python3
"""Aldi-Nord-Prospekt-OCR: holt das komplette Wochensortiment aus dem Online-Blätterkatalog
(iPaper-Viewer), weil der Newsletter (newsletter_scanner.py) nur ~10-14 Highlight-Artikel
inline im Mailtext enthält, der Rest des Wochensortiments aber hinter "ZUM PROSPEKT" sitzt.

Quelle: __NEXT_DATA__-JSON auf aldi-nord.de/prospekte/aldi-aktuell.html enthält den aktuell
gültigen iPaper-Link (ändert sich wöchentlich, z.B. .../2026cw35mopromotionaldi-.../) — kein
Mail-Zugriff nötig, das __NEXT_DATA__-JSON ist serverseitig gerendert (plain HTTP GET reicht).

Bildzugriff auf iPaper (Image.ashx) braucht einen gültigen Referer-Header (Viewer-URL), sonst
404 (Hotlink-Schutz). Mit korrektem Referer liefert Image.ashx einen 302 auf eine signierte
CDN-URL (cdn.ipaper.io/.../Normal.jpg?token=...) — reines urllib reicht dafür aus, kein
Playwright/Browser nötig.

Pro Seiten-Batch lässt die Claude-CLI (Vision, gleiches Subprocess-Pattern wie
extract_aldi_offers() in newsletter_scanner.py) die Produkte strukturiert extrahieren.

Ergänzt cache/aldi_offers.json um die Vollsortiment-Artikel (source="prospekt"), ohne die
Newsletter-Highlights (source="newsletter", von newsletter_scanner.py geschrieben) zu
verdrängen — bei jedem Lauf werden nur die alten "prospekt"-Einträge ersetzt, "newsletter"-
Einträge bleiben unangetastet stehen. mission_control_api.py's _aldi_offer_hits() braucht
keine Anpassung, da sie offers[] generisch über .get() liest (zusätzliches "source"-Feld
stört nicht)."""
import json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
from datetime import datetime

WORKSPACE = os.environ.get("BOLLA_WORKSPACE", os.path.expanduser("~/workspace"))
ALDI_OFFERS_FILE = Path(WORKSPACE) / "cache" / "aldi_offers.json"
SCRATCH_DIR = Path(WORKSPACE) / "cache" / "aldi_prospekt_pages"
LANDING_URL = "https://www.aldi-nord.de/prospekte/aldi-aktuell.html"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
BATCH_SIZE = 4          # Seiten pro Claude-Vision-Aufruf (Kompromiss Laufzeit/Kosten vs. Genauigkeit)
CLAUDE_TIMEOUT = 180     # Sek. pro Batch-Aufruf (Vision braucht länger als reiner Text)


def fetch(url, referer=None):
    headers = {"User-Agent": UA}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def find_ipaper_slug():
    """Liest die aktuelle Aldi-Prospektseite und extrahiert Slug + Seitenzahl aus dem
    __NEXT_DATA__-JSON (dort steckt der wöchentlich wechselnde iPaper-Link)."""
    html = fetch(LANDING_URL).decode("utf-8", errors="replace")
    m = re.search(r'https://ipaper\.ipapercms\.dk/([a-zA-Z0-9/_-]+?)/Image\.ashx', html)
    if not m:
        raise RuntimeError("Kein iPaper-Link im __NEXT_DATA__ von aldi-aktuell.html gefunden — "
                            "Seitenstruktur hat sich vermutlich geändert.")
    slug = m.group(1)
    pages = [int(p) for p in re.findall(r'Image\.ashx\?PageNumber=(\d+)', html)]
    if not pages:
        raise RuntimeError("Keine Seitenzahlen im __NEXT_DATA__ gefunden.")
    page_count = max(pages)
    return slug, page_count


def download_pages(slug, page_count):
    """Lädt jede Katalogseite als JPEG. Braucht einen gültigen Referer (iPaper-Viewer-URL),
    sonst liefert Image.ashx nur einen 404 (Hotlink-Schutz)."""
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
    base = f"https://ipaper.ipapercms.dk/{slug}/"
    paths = []
    for n in range(1, page_count + 1):
        url = f"{base}Image.ashx?PageNumber={n}&ImageType=Normal"
        try:
            img = fetch(url, referer=base)
        except Exception as e:
            print(f"  Seite {n}: Download-Fehler ({e})")
            continue
        p = SCRATCH_DIR / f"page_{n:02d}.jpg"
        p.write_bytes(img)
        paths.append(p)
        print(f"  Seite {n}/{page_count} geladen ({len(img)} Bytes)")
    return paths


def extract_batch(paths):
    """Lässt Claude (Vision, gleiches CLI-Subprocess-Pattern wie extract_aldi_offers() in
    newsletter_scanner.py) alle Produkte aus einem Bild-Batch extrahieren."""
    file_list = "\n".join(f"- {p}" for p in paths)
    prompt = f"""Du extrahierst ALLE beworbenen Produkte mit Preis aus Seiten eines Aldi-Nord-Prospekts
für eine durchsuchbare Angebotsliste. Lies diese Bilddateien:
{file_list}

Antworte NUR mit einem JSON-Array, ein Objekt pro Produkt:
[{{"name": "Produktname", "brand": "Marke falls erkennbar, sonst leer", "price": 1.99, "old_price": null, "valid_from": "TT.MM.", "valid_to": "TT.MM.", "category": "grobe Kategorie falls erkennbar, sonst leer"}}]

Preise als Zahl mit Punkt (z.B. 2.49), kein Währungszeichen, kein Komma. "old_price" nur setzen wenn ein Streichpreis genannt wird, sonst null. Gültigkeitszeitraum wenn auf der Seite angegeben (sonst leer lassen). Nur Produkte mit erkennbarem Preis aufnehmen. Ignoriere reine Werbe-/App-/Rezeptseiten ohne Produktpreise. Kein Text außerhalb des JSON-Arrays."""
    try:
        r = subprocess.run(["claude", "-p", prompt], capture_output=True, text=True, timeout=CLAUDE_TIMEOUT)
        text = r.stdout.strip()
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        print(f"  Kein JSON in Claude-Antwort: {text[:200]}")
        return []
    except Exception as e:
        print(f"  Claude-Fehler (Batch {paths[0].name}..{paths[-1].name}): {e}")
        return []


def cleanup_pages(paths):
    for p in paths:
        try:
            p.unlink()
        except Exception:
            pass


def merge_into_cache(prospekt_offers, slug, page_count):
    existing = {}
    if ALDI_OFFERS_FILE.exists():
        try:
            existing = json.loads(ALDI_OFFERS_FILE.read_text())
        except Exception:
            existing = {}
    all_offers = existing.get("offers", [])
    before_count = len(all_offers)
    # Bestehende Newsletter-Highlights (source=="newsletter" bzw. noch kein "source"-Feld)
    # behalten, alte Prospekt-Treffer eines vorherigen Laufs dieser Woche ersetzen.
    kept = []
    for o in all_offers:
        if o.get("source") == "prospekt":
            continue
        o.setdefault("source", "newsletter")
        kept.append(o)
    for o in prospekt_offers:
        o["source"] = "prospekt"
    merged = kept + prospekt_offers
    payload = dict(existing)
    payload["offers"] = merged
    payload["prospekt_scanned_at"] = datetime.now().strftime("%d.%m.%Y %H:%M")
    payload["prospekt_slug"] = slug
    payload["prospekt_pages"] = page_count
    if "scanned_at" not in payload:
        payload["scanned_at"] = payload["prospekt_scanned_at"]
    ALDI_OFFERS_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return before_count, len(merged)


def run():
    print(f"Aldi-Prospekt-OCR gestartet — {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    slug, page_count = find_ipaper_slug()
    print(f"Aktueller Prospekt: {slug} ({page_count} Seiten)")
    paths = download_pages(slug, page_count)
    if not paths:
        print("Keine Seiten geladen — Abbruch, Cache bleibt unangetastet.")
        return
    all_offers = []
    for i in range(0, len(paths), BATCH_SIZE):
        batch = paths[i:i + BATCH_SIZE]
        print(f"Extrahiere Batch {i // BATCH_SIZE + 1} ({len(batch)} Seiten)…")
        offers = extract_batch(batch)
        print(f"  -> {len(offers)} Artikel gefunden.")
        all_offers.extend(offers)
        time.sleep(2)
    before, after = merge_into_cache(all_offers, slug, page_count)
    cleanup_pages(paths)
    print(f"\nFertig — Prospekt-Artikel gesamt: {len(all_offers)}. "
          f"Cache vorher: {before} -> nachher: {after} Artikel.")


if __name__ == "__main__":
    run()
