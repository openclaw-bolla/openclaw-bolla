#!/usr/bin/env python3
"""
Aufpeppen-Wächter (Cron, jede Minute).

Chris legt ein Bild/Video in den OneDrive-Ordner
    D:\\OneDrive\\Dokumente\\Bolla\\Aufpeppen_Eingang\\
(am Handy: OneDrive-App -> Hochladen / Teilen in diesen Ordner).

Der Wächter peppt es via aufpeppen.py im Sinne von Chris' Feel-Good-Profil auf:
  - Bild  -> Insta-Bild (4:5, sonniges Grading), Ergebnis .jpg
  - Video -> TikTok-Video (Hochformat, Grading), Ergebnis .mp4
Ergebnis landet a) auf dem Desktop (Ordner 'Aufgepeppt') und b) im mmp (Clipboard-URL + grüner
„Auf Handy speichern"-Knopf). Original wandert nach _verarbeitet/.

Optionaler Kontext: eine gleichnamige .txt (z.B. foto.txt) daneben legen. Erste Zeile darf
Optionen enthalten: 'tiktok', 'insta', 'spectacular', 'natural', 'vivid', 'song' (Musikbett).
Weiterer Text = Overlay-Hook.
Idempotent über State-Datei. Kein Server-Neustart nötig.
"""
import os, sys, json, subprocess, hashlib, datetime, urllib.request, shutil, fcntl, re

HOME = "/home/bolla"
WS = f"{HOME}/workspace"
sys.path.insert(0, f"{WS}/scripts")
EINGANG = "/mnt/d/OneDrive/Dokumente/Bolla/Aufpeppen_Eingang"
VERARB = os.path.join(EINGANG, "_verarbeitet")
DESKTOP_OUT = "/mnt/d/OneDrive/Desktop/Aufgepeppt"
CLIP_IMAGES = f"{WS}/config/clipboard_images"
ENGINE = f"{WS}/scripts/aufpeppen.py"
SONG_ARCHIVE = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid"
STATE = f"{WS}/config/aufpeppen_watcher_state.json"
LOCK = f"{WS}/config/.aufpeppen_watcher.lock"
LOG = f"{WS}/data/aufpeppen_watcher.log"
API = "http://127.0.0.1:18790"
PUBLIC = "https://bolla.chrismandel.de"

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
VID_EXT = (".mp4", ".mov", ".m4v", ".avi", ".mkv")
OPTS = {"tiktok", "insta", "spectacular", "natural", "vivid", "song"}


def log(m):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try: open(LOG, "a", encoding="utf-8").write(f"[{ts}] {m}\n")
    except Exception: pass


def load_state():
    try: return set(json.load(open(STATE)))
    except Exception: return set()


def save_state(s):
    json.dump(sorted(s), open(STATE, "w"))


def post_clip(text):
    req = urllib.request.Request(f"{API}/api/clipboard",
        data=json.dumps({"text": text, "append": True, "source": "bolla-aufpeppen"}).encode(),
        headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=15)


def latest_song_mp3():
    try:
        mp3s = [os.path.join(SONG_ARCHIVE, f) for f in os.listdir(SONG_ARCHIVE) if f.lower().endswith(".mp3")]
        return max(mp3s, key=os.path.getmtime) if mp3s else None
    except Exception:
        return None


def parse_sidecar(path):
    """Optionale .txt: Optionen (erste Zeile) + Overlay-Text."""
    platform = style = None; music = False; text = ""
    if os.path.isfile(path):
        raw = open(path, encoding="utf-8-sig", errors="ignore").read().strip()
        lines = raw.splitlines()
        if lines:
            first = lines[0].lower()
            toks = set(re.findall(r"[a-zä]+", first))
            if toks & OPTS:
                if "tiktok" in toks: platform = "tiktok"
                if "insta" in toks: platform = "insta"
                for s in ("spectacular", "natural", "vivid"):
                    if s in toks: style = s
                if "song" in toks: music = True
                lines = lines[1:]  # Optionszeile raus
        text = "\n".join(lines).strip()
    return platform, style, music, text


