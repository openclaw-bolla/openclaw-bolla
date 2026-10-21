# chrismandel.de Neubau — STAND (laufend aktualisieren)
STATUS: FERTIG (Startseite+Landing live, Chris 21.10.: "gut so, alles lassen"). Folgeseiten = spaeterer Schritt, in moin/offene_punkte p19
Quelle der Seite: /home/bolla/workspace/chrismandel-site/ (Backup: backups/chrismandel-site_vor_neubau_20261021)
Budget-Sperre: scripts/budget_guard.sh (Wochen-Verbrauch Mi 50 / Do 60 / Fr 70 %), zwischen Schritten pruefen.
## Auftrag (Chris 21.10.2026)
1. Startseite neu: Hero neutral ueber Chris, mit Bildern/Grafiken, spektakulaer+neugierig.
2. Kacheln bleiben, deutlich groesser: Titel zum konkreten Inhalt statt "70...", Screenshot + kurze Neugier-Erklaerung; kleine Kicker-Texte ueber dem Titel bleiben.
3. Unterseiten vorerst unveraendert.
4. Landing Page fuers AURORA-II-Video (QR-Code im Buch), hochladen (spaeter verbesserbar).
5. Impressum + Kontakt auf der Startseite. ALLES auch Englisch (check_en_parity.sh vor Deploy).
## Erledigt (21.10.)
- Neue Startseite DE+EN (Generator build_home.py): Nordlicht-Hero, Zahlen-Leiste, 3 große Kacheln mit Screenshots, Kontakt+Impressum
- Landing AURORA II /aurora2/ + /en/aurora2/ (build_aurora2.py, Video 20MB web, Poster)
- Kartenstapel (assets/cards.js) statt Kachelliste, Chris-Feedback 21.10.: sehr gut
- Parity-Check OK, LIVE seit 21.10. (wrangler --branch=main), Vorschau-Alias vorschau-neu.chrismandel.pages.dev
## Naechster Schritt
- Chris schaut Vorschau an, Feinschliff, dann Go-Live (wrangler --branch=main). Mobile-Check. Unterseiten spaeter.
- 21.10. abends: AURORA-II-Karte (Karte 1), Halbkreis-Fächer + Autoplay (assets/cards.js?v=3 — bei Änderungen v hochzählen in build_home.py!), alles LIVE, am Duo (adb 192.168.178.20:5555) geprüft.
- Offen: Unterseiten neu (2. Schritt), Song/Streaming-Link auf /aurora2/ sobald fertig.
- cards.js jetzt v=3: Wheel wrappt, Überlappung stärker (R=.64W, 28°)
