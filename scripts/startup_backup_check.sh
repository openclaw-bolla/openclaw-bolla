#!/bin/bash
# @reboot: Prüft ob Backup fehlt und holt es nach

LAST_OK_FILE="/tmp/bolla_backup_last_ok"
LOG="/tmp/bolla_backup.log"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

# Kurz warten bis Netzwerk steht
sleep 15

LAST_OK=$(cat "$LAST_OK_FILE" 2>/dev/null || echo "")

if [ "$LAST_OK" = "$TODAY" ]; then
    log "Startup-Check: Backup heute bereits OK — nichts zu tun"
    exit 0
fi

if [ "$LAST_OK" = "$YESTERDAY" ]; then
    log "Startup-Check: Backup gestern OK, Push ggf. ausstehend"
    # Nur Push nachholen
    cd /home/bolla/workspace && git push >> "$LOG" 2>&1 && {
        log "Nachholender Push OK"
        echo "$TODAY" > "$LAST_OK_FILE"
    }
    exit 0
fi

# Backup fehlt komplett — alles nachholen
log "Startup-Check: Backup fehlt (last_ok=$LAST_OK) — hole nach"
bash /home/bolla/workspace/scripts/nacht_backup.sh
