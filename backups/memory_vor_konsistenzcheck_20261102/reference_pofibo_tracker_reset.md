---
name: reference-pofibo-tracker-reset
description: "Korrekter Reset-Ablauf für Chris' POFIBO-Tracker-Karte (Geldbörse) — Anleitung des Herstellers ist unvollständig"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3eea9f17-af36-4c6c-99bc-0200da0f7635
  modified: 2026-07-21T14:09:05.561Z
---

Chris' POFIBO-Tracker-Karte (in der Geldbörse, Bluetooth/Google-Mein-Gerät-Finden-kompatibel) ließ sich
lange nicht koppeln — Pairing hing endlos in der Sanduhr. Ursache war kein Hardware-/Zertifizierungsproblem,
sondern eine **unvollständige Reset-Anleitung** des Herstellers.

**Falsch/unvollständig laut Anleitung:** 5× schnell hintereinander den Button drücken.

**Tatsächlich nötig:** 5× schnell drücken, aber **beim letzten (5.) Mal die Taste gedrückt halten, bis
zwei etwas hellere Töne ertönen.** Erst dann ist die Karte wirklich auf Werkseinstellungen zurückgesetzt.
Danach erscheint sofort das Kopplungs-Popup und die Karte wird sofort erkannt.

**Warum das hier steht:** Falls Chris (oder eine der Tracker-Karten in der Familie) das Ding nochmal
zurücksetzen muss — nicht erst wieder stundenlang suchen, sondern gleich den korrekten Ablauf nennen.
Ursprünglich als Sackgasse eingeschätzt (siehe alter Eintrag in `aktuell.md`, 21.07.2026) — war aber
lösbar, ein geplanter Ersatzkauf (Chipolo CARD Point) wurde daraufhin **nicht** getätigt.
