---
name: reference-outlook-sync-haenger-fix
description: "Outlook synct nicht (Kategorien fehlen, neue Termine erscheinen nirgends sonst) — Fix per Offline-Toggle"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 00b8b6b4-a6e1-42f9-a13b-5827ea89f6de
  modified: 2026-09-22T13:01:59.645Z
---

Symptom: Outlook (klassisch UND neu, auf demselben Gerät) zeigt veraltete Daten — z.B. Kategorienamen fehlen (nur "Blue Category" etc. statt echtem Namen), oder neu angelegte Kalendertermine erscheinen nirgendwo sonst (nicht im Web, nicht auf anderen Geräten). "Offline arbeiten" ist dabei NICHT aktiv — die Sync-Verbindung hängt aber trotzdem fest, ohne sichtbare Fehlermeldung.

**Fix:** Im klassischen Outlook (Senden/Empfangen-Tab) "Offline arbeiten" einmal AN- und wieder AUSschalten. Erzwingt einen Verbindungsneuaufbau, danach normalisiert sich alles (Kategorien korrekt, Termine sofort sichtbar) — auch im parallel laufenden neuen Outlook auf demselben Gerät.

**How to apply:** Bei Chris tauchte das 22.09.2026 auf dem Studio auf (Surface Laptop) — Book und Web waren die ganze Zeit korrekt, nur Studio hing fest. Vor größeren Diagnose-Umwegen (Konto reparieren, .ost löschen, Kategorien manuell umbenennen) zuerst diesen Toggle probieren — deutlich schneller.
