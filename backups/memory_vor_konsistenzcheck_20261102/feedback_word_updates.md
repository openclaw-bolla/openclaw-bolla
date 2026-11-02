---
name: word-datei-update-vorgehen
description: Wie Word-Dateien (.docx) korrekt aktualisiert werden — Reihenfolge einhalten!
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b0f104b7-97a3-4ae8-a86e-722b13d75cfa
---

# Vorgehen bei Word-Datei Updates

**Why:** Mehrfaches Scheitern wegen falscher Reihenfolge und fehlender Strukturanalyse (Mai 2026).

**How to apply:** Immer diese Reihenfolge einhalten:

## 1. Erst fragen: Ist die Datei in Word offen?
- Wenn ja: Chris bitten sie zu schließen, BEVOR irgendwas gemacht wird
- Lock-File prüfen: `ls /mnt/d/.../~\$*.docx`

## 2. Dokumentstruktur vollständig analysieren
- Alle Paragraphen UND Tabellen im Body auflesen (body children in Reihenfolge)
- Nie blind Paragraphen einfügen ohne zu wissen was drin ist
- Code: body children mit tag-Check (w:p vs w:tbl)

## 3. Richtigen Ansatz wählen
- Dokument nutzt Tabellen → Tabellen bearbeiten, KEINE Text-Paragraphen einfügen
- Vorhandene Elemente als XML-Vorlage klonen (copy.deepcopy) statt neue OxmlElement erstellen
- OxmlElement nur wenn unbedingt nötig — erzeugt oft fehlerhafte Namespaces

## 4. Sauber aufräumen vor neuen Änderungen
- Alte Reste (von fehlgeschlagenen Versuchen) zuerst per Text-Suche entfernen
- Nie neue Elemente einfügen ohne vorher die alten zu löschen

## 5. Nach dem Speichern verifizieren
- Dokument neu öffnen und Struktur erneut auslesen
- Erst dann als "fertig" melden
