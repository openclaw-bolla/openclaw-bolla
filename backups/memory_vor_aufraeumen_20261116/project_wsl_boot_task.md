---
name: project-wsl-boot-task
description: Windows-Task "Bolla WSL Boot" startet WSL beim Systemstart ohne Login (nach Update-Neustart laufen Cron/@reboot-Jobs)
metadata:
  type: project
---

Am 12.11.2026 Windows-Update-Neustart 01:35 → WSL blieb bis 09:58 aus (Login-Autostart StartBolla.vbs greift nur nach Anmeldung) → Spam-Watcher, MC, Tunnel standen.

**Fix:** Aufgabenplanung-Task `Bolla WSL Boot` (Trigger AtStartup, Benutzer ernst, S4U = ohne Passwort/ohne Login, Aktion `wsl.exe -d Ubuntu -u bolla -- sleep infinity` hält WSL am Leben). Per UAC-Erhöhung angelegt (Shell ist nicht Admin).

**Why:** Cron-Jobs laufen nur, solange WSL läuft.
**How to apply:** Bei Lücken in Cron-Logs nach Neustart zuerst prüfen, ob der Task läuft/Ready ist. Ungetestet: echter Boot ohne Login (nächster Update-Neustart zeigt es).
