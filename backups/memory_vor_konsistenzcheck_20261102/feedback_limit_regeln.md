---
name: feedback_limit_regeln
description: EINZIGE Regeldatei für Claude-Limits — 5h-Fenster vs. Wochenlimit getrennt, Reserve-Tage Mo/Di/Fr/Sa tagsüber 20 % frei, gilt für ALLE (Hintergrund + Bolla + Subagents)
metadata:
  type: feedback
---

Konsolidiert 25.10.2026, neu geordnet + verschärft 27.10.2026 (Backups: workspace/backups/memory_limit_20261025/, workspace/backups/limit_regeln_20261027/). Quota immer über `/api/claudequota` (kein Token-Verbrauch), nie Probe-Calls. **Schwellen stehen im Code an EINER Stelle: `scripts/limit_policy.py`** — bei Regeländerung dort + hier ändern, sonst nirgends.

## 0. Zwei getrennte Töpfe — nie vermischen
| | **5h-Fenster** | **Wochenlimit** |
|---|---|---|
| Größe | klein, Reset alle 5 h rollierend | ≈ 10× so groß, Reset **Sa 22:59** (Anzeige) / Verfall zum Wochenwechsel |
| Gefahr | Chris (Schule/Book/MP) steht ohne Bolla da | Reserve für Alltag weg / Rest verfällt ungenutzt |
| Steuerung | **Gate/Obergrenze (§1)**, wirkt sekundenaktuell | **Alltagsreserve + Ausreizen (§2/§3)**, wirkt tageweise |
| Prozente | nicht mit Woche vergleichbar (5h +4 Pp ≈ Woche <1 %) | |
Ein Schritt kostet bis ~13 Pkt im 5h-Fenster, aber nur ~1 Pkt in der Woche → **das 5h-Fenster ist fast immer der Engpass**, die Woche das Budget.

## 1. 5h-Fenster (gilt immer, für ALLE Verbraucher)
- **Reserve-Tage Mo/Di/Fr/Sa, tagsüber 07:00–22:00:** IMMER 20 % im 5h-Fenster übrig → Obergrenze **80 %**, Gate **67 %** (67 + ein Schritt ≤ 13 Pkt = 80). (Chris 27.10.2026)
- **Sa-Nacht (ab Sa 22:00 bis Wochenreset/Deadline 23:50):** Gate **82 %**, Obergrenze **95 %** — der Rest verfällt ohnehin, keine Reserve nötig. (Chris 27.10.2026)
- **Sonst (Mi/Do/So + nachts 22–07):** Gate **75 %**, Obergrenze **85 %**.
- **Gate** = vor einem neuen Schritt prüfen; ≥ Gate → pausieren bis Reset (+90 s) und **automatisch** weitermachen. **Obergrenze/Watchdog** = laufenden Schritt abbrechen, Fehlversuch zählt nicht. Chris soll nie anstupsen müssen.
- 5h-Fenster darf nie gerissen werden. Hook `context_check.py` warnt zusätzlich bei Rest < 10 %.

## 2. Wochenlimit
- **Alltagsreserve (Mo–Fr bis Fr 19:00):** Woche ≥ **60 %** → keine schweren/optionalen Projekte mehr, Chris fragen (40 % Reserve für Schule/Mails/MP). Alltagsautomatiken (Mail→Kalender, Newsletter, MP-Chat) laufen weiter — für die ist die Reserve da.
- **Wochenanfang (So/Mo) schonen**; nichts läuft automatisch über Sa 23:50 hinaus.
- Tagsüber nichts Schweres starten; Massenläufe (> 10 `claude -p`) nachts vorschlagen, ohne Kosten zu nennen, Entscheidung bei Chris ([[feedback_claude_p_massenlaeufe_kosten]]).
- **Vor größeren Projekten:** 5h-% und Wochen-% aktiv ansagen. Unter 10 % Rest (5h oder Woche) → nicht starten. Bei mehrteiligen Projekten zwischen den Häppchen neu prüfen; danach vorher/nachher zeigen.

