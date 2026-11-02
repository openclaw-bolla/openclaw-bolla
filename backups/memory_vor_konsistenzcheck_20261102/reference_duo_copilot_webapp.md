---
name: reference-duo-copilot-webapp
description: "Surface Duo 2 (Android 12): neue Copilot-App per Play Store nicht installierbar, Copilot läuft als Edge-Web-App; adb-Zugriff geht"
metadata:
  node_type: memory
  type: reference
  originSessionId: e1fe2e4a-f10e-4f75-93d8-d607ef366205
  modified: 2026-10-04T10:08:41.381Z
---

Surface Duo 2 läuft auf Android 12 (API 32, Patch 10/2024, bleibt dort). Microsoft hat die alte App in „Copilot (legacy)" (`com.microsoft.copilot`) umbenannt und eine neue Copilot-App veröffentlicht. Auf Z Flip/P8 lässt sich die neue installieren, auf dem Duo meldet der Play Store „funktioniert nicht auf deinem Gerät" (Ursache vermutet: höhere Mindest-Android-Version, nicht verifiziert).

**Lösung 04.10.2026:** Legacy-App deinstalliert, `copilot.microsoft.com` in Edge als Web-App auf den Startbildschirm gelegt.

**Why:** Chris fragte, warum Copilot auf dem Duo verschwand; Launcher zeigte nur „Copilot (legacy)".
**How to apply:** Bei ähnlichen App-Ausfällen auf dem Duo zuerst Android-Version als Grund prüfen und Web-App/PWA vorschlagen. `adb connect 192.168.178.20:5555` funktioniert (Bash(adb:*) ist in den Berechtigungen freigegeben). Siehe [[user_devices]].
