---
name: feedback-word-schriftart
description: Alle Word-Ausgaben grundsätzlich mit Schriftart Aptos (nicht Calibri o.ä.)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67df5b73-aed6-4770-b53c-31d5403c9ba1
---

# Word-Ausgaben: Schriftart Aptos

Bei ALLEN Word-Dateien (.docx) die ich erstelle oder bearbeite, grundsätzlich **Aptos** als Schriftart verwenden.

**Why:** Chris hat das explizit so gewünscht (01.06.2026).

**How to apply:** In python-docx: `run.font.name = 'Aptos'` für alle Runs. Default-Style des Dokuments ebenfalls auf Aptos setzen:
```python
doc.styles['Normal'].font.name = 'Aptos'
from docx.oxml.ns import qn
doc.styles['Normal'].element.rPr.rFonts.set(qn('w:asciiTheme'), 'minorHAnsi')
```
Gilt für: Fließtext, Überschriften, Bullet-Listen, Code-Blöcke, Tabellen.