## 3. Wochenende ausreizen (Pro-Abo ist fix bezahlt, Rest verfällt beim Reset)
- Ziel: Wochenrest bei Reset **< 10 %** („Schwaben-Protokoll"). Rezept (10.10. ✅, 17.10. 100 %): **Fr ~19:00 starten** (Cron + Wrapper `ausreizen_fr_wrapper.sh`), detachter Orchestrator, ein Prozess zur Zeit (parallele `claude -p` lassen WSL laggen), in jedem neuen 5h-Fenster sofort wieder voll loslegen, Deadline Sa 23:50, Wochen-Stopp 98,5 %. Notbremse `touch /tmp/aurora_samstag_stop`.
- **Auch hier gilt §1:** Fr 19–22 und Sa 07–22 nur bis Obergrenze 80 % (20 % bleiben frei); Sa ab 22:00 bis 95 %, andere Nächte bis 85 %. Das kostet etwas Durchsatz — Plan an möglichst vielen vollen Fenstern/Nachtstunden ausrichten.
- Chris meldet bis Fr 19:00 nichts → Start ohne Rückfrage; Tagesplan vorher als Liste ins Terminal.
- **Arbeitsvorrat vorab bauen:** erst Vorgemerktes (AURORA-II, Kurstage, Backlog), dann sinnvolle Eigenaufgaben, Reserve-Queue; keine Fake-Arbeit; Opus/Sonnet nach Sinn, nie Fable ([[feedback_modell_auswahl]]). Änderungen nur mit Backup + Protokoll, nichts löschen, nichts extern senden; nicht mehr Kapitel als Chris lesen kann.
- In den letzten ~6 h vor Reset Wochenreserve NICHT schonen, aktiv Verbrauch vorschlagen.

## 5. Durchsetzung — wer hält sich woran (27.10.2026)
**Regel: Alles, was Tokens verbraucht, hält sich daran — nicht nur Hintergrundprozesse.**
- **Hintergrundskripte mit `claude -p`:** `scripts/limit_gate.py` (`limit_gate.run(..., heavy=True)` für schwere/optionale Läufe → zusätzlich Wochen-60-%-Regel). Eingebaut in aldi_prospekt_ocr, build_f_photos, newsletter_scanner, caption_watcher, mail_to_calendar, schuljahr_modul_watcher, distrokid_social_paket. Selbsttest `python3 limit_gate.py` (0 Tokens). Laufende Prozesse laden Code nur beim Start → nach Änderung neu starten (resumable). Bewusst NICHT gegatet: nutzergetriebene Aufrufe (MP-Chat, telegram_bot, aufpeppen).
- **Ausreiz-Orchestratoren:** `scripts/samstag_ausreizen.py` (`gate()`, `_run_watchdog()`), Schwellen jetzt aus `limit_policy`; Env `AUSREIZEN_5H_LIMIT`/`AUSREIZEN_5H_HARD` überschreiben nur bewusst.
- **Ich selbst (Hauptsession):** Hook `context_check.py` hängt bei JEDEM Prompt eine LIMIT-STATUS-Zeile an (5h, Woche, geltende Schwellen, STOP/GATE-Hinweis). **Wenn dort GATE/STOP steht, gilt das für mich:** keine Subagents, keine großen Schreib-/Rechenläufe, Chris kurz informieren, bis Reset warten.
- **Subagents (Agent-Tool):** PreToolUse-Hook `~/.claude/hooks/agent_limit_guard.py` (in settings.json, Matcher „Agent") **blockiert den Start** bei 5h ≥ Gate oder Woche ≥ 60 % (Mo–Fr). Bei Block nicht umgehen — vertagen, Chris informieren. (Lücke 26.10. behoben: Welle-3-Agent riss das Fenster auf 96 %.) Lange Schreibläufe bevorzugt als `claude -p` via `limit_gate.run`.
- **Kommt „session/rate limit"-Meldung:** nicht quittieren → Quota prüfen; Fenster frei → fehlende Teile sofort neu starten, sonst Weckruf kurz nach `five_hour_reset_label`. Chris nur informieren („X von Y fertig, Rest ab HH:MM").
- **Manifest-Prinzip:** Jede Teilaufgabe schreibt eine eigene Output-Datei; fertig = Datei existiert.

## 4. Lehren/Messungen (Historie)
- Sa-Lauf 24.10. (Analogie-Check Kap. 31–36) startete erst Sa 19:28 bei 68 % und hatte nur 6 Kapitel → um 22:15 fertig bei Woche 79 %, Rest verfiel. Ursachen: Freitag-Start fehlte, Arbeitsvorrat zu klein.
- Do 29.10.2026 mittag: einmalig proaktiv Tipps geben, wie wir besser ausreizen (Fr-19:00-Start, größere Queue/Reserve-Aufgaben, Gate-Pausen statt Abbruch). Die frühere Sperre „bis Do nichts riskieren“ ist als Dauerregel in §2/§3 aufgegangen (Chris 27.10.: die Wochenregeln gelten grundsätzlich).

Verwandt: [[feedback_hintergrundjob_zuerst]], [[feedback_hintergrund_fork_lange_aktionen]], [[feedback_wartungsfenster_surfaces]], [[feedback_mp_chat_lag_ursache]].

### Messung 25.10.26: Tonie-Kosten (5h vs. Woche)
- 5h-Fenster und Wochenlimit sind getrennte Töpfe, Prozente NICHT vergleichbar. Woche ≈ 10× so groß wie 5h.
- Gemessen (4 `claude -p`-Jobs: Anton Lied + Mia Song/Lied/Geschichte): 5h +4 Pp, Woche ±0 (<1 %, Anzeige nur ganze %). Alle 7 Tonie-Teile ≈ 1 % Woche, selbst 3× neu erzeugen.
- **Why:** Chris fragte, was Tonies am Wochenlimit verbrauchen. **How to apply:** Tonie-Neuerzeugung fürs Wochenlimit vernachlässigbar; nur das 5h-Gate beachten. Messen: `/api/claudequota` vor/nach (kostenlos), Skript scripts/tonie_quotamessung.py.

### Lücke 26.10.26 abends (→ behoben 27.10., siehe §5)
5h-Fenster stand 19:30 bei 96 % (Gate 75 %/Watchdog 85 % griff nicht). Wahrscheinliche Ursache: Welle-3-Opus-Subagent (Agent-Tool, Kürzung Kap. 9–12) läuft NICHT über `limit_gate.py` und wird erst nach dem Überschreiten bemerkt (Abbruch bei 91 %). **How to apply:** Vor jedem Agent-/Subagent-Start `/api/claudequota` prüfen (nicht über 60 % starten); lange Kürzungs-/Schreibläufe bevorzugt als `claude -p` via `limit_gate.run`. Reset 22:49.


Verwandt: [[feedback_hintergrundjob_zuerst]], [[feedback_hintergrund_fork_lange_aktionen]], [[feedback_wartungsfenster_surfaces]], [[feedback_mp_chat_lag_ursache]].

**Wochenreset-Zeit (Chris 28.10.2026, im Account geprüft):** Reset ist samstags 23:00 Uhr (früher 0:00, Anthropic hat geändert). Nächster: Sa 31.10. 23:00. Immer den echten Account-Wert nehmen, nicht annehmen.