def process_one(src):
    stem, ext = os.path.splitext(os.path.basename(src))
    is_img = ext.lower() in IMG_EXT
    platform, style, music, text = parse_sidecar(os.path.join(EINGANG, stem + ".txt"))
    if platform is None:
        platform = "insta" if is_img else "tiktok"
    if style is None:
        style = "auto"
    out_ext = ".jpg" if (is_img and platform == "insta") else ".mp4"
    out = os.path.join(DESKTOP_OUT, f"{stem}_aufgepeppt{out_ext}")
    os.makedirs(DESKTOP_OUT, exist_ok=True)
    cmd = ["python3", ENGINE, src, "--platform", platform, "--style", style, "--out", out]
    if text:
        cmd += ["--text", text]
    else:
        cmd += ["--ai"]  # kein Text von Chris vorgegeben -> Fable schaut sich's an und schreibt content-bezogenen Hook
    if music:
        m = latest_song_mp3()
        if m: cmd += ["--music", m]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
    if r.returncode != 0 or not os.path.isfile(out):
        log(f"FEHLER bei {os.path.basename(src)}: {(r.stderr or r.stdout)[:200]}")
        post_clip(f"⚠️ Aufpeppen fehlgeschlagen: {os.path.basename(src)}")
        return
    # ins mmp (über clipboard_images servierbar)
    pub = f"{stem}_aufgepeppt{out_ext}".replace(" ", "_")
    shutil.copy2(out, os.path.join(CLIP_IMAGES, pub))
    post_clip(f"✨ Aufgepeppt ({platform}): {PUBLIC}/api/clipboard/image/{pub}")
    log(f"OK: {os.path.basename(src)} -> {os.path.basename(out)} ({platform}/{style})")


def build_batch_montage(new_files):
    """Mehrere Dateien auf einmal reingekippt -> EIN spektakuläres Reel statt viele Einzel-Clips."""
    import aufpeppen_montage as amon
    stems = "+".join(os.path.splitext(os.path.basename(f))[0] for f in new_files[:3])
    out = os.path.join(DESKTOP_OUT, f"Reel_{stems[:60]}_{len(new_files)}x.mp4")
    ok, hook_or_err = amon.build_montage(new_files, out, music=None, style="auto", hook=None, max_clips=8)
    if not ok:
        log(f"FEHLER Montage ({len(new_files)} Dateien): {hook_or_err}")
        post_clip(f"⚠️ Reel-Montage fehlgeschlagen ({len(new_files)} Dateien)")
        return
    pub = os.path.basename(out).replace(" ", "_")
    shutil.copy2(out, os.path.join(CLIP_IMAGES, pub))
    post_clip(f"🎬 Spektakel-Reel aus {len(new_files)} Fotos/Videos: {PUBLIC}/api/clipboard/image/{pub}")
    log(f"OK Montage: {len(new_files)} Dateien -> {os.path.basename(out)} (Hook: {hook_or_err})")


def main():
    os.makedirs(EINGANG, exist_ok=True)
    os.makedirs(VERARB, exist_ok=True)
    lf = open(LOCK, "w")
    try: fcntl.flock(lf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: return
    seen = load_state(); changed = False
    new_files = []
    for f in sorted(os.listdir(EINGANG)):
        src = os.path.join(EINGANG, f)
        if not os.path.isfile(src): continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in IMG_EXT + VID_EXT: continue
        h = hashlib.md5(f.encode()).hexdigest()[:12]
        if h in seen: continue
        new_files.append((f, src, h))

    for f, src, h in new_files:
        log(f"Neue Datei: {f}")
        try:
            process_one(src)
        except Exception as e:
            log(f"Ausnahme {f}: {e}")
        seen.add(h); changed = True

    if len(new_files) >= 2:
        try:
            build_batch_montage([src for _, src, _ in new_files])
        except Exception as e:
            log(f"Ausnahme Montage: {e}")

    # Originale + Sidecars wegräumen (erst NACH Einzel- und Montage-Verarbeitung)
    for f, src, h in new_files:
        try:
            shutil.move(src, os.path.join(VERARB, f))
            sc = os.path.join(EINGANG, os.path.splitext(f)[0] + ".txt")
            if os.path.isfile(sc): shutil.move(sc, os.path.join(VERARB, os.path.basename(sc)))
        except Exception: pass

    if changed: save_state(seen)


if __name__ == "__main__":
    main()
