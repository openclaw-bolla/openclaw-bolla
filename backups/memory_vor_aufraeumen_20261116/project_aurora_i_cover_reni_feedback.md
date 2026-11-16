---
name: project_aurora_i_cover_reni_feedback
description: AURORA-I-Cover-Verbesserungen nach Renis Feedback (16.10.26): Wraparound, heller, Rückseite lesbarer, Titel „AURORA I“
metadata:
  type: project
---
Reni (fertig gelesen) schlägt vor: Vorderbild über Rücken bis Rückseite durchziehen (nur oberer Lichteinfall), Taschenbuch heller, Rückseitentext größer + breitere Ränder links/rechts, Titel „AURORA I“. Datei: `Bolla\AURORA\7_Cover_Verbesserung_Reni\Cover_Verbesserungen_Reni_2026-10-16.md`.
**Why:** Chris: „kleinere Projektidee“, nur merken (noch nicht umsetzen). **How to apply:** Auf Zuruf umsetzen; vorher [[project_aurora_update_checklist]] und [[feedback_kdp]] lesen. Zweite Projektidee: von Chris 21.10.2026 vergessen, Punkt gestrichen.

**✅ ERLEDIGT 19.10.2026:** Neues Wraparound-Cover (DE+EN, „AURORA I", Rückenschrift groß unten→oben, Szene über Rücken, heller, Rückseite 13,4 pt) von Chris freigegeben und eingespielt: `Bolla\AURORA\3_Taschenbuch\2_DE_Cover.pdf` / `4_EN_Cover.pdf`, `2_eBook\AURORA_Cover.jpg` + beide EPUBs (cover.png getauscht), Quellen+Skript `4_Cover_Quellen\build_cover.py` (Aufruf `de 460 <outdir> I` / `en 441 <outdir> I`). Alte Fassungen: `workspace/backups/aurora_cover_vor_I_20261019/`. **OFFEN: Upload KDP (Print DE/EN + eBook DE/EN), D2D, Google Play** — Chris klickt geführt; ⚠️ Titelfeld „AURORA I" zu Cover passend prüfen (Amazon gleicht Cover-Titel mit Metadaten ab).

**Chris 19.10.:** Titel „AURORA I" mit schlichtem Orbitron-I (wie die anderen Buchstaben). Ein Serifen-I (Querbalken) gefiel ihm NICHT — nicht wieder vorschlagen.
**Chris 19.10. (später):** „I" steht wie bei Band II ZENTRIERT UNTER „AURORA" (~64 % Titelgröße, y≈468/2560), nicht rechts daneben; Rücken bleibt „AURORA I" in einer Zeile. Aktueller Stand in Bolla\AURORA eingespielt.
**Chris 19.10. (abends):** Naht-Korrektur auch für Band I gewählt („korrigiert nehmen"): Wrap-PDFs 2_DE_Cover/4_EN_Cover neu eingespielt (Bild läuft durchgehend über den Rücken). build_cover.py: `MIRROR_FIX` jetzt Standard für beide Bände (=0 nur für alten Stand). eBook-Front/EPUBs unverändert. Taschenbuch-Upload (KDP) → mit diesen PDFs.
