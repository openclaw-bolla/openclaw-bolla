---
name: feedback-ferien-abgleich-vorschlaege
description: "Vor zeitgebundenen Vorschlägen (Kurstag, Schule) immer Wochentag/Datum UND Ferien aus data/schuljahr2627.json abgleichen"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4eb2e3bb-9975-4f01-a99b-460d909c3b3e
  modified: 2026-10-19T07:36:05.573Z
---

Am 19.10.2026 (Herbstferien 12.–25.10.) habe ich beim „moin" den Kurstag-Montag als „heute fällig" vorgeschlagen, obwohl Ferien sind. Chris hat das bemängelt.

**Why:** Datum/Uhrzeit allein reichen nicht — ohne Ferienabgleich werden Schul-Vorschläge falsch.

**How to apply:** Bei jedem Session-Start-Vorschlag mit Schulbezug erst `data/schuljahr2627.json` (Ferien, Kurstage) prüfen; Punkte nur nennen, wenn sie an diesem Tag wirklich anstehen. Siehe [[project_kurstag_montag_freigabe]], [[feedback_zahl_verweis_session_start]].
