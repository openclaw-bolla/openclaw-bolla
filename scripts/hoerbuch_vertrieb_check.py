#!/usr/bin/env python3
"""Wöchentlicher Check (Chris 10.11.2026): gibt es einen günstigen/kostenlosen (≤ ~20-25 EUR/Jahr,
DistroKid-artig) Vertriebsweg für deutsche KI-Hörbücher? Meldet nur bei Treffer ('aktion'), sonst ok.
Cron: Do 9:05. Ergänzt kdp_virtual_voice_de_check.py (Mo)."""
import subprocess, sys, json, os, urllib.request
from pathlib import Path
from datetime import datetime
sys.path.insert(0, "/home/bolla/workspace/scripts")
from job_status import report

WORKSPACE = Path("/home/bolla/workspace")
CLAUDE_BIN = Path("/home/bolla/.local/bin/claude")
AKTUELL_MD = Path("/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md")
JOB = "hoerbuch-guenstiger-vertrieb"

PROMPT = """Prüfe per WebSearch/WebFetch (aktuelle Quellen), ob es einen GÜNSTIGEN oder KOSTENLOSEN
Vertriebsweg für DEUTSCHE Hörbücher gibt, analog zu DistroKid bei Musik (Pauschale ca. 20 EUR/Jahr
oder weniger, Autor behält ~100 % bzw. fast alles, Verteilung an mehrere Stores). Kontext: Chris
(Selbstverlag-Autor, Reihe AURORA) hat ein Hörbuch mit KI-/geklonter eigener Stimme (ElevenLabs),
das Hörbuch als fertige MP3-Dateien pro Kapitel. Hörbuch-Produktion selbst ist erledigt; es geht NUR
um Vertrieb/Veröffentlichung. Nicht gewollt: Einzelgebühren je Titel im dreistelligen Bereich.
Prüfe insbesondere: (a) Findaway Voices / Spotify for Authors (Gebühren, Deutsch, KI-Stimmen erlaubt?),
(b) Google Play Books (eigene Audiodateien hochladen, Deutsch), (c) Bookwire, BookBeat, Storytel
Self-Publishing, Nextory, (d) Direktverkauf (Payhip/Gumroad/eigene Website: Gebühren, Auslieferung als
Download), (e) neue DistroKid-/TuneCore-artige Hörbuch-Aggregatoren (2026), (f) Podcast-/Hosting-Wege
(z. B. Spotify/Apple als Hörbuch-Podcast) als Notlösung. Bewerte pro Weg: Kosten (einmalig/jährlich),
Deutsch ja/nein, KI-Stimme erlaubt, Kennzeichnungspflicht.
Antworte in der ERSTEN Zeile exakt mit JA, wenn mindestens ein Weg Deutsch erlaubt, KI-/geklonte
Stimme zulässt und insgesamt höchstens ca. 25 EUR pro Jahr (bzw. einmalig bis ~25 EUR) kostet oder
kostenlos ist; sonst NEIN. Bei JA danach 3-5 Sätze: welcher Weg, Kosten, Bedingungen, URL.
Bei NEIN eine Zeile: günstigster gefundener Weg mit Preis. Nichts erfinden; im Zweifel NEIN."""

JOB2 = "hoerbuch-guenstigere-vertonung"
PROMPT2 = """Prüfe per WebSearch/WebFetch (aktuelle Preisseiten, nichts aus dem Gedächtnis), ob es einen
deutlich GÜNSTIGEREN Weg gibt, ein komplettes deutsches Hörbuch (ca. 600.000-900.000 Zeichen je Band,
Zielwert 750.000) mit Chris' GEKLONTER EIGENER STIMME (Instant-Clone aus ~2 Min. Aufnahme reicht) zu erzeugen.
Referenz (Stand 10.11.2026): ElevenLabs Pro ca. 99 $/Monat (600k Credits), ein Buch braucht 1-2 Monate
= ca. 100-200 $ pro Band; Modell eleven_v3 (mit Audio-Tags) liefert die beste Qualität, Chris' Bestprobe E2.
Prüfe: (a) ElevenLabs selbst: aktuelle Tarife, Creator/Pro/Scale, Jahresabo-Rabatt, Zusatz-Credits,
Aktionen, günstigere Modelle (Flash/Turbo: Credit-Faktor je Zeichen? Deutsch-Qualität?), Kosten pro Zeichen
bei der API, Mindestlaufzeit; (b) andere Anbieter mit Stimmklon + gutem Deutsch (z. B. Fish Audio, Cartesia,
Resemble, Speechify, Murf, WellSaid, Hume, OpenAI/Google/Azure Custom Voice); (c) kostenlose Open-Source-
Modelle zum selbst Laufenlassen (XTTS-v2, F5-TTS, Chatterbox Multilingual, Kokoro u. ä.): Deutsch-Qualität,
Hardware-Bedarf. REFERENZ-HARDWARE ist AUSSCHLIESSLICH Chris' Surface Laptop Studio (Intel i7-13700H,
16 GB RAM, NVIDIA GeForce RTX 4050 Laptop mit ca. 6 GB VRAM, Windows 11; WSL2 ist künstlich auf 6 GB/4 Kerne
begrenzt, Windows-seitig läuft mehr). Das Surface Book 1 (i7-6600U, 8 GB, Schulgerät) NIE als Maßstab nehmen.
Bewerte, ob ein Modell mit 6 GB VRAM ein ganzes Buch (750k Zeichen) in vertretbarer Zeit rendert.
Chris' HARTE GRENZE (10.11.2026): maximal 20 EUR GESAMT für ein ganzes Buch (Vertonung, ohne Vertrieb).
Antworte in der ERSTEN Zeile exakt mit JA, wenn ein Weg das ganze Buch (>= 750k Zeichen) in vergleichbar
natürlicher deutscher Qualität mit Klon für insgesamt höchstens 20 EUR (inkl. nötiger Abos/Credits) ermöglicht
(kostenlos/Open-Source zählt, wenn es auf Chris' Hardware realistisch läuft); sonst NEIN. Bei JA danach 4-6 Sätze:
Weg, Gesamtkosten pro Band, Qualitätsurteil (nur belegen, nicht raten), URL. Bei NEIN eine Zeile: günstigster
gefundener Weg mit Preis pro Band. Nichts erfinden; im Zweifel NEIN."""

