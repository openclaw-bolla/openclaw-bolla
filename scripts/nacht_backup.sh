#!/bin/bash
# Nächtliche Sicherung: git commit+push + OneDrive-Backup
# Läuft 0:15 Uhr via Cron; @reboot prüft ob Backup fehlt

WORKSPACE="/home/bolla/workspace"
LOG="/tmp/bolla_backup.log"
LAST_OK_FILE="/tmp/bolla_backup_last_ok"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

TODAY=$(date +%Y-%m-%d)
log "=== Backup gestartet (heute: $TODAY) ==="

# 1. git: uncommittete Änderungen sichern
cd "$WORKSPACE" || { log "ERROR: cd workspace fehlgeschlagen"; exit 1; }

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    git add mission-control/index.html scripts/mission_control_api.py scripts/ memory/ korrektur/ 2>>"$LOG"
    git commit -m "Automatische Nachtsicherung $TODAY" 2>>"$LOG" \
        && log "git commit OK" || log "git commit: nichts Neues oder Fehler (OK)"
fi

# 2. git push (mit Retry)
PUSH_OK=false
for i in 1 2 3; do
    if git push 2>>"$LOG"; then
        PUSH_OK=true
        log "git push OK (Versuch $i)"
        break
    fi
    log "git push Versuch $i fehlgeschlagen — warte 30s"
    sleep 30
done
$PUSH_OK || log "WARNING: git push nicht möglich (Netz/Cloudflare?) — wird beim nächsten Start nachgeholt"

# 3. OneDrive-Backup
if cp -a /home/bolla/.claude "/mnt/d/OneDrive/Dokumente/Bolla/claude-code" 2>>"$LOG"; then
    log "OneDrive-Backup OK"
else
    log "WARNING: OneDrive-Backup fehlgeschlagen"
fi

# Erfolg vermerken (auch bei Push-Fehler, da lokales Commit reicht)
echo "$TODAY" > "$LAST_OK_FILE"
log "=== Backup abgeschlossen ==="
