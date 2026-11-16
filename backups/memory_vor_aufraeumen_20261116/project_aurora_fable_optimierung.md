---
name: project-aurora-fable-optimierung
description: "AURORA-Stolperstein-Archiv (Telegram) + Auftrag für die spätere Fable-5-Komplettpolitur des Buchs"
metadata:
  node_type: memory
  type: project
  originSessionId: current
---

# AURORA — Stolperstein-Sammlung & Fable-5-Politur

Chris liest AURORA und sammelt **Sätze, die ihm auffallen** (schwer verständlich, mögliche Grammatikfehler, holprig). Diese werden archiviert und dienen später als **Input für eine gründliche Komplettüberarbeitung mit Fable 5**, sobald das Modell verfügbar ist.

## Erfassung — läuft über den Telegram-Bot (seit 23.06.2026)
Implementiert in `scripts/telegram_bot.py` (Befehle werden VOR dem Claude-Aufruf abgefangen → kein Token-Verbrauch, sofortige Bestätigung). Nur Chris, privater Chat.
- **Sammel-Modus (für Copy-Paste!):** `sammeln` schicken → ab dann wird JEDE Nachricht von Chris archiviert (ohne Präfix, kein Claude-Call), Bestätigung knapp „📌 #N"; `fertig` beendet. Ideal um beim Lesen mehrere Sätze hintereinander reinzukippen. Flag-Datei `data/.aurora_sammelmodus` (Default aus → sicher nach Bot-Neustart). Reihenfolge im Bot: Satz-Check VOR ADB & Claude.
- **Text (einzeln, ohne Modus):** Nachricht mit Präfix `satz: …`, `stolperstein: …` oder `📌 …` → Rest wird archiviert.
- **Sprache:** Sprachnachricht, die mit „Satz …" beginnt → Azure-Speech-Transkription (de-DE), „Satz" wird abgeschnitten, Rest archiviert. (Sprachnachricht OHNE „Satz" davor = normales Bolla-Gespräch; Voice wird seit dieser Änderung generell transkribiert statt roh an Claude geschickt.)
- **Abfragen:** `sätze` → Anzahl + letzte 5 · `satz undo` → letzten Eintrag löschen.
- **Bestätigung:** „📌 Stolperstein #N archiviert: »…«".

**Sammeldatei:** `~/workspace/data/aurora_stolpersteine.jsonl` — eine Zeile pro Eintrag: `{ts, source: text|voice, text, status: offen}`.
Technik: ffmpeg (ogg→wav 16k mono) + Azure Speech STT REST (`{region}.stt.speech.microsoft.com`, key aus `config/azure_speech.json`, region westeurope). Kosten: Azure-Free-Tier 5 h/Monat → bei diktierten Sätzen praktisch 0; Text-Erfassung kostenlos.

## Auftrag für Fable 5 (wenn verfügbar) — WICHTIG: Fable entscheidet selbst
Wenn die Komplettpolitur startet:
1. **Stolperstein-Sätze einkippen** als Hinweise — ABER **Fable entscheidet eigenständig**, ob ein eingekippter Satz überhaupt verbessert werden muss (nicht blind jeden ändern). Chris' Sätze = Aufmerksamkeits-Marker, kein Pflicht-Edit.
2. **Fable nimmt zusätzlich EIGENE Optimierungen vor** über das ganze Buch — bzgl.: **Spannung, Wendungen, Charaktere/Charakterzeichnung, Humor**, sprachliche Klarheit, Lesefluss.
3. **Quelle bleibt die JSON** (`workspace/data/ki_buch.json` DE / `ki_buch_en_adapted.json` EN). Backup vorher. Hartkodierte Blöcke beachten: [[project-aurora-hardcoded-blocks]].
4. **Verteilung danach über ALLE Kanäle** gemäß [[project-aurora-update-checklist]] (6 Distributionspunkte: D2D + KDP, eBook + Print, DE + EN). Bei Seitenzahländerung Print-Cover neu.
5. **Modell-Disziplin:** Fable 5 = einmaliger Hochqualitäts-Task (zählt ~2× Opus gegen Wochenlimit) → gezielt einplanen, nur wenn Budget < 50 % verbraucht. [[feedback-modell-auswahl]]

## ⭐ Chris' OBERSTES Qualitätsziel (01.07.2026 — wichtiger als alles andere)
Chris' **wichtigstes Kriterium ist NICHT Lesbarkeit**, sondern: **Die Gesamtqualität des Buches soll von den MEISTEN Lesern als hoch bis sehr hoch bewertet werden.** Das ist der Nordstern für den Fable-Lauf — jede Optimierung (Lesefluss, Spannung, Humor, Charaktere) dient diesem einen Ziel. Bei Zielkonflikten gewinnt „hohe Leserbewertung durch die Mehrheit".

## Renis Leseeindruck + Lesbarkeits-Diagnose (01.07.2026)
**Reni (explizite Zielleserin lt. Stil-DNA!) sagt: mag das Buch nicht / liest es nicht gern.** Sie kann nicht genau benennen was stört, aber: *„muss immer wieder zurück im Text, versteht sonst viele Sätze nicht"*, tut sich schwer, „für 13-Jährige unmöglich zu lesen". Reni mag am liebsten **einfache, sympathische Lovestories mit Humor** (keine Groschenromane) — Genre-Mismatch ist also ein Teil (AURORA = Thriller), aber der Lese-Widerstand ist real und messbar → [[user_reni]].

**Objektive Messung (lokal, Flesch-Amstad-DE, kostenlos):**
- Gesamt eher LEICHT: Flesch **76,6**, Ø-Satz **11,5 W**, Median **8 W** — die meisten Sätze sind harmlos.
- ABER: **411 Schachtel-/Kettensätze ≥35 Wörter**, einige bis **80/94/113/151 Wörter** (Bewusstseinsstrom „und…und…und", viele Einschübe zwischen Subjekt & Verb), meist an emotionalen Höhepunkten. **Diese ~400 Sätze sind der Grund fürs Zurückspringen**, ~40 Extrem-Monster (≥50 W) sind die schlimmsten. Ken-Follett-„epische Breite" kollidiert hier mit „auch für Reni & 13-Jährige".
- Behebbar OHNE Inhalts-/Genre-Änderung: lange Kettensätze in 2–3 teilen, Einschübe rausziehen — Ton/Wärme/Humor bleiben. Beispiel-Entzerrung demonstriert (funktioniert).

## Plan (Chris-Entscheidung 01.07.2026)
- **KEIN großer Durchgang jetzt.** Chris' Argument: Mikro-Lesbarkeit treibt keine Verkäufe (stimmt direkt; mittelbar über Sternebewertungen aber schon → siehe Nordstern-Ziel).
- Wenn's soweit ist: **Fable 5 FRAGEN, was ER für sinnvoll hält** (nicht vorgeben) → dann **gemeinsam in der Diskussion** entscheiden, was gemacht wird — **budgetabhängig**.
- „Satzentzerrung / Lesefluss (kein Leser muss zurückspringen)" als **ein** Kriterium einbringen — aber untergeordnet dem Nordstern „hohe Gesamtbewertung durch die Mehrheit".

## Stand
- Erfassung **live & getestet** (Trigger-Erkennung ✅, eine Bot-Instanz läuft). Chris kann ab sofort sammeln.
- Fable 5 (`claude-fable-5`) ist inzwischen verfügbar → nächster Schritt ist die **Fable-Konsultation** (s. Plan oben), NICHT ein direkter Vollausgleich.

Siehe [[projekt-ki-thriller]] · [[project-aurora-update-checklist]] · [[aktuell]]
