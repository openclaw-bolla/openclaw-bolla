#!/usr/bin/env bash
# Healthcheck für cloudflared-Tunnel "bolla-mc".
# Prüft: Prozess, Metrics (ha_connections), Edge-URL, Max-Uptime.
# Läuft alle 2 Minuten per Cron.
set -u

LOG=/home/bolla/workspace/logs/cloudflared_health.log
TUNNEL=bolla-mc
URL=https://bolla.chrismandel.de
CFD=/home/bolla/.local/bin/cloudflared
RUNLOG=/home/bolla/workspace/logs/cloudflared.log
METRICS=http://127.0.0.1:20241/metrics
MAX_UPTIME_SEC=21600  # 6 Stunden
FAIL_FLAG=/tmp/cloudflared_health_fail
PID_START_FILE=/tmp/cloudflared_start_ts
RESTART_LOCK=/tmp/cloudflared_restarting

ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

# Mission Control API Watchdog: bewusst NICHT hier — mc_watchdog.sh (eigener
# Cron, gleicher 2-Min-Takt) besitzt das exklusiv inkl. Doppelstart-Schutz.
# Ein zweiter Watchdog hier lief unkoordiniert dagegen und erzeugte bei jedem
# MC-Neustart ein kurzes Zeitfenster mit zwei konkurrierenden Prozessen
# (sichtbar als "Doppelstart erkannt" in mc_watchdog.log, mehrfach täglich).
# Entfernt 2026-08-18.

restart() {
  # Nicht neu starten wenn letzter Restart weniger als 90 Sek her
  if [ -f "$RESTART_LOCK" ]; then
    lock_age=$(( $(date +%s) - $(cat "$RESTART_LOCK") ))
    if [ "$lock_age" -lt 90 ]; then
      log "Restart übersprungen (letzter vor ${lock_age}s, Cooldown 90s)"
      return
    fi
  fi
  log "RESTART: $1"
  pkill -f "cloudflared tunnel run $TUNNEL" 2>/dev/null
  sleep 5
  nohup "$CFD" tunnel run "$TUNNEL" >> "$RUNLOG" 2>&1 &
  log "neu gestartet, PID $!"
  date +%s > "$PID_START_FILE"
  date +%s > "$RESTART_LOCK"
  rm -f "$FAIL_FLAG"
}

# 1) Prozess da?
if ! pgrep -f "cloudflared tunnel run $TUNNEL" >/dev/null; then
  restart "Prozess fehlt"
  exit 0
fi

# 2) Proaktiver Restart nach 6h (QUIC-Connections werden in WSL stale)
if [ -f "$PID_START_FILE" ]; then
  started=$(cat "$PID_START_FILE")
else
  # Fallback: Prozess-Startzeit aus /proc
  pid=$(pgrep -f "cloudflared tunnel run $TUNNEL" | head -1)
  if [ -n "$pid" ] && [ -d "/proc/$pid" ]; then
    started=$(stat -c %Y "/proc/$pid" 2>/dev/null || echo 0)
  else
    started=$(date +%s)
  fi
  echo "$started" > "$PID_START_FILE"
fi
now=$(date +%s)
age=$(( now - started ))
if [ "$age" -ge "$MAX_UPTIME_SEC" ]; then
  restart "Proaktiver Restart nach $(( age / 3600 ))h (Max: $(( MAX_UPTIME_SEC / 3600 ))h)"
  exit 0
fi

# 3) Metrics: ha_connections muss >= 1 sein
ha=$(curl -s --max-time 5 "$METRICS" 2>/dev/null \
  | grep '^cloudflared_tunnel_ha_connections ' \
  | awk '{print int($2)}')
if [ -n "$ha" ] && [ "$ha" -lt 1 ]; then
  restart "ha_connections=$ha (keine aktiven Tunnel-Verbindungen)"
  exit 0
fi

# 4) Edge erreichbar? (302 = Access-Login ist OK)
#    2 Fehler in Folge nötig, um Flapping zu vermeiden.
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$URL" 2>/dev/null || echo "000")
case "$code" in
  2*|3*)
    rm -f "$FAIL_FLAG"
    ;;
  *)
    if [ -f "$FAIL_FLAG" ]; then
      log "HTTP $code von $URL — zweiter Fehler in Folge"
      restart "Edge antwortet nicht ($code, 2× in Folge)"
    else
      log "HTTP $code von $URL — erster Fehler, warte auf nächsten Check"
      touch "$FAIL_FLAG"
    fi
    ;;
esac
