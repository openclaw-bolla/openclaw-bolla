---
name: Graph API Kalender-Kategorien
description: Beim Erstellen von Outlook-Kalendereinträgen via Graph API den Kategorienamen verwenden, nicht den Preset-Wert
type: feedback
originSessionId: 4eaf32ae-1b2c-4d6d-aa75-ca554efa6383
---
Beim Erstellen von Kalendereinträgen über die Microsoft Graph API muss `"categories"` den **Anzeigenamen** der Kategorie enthalten (z.B. `["Termin"]`), nicht den internen Farbcode (`["preset1"]`).

**Why:** Ich habe einmal `"preset1"` statt `"Termin"` eingetragen — das hat eine falsche/keine Farbe gesetzt und beide Werte landeten als Kategorien im Eintrag.

**How to apply:** Immer `CATEGORIES`-Keys aus `mail_to_calendar.py` verwenden (z.B. `"Termin"`, `"Event"`, `"Arzt"`). Die Preset-Werte im Dict sind nur zur Dokumentation der Farben, nie als API-Wert.
