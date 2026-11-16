---
name: feedback-kostenlose-alternative-zuerst
description: Bei jedem Projekt zuerst eine kostenlose Alternative vorschlagen/testen, bevor ein bezahlter Dienst (Gemini, MAI …) genommen wird
metadata:
  type: feedback
---

Für ALLE Projekte gilt: Erst eine kostenlose Alternative vorschlagen und testen, bevor ich einen bezahlten Dienst einsetze (Gemini, MAI, …). Auch wenn der bezahlte Dienst billig wäre (Gemini ~3 ct/Tag), ist es oft unnötig.

**Why:** Rezept des Tages (28.10.2026): Gemini-Prepay war leer, ich baute MAI als Fallback ein — Chris: zu teuer, nimm Cloudflare. Das Cloudflare-Bild (flux-1-schnell, Free-Tier) ist laut Chris „top". Gemini hätte gereicht, war aber nicht nötig.

**How to apply:** Bildgenerierung zuerst Cloudflare Workers AI (`cf_workers_ai_generate`, flux-1-schnell), erst bei echtem Qualitätsproblem teurere Quelle vorschlagen. Gilt analog für Text/Audio/Sonstiges: kostenlose Option testen, Ergebnis bewerten, bezahlte nur mit Begründung. Siehe [[feedback_automatisierung_vorziehen]], [[feedback_limit_regeln]].
