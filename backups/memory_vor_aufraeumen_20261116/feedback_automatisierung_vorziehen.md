---
name: feedback-automatisierung-vorziehen
description: "Bei wiederkehrenden Prozessen Automatisierung + Content-Vorbereitung EINMAL investieren, dann läuft jede Wiederholung schnell — bei echten Einmal-Aufgaben lohnt sich der Aufwand nicht"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-28T07:18:25.929Z
---

Bei Kurstag 3 (itslearning, 28.09.2026) fiel Chris auf, wie schnell die eigentliche Ausführung ging ("das
ging ja unglaublich schnell") — obwohl frühere Kurstage sehr lange gedauert haben. Grund: die ganze Arbeit
war in zwei getrennte Phasen aufgeteilt, die zu unterschiedlichen Zeitpunkten liefen.

**Das Prinzip (von Chris bestätigt, gilt allgemein für wiederkehrende Prozesse):**
1. **Automatisierung ist eine Einmal-Investition.** Alle DOM-Fallstricke/Selektoren/Fehlerquellen eines
   Prozesses (hier: `itslearning_post_kurstag.py`, siehe [[project_itslearning_automation]]) wurden über
   mehrere Durchläufe hinweg mühsam ausgebügelt. Sobald das Skript stabil ist, kostet jede weitere
   Wiederholung nur noch "Parameter tauschen", nicht mehr Entwicklung.
2. **Content-Vorbereitung von der Ausführung trennen.** Texte/Dateien/Inhalte können lange VOR dem
   eigentlichen Live-Lauf fertiggestellt werden (hier: Mitteilungstexte + PDF-Export schon am 26.09.
   erledigt, siehe [[feedback_limit_regeln]]). Wenn der eigentliche Anstoß kommt, gibt's
   nichts mehr zu erfinden, nur noch auszuführen.

**Wann sich das lohnt:** Nur wenn ein Prozess absehbar OFT wiederkommt (z.B. 19 Kurstage im Schuljahr,
siehe [[feedback_itslearning_workflow_bewaehrt]]). Bei echten Einmal-Aufgaben rechtfertigt der
Automatisierungsaufwand sich nicht — da bleibt's zwangsläufig langsamer, und Ad-hoc-Vorgehen ist okay.

**How to apply:** Bei jedem neuen wiederkehrenden Auftrag (nicht nur itslearning) früh prüfen: (a) lohnt
sich ein wiederverwendbares Skript/Template? (b) kann der Content-Teil zeitlich vom Ausführungs-Teil
getrennt und vorgezogen werden, sobald Leerlauf/Kontingent da ist (vgl.
[[feedback_limit_regeln]])? Beides aktiv anbieten, nicht nur wenn Chris danach fragt.
