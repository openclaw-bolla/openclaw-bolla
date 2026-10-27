---
name: feedback_limit_regeln
description: EINZIGE Regeldatei für Claude-Limits (5h + Woche) — Gating, Auto-Resume, Budget-Check, Samstag-Ausreizen, Tipps ab Do 29.10.
metadata:
  type: feedback
---

Konsolidiert 25.10.2026 aus 6 Einzeldateien (Backup: workspace/backups/memory_limit_20261025/). Quota immer über `/api/claudequota` (kein Token-Verbrauch), nie Probe-Calls.

## 1. Harte Regeln (gelten immer)
- **5h-Fenster darf NIE gerissen werden.** Jeder große/Hintergrundprozess pausiert bei **75 %** (Gate) bis zum Reset und macht **automatisch** weiter (+90 s Puffer). Zusätzlich Watchdog: bei **85 %** laufenden Schritt abbrechen, Fehlversuch zählt nicht. Chris soll nie anstupsen müssen (Chris 23.10. + 25.10.: „das soll nie mehr passieren").
- Referenz-Implementierung: `scripts/samstag_ausreizen.py` (`gate()`, `_run_watchdog()`, Env `AUSREIZEN_5H_LIMIT`=75, `AUSREIZEN_5H_HARD`=85). Alle Ausreiz-Skripte importieren sie. **Neue Hintergrundläufe mit `claude -p` müssen `scripts/limit_gate.py` nutzen** (`limit_gate.run(...)` = Drop-in für `subprocess.run`, wartet bei ≥75 % bis Reset, killt bei ≥85 %; Selbsttest `python3 limit_gate.py`, kostet keine Tokens; gebaut 25.10.26, eingebaut in aldi_prospekt_ocr, build_f_photos, newsletter_scanner, caption_watcher, mail_to_calendar, schuljahr_modul_watcher, distrokid_social_paket; Backups workspace/backups/limit_gate_20261025/). Bewusst NICHT gegatet: nutzergetriebene Aufrufe (MP-Chat, telegram_bot, aufpeppen). Laufende Prozesse laden Code nur beim Start → nach Änderung neu starten (resumable).
- **Manifest-Prinzip:** Jede Teilaufgabe schreibt eine eigene Output-Datei; fertig = Datei existiert. So ist jederzeit klar, was fehlt (auch nach Crash).
- **Kommt "session/rate limit"-Meldung:** nicht quittieren → Quota prüfen; Fenster frei → fehlende Teile sofort neu starten; sonst Weckruf kurz nach `five_hour_reset_label`. Chris nur informieren („X von Y fertig, Rest ab HH:MM"), nicht fragen.
- **Vor größeren Projekten:** 5h-% und Wochen-% aktiv ansagen. Unter **10 % Rest** (5h oder Woche) → nicht starten, Zahlen zeigen. Bei mehrteiligen Projekten zwischen den Häppchen erneut prüfen. Danach vorher/nachher zeigen.
- **Alltagsreserve (Mo–Fr):** Woche > 60 % → stoppen und Chris fragen (40 % Reserve für Schule/Mails/MP). Tagsüber nichts Schweres starten; Massenläufe (>10 `claude -p`) nachts vorschlagen, ohne Kosten zu nennen, Entscheidung bei Chris ([[feedback_claude_p_massenlaeufe_kosten]]).
- Hook `context_check.py` warnt nur bei 5h-Rest < 10 %.
- Wochenanfang (So/Mo) wird geschont — nichts läuft automatisch über Samstag 23:50 hinaus.

## 2. Wochenende ausreizen (Pro-Abo ist fix bezahlt, Rest verfällt beim Reset)
- Reset: **Sonntag 00:00**. Ziel: Rest **< 10 %** („Schwaben-Protokoll"). Bestätigtes Rezept (10.10. ✅, 17.10. 100 %): **Freitag ~19:00 starten** (Cron + Wrapper), detachter Orchestrator, ein Prozess zur Zeit (parallele `claude -p` lassen WSL laggen), bei jedem neuen 5h-Fenster sofort wieder voll loslegen, Deadline Sa 23:50, Woche-Stopp 98,5 %. Notbremse `touch /tmp/aurora_samstag_stop`.
- Chris meldet bis Fr 19:00 nichts → Start ohne Rückfrage. Tagesplan als Liste ins Terminal, bevor gestartet wird.
- Engpass ist das 5h-Fenster (≈7 Wochenpunkte pro Fenster), nicht die Woche → Plan an möglichst vielen vollen Fenstern ausrichten, nicht an Wochen-%.
- **Arbeitsvorrat vorab bauen:** erst Vorgemerktes (AURORA-II, Kurstage, Backlog), dann selbst sinnvolle Aufgaben; keine Fake-Arbeit; Opus/Sonnet nach Sinn, nie Fable ([[feedback_modell_auswahl]]). Reserve-Queue, damit der Lauf nicht vorzeitig endet.
- Änderungen nur mit Backup + Protokoll, nichts löschen, nichts extern senden. Chris braucht Lesezeit: nicht mehr Kapitel produzieren als er lesen kann.
- In den letzten ~6 h vor Reset: Wochenreserve NICHT schonen, aktiv Verbrauch vorschlagen.

## 3. Lehre 24.10.2026 + offener Auftrag
- Sa-Lauf 24.10. (Analogie-Check Kap. 31–36) startete erst Sa 19:28 bei 68 % und hatte nur 6 Kapitel → um 22:15 fertig bei Woche 79 %, Rest verfiel. Ursachen: Freitag-Start fehlte, Arbeitsvorrat zu klein.
- **Bis Do 29.10.2026 mittag NICHTS riskieren** (Schule/private Jobs mit hoher Token-Last). **Ab Do mittag** proaktiv Tipps geben, wie wir besser ausreizen (Fr-19:00-Start wieder, größere Queue/Reserve-Aufgaben, Gate-Pausen statt Abbruch) — mit aktuellem Stand aus `/api/claudequota`.

Verwandt: [[feedback_hintergrundjob_zuerst]], [[feedback_hintergrund_fork_lange_aktionen]], [[feedback_wartungsfenster_surfaces]], [[feedback_mp_chat_lag_ursache]].

## Messung 25.10.26: Tonie-Kosten (5h vs. Woche)
- 5h-Fenster und Wochenlimit sind getrennte Töpfe, Prozente NICHT vergleichbar. Woche ≈ 10× so groß wie 5h.
- Gemessen (4 `claude -p`-Jobs: Anton Lied + Mia Song/Lied/Geschichte): 5h +4 Pp, Woche ±0 (<1 %, Anzeige nur ganze %). Alle 7 Tonie-Teile ≈ 1 % Woche, selbst 3× neu erzeugen.
- **Why:** Chris fragte, was Tonies am Wochenlimit verbrauchen. **How to apply:** Tonie-Neuerzeugung fürs Wochenlimit vernachlässigbar; nur das 5h-Gate beachten. Messen: `/api/claudequota` vor/nach (kostenlos), Skript scripts/tonie_quotamessung.py.

## Lücke 26.10.26 abends
5h-Fenster stand 19:30 bei 96 % (Gate 75 %/Watchdog 85 % griff nicht). Wahrscheinliche Ursache: Welle-3-Opus-Subagent (Agent-Tool, Kürzung Kap. 9–12) läuft NICHT über `limit_gate.py` und wird erst nach dem Überschreiten bemerkt (Abbruch bei 91 %). **How to apply:** Vor jedem Agent-/Subagent-Start `/api/claudequota` prüfen (nicht über 60 % starten); lange Kürzungs-/Schreibläufe bevorzugt als `claude -p` via `limit_gate.run`. Reset 22:49.
