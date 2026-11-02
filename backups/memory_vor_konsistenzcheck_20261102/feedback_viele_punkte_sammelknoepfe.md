---
name: feedback_viele_punkte_sammelknoepfe
description: Word-Dateien mit vielen Einzelpunkten (Vorschläge, Prüflisten) immer mit Sammel-Knöpfen ALLES ÜBERNEHMEN / ALLES LASSEN / FERTIG
metadata:
  type: feedback
---

Chris (16.10.2026): Bei Dokumenten mit vielen Punkten immer drei Knöpfe: ✔ ALLES ÜBERNEHMEN, ✖ ALLES LASSEN, ✅ FERTIG (= Einzelentscheidung getroffen). So kann er per Stichpunkt-Check entscheiden.

**How to apply:** `scripts/docx_fertig.py` → `add_entscheidungs_buttons(doc, job_id, titel, anchor=…)` (oben UND unten) plus `add_fertig_button`. Klick → `/api/fertig?aktion=alle_uebernehmen|alle_lassen`, Job-Detail in /jobs zeigt „ENTSCHEIDUNG: …", Eintrag in data/fertig_log.json (Feld aktion) – dort nachschauen und umsetzen. Gesamtübersicht offener Projekte: data/offene_punkte.json (auf /jobs, antippbar); neue offene Punkte dort eintragen, erledigte abhaken. Siehe [[feedback_status_uebersichtstabelle]].
