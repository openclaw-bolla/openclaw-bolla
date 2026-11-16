---
name: project-immo-kontaktformulare
description: Immo-Makler ohne Mail, aber mit Kontaktformular — Bolla soll sie später ausfüllen; Chris dran erinnern
metadata:
  type: project
---

Chris (14.10.2026): Makler-Einträge ohne E-Mail, die ein **Kontaktformular** haben, bleiben in der Liste (`makler_status.json`, Feld `kontaktformular`). Nur-Telefon-Einträge wurden entfernt.

**Why:** Mail-Welle geht nur an echte Adressen; Formulare sind der zweite Kanal für dieselbe Voranfrage.
**⏸️ ZURÜCKGESTELLT (Chris, 14.10.2026): „für länger zurückstellen“ — NICHT von selbst erinnern/anstoßen; erst wenn Chris das Thema wieder aufmacht (oder nach den Mail-Antworten Bedarf entsteht).**
**How to apply (wenn wieder aktuell):** Formulare ausfüllen (Playwright, gleicher Text wie die Mail, Freigabe vorher gemäß [[feedback_mail_freigabe]] / Website-Schreibzugriff [[feedback_website_schreibzugriff]]). Nach Versand Status auf `email_gesendet` setzen. Zusammenhang: [[project_immokauf]].
