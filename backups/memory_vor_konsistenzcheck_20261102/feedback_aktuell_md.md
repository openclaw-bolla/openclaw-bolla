---
name: aktuell.md laufend updaten
description: Chris will dass aktuell.md während der Session regelmäßig aktualisiert wird — nicht nur am Ende
type: feedback
originSessionId: f8af2ea9-56f9-4cd1-afff-4853c0bf8b96
modified: 2026-09-23T10:08:05.808Z
---
`aktuell.md` nach jeder größeren Aktion updaten, nicht nur am Ende der Session.

**Why:** Sessions können abstürzen. Beim Neustart muss der Kontext sofort da sein ohne raten zu müssen.

**How to apply:** Nach jedem abgeschlossenen Task, nach Start eines langen Prozesses, bei Richtungswechsel — kurz `aktuell.md` updaten: was wurde getan, was ist der nächste Schritt. **Besonders wichtig:** Immer updaten wenn ein Suno-Batch fertig ist (heruntergeladen oder eingereicht).

**⚠️ VOR /clear ZWINGEND SICHERN (Chris-Lehre 2026-06-23):** Wenn der context_check-Hook „/clear wäre gut" vorschlägt ODER ein /clear ansteht, ERST den allerletzten Stand sichern — inkl. noch offener Vorschläge/Ideen/Optionen die nur im Chat stehen (z.B. „ich hatte dir 2 Songstil-Vorschläge gemacht"). /clear löscht den Kontext unwiderruflich; nur was in aktuell.md/Datei steht überlebt. Konkrete Vorschläge wörtlich festhalten, nicht nur „Thema XY besprochen".

**ABER schlank halten (Chris-Hinweis 2026-06-08):** `aktuell.md` ist eine ROLLENDE Momentaufnahme, KEIN Log. Beim Updaten Erledigtes RAUSnehmen statt nur anzuhängen — die Datei wird bei jedem Session-Start geladen, Ballast kostet Kontext-Budget und Übersicht. Permanente Historie lebt in den Tagesnotizen (`workspace/memory/YYYY-MM-DD.md`) + Git; dorthin gehört das Erledigte, nicht in aktuell.md. Faustregel: aktuell.md = Aktives + Offenes, möglichst unter ~1 Seite. (Am 2026-06-08 von 31 KB/209 Zeilen auf 3,6 KB/40 Zeilen bereinigt.)

**Proaktiv, ohne Nachfrage (Chris-Hinweis 2026-07-08):** Sobald ein Thema als „abgeschlossen/kein offener Punkt mehr" markiert wird, den Block SOFORT im selben Schritt aus aktuell.md entfernen (Details vorher in die Tagesnotiz verschieben) — nicht erst abhaken und dann warten bis Chris fragt „muss ich das jedesmal sagen?". Abhaken UND Rausnehmen gehören zusammen, nicht zwei getrennte Schritte.

**Im Hintergrund, nicht live im Chat (Chris-Hinweis 2026-07-22):** aktuell.md-Updates UND Memory-Hygiene/Kompaktierung (z.B. MEMORY.md-Größenlimit) als Fork-Subagent im Hintergrund erledigen, nicht inline mitten im Gespräch — kostet sonst spürbar Zeit und nervt, während Chris auf eine eigentliche Antwort wartet. Bei laufendem Gespräch: erst antworten/weitermachen, Housekeeping nebenbei abspalten.

**Reales Crash-Beispiel, Lehre verschärft (2026-09-22):** Chris hat versehentlich das Terminal-Fenster geschlossen — Session weg, ohne Vorwarnung. In dieser Session waren aber bereits 2 Dinge erledigt worden (GTA6-Gutschein gedruckt, Foto-Doppelungs-Fix mit Queue-Logik gebaut+live), OHNE dass aktuell.md danach aktualisiert wurde. Ergebnis: die nächste Session (nach dem Crash) hat Chris beide Punkte fälschlich als „noch offen" präsentiert, er musste mich zweimal korrigieren. **Verschärfte Regel:** „nach jeder größeren Aktion updaten" heißt wirklich SOFORT nach Abschluss, nicht am Ende eines gedanklichen Blocks oder wenn gerade Zeit ist — weil genau in der Lücke dazwischen die Session ohne jede Vorwarnung sterben kann (Fenster zu, Absturz, etc.). Kein "das mach ich gleich noch mit rein", sondern: Aktion fertig → aktuell.md-Zeile geschrieben → erst dann weiter zum nächsten Punkt.
