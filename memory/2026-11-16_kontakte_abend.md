# 16.11.2026 abends — Kontakte (Outlook) final
- Neue Kontakte hatten leeres `fileAs` → Outlook sortierte sie nach vorne. 6 per Graph-PATCH repariert; `outlook_gmail_sync.py` setzt fileAs bei Neuanlage.
- Visitenkarten-Ansicht (Classic Outlook) zeigt Fotos >~64 KB / >256 px nicht → 55 Kontakte per Outlook-COM (RemovePicture/AddPicture/Save) auf 256 px gesetzt. kb-Skripte (`kontaktfoto_neu.py`, `kontaktfoto_import.py`, `kontaktfoto_nachbesserung/analyze.py`) auf 256 px umgestellt.
- Chris: „endlich nach Jahren eine stimmige Kontaktkachel für alle — alle sind da“.
- Backups: `backups/kontaktfotos_20261116_grossbilder/` (Originale), `backups/kontakte_fileas_vorher_20261116.json` (alle privat, nicht ins Git).
- Aufgeräumt: Scratch-Dateien (cs.json, Fotos), Desktop\temp\Kontaktfotos_Abhakliste.docx gelöscht.
