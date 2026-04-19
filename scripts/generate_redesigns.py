#!/usr/bin/env python3
"""
Täglich 2 neue Mission Control Redesign-Mockups via Claude generieren.
Speichert HTML-Dateien + Metadaten für die Redesigns-Seite.
"""
import subprocess, shutil, json, os, re, sys
from datetime import date

OUTDIR   = os.path.expanduser("~/workspace/mission-control")
META_FILE = os.path.join(OUTDIR, "redesign-meta.json")

PROMPT = """Du bist ein kreativer UI/UX-Designer. Generiere 2 komplett verschiedene HTML-Mockup-Seiten für ein persönliches Dashboard namens "Mission Control" (Besitzer: Chris Mandel, KI-Assistent Bolla).

Das Dashboard hat:
- Sidebar links mit Navigation (Dashboard, Bolla, Schule, Kalender, E-Mail, Robin, Geburtstage, Local Server, Wetter, System Info)
- Topbar mit Seitentitel + Uhrzeit
- Hauptbereich mit Widget-Karten (Stats, Chat-Widget für Bolla, Aktivitäten, Wetter)

Jedes Design soll einen völlig anderen visuellen Stil haben — überraschend, frisch, kreativ. Keine zwei Designs sollen sich ähneln.

Antworte GENAU in diesem Format (keine anderen Texte davor oder danach):

===META===
{"name1":"DESIGN_NAME_1","tagline1":"KURZE_BESCHREIBUNG_1","desc1":"2 SÄTZE ÜBER STIL","color1a":"#HEX","color1b":"#HEX","name2":"DESIGN_NAME_2","tagline2":"KURZE_BESCHREIBUNG_2","desc2":"2 SÄTZE ÜBER STIL","color2a":"#HEX","color2b":"#HEX"}
===HTML1===
<!DOCTYPE html>
[komplettes, selbstständiges HTML für Design 1 — mit allem CSS inline, keine externen Abhängigkeiten, funktioniert als einzelne Datei, realistische Dummy-Daten, kein JS nötig]
===HTML2===
<!DOCTYPE html>
[komplettes, selbstständiges HTML für Design 2 — mit allem CSS inline, keine externen Abhängigkeiten, funktioniert als einzelne Datei, realistische Dummy-Daten, kein JS nötig]
===END==="""


def run_claude(prompt: str) -> str:
    claude_bin = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
    result = subprocess.run(
        [claude_bin, "-p", "--output-format", "json", prompt],
        capture_output=True, text=True, timeout=180,
        cwd=os.path.expanduser("~/workspace"),
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude exit {result.returncode}: {result.stderr[:300]}")
    data = json.loads(result.stdout)
    return data.get("result", "")


def parse_response(text: str):
    meta_m   = re.search(r"===META===\s*(\{.*?\})\s*===HTML1===", text, re.DOTALL)
    html1_m  = re.search(r"===HTML1===\s*(<!DOCTYPE.*?)===HTML2===", text, re.DOTALL | re.IGNORECASE)
    html2_m  = re.search(r"===HTML2===\s*(<!DOCTYPE.*?)===END===", text, re.DOTALL | re.IGNORECASE)

    if not (meta_m and html1_m and html2_m):
        raise ValueError("Antwort-Format ungültig — Marker nicht gefunden")

    meta  = json.loads(meta_m.group(1))
    html1 = html1_m.group(1).strip()
    html2 = html2_m.group(1).strip()
    return meta, html1, html2


def save(meta: dict, html1: str, html2: str):
    today = date.today().isoformat()

    with open(os.path.join(OUTDIR, "redesign-1.html"), "w", encoding="utf-8") as f:
        f.write(html1)
    with open(os.path.join(OUTDIR, "redesign-2.html"), "w", encoding="utf-8") as f:
        f.write(html2)

    out = {
        "date":    today,
        "design1": {
            "name":        meta.get("name1", "Design 1"),
            "tagline":     meta.get("tagline1", ""),
            "description": meta.get("desc1", ""),
            "color_a":     meta.get("color1a", "#4fc3f7"),
            "color_b":     meta.get("color1b", "#2196f3"),
            "file":        "redesign-1.html",
        },
        "design2": {
            "name":        meta.get("name2", "Design 2"),
            "tagline":     meta.get("tagline2", ""),
            "description": meta.get("desc2", ""),
            "color_a":     meta.get("color2a", "#9c27b0"),
            "color_b":     meta.get("color2b", "#673ab7"),
            "file":        "redesign-2.html",
        },
    }
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"✓ Redesigns generiert: {meta.get('name1')} · {meta.get('name2')}")


def already_done_today() -> bool:
    if not os.path.exists(META_FILE):
        return False
    try:
        with open(META_FILE) as f:
            d = json.load(f)
        return d.get("date") == date.today().isoformat()
    except Exception:
        return False


if __name__ == "__main__":
    force = "--force" in sys.argv
    if already_done_today() and not force:
        print("Heute bereits generiert — überspringe. (--force zum Erzwingen)")
        sys.exit(0)

    print("Generiere 2 neue Redesigns...")
    try:
        raw = run_claude(PROMPT)
        meta, html1, html2 = parse_response(raw)
        save(meta, html1, html2)
    except Exception as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        sys.exit(1)
