---
name: project-aurora-ii-cover
description: AURORA II Cover — Stand 09.10.2026 (Skizze v1h), Entscheidungen, Dateien, Weiterarbeit (Blender-Basis + Cloudflare-Gesicht + MAI-Figuren + Orbitron-Typo)
metadata:
  type: project
---

**Stand 09.10.2026:** Cover-Skizze **v1h** ist „soweit in Ordnung" (Chris). Weiterarbeiten später (nicht dringend, kein Zeitdruck — [[feedback_projekte_entspannt]]). Farbwelt/Hintergrund: [[project_aurora_ii_farbwelt_nordlicht]], Blender-Setup: [[project_blender_3d]], Song/QR: [[project_aurora_ii_song_qr]].

## Entscheidungen (Chris)
- **Richtung V1:** Serverkorridor wie Band I, aber kühl: Racks mit türkis/blau/smaragd/(selten magenta) LEDs, spiegelnder Boden, 7 „Stufen-Lichter" (Abstände halbieren sich = Zeitregime) hinten im Korridor.
- **Nordlicht:** großflächig, weich, mit feinen senkrechten Strahlen (Chris: „reale Nordlichter sind flächiger", streifig/schwarze Löcher = unschön). Zwei große Vorhänge über dem Korridor; Kante darf nicht durchs Auge laufen. Bezug im Buch nur über die Vorspann-Definition („Das Nordlicht verändert sich, während man es ansieht"), Kapitel enthalten kein „Nordlicht" (geprüft 09.10.).
- **AURORA = Gesicht im Vorhang**, analog Band I (dort frontal, mittig). Hier Profil/3⁄4, **Blick nach RECHTS** (zu Marlie+Leni), Gesicht leicht links der Mitte; Lippen nicht zu rot (natürlich blass); Gesicht per Screen-Blend, Nordlicht dahinter abgedunkelt.
- **Marlie+Leni unten RECHTS** (wie Marlie in Band I), schauen nach links zu den Monitoren. MAI-Image-2.5, 3 Versuche (~0,30 €), gewählt `figuren_mai3.png` (Marlie Zopf+Lederjacke vorn, Leni mit Brille grinsend), Alternative `figuren_mai1.png`.
- **Typo wie Band I EXAKT:** Orbitron Bold, „AURORA" 1080/1600 px breit, Mitte y=300/2560; Autor „Chris Mandel" Orbitron SemiBold 560 px breit, y=2410. **Titelfarbe MINT** (215,250,240) statt Gold. **„II" zentriert UNTER dem Titel**, ~55 % der Titelgröße (rechts daneben würde zu breit).
- Skizzenmaßstab 800×1280 (= halber Endmaßstab 1600×2560 wie KDP-Cover Band I).

## Update 09.10.2026 abends (v2a)
Chris-Kritik an v1h: Figuren zu groß, Lichter am Korridorende = weiße Kleckse (sollen 7 saubere mint Stufenpunkte werden), Pünktchen an Rack-Enden = Rauschen, Bodenverlauf-Fleck, Vorhangkanten hart, „II" auf Stirn. Marlie Braun ist 36, Leni Hoffmann 27 (Alter passt). Stimmung beschlossen: **B + Monitor-Türkislicht** (Marlie schaut hoch zum Nordlicht-Gesicht, Leni grinst auf Schirm; keine lesbare Textzeile — auf Thumbnail nicht erkennbar). Neue Figuren via MAI (`figuren_neu1/3.png`, gespiegelt, 360×480 bei (395,690)); `composite2.py <out> <fig>`; **v2c** = neu1 + Blender-Fix (7 Lichter mint in Augenhöhe y=13..29, hintere Rack-LEDs ruhiger, Bodenlampe 120 W, Boden rough 0.2) → **v2d (10.10.)** = aktuelle Skizze: Rack-Rahmen (Blender), Figuren 285×380 bei (440,770), Gesicht 13° nach unten gekippt (Blick zu Marlie), pos (70,148), Hintergrund hinter Gesicht stärker abgedunkelt (0.85) → Vorhangkante nicht mehr durchs Auge, „II" im Dunkeln. Chris hat v2d noch nicht freigegeben; Endrender 1600×2560 erst nach OK. Noch offen: Lichter/Pünktchen/Boden/Kanten/Gesicht „aus Licht"/„II" verschieben, Endrender.

