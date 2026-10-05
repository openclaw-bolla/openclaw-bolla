#!/bin/bash
# Räumt tote sshd-Sitzungen (user bolla) auf, die sich über Wochen ansammeln
# (Reverse-Tunnel-Reconnects von Book/Pro über Windows-Portproxy :2200 -> WSL :22).
#
# Beendet nur sshd-Kindprozesse die
#   - älter als MIN_AGE Sekunden sind,
#   - keine Kindprozesse haben (keine Shell/kein Befehl läuft),
#   - und KEINEN Listen-Port halten (Book :2222, Pro :2223 usw. bleiben dadurch geschützt).
# Keeper werden dynamisch über die cgroup-Session der Listener ermittelt.

MIN_AGE=600
LOG=/home/bolla/workspace/logs/ssh_session_reaper.log

# Sessions, die einen Listener (außer Port 22) halten
KEEP_SCOPES=$(ss -tlnpe 2>/dev/null | grep -v -E ':22 ' | grep -o 'session-[0-9]*\.scope' | sort -u)

n=0
for p in $(pgrep -u bolla -f '^sshd: bolla'); do
    age=$(ps -o etimes= -p "$p" 2>/dev/null | tr -d ' ')
    [ -z "$age" ] || [ "$age" -lt "$MIN_AGE" ] && continue
    [ -n "$(pgrep -P "$p")" ] && continue
    scope=$(grep -o 'session-[0-9]*\.scope' /proc/$p/cgroup 2>/dev/null | head -1)
    if [ -n "$scope" ] && echo "$KEEP_SCOPES" | grep -qx "$scope"; then
        continue
    fi
    kill "$p" 2>/dev/null && n=$((n+1))
done

# Tote Tunnel-Halter: lauscht Book/Pro-Port, antwortet aber 3x hintereinander nicht
# (z.B. Gerät schlief, Sitzung blieb als Leiche) -> Halter beenden, damit der Watchdog
# den Tunnel neu aufbauen kann. Sonst blockiert die Leiche den Port.
for port in 2222 2223; do
    cnt=/tmp/ssh_reaper_fail_$port
    if ss -tln 2>/dev/null | grep -q "127.0.0.1:$port "; then
        if ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=no \
               -p $port ernst@localhost hostname >/dev/null 2>&1; then
            rm -f "$cnt"
        else
            f=$(( $(cat "$cnt" 2>/dev/null || echo 0) + 1 )); echo $f > "$cnt"
            if [ "$f" -ge 3 ]; then
                scope=$(ss -tlnpe 2>/dev/null | grep "127.0.0.1:$port " | grep -o 'session-[0-9]*\.scope' | head -1)
                for p in $(pgrep -u bolla -f '^sshd: bolla'); do
                    grep -q "$scope" /proc/$p/cgroup 2>/dev/null && kill "$p" && n=$((n+1))
                done
                rm -f "$cnt"
                echo "[$(date '+%F %T')] toter Tunnel-Halter Port $port ($scope) beendet" >> "$LOG"
            fi
        fi
    else
        rm -f "$cnt"
    fi
done

[ "$n" -gt 0 ] && echo "[$(date '+%F %T')] $n tote sshd-Sitzungen beendet" >> "$LOG"
exit 0
