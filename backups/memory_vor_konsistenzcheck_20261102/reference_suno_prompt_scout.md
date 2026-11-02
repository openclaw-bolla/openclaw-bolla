---
name: reference-suno-prompt-scout
description: Monatlicher Cron prüft automatisch ob Suno-Prompt-System (Style/Lyrics DE+EN) Optimierung braucht
metadata:
  node_type: memory
  type: reference
  originSessionId: current
---

**Was:** `suno_prompt_scout.py`, Cron `0 9 1 * *` (1. jedes Monats, 9:00) — Nachfolge-Automation zum
19.08.2026-Opus-Audit (siehe [[feedback_suno_lyrics_qualitaet]]). Ruft `claude -p` (Sonnet, Default-Modell)
mit Read+WebSearch auf: liest den aktuellen `/api/suno/generate`-Prompt-Code in `mission_control_api.py`
selbst, recherchiert neue Suno-Modellversionen/Community-Best-Practices (DE+EN), vergleicht gegen eine im
Prompt fest eingebettete Liste dessen, was am 19.08. schon umgesetzt wurde (damit nichts doppelt gemeldet
wird).

**Output-Verhalten:** Meldet NUR, wenn wirklich etwas Neues/Substanzielles gefunden wird (Antwort exakt
"NICHTS" sonst, wie [[user_devices]]-nahes Muster `hardware_tips.py`) — kein Rauschen bei Fehlschlag/nichts
Neuem. Bei einem echten Fund: neuer datierter Eintrag oben in `aktuell.md` (kanonischer Pfad
`/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md`, NICHT der Symlink) + kurze Telegram-Meldung
an Chris. Python-Wrapper macht den Datei-Append selbst (kontrollierte Formatierung), Claude liefert nur den
reinen Fundtext zurück — kein Write-Tool-Zugriff der unbeaufsichtigten Instanz auf die Memory-Datei.

**Getestet 19.08.2026:** Läuft sauber, lieferte erwartungsgemäß "NICHTS" (Test direkt nach dem großen Audit
am selben Tag — logisch, dass da noch nichts Neues sein kann).

**How to apply:** Wenn ein Fund in `aktuell.md` auftaucht, mit Chris besprechen ob umsetzen — nicht
automatisch anwenden. Bei wiederholten "NICHTS"-Läufen über mehrere Monate ist das Intervall evtl. zu
kurz gewählt (Suno-Community-Best-Practices ändern sich nicht monatlich) — dann ggf. auf quartalsweise
strecken, Chris fragen statt selbst zu entscheiden.
