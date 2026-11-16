---
name: feedback_erfolg_nur_mit_beleg
description: Nie "gelaufen/OK" melden ohne Datum+Inhalt des Belegs geprüft zu haben; Cron-Skripte vor Terminen auf Leerdatei prüfen
metadata:
  type: feedback
---

Am 27.10.2026 meldete ich den Kurstag-5-Post als "gelaufen, alle OK", obwohl ich nur das neueste Log (vom 5.10., Kurstag 4) gelesen hatte. Zusätzlich war der Cron-Wrapper 0 Bytes groß (Umbau am 26.10. abgeschnitten) – der Post um 14:30 wäre still ins Leere gelaufen.

**Why:** Chris verlässt sich auf meine Statusmeldungen; eine falsche Erfolgsmeldung kostet Vertrauen und hätte Schüler-Mitteilungen verpasst.

**How to apply:**
- Vor "gelaufen/erledigt": Datum UND Inhalt des Belegs prüfen (mtime, Datum im Log, richtiger Kurstag/Gruppe), nie nur `ls -t | head -1`. Kein Log von heute = "noch nicht gelaufen".
- Nach jedem Umbau eines Cron-Skripts/Wrappers: `wc -c` > 0, `py_compile`, Cron-Eintrag und Skript-Ziel gegenprüfen. Vor geplanten Posts (Kurstag-Dienstag) am Morgen Skripte auf Größe/Syntax checken.
- Verwandt: [[project_kurstag_montag_freigabe]], [[feedback_cron_nur_nach_freigabe_mit_rueckmeldung]].
