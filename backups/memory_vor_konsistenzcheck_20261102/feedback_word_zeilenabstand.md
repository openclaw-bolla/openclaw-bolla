---
name: feedback-word-zeilenabstand
description: Word-Ausgaben immer mit 0pt Absatzabstand + einfachem Zeilenabstand — python-docx-Default ist zu groß
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 476e6fe8-d826-4f31-a5b5-e066549eb236
---

Chris stören zu große Zeilen-/Absatzabstände in Word. Ursache: **python-docx' Standard-Formatvorlage** („Normal" aus dem eingebauten default.docx) bringt serienmäßig **10 pt Abstand NACH Absatz** und **1,15 Zeilenabstand** mit — nicht von mir bewusst gesetzt, sondern der Template-Default.

**Why:** Sieht luftig/unruhig aus, Chris muss es sonst jedes Mal manuell in Word korrigieren.

**How to apply:** Bei JEDER python-docx-Ausgabe direkt setzen:
```python
pf = doc.styles['Normal'].paragraph_format
pf.space_after = Pt(0); pf.space_before = Pt(0); pf.line_spacing = 1.15
```
**Wichtig:** Absatzabstand = 0 (Chris trennt Absätze über Leerzeilen), ABER **Zeilenabstand 1,15 behalten** — das macht das Textbild schöner und ist für Chris (künstliche Linsen) leichter zu lesen. Nicht auf 1,0 runter. Passt zu [[feedback_word_schriftart]] (Aptos) und [[feedback_word_output]] (kompakt).

**Merke:** .docx wird von Word gesperrt solange geöffnet → beim Überschreiben „PermissionError" = Chris bitten, die Datei in Word zu schließen.
