---
name: feedback-grossprojekt-budget-check
description: "Vor größeren Projekten IMMER 5h+Wochen-Limit via /api/claudequota zeigen und Arbeit als Fork laufen lassen, um Budget für Kleinkram übrig zu halten"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 50aa2d48-8cd6-476b-a1b6-337065fba2d3
  modified: 2026-08-24T17:18:40.219Z
---

Bei größeren/länger laufenden Projekten (viel Code, viele Schritte) IMMER zuerst `/api/claudequota` abrufen und Chris die aktuelle 5h-% und Wochen-% zeigen, BEVOR losgelegt wird. Die eigentliche Umsetzung dann konsequent als Fork/Hintergrund laufen lassen.

**Why:** Chris meint mit "Budget" nicht Geld (das kostet bei Claude Code/Subagents eh nichts, siehe [[feedback_kosten_freigabe]]), sondern seine Anthropic-Nutzungslimits (5h-Fenster + 7-Tage-Kontingent im Pro Plan). Vereinbart erstmals bei der AURORA-Kapitel-47-Überarbeitung (13.08.2026, siehe aktuell.md-Historie: Ampel 13%→23%/5h, 33%→34%/Woche explizit gezeigt). Ziel: er will nach einem großen Projekt immer noch genug 5h- und Wochenbudget übrig haben für spontane kleinere Anfragen zwischendurch — nicht mitten am Tag ins Limit laufen.

**Harte Schwellen (übernommen aus der Fable-Budget-Regel, [[feedback_fable_budget_disziplin]], gilt jetzt generell für alle Modelle/größere Projekte):**
- **⛔ Restbudget unter 10 % → NICHT starten (Chris 03.09.2026).** Vor jedem größeren Projekt BEIDE Limits prüfen; hat das 5h-Fenster ODER das 7-Tage-Kontingent weniger als **10 % Rest** übrig (`five_hour_pct` bzw. `seven_day_pct` über 90 %), das Projekt gar nicht erst anfangen — Zahlen zeigen und bei Chris rückfragen (verschieben / auf Reset warten / Umfang kürzen). Harte Untergrenze, zusätzlich zu den weicheren Ampel-Schwellen unten.
- **5h-Fenster über ~60 % → Pause bis Reset.** Nicht weiterlaufen lassen, sondern anhalten und Reset abwarten (Zeit steht in `five_hour_reset_label`).
- **Wochenbudget: mindestens 40 % Reserve muss übrig bleiben** für Chris' Alltagskram (Mails, MP, Schule, Kleinanfragen). Rutscht die Reserve darunter (Wochen-% über 60 %) → stoppen und aktiv bei Chris rückfragen, nicht einfach weitermachen.
- Diese Schwellen gelten als Ampel-Grenze, nicht nur als grobe Orientierung — bei Überschreitung IMMER anhalten, nicht nur erwähnen.
- **Hook nur für die Notfall-Grenze (Chris 03.09.2026):** `context_check.py` prüft bei jedem Prompt `/api/claudequota` und meldet sich NUR, wenn das **5h-Fenster < 10 % Rest** hat (`five_hour_pct` > 90) → Block `🚨 5h-RESERVE FAST WEG`, Re-Warnung je +3 Punkte, Marker `/tmp/bolla_5hlow_<sid>`. Zweck: Chris soll am Book in der Schule nicht plötzlich ohne Bolla dastehen. Ein früher gebauter „ab 10 % Verbrauch"-Hook war zu nervig und wurde entfernt — der normale Budget-Check bleibt bewusst nur vor größeren Projekten.

**How to apply:**
- Vor Start eines größeren Projekts: `/api/claudequota` checken, 5h-% und Wochen-% + Ampelfarbe kurz nennen (nicht nur beiläufig in aktuell.md, sondern aktiv ansagen)
- Gegen die harten Schwellen oben prüfen — bei Überschreitung VOR Start warnen, ggf. Timing verschieben oder Umfang absprechen
- Bei langlaufenden/mehrteiligen Projekten (nicht nur einmalig vorher): Ampel **zwischen den Häppchen erneut prüfen**, nicht nur einmal zu Beginn — ein einzelner großer Lauf kann das 5h-Fenster trotzdem überfahren (Lehre aus dem AURORA-Crash 02.07.2026, s. [[feedback_fable_budget_disziplin]])
- Umsetzung selbst als Fork/Hintergrund laufen lassen (spart nicht direkt Budget, hält aber Chris' Hauptsession frei für Zwischendurch-Anfragen, siehe [[feedback_hintergrund_fork_lange_aktionen]])
- Nach Abschluss des Projekts erneut kurz Ampel zeigen (vorher/nachher-Vergleich, wie bei AURORA Kap. 47)
- Gilt für ALLE größeren Projekte künftig, nicht nur AURORA — z.B. auch für den World-Monitor in MP

**⏰ Temporäre Limit-Erhöhung (befristet):** Laut claude.ai-Kontoseite "Nutzung" (Screenshot 24.08.2026) ist das wöchentliche Claude Code-Limit im Pro-Plan **bis 31.08.2026 um 50% erhöht** ("Aktion"). Danach fällt es zurück auf den Standardwert. Die Seite zeigt Modell-Nutzung nur aggregiert als "Alle Modelle" — keine Aufschlüsselung nach Opus/Sonnet einzeln, klärt also NICHT die offene Frage ob Opus im Pro-Plan enthalten ist. **Update 24.08.2026 abends: Opus-Retest erfolgreich** (kurzer Testagent lief sauber durch, kein 403-Fehler mehr) — der Fehler beim Aufpeppen-Umbau am selben Tag war ein einmaliger Aussetzer, kein grundsätzliches Plan-Problem. Opus bleibt normal in der Modell-Hierarchie nutzbar. Bis 31.08. also ruhig etwas offensiver mit Wochenbudget umgehen, danach wieder auf Standard-Schwellen zurück.
