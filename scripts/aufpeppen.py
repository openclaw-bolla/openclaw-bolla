#!/usr/bin/env python3
"""
Aufpeppen-Engine — macht aus einem Bild/Video einen Feel-Good-Post im Sinne von Chris' Profil
(„Feel-Good mit Augenzwinkern": sonnig, optimistisch, verspielt). Kostenlos: PIL + ffmpeg, kein API-€.

Aufruf:
    python3 aufpeppen.py <datei> [--platform insta|tiktok] [--style auto|natural|vivid|spectacular|cinematic|golden|punch]
                                 [--text "Hook/Slogan"] [--music <song.mp3>] [--out <zieldatei>]

BILD  -> Feel-Good-Grading (Wärme, Sättigung, Kontrast, Glow, Grain, Licht-Leak, Vignette),
         Format je Plattform (insta 4:5 = 1080x1350, sonst 1:1 = 1080x1080), optional Text-Overlay.
BILD als TikTok -> wird zu einem mehrschichtigen Hochformat-Reel: 3 "Kamera-Einstellungen" (verschiedene
         Ausschnitte/Zoomziele DESSELBEN Bilds) mit Speed-Ramp-Punch-in am Start, verbunden über knackige
         Schnitte (xfade: Zoom/Wipe/Flash) statt einem einzigen trägen Dauerzoom.
VIDEO -> Hochformat 1080x1920 (Crop-Fill + leichtes Kamera-Wackeln), sonniges/filmisches Grading,
         Grain + Licht-Leak, optional Musikbett + Musik-Wellen, optional 2-Beat-Caption.

--ai -> Opus (claude-opus-5) schaut sich das Bild/den Video-Frame an und schreibt ZWEI Text-Beats
        (Setup + witzige Pointe) + wählt automatisch den passenden Stil, statt generischer Standard-Filter.
        Greift automatisch, wenn --text leer ist bzw. --style auto ist.

Rückgabe: schreibt Zieldatei, druckt am Ende  RESULT:<pfad>
"""
import os, sys, re, json, subprocess, argparse, tempfile, shutil, hashlib

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

# Grading-Presets: (Sättigung, Kontrast, Helligkeit, Wärme-R, Wärme-B, Glow, Vignette,
#                    Grain, Licht-Leak, Kamera-Wackeln, Flash-Cuts, Teal-Orange)
IMG_PRESETS = {
    "natural":     dict(sat=1.10, con=1.05, bri=1.03, warm=1.03, cool=0.99, glow=0.12, vig=0.10,
                         grain=0.04, leak=0.00, shake=0.00, flash=0, teal_orange=False),
    "vivid":       dict(sat=1.16, con=1.12, bri=1.05, warm=1.03, cool=0.98, glow=0.20, vig=0.12,
                         grain=0.10, leak=0.08, shake=0.35, flash=1, teal_orange=False),
    "spectacular": dict(sat=1.26, con=1.18, bri=1.06, warm=1.05, cool=0.97, glow=0.24, vig=0.18,
                         grain=0.16, leak=0.18, shake=0.65, flash=1, teal_orange=False),
    "cinematic":   dict(sat=1.05, con=1.22, bri=1.00, warm=1.02, cool=1.05, glow=0.10, vig=0.24,
                         grain=0.14, leak=0.12, shake=0.25, flash=0, teal_orange=True),
    "golden":      dict(sat=1.22, con=1.08, bri=1.07, warm=1.18, cool=0.90, glow=0.30, vig=0.16,
                         grain=0.06, leak=0.38, shake=0.15, flash=0, teal_orange=False),
    "punch":       dict(sat=1.38, con=1.32, bri=1.02, warm=1.05, cool=0.96, glow=0.16, vig=0.20,
                         grain=0.14, leak=0.10, shake=0.70, flash=1, teal_orange=False),
}

def is_image(p): return p.lower().endswith(IMG_EXT)
def is_video(p): return p.lower().endswith(VID_EXT)

def pick_style(style):
    # Default 25.08.2026 (Chris' Wunsch): "cinematic" (kühle Schatten/warme Lichter, Teal-Orange-Split)
    # statt "vivid" (pauschaler Orange-Lichtleck-Stich über allem) -- vivid wirkte wie ein 2013er
    # Instagram-Filter, cinematic liest sich als aktueller Kino-/Trailer-Look.
    return IMG_PRESETS.get(style if style in IMG_PRESETS else "cinematic")

