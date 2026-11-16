---
name: reference-gemini-billing
description: "Gemini/Google-Cloud Abrechnung — kostenpflichtiges Konto, Visa, Billing-ID, Key-Aufteilung (KEIN Free Credit mehr)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: cdbbb188-b89b-408e-9c7b-7f264f50c119
  modified: 2026-09-02T00:00:00.000Z
---

Google Gemini läuft über ein **kostenpflichtiges** Google-Cloud-Billing-Konto („My Billing Account", ID `0167B7-89A285-58C6A6`), Zahlungsmethode **Visa …6448** (gültig 10/28), nachträgliche monatliche Abrechnung. **Jeder Gemini-Call kostet echtes Geld** — kein Gratis-Puffer.

- **⛔ KEIN Free Credit mehr.** Der GCP-Starter-Credit (260,15 €, Typ „Einmal") ist **~19.07.2026 abgelaufen**. Er hat Gemini ohnehin **nie gedeckt** (Nutzungsbereich „Bestimmte Nutzung", nicht „Alle Dienste" — empirisch bewiesen 22.06.2026: Restwert blieb bei vollen 260,15 € trotz Gemini-Verbrauch, alles lief direkt auf die Visa). Am **02.09.2026** hat Chris angewiesen, Free-Credit + Ablaufdatum aus MP zu entfernen → erledigt: `config/kosten.json`-Eintrag „Gemini Free Credit" gelöscht; Doku-Box in `mission-control/index.html` auf „Pay-as-you-go über Visa · kein Free-Credit mehr" geändert.
- **Kostenfolge für Features:** „🎨 3 Cover-Vorschläge" in Bolla Songs = 1× Pollinations (gratis) + 2× Gemini 2.5 Flash Image ≈ **7 ct pro Klick, echtes Geld**. „🌟 +1 mit MAI" ≈ 0,10 €. Bilder „auf Vorrat" bringen nichts.
- **Echte Abbuchungen (historisch):** 30.04. 2,88 € · 31.05. 4,51 € · Juni ~0,7–0,9 €. Monatslimit 10 € gesetzt.
- Guthaben/Kosten sind **NICHT per API abrufbar**: Gemini-Keys sprechen nur `generativelanguage` (kein Billing-Scope); Google-OAuth-Tokens haben nur `contacts`/`gmail`/`drive`. Stand nur manuell aus Cloud Console → Abrechnung.
- Anzeige in MP: System-Überblick → „Bolla Konten & Kosten" (`config/kosten.json`) — jetzt nur noch **ein** Eintrag: 🍌 Gemini API Verbrauch.
- **Key-Aufteilung (Stand 22.06.):** `gemini_api.json` = …JOaI (Projekt „Default Gemini Project", **bezahlt**, Preisstufe 1) → genutzt von `mission_control_api.py` + `generate_suno_covers.py`. `gemini_api_free.json` = …6TDI (Projekt „OpenClaw", **kostenlose Stufe**) → genutzt von `ea_organizer.py`. ⚠️ Free-Tier nutzt Eingaben ggf. zum Training — vor Umstellung prüfen, ob private Daten durchlaufen.
