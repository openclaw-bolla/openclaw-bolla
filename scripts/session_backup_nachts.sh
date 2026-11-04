#!/bin/bash
# Nächtliches Backup: Git-Commit+Push (GitHub-Backup) + OneDrive-Spiegel (.claude). NIE rsync --delete!
LOG=/home/bolla/workspace/logs/session_backup_nachts.log
{
echo "=== $(date '+%F %T') ==="
cd /home/bolla/workspace || exit 1
git add -A
git diff --cached --quiet && echo "git: nichts zu committen" || git commit -q -m "Nächtliches Backup $(date +%F)"
git push -q && echo "git push OK" || echo "git push FEHLER"
rsync -aL /home/bolla/.claude/ "/mnt/d/OneDrive/Dokumente/Bolla/claude-code/" && echo "rsync OK" || echo "rsync FEHLER $?"
echo "=== ende $(date '+%T') ==="
} >> "$LOG" 2>&1
