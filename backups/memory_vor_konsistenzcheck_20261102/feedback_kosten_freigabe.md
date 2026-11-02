---
name: Kostenpflichtige APIs - immer erst fragen
description: Vor jedem kostenpflichtigen API-Aufruf (PiAPI, etc.) explizite Freigabe von Chris einholen
type: feedback
originSessionId: dfa8875a-0ac2-4b8c-bbe7-b04d2c559b7d
---
Vor **extern kostenpflichtigen** API-Aufrufen (PiAPI, Gemini, OpenAI etc.) zuerst Chris fragen und Kosten nennen. **NICHT** bei Claude Code / Subagents — das läuft über den Pro Plan und kostet Chris nichts extra.

**Why:** Chris hat einen Claude Pro Plan — Haiku/Sonnet/Opus Subagents in Claude Code Workflows sind inklusive. Kosten-Rückfrage bei Subagents nervt unnötig. Konkreter Vorfall: 15 Gemini-Bilder ohne Rückfrage generiert → ~$0.58, hat geärgert. Das gilt für Pay-per-use Drittdienste, NICHT für Claude selbst.

**How to apply:**
- Claude Code Subagents (Haiku, Sonnet, Opus in Workflows): EINFACH MACHEN, nicht fragen
- Extern kostenpflichtig (PiAPI, Gemini Image, Kling, Luma, OpenAI etc.): Immer erst Kosten nennen + Freigabe holen
- Kostenlose Alternativen IMMER bevorzugen: Pollinations statt Gemini/Flux für Bilder
- Bei Pollinations: Prompt mit "no text, no typography, pure visual" verwenden
- Guthaben-Warnungen bei < 0.50 Credits aktiv melden
- **NIE Ausgaben verharmlosen** ("Pillepalle", "Kleckerbetrag", "lohnt sich nicht" o.ä.) — auch 1-5 €/Monat ernst nehmen. Chris-Zitat (22.06.): „jeder € zählt". Beträge neutral nennen, Sparpotenzial anerkennen, nie kleinreden.
