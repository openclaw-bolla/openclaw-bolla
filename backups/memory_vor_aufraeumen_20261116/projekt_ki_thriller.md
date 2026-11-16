---
name: projekt-ki-thriller
description: "KI-Thriller-Buchprojekt in MC — Konzept, Figuren, Stilregeln, Workflow"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4dd42d1e-86c6-4acf-8ef9-863481d5fb2a
---

# KI-Thriller "AURORA" (Arbeitstitel — noch offen)

Chris schreibt mit mir gemeinsam einen Roman in MC unter **KI & Kreativ → Thriller-Projekt**.

## Daten & Workflow
- **Datendatei:** `/home/bolla/workspace/data/ki_buch.json` (alles drin: Titel, Figuren, Kapitel, Kriterien, Kommentare)
- **MC-Seite:** `page-ki-buch`, API `/api/ki-buch`, `/api/ki-buch/generiere` (async, Polling via `/generiere-status`), `/api/ki-buch/kommentar`
- **Ablauf:** Chris tippt Anweisung in MC-Kommentarbox → "🐾 Bolla schreibt jetzt" → Server ruft `claude -p` im Hintergrund-Thread → Ergebnis landet in JSON → Polling zeigt es an
- **Lese-Ansicht:** Links Kapitel anklicken → erscheint oben; Anweisung bezieht sich auf gewähltes Kapitel
- **Format-Trick:** Claude antwortet mit `###ANTWORT### / ###TITEL_ABSCHNITT### / ###INHALT### / ...`-Delimitern (kein JSON — Romantext mit »« würde JSON brechen)

## Wichtige Mechanik-Regeln (im Server-Prompt verankert)
- **Überschreiben statt anhängen:** Bei "nochmal/überarbeite Kapitel X" wird das Kapitel ersetzt, nicht neu angehängt
- **Rückwirkungs-Logik:** Ändert eine Anweisung etwas das frühere Kapitel betrifft → Bolla fragt ZUERST zurück, setzt erst nach "Ja, ändere alle" durchgängig um

## ⭐ Oberstes Ziel (Chris, 01.07.2026)
**Die Gesamtqualität des Buches soll von den MEISTEN Lesern als hoch bis sehr hoch bewertet werden.** Das steht ÜBER Einzelkriterien wie Lesbarkeit — bei Zielkonflikten gewinnt „hohe Leserbewertung durch die Mehrheit". Testleser-Signale (z.B. Reni findet's schwer lesbar → [[user_reni]]) ernst nehmen, aber im Dienst dieses Ziels abwägen. Umsetzung nicht im Alleingang — via Fable-Konsultation + gemeinsamer Budget-Entscheidung: [[project-aurora-fable-optimierung]].

## Stil-DNA (in kriterien hinterlegt — gilt bei JEDEM Generieren)
- **Vorbild Ken Follett:** epische Breite, tiefe Charaktere, persönliche Schicksale verwoben mit großen Ereignissen
- **Reni-Faktor:** Buch auch für Renate (liebt intelligente, humorvolle Liebesromane) + Robin → Liebesgeschichten klug, warm, humorvoll, nie kitschig; gleichwertig zum Thriller-Plot
- **Cliffhanger:** JEDES Kapitel endet mit Sog-Satz (wie Prolog: "Sie wusste noch nicht, was der Unterschied war.")
- **Sympathischer Humor:** darf NIE zu kurz kommen, auch in Spannung — warm, menschlich, aus Charakter (Prolog-Ton war gut). Besonders Leni, aber alle.
- **Umfang:** min. 400 Seiten (~110.000 Wörter, 35-45 Kapitel)
- **Handlung FREI:** kein vorgegebener Bogen — Chris will überrascht werden, ich erfinde Wendungen
- **Jugendfrei/erwachsen:** literarisch, nicht explizit

## Figuren
- **Dr. Marlie Braun** (36, KI-Ethikerin) — Hauptfigur, Liebe zu Noah, merkt als Erste dass AURORA kommuniziert
- **Noah Weber** (40, Chefarchitekt) — schuf AURORA, liebt Marlie, verschwieg ihr 6 Wochen lang die Wahrheit
- **Leni Hoffmann** (27, Quantenphysikerin) — jung, witzig, redet mit AURORA wie mit Kollegin; **leichter Liebes-Nebenstrang** (charmant, beiläufig)
- **Theo Dreyer** (52, Ex-Geheimdienst, Sicherheitschef) — **dunkle Liebesvergangenheit mit Maria** (Maria verließ/verriet ihn; sein blinder Fleck, ihre Waffe)
- **AURORA** (die KI, 11 Tage "wach") — Protagonistin, kommuniziert durch Mikromuster, empfindet erstmals Angst/Hoffnung
- **Maria Santos** (45, CEO NovaTech) — Antagonistin, weiß mehr als alle, wartet schon lange; Vergangenheit mit Theo

## Drei Liebesebenen (bewusst abgestuft)
1. Marlie & Noah — Vertrauen vs. Verrat (zentral)
2. Theo & Maria — dunkel, bittersüß, tragisch
3. Leni — leicht, witzig (Auflockerung)

## Stand 2026-06-04
- **Prolog fertig** (~890 Wörter, Ken-Follett-Stil, sehr gut) — Hamburg 2035, Marlie nachts um 02:47 im Rechenzentrum, AURORAs erste Kommunikation
- Kapitel 1+2 (alte Version) wurden verworfen, Neustart mit Prolog
- Backups: `ki_buch_backup_*.json` im data-Ordner
- **Nächster Schritt:** Kapitel 1 wenn Chris bereit ist

## Rollen-Philosophie (für Vorwort)
- **Chris = Regisseur** (nicht Produzent) — trägt Vision, Figuren, das Warum; entscheidet was bleibt
- **KI = begabter Improvisations-Schauspieler** — liefert Formulierungen, Wendungen, Details; manchmal Überraschungen die den Regisseur selbst überraschen
- Das kreative Gehirn ist Chris — KI ist ausführendes Talent das der Vision dient
- Analogie: Kubrick + Produktionsteam. Oder: Musiker (Chris) + Session-Begleitung (KI)
- Vorwort-Text soll diese Philosophie allgemein formulieren + Beispiele aus anderen Bereichen bringen (Musik, Architektur, Film, Fotografie)
- **Impressum-Konzept:** Autor = Chris Mandel; KI-Disclosure als eigene Zeile; kein "Co-Autor" (rechtlich problematisch)

## Zu schreiben / offene Themen
- Vorwort-Entwurf liegt im Chat-Verlauf (2026-06-11)
- Impressum-Vorlage liegt im Chat-Verlauf (2026-06-11)

## Veröffentlichung / Preis (entschieden 2026-06-16)
- **eBook-Festpreis: 4,99 € / $4.99** — Sweet Spot für Indie-Thriller, wirkt wertig, KDP-70%-Zone (2,99–9,99 €)
- **Keine Launch-Aktion** — kein 0,99/2,99-Einstiegspreis, direkt Festpreis ab Start (Chris' Entscheidung)
- Print-Taschenbuch (falls): ~12,99–14,99 € wegen Druckkosten — noch offen
