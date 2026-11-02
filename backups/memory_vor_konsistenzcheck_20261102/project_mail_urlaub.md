---
name: project_mail_urlaub
description: mail_to_calendar läuft nur auf Studio, holt aber bei Neustart automatisch die verpasste Zeit nach — kein Urlaubsrisiko mehr
metadata: 
  node_type: memory
  type: project
  originSessionId: 2470f4da-762c-47fe-9179-bb62cf000d86
  modified: 2026-07-22T08:16:53.047Z
---

**Update 22.07.2026 (verifiziert im Code, nicht nur erinnert):** Die frühere Sorge ("Studio aus im Urlaub = Terminmails verpasst") ist überholt — `load_days_since_last_run()` in `mail_to_calendar.py` merkt sich den Zeitpunkt des letzten erfolgreichen Laufs und scannt beim nächsten Start automatisch genau den Zeitraum nach, der dazwischen lag (gedeckelt auf max. 90 Tage). Damit ist **Option A aus der alten Planung längst umgesetzt** — kein Handlungsbedarf mehr.

Ebenso geprüft: [[aurora_reply_watcher]] (bzw. dessen Skript) merkt sich gesehene Mail-IDs dauerhaft und prüft bei jedem Lauf die letzten 30 Postfach-Mails — holt Antworten zuverlässig nach, solange nicht 30+ neue Mails zwischen zwei Studio-Starts reinkommen.

**Why:** Beide Skripte laufen per Cron nur auf dem Studio — kein Studio an = kein Scan in dem Moment. Aber beide sind zustandsbasiert (nicht zeitfenster-blind), holen also beim nächsten Lauf alles Verpasste nach.

**How to apply:** Bei Reisen mit unregelmäßiger Studio-Nutzung (z.B. [[project_immokauf]]-Termine unterwegs, oder die Sommerreise ab 25.07.2026) reicht es, das Studio alle paar Tage kurz mit Internet hochzufahren — nichts geht verloren. Kein Vorab-Workaround nötig.
