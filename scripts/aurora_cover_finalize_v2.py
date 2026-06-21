#!/usr/bin/env python3
"""
AURORA Cover FINAL — Variante V2 (Titel oben, sauberes Dunkelband, Name ganz unten).
Baut aus textloser Basis cover_v6.png, max. Schärfe (Lanczos + Unsharp + feines Korn).
Schreibt in die echten Cover-Pfade (mit Backups) und triggert KEINE Rebuilds
(die laufen separat im Aufrufer).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np, shutil, datetime

SRC   = "/mnt/d/OneDrive/Dokumente/AURORA/cover_v6.png"
FONT  = "/tmp/aurora_fonts/Orbitron-var.ttf"
KDP   = "/mnt/d/OneDrive/Dokumente/AURORA/cover_kdp.jpg"
KDPP  = "/mnt/d/OneDrive/Dokumente/AURORA/cover_kdp.png"
PORT  = "/mnt/d/OneDrive/Dokumente/AURORA/cover_v6_portrait.png"

CW, CH = 1600, 2560
BG = np.array((8,5,3), np.float32)
TITLE_GOLD  = (224,158,42)
AUTHOR_GOLD = (200,146,40)
SHADOW = (10,5,0)

def f_bold(s):
    f=ImageFont.truetype(FONT,s)
    try: f.set_variation_by_name("Bold")
    except: pass
    return f
def f_semibold(s):
    f=ImageFont.truetype(FONT,s)
    try: f.set_variation_by_name("SemiBold")
    except: pass
    return f

# --- Szene laden, scharf hochskalieren ---------------------------------------
sq = Image.open(SRC).convert("RGB")
scene = sq.resize((CW,CW), Image.LANCZOS)
scene = scene.filter(ImageFilter.UnsharpMask(radius=2.2, percent=95, threshold=2))
scene = ImageEnhance.Contrast(scene).enhance(1.04)
scene_arr = np.asarray(scene).astype(np.float32)

# --- Plate: Szene bei scene_top, Ränder weich auf BG ausblenden --------------
scene_top = 560
canvas = np.zeros((CH,CW,3), np.float32); canvas[:] = BG
y0, y1 = scene_top, scene_top+CW
canvas[y0:y1] = scene_arr
top_row, bot_row = scene_arr[0], scene_arr[-1]
for y in range(y0):
    t=y/y0; canvas[y]=BG*(1-t)+top_row*t
n=CH-y1
for i in range(n):
    t=i/n; canvas[y1+i]=bot_row*(1-t)+BG*t

# --- feines Filmkorn NUR auf der helleren Szene (nicht in dunklen Flächen) ----
# Grain in großen Schwarzflächen killt PNG-Kompression → nur dort, wo Bildinhalt.
rng=np.random.default_rng(7)
lum=canvas.mean(axis=2,keepdims=True)
grain_mask=np.clip((lum-25)/60,0,1)            # erst ab mittlerer Helligkeit
grain=rng.normal(0,1.6,(CH,CW,1))*grain_mask
canvas=np.clip(canvas+grain,0,255)

img=Image.fromarray(canvas.astype(np.uint8))

# --- Text: AURORA oben, Chris Mandel unten -----------------------------------
def tilted(im,text,font,color,cx,cy,angle=0,soff=6):
    d=ImageDraw.Draw(Image.new("RGBA",(1,1)))
    bb=d.textbbox((0,0),text,font=font); tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    pad=max(tw,th)+40
    tmp=Image.new("RGBA",(tw+pad,th+pad),(0,0,0,0)); td=ImageDraw.Draw(tmp)
    ox=pad//2-bb[0]; oy=pad//2-bb[1]
    td.text((ox+soff,oy+soff),text,font=font,fill=SHADOW+(210,))
    td.text((ox,oy),text,font=font,fill=color+(255,))
    rot=tmp.rotate(angle,expand=True,resample=Image.BICUBIC)
    rx,ry=rot.size
    im.paste(rot,(int(cx-rx/2),int(cy-ry/2)),rot)

def fit(text,target_w,maker,start=60,cap=420):
    d=ImageDraw.Draw(Image.new("RGB",(10,10))); s=start
    while s<cap and d.textlength(text,font=maker(s))<target_w: s+=2
    return maker(s)

tilted(img,"AURORA", fit("AURORA",1080,f_bold), TITLE_GOLD, CW//2, 300, angle=0, soff=6)
tilted(img,"Chris Mandel", fit("Chris Mandel",560,f_semibold), AUTHOR_GOLD, CW//2, 2410, angle=0, soff=4)

# --- Backups + Speichern -----------------------------------------------------
ts=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
for p in (KDP,KDPP,PORT):
    try: shutil.copy2(p, p.rsplit(".",1)[0]+f".bak_vorV2_{ts}."+p.rsplit(".",1)[1])
    except FileNotFoundError: pass
out=img.convert("RGB")
out.save(KDP,"JPEG",quality=93)
out.save(KDPP,"PNG",optimize=True)
out.save(PORT,"PNG",optimize=True)
print("FINAL V2 gespeichert:", KDP, KDPP, PORT, out.size)
