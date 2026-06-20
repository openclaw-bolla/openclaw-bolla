#!/usr/bin/env python3
"""
AURORA — KDP-Taschenbuch-Cover-Wrap (Vorderseite + Rücken + Rückseite) als 300-dpi-PDF.
Front nutzt das vorhandene eBook-Cover; Rücken + Rückseite werden im Cover-Stil
(dunkel mit warmem Glow) gesetzt. Buchrücken-Breite aus Seitenzahl (creme Papier).

Aufruf:  python3 aurora_cover_wrap.py de 459
         python3 aurora_cover_wrap.py en 442
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LANG  = sys.argv[1].lower()
PAGES = int(sys.argv[2])

DPI = 300
BLEED, TRIM_W, TRIM_H = 0.125, 5.0, 8.0
CREME = 0.0025                       # Zoll pro Seite (cremefarbenes Papier)
SPINE = PAGES * CREME
COVER_W_IN = BLEED*2 + TRIM_W*2 + SPINE
COVER_H_IN = TRIM_H + BLEED*2
def px(inch): return int(round(inch * DPI))

CW, CH = px(COVER_W_IN), px(COVER_H_IN)
FB = "/home/bolla/workspace/fonts/ebgaramond"
FRONT_IMG = "/mnt/d/OneDrive/Dokumente/AURORA/cover_kdp.jpg"
BLURB = Path(f"/home/bolla/workspace/data/klappentext_{LANG}.txt").read_text().strip()
OUT = f"/mnt/d/OneDrive/Dokumente/AURORA/AURORA_cover_{LANG}.pdf"

# Farben (aus Cover gesampelt: dunkles Braun-Schwarz, warmes Orange)
BG      = (13, 8, 5)
GLOW    = (150, 60, 15)
CREAM   = (235, 222, 205)
ORANGE  = (240, 150, 60)

canvas = Image.new("RGB", (CW, CH), BG)
draw = ImageDraw.Draw(canvas)

# --- Warmer Glow oben über Rückseite + Rücken (subtil) ------------------------
glow = Image.new("RGB", (CW, CH), BG)
gd = ImageDraw.Draw(glow)
for y in range(CH):
    t = max(0, 1 - y / (CH*0.55))           # oben am stärksten
    r = int(BG[0] + (GLOW[0]-BG[0]) * t * 0.5)
    g = int(BG[1] + (GLOW[1]-BG[1]) * t * 0.5)
    b = int(BG[2] + (GLOW[2]-BG[2]) * t * 0.5)
    gd.line([(0, y), (CW, y)], fill=(r, g, b))
canvas.paste(glow, (0, 0))
draw = ImageDraw.Draw(canvas)

# --- Front-Panel (rechts): vorhandenes Cover, randfüllend ---------------------
front_w = px(TRIM_W + BLEED)            # 5.125"
front_x = px(BLEED + TRIM_W + SPINE)
fimg = Image.open(FRONT_IMG).convert("RGB")
# auf Panelgröße skalieren (cover-fill, mittig croppen)
scale = max(front_w / fimg.width, CH / fimg.height)
fimg_r = fimg.resize((int(fimg.width*scale)+1, int(fimg.height*scale)+1))
ox = (fimg_r.width - front_w)//2
oy = (fimg_r.height - CH)//2
fimg_c = fimg_r.crop((ox, oy, ox+front_w, oy+CH))
canvas.paste(fimg_c, (front_x, 0))

# --- Schriften ----------------------------------------------------------------
def font(name, size): return ImageFont.truetype(f"{FB}/{name}", size)
f_spine_t = font("EBGaramond-Bold.ttf", 64)
f_spine_a = font("EBGaramond-Regular.ttf", 40)
f_blurb   = font("EBGaramond-Regular.ttf", 41)
f_blurb_i = font("EBGaramond-Italic.ttf", 41)
f_tag     = font("EBGaramond-Italic.ttf", 38)

# --- Buchrücken ---------------------------------------------------------------
spine_x0 = px(BLEED + TRIM_W)
spine_w  = px(SPINE)
si = Image.new("RGB", (CH, spine_w), (0,0,0))   # quer, wird gedreht
sd = ImageDraw.Draw(si)
title = "AURORA"
author = "Chris Mandel"
tb = sd.textbbox((0,0), title, font=f_spine_t)
ab = sd.textbbox((0,0), author, font=f_spine_a)
# Titel links (=oben nach Drehung), Autor rechts (=unten)
sd.text((px(0.8), (spine_w-(tb[3]-tb[1]))//2 - tb[1]), title, font=f_spine_t, fill=ORANGE)
sd.text((CH-px(0.8)-(ab[2]-ab[0]), (spine_w-(ab[3]-ab[1]))//2 - ab[1]), author, font=f_spine_a, fill=CREAM)
si = si.rotate(90, expand=True)
# transparente schwarze Pixel nicht übernehmen → direkt pasten (Rücken ist eh dunkel)
canvas.paste(si, (spine_x0, 0))

# --- Rückseite (links): Klappentext -------------------------------------------
safe = px(BLEED + 0.3)                      # Sicherheitsabstand vom Trim
back_x0 = safe
back_x1 = px(BLEED + TRIM_W) - px(0.3)
text_w = back_x1 - back_x0

def wrap(text, fnt):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= text_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

y = px(0.9)
for para in BLURB.split("\n\n"):
    para = para.strip()
    if not para: continue
    is_last = para.startswith("AURORA ist") or para.startswith("AURORA is")
    fnt = f_tag if is_last else f_blurb
    col = ORANGE if is_last else CREAM
    for ln in wrap(para, fnt):
        draw.text((back_x0, y), ln, font=fnt, fill=col)
        y += int(fnt.size * 1.34)
    y += int(fnt.size * 0.6)

# Barcode-Freibereich unten rechts (KDP setzt ISBN-Barcode ~2"x1.2")
# -> dort lassen wir bewusst Platz (kein Text); optional dezenter Kasten:
bx1, by1 = px(BLEED + TRIM_W) - px(0.35), CH - px(BLEED + 0.4)
bx0, by0 = bx1 - px(2.0), by1 - px(1.2)
# (kein Kasten gezeichnet — KDP legt Barcode auf weißen Grund automatisch an)

canvas.save(OUT, "PDF", resolution=DPI)
print(f"✅ {OUT}")
print(f"   Gesamt: {COVER_W_IN:.3f} x {COVER_H_IN:.3f} Zoll  ({CW}x{CH}px @ {DPI}dpi)")
print(f"   Buchrücken: {SPINE:.3f} Zoll ({SPINE*25.4:.1f} mm) bei {PAGES} Seiten, creme")
