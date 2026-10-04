#!/bin/bash
# Telegram-Bot Watchdog — startet den Bot neu, wenn er nicht läuft.
# Bisher kam der Bot nur per @reboot zurück; crasht er zwischendurch,
# blieb Telegram stumm bis zum nächsten Neustart. Läuft alle 2 Min via Cron.

BOT=/home/bolla/workspace/scripts/telegram_bot.py
LOG=/home/bolla/workspace/logs/telegram_bot.log
WATCHDOG_LOG=/home/bolla/workspace/logs/telegram_bot_watchdog.log

log_w() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$WATCHDOG_LOG"; }

if ! pgrep -f "telegram_bot.py" > /dev/null; then
    log_w "Telegram-Bot läuft nicht — starte neu"
    nohup python3 "$BOT" >> "$LOG" 2>&1 &
fi
