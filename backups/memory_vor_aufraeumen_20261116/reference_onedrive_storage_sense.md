---
name: reference-onedrive-storage-sense
description: Windows Storage Sense setzt lokal erstellte OneDrive-Dateien nach Inaktivität automatisch auf online-only zurück — Fix per attrib +P
metadata:
  node_type: memory
  type: reference
  originSessionId: current
  modified: 2026-08-12T17:15:21.595Z
---

Chris bemerkte 22.07.2026 den `d.docs.live...`-Pfadhinweis beim Öffnen einer PPTX aus dem OneDrive-Office-Ordner —
irritierend, weil er eine lokale Kopie auf D: hat. Grund: **Windows Storage Sense** (nicht OneDrive selbst)
setzt lokal verfügbare OneDrive-Dateien nach einer Weile ohne Nutzung automatisch auf "online-only" zurück,
auch wenn sie ursprünglich lokal erstellt wurden. Nur explizit gepinnte Dateien ("Immer auf diesem Gerät
behalten") sind davon ausgenommen. Bestätigt per Registry: `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\
StorageSense\Parameters\StoragePolicy` — Werte `01=1` (Storage Sense aktiv) und `04=1` (Auto-Optimierung
OneDrive-Inhalte aktiv).

**Diagnose:** `attrib.exe "Pfad\Datei"` zeigt `P` (gepinnt) oder fehlendes P (online-only-gefährdet).

**Fix (einmalig, für einen ganzen Ordner):**
```
attrib.exe +P -U "D:\Pfad\Ordner\*" /S /D
```
Warnung "Versteckte Datei wird nicht zurückgesetzt" bei `~$...`-Dateien (Office-Sperrdateien) ist harmlos,
kein echter Inhalt.

**Dauerhafter Fix (für künftige neue Dateien im Ordner):** Es gibt keinen Windows-Ordner-Schalter "alle
künftigen Dateien automatisch pinnen" — Storage Sense kann auch neu erstellte Dateien nach Inaktivität
wieder dehydrieren. Lösung: Cron-Job, der den Ordner erneut pinnt. Für den Lehrer-Office-Ordner
eingerichtet: `scripts/office_ordner_pin.sh`, Log `logs/office_ordner_pin.log`.

**⚠️ 12.08.2026 — Lücke gefunden und geschlossen:** Cron lief nur 1×/Tag (`23 6 * * *`), eine Datei, die
Chris am selben Tag NACH 06:23 bearbeitet hatte (`02-The Basics - Grundbegriffe - II.pptx`), war beim
Öffnen noch online-only (orangener Ladebalken beim Doppelklick) — der nächste Pin-Lauf wäre erst am
Folgetag gekommen. Einmalig sofort nachgepinnt + Cron auf `23 6,12,18 * * *` erweitert (3× täglich), damit
tagesaktuell bearbeitete Dateien nicht mehr bis zum nächsten Morgen ungepinnt bleiben.

**⚠️⚠️ 12.08.2026 (später, wichtiger) — Aufs Book ausgeweitet, das ist der eigentlich kritische Fall:**
Chris braucht Offline-Zugriff vor allem auf dem **Book** (Schulgerät, WLAN dort unzuverlässig) — noch
wichtiger als am Studio. `scripts/office_ordner_pin.sh` pinnt jetzt bei jedem Lauf BEIDE Geräte:
- **Studio:** `D:\OneDrive\Dokumente\Office\*` (wie bisher)
- **Book:** `C:\Users\ernst\OneDrive\Dokumente\Office\*` — ⚠️ **anderer Pfad als Studio!** Book hat kein
  eigenes D:-Laufwerk, OneDrive liegt unter `C:\Users\ernst\OneDrive\...`. Wird per SSH (Port 2222,
  Reverse-Tunnel) angestoßen, übersprungen falls Tunnel gerade down (kein Hänger/Fehler im Cron-Lauf).

**Zusätzliche Absicherung, weil der Book-Tunnel nachweislich öfter down ist:** eigener lokaler Scheduled
Task **`BollaOfficePin`** direkt auf dem Book angelegt (`schtasks /create ... /sc onlogon`), pinnt bei
JEDER Anmeldung automatisch, unabhängig vom Tunnel zum Studio. Ergänzt (nicht ersetzt) den bestehenden
`BollaTunnel`-Task. Getestet: `Letztes Ergebnis: 0` (Erfolg).

**Wichtig zu verstehen (Chris' Frage "was wenn das Book aus ist"):** Pinnen ist ein dauerhaftes
Dateisystem-Flag, kein "am Leben halten" — bereits gepinnte Dateien bleiben gepinnt, auch offline/aus.
Risiko besteht nur für Dateien, die ganz frisch geändert wurden, BEVOR das Book sie das erste Mal
synced+gepinnt hat. Der `onlogon`-Trigger deckt das ab: sobald Chris sich am Book anmeldet (z.B. in der
Schule), pinnt der Task sofort alles nach, was OneDrive bis dahin synchronisiert hat.

**Nebenbei entdeckter+gefixter Bug (12.08.2026):** `book_tunnel_watchdog.sh` (Cron alle 2 Min, killt
hängende Tunnel neu) rief die falsche MC-API-Adresse auf (`/api/book/action` statt korrekt
`/api/surfaces/book/action`) — der Auto-Reparatur-Versuch lief seit Tagen(?) ins Leere mit „not found",
ohne dass es auffiel. Gefixt.

**How to apply:** Bei ähnlichen Beschwerden ("Datei zeigt online-only-Symbol", "d.docs.live-Pfad", Sorge
vor Zugriffsverlust ohne WLAN) — erst mit `attrib.exe` den P-Status prüfen, dann bei Bedarf denselben
Cron-Wächter-Ansatz für den betroffenen Ordner anbieten (z.B. andere wichtige Unterrichts-/Bolla-Ordner).
Bei Geräten mit Reverse-Tunnel (Book, Pro) IMMER zusätzlich einen lokalen `onlogon`-Task in Betracht
ziehen, nicht nur auf den Studio-gesteuerten Cron verlassen — der Tunnel ist nicht zuverlässig genug als
einzige Absicherung.
