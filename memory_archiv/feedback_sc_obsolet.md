---
name: feedback-sc-obsolet
description: sc-Befehl faktisch überflüssig seit Bolla Bilder direkt per Strg+V lesen kann
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 00128d31-85df-4b33-963d-11d5cdd28af8
  modified: 2026-08-12T07:16:58.559Z
---

`!sc` nimmt **keinen aktiven Screenshot** auf (das war eine falsche Annahme von Bolla, 12.08.2026) — es liest nur, was gerade in der Windows-Zwischenablage liegt (`Clipboard::GetDataObject`), und schreibt das als PNG-Datei nach `D:\OneDrive\Bilder\bolla_screenshot.png`. Chris muss also so oder so vorher selbst Win+Shift+S drücken.

**Why:** Seit Chris Bilder/Screenshots direkt per Drag&Drop oder Strg+V ins Claude-Code-Terminal einfügen kann, ist der Umweg über `sc` (Zwischenablage → Datei → Pfad ins Terminal tippen → Bolla liest Datei) ein überflüssiger Zwischenschritt geworden. Direkt einfügen ist ein Schritt kürzer und macht dasselbe.

**How to apply:** `sc` nicht mehr aktiv vorschlagen oder erklären, als würde es einen Screenshot "aufnehmen". Wenn Chris fragt, wie er mir was zeigt: einfach "Win+Shift+S, dann Strg+V hier rein" sagen. `sc`/[[feedback_sc_path]] bleibt als Fallback im Hinterkopf, falls Drag&Drop/Paste in der jeweiligen Umgebung mal nicht geht.
