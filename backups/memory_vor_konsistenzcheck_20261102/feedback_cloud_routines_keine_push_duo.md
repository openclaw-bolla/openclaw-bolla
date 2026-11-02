---
name: feedback-cloud-routines-keine-push-duo
description: Cloud-Routinen (Scheduled Tasks) im Claude-Account pushen aufs Duo/Handy — Chris will dort keine Modell-/Update-Erinnerungen
metadata:
  type: feedback
---

Chris bekam auf dem Surface Duo (Claude-App) ständig Erinnerungen wie „MAI-Image 2.5 verfügbar" / „Sonnet 5.5 verfügbar". Ursache: **Cloud-Routinen („Scheduled tasks") im Claude-Account** (claude.ai/code/routines, per RemoteTrigger-Tool listbar), die Chris früher selbst per Chat angefordert hatte; sie laufen in Anthropics Cloud (nicht per Cron auf dem PC) und schicken Push/Mail.

Am 26.10.2026 deaktiviert (enabled=false, nicht gelöscht): `MAI-Image-2 Copilot Pro Check` (trig_018Xg8yBhsMpzQoRjJqTbWiK, Mo 06:00 UTC) und `Sonnet-Upgrade-Check` (trig_01FduNchBR1PE7KM9oXtmh1b, Mo 07:00 UTC; verglich noch gegen Sonnet 4.6). Bewusst aktiv gelassen: einmalige Erinnerung `bollawave Saison-Songs 2027` (2.2.2027, trig_01LEvt17hHS4QDxYyeH1pvs1).

**Why:** Chris will auf dem Duo keine solchen Meldungen. **How to apply:** Nie wiederkehrende Cloud-Routinen mit Push anlegen, ohne dass Chris es ausdrücklich will; bei neuen Handy-Meldungen zuerst RemoteTrigger list prüfen. [[user_devices]]
