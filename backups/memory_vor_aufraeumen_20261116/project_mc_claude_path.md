---
name: Mission Control — claude immer mit vollem Pfad aufrufen
description: mission_control_api.py läuft als Cron-Job ohne ~/.local/bin im PATH
type: project
originSessionId: 9e265b90-8a7b-4aa0-beb8-e3662b86254a
---
Der Mission Control Server startet @reboot per Cron. Cron hat keinen User-PATH, daher schlägt `["claude", ...]` als subprocess fehl mit "No such file or directory".

**Why:** Verursachte täglich fehlerhafte Rezepte (Fallback "Pasta al Pomodoro") und fehlende Bilder.

**How to apply:** In `mission_control_api.py` immer `CLAUDE_BIN = os.path.expanduser("~/.local/bin/claude")` verwenden, nie den String `"claude"`. Am Skript-Anfang wird auch `os.environ["PATH"]` erweitert.
