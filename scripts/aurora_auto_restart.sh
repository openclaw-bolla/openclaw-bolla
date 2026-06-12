#!/bin/bash
# AURORA Schreib-Workflow Auto-Restart — mit intelligentem Quota-Check
# Läuft alle 2h via Crontab.
# Logik: erst Quota-Probe → wenn rate-limited: loggen+warten.
#         wenn frei → Workflow starten.

LOG=/home/bolla/workspace/logs/aurora_auto_restart.log
JSON=/home/bolla/workspace/data/ki_buch.json
CLAUDE=/home/bolla/.local/bin/claude

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

log "=== Auto-Restart Check ==="

# 1. Buch schon fertig?
FERTIG=$(python3 -c "
import json, sys
try:
    d = json.load(open('$JSON'))
    print('ja' if d.get('buch_fertig') else f'nein ({len(d[\"kapitel\"])} Kap)')
except Exception as e:
    print(f'fehler: {e}')
" 2>/dev/null)

log "Buch-Status: $FERTIG"

if [[ "$FERTIG" == ja* ]]; then
    log "Buch fertig — kein Restart nötig. Crontab-Einträge bereinigen."
    # Crontab-Einträge entfernen wenn Buch fertig
    crontab -l 2>/dev/null | grep -v aurora_auto_restart | crontab -
    log "Crontab bereinigt."
    exit 0
fi

# 2. Quota-Probe (minimaler call — gibt sofort Fehler zurück wenn rate-limited)
log "Probe-Call..."
PROBE=$("$CLAUDE" --dangerously-skip-permissions -p "Antworte nur mit dem Wort: OK" 2>&1)
PROBE_EXIT=$?

log "Probe-Ergebnis (Exit $PROBE_EXIT): ${PROBE:0:200}"

if echo "$PROBE" | grep -qi "session limit\|rate limit\|too many\|usage limit"; then
    # Rate limited — Reset-Zeit aus Fehlermeldung parsen
    RESET_INFO=$(echo "$PROBE" | grep -oi 'resets [^)]*' | head -1)
    log "Rate limited. $RESET_INFO — warte auf nächsten Cron-Lauf (in ~2h)"
    exit 0
fi

if [ $PROBE_EXIT -ne 0 ] || [ -z "$PROBE" ]; then
    log "Probe fehlgeschlagen (unbekannter Fehler) — abbruch"
    exit 1
fi

log "Quota frei (Probe OK)..."

# 3a. Falls Buch fertig → Schlusslektorat starten
if [[ "$FERTIG" == ja* ]]; then
    # Prüfe ob Lektorat schon läuft/erledigt
    LEKTORAT_DONE=$(python3 -c "
import json, os
d = json.load(open('$JSON'))
print('ja' if d.get('schlusslektorat_fertig') else 'nein')
" 2>/dev/null)
    if [ "$LEKTORAT_DONE" = "nein" ]; then
        log "Buch fertig — starte Schlusslektorat..."
        "$CLAUDE" --dangerously-skip-permissions -p \
            "Das AURORA-Buch ist fertig. Starte sofort das Schlusslektorat: Workflow mit scriptPath /home/bolla/workspace/scripts/aurora_schluss_lektorat.js" \
            >> "$LOG" 2>&1
        log "Lektorat-Aufruf beendet (Exit: $?)"
    else
        log "Lektorat bereits erledigt — nichts zu tun."
    fi
    exit 0
fi

# 3b. Buch noch nicht fertig → Schreib-Workflow starten
log "Starte Schreib-Workflow..."
"$CLAUDE" --dangerously-skip-permissions -p \
    "Das AURORA-Buch (deutscher KI-Thriller) muss noch fertiggeschrieben werden. \
Starte sofort den Schreib-Workflow mit dem scriptPath /home/bolla/workspace/scripts/aurora_schreib_workflow.js \
Kein Text, nur die Workflow-Aktion ausführen." \
    >> "$LOG" 2>&1

log "Schreib-Workflow-Aufruf beendet (Exit: $?)"
