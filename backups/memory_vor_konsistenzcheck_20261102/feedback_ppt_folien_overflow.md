---
name: feedback_ppt_folien_overflow
description: "Bei PPT-Folien-Generierung mit vielen Bullet-Punkten auf Überlauf prüfen, nicht nur Format 1:1 aus Nachbarfolie kopieren"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e584c3d0-1265-4feb-a057-39d5eeaba9d2
---

Wenn ich per Skript (python-pptx) eine neue Folie mit mehreren Bullet-Ebenen fülle, muss ich prüfen, ob der Text
bei der übernommenen Schriftgröße/Textbox-Höhe tatsächlich auf die Folie passt — nicht blind das Format einer
Nachbarfolie 1:1 übernehmen, wenn deutlich mehr Textzeilen reinkommen.

**Why:** Am 14.07.2026 hab ich Folie 7 in "1-Intro KLassenstufe 7.pptx" mit dem kompletten Praktikum-1-Ablauf
gefüllt (11 Zeilen über 3 Ebenen), formatiert 1:1 nach Folie 6 (36pt/32pt, `SHAPE_TO_FIT_TEXT`). Das war zu viel
Text für die Fläche — Chris musste es hinterher selbst manuell verkleinern. Sein Wunsch danach: "das grundsätzlich
bei der Folien-Generierung merken."

**How to apply:**
- Vor dem Speichern grob überschlagen: Zeilenanzahl × Zeilenhöhe (inkl. 150% Zeilenabstand) im Verhältnis zur
  Textbox-/Folienhöhe — reicht der Platz bei der Zielschriftgröße aus [[feedback_ppt_schriftgroesse]] (Chris will
  eher größer, nicht kleiner)?
- Wenn's bei großer Schrift nicht passt: lieber Inhalt kürzen/auf zwei Folien aufteilen als die Schrift klein
  quetschen — die Lesbarkeits-Vorgabe aus [[feedback_ppt_schriftgroesse]] hat Vorrang vor "alles auf eine Folie".
- Bei Unsicherheit: nach dem Bauen kurz nachfragen/Screenshot zeigen (der Headless-Browser-Weg funktioniert für
  PPTX nicht direkt, aber ein Blick auf die gerenderte Folie z.B. per LibreOffice-Export wäre denkbar, falls
  verfügbar) statt anzunehmen dass es schon passt.
