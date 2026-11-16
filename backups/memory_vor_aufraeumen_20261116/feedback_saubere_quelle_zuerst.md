---
name: feedback-saubere-quelle-zuerst
description: "Vor dem Reparieren eines kaputten Artefakts IMMER prüfen, ob eine saubere Ausgangsquelle existiert"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3ba6c459-309a-43a0-8694-24a67bad9562
---

# Erst saubere Quelle suchen, dann reparieren — nicht am kaputten Ergebnis herumoperieren

Beim AURORA-Cover (20./21.06.2026) sollte ich den Autorennamen verschieben. Ich habe zunächst lokal am fertigen, bereits verkorksten Portrait herumretuschiert (Name im engen, geister-verseuchten Bild verschoben) — Chris fand das Ergebnis zurecht unbefriedigend. Die saubere, textlose Basis (`cover_v6.png`) lag die ganze Zeit da; daraus neu aufgebaut war es in einem Rutsch gut (Variante V2).

**Why:** Klassischer Tunnelblick — das offensichtliche Teilproblem (Name) sofort am sichtbaren Artefakt flicken, statt einen Schritt zurückzutreten und das Gesamtbild + die verfügbaren Rohquellen zu prüfen. Das kostet Chris einen unnötigen Korrekturzyklus.

**How to apply:** Bei jeder Aufgabe an einem abgeleiteten/gerenderten Artefakt (Cover, Bild, PDF, generiertes Dokument, Build-Output) ZUERST fragen: „Gibt es eine sauberere/frühere Quelle, aus der das entstanden ist?" Lieber sauber neu erzeugen als am Endprodukt herumdoktern. Verfügbare Assets (Backups, textlose Basen, JSON-Quellen, Roh-Layer) vor dem ersten Eingriff sichten. Verwandt: [[project-aurora-hardcoded-blocks]] (Quelle = JSON, nie das Skript), [[feedback-cleanup]].