# ---------------- Opus-Regisseur (content-aware 2-Beat-Caption + Stil) ----------------
def extract_frame(video, out_jpg, at="00:00:01"):
    cmd = ["ffmpeg", "-y", "-ss", at, "-i", video, "-frames:v", "1", out_jpg]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=30).returncode == 0

def ai_direct(image_paths, platform):
    """Opus schaut sich 1-3 Bild(er) an und liefert (setup, punchline, style) — zwei kurze, content-
    bezogene Text-Beats statt einer einzigen generischen Zeile, plus Stilempfehlung aus allen Presets."""
    imgs = "\n".join(f"- {p}" for p in image_paths[:3])
    preset_hint = ("'natural' (dezent-echt), 'vivid' (knallig normal), 'spectacular' (maximaler Wow-Effekt), "
                   "'cinematic' (Kino-Look, Teal-Orange), 'golden' (warmes Golden-Hour-Licht), "
                   "'punch' (High-Energy, sehr knackiger Kontrast)")
    prompt = (
        "Du bist Bolla, Chris' KI-Assistent. Schau dir mit dem Read-Tool folgende(s) Bild(er) an:\n"
        f"{imgs}\n\n"
        "Chris' Marken-Ton (bollawave/Feel-Good-Profil): sonnig, optimistisch, verspielt, mit einem "
        "Augenzwinkern — NIE Kitsch-Klischee, NIE generisch.\n"
        f"Schreib dazu ZWEI kurze deutsche Text-Beats für ein "
        f"{'TikTok' if platform == 'tiktok' else 'Instagram'}-Reel, die sich KONKRET auf das beziehen, "
        "was auf dem Bild zu sehen ist:\n"
        "1. 'setup': kurzer Anspieler/Aufhänger (max. ca. 28 Zeichen)\n"
        "2. 'punchline': eine wirklich WITZIGE Pointe dazu, die zum Bildinhalt passt (max. ca. 32 Zeichen) "
        "— kein generisches Feel-Good-Blabla, sondern ein echter kleiner Lacher\n"
        "KEINE Hashtags, keine Anführungszeichen, höchstens 1 treffendes Emoji pro Zeile.\n"
        "Denk dir dafür zuerst 3 wirklich unterschiedliche Pointen-Ideen aus (Wortspiel, Understatement, "
        "überraschende Wendung o.ä. — kurz stichwortartig notieren), vergleich sie dann und such dir die "
        "schärfste aus. Eine schwache generische Idee zählt nicht als Option — lieber 3 Minuten länger "
        "nachdenken als eine brave Standard-Zeile abliefern.\n"
        f"Empfiehl außerdem den Bildstil je nach Stimmung: {preset_hint}.\n"
        "Schreib deine kurzen Stichwort-Ideen zuerst, dann als LETZTE Zeile NUR das finale JSON-Objekt "
        '(kein Codeblock): {"setup": "...", "punchline": "...", "style": '
        '"natural|vivid|spectacular|cinematic|golden|punch"}'
    )
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", "claude-opus-5"],
                            capture_output=True, text=True, timeout=120)
        m = re.search(r"\{.*\}", r.stdout.strip(), re.S)
        if m:
            d = json.loads(m.group(0))
            setup = (d.get("setup") or "").strip()
            punch = (d.get("punchline") or "").strip()
            style = d.get("style") if d.get("style") in IMG_PRESETS else "cinematic"
            return setup, punch, style
    except Exception:
        pass
    return "", "", "cinematic"

# ---------------- Gemeinsame Grading/Effekt-Bausteine (Bild + Video) ----------------
def focus_points(seed_key):
    """3 rule-of-thirds-artige Fokuspunkte, Reihenfolge variiert je Datei (kein CV, aber nicht immer
    dieselbe Kamerafahrt bei jedem Bild)."""
    pts = [(0.5, 0.45), (0.30, 0.55), (0.72, 0.38)]
    h = int(hashlib.md5(str(seed_key).encode()).hexdigest(), 16)
    rot = h % len(pts)
    return pts[rot:] + pts[:rot]

