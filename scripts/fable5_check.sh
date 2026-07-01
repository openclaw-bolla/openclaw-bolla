#!/bin/bash
# Fable 5 Verfügbarkeits-Check — stündlich via Crontab
# Testet ob claude-fable-5 antwortet. Bei Erfolg: MC-Benachrichtigung + Crontab-Eintrag entfernen.

LOG=/home/bolla/workspace/logs/fable5_check.log
CLAUDE=/home/bolla/.local/bin/claude
MC=http://127.0.0.1:18790

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG"; }

log "Fable-5-Check..."

RESULT=$("$CLAUDE" --model fable -p "Antworte nur mit: FABLE5-OK" 2>&1)
EXIT=$?

if echo "$RESULT" | grep -q "FABLE5-OK"; then
    log "FABLE 5 FUNKTIONIERT! Sende Benachrichtigung."

    # MC-Benachrichtigung via Clipboard (gclip)
    curl -s -X POST "$MC/api/clipboard" \
        -H "Content-Type: application/json" \
        -d '{"content": "🎉 Fable 5 ist jetzt verfügbar! Bug gefixt. Neuschrieb der AURORA-Kapitel kann starten.", "append": true}' \
        >> "$LOG" 2>&1

    # Auch als MC-Notification falls Endpoint existiert
    curl -s -X POST "$MC/api/notifications" \
        -H "Content-Type: application/json" \
        -d '{"title": "Fable 5 verfügbar!", "message": "claude-fable-5 antwortet. AURORA-Neuschrieb kann starten.", "type": "success"}' \
        >> "$LOG" 2>&1

    # Direkte Telegram-Push-Meldung (aufs Handy)
    TG_CFG=/home/bolla/workspace/config/telegram_bot.json
    TG_TOKEN=$(python3 -c "import json;print(json.load(open('$TG_CFG'))['bot_token'])" 2>/dev/null)
    TG_CHAT=$(python3 -c "import json;print(json.load(open('$TG_CFG'))['chris_id'])" 2>/dev/null)
    curl -s "https://api.telegram.org/bot$TG_TOKEN/sendMessage" \
        --data-urlencode "chat_id=$TG_CHAT" \
        --data-urlencode "text=🎉 Fable 5 ist jetzt für dich freigeschaltet! Anthropics stärkstes Modell — ideal fürs AURORA-Feintuning, solange der Max-Plan läuft (bis 14.07.). Sag Bescheid, dann leg ich los. 🐾" \
        >> "$LOG" 2>&1

    log "Benachrichtigung gesendet (gclip + MC + Telegram). Entferne Crontab-Eintrag."

    # Crontab-Eintrag entfernen — SICHER über Datei (nie '| crontab -', sonst droht Leerung)
    TMP_CRON=$(mktemp)
    crontab -l 2>/dev/null | grep -v "fable5_check" > "$TMP_CRON"
    crontab "$TMP_CRON"
    rm -f "$TMP_CRON"
    log "Crontab bereinigt. Script hat seine Arbeit getan."
else
    log "Noch nicht verfügbar (Exit $EXIT): ${RESULT:0:100}"
fi
