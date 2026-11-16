---
name: feedback_keine_telegram_mc_jobs_oben
description: Ergebnisse von Checks/Watchern/Remindern NICHT per Telegram, sondern per job_status.report ganz oben in MC-Jobs
metadata:
  type: feedback
---

Chris 03.11.2026: Ergebnisse von Checks, Watchern und Remindern NICHT mehr in Telegram (er schaut zu selten drauf), sondern ganz oben in den MC-Jobs (jobs.html, fehler/aktion stehen oben).

**Why:** Telegram wird zu selten gelesen, Meldungen gehen unter.

**How to apply:** Neue Cron-Skripte melden per `job_status.report(...)` bzw. `job_status.mc_meldung(job_id, titel, text)`. `TG_STATUS=()` in job_status.py → kein Telegram. Umgestellt 03.11.2026: ~40 Skripte (frühe `return mc_meldung(...)` in tg()/telegram(); alter Telegram-Code steht unerreichbar darunter, Backups backups/*.bak_vor_tg_mc_20261103). Bewusst NICHT: telegram_bot.py, telegram_bot_watchdog.sh, mail_to_calendar.py (Rückfragen per Telegram-Chat). Siehe [[feedback_jobstatus_statt_telegram]].
