---
name: feedback-brain-graph-pflege
description: Bolla's Brain-Graph in MP ist kuratiert, nicht automatisiert — proaktiv pflegen statt warten bis Chris eine Lücke findet
metadata:
  node_type: memory
  type: feedback
  originSessionId: c9dc3abd-da45-49d8-af00-98405689704b
---

Der Node-Graph auf der 🧠 „Bolla's Brain"-Seite in MP (`mission-control/index.html`, Funktion `initBrain()`) ist eine **fest codierte Liste** (`nodes`/`links`-Arrays), kein Live-Abgriff aus den Memory-Dateien. Er aktualisiert sich nicht von selbst.

**Why:** Chris fragte am 04.09.2026 „und in Zukunft automatisch anpassen?", nachdem ihm aufgefallen war, dass Anne (Tochter) seit Erstellung des Graphen am 03.04.2026 komplett fehlte und mehrere andere Lücken/Fehler entstanden waren (Riverty-Fall längst erledigt aber noch drin, „Surface Laptop" statt korrekt „Studio", Book fehlte komplett). Eine vollautomatische Version (Skript liest alle Memory-Dateien) wäre möglich, aber unerwünscht: dann würden auch Verwaltungs-Einzelfälle wie Konstanz-Verwarnung oder ADAC-Kündigung automatisch reinrutschen — genau das, was Chris beim Riverty-Fall bewusst rausgenommen haben wollte. Der Graph soll „wer ich bin" zeigen (Dauerthemen, Personen, Infrastruktur), nicht jeden Vorgang.

**How to apply:**
- Wenn ich eine neue Memory-Datei vom Typ `user` oder `project` anlege, die ein **Dauerthema** ist (neues Hobby, neues laufendes Projekt, neue Person in Chris' Leben, neues Dauer-Tool) → von mir aus kurz prüfen, ob's in den Brain-Graph gehört, und einpflegen. Nicht erst warten bis Chris die Lücke selbst findet.
- **Nicht** aufnehmen: einmalige Verwaltungsvorgänge, befristete Fälle (Behörden-/Inkasso-Sachen, Kündigungen, Bußgelder) — die kommen erst rein, wenn sie zu einem echten Dauerthema werden, und sollten raus, sobald sie erledigt sind (wie Riverty am 04.09.2026 entfernt).
- Nach jeder Änderung: `node --check` auf die extrahierte `initBrain()`-Funktion laufen lassen (Syntax-Check), dann live per curl gegen `127.0.0.1:18790/` verifizieren dass die neuen IDs im HTML auftauchen. Kein Server-Neustart nötig (`index.html` wird mit `Cache-Control: no-store` direkt von Platte serviert).
