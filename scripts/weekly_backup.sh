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

# 4b) System-Reproduzierbarkeit: Paketlisten, Dotfiles, ~/bin, SSH-Keys, Windows-Hotkey
#     Damit ein blanker Neu-PC exakt nachgebaut werden kann (siehe docs/DISASTER_RECOVERY.md).
WINUSER="ernst"   # Windows-Benutzer auf dem Surface (für /mnt/c/Users/<user>/)
mkdir -p "$DEST/system/dotfiles" "$DEST/system/bin" "$DEST/ssh" "$DEST/windows-bolla"

# Python- und apt-Paketlisten (Restore-Befehle, nicht die Pakete selbst)
pip freeze > "$DEST/system/pip-freeze.txt" 2>/dev/null \
    && log "OK  pip freeze → system/pip-freeze.txt" || log "WARN pip freeze fehlgeschlagen"
apt-mark showmanual > "$DEST/system/apt-manual.txt" 2>/dev/null \
    && log "OK  apt-mark showmanual → system/apt-manual.txt" || log "WARN apt-mark fehlgeschlagen"
cp /etc/wsl.conf "$DEST/system/wsl.conf" 2>/dev/null && log "OK  /etc/wsl.conf" || log "WARN wsl.conf"

# Dotfiles + ~/bin (BROWSER-Autoopen, PATH, wslbrowser)
cp /home/bolla/.bashrc "$DEST/system/dotfiles/.bashrc" 2>/dev/null
cp /home/bolla/.profile "$DEST/system/dotfiles/.profile" 2>/dev/null
[ -f /home/bolla/.bash_aliases ] && cp /home/bolla/.bash_aliases "$DEST/system/dotfiles/.bash_aliases" 2>/dev/null
rsync $RSYNC_OPTS /home/bolla/bin/ "$DEST/system/bin/" 2>/dev/null \
    && log "OK  ~/bin → system/bin/" || log "WARN ~/bin"

# SSH-Keys (privat! liegt in Chris' eigenem OneDrive — bewusst so entschieden)
if rsync $RSYNC_OPTS /home/bolla/.ssh/ "$DEST/ssh/"; then
    log "OK  ~/.ssh → ssh/"
else
    log "WARN ~/.ssh konnte nicht gespiegelt werden"
fi

# Windows-Hotkey-Schicht (AutoHotkey + Launcher + .ahk) — in KEINEM anderen Backup
if [ -d "/mnt/c/Users/$WINUSER/AppData/Local/Bolla" ]; then
    if rsync $RSYNC_OPTS "/mnt/c/Users/$WINUSER/AppData/Local/Bolla/" "$DEST/windows-bolla/"; then
        log "OK  Windows Bolla-Ordner → windows-bolla/"
    else
        log "WARN Windows Bolla-Ordner konnte nicht gespiegelt werden"
    fi
else
    log "WARN Windows Bolla-Ordner nicht gefunden (/mnt/c/Users/$WINUSER/...)"
fi

# 5) Wöchentliches Snapshot-Archiv mit Datum (für Rollback falls was überschrieben wird)
SNAP="$DEST/history/snapshot_$(date +%Y%m%d).tar.gz"
if tar -czf "$SNAP" \
       -C /home/bolla workspace/config \
       -C /home/bolla .cloudflared \
       -C /home/bolla .claude \
       -C /home/bolla .ssh \
       -C /home/bolla .bashrc \
       -C "$DEST" system \
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