def grade_filter(p):
    """eq+colorbalance-Kette aus einem Preset — 'teal_orange' baut echten Kino-Split-Tone
    (Schatten kühl/türkis, Lichter warm/orange) statt nur globaler Wärme-Verschiebung."""
    eq = (f"eq=saturation={p['sat']:.2f}:contrast={p['con']:.2f}:"
          f"brightness={(p['bri']-1)*0.4:.3f}:gamma=1.02")
    if p.get("teal_orange"):
        cb = "colorbalance=rs=-0.10:bs=0.10:rm=0.02:bm=-0.02:rh=0.14:bh=-0.10"
    else:
        cb = f"colorbalance=rm={(p['warm']-1):.3f}:bm={(p['cool']-1):.3f}"
    return f"{eq},{cb}"

def grain_filter(p):
    g = p.get("grain", 0)
    if g <= 0:
        return None
    return f"noise=alls={int(g*38)}:allf=t+u"

def leak_filter_chain(w, h, p, tag_in, tag_out, dur, cx=0.85, cy=0.15, radius=0.55):
    """Warmer, prozedural erzeugter Licht-Leak (radialer Screen-Blend) — kein externes Asset nötig.
    WICHTIG 1: geq ist pro Pixel/Frame extrem teuer (ungefähr 400x langsamer als reguläre Filter).
    Der Gradient ändert sich nie mit der Zeit -> wird deshalb auf einem winzigen Raster (1/20
    Auflösung) berechnet und danach hochskaliert (bicubic liefert die weiche Kante gleich mit,
    kein Blur nötig).
    WICHTIG 2: nullsrc OHNE Dauer ist eine unendliche Quelle -> zusammen mit `blend` (framesync)
    gegen den echten, endlichen Videostream deadlockt ffmpeg dann komplett (0 Frames Output,
    hängt für immer statt zu terminieren, gemessen: >8 Minuten ohne einen einzigen Frame).
    Deshalb IMMER `d=<dur>` an nullsrc übergeben, exakt passend zur Segment-/Clip-Länge."""
    amount = p.get("leak", 0)
    if amount <= 0:
        return "", tag_in
    lw, lh = max(8, w // 20), max(8, h // 20)
    src_tag = f"{tag_out}_lksrc"
    up_tag = f"{tag_out}_lkup"
    src = (f"nullsrc=s={lw}x{lh}:r=30:d={dur:.3f},format=rgb24,"
           f"geq=r='255':"
           f"g='190*(1-min(1\\,hypot(X-{lw}*{cx}\\,Y-{lh}*{cy})/({lw}*{radius})))':"
           f"b='90*(1-min(1\\,hypot(X-{lw}*{cx}\\,Y-{lh}*{cy})/({lw}*{radius})))'[{src_tag}];"
           f"[{src_tag}]scale={w}:{h}:flags=bicubic[{up_tag}]")
    blend = f"[{tag_in}][{up_tag}]blend=all_mode=screen:all_opacity={amount:.2f}[{tag_out}]"
    return src + ";" + blend, tag_out

def base_scale_crop(w, h, shake_amt=0.0):
    """Vollflächiger Crop+Zoom (füllt IMMER den ganzen Screen). Bei shake_amt>0 zusätzlich
    minimales oszillierendes x/y-Jitter (dezentes Kamera-Wackeln, 'handheld'-Gefühl)."""
    if shake_amt and shake_amt > 0:
        pad = 1.0 + 0.05 * min(1.0, shake_amt)
        sw, sh = int(round(w*pad/2))*2, int(round(h*pad/2))*2
        ax, ay = (sw-w)/2.0, (sh-h)/2.0
        return (f"scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},"
                f"crop=w={w}:h={h}:x='{ax:.1f}+{ax:.1f}*sin(2*PI*2.8*t)':"
                f"y='{ay*0.6:.1f}+{ay*0.6:.1f}*cos(2*PI*2.3*t)'")
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"

def build_visual_chain(fc_parts, w, h, p, cur_tag, dur, use_shake=True):
    """Hängt scale/crop(+Wackeln)+Grading+Grain+Licht-Leak an fc_parts an, gibt das neue Stream-Label
    zurück. Gemeinsamer Baustein für alle Video-Pfade (Einzelfoto-Shots, Einzelvideo, Montage-Segmente).
    `dur` = Segment-/Clip-Länge in Sekunden, nötig für den Licht-Leak (siehe leak_filter_chain)."""
    base = base_scale_crop(w, h, p.get("shake", 0.0) if use_shake else 0.0)
    grade = grade_filter(p)
    nxt = f"{cur_tag}_g"
    fc_parts.append(f"[{cur_tag}]{base},{grade}[{nxt}]")
    cur_tag = nxt
    grain = grain_filter(p)
    if grain:
        nxt = f"{cur_tag}_n"
        fc_parts.append(f"[{cur_tag}]{grain}[{nxt}]")
        cur_tag = nxt
    leak_chain, nxt2 = leak_filter_chain(w, h, p, cur_tag, f"{cur_tag}_lk", dur)
    if leak_chain:
        fc_parts.append(leak_chain)
        cur_tag = nxt2
    return cur_tag

# ---------------- Übergänge (Schnitte statt Diashow) ----------------
TRANSITIONS_BASE = ["zoomin", "circleopen", "wipeleft", "slideup", "smoothleft", "wiperight"]
TRANSITIONS_FLASH = ["fadewhite", "zoomin", "circleopen", "fadewhite", "wipeleft", "smoothleft", "wiperight"]

def transitions_for(p):
    """Presets mit 'flash' mischen Weißblitz-Schnitte (ffmpeg-xfade 'fadewhite') in die Rotation —
    fühlt sich nach echtem Energie-Edit an statt gleichförmigem Crossfade."""
    return TRANSITIONS_FLASH if p.get("flash") else TRANSITIONS_BASE

def chain_xfade(segments, out_video, clip_dur, xfade_dur, transitions):
    """Verkettet gleich lange Segmente mit variierenden xfade-Übergängen. Gibt (ok, gesamtdauer) zurück."""
    n = len(segments)
    if n == 1:
        shutil.copy2(segments[0], out_video)
        return True, clip_dur
    inputs = []
    for s in segments:
        inputs += ["-i", s]
    filters = []
    cur = "0:v"
    running = clip_dur
    for i in range(1, n):
        tag = f"v{i}"
        offset = running - xfade_dur
        trans = transitions[(i - 1) % len(transitions)]
        filters.append(f"[{cur}][{i}:v]xfade=transition={trans}:duration={xfade_dur}:offset={offset:.2f}[{tag}]")
        cur = tag
        running += clip_dur - xfade_dur
    fc = ";".join(filters)
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", f"[{cur}]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", out_video]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, running

# ---------------- Segment-Bausteine (1 "Shot") ----------------
def image_shot_segment(src, out, w, h, dur, p, focus, zoom_from, zoom_to, speed_ramp, fps=30):
    """EIN Standbild-Shot: Crop+Grading+Grain+Leak, dann Ken-Burns-Zoom Richtung Fokuspunkt.
    speed_ramp=True -> schneller Punch-Zoom in den ersten ~0.35s, danach gemächlich."""
    frames = int(dur * fps)
    fc_parts = []
    cur = build_visual_chain(fc_parts, w, h, p, "0:v", dur, use_shake=False)
    fx, fy = focus
    if speed_ramp:
        ramp_frames = max(4, int(fps * 0.35))
        ramp_end = zoom_from + (zoom_to - zoom_from) * 0.55
        z_expr = (f"if(lte(on,{ramp_frames}),{zoom_from}+({ramp_end-zoom_from}/{ramp_frames})*on,"
                  f"{ramp_end}+({zoom_to-ramp_end}/{max(1,frames-ramp_frames)})*(on-{ramp_frames}))")
    else:
        z_expr = f"{zoom_from}+({zoom_to-zoom_from}/{frames})*on"
    x_expr = f"(iw-iw/zoom)*{fx}"
    y_expr = f"(ih-ih/zoom)*{fy}"
    zoom_tag = f"{cur}_z"
    fc_parts.append(f"[{cur}]zoompan=z='{z_expr}':x='{x_expr}':y='{y_expr}':d={frames}:s={w}x{h}:fps={fps}[{zoom_tag}]")
    fc = ";".join(fc_parts)
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", src, "-t", str(dur), "-filter_complex", fc,
           "-map", f"[{zoom_tag}]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), "-an", out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=90).returncode == 0

def video_clip_segment(src, out, w, h, dur, p, fps=30):
    """EIN Video-Shot (aus einer echten Videodatei): Crop+Wackeln+Grading+Grain+Leak, kein Zoompan."""
    fc_parts = []
    cur = build_visual_chain(fc_parts, w, h, p, "0:v", dur, use_shake=True)
    fc = ";".join(fc_parts)
    cmd = ["ffmpeg", "-y", "-i", src, "-t", str(dur), "-filter_complex", fc,
           "-map", f"[{cur}]", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120).returncode == 0

# ---------------- 2-Beat-Captions ----------------
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

def caption_beat_clause(text, start, dur, y, fontsize=58):
    """EIN Caption-Beat: Pop-in (Alpha-Fade + leichter Y-Ease-Bounce) am Anfang, sanftes Ausblenden
    am Ende des Zeitfensters — statt stumpf-statischem Text die ganze Laufzeit.
    Zeilenumbruch skaliert mit fontsize (an fontsize=58 kalibriert), sonst laufen große Schriften
    (Chris' Wunsch 25.08.: Sprüche größer/auffälliger) rechts aus dem 1080px-Frame."""
    max_chars = max(10, round(30 * 58 / fontsize))
    safe = for_drawtext(text, max_chars=max_chars).replace(":", "\\:").replace("'", "’")
    fp = caption_font_path()
    fontfile = f"fontfile='{fp}':" if fp else ""
    end = start + dur
    pop, ease, fadeout = 0.18, 0.30, 0.18
    alpha = (f"if(lt(t-{start:.2f},{pop}),(t-{start:.2f})/{pop},"
             f"if(gt(t,{end-fadeout:.2f}),max(0,({end:.2f}-t)/{fadeout}),1))")
    y_expr = f"{y}+48*max(0,1-(t-{start:.2f})/{ease})"
    return (f"drawtext={fontfile}text='{safe}':fontcolor=white:fontsize={fontsize}:"
            f"borderw=7:bordercolor=black:shadowx=3:shadowy=3:shadowcolor=black@0.6:"
            f"box=1:boxcolor=black@0.42:boxborderw=20:"
            f"x=(w-text_w)/2:y='{y_expr}':line_spacing=10:"
            f"enable='between(t,{start:.2f},{end:.2f})':alpha='{alpha}'")

def build_caption_clauses(beats, y="h-360", fontsize=58):
    return ",".join(caption_beat_clause(t, s, d, y, fontsize) for (t, s, d) in beats)

def build_beats(text, ai_beats, total_dur):
    """Baut die Zeitfenster-Liste [(text, start, dauer), ...]. Manueller --text -> ein Beat über
    fast die ganze Laufzeit (altes Verhalten). Opus-Beats (setup, punchline) -> zwei Beats nacheinander."""
    if ai_beats and (ai_beats[0] or ai_beats[1]):
        setup, punch = ai_beats
        half = total_dur / 2.0
        beats = []
        if setup:
            beats.append((setup, 0.05, max(0.6, half - 0.15)))
        if punch:
            start = half + 0.05 if setup else 0.05
            beats.append((punch, start, max(0.6, total_dur - start - 0.15)))
        return beats
    if text:
        return [(text, 0.2, max(0.6, min(total_dur - 0.3, total_dur * 0.8)))]
    return []

def finalize_with_captions_and_music(video_in, out, beats, music, total_dur, y="h-360", fontsize=58):
    """Legt Caption-Beats + optionales Musikbett (mit Fades) über ein bereits fertig geschnittenes Video."""
    draw = build_caption_clauses(beats, y=y, fontsize=fontsize) if beats else ""
    if music and os.path.isfile(music):
        # Fester 25s-Einstieg ins Musikstück (überspringt oft ein leises Intro) -- aber NUR wenn der Song
        # tatsächlich so lang ist. Sonst seekt ffmpeg hinters Dateiende -> 0 Audio-Samples -> zusammen mit
        # -shortest wird das GESAMTE Video auf ~0s gekappt (Ursache für einen "korrupten", nicht abspielbaren
        # Export bei kurzen Songs -- gefunden 24.08.2026 am echten Multi-Foto-Reel).
        music_dur = video_duration(music) or 0
        safe_margin = 1.0
        start = 25.0 if music_dur >= 25.0 + total_dur + safe_margin else max(0.0, music_dur - total_dur - safe_margin)
        vf = draw if draw else "null"
        fc = (f"[0:v]{vf}[vid];"
              f"[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st={max(0, total_dur - 0.8):.2f}:d=0.8[aud]")
        cmd = ["ffmpeg", "-y", "-i", video_in, "-ss", f"{start:.2f}", "-t", str(total_dur), "-i", music,
               "-filter_complex", fc, "-map", "[vid]", "-map", "[aud]",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
               "-movflags", "+faststart", "-shortest", out]
    else:
        if draw:
            cmd = ["ffmpeg", "-y", "-i", video_in, "-vf", draw,
                   "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
        else:
            cmd = ["ffmpeg", "-y", "-i", video_in, "-c", "copy", "-movflags", "+faststart", out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180).returncode == 0

def video_duration(path):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                             "-of", "default=noprint_wrappers=1:nokey=1", path],
                            capture_output=True, text=True, timeout=15)
        return float(r.stdout.strip())
    except Exception:
        return None

