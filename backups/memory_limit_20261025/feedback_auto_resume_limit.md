---
name: feedback_auto_resume_limit
description: Bei Raten-/Session-Limit während Batch-Arbeit IMMER automatisch wiederaufnehmen — nie auf Chris warten
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8d24e232-ec4f-4f9c-975b-b68f50d921a0
---

Wenn ein langer Batch-Job (Subagents, Fable-Politur, große Modell-Läufe — egal ob Fable/Opus/Sonnet) durch ein **Raten- oder Session-Limit** unterbrochen wird, ist das automatische Wiederaufnehmen **Pflicht-Reflex**. Chris soll NIE anstupsen müssen ("läuft das jetzt weiter?").

**Warum:** Das Limit selbst ist unumgehbar (Anthropic-Seite) — aber das lästige Nachfassen ist vermeidbar. Chris' Frust kam genau daher: 5 Kapitel liefen nach Fable-5h-Limit nicht weiter, und der Neustart passierte erst auf Nachfrage.

**How to apply:**
1. **Manifest-Prinzip:** Batch-Jobs immer so bauen, dass jede Teilaufgabe in eine eigene Output-Datei schreibt. Fertig = Datei existiert & plausibel groß. So ist jederzeit erkennbar, was noch fehlt (Soll-Liste vs. vorhandene Dateien) — auch nach Session-Crash.
2. **Sofort-Reflex:** Kommt eine Task-Notification mit "session limit"/"rate limit"/"hit your ... limit", NICHT einfach quittieren → sofort `curl -s http://127.0.0.1:18790/api/claudequota` prüfen. Ist das Fenster schon zurückgesetzt (5h/7d wieder Luft) → fehlende Teile SOFORT neu starten.
3. **Terminierter Reflex:** Ist das Fenster noch zu → aus der Quota die genaue Reset-Zeit lesen (`five_hour_reset_label` / `reset_label`) und einen **automatischen Weckruf kurz nach Reset** setzen (ScheduleWakeup bzw. send_later/Trigger). Der weckt die Session und arbeitet die fehlenden Manifest-Einträge ab.
4. **Chris informieren, nicht fragen:** Kurz melden „X von Y fertig, Rest läuft automatisch weiter um HH:MM" — keine Rückfrage.

Gilt für ALLE Modelle/Jobs. Siehe auch [[feedback_einfach_machen]], [[feedback_aktuell_md]], [[feedback_fable_budget_disziplin]].
