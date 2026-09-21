#!/usr/bin/env python3
"""Robins GTA-VI-Geburtstagsgutschein (10x15 quer, 1772x1181) — v10, Logo exakt zentriert.

Quellen: workspace-unabhängig unter Bolla\\KI Bilder\\GTA VI\\
  _used_for_gutschein_v3.jpg  = Rockstar-Cover-Mosaik 3840x2160 (Logo liegt dort bei x1156..2681, y672..1693)
  vi.*.png                    = freigestelltes GTA-VI-Logo (807x540, Alpha)
  Jason_and_Lucia_Robbery_portrait.*.jpg = Ersatzbild fuer das Umarmungs-Panel (Renis Wunsch)

Aufruf: build_gta6_gutschein_robin.py <ausgabe.png> [crop|letterbox]
  crop      = 3:2-Ausschnitt mit Logo exakt in der Kartenmitte (Standard)
  letterbox = komplettes Mosaik unbeschnitten, oben/unten dunkler Rahmen, Logo exakt in der Mitte
"""
import glob
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = "/mnt/d/OneDrive/Dokumente/Bolla/KI Bilder/GTA VI/"
W, H = 1772, 1181
FRAME = (29, 0, 46)
LOGO_SCALE, LOGO_X0, LOGO_Y0 = 1.89, 1156, 672          # per Template-Matching gemessen (NCC 0.997)
PANEL = (779, 64, 1904, 1208)                            # Umarmungs-Panel im 3840er Mosaik
TEXT = "Gutschein GTA VI & Konsole"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAQUE_BOTTOM_MARGIN = 75


def build_mosaic():
    mosaic = Image.open(SRC + "_used_for_gutschein_v3.jpg").convert("RGB")
    photo = Image.open(glob.glob(SRC + "Jason_and_Lucia_Robbery_portrait.*.jpg")[0]).convert("RGB")
    pw, ph = PANEL[2] - PANEL[0], PANEL[3] - PANEL[1]
    mosaic.paste(photo.crop((0, 220, 1080, 1323)).resize((pw, ph), Image.LANCZOS), PANEL[:2])

    logo = Image.open(glob.glob(SRC + "vi.*.png")[0]).convert("RGBA")
    lw, lh = round(logo.width * LOGO_SCALE), round(logo.height * LOGO_SCALE)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    layer = Image.new("RGBA", mosaic.size, (0, 0, 0, 0))
    layer.paste(logo, (LOGO_X0, LOGO_Y0))
    clip = Image.new("L", mosaic.size, 0)
    ImageDraw.Draw(clip).rectangle(PANEL, fill=255)          # Logo nur im getauschten Panel neu aufsetzen
    a = layer.getchannel("A")
    from PIL import ImageChops
    layer.putalpha(ImageChops.multiply(a, clip))
    mosaic = Image.alpha_composite(mosaic.convert("RGBA"), layer).convert("RGB")
    cx, cy = LOGO_X0 + lw / 2, LOGO_Y0 + lh / 2
    return mosaic, cx, cy, lw, lh


def place(mosaic, cx, cy, mode):
    if mode == "letterbox":
        s = W / mosaic.width
        m = mosaic.resize((W, round(mosaic.height * s)), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), FRAME)
        canvas.paste(m, (0, round(H / 2 - cy * s)))
        return canvas, s
    # crop: 3:2-Fenster, vertikal + horizontal exakt um den Logo-Mittelpunkt
    ch = 2 * min(cy, mosaic.height - cy)
    cw = ch * W / H
    x0, y0 = cx - cw / 2, cy - ch / 2
    if x0 < 0 or x0 + cw > mosaic.width:
        raise SystemExit("Fenster ragt seitlich raus")
    canvas = mosaic.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W, H), Image.LANCZOS)
    return canvas, H / ch


def add_plaque(canvas):
    d = ImageDraw.Draw(canvas)
    size = 66
    font = ImageFont.truetype(FONT, size)
    bb = d.textbbox((0, 0), TEXT, font=font, stroke_width=3)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad_x, pad_y = 56, 30
    pw, ph = tw + 2 * pad_x, th + 2 * pad_y
    x0, y0 = (W - pw) // 2, H - PLAQUE_BOTTOM_MARGIN - ph
    box = (x0, y0, x0 + pw, y0 + ph)

    region = canvas.crop(box).filter(ImageFilter.GaussianBlur(14)).filter(ImageFilter.GaussianBlur(14))
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=28, fill=255)
    canvas.paste(region, (x0, y0), mask)
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=28, fill=(24, 8, 40, 120), outline=(255, 255, 255, 95), width=3)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
    ImageDraw.Draw(canvas).text(((W) / 2, y0 + ph / 2), TEXT, font=font, fill=(255, 255, 255),
                                stroke_width=3, stroke_fill=(0, 0, 0), anchor="mm")
    return canvas, box


if __name__ == "__main__":
    out = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "crop"
    mosaic, cx, cy, lw, lh = build_mosaic()
    canvas, s = place(mosaic, cx, cy, mode)
    logo_box = (W / 2 - lw * s / 2, H / 2 - lh * s / 2, W / 2 + lw * s / 2, H / 2 + lh * s / 2)
    canvas, plaque = add_plaque(canvas)
    print("Logo-Box", [round(v) for v in logo_box], "Plakette", plaque,
          "Ueberschneidung:", not (plaque[1] >= logo_box[3] or plaque[3] <= logo_box[1]))
    canvas.save(out)
