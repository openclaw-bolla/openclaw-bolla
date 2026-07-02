#!/usr/bin/env python3
"""
AURORA Satz-Kur — Extraktion (kostenlos, reines Python).

Baut zwei Arbeitsgrundlagen für den Fable-Lauf:
1. satzkur_worklist.json — pro Kapitel die Schachtelsätze (>=35 Wörter) plus die
   Kapitel-Schlusssätze >35 Wörter (Fables Stufe-1-Empfehlung). Das ist die
   Ziel-Liste für die Satz-Kur.
2. konsistenz_index.json — Namen- und Zahlen-Index pro Kapitel als Referenz für
   den Konsistenz-Check (Personen/Orte/Zahlen/Daten). Fable prüft damit
   kapitelübergreifend auf Widersprüche.

Nichts wird verändert — nur gelesen und indexiert.
"""
import json, re, os

HOME = "/home/bolla"
WS = f"{HOME}/workspace"
BOOK = f"{WS}/data/ki_buch.json"
OUTDIR = f"{WS}/data/satzkur"
os.makedirs(OUTDIR, exist_ok=True)

LONG = 35  # Wortgrenze für "Schachtelsatz"

# Kanonische Namen (aus Buch-Metadaten) — Referenz fürs Konsistenz-Auge
CANON = {
    "Marlie Braun": ["Marlie", "Braun"],
    "Noah Khoury": ["Noah", "Khoury"],
    "Leni Yilmaz": ["Leni", "Yilmaz"],
    "Theo Dreyer": ["Theo", "Dreyer"],
    "Maria Santos": ["Maria", "Santos"],
    "Aurora Santos (geheim)": ["Aurora"],
    "Günter Brandt": ["Günter", "Brandt"],
    "Hannelore 'Hanni' Brandt": ["Hannelore", "Hanni"],
}
# Bekannte Falsch-Nachnamen / Verwechslungsgefahr (aus früheren Fixes gelernt)
NAME_ALARM = ["Weber", "Khoury", "Santos", "Braun", "Dreyer", "Yilmaz", "Brandt"]

WORDNUM = (r"\b(?:null|eins?|zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|"
           r"dreizehn|vierzehn|fünfzehn|sechzehn|siebzehn|achtzehn|neunzehn|zwanzig|"
           r"einundzwanzig|zweiundzwanzig|dreiundzwanzig|dreißig|vierzig|fünfzig|"
           r"sechzig|siebzig|achtzig|neunzig|hundert|tausend|million(?:en)?|milliard(?:en)?|"
           r"billion(?:en)?)\b")

def clean(text):
    """Markdown-Deko (Szene-Header, **, *) für die Satzanalyse entfernen."""
    # Fettgedruckte Zeilen (Szene-Marker) am Anfang: **NovaTech, ... Uhr**
    t = text
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\*(.+?)\*", r"\1", t)
    return t

def sentences(text):
    """Grobe Satzsegmentierung (DE). Für Längen-Flagging ausreichend."""
    t = clean(text)
    # Zeilenumbrüche zu Leerzeichen
    t = re.sub(r"\s+", " ", t).strip()
    # An .!?… splitten, wenn danach Leerzeichen + Großbuchstabe/Anführung folgt
    parts = re.split(r'(?<=[.!?…])\s+(?=[»„"A-ZÄÖÜ])', t)
    return [p.strip() for p in parts if p.strip()]

def wc(s):
    return len(re.findall(r"\S+", s))

def chapnum(k, pos=None):
    m = re.match(r"Kapitel (\d+):", k.get("titel", ""))
    if m:
        return int(m.group(1))
    t = k.get("titel", "")
    if t.strip().lower() == "prolog":
        return 0
    # Fallback: Position = Nummer (Prolog=0, Kap N an pos N — im Buch durchgängig so)
    return pos

def main():
    d = json.load(open(BOOK, encoding="utf-8"))
    kaps = d["kapitel"]
    worklist = []
    index = []
    total_long = 0
    for i, k in enumerate(kaps):
        text = k.get("text") or ""
        titel = k.get("titel", "")
        nr = chapnum(k, i)
        sents = sentences(text)
        longs = []
        for si, s in enumerate(sents):
            n = wc(s)
            if n >= LONG:
                longs.append({"idx": si, "words": n, "is_last": si == len(sents) - 1, "sentence": s})
        # Kapitel-Schlusssatz separat markieren (auch wenn knapp unter 35, wenn >30)
        last_wc = wc(sents[-1]) if sents else 0
        total_long += len(longs)
        worklist.append({
            "pos": i, "kapitel": nr, "titel": titel,
            "satz_count": len(sents), "long_count": len(longs),
            "last_sentence_words": last_wc,
            "long_sentences": longs,
        })
        # --- Konsistenz-Index ---
        names_found = {}
        for canon, variants in CANON.items():
            hits = sum(len(re.findall(r"\b" + re.escape(v) + r"\b", text)) for v in variants)
            if hits:
                names_found[canon] = hits
        alarms = [w for w in NAME_ALARM if re.search(r"\b" + w + r"\b", text)]
        digits = re.findall(r"\b\d[\d.,]*\b", text)
        years = re.findall(r"\b(?:19|20)\d{2}\b", text)
        wordnums = re.findall(WORDNUM, text, flags=re.IGNORECASE)
        jahre = re.findall(r"\b(\w+)\s+Jahren?\b", text)  # "22 Jahren", "zweiundzwanzig Jahre"
        tage = re.findall(r"\b(\w+)\s+Tagen?\b", text)
        index.append({
            "pos": i, "kapitel": nr, "titel": titel,
            "names": names_found,
            "name_tokens_present": alarms,
            "digits": digits[:60],
            "years": sorted(set(years)),
            "wordnums": wordnums,
            "jahr_spans": jahre[:30],
            "tag_spans": tage[:30],
        })

    json.dump(worklist, open(f"{OUTDIR}/satzkur_worklist.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    json.dump(index, open(f"{OUTDIR}/konsistenz_index.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # Zusammenfassung
    print(f"Kapitel: {len(kaps)}")
    print(f"Schachtelsätze (>= {LONG} Wörter) gesamt: {total_long}")
    print()
    print("Pro Kapitel (nur die mit Schachtelsätzen):")
    for w in worklist:
        if w["long_count"]:
            print(f"  Kap {str(w['kapitel']):>3} — {w['long_count']:>2} lange Sätze "
                  f"(Schlusssatz {w['last_sentence_words']} W) — {w['titel'][:45]}")
    print()
    print(f"→ Worklist:  {OUTDIR}/satzkur_worklist.json")
    print(f"→ Index:     {OUTDIR}/konsistenz_index.json")

if __name__ == "__main__":
    main()
