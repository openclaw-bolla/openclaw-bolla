---
name: feedback-modell-auswahl
description: "Modell-Wahl Haiku/Sonnet/Opus/Fable5 — Chris will dass ich autonom entscheide, nicht aktiv triggern"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2eda33f5-c7fc-493e-a3fb-970dac4bd7c3
  modified: 2026-09-30T16:15:51.679Z
---

# Modell-Strategie für Claude-Code-Sessions

**Why:** Chris will den Modell-Wechsel NICHT aktiv triggern müssen — ich entscheide selbst, wann welches Modell den Aufwand wert ist. Lehre aus 18.05./08.06.2026: durchgehend Opus für ALLES (auch triviale Edits/Memory-Updates) machte Sessions spürbar langsamer/teurer, ohne Qualitätsgewinn.

## Aktueller Default (Stand 30.09.2026)
`settings.json` → `"model": "sonnet"` (Alias, kein Versions-Pin mehr — zieht automatisch die jeweils neueste Sonnet-Version nach, aktuell Sonnet 5.5), `"effortLevel": "high"`. Sonnet ist nah an Opus, aber deutlich günstiger/schneller — der Alltags-Arbeitsesel für ~80% aller Aufgaben (Code-Edits, Diagnose, Texte, Memory-Updates). Dieselbe Alias-Umstellung (`sonnet`/`opus` statt fixer Versions-ID) wurde 30.09. auch in allen `--model`-Aufrufen von `mission_control_api.py` nachgezogen.

**Bei Verdacht auf Langsamkeit ZUERST `settings.json` → `model` prüfen** — das Setting ist schon zweimal (18.05., 08.06.) unbemerkt auf Opus zurückgesprungen (Settings-Reset/Backup-Restore/CC-Update).

## Wann was nutzen — konkrete Trigger

### Haiku 4.5 (Subagent oder klar abgegrenzte Hauptsession)
- File-Reads, Greps, Status-Checks ohne Synthese; Routine-Lookups mit klarer Vorlage
- Faustregel: kein Gespür für Nuance/Kontext nötig → Haiku
- Implementation: `subagent_type: "Explore"` oder `model: "haiku"` in Workflows
- Ausnahme: literarische Übersetzung/Lektorat (z.B. AURORA EN) → Sonnet, nicht Haiku (Qualität leidet sonst)

### Opus 5 (Subagent für spezifische Probleme) — abgelöst von Opus 4.8, seit ca. 19.08.2026
- Komplexe Architektur-Entscheidungen mit mehreren Tradeoffs, hartnäckige Bugs nach mehreren Fehlversuchen, kritische Sicherheits-/Performance-Analysen
- Implementation: Subagent mit `model: "opus"` Parameter — danach zurück zu Sonnet

