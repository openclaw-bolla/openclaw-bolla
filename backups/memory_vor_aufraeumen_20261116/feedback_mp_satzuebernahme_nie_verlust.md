---
name: feedback-mp-satzuebernahme-nie-verlust
description: MP Satz-Feedback „Übernehmen" darf NIE Text vernichten — Vorschlag ersetzt ganze Markierung; Schutz (Merge, Kürzungs-Sperre, Backup) eingebaut 09.10.2026
metadata:
  type: feedback
---

**Vorfall 09.10.2026 (Kap. 11):** Chris markierte ein ganzes Protokoll (7 Zeilen), wollte nur die Zahlen prüfen lassen und übernahm eine Änderung („Nicht zehn."). Der Opus-Vorschlag enthielt nur die EINE geänderte Zeile, `satz-entscheidung` ersetzte aber die GANZE Markierung (`ziel_text.replace(m["satz"], m["vorschlag"])`) → „Sie klickte." + 5 Protokollzeilen waren weg. Chris: „großer Fehler im System, unbedingt korrigieren und für Dauer merken."

**Why:** Übernehmen = 1:1-Ersetzung der markierten Stelle. Ist der KI-Vorschlag kürzer als die Markierung (nur geänderte Zeile), geht der Rest unbemerkt verloren. Chris liest viel und markiert oft großzügig.

**Eingebaut (alle drei Schichten, `mission_control_api.py` + `index.html` + `aurora-reader.html`):**
1. **Prompt:** Vorschlag MUSS die gesamte Markierung vollständig zurückgeben (alle Zeilen/Kursiv-/Protokollzeilen, auch unveränderte); Extraktions-Regex stoppt nur noch an `ANTWORT:`/`VORSCHLAG:`.
2. **Auto-Merge** (`_a2_merge_vorschlag`): liefert die KI weniger Zeilen als markiert, wird nur die passende (ähnlichste, ≥0,55) Zeile ersetzt, der Rest bleibt; Hinweis in der Antwort; Rohvorschlag in `vorschlag_roh`. Echte Löschabsicht (Merge ergäbe Original) wird NICHT rückgängig gemacht.
3. **Kürzungs-Sperre** (`_a2_verlust`) beim Übernehmen: weniger Zeilen oder <75 % Länge (bei >120 Zeichen) → Server antwortet `kuerzung:true` mit Liste der verschwindenden Zeilen; UI fragt per `confirm()`, erst mit `kuerzung_ok` wird übernommen.
4. **Backup vor JEDEM Übernehmen:** `workspace/backups/aurora2_vor_satz_<id>_<zeit>.json` (die letzten 60 bleiben).

**Reparatur:** Die 5 Zeilen + „Sie klickte." in Kap. 11 wiederhergestellt (Markierung a0341ec2). ⚠️ Offene Stichprobe: Kap. 9 „Warmgang", Markierung dbecc283 (29.09.), Vorschlag ließ die Zeile „In konzentrierter Form …Das klang im Kopf netter." weg — Chris fragen, ob Absicht.

**How to apply:** Wenn ich am Satz-Feedback-Tool (satz-frage/satz-entscheidung) oder ähnlichen Ersetz-Mechanismen etwas ändere: Schutz-Schichten nicht entfernen. Bei jeder automatischen Textersetzung in Buchdaten: erst Backup, dann ersetzen, nie Teilvorschlag für Gesamtmarkierung einsetzen. Verwandt: [[project_aurora_ii]].
