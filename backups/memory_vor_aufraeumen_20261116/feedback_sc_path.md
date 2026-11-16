---
name: feedback-sc-path
description: sc-Befehl PATH-Problem — was schiefging und wie es dauerhaft gelöst ist
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b0f104b7-97a3-4ae8-a86e-722b13d75cfa
---

`sc` braucht zwei Dinge um zu funktionieren — beide müssen stimmen:

1. **Symlink in /usr/local/bin**: `sudo ln -sf /home/bolla/.local/bin/sc /usr/local/bin/sc`  
   Nötig weil Claude Code `.bashrc` nicht lädt und `~/.local/bin` nicht im PATH ist.

2. **PowerShell mit vollem Pfad im Script**: `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`  
   Nicht `powershell.exe` — das funktioniert nur wenn der PATH stimmt.

**Dauerhaft gelöst durch:**
- PATH-Eintrag in `~/.claude/settings.json` (greift ab nächster Session)
- Symlink `/usr/local/bin/sc` (bleibt bis Neuinstallation)
- sc-Script nutzt jetzt vollen PowerShell-Pfad

**Why:** Chris möchte das nie wieder debuggen müssen. Wenn `! sc` nicht geht, zuerst prüfen ob Symlink existiert (`ls /usr/local/bin/sc`), dann ob powershell.exe erreichbar ist.

**How to apply:** Bei jedem Systemwechsel / WSL-Neuinstallation sofort Symlink setzen und settings.json PATH prüfen.
