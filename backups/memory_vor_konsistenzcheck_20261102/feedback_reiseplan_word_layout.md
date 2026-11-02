---
name: feedback-reiseplan-word-layout
description: Finales Seiten-Layout für Word-Reisepläne (reise_sightseeing_docx) — Vorlage für künftige Routenplanungen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 813902cf-a4a5-48f4-aad8-c5f5b904f5ec
---

Finales, von Chris abgenommenes Seitenlayout für Word-Reisepläne (Stand 08.07.2026, nach mehreren Feedback-Runden + eigener manueller Nachbesserung von Chris in Word). Bei einer künftigen neuen Routenplanung dieses Layout 1:1 übernehmen, nicht neu erfinden.

**Aufbau (Funktion `reise_sightseeing_docx()` in `scripts/mission_control_api.py`):**
1. **Seite 1:** Titel + Übersichtskarte (durchgezogene Route, Marker mit Datums-Tooltip, Legende oben links) + Eckdaten-Zeile (Start/Ziel/Übernachtungen/km) + Google-Maps-Gesamtlink.
2. **Seite 2:** „📅 Tagesübersicht"-Tabelle — eine Zeile pro Reisetag mit Vormittag/Nachmittag/Abend/Übernachtungsort, unabhängig von den Detailseiten (`_reise_tagesuebersicht_rows()`).
3. **Ab Seite 3: jeder einzelne Reisetag bekommt seine eigene neue Seite — ausnahmslos**, auch Standquartier-Fortsetzungstage (z.B. Tag 5+6 in Freiburg, obwohl gleiche Übernachtungs-Basis wie Tag 4). Kein Zusammenlegen mehrtägiger Standquartiere mehr auf einer Seite, auch wenn das in einer früheren Runde (Round 6) mal anders beschlossen war — diese Version ist überholt.

**Wichtige Detail-Lehre (Bug, der zum jetzigen Stand führte):** Ein Zwischenstand hatte den Seitenumbruch nur beim *Wechsel der Übernachtungs-Station* ausgelöst (nicht pro Tag) — das brach bei Tagen mit Tagesausflug + neuer Übernachtung (z.B. Tag 8: Mainau tagsüber, Übernachtung erst in Meersburg) mittendrin, sodass die Tagesüberschrift + der erste Stopp noch auf der Vorseite hingen. Endgültige Lösung: Umbruch bedingungslos vor jede Tagesüberschrift (außer vor Tag 1), unabhängig von Basiswechsel oder Standquartier-Status.

**Pro Tagesseite:** Fahrt-Info (km/Zeit/Etappen/Fähre), je Station: Name+Uhrzeit, Anfahrt, Beschreibung, 💡 Tipp, Sehenswürdigkeiten & Highlights (mit `hlInfo`-Zusatztext + 🅿️-Parkhinweis je Highlight). Freie Standquartier-Tage ohne eigene Station zeigen „🏡 [Ort] — Standquartier" + `tagesplan`-Einträge (halbtags-genau) oder einen generischen Hinweistext.

**Datenquelle:** `SR_ROUTE`-Array in `mission-control/index.html`, geparst über `_reise_stationen_full()` — Frontend bleibt einzige Datenquelle, kein Drift zur Karte.

## Update 08.07.2026 — zwei weitere Bugs gefunden + gefixt, für jede künftige Routenplanung verbindlich:

**1. Seitenformat A4, nicht Letter.** `Document()` von python-docx setzt standardmäßig US-Letter (21,59×27,94cm), nicht A4 (21×29,7cm) — ca. 1,8cm weniger Höhe pro Seite. Immer explizit setzen:
```python
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
```

**2. Nie `doc.add_page_break()` vor eine Überschrift setzen — immer `paragraph_format.page_break_before = True` auf der Überschrift selbst.** Ein hartes Umbruchzeichen (`add_page_break()`) erzwingt *immer* einen Seitenwechsel, auch wenn der Vortext schon exakt bis zum unteren Rand reicht — dann entsteht eine komplett leere Zwischenseite (live mit Word-COM verifiziert: Seite war da, 0 sichtbarer Inhalt). Die Absatz-Eigenschaft `page_break_before` ist dagegen ein Zustand („diese Überschrift startet immer eine neue Seite") und verdoppelt sich nie, egal wo der Vortext endet. Gilt für alle drei Break-Stellen in `reise_sightseeing_docx()`: Tagesübersicht-Überschrift, jede Tagesüberschrift, Freiburg-Sonderumbruch bei Standquartier-Fortsetzung.

**3. Hotel-Adresse: Position hängt davon ab, WANN eingecheckt wird, nicht nur ob übernachtet wird.**
- **Oben direkt unter dem Stationsnamen** (`hotel_oben = True`): wenn dort *sofort bei Ankunft* eingecheckt wird — insbesondere Standquartiere mit Tagesausflügen von dort aus (z.B. Baden-Baden, Freiburg als 3-Nächte-Basis für Kaiserstuhl/Schlossberg-Ausflüge). Chris' Formulierung: „außer von da aus gibt es Tagestrips" = genau diese Fälle bleiben oben.
- **Unten am Ende des Stationsblocks** (nach Sehenswürdigkeiten/Öffnungszeiten-Link): wenn erst *abends nach der Besichtigung* eingecheckt wird (Freudenstadt, Titisee, Konstanz, Meersburg, Lindau bei dieser Reise) — die Chronologie im Dokument soll der echten Chronologie des Tages entsprechen.
- Implementiert über eine kleine `_hotel_block()`-Hilfsfunktion + Liste der "oben"-Stations-IDs, an zwei Stellen im Stations-Loop aufgerufen (vor Anfahrt-Absatz bzw. nach infoUrl-Absatz).
- **Faustregel für die nächste Reise:** pro Übernachtungsstation selbst festlegen (nicht raten) ob Ankunft=Einchecken oder Ankunft=erst losziehen-dann-einchecken, und danach die Position wählen.

**Verifikations-Workflow, der sich bewährt hat (nutzen bei jedem künftigen Layout-Zweifel):** docx über die POST-API generieren, per WSL nach `/mnt/d/OneDrive/Desktop/_bolla_temp/` kopieren, mit `powershell.exe` + Word-COM (`New-Object -ComObject Word.Application`, `$doc.GoTo(wdGoToPage,...)`) Seite für Seite den tatsächlichen Text auslesen — das zeigt echte Seitenumbrüche/leere Seiten, die aus der reinen XML-Struktur (python-docx `paragraphs`) nicht zuverlässig erkennbar sind. Testdatei danach vom Desktop löschen (Cleanup).

Siehe auch [[project_reise_sommer2026]] (falls vorhanden) für den konkreten Trip-Stand.
