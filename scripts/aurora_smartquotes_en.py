#!/usr/bin/env python3
"""
AURORA EN — Smart-Quotes-Konvertierung.
Wandelt gerade ASCII-Anführungszeichen ("..." / '...') in typografische
englische Anführungszeichen (“ ” ‘ ’) um. Port des bewährten SmartyPants-
EducateQuotes-Algorithmus mit Unicode-Ausgabe.

Wirkt NUR auf gerade Anführungszeichen → idempotent (zweiter Lauf macht nichts).
Lässt *kursiv*-Marker, ## Zwischenüberschriften, --- Szenentrenner und em-dashes
unangetastet (nur " und ' werden ersetzt).

Aufruf:  python3 aurora_smartquotes_en.py        (schreibt in die EN-JSON zurück)
         python3 aurora_smartquotes_en.py --dry  (nur Statistik, nichts schreiben)
"""
import json, re, sys
from pathlib import Path

JSON_PATH = "/home/bolla/workspace/data/ki_buch_en_adapted.json"
# Felder, die im Buch erscheinen (Meta-/Arbeitsfelder bleiben unangetastet):
BOOK_FIELDS = ["titel", "untertitel", "vorwort", "impressum", "vorspann",
               "epilog", "epilog_untertitel", "ueber_autor", "danksagung",
               "rezensions_bitte"]

LSQ, RSQ = "‘", "’"   # ‘ ’
LDQ, RDQ = "“", "”"   # “ ”

_dec_dashes = r"--|–|—"
_close = r"[^\ \t\r\n\[\{\(\-]"      # Zeichen, hinter dem ein " schließt
_punct = r"""[!"#\$\%'()*+,.\/:;<=>?@\[\\\]\^_`{|}~-]"""

# Häufige Wörter, die mit einem Apostroph BEGINNEN (kein öffnendes Zitat!)
_lead_contractions = re.compile(
    r"‘(em|tis|twas|cause|round|bout|til|fraid|nother|n)\b", re.I)


def educate(text):
    if not text:
        return text
    # Zitat ganz am Anfang, gefolgt von Satzzeichen → schließend (Brute Force)
    text = re.sub(r"^'(?=%s\B)" % _punct, RSQ, text)
    text = re.sub(r'^"(?=%s\B)' % _punct, RDQ, text)
    # Verschachtelte Sets:  "'  und  '"
    text = re.sub(r"\"'(?=\w)", LDQ + LSQ, text)
    text = re.sub(r"'\"(?=\w)", LSQ + LDQ, text)
    # Jahrzehnte: '80s  (kein \b — zwischen Space und ' gibt es keine Wortgrenze)
    text = re.sub(r"'(?=\d{2}s\b)", RSQ, text)

    # Öffnende einfache
    text = re.sub(r"(\s|--|%s)'(?=\w)" % _dec_dashes, r"\1" + LSQ, text)
    # Schließende einfache (vor Nicht-Space / Plural-s / Ziffer ausnehmen)
    text = re.sub(r"(%s)'(?!\s|s\b|\d)" % _close, r"\1" + RSQ, text)
    text = re.sub(r"(%s)'(\s|s\b)" % _close, r"\1" + RSQ + r"\2", text)
    # Reste = öffnend
    text = text.replace("'", LSQ)

    # Öffnende doppelte
    text = re.sub(r'(\s|--|%s)"(?=\w)' % _dec_dashes, r"\1" + LDQ, text)
    # Schließende doppelte
    text = re.sub(r'"(?=\s)', RDQ, text)
    text = re.sub(r'(%s)"' % _close, r"\1" + RDQ, text)
    # Reste = öffnend
    text = text.replace('"', LDQ)

    # Korrektur: fälschlich als öffnendes ‘ erkannte führende Apostroph-Wörter
    text = _lead_contractions.sub(RSQ + r"\1", text)
    return text


def main():
    dry = "--dry" in sys.argv
    data = json.loads(Path(JSON_PATH).read_text(encoding="utf-8"))

    before_d = before_s = 0
    changed = 0

    def count(s):
        return s.count('"'), s.count("'")

    for f in BOOK_FIELDS:
        v = data.get(f)
        if isinstance(v, str):
            d, s = count(v); before_d += d; before_s += s
            nv = educate(v)
            if nv != v:
                changed += 1
                if not dry:
                    data[f] = nv

    for k in data.get("kapitel", []):
        for key in ("titel", "text"):
            v = k.get(key)
            if isinstance(v, str):
                d, s = count(v); before_d += d; before_s += s
                nv = educate(v)
                if nv != v and not dry:
                    k[key] = nv

    # Restkontrolle nach Konvertierung
    rest = 0
    src = data if not dry else json.loads(Path(JSON_PATH).read_text(encoding="utf-8"))
    if not dry:
        for f in BOOK_FIELDS:
            if isinstance(data.get(f), str):
                rest += data[f].count('"') + data[f].count("'")
        for k in data.get("kapitel", []):
            rest += str(k.get("titel", "")).count('"') + str(k.get("titel", "")).count("'")
            rest += str(k.get("text", "")).count('"') + str(k.get("text", "")).count("'")

    print(f"Gerade Zeichen vorher:  \" = {before_d}   ' = {before_s}")
    print(f"Geänderte Felder/Texte: {changed} Buch-Felder + Kapitel")
    if not dry:
        print(f"Verbleibende gerade \" oder ' nach Konvertierung: {rest}")
        Path(JSON_PATH).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"✅ Geschrieben: {JSON_PATH}")
    else:
        print("(dry run — nichts geschrieben)")


if __name__ == "__main__":
    main()