# ---------------- BILD (Insta, statisches JPG) ----------------
def apply_grain(im, amount):
    if amount <= 0:
        return im
    import numpy as np
    from PIL import Image
    arr = np.asarray(im).astype(np.int16)
    noise = np.random.randint(-int(amount * 40), int(amount * 40) + 1, arr.shape[:2], dtype=np.int16)
    arr = np.clip(arr + noise[:, :, None], 0, 255).astype("uint8")
    return Image.fromarray(arr)

def apply_light_leak(im, amount, cx=0.85, cy=0.15, radius_frac=0.55):
    if amount <= 0:
        return im
    import numpy as np
    from PIL import Image, ImageChops
    w, h = im.size
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot(xx - w * cx, yy - h * cy) / (w * radius_frac)
    falloff = np.clip(1 - d, 0, 1)
    leak = np.zeros((h, w, 3), dtype="uint8")
    leak[..., 0] = (255 * falloff).astype("uint8")
    leak[..., 1] = (190 * falloff).astype("uint8")
    leak[..., 2] = (90 * falloff).astype("uint8")
    screened = ImageChops.screen(im, Image.fromarray(leak, "RGB"))
    return Image.blend(im, screened, amount)

def pep_image(src, out, platform, style, text):
    from PIL import Image, ImageEnhance, ImageFilter, ImageChops
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

    # Licht-Leak + Grain (vor der Vignette, wie bei einem echten Film-Look)
    if p.get("leak", 0) > 0:
        im = apply_light_leak(im, p["leak"])
    if p.get("grain", 0) > 0:
        im = apply_grain(im, p["grain"])

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
def pep_video(src, out, style, text, music, ai_beats=None):
    p = pick_style(style)
    total_dur = video_duration(src) or 6.0
    fc_parts = []
    # Echtes Videomaterial hat schon eigene Kamerabewegung -> kein synthetisches Wackeln obendrauf
    # (das machte reale Handyclips nur noch zittriger, siehe Chris-Feedback 24.08.2026 Regenbogen-Video).
    cur = build_visual_chain(fc_parts, 1080, 1920, p, "0:v", total_dur, use_shake=False)
    beats = build_beats(text, ai_beats, total_dur)
    if beats:
        nxt = f"{cur}_t"
        fc_parts.append(f"[{cur}]{build_caption_clauses(beats)}[{nxt}]")
        cur = nxt
    if music and os.path.isfile(music):
        fc_parts.append("[1:a]showwaves=s=1080x200:mode=cline:rate=30:colors=0xFFFFFF|0xFFD447[w]")
        fc_parts.append(f"[{cur}][w]overlay=0:H-260:format=auto[vidf]")
        fc = ";".join(fc_parts)
        cmd = ["ffmpeg","-y","-i",src,"-i",music,"-filter_complex",fc,
               "-map","[vidf]","-map","1:a","-c:v","libx264","-pix_fmt","yuv420p",
               "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out]
    else:
        fc = ";".join(fc_parts)
        cmd = ["ffmpeg","-y","-i",src,"-filter_complex",fc,"-map",f"[{cur}]",
               "-map","0:a?","-c:v","libx264","-pix_fmt","yuv420p",
               "-c:a","aac","-b:a","192k","-movflags","+faststart",out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=300).returncode == 0

def image_to_video(src, out, text, music, dur=6, ai_beats=None, style="cinematic"):
    """Einzelfoto -> mehrschichtiges Hochformat-Reel: 3 'Kamera-Einstellungen' (verschiedene
    Ausschnitte/Zoomziele desselben Bilds) mit Speed-Ramp-Punch-in am Start, verbunden über knackige
    Schnitte (xfade) statt einem einzigen trägen Dauerzoom."""
    p = pick_style(style)
    n_shots = 3
    xfade = min(0.35, max(0.2, dur / n_shots * 0.18))
    shot_dur = (dur + (n_shots - 1) * xfade) / n_shots
    focuses = focus_points(src)
    zoom_plan = [(1.00, 1.11), (1.06, 1.24), (1.16, 1.34)]
    with tempfile.TemporaryDirectory() as td:
        segs = []
        for i in range(n_shots):
            seg = os.path.join(td, f"shot{i}.mp4")
            zf, zt = zoom_plan[i % len(zoom_plan)]
            if image_shot_segment(src, seg, 1080, 1920, shot_dur, p, focuses[i % len(focuses)],
                                   zf, zt, speed_ramp=(i == 0)):
                segs.append(seg)
        if not segs:
            return False
        chained = os.path.join(td, "chained.mp4")
        ok, total_dur = chain_xfade(segs, chained, shot_dur, xfade, transitions_for(p))
        if not ok:
            return False
        beats = build_beats(text, ai_beats, total_dur)
        return finalize_with_captions_and_music(chained, out, beats, music, total_dur)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--platform", default="insta", choices=["insta","tiktok"])
    ap.add_argument("--style", default="auto")
    ap.add_argument("--text", default="")
    ap.add_argument("--music", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--ai", action="store_true", help="Opus schreibt content-bezogene 2-Beat-Caption + wählt Stil")
    a = ap.parse_args()
    if not os.path.isfile(a.src):
        print("FEHLER: Datei nicht gefunden:", a.src); sys.exit(2)
    ai_beats = None
    if a.ai and not a.text:
        frame_src = a.src
        tmp_frame = None
        if is_video(a.src):
            tmp_frame = a.src + ".ai_frame.jpg"
            if extract_frame(a.src, tmp_frame):
                frame_src = tmp_frame
        setup, punch, ai_style = ai_direct([frame_src], a.platform)
        if setup or punch:
            ai_beats = (setup, punch)
        if a.style == "auto":
            a.style = ai_style
        if tmp_frame and os.path.isfile(tmp_frame):
            os.remove(tmp_frame)
    style = "cinematic" if a.style == "auto" else a.style
    stem, _ = os.path.splitext(a.src)
    if is_image(a.src):
        if a.platform == "tiktok":
            out = a.out or (stem + "_aufgepeppt.mp4")
            ok = image_to_video(a.src, out, a.text, a.music, ai_beats=ai_beats, style=style)
        else:
            out = a.out or (stem + "_aufgepeppt.jpg")
            combo_text = a.text or (" ".join(x for x in ai_beats if x) if ai_beats else "")
            ok = bool(pep_image(a.src, out, a.platform, style, combo_text))
    elif is_video(a.src):
        out = a.out or (stem + "_aufgepeppt.mp4")
        ok = pep_video(a.src, out, style, a.text, a.music, ai_beats=ai_beats)
    else:
        print("FEHLER: Unbekannter Dateityp:", a.src); sys.exit(3)
    if ok and os.path.isfile(out):
        print("RESULT:" + out)
    else:
        print("FEHLER: Aufpeppen fehlgeschlagen."); sys.exit(1)

if __name__ == "__main__":
    main()
