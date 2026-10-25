---
name: feedback_wochenlimit_vor_reset_ausreizen
description: "In den letzten Stunden vor dem wöchentlichen Quota-Reset aktiv Kontingent verbrauchen statt Reserve halten (Schwaben-Prinzip: Abo-Gebühr ausreizen)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-26
---

Chris (26.09.2026, ~18:00): kurz vor dem wöchentlichen Reset (`reset_label` aus `/api/claudequota`,
meist So 00:00) soll ich NICHT die übliche 40%-Wochenreserve schonen ([[feedback_grossprojekt_budget_check]]),
sondern aktiv vorschlagen, wie das restliche Kontingent noch sinnvoll verbraucht wird (z.B. weitere
AURORA-II-Kapitel, Kurstage komplett vorbereiten, Analogie-Check-Vollpass, Memory-Aufräumen).

**Why:** Chris zahlt das Pro-Abo fix pro Woche — ungenutztes Kontingent, das beim Reset verfällt, ist aus
seiner Sicht verschenktes Geld ("bin Schwabe"). Die 40%-Reserve-Regel ergibt nur Sinn, wenn noch Tage bis
zum Reset übrig sind und Chris zwischendurch spontanen Alltagsbedarf hat — nicht in den letzten Stunden
vor einem Reset, wo "Rest der Woche" praktisch nicht mehr existiert.

**How to apply:**
- Wenn `reset_label`/`reset_hours` aus `/api/claudequota` anzeigt, dass der Wochenreset in wenigen Stunden
  bevorsteht (Faustregel: < ~6h) UND noch nennenswertes Restkontingent übrig ist (`seven_day_rem` deutlich
  > 0): proaktiv 2–3 sinnvolle, bereits vorgemerkte oder naheliegende Arbeiten vorschlagen, die dieses
  Fenster ausnutzen (offene Buchkapitel, Kurstag-Vorbereitung, Backlog aus `aktuell.md`).
- Das **5h-Fenster** bleibt trotzdem die härtere Grenze (siehe [[feedback_fable_budget_disziplin]]) — bei
  Erreichen dort automatisch per Cron/Wakeup nach Reset fortsetzen ([[feedback_auto_resume_limit]]), nicht
  auf Chris warten.
- Gilt für ALLE Modelle (auch teure wie Opus), nicht nur Sonnet — genau in diesem Fenster ist "teuer" sogar
  gewünscht, weil es das Kontingent schneller sinnvoll aufbraucht.
- Modellwahl bleibt trotzdem inhaltlich sinnvoll (nicht künstlich Opus für triviale Tasks erzwingen, nur
  um Tokens zu verbrennen) — echte, ohnehin anstehende Arbeit vorziehen, keine Fake-Arbeit erfinden.
