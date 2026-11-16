---
name: feedback_pptx_entwurf_workflow
description: PPTX-Kursdateien (7. Klassen): Bolla baut angepasste Version in Handouts/Entwurf mit GLEICHEM Dateinamen wie Original; Praktika wandern nach Prüfung in Handouts/Praktikum
metadata:
  type: feedback
---

Workflow (Chris, 05.10.2026), Ordner `Office/7. Klassen/Handouts/`:
- Bolla erzeugt aus der Original-PPTX eine angepasste Version in `Handouts/Entwurf/` — **Dateiname exakt wie das Original** (kein `_Entwurf`-Suffix), Layout nicht zerschießen (python-pptx, nur gezielt editieren).
- Chris macht Formatierung selbst, verschiebt den Entwurf nach oben und überschreibt das Original.
- Zugehörige `NN-Praktikum.html` liegen erst in `Entwurf/`; Chris verschiebt sie nach Prüfung nach `Handouts/Praktikum/`. Vergisst er es, holt Bolla sie beim Bauen der itslearning-Mitteilung von dort und verschiebt sie dann selbst nach `Praktikum/`.
- Hintergrund: Chris hatte bei 05/06 Anpassungen direkt ins Original eingebaut und die Entwürfe gelöscht → Überblick verloren. Bolla nie direkt im Original ändern.
- Achtung: Original 08 heißt bereits „08-2 Powerpoint Profi Ansichten Entwurf.pptx".

**Update 06.10.2026 (Chris, korrigiert):** Die nächsten PPTX (Kurstage 8–11) sind **fast alle schon final in `Handouts/`** — dort gehören die PPTX hin (nicht in `Entwurf/` suchen/ablegen). Nur die **Praktika (`NN-Praktikum.html`) liegen noch in `Entwurf/`** und bleiben dort, bis Chris sie selbst nach `Praktikum/` verschiebt.
- Chris prüft Praktikum jeweils in der laufenden Kurswoche, verschiebt es und gibt **dann das Go für itslearning**.
- **Bolla postet/verschiebt vorher nichts**, auch wenn alles fertig aussieht. Auch Crons für Kurstag-Posts erst nach diesem Go.
Siehe [[project_edv7_impress_vergleichsfolie_taeglich]], [[feedback_itslearning_workflow_bewaehrt]].
