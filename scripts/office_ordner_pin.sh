#!/bin/bash
# Pinnt den Office-Unterrichtsordner regelmäßig neu ("Immer auf diesem Gerät behalten"),
# damit Windows Storage Sense neue/länger ungenutzte Dateien nicht wieder auf
# online-only zurücksetzt (Chris-Wunsch 22.07.2026, WLAN-Ausfall in der Schule).
# Seit 12.08.2026 auch aufs Book (Schulgerät, WLAN dort besonders unzuverlässig) ausgeweitet -
# Chris braucht dort zwingend Offline-Zugriff. Book-Pfad ist C:\...\OneDrive\... (kein D:-Laufwerk
# wie beim Studio). Book-Teil wird uebersprungen, wenn der Reverse-Tunnel (Port 2222) gerade down ist.

/mnt/c/Windows/System32/attrib.exe +P -U "D:\OneDrive\Dokumente\Office\*" /S /D
echo "$(date '+%Y-%m-%d %H:%M') Studio gepinnt"

if ss -tln 2>/dev/null | grep -q ':2222 '; then
    ssh -p 2222 -i /home/bolla/.ssh/id_ed25519 -o ConnectTimeout=8 -o StrictHostKeyChecking=no \
        ernst@localhost "powershell -Command \"attrib.exe +P -U 'C:\\Users\\ernst\\OneDrive\\Dokumente\\Office\\*' /S /D\"" \
        > /dev/null 2>&1
    echo "$(date '+%Y-%m-%d %H:%M') Book gepinnt"
else
    echo "$(date '+%Y-%m-%d %H:%M') Book übersprungen (Tunnel down)"
fi
