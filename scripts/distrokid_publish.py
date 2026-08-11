#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DistroKid-Komplett-Vorbereitung ("Veröffentlichen"-Knopf in Bolla Songs).

Verkettet alles, was für einen bollawave-Release nötig ist — nachdem der Song
bei Suno fertig ist und MP3 + Cover im Archiv liegen:

    Desktop/DistroKid/  aufräumen (done-Songs ins Backup)   [staging_cleanup]
      → Staging-Ordner  Desktop/DistroKid/<Titel>/  anlegen
          <Titel>.mp3                (320 kbps, aus Archiv)
          <Titel> (Cover).jpg        (3000², aus Archiv)
          Lyrics.txt                 (falls Liedtext übergeben)
          DistroKid-Checkliste.txt   (Felder für den Upload)
          Social Media/              (PromoCard, TikTok/Insta-Video, Captions, Anleitung)

Aufruf (CLI, wird auch vom Server /api/suno/publish genutzt):
    python3 distrokid_publish.py "<Titel>" --sprache de --genre Pop [--lyrics-file /pfad] [--no-cleanup]

Gibt am Ende eine JSON-Zeile mit Ergebnis/Warnungen aus (für den Server parsebar):
    __RESULT__ {"ok": true, "folder": "...", "files": [...], "warnings": [...]}
