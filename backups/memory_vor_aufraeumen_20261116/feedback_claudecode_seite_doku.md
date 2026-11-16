---
name: claudecode-seite-doku-sync
description: "Wenn Inhalte der Claude Code Seite in MC geändert werden, Doku-Box in index.html mitpflegen"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 67df5b73-aed6-4770-b53c-31d5403c9ba1
---

# Regel: Claude Code Seite → Doku-Box synchron halten

Immer wenn sich Inhalte auf der Claude Code Seite in MC inhaltlich ändern (neue Dokumente, umbenannte Dokumente, gelöschte Dokumente), muss die GROUPS-Liste in `loadBollaProjects()` / `loadDocumente()` in `index.html` ebenfalls aktualisiert werden.

**Why:** Sonst zeigt MC veraltete oder nicht-existente Dateien in der Doku-Box an (404-Klicks).

**How to apply:**
- Neue Datei im Doku-Ordner anlegen → Dateinamen in passende Gruppe in GROUPS eintragen
- Datei umbenennen → alten Namen in GROUPS suchen und ersetzen
- Datei löschen → aus GROUPS entfernen
- GROUPS liegt in `index.html` ca. Zeile 6357–6364

**Doku-Ordner:** `D:\OneDrive\Dokumente\Bolla\claud code - openclaw Doku\`
