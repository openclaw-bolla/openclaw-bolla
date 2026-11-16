---
name: feedback-zielebene-windows-android
description: Lösungen auf der NATIVEN Zielebene bauen (Windows/Android), nicht aus WSL fummeln — der Kommunikationskanal ≠ die Ausführungsebene
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
---

⭐ **Der WSL-Terminal ist nur unser GESPRÄCHSKANAL — die eigentlichen Aktionen passieren fast immer auf der Windows- oder Android(Handy)-Ebene.** Beim Lösungsdesign IMMER zuerst auf der nativen Zielebene denken, nicht aus WSL heraus etwas erzwingen.

**Why:** Der instinktive Reflex „der WSL-Prozess/Server macht das" führt regelmäßig in Gefrickel-Sackgassen — WSL ist headless Linux ohne Draht zur Windows-GUI und ohne Bezug zum Handy. Konkretes Beispiel (24.06.2026): BildGen-Ordnerwahl. Erst als „Server (WSL) öffnet Ordner-Dialog" gedacht → unmöglich/fummelig. Lösung war die Ebene zu wechseln: der **Browser auf Windows** öffnet den nativen Ordner-Dialog (`showDirectoryPicker`). Server muss gar nichts. Chris' Regel dazu: „lass jedes Gefrickel weg".

**How to apply — bei jeder Aktion zuerst fragen: WO passiert das wirklich?**
- **Windows-Ebene** (Edge/Browser, Explorer, Office, Dateien, Dialoge, Zwischenablage): nativ lösen — Browser-APIs (File System Access, Clipboard), `clip.exe`, `explorer.exe`, PowerShell/Registry, `.lnk`/AutoHotkey. NICHT versuchen, einen Windows-GUI-Dialog aus WSL aufzupoppen.
- **Android-Ebene** (Handy/Duo/P20): Aktionen müssen am Gerät selbst klickbar sein → Links/Pfade ins gclip ([[rules-kritisch]] gclip-Regel), nicht ins Studio-Terminal. Folder-Picker & Co. am Handy ggf. anders/nicht verfügbar → Fallback mitdenken.
- **WSL-Ebene** ist nur für: mit Chris reden, Dateien/Skripte/Server/Cron verwalten, Backend-Logik. Sie ist Mittel zum Zweck, selten der Ort der Endaktion.
- **Faustregel:** Wenn eine Lösung WSL→Windows-GUI-Brücken oder exotische Tricks braucht → Stopp, falsche Ebene. Es gibt fast immer einen sauberen nativen Weg auf der Zielebene. Gefrickel = Signal, neu anzusetzen.

Verwandt: [[feedback-windows-ui]] (Registry/PowerShell statt fixer UI-Pfade), [[feedback-copy-from-terminal]] (clip.exe), [[feedback-datei-dialog-anweisung]], [[reference-mc]].
