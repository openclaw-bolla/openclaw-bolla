#!/usr/bin/env python3
"""
Aufpeppen-Engine — macht aus einem Bild/Video einen Feel-Good-Post im Sinne von Chris' Profil
(„Feel-Good mit Augenzwinkern": sonnig, optimistisch, verspielt). Kostenlos: PIL + ffmpeg, kein API-€.

Aufruf:
    python3 aufpeppen.py <datei> [--platform insta|tiktok] [--style auto|natural|vivid|spectacular]
                                 [--text "Hook/Slogan"] [--music <song.mp3>] [--out <zieldatei>]

BILD  -> Feel-Good-Grading (Wärme, Sättigung, Kontrast, sanfter Glow, Vignette),
         Format je Plattform (insta 4:5 = 1080x1350, sonst 1:1 = 1080x1080), optional Text-Overlay.
BILD als TikTok -> wird zusätzlich zu einem 6s-Ken-Burns-Video (Hochformat) gemacht.
VIDEO -> Hochformat 1080x1920 (Blur-Fill), sonniges Grading, optional Musikbett + Musik-Wellen, optional Hook-Text.

Rückgabe: schreibt Zieldatei, druckt am Ende  RESULT:<pfad>
"""
import os, sys, subprocess, argparse

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic")
VID_EXT = (".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm")

# Grading-Presets (Bild): (Sättigung, Kontrast, Helligkeit, Wärme-R, Wärme-B, Glow, Vignette)
IMG_PRESETS = {
    "natural":     dict(sat=1.10, con=1.05, bri=1.03, warm=1.03, cool=0.99, glow=0.12, vig=0.10),
    "vivid":       dict(sat=1.28, con=1.12, bri=1.05, warm=1.06, cool=0.97, glow=0.20, vig=0.18),
    "spectacular": dict(sat=1.45, con=1.18, bri=1.06, warm=1.09, cool=0.95, glow=0.30, vig=0.26),
}

def is_image(p): return p.lower().endswith(IMG_EXT)
def is_video(p): return p.lower().endswith(VID_EXT)

def pick_style(style):
    return IMG_PRESETS.get(style if style in IMG_PRESETS else "vivid")

# ---------------- BILD ----------------
def pep_image(src, out, platform, style, text):
    from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageChops
    p = pick_style(style)
    im = Image.open(src).convert("RGB")

    # Wärme (Farbkanäle skalieren)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * p["warm"])))
    b = b.point(lambda v: int(v * p["cool"]))
    im = Image.merge("RGB", (r, g, b))
    # Sättigung / Kontrast / Helligkeit
    im = ImageEnhance.Color(im).enhance(p["sat"])
    im = ImageEnhance.Contrast(im).enhance(p["con"])
    im = ImageEnhance.Brightness(im).enhance(p["bri"])
    # Glow (Bloom): heller Blur additiv drübergelegt
    if p["glow"] > 0:
        blur = im.filter(ImageFilter.GaussianBlur(max(2, im.width // 120)))
        im = ImageChops.screen(im, ImageChops.multiply(blur, Image.new("RGB", im.size, (int(255*p["glow"]),)*3)))
    # leichte Schärfung
    im = im.filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))

    # Format / Crop
    tw, th = (1080, 1350) if platform == "insta" else (1080, 1080)
    im = crop_to(im, tw, th)

    # Vignette
    if p["vig"] > 0:
        im = apply_vignette(im, p["vig"])

    # Text-Overlay (optional)
    if text:
        im = draw_text(im, text)

    im.save(out, quality=92)
    return out

def crop_to(im, tw, th):
    from PIL import Image
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))

def apply_vignette(im, strength):
    from PIL import Image, ImageDraw, ImageFilter
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w*0.2, -h*0.2, w*1.2, h*1.2], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h)//6))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(im, Image.blend(im, dark, strength), mask)

def draw_text(im, text):
    from PIL import ImageDraw, ImageFont
    w, h = im.size
    d = ImageDraw.Draw(im)
    size = int(w / 12)
    font = None
    for fp in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
               "/mnt/c/Windows/Fonts/ ariblk.ttf", "/mnt/c/Windows/Fonts/arialbd.ttf"]:
        if os.path.isfile(fp):
            try: font = ImageFont.truetype(fp, size); break
            except Exception: pass
    if font is None:
        font = ImageFont.load_default()
    # unten mittig, mit Schatten + Halbtransparenz-Balken
    lines = wrap(text, font, d, int(w*0.9))
    total_h = sum((d.textbbox((0,0), l, font=font)[3]) for l in lines) + (len(lines)-1)*10
    y = h - total_h - int(h*0.06)
    for line in lines:
        bb = d.textbbox((0,0), line, font=font)
        lw = bb[2]-bb[0]
        x = (w - lw)//2
        for dx,dy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,4)]:
            d.text((x+dx, y+dy), line, font=font, fill=(0,0,0))
        d.text((x, y), line, font=font, fill=(255, 240, 150))
        y += bb[3]-bb[1] + 14
    return im

