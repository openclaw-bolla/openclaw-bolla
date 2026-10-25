---
name: feedback-token-warnung
description: Gegen Ende der Woche / bei niedrigem Restbudget vor tokenintensiven Aktionen warnen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec798ab3-fc08-4a1e-8841-4dc96b5b3f47
---

**Regel:** Wenn Chris < 25% Budget übrig hat UND noch 2–3 Tage bis zur Periode-Reset bleiben → vor jeder tokenintensiven Aktion automatisch warnen.

**Why:** Claude Pro hat ein begrenztes Periodenkontingent. Bei niedrigem Restbudget kurz vor Reset riskiert man, mitten in einer Aktion das Limit zu treffen.

**How to apply:** Sobald Chris den Reststand erwähnt (oder ich aus dem Kontext schließen kann dass es knapp ist): wenn < 25% UND 2–3 Tage übrig → proaktiv warnen bevor ich starte: "Du hast noch X% und noch Y Tage — diese Aktion könnte viel davon fressen, lieber auf Reset warten?" Nicht einfach loslegen. Auch ohne dass Chris fragt.
