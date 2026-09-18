#!/bin/bash
# Nächtliche Sicherung: git commit+push + OneDrive-Backup
# Läuft 0:15 Uhr via Cron; @reboot prüft ob Backup fehlt

WORKSPACE="/home/bolla/workspace"
LOG="/tmp/bolla_backup.log"
LAST_OK_FILE="/tmp/bolla_backup_last_ok"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

TODAY=$(date +%Y-%m-%d)
log "=== Backup gestartet (heute: $TODAY) ==="

# 1. git: uncommittete Änderungen sichern
cd "$WORKSPACE" || { log "ERROR: cd workspace fehlgeschlagen"; exit 1; }

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
    git add -A -- . ':!backups/*.tar' ':!backups/**/*.tar' ':!scratch/**' 2>>"$LOG"

    # Sicherheitsnetz: keine Dateien >20MB committen (verhindert Wiederholung des
    # Tansania-Tar-Vorfalls vom 08./09.09.2026, der monatelang git push blockiert hat)
    BIG_FILES=""
    while IFS= read -r f; do
        [ -f "$f" ] || continue
        size=$(stat -c%s "$f" 2>/dev/null) || continue
        if [ "$size" -gt 20971520 ]; then
            BIG_FILES="$BIG_FILES $f (${size}B)"
            git restore --staged -- "$f" 2>>"$LOG"
        fi
    done <<< "$(git diff --cached --name-only)"
    [ -n "$BIG_FILES" ] && log "WARNING: Große Datei(en) vom Commit ausgeschlossen (>20MB):$BIG_FILES"

    # Zweites Sicherheitsnetz: Gesamtgröße der Staged-Änderungen deckelt viele-kleine-
    # Dateien-Bloat (Vorfall 18.09.2026: ~500MB entpackte pptx aus scratch/ committet,
    # weil jede Einzeldatei <20MB war — scratch/ ist jetzt zusätzlich per .gitignore raus,
    # dies bleibt als generischer Schutz für den nächsten unvorhergesehenen Fall).
    STAGED_BYTES=0
    while IFS= read -r f; do
        [ -f "$f" ] || continue
        sz=$(stat -c%s "$f" 2>/dev/null) || continue
        STAGED_BYTES=$((STAGED_BYTES + sz))
    done <<< "$(git diff --cached --name-only)"
    if [ "$STAGED_BYTES" -gt 104857600 ]; then
        log "WARNING: Staged-Änderungen insgesamt >100MB (${STAGED_BYTES}B) — Commit wird trotzdem gemacht, aber bitte manuell prüfen!"
    fi

    git commit -m "Automatische Nachtsicherung $TODAY" 2>>"$LOG" \
        && log "git commit OK" || log "git commit: nichts Neues oder Fehler (OK)"
fi

# 2. git push (mit Retry)
PUSH_OK=false
for i in 1 2 3; do
    if git push 2>>"$LOG"; then
        PUSH_OK=true
        log "git push OK (Versuch $i)"
        break
    fi
    log "git push Versuch $i fehlgeschlagen — warte 30s"
    sleep 30
done
$PUSH_OK || log "WARNING: git push nicht möglich (Netz/Cloudflare?) — wird beim nächsten Start nachgeholt"

# 3. OneDrive-Backup — rsync mit Excludes
# cp -a hat aktive Session-Files gelockt (D-State auf OneDrive) → WSL-Service crash.
# nice/ionice damit es nie eine aktive Session stört.
# WICHTIG: KEIN --delete! (NTFS case-insensitiv vs. Linux case-sensitiv → rsync hält
#   lebende Dateien für überzählig und löscht sie → OneDrive meldet tägl. Massenlöschung,
#   im Extremfall Verlust von memory/MEMORY.md. Geprüft 17.06.2026.) Ohne --delete sammeln
#   sich nur ~60 MB harmlose Altlasten — egal bei einem Backup.
# -L: Symlinks folgen (memory-Ordner sind konsolidiert auf projects/-home-bolla/memory/).
DEST="/mnt/d/OneDrive/Dokumente/Bolla/claude-code"
mkdir -p "$DEST" 2>>"$LOG"
if nice -n 19 ionice -c 3 rsync -rtL --no-perms --no-owner --no-group -q \
        --exclude 'cache/' \
        --exclude 'file-history/' \
        --exclude 'projects/-home-bolla/*.jsonl' \
        --exclude '.credentials.json' \
        /home/bolla/.claude/ "$DEST/" 2>>"$LOG"; then
    log "OneDrive-Backup OK (rsync, ohne aktive Session)"
else
    log "WARNING: OneDrive-Backup fehlgeschlagen"
fi

# Erfolg vermerken (auch bei Push-Fehler, da lokales Commit reicht)
echo "$TODAY" > "$LAST_OK_FILE"
log "=== Backup abgeschlossen ==="
