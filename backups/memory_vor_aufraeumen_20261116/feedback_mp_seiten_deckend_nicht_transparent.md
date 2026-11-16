---
name: feedback-mp-seiten-deckend-nicht-transparent
description: Jede NEUE/geänderte MP-Seite (mission-control) braucht DECKENDE Karten/Flächen — halbtransparente rgba-Hintergründe sind auf dem MP-Hintergrund unlesbar; passiert bei neuen Seiten fast jedes Mal
metadata:
  type: feedback
---

Chris (10.11.2026, Englisch-Seite in MP): „hat wieder mal einen transparenten Hintergrund – bitte endlich merken, das passiert eigentlich jedes Mal“. Zweiter belegter Fall: AURORA-II-Hinweis-Karten 13.10.2026 (rgba 0.07 → deckend #1a1538).

**Why:** MP (`mission-control/index.html`) hat einen Verlaufs-/Video-Hintergrund. Karten mit `rgba(127,127,127,.1x)` (so war englisch.js zunächst für „neutral“ geschrieben) lassen ihn durchscheinen → Text schlecht lesbar.

**How to apply:** Bei JEDER neuen oder umgebauten MP-Seite/-Komponente (auch geteilte Clients wie englisch.js) Karten, Eingabefelder, Buttons, Erklärboxen, Balken mit **deckenden** Farben bauen (MP-Karte z. B. #1b1740 / Felder #262050 / Feld2 #3a3070; `--card` in index.html ist nur 0.88 deckend, `--card2` 0.92 → für Lesetext nicht ausreichend). Bei geteiltem Code Farben per CSS-Variablen je Umgebung setzen (englisch.js: `themeVars()` im mount, hell/dunkel nach Schriftfarbe). **Vor Meldung „fertig“ prüfen**, dass kein `rgba(…,0.x)` als Flächen-Hintergrund steht (grep), nur für dünne Rahmen erlaubt. Verwandt: [[project_englisch_trainer]].
