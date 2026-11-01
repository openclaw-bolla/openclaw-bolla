#!/usr/bin/env python3
"""Einmaljob So 01.11.2026 (Chris-Auftrag 31.10.): Kinderlied-Playback + Liedtext (Word) fuer Mia.
Reihenfolge: 1) Meine Oma faehrt im Huehnerstall Motorrad  2) Drei Chinesen mit dem Kontrabass  3) Auf der Mauer, auf der Lauer.
Erst das naechste Lied, wenn das vorige NICHT beides (Word + Playback) schafft. Ein `claude -p` (Sonnet) ueber limit_gate,
laeuft erst, wenn die Token wieder frei sind (Gate wartet). Ergebnis -> Telegram + aktuell.md."""
import os, sys, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import limit_gate
W = "/home/bolla/workspace"
LOG = f"{W}/logs/mia_lied_so01.log"
CL = os.path.expanduser("~/.local/bin/claude")
PROMPT = """Auftrag von Chris (31.10.2026), selbststaendig, keine Rueckfragen. Kinderlied fuer MIA (Tonie-Seite, kind=mia): Liedtext (Word) UND Playback (MP3) erzeugen.
Reihenfolge strikt: 1) "Meine Oma fährt im Hühnerstall Motorrad"  2) "Drei Chinesen mit dem Kontrabass"  3) "Auf der Mauer, auf der Lauer".
Nimm das erste Lied, bei dem BEIDES klappt; die folgenden nur versuchen, wenn das vorige nicht beides schafft.
Vorgehen: Lies ~/.claude/projects/-home-bolla/memory/aktuell.md (letzte Eintraege 31.10. zu Tonie/Hopp hopp hopp) und project_tonie_zwillinge.md, feedback_liedtext_nur_mit_echter_quelle.md.
Endpunkte (Server http://127.0.0.1:18790): POST /api/tonies/liedtext und /api/tonies/playback, Body {"kind":"mia","titel":"<Titel>"} (Code: scripts/mission_control_api.py tonies_liedtext/tonies_playback/_tonies_lied_quelle, Rendering scripts/tonie_playback.py, Noten data/tonie_noten.json).
Liedtext nur mit echter Quelle (Wikibooks-Liederbuch, wortgleich) - nie aus dem Gedaechtnis. Noten bevorzugt aus dem LilyPond-Code der Wikibooks-Seite (Beispiel: Eintrag "hopp, hopp, hopp, pferdchen lauf galopp" in tonie_noten.json, Quelle-Feld dokumentieren), nur zur Not Claude-Noten.
Wenn der Standardweg scheitert (Quelle nicht gefunden, Noten nicht sicher), repariere/erweitere ihn (z. B. Titelabgleich, Seitenformat, LilyPond-Noten von Hand uebertragen) statt aufzugeben. Tempo kindgerecht langsam (siehe min_bpm-Feld, Hopp-Lied 104 bpm). Backup von Dateien vor Aenderung nach workspace/backups/.
Pruefe am Ende mit ls (Datum!), dass Lied_Mia_<Titel>.docx und Playback_<Titel>.mp3 in /mnt/d/OneDrive/Dokumente/Bolla/Tonies/ neu sind (Datum heute, Groesse > 0). Setze danach in /home/bolla/workspace/data/tonies.json bei mia.lied.titel das gewaehlte Lied (ueber POST /api/tonies/save {"kind":"mia","teil":"lied","titel":"...","stage":"text"}).
Pruefe zusaetzlich: laufen Liedtext UND Playback bei allen drei Kandidaten oder nicht (kurze Tabelle mit Grund pro Lied; fuer nicht gewaehlte Lieder KEINE Dateien dauerhaft liegen lassen, also Test-Word/MP3 wieder loeschen ausser dem gewaehlten).
Haenge einen kurzen Eintrag an aktuell.md an. Letzte Zeile deiner Antwort: ERGEBNIS: <gewaehltes Lied> | <Word ok/nein> | <Playback ok/nein> | <Kurzbegruendung der anderen>."""
def log(m):
    open(LOG, "a").write(f"{dt.datetime.now():%F %T} {m}\n")
def telegram(t):
    try:
        import requests, json
        c = json.load(open(f"{W}/config/telegram_bot.json"))
        requests.post(f"https://api.telegram.org/bot{c['bot_token']}/sendMessage", json={"chat_id": c["chris_id"], "text": t}, timeout=10)
    except Exception as e:
        log(f"Telegram fehlgeschlagen: {e}")
def main():
    if dt.date.today() != dt.date(2026, 11, 1) and "--force" not in sys.argv:
        return
    log("Start")
    r = limit_gate.run([CL, "-p", "--model", "sonnet", "--allowedTools", "Read,Write,Edit,Bash,Glob,Grep"], input=PROMPT, timeout=3000)
    out = (getattr(r, "stdout", "") or "")
    log(out[-1500:])
    last = [l for l in out.splitlines() if l.startswith("ERGEBNIS")]
    telegram("🐾 Mia-Kinderlied: " + (last[-1] if last else "Job lief, aber ohne klares Ergebnis – bitte im Log nachsehen (logs/mia_lied_so01.log)"))
if __name__ == "__main__":
    main()
