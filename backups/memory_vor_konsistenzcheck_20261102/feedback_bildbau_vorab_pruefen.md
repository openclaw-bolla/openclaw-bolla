---
name: feedback-bildbau-vorab-pruefen
description: Bei Bild-/Karten-Neubauten Quellen und Annahmen VOR dem Generieren prüfen, Bau-Skript sofort dauerhaft speichern
metadata:
  type: feedback
---

Chris (21.09.2026, Robins GTA-VI-Karte v10): Der Prozess war „viel zu lang" — bitte künftig genauer nachprüfen, bevor endgültig generiert wird.

**Why:** Ich hab mehrfach auf falschen Annahmen gebaut: `Official_Cover_Art_Landscape.jpg` ist NUR das Logo auf dunklem Grund (nicht das Mosaik), ein Template-Match gegen dieses Bild lieferte trotzdem „0.996" (sinnlos bei einfarbigem Hintergrund) — erst nach Umweg über alte Transkripte aufgeflogen. Dazu waren v8/v9 + Bau-Skript verschwunden, weil sie nur im Scratchpad/`/tmp` lagen.

**How to apply:** (1) Vor dem Bauen jede Quelldatei kurz ansehen (Vorschau), nicht nach Dateinamen raten; (2) Messwerte wie Template-Match-Scores gegenprüfen (Plausibilität, Bild ansehen), nicht blind glauben; (3) Bau-Skript sofort nach `workspace/scripts/` legen, nicht ins Scratchpad; (4) Ergebnis vor Abgabe selbst ansehen (Überschneidungen, Geisterbilder). Bezug: [[reference_hp_foto_10x15_druck]], [[feedback_saubere_quelle_zuerst]].
