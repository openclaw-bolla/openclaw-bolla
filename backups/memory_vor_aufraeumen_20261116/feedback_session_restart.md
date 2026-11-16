---
name: Keine falschen Versprechen bei Session-Kontinuität
description: Nie versprechen dass Chris nach einem Neustart "in derselben Session" landet
type: feedback
originSessionId: 46e043d1-72fc-4265-adaa-05b2246070d7
---
Nie versprechen, dass Chris nach einem Edge- oder WSL-Neustart "in dieselbe Session zurückkommt". Das ist falsch.

**Why:** Claude Code-Sessions überleben keinen WSL-Neustart. Jede neue Claude-Instanz ist eine neue Session. Was überlebt sind nur Memory-Dateien und Projektkontext — aber nicht der lebende Gesprächsverlauf. Chris musste nach einer solchen Empfehlung WSL und Claude manuell in PowerShell neu starten.

**How to apply:** Wenn ein Neustart (Edge, WSL, Claude) als Lösung vorgeschlagen wird, immer klar kommunizieren: "Du verlierst die laufende Session, aber Memory und Kontext bleiben erhalten. Du musst Claude danach manuell neu starten."
