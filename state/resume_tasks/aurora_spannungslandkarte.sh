#!/bin/bash
# Resume-Task: AURORA Spannungslandkarte Workflow
# Workflow-ID: wf_59bfe369-90b
# Erstellt: 2026-06-13

SCRIPT_PATH="/home/bolla/.claude/projects/-mnt-c-WINDOWS-system32/c30f43b0-5782-4a6e-a1ed-946538be178e/workflows/scripts/aurora-spannungslandkarte-wf_59bfe369-90b.js"
RUN_ID="wf_59bfe369-90b"
CLAUDE=/home/bolla/.local/bin/claude
LOG=/home/bolla/workspace/logs/limit_watcher.log

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] [aurora_spannungslandkarte] $*" >> "$LOG"; }

# Prüfen ob Ergebnis-Datei schon existiert (dann ist der Workflow fertig)
DONE=false
for OUTFILE in \
    "/mnt/d/OneDrive/Desktop/AURORA_Spannungslandkarte_2026-06-13.md" \
    "/mnt/c/Users/ernst/OneDrive/Desktop/AURORA_Spannungslandkarte_2026-06-13.md" \
    "/home/bolla/workspace/data/AURORA_Spannungslandkarte_2026-06-13.md"; do
    if [ -f "$OUTFILE" ]; then
        DONE=true
        log "Ergebnisdatei gefunden: $OUTFILE — Workflow abgeschlossen."
        break
    fi
done

if [ "$DONE" = "true" ]; then
    log "Alles fertig. Entferne diesen Resume-Task."
    rm -f "$0"
    exit 0
fi

log "Spannungslandkarte noch nicht fertig — starte Workflow-Resume..."

"$CLAUDE" --dangerously-skip-permissions -p "Resumt den AURORA-Spannungslandkarte-Workflow. Führe aus: Workflow({scriptPath: '$SCRIPT_PATH', resumeFromRunId: '$RUN_ID'}). Bereits abgeschlossene Kapitel-Analysen werden aus dem Cache geladen." \
    >> "$LOG" 2>&1

log "Workflow-Resume gestartet."
