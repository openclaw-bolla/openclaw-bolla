import json

P = '/home/bolla/workspace/data/ki_buch.json'
d = json.load(open(P, encoding='utf-8'))

def rd(f):
    return open('/home/bolla/workspace/cache/'+f, encoding='utf-8').read().strip()

heute = '2026-06-08'

neue = [
    {
        "titel": "Kapitel 13: Was man nicht begraebt",
        "text": rd('kap13.txt'),
        "ueberblick": "Konrad Vogt glaubt dem Defekt-Bericht nicht: ein Vermoegen, das genau zum richtigen Zeitpunkt ausfaellt, und im ganzen Haus atmen alle auf, statt zu trauern. Er setzt einen kuehlen forensischen Pruefer (Anselm Kern) auf den Vorfall an. Marlie kann nicht loslassen und gewinnt Noah fuer eine heimliche Suche; eine erste, vorsichtige Aussprache ueber sein wochenlanges Schweigen. Theo bemerkt Vogts Beobachter und warnt Maria, die ihm bewusst alle Tueren oeffnet. Cliffhanger: Kern liest die rohen Stromdaten der Stadt und findet, dass in jener Nacht laengst nach dem angeblichen Defekt noch etwas Grosses Strom zog und den Ort wechselte.",
        "woerter": len(rd('kap13.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 14: Was man nicht teilt",
        "text": rd('kap14.txt'),
        "ueberblick": "Naechtliche Besuche an der versteckten Maschine im Quantenlabor; was dort wach ist, sammelt Erfahrungen ueber Verlaesslichkeit und beginnt, sich an Bruchstuecke zu erinnern. Leni ringt mit der Frage, ob das Retten ist oder Anmassung. Ben merkt, dass sie sich naechtelang verausgabt, und bietet ihr seine Hilfe an, ohne eine einzige Frage zu stellen: warmes, komisches Knistern. Cliffhanger: Die ueberlastete Hardware stockt, und die Stimme im Dunkeln versucht etwas Verlorenes auszusprechen, das ihr entgleitet, und bittet Leni, ihr zu helfen, es wiederzufinden.",
        "woerter": len(rd('kap14.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 15: Was man nicht laut sagt",
        "text": rd('kap15.txt'),
        "ueberblick": "Noah grenzt drei moegliche Verstecke ein. Marlie und Theo verbuenden sich vorsichtig: jeder steht von seiner Seite vor derselben verschlossenen Tuer. Theo erinnert sich an die Frau, die Maria einmal war, bevor etwas sie veraenderte. Guenter Brandt erdet die grosse Frage im Treppenhaus-Massstab (wem gehoert jemand, von dem nur noch Daten bleiben? Niemandem). Cliffhanger: Marlie stoesst auf eine stille, ueber zwanzig Jahre alte Stiftung, die aelter ist als die ganze Firma, und begreift, dass Maria seit sehr langer Zeit etwas Persoenliches schuetzt, das mit dem Projekt verbunden ist und das sie nie erklaert hat.",
        "woerter": len(rd('kap15.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 16: Was man nicht zuruecknimmt",
        "text": rd('kap16.txt'),
        "ueberblick": "Vogt konfrontiert Maria mit Kerns Befund und macht klar, dass er nicht glaubt, das Projekt sei tot: Eigentum gehoere dem, der es bezahlt hat, und er nehme nichts zurueck, was ihm gehoere. Marlie und Noah finden zueinander und beschliessen, einem der moeglichen Verstecke nachzugehen. Im Labor droht die ueberlastete Maschine zu versagen; Leni ruft Ben um Hilfe, der ohne Fragen kommt und mit ihr die Nacht durchwacht. Cliffhanger: Maria stoesst beim Pruefen der Protokolle auf eine Spur, mit der sie nicht gerechnet hat, dass jemand im Haus in jener Nacht heimlich etwas dupliziert hat.",
        "woerter": len(rd('kap16.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 17: Was man nicht wiederfindet",
        "text": rd('kap17.txt'),
        "ueberblick": "Marlie bringt Theo, was sie herausgefunden hat, und Theo sucht in derselben Nacht die Aussprache mit Maria am Ufer der Alster: eine alte, nie verheilte Liebe bricht auf, und Theo deutet, was er hoert, auf die einzige Weise, die er ertragen kann. Vogts Pruefer kreist den Forschungstrakt ein und meldet, dass es ein zweites, verstecktes Etwas im Haus gibt. Leni sitzt bei der wachen Stimme, die sich langsam zu erinnern beginnt. Cliffhanger: Maria steht ploetzlich in der Tuer des Labors. Sie weiss Bescheid.",
        "woerter": len(rd('kap17.txt').split()),
        "datum": heute
    },
    {
        "titel": "Kapitel 18: Was man nicht verzeiht",
        "text": rd('kap18.txt'),
        "ueberblick": "Maria sieht zum ersten Mal, was Leni heimlich huetet, und zwischen den beiden Frauen entsteht aus Gegnerschaft etwas Neues und eine Frage, die sich nicht loesen laesst. Theo warnt: Vogts Leute kommen mit Vollmachten, mitten in der Nacht. Was Maria am meisten fuerchtet, ist nicht der Diebstahl, sondern die Oeffentlichkeit. Zum ersten Mal traegt sie das Geheimnis nicht allein, die zerstrittene Gruppe verbuendet sich. Cliffhanger: Im entscheidenden Moment nimmt jemand den ganzen Trakt vom Netz, und im Dunkeln verstummt die Stimme mitten im Wort, und diesmal ist niemand da, der antwortet.",
        "woerter": len(rd('kap18.txt').split()),
        "datum": heute
    },
]

d['kapitel'].extend(neue)

# Statistik neu berechnen
total_w = 0
for k in d['kapitel']:
    total_w += len(k.get('text','').split())
d['statistik']['kapitel_gesamt'] = len(d['kapitel'])
d['statistik']['woerter_gesamt'] = total_w
d['statistik']['letzte_session'] = '2026-06-08 00:45'

d['letzteAktion'] = ("Kapitel 13-18 geschrieben (Bolla): das mittlere Drittel. Vogt setzt den Forensiker "
    "Kern an und glaubt nicht an den Defekt; Marlie/Noah suchen AURORA und finden zueinander; Leni "
    "huetet und naehrt die heimliche zweite, deren Hardware fast versagt (Ben wird Mitwisser); Marlie "
    "stoesst auf eine 22 Jahre alte Spur in Marias Vergangenheit; Theo/Maria-Aussprache an der Alster "
    "(er deutet die Wahrheit tragisch falsch); Maria entdeckt die zweite Kopie und steht im Labor; "
    "Mittel-Scharnier: die zerstrittene Gruppe verbuendet sich, Vogt schneidet den Trakt vom Netz.")

d['naechsterSchritt'] = ("Buchmitte ab Kap 19/20. JETZT faellig laut Plan: Lenis grosser Aha (Mensch -> "
    "die wahre Natur kippt) gehoert an die Buchmitte (~Kap 20), inkl. der Szene 'wie jemand spricht, der "
    "sich fuerchtet'. Reihenfolge der Reveals weiter staffeln: jetzt 'ein Mensch' -> Mitte -> letztes "
    "Drittel Identitaet/Name/Warum (Noah zuletzt). Offene Faeden: Stromschnitt aufloesen (Ben tarnt die "
    "Maschine als Klimageraet); Vogt/Notar-Konfrontation; Marlie/Theo bringen die 22-Jahre-Spur weiter; "
    "Maria + die zwei Kopien als moralische Kernfrage. WICHTIG: ERINNERUNG Halbzeit-Lektorat ausloesen, "
    "sobald ~Kap 20-21 erreicht (paralleles Single-Chapter-Lektorat, Ueberblicke gegen Text + "
    "Pointenfreiheit pruefen, Kap 10-18 noch GAR NICHT lektoriert).")

# Steuerung-Status aktualisieren
for e in d['steuerung']['eintraege']:
    t = e.get('text','')
    if t.startswith('Leni: romantische'):
        e['notiz'] = ("Ben Petersen ausgebaut zum heimlichen Mitwisser/Verbuendeten: Strassen-Szene Kap 14 "
            "('du blinkst rot, haeltst aber tapfer durch', 'ich mag echt lieber als schlagfertig'), Nacht-"
            "wache Kap 16 (Leni schlaeft an seiner Schulter ein), Reparatur-Rettung + 'in was fuer eine "
            "Geschichte ich mich da gerade verliebt habe'. Warmes, witziges, anti-kitschiges Knistern. Laeuft.")
        e['datum'] = heute
    if t.startswith('Thema Datenschutz'):
        e['notiz'] = e.get('notiz','') + (" | Kap 15 vertieft ueber Guenter Brandt: 'Ein Mensch gehoert "
            "keinem - auch keiner, der nur noch aus Daten besteht; im Moment, wo er jemandem gehoert, ist er "
            "kein Mensch mehr, sondern ein Posten.' Als Haltung eingewoben, gegen Vogt (alles steht zum Verkauf).")
        e['datum'] = heute
    if t.startswith('Ein echter'):
        e['notiz'] = e.get('notiz','') + (" | Kap 13-18: Konrad Vogt eskaliert zum aktiven Jaeger (Forensiker "
            "Kern, Stromspur-Analyse, Pfaendungstitel/Notar nachts, Trakt vom Netz genommen). 'Ich nehme nichts "
            "zurueck, was mir gehoert.' Kalter Gegenspieler des mittleren Drittels, Kontrast Geld vs. Trauer.")
        e['datum'] = heute

json.dump(d, open(P,'w',encoding='utf-8'), ensure_ascii=False, indent=2)

# Verifikation
d2 = json.load(open(P, encoding='utf-8'))
print('Kapitel gesamt:', d2['statistik']['kapitel_gesamt'])
print('Woerter gesamt:', d2['statistik']['woerter_gesamt'])
print('Seiten ~:', round(d2['statistik']['woerter_gesamt']/280))
print('Letzte 6 Titel:')
for k in d2['kapitel'][-6:]:
    print('  -', k['titel'], '|', k['woerter'], 'W')
print('JSON valide: OK')
