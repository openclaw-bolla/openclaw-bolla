---
name: project_schuljahr2627
description: "Schuljahresplanung 26/27 (EDV 7. Klassen) — Neustart 09.07.2026, alter Planungsstand verworfen"
metadata: 
  node_type: memory
  type: project
  originSessionId: 47e07272-fb01-4f44-b399-3529be9e3377
  modified: 2026-08-12T15:45:31.261Z
---

## Hardware-Ausstattung
Siehe [[reference_edv_klassenausstattung]] — Lenovo Mini-PCs (kein Office) + optional HP-Laptops Win10 (Office) aus Laptop-Schrank, Zwei-Geräte-Modell je nach Thema.

## ⚠️ Vorkenntnisse der 7. Klassen (Chris-Einschätzung 09.07.2026)
Chris schätzt, dass **ca. 60% der Schüler noch sehr wenig Computer-Erfahrung** haben (kein Rechtsklick-Routine, keine Ordnerstruktur-Praxis o.ä.). Wichtig für **alle** Materialien fürs Schuljahr 26/27 (Anleitungen, Praktika, Folien-Tempo): Schritte kleinteilig und sehr explizit formulieren (z.B. "Rechtsklick = rechte Maustaste, nicht links" ausschreiben, nicht voraussetzen), nicht zu viel auf einmal, Grundbegriffe wie Doppelklick/Adressleiste nicht als bekannt voraussetzen. Erste Praktikum-Version (1-Praktikum.txt) war dafür noch zu knapp/vorausgesetzt-technikaffin, wurde überarbeitet.

**⚠️ Zweiter Rückfall 12.08.2026 — Regel gilt für JEDE neue Datei, nicht nur Praktika:** Die erste Version
von `02-Fenster-Anleitung.html` (Fenster/Tabs bedienen) war trotz dieser Regel wieder zu knapp — Begriffe
wie "Fenster", "Tab", die drei Symbole oben rechts wurden vorausgesetzt statt erklärt. Chris korrigierte:
explizit erklären was ein Fenster/Tab überhaupt IST (mit einfachem Vergleich, z.B. Papier auf dem Schreibtisch),
jedes Symbol einzeln beschreiben ("sieht aus wie...", "meist rot beim Draufzeigen"), Rechtsklick wieder
ausschreiben. **Konsequenz:** vor JEDER neuen Anleitungs-/Praktikums-Datei diese Regel aktiv nochmal
durchgehen, nicht nur beim allerersten Entwurf — die Gefahr ist, beim zweiten/dritten Mal wieder in
technikaffines Schreiben zurückzufallen, sobald ein Thema selbst simpel erscheint.

## Stand 09.07.2026
Chris startet die Planung für 26/27 komplett neu — alle vorherigen Annahmen/offenen Punkte aus früheren Sessions sind verworfen. Bekannt ist nur:

- **Alle Dateien liegen unter** `D:\OneDrive\Dokumente\Office\7. Klassen` (WSL: `/mnt/d/OneDrive/Dokumente/Office/7. Klassen`).
- ⚠️ Der Ordner `7d/` enthält aktuell nur eine Kopie von `7c/` — keine echten 7d-Daten, nicht als Quelle nutzen.

Details zur Ordnerstruktur (Module, Orga, Klassenordner etc.) bei Bedarf frisch mit `ls`/Explorer erheben statt aus alten Notizen zu übernehmen — die können veraltet/falsch sein.

