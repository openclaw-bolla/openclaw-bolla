---
name: reference-onedrive-mandels-pfad
description: "Korrekter Zielpfad für Mandels-Familienfotos in OneDrive — OHNE 'Bilder\' davor, sonst landen Dateien in einem unsichtbaren Zweit-Ordner"
metadata:
  node_type: memory
  type: reference
  originSessionId: current
  modified: 2026-09-07T09:55:00.000Z
---

# Korrekter Pfad für Mandels-Familienfotos

**Richtig:** `D:\OneDrive\Mandels\<Jahr>\...` — Mandels liegt DIREKT unter der OneDrive-Wurzel, NICHT unter `Bilder\`.

**Falsch (Falle, 06.–07.09.2026 passiert):** `D:\OneDrive\Bilder\Mandels\<Jahr>\...` — sieht auf den ersten
Blick logisch aus (Familienfotos → "Bilder"-Ordner), ist aber ein zweiter, praktisch leerer Ordner, den
Chris nie öffnet. Dort landete am 06.09. abends die Lüneburger-Heide-Archivierung — Chris fand die Fotos
am nächsten Morgen nicht, weil sein Explorer-Fenster den ECHTEN `Mandels\2026`-Ordner offen hatte.

**Wie es aufgefallen ist:** ~90 Minuten Fehlersuche in die falsche Richtung (Modern-Standby-Theorie,
OneDrive-Sync-Engine-Restart, natives PowerShell-Rename/Copy, Explorer.exe-Neustart, sogar ein Fund in
`healingItems.txt` zu einem unabhängigen Bolla-Backup-Sync-Fehler) — erst `find /mnt/d/OneDrive -type d
-iname "2026"` zeigte zwei Treffer und damit den echten Fehler.

**Beleg, dass `Mandels\2026` (ohne Bilder\) der aktiv genutzte Ordner ist:** enthält u.a. "Anne und Bene
bei uns", "Essen und Trinken", "Vitalia Neu" sowie das Kilimanjaro-Foto vom 23.08.2026 — passt exakt zum
damaligen Zielpfad `Mandels/Robin/23-24/Kilimanjaro/` aus [[project_handy_foto_zwischenablage]], der
ebenfalls ohne "Bilder\" auskommt.

**How to apply:** Vor JEDER künftigen Foto-Archivierung nach `Mandels\...` erst mit `find` oder `ls`
gegenchecken, dass der Zielordner bereits existierende, plausible Chris-Inhalte hat (nicht nur leer
anlegen und hoffen). Bei Unsicherheit über den Basispfad lieber einmal mehr nachschauen als einen
Parallelordner erzeugen. Verwandt: [[project_foto_organisation]], [[feedback_foto_tagesausflug_workflow]].
