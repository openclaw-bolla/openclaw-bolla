#!/usr/bin/env python3
"""
Täglich 2 neue Mission Control Redesign-Mockups via Claude generieren.
Speichert HTML-Dateien + Metadaten für die Redesigns-Seite.
"""
import subprocess, shutil, json, os, re, sys
from datetime import date

OUTDIR    = os.path.expanduser("~/workspace/mission-control")
META_FILE = os.path.join(OUTDIR, "redesign-meta.json")
CLAUDE_BIN = os.path.expanduser("~/.local/bin/claude")

PROMPT_TEMPLATE = """Du bist ein kreativer UI/UX-Designer. Generiere GENAU EIN HTML-Mockup für ein persönliches Dashboard namens "Mission Control".

Stil-Vorgabe: {style}

Das Dashboard hat:
- Sidebar links mit Navigation (Dashboard, Bolla, Schule, Kalender, E-Mail, Wetter, System Info)
- Topbar mit Seitentitel + Uhrzeit (20:14)
- Hauptbereich mit Widget-Karten (RAM 34%, CPU 12%, 3 neue Mails, Wetter Hamburg 18°C)

Antworte GENAU in diesem Format (kein Text davor oder danach):

===META===
{{"name":"DESIGN_NAME","tagline":"KURZBESCHREIBUNG","desc":"EIN SATZ ÜBER DEN STIL","color_a":"#HEX","color_b":"#HEX"}}
===HTML===
<!DOCTYPE html>
[komplettes HTML mit allem CSS inline, keine externen Abhängigkeiten, realistische Dummy-Daten]
===END==="""

STYLES = [
    "Dunkel, futuristisch, Neon-Akzente — wie ein Sci-Fi Cockpit",
    "Hell, minimalistisch, viel Weißraum — wie ein Apple-Produkt",
    "Terminal-Look, grüner Text auf Schwarz, Monospace — wie ein Hacker",
    "Warm, papierfarben, handgezeichnet wirken — wie ein Notizbuch",
    "Glassmorphism, Blur-Effekte, pastellig — modern und verspielt",
    "Bold, Brutalist, starke Farben, kein Schnickschnack",
]


def run_claude(prompt: str) -> str:
    result = subprocess.run(
        [CLAUDE_BIN, "-p", prompt],
        capture_output=True, text=True, timeout=300,
        cwd=os.path.expanduser("~/workspace"),
        env={**os.environ, "PATH": os.path.expanduser("~/.local/bin") + ":" + os.environ.get("PATH", "")}
    )
    if result.returncode != 0:
        raise RuntimeError(f"Claude exit {result.returncode}: {result.stderr[:300]}")
    return result.stdout.strip()


def parse_response(text: str):
    meta_m = re.search(r"===META===\s*(\{.*?\})\s*===HTML===", text, re.DOTALL)
    html_m = re.search(r"===HTML===\s*(<!DOCTYPE.*?)===END===", text, re.DOTALL | re.IGNORECASE)
    if not (meta_m and html_m):
        # Fallback: versuche HTML ohne Marker zu finden
        html_fallback = re.search(r"(<!DOCTYPE html>.*)", text, re.DOTALL | re.IGNORECASE)
        if html_fallback:
            raise ValueError(f"META-Marker fehlt. HTML gefunden aber kein META-Block.")
        raise ValueError("Antwort-Format ungültig — Marker nicht gefunden")
    meta = json.loads(meta_m.group(1))
    html = html_m.group(1).strip()
    return meta, html


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

    import random
    random.shuffle(STYLES)
    style1, style2 = STYLES[0], STYLES[1]

    designs = []
    for i, style in enumerate([style1, style2], 1):
        print(f"Generiere Design {i}/2: {style[:40]}...")
        for attempt in range(3):
            try:
                raw = run_claude(PROMPT_TEMPLATE.format(style=style))
                meta, html = parse_response(raw)
                designs.append((meta, html))
                print(f"  ✓ {meta.get('name')}")
                break
            except Exception as e:
                print(f"  Versuch {attempt+1} fehlgeschlagen: {e}", file=sys.stderr)
                if attempt == 2:
                    print(f"FEHLER Design {i}: {e}", file=sys.stderr)
                    sys.exit(1)

    meta1, html1 = designs[0]
    meta2, html2 = designs[1]

    with open(os.path.join(OUTDIR, "redesign-1.html"), "w", encoding="utf-8") as f:
        f.write(html1)
    with open(os.path.join(OUTDIR, "redesign-2.html"), "w", encoding="utf-8") as f:
        f.write(html2)

    out = {
        "date": date.today().isoformat(),
        "design1": {
            "name":        meta1.get("name", "Design 1"),
            "tagline":     meta1.get("tagline", ""),
            "description": meta1.get("desc", ""),
            "color_a":     meta1.get("color_a", "#4fc3f7"),
            "color_b":     meta1.get("color_b", "#2196f3"),
            "file":        "redesign-1.html",
        },
        "design2": {
            "name":        meta2.get("name", "Design 2"),
            "tagline":     meta2.get("tagline", ""),
            "description": meta2.get("desc", ""),
            "color_a":     meta2.get("color_a", "#9c27b0"),
            "color_b":     meta2.get("color_b", "#673ab7"),
            "file":        "redesign-2.html",
        },
    }
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"✓ Fertig: {meta1.get('name')} · {meta2.get('name')}")
