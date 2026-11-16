---
name: project_aurora_i_ebook_cover_png_google_d2d
description: Bei Google Play + D2D fehlt im Cover-PNG die „I“ (AURORA I) — erst tauschen, wenn AURORA II veröffentlicht wird; NICHT in moin, dann selbst vorschlagen
metadata:
  type: project
---
Stand 03.11.2026: Die eBook-Cover (PNG/JPG) bei **Google Play Books** (DE `68ES01N6JE2`, EN `RCD8HR2D4AE`) und **Draft2Digital** (DE 4310151, EN 4310229) zeigen noch „AURORA" **ohne das „I"**. Richtige Dateien: `Bolla\AURORA\4_Cover_Quellen\` (`AURORA_I_ebook_front_{de,en}.png/jpg`, erzeugt von `build_cover.py de|en <Seitenzahl> <outdir> I`) bzw. `2_eBook\AURORA_Cover.jpg`.

**Why:** Chris 03.11.2026: Das reicht, wenn wir AURORA II veröffentlichen (dann ohnehin alle Kanäle anfassen); KDP-eBook/Print wurden schon bzw. werden separat getauscht. Als moin-Punkt würde es ihn nur ablenken.

**How to apply:** NICHT in `offene_punkte.json`/moin aufnehmen. Sobald AURORA II zur Veröffentlichung ansteht (Upload bei KDP/D2D/Google beginnt, Release-Termin steht), von selbst vorschlagen: „Cover-PNG bei Google + D2D für Band I mit „I" tauschen?" und gleich mit erledigen. Vorher prüfen, ob KDP-eBook-Cover Band I das „I" schon hat. Cover immer mit `4_Cover_Quellen\build_cover.py` bauen, nie `scripts/aurora_cover_wrap.py` ([[project_aurora_update_checklist]], [[project_aurora_i_cover_reni_feedback]], [[project_aurora_ii]]).
