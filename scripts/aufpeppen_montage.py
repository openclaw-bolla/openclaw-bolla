#!/usr/bin/env python3
"""
Aufpeppen-Montage — baut aus MEHREREN Fotos/Videos EIN spektakuläres TikTok-Reel
(Crossfade-Übergänge, Musikbett, Fable-Hook-Text) statt vieler einzelner Klein-Clips.
Ergänzt aufpeppen.py (Einzeldatei) — für Chris' "mehrere Fotos/Videos auf einmal einkippen".

Aufruf:
    python3 aufpeppen_montage.py <datei1> <datei2> ... --out <ziel.mp4>
                                  [--music <song.mp3>] [--style auto|natural|vivid|spectacular]
                                  [--hook "Text"] [--max 8]

Rückgabe: schreibt Zieldatei, druckt am Ende  RESULT:<pfad>
"""
import os, sys, subprocess, argparse, tempfile, shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aufpeppen as ap

W, H = 1080, 1920
CLIP_DUR = 3.0
XFADE = 0.35
# kurze, knackige Cuts statt immer nur "fade" -> fühlt sich nach echtem Edit an, nicht nach Diashow.
TRANSITIONS = ["zoomin", "circleopen", "wipeleft", "slideup", "smoothleft", "wiperight"]

IMG_EXT = ap.IMG_EXT
VID_EXT = ap.VID_EXT
SONG_ARCHIVE = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid"


def latest_song_mp3():
    try:
        mp3s = [os.path.join(SONG_ARCHIVE, f) for f in os.listdir(SONG_ARCHIVE) if f.lower().endswith(".mp3")]
        return max(mp3s, key=os.path.getmtime) if mp3s else None
    except Exception:
        return None


def make_segment(src, out, is_img, style):
    p = ap.pick_style(style)
    grade = (f"eq=saturation={p['sat']:.2f}:contrast={p['con']:.2f}:brightness={(p['bri']-1)*0.4:.3f}:gamma=1.02,"
             f"colorbalance=rm=0.06:bm=-0.05")
    if is_img:
        frames = int(CLIP_DUR * 30)
        # vollflächiger Crop+Zoom statt Blur-Rand mit kleinem zentriertem Bild -> füllt den Screen wie TikTok.
        base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{grade}"
        fc = (f"[0:v]{base}[base];"
              f"[base]zoompan=z='min(zoom+0.0014,1.22)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
              f"d={frames}:s={W}x{H}:fps=30[vid]")
        cmd = ["ffmpeg", "-y", "-loop", "1", "-i", src, "-t", str(CLIP_DUR), "-filter_complex", fc,
               "-map", "[vid]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-an", out]
    else:
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},{grade}"
        cmd = ["ffmpeg", "-y", "-i", src, "-t", str(CLIP_DUR), "-vf", vf,
               "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", out]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120).returncode == 0


def chain_xfade(segments, out_video):
    """Verkettet Segmente gleicher Länge mit Crossfade-Übergängen. Gibt (ok, gesamtdauer) zurück."""
    n = len(segments)
    if n == 1:
        shutil.copy2(segments[0], out_video)
        return True, CLIP_DUR
    inputs = []
    for s in segments:
        inputs += ["-i", s]
    filters = []
    cur = "0:v"
    running = CLIP_DUR
    for i in range(1, n):
        tag = f"v{i}"
        offset = running - XFADE
        trans = TRANSITIONS[(i - 1) % len(TRANSITIONS)]
        filters.append(f"[{cur}][{i}:v]xfade=transition={trans}:duration={XFADE}:offset={offset:.2f}[{tag}]")
        cur = tag
        running += CLIP_DUR - XFADE
    fc = ";".join(filters)
    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", fc, "-map", f"[{cur}]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", out_video]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode == 0, running


def finalize(video_in, out, hook, music, total_dur):
    """Fable-Hook (erste ~3s) + Musikbett mit Fade drüberlegen."""
    draw = ""
    if hook:
        safe = ap.for_drawtext(hook).replace(":", "\\:").replace("'", "’")
        clause = ap.drawtext_clause(safe, y=180, fontsize=64)
        draw = clause + ":enable='between(t\\,0\\,3.2)'"
    if music and os.path.isfile(music):
        vf = draw if draw else "null"
        fc = (f"[0:v]{vf}[vid];"
              f"[1:a]afade=t=in:st=0:d=0.5,afade=t=out:st={max(0, total_dur - 0.8):.2f}:d=0.8[aud]")
        cmd = ["ffmpeg", "-y", "-i", video_in, "-ss", "25", "-t", str(total_dur), "-i", music,
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


def build_montage(files, out, music=None, style="auto", hook=None, max_clips=8):
    files = [f for f in files if os.path.isfile(f)][:max_clips]
    if not files:
        return False, "Keine gültigen Dateien."

    # Stil + Hook per Fable (schaut sich das erste Bild bzw. einen Video-Frame an), falls nicht vorgegeben
    tmp_frame = None
    if hook is None or style == "auto":
        frame_src = files[0]
        if frame_src.lower().endswith(VID_EXT):
            tmp_frame = frame_src + ".ai_frame.jpg"
            if not ap.extract_frame(frame_src, tmp_frame):
                tmp_frame = None
            else:
                frame_src = tmp_frame
        ai_hook, ai_style = ap.ai_direct([frame_src], "tiktok")
        if hook is None:
            hook = ai_hook
        if style == "auto":
            style = ai_style
        if tmp_frame and os.path.isfile(tmp_frame):
            os.remove(tmp_frame)

    with tempfile.TemporaryDirectory() as td:
        segs = []
        for i, f in enumerate(files):
            is_img = f.lower().endswith(IMG_EXT)
            seg = os.path.join(td, f"seg{i:02d}.mp4")
            if make_segment(f, seg, is_img, style):
                segs.append(seg)
        if not segs:
            return False, "Segmenterstellung fehlgeschlagen."

        chained = os.path.join(td, "chained.mp4")
        ok, total_dur = chain_xfade(segs, chained)
        if not ok:
            return False, "Crossfade-Verkettung fehlgeschlagen."

        if not music:
            music = latest_song_mp3()
        ok = finalize(chained, out, hook, music, total_dur)
        if not ok or not os.path.isfile(out):
            return False, "Finalisierung (Musik/Text) fehlgeschlagen."
    return True, hook


def main():
    ap_arg = argparse.ArgumentParser()
    ap_arg.add_argument("files", nargs="+")
    ap_arg.add_argument("--out", required=True)
    ap_arg.add_argument("--music", default="")
    ap_arg.add_argument("--style", default="auto")
    ap_arg.add_argument("--hook", default=None)
    ap_arg.add_argument("--max", type=int, default=8)
    a = ap_arg.parse_args()

    ok, info = build_montage(a.files, a.out, music=(a.music or None), style=a.style,
                              hook=a.hook, max_clips=a.max)
    if ok:
        print("HOOK:" + (info or ""))
        print("RESULT:" + a.out)
    else:
        print("FEHLER:", info)
        sys.exit(1)


if __name__ == "__main__":
    main()
