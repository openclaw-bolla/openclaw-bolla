#!/bin/bash
# Einmalig Sa 17.10.2026: um 23:00 AURORA-II-Lauf fortsetzen, Woche bis 98,5 %, Deadline 23:55. Notbremse: touch /tmp/aurora_samstag_stop
LOG=/home/bolla/workspace/logs/ausreizen_fr_aurora.log
target=$(date -d "2026-10-17 23:00" +%s)
now=$(date +%s)
[ $target -gt $now ] && sleep $((target-now))
[ -f /tmp/aurora_samstag_stop ] && { echo "$(date) Stopp-Datei, kein Start" >> $LOG; exit 0; }
AUSREIZEN_WEEK_STOP=98.5 AUSREIZEN_DEADLINE=2026-10-17T23:55:00 python3 /home/bolla/workspace/scripts/ausreizen_fr_aurora.py >> $LOG 2>&1
