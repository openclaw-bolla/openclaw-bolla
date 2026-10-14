---
name: Mission Control Sidebar — Terminologie
description: Gemeinsame Begriffe für MC-Sidebar-Elemente
type: feedback
originSessionId: 9e265b90-8a7b-4aa0-beb8-e3662b86254a
---
Sektionen = aufklappbare Hauptbereiche (ARBEIT, KI, FAMILIE, INFO, ÜBERSICHT)
Gruppen alias "Navgruppe" (Chris' bevorzugter Begriff, 10.08.2026) = aufklappbare Untergruppen innerhalb einer Sektion (z.B. Lehrer-Gruppe, Reiseplaner-Gruppe) — technisch `nav-group-<name>` mit `nav-group-header-<name>` + `nav-group-items-<name>`, Auf/Zu-Pfeil per `toggleNavGroup(name)`, Zähler daneben wird seit 10.08.2026 live per `updateNavGroupCounts()` berechnet (kein Hardcode mehr)
Einträge = einzelne klickbare Punkte (Kalender, E-Mail, etc.)
Subitems = Einträge innerhalb einer Gruppe (eingerückt)

**Konvention ab 25.06.2026:** Chris schreibt SEKTIONS-Namen ab jetzt immer in GROSSBUCHSTABEN (z.B. „ARBEIT", „FAMILIE"), damit klar ist, dass er die Sektion meint (nicht eine gleichnamige Gruppe/Eintrag).

**⚠️ Sidebar-Reihenfolge lebt im SERVER-STATE** (`GET/POST /api/sidebar-state`, Keys `itemOrder`/`blockOrder` mit IDs `nav-di-<page>` / `nav-group-<x>`), NICHT im HTML — der State überschreibt beim Laden die HTML-Position. Beim Verschieben/Hinzufügen von Einträgen IMMER HTML **und** Server-State konsistent ändern, sonst zieht der State es zurück (das war die Ursache des stundenlangen „Verschlimmbesserns" früher). Einrückung dagegen ist reines CSS (`.nav-group-header` padding-left). Notfall-Reset: `?reset-sidebar=1` oder roter Reparatur-Banner.

**Why:** Einheitliche Sprache damit Chris und Bolla beim Beschreiben von MC-Änderungen klar kommunizieren.

**How to apply:** Diese Begriffe bei allen MC-Sidebar-Änderungen verwenden.
