---
name: feedback-makler-excel-sofort-updaten
description: Nach jeder Makler-Aktion (Mail gesendet/Antwort/Absage/Angebot/Status) sofort Makler-Excel neu bauen
metadata:
  type: feedback
---

Nach **jeder Makler-Aktion** (Mail gesendet, Antwort eingegangen/bearbeitet, Absage, Angebot bewertet, Status geändert) die Excel **sofort** aktualisieren: erst Backup, dann `python3 scripts/makler_excel_bauen_v2.py` (schreibt Desktop\Makler_Antworten_Archiv_neu.xlsx + data/makler_antworten_archiv.xlsx). Nicht erst auf Nachfrage.

**Why:** Chris 15.10.2026 — Excel ist seine Arbeitsübersicht, muss immer aktuell sein.
**How to apply:** Am Ende jeder Makler-Aktion Excel neu bauen und kurz melden. Versand an Makler mit Chris' Daten läuft über Outlook-Entwurf, den Chris selbst absendet ([[feedback_keine_datei_editor_permissions]], [[project_immokauf]]).
