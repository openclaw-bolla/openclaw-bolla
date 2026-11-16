---
name: reference-wsl-timesync
description: "WSL-Uhr-Drift nach Standby — Auto-Sync-Skript + Cron, manueller Nachzieh-Befehl"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a1144717-7a19-4b14-a0fe-cf7f46c0c974
---

# WSL-Uhr-Sync (Drift nach Windows-Standby)

**Problem:** Nach Windows-Standby/Ruhezustand springt die WSL2-Uhr stundenweise weg (z.B. 19:35 statt 14:1x) und korrigiert sich erst nach einer Weile per NTP von selbst. In genau diesem Fenster sind Begrüßungen/Zeitstempel falsch. `hwclock` existiert auf diesem WSL **nicht** (keine echte Hardware-Uhr) — der alte hwclock-Plan ist hinfällig.

**Dauer-Fix (eingerichtet 19.06.2026):**
- Skript `/home/bolla/workspace/scripts/wsl_timesync.sh` liest die **echte Windows-Host-Zeit** per PowerShell (`Get-Date`) und setzt die WSL-Uhr mit `date -s` darauf. Root-eigen (chown root:root, 755).
- Passwortlose Freigabe: `/etc/sudoers.d/bolla-timesync` → `bolla ALL=(root) NOPASSWD: /home/bolla/workspace/scripts/wsl_timesync.sh`
- Cron (bolla): `*/10 * * * * sudo -n /home/bolla/workspace/scripts/wsl_timesync.sh >/dev/null 2>&1` → max. 10 Min Drift.

**Manuell sofort nachziehen** (z.B. bei Session-Start, wenn `date` offensichtlich daneben):
```
sudo -n /home/bolla/workspace/scripts/wsl_timesync.sh
```
Gibt „WSL-Uhr gesetzt auf: …" aus. Geht passwortlos, kann ich selbst aufrufen.

**Echte Zeit ohne System-Uhr prüfen:** Windows-Host per `powershell.exe Get-Date`, oder HTTP-Header `curl -sI https://google.com | grep -i ^date` (liefert UTC → +2h Sommerzeit für CEST).

Siehe [[feedback-tageszeit]].
