#!/bin/bash
# Pinnt den Office-Unterrichtsordner täglich neu ("Immer auf diesem Gerät behalten"),
# damit Windows Storage Sense neue/länger ungenutzte Dateien nicht wieder auf
# online-only zurücksetzt (Chris-Wunsch 22.07.2026, WLAN-Ausfall in der Schule).
/mnt/c/Windows/System32/attrib.exe +P -U "D:\OneDrive\Dokumente\Office\*" /S /D
echo "$(date '+%Y-%m-%d %H:%M') gepinnt"
