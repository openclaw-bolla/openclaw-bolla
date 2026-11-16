---
name: project_kurstag_montag_freigabe
description: Kurstag-Mitteilungen werden montags vor dem Kurstag freigegeben (Chris gibt Mo vormittags frei, sonst nachfragen); nächster Termin Mo 26.10.2026 für Kurstag 5 Gruppe I
metadata:
  type: project
---

Chris (07.10.2026): Er erteilt die Freigabe für die itslearning-Kurstag-Mitteilungen immer **montags vormittags** der Kurstag-Woche. Tut er es nicht, soll ich passend nachfragen.

**Nächster Termin:** Herbstferien 12.–25.10.2026 → erster Montag danach ist **Mo 26.10.**, Kurstag 5 (Basics Office: WebApps, Designer, Copilot) für **Gruppe I**: 7d I + 7b I Mi 28.10., 7a I + 7c I Do 29.10. (laut data/schuljahr2627.json). Kurstag 6 Gruppe I: Mi 04.11./Do 05.11.

**How to apply:** Cron `0 11 26 10 *` → scripts/itslearning_kurstag5_freigabe_check.py: ohne `config/kurstag5_freigabe.json {"approved": true}` erscheint ein "Braucht dich"-Eintrag auf /jobs + Telegram. Nach Chris' Freigabe: Post-Cron setzen (siehe [[feedback_cron_nur_nach_freigabe_mit_rueckmeldung]]) und Datei auf approved setzen. Ferienzeiten immer aus data/schuljahr2627.json prüfen, nicht raten. Verwandt: [[feedback_jobstatus_statt_telegram]], [[project_schuljahr2627]].
