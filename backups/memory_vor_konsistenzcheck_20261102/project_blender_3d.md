---
name: project_blender_3d
description: Blender 4.5.9 auf dem Studio installiert (C:\Tools), Bolla steuert per Python headless; erstes Projekt "Aus 0 und 1 wird ein Bild" für den Unterricht (Kurstag 4 Codierung)
metadata:
  type: project
---

Chris (07.10.2026): Interesse an Claude+Blender (Robins Diss-Film `Dissertation/Film_v5_1080p.mp4`, 11 Min, Blender-3D, auf Robins altem PC mit ~3090 gerendert). Chris will ein kleines, feines Projekt, das Schülern "den Mund offen stehen lässt".

**Setup:** Blender 4.5.9 LTS portable unter `C:\Tools\blender-4.5.9-windows-x64\blender.exe` (SHA256 geprüft, winget gibt es nicht). Kein Claude-Desktop-Connector (Chris: keine Desktop-App, [[feedback_keine_desktop_app]]) – Steuerung per Python-Skript: `blender.exe -b -P skript.py`. Studio-GPU: RTX 4050 Laptop 4 GB, OptiX läuft. Projektordner `C:\Tools\blender_proj\`.

**Projekt 1:** `bits2pixel.py` – 16×16 Würfel mit leuchtenden 0/1, Welle deckt ein rotes Pixel-Herz auf (Kamera-Flug, 14 s, 1080p). Render-Wrapper `scripts/blender_render_bits.sh`; Ergebnis nach `Desktop\temp\Aus 0 und 1 wird ein Bild.mp4`; Status auf /jobs.

**How to apply:** Renderläufe im Hintergrund, Status über [[feedback_jobstatus_statt_telegram]]. 4-GB-VRAM beachten (keine riesigen Szenen). Ideen später: AURORA-Trailer ([[project_aurora_ii_song_qr]]), Wohnungs-Walkthrough, Unterricht (Codierung, Kurstag 4). Verwandt: [[project_robin]].
