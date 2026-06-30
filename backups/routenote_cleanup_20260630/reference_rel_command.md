---
name: reference-rel-command
description: "rel-Befehl — verschiebt fertigen Song + Cover in released/-Ordner, mit auto-Konvertierung 320kbps"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6f7a5017-294d-4876-8441-7eca934fd61a
---

`rel "<Songtitel>"` — Shell-Skript in `~/.local/bin/rel`

**Was es tut:**
1. Sucht `<Titel>_320.mp3` oder `<Titel>.mp3` im Song-Ordner
2. Konvertiert automatisch auf 320kbps/44.1kHz via ffmpeg (falls noch kein _320)
3. Verschiebt MP3 + `<Titel>_cover.jpg` in den `released/`-Unterordner

**Beispiel:** `rel "Seven more weeks"`

⚠️ **Veraltet seit RouteNote-Aus (24.06.2026):** Das Skript zeigte auf den gelöschten Ordner `…/Bolla/Suno_RouteNote/` und den entfernten `routenote_watcher.py`. Distribution läuft jetzt über DistroKid mit Ordner `…/Bolla/Suno_DistroKid/`. Falls `rel` wieder gebraucht wird: Pfad im Skript `~/.local/bin/rel` auf den DistroKid-Ordner umbiegen.
