#!/bin/bash
# Start der Freitags-Ausreizung AURORA II (Cron Fr 16.10.2026 19:00). Startet ausreizen_fr_aurora.py detached.
ORCH=/home/bolla/workspace/scripts/ausreizen_fr_aurora.py
LOG=/home/bolla/workspace/logs/ausreizen_fr_aurora.log
if [ -f /tmp/aurora_samstag_stop ]; then echo "$(date) Stopp-Datei vorhanden, kein Start" >> $LOG; exit 0; fi
if [ ! -f "$ORCH" ]; then
  python3 - <<'PY'
import sys; sys.path.insert(0,"/home/bolla/workspace/scripts")
from job_status import report
report('ausreizen-fr','Freitags-Ausreizung AURORA II',"fehler","⚠️ Freitags-Ausreizung 19:00: Skript fehlt — nichts gestartet.")
PY
  exit 1
fi
setsid nohup python3 "$ORCH" >> $LOG 2>&1 &
