#!/bin/bash
# Chris-Go 21.11.2026: Sa-Abend 2 Opus-Kapitelentwuerfe (31 um 18:00, 33 um 22:00). Notbremse: touch /tmp/aurora_samstag_stop
W=/home/bolla/workspace
warte() { t=$(date -d "$1" +%s); n=$(date +%s); [ $t -gt $n ] && sleep $((t-n)); }
ausnahme() { cat > $W/data/limit_ausnahme.json <<J
{"von":"$1","bis":"$2","gate":55,"hard":$3,"grund":"Chris 21.11. Go: 2 Kapitel Sa-Abend (Kap. 31 / 33), Puffer fuer Chris tagsueber","woche_frei":true}
J
}
warte "2026-11-21 18:01"
ausnahme "2026-11-21T18:00" "2026-11-21T21:59" 80
python3 $W/scripts/plot_umsetzung_opus.py --nur 31 >> $W/logs/sa_abend_aurora_21_11.log 2>&1
warte "2026-11-21 22:01"
if [ $(date +%H%M) -lt 2230 ]; then
  ausnahme "2026-11-21T22:00" "2026-11-21T22:45" 95
  python3 $W/scripts/plot_umsetzung_opus.py --nur 33 >> $W/logs/sa_abend_aurora_21_11.log 2>&1
fi
rm -f $W/data/limit_ausnahme.json.bak
echo "fertig $(date)" >> $W/logs/sa_abend_aurora_21_11.log
