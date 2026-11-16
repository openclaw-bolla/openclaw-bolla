---
name: feedback-mp-plan-live
description: "Claude-Plan in MP immer live von Anthropic holen, nie hartkodieren"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: cdbbb188-b89b-408e-9c7b-7f264f50c119
---

In Mission Possible den Claude-Plan (Max/Pro/…) **IMMER live von `/api/claudequota` (`plan_label`)** holen, NIE im Code/JSON hartkodieren.

**Why:** Ein hartkodiertes „(Pro Plan)" in `mission_control_api.py` (get_token_usage) zeigte fälschlich „Pro", obwohl Chris **Max Plan** hat — fiel ihm am 22.06.2026 in der System-Überblick-Box auf.
**How to apply:** Plan-Anzeigen (`loadSystem`/`bolla-status-block`/`tokenusage`) ziehen `plan_label` aus `/api/claudequota`. Bei jeder neuen Plan-/Abo-Anzeige genauso verfahren. Verwandt: [[reference_mc]], [[reference_graph_capabilities]].