## Dateien
- Arbeitsordner: `C:\Tools\blender_proj\cover\` (WSL `/mnt/c/Tools/blender_proj/cover/`): `composite.py` (setzt alles zusammen → `python3 composite.py skizze_vX.png`), `skizze_v1d.png` (Blender-Basis ohne Gesicht), `gesicht_neu2.jpg` (Cloudflare FLUX), `figuren_mai1/3.png`, `skizze_v1h.png` (aktuelle Gesamtskizze, auch `Desktop\temp\AURORA2_Cover_Skizze_v1h.png`).
- Blender-Szene: `C:\Tools\blender_proj\cover_skizzen.py -- v1d [W H SAMPLES]` (Prozedural: Racks aus Quadern+LED-Quadern, Aurora-Material = gewellte Fläche + Noise-Alpha + Farbverlauf Smaragd→Türkis→Magenta, Kamera 24 mm). Render 800×1280/48 Samples ≈ 1–2 min (RTX 4050, OptiX).
- Typo-Font: `workspace/fonts/orbitron/Orbitron-var.ttf` (`set_variation_by_name("Bold"/"SemiBold")`). Band-I-Vorlage: `scripts/aurora_cover_finalize_v2.py`.
- **Sicherung (OneDrive):** `Dokumente\Bolla\AURORA II\4_Cover_Quellen\Cover_Quellen_aktuell\` (Skripte, Gesicht, Figur neu1, v1d/v2d, Font) — Stand 09.10. abends v2c.

## Offen / nächste Schritte
1. Autorenname überlappt das Pult → Name oder Figuren verschieben; Marlie sitzt zu dicht am rechten Rand → Figuren etwas nach links.
2. Kanten der Vorhänge hinter/neben dem Gesicht weicher; Fleckentextur auf der Wange (Nordlicht-Struktur scheint durch).
3. **Endrender 1600×2560** (Blender `-- v1d 1600 2560 128`), `composite.py` auf Skalierfaktor 2 umstellen (aktuell fest 800×1280); MAI-Figur (864×1152) hochskalieren (Pillow LANCZOS + sanfte UnsharpMask 80) oder größer neu erzeugen; Gesicht ebenfalls hochskalieren.
4. Gesicht evtl. noch mehr „aus Licht" (stärker mit Vorhang verschmelzen); Frage: bleibt Gesicht echtes Porträt?
5. Rückcover/Buchrücken/QR-Platzierung ([[project_aurora_ii_song_qr]]); KDP-Maße wie Band I ([[project_aurora_update_checklist]]).
6. Aufräumregel: ungenutzte Entwürfe sofort löschen ([[feedback_cleanup]]); MAI/Gemini-Terminalaufrufe ins Kostenbuch (`kosten_add.py`), über `/api/bildgen` automatisch.

**Cloudflare-Falle:** Prompts mit Altersangaben („sixteen", „teenage") → HTTP 500; neutral formulieren („young woman"). MAI erzeugt 864×1152 für 3:4.

## Update 10.10.2026 — FINAL gerendert (Chris-Freigabe v2e + „Punkte mit Schein")
Endrender 1600×2560 fertig: `Bolla\AURORA II\4_Cover_Quellen\AURORA2_Cover_FINAL_1600x2560.png`. Quellen (cover_skizzen.py, composite3.py mit Skalierfaktor K + Gangende-Schein, skizze_v1d_1600.png, Figuren/Gesicht, Orbitron) in `Cover_Quellen_aktuell`. Gesicht 35 px nach links (pos 35,148). Offen: Rückcover/QR, KDP-Maße/Rücken; Gesicht/Figuren sind auf 864×1152 MAI-Basis hochskaliert (leicht weich) — bei Bedarf Upscale prüfen.

## ⏳ MERKEN (Chris 10.10.2026): Buchrücken + Rückcover noch zu machen
Front ist FINAL. Offen: Buchrücken (Taschenbuch/KDP, Rückenbreite nach Seitenzahl, Titel/Autor/Logo), Rückcover (Klappentext, QR, Barcode-Fläche) wie bei Band I (`Bolla\AURORA\4_Cover_Quellen` als Vorlage). Vorher Upscale von Gesicht/Figuren für Druck prüfen. Erst Buch-Endphase (Seitenzahl bekannt), Song/QR siehe [[project_aurora_ii_song_qr]]. Bei Cover-Thema proaktiv erinnern.

## ✅ 10.10.2026 abends — Kanten weicher, FINAL = v3, aufgeräumt
Chris: dunkle Fläche links über „AU", Fläche rechts vom linken Auge und Spitze unter dem Kinn waren zu eckig/„Bergspitze"; gerade steile Kante über dem „U" unnatürlich für Nordlicht → Nordlicht-Ebene lokal weichgezeichnet (`composite_final.py`, `soften_regions`). **`AURORA2_Cover_FINAL_1600x2560.png` ist jetzt die Version mit weichen Kanten** (Chris: „so lassen wir es erst mal"). Alte Fassung, Arbeitsordner `C:\Tools\blender_proj\cover\` und Zwischenbilder gelöscht. **Einzige Quellen jetzt:** `Bolla\AURORA II\4_Cover_Quellen\Cover_Quellen_aktuell\` (composite_final.py, cover_skizzen.py, figuren_neu1.png, gesicht_neu2.jpg, skizze_v1d_1600.png, Orbitron) — Skripte brauchen die Dateien im selben Ordner. Rücken + Rückcover weiter offen.

**19.10.2026 — Wraparound-Vorlage Band II (Reni-Verbesserungen übertragen):** `Bolla\AURORA II\4_Cover_Quellen\build_cover.py` (gleiches Skript wie Band I, Parameter `<de|en> <Seiten> <outdir> II`) + textfreie Basis `AURORA2_Cover_ohne_Text_1600x2560.png` (pixelgenau rekonstruiert aus composite_final.py ohne Typo-Block). Enthält: Szene läuft über Rücken auf Rückseite, mild aufgehellt, großer Rücken „AURORA II" (unten→oben), Rückseitentext ~14,9 pt mit breiten Rändern, „II" zentriert unter Titel. **Zum Veröffentlichen fehlen:** (1) `workspace/data/klappentext_ii_de.txt` (+ `_en`) — Skript nimmt sonst Platzhalter; (2) ECHTE Seitenzahl (Schätzung ~694 DE nach Wortzahl 158.9k vs. Band I 105k/460 S.; Rücken ~1,74"), danach Skript neu laufen lassen; (3) EPUB-cover.png tauschen wie bei Band I. Vorschau lag in Desktop\temp (Platzhaltertext). Nicht vergessen: Klappentext II schreibt/prüft Chris erst gegen Buchende (Spoiler-Schutz, [[feedback_aurora_ii_chris_lesestand]]).

**19.10.2026 Naht-Korrektur:** Chris sah scharfe Kante rechts am Rücken (Wrap II). Ursache = Bug im Spiegel-Anfügen (an der Naht lag der RECHTE statt der LINKE Frontrand). Fix `MIRROR_FIX` in build_cover.py: für Band II standardmäßig an (+ weichere Rückenabdunklung/Glocke, unteres Ausblenden langsam). Band I läuft weiter im ALTEN Stand (freigegeben, im KDP-Upload) — Korrektur nur per `MIRROR_FIX=1`; Vergleichsbild lag in Desktop\temp, Chris entscheidet (Neu-Upload nötig).
**19.10. Rückenschrift:** Chris: Band II wirkte größer als I → Schrifthöhe auf dem Rücken jetzt absolut gedeckelt (172 px ≈ 0,57"), gilt für beide Bände (Band I pixelgleich geblieben). Bei dicker Rückenbreite wächst die Schrift nicht mehr mit.
**19.10. (abends):** Chris: Wrap-Vorlage II „gefällt mir gut" → als `Bolla\AURORA II\AURORA_II_Cover_Wraparound_Vorlage.jpg` (Hauptverzeichnis, Platzhaltertext!) abgelegt. Band I nutzt jetzt dieselbe Naht-Korrektur.
**19.10. Untertitel Band II:** noch NICHT festgelegt (aurora2.json untertitel leer). Chris fragte, ob er schon in der Beschreibung von Band I erwähnt werden soll → Empfehlung/Entscheid: nein, erst festlegen wenn Ende/Ton stehen; Ankündigungssatz „AURORA II erscheint noch in diesem Jahr" reicht; Untertitel später in Beschreibungen (KDP/D2D/Google) + Website nachtragen. Vorschläge spoilerfrei machen ([[feedback_aurora_ii_chris_lesestand]]).
