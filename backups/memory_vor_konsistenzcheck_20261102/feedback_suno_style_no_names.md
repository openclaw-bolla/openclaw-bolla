---
name: feedback-suno-style-no-names
description: Suno-Style-Feld NIE mit Künstler-/Bandnamen — proaktiv durch beschreibende Sound-Begriffe ersetzen
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d6d4a31d-366a-483e-a4a1-e9b064b9cbb7
---

# Suno Style-Prompt: keine Künstler-/Bandnamen

Suno **filtert/ersetzt Künstler- und Bandnamen im „Style of Music"-Feld** (Copyright) → der Groove-Hinweis geht verloren, der Take wird beliebig.

**Regel:** Künstler-/Bandnamen (z.B. „Mungo Jerry", „In the Summertime", „like Billie Eilish") NIE direkt in den Style schreiben. Stattdessen **proaktiv selbst** den Sound mit beschreibenden Genre-/Instrument-/Groove-Begriffen umschreiben — ich mach das von allein, Chris muss nicht dran erinnern.

**Beispiel:** `Mungo Jerry "In the Summertime"` → `early-70s skiffle jug-band shuffle groove, bouncy swung rhythm`.

**Gilt für:** alle Suno-Styles UND den Bolla-Songs-Autogenerator ([[reference_bolla_songs]]). Beim Bauen von Style-Prompts (auch im MP-Backend, falls Vorbild-Namen reingeraten) immer name-frei halten.

**Warum:** name-freier, beschreibender Style trifft den Vibe zuverlässiger als ein Name, den Suno eh rauswirft. Doppelter Bonus: vermeidet Soundalike-/Rechte-Risiko ([[project_suno_distrokid_blocklist]] — Billie-Eilish-Falle).
