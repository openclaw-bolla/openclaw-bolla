#!/usr/bin/env python3
"""Playback (Instrumental) fuer Tonie-Kinderlieder: gemeinfreie Melodie als Noten, per numpy zu Spieluhr/Harfe gerendert.
Aufruf: tonie_playback.py "<Liedtitel>" [ausgabe.mp3] [--tempo BPM] [--runden N]"""
import sys, subprocess, wave, os
import numpy as np

SR = 44100
NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "H": 11}

def midi(n):
    # n wie "C4", "G3"
    return 12 * (int(n[-1]) + 1) + NOTE[n[0]]

def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)

# Melodie: Liste (Note, Schlaege); Akkorde: Liste (Grundton, Terz-Typ) je Takt
SONGS = {
    "alle meine entchen": {
        "takt": 4,
        "bpm": 120,
        "melodie": [("C4", 1), ("D4", 1), ("E4", 1), ("F4", 1), ("G4", 2), ("G4", 2),
                    ("A4", 1), ("A4", 1), ("A4", 1), ("A4", 1), ("G4", 4),
                    ("F4", 1), ("F4", 1), ("F4", 1), ("F4", 1), ("E4", 2), ("E4", 2),
                    ("D4", 1), ("D4", 1), ("D4", 1), ("D4", 1), ("C4", 4)],
        "akkorde": [("C3", "dur")] * 2 + [("F3", "dur"), ("C3", "dur"), ("F3", "dur"), ("C3", "dur"), ("G3", "dur"), ("C3", "dur")],
    },
}

def spieluhr(f, dauer, vel=0.5):
    """Weicher Spieluhr-/Glockenspiel-Klang: FM mit schnellem Obertonabfall."""
    t = np.arange(int(SR * dauer)) / SR
    env = np.exp(-t * 2.6)
    mod = 2.0 * np.exp(-t * 9) * np.sin(2 * np.pi * f * 3.5 * t)
    x = np.sin(2 * np.pi * f * t + mod) * env + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 5)
    a = int(SR * 0.004); x[:a] *= np.linspace(0, 1, a)
    return x * vel

def harfe(f, dauer, vel=0.35):
    """Gezupfte Saite (Karplus-Strong), warm."""
    n = int(SR * dauer); p = max(2, int(SR / f))
    buf = np.random.RandomState(7).uniform(-1, 1, p)
    buf = np.convolve(buf, np.ones(3) / 3, mode="same")
    out = np.empty(n)
    for i in range(n):
        j = i % p
        out[i] = buf[j]
        buf[j] = 0.4975 * (buf[j] + buf[(j + 1) % p])
    return out * vel

def mix_in(track, start, snd):
    e = min(len(track), start + len(snd))
    track[start:e] += snd[: e - start]

def render(song, bpm=None, runden=3):
    s = SONGS[song]
    beat = 60.0 / (bpm or s["bpm"]); takt = s["takt"]
    dauer_lied = sum(b for _, b in s["melodie"]) * beat
    vorspann = takt * beat
    total = vorspann + dauer_lied * runden + 3.0
    tr = np.zeros(int(SR * total))
    # Einzaehler: 4 leise Klicks
    for i in range(takt):
        k = np.sin(2 * np.pi * 1200 * np.arange(int(SR * 0.04)) / SR) * np.exp(-np.arange(int(SR * 0.04)) / SR * 80) * 0.3
        mix_in(tr, int(SR * i * beat), k)
    for r in range(runden):
        t0 = vorspann + r * dauer_lied
        pos = 0
        for note, b in s["melodie"]:
            mix_in(tr, int(SR * (t0 + pos * beat)), spieluhr(hz(midi(note)), b * beat * 1.6 + 0.8))
            pos += b
        for i, (gt, typ) in enumerate(s["akkorde"]):
            g = midi(gt); toene = [g, g + 4, g + 7, g + 12]
            for q in range(takt):  # Harfen-Arpeggio, je Schlag ein Ton
                m = toene[[0, 1, 2, 1][q % 4]] if q % 2 == 0 else toene[3 if q == 1 else 2]
                mix_in(tr, int(SR * (t0 + (i * takt + q) * beat)), harfe(hz(m), 1.3))
    # leichter Hall
    hall = np.zeros_like(tr)
    for d, g in ((0.043, 0.28), (0.071, 0.2), (0.113, 0.14)):
        o = int(SR * d); hall[o:] += tr[:-o] * g
    tr = tr + hall
    tr = tr / max(1e-9, np.max(np.abs(tr))) * 0.85
    return tr

def main():
    a = sys.argv[1:]
    titel = a[0].strip().lower() if a else ""
    if titel not in SONGS:
        print("Kein Notensatz fuer:", titel, "| vorhanden:", ", ".join(SONGS)); sys.exit(2)
    bpm = None; runden = 3; rest = []
    i = 1
    while i < len(a):
        if a[i] == "--tempo": bpm = float(a[i + 1]); i += 2
        elif a[i] == "--runden": runden = int(a[i + 1]); i += 2
        else: rest.append(a[i]); i += 1
    out = rest[0] if rest else f"Playback_{titel.replace(' ', '_')}.mp3"
    x = render(titel, bpm, runden)
    wav = out.rsplit(".", 1)[0] + ".wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-b:a", "192k", out], check=True)
    os.remove(wav)
    print(out)

if __name__ == "__main__":
    main()