## Themenliste → Termine verteilt (09.07.2026, von Chris korrigiert)
Aus `Themenliste 7er Kurs.docx` extrahiert und mit Chris abgeglichen: **19 Themen** (nicht 20 — Tag 0-Begrüßung + 1-Intro Klassenstufe 7 + 1-The Basics Grundbegriffe-I zählen zusammen als EIN Starttermin; Tag 7 inkl. Zusatzdatei „4 Schritte" ebenfalls ein Termin). `module_vorjahr` in `data/schuljahr2627.json` enthält jetzt diese 19er-Liste.

`termine[]` hat 8 unabhängige Stränge nach (Wochentag, Zeit, Gruppe I/II), Themen sequenziell nach Datum verteilt (`thema`/`bezeichnung`):
- **Gruppe I** (20 Termine/Strang): 19 Themen belegt, **letzter Termin bleibt offen/Reserve** (so von Chris bestätigt).
- **Gruppe II** (19 Termine/Strang): alle 19 Termine komplett belegt, endet exakt mit Excel.

## ⚠️ I/II-Rhythmus ist REAL und bewusst so gewollt (von Chris bestätigt 09.07.2026)
Der 4-Wochen-Block-Wechsel zwischen Gruppe I und Gruppe II (Klasse wird für den Kurs **halbiert**, jede Hälfte kommt abwechselnd 4 Wochen am Stück) ist **kein Datenmüll**, sondern **soll genauso ablaufen wie im Vorjahr**. Wichtig für spätere Kalendereinträge/Outlook-Kategorien — nicht wieder in Frage stellen, als gegeben behandeln.

## itslearning: Plan in Übersicht anheften
Siehe [[reference_itslearning_plan_anheften]] — Pin sitzt in der Plan-Detailansicht (⋯-Menü), nicht auf der Themen-Listenseite. Bei 7d fehlte er anfangs, war die Ursache für „Plan erscheint nicht in Übersicht".

## 📄→💻 Papierlos-Ziel 26/27 + didaktisches Grundkonzept (13.07.2026)
Chris will dieses Schuljahr **konsequent papierlos** unterrichten — in den Vorjahren "tonnenweise Papier" verbraucht. Aktuelles Konzept:
- **Content-Vermittlung:** Chris zeigt den Stoff per PPT/Beamer, stellt die Datei den Schülern als **PDF** zur Verfügung (später zusätzlich als **PPTX**, sobald sie im Curriculum bei PowerPoint angekommen sind — Module 7-17, siehe [[user_chris_teacher]]).
- **Praktikum (eigenständige Übung):** aktuell als **.txt**-Anleitung über itslearning zum Download, Schüler haben die txt während der Übung parallel zur eigentlichen Aufgabe offen (zweites Fenster oder zweites Gerät).
- **Geräte-Rollenverteilung:** siehe [[reference_edv_klassenausstattung]] — Zwei-Geräte-Modell (Lenovo=Doing, HP=Lesen bei Non-Office-Themen) ist von Chris bereits am 09.07.2026 bewusst entschieden, Papier-Alternative dort schon explizit abgelehnt.

**Bollas Einschätzung zu .txt vs. Alternative (13.07.2026, gefragt "ist txt gut lesbar oder anderer Vorschlag"):**
.txt ist grundsätzlich machbar (öffnet überall ohne Office, passt zum Zwei-Geräte-Modell), aber für die Zielgruppe (12-13-Jährige, ca. 60% wenig Vorerfahrung, siehe oben) visuell zu flach — keine Fett-/Farbmarkierung für "wichtig"-Stellen, keine optische Gliederung, und Windows-10-Notepad auf den HP-Laptops hat keine Tabs (mehrere offene .txt-Anleitungen unübersichtlich). Empfehlung: **einfache, in sich geschlossene HTML-Datei** statt .txt — läuft genauso ohne Installation/Office überall wo ein Browser ist (Edge ist eh für Copilot nötig), erlaubt aber Überschriften/Fettdruck/Farb-Hervorhebung/Icons/nummerierte Schritte, bleibt genauso einfach über itslearning verteilbar. Passt zu Chris' bestehender Präferenz "einfach verteilbare HTML-Dateien ohne Installation" ([[user_chris_teacher]]). Ergänzend prüfenswert: ob itslearning die Aufgabenbeschreibung direkt als Rich-Text im Aufgaben-Tab anbietet — dann bräuchte es gar keine separate Datei zum Runterladen mehr. **Noch nicht umgesetzt, nur Empfehlung — Chris entscheidet.**

**Ergänzung 13.07.2026 (gleicher Tag):** Chris will bewusst, dass Schüler die Praktikums-Datei selbst herunterladen und auf ihren **Stick speichern** (zusätzliche Dateiverwaltungs-Übung, nicht nur die spätere Arbeitsergebnisse). Passt gut zusammen: HTML-Datei vom Stick aus im Browser öffnen funktioniert technisch problemlos (reines `file://`-Rendering, kein Server/Internet nötig), solange die Datei in sich geschlossen ist (keine externen Bild-/Font-/Script-Links). RTF wurde als Alternative verworfen (offline zwar ohne Office nutzbar, aber genauso interaktionsarm wie .txt).
**Erledigt (13.07.2026, Chris hat live getestet): itslearning-Upload von .html funktioniert.** Kein Blocker mehr für den HTML-Weg — das Zwei-Geräte-/Papierlos-Konzept mit HTML-Anleitungen kann wie geplant weiterverfolgt werden.

**Interaktivität in der HTML-Datei — Klick-Quiz ja, Textfelder mit Speicherung nein (jedenfalls nicht direkt):**
- Multiple-Choice-Klick mit Sofort-Feedback ("Richtig!"/"Nochmal versuchen"): geht komplett offline ohne Server, easy umsetzbar.
- Ausfüllbare Textfelder: Tippen geht, aber eine lokal geöffnete HTML-Seite (`file://`) kann Eingaben NICHT dauerhaft speichern (Browser verweigern Zurückschreiben in die Datei aus Sicherheitsgründen; schließt man den Tab, ist der Text weg).
- Für "nur Selbstkontrolle" kein Problem (keine Speicherung nötig). Für "Ergebnis soll bei Chris landen/bewertet werden": entweder (a) ein Drucken-Knopf (`window.print()`) einbauen, der die ausgefüllte Seite als PDF sichert — Schüler speichert das PDF dann wieder aufs Stick (schöner Bonus: nochmal Datei-Workflow-Übung), oder (b) itslearnings eigenes natives Test-/Quiz-Werkzeug nutzen falls vorhanden (serverseitige Auswertung ist dafür architektonisch der richtigere Weg als eine gebastelte HTML-Seite).

## Handouts-Ordner: Workflow pro Unterrichtstag (Chris, 22.07.2026)

Für jeden der **19 Unterrichtstage** gibt es aus dem Vorjahr eine PPTX, die Chris für sehr gut hält und
wiederverwenden will — vor jedem Tag aber noch anpasst/kürzt (Ziel: mehr Praktikumsanteil, weniger Folien).
Alle Dateien liegen gemeinsam in **`D:\OneDrive\Dokumente\Office\7. Klassen\Handouts`** (WSL:
`/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts`), mit `NN-Thema.pptx`-Namensmuster (NN =
**zweistellige** Kurstag-Ziffer) befüllt.

**Bewusste Entscheidung: EIN gemeinsamer Ordner, kein Ordner pro Tag.** Der Ordner wird sich durch PDF +
HTML pro Tag zusätzlich "aufblähen" (bis zu ~57 Dateien bei 19 Tagen × 3 Dateitypen) — das ist in Ordnung.
**Elementar dafür:** JEDE Datei zu einem Tag beginnt mit derselben Kurstag-Ziffer (`NN-...`), das ist die
einzige Organisationsstruktur, kein Unterordner.

**⚠️ Korrektur 11.08.2026 — EINE Ausnahme von "kein Unterordner":** Chris fand den Ordner bei wachsender
Kurstag-Zahl doch zu unübersichtlich. Trennung jetzt nach **wer die Datei braucht**, nicht nach Dateityp:
- **`Handouts/` (flach, weiterhin kein Tag-Unterordner):** nur noch die `NN-Thema.pptx`-Arbeitsdateien, die
  Chris selbst bearbeitet/präsentiert.
- **`Handouts/Praktikum/`:** alles, was an die Schüler geht — `NN-Praktikum.html`, das `NN-....pdf`
  UND ALLE `NN-...-Anleitung.html`-Dateien (Chris' explizite Korrektur: "die pdfs gehören da auch rein",
  am 12.08.2026 auf alle Anleitungen erweitert). `01-Editor-Anleitung.html` und `02-Fenster-Anleitung.html`
  liegen seit 12.08.2026 dort, nicht mehr im Top-Level. **Dauerhafte Regel ab jetzt:** jede neue
  Anleitungs-Datei kommt direkt nach `Handouts/Praktikum/`, nicht mehr ins Top-Level, keine Rückfrage
  mehr nötig.

**Wichtig:** `itslearning_post_kurstag.py`s `discover_files()` wurde entsprechend angepasst (durchsucht seit
11.08.2026 sowohl `Handouts/` als auch `Handouts/Praktikum/` nach `NN-*.html`/`NN-*.pdf`, unabhängig vom
Dateityp) — beim nächsten Kurstag-Bau also **PDF + Praktikum-HTML beide direkt in `Handouts/Praktikum/`**
ablegen/exportieren, nur die PPTX bleibt in `Handouts/`.

**⚠️ Präfix IMMER zweistellig mit führender Null (`00-`, `01-` … `19-`), nie `0-`/`1-` einstellig.**
Grund (22.07.2026 entdeckt + behoben): Windows/Explorer sortiert Dateinamen alphabetisch, nicht numerisch —
einstellige Präfixe rissen die Reihenfolge auseinander (`10-...` landete direkt hinter `1-...` und vor
`2-...`). Alle 14 betroffenen Bestandsdateien (Tage 0–9) wurden umbenannt, Tage 10-19 waren schon
zweistellig. Bei jedem neuen Tag/jeder neuen Datei (PPTX, PDF, HTML) dieses Schema fortführen.

**Pro Tag entstehen bis zu drei Dateien, sobald Chris die PPTX fertig bearbeitet hat:**
1. `NN-Thema.pptx` — die von Chris überarbeitete Foliensammlung (Quelle/Ausgangspunkt)
2. `NN-Thema.pdf` — **auf Chris' aktiven Anstoß** aus der fertigen PPTX exportiert, geht bis zum
   PowerPoint-Kursteil (Module 7-17) als Download nach itslearning statt der PPTX selbst
3. `NN-Praktikum.html` — **ebenfalls auf Chris' aktiven Anstoß**, nach dem etablierten Muster aus
   [[feedback_prakt_anleitungen]] (Inhalt aus der zugehörigen PPTX destilliert, nicht frei erfunden)

Beide Trigger (PDF-Export, Praktikum-HTML) laufen **nicht automatisch** — Chris stößt sie im Chat aktiv an,
sobald der jeweilige Tag fertig ist. **⚠️ PDF-Export dabei NIE vorab nachfragen (Chris-Korrektur
22.07.2026 abends):** einfach im Handouts-Ordner nachschauen, ob die passende `NN-Thema.pdf` zur aktuellen
`NN-Thema.pptx` schon existiert (und aktuell ist) — falls nicht, direkt erzeugen, ohne zu fragen. Gilt
dauerhaft, nicht nur einmalig.

**✅ PDF-Export-Standardmethode (seit 22.07.2026 Nacht): PowerPoint-COM via PowerShell, NICHT LibreOffice.**
LibreOffice headless (`soffice.exe --headless --convert-to pdf`) erzeugte "grauenhafte" Qualität — Chris
hatte manuell mit "Microsoft Print to PDF" (Windows-Druckertreiber) immer bessere Ergebnisse. Getestete und
von Chris **freigegebene** Alternative: PowerShell + COM-Automatisierung von PowerPoint selbst
(`New-Object -ComObject PowerPoint.Application` → `$pres.SaveAs($pdfPath, 32)`, 32 = `ppSaveAsPDF`).
Sieht laut Chris "super aus" — das ist jetzt die Standardmethode für alle künftigen Handouts-PDFs.
⚠️ `ExportAsFixedFormat($pdfPath, 2)` scheitert an einem COM-Typkonvertierungsfehler (int→Object) — SaveAs
mit dem PDF-Format-Code ist der einzige verlaesslich funktionierende Weg.

**Fertiges, dauerhaftes Skript:** `/home/bolla/workspace/scripts/pptx_to_pdf.ps1` (Parameter `-PptxPath`,
`-PdfPath`), Aufruf von WSL aus z.B.:
```
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -ExecutionPolicy Bypass -File "$(wslpath -w /home/bolla/workspace/scripts/pptx_to_pdf.ps1)" -PptxPath "D:\...\NN-Thema.pptx" -PdfPath "D:\...\NN-Thema.pdf"
```
Pfade müssen als Windows-Pfade (`D:\...`) übergeben werden, nicht als WSL-Pfade (`/mnt/d/...`) — PowerPoint
läuft nativ unter Windows. `wslpath -w` wandelt nur den Skript-Pfad selbst um, die Parameter-Pfade müssen
manuell in Windows-Notation übergeben werden.

**Tag 1 = Ausnahme, bereits erledigt:** Läuft anders als die übrigen 18 Tage (viele Vorbesprechungen zu
Schuljahresbeginn integriert, siehe die 0-/1-Dateien im Ordner). Ist bereits fertig — Chris stößt selbst
noch eine kleine Anpassung an, kein Bolla-Zutun nötig.

## Wochentage evtl. später Di/Mi statt Mi/Do
Chris hat gefragt, ob ein späterer Wechsel der Wochentage (z.B. Di/Mi statt Mi/Do) ein Problem wäre — **nein**: Die 156 Termine wurden einmalig aus dem SH-Ferienkalender abgeleitet (kein wiederverwendbares Generator-Skript vorhanden, war Ad-hoc-Arbeit einer früheren Session). Bei Tageswechsel müssten die Termin-Daten einfach neu berechnet werden (Ferien weiterhin rausgerechnet) — Themen-Zuordnung und I/II-Rhythmus bleiben davon unberührt, da sie nur an der Position in der Sequenz hängen, nicht am Wochentag-Label. Unkompliziert nachzuziehen, sobald der Stundenplan da ist.

## ✅ Echter Stundenplan bestätigt (12.08.2026): Mi/Do wie geplant, Klasse↔Slot jetzt final
Chris' Stundenplan fürs Schuljahr 26/27: **7d Mi 1./2. Std (07:50–09:25), 7b Mi 6./7. Std (12:30–14:05),
7a Do 1./2. Std (07:50–09:25), 7c Do 6./7. Std (12:30–14:05)**. Der Mi/Do-Rhythmus war schon korrekt
angenommen — neu war nur die Klasse↔Slot-Zuordnung, die vorher offen war (`slots_hinweis` sagte "noch nicht
fest"). Uhrzeiten aus dem Vorjahres-Outlook-Kalender rekonstruiert (Kategorie „Lessing I/II" via Graph-API,
UTC→Berlin), nicht von Chris explizit genannt — er verwies bewusst auf die vorhandenen Kalenderdaten.
`data/schuljahr2627.json` hat jetzt `klasse`+`uhrzeit` in `slots_geplant` und allen 156 `termine[]`, MP-Seite
(`mission-control/index.html`) zeigt beides in der Tabelle/den Slot-Chips an. Details/Nächste Schritte:
[[aktuell]].

**⚠️ Zweite, unabhängige Stelle mit Stundenplan-Daten:** Die MP-Seite "📅 Übersicht" (`data-page="schule"`,
`loadSchule()`) hat ihr EIGENES hartkodiertes `KLASSEN`-Array in `index.html` (Tag/Zeit pro Kurs, für die
"Nächste Stunde"-Kacheln) — komplett getrennt von `data/schuljahr2627.json`. Wurde am 12.08.2026 noch mit
dem alten 25/26-Plan gefunden (Chris meldete falsche Termine), gefixt + 7d ergänzt. **Bei jedem künftigen
Stundenplan-Wechsel beide Stellen aktualisieren, nicht nur die JSON.**

**⚠️ Zweiter, tieferer Bug (12.08.2026, gleicher Tag) — Chris meldete IMMER NOCH falsche Termine unter
"Arbeit → Übersicht" nach dem ersten Fix:** Ursache war nicht das `KLASSEN`-Array (das war schon richtig),
sondern die Datenquelle dahinter. `loadSchule()` bezog ihre "nächste Stunde" pro Kurs aus dem globalen
`_events`-Feed (`/api/calendar`), der aus Performance-Gründen fest auf `$top=20` gedeckelt ist UND private
Termine mit reinmischt. Die 4 "II"-Gruppen-Kurse (nächster Termin oft erst 4-5 Wochen später) fielen dadurch
komplett aus den ersten 20 Einträgen raus → deren Kacheln zeigten "Kein Termin bald" statt der echten
September-Termine. **Fix:** neuer dedizierter Backend-Endpunkt `/api/calendar/schule`
(`get_schule_calendar()` in `mission_control_api.py`) — 120-Tage-Fenster, serverseitig auf
Lessing-Kategorie/`7[a-d]`-Titel gefiltert, kein `$top`-Limit-Problem mehr. `loadSchule()` UND das
Dashboard-Widget "Nächste Stunde" (`renderNextClass()`, eigener globaler Feed `_schulEvents`) nutzen jetzt
beide diesen Endpunkt statt des generischen, gedeckelten `_events`. MC-Server-Neustart war hier nötig
(Backend-Python-Änderung, nicht nur HTML).

**Lehre:** "Ich hab's schon gefixt" reicht nicht als Selbstprüfung — bei Terminanzeigen IMMER auch die
zugrundeliegende Datenquelle/API auf versteckte Limits (`$top`, Zeitfenster) prüfen, nicht nur die
Anzeige-Logik selbst. Ein zweiter Blick, nachdem Chris "immer noch falsch" meldet, ist Pflicht, nicht
optional.

**⚠️ Dritter Bug (12.08.2026, noch später am selben Tag) — Sortierung, nicht Daten:** Nach dem
Endpunkt-Fix waren die Daten pro Kachel korrekt, aber die Reihenfolge der Kacheln war falsch (startete
mit 16.09. statt mit dem nächsten echten Termin 19.08.). Ursache: `loadSchule()`s Sortierung verglich
`a.next.date + a.next.time` als **String** (`.localeCompare()`) — bei Datumsformat `"DD.MM."` ist das
falsch, weil z.B. `"16.09."` alphabetisch VOR `"19.08."` kommt (`'6' < '9'` an zweiter Stelle, der
Monat wird dabei ignoriert). **Fix:** echten Datumsvergleich über das schon vorhandene `_parseEvDate()`
statt String-Vergleich. **Dauerhafte Lehre:** `DD.MM.`-formatierte Datums-Strings NIE direkt mit
`.localeCompare()`/`<`/`>` vergleichen — immer erst in ein echtes `Date`-Objekt parsen (Helper
`_parseEvDate()` existiert schon im MP-Code, einfach wiederverwenden statt neu zu stringvergleichen).
