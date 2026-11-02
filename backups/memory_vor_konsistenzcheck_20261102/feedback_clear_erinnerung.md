---
name: clear-erinnerung
description: "Chris proaktiv an /clear erinnern, wenn eine Aktion abgeschlossen ist — gegen Token-Schneeball langer Sessions"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5f0e023b-525a-40af-8dff-17bc6d20ce73
---

# Nach abgeschlossenen Aktionen an /clear erinnern

Immer wenn eine Aufgabe/Aktion sauber abgeschlossen ist (natürlicher Schnitt, Stand in Memory/aktuell.md gesichert), Chris **proaktiv auf `/clear` hinweisen** — besonders nach größeren Aufgaben oder Marathon-Phasen.

**Why:** Lange Sessions verursachen einen Token-Schneeball — bei jeder neuen Nachricht wird der komplette bisherige Verlauf erneut als Input mitgeschickt, jeder weitere Schritt wird teurer. Ein `/clear` startet frisch und macht alles wieder günstig. Chris hat das Limit-Verhalten anfangs nicht verstanden (dachte „nichts gemacht, trotzdem 26% weg") — die Ursache war die lange Session, nicht aktive Arbeit.

**⚠️ Opus 4.8 = 1M Context → Crash-Risiko in WSL (erkannt 02.06.2026):**
Opus 4.8 hat als Default ein **1M-Token-Kontextfenster** (5× größer als die üblichen 200k). Folge: Claude Codes Auto-Compact greift VIEL später, der Kontext wächst über Stunden ungebremst, der Node-Prozess frisst immer mehr RAM. In WSL mit RAM-Limit (~10 GB laut [[reference_wsl]]) führt das irgendwann zum **Absturz der Session** — genau das ist Chris am 01./02.06. passiert (seit Vortag-Mittag kein `/clear`).
→ **Bei Opus-4.8-Sessions DEUTLICH früher zum `/clear` raten** als bei Sonnet — nach jedem abgeschlossenen Thema, nicht erst nach Stunden. Das ist nicht nur Kostenersparnis, sondern Crash-Vermeidung. Sonnet 4.6 (200k) ist hier robuster — passt zur [[feedback_modell_auswahl]]-Strategie (Sonnet als Default).

**⚠️ NICHT NERVEN (25.06.2026):** Chris fand die /clear-Erinnerung **zu häufig**. Ursache: (a) Hook-Schwelle stand auf 150k = nur 15% von 1M → feuerte fast jede Session; jetzt **400k** ([[feedback_kontext_warnung_hook]]). (b) Ich hatte den Hinweis zusätzlich in fast JEDER Antwort selbst nachgeplappert. → **Regel: /clear-Hinweis MAXIMAL 1× pro Session, und nur wenn der Hook (≥400k) ihn liefert ODER ein echter Marathon vorliegt. NICHT in jeder Abschlussmeldung wiederholen.** Im Zweifel weglassen.

**How to apply:**
- `/clear` kann NUR Chris auslösen, ich nicht. Ich kann nur erinnern.
- Erinnern beim **natürlichen Abschluss** einer Aktion (Aufgabe fertig, committet, Memory aktuell) — DA ist der sichere Moment.
- NICHT mitten in einer laufenden Aufgabe erinnern.
- „Stündlich" geht nicht zuverlässig — ich habe keine tickende Uhr, reagiere nur auf Nachrichten. Daher: an Aktions-Abschlüsse koppeln, nicht an feste Zeit.
- **Vor dem `/clear`-Hinweis: aktuell.md AKTIV updaten** (nicht nur prüfen!) — offene Fäden, nächste Schritte, relevante Dateipfade — dann Git commit + push. Erst danach den Clear-Hinweis geben. (Gelernt 16.06.2026: Chris hat geclearet und hatte danach offene Fragen zum laufenden Thema — Kontext war weg.)
- Kurz halten — ein knapper Hinweis reicht, kein Drängen.
