---
name: feedback-aurora-ii-analogie-check
description: "AURORA II: nach jedem fertig korrigierten Kapitel proaktiv an Analogie-Check erinnern und durchführen — Korrekturen des gerade fertigen Kapitels gegen alle bereits bearbeiteten Kapitel gegenchecken"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 69b94b61-8361-478c-88f8-a8df7365dfb8
  modified: 2026-09-15T11:06:18.347Z
---

Chris' Wunsch (15.09.2026, direkt nachdem Kapitel 1 fertig durchkorrigiert war): **nach jedem
Kapitel, das er in AURORA II fertig bearbeitet hat, soll ich ihn proaktiv daran erinnern**, dass ein
Analogie-Check ansteht — und ihn dann auch durchführen, nicht nur ankündigen.

**Ablauf:**
1. Sobald Chris ein Kapitel als fertig korrigiert meldet (oder ich selbst merke, dass seine
   Korrekturrunde zu einem Kapitel abgeschlossen ist — z. B. keine `wartet_entscheidung`-Einträge
   mehr offen): kurz proaktiv ansprechen, dass jetzt der übliche Analogie-Check drankommt.
2. Alle `satz_markierungen` mit `status == "uebernommen"` (plus `abgelehnt` als Gegenprobe) DES GERADE
   FERTIGEN Kapitels als Muster nehmen (Fehlerklassen ableiten wie beim ersten Durchgang: Wortwiederholungen,
   Business-Jargon, redundante Füllsätze, schwache Pointen, Zahlen-/Timing-Ungenauigkeiten usw.).
3. Damit **alle bereits vorher bearbeiteten/fertigen Kapitel** (nicht die noch kommenden, unbearbeiteten)
   erneut durchsuchen — es kann sein, dass ein Muster erst durch die neuesten Korrekturen sichtbar wird
   und in früheren, schon "fertigen" Kapiteln trotzdem noch drinsteckt.
4. Ergebnis wie beim ersten Mal: Bericht (Markdown, `workspace/scratch/`), keine automatischen Änderungen
   an `aurora2.json` außer nach Chris' ausdrücklichem OK je Fund.

**Wichtig — Modellwahl:** [[project_aurora_ii]] legt fest, dass ALLES inhaltliche an AURORA II auf
`claude-opus-5` läuft (Chris-Entscheidung 13.09.2026), nicht Sonnet-Standard. Der Analogie-Check ist
inhaltliche Textarbeit am Buch — also nicht als normaler `fork` (der immer auf meinem eigenen Modell
läuft), sondern als frischer Agent mit explizitem `model: "opus"` starten.

**Praktischer Vorlauf (erster Durchgang, 15.09.2026):** Nach Kapitel 1 (46 Korrekturrunden) wurden
Kapitel 2–9 (~19.200 Wörter) einmal komplett gegengecheckt, ein echter Fund (Kap. 2 "viermal" vs.
overall etabliertes "dreimal"), auf Chris' OK korrigiert. Ab jetzt läuft das iterativ weiter: nach
Kapitel 2 gegen Kapitel 1, nach Kapitel 3 gegen Kapitel 1+2, usw. — die Musterbibliothek wächst mit
jedem Kapitel.

**Why:** Chris übersieht selbst nach eigener Aussage "bestimmt einiges" an analogen Fehlern in bereits
abgehakten Kapiteln, wenn ein neues Muster erst später auffällt. Ein automatischer Rückwärts-Check
nach jedem Kapitel fängt das ab, ohne dass er selbst daran denken muss.

**How to apply:** Bei jeder künftigen AURORA-II-Session: wenn ein Kapitel fertig wird, diesen Check
proaktiv ansprechen (nicht erst warten bis Chris fragt) und durchführen.
