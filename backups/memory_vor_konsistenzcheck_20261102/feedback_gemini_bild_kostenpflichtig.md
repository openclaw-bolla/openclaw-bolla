---
name: feedback-gemini-bild-kostenpflichtig
description: Gemini-Bild-API kostet Chris jetzt Geld (kein Guthaben mehr) — nicht mehr als Gratis-Bildquelle nutzen
metadata:
  node_type: memory
  type: feedback
---

# Gemini-Bildgenerierung ist für Chris NICHT mehr gratis

Chris (10.09.2026): „gemini ist nicht kostenlos ich habe dort kein budget mehr."

Gilt für die Google-Gemini-Bild-API (`gemini-2.5-flash-image` u.ä.) — das früher großzügige
Gratis-Kontingent ist bei ihm aufgebraucht, jeder Call kostet jetzt.

**Warum wichtig:** In MP war Gemini bisher die stille „Gratis"-Zweitquelle für Cover
(3 Cover-Vorschläge = 1× Pollinations gratis + 2× Gemini ~7 ct). Das war also gar nicht mehr
gratis. Passt zu [[reference_gemini_billing]] (Gemini generell bezahlt, kein Free-Credit).

**How to apply:**
- Für **kostenlose Bilderzeugung**: Pollinations (kein Key, aber anonymer Tier abgespeckt —
  liefert teils nur noch `sana`) **oder besser Cloudflare Workers AI FLUX.1-schnell**
  (`cf_workers_ai_generate`, 10.000 Neuronen/Tag ≈ 230 Bilder, Reset 0 Uhr UTC, Chris hat
  Account+Token schon → `config/cloudflare_token.json`). Cloudflare ist in MP-BildGen längst drin.
- **Gemini nur** wenn Chris es explizit will/freigibt, oder als reiner Notnagel-Fallback.
- Kosten für Gemini-Bilder wie jede kostenpflichtige API vorher ansagen ([[feedback_kosten_freigabe]]).
- Betrifft auch [[feedback_bildgenerierung]] (dort Pollinations.ai als Default) — Cloudflare-FLUX
  ist die bessere Gratis-Wahl, wenn Qualität zählt.

Siehe Cover-Umbau „Bolla Songs" 10.09.2026 in [[feedback_aktuell_md]]-Verlauf.
