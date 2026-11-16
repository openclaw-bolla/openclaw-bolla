---
name: feedback_pptx_timing_node_falle
description: "PPTX-Shapes/Folien mit python-pptx löschen — <p:timing>-Animationsknoten bricht PowerPoint-Öffnen"
metadata:
  node_type: memory
  type: feedback
---

Beim Bearbeiten von Kurs-PPTX mit `python-pptx` (Shapes von einer Folie entfernen, Folien löschen):
Wenn eine Folie einen **`<p:timing>`-Knoten** (Klick-/Eingangs-Animationen) hat, der per Shape-ID
auf eine **gerade gelöschte Form** zeigt, verweigert **PowerPoint** danach das Öffnen mit
„PowerPoint konnte die Datei nicht öffnen" — **LibreOffice und der zip/rels-Check merken nichts**
(LO ignoriert den toten Verweis stillschweigend).

**Konkret aufgetreten 01.09.2026, Kurstag 4 (`04-The Basics - Codierung.pptx`):** Folie 9 umgebaut
(alte Beispiel-Shapes + 2 Ellipsen raus, neue Grafik rein). Folie 9 hatte einen 24-KB-`<p:timing>`.
Ergebnis: PP-COM `Presentations.Open` warf `COMException: PowerPoint could not open the file`.

**Fix:** nach dem Shape-Löschen den kompletten `<p:timing>` der Folie entfernen:
```python
from pptx.oxml.ns import qn
for tm in slide._element.findall(qn('p:timing')):
    slide._element.remove(tm)
```
Kostet die Klick-für-Klick-Animation der Folie — bei „Folie wird eh durch eine Grafik ersetzt"
egal. Wenn Animationen erhalten bleiben MÜSSEN: nur Shapes löschen, die NICHT im `<p:timing>`
referenziert sind (Shape-`id` gegen die `spid`-Werte im timing-XML prüfen).

**Verifikation immer mit PowerPoint-COM, nicht LibreOffice:**
`powershell -Command "$pp=New-Object -ComObject PowerPoint.Application; $p=$pp.Presentations.Open('D:\...pptx',$true,$false,$false); $p.Slides.Count; $p.Close(); $pp.Quit()"`
— nur PP deckt solche Ladefehler auf. Reines Neu-Öffnen mit `python-pptx` reicht ebenfalls NICHT
(zu tolerant). Siehe auch [[feedback_ppt_direkt_bearbeiten]], [[project_schuljahr2627]].
