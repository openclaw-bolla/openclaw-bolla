#!/usr/bin/env python3
"""
Aufpeppen-Montage — baut aus MEHREREN Fotos/Videos EIN spektakuläres TikTok-Reel
(Übergänge inkl. Flash-Cuts, Grain/Licht-Leak, Musikbett, Fable-2-Beat-Caption) statt vieler
einzelner Klein-Clips. Ergänzt aufpeppen.py (Einzeldatei) — für Chris' "mehrere Fotos/Videos
auf einmal einkippen". Nutzt dieselben Grading-/Übergangs-/Caption-Bausteine wie aufpeppen.py.

Aufruf:
    python3 aufpeppen_montage.py <datei1> <datei2> ... --out <ziel.mp4>
                                  [--music <song.mp3>] [--style auto|natural|vivid|spectacular|cinematic|golden|punch]
                                  [--hook "Text"] [--max 8]

Rückgabe: schreibt Zieldatei, druckt am Ende  RESULT:<pfad>
"""
import os, sys, subprocess, argparse, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aufpeppen as ap

W, H = 1080, 1920
CLIP_DUR = 3.0
XFADE = 0.35

IMG_EXT = ap.IMG_EXT
VID_EXT = ap.VID_EXT
SONG_ARCHIVE = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid"


def latest_song_mp3():
    try:
        mp3s = [os.path.join(SONG_ARCHIVE, f) for f in os.listdir(SONG_ARCHIVE) if f.lower().endswith(".mp3")]
        return max(mp3s, key=os.path.getmtime) if mp3s else None
    except Exception:
        return None


def build_montage(files, out, music=None, style="auto", hook=None, max_clips=8):
    files = [f for f in files if os.path.isfile(f)][:max_clips]
    if not files:
        return False, "Keine gültigen Dateien."

    # Stil + 2-Beat-Caption per Fable (schaut sich das erste Bild bzw. einen Video-Frame an),
    # falls nicht vorgegeben. Ein manuelles --hook bleibt als Einzel-Text-Beat (Rückwärtskompatibilität).
    ai_setup, ai_punch = "", ""
    if hook is None or style == "auto":
        frame_src = files[0]
        tmp_frame = None
        if frame_src.lower().endswith(VID_EXT):
            tmp_frame = frame_src + ".ai_frame.jpg"
            if not ap.extract_frame(frame_src, tmp_frame):
                tmp_frame = None
            else:
                frame_src = tmp_frame
        ai_setup, ai_punch, ai_style = ap.ai_direct([frame_src], "tiktok")
        if style == "auto":
            style = ai_style
        if tmp_frame and os.path.isfile(tmp_frame):
            os.remove(tmp_frame)
    p = ap.pick_style(style)

    with tempfile.TemporaryDirectory() as td:
        segs = []
        for i, f in enumerate(files):
            is_img = f.lower().endswith(IMG_EXT)
            seg = os.path.join(td, f"seg{i:02d}.mp4")
            # Erstes Segment bekommt den Speed-Ramp-Punch-in -> knackiger Einstieg ins ganze Reel.
            ok = (ap.image_shot_segment(f, seg, W, H, CLIP_DUR, p, (0.5, 0.5), 1.0, 1.18, i == 0)
                  if is_img else ap.video_clip_segment(f, seg, W, H, CLIP_DUR, p))
            if ok:
                segs.append(seg)
        if not segs:
            return False, "Segmenterstellung fehlgeschlagen."

        chained = os.path.join(td, "chained.mp4")
        ok, total_dur = ap.chain_xfade(segs, chained, CLIP_DUR, XFADE, ap.transitions_for(p))
        if not ok:
            return False, "Crossfade-Verkettung fehlgeschlagen."

        if music is None:
            music = latest_song_mp3()  # nicht angegeben (Watcher/CLI-Default) -> automatisch neuesten Song nehmen
        elif music == "none":
            music = None  # explizit abgewählt (mmp-Checkbox aus) -> NICHT automatisch ersetzen
        beats = ap.build_beats(hook, None if hook is not None else (ai_setup, ai_punch), total_dur)
        ok = ap.finalize_with_captions_and_music(chained, out, beats, music, total_dur, y=180, fontsize=64)
        if not ok or not os.path.isfile(out):
            return False, "Finalisierung (Musik/Text) fehlgeschlagen."
    info = hook if hook is not None else " / ".join(x for x in (ai_setup, ai_punch) if x)
    return True, info


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
