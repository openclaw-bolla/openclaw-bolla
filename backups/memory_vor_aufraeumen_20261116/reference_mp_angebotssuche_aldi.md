---
name: reference-mp-angebotssuche-aldi
description: Wie die MP-Angebots-Suche funktioniert und warum/wie Aldi Nord eingebunden ist
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4465bb22-107a-4503-92ab-1a3be6aea3ba
  modified: 2026-08-23T18:01:57.981Z
---

# MP Angebots-Suche (🛒-Karte) — Aufbau

Die Live-Suche in MP (`mission-control/index.html`, "ANGEBOTE PANEL") läuft über die marktguru.de-API
(`offers_search()` in `mission_control_api.py`, Endpoint `/api/offers/search`).

## Aldi Nord fehlt bei marktguru — echte externe Grenze
marktguru.de führt **keine** Aldi-Daten (verifiziert 22.08.2026: 0 Treffer selbst bei direkter Suche nach
"aldi"). Aldi macht bei Drittanbieter-Prospektportalen traditionell nicht mit (eigene App/Website statt
Syndizierung). Keine API-Einstellung o.ä. kann das beheben — bevor ich das nochmal als "Bug" recherchiere:
das ist marktguru-seitig so, geprüft und bestätigt.

## Lösung: eigener Aldi-Kanal über Newsletter
`newsletter_scanner.py` (Cron Mo 5 Uhr) hat Aldi Nord schon lange in seiner `STORES`-Liste (Watchlist-Check).
Seit 22.08.2026 zusätzlich: `update_aldi_offers_cache()` extrahiert bei jedem Scan ALLE Artikel (nicht nur
Watchlist-Treffer) aus der neuesten Aldi-Mail strukturiert per Claude → `cache/aldi_offers.json`.
`offers_search()` merged diese lokalen Treffer mit marktguru (Aldi-Slots werden vorher reserviert, damit
sie nicht durch marktguru-Fülle verdrängt werden).

⚠️ **Root Cause gefunden (22.08.2026):** Aldi-Mail kam durchaus regelmäßig (vermutlich Sa.), wurde aber
von Chris vor dem nächsten Mo.-Scan bereits unwiderruflich gelöscht (Papierkorb praktisch leer, nur 4 Mails
insgesamt). Kein Timing-Problem, sondern "Mail existiert nicht mehr"-Problem.

**⚠️ Microsoft-Graph-Limit bei privaten Outlook.de/Hotmail-Konten:** Mail-Regeln (`/me/mailFolders/inbox/
messageRules`) sind per API **nur bei Firmenkonten (Exchange Online) verfügbar, nicht bei Consumer/MSA-
Konten** — direkt getestet, `AccessDenied` trotz vollem `MailboxSettings.ReadWrite`-Scope. Bevor ich das
nochmal als lösbar recherchiere: echte Plattform-Grenze, nicht scope-bedingt.

**Workaround:** `aldi_mail_archiver.py` (Cron alle 2h, `0 */2 * * *`) verschiebt Aldi-Nord-Mails per
Graph-API-Move sofort in den neuen Ordner `Ablage/Archiv/Angebote`, bevor Chris sie löschen kann.
`newsletter_scanner.py` braucht dafür keine Anpassung (durchsucht per `$search` ohnehin die ganze Mailbox).

## ⚠️ Newsletter-Extraktion erfasst nur ~10-14 "Highlight"-Artikel, nicht das Wochensortiment (23.08.2026)

Live an den beiden echten Aldi-Mails vom 23.08.2026 geprüft: Die Newsletter selbst zeigen nur eine Handvoll
handverlesener "Highlight"-Produkte pro Kategorie (Frische, Garten, Putzen, Küche, Kindermode, Pflanzen,
Food) inline im Mailtext — der Rest sitzt hinter "ZUM PROSPEKT"-Buttons. `extract_aldi_offers()` (s.o.)
extrahiert deshalb strukturell nur diese Teilmenge, nie das komplette Wochenangebot (Aldi hat üblicherweise
50-100+ Artikel/Woche).

**Prospekt-Link-Kette nachverfolgt (23.08.2026):**
1. "ZUM PROSPEKT" → Salesforce-Marketing-Cloud-Tracking-Link (`click.info.aldi-nord.de/?qs=...`)
2. → redirected auf `https://www.aldi-nord.de/prospekte/aldi-aktuell.html` (Next.js-App, `__NEXT_DATA__`
   JSON im Seiten-HTML — grundsätzlich ohne Headless-Browser lesbar)
3. → `pageProps.apiData` enthält aber nur einen `LEAFLET_IPAPER_STRUCTURE_GET`-Verweis auf
   `magazine.aldi-nord.de/.../` — das ist ein **iPaper-Blätterkatalog** (`ipapercms.dk`/`ipaper.io`,
   `Frontend-Desktop`-JS-Bundle)
4. → Die "Seiten" sind **gerenderte Bild-Dateien** (`Image.ashx?PageNumber=N&ImageType=Normal`, ~16 Seiten
   pro Woche), **keine strukturierten Produktdaten**. Direkter Zugriff auf `Image.ashx` ohne Referer/Session
   liefert 404 (Hotlink-Schutz). Ein paar schnelle Rateversuche auf mögliche iPaper-Hotspot-APIs
   (`ipapercms.dk/api/publication/{guid}`, `services.ipaper.io/api/v1/publications/{guid}`) liefen ins
   Leere (500/keine Verbindung) — kein öffentlich dokumentiertes API-Muster gefunden in der Kürze.

**Fazit: echte Sackgasse für "einfaches" Scraping.** Um das Wochensortiment vollständig zu bekommen, bräuchte
es OCR über die ~16 Katalogbilder pro Woche (Bildanalyse à la [[project_foto_analyse]]/Vision-Modell) statt
simplem HTML/JSON-Parsing — spürbar aufwendiger, fehleranfälliger (Preise/Mengen aus Bildern lesen) und
pro Woche neu zu wiederholen (neue Bild-URLs, neue Aldi-Woche = `2026cw35...` ändert sich). **Nicht als
Quick-Fix umgesetzt (23.08.2026 abends per Fork geprüft und bewusst gestoppt statt einer unzuverlässigen
Notlösung) — falls Chris das trotzdem will, wäre der nächste Schritt ein Vision-Modell-Durchlauf über die
16 Seitenbilder pro Woche, kein reiner Scraper.** Bis dahin bleibt `cache/aldi_offers.json` bei den
~10-14 Highlight-Artikeln pro Newsletter-Mail (2/Woche = ~2 Mails × 10-14 Artikel).

Siehe auch [[reference_mc]], [[reference_graph_capabilities]].
