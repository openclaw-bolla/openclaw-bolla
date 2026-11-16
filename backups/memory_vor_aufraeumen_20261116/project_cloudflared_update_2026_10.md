---
name: project-cloudflared-update-2026-10
description: cloudflared 26.10.2026 auf 2026.10.4 aktualisiert (eMudhra-Zertifikatsproblem); Update-Methode und Neustart-Falle
metadata:
  type: project
---

26.10.2026: Cloudflare-Mail "Upgrade Tunnel auf >= 2026.10.2" (eMudhra/emSign-Zertifikate kompromittiert). cloudflared von 2026.3.0 auf **2026.10.4** aktualisiert, Tunnel bolla-mc ready (4 Verbindungen), Mail gelöscht. Altes Binary: `~/.local/bin/cloudflared.bak_2026.3.0` (kann später weg).

**How to apply (nächstes Update):** Binary von github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 nach `~/.local/bin/` (Chris muss den Download freigeben, Auto-Mode blockt sonst). Neustart NICHT mit `pkill -f "cloudflared tunnel run"` im selben Bash-Aufruf (killt die eigene Shell, Exit 144) — separat `pkill`, dann `setsid nohup ... &`. Der Healthcheck-Cron (alle 2 min) startet ihn sonst ohnehin neu. Prüfen: `curl 127.0.0.1:20241/ready`.
