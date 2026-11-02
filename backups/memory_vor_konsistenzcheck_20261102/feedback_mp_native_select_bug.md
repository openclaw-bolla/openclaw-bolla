---
name: feedback-mp-native-select-bug
description: MP/World-Monitor-UI keine nativen <select>-Dropdowns verwenden — bei Chris real kaputt gerendert; eigene Dropdown-Widgets nutzen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6fe18dab-d09b-406c-898c-38d23a5ae009
  modified: 2026-08-16T15:12:47.213Z
---

**Regel: In Mission-Control-Frontend (`mission-control/index.html`) keine nativen HTML `<select>`-Elemente für wichtige Bedienelemente verwenden — stattdessen selbst gezeichnete Dropdowns (Button + absolut positionierte `<div>`-Liste, eigenes CSS/JS).**

**Was passierte (16.08.2026):** World-Monitor-Satelliten-Panel hatte zwei native `<select>` (Kategorie/Region). Bei mir (Playwright/headless Chromium) rendersten sie einwandfrei — alle 7 Optionen im DOM, kein JS-Fehler, mehrfach frisch getestet. Bei Chris (echtes Edge) zeigte das aufgeklappte Dropdown nur die AKTUELL gewählte Option, sonst leer — erst durch einen Screenshot von ihm sichtbar geworden, vorher tagelanges Hin und Her weil ich "bei mir funktioniert's" nicht auflösen konnte. Ursache nie gefunden (vermutlich Edge/Windows-Rendering-Eigenheit, evtl. Zoom/Accessibility-Einstellung) und nicht reproduzierbar — daher Fix: natives `<select>` komplett durch eigenes Dropdown ersetzt (`wmToggleSatDropdown()`/`wmSatGroupPick()` als Vorlage), seitdem browserunabhängig zuverlässig.

**Warum:** Chris' Setup (Edge, evtl. Zoom-/Skalierungseinstellungen wegen Kunstlinsen, s. [[user_sehvermoegen]]) scheint native Browser-UI-Popups (mindestens `<select>`) anders/fehlerhaft zu rendern als meine Testumgebung. Das ist nicht debugbar ohne sein Gerät — also gar nicht erst in diese Falle laufen.

**Wie anwenden:**
- Bei jedem neuen MP-Feature mit Dropdown/Auswahlmenü von vornherein ein eigenes Widget bauen (Muster liegt in `index.html` bei `wm-sat-group`/`wm-sat-region`), keine nativen `<select>`.
- Bestehende native `<select>` in anderen MP-Seiten NICHT präventiv umbauen (kein bekanntes Problem dort), aber bei Meldungen wie "Dropdown zeigt nichts/leer" sofort an diesen Bug denken statt lange zu rätseln.
- Allgemeiner Debugging-Lehrsatz: Wenn etwas bei mir (Playwright-Test) nachweislich funktioniert, aber Chris sagt "geht nicht" — nicht auf eigenen Tests beharren, sondern zügig um einen Screenshot bitten (`sc`-Befehl, landet unter `/mnt/d/OneDrive/Bilder/`). Das hat hier den Knoten sofort gelöst, wo reines Code-Lesen/Wiederholtes-Testen tagelang nicht weiterkam.

Verwandt: [[feedback_website_schreibzugriff]] (Playwright-Setup), [[user_sehvermoegen]] (Schriftgrößen/Zugänglichkeit), [[feedback_hintergrund_fork_lange_aktionen]] (Playwright als Fork).
