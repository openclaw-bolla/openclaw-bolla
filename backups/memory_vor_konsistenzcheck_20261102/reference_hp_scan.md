---
name: reference_hp_scan
description: HP Drucker Scan-Zielordner auf dem Studio — wo landen Scans die ans Studio gesendet werden
metadata: 
  node_type: memory
  type: reference
  originSessionId: 5f210e9b-da95-44fc-9bf4-07ee48e1fad6
---

## HP Scan-Speicherort (Studio)

HP Smart legt Scans standardmäßig ab unter:

**`D:\OneDrive\Bilder\YYYY-MM-DD\`** (nach Datum sortiert, z.B. `2026-06-12\001.jpg`, `002.jpg`)

Ermittelt 2026-06-12 durch Suche nach frisch erstellten Dateien nach einem Scan-Vorgang.

Weitere (ältere, nicht mehr aktive) Scan-Ordner:
- `D:\OneDrive\Eigene Dateien\Documents\Scan_HP\` — letzter Eintrag Jan 2024
- `D:\OneDrive\Scans\` — existiert, aber leer
- `D:\OneDrive\Eigene Dateien\Documents\Scanned Documents\` — Windows Fax & Scan, alt

**Format:** JPG (nicht PDF), nummeriert (001.jpg, 002.jpg, ...)
