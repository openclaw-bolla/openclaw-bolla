---
name: feedback-praktika-handy-ios-android
description: "Bei Praktika, die auf dem eigenen Handy der Schüler laufen, IMMER Android- und iOS-Pfade getrennt beschreiben — Menünamen/Icons unterscheiden sich je Hersteller/Version"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-28T07:36:22.516Z
---

Chris' Auftrag für Kurstag 6 (Video aufnehmen/schneiden auf dem eigenen Handy, `06-Praktikum.html` in
Handouts/Entwurf): explizit berücksichtigen, dass die Schüler **verschiedene Handys mit verschiedenen
iOS-/Android-Versionen** haben — als **grundsätzliche** Regel für alle künftigen Handy-Praktika, nicht
nur dieses eine Mal.

**Why:** Anders als bei den Schul-PCs/-Laptops (dort ein bekannter, einheitlicher Software-Stand, siehe
[[feedback_praktikum_geraete_check]]) ist bei privaten Schüler-Handys die Geräte-/Versions-Landschaft
komplett uneinheitlich — Menüpfade, Symbolnamen und sogar ob eine Funktion in den Schnelleinstellungen
schon sichtbar ist, unterscheiden sich zwischen Herstellern und OS-Versionen.

**How to apply, bei jedem künftigen Handy-basierten Praktikum:**
- Schritte, die vom Betriebssystem abhängen (Bildschirmaufnahme, Datei-Verwaltung, Video schneiden,
  Screenshot o.ä.), **immer in zwei parallelen Kästen** darstellen: 🤖 Android und 🍎 iOS — nicht nur
  einen Weg beschreiben und "so ähnlich bei den anderen" hoffen.
  Umgesetzt in `06-Praktikum.html` als `.os-box.android` / `.os-box.ios` Zwei-Spalten-Layout (Vorlage
  bei Bedarf wiederverwenden).
- Zusätzlich einen Hinweis, dass exakte Menü-/Symbolnamen je nach Hersteller/Version abweichen können,
  aber das **Symbol** (z.B. Kreis fürs Aufnehmen) meist wiedererkennbar ist — plus einen Fallback-Tipp
  ("frag ein Handy mit gleichem Betriebssystem in der Nähe").
- Wo möglich, eine geräteunabhängige Ausweich-Option nennen (z.B. "Video stattdessen einfach mit der
  Kamera-App aufnehmen"), falls der OS-spezifische Weg bei einem Gerät nicht auffindbar ist.

Passt inhaltlich neben [[feedback_praktikum_geraete_check]] (das war Schul-PC-spezifisch, jetzt bewusst
um den Handy-Fall ergänzt) und [[feedback_prakt_anleitungen]] (Grundregeln fürs Anleitungs-Format
bleiben gleich, hier nur um die OS-Zweiteilung ergänzt).
