---
name: feedback-geburtstagssong-zeitlos
description: Schüler-Geburtstagssong-Texte (Suno, MC-Feature) sollen zeitlos formuliert sein — weder Tage-Differenz-Bezüge noch reine "heute ist dein Tag"-Fixierung, ganzjährig einsetzbar, und seit 31.08.2026 KEIN Alter mehr im Text (nur der Tag)
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-08-31T09:06:16.518Z
---

Bei den Geburtstagssongs für Schüler (MC-Feature in `mission_control_api.py`, Route die `gb_kontext()`/`gb_lyrics_hint()` nutzt) sollen die Lyrics **zeitlos** formuliert sein — in zwei Stufen:

1. **10.08.2026:** Kein "noch X Tage", "in X Tagen" und keine Entschuldigung dafür, dass der Geburtstag schon "vor X Tagen" war. Einfach fröhliche Geburtstagsstimmung, unabhängig vom genauen Abspieltag.
2. **17.08.2026 (Erweiterung):** Der Song soll auch **ganzjährig einsetzbar** sein, nicht nur exakt am Kalendertag passen — Chris' Wunsch: "der Text soll generell für das ganze Jahr gelten und nicht nur für den Tag selbst". Datum und Alter dürfen weiterhin im Songtext vorkommen, es soll erkennbar ein Geburtstagssong bleiben — nur die zentrale "HEUTE ist dein großer Tag/heute feiern wir dich"-Fixierung als tragendes Songthema soll vermieden werden, damit der Song auch Wochen/Monate später noch stimmig klingt, wenn er nochmal gehört wird.

**Why:** Vorher haben `gb_kontext()` und `gb_lyrics_hint()` dem Songwriter-Prompt explizit Zeitdifferenz + Ton (Vorfreude/Countdown bei früherem Abspieltag, Entschuldigung/Augenzwinkern bei späterem) mitgegeben — führte zu Formulierungen, die Chris nicht mehr wollte. Später zeigte sich zusätzlich: reine "heute ist der Tag"-Texte lassen sich schlecht wiederverwenden, wenn der Song nicht exakt am Geburtstag selbst gespielt wird.

**Umgesetzt:** `gb_kontext()` liefert nur das nackte Datum ("Geburtstag: DD.MM.YYYY") ohne Tage-Differenz-Text. `gb_lyrics_hint()` (ca. Zeile 8808 in `mission_control_api.py`) enthält jetzt zwei Anweisungsblöcke: (a) keine Tage-Differenz-Bezüge/Entschuldigungen, (b) explizite "GANZJÄHRIG EINSETZBAR"-Regel gegen die "heute ist dein Tag"-Fixierung, mit Erlaubnis dass Datum/Alter im Text vorkommen dürfen. Die alte `_style_timing_hint()`-Funktion wurde bereits am 10.08. entfernt. MC-Server nach der Änderung neu gestartet (Python-Änderung, PID-Wechsel verifiziert, Port 18790 sauber).

**How to apply:** Bei künftigen Änderungen an diesem Feature beide Zeitlosigkeits-Vorgaben (Tage-Differenz UND Ganzjahres-Tauglichkeit) nicht wieder rückgängig machen, außer Chris sagt explizit was anderes.