"""
import os, re, sys, json, shutil, subprocess, argparse
from datetime import datetime

# Funktionen aus dem Social-Paket wiederverwenden (Video, Captions, Anleitung)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import distrokid_social_paket as sp

ARCHIVE   = "/mnt/d/OneDrive/Dokumente/Bolla/Suno_DistroKid"
DK_BASE   = "/mnt/d/OneDrive/Desktop/DistroKid"
CLEANUP   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "distrokid_staging_cleanup.py")
ARTIST      = "bollawave"
ARTIST_SLUG = "bollawave"
SONGWRITER  = "Christoph Mandel"
CLAUDE_BIN  = os.path.expanduser("~/.local/bin/claude")

# Echte DistroKid-Dropdown-Genres (Stand 11.08.2026, per Recherche — DistroKid hat KEIN
# "Hyperpop"/"Phonk"/"Drill"/"Amapiano" etc. als eigene Einträge, nur diese groben Kategorien).
DISTROKID_GENRES = [
    "Afrobeat", "Afropop", "Alternative", "Big Band", "Blues", "Children's Music",
    "Christian/Gospel", "Classical", "Comedy", "Contemporary Latin", "Country", "Dance",
    "Electronic", "Electronica / Downtempo", "Fitness & Workout", "Folk", "French Pop",
    "German Folk", "German Pop", "Hip Hop/Rap", "Hip-Hop / R&B", "Holiday", "J-Pop", "Jazz",
    "K-Pop", "Latin", "Latin House", "Latin Jazz", "Latin Urban", "Maskandi", "Metal",
    "New Age", "Pop", "Pop in Spanish", "Punk", "R&B/Soul", "Reggae", "Rock",
    "Rock en Español", "Singer/Songwriter", "Soundtrack", "Spoken Word", "Techno", "Vocal",
]


def resolve_distrokid_genre(user_genre, title):
    """Mappt einen freien Genre-Text (z.B. von Suno-Stilbeschreibungen wie "Hyperpop"/"Drift-Phonk",
    die es bei DistroKid nicht gibt) auf den nächstliegenden ECHTEN DistroKid-Dropdown-Wert.
    Gibt (resolved, original_falls_abweichend) zurück."""
    ug = (user_genre or "").strip()
    if not ug:
        return "Pop", None
    for g in DISTROKID_GENRES:
        if g.lower() == ug.lower():
            return g, None
    prompt = (
        f"Der Nutzer hat für den Song \"{title}\" das Genre \"{ug}\" eingegeben — das ist KEIN "
        f"gültiger DistroKid-Dropdown-Wert. Wähle aus DIESER Liste exakt EINEN Eintrag, der am "
        f"besten zum eingegebenen Stil passt:\n{', '.join(DISTROKID_GENRES)}\n"
        f"Antworte NUR mit dem exakten Listen-Eintrag, sonst nichts.")
    try:
        r = subprocess.run([CLAUDE_BIN, "-p", "--model", "claude-sonnet-5", "--output-format", "json", prompt],
                            capture_output=True, text=True, timeout=30)
        out = json.loads(r.stdout).get("result", "").strip() if r.returncode == 0 else ""
        for g in DISTROKID_GENRES:
            if g.lower() == out.lower():
                return g, ug
    except Exception:
        pass
    return "Pop", ug


# DistroKid zeigt bei Primärgenre "Electronic" zusätzlich ein Subgenre-Dropdown (Chris-Wunsch 11.08.2026:
# das immer mit vorschlagen). Andere Primärgenres haben KEIN eigenes Subgenre-Feld bei DistroKid.
ELECTRONIC_SUBGENRES = [
    "Big Room", "Breaks", "Chill Out", "Deep House", "Drum & Bass", "Dubstep", "Electro House",
    "Electronica / Downtempo", "Funk / Soul / Disco", "Glitch Hop", "Hard Dance",
    "Hardcore / Hard Techno", "Hip-Hop / R&B", "House", "Indie Dance / Nu Disco",
    "Minimal / Deep Tech", "Progressive House", "Psy-Trance", "Reggae / Dancehall / Dub",
    "Tech House", "Techno", "Trance",
]


def resolve_electronic_subgenre(user_genre, title):
    """Nur relevant wenn das Primärgenre "Electronic" ist — DistroKid fragt dann zusätzlich ein
    Subgenre ab. Wählt aus ELECTRONIC_SUBGENRES das am besten passende."""
    ug = (user_genre or "").strip()
    prompt = (
        f"Der Song \"{title}\" wurde als Suno-Stil/Genre-Text \"{ug or 'Electronic'}\" beschrieben und "
        f"bekommt bei DistroKid das Primärgenre \"Electronic\" — dafür ist ZUSÄTZLICH ein Subgenre nötig. "
        f"Wähle aus DIESER Liste exakt EINEN Eintrag, der am besten passt:\n{', '.join(ELECTRONIC_SUBGENRES)}\n"
        f"Antworte NUR mit dem exakten Listen-Eintrag, sonst nichts.")
    try:
        r = subprocess.run([CLAUDE_BIN, "-p", "--model", "claude-sonnet-5", "--output-format", "json", prompt],
                            capture_output=True, text=True, timeout=30)
        out = json.loads(r.stdout).get("result", "").strip() if r.returncode == 0 else ""
        for g in ELECTRONIC_SUBGENRES:
            if g.lower() == out.lower():
                return g
    except Exception:
        pass
    return "House"

# Lyrics-Scan: was NICHT im veröffentlichten Text stehen darf (Schul-/Personen-/Künstlerbezug)
SCAN_PATTERNS = {
    "Nachname Mandel":      r"\bmandel\b",
    "Schule (Lessing)":     r"\blessing\b",
    "Schul-Wort":           r"\b(schule|schüler|klassenzimmer|gymnasium|pausenklingel|hausaufgab)\w*\b",
    "Lehrer-Anrede":        r"\bherr\s+\w+",
    "Künstlername im Text": r"\bbollawave\b",
    "Klassen-Kürzel":       r"\bklasse\s*\d",
    "Klassen-Kurzform (7a/7b/…)": r"\b[5-9][a-dA-D]\b",
}


def slug(name):
    return sp.slugify(name)


def safe(name):
    return sp.safe(name)


def lyrics_scan(lyrics):
    """Sucht nach kritischen Begriffen. Gibt Liste von Warnungen zurück (leer = sauber)."""
    if not lyrics:
        return ["ℹ️ Kein Liedtext eingefügt → Namens-Scan übersprungen (nur als Absicherung "
                "gegen versehentliche Schüler-Namen gedacht — bei einem bollawave-Song unkritisch)."]
    warns = []
    low = lyrics.lower()
    for label, pat in SCAN_PATTERNS.items():
        if re.search(pat, low):
            warns.append(f"⚠ Lyrics-Scan: „{label}\" im Text gefunden — vor Upload prüfen!")
    return warns


def write_checklist(path, title, sprache, genre, link, warns, genre_original=None, subgenre=None):
    lang = "Deutsch" if sprache == "de" else "Englisch"
    genre_line = f"  [ ] Primäres Genre    : {genre}"
    if genre_original:
        genre_line += f"  (dein Text „{genre_original}\" gibt's bei DistroKid nicht als Dropdown-Wert — nächstliegender echter Eintrag)"
    lines = [
        f"DISTROKID-UPLOAD — {title}",
        "=" * 48,
        "",
        "  DATEIEN",
        "  [ ] MP3 320 kbps + Cover 3000×3000 px (quadratisch) — liegen in diesem Ordner",
        "",
        "  GRUNDDATEN",
        f"  [ ] Künstler          : {ARTIST}",
        "  [ ] Songtitel exakt — KEIN Leerzeichen vor Apostroph",
        f"  [ ] Sprache           : {lang}  ⚠ (English bei EN-Song / German bei DE-Song)",
        genre_line,
    ]
    if subgenre:
        lines.append(f"  [ ] Subgenre (Electronic) : {subgenre}  — DistroKid fragt das nur bei Primärgenre \"Electronic\" extra ab")
    lines += [
        "  [ ] Zweites Genre     : Singer/Songwriter (oder Dance)",
        "  [ ] Stadt             : Norderstedt (NICHT Hamburg!)",
        "  [ ] Explicit          : Nein (bollawave = Feel-Good-Profil — Lyrics trotzdem gegenchecken)",
        "",
        "  KI-DEKLARATION (KI-Transparenz ist Chris wichtig — ehrlich ankreuzen)",
        "  [x] Songtext ✓  (Bolla = KI)",
        "  [x] Musik    ✓  (Suno = KI)",
        "  [ ] Audio-Ebene — je nachdem ob Chris' eigene Suno-Voice drin ist:",
        "        · Eigene Voice genutzt   -> \"Teile des Audios\" -> Gesang ankreuzen",
        "        · Reine Suno-KI-Stimme   -> \"Das gesamte Audio (mittels KI erstellt)\" ankreuzen",
        "",
        "  CREDITS / ROLLEN (Pflicht für Apple Music, sonst 'Bestätigungsfehler' beim Einreichen)",
        f"  [ ] Interpret*in : Rolle \"Gesang & Vocals\"     · Name: {ARTIST}",
        f"  [ ] Produzent*in : Rolle \"Executive Producer\" · Name: {SONGWRITER}",
        f"  [ ] Songwriter / Rechte: {SONGWRITER}",
        "      (feste Dropdown-Werte bei DistroKid — \"Interpret*in\" als Rollenname gibt's nicht)",
        "  ⚠️ Apple-Songwriter-Credit MUSS WÄHREND des Uploads im ausklappbaren",
        "     \"Credits/Apple Music\"-Bereich eingetragen werden — nachträglich sperrt",
        "     DistroKid das Feld (im Release-Bearbeiten nicht mehr auffindbar).",
        "",
        "  STORES & OPTIONEN",
        "  [ ] Alle Stores AN (Spotify, Apple, Amazon, YouTube Music, TikTok …)",
        "  [ ] KEIN Exklusiv-/Select-Häkchen (kollidiert mit D2D)",
        "  [ ] Releasedate: ASAP (gratis)",
        "  [ ] Label: Standard \"Records DK\" lassen",
        "  [ ] Upsells ablehnen: Ultimate / Vermächtnis / Store Maximizer / Mixea",
        "",
        "  ANTI-SPAM",
        "  [ ] Mind. 4 Tage Abstand zum letzten Release (Kalender prüfen)",
        "",
        "  VOR DEM ABSENDEN PRÜFEN",
        "  [ ] Titel korrekt (kein \"Track 1\"/\"Songtitel\")",
        "  [ ] Cover = richtiges Bild",
        "  [ ] ALLE Felder gegenchecken — DistroKid übernimmt oft alte Werte vom Vorgänger-Song!",
        "",
        f"  Hyperfollow-Link (nach Release): {link}",
        "",
        "  DATEIEN in diesem Ordner:",
        "  - <Titel>.mp3            (320 kbps, Upload-fertig)",
        "  - <Titel> (Cover).jpg    (3000×3000, textfrei)",
        "  - Lyrics.txt             (Songtext)",
        "  - Social Media/          (Video + Captions zum Posten — NACH Release)",
        "",
    ]
    if warns:
        lines.append("  ⚠ WARNUNGEN aus dem Lyrics-Scan:")
        for w in warns:
            lines.append(f"    {w}")
        lines.append("")
    lines.append("  Danach: Ordner nach dem Upload löschbar (räumt sich sonst automatisch auf).")
    lines.append("  — vorbereitet von Bolla 🐾")
    with open(path, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(lines))


def build(title, sprache="de", genre="Pop", lyrics="", do_cleanup=True):
    result = {"ok": False, "folder": None, "files": [], "warnings": []}

    # 1) Aufräumen (done-Songs ins Backup) — best effort
    if do_cleanup and os.path.isfile(CLEANUP):
        try:
            subprocess.run([sys.executable, CLEANUP], capture_output=True, timeout=120)
        except Exception as e:
            result["warnings"].append(f"Cleanup übersprungen: {e}")

    # 2) Assets im Archiv finden
    cover, mp3 = sp.find_asset(title)
    if not mp3:
        result["warnings"].append(
            f"❌ Keine MP3 für „{title}\" im Archiv ({ARCHIVE}). "
            f"Erst über „Cover & MP3 laden\" aus Suno holen.")
        return result
    if not cover:
        result["warnings"].append(
            f"❌ Kein Cover für „{title}\" im Archiv. Erst Cover erzeugen/ablegen.")
        return result

    # 3) Staging-Ordner anlegen
    dest = os.path.join(DK_BASE, safe(title))
    social = os.path.join(dest, "Social Media")
    os.makedirs(social, exist_ok=True)
    base = os.path.join(dest, safe(title))

    # 4) DistroKid-Upload-Dateien: MP3 + Cover + Lyrics + Checkliste
    shutil.copy2(mp3, base + ".mp3")
    result["files"].append(os.path.basename(base + ".mp3"))
    shutil.copy2(cover, base + " (Cover).jpg")
    result["files"].append(os.path.basename(base + " (Cover).jpg"))

    if lyrics:
        with open(os.path.join(dest, "Lyrics.txt"), "w", encoding="utf-8-sig") as f:
            f.write(lyrics.strip() + "\n")
        result["files"].append("Lyrics.txt")

    warns = lyrics_scan(lyrics)
    link = f"https://distrokid.com/hyperfollow/{ARTIST_SLUG}/{slug(title)}"
    resolved_genre, genre_original = resolve_distrokid_genre(genre, title)
    if genre_original:
        result["warnings"].append(
            f"ℹ️ Genre „{genre_original}\" gibt's bei DistroKid nicht — Checkliste nutzt stattdessen „{resolved_genre}\".")
    subgenre = None
    if resolved_genre == "Electronic":
        subgenre = resolve_electronic_subgenre(genre_original or genre, title)
        result["warnings"].append(f"ℹ️ Electronic-Subgenre-Vorschlag: „{subgenre}\".")
    write_checklist(os.path.join(dest, "DistroKid-Checkliste.txt"),
                    title, sprache, resolved_genre, link, warns, genre_original, subgenre)
    result["files"].append("DistroKid-Checkliste.txt")
    result["warnings"].extend(warns)

    # 5) Social-Paket in den Unterordner (PromoCard, Video, Captions, Anleitung)
    sbase = os.path.join(social, safe(title))
    shutil.copy2(cover, sbase + "_PromoCard.jpg")
    result["files"].append("Social Media/" + os.path.basename(sbase + "_PromoCard.jpg"))

    ok = sp.make_video(cover, mp3, sbase + "_TikTok-Video.mp4")
    if ok:
        result["files"].append("Social Media/" + os.path.basename(sbase + "_TikTok-Video.mp4"))
    else:
        result["warnings"].append("⚠ Video-Erzeugung fehlgeschlagen (ffmpeg).")

    try:
        sp.write_caption(sbase + "_Insta-Caption.txt", sp.llm_caption(title, "insta", link), link, title)
        sp.write_caption(sbase + "_TikTok-Caption.txt", sp.llm_caption(title, "tiktok", link), link, title)
        result["files"].append("Social Media/…_Insta-Caption.txt + …_TikTok-Caption.txt")
    except Exception as e:
        result["warnings"].append(f"⚠ Captions: {e}")

    try:
        sp.make_anleitung(os.path.join(social, f"ANLEITUNG_{safe(title)}_Posten.docx"), title, link)
        result["files"].append("Social Media/ANLEITUNG_…_Posten.docx")
    except Exception as e:
        result["warnings"].append(f"⚠ Anleitung: {e}")

    result["ok"] = True
    result["folder"] = dest
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title")
    ap.add_argument("--sprache", default="de")
    ap.add_argument("--genre", default="Pop")
    ap.add_argument("--lyrics-file", default="")
    ap.add_argument("--no-cleanup", action="store_true")
    a = ap.parse_args()

    lyrics = ""
    if a.lyrics_file and os.path.isfile(a.lyrics_file):
        with open(a.lyrics_file, encoding="utf-8") as f:
            lyrics = f.read()

    r = build(a.title, a.sprache, a.genre, lyrics, do_cleanup=not a.no_cleanup)
    # Menschlich lesbar …
    print(f"🎵 {a.title}")
    if r["ok"]:
        print(f"   ✓ Ordner: {r['folder']}")
        for f in r["files"]:
            print(f"     - {f}")
    for w in r["warnings"]:
        print(f"   {w}")
    # … und maschinell parsebar für den Server
    print("__RESULT__ " + json.dumps(r, ensure_ascii=False))
    sys.exit(0 if r["ok"] else 2)


if __name__ == "__main__":
    main()
