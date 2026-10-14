---
name: project-bildgen-ordner
description: BildGen Wunsch-Feature — Zielordner frei wählbar beim Speichern
metadata: 
  node_type: memory
  type: project
  originSessionId: 15a49665-2efe-468c-a1eb-7159840d986d
---

Chris möchte beim BildGen-Download (⬇-Button) den Zielordner selbst auswählen können.

**Wunsch:** Ordner-Auswahl idealerweise direkt über den Windows-Explorer-Dialog (Folder-Picker).

**Why:** Aktuell wird immer fix nach `/mnt/d/OneDrive/Bilder/BildGen` gespeichert. Chris will flexibel wählen können.

**How to apply:** Wenn BildGen-Download verbessert wird: `window.showDirectoryPicker()` API im Browser (Chromium/Edge unterstützt das), oder alternativ über MC-API einen `POST /api/bildgen/save-to-disk` mit optionalem `folder`-Parameter + Server-seitiger Ordner-Auswahl via Dialog.

**Status:** ✅ UMGESETZT 24.06.2026. Gemeinsame Helper-Funktion `bgSaveBlob(blob,mime,forcePick)` in `index.html`: nutzt `window.showDirectoryPicker({id:'bildgen-save',mode:'readwrite',startIn:'pictures'})` → nativer Windows-Ordner-Picker in Edge/Chrome, merkt sich den Ordner über `_bgDirHandle` (Folge-Downloads ohne erneute Wahl), Link „anderer Ordner" erzwingt Neuwahl (`bgDownload(true)`). Fallback für Handy/alte Browser (kein showDirectoryPicker): bisheriger Server-Save `/api/bildgen/save-to-disk` (fester Ordner `/mnt/d/OneDrive/Bilder/BildGen`). Beide Buttons umgestellt: `bgDownload()` (Haupt) + `bgArchiveDownload()` (Archiv, via `_bgB64ToBlob`). Statische HTML → nur Strg+F5. Voraussetzung Picker: secure context — erfüllt über http://127.0.0.1 (localhost) + https-Tunnel. Chris testet noch, dann sw-06 auf ✅.
