---
name: reference-pptx-com-grosse-dateien
description: "PowerPoint-COM-Automatisierung bei großen PPTX (>1GB, viele Videos) ist unzuverlässig — Lehren aus Kurstag-6-Umbau 29.09.2026"
metadata:
  node_type: memory
  type: reference
  originSessionId: 71704f40-e2fe-437b-85ec-c3521abeaa99
  modified: 2026-09-29T13:25:43.368Z
---

Beim Umbau von `06-Basics Office Videos-Clipchamp.pptx` (1,17 GB, viele eingebettete Videos) über
PowerShell + PowerPoint-COM traten mehrere hartnäckige, schwer diagnostizierbare Fehlerquellen auf.
Für **künftige Bearbeitung großer PPTX-Dateien per Skript** merken:

**1. Deutsche vs. englische Shape-Namen:** python-pptx liest den in der XML gespeicherten Namen
(z. B. „Textfeld 3", „Rechteck 7" — von deutscher PowerPoint-UI vergeben). COM auf diesem Rechner
(englische PowerPoint-Installation) zeigt bei `.Name` für **manche** dieser Shapes stattdessen einen
lokalisierten Alias (z. B. „TextBox 3", „Rectangle 7"), für andere wieder den Original-Namen — nicht
vorhersehbar welche. Ein per COM geschriebenes Namens-Matching (`$shape.Name -eq "TextBox 3"`) kann
deshalb **grundlos ins Leere laufen oder falsch matchen**, je nach Moment/Shape.

**2. Geometrie-Änderungen (Left/Top/Width/Height) und manchmal sogar Text-Änderungen per COM gehen
bei dieser großen Datei öfter „verloren"**, obwohl das Skript die Zeile fehlerfrei durchläuft und
"OK"/Erfolg loggt. Kein klares Muster gefunden (nicht zuverlässig an `.Duplicate()`, Batch-Größe oder
Slide-Position festzumachen) — wirkt wie eine COM-interne Race Condition bei sehr großen/video-lastigen
Präsentationen.

**3. Der PNG-Export-Weg zur Sichtprüfung** (`pptx_slides_to_png.ps1`, PowerPoint-COM `.Export()`) kann
ebenfalls **veraltete/gecachte Inhalte** rendern, wenn kurz zuvor mehrere COM-Sessions geöffnet/
geschlossen wurden — ein bereits korrekt gespeicherter Zustand wurde mehrfach fälschlich als „immer
noch kaputt" angezeigt. Abhilfe: kompletten `POWERPNT.exe`-Prozess killen, ein paar Sekunden warten,
in einen **frischen/neuen Ausgabeordner** rendern (nicht denselben überschreiben).

**Empfohlenes Vorgehen für künftige große-PPTX-Skriptaufträge:**
- **Ground Truth ist python-pptx, nicht COM/Renderings.** Nach jeder Änderung den tatsächlichen
  Dateiinhalt per python-pptx (`shape.top/left/width/height`, `shape.text_frame.text`) direkt
  auslesen — das liest garantiert die echten, gerade gespeicherten Bytes, ohne COM-Zwischenschicht.
- **Für reine Text-/Geometrie-Edits ohne neue Folien/Bilder: python-pptx direkt verwenden statt COM.**
  Funktioniert bei dieser 1,17-GB-Datei zuverlässig und deutlich schneller (kein PowerPoint-Start
  nötig), sofern nur Text/Position/Schriftgröße geändert werden — eingebettete Videos/Bilder bleiben
  als unangetastete Parts erhalten. COM/PowerShell nur noch für Dinge nutzen, die python-pptx nicht
  kann (z. B. Folien duplizieren mit allen Animationen/Verknüpfungen 1:1, PDF-Export).
- Falls COM doch nötig ist: **ein Shape = ein volles Open/Edit/Save/Close-Zyklus**, keine Batches mit
  vielen Shapes in einer Session — deutlich zuverlässiger, wenn auch langsamer.
- Nach Abschluss **immer per python-pptx gegenchecken**, nicht nur auf das PowerShell-„OK"-Log
  vertrauen.

Siehe auch [[project_edv7_grossprojekt_powerpoint]] (Kontext des Kurstag-6-Umbaus) und
[[feedback_ppt_direkt_bearbeiten]] (Scope-Regel: nur Text in bestehende Folien, kein Redesign).
