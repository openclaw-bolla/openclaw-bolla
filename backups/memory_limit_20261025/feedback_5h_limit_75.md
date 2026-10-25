---
name: feedback-5h-limit-75
description: 5h-Fenster-Gating für Ausreiz-/Hintergrundläufe ist 75 % (nicht 92) — Chris 23.10.2026
metadata:
  type: feedback
---

Chris (23.10.2026): Hintergrundläufe dürfen das 5h-Fenster nicht mehr reißen — Gating **75 %** statt 92 %.

**Why:** Ein Schritt kostet bis ~13 Punkte; bei 92 % war die Reserve für Chris weg. Am 23.10. lief der Kap.-31–36-Lauf (Start 13:40, noch mit altem 92er-Code) auf 90 % und löste die 5h-Warnung aus.
**How to apply:** `samstag_ausreizen.py` Zeile ~122: `AUSREIZEN_5H_LIMIT` Default 75. Laufende Prozesse laden Code nur beim Start → nach Änderung Lauf neu starten (resumable). Ersetzt die 92-%-Angabe in [[feedback_samstag_limit_ausreizen]]. Neue Hintergrundläufe immer mit 75 gaten.
