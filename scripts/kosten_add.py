#!/usr/bin/env python3
"""
Bolla-Kosten-Ledger von Hand füttern — für kostenpflichtige Bild-Calls, die
NICHT durch die MC-API laufen (v.a. MAI-Image-Aufträge direkt aus dem Terminal).

Der Ledger (data/api_kosten_ledger.json) wird auch von scripts/mission_control_api.py
gelesen; `/api/kosten` rechnet daraus die Monatskosten der Gemini-/Azure-Kacheln hoch.

Nutzung:
    python3 scripts/kosten_add.py mai 3                "3 MAI-Bilder"
    python3 scripts/kosten_add.py mai 1 "Cover XY, Terminal-Direktcall"
    python3 scripts/kosten_add.py gemini 2 "Nano-Banana-Test"
    python3 scripts/kosten_add.py --list                aktuellen Monat zeigen

Preise MÜSSEN mit mission_control_api.py (GEMINI_IMG_PREIS / MAI_IMG_PREIS) übereinstimmen.
"""
import json, os, sys
from datetime import datetime

LEDGER = os.path.join(os.path.dirname(__file__), "..", "data", "api_kosten_ledger.json")
LEDGER = os.path.abspath(LEDGER)

PREISE = {          # Service-Key -> €/Bild  (Spiegel von mission_control_api.py)
    "gemini_image":   0.04,    # Nano Banana (gemini-2.5-flash-image)
    "gemini_analyse": 0.0005,  # Foto-Analyse
    "mai_image":      0.10,    # MAI-Image-2.5 über Azure (Mittel 0,08–0,13)
}
ALIAS = {"mai": "mai_image", "gemini": "gemini_image", "analyse": "gemini_analyse",
         "gemini-analyse": "gemini_analyse"}


def load():
    try:
        with open(LEDGER, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def month_summary(eintraege, yyyymm=None):
    yyyymm = yyyymm or datetime.now().strftime("%Y-%m")
    sums, counts = {}, {}
    for e in eintraege:
        if e.get("datum", "").startswith(yyyymm):
            s = e.get("service", "?")
            sums[s] = round(sums.get(s, 0.0) + e.get("betrag", 0.0), 4)
            counts[s] = counts.get(s, 0) + 1
    return yyyymm, sums, counts


def show():
    ym, sums, counts = month_summary(load())
    print(f"Ledger: {LEDGER}")
    print(f"Monat {ym}:")
    if not sums:
        print("  (noch nichts erfasst)")
    for s in sorted(sums):
        print(f"  {s:16s} {counts[s]:3d} Stück   {sums[s]:6.2f} €")
    print(f"  {'SUMME':16s} {sum(counts.values()):3d} Stück   {sum(sums.values()):6.2f} €")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("--list", "-l", "--show"):
        show()
        return
    if len(args) < 2:
        print(__doc__)
        sys.exit(1)

    service = ALIAS.get(args[0].lower(), args[0].lower())
    if service not in PREISE:
        print(f"Unbekannter Service '{args[0]}'. Erlaubt: {', '.join(ALIAS)} (bzw. {', '.join(PREISE)})")
        sys.exit(1)
    try:
        n = int(args[1])
    except ValueError:
        print(f"Anzahl muss eine Zahl sein, nicht '{args[1]}'")
        sys.exit(1)
    note = " ".join(args[2:]) or "Terminal-Direktcall"
    preis = PREISE[service]

    eintraege = load()
    now = datetime.now()
    for _ in range(n):
        eintraege.append({
            "ts": now.strftime("%Y-%m-%d %H:%M:%S"),
            "datum": now.strftime("%Y-%m-%d"),
            "service": service,
            "betrag": preis,
            "info": note + " [manuell via kosten_add.py]",
        })
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as f:
        json.dump(eintraege, f, ensure_ascii=False, indent=2)

    print(f"+ {n}× {service} à {preis:.4f} €  =  {n * preis:.2f} €   ({note})")
    show()


if __name__ == "__main__":
    main()
