---
name: reference-opern-infoblatt
description: "Wiederverwendbare Vorlage für einseitige Opern-Übersichtsseiten (Word) — Stil \"Freischütz/Barbier\""
metadata: 
  node_type: memory
  type: reference
  originSessionId: 056ed88c-374c-4363-b2ba-49257524c8b4
---

# Opern-Infoblatt-Vorlage 🐾

Chris geht regelmäßig in die Oper (Hamburg) und mag vorab eine **einseitige Word-Übersichtsseite** zur Aufführung. Etabliert seit Freischütz + Barbier von Sevilla — Chris will das als feste Serie ("sehr gut machen", 08.06.2026).

## Bei "mach mir die Übersichtsseite für [Oper]"
Generator: `/home/bolla/workspace/tools/opern/opern_infoblatt.py`
1. Den `OPER`-Datenblock oben im Script mit dem Werk füllen (datei, titel, untertitel, akzent, info, personen, akte, musik, bedeutung).
2. **Eigene Akzentfarbe pro Oper** wählen (Hex ohne #, dunkel genug für weiße Schrift) — Chris mag eine eigene Farbe je Werk, nicht serielles Einheitsrot.
3. `python3 opern_infoblatt.py` → speichert nach Freizeit-Ordner **und** Desktop.

## Design-DNA (nicht ändern)
- Cambria, US-Letter, Rand 2/2/0.75/0.75 cm
- Titel 26pt bold Akzent · Untertitel 10pt grau (777777), beide zentriert
- 2-Spalten-Boxen ohne Rahmen, Headerleiste = weiße Schrift auf Akzent-Shading
- Labels bold/Akzent, Fließtext 333333 (10pt)
- "Handlung"-Leiste (14pt), darunter Akt-Überschriften (11pt bold Akzent) + Bullets
- Box 1: Allgemeine Informationen | Personen — Box 2: Berühmte Musiknummern | Bedeutung

## Ablage
- Freizeit: `/mnt/d/OneDrive/Dokumente/Allgemeines/Freizeit/<Datei>.docx`
- Desktop: `/mnt/d/OneDrive/Desktop/<Datei>.docx`

Ausnahme zur globalen Aptos-Regel: Diese Blätter bewusst in **Cambria** (Serien-Look). Vgl. [[feedback_word_schriftart]], Ablage [[feedback_datei_speicherort]].
