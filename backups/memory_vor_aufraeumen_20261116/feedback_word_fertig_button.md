---
name: feedback_word_fertig_button
description: Jede Word-Datei für Chris bekommt am Ende einen grünen FERTIG-Knopf (Hyperlink → MP /api/fertig), der den Job-Status setzt und ein Log füllt
metadata:
  type: feedback
---
Chris 16.10.2026: In alle Word-Dateien, die er lesen/prüfen soll, am Ende einen Fertig-Button einbauen; Klick informiert mich, ich speichere den Status.
**Wie:** `scripts/docx_fertig.py` → `add_fertig_button(doc, job_id, titel)`; Link `http://127.0.0.1:18790/api/fertig?id=<job_id>` (nur zuhause). Endpunkt in `mission_control_api.py` setzt den /jobs-Eintrag `<job_id>` auf `ok` und hängt an `data/fertig_log.json` (`gesehen:false`). Vor dem Erzeugen der Datei den Job per `job_status.report(job_id, …, 'aktion', notify=False)` anlegen.
**Bei „moin“:** `fertig_log.json` lesen, ungesehene Einträge nennen, `gesehen:true` setzen, aktuell.md/Memory-Status nachziehen. Siehe [[feedback_moin_offene_aktionen]], [[feedback_keine_md_dateien_fuer_chris]].
