---
name: project-aurora-identifiers
description: "AURORA — Registry aller ISBNs & ASINs (eBook + Taschenbuch, DE + EN)"
metadata: 
  node_type: memory
  type: project
  originSessionId: af3a436d-4067-4c49-a60f-4262107e3296
---

# AURORA — ISBN- & ASIN-Registry

Kanonische Liste aller Identifikationsnummern. Bei jeder neuen Zuweisung hier ergänzen.

| Ausgabe | Typ | Nummer | Stand |
|---|---|---|---|
| **Taschenbuch Deutsch** | ISBN-13 (kostenlose KDP-ISBN) | **9798183595307** (979-8-18359-530-7) | zugewiesen 21.06.2026 |
| **Taschenbuch Englisch** | ISBN-13 (kostenlose KDP-ISBN) | **9798183599152** (979-8-18359-915-2) | zugewiesen 21.06.2026 |
| **Taschenbuch Deutsch** | ASIN | **B0H6JGRRTJ** | abgelesen 24.06.2026 (Status „Wird veröffentlicht") |
| **Taschenbuch Englisch** | ASIN | **B0H6JGNK89** | abgelesen 24.06.2026 (Status „Wird veröffentlicht") |
| **eBook Deutsch** | ASIN | **B0H6JD2KDJ** | 🟢 **LIVE** 24.06.2026 (4,99 €) |
| **eBook Englisch** | ASIN | **B0H6JQK6JQ** | 🟢 **LIVE** 24.06.2026 ($4.99) |
| **eBook Englisch (D2D)** | ISBN-13 | **9798233715327** · UBL books2read.com/u/4A9A6o | erfasst 21.06.2026 (oberer Eintrag in My Books) |
| **eBook Deutsch (D2D)** | ISBN-13 | **9798235162075** · UBL **books2read.com/u/bz0nwj** (mit „j" am Ende!) | erfasst 21.06.2026. **🐞→✅ 09.07.2026 aufgeklärt:** Der bisherige Eintrag `u/bz0nw` (ohne j) war schlicht falsch abgetippt/unvollständig — kein echtes D2D-Problem. Mit „j" liefert der Link HTTP 200 (verifiziert per curl). Store-Liste auf der UBL-Seite ist aber noch nicht aktuell (zeigt "Add additional Stores" statt Kauflinks), obwohl laut D2D-Dashboard eBook DE schon seit 04.07.2026 bei **Barnes & Noble + Rakuten Kobo live** ist — braucht nur einen "Rescan" auf books2read.com (Link Tools → UBL Dashboard). |
| **eBook Englisch @ Google Play (DIREKT)** | GGKEY | **RCD8HR2D4AE** (4,69 €) | 🟢 **LIVE**, bestätigt per Screenshot 12.07.2026 ("Online bei Google Play") — direkt im Google Play Books Partner Center hochgeladen (NICHT via D2D — D2D verteilt nicht an Google Play) |
| **eBook Deutsch @ Google Play (DIREKT)** | GGKEY | **68ES01N6JE2** (Ziel 4,99 €, alt 5,34 €) | 🟢 LIVE. Preis-Fix 12.07.2026 abgeschlossen: neue Preisregel EUR 4,99 auf Geltungsbereich **„ECZ" (Eurozone)** angelegt (die alte 5,34 €-Regel war offenbar ebenfalls Eurozone-scoped und hat die WORLD-Regel übersteuert — Länder-Einzelregel schlägt WORLD-Regel). Mehrfach gespeichert. Google braucht laut UI Minuten bis Stunden zur Neuberechnung der Länderpreise-Tabelle — Chris hat entschieden, das nicht weiter zu verfolgen/prüfen. **Projekt für Chris abgeschlossen.** |

**Hinweise:**
- 🟡 **IngramSpark (EN-Print) = GEPARKT & ÜBERWACHT, NICHT tot:** Verworfen wurde nur die Variante „jetzt 80 € für eine eigene ISBN kaufen" — IngramSparks Gratis-ISBN gibt es bislang **nur für US-Kunden** (DE-Kunde müsste eigene ISBN ~80 € kaufen, MVB/german-isbn.de; KDP-/D2D-ISBNs dort nicht nutzbar). Chris will aber **dranbleiben**: Wächter `scripts/ingramspark_isbn_watcher.py` (Cron `0 9 3 * *`, monatlich) prüft, ob Ingram die Gratis-ISBN für Nicht-US-Kunden öffnet (Sentinel „only available in the U.S. for now" verschwindet → Telegram-Alarm). **Sobald die Sperre fällt → EN-Taschenbuch kostenlos über Ingram in den echten Buchhandel** (über Amazon hinaus). Stand 29.06.2026: Sperre steht noch. ⚠️ Der Cron war beim Crontab-Unfall 24.06. rausgeflogen, am 29.06. wieder eingebaut + verifiziert. Ingram-Account 9944039 existiert (leer, kein Druckauftrag); 0,02 €-Abbuchung von „LIGHTNINGSRC/INGRAMSPA" = reine Karten-Verifizierung vom Account-Setup, harmlos. Bis dahin EN-Taschenbuch **nur über KDP/Amazon** live (D2D-Print war eh raus — Amazon nicht abwählbar).
- **ASIN** wird von Amazon erst bei tatsächlicher Veröffentlichung vergeben (Drafts haben oft noch keine). → nach dem Publish im Bücherregal ablesen und hier eintragen.
- Jede Sprache + jedes Format = eigene Nummer. Taschenbuch-ISBN ist fix mit Trim 5×8″ verknüpft.
- Strategie-Erklärdokument: `D:/OneDrive/Dokumente/AURORA/AURORA_ISBN_ASIN_Uebersicht.docx` — ⚠️ veraltet („nur eBook, kein eigener Print"): wir veröffentlichen jetzt DOCH Taschenbücher. Bei Gelegenheit aktualisieren.
- Siehe [[project-kdp-taschenbuch-anleitung]] · [[aktuell]].
