---
name: feedback-html-pdf-weasyprint
description: "Für HTML-Handouts (nicht PPTX!) ist WeasyPrint die bevorzugte PDF-Export-Methode, von Chris bestätigt"
metadata:
  node_type: memory
  type: feedback
  originSessionId: unknown
  modified: 2026-08-18T12:01:22.169Z
---

Für HTML-basierte Handout-PDFs (z. B. Elternbriefe, Praktikums-Infoblätter) WeasyPrint verwenden
(`pip3 install --user --break-system-packages weasyprint`, dann `HTML(pfad).write_pdf(ausgabe)` in
Python). Ergebnis am 18.08.2026 von Chris ausdrücklich als besser als erwartet bestätigt ("deine PDF
gefällt mir besser") — sogar im Vergleich zur eigentlich favorisierten Windows-eigenen Route (Edge
"Als PDF speichern" / Microsoft Print to PDF), die ich als Alternative vorgeschlagen hatte.

**Why:** Playwright/Chromium-PDF-Export funktioniert auf diesem WSL-System NICHT (fehlende
`libnspr4`/`libnss3` u. a., kein passwordless sudo verfügbar, siehe Session vom 18.08.2026) —
WeasyPrint war der funktionierende Ersatz und hat sich dabei als qualitativ überzeugend erwiesen.

**Wichtig — Abgrenzung zu [[project_schuljahr2627]]:** Die dortige Regel "PowerPoint-COM statt
LibreOffice, MS Print to PDF ist Referenzqualität" gilt weiterhin für **PPTX→PDF**-Exports (LibreOffice
headless erzeugte dort nachweislich schlechte Qualität). Diese Regel hier betrifft nur den anderen
Fall: **HTML→PDF**. Beide Regeln koexistieren, nicht verwechseln.

**How to apply:** Bei künftigen HTML-Handouts, die als PDF gebraucht werden (Elternbriefe, Infoblätter,
Ein-Seiten-Kompression), WeasyPrint direkt als ersten Weg nehmen, nicht erst Playwright probieren oder
Chris zur Edge-Druckfunktion schicken.
