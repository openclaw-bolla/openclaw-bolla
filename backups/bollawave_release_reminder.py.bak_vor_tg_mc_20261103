#!/usr/bin/env python3
"""
Bollawave Release-Kalender Reminder.
Erinnert pro geplanter Single am Stichtag per Telegram an den DistroKid-Upload.
Datumsbasiert (übersteht aus-PC: holt verpasste nach). Jede Single nur 1× erinnert.
Stoppen einer Single: im Schedule "done": true setzen (oder Bolla sagen, dass sie raus ist).
Schedule: config/bollawave_release_schedule.json
Cron: 30 9 * * * python3 /home/bolla/workspace/scripts/bollawave_release_reminder.py
"""
import json
import urllib.request
from pathlib import Path
from datetime import date

CFG = json.loads(Path("/home/bolla/workspace/config/telegram_bot.json").read_text())
BOT, CHRIS = CFG["bot_token"], CFG["chris_id"]
SCHED = Path("/home/bolla/workspace/config/bollawave_release_schedule.json")
FOLDER = r"Suno_DistroKid\Cleanstart_8"


def tg(text):
    urllib.request.urlopen(urllib.request.Request(
        f"https://api.telegram.org/bot{BOT}/sendMessage",
        data=json.dumps({"chat_id": CHRIS, "text": text, "parse_mode": "Markdown",
                         "disable_web_page_preview": True}).encode(),
        headers={"Content-Type": "application/json"}), timeout=20)


def main():
    data = json.loads(SCHED.read_text())
    today = date.today()
    changed = False
    for s in data["singles"]:
        if s.get("done") or s.get("reminded"):
            continue
        if today < date.fromisoformat(s["date"]):
            continue
        emoji_hint = ("\n⚠️ *Titel OHNE Emojis tippen!*" if s.get("emoji_warnung") else "")
        tg(
            f"🎵 *Bollawave — nächste Single hochladen* (#{s['nr']}/8)\n\n"
            f"Heute dran: *{s['title']}*\n"
            f"📁 Datei + Cover: Ordner `{FOLDER}`{emoji_hint}\n\n"
            f"*Schnell-Einstellungen DistroKid:*\n"
            f"• Artist: *Bollawave*\n"
            f"• Sprache: *{s['sprache']}*  ·  Genre: {s['genre']}\n"
            f"• Explicit: *Nein*  ·  Songwriter: *Christoph Mandel*\n"
            f"• KI-Deklaration: *alle Teile an* (Songtext + Musik + Audio, Typ: menschlicher Künstler)\n"
            f"• Apple-Credits: Gesang→Bollawave / Exec Producer→Christoph Mandel\n"
            f"• *Alle Upsells ablehnen* (Ultimate, Vermächtnis, Store Maximizer, Mixea 9,99€)\n\n"
            f"_Hochgeladen? Sag Bolla: {s['title']} ist raus — dann hak ich's ab._ 🐾"
        )
        s["reminded"] = True
        changed = True
        break  # max 1 Reminder pro Lauf (saubere Taktung)
    if changed:
        SCHED.write_text(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
