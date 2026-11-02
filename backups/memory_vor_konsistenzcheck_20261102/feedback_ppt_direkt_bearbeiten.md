---
name: feedback-ppt-direkt-bearbeiten
description: "PPT-Scope eng halten: nur Text in BESTEHENDEN Folien einfügen/ändern, direkt in der PPTX, keine .bak-Kopien, kein Redesign"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33accb2a-0f6a-4d2c-a25a-be8944755fd0
  modified: 2026-09-18T16:51:50.608Z
---

Wenn Chris einen Auftrag zu einer Unterrichts-PPT gibt: NUR Text in **bestehenden** Folien einfügen/ändern
(python-pptx: Textboxen/Runs bearbeiten, Formatierung beibehalten) — NICHT standardmäßig eine separate
Word-/Arbeitsblatt-Datei erzeugen, und NICHT selbst am Layout/Design/an neuen Folien herumbauen.

**Why:** Ursprünglich (13.07.2026) ging es nur darum, keine separate docx statt PPT-Bearbeitung anzulegen.
**Am 18.09.2026 präzisiert:** Chris macht das eigentliche PPT-Design/Redesign lieber selbst — "das kann ich
besser und vor allem schneller". Von mir will er bei Bedarf NUR Texte in bereits vorhandenen Folien, nicht
mehr. Anlass: bei Kurstag 5 hatte ich eine komplette Folie neu aufgebaut (inkl. Positionierung/Animation)
und mangels funktionierendem python-pptx/lxml auf PowerPoint-COM-Automatisierung ausweichen müssen — im
Nachhinein wollte Chris das gar nicht in dieser Tiefe von mir, nur den Text.

**⚠️ Kein `.bak_JJJJMMTT_HHMMSS` mehr anlegen** (Kurskorrektur zur alten Regel unten) — Chris hat eigene
Sicherungen der Original-PPTs, zusätzliche Bak-Kopien im Handouts-Ordner sind nur Unordnung, die er dann
selbst wieder aufräumen muss. Direkt in der Live-Datei ändern.

**How to apply:**
- Auftrag zuerst darauf prüfen, ob es wirklich nur "Text in Folie X" ist. Wenn der Auftrag nach Redesign/
  neuen Folien/Umbau klingt: lieber kurz nachfragen oder nur den Text-Teil übernehmen und den Rest Chris
  überlassen, statt eigenmächtig zu gestalten.
- Passende PPTX im entsprechenden Klassenordner suchen (`/mnt/d/OneDrive/Dokumente/Office/7. Klassen/`
  u.ä., Dateiname korrespondiert meist zur Modulnummer).
- Bestehende Formatierung (Schriftgröße, bold, Boxen-Layout) beim Ersetzen von Runs/Absätzen möglichst
  beibehalten statt wahllos zu überschreiben.
- Separate Word-Datei nur, wenn der Auftrag ausdrücklich ein Extra-Dokument verlangt (z.B. Ausdruck/Handout
  zum Verteilen, das die Schüler in der Hand halten sollen).
- QA-Screenshots (Foliensichtprüfung) NICHT in `Desktop\temp` liegen lassen — nach Erledigung selbst
  aufräumen oder gleich in scratch/ arbeiten statt im sichtbaren temp-Ordner.
- Siehe auch [[feature_schuljahr_modul_auftrag]] für den automatisierten Auftrags-Workflow.
