---
name: Robin Map — automatisch Marker setzen
description: Bei neuen Robin-Events sofort einen Kartenmarker in loadRobin() ergänzen
type: feedback
originSessionId: 7265fa90-2a51-4c5a-8721-102beb2f414a
---
Bei jedem neuen Event das Chris für Robin nennt (Reise, Veranstaltung, Ort) sofort einen Marker in der `initMap()`-Funktion in `index.html` ergänzen — Koordinaten geocoden, passendes Emoji + Farbe wählen, Popup mit Titel/Datum/Ort.

**Why:** Chris hat explizit darum gebeten dass das automatisch passiert, ohne dass er extra daran erinnern muss.

**How to apply:** Sobald Chris ein neues Robin-Event erwähnt → geocoden → Marker in `initMap()` eintragen → Memory in `project_robin.md` updaten.