def wrap(text, font, d, maxw):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textbbox((0,0), t, font=font)[2] <= maxw:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines[:3]

# ---------------- VIDEO ----------------
def pep_video(src, out, style, text, music):
    p = pick_style(style if style in IMG_PRESETS else "vivid")
    # sonniges Grading via eq + colorbalance
    grade = (f"eq=saturation={p['sat']:.2f}:contrast={p['con']:.2f}:brightness={(p['bri']-1)*0.4:.3f}:gamma=1.02,"
             f"colorbalance=rm=0.06:bm=-0.05")
    base = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            + grade)
    draw = ""
    if text:
        safe = text.replace(":", "\\:").replace("'", "’")
        draw = (f",drawtext=text='{safe}':fontcolor=0xFFF096:fontsize=58:borderw=4:bordercolor=black:"
                f"x=(w-text_w)/2:y=h-360:box=0")
    if music and os.path.isfile(music):
        fc = (f"[0:v]{base}{draw}[v];"
              f"[1:a]showwaves=s=1080x200:mode=cline:rate=30:colors=0xFFFFFF|0xFFD447[w];"
              f"[v][w]overlay=0:H-260:format=auto[vid]")
        cmd = ["ffmpeg","-y","-i",src,"-i",music,"-filter_complex",fc,
               "-map","[vid]","-map","1:a","-c:v","libx264","-pix_fmt","yuv420p",
               "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out]
    else:
        fc = f"[0:v]{base}{draw}[vid]"
        cmd = ["ffmpeg","-y","-i",src,"-filter_complex",fc,"-map","[vid]",
               "-map","0:a?","-c:v","libx264","-pix_fmt","yuv420p",
               "-c:a","aac","-b:a","192k","-movflags","+faststart",out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=300).returncode == 0

def image_to_video(src, out, text, music, dur=6):
    """Standbild -> Ken-Burns-Hochformat-Video (für TikTok aus einem Foto)."""
    frames = dur*30
    grade = "eq=saturation=1.25:contrast=1.1:brightness=0.02,colorbalance=rm=0.06:bm=-0.05"
    fc = (f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,{grade}[bg];"
          f"[0:v]scale=1600:1600:flags=lanczos,{grade}[big];"
          f"[big]zoompan=z='min(zoom+0.0008,1.2)':d={frames}:s=1000x1000:fps=30[fg];"
          f"[bg][fg]overlay=x=(W-w)/2:y=(H-h)/2[vid]")
    inp = ["-loop","1","-i",src]
    if music and os.path.isfile(music):
        inp += ["-ss","30","-t",str(dur),"-i",music]
        cmd = ["ffmpeg","-y",*inp,"-filter_complex",fc,"-map","[vid]","-map","1:a",
               "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out]
    else:
        cmd = ["ffmpeg","-y",*inp,"-t",str(dur),"-filter_complex",fc,"-map","[vid]",
               "-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=240).returncode == 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--platform", default="insta", choices=["insta","tiktok"])
    ap.add_argument("--style", default="auto")
    ap.add_argument("--text", default="")
    ap.add_argument("--music", default="")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    if not os.path.isfile(a.src):
        print("FEHLER: Datei nicht gefunden:", a.src); sys.exit(2)
    style = "vivid" if a.style == "auto" else a.style
    stem, _ = os.path.splitext(a.src)
    if is_image(a.src):
        if a.platform == "tiktok":
            out = a.out or (stem + "_aufgepeppt.mp4")
            ok = image_to_video(a.src, out, a.text, a.music)
        else:
            out = a.out or (stem + "_aufgepeppt.jpg")
            ok = bool(pep_image(a.src, out, a.platform, style, a.text))
    elif is_video(a.src):
        out = a.out or (stem + "_aufgepeppt.mp4")
        ok = pep_video(a.src, out, style, a.text, a.music)
    else:
        print("FEHLER: Unbekannter Dateityp:", a.src); sys.exit(3)
    if ok and os.path.isfile(out):
        print("RESULT:" + out)
    else:
        print("FEHLER: Aufpeppen fehlgeschlagen."); sys.exit(1)

if __name__ == "__main__":
    main()
