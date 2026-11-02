---
name: feedback_status_bestaetigung_sofort
description: "Erledigungsmeldungen (auch nebenbei/mitten im Themenwechsel) sofort im Board/Memory festhalten, nicht verzögern"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f38d6dd9-009c-43a1-bbc4-6937431f96b7
  modified: 2026-07-23T16:12:04.421Z
---

Wenn Chris eine Erledigung meldet ("X ist raus", "erledigt", "geschickt", "fertig") — auch nur als Nebensatz
mitten in einem ganz anderen Thema — sofort in diesem Moment den passenden Board-Eintrag (`data/board.json`)
und ggf. Memory aktualisieren, BEVOR zum nächsten Punkt weitergegangen wird. Nicht "merk ich mir, mach ich
später".

**Why:** Am 23.07.2026 hat Chris nebenbei bestätigt, dass er die LinkedIn-Vernetzungsanfrage an Daniela
Hanauer selbst verschickt hat ("vernetzung ist raus"). Direkt danach ging's im selben Gespräch weiter zu
Azure-Mail-Fragen und dann zum itslearning-Kurstag-Test — der Board-Eintrag blieb fälschlich auf "open"
stehen, weil die Erledigung im Themenwechsel unterging. Chris wirft bewusst oft 2-4 Dinge gleichzeitig in
eine Nachricht ([[feedback_projekte_entspannt]]-Stil, entspannt nebenbei) — das ist sein normales Muster,
nicht etwas das er ändern soll. Die Pflicht, nichts zu verlieren, liegt bei mir.

**How to apply:** Bei jeder Nachricht von Chris kurz prüfen: enthält sie (auch beiläufig) eine
Status-Bestätigung zu einem offenen Board-Punkt? Falls ja: Board/Memory-Update SOFORT, nicht am Ende des
Gesprächs oder der Session. Zusätzlich bei der Session-Ende-Routine ([[feedback_session_ende]] falls
vorhanden, sonst CLAUDE.md-Routine) einen kurzen Konsistenz-Check einbauen: Gab es im Gesprächsverlauf
Erledigungsmeldungen, die noch nicht im Board reflektiert sind?
