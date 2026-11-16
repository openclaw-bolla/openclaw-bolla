---
name: reference-paypal-2fa
description: "PayPal 2FA (zweistufige Verifizierung) nur im Browser einrichtbar, nicht in der App"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 8be668ab-e2de-4efb-a815-c398a8f34c7b
---

PayPals **zweistufige Verifizierung (2FA)** lässt sich **NUR im Browser** einrichten — paypal.com → ⚙ Einstellungen → Sicherheit → „Zweistufige Verifizierung" → Einrichten → Authentifizierungs-App (QR scannen) oder SMS.

**In der PayPal-App geht das NICHT** — die „Sicherheit"-Seite der App zeigt nur Fingerabdruck/PIN/Passwort, der 2FA-Schalter fehlt dort absichtlich. Am Handy nur über den Browser (Chrome → ⋮ → „Desktopwebsite" anhaken), am stressfreisten direkt am PC.

**Fingerabdruck** dagegen schaltet man in der App ein (Mehr → Sicherheit → biometrische Anmeldung).

Verifiziert per WebSearch (PayPal-Hilfe + heise) am 26.06.2026, ausgelöst durch Renis PayPal-Konsolidierung (wtnet.de-Konto schließen, outlook.de behalten). Anleitung als Word liegt unter `/mnt/d/OneDrive/Desktop/Konten-absichern_Reni.docx`.

Microsoft/Outlook 2FA dagegen geht sowohl im Browser (account.microsoft.com → Sicherheit) als auch via Authenticator-App.
