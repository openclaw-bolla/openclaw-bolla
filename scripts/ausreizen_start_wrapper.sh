#!/bin/bash
# Start des Wochenend-Ausreizens (Cron Fr 09.10.2026 19:00). Startet scripts/ausreizen_orchestrator.py detached.
# Fehlt der Orchestrator, kommt eine Telegram-Warnung statt Stille.
ORCH=/home/bolla/workspace/scripts/ausreizen_orchestrator.py
LOG=/home/bolla/workspace/logs/ausreizen_orchestrator.log
if [ -f /tmp/aurora_samstag_stop ]; then echo "$(date) Stopp-Datei vorhanden, kein Start" >> $LOG; exit 0; fi
if [ ! -f "$ORCH" ]; then
  python3 - <<'PY'
import sys; sys.path.insert(0,"/home/bolla/workspace/scripts")
from job_status import report
report('ausreizen-start','Wochenend-Ausreizen starten',"fehler","⚠️ Ausreizen-Start Fr 19:00: Orchestrator-Skript fehlt noch — nichts gestartet. Bolla muss es bauen.")
PY
  exit 1
fi
setsid nohup python3 "$ORCH" >> $LOG 2>&1 &
