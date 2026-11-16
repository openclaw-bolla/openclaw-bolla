---
name: memory-hygiene
description: Memory-Dateien schlank halten — nächtlicher Wächter + Aufräum-Regel (Chris-Wunsch 2026-06-08)
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
---

Chris ist aufgefallen, dass Antworten sich langsamer anfühlen, und hat nach Bloat in den Memory-Dateien gefragt. Regel: Das Memory-System schlank halten und nicht unbemerkt anwachsen lassen.

**Why:** Was bei jeder Antwort/Session geladen wird, kostet Kontext-Budget (CLAUDE.md jede Antwort, MEMORY.md-Index + aktuell.md bei Session-Start, rules_kritisch + facts_kern per Hook jede Antwort). Aufgeblähte Dateien = mehr Tokens + mehr Rauschen. Die 119 Einzel-Memories laden NICHT alle pro Turn (nur bei Recall) — der per-Turn-Fixkostentreiber sind Index + Hook-Dateien + aktuell.md.

**How to apply:**
- **aktuell.md** = rollende Momentaufnahme, beim Updaten Erledigtes RAUS (Details siehe [[aktuell.md laufend updaten]]). Erledigtes lebt in Tagesnotizen + Git.
- **Nächtlicher Wächter:** `scripts/memory_health.py` läuft per Cron (03:30, reines Python, KEINE Quota), misst Größen, markiert Bloat/Dubletten/verwaiste Memories → Report in `memory/_memhealth.md` (siehe [[_memhealth]]). Bei STATUS „ACTION NEEDED" in einer Session aufräumen (nicht vollautomatisch — Urteilsarbeit; Git/OneDrive macht alles reversibel).
- **Schlankmach-Arbeit nachts** erledigen (Chris-Wunsch), nicht laufende Arbeit ausbremsen.
- **Vollautomatischer Nacht-Putzer (LLM)** wäre möglich, zieht aber Quota + editiert Memory unbeaufsichtigt → nur auf ausdrücklichen Wunsch. Default = Gratis-Wächter + Bolla macht das Schlankmachen gezielt.
- Wenn neue Memory angelegt wird: prüfen ob es eine ähnliche schon gibt (updaten statt duplizieren) und im MEMORY.md-Index verlinken (sonst „verwaist").
