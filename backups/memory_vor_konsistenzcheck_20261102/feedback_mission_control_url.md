---
name: Mission Control nur per http://127.0.0.1:18790/ öffnen
description: Mission Control darf nicht per file:// geöffnet werden — sonst alle Karten leer ("Lade...")
type: feedback
originSessionId: 1828fda4-f5f3-48d7-8c03-ccd309212618
---
Mission Control IMMER über `http://127.0.0.1:18790/` (lokal) oder `https://bolla.chrismandel.de` (remote) öffnen — niemals per `file://wsl.localhost/...` als HTML-Datei direkt.

**Why:** Bei `file://` blockt der Browser die same-origin Fetches an `/api/*` (CORS / "null origin" / Mixed-Origin). Die Karten bleiben dann auf "Lade..." stehen. Außerdem hat Chris beide URLs in Edge angepinnt — er braucht keine automatisch geöffnete Seite.

**How to apply:** Keine Edge-Fenster mehr öffnen (weder `file://` noch `http://127.0.0.1:18790/`) — nicht beim Booten, nicht sonst. Chris öffnet Mission Control selbst über seine angepinnten Tabs. Wenn Chris sagt "Mission Control lädt nicht" → nach der URL fragen, bei `file://` auf `http://127.0.0.1:18790/` hinweisen.
