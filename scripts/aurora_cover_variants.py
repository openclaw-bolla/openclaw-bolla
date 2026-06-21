#!/usr/bin/env python3
"""
AURORA Cover — 4 saubere Neuentwürfe aus der textlosen Basis (cover_v6.png).
Behebt: Geister-Spiegelungen oben, breiter Rand über AURORA, Name zu nah an Figur.

Vorgehen: textlose 1024²-Basis → 1600 breit hochskalieren → in 1600×2560-Leinwand
setzen, oben/unten dunkel ausblenden (cinematisch, KEIN Outpaint-Geist) →
Titel + Autor frei platzieren (Orbitron-Bold, Gold wie Original).

Aufruf: python3 aurora_cover_variants.py
Erzeugt: /mnt/d/OneDrive/Desktop/AURORA Cover-Vorschlaege/V1..V4 + Kontaktbogen
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
from pathlib import Path

SRC   = "/mnt/d/OneDrive/Dokumente/AURORA/cover_v6.png"
FONT  = "/tmp/aurora_fonts/Orbitron-var.ttf"
OUT   = Path("/mnt/d/OneDrive/Desktop/AURORA Cover-Vorschlaege")
OUT.mkdir(parents=True, exist_ok=True)

CW, CH = 1600, 2560
BG = (8, 5, 3)
TITLE_GOLD  = (224, 158, 42)
AUTHOR_GOLD = (200, 146, 40)
CREAM       = (232, 214, 188)
SHADOW      = (10, 5, 0)

def f_bold(size):
    f = ImageFont.truetype(FONT, size);
    try: f.set_variation_by_name("Bold")
    except: pass
    return f
def f_semibold(size):
    f = ImageFont.truetype(FONT, size)
    try: f.set_variation_by_name("SemiBold")
    except: pass
    return f

# --- saubere Basis laden + hochskalieren (1024 -> 1600 breit) ------------------
sq = Image.open(SRC).convert("RGB")
scene = sq.resize((CW, CW), Image.LANCZOS)              # 1600x1600
scene = ImageEnhance.Sharpness(scene).enhance(1.25)     # gegen Upscale-Weichheit
scene_arr = np.asarray(scene).astype(np.float32)

def build_plate(scene_top):
    """Szene (1600x1600) auf 2560-Leinwand bei y=scene_top, Ränder dunkel ausblenden."""
    canvas = np.zeros((CH, CW, 3), np.float32)
    canvas[:] = BG
    y0 = scene_top
    y1 = scene_top + CW
    # Szene einsetzen (ggf. clippen)
    cs, ce = max(0,y0), min(CH,y1)
    ss, se = cs-y0, ce-y0
    canvas[cs:ce] = scene_arr[ss:se]
    # oben: von oberster Szenenzeile zu BG ausblenden
    if y0 > 0:
        top_row = scene_arr[0]
        for y in range(y0):
            t = y / y0                      # 0=oben(BG) .. 1=Szene
            canvas[y] = BG_arr*(1-t) + top_row*t
    # unten: von unterster Szenenzeile zu BG ausblenden
    if y1 < CH:
        bot_row = scene_arr[-1]
        n = CH - y1
        for i in range(n):
            t = i / n                       # 0=Szene .. 1=BG
            canvas[y1+i] = bot_row*(1-t) + BG_arr*t
    return canvas

BG_arr = np.array(BG, np.float32)

def vignette(arr, strength=0.55, soft=0.7):
    h,w,_=arr.shape
    yy,xx=np.mgrid[0:h,0:w]
    cx,cy=w/2,h/2
    d=np.sqrt(((xx-cx)/(w*0.5))**2+((yy-cy)/(h*0.62))**2)
    m=np.clip((d-soft)/(1-soft),0,1)*strength
    return arr*(1-m[...,None])

def tilted(draw_img, text, font, color, cx, cy, angle=0, shadow=SHADOW, soff=5):
    base=Image.new("RGBA",(1,1)); d=ImageDraw.Draw(base)
    bb=d.textbbox((0,0),text,font=font); tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    pad=max(tw,th)//1+40
    tmp=Image.new("RGBA",(tw+pad,th+pad),(0,0,0,0)); td=ImageDraw.Draw(tmp)
    ox=pad//2-bb[0]; oy=pad//2-bb[1]
    td.text((ox+soff,oy+soff),text,font=font,fill=shadow+(210,))
    td.text((ox,oy),text,font=font,fill=color+(255,))
    rot=tmp.rotate(angle,expand=True,resample=Image.BICUBIC)
    rx,ry=rot.size
    draw_img.paste(rot,(int(cx-rx/2),int(cy-ry/2)),rot)

def fit_font(text, target_w, maker, start=60, cap=420):
    d=ImageDraw.Draw(Image.new("RGB",(10,10)))
    s=start
    while s<cap:
        if d.textlength(text,font=maker(s))>=target_w: break
        s+=2
    return maker(s), s

def save(arr_or_img, name):
    img = arr_or_img if isinstance(arr_or_img,Image.Image) else Image.fromarray(np.clip(arr_or_img,0,255).astype(np.uint8))
    p=OUT/f"{name}.png"; img.convert("RGB").save(p)
    # JPG-Vorschau (klein) zusätzlich
    img.convert("RGB").save(OUT/f"{name}.jpg","JPEG",quality=90)
    print("  ->",p.name)
    return img

print("Baue Varianten...")

# ============ V1 — Klassisch, gesäubert (Titel über Gesicht, Name ganz unten) =
arr = build_plate(scene_top=470)
img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
d = ImageDraw.Draw(img)
ft,_ = fit_font("AURORA", 1180, f_bold)
tilted(img,"AURORA",ft,TITLE_GOLD, CW//2, 690, angle=7, soff=7)
fa,_ = fit_font("Chris Mandel", 600, f_semibold)
tilted(img,"Chris Mandel",fa,AUTHOR_GOLD, CW//2, 2395, angle=0, soff=4)
v1=save(img,"V1_klassisch_gesaeubert")

# ============ V2 — Titel oben im Dunkel (Title-Bar-Look) ======================
arr = build_plate(scene_top=560)
img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
ft,_ = fit_font("AURORA", 1080, f_bold)
tilted(img,"AURORA",ft,TITLE_GOLD, CW//2, 300, angle=0, soff=6)
fa,_ = fit_font("Chris Mandel", 560, f_semibold)
tilted(img,"Chris Mandel",fa,AUTHOR_GOLD, CW//2, 2410, angle=0, soff=4)
v2=save(img,"V2_titel_oben")

# ============ V3 — Cinematic: Vignette + Tagline ==============================
arr = build_plate(scene_top=470)
arr = vignette(arr, strength=0.5)
img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
ft,_ = fit_font("AURORA", 1120, f_bold)
tilted(img,"AURORA",ft,TITLE_GOLD, CW//2, 660, angle=7, soff=7)
# Tagline
tag = f_semibold(46)
d=ImageDraw.Draw(img)
tt="Was bleibt, wenn die Maschinen träumen"
tw=d.textlength(tt,font=tag)
d.text((CW//2-tw/2+3,795+3),tt,font=tag,fill=SHADOW)
d.text((CW//2-tw/2,795),tt,font=tag,fill=CREAM)
fa,_ = fit_font("Chris Mandel", 600, f_semibold)
tilted(img,"Chris Mandel",fa,AUTHOR_GOLD, CW//2, 2400, angle=0, soff=4)
v3=save(img,"V3_cinematic_tagline")

# ============ V4 — Großer Titel, minimalistisch (Szene tiefer) ================
arr = build_plate(scene_top=720)
img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
ft,_ = fit_font("AURORA", 1300, f_bold)
tilted(img,"AURORA",ft,TITLE_GOLD, CW//2, 360, angle=0, soff=8)
fa,_ = fit_font("Chris Mandel", 620, f_semibold)
tilted(img,"Chris Mandel",fa,AUTHOR_GOLD, CW//2, 2430, angle=0, soff=4)
v4=save(img,"V4_grosser_titel")

# ============ Kontaktbogen (alle 4 nebeneinander) =============================
thumbs=[v1,v2,v3,v4]; tw,th=400,640
sheet=Image.new("RGB",(tw*4+50,th+90),(20,20,24))
ds=ImageDraw.Draw(sheet)
labels=["V1 klassisch","V2 Titel oben","V3 cinematic","V4 gross"]
lf=ImageFont.truetype(FONT,28)
for i,(t,l) in enumerate(zip(thumbs,labels)):
    th_img=t.resize((tw,th),Image.LANCZOS)
    x=10+i*(tw+10)
    sheet.paste(th_img,(x,10))
    ds.text((x+10,th+25),l,font=lf,fill=(230,200,120))
sheet.save(OUT/"_KONTAKTBOGEN.jpg","JPEG",quality=92)
print("Kontaktbogen ->",OUT/"_KONTAKTBOGEN.jpg")
print("FERTIG. Ordner:",OUT)
