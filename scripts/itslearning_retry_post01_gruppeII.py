#!/usr/bin/env python3
"""Retry: nur post_message() fuer die 4 II-Kurse, Dateien liegen schon in den Ressourcen
(Upload lief bereits durch, nur die Mitteilung selbst scheiterte an Indexierungs-Verzoegerung)."""
import sys, time
sys.path.insert(0, "/home/bolla/workspace/scripts")
import itslearning_post_kurstag as base
from playwright.sync_api import sync_playwright

DAY_PREFIX = "01"

import itslearning_post_kurstag01_gruppeII as job
COURSES = job.COURSES

if __name__ == "__main__":
    files = base.discover_files(DAY_PREFIX)
    print(f"Dateien: {[f['filename'] for f in files]}")

    results = []
    with sync_playwright() as p:
        browser, its = base.login(p)
        try:
            print("Warte 15s auf itslearning-Indexierung...")
            time.sleep(15)
            for c in COURSES:
                print(f"\n=== {c['kuerzel']} (CourseID {c['id']}) ===")
                post_ok = base.post_message(its, c["id"], c["text"], files)
                results.append((c["kuerzel"], "OK" if post_ok else "MITTEILUNG FEHLGESCHLAGEN"))
        finally:
            browser.close()

    print("\n=== ZUSAMMENFASSUNG ===")
    for kuerzel, status in results:
        print(f"{kuerzel}: {status}")
