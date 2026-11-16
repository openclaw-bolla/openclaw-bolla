---
name: feedback-ppt-fertig-ablage-privat
description: Standard-Workflow für Foto+Text-Karten (Geburtstag etc.): PPTX mit Foto + Textfeld zum Selbstpositionieren, Druck hochaufgelöst, bei "fertig" PPTX nach Office\KI\Privat und Hilfsbilder löschen
metadata:
  type: feedback
---

**Standard-Workflow (von Chris am 03.10.2026 bestätigt: "hat sehr gut geklappt, das machen wir ab jetzt immer so"):**
Bei Karten/Bildern mit Text auf einem Foto (Geburtstagskarte, Gruß etc.):
1. **NICHT** Text per Skript auf dem Foto positionieren/perspektivisch verzerren (klappt bei mir nicht, Chris/Reni waren 3× unzufrieden).
2. Stattdessen **PPTX** bauen (python-pptx): Folie in Zielformat (10×15 = 15×10 cm), Foto randlos vollflächig (Zuschnitt + dezente Optimierung: Schatten leicht heben, Kontrast/Sättigung max. +7 %), **Text als echtes Textfeld davor** mit gewünschter Schriftart/Farbe/Schatten. Chris positioniert/dreht selbst.
3. Ablage zum Bearbeiten: `D:\OneDrive\Desktop\temp`, nach dem Schreiben per powershell `LastWriteTime` anfassen (Sichtbarkeit).
4. Chris exportiert PNG → ist niedrig aufgelöst (~567×378). **Zum Drucken** Layout (Position/Drehung/Schrift aus der PPTX lesen) in 2400×1600 nachrendern, per Überlagerung gegen Chris' PNG prüfen, dann mit `print_foto_10x15.ps1` drucken ([[reference_hp_foto_10x15_druck]]).
5. Sagt Chris **"fertig"**: PPTX per powershell `Move-Item` nach `D:\OneDrive\Dokumente\Office\KI\Privat` (Ordner existiert) und ALLE von mir erzeugten Hilfsbilder/Zwischenstände löschen (Karte_V*, Druck-PNG, Scratchpad). Chris' eigenen PNG-Export nicht ungefragt löschen.

**Why:** Chris will Desktop\temp sauber, Endablage zentral, und selbst das Positionieren kontrollieren. Siehe auch [[feedback_ppt_direkt_bearbeiten]], [[feedback_foto_zuschnitt_praezision]].
**How to apply:** Gilt ab jetzt immer für solche Aufträge, ohne Rückfrage. Hängende Alt-Druckjobs vorher kurz prüfen (nur nach Rückfrage entfernen).
