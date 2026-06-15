#!/usr/bin/env python3
"""
AURORA Cover — Textoverlay
Alle Anpassungen in den === PARAMETER === Block, dann neu ausführen.
"""
from PIL import Image, ImageDraw, ImageFont

# === PARAMETER ===
INPUT   = "/mnt/d/OneDrive/Dokumente/AURORA/cover_v6.png"
OUTPUT  = "/mnt/d/OneDrive/Dokumente/AURORA/cover_v6_text.png"
FONT    = "/tmp/aurora_fonts/Orbitron-Bold.ttf"

TITLE        = "AURORA"
AUTHOR       = "Chris Mandel"

TITLE_SIZE   = 140    # Schriftgröße Titel (px)
AUTHOR_SIZE  = 52     # Schriftgröße Autor (px)

# Echtes Gold: dunkler, wärmer, mehr Bernstein
TITLE_GOLD   = (210, 155, 30)     # sattes Gold
AUTHOR_GOLD  = (185, 135, 25)     # etwas gedämpfter
SHADOW       = (15, 8, 0)         # dunkles Braun-Schwarz

TITLE_TILT   = 7      # Grad Neigung (positiv = links runter, rechts hoch)
AUTHOR_TILT  = 0      # Autor gerade lassen

TITLE_CENTER_Y  = 90  # Mitte des Titels vom oberen Rand (px)
AUTHOR_BOTTOM   = 55  # Y-Abstand Autor vom unteren Rand (px)

SHADOW_OFFSET = 5     # Schatten-Versatz (px)
# =================

img = Image.open(INPUT).convert("RGBA")
W, H = img.size

ft = ImageFont.truetype(FONT, TITLE_SIZE)
fa = ImageFont.truetype(FONT, AUTHOR_SIZE)

def paste_tilted_text(base, text, font, color, shadow_color, shadow_off, center_x, center_y, angle):
    """Text auf transparentem Layer rendern, kippen, auf Basis einfügen."""
    dummy_draw = ImageDraw.Draw(base)
    bb = dummy_draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]

    pad = max(tw, th)
    tmp = Image.new("RGBA", (tw + pad, th + pad), (0, 0, 0, 0))
    td  = ImageDraw.Draw(tmp)

    ox = pad // 2 - bb[0]
    oy = pad // 2 - bb[1]

    # Schatten
    td.text((ox + shadow_off, oy + shadow_off), text, font=font, fill=shadow_color + (220,))
    # Text
    td.text((ox, oy), text, font=font, fill=color + (255,))

    rotated = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
    rx, ry  = rotated.size
    px = center_x - rx // 2
    py = center_y - ry // 2
    base.paste(rotated, (px, py), rotated)

# Titel: geneigt, zentriert
paste_tilted_text(img, TITLE, ft, TITLE_GOLD, SHADOW, SHADOW_OFFSET,
                  W // 2, TITLE_CENTER_Y, TITLE_TILT)

# Autor: gerade, unten zentriert
dummy = ImageDraw.Draw(img)
bb2 = dummy.textbbox((0, 0), AUTHOR, font=fa)
ah  = bb2[3] - bb2[1]
paste_tilted_text(img, AUTHOR, fa, AUTHOR_GOLD, SHADOW, SHADOW_OFFSET,
                  W // 2, H - AUTHOR_BOTTOM - ah // 2, AUTHOR_TILT)

out = img.convert("RGB")
out.save(OUTPUT, "PNG", quality=95)
print(f"Gespeichert: {OUTPUT}  ({W}x{H})")
