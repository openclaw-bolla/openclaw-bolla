#!/usr/bin/env bash
# Healthcheck für cloudflared-Tunnel "bolla-mc".
# Prüft ob der Prozess läuft UND ob die Edge-Verbindung antwortet.
# Startet bei Bedarf neu. Läuft alle 2 Minuten per Cron.
set -u

LOG=/home/bolla/workspace/logs/cloudflared_health.log
TUNNEL=bolla-mc
URL=https://bolla.chrismandel.de
CFD=/home/bolla/.local/bin/cloudflared
RUNLOG=/home/bolla/workspace/logs/cloudflared.log

ts() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

restart() {
  log "RESTART: $1"
  pkill -f "cloudflared tunnel run $TUNNEL" 2>/dev/null
  sleep 3
  nohup "$CFD" tunnel run "$TUNNEL" >> "$RUNLOG" 2>&1 &
  log "neu gestartet, PID $!"
}

# 1) Prozess da?
if ! pgrep -f "cloudflared tunnel run $TUNNEL" >/dev/null; then
  restart "Prozess fehlt"
  exit 0
fi

# 2) Edge erreichbar? (302 zur Access-Login-Seite ist OK)
# Wir restarten nur, wenn 2 Checks in Folge fehlschlagen — sonst werfen wir
# aktive User-Sessions raus, nur weil ein einzelner Check zufällig timeoute.
FAIL_FLAG=/tmp/cloudflared_health_fail
code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 15 "$URL" || echo "000")
case "$code" in
  2*|3*)
    rm -f "$FAIL_FLAG"
    ;;
  *)
    if [ -f "$FAIL_FLAG" ]; then
      log "HTTP $code von $URL — zweiter Fehler in Folge"
      restart "Edge antwortet nicht ($code, 2× in Folge)"
      rm -f "$FAIL_FLAG"
    else
      log "HTTP $code von $URL — erster Fehler, warte auf nächsten Check"
      touch "$FAIL_FLAG"
    fi
    ;;
esac
