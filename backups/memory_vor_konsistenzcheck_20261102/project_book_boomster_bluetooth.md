---
name: project_book_boomster_bluetooth
description: Book verliert in der Schule BT-Verbindung zum Teufel Boomster (Miracast/Marvell-Chip) — Befunde + Fix-Stand
metadata:
  type: project
---

Problem (Chris, 08.10.2026, öfter in der Schule): Am Surface Book bricht die Bluetooth-Verbindung zum Teufel BOOMSTER GO ab, wenn parallel Miracast (MS Wireless Display Adapter) zum Beamer läuft. Nur Neustart half.

**Befunde 09.10.2026 (nur lesend):** WLAN + BT teilen sich den Marvell-AVASTAR-Chip (BT = USB\VID_1286&PID_204C, WLAN = mrvlpcie8897). Ereignisprotokoll 08.10. 09:15/09:16 (= Unterricht): BTHUSB 5 + 3 „Adapter hat nicht geantwortet" (Funkchip hing). 07.10. 10:15: mrvlpcie8897 5002 „Fehlfunktion Netzwerkadapter". BTHUSB 18 (Verbindungsschlüssel nicht speicherbar) bei jedem Start — harmlos/bekannt. Dienste bthserv/BthAvctpSvc stehen auf Manual (laufen aber).

**Fix 09.10.:** „Computer darf Gerät ausschalten" für BT-Radio aus (MSPower_DeviceEnable=False; vorher True, Notiz in workspace/backups/book_bt_power_vorher_20261009.txt). WLAN-Adapter (PCI VEN_11AB&DEV_2B38) ebenfalls aus. **bt_reset.ps1** liegt am Book in C:\ProgramData\Bolla\, Desktop-Verknüpfung „Bluetooth-Reset“ (OneDrive-Desktop, läuft als Admin): Dienste stoppen, Radio aus/an, Dienste starten.

**Offen / Ideen:** Reset-Verknüpfung beim ersten Hänger testen; Wirksamkeit im nächsten Unterricht beobachten.

**Why:** Chris hatte es am 08.10. in der MP-UI besprochen, aber dort scheiterte alles an Bash-Freigaben (MP-Session) — nichts wurde im Memory festgehalten.
**How to apply:** Book-Zugriff: `bash /home/bolla/workspace/scripts/book_ps.sh '<PowerShell>'` (EncodedCommand, Tunnel :2222, Fallback 192.168.178.38). Siehe [[project_book_akku]], [[feedback_mp_chat_freigabe_dialog_bug]].

**Randbedingung (Chris 09.10.2026):** Beamer-Kabel (HDMI) ist KEINE Option — der Beamer hängt in den Klassenräumen an der Decke, Miracast ist der einzige Weg. Nicht mehr vorschlagen; Lösungen nur über Funk-/Treiber-/Reset-Seite des Book (z.B. externer USB-Bluetooth-Dongle, 5-GHz-Miracast, Boomster per Kabel/AUX).

**Entscheidung Chris 09.10.2026:** USB-Dongle (Empfehlung war ASUS USB-BT500) ist ihm zu kompliziert → NICHT weiterverfolgen. Er testet erst Energiesparen-aus + Bluetooth-Reset-Verknüpfung. Falls es in der Schule wieder hängt: Ergebnis abwarten, dann neu entscheiden (nicht von selbst den Dongle wieder anbringen).

**Beamer-Verbindung:** MS Wireless Display Adapter meldet sich als „Computerraum 1" (Miracast, Windows+K). Der BT-Reset berührt das WLAN nicht → Beamer-Verbindung bleibt, kein Neu-Koppeln nötig.

**Weitere BT-Geräte am Book (09.10.2026):** Microsoft Wedge Touch Mouse (BLE, fällt auch manchmal weg), „Bluetooth Ergonomic Mouse", „BT Keyboard" — alle am selben Marvell-Funkchip wie der Boomster. Eventlog 08.10.: HidBth-Fehler 2 um 08:05, 09:12 (kurz vor dem BT-Adapter-Hänger 09:15) und 12:48 → Maus-Aussetzer und Boomster-Abbrüche haben vermutlich dieselbe Ursache (Funkchip überlastet/hängt). Energiesparen-aus + BT-Reset sollen beides abdecken.

**Reset-Test 09.10.2026 ~11 Uhr (per SSH, ohne UAC):** bt_reset.ps1 lief in 22 s sauber durch, Dienste Running, Radio OK, Tastatur + beide Mäuse wieder vorhanden. Noch NICHT getestet: Doppelklick auf die Desktop-Verknüpfung (UAC-Abfrage am Book) und echter Praxistest in der Schule (ab 26.10.).
