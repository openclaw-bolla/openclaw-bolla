---
name: feedback-blaue-einschuebe-duo-reader
description: Standard-Mechanismus für ALLE Buchprojekte (AURORA II, III …): nachträgliche Einschübe als BLAUE Vorschläge im Duo-Reader, Tippen → Behalten/Weg damit
metadata:
  type: feedback
---

Chris 09.11.2026: „genau so sollte das sein … diesen Mechanismus für alle Zeiten merken, z. B. AURORA III“.

**Mechanismus:** Nachträgliche Ergänzungen (Saat-Einschübe, Figuren-Pass, spätere Korrekturen) werden NICHT stumm in den Text geschrieben, sondern als Eintrag in `einschub_vorschlaege` (Felder id, saat/label, kapitel_titel, text, begruendung, status `wartet`, erstellt_am) UND gleichzeitig im Kapiteltext eingebaut. Im Duo-Reader `/aurora` (`mission-control/aurora-reader.html`, eigene Seite, nicht index.html) erscheint der Text hellblau; Kapitelliste zeigt „✎ n blau"; Tippen öffnet ein Fenster mit Begründung und **✓ Behalten** (`annehmen`, Text bleibt) / **✗ Weg damit** (`ablehnen`, Text wird aus dem Kapitel gelöscht) über `/api/aurora2/einschub-entscheidung`.

**Why:** Chris überfliegt die Kapitel auf dem Duo und entscheidet Stelle für Stelle; er will nichts Verstecktes im Buch. Pannenlehre: Der Reader kannte zunächst nur Satz-Markierungen (lila) — neue Markierungsarten müssen in `aurora-reader.html` UND in `index.html` (MC) eingebaut werden, sonst sieht Chris sie nicht.

**How to apply:** Für AURORA III denselben Mechanismus ab Anfang nutzen (Beispielcode: `scripts/aurora2_spannung_uebernahme.py` ab Zeile ~160, Einbau-Funktion; `scripts/aurora2_figuren_pass.py`). Nach Einbau immer prüfen, dass `neu in kapitel.text` gilt und der Reader-Endpunkt die Einträge liefert. Siehe [[feedback_blaue_markierung_vorschlaege]], [[project_aurora_ii]], [[project_aurora_ii_optimierungen_fuer_iii]].
