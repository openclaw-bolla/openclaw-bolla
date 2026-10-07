#!/usr/bin/env python3
"""Mo 26.10.2026 (erster Montag nach den Herbstferien): Freigabe fuer die Kurstag-5-Mitteilungen
(Gruppe I: 7d I + 7b I Mi 28.10., 7a I + 7c I Do 29.10.) pruefen.
Chris gibt montags vormittags frei (-> Bolla setzt den Post-Cron). Liegt bis zum Check keine Freigabe vor,
erscheint auf /jobs unter "Braucht dich" + 1x Telegram. Freigabe: config/kurstag5_freigabe.json {"approved": true}"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/bolla/workspace/scripts")
from job_status import report

F = Path("/home/bolla/workspace/config/kurstag5_freigabe.json")
approved = json.loads(F.read_text()).get("approved") if F.exists() else False
if approved:
    report("itslearning-kurstag5-freigabe", "Kurstag 5 (Gruppe I): Freigabe", "ok", "freigegeben")
else:
    report("itslearning-kurstag5-freigabe", "Kurstag 5 (Gruppe I): Freigabe fehlt", "aktion",
           "Mitteilungen für 7d I/7b I (Mi 28.10.) und 7a I/7c I (Do 29.10.) sind noch nicht freigegeben – bitte kurz Bescheid sagen")
