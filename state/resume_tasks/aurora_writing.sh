#!/bin/bash
# Task: AURORA Thriller — Kapitel fertigschreiben
# Startet automatisch ab START_AFTER (wird von limit_watcher.sh aufgerufen).
# Löscht sich selbst wenn das Buch fertig ist.

START_AFTER="2026-06-13 19:00:00"

NOW=$(date '+%Y-%m-%d %H:%M:%S')
if [[ "$NOW" < "$START_AFTER" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] aurora_writing: noch nicht gestartet (wartet auf $START_AFTER) — übersprungen."
    exit 0
fi

/home/bolla/workspace/scripts/aurora_auto_restart.sh

# Nach dem Run: Buch fertig?
FERTIG=$(python3 -c "
import json, os
f = '/home/bolla/workspace/data/ki_buch.json'
if os.path.exists(f):
    d = json.load(open(f))
    print('ja' if d.get('buch_fertig') else 'nein')
else:
    print('nein')
" 2>/dev/null)

if [ "$FERTIG" = "ja" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Buch fertig — aurora_writing.sh löscht sich selbst."
    rm -- "$0"
fi
