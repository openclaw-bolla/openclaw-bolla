---
name: project-aurora-hardcoded-blocks
description: AURORA-Falle — Epilog UND Vorspann/Epigraph werden in den EPUB-Build-Skripten hartkodiert/überschrieben, nicht aus der JSON
metadata:
  node_type: memory
  type: project
---

# AURORA: Mehrere Textblöcke kommen NICHT aus der JSON, sondern hartkodiert aus dem Build-Skript

Build: DE `ki_buch.json` → `scripts/aurora_epub_gen.py` · EN `ki_buch_en_adapted.json` → `scripts/aurora_epub_en.py`.
Kapitel + Vorwort kommen aus der JSON. ABER folgende Blöcke waren im EN-Skript hartkodiert bzw. überschrieben:

1. **Epilog** (`EPILOG_BODY`, `EPILOG_SUBTITLE`): komplett als String-Literal im Skript, NIE aus JSON. War bei der US-Adaption übersehen → blieb deutsch ("Marlie Braun", "Theo had stayed in Lübeck"). Fix 17.06.: Marlie→Marley, Braun→Brown, Lübeck→Providence.

2. **Vorspann/Epigraph** (`vorspann_xhtml`): Funktion bekam den JSON-Vorspann übergeben, warf ihn aber mit `text = VORSPANN_EN.strip()` weg und nutzte die hartkodierte Konstante. Dadurch landete eine alte, von Chris als "grottig" empfundene "princess who sleeps"-Fassung im Buch, NICHT die gewünschte. Fix 17.06.: Zeile auf `text = (text or "").strip() or VORSPANN_EN.strip()` geändert → liest jetzt JSON. Die gewünschte EN-Definition (Lexikon-Stil wie DE, US-adaptiert: "aurora · noun, feminine · Latin: the dawn … She is the moment when you sense that it is ending.") war verloren gegangen; aus altem Skript-Stand im Transkript `f61ff412-…jsonl` wiederhergestellt und ins `vorspann`-Feld von `ki_buch_en_adapted.json` geschrieben.

3. **Impressum** (`impressum_xhtml`): nutzt BEWUSST `IMPRESSUM_EN` (volle EN-Fassung), ignoriert kürzeres JSON — das ist OK so.
4. **Autoren-Bio** (`ABOUT_THE_AUTHOR`): hartkodiert; "near Hamburg, Germany" ist korrekt (Chris' echter Wohnort).

## ✅ GELÖST 17.06.2026 — vollständig ent-hartkodiert
Beide Skripte wurden umgebaut: **kein Buchtext mehr im Skript** (nur CSS). Alle Inhalte aus JSON-Feldern (`epilog`, `epilog_untertitel`, `vorspann`, `impressum`, `vorwort`, `ueber_autor`, `danksagung`, `rezensions_bitte`). Build bricht bei fehlendem Pflichtfeld mit `SystemExit` ab (kein Fallback). Vor/Nach-Text-Diff bewies identischen Output. Prozess-Playbook: `workspace/docs/BUCHPROJEKT_EPUB_PROZESS.md`.

**How to apply:** Bei JEDER künftigen AURORA-Inhalts-/Namens-/Ortsänderung nur die JSON ändern, nie das Skript. Trotzdem nach jedem Build den Restmarker-Scan fahren. Nach jedem Build IMMER Restmarker-Scan der EPUB fahren (deutsche Namen/Orte in EN: Marlie, Braun, Lübeck, Hamburg, Leni, Kiel). Ortsmapping EN-Adaption: Hamburg→Boston, Uni/Tech→Cambridge (Kendall Sq.), Lübeck→Providence RI.

Backups der Fixes: `aurora_epub_en.py.bak_vor_epilogfix_*`, `AURORA_english_backup_vor_epilogfix_*.epub`, `ki_buch_en_adapted_backup_vor_vorspannfix_*.json`. Stand siehe [[aktuell]] · [[facts-kern]].
