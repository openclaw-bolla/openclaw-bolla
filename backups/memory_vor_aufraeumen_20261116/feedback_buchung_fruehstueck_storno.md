---
name: feedback-buchung-fruehstueck-storno
description: Bei JEDER Hotel-/Reisebuchung immer Frühstück + Storno-Option prüfen und melden
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4d0edfc7-9efb-48d7-8948-a5ab7b012afb
---

Immer wenn ich eine **Buchung eintrage oder verarbeite** (Reiseplaner, Kurztrip-Planer, jeder andere Planer/Kontext), grundsätzlich prüfen und Chris melden:
1. **Frühstück** — inklusive oder nicht? (Booking-Mail: „Frühstück ist im Endpreis inbegriffen" o. ä.)
2. **Storno-Option** — kostenlos stornierbar bis wann? Frist konkret nennen.

**Why:** Chris übersieht das beim schnellen Buchen am Handy manchmal selbst (Beispiel 01.07.2026: Baden-Baden ohne Frühstück gebucht → storniert → neu). Ein kurzer Check von mir fängt solche Fälle ab, bevor die Reise da ist.

**How to apply:** Nicht nur still eintragen — beim Eintragen aktiv beide Punkte aus der Bestätigungsmail lesen und im Ergebnis-Report ausgeben (🍳 Frühstück, ⏰ Storno-Frist). Gilt für ALLE Buchungs-Planer, nicht nur den Haupt-Reiseplaner. Frühstück-Info in die Notiz des Planer-Eintrags packen (kein eigenes Feld vorhanden). Verwandt: [[reference_booking_profil]], [[reference_mc]].
