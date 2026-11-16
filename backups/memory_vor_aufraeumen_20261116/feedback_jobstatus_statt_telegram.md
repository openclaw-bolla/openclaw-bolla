---
name: feedback_jobstatus_statt_telegram
description: Rückmeldung zu Jobs/Crons läuft über Statusseite /jobs (job_status.report), Telegram nur bei Fehler/Aktion nötig; 5h-Limit-Warner aus
metadata:
  type: feedback
---

Chris (07.10.2026): Telegram-Meldungen sind als Rückmeldung zu laufenden/gelaufenen/anstehenden Prozessen nicht optimal, die 5h-Limit-Meldungen waren unnötig viele.

**Umgesetzt:** `scripts/job_status.py` (`report(job_id, titel, status, detail)`, Status laeuft|ok|fehler|aktion; Telegram nur bei fehler/aktion), Daten in `data/job_status.json`, API `/api/jobs`, Seite `mission-control/jobs.html` unter `http://127.0.0.1:18790/jobs` (zeigt auch anstehende Einmal-Crons automatisch aus dem Crontab). `five_hour_warner.py`-Cron am 07.10.2026 auskommentiert (Backup backups/crontab_vor_5h_warner_aus_*). Handy-Ansicht: Chris will das erstmal nicht.

**Why:** Dauer-Pings nerven; Chris will nachschauen können statt benachrichtigt zu werden.

**How to apply:** Neue Cron-/Hintergrundjobs melden per `report(...)` statt eigener tg()-Funktion; Erfolg still. Bestehende Skripte mit eigener Telegram-Meldung bei Gelegenheit umstellen (bisher umgestellt: Song-Batch 0710, Nächste Termine Gruppe II). Dauer-Jobs wie Termine eintragen/Surface-Infos dürfen weiter melden, wenn es etwas Relevantes gibt. Verwandt: [[feedback_cron_nur_nach_freigabe_mit_rueckmeldung]], [[reference_mc]].
