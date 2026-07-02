#!/usr/bin/env python3
"""
Toleranter Parser für die Fable-Batch-Ausgaben der AURORA Satz-Kur.

Warum nicht json.loads? Die Original-/Vorschlagssätze enthalten teils gerade
Anführungszeichen (") aus den Buchdialogen, die strenges JSON sprengen. Statt
an Quotes zu trennen, trennen wir an den FESTEN Feldnamen-Delimitern
(z. B. '", "revised":'), die in Prosa nicht vorkommen — robust gegen jedes
Anführungszeichen im Text.

Aufruf:
  python3 aurora_satzkur_parse.py data/satzkur/batch_00_raw.txt   # -> batch_00.json + Zusammenfassung
"""
import re, json, sys, os

def parse_batch(raw):
    result = {"kapitel": [], "konsistenz": []}
    # --- Rewrites ---
    rw_re = re.compile(
        r'"original"\s*:\s*"(?P<orig>.*?)"\s*,\s*"revised"\s*:\s*"(?P<rev>.*?)"\s*,\s*"grund"\s*:\s*"(?P<grund>.*?)"\s*\}',
        re.DOTALL)
    # Kapitelblöcke: "nr": N, "rewrites": [ ... ]  — grob nach nr-Vorkommen im kapitel-Teil
    # Wir ordnen jeden Rewrite dem letzten davor stehenden '"nr": N' zu.
    kapitel_split = raw.split('"konsistenz"')
    kap_part = kapitel_split[0]
    kons_part = '"konsistenz"' + kapitel_split[1] if len(kapitel_split) > 1 else ""

    # Positionen der "nr": N Marker im Kapitel-Teil
    nr_markers = [(m.start(), int(m.group(1)))
                  for m in re.finditer(r'"nr"\s*:\s*(\d+)', kap_part)]

    def nr_for(pos):
        cur = None
        for start, nr in nr_markers:
            if start <= pos:
                cur = nr
            else:
                break
        return cur

    kap_map = {}
    for m in rw_re.finditer(kap_part):
        nr = nr_for(m.start())
        kap_map.setdefault(nr, []).append({
            "original": m.group("orig"),
            "revised": m.group("rev"),
            "grund": m.group("grund"),
        })
    for nr in sorted(kap_map, key=lambda x: (x is None, x)):
        result["kapitel"].append({"nr": nr, "rewrites": kap_map[nr]})

    # --- Konsistenz ---
    ks_re = re.compile(
        r'"nr"\s*:\s*(?P<nr>\d+)\s*,\s*"typ"\s*:\s*"(?P<typ>.*?)"\s*,\s*"fund"\s*:\s*"(?P<fund>.*?)"\s*,\s*"problem"\s*:\s*"(?P<problem>.*?)"\s*,\s*"vorschlag"\s*:\s*"(?P<vorschlag>.*?)"\s*\}',
        re.DOTALL)
    for m in ks_re.finditer(kons_part):
        result["konsistenz"].append({
            "nr": int(m.group("nr")), "typ": m.group("typ"),
            "fund": m.group("fund"), "problem": m.group("problem"),
            "vorschlag": m.group("vorschlag"),
        })
    return result

def main():
    raw_path = sys.argv[1]
    raw = open(raw_path, encoding="utf-8").read()
    res = parse_batch(raw)
    out_path = raw_path.replace("_raw.txt", ".json")
    json.dump(res, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    nrw = sum(len(k["rewrites"]) for k in res["kapitel"])
    print(f"{os.path.basename(raw_path)}: {nrw} Satz-Umbauten, {len(res['konsistenz'])} Konsistenz-Funde → {os.path.basename(out_path)}")
    for k in res["kapitel"]:
        print(f"  Kap {k['nr']}: {len(k['rewrites'])} Umbauten")

if __name__ == "__main__":
    main()
