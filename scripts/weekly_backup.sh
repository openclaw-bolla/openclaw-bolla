#!/bin/bash
# Wöchentliches Backup für Disaster-Recovery
# Läuft sonntags via Cron; spielt alle kritischen Artefakte nach OneDrive.
# Die Recovery-Anleitung (docs/bolla_recovery.docx) referenziert diese Pfade.

set -u

DEST="/mnt/d/OneDrive/Dokumente/Bolla/backups"
LOG_TAG="[$(date +%Y-%m-%d\ %H:%M)]"

log() { echo "$LOG_TAG $1"; }

if [ ! -d "$DEST" ]; then
    log "FEHLER: $DEST nicht erreichbar — OneDrive gemountet?"
    exit 1
fi

mkdir -p "$DEST/config-latest" "$DEST/cloudflared" "$DEST/claude-code" "$DEST/history"

# rsync-Optionen: -r rekursiv, -t Timestamps, --delete spiegelt (löscht verwaist),
# --no-perms/owner/group für NTFS-Kompatibilität, -q still (Fehler via Exit-Code)
RSYNC_OPTS="-rt --delete --no-perms --no-owner --no-group -q"

# 1) workspace/config — OAuth-Tokens, Keys, Bot-Config
if rsync $RSYNC_OPTS /home/bolla/workspace/config/ "$DEST/config-latest/"; then
    log "OK  workspace/config → config-latest/"
else
    log "WARN workspace/config konnte nicht komplett gespiegelt werden"
fi

# 2) cloudflared — Tunnel-Credentials + config.yml + cert.pem
if rsync $RSYNC_OPTS /home/bolla/.cloudflared/ "$DEST/cloudflared/"; then
    log "OK  ~/.cloudflared → cloudflared/"
else
    log "WARN ~/.cloudflared konnte nicht gespiegelt werden"
fi

# 3) crontab
if crontab -l > "$DEST/crontab-latest.txt" 2>/dev/null; then
    log "OK  crontab → crontab-latest.txt"
else
    log "WARN crontab -l leer oder Fehler"
fi

# 4) ~/.claude (Memory, Settings, Session-History, CLAUDE.md)
#   Ausgeschlossen: Cache-Ordner und Session-Verzeichnisse fremder Projekte (brauchen wir nicht)
if rsync $RSYNC_OPTS \
        --exclude 'cache/' \
        --exclude 'file-history/' \
        --exclude 'projects/-mnt-c-*' \
        /home/bolla/.claude/ "$DEST/claude-code/"; then
    log "OK  ~/.claude → claude-code/"
else
    log "WARN ~/.claude konnte nicht komplett gespiegelt werden"
fi

# 5) Wöchentliches Snapshot-Archiv mit Datum (für Rollback falls was überschrieben wird)
SNAP="$DEST/history/snapshot_$(date +%Y%m%d).tar.gz"
if tar -czf "$SNAP" \
       -C /home/bolla workspace/config \
       -C /home/bolla .cloudflared \
       -C /home/bolla .claude \
       "$DEST/crontab-latest.txt" 2>/dev/null; then
    log "OK  snapshot → $(basename "$SNAP") ($(du -h "$SNAP" | cut -f1))"
else
    log "WARN snapshot konnte nicht erstellt werden"
fi

# 6) Alte Snapshots: nur die letzten 8 behalten
find "$DEST/history" -name "snapshot_*.tar.gz" -printf '%T@ %p\n' 2>/dev/null \
    | sort -n | head -n -8 | cut -d' ' -f2- | while read -r f; do
        rm -f "$f" && log "OK  gelöscht: $(basename "$f")"
    done

log "fertig."
