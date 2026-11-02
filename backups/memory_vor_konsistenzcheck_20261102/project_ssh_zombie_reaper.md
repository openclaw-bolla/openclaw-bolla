---
name: project-ssh-zombie-reaper
description: SSH-Zombie-Sitzungen (Book/Pro-Tunnel) – Ursache, Reaper-Cron, offener Pro-Fix ExitOnForwardFailure
metadata:
  type: project
---

05.10.2026: 132 tote `sshd: bolla`-Sitzungen am Studio beendet. Ursache: Pro (192.168.178.41) versuchte Tunnel :2223 neu zu binden, Port war von toter Sitzung (26.09.) blockiert -> jeder Versuch hinterließ eine Zombie-Sitzung (ohne `ExitOnForwardFailure`). Alle Verbindungen kommen über Windows-Portproxy :2200 -> WSL :22.

Schutz: `workspace/scripts/ssh_session_reaper.sh` (Cron alle 10 Min) beendet Sitzungen >10 Min ohne Kinder/Listener; Tunnel-Halter :2222/:2223 werden nach 3x Nichtantwort (hostname-Test) gekillt. Log `logs/ssh_session_reaper.log`. Crontab-Backup `backups/crontab_vor_sshreaper_20261005.txt`. Test-Kommando muss `hostname` sein (`true` gibt es auf Windows nicht).

**OFFEN:** Am Pro beim Tunnelstart `-o ExitOnForwardFailure=yes` ergänzen (wie Book `tunnel.ps1`), Wurzelfix. Pro schlief am 05.10. -> beim nächsten Aufwachen machen. Wirkung: Pro startet den Tunnel nach Aufwachen automatisch über `pro_tunnel_watchdog.sh` (Studio, alle 30 s).

**Why:** Chris wollte Müll weg und Book-/Pro-Verbindung erhalten. **How to apply:** Bei SSH-Sitzungs-Häufung zuerst Reaper-Log und `ss -tlnpe | grep 222` prüfen; Halter nur über cgroup-Scope finden (sshd-fd nicht lesbar). Siehe [[reference_mc]].
