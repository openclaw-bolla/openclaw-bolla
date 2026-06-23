#!/bin/bash
# duoclip.sh — Greift den AKTUELLEN Surface-Duo-2-Bildschirm per ADB (WLAN)
# und legt ihn als BILD direkt in die Windows-Zwischenablage.
# Danach: einfach Strg+V wo immer du willst. Kein Screenshot, keine Galerie.
#
# Duo 2 ist Dual-Screen: bei aufgeklapptem Gerät liefert screencap BEIDE
# Bildschirme nebeneinander. Dieses Skript schneidet automatisch auf EINE
# Seite zu (die mit Inhalt) — Override: ./duoclip.sh left | right | auto | both
#
# Voraussetzung: Am Duo "Kabelloses Debugging" aktiviert
#   (Einstellungen -> System -> Entwickleroptionen -> Kabelloses Debugging)

SIDE="${1:-auto}"           # auto (Standard) | left | right | both
DUO_IP="192.168.178.20"
KNOWN_PORT="41873"          # zuletzt bekannter Connect-Port (kann nach Reboot wechseln)
PNG_WSL="/mnt/c/Temp/duoshot.png"
PNG_WIN='C:\Temp\duoshot.png'
PS='/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'

mkdir -p /mnt/c/Temp

# 1) Verbindung herstellen: erst bekannter Port, sonst per mDNS aktuellen Port suchen
TARGET="$DUO_IP:$KNOWN_PORT"
adb connect "$TARGET" >/dev/null 2>&1
if ! adb devices | grep -q "$DUO_IP"; then
  SVC=$(adb mdns services 2>/dev/null | grep '_adb-tls-connect' | grep "$DUO_IP" | head -1 | awk '{print $NF}')
  if [ -n "$SVC" ]; then
    TARGET="$SVC"
    adb connect "$TARGET" >/dev/null 2>&1
  fi
fi

if ! adb devices | grep -q "$DUO_IP"; then
  echo "❌ Duo nicht erreichbar. Am Duo 'Kabelloses Debugging' einschalten."
  exit 1
fi

# Tatsaechlich verbundenen Eintrag nehmen (Port kann abweichen vom versuchten!)
TARGET=$(adb devices | awk -v ip="$DUO_IP" '$2=="device" && $1 ~ ip {print $1; exit}')

# 2) Aktuellen Bildschirm grabben
adb -s "$TARGET" exec-out screencap -p > "$PNG_WSL" 2>/dev/null
if [ ! -s "$PNG_WSL" ]; then
  echo "❌ Kein Bild bekommen (Verbindung verloren?)."
  exit 1
fi

# 2b) Auf eine Seite zuschneiden (Duo-Dual-Screen). 'both' = unverändert lassen.
if [ "$SIDE" != "both" ]; then
  CROPMSG=$(python3 - "$PNG_WSL" "$SIDE" <<'PY'
import sys
from PIL import Image, ImageStat

path, side = sys.argv[1], sys.argv[2]
im = Image.open(path).convert("RGB")
w, h = im.size

# Querformat-Bild = zwei Hochkant-Panels nebeneinander -> teilen.
# Hochkant-Bild = nur ein Panel aktiv -> nichts zu tun.
if w <= h:
    print("single")  # nur ein Bildschirm aktiv, kein Crop noetig
    sys.exit(0)

mid = w // 2
left  = im.crop((0, 0, mid, h))
right = im.crop((mid, 0, w, h))

def score(part):
    g = part.convert("L")
    st = ImageStat.Stat(g)
    return st.mean[0], st.stddev[0]   # Helligkeit, Kontrast/Inhalt

lm, ls = score(left)
rm, rs = score(right)

if side == "left":
    pick = left
elif side == "right":
    pick = right
else:  # auto: ausgeschalteter/schwarzer Schirm hat sehr niedrige Helligkeit;
       # sonst die inhaltsreichere Haelfte (hoehere Stddev) nehmen.
    if lm < 12 and rm >= 12:
        pick = right
    elif rm < 12 and lm >= 12:
        pick = left
    else:
        pick = left if ls >= rs else right

pick.save(path)
print(f"crop {pick.size[0]}x{pick.size[1]}")
PY
)
fi

# 3) Als Bitmap in die Windows-Zwischenablage legen (STA-Modus noetig)
"$PS" -STA -NoProfile -Command \
  "Add-Type -AssemblyName System.Windows.Forms,System.Drawing; \$i=[System.Drawing.Image]::FromFile('$PNG_WIN'); [System.Windows.Forms.Clipboard]::SetImage(\$i); \$i.Dispose()" >/dev/null 2>&1

echo "✅ Duo-Bildschirm (${SIDE}${CROPMSG:+, $CROPMSG}) liegt in der Zwischenablage — jetzt Strg+V"