**17.08.2026 (Erweiterung #2) — Altersangabe zeitlos, per Ordnungszahl statt Zustandsform:** Erster Versuch war FALSCH und wurde noch am selben Tag korrigiert: eine "wird bald X" (Geburtstag noch nicht da) vs. "ist jetzt X" (Geburtstag schon gefeiert) Zeitform-Unterscheidung anhand von `ref_date` (Abspieltag oder Erstellungstag) klingt nach reiner Grammatik, ist aber an den Erstellungszeitpunkt gebunden — genau das widerspricht der Ganzjahres-Tauglichkeit aus Erweiterung #1: hört sie den Song Monate später nochmal, ist "wird bald 14" plötzlich falsch, wenn der Geburtstag inzwischen verstrichen ist (oder umgekehrt). Chris hat das selbst bemerkt und korrigieren lassen ("baue das so ein, dass sie den Song das ganze Jahr hören kann und der Text trotzdem stimmt").

**Finale Lösung:** Kein Zeitvergleich mehr nötig. `gb_lyrics_hint()` weist die KI stattdessen an, das Alter IMMER als Ordnungszahl/Bezeichnung des Geburtstags zu formulieren — "dein 14. Geburtstag", "zu deinen 14 Jahren" — statt als Zustandsform ("wird bald"/"ist jetzt"). Die Ordnungszahl-Form ist ganzjährig wahr, unabhängig davon wann generiert oder gehört wird — braucht daher keinerlei Datumsvergleich. `ref_date`/`abspieltag` bleiben im Code nur noch für die (ungenutzte, aber harmlose) `ref`-Parameter-Signatur bestehen, ohne Funktion für die Zeitform. Gleichzeitig wurde `data/schueler_stammdaten.json` um `geburtsjahr` ergänzt (Alter = aktuelles Jahr − Geburtsjahr) und die Tab-Autofill-Funktion im Bolla-Songs-Formular füllt jetzt auch `suno-alter` mit (siehe [[reference_schuelerlisten_7abcd]]).

**Lehre:** Bei "zeitlos"-Anforderungen jede neue Formulierungsregel gegen die Frage prüfen "bleibt das auch noch in 3 Monaten wahr, wenn nichts am Song verändert wird?" — nicht nur "klingt das am Erstellungstag richtig?".

**17.08.2026 (Bugfix #3) — Konkrete Beispielzahl im Prompt-Text wurde von der KI wörtlich übernommen.** Live-Test mit Albina Bozhdaraj (7b, wird am 18.09. 13, `suno-alter` korrekt via Autofill auf 13 gesetzt) ergab trotzdem "dein 14. Geburtstag" im generierten Text — falsch, +1 zu viel. Ursache gefunden: Die `ALTERSANGABE ZEITLOS HALTEN`-Anweisung in `gb_lyrics_hint()` benutzte als Beispiel wörtlich die Ziffer "14" ("z.B. 'dein 14. Geburtstag'") — reiner Zufall, dass das zufällig dieselbe Zahl war wie ein früherer Test, aber die KI hat diese Beispielziffer aus der Anweisung kopiert statt die tatsächlich übergebene `Alter: 13` zu verwenden. Klassischer Prompt-Engineering-Fehler: **nie eine konkrete Beispielzahl in eine Anweisung schreiben, wenn der echte Wert variabel ist** — die KI kann das Beispiel für die Vorgabe halten. Fix: Beispiel-Ziffern durch den abstrakten Platzhalter "X" ersetzt, plus expliziter Zusatz "IMMER exakt die oben unter 'Alter:' angegebene Zahl verwenden — NICHT selbst nachrechnen, NICHT +1 addieren". Zusätzlich die `Alter: {alter}`-Zeile im Prompt selbst um einen Klammerzusatz ergänzt ("dies ist die Zahl für den Geburtstag, um den es geht — wörtlich übernehmen, nicht selbst neu berechnen"), doppelte Absicherung.

**Lehre #2:** Instruktionstext und tatsächliche Nutzdaten sauber trennen — Beispiele in Anweisungen mit Buchstaben-Platzhaltern (X, Y) statt Zahlen schreiben, sonst besteht Verwechslungsgefahr mit echten Werten weiter oben im selben Prompt.

**31.08.2026 (Kehrtwende #4) — Alter GANZ raus aus den Lyrics, nur noch der Tag.** Chris' Wunsch wörtlich: „verbesserung für bolla schüler songs, dass die schüler den geburtstagssong immer als solchen genießen können, bitte das jeweilige alter in den lyrics nicht mehr verwenden, nur den tag". Die Ordnungszahl-Lösung aus Erweiterung #2 war zwar grammatisch ganzjährig wahr, aber „dein 14. Geburtstag" bindet den Song trotzdem an ein bestimmtes Lebensjahr — hört ihn die/der Schüler:in ein Jahr später nochmal, passt die Zahl gefühlt nicht mehr und der Song verliert seinen zeitlosen Charme. Neue Regel: **im Liedtext kommt gar keine Altersangabe mehr vor** — keine Zahl, keine Ordnungszahl, keine Zustandsform, keine Anspielung („ein Jahr älter", „noch eine Kerze mehr"). Nur Name + Geburtstag als Tag/Datum. Damit ist der Song jedes Jahr aufs Neue uneingeschränkt gültig.

**Umgesetzt (`mission_control_api.py`):**
- `gb_lyrics_hint()`: der Block „ALTERSANGABE ZEITLOS HALTEN" (Ordnungszahl-Anweisung) ist ersetzt durch „KEIN ALTER IM TEXT" — explizites Verbot jeder Altersangabe/Anspielung. Der „GANZJÄHRIG EINSETZBAR"-Satz sagt jetzt „Anlass und Datum dürfen vorkommen" (Alter gestrichen).
- Schul-Song-Prompt: die Zeile `Alter: {alter} (…)` ist ganz entfernt — die KI bekommt die Zahl nicht mehr zu sehen.
- Song-Titel-Bau (`is_school`-Zweig): `alter` wird nicht mehr an `parts` angehängt → interner Titel jetzt „Happy Birthday <Name> <Datum>" statt „… <Alter> <Datum>".
- `suno-alter`-Formularfeld + `geburtsjahr`-Autofill bleiben im Code (harmlos, ungenutzt) — nicht extra ausbauen.
- MC-Server nach der Änderung neu gestartet (PID-Wechsel 157835 → 207103, py_compile OK, Port 18790 → HTTP 200).

**How to apply:** Auch diese vierte Vorgabe (kein Alter im Text) bei künftigen Änderungen nicht zurückdrehen, außer Chris sagt ausdrücklich etwas anderes. Die frühere Erlaubnis „Alter darf im Text vorkommen" aus Erweiterung #1/#2 ist damit überholt.
