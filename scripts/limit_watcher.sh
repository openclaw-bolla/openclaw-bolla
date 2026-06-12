#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# limit_watcher.sh — Allgemeiner Anthropic-Limit-Monitor & Resume-Manager
#
# Liest ECHTE Anthropic-Quota-Daten über die MC-API (kein Probe-Call nötig!):
#   • 5h-Fenster:  Nutzung in den letzten 5h (rollendes Fenster)
#   • 7-Tage:      Wochenbudget (typisch Sa 23:59 Reset)
#
# Bei jedem Lauf:
#   1. GET http://127.0.0.1:18790/api/claudequota → echte Prozentwerte + Reset-Zeiten
#   2. Zustand + Timestamps in state/claude_limits.json speichern
#   3. Wenn nicht limitiert → alle Tasks in state/resume_tasks/*.sh ausführen
#
# Crontab-Einträge:
#   1 0 * * *      Mitternacht täglich (nach 7-Tage-Reset um Sa 23:59)
#   13 */2 * * *   Alle 2h Fallback
#   0 19 13 6 *    One-Shot: Sa 13.06. 19:00 (Start Aurora nach Budgetstart)
# ─────────────────────────────────────────────────────────────────────────────

LOG=/home/bolla/workspace/logs/limit_watcher.log
STATE=/home/bolla/workspace/state/claude_limits.json
TASKS_DIR=/home/bolla/workspace/state/resume_tasks
MC_API=http://127.0.0.1:18790

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

log "=== limit_watcher Start ==="

# ── 1. Vorherigen Zustand lesen ──────────────────────────────────────────────
WAS_LIMITED=$(python3 -c "
import json, os
f = '$STATE'
if os.path.exists(f):
    try:
        d = json.load(open(f))
        print('true' if d.get('limited') else 'false')
    except:
        print('false')
else:
    print('false')
" 2>/dev/null)

# ── 2. Echte Quota via MC-API (kein Token-Verbrauch!) ───────────────────────
QUOTA=$(curl -s --max-time 10 "$MC_API/api/claudequota" 2>/dev/null)

if [ -z "$QUOTA" ] || echo "$QUOTA" | grep -q '"error"'; then
    log "MC-API nicht erreichbar oder Fehler: $QUOTA"
    log "Fallback: nehme an, kein Limit (MC-Server läuft evtl. nicht)"
    # Kein harter Abbruch — Tasks laufen lassen, schlimmstenfalls schlägt der Agent-Call fehl
    QUOTA='{"five_hour_pct": 0, "seven_day_pct": 0, "seven_day_rem": 100}'
fi

# Prozentwerte extrahieren
FIVE_H_PCT=$(echo "$QUOTA" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('five_hour_pct', 0))" 2>/dev/null || echo "0")
SEVEN_D_PCT=$(echo "$QUOTA" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('seven_day_pct', 0))" 2>/dev/null || echo "0")
RESET_LABEL=$(echo "$QUOTA" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('reset_label', '?'))" 2>/dev/null || echo "?")
FH_RESET_LABEL=$(echo "$QUOTA" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('five_hour_reset_label', '?'))" 2>/dev/null || echo "?")

log "5h-Fenster: ${FIVE_H_PCT}% (Reset: $FH_RESET_LABEL) | 7-Tage: ${SEVEN_D_PCT}% (Reset: $RESET_LABEL)"

# ── 3. Limit erkennen ────────────────────────────────────────────────────────
# Limit gilt als aktiv wenn:
#   • 7-Tage >= 95% (reservieren ~5% Puffer für laufende Sessions)
#   • ODER 5h-Fenster >= 95%
IS_LIMITED=false
LIMIT_REASON=""

SEVEN_D_HIGH=$(python3 -c "print('true' if float('$SEVEN_D_PCT') >= 95 else 'false')" 2>/dev/null)
FIVE_H_HIGH=$(python3 -c "print('true' if float('$FIVE_H_PCT') >= 95 else 'false')" 2>/dev/null)

if [ "$SEVEN_D_HIGH" = "true" ]; then
    IS_LIMITED=true
    LIMIT_REASON="7-Tage ${SEVEN_D_PCT}% >= 95% (Reset: $RESET_LABEL)"
fi
if [ "$FIVE_H_HIGH" = "true" ]; then
    IS_LIMITED=true
    LIMIT_REASON="${LIMIT_REASON:+$LIMIT_REASON | }5h-Fenster ${FIVE_H_PCT}% >= 95% (Reset: $FH_RESET_LABEL)"
fi

# ── 4. Zustand speichern ─────────────────────────────────────────────────────
NOW=$(date -Iseconds)

if [ "$IS_LIMITED" = "true" ]; then
    log "LIMIT AKTIV — $LIMIT_REASON"
    python3 -c "
import json, os
f = '$STATE'
state = {}
if os.path.exists(f):
    try: state = json.load(open(f))
    except: pass
if not state.get('limited'):
    state['limited_since'] = '$NOW'
state['limited'] = True
state['limit_reason'] = '$LIMIT_REASON'
state['reset_label'] = '$RESET_LABEL'
state['fh_reset_label'] = '$FH_RESET_LABEL'
state['last_check'] = '$NOW'
with open(f, 'w') as out:
    json.dump(state, out, indent=2, ensure_ascii=False)
" 2>/dev/null
    log "=== Ende (limitiert — Tasks pausiert) ==="
    exit 0
fi

# Nicht limitiert — Zustand aktualisieren
python3 -c "
import json, os
f = '$STATE'
state = {}
if os.path.exists(f):
    try: state = json.load(open(f))
    except: pass
was_limited = state.get('limited', False)
state['limited'] = False
state['last_check'] = '$NOW'
state['last_ok'] = '$NOW'
state['five_hour_pct'] = float('$FIVE_H_PCT')
state['seven_day_pct'] = float('$SEVEN_D_PCT')
if was_limited:
    state['last_resume'] = '$NOW'
    state['limited_since'] = None
    state['limit_reason'] = None
with open(f, 'w') as out:
    json.dump(state, out, indent=2, ensure_ascii=False)
" 2>/dev/null

if [ "$WAS_LIMITED" = "true" ]; then
    log "LIMIT AUFGEHOBEN — starte alle Resume-Tasks (5h: ${FIVE_H_PCT}%, 7d: ${SEVEN_D_PCT}%)"
else
    log "Kein Limit (5h: ${FIVE_H_PCT}%, 7d: ${SEVEN_D_PCT}%) — Tasks regulär prüfen..."
fi

# ── 5. Tasks ausführen ───────────────────────────────────────────────────────
TASK_COUNT=0

if [ -d "$TASKS_DIR" ]; then
    for TASK_SCRIPT in "$TASKS_DIR"/*.sh; do
        [ -f "$TASK_SCRIPT" ] || continue
        TASK_NAME=$(basename "$TASK_SCRIPT" .sh)
        log "→ Task '$TASK_NAME' startet..."
        bash "$TASK_SCRIPT" >> "$LOG" 2>&1
        EXIT_CODE=$?
        log "← Task '$TASK_NAME' beendet (Exit: $EXIT_CODE)"
        TASK_COUNT=$((TASK_COUNT + 1))
    done
fi

[ $TASK_COUNT -eq 0 ] && log "Keine Tasks registriert."
log "=== Ende ($TASK_COUNT Tasks ausgeführt) ==="
