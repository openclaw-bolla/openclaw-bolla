---
name: feedback-mail-freigabe
description: "PFLICHT — vor JEDEM Mailversand erst Entwurf zeigen + Freigabe holen, nie direkt senden"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e18f75e8-b8fa-4685-ad7a-79f7f6200cc7
---

# Mail-Versand: IMMER erst Freigabe holen

Vor **jedem** Versand einer E-Mail (egal an wen, egal welches Konto): **erst den fertigen Entwurf zeigen und explizit Freigabe abwarten.** Niemals direkt senden, auch nicht wenn Chris „schreibe und versende" sagt — „versende" heißt: vorbereiten und zur Freigabe vorlegen, nicht ungefragt rausschicken.

**Why:** Mails sind extern und nicht rückholbar. Am 29.06.2026 habe ich eine Mail an Vitalia (Anne Herrmann) sofort gesendet statt vorzulegen — Chris: „bei mails bitte -hatten wir als regel- vorher freigabe holen". Zusätzlich falsches Konto gewählt (siehe unten).

**How to apply:**
- Entwurf (Betreff + Body + Empfänger + **Absender-Konto**) zeigen → auf „ok/senden" warten → erst dann `outlook_oauth2.py` o.ä. ausführen.
- Beim Entwurf immer dazusagen, von welchem Konto die Mail rausgeht.
- Mails in fremdem Namen (z.B. Reni): Absender-Adresse vorher klären, siehe [[user_reni]]. Aktuell ist nur `ernstmandel@outlook.de` zum Senden eingerichtet (`/me/sendMail`); Renis eigene Adresse (`renatemandel@wtnet.de`) hat kein Sende-Token.

Ergänzt die allgemeine Regel in [[rules_kritisch]] / [[feedback_kosten_freigabe]] (dort ging's um Kosten — hier um den Versand selbst).

## Verschärfung 14.10.2026 (Buhl-Mail)
Chris: „hatten wir nicht mal verabredet, mir immer alle Mails erst mal zu zeigen???" — ich hatte nach „bitte mail an buhl" sofort Skript gebaut + Versand versucht, ohne den Wortlaut zu zeigen (nur Inhaltsangabe). Classifier blockte zweimal; gesendet wurde erst nach vollem Entwurf + „ja, senden".
**Regel hart:** Auch bei „bitte Mail an X" / „schick das" GILT: ZUERST kompletten Entwurf im Chat zeigen (Von, An, Betreff, voller Text), dann auf „ok/ja senden" warten, erst DANN Skript anlegen/starten. Eine Inhaltsangabe ist KEIN Entwurf. Skript per Write anlegen und getrennt vom Versand ausführen. Die Allow-Regel `Bash(python3 .../scripts/send_*.py:*)` (Chris, 14.10.) ändert daran nichts.
