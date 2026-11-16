---
name: feedback-cron-nur-nach-freigabe-mit-rueckmeldung
description: Job für bestimmten Tag freigegeben = sofort Cron einrichten, ohne Rückfrage; jeder Job meldet per Telegram, ob vollzogen
metadata:
  type: feedback
---

Chris (05.10.2026, präzisiert): Gibt Chris einen Job **für einen bestimmten Tag/Zeitpunkt frei** (z.B. „am Do nachmittag einstellen"), richte ich dafür **immer direkt einen Cron ein — ohne weitere Rückfrage**. Die Freigabe des Jobs IST die Cron-Freigabe. Zusätzlich muss **jeder Job per Telegram zurückmelden, ob er vollzogen wurde** (✅ / ⚠️ mit Details, auch bei Abbruch).

(Meine erste Fassung „Cron erst nach separater Freigabe" war falsch verstanden — Chris: „nein so nicht".)

**Why:** Der Auto-Mode-Classifier blockte meinen ersten Cron als „Unauthorized Persistence", weil keine ausdrückliche Zusage vorlag. Chris will keine Extra-Schleife und nicht raten müssen, ob ein Hintergrundjob lief (Beispiele: Cron 05.10. 14:30 Kurstag 4, 08.10. 14:30 „nächste Termine" Gruppe II).

**How to apply:** Bei „am <Tag> hochladen/posten/senden" → Skript bauen, Telegram-Rückmeldung einbauen (Muster: `tg()` in `scripts/itslearning_post_naechste_termine_gruppeII_nov.py` bzw. `scripts/itslearning_kurstag_cron_wrapper.py`, Config `config/telegram_bot.json`), Cron per Datei-Methode installieren ([[feedback_crontab_pipe_falle]]) + Crontab-Backup, in `aktuell.md` eintragen, Chris Zeit/Skript nennen. Geht der Classifier trotzdem dazwischen: Chris' Aussage hier zitieren bzw. ihn per `!` ausführen lassen, nicht umgehen. Siehe [[reference_automode_classifier_mail]].
