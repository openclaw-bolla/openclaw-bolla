---
name: Sidebar — Vorsicht (Drag nicht anfassen + vor Löschen prüfen)
description: Zwei Sidebar-Regeln — Drag-Code eingefroren; UND vor dem Löschen einer Gruppe/Element IMMER erst im Code prüfen ob wirklich leer
type: feedback
originSessionId: dfa8875a-0ac2-4b8c-bbe7-b04d2c559b7d
---
Zwei Vorsichtsregeln für die MP-Sidebar (`mission-control/index.html`).

## 1. Drag & Drop nicht mehr anfassen
Sidebar Drag & Drop ist abgeschlossen und funktioniert zufriedenstellend. Chris: "so lassen wir es bitte nicht mehr anfassen".
**Why:** Langes Debugging, viele Iterationen — Status ist gut genug.
**How to apply:** Keine Änderungen an `initNavDrag()`, auch wenn etwas suboptimal wirkt. Nur bei explizit gemeldetem neuen Bug.

## 2. Sidebar-Gruppe leer? → LIVE-STATE prüfen, NICHT HTML-Quelltext (06.07.2026)
Chris bat, die leere Gruppe „🗂️ Projekte" zu löschen. Ich schaute in `index.html` und sah dort 3 Items + Zähler „3" → behauptete fälschlich „nicht leer". Chris korrigierte: **die Gruppe IST leer, der Zähler `3` ist hartkodiert (Blödsinn), und die 3 Items waren längst per Drag rausgezogen.**
**Warum der HTML-Check falsch ist:** Die tatsächliche Sidebar-Anordnung steht in `data/sidebar_state.json` (bzw. `GET /api/sidebar-state`), NICHT im HTML. `initNavDrag()` hängt beim Laden DOM-Elemente per State cross-section um. Der HTML-`<div id="nav-group-items-*">`-Block ist nur die Default-Ausgangslage; `<span class="nav-group-count">` ist eine feste Zahl, die nichts zählt.
**How to apply:** „Ist Gruppe X leer?" → `data/sidebar_state.json` → `itemOrder["nav-group-items-X"]` ansehen. Leeres Array = wirklich leer. NIE den hartkodierten Zähler oder die HTML-Verschachtelung glauben.
**Löschen einer leeren Gruppe (sauber, ohne den eingefrorenen Drag-Code zu berühren — nur Daten):** (a) im HTML den `<div id="nav-group-X">`-Wrapper+Header entfernen, die enthaltenen `nav-item` als normale Einträge (ohne `nav-subitem`) stehen lassen; (b) in `sidebar_state.json` den Header `nav-group-X` aus seiner Sektions-Liste streichen + Key `nav-group-items-X` löschen; (c) fehlende `data-page` der befreiten Items in die `DEFAULT_SECTION`-Self-Heal-Map eintragen. Browser übernimmt beim nächsten Laden automatisch (Server-State überschreibt localStorage). So 06.07. mit „Projekte" gemacht.
