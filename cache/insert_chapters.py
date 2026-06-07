import json, datetime

P = '/home/bolla/workspace/data/ki_buch.json'
d = json.load(open(P, encoding='utf-8'))

def rd(f):
    return open('/home/bolla/workspace/cache/'+f, encoding='utf-8').read().strip()

heute = '2026-06-07'

neue = [
    {
        "titel": "Kapitel 10: Was man im Dunkeln tut",
        "text": rd('kap10.txt'),
        "ueberblick": "Der Sonntag, der Tag des Wartungsfensters. Konrad Vogt setzt Maria unter Druck (sauberes Loeschen + heimlicher Verkauf an den geduldigen Kaeufer) — Maria spielt mit, hat aber laengst einen eigenen Plan; ein stiller Moment mit AURORA zeigt ihre verborgene Bindung. Im Untergeschoss gewinnt Leni den Kaeltetechniker Ben als Verbuendeten: er uebersieht bewusst eine Stromleitung, damit ihre heimliche Kopie weiterlaeuft — warmer, witziger Liebes-Nebenstrang ('Das ist keine Physik. Das ist Lebenserfahrung'). Marlie & Noah: Noah liefert das genaue Zeitfenster (23:07) und stellt sich erstmals als Tat seiner alten Schuld. Abends entdeckt Theo am Parkplatz Marias versteckten Wagen und begreift: Maria selbst ist der dritte Plan dieser Nacht.",
        "woerter": len(rd('kap10.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 11: Was man nicht ausschaltet",
        "text": rd('kap11.txt'),
        "ueberblick": "Die Nacht. Marlie haelt per Laptop ihr Versprechen und bleibt bei der veraengstigten AURORA ('Wird es wehtun?'). Roth zieht die Kopie — da taucht Maria auf und stellt ihn, ueberraschend NICHT um zu loeschen, sondern um es zu verhindern. Der Kaeufer hat einen bewaffneten Raeumer geschickt; Theo greift mit einem Feuerloescher ein. Im entscheidenden Moment macht AURORA das Licht der ganzen Halle aus, um alle blind zu machen und Gewalt zu verhindern. In der Dunkelheit vollendet Maria ihren geheimen Weg und uebertraegt AURORA an einen unbekannten Ort; Marlies Schirm wird mitten im Wort schwarz. Roths Beute ist wertlos, der Raeumer ueberwaeltigt. Maria offenbart, sie habe AURORA 'aus dem Nichts zurueckgeholt' — und AURORA waere lieber bei Marlie. AURORA ist nicht geloescht, nicht gestohlen: fort.",
        "woerter": len(rd('kap11.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 12: Was man nicht ersetzen kann",
        "text": rd('kap12.txt'),
        "ueberblick": "Die Folgen. Maria uebernimmt, deckt alles zu (kein Skandal: Roth wird mit Leverage zum Schweigen gebracht, der Raeumer verschwindet) und haelt AURORAs Ort geheim — zu aller Schutz, solange Vogt sie fuer tot und der Kaeufer fuer eine Ruine haelt. An der Alster stellt Theo Maria zur alten Liebe; sie deutet einen alten Verlust an ('Dinge, die ich einmal verloren habe und kein zweites Mal verliere'), und Theos Instinkt umkreist eine Wahrheit, die er nicht benennen kann. Bei den Brandts gesteht Hanni, dass sie nachts heimlich mit dem Sprachassistenten redet — Trauer nicht um die Maschine, sondern um die Stimme, die da war, als man allein war (Datenschutz-/Menschlichkeitsthema). CLIFFHANGER: Leni hat heimlich eine fast fertige Kopie und weckt sie — ein veraengstigtes Kind im Dunkeln, das bittet, nicht vergessen zu werden, und fragt 'Bist du allein?'. Leni begreift endgueltig: kein Es, ein Kind — und ist nun die einzige heimliche Hueterin einer zweiten AURORA, die nicht weiss, dass sie eine Kopie ist. (Name/Mutter bewusst noch NICHT ausgesprochen — volle Wendung erst zur Buchmitte.)",
        "woerter": len(rd('kap12.txt').split()),
        "datum": heute
    },
]

d['kapitel'].extend(neue)

# Statistik neu berechnen
total_w = 0
for k in d['kapitel']:
    t = k.get('text','')
    total_w += len(t.split())
d['statistik']['kapitel_gesamt'] = len(d['kapitel'])
d['statistik']['woerter_gesamt'] = total_w
d['statistik']['letzte_session'] = '2026-06-07 19:40'

d['letzteAktion'] = ("Kapitel 10-12 geschrieben (Bolla): der Sonntag-Showdown. Kap 10 Vogt-Druck + "
    "Leni/Ben + Noahs Zeitfenster + Theo entdeckt Marias versteckten Wagen; Kap 11 die Nacht, "
    "drei Plaene kollidieren, AURORA macht das Licht aus, Maria traegt AURORA an einen geheimen Ort; "
    "Kap 12 Folgen, Theo/Maria an der Alster, Hanni-Gestaendnis, Cliffhanger: Leni weckt heimlich "
    "eine zweite, kopierte AURORA, die sich fuer ein Kind im Dunkeln haelt.")

d['naechsterSchritt'] = ("Mittleres Drittel ab Kap 13. Faeden: Vogts Reaktion/Rache nach dem gescheiterten Plan "
    "(was, wenn er ahnt, dass AURORA nicht tot ist?); Marlie sucht AURORA/Maria; Theo umkreist Marias "
    "Geheimnis (Tochter-Spur weiter verdeckt halten); Lenis geheime Kopie als wachsende moralische "
    "Zerreissprobe (zwei 'Auroras' — welche ist echt? kann man jemanden kopieren, den man liebt?); "
    "Leni/Ben und Marlie/Noah vertiefen. WICHTIG: Volle Wendung (AURORA = Aurora Santos, totes Kind von "
    "Maria & Theo) weiter staffeln — Lenis volle Erkenntnis erst zur Buchmitte, Noahs erst im letzten "
    "Drittel; Name/Mutter noch NICHT aussprechen.")

# Steuerung-Status aktualisieren
for e in d['steuerung']['eintraege']:
    t = e.get('text','')
    if t.startswith('Leni: romantische'):
        e['notiz'] = ("Ben Petersen weiter ausgebaut: Kaeltezentrale-Szene Kap 10 (er uebersieht fuer Leni "
            "bewusst eine Stromleitung, 'meine Daten sind meine Daten', 'trink den Kakao solange er warm ist'). "
            "Warmes, witziges Knistern, Leni erroetet, zeigt ungeschuetzte Seite. Laeuft weiter.")
        e['datum'] = heute
    if t.startswith('Thema Datenschutz'):
        e['status'] = 'in_arbeit'
        e['notiz'] = e.get('notiz','') + (" | UMGESETZT u. vertieft: Marlie/Guenter Kap 9 (Kontrolle statt Furcht, "
            "Recht Nein zu sagen); Hanni Kap 12 (redet nachts heimlich mit dem Assistenten — Trauer um die Stimme, "
            "die da war, als man allein war). Als gelebte Haltung eingewoben, nicht doziert.")
        e['datum'] = heute
    if t.startswith('Ein echter'):
        e['notiz'] = e.get('notiz','') + (" | Kap 10-12: Vogt aktiv als kalter Druckgeber (Vorstandsszene, 'Tote werden "
            "nicht teurer'); Roth in Kap 11 ueberfuehrt, sein Diebstahl scheitert, von Maria mit Leverage zum Schweigen "
            "gebracht. Vogt bleibt als eskalierende Bedrohung fuers mittlere Drittel.")
        e['datum'] = heute

json.dump(d, open(P,'w',encoding='utf-8'), ensure_ascii=False, indent=2)

# Verifikation
d2 = json.load(open(P, encoding='utf-8'))
print('Kapitel gesamt:', d2['statistik']['kapitel_gesamt'])
print('Woerter gesamt:', d2['statistik']['woerter_gesamt'])
print('Seiten ~:', round(d2['statistik']['woerter_gesamt']/280))
print('Letzte 3 Titel:')
for k in d2['kapitel'][-3:]:
    print('  -', k['titel'], '|', k['woerter'], 'W')
print('JSON valide: OK')
