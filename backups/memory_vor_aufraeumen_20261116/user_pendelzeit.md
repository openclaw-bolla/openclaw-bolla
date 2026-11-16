---
name: pendelzeit-schule
description: "Chris' Unterrichtszeiten + 20 Min An-/Abfahrt = wann er von/zu Hause ist (für Verfügbarkeits-Einschätzung)"
metadata: 
  node_type: memory
  type: user
  originSessionId: 5f0e023b-525a-40af-8dff-17bc6d20ce73
  modified: 2026-08-27T08:33:36.301Z
---

# Pendelzeit Schule — wann Chris zu Hause / unterwegs ist

Chris unterrichtet am **Lessing-Gymnasium**. Seine Unterrichtstermine stehen im Kalender (Kategorien „Lessing I" / „Lessing II", mit Uhrzeiten). Aus diesen Daten lässt sich seine Verfügbarkeit ableiten:

- **Anfahrt:** ~20 Min → Abfahrt von zu Hause = **Unterrichtsbeginn − 20 Min**
- **Abfahrt/Heimweg:** ~20 Min → zu Hause = **Unterrichtsende + 20 Min**
- **Zusatzpuffer:** Nach Unterrichtsende bleibt Chris oft noch, um Schülerfragen zu beantworten — die 20 Min Heimweg sind also ein **Minimum**, kein Fixwert. „Frühestens ca. X Uhr zu Hause" ist die richtige Formulierung, nicht „genau um X Uhr".

**Why:** Chris möchte, dass ich anhand des Kalenders + dieser Pendelzeit selbst einschätzen kann, wann er unterwegs bzw. wieder zu Hause (und damit für eine Session erreichbar) ist — ohne dass er es jedes Mal sagen muss. Er hat das am 27.08.2026 explizit präzisiert, weil die reine Unterrichtsende+20-Min-Rechnung die Nachfrage-Zeit an der Schule ignoriert.

**How to apply:**
- Kalender via MC-API `/api/calendar` (Termine mit Kategorie „Lessing I/II" sind Unterricht).
- Beispiel: Unterricht endet 13:15 → Chris ist **frühestens ca. 13:35** zu Hause, ggf. später wegen Schülerfragen.
- Bei Begrüßungen / „wann hast du Zeit"-Einschätzungen / Planung von längeren Aktionen mitdenken: Ist Chris laut Kalender gerade in der Schule, auf dem Heimweg (inkl. Zusatzpuffer), oder schon/noch zu Hause?
- Verknüpft mit [[ki-workshop-lehrer]] (gleiche Schule) und der Session-Pausen-Logik [[feedback_session_pause]].
