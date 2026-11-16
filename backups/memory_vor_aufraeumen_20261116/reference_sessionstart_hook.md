---
name: reference-sessionstart-hook
description: SessionStart-Hook lädt aktuell.md automatisch beim Start — nicht wegräumen
metadata: 
  node_type: memory
  type: reference
  originSessionId: 675369e7-6200-4b37-b8f0-91ad6a1cb560
---

Seit 02.07.2026 lädt ein **SessionStart-Hook** den obersten (aktuellsten) Teil von `aktuell.md` automatisch beim Session-Start in den Kontext — damit Bolla sofort den Arbeitsstand kennt, ohne dass Chris ihn erinnern muss.

- Hook-Skript: `/home/bolla/.claude/hooks/session_start_aktuell.sh` (head -c 9000 der Datei)
- Registriert in `settings.json` unter `hooks.SessionStart`
- Grund für die Kürzung: `aktuell.md` ist ~680 Zeilen, zu groß fürs Ganze bei jedem Start; Datei ist chronologisch (neu oben).
- `rules_kritisch.md` + `facts_kern.md` kommen weiterhin per `UserPromptSubmit`-Hook (context_check.py) bei jeder Frage.

⚠️ NICHT löschen — erfüllt Chris' ausdrücklichen Wunsch „aktuell.md beim Start automatisch lesen". Siehe [[feedback_aktuell_md]].
