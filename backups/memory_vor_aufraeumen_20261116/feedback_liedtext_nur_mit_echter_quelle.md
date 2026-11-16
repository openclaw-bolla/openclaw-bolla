---
name: feedback-liedtext-nur-mit-echter-quelle
description: Tonie-Kinderlied-Word (Liedtext) nur nach Abgleich mit echter Quelle füllen, nie aus Modell-Gedächtnis; Playback-Noten ebenfalls aus Quelle
metadata:
  type: feedback
---

Liedtext-Word für Tonie-Kinderlieder immer erst mit echter Quelle abgleichen, bevor die Word gefüllt wird (Chris 28.10.26).

**Why:** Der aus dem Gedächtnis erzeugte Text für „Der Kuckuck und der Esel" wich ab („einen Streit" statt „einmal Streit", Anführungszeichen ergänzt). Auch Melodien aus dem Gedächtnis lehnt das Modell ab.

**How to apply:** `tonies_liedtext()` in scripts/mission_control_api.py holt jetzt den Text aus de.wikibooks Liederbuch (`_tonies_lied_quelle`), lässt Claude nur gliedern und gleicht wörtlich ab; ohne Quelle/bei Abweichung KEIN Word, Fehlermeldung. Quelle steht unten im Word. Noten (data/tonie_noten.json) bevorzugt aus Wikibooks-LilyPond übernehmen (Beispiel Kuckuck, mit "auftakt" und Pause "R"; deutsches H statt B). Vorhandene Noten: Entchen, Hänschen klein, Kuckuck. Lücke: für Entchen/Hänschen findet die Wikibooks-Suche keine Quelle → Word würde abgelehnt; ggf. weitere Quelle ergänzen. Siehe [[project_tonie_zwillinge]].