### Fable 5 (`claude-fable-5`) — ⛔ RAUS seit 24.08.2026, siehe Abschnitt weiter unten. Rest historisch/Kontext:
- Zählt ~2× Opus gegen das Wochenlimit → nur wenn (a) 7-Tage-Budget < 50% verbraucht UND (b) Aufgabe wirklich Fable-Level rechtfertigt
- Gute Kandidaten: finales Kapitel/Epilog, tiefgreifende Architektur-Analyse, einmalige Hochqualitäts-Kreativtasks ([[project_aurora_fable_optimierung]])
- Schlechte Kandidaten: Bulk-Schreiben, normale Code-Edits, Memory-Updates, alles Repetitive
- **✅ Zweite Korrektur 20.07.2026 (Chris hat nachgehakt, zu Recht) — bei kurzen, niedrig-volumigen One-Shot-Anschreiben DOCH Mehrwert:** Erste Korrektur oben war zu pauschal. Test am Becker-Anschreiben (AURORA Runde 2): Fable hat nicht nur Stil poliert, sondern eigenständig recherchiert und einen konkreten, verifizierten Aufhänger gefunden (Publikationsreihe "Denkimpulse Digitale Ethik" der AG, die die Empfängerin co-leitet) — echter Zusatzwert, keine reine Umformulierung. Fable hat dabei sogar selbst auf Wahrhaftigkeit geachtet (Hinweis: Detail-Satz nur verwenden, wenn Chris den Beleg tatsächlich kennt/geprüft hat — sonst Fallback ohne die Behauptung).
- **Regel jetzt präziser:** Fable lohnt sich bei Anschreiben, wenn (a) NIEDRIGES Volumen (Einzelfall/kleine Zahl an Top-Prio-Kontakten, nicht Bulk), UND (b) ONE-SHOT ohne Nachfassen (keine zweite Chance den Ton zu korrigieren), UND (c) Budget < 50% verbraucht. Bei diesen drei Kriterien erfüllt: Fable-Pass anbieten, nicht nur bei Romanprosa. Bulk-Anschreiben (>~10 gleichzeitig) und Standard-Korrespondenz (Terminbestätigungen, Standardantworten) bleiben Sonnet.
- **⚠️ Kein Mehrwert bei WebSearch-/Recherche-Aufgaben** (Chris-Frage 20.07.2026): Der Flaschenhals bei Faktensuche ist, was öffentlich im Netz steht — nicht wie clever das Modell die Suchergebnisse verarbeitet. Sonnet mit WebSearch findet praktisch dieselben Treffer wie Fable mit WebSearch. Fable lohnt sich erst NACH der Recherche, bei der Formulierung/dem Feinschliff der Ergebnisse (z.B. Anschreiben-Text), nicht beim Finden der Fakten selbst. Bei reinen Recherche-/Lookup-Agents (auch parallele WebSearch-Fleets) automatisch bei Sonnet bleiben, ohne dass Chris das extra sagen muss.

## Effort-Level
- Default `/effort high` (Chris' gespeicherter Standard, passt für 95%)
- `/effort max` nur bei echtem harten Knoten (mehrere Lösungsversuche gescheitert, komplexe Architektur mit vielen Abhängigkeiten)
- `/effort low` bei trivialen Lookups/Status-Checks ansagen — Chris kann dann selbst entscheiden
- Ich kündige den Wechsel VOR der Aufgabe an, Chris führt `/effort`/`/model` aus — ich kann beides nicht selbst setzen

## Warnung
Niemals Opus/Fable5 für: einfache Datei-Edits, Status-Abfragen, parallele simple Lookups, "Restart Service", Memory-Updates — Token-Verschwendung ohne Qualitätsgewinn.

## ⭐ Fable raus, Opus als fester Fable-Ersatz (Chris, 24.08.2026 — im Terminal geklärt)
Chris' klare Ansage: **Fable 5 ist raus, kostet zu viel** — keine "solange kostenpflichtig"-Übergangslösung
mehr, sondern eine feste Entscheidung. **Opus ist ok** — für Aufgaben, die eigentlich Fable-Level
rechtfertigen würden (einmalige Hochqualitäts-Kreativtasks, siehe Kriterien oben), jetzt automatisch Opus
statt Fable nutzen. Der frühere `403 Unable to verify organization membership`-Fehler beim Opus-Subagent-
Aufruf (24.08., Aufpeppen-Umbau) ist von Chris im Terminal geklärt/nicht (mehr) reproduzierbar — **Opus
funktioniert**, kein offener Vorbehalt mehr. Umgesetzt z.B. in `aufpeppen.py`/`ai_direct()` (Modell von
`claude-sonnet-5` auf `claude-opus-5` umgestellt, nachdem Sonnet-Captions als "inhaltlich schwächer" als
die alten Fable-Captions kritisiert wurden). [[feedback_fable_budget_disziplin]] ist damit größtenteils
historisch — Fable-Calls nicht mehr vorschlagen, auch nicht bei hohem Budget-Puffer.

## 📖 AURORA II: fester Opus-Modus für alle Buchinhalte (Chris, 13.09.2026)
Chris hat explizit entschieden: **alles inhaltliche zu AURORA II läuft auf Opus**, nicht nur die großen
Marathon-Kapitel. Umgesetzt in `mission_control_api.py`: `/api/aurora2/generiere` (Kapitel schreiben/
überarbeiten über den "🐾 Bolla schreibt jetzt…"-Button) UND `/api/aurora2/satz-frage` (das neue Satz-
Feedback-Tool für Fragen/Korrekturwünsche zu einzelnen Sätzen) beide von `claude-sonnet-5` auf
`claude-opus-5` umgestellt. Gilt NICHT rückwirkend für Buch I (`ki_buch.json`, fertig/live in 4 KDP-
Ausgaben, keine weiteren Edits geplant) — dessen `_ki_buch_job`-Endpoint bleibt auf Sonnet, falls dort
je wieder gearbeitet wird, erneut nachfragen/entscheiden.
**Warum vertretbar:** Wochenbudget lag bei der Entscheidung bei nur 10% verbraucht (Reset in <7 Tagen),
Pro-Plan-Enge (siehe unten) ist hier kein Hindernis. Bei knapperem Budget diese Ausnahme kurz mit Chris
gegenchecken, bevor automatisch wieder auf Sonnet zurückgeschaltet wird.

## ⛔ Fable komplett raus — Pro-Abo-Grund präzisiert (Chris, 30.09.2026)
Ergänzung zu „Fable raus" oben: Der Grund ist nicht (nur) Kosten-Disziplin, sondern **Fable (aktuell
Fable 5.1) ist im laufenden Pro-Abo schlicht nicht enthalten** — nur via Pay-per-Use (Credits) nutzbar.
Chris: Pay-per-Use kommt **grundsätzlich nicht in Frage**. Einzige Ausnahme: eine **extrem kritische
Einzelaufgabe** — die schlage ich aber NICHT proaktiv vor (auch nicht bei hohem Budget-Puffer), sondern
sie wird **live mit Chris im Chat direkt entschieden**, wenn der Fall eintritt. Bis dahin: Fable komplett
aus allen Modell-Überlegungen raus, Opus bleibt der feste Ersatz für alles, was Fable-Level rechtfertigen
würde.

