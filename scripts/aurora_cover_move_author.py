#!/usr/bin/env python3
"""
AURORA Cover — Autorenname tiefer setzen.
Chris' Wunsch (20.06.2026): "Chris Mandel" stand direkt unter der sitzenden Frau
(= Figur Marlie) → konnte wirken, als sei ER Marlie. Name wird nach unten gezogen,
klar von der Figur abgesetzt (wie bei Büchern üblich).

Vorgehen:
  1. Alten Namen entfernen: schmale bbox per vertikaler Interpolation der sauberen
     Zeilen ober-/unterhalb rekonstruieren (Boden ist glatter Horizontal-Gradient).
  2. Zielzone tiefer dezent abdunkeln (unterdrückt Spiegel-Ghosting/Orange-Streifen).
  3. Namen in Orbitron-Bold (Gold, wie Original) neu setzen, mittig, tiefer.

Aufruf:  python3 aurora_cover_move_author.py
Erzeugt: cover_kdp.jpg (überschrieben, Backup vorher) + cover_kdp.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from pathlib import Path
import shutil, datetime

SRC   = "/mnt/d/OneDrive/Dokumente/AURORA/cover_kdp.jpg"
FONT  = "/tmp/aurora_fonts/Orbitron-var.ttf"
AUTHOR = "Chris Mandel"
GOLD   = (193, 143, 40)
SHADOW = (12, 6, 0)

# Backup
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bak = SRC.replace(".jpg", f".bak_vor_namensverschiebung_{ts}.jpg")
shutil.copy2(SRC, bak)
print("Backup:", bak)

im = Image.open(SRC).convert("RGB")
W, H = im.size
arr = np.asarray(im).astype(np.float32)

# --- 1. Alten Namen entfernen (vertikale Interpolation) -----------------------
# Text gemessen: x 460-1150, y 1932-1993 (Kern). Schatten ~+8px. Großzügige bbox:
x0, x1 = 360, 1240
yt, yb = 1900, 2030
top_row = arr[yt-12]          # saubere Bodenzeile oberhalb
bot_row = arr[yb+12]          # saubere Bodenzeile unterhalb
h = yb - yt
for i in range(h):
    t = i / h
    arr[yt + i, x0:x1] = (top_row[x0:x1] * (1 - t) + bot_row[x0:x1] * t)
# leichtes Rauschen gegen Banding
rng = np.random.default_rng(42)
noise = rng.normal(0, 2.0, (h, x1 - x0, 3))
arr[yt:yb, x0:x1] += noise
arr = np.clip(arr, 0, 255)

im = Image.fromarray(arr.astype(np.uint8))
# Feather: die rekonstruierte bbox leicht glätten + mit Original-Rand verblenden
patch = im.crop((x0, yt, x1, yb)).filter(ImageFilter.GaussianBlur(2))
im.paste(patch, (x0, yt))

# --- 2. Zielzone tiefer dezent abdunkeln --------------------------------------
arr = np.asarray(im).astype(np.float32)
ny0, ny1 = 2070, 2240          # neue Namens-Zone
nx0, nx1 = 300, 1300
# weiche Maske (innen voll, Ränder feathern)
mask = np.zeros((H, W), np.float32)
mask[ny0:ny1, nx0:nx1] = 1.0
mask = np.asarray(Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(60))).astype(np.float32)/255.0
DARK = 0.45                     # auf 45% abdunkeln
arr *= (1 - mask[..., None]*(1-DARK))
im = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))

# --- 3. Namen neu setzen (mittig, tiefer) -------------------------------------
draw = ImageDraw.Draw(im)
def author_font(size):
    f = ImageFont.truetype(FONT, size)
    try: f.set_variation_by_name("Bold")
    except Exception: pass
    return f

# Größe so wählen, dass Breite ~ Original (~640px inkl. Original-Spacing-Optik)
TARGET_W = 640
size = 60
while size < 200:
    f = author_font(size)
    w = draw.textlength(AUTHOR, font=f)
    if w >= TARGET_W: break
    size += 2
f = author_font(size)
w = draw.textlength(AUTHOR, font=f)
bb = draw.textbbox((0,0), AUTHOR, font=f)
th = bb[3]-bb[1]
cx = W//2
cy = (ny0+ny1)//2
px = cx - int(w)//2
py = cy - th//2 - bb[1]
# Schatten + Text
draw.text((px+5, py+5), AUTHOR, font=f, fill=SHADOW)
draw.text((px, py), AUTHOR, font=f, fill=GOLD)
print(f"Neuer Name: size={size}, breite={int(w)}px, center_y={cy}")

# --- Speichern ----------------------------------------------------------------
out = im.convert("RGB")
out.save(SRC, "JPEG", quality=92)
out.save(SRC.replace(".jpg", ".png"), "PNG")
print("Gespeichert:", SRC, "+ .png", out.size)
