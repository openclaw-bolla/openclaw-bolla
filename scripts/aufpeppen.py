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

--ai -> Fable (claude-fable-5) schaut sich das Bild/Frame an und schreibt einen content-bezogenen
        Hook-Text + wählt den passenden Stil, statt generischer Standard-Filter (fixt "langweilig").
        Greift nur, wenn --text leer ist bzw. --style auto ist.

Rückgabe: schreibt Zieldatei, druckt am Ende  RESULT:<pfad>
"""
import os, sys, re, json, subprocess, argparse

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic")
VID_EXT = (".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm")

# Meme/TikTok-Caption-Look: fette, laute Schrift statt braver DejaVu-Standardschrift.
CAPTION_FONTS = [
    "/mnt/c/Windows/Fonts/impact.ttf",
    "/mnt/c/Windows/Fonts/ariblk.ttf",
    "/mnt/c/Windows/Fonts/arialbd.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def caption_font_path():
    for fp in CAPTION_FONTS:
        if os.path.isfile(fp):
            return fp
    return None

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

# ---------------- Fable-Regisseur (content-aware Hook + Stil) ----------------
def extract_frame(video, out_jpg, at="00:00:01"):
    cmd = ["ffmpeg", "-y", "-ss", at, "-i", video, "-frames:v", "1", out_jpg]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=30).returncode == 0

def ai_direct(image_paths, platform):
    """Fable schaut sich 1-3 Bild(er) an und liefert (hook_text, style) — content-bezogen statt generisch."""
    imgs = "\n".join(f"- {p}" for p in image_paths[:3])
    prompt = (
        "Du bist Bolla, Chris' KI-Assistent. Schau dir mit dem Read-Tool folgende(s) Bild(er) an:\n"
        f"{imgs}\n\n"
        "Chris' Marken-Ton (bollawave/Feel-Good-Profil): sonnig, optimistisch, verspielt, mit einem "
        "Augenzwinkern — NIE Kitsch-Klischee, NIE generisch.\n"
        f"Schreib dazu einen KURZEN knackigen deutschen Hook-Text für "
        f"{'TikTok' if platform == 'tiktok' else 'Instagram'}, der sich konkret auf das bezieht, was auf "
        "dem Bild zu sehen ist (max. 2 kurze Zeilen, zusammen max. ca. 55 Zeichen, gern 1 treffendes Emoji, "
        "KEINE Hashtags, keine Anführungszeichen).\n"
        "Empfiehl außerdem den Bildstil je nach Stimmung: 'natural' (dezent-echt), 'vivid' (knallig normal) "
        "oder 'spectacular' (maximaler Wow-Effekt).\n"
        'Antworte NUR mit einem JSON-Objekt in einer Zeile, kein Codeblock, keine Erklärung: '
        '{"hook": "...", "style": "natural|vivid|spectacular"}'
    )
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", "claude-fable-5"],
                            capture_output=True, text=True, timeout=120)
        m = re.search(r"\{.*\}", r.stdout.strip(), re.S)
        if m:
            d = json.loads(m.group(0))
            hook = (d.get("hook") or "").strip()
            style = d.get("style") if d.get("style") in IMG_PRESETS else "vivid"
            return hook, style
    except Exception:
        pass
    return "", "vivid"

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
    text = re.sub(r"\s{2,}", " ", EMOJI_RE.sub("", text)).strip().upper()
    w, h = im.size
    d = ImageDraw.Draw(im)
    size = int(w / 12)
    font = None
    for fp in CAPTION_FONTS:
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
    return lines[:4]

# ---------------- VIDEO ----------------
EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF"
    "\U00002190-\U000021FF\U00002B00-\U00002BFF️]+")

def for_drawtext(text, max_chars=30, max_lines=3):
    """Emoji raus (ffmpeg-Font kann sie eh nicht rendern), GROSSSCHRIFT (Meme-Caption-Look) +
    Zeilenumbruch. Bricht bei echtem Überlauf mit „…" statt Wörter kommentarlos zu verschlucken."""
    clean = re.sub(r"\s{2,}", " ", EMOJI_RE.sub("", text)).strip().upper()
    words, lines, cur = clean.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if len(t) <= max_chars:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".,!?") + " …"
    return "\n".join(lines)

def drawtext_clause(safe_text, y, fontsize=58, pop_in=True):
    """Baut die drawtext-Filterklausel: feste Caption-Schriftart + kurzer Pop-in-Fade statt
    stumpf-statischem Text die ganze Laufzeit."""
    fp = caption_font_path()
    fontfile = f"fontfile='{fp}':" if fp else ""
    alpha = ":alpha='if(lt(t,0.35),t/0.35,1)'" if pop_in else ""
    return (f"drawtext={fontfile}text='{safe_text}':fontcolor=0xFFF096:fontsize={fontsize}:"
            f"borderw=4:bordercolor=black:x=(w-text_w)/2:y={y}:box=0:line_spacing=10{alpha}")


def pep_video(src, out, style, text, music):
    p = pick_style(style if style in IMG_PRESETS else "vivid")
    # sonniges Grading via eq + colorbalance
    grade = (f"eq=saturation={p['sat']:.2f}:contrast={p['con']:.2f}:brightness={(p['bri']-1)*0.4:.3f}:gamma=1.02,"
             f"colorbalance=rm=0.06:bm=-0.05")
    base = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            + grade)
    draw = ""
    if text:
        safe = for_drawtext(text).replace(":", "\\:").replace("'", "’")
        draw = (f",{drawtext_clause(safe, y='h-360', fontsize=58)}")
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
    """Standbild -> Ken-Burns-Hochformat-Video (für TikTok aus einem Foto).
    Vollflächiger Crop+Zoom (wie TikTok/Reels), KEIN verschwommener Rand mit kleinem
    zentriertem Bild mehr — Querformat wird direkt hochkant beschnitten und füllt den Screen."""
    frames = dur*30
    grade = "eq=saturation=1.25:contrast=1.1:brightness=0.02,colorbalance=rm=0.06:bm=-0.05"
    draw = ""
    if text:
        safe = for_drawtext(text).replace(":", "\\:").replace("'", "’")
        draw = f",{drawtext_clause(safe, y='h-360', fontsize=58)}"
    # erst voll auf 9:16 zuschneiden (füllt IMMER den ganzen Screen, egal ob Quer- oder Hochformat-Quelle),
    # dann in dieses bereits randfüllende Bild langsam reinzoomen -> "lebendiges Foto" statt Blur-Rand.
    base = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,{grade}"
    fc = (f"[0:v]{base}[base];"
          f"[base]zoompan=z='min(zoom+0.0012,1.28)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
          f"d={frames}:s=1080x1920:fps=30{draw}[vid]")
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
    ap.add_argument("--ai", action="store_true", help="Fable schreibt content-bezogenen Hook + wählt Stil")
    a = ap.parse_args()
    if not os.path.isfile(a.src):
        print("FEHLER: Datei nicht gefunden:", a.src); sys.exit(2)
    if a.ai and not a.text:
        frame_src = a.src
        tmp_frame = None
        if is_video(a.src):
            tmp_frame = a.src + ".ai_frame.jpg"
            if extract_frame(a.src, tmp_frame):
                frame_src = tmp_frame
        ai_hook, ai_style = ai_direct([frame_src], a.platform)
        if ai_hook:
            a.text = ai_hook
        if a.style == "auto":
            a.style = ai_style
        if tmp_frame and os.path.isfile(tmp_frame):
            os.remove(tmp_frame)
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
