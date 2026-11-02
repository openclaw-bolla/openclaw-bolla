---
name: feedback-summary-vertrauen
description: Session-Summary nicht durch Re-Reads aufblähen — Infos aus Summary direkt verwenden
metadata:
  type: feedback
---

**Regel:** Wenn eine Datei bereits im Session-Summary vollständig abgebildet ist, NICHT nochmal lesen. Direkt mit den Summary-Daten arbeiten.

**Why:** Chris hat explizit kritisiert dass nach Context-Compaction redundante Read-Calls gemacht wurden (limit_watcher.sh, aurora_spannungslandkarte.sh, workflow-script — alles schon im Summary). Das frisst unnötig Tokens und Kontext.

**How to apply:** Vor jedem Read-Tool-Aufruf: Steht der Inhalt bereits im Summary/Conversation? Dann kein Read. Nur lesen wenn: (a) Datei seit Summary verändert wurde, (b) Inhalt war nicht im Summary, (c) Ich brauche einen bestimmten Zeilenbereich der nicht zusammengefasst wurde. Gilt auch für Find/Grep auf bekannte Strukturen.
