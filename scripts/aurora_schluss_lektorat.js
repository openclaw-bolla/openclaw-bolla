export const meta = {
  name: 'aurora-schluss-lektorat',
  description: 'AURORA Lektorat + Konsistenz-Check für Kapitel 25 bis Buchende',
  phases: [
    { title: 'Lektorat', detail: 'Alle neuen Kapitel parallel' },
    { title: 'Konsistenz', detail: 'Plot-Kontinuität + Reveal-Staffelung' },
    { title: 'Bericht', detail: 'Zusammenfassung + Desktop-Datei' },
  ],
}

const SPOILER_CONTEXT = `GEHEIMNIS DES BUCHES (bekannt, weil du Lektor bist):
AURORA = rekonstruierte Bewusstseinsspur von Aurora Santos, totem Kind von Maria Santos und Theo Dreyer.
REVEAL-STAFFELUNG:
- Kap 20 ERLEDIGT: Kind-Reveal (Leni)
- Kap 25-30: Eltern-Andeutungen beginnen (Theo spürt etwas, deutet es falsch)
- Kap 31-38: Theo begreift langsam. Maria/Theo-Vergangenheit enthüllt sich.
- Kap 39+: Warum (Auferstehungs-Versuch). Noah als Letzter.
- Name "Aurora Santos" und "Marias Tochter": erst im letzten Fünftel explizit.
SPOILER-DISZIPLIN: Prüfe ob Überblick-Texte oder Dialoge die Staffelung verletzen.`

const FIGUREN = `FIGUREN: Marlie Braun (36, KI-Ethikerin, Hauptfigur, liebt Noah, läuft nachts), Noah Weber (40, Chefarchitekt, schuf AURORA, liebt Marlie, hatte Geheimnis), Leni Hoffmann (27, Quantenphysikerin, witzig, Gummibärchen), Ben Petersen (Lenis Partner, bodenständig, 7-j. Tochter), Theo Dreyer (52, Ex-Geheimdienst, Sicherheitschef, dunkle Vergangenheit mit Maria), Maria Santos (45, CEO NovaTech, Motiv: Auferstehung ihrer Tochter), Konrad Vogt (Investor, kalt, will AURORA verkaufen), Günter & Hanni Brandt (Nachbarn, Rentner, KI-skeptisch)`

const LEKTORAT_AUFGABEN = `LEKTORAT-AUFGABEN:
1. GRAMMATIK & TIPPFEHLER: Alle Fehler wörtlich zitieren + Korrektur.
2. KLANG-KOLLISIONEN: Unbeabsichtigte Wortwiederholungen im Abstand 1-3 Sätze.
3. TIMELINE/NAMEN: Inkonsistenzen — falscher Name, falsches Datum, Widersprüche.
4. ÜBERBLICK vs. TEXT: Verrät der Überblick Pointen/Cliffhanger? (Pointenfreiheits-Regel)
5. SPOILER-DISZIPLIN: Verstoß gegen Reveal-Staffelung? Jeden Verstoß wörtlich zitieren.
6. CLIFFHANGER: Endet das Kapitel mit Sog-Satz? Falls schwach, sagen.
7. ZU LANG / STRAFFEN: Falls Kapitel > 2800 Wörter UND Füllpassagen enthält — konkret benennen welche Absätze gestrichen werden können.
8. HUMOR/TON: Fehlt sympathischer Humor? Kurz ja/nein.`

const SCHEMA = {
  type: 'object',
  properties: {
    kapitel: { type: 'string' },
    grammatik: { type: 'array', items: { type: 'object', properties: { zitat: { type: 'string' }, fehler: { type: 'string' }, korrektur: { type: 'string' } }, required: ['zitat','fehler','korrektur'] } },
    klang_kollisionen: { type: 'array', items: { type: 'object', properties: { zitat: { type: 'string' }, problem: { type: 'string' } }, required: ['zitat','problem'] } },
    timeline_namen: { type: 'array', items: { type: 'object', properties: { zitat: { type: 'string' }, problem: { type: 'string' } }, required: ['zitat','problem'] } },
    ueberblick_check: { type: 'object', properties: { ok: { type: 'boolean' }, problem: { type: 'string' } }, required: ['ok'] },
    spoiler_check: { type: 'object', properties: { ok: { type: 'boolean' }, verstoesse: { type: 'array', items: { type: 'string' } } }, required: ['ok','verstoesse'] },
    cliffhanger: { type: 'object', properties: { ok: { type: 'boolean' }, schlusssatz: { type: 'string' }, anmerkung: { type: 'string' } }, required: ['ok','schlusssatz'] },
    straffen: { type: 'object', properties: { noetig: { type: 'boolean' }, wortanzahl: { type: 'number' }, streichvorschlaege: { type: 'array', items: { type: 'string' } } }, required: ['noetig','wortanzahl'] },
    humor_ton: { type: 'object', properties: { ok: { type: 'boolean' }, anmerkung: { type: 'string' } }, required: ['ok'] },
    gesamturteil: { type: 'string' }
  },
  required: ['kapitel','grammatik','klang_kollisionen','timeline_namen','ueberblick_check','spoiler_check','cliffhanger','straffen','humor_ton','gesamturteil']
}

