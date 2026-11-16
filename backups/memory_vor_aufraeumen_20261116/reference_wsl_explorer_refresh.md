---
name: reference-wsl-explorer-refresh
description: "Windows Explorer zeigt neue Dateien nicht sofort, wenn Bolla aus WSL heraus in einen bereits offenen Ordner schreibt — F5 hilft"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6167270a-1e2c-4d44-ab09-4b3226e4baf5
  modified: 2026-08-23T17:37:56.367Z
---

Wenn ich (Bolla/WSL) Dateien in einen OneDrive- oder sonstigen Windows-Ordner schreibe, den Chris gerade in einem offenen Explorer-Fenster anschaut, tauchen die neuen Dateien dort oft nicht automatisch auf.

**Warum:** Die Windows-↔WSL-Dateibrücke (9P-Protokoll) löst die normalen Windows-Dateisystem-Benachrichtigungen (`ReadDirectoryChangesW`), auf die Explorer für Live-Updates lauscht, nicht zuverlässig aus.

**Beobachtet:** 23.08.2026 — 150 Dateien (Kilimanjaro-WhatsApp-Archiv) per WSL/ADB nach `Mandels/Robin/23-24/Kilimanjaro/` geschrieben, Chris sah im offenen Explorer-Fenster nur ~30 davon. Fix: F5 / Ordner neu öffnen → alle da, keine Dateien fehlten tatsächlich.

**How to apply:** Wenn Chris nach einer Datei-Schreibaktion aus WSL meldet, dass Dateien fehlen/unvollständig aussehen → ERST selbst auf der Linux-Seite (`ls`) die tatsächliche Anzahl/Vollständigkeit gegenchecken, bevor an einen echten Fehler geglaubt wird. Meist ist alles da, nur Chris' Explorer-Fenster ist veraltet. Als Erklärung/Fix direkt "F5 drücken oder Ordner neu öffnen" vorschlagen.
