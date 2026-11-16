---
name: feedback-fable-budget-disziplin
description: Arbeitsregeln für Fable-5-Nutzung — kein Durchpeitschen, Budget-Reserve halten, Häppchen im Hintergrund
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-08-13T08:21:13.840Z
---

# Fable-5-Arbeit: Budget-Disziplin (Chris, 01.07.2026)

**Why:** Chris will Fable 5 nutzen (genug Budget da), aber NICHT in die Limitfallen (5h-Fenster + Wochenlimit) laufen. Es gibt keine Eile — lieber schluckweise als die Flasche auf ex. Er will immer genug Budget für andere Alltags-Aktionen (Mails, MC, Schule) übrig behalten.

## ⚡ AUSNAHME: Fable-Intensiv-Fenster bis 07.07.2026 (Chris-Entscheidung 01.07., 23:40)
Solange Fable 5 zur **50 %-Wochenlimit-Rate auf Max** läuft (**bis 07.07.**, danach Credits = echtes Geld), wird **bewusst Fable-intensiv** gefahren — der **Engpass ist das Zeitfenster, nicht die Tokens**. In diesem Fenster:
- Die **token-schweren Brocken** hier reinlegen: AURORA-Vollpolitur (kapitelweise), englische Version in Premium-Qualität, weitere Hochqualitäts-Tasks.
- Reserve-Regel **gelockert** — das Wochenbudget resettet ohnehin regelmäßig (nächstes Reset Sa 04.07. 23:59). Nur das **5h-Fenster** respektieren (nicht überfahren → sonst Zwangspause bis Reset).
- **Ab 07.07.:** zurück zum Schwaben-Protokoll — Fable dann kostenpflichtig (Credits), vor jedem Fable-Call erst fragen. [[feedback_kosten_freigabe]]
- ⚠️ Die **07.07-Grenze ist Bollas frühere Recherche-Notiz, kein Anthropic-Live-Wert** → vor dem Vollgas gegenchecken.
- **Fable läuft NUR über die claude-CLI** (`claude -p --model claude-fable-5`), NICHT über den Agent-Tool-Layer (dort "unavailable").

## ⚠️ LEHRE 02.07. — warum die Ampel allein NICHT reicht (5h-Limit-Crash)
Die „Ampel vor dem Start" prüft nur EINMAL vorher — sie verhindert nicht, dass **ein einzelner großer Lauf** (ganzes Buch, Fable 2×) das 5h-Fenster überfährt. Konkreter Crash 01.07. nachts: Der Wächter lief **doppelt** (manueller nohup-Start + Cron feuerte in der 19-Min-Laufzeit, weil das done-Flag erst am Ende gesetzt wird) → zwei parallele Fable-Vollläufe → 5h-Fenster schoss auf ~97 %. Fix: **Exklusiv-Lock** (`fcntl.flock` auf `.aurora_fable_watcher.lock`) in `aurora_fable_watcher.py` — kein Parallellauf mehr.
**Für die AURORA-Vollpolitur zwingend:** (1) NIE das ganze Buch in EINEM Fable-Call — **kapitelweise Häppchen**. (2) Ampel **zwischen** den Häppchen neu prüfen, bei 5h >~50 % **pausieren bis Reset** (5h-Reset alle 5 h). (3) Lock gegen Parallelläufe. (4) Bedenken: die interaktive Opus-Session verbraucht PARALLEL mit — das 5h-Fenster teilen sich alle Prozesse.

## ⚠️ Update 13.08.2026 — Fable 5 braucht jetzt Credits (kostenpflichtig), Intensiv-Fenster vorbei
Bei einem Hintergrund-Fork-Versuch (`claude -p --model claude-fable-5 ...`) kam der Fehler **"Fable 5 requires usage credits"** — das kostenlose Intensiv-Fenster (war eh nur bis ~07.07. gedacht) ist längst vorbei, Fable läuft jetzt NICHT mehr im normalen Pro-Plan-Kontingent mit. **Vor jedem künftigen Fable-Call also erst Kosten nennen + Freigabe holen** (Schwaben-Protokoll, [[feedback_kosten_freigabe]]) — die alte "Ampel reicht"-Regel unten gilt nur noch fürs 5h-/Wochen-Fenster der übrigen Modelle, NICHT mehr für Fable selbst. Bei Hintergrund-Forks, die nicht rückfragen können: bei diesem Fehler NICHT abbrechen, sondern automatisch auf Sonnet ausweichen und das im Abschlussbericht klar kennzeichnen (so gehandhabt bei der AURORA-Kapitel-47-Überarbeitung).

## Grundregeln (außerhalb des Intensiv-Fensters)
**How to apply:**
- **Kein Durchpeitschen.** Fable arbeitet in **kleinen, abgegrenzten Häppchen** (kapitel-/themenweise), nie das ganze Buch in einem Rutsch.
- **So viel wie möglich im Hintergrund mit Subagenten** (wie beim letzten Mal) — Chris kann nebenher weitermachen.
- **Ampel vor JEDEM Fable-Schritt:** erst `/api/claudequota` prüfen (kostenlos), Zahlen nennen. Harte Stopp-Regeln:
  - 5h-Fenster über **~60 %** → Pause bis Reset.
  - Wochenbudget: **mind. 40 % Reserve** freihalten für alles andere. Reserve drunter → Stopp + Rückfrage.
- **Reihenfolge:** erst billige Diagnose/Konsultation (ein kompakter Fable-Lauf), dann GEMEINSAM entscheiden, welche Umsetzungs-Häppchen es wert sind. Nie blind lostippen.
- Fable zählt ~2× Opus gegen das Wochenlimit → siehe [[feedback-modell-auswahl]].

Gehört zum AURORA-Fable-Projekt: [[project-aurora-fable-optimierung]].
