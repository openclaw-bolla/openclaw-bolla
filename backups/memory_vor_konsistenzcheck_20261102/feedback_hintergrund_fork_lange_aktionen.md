---
name: feedback-hintergrund-fork-lange-aktionen
description: "Große/langwierige Aktionen (Playwright-Läufe, Multi-Schritt-Automatisierung) immer als Hintergrund-Fork starten, nie blockierend im Chat"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 14c2129c-e27a-4adc-aece-dbffd934513e
  modified: 2026-07-23T09:15:27.740Z
---

Große, langwierige oder mehrstufige Aktionen (typisch: Playwright-Browser-Automatisierung über mehrere
Kurse/Objekte hinweg, lange Recherchen, Multi-Schritt-Workflows) IMMER als Hintergrund-Fork starten
(`Agent` Tool, `subagent_type: "fork"`), nicht blockierend in der laufenden Session ausführen.

**Warum:** Chris nutzt diese WSL-Terminal-Session parallel zum MP-Bolla-Chat. Wenn eine lange Aktion die
Session blockiert, muss er zum Weiterarbeiten auf den MP-Chat umsteigen — unnötige Reibung. Ein
Hintergrund-Fork lässt die Session währenddessen frei für andere Anliegen, Chris bekommt trotzdem eine
Fertig-Meldung.

**Wie anwenden:** Sobald erkennbar ist, dass eine Aufgabe mehrere Minuten dauert und/oder viele
Zwischenschritte/Tool-Aufrufe braucht (Beispiel: [[project_itslearning_automation]] Kurs-Umbauten), sofort
als Fork starten statt selbst durchzuarbeiten — auch ohne dass Chris explizit "im Hintergrund" sagt. Gilt
nicht für kurze, schnelle Einzel-Aktionen (die bleiben normal inline).

**✅ Präzisierung + Bestätigung (Chris, 21.09.2026 „genau so!"):** Zwei Stufen. (1) **Einzelnes langes Skript** (>~1–2 Min, keine Entscheidungen
dazwischen, z. B. Foto-Pool-Rebuild ~8 Min) → normaler Hintergrund-Prozess (`run_in_background`), Session bleibt frei, Fertig-Meldung kommt automatisch;
KEIN Fork (der würde nur Kontingent fürs Warten verbrennen). (2) **Mehrstufige Aufgaben mit vielen Einzelschritten/Urteilen** → Fork wie oben. Kurzes bleibt inline.
Dabei den Build so bauen, dass `/f` o. ä. währenddessen live bleibt (Staging-Ordner + Tausch). Session schließen = Prozess läuft weiter, aber Nacharbeit (Prüfen/Tauschen) passiert nicht → vorher sagen.
