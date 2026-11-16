---
name: reference-rezept-layout
description: Standard-Layout für Rezept-Word-Dateien (Ordner Rezepte-Cocktails) — vor allem Bildgröße
metadata: 
  node_type: memory
  type: reference
  originSessionId: 071bf1e0-f676-4542-bef7-e65746fdc0ff
---

Rezept-.docx (Ordner `D:\OneDrive\Dokumente\Rezepte-Cocktails`) baue ich ad-hoc — es gibt KEIN festes Generator-Skript. Aufbau: Heading1 (Titel, Farbe C0392B) → kursiver Untertitel → Trennlinie → 2-Spalten-Tabelle (links Bild, rechts Zutaten, je tcW 5100 dxa) → Zubereitung (ListNumber) → Footer "🐾 Bolla · Datum".

**Bildgröße = WICHTIG (Chris-Wunsch 24.06.2026): Bild füllt die linke Tabellenzelle als großes Rechteck, NICHT klein.**
- Standard-Extent: `cx="3100000" cy="2262162"` (≈3,4″ breit) — sowohl in `<wp:extent>` als auch in `<a:ext>` der xfrm.
- Aspect-Ratio der generierten Bilder ist 1184×864 (=1.3704); bei anderem Bild Ratio beibehalten (cy = cx × Bildhöhe/Bildbreite), nicht verzerren.
- Alter (zu kleiner) Wert war `cx="1800000" cy="1313514"` — nicht mehr verwenden.

Nur MEINE Rezepte (Footer "🐾 Bolla") betreffen diesen Standard; fremde Dateien im Ordner (Sushi, Pizza Ring, Shakshuka, Pina Colada, Spaghetti, Zitronen-Hähnchen) nicht anfassen.
