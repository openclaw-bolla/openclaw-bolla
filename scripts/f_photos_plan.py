"""Zyklus-Vorplanung fuer Renis Fotoseite /f (21.09.2026).

Statt jeden Tag frisch zu wuerfeln, wird der GANZE Pool auf einmal auf Tage verteilt (120 Fotos -> 8 Tage a 15),
Themengruppen gleichmaessig ueber die Tage gestreut, gleiche Gruppe nie direkt hintereinander. Die Tageslisten
liegen als `queue` in served.json und werden pro Tagesabruf (nicht datumsgebunden) verbraucht.
Reine Funktionen ohne Server-Abhaengigkeit -> per Simulation testbar (siehe __main__)."""
import random
import re

DAILY = 15


def group_of(item):
    """Themengruppe eines Manifest-Eintrags {src, cap, folder}. Reihenfolge = Prioritaet."""
    fol = (item.get("folder") or "").lower()
    cap = (item.get("cap") or "").lower()
    both = fol + " | " + cap
    if "/robin" in fol or cap.startswith("robin"):
        return "robin"
    if "weihnacht" in both or "neues jahr" in both or "silvester" in both:
        return "weihnachten"
    if re.search(r"geburtstag|taufe|hochzeit|konfirmation|feier|jubil|party|fasching|ostern feier", both):
        return "feiern"
    if "hagenbeck" in both or "hamburg" in both:
        return "hamburg"
    if "norderstedt" in both:
        return "norderstedt"
    top = fol.split("/")[0]
    if re.match(r"(usa|new york|florida)", top) or re.search(r"\busa\b|new york|florida|miami", cap):
        return "usa"
    if re.match(r"(italien|venedig|sizilien)", top) or re.search(r"italien|venedig|sizilien|rom\b", cap):
        return "italien"
    if re.match(r"(wien|zillertal|kitz|schladming|filzmoos|fiss|ischgl|sölden|warth|damüls|kaprun|zell am see)", top) \
            or "österreich" in cap:
        return "oesterreich"
    if top == "renis camera roll 09-06-16" or fol.endswith("/renate") or cap.startswith("renate"):
        return "renate"
    if top == "mandels":
        return "mandels"
    return top or "sonst"


def plan_cycle(pool, prev_picks=(), seed=None):
    """pool = Manifest-Liste. Gibt Liste von Tageslisten (jeweils src-Strings) zurueck."""
    rnd = random.Random(seed)
    n_days = max(1, len(pool) // DAILY)
    cap = -(-len(pool) // n_days)            # aufrunden -> alle Fotos werden verplant
    groups = {}
    for it in pool:
        groups.setdefault(group_of(it), []).append(it)
    order = sorted(groups, key=lambda g: (-len(groups[g]), rnd.random()))
    days = [[] for _ in range(n_days)]
    d = rnd.randrange(n_days)
    for g in order:
        items = groups[g][:]
        rnd.shuffle(items)
        for it in items:
            tries = 0
            while len(days[d % n_days]) >= cap and tries < n_days:
                d += 1; tries += 1
            days[d % n_days].append(it)
            d += 1
    # Naht: Fotos von gestern nicht direkt am ersten Tag
    prev = set(prev_picks)
    if prev and n_days > 1:
        for it in [x for x in days[0] if x["src"] in prev]:
            for cand in reversed(days[1:]):
                swap = next((x for x in cand if x["src"] not in prev
                             and group_of(x) == group_of(it)), None) or \
                       next((x for x in cand if x["src"] not in prev), None)
                if swap:
                    days[0].remove(it); cand.remove(swap)
                    days[0].append(swap); cand.append(it)
                    break
    return [[it["src"] for it in _spread(day, rnd)] for day in days]


def _spread(day, rnd):
    """Reihenfolge im Tag: gleiche Gruppe (und gleicher Ordner) nicht direkt hintereinander."""
    rest = day[:]
    rnd.shuffle(rest)
    out = []
    while rest:
        last_g = group_of(out[-1]) if out else None
        last_f = out[-1].get("folder") if out else None
        cnt = {}
        for x in rest:
            cnt[group_of(x)] = cnt.get(group_of(x), 0) + 1
        good = [x for x in rest if group_of(x) != last_g and x.get("folder") != last_f]
        pool = good or [x for x in rest if group_of(x) != last_g] or rest
        pick = max(pool, key=lambda x: (cnt[group_of(x)], rnd.random()))   # groesste Restgruppe zuerst
        rest.remove(pick)
        out.append(pick)
    return out


if __name__ == "__main__":
    import json, sys, collections
    mf = sys.argv[1] if len(sys.argv) > 1 else "/home/bolla/workspace/mission-control/f-photos/manifest.json"
    pool = json.load(open(mf))
    by = {it["src"]: it for it in pool}
    print("Pool:", len(pool), "| Gruppen:", dict(collections.Counter(group_of(i) for i in pool).most_common()))
    plan = plan_cycle(pool, seed=42)
    seen = [s for day in plan for s in day]
    assert len(seen) == len(set(seen)) == len(pool), "Foto doppelt/fehlt im Zyklus!"
    for i, day in enumerate(plan, 1):
        gs = [group_of(by[s]) for s in day]
        adj = sum(1 for a, b in zip(gs, gs[1:]) if a == b)
        folders = [by[s].get("folder") for s in day]
        print(f"Tag {i}: {len(day)} Fotos | direkt gleiche Gruppe hintereinander: {adj} | "
              f"doppelte Ordner: {len(folders) - len(set(folders))} | Robin: {gs.count('robin')} | {dict(collections.Counter(gs).most_common(4))}")
    # Nahtpruefung neuer Zyklus
    plan2 = plan_cycle(pool, prev_picks=plan[-1], seed=7)
    print("Naht: Ueberschneidung letzter Tag alt / erster Tag neu:", len(set(plan[-1]) & set(plan2[0])))