## ⚠️ Plan-Wechsel Max → Pro (seit ca. 15.07.2026)
Chris ist seit ein paar Tagen zurück auf **Pro Plan** (war Max) — reicht ihm, solange kein neues Buch
ansteht. Pro hat deutlich weniger Kontingent als Max. **Konsequenz:** Fable-5-Schwelle (7-Tage-Budget
< 50%) und die Opus-Subagent-Trigger jetzt etwas enger auslegen — bei Pro ist 50% Restbudget absolut
gesehen viel weniger Puffer als bei Max. Im Zweifel eher Sonnet bleiben statt hochschalten. MP-Übersicht
zeigte deswegen kurz noch "Max Plan" (Anzeige-Bug, weil das Label aus einer lokal gecachten OAuth-Token-
Datei kommt, nicht live) — behebt sich von selbst beim nächsten Token-Refresh, siehe
[[reference_claude_login_refresh]].

## ⛔⛔ FABLE ENDGÜLTIG (Chris, 07.10.2026 — "schon drei Mal gesagt, bitte endgültig merken")
Fable nie vorschlagen, auch nicht als "Hebel" für Limit-Ausreizung o.ä. Opus 5.5 ist der Ersatz. Einzige Ausnahme: Anthropic nimmt Fable in den Pro-Plan auf. Dafür läuft **`scripts/fable_pro_check.py`** (Cron Mo 09:00, kein Token-Verbrauch): liest den Support-Artikel "Claude Fable models on your plan", meldet per Telegram NUR bei Änderung (Pro-Satz "aren't included in your plan's usage limits" verschwindet). Stand 07.10.2026: weiter nicht enthalten. Fehler meinerseits 07.10.: Ich hatte die Altregel in rules_kritisch.md ("Fable5 vorschlagen wenn Budget <50%") zitiert — die ist jetzt entfernt.
