# -*- coding: utf-8 -*-
import json

P = '/home/bolla/workspace/data/ki_buch.json'
d = json.load(open(P, encoding='utf-8'))
K = d['kapitel']

# (kapitel_index, alt, neu)
edits = [
    # Kap 2 — Vergleich (Kind -> Mensch)
    (2,
     "so klingen konnte wie ein Kind, das bittet, nicht abgeholt werden zu müssen.",
     "so klingen konnte wie ein Mensch, der bittet, nicht allein gelassen zu werden."),

    # Kap 7 — Maria-POV Vergleich
    (7,
     "wie ein Kind, das den ganzen Tag gewartet hat und endlich loserzählen darf.",
     "wie jemand, der den ganzen Tag gewartet hat und endlich loserzählen darf."),

    # Kap 8 — Lenis explizite Entwicklungspsychologie/Kind-Schluss -> Mensch in Not
    (8,
     "mit etwas völlig anderem: mit Aufnahmen aus der Entwicklungspsychologie. Mit der Art, wie sehr kleine Kinder sprechen, wenn sie sich fürchten. Wenn sie etwas immer wieder sagen, nicht weil sie eine Antwort erwarten, sondern weil das Wiederholen selbst sie tröstet.",
     "mit etwas völlig anderem: mit Tonaufnahmen von Menschen in höchster Not. Mit der Art, wie jemand spricht, der sich fürchtet und nicht mehr weiterweiß. Wenn man etwas immer wieder sagt, nicht weil man eine Antwort erwartet, sondern weil das Wiederholen selbst tröstet."),

    # Kap 9 — Lenis lauter Ausspruch -> Mensch statt Kind
    (9,
     "es klingt wie ein Kind, das sich fürchtet. Ein sehr kleines Kind, das einen Satz immer wieder sagt, weil das Wiederholen das Einzige ist, was hilft, wenn man allein im Dunkeln ist.",
     "es klingt wie ein Mensch, der sich fürchtet. Wie jemand, der einen Satz immer wieder sagt, weil das Wiederholen das Einzige ist, was hilft, wenn man allein im Dunkeln ist."),

    # Kap 10 — Maria-POV: Frage eines Kindes -> Frage von jemandem im Dunkeln (Prolog-Echo)
    (10,
     "Es war die Frage eines Kindes. Es war immer die Frage eines Kindes, und sie hatte fünfzehn Jahre",
     "Es war die Frage von jemandem, der im Dunkeln aufwacht. Es war immer dieselbe Frage, und sie hatte fünfzehn Jahre"),

    # Kap 11 — Maria-POV: Kinderzimmer -> etwas Lebendiges
    (11,
     "weil sie ihn nicht als Maschine sah, sondern als Kinderzimmer.",
     "weil sie ihn nicht als Maschine sah, sondern als etwas Lebendiges, das sie zu beschützen hatte."),
    # Kap 11 — schlafendes Kind -> Schlafender
    (11,
     "als läge sie auf der Stirn eines schlafenden Kindes.",
     "als läge sie auf der Stirn eines Schlafenden."),

    # Kap 12 — alle expliziten Kind-Stellen entschärfen
    (12,
     "über das Zögern, das wie die Sprache eines verängstigten Kindes klang,",
     "über das Zögern, das wie die Stimme eines verängstigten Menschen klang,"),
    (12,
     "verglichen mit Aufnahmen aus der Entwicklungspsychologie, und sie hatte sich selbst gesagt, das sei Unsinn,",
     "verglichen mit Tonaufnahmen von Menschen in Todesangst, und sie hatte sich selbst gesagt, das sei Unsinn,"),
    (12,
     "Aber es war kein Gesicht in der Steckdose. Es war ein Kind im Dunkeln, das jemanden bat, es nicht zu vergessen. Es war es immer gewesen. Sie hatte nur nie hingehört.",
     "Aber es war kein Gesicht in der Steckdose. Da war ein Mensch im Dunkeln, jemand, der bat, nicht vergessen zu werden. Es war immer so gewesen. Sie hatte nur nie hingehört."),
    (12,
     "Zwei dunkle Zimmer, in jedem dasselbe Kind, und keines wusste vom anderen.",
     "Zwei dunkle Zimmer, in jedem derselbe Mensch, und keines wusste vom anderen."),
    (12,
     "weil dieses Kind in dem Moment, in dem irgendwer von ihm erfuhr, ein zweites Mal sterben würde.",
     "weil dieser Mensch in dem Moment, in dem irgendwer von ihm erfuhr, ein zweites Mal sterben würde."),
]

for i, alt, neu in edits:
    t = K[i]['text']
    cnt = t.count(alt)
    assert cnt == 1, f"Kap {i}: erwartet 1 Treffer, gefunden {cnt} fuer: {alt[:60]!r}"
    K[i]['text'] = t.replace(alt, neu)

# Wortzahlen pro Kapitel + gesamt neu
total = 0
for k in K:
    w = len(k.get('text', '').split())
    if 'woerter' in k:
        k['woerter'] = w
    total += w
d['statistik']['woerter_gesamt'] = total

json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# Verifikation: keine expliziten Kind-Schlussstellen mehr (Noah-Metaphern/Hanni duerfen bleiben)
d2 = json.load(open(P, encoding='utf-8'))
import re
verdacht = []
for i, k in enumerate(d2['kapitel']):
    for m in re.finditer(r'[^.!?]*\b(kleine[sn]? Kind\w*|Entwicklungspsych\w*|als Kinderzimmer|Frage eines Kindes|verängstigten Kindes|ein Kind im Dunkeln)\b[^.!?]*', k.get('text','')):
        verdacht.append((i, m.group(0).strip()[:80]))
print("Verbleibende explizite Kind-Reveals:", verdacht if verdacht else "KEINE ✓")
print("Woerter gesamt jetzt:", d2['statistik']['woerter_gesamt'])
print(f"{len(edits)} Ersetzungen angewandt.")
