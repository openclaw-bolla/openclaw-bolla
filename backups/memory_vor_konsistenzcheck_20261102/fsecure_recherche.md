# F-Secure / WISO Internet Security: Web Speech API Blockierung

**Recherche-Datum:** 2026-05-12
**Status:** Recherche abgeschlossen, Mail-Versand nicht möglich (kein E-Mail-Tool in dieser Session)

---

## Zusammenfassung des Problems

Die Web Speech API in Microsoft Edge verbindet sich per WebSocket (wss://) zu `speech.platform.bing.com` für Spracheingabe. Nach einem F-Secure/WISO-Update (Mai 2026) werden diese Verbindungen auf **Netzwerktreiber-Ebene** blockiert — nicht nur durch die Browser-Extension.

**Symptome:**
- `continuous: true` (persistente WSS-Verbindung) → sofort blockiert
- `continuous: false` (kurze Verbindung) → geht einmal durch, dann blockiert
- Eintrag in "Sicherer Browser → Website-Ausnahmen → Zugelassen" hilft nur beim ersten Verbindungsaufbau
- Browser-Extension deaktivieren hilft NICHT

---

## Wichtige Erkenntnis: Möglicherweise KEIN reines F-Secure-Problem

**Kritischer Fund:** Die Web Speech API in Edge hat seit Ende 2024 bekannte Bugs, die unabhängig von Antivirensoftware auftreten:

- **Edge v134 (Feb 2025):** Web Speech API brach komplett zusammen → Microsoft fix in v134.0.3124.68 (März 2025)
- **Edge v147 (April 2026):** Problem kehrt zurück, betrifft Nutzer weltweit (Spanien, Italien, Türkei, Mexiko, Polen, USA)
- **Edge v148 (Mai 2026):** Problem weiterhin ungeklärt, kein offizielles Statement von Microsoft

Threads:
- https://techcommunity.microsoft.com/discussions/edgeinsiderdiscussions/web-speech-api-stopped-working-on-edge-starting-with-v-134/4391156
- https://techcommunity.microsoft.com/discussions/edgeinsiderdiscussions/web-speech-api-not-working-in-edge-v-147/4514880

**Das bedeutet:** Chris' Problem könnte eine Kombination aus Edge v147/148-Bug + F-Secure-Verstärkung sein. Selbst ohne F-Secure wäre die API in Edge 147+ möglicherweise kaputt.

---

## F-Secure / WISO Architektur: Was blockiert was?

### 1. Netzwerktreiber (fsnifdrv / fsnethoster)
F-Secure arbeitet auf Kernel-Ebene mit dem Treiber `fsnifdrv` (F-Secure Network Interception Driver). Dieser:
- Scannt und filtert Netzwerkverkehr BEVOR er den Browser erreicht
- Ist unabhängig von der Browser-Extension
- Kann WebSocket-Verbindungen (wss://) abwürgen

Temporärer Test (NUR zum Testen, erhöht Sicherheitsrisiko!):
```
net stop fsnifdrv
net stop fsnethoster
```
Wiederherstellung: PC neu starten oder `net start fsnifdrv`

### 2. Advanced Network Protection (ANP)
- Heißt in der UI: "Do not allow applications to download harmful files"
- Arbeitet **unabhängig von der Firewall** — Firewall deaktivieren hilft nicht
- **Keine Whitelist-Funktion für Domains** (historisch: "Sadly, no exceptions can be made with it enabled")
- Kann nur komplett ein/aus geschaltet werden
- Für Home-User keine granulare Steuerung dokumentiert

### 3. Web Traffic Scanning (wurde entfernt)
- In F-Secure v19.4 entfernt, weil es nur HTTP (nicht HTTPS) scannen konnte
- Irrelevant für aktuelle Versionen

### 4. Banking Protection
- Blockiert beim Start einer Banktransaktion ALLE anderen Netzwerkverbindungen
- Whitelist in "Sicherer Browser → Website-Ausnahmen → Zugelassen" steuert dies
- Problem: wirkt nur auf der Browser-Extension-Ebene, nicht auf Netzwerktreiber-Ebene

---

## Online gefundene Meldungen zum Problem

Zu "F-Secure + Web Speech API / speech.platform.bing.com + WebSocket blockiert" gibt es **keine spezifischen Forenbeiträge** in der F-Secure Community, Reddit oder StackOverflow. Das Problem ist spezifisch für Chris oder sehr neu (Mai 2026).

Das deutet darauf hin, dass es ein frisches Problem nach einem Mai-2026-Update ist, für das noch keine öffentliche Lösung dokumentiert ist.

---

## Mögliche Lösungsansätze (nach Erfolgswahrscheinlichkeit sortiert)

### Option 1: Edge-Version prüfen / downgraden (EMPFOHLEN als erster Test)
Da Edge v147/148 auch ohne F-Secure die Web Speech API bricht:
1. Edge-Version prüfen: `edge://settings/help`
2. Testen: Speech API in Chrome (ohne F-Secure Extension) — funktioniert das?
3. Wenn Chrome funktioniert → Edge-Bug + F-Secure-Kombination
4. Wenn Chrome auch nicht funktioniert → F-Secure-Problem

### Option 2: Bestimmte F-Secure-Schutzfunktionen temporär deaktivieren (Test)
Nacheinander testen:
- "Privacy Protection" / Tracker-Schutz deaktivieren
- "Family Rules" / Content Filtering deaktivieren  
- "Advanced Network Protection" deaktivieren (falls sichtbar in Einstellungen)
- Ad-Blocker deaktivieren

### Option 3: Windows Firewall-Ausnahme (zusätzlich zur WISO-Whitelist)
1. Windows-Sicherheit öffnen → Firewall & Netzwerkschutz → App durch Firewall zulassen
2. Microsoft Edge explizit für alle Netzwerke freigeben
3. Testen ob Edge-Prozess (msedge.exe) in Ausnahmeliste ist

### Option 4: F-Secure "Sicherer Browser" für speech.platform.bing.com
Die aktuelle Vorgehensweise (Zugelassen-Liste) sollte richtig sein, aber:
- Domain OHNE "www." eintragen: `speech.platform.bing.com`
- Auch eintragen: `*.bing.com` (Wildcard falls unterstützt)
- Auch eintragen: `cognitive.microsoft.com` und `*.cognitiveservices.azure.com`

### Option 5: Netzwerktreiber-Test (nur für Diagnose)
Um zu testen ob fsnifdrv der Schuldige ist:
```cmd
net stop fsnethoster
net stop fsnifdrv
```
Dann Speech API testen. Danach PC neu starten!
WARNUNG: Nur kurz zum Testen, danach sofort neu starten.

### Option 6: F-Secure/WISO Support kontaktieren
Da keine fertige Lösung online dokumentiert ist, sollte der Support kontaktiert werden.

---

## WISO/Buhl Support-Kontakt

**Kein direkter E-Mail-Support** — nur Ticketsystem und Telefon:
- **Online-Ticket:** https://www.buhl.de/shop/anfrage-stellen
- **Telefon:** 02735 90 96 99 (Mo-Fr 9-21 Uhr, Sa 9-13 Uhr)
- **Fax:** 02735 9096 500
- **Post:** Buhl Data Service GmbH, Support Center, Carl-Benz-Str. 2, 57299 Burbach

### Vorgefertigte Support-Mail (für Online-Ticket)

**Betreff:** Web Speech API (speech.platform.bing.com) wird durch WISO Internet Security blockiert

**Text:**
```
Guten Tag,

ich nutze WISO Internet Security und habe seit einem kürzlichen Update ein Problem: Die Web Speech API in Microsoft Edge (Spracheingabe) wird durch WISO blockiert. Die Verbindung zu speech.platform.bing.com (WebSocket, wss://) wird nach dem ersten Versuch mit einem Netzwerkfehler abgelehnt, obwohl die Domain unter "Sicherer Browser → Website-Ausnahmen → Zugelassen" eingetragen ist.

Das Deaktivieren der Browser-Extension hilft nicht — das Problem liegt auf Netzwerkebene (vermutlich der WISO-Netzwerktreiber fsnifdrv oder die Advanced Network Protection Funktion).

Konkret: "continuous: true" (persistente WebSocket-Verbindung) wird sofort blockiert; "continuous: false" (kurze Verbindung) kommt einmal durch und wird dann ebenfalls blockiert.

Frage: Gibt es eine spezifische Einstellung in WISO Internet Security, um WebSocket-Verbindungen zu speech.platform.bing.com dauerhaft freizugeben? Z.B. eine Firewall-Ausnahme auf Netzwerktreiber-Ebene, HTTPS-Scanning-Ausnahme oder ähnliches?

Alternativ: Welche Schutzfunktion in WISO ist für das Blockieren von persistenten WebSocket-Verbindungen (wss://) zu externen Microsoft-Servern zuständig?

Vielen Dank für Ihre Hilfe.

Mit freundlichen Grüßen,
Chris Mandel
```

---

## Status-Tracking

- [ ] Edge-Version prüfen + Chrome-Test durchgeführt
- [ ] Option 2 (einzelne Schutzfunktionen) getestet
- [ ] Option 4 (erweiterte Whitelist) konfiguriert
- [ ] Support-Ticket bei WISO eingereicht
- [ ] Antwort von WISO erhalten
- [ ] Lösung gefunden und dokumentiert

---

## Quellen

- F-Secure Community - Advanced Network Protection: https://community.f-secure.com/en/discussion/112314/advanced-network-protection
- F-Secure Community - UDP-Blockierung durch Update 25.2: https://community.f-secure.com/en/discussion/129259/current-update-of-f-secure-causes-problems-with-udp-communication
- F-Secure Community - Banking Protection & trusted apps: https://community.f-secure.com/en/discussion/126624/allowing-new-connections-for-trusted-apps-while-in-banking-protection-mode
- Edge Web Speech API bug (v134): https://techcommunity.microsoft.com/discussions/edgeinsiderdiscussions/web-speech-api-stopped-working-on-edge-starting-with-v-134/4391156
- Edge Web Speech API bug (v147): https://techcommunity.microsoft.com/discussions/edgeinsiderdiscussions/web-speech-api-not-working-in-edge-v-147/4514880
- WISO Support-Kontakt: https://www.buhl.de/shop/kontaktcenter
- Microsoft Edge SpeechRecognitionEnabled Policy: https://learn.microsoft.com/en-us/deployedge/microsoft-edge-browser-policies/speechrecognitionenabled