phase('Lektorat')

// Kapitel-Indizes ab 25 dynamisch ermitteln
const indicesRaw = await agent(
  'Führe aus: python3 -c "import json; d=json.load(open(\'/home/bolla/workspace/data/ki_buch.json\')); print(\',\'.join(str(i) for i in range(25, len(d[\'kapitel\']))))"',
  { label: 'Indizes ermitteln', model: 'haiku' }
)

const indices = indicesRaw.trim().split(',').map(Number).filter(n => !isNaN(n))
log(`Lektoriere Kapitel-Indizes: ${indices.join(', ')} (${indices.length} Kapitel)`)

const ergebnisse = await parallel(
  indices.map(idx => () => agent(
    `Du bist Lektor für den deutschen KI-Thriller "AURORA". Lektoriere Kapitel-Index ${idx}.

Schritt 1 — Lies das Kapitel:
python3 -c "import json; d=json.load(open('/home/bolla/workspace/data/ki_buch.json')); k=d['kapitel'][${idx}]; print('TITEL:', k['titel']); print('WORTANZAHL:', len(k.get('text','').split())); print('UEBERBLICK:', k.get('ueberblick','')); print('---TEXT---'); print(k['text'])"

Schritt 2 — Lektorat:

${SPOILER_CONTEXT}

${FIGUREN}

${LEKTORAT_AUFGABEN}

Gib strukturiertes JSON zurück.`,
    { label: `Kap ${idx}`, phase: 'Lektorat', schema: SCHEMA, model: 'haiku' }
  ))
)

phase('Konsistenz')

const konsistenz = await agent(
  `Du prüfst den AURORA-Roman auf Plot-Konsistenz. Lies alle Überblicke und prüfe gezielt Kapitel 25+.

python3 -c "
import json
d = json.load(open('/home/bolla/workspace/data/ki_buch.json'))
for i,k in enumerate(d['kapitel']):
    print(f'[{i}] {k[\"titel\"]}: {k.get(\"ueberblick\",\"\")[:250]}')
"

${SPOILER_CONTEXT}

Prüfe:
1. PLOT-LÖCHER: Szenen die zueinander im Widerspruch stehen (falsche Zeitangaben, Figur an zwei Orten gleichzeitig, bereits erledigte Konflikte die wieder auftauchen)
2. REVEAL-STAFFELUNG: Wird die Enthüllungs-Reihenfolge eingehalten?
3. FIGUREN-KONSISTENZ: Verhält sich eine Figur plötzlich anders als etabliert?
4. CLIFFHANGER-KETTE: Werden wichtige Cliffhanger aus den Vorgängerkapiteln im Nachfolger aufgelöst oder zumindest aufgegriffen?
5. LENI/BEN Liebesgeschichte: Wird sie konsequent weitergeführt oder fällt sie weg?

Antworte strukturiert mit konkreten Kapitel-Angaben.`,
  { label: 'Konsistenz-Check', phase: 'Konsistenz', model: 'sonnet' }
)

phase('Bericht')

const gefiltert = ergebnisse.filter(Boolean)

const bericht = await agent(
  `Erstelle den finalen Schlusslektorat-Bericht für AURORA (Kapitel 25 bis Ende).

Einzelberichte:
${JSON.stringify(gefiltert, null, 2)}

Konsistenz-Check:
${konsistenz}

Struktur:
1. ZUSAMMENFASSUNG: Gesamtqualität + Fehlerstatistik
2. DRINGENDE KORREKTUREN (Grammatik/Tippfehler): Kapitel | Fehler | Korrektur
3. KLANG-KOLLISIONEN (max 10 auffälligste)
4. TIMELINE/NAMEN-PROBLEME
5. ÜBERBLICK-PROBLEME (Pointenfreiheit verletzt)
6. SPOILER-VERSTOESSE — KRITISCH, jeden einzeln
7. KAPITEL ZUM STRAFFEN: Liste mit Kapitel + Wortanzahl + konkreten Streichvorschlägen
8. KONSISTENZ-PROBLEME (aus dem Konsistenz-Check)
9. CLIFFHANGER-KETTE: Schwache Enden
10. GESAMTURTEIL: Ist das Buch fertig für den Review?

Direkt mit Zusammenfassung beginnen, keine Einleitung.`,
  { label: 'Bericht erstellen', model: 'sonnet' }
)

// Bericht auf Desktop speichern
await agent(
  `Speichere als /mnt/c/Users/ernst/Desktop/AURORA_Schlusslektorat.txt:
${bericht}`,
  { label: 'Bericht speichern', model: 'haiku' }
)

// aktuell.md updaten
await agent(
  `Aktualisiere /home/bolla/.claude/projects/-home-bolla/memory/aktuell.md:
- Ersetze den AURORA-Abschnitt: Schlusslektorat Kap 25+ ist abgeschlossen (2026-06-12).
- Bericht liegt auf Desktop: AURORA_Schlusslektorat.txt
- Nächster Schritt: Chris-Review, dann EPUB/Kindle-Export`,
  { label: 'aktuell.md updaten', model: 'haiku' }
)

log(`Fertig! ${gefiltert.length} Kapitel lektoriert.`)
return { lektoriert: gefiltert.length, bericht }
