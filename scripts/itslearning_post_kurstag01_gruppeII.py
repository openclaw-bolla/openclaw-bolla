#!/usr/bin/env python3
"""Kurstag 1 (Grundbegriffe I - Dateien und Ordner) fuer die 4 "II"-Kurse posten.
Basiert auf itslearning_post_kurstag.py, siehe dort fuer alle DOM-Fallstricke."""
import sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_post_kurstag as base
from playwright.sync_api import sync_playwright

DAY_PREFIX = "01"

COURSES = [
    {"id": 190877, "kuerzel": "7d II", "text":
        "\U0001F44B Hallo liebe 7d! Am Mittwoch startet für euch die EDV – schön, dass ihr "
        "dabei seid! 1️⃣ Zu Beginn zeige ich euch gemeinsam, wie ihr Dateien aus itslearning "
        "herunterladet und auf euren Stick packt. 2️⃣ Danach geht's direkt ins Praktikum: Ordner "
        "anlegen, Dateien umbenennen, den Editor kennenlernen. 3️⃣ Bringt unbedingt euren "
        "USB-Stick mit! Bis Mittwoch! \U0001F60A"},
    {"id": 190743, "kuerzel": "7b II", "text":
        "\U0001F5A5️ Liebe 7b, am Mittwoch geht's für euch mit EDV los! 1️⃣ Wir laden "
        "gemeinsam die Materialien aus itslearning herunter – das übt ihr direkt am ersten Tag. "
        "2️⃣ Dann geht's ins Praktikum: Ordner erstellen, Dateien anlegen, speichern – "
        "Schritt für Schritt erklärt. 3️⃣ Denkt an euren USB-Stick – ohne geht "
        "nix. Freu mich auf euch! \U0001F680"},
    {"id": 190738, "kuerzel": "7a II", "text":
        "\U0001F4BB Hallo 7a! Am Donnerstag startet eure EDV-Zeit. 1️⃣ Als Erstes zeige ich "
        "euch, wie man Dateien aus itslearning holt und sicher auf dem Stick speichert. 2️⃣ "
        "Danach übt ihr im Praktikum den Umgang mit Ordnern und Dateien, ganz kleinschrittig "
        "erklärt. 3️⃣ USB-Stick nicht vergessen! Bis Donnerstag! \U0001F60A"},
    {"id": 190878, "kuerzel": "7c II", "text":
        "\U0001F4C1 Liebe 7c, Donnerstag ist euer erster EDV-Tag. 1️⃣ Wir laden zusammen die "
        "Dateien aus itslearning herunter – der erste Schritt, den ihr ab jetzt öfter braucht. "
        "2️⃣ Dann geht's ins Praktikum: Ordner anlegen, Dateien benennen, speichern – "
        "ganz in eurem Tempo. 3️⃣ Bringt euren Stick mit! Bin gespannt auf euch! \U0001F642"},
]

if __name__ == "__main__":
    files = base.discover_files(DAY_PREFIX)
    print(f"Standard-Paket fuer Tag {DAY_PREFIX}: {[f['filename'] for f in files]}")
    if not files:
        raise SystemExit(f"Keine Dateien mit Praefix '{DAY_PREFIX}-' gefunden.")

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
