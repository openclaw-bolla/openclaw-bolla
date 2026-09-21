#!/usr/bin/env python3
"""Kurstag 2 (Grundbegriffe II) fuer die 4 "II"-Kurse posten (21.09.2026).
Basiert auf itslearning_post_kurstag01_gruppeII.py / itslearning_post_kurstag.py (DOM-Fallstricke dort).
Termine: 7d II + 7b II = Mi 23.09.  |  7a II + 7c II = Do 24.09. (gegen data/schuljahr2627.json geprueft)."""
import sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_post_kurstag as base
from playwright.sync_api import sync_playwright

DAY_PREFIX = "02"

COURSES = [
    {"id": 190877, "kuerzel": "7d II", "text":
        "🖥️ Am Mittwoch (23.09.) geht's weiter mit Kurstag 2! Ihr ladet euch in der Stunde direkt "
        "die neuen Folien „Grundbegriffe II“ herunter und macht als Erstes euer Praktikum 1 fertig, "
        "falls da noch was offen ist. Wer schon durch ist, kann sich an die Zusatzaufgabe "
        "„Praktikum 2“ wagen – ein paar knifflige Fragen zu KI, Cloud & Co. 🧠✨ Bis Mittwoch!"},
    {"id": 190743, "kuerzel": "7b II", "text":
        "👋 Kurstag 2 steht an – am Mittwoch (23.09.) in der 6./7. Stunde. Die Folien „Grundbegriffe II“ "
        "und das Praktikum gibt's direkt in der Stunde zum Herunterladen. Erst mal Praktikum 1 zu Ende "
        "bringen, dann – falls noch Zeit ist – die Zusatzfragen aus Praktikum 2 knacken. 💡 Wir sehen uns!"},
    {"id": 190738, "kuerzel": "7a II", "text":
        "🚀 Am Donnerstag (24.09.) läuft Kurstag 2! In der Stunde gibt's die Folien „Grundbegriffe II“ "
        "zum Download. Wichtig: erst Praktikum 1 fertigstellen, dann könnt ihr euch – wenn noch Zeit "
        "bleibt – an die Zusatzaufgabe Praktikum 2 setzen, mit Fragen rund um Hardware, Cloud und KI. "
        "🤖 Bis dahin!"},
    {"id": 190878, "kuerzel": "7c II", "text":
        "📚 Weiter geht's am Donnerstag (24.09.) mit Kurstag 2! Wir laden gemeinsam in der Stunde die "
        "Folien „Grundbegriffe II“ herunter. Wer sein Praktikum 1 schon fertig hat, darf sich an der "
        "optionalen Zusatzaufgabe Praktikum 2 versuchen – knifflige Fragen zu Cloud, Browser & KI "
        "warten. 😊"},
]

if __name__ == "__main__":
    files = base.discover_files(DAY_PREFIX)
    print(f"Standard-Paket fuer Tag {DAY_PREFIX}: {[f['filename'] for f in files]}")
    if "--dry" in sys.argv:
        raise SystemExit(0)
    if len(files) != 2:
        raise SystemExit(f"Erwartet 2 Dateien (Praktikum.html + PDF), gefunden {len(files)} - Abbruch.")

    results = []
    with sync_playwright() as p:
        browser, its = base.login(p)
        try:
            for c in COURSES:
                ok, used_pct = base.mem_ok()
                if not ok:
                    print(f"\n⚠️ Speicher bei {used_pct:.0f}% — breche vor '{c['kuerzel']}' ab.")
                    results.append((c["kuerzel"], f"ABGEBROCHEN (Speicher {used_pct:.0f}%)"))
                    break
                print(f"\n=== {c['kuerzel']} (CourseID {c['id']}) ===")
                up_ok = base.upload_files(its, c["id"], files)
                if not up_ok:
                    results.append((c["kuerzel"], "UPLOAD FEHLGESCHLAGEN"))
                    continue
                post_ok = base.post_message(its, c["id"], c["text"], files)
                results.append((c["kuerzel"], "OK" if post_ok else "MITTEILUNG FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
