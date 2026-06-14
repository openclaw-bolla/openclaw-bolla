#!/bin/bash
# VORLAGE für schwere Resume-Tasks (Workflows, lange Operationen)
#
# BOLLA_HEAVY_OK wird von limit_watcher.sh gesetzt:
#   true  = 5h-Budget < 70% verbraucht → mind. 30% Reserve für Chris → Task darf laufen
#   false = 5h-Budget >= 70% → zu wenig Reserve → Task wird übersprungen
#
# Einfach diese Prüfung am Anfang jedes schweren Tasks einfügen:

LOG=/home/bolla/workspace/logs/limit_watcher.log
CLAUDE=/home/bolla/.local/bin/claude

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [TASKNAME] $*" >> "$LOG"; }

# ── Budget-Check ─────────────────────────────────────────────────────────────
if [ "${BOLLA_HEAVY_OK:-false}" != "true" ]; then
    log "BOLLA_HEAVY_OK=false (5h: ${BOLLA_FIVE_H_PCT:-?}%) — überspringe. Nächster Versuch beim nächsten Watcher-Lauf."
    exit 0
fi

# ── Hier kommt die eigentliche Task-Logik ────────────────────────────────────
log "Starte schweren Task..."

"$CLAUDE" --dangerously-skip-permissions -p "..." >> "$LOG" 2>&1

log "Task beendet."
