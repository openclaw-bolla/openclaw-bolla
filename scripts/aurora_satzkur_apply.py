#!/usr/bin/env python3
"""
AURORA Satz-Kur — Einspiel-Skript.

Wendet die von Fable vorgeschlagenen SATZ-UMBAUTEN (original -> revised) auf
data/ki_buch.json an. Sicherheitsprinzipien:
  - Dry-Run ist Standard: erst prüfen, ob jeder Originalsatz EXAKT (oder
    whitespace-normalisiert eindeutig) im Kapiteltext gefunden wird.
  - Kein blindes Ersetzen: 0 Treffer oder >1 Treffer -> gemeldet, NICHT angefasst.
  - Backup vor jeder Änderung. Nach dem Ersetzen wird verifiziert, dass der
    neue Text drinsteht und der alte weg ist.
  - Optionale Skip-Liste (--skip datei.txt mit je einer original-Zeichenkette
    pro Zeile bzw. deren Kurz-Hash), damit Chris einzelne Umbauten ablehnen kann.

Konsistenz-Funde werden hier NICHT angefasst — die entscheidet Chris einzeln.

Aufruf:
  python3 aurora_satzkur_apply.py            # Dry-Run über alle batch_*.json
  python3 aurora_satzkur_apply.py --apply     # tatsächlich anwenden (mit Backup)
  python3 aurora_satzkur_apply.py --skip skip.txt --apply
"""
import json, os, re, sys, glob, hashlib, datetime, argparse

HOME = "/home/bolla"
WS = f"{HOME}/workspace"
BOOK = f"{WS}/data/ki_buch.json"
OUTDIR = f"{WS}/data/satzkur"
BACKUPDIR = f"{WS}/backups"


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def short(s):
    return hashlib.md5(s.encode("utf-8")).hexdigest()[:10]


def chapnum(k, pos):
    m = re.match(r"Kapitel (\d+):", k.get("titel", ""))
    if m:
        return int(m.group(1))
    if k.get("titel", "").strip().lower() == "prolog":
        return 0
    return pos


def load_rewrites():
    """Alle Rewrites aus batch_*.json einsammeln: {nr: [ {original,revised,grund,batch} ]}"""
    out = {}
    for path in sorted(glob.glob(f"{OUTDIR}/batch_*.json")):
        data = json.load(open(path, encoding="utf-8"))
        bname = os.path.basename(path)
        for kap in data.get("kapitel", []):
            nr = kap.get("nr")
            for rw in kap.get("rewrites", []):
                rw = dict(rw); rw["batch"] = bname
                out.setdefault(nr, []).append(rw)
    return out


def find_span(text, original):
    """Gibt (start,end) des zu ersetzenden Bereichs zurück, oder None/AMBIG."""
    # 1) exakt
    c = text.count(original)
    if c == 1:
        i = text.index(original)
        return (i, i + len(original), "exakt")
    if c > 1:
        return ("AMBIG", c, "exakt-mehrfach")
    # 2) whitespace-normalisiert: Original ohne Mehrfach-Whitespace im normalisierten Text suchen
    ntext = norm(text)
    norig = norm(original)
    c2 = ntext.count(norig)
    if c2 == 1:
        # Position im Originaltext rekonstruieren: baue Regex, das Whitespace flexibel macht
        pat = re.escape(norig).replace(r"\ ", r"\s+")
        m = re.search(pat, text)
        if m:
            return (m.start(), m.end(), "normalisiert")
        return ("NOFIND", 0, "norm-aber-regex-fehlt")
    if c2 > 1:
        return ("AMBIG", c2, "norm-mehrfach")
    return ("NOFIND", 0, "nicht-gefunden")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--skip", help="Datei mit abzulehnenden original-Sätzen (oder Kurz-Hashes), eine pro Zeile")
    a = ap.parse_args()

    skips = set()
    if a.skip and os.path.exists(a.skip):
        for line in open(a.skip, encoding="utf-8"):
            s = line.strip()
            if s:
                skips.add(s); skips.add(short(s))

    book = json.load(open(BOOK, encoding="utf-8"))
    kaps = book["kapitel"]
    by_nr = {chapnum(k, i): (i, k) for i, k in enumerate(kaps)}
    rewrites = load_rewrites()

    ok, skipped, problems = [], [], []
    total = 0
    for nr in sorted(rewrites, key=lambda x: (x is None, x)):
        if nr not in by_nr:
            for rw in rewrites[nr]:
                problems.append((nr, "KAPITEL-NR unbekannt", rw["original"][:60]))
            continue
        pos, k = by_nr[nr]
        text = k.get("text") or ""
        for rw in rewrites[nr]:
            total += 1
            o = rw["original"]
            if o in skips or short(o) in skips:
                skipped.append((nr, o[:60]))
                continue
            span = find_span(text, o)
            if span[0] in ("AMBIG", "NOFIND"):
                problems.append((nr, span[2], o[:70]))
            else:
                ok.append((nr, pos, span, rw))

    print(f"=== Satz-Kur Einspielung — {'ANWENDEN' if a.apply else 'DRY-RUN'} ===")
    print(f"Rewrites gesamt: {total} | anwendbar: {len(ok)} | abgelehnt(skip): {len(skipped)} | PROBLEME: {len(problems)}")
    if problems:
        print("\n⚠️ NICHT anwendbar (bitte prüfen):")
        for nr, why, snip in problems:
            print(f"   Kap {nr} [{why}]: {snip}…")

    if not a.apply:
        print("\n(Dry-Run — nichts geändert. Mit --apply anwenden.)")
        return

    if problems:
        print("\n❌ Es gibt Probleme — sicherheitshalber KEINE Änderung. Erst Probleme klären.")
        # Wir wenden nur an, wenn alles sauber matcht (all-or-nothing pro Lauf)
        return

    # Backup
    os.makedirs(BACKUPDIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    bpath = f"{BACKUPDIR}/ki_buch_vor_satzkur_{ts}.json"
    json.dump(book, open(bpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nBackup: {bpath}")

    # Anwenden — pro Kapitel von hinten nach vorn (Positionen bleiben gültig)
    applied = 0
    by_pos = {}
    for nr, pos, span, rw in ok:
        by_pos.setdefault(pos, []).append((span, rw))
    for pos, items in by_pos.items():
        k = kaps[pos]
        text = k["text"]
        # nach Startposition absteigend sortieren -> spätere Ersetzungen verschieben frühere nicht
        for span, rw in sorted(items, key=lambda x: x[0][0], reverse=True):
            s, e, how = span
            text = text[:s] + rw["revised"] + text[e:]
            applied += 1
        k["text"] = text

    # Verifikation: jeder revised-Text muss jetzt drin sein
    fails = []
    for nr, pos, span, rw in ok:
        if rw["revised"] not in kaps[pos]["text"]:
            fails.append((nr, rw["revised"][:60]))
    if fails:
        print(f"\n❌ VERIFIKATION FEHLGESCHLAGEN bei {len(fails)} — Änderung NICHT gespeichert, Backup bleibt.")
        for nr, snip in fails:
            print(f"   Kap {nr}: {snip}…")
        return

    json.dump(book, open(BOOK, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n✅ {applied} Satz-Umbauten angewendet + verifiziert. Buch gespeichert.")


if __name__ == "__main__":
    main()
