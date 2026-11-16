---
name: reference-kuerzel-kb-kontaktbilder
description: Kürzel "kb" = neue Kontaktbilder aus OneDrive/Bilder/Kontaktbilder automatisch in Outlook+Google einbauen
metadata:
  type: reference
---

**Kürzel „kb“** (Chris, 12.11.2026) = neue Kontaktbilder einbauen. Ablauf: `python3 /home/bolla/workspace/scripts/kontaktfoto_neu.py` (vorher optional `dry`). Ohne Rückfrage ausführen, Ergebnis kurz melden.

- Nimmt nur NEUE/geänderte Dateien in `D:\OneDrive\Bilder\Kontaktbilder` (Stand: `scripts/kontaktfoto_state.json`).
- Zuordnung: exakter Name > Alias (`scripts/kontaktfoto_alias.json`, z. B. „reni“→Renate Mandel) > eindeutiger Vorname. Mehrdeutig/kein Treffer/mehrere Gesichter → wird nur gemeldet, dann Chris fragen und ggf. Alias bzw. `crops` (Box x0,y0,x1,y1) in alias.json eintragen.
- Zuschnitt quadratisch (Gesichtserkennung bei genau 1 Gesicht, sonst Mitte), setzt Outlook + Google-Foto direkt (kein Vollsync), Backup altes Foto in `backups/kontaktfotos_<ts>_neu/`.
- Erster Test: Reni.jpg → Renate Mandel (manueller Zuschnitt, Foto zeigt Reni+Chris). Ablösung für das ältere `kontaktfoto_import.py` (das nur exakte Vollnamen kann). Siehe [[project_kontakte_architektur]].
- **Seit 12.11.2026 (Chris-Wunsch):** Nach erfolgreichem Einfügen (Outlook UND Google) wird das Quellbild aus `Kontaktbilder` gelöscht (Kopie in `backups/kontaktfotos_<ts>_neu/quellbilder/`). Nur bei Erfolg; bei Warnung/Fehler bleibt die Datei liegen.
