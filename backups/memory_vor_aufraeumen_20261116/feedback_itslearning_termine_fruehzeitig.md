---
name: feedback-itslearning-termine-fruehzeitig
description: "Termine-Ankündigungen (\"Eure nächsten Termine\") in itslearning immer frühzeitig planen/erinnern, nicht erst kurz vor knapp"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69a38b8d-d60d-499e-89a9-4518940336fa
  modified: 2026-08-12T10:59:31.129Z
---

Chris will bei den wiederkehrenden "Eure [ersten/nächsten] Termine"-Mitteilungen (siehe
[[project_itslearning_automation]]) **immer frühzeitig** erinnert und die Ankündigung entsprechend
früh vorbereitet/gepostet haben — nicht erst am letzten Tag vor dem Block-/Gruppenwechsel.

**Why:** Chris' explizite Bitte am 12.08.2026, als der erste "Eure nächsten Termine"-Reminder
(für den Wechsel Gruppe I → II am 09./10.09.2026) nur ~4-5 Tage Vorlauf hatte. Er wollte das als
Dauerprinzip festgehalten haben, nicht nur für diesen einen Fall.

**How to apply:**
- Faustregel: Reminder/Ankündigung **ca. 1 Woche vor** dem jeweiligen Block-/Gruppenwechsel ansetzen,
  nicht erst 2-3 Tage vorher.
- Gilt für JEDEN künftigen Blockwechsel im Schuljahr (ca. 9-10× über 26/27 verteilt, siehe
  [[project_schuljahr2627]] für den 4-Wochen-Rhythmus) — beim Einrichten des jeweils nächsten
  Reminders (Cron-Job nach Muster `itslearning_naechste_termine_reminder.py`) das Datum automatisch
  ca. 7 Tage vor Blockende wählen, ohne dass Chris das jedes Mal explizit sagen muss.
- Gilt sinngemäß auch für die tatsächliche Schüler-Ankündigung selbst (nicht nur die Erinnerung an
  Chris) — Termine früh genug ankündigen, damit Schüler sich darauf einstellen können.
