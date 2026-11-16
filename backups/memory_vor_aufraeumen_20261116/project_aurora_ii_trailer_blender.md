---
name: project_aurora_ii_trailer_blender
description: AURORA-II-Blender-Trailer – Zwischenstand 15.10.26 gesichert in Bolla\AURORA II\7_Trailer (Videos, Skripte, Ideen)
metadata:
  type: project
---

Zwischenstand 15.10.2026, Chris: „nicht schlecht, unbedingt merken“. Ablage: `D:\OneDrive\Dokumente\Bolla\AURORA II\7_Trailer\` (2 Videos: 10-s-Korridor-Test mit Smiley, 30-s-Gesichtsversion; Skripte, Wrapper, README). Desktop\temp-Kopien gelöscht.
Gesicht = AURORA-I-Cover (~18k Lichtpunkte), Orange→Smaragd. Blender 4.5.9, Eevee Next, Kamera-Falle: Blick −Y = rotation (90°,0,180°).
**Why:** Perspektive ~3-Min-Video mit Song (Suno, später) + QR-Code. **How to apply:** Weiterbauen aus den Skripten dort; Chris-Feedback zum Gesicht (Aufleuchten, Dunkelseite) einholen. Siehe [[project_aurora_ii_song_qr]], [[project_blender_3d]].

**Chris 16.10.2026 (Ziel):** Das ZIEL-Bild ist das Mädchen-Gesicht vom AURORA-II-Cover (aus Punkten, nicht scharf); Start = orange Cover I als Punkte. Das soll mit dem **Korridor** kombiniert werden. Punkte-Morph-Versuch v1 (`C:\Tools\blender_proj\aurora_bg.py`, Wrapper `scripts/blender_aurora_bg.sh`, Ganz-Cover-Raster 41k Punkte): „nicht so toll" (Gesicht I zu flau). Nächster Versuch: Gesicht-Crop statt ganzes Cover, mehr Kontrast, in `trailer_face.py`-Korridor einbauen.
**Wichtig:** Heute (16.10.) NICHT mehr auf Zuruf starten — Chris meldet sich selbst. Siehe [[project_aurora_ii_song_qr]].
**Präzisierung Chris 16.10.:** „Nicht scharf" = weich/aus Pünktchen, aber das Gesicht muss klar ERKENNBAR sein — in den Vorschauen war es das kaum. **Why:** Ganz-Cover-Raster (160×256) gab dem Gesicht zu wenig Punkte + zu wenig Kontrast. **How to apply:** Nur Gesichts-Crop, deutlich dichteres Raster (Gesicht ≥150 Punkte breit), Kontrast/Gamma erhöhen; bei Vorschau-Stills zuerst prüfen, ob das Gesicht auf Anhieb erkennbar ist, bevor ein Voll-Render startet.

**18.10.2026 Video-Neuaufbau (Chris-Auftrag, 3 min):** Cover I klein in der Röhre → nach hinten/größer → Explosion → Cover II **scharf aus 256k Kacheln** (statt weicher Punkte; Gesicht klar erkennbar, Stills geprüft). Skript `C:\Tools\blender_proj\aurora_video\aurora_video.py`, Wrapper `scripts/blender_aurora_video.sh`. Lehre: Kacheln (Quads, 1,5 px/Zelle) + Rang-Zuordnung nach Helligkeit liefern scharfe Morphs; Plane+Textur für die Flugphase. Eevee ~1–1,6 s/Bild.

**Umbau 21.10.2026 (Chris):** Ordner heißt jetzt `Bolla\AURORA II\7_Trailer` (Video + Song werden zum Trailer kombiniert). Struktur: `Video\` (v5 + _Arbeitsstand_Quervideo_v5), `Song\` ([[project_aurora_ii_song_qr]]), `_Archiv_alte_Versionen\` (frühe Tests, nichts gelöscht), `LIES_MICH.txt`. Wrapper/Aufräumskripte in workspace/scripts zeigen auf `7_Trailer/Video`. Desktop\temp-Kopie des v5-Videos gelöscht.
