---
name: feedback-kurstag-versand-regeln
description: Feste Regeln für jeden Kurstag-Versand (itslearning): Mitteilungs-Reihenfolge/Download-Zeitpunkt, nur Mitteilungs-Screenshot, Aufräumen nach Versand
metadata:
  type: feedback
---

Chris (02.11.2026, Kurstag 6) — gilt für JEDEN Kurstag:

0. **⏰ Post-Cron immer um 11:00 (nicht 13:00, nicht 14:30!)** am Versandtag (Di der Kurstag-Woche) — Chris 03.11.2026: ab der nächsten Woche braucht er mehr Zeit zum Prüfen (Kurstag 6 wurde ausnahmsweise 13:25 manuell gepostet). Beim Setzen des Crons also `0 11 <Tag> <Monat> *`. Das Skript verifiziert jetzt selbst (Ressourcen + Mitteilung sichtbar); das Ergebnis steht in den MC-Jobs.

1. **Download-Zeitpunkt in den Mitteilungen:** Folien + Praktikum werden NICHT „zu Beginn der Stunde“ heruntergeladen, sondern **zu Beginn des Praktikums** (nach dem Folienteil). Texte in dieser Reihenfolge: 1️⃣ Folien/Inhalt, 2️⃣ „Zu Beginn des Praktikums laden wir … herunter“, 3️⃣ Praktikum-Inhalt. Wiederkehrender Fehler früherer Kurstage.
2. **Screenshots:** Vorschau-PNG nur für die **Mitteilungen**. **Nie** eine Vorschau des Praktikums (HTML/PNG) in Desktop\temp ablegen. (Ergänzt [[feedback_mitteilungen_screenshot_vorschau]].)
3. **Aufräumen nach dem Versand** (am Tag des Posts/danach, ohne Rückfrage): alles Temporäre löschen — Desktop\temp-Vorschauen (auch alte, z. B. Kurstag-05-PNG), Handouts/Entwurf-Reste, scratch-Entwürfe, /tmp. Offener Punkt p_k6_aufraeumen in offene_punkte.json.
4. Chris' PPTX nie anfassen, PDF = 1:1-Export ([[feedback_pptx_nie_anfassen_pdf_1zu1]]); PDF neu exportieren, wenn er die PPTX nachträglich ändert (prüfe Änderungsdatum der PPTX vs. PDF vor dem Post).
5. **Praktikum-Entwurf vorher suchen (Chris 10.11.2026, Kurstag 8):** Ich hatte 08-Praktikum.html neu gebaut, obwohl in `Handouts/Entwurf/` schon Chris' eigener Entwurf lag („der ist besser“). **Vor jedem neuen Praktikum IMMER `Handouts/Entwurf/` (und Handouts/Praktikum/) nach `NN-*` prüfen** — vorhandenen Entwurf verwenden/verschieben (nach `Handouts/Praktikum/`), nur bei Fehlen selbst bauen.
