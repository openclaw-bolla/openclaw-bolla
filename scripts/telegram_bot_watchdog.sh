#!/bin/bash
# Telegram-Bot Watchdog — startet den Bot neu, wenn er nicht läuft ODER hängt.
# Bisher kam der Bot nur per @reboot zurück; crasht er zwischendurch,
# blieb Telegram stumm bis zum nächsten Neustart. Läuft alle 2 Min via Cron.
# Neu (04.10.2026): Hänger-Erkennung. Der Bot-Prozess lebte, bekam aber
# stundenlang "Temporary failure in name resolution", während das Netz ok war.

BOT=/home/bolla/workspace/scripts/telegram_bot.py
LOG=/home/bolla/workspace/logs/telegram_bot.log
WATCHDOG_LOG=/home/bolla/workspace/logs/telegram_bot_watchdog.log
STAMP=/tmp/telegram_bot_hang_restart.stamp

log_w() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$WATCHDOG_LOG"; }

start_bot() { nohup python3 "$BOT" >> "$LOG" 2>&1 & }

if ! pgrep -f "python3 .*telegram_bot.py" > /dev/null; then
    log_w "Telegram-Bot läuft nicht — starte neu"
    start_bot
    exit 0
fi

# Hänger: die letzten 30 Logzeilen sind ALLE getUpdates-Fehler, das Log wird
# noch aktiv beschrieben (< 3 Min alt), aber DNS funktioniert von hier aus.
# Nur dann liegt es am Bot-Prozess und ein Neustart hilft (bei echtem
# Netzausfall wäre er sinnlos). Cooldown 10 Min gegen Neustart-Schleifen.
now=$(date +%s)
age=$(( now - $(stat -c %Y "$LOG") ))
if [ "$age" -lt 180 ] \
   && [ -z "$(tail -n 30 "$LOG" | grep -v 'getUpdates Fehler')" ] \
   && getent hosts api.telegram.org > /dev/null; then
    last=$(stat -c %Y "$STAMP" 2>/dev/null || echo 0)
    if [ $(( now - last )) -gt 600 ]; then
        log_w "Bot hängt (nur getUpdates-Fehler, DNS ok) — Neustart"
        touch "$STAMP"
        pkill -f "python3 .*telegram_bot.py"
        sleep 3
        start_bot
    fi
fi
