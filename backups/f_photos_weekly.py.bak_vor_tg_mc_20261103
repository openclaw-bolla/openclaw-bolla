#!/usr/bin/env python3
"""Wochen-Neubau des Foto-Pools fuer Renis Seite /f (Cron So 03:00).
Baut 120 neue Fotos (nie gezeigte, f_used.json), entfernt Beinahe-Dubletten, tauscht den Pool atomar,
merkt sich alle Fotos dauerhaft als gezeigt und meldet per Telegram. Bei Fehler bleibt der alte Pool live."""
import json, os, shutil, subprocess, sys, itertools, urllib.request
from PIL import Image

MC = "/home/bolla/workspace/mission-control"
LIVE, STAGE, PREV = f"{MC}/f-photos", f"{MC}/f-photos_staging", f"{MC}/f-photos_prev"
USED = "/home/bolla/workspace/scripts/f_used.json"
CFG = json.load(open("/home/bolla/workspace/config/telegram_bot.json"))
NEAR_DUP = 40      # Hamming-Distanz (von 256 Bit) darunter = Beinahe-Dublette
MIN_POOL = 105     # 7 Tage x 15


def tg(t):
    try:
        urllib.request.urlopen(urllib.request.Request(
            f"https://api.telegram.org/bot{CFG['bot_token']}/sendMessage",
            data=json.dumps({"chat_id": CFG["chris_id"], "text": t}).encode(),
            headers={"Content-Type": "application/json"}), timeout=20)
    except Exception as e:
        print("telegram fail", e)


def dh(p):
    px = list(Image.open(p).convert("L").resize((17, 16)).getdata())
    return sum(1 << (r * 16 + c) for r in range(16) for c in range(16) if px[r * 17 + c] > px[r * 17 + c + 1])


def main():
    shutil.rmtree(STAGE, ignore_errors=True)
    r = subprocess.run([sys.executable, "/home/bolla/workspace/scripts/build_f_photos.py"],
                       capture_output=True, text=True, timeout=3300)
    mf = f"{STAGE}/manifest.json"
    if r.returncode != 0 or not os.path.exists(mf):
        return tg("⚠️ Foto-Pool Wochen-Neubau FEHLGESCHLAGEN – alter Pool bleibt live.\n" + (r.stderr or r.stdout)[-500:])
    man = json.load(open(mf))
    man = [x for x in man if os.path.exists(f"{STAGE}/{x['src'].split('/')[-1]}")]
    hs = {x["src"]: dh(f"{STAGE}/{x['src'].split('/')[-1]}") for x in man}
    drop = set()
    for a, b in itertools.combinations(man, 2):
        if a["src"] in drop or b["src"] in drop:
            continue
        if bin(hs[a["src"]] ^ hs[b["src"]]).count("1") <= NEAR_DUP:
            drop.add(b["src"])
    for x in man:
        if x["src"] in drop:
            os.remove(f"{STAGE}/{x['src'].split('/')[-1]}")
    man = [x for x in man if x["src"] not in drop]
    if len(man) < MIN_POOL:
        return tg(f"⚠️ Foto-Pool Neubau nur {len(man)} Fotos (<{MIN_POOL}) – alter Pool bleibt live.")
    json.dump(man, open(mf, "w"), ensure_ascii=False, indent=1)
    # Tausch
    shutil.rmtree(PREV, ignore_errors=True)
    shutil.copy(f"{LIVE}/history.jsonl", f"{STAGE}/history.jsonl") if os.path.exists(f"{LIVE}/history.jsonl") else None
    os.rename(LIVE, PREV)
    os.rename(STAGE, LIVE)
    try:
        os.remove(f"{LIVE}/served.json")
    except OSError:
        pass
    used = set(json.load(open(USED))) if os.path.exists(USED) else set()
    used |= {x["orig"] for x in man if x.get("orig")}
    json.dump(sorted(used), open(USED, "w"), ensure_ascii=False, indent=0)
    tg(f"✅ Foto-Pool /f neu gebaut: {len(man)} frische Fotos ({len(drop)} Beinahe-Dubletten entfernt), "
       f"{len(used)} insgesamt schon verbraucht 🐾")


main()
