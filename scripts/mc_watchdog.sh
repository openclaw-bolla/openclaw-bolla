#!/bin/bash
# MC-Server Watchdog — killt + restart wenn er amok läuft
# Trigger:
#   - RSS > 1.5 GB (normal: < 500 MB)
#   - Log wächst > 500 KB pro Minute (Error-Spam-Loop)
# Läuft alle 2 Min via Cron

LOG=/home/bolla/workspace/logs/mission_control_api.log
WATCHDOG_LOG=/home/bolla/workspace/logs/mc_watchdog.log
STATE_SIZE=/tmp/mc_watchdog.lastsize
STATE_TIME=/tmp/mc_watchdog.lasttime

log_w() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$WATCHDOG_LOG"; }

PID=$(pgrep -f "mission_control_api.py" | head -1)
if [ -z "$PID" ]; then
    log_w "MC-Server läuft nicht — starte neu"
    nohup /home/bolla/workspace/scripts/start_mc_server.sh >> "$LOG" 2>&1 &
    exit 0
fi

# RSS-Check (KB)
RSS=$(ps -p "$PID" -o rss= 2>/dev/null | awk '{print $1}')
RSS_MB=$((RSS / 1024))

# Log-Wachstum (Bytes)
CUR_SIZE=$(stat -c %s "$LOG" 2>/dev/null || echo 0)
CUR_TIME=$(date +%s)
PREV_SIZE=$(cat "$STATE_SIZE" 2>/dev/null || echo 0)
PREV_TIME=$(cat "$STATE_TIME" 2>/dev/null || echo $CUR_TIME)
echo "$CUR_SIZE" > "$STATE_SIZE"
echo "$CUR_TIME" > "$STATE_TIME"

GROWTH=$((CUR_SIZE - PREV_SIZE))
ELAPSED=$((CUR_TIME - PREV_TIME))
[ "$ELAPSED" -lt 1 ] && ELAPSED=1
GROWTH_PER_MIN=$((GROWTH * 60 / ELAPSED))

AMOK=0
REASON=""
# Normal-Footprint mit Whisper large-v3 CUDA geladen: ~3 GB RAM. Erst ab 4.5 GB als Amok werten.
if [ "$RSS_MB" -gt 4500 ]; then
    AMOK=1; REASON="RSS=${RSS_MB}MB > 4.5GB"
fi
# Log-Wachstum ist der bessere Amok-Indikator (Endlos-Retry-Loops spammen Log)
if [ "$GROWTH_PER_MIN" -gt 524288 ]; then  # 512 KB/Min
    AMOK=1; REASON="${REASON} Log-Wachstum=${GROWTH_PER_MIN}B/min > 512KB/min"
fi

if [ "$AMOK" = "1" ]; then
    log_w "AMOK erkannt (PID $PID, $REASON) — kill+restart"
    kill -9 "$PID" 2>/dev/null
    sleep 2
    # Falls Log > 5 MB ist, archivieren
    if [ -f "$LOG" ] && [ $(stat -c %s "$LOG") -gt 5242880 ]; then
        mv "$LOG" "${LOG}.amok-$(date +%Y%m%d-%H%M)"
        touch "$LOG"
        log_w "Log archiviert (war > 5 MB)"
    fi
    nohup /home/bolla/workspace/scripts/start_mc_server.sh >> "$LOG" 2>&1 &
    log_w "MC neu gestartet"
fi