def el_konto():
    """Aktuelle ElevenLabs-Kontodaten (Tarif, Credits) per API; Key nie ausgeben."""
    try:
        k = open(os.path.expanduser("~/.elevenlabs_key")).read().strip()
        r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": k})
        d = json.load(urllib.request.urlopen(r, timeout=30))
        frei = d.get("character_limit", 0) - d.get("character_count", 0)
        return f"Chris' Konto jetzt (API): Tarif {d.get('tier')}, {d.get('character_count')}/{d.get('character_limit')} Credits genutzt (frei: {frei}), Status {d.get('status')}, Abo gekündigt zum 02.12.2026."
    except Exception as e:
        return "Kontodaten per API nicht abrufbar (" + type(e).__name__ + ", Key evtl. abgelaufen/gelöscht)."

def check_vertonung():
    report(JOB2, "Hörbuch: günstigere Vertonung?", "laeuft")
    try:
        konto = el_konto()
        r = subprocess.run([str(CLAUDE_BIN), "-p", PROMPT2 + "\n\n" + konto], capture_output=True, text=True,
                           timeout=480, cwd=str(WORKSPACE))
        a = r.stdout.strip()
        if not a:
            report(JOB2, "Hörbuch: günstigere Vertonung?", "fehler", (r.stderr or "leere Antwort")[:300]); return
        if a.splitlines()[0].strip().upper().startswith("JA"):
            heute = datetime.now().strftime("%d.%m.%Y")
            old = AKTUELL_MD.read_text(encoding="utf-8") if AKTUELL_MD.exists() else ""
            AKTUELL_MD.write_text(f"## 🎧 {heute} — Hörbuch: günstigere Vertonung gefunden?\n\n{a}\n\n---\n\n" + old, encoding="utf-8")
            report(JOB2, "Hörbuch: günstigere Vertonung gefunden", "aktion", a[:400])
        else:
            report(JOB2, "Hörbuch: günstigere Vertonung?", "ok", "Nichts deutlich Günstigeres (" + datetime.now().strftime("%d.%m.") + ")")
    except Exception as e:
        report(JOB2, "Hörbuch: günstigere Vertonung?", "fehler", str(e)[:300])

def main():
    report(JOB, "Hörbuch: günstiger Vertrieb?", "laeuft")
    try:
        r = subprocess.run([str(CLAUDE_BIN), "-p", PROMPT], capture_output=True, text=True,
                           timeout=420, cwd=str(WORKSPACE))
        a = r.stdout.strip()
        if not a:
            report(JOB, "Hörbuch: günstiger Vertrieb?", "fehler", (r.stderr or "leere Antwort")[:300]); return
        if a.splitlines()[0].strip().upper().startswith("JA"):
            heute = datetime.now().strftime("%d.%m.%Y")
            old = AKTUELL_MD.read_text(encoding="utf-8") if AKTUELL_MD.exists() else ""
            AKTUELL_MD.write_text(f"## 🎧 {heute} — Hörbuch: günstiger Vertriebsweg (≤ ~25 €/Jahr)\n\n{a}\n\n---\n\n" + old, encoding="utf-8")
            report(JOB, "Hörbuch: günstiger Vertriebsweg gefunden", "aktion", a[:400])
        else:
            report(JOB, "Hörbuch: günstiger Vertrieb?", "ok", "Noch nichts Günstiges (" + datetime.now().strftime("%d.%m.") + ")")
    except Exception as e:
        report(JOB, "Hörbuch: günstiger Vertrieb?", "fehler", str(e)[:300])

if __name__ == "__main__":
    main()
    check_vertonung()
