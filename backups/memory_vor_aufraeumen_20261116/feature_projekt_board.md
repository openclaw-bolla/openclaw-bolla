---
name: feature-projekt-board
description: MP-Projekt-Board — eigene Seite mit Projekten/Aktionen, interaktiv, Anstups-Queue, Antwort-Wächter
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

**MP-Projekt-Board** (seit 06.07.2026) — eigene MP-Seite, Detailebene zum Dashboard. Sidebar → Arbeit → Gruppe „Projekte" → „📋 Projekt-Board".

**Datenmodell** `data/board.json`: `{projects:[{id,title,icon,status,summary,actions:[{id,text,status,note?,date?,match?,reply?}]}]}`. Status je Aktion/Projekt: done/doing/open/paused/dropped (farbige Badges). IDs vergibt das Backend automatisch beim GET (`_board_ensure_ids`).

**Backend** `scripts/mission_control_api.py`:
- GET `/api/board` → `board_list()`
- POST `/api/board/action-toggle` {projId,actId} → erledigt↔offen
- POST `/api/board/action-delete` {projId,actId} → Aktion löschen
- POST `/api/board/nudge` {projId} → Anstups: baut Prompt aus Projekt (Titel+Stand+offene Punkte), hängt ihn an `data/board_nudges.json`, gibt ihn zurück.

**Frontend** (index.html, `loadBoard()`): Projekte als aufklappbare Cards (Aufklapp-Zustand client-seitig via localStorage). Pro Aktion: ✓ (erledigt), ↩ (zurück), ✕ (löschen, nur bei done). Pro Projekt: „📌 Anstupsen"-Button.

**Anstups (B+C):** Button kopiert den Auftrags-Prompt via `navigator.clipboard` in die Windows-Zwischenablage (B) UND legt ihn in die Queue `data/board_nudges.json` (C). Der **SessionStart-Hook** `~/.claude/hooks/session_start_aktuell.sh` zeigt offene Nudges automatisch beim Session-Start → **PFLICHT: Anstups-Queue bei Session-Start abarbeiten, danach `board_nudges.json` auf `{"nudges":[]}` leeren.**

**Antwort-Wächter** (AURORA-Kanäle) setzt `reply:true` bei Aktionen mit `match`-Feld → ✉️-Badge im Board. Siehe [[reference_bolla_docs]] / aktuell.md.

**Pflege:** board.json direkt editieren (wird pro Request gelesen, KEIN Neustart). Nur Python-Änderung braucht Neustart. Bolla pflegt Status auch selbst (erkannt erledigt → done/löschen).

**Proaktiv, ohne Nachfrage (Chris-Hinweis 2026-07-08):** Sobald eine Aufgabe fertig ist, IMMER selbst kurz `data/board.json` durchsuchen, ob sie einem bestehenden Projekt/einer Aktion entspricht — nicht erst warten bis Chris „steht das im Board?" fragt. Falls Treffer: Status auf done setzen (oder Aktion/Projekt entfernen, s.o.) im selben Arbeitsschritt wie [[feedback_aktuell_md]]. Gilt gleichrangig neben dem aktuell.md-Update, nicht als Extra-Schritt danach.

**Chris-Präferenz (06.07.2026):** Vollständig erledigte Projekte **ganz aus dem Board entfernen** (nicht nur als „done" abhaken) — Chris will Seiten schlank, die er schnell erfassen kann. Vor dem Entfernen: offene, aber nur zukünftige/terminierte Rest-Punkte in eine passende Memory auslagern (z.B. Saison-Songs → [[project_suno_saison_songs]]). Immer Backup nach `backups/board_*_pre-*.json`.


**⛔ STILLGELEGT 14.10.2026:** Nav-Eintrag entfernt (Chris: „Projekte machen wir in Zukunft lieber anders"). Seite/API/`board.json` bleiben technisch bestehen, werden aber nicht mehr gepflegt; Anstups-Queue nicht mehr genutzt. Highlights → MP-Archiv + [[project_aurora_marketing_historie]].
