---
name: feedback-blaue-markierung-vorschlaege
description: Muster „blaue Markierungen" aus AURORA II (Vorschläge im Text sichtbar, einzeln bestätigen) — Chris: hervorragend, für analoge Aktionen unbedingt anwenden
metadata:
  type: feedback
---

Chris (14.10.2026): Das **blaue Markieren in AURORA II funktioniert „hervorragend"** — bei analogen Aktionen unbedingt wieder so machen.

**Das Muster:** Änderungsvorschläge (Einschübe, Umformulierungen) werden NICHT still in den Text geschrieben, sondern **direkt im Text blau markiert** eingefügt. Chris sieht sie beim Lesen im Kontext und entscheidet je Vorschlag: annehmen / ablehnen (Text wird wieder entfernt) / Korrektur-Wunsch. „Nichts tun = bleibt drin". Der Status je Kapitel wird in der Liste links live gezählt („✎ N von M offen (blau)" → grün „entschieden ✓"), Daten in `einschub_vorschlaege` mit `status` (wartet/uebernommen/abgelehnt/korrektur_angefragt), Backup + Protokoll je Änderung. Umsetzung: `mission-control/index.html` (aurora2FpBadges/aurora2FpEinschubZaehl), API `/api/aurora2/einschub-entscheidung`.

**Why:** Chris liest selbst und behält die Kontrolle; sichtbare Vorschläge im Kontext sind für ihn viel leichter zu beurteilen als Listen/Berichte (vgl. [[feedback_selbst_entscheiden_keine_berichte]]) und nichts geht unbemerkt verloren ([[feedback_mp_satzuebernahme_nie_verlust]]).

**How to apply:** Überall, wo ich an Texten/Dokumenten arbeite, die Chris selbst prüft (Buchkapitel, Songtexte, Anleitungen, Schüler-Material, Mailentwürfe …) und die Änderungen bei ihm landen: Vorschläge visuell markiert + einzeln entscheidbar + Statuszähler, statt stiller Überschreibung. Hängt an [[project_aurora_ii]], [[project_aurora_ii_optimierungen_fuer_iii]].

**Kanon-Konflikte (Chris 14.10.2026, „2"):** Auch Funde aus Kanon-Liste/Analogie-Check/Zahlen-Abgleich ([[project_aurora_ii_optimierungen_fuer_iii]], [[feedback_aurora_zahlen_exakt]], [[feedback_aurora_ii_analogie_check]]) erscheinen als **blaue Vorschläge** im Text, nicht als stille Korrektur. Bestätigte Entscheidungen wandern danach als Eintrag in die `kanon`-Liste in `aurora2.json`, damit der Satz-Korrekturdialog nicht dagegen läuft.
