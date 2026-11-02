---
name: feedback-mitteilungen-screenshot-vorschau
description: "itslearning-Mitteilungen (und ähnliche Veröffentlichungen) vor Freigabe IMMER als Screenshot in Desktop\\temp ablegen, nicht nur als Text im Chat zeigen"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-07T08:28:53.687Z
---

Bei Kurstag 4 (07.09.2026) hatte ich die 4 Mitteilungstexte nur als Rohtext im Chat gezeigt (aus dem
Python-Skript kopiert). Chris' Korrektur: **das war früher schon als Screenshot in `Desktop\temp` üblich,
soll ab sofort immer so laufen** — nicht nur eine Ausnahme für dieses eine Mal.

**Why:** Chris will Mitteilungen so sehen, wie sie später ungefähr wirken (Karte/Kurs/Datum sauber
gruppiert), nicht als Python-Code mit Escape-Zeichen im Terminal — und an einem festen, bekannten Ort
(siehe [[feedback_pruef_ordner_temp]]), nicht nur flüchtig im Chat-Verlauf.

**How to apply — vor JEDER Veröffentlichung/Freigabe von Mitteilungstexten (itslearning o.ä.):**
1. Kleine, saubere HTML-Vorschauseite bauen (Karten pro Kurs: Kurs-Kürzel, Datum/Zeit, Text) — kein
   Server nötig, reines lokales HTML.
2. Per Playwright screenshotten (`LD_LIBRARY_PATH` auf `browser_libs/extracted/...` setzen wie im
   itslearning-Skript, `full_page=True`).
3. PNG nach `/mnt/d/OneDrive/Desktop/temp/` speichern, sprechender Dateiname
   (`Mitteilungen_Kurstag<NN>_Vorschau.png`).
4. Erst NACH Chris' Freigabe den eigentlichen Playwright-Post-Lauf (`itslearning_post_kurstag.py`)
   anstoßen.
5. Nach erfolgreichem Post die Vorschau-PNG wie andere temp-Dateien wieder aufräumen (siehe
   [[feedback_pruef_ordner_temp]] — proaktiv fragen ob löschbar).

Verwandt: [[feedback_itslearning_workflow_bewaehrt]] (Vorab-Check-Schritt, jetzt um dieses Screenshot-
Format ergänzt), [[project_itslearning_automation]].

## 🔁 Bekräftigt 26.10.2026 (Kurstag 5)
Ich hatte die Texte wieder als .md in scratch abgelegt und auf Chris' „Mach vorher das Screenshot-Zeug" nicht gedacht. Chris: „bitte die texte immer als screenshot in temp (hatten wir schon, dass ich mds unübersichtlich finde)". **Nie wieder .md zum Lesen für Chris** ([[feedback_keine_md_dateien_fuer_chris]]) — Entwürfe direkt als Vorschau-PNG in Desktop\temp. Fallstrick: Playwright-Skript NICHT aus `workspace/scratch` starten (dort liegt ein `inspect.py`, das die stdlib überdeckt → AttributeError); aus /tmp starten, ohne `python -I`.
**Folien-PDFs** (`pptx_to_pdf.ps1`, Befehl in [[project_schuljahr2627]]) erzeuge ich IMMER selbst und ohne Rückfrage — gehört zur Vorbereitung. Frei­gabe von Chris brauche ich nur für den eigentlichen Post (Montags-Freigabe, [[project_kurstag_montag_freigabe]]).
