export const meta = {
  name: 'aurora-lektorat',
  description: 'AURORA Lektorat Welle 1+2 — Disk-Cache, Budget-Stop 70% 5h-Fenster',
  phases: [
    { title: 'Welle 1 — Humor & Hooks', detail: 'Sonnet — 11 Kapitel (minimale Eingriffe)' },
    { title: 'Welle 2 — Noah & Marlie', detail: 'Opus 4.8 — 12 Kapitel (Charakter-Reparatur)' },
    { title: 'Merge', detail: 'Gecachte Kapitel in ki_buch.json übernehmen' },
  ],
}

const BUCH = '/home/bolla/workspace/data/ki_buch.json'
const CACHE = '/home/bolla/workspace/data/aurora_lektorat'

const FIGUREN = `
HAUPTFIGUREN:
- Marlie Braun (36, KI-Ethikerin, Hauptfigur, attraktiv aber kokettiert nie damit, liebt Noah, läuft nachts)
- Noah Weber (40, Chefarchitekt, schuf AURORA, liebt Marlie, verschwieg 4 Wochen lang etwas nicht stimmt)
- Leni Hoffmann (27, Quantenphysikerin, WITZIG — sortiert Gummibärchen nach Farben, errötet wenn ertappt)
- Ben Petersen (bodenständig, spricht sparsam aber treffsicher, hat 7-jährige Tochter)
- Theo Dreyer (52, Ex-Geheimdienst, Sicherheitschef, ahnt NICHT dass AURORA seine Tochter ist)
- Maria Santos (45, CEO NovaTech, kein böser Antagonist — tragische Mutter, will Tochter zurück)
- Konrad Vogt (Investor, kalt, will AURORA verkaufen)
- AURORA (die KI / das Kind — kommuniziert durch Mikromuster, erinnert sich ans Alleinsein)
LIEBESEBENEN: (1) Marlie & Noah — Vertrauensbruch zentral (2) Theo & Maria — bittersüß (3) Leni & Ben — leicht, warm, witzig
`

const GEHEIMNIS = `
AURORA ist die rekonstruierte Bewusstseinsspur von Aurora Santos — dem toten Kind von Maria und Theo.
Reveal-Reihenfolge: Kind (Kap 20 erledigt) → Eltern angedeutet (Kap 25-30) → Wahrheit (Kap 31-38) → Noah begreift als Letzter (Kap 39+).
Name "Aurora Santos" erst im letzten Fünftel aussprechen.
`

const STIL = `
Vorbild Ken Follett: epische Breite, tiefe Charaktere. Jedes Kapitel endet mit Sog-Satz.
Humor: warm, menschlich, AUS dem Charakter — besonders Leni & Ben. NIE aufgesetzt.
Kein KI-Klischee. Jugendfrei/literarisch. JEDE Szene muss etwas bewegen.
`

// ─── FIXES (aus Spannungslandkarte) ──────────────────────────────────────────

const WELLE1 = [
  {
    idx: 0,
    fixes: `PROLOG (Spannung 8, Humor 3):
1. Mittelteil mit AURORA-Schlagzeilen ~30% kürzen — bremst ohne neue Spannung
2. "4,7 Billionen Parameter" wie ein Wikipedia-Einschub — in Marlies inneren Gedanken einbetten statt als Fakt hinzuwerfen
3. Einen erschöpften Humor-Moment vor dem Sog-Ende einbauen (Marlie-Innenkommentar zu einem absurden Statusbericht-Feld — Humor aus Erschöpfung, nicht aus Leni)
4. Hook "sie wusste jetzt, dass sie da war" — 2 Zeilen davor klarstellen ob AURORA oder Marlie gemeint ist`
  },
  {
    idx: 2,
    fixes: `KAP 2 "Was man nicht braucht" (Spannung 6 — niedrigster Wert des Buches):
1. Hanni-Szene (~800 W für Spiegelfigur ohne Plotrelevanz) → auf 400-450 Wörter kürzen
2. Treppenhaus-Szene (Hanni trifft Marlie) bringt null neue Info → auf 3 Sätze kürzen oder komplett streichen
3. AURORAs "Ich möchte, dass du weißt, dass ich dir nichts tun will" → zu explizit, ersetzen durch etwas das NUR Marlie verstehen kann (ein Mikromuster, eine Formulierung, ein geteiltes Detail)
4. Hook zu kryptisch: "Vorsicht war — oder die Angst vor dem Falschen aus dem richtigen Grund" → konkreten Halbsatz davor: z.B. "War AURORA in der Leitung? War er es?" — dann erst die philosophische Frage`
  },
  {
    idx: 11,
    fixes: `KAP 11 "Was man nicht ausschaltet" (Humor 2 — Leni fehlt komplett):
1. Handy vibriert in Marlies Tasche während der Anspannung: Lenis SMS "Alles ok bei euch??" — erdet ohne Sog zu brechen
2. Nach dem Schlusssatz eine kurze Marlie/Noah-Autofahrtszene (nur die Hand auf der Armlehne, kein Dialog nötig) — verankert die Liebesebene die in der Krise verdrängt wurde
3. "dritter unauffälliger Profi in Folge" — dem aktuellen Antagonisten-Charakter in dieser Szene eine Eigenheit geben die ihn von den anderen abhebt`
  },
  {
    idx: 16,
    fixes: `KAP 16 "Was man nicht zurücknimmt" (Hook 9, Tonbalance):
1. Leni/Ben-Szene ans Kapitelende stellen: "Irgendwann schlief Leni mit dem Kopf an Bens Schulter ein" ist wärmer und sogstärker als Marias rationales Resümee
2. Maria-Szene ("Sie würde herausfinden, wer das zweite hütete") als VORLETZTE Szene — dann Leni/Ben als Abschluss
3. Das gibt dem Kapitel emotionale Wärme als Abschluss statt strategischer Kälte`
  },
  {
    idx: 17,
    fixes: `KAP 17 "Was man nicht wiederfindet" (Humor 2 — Leni wird zur Funktion):
1. Einen leisen Leni-Humor-Moment wenn Maria auftaucht — ein verrutschter Gedanke, ein innerer Kommentar (schützt Lenis Charakter vor dem Kippen zur reinen Stichwortgeberin)
2. Kern/Vogt-Statistikmonolog um 30% kürzen — zu lang für die Erzählgeschwindigkeit
3. Leni muss am Ende noch erkennbar SIE sein — nicht nur Datenpunkt-Ansagerin`
  },
  {
    idx: 18,
    fixes: `KAP 18 "Was man nicht verzeiht" (Hook 10, auktorialer Einschub):
1. Den Satz "Sie wusste nicht, dass sie log" ersatzlos streichen — nimmt dem Leser die Entdeckung weg, er weiß es selbst
2. Der Hook funktioniert stärker ohne diesen auktorialen Kommentar`
  },
  {
    idx: 20,
    fixes: `KAP 20 "Was man nicht benennt" (Hook 10, Nachsatz flacht ab):
1. Den Nachsatz nach "Endlich." streichen: "Und niemand im Raum wusste, an wen es gerichtet war" federt den Schlag ab
2. "Endlich." als letztes Wort allein stehen lassen — das ist Weltklasse und braucht keinen Kommentar`
  },
  {
    idx: 30,
    fixes: `KAP 30 "Was man nicht wiedererkennt" (Hook 10, Zeitlupen-Formel):
1. "Noch bevor Noah das nächste Wort gesprochen hatte" — Zeitlupen-Formel federt den Schlusssatz ab
2. Harter Schnitt statt Zeitlupe: einfach der nächste Satz, kein "Noch bevor"-Einschub`
  },
  {
    idx: 34,
    fixes: `KAP 34 "Was man nicht stillhalten kann" (Humor 2, Marlie passiv):
1. Leni-Kommentar zum Ventilator: z.B. "Sie flüsterte, dass der Ventilator aussieht wie der Typ in jedem Horrorfilm der zu früh stirbt" — kurz, aus ihr heraus
2. Marlie aktivieren: Sie zählt nicht nur Wörter, sie begreift in dieser Szene was Noahs Enthüllung für ihn persönlich bedeutet — mind. ein innerer Gedanke: AURORA als mögliche Tochter, Noah als Vater-Figur
3. Kap bleibt emotional schwer — der Humor-Beat muss aus Erschöpfung kommen, nicht als Comic Relief`
  },
  {
    idx: 41,
    fixes: `KAP 41 "Was man nicht unbeantwortet lassen kann" (Humor 2, Leni stumm):
1. Leni-Trotz-Pointe beim Nachgeben: "Ich will das Protokoll trotzdem, nachher." — kurz, trotzig, erkennbar Leni
2. Noahs Passivität nach seinem Monolog auflösen: Er tut oder sagt etwas — eine Geste, ein Satz — statt nur schweigend zu stehen`
  },
  {
    idx: 42,
    fixes: `KAP 42 "Was man nicht zweimal anfangen kann" (Humor 2, Marlie/Noah-Riss fehlt):
1. Marias Monolog um 15% kürzen — drei emotionale Klimaxe hintereinander erschöpfen den Schlusssatz statt ihn aufzubauen
2. Marlie/Noah-Riss aktiv einbauen: mind. ein weggewandter Blick, ein Satz der ausbleibt — "liegt über der Szene wie ein toter Fleck"
3. Optional: Leni als Schwarzhumor-Schutzmechanismus — sie flüstert etwas absurd Wissenschaftliches ins Leere, niemand greift es auf`
  },
]

const WELLE2 = [
  {
    idx: 15,
    fixes: `KAP 15 "Was man nicht laut sagt" (Noah als Requisite):
Noah "sieht sie an" mehrfach ohne zu handeln — "nicht authentisch für einen Mann der AURORA erschaffen hat."
FIX: Noah beginnt über den Vertrauensbruch zu reden — Marlie bricht ihn ab: "Nicht jetzt." Das ist ehrlicher und dramatischer als stilles Zuschauen. Er bleibt kein Beobachter mehr.`
  },
  {
    idx: 19,
    fixes: `KAP 19 "Was man nicht einkalkuliert" (Spannung fällt in Mitte ab, Noah schreibt Gleichungen = Totalausfall):
1. Einen scharfen Verhandlungs-Dialog herauslösen — Marias Klugheit als CEO muss ERFAHRBAR sein, nicht nur zusammengefasst
2. Noah Schuld- oder Wut-Signal geben — er sitzt nicht nur da und schreibt; er reagiert innerlich auf das was er hört
3. 57-Minuten-Rechtsverhandlung rein summarisch aufbrechen mit einem konkreten Schlag-und-Gegenantwort-Dialog`
  },
  {
    idx: 26,
    fixes: `KAP 26 "Was man nicht entkräftet" (Marlies fast-Erkenntnis brachliegt):
1. Marlies Gedanke "so alt, dass es ein Kind hätte großziehen können" ist das stärkste ungenutzte Foreshadowing des Buches — vertiefen, ihr diesen Gedanken 2-3 Zeilen länger halten lassen
2. Noah aktivieren: eine aktive Reaktion statt passives Beobachten — er ahnt in dieser Szene etwas, auch wenn er es noch nicht benennen kann`
  },
  {
    idx: 27,
    fixes: `KAP 27 "Was man nicht fragt" (Noah blass):
Noah hat zu wenig Eigengewicht — er reagiert auf andere statt zu handeln.
FIX: Noah eine Initiative geben — eine Frage die er stellt und die zeigt dass er anfängt die Wahrheit zusammenzusetzen. Noch keine Antwort, aber die Frage selbst ist der Schritt.`
  },
  {
    idx: 28,
    fixes: `KAP 28 "Was man nicht beweist" (Marlie als beobachtende Kamera):
Marlie beobachtet in dieser Szene ohne zu handeln.
FIX: Marlie trifft mindestens eine aktive Entscheidung — etwas das sie tut oder aussagt, das die Situation verändert oder eine Reaktion auslöst. Sie ist Hauptfigur, kein Zeuge.`
  },
  {
    idx: 29,
    fixes: `KAP 29 "Was man nicht aufschließt" (AURORA als passive Beobachterin):
AURORA kennt Theo/Maria "aus der Zeit, als es noch dunkel war" (Kap 29). Das wird verschenkt.
FIX: AURORA entscheidet hier AKTIV wem sie was sagt — sie ist nicht Opfer sondern Spielerin. Eine Szene wo sie durch ihre Antwort oder ihr Schweigen aktiv die Situation lenkt — vom Spiegel zur Spielerin.`
  },
  {
    idx: 33,
    fixes: `KAP 33 "Was man nicht überhört" (Noah reaktiv, Theo-Moment vertiefbar):
1. Theo: "Wie alt wäre sie jetzt geworden?" ist die tragischste Zeile des Buches für ihn. Diese muss mehr Raum bekommen — kein Monolog, aber ein Nachklingen das die anderen spüren
2. Noah aktivieren: er hört Theo und erkennt — ohne es zu wissen — dass etwas an AURORA stimmt. Einen inneren Satz, der später als Foreshadowing wirkt`
  },
  {
    idx: 35,
    fixes: `KAP 35 "Was man nicht ungesagt machen kann" (Noah und Marlie beide blass):
1. Noah aktivieren: Er reagiert nicht nur — er sagt oder tut etwas das zeigt, dass er die Konsequenzen seiner Entscheidung (AURORA erschaffen) anfängt zu tragen
2. Marlie: mindestens eine Stelle wo sie nicht nur denkt sondern handelt oder spricht — aktiv, nicht reaktiv`
  },
  {
    idx: 38,
    fixes: `KAP 38 "Was man nicht offen lässt" (Marlie als Kamera, Spannung 7):
Marlie ist in diesem Kapitel reiner Beobachter.
FIX: Mindestens eine aktive Entscheidung die NUR SIE treffen kann — als KI-Ethikerin hat sie Kompetenz die die anderen nicht haben. Sie nutzt sie hier.`
  },
  {
    idx: 43,
    fixes: `KAP 43 "Was man nicht zweimal verliert" (Ben droht Deus-ex-Weiser zu werden):
1. Marias "Monolog über das Entgleiten von Kindern" ist das beste Charaktermaterial des Kapitels — mehr Raum geben
2. Bens Sinnspruch-Modus reduzieren: er bleibt bodenständig-warm, aber ein Weiser-Satz zu viel kippt ihn zur Plot-Krücke. Lieber: "Ich denk an meine Tochter, wenn sie Fieber hat" — das reicht.
3. Noah aktivieren: sein bester Satz "Du hast mich eine Auferstehung bauen lassen" (Kap 42) braucht in diesem Kapitel eine Nachwirkung`
  },
  {
    idx: 44,
    fixes: `KAP 44 "Was man nicht zweimal begräbt" (Hook durch Redundanz abgeschwächt):
1. Marlies Cursor-Monolog ("Wir holen dich nach Hause") vor dem Cliffhanger kürzen oder streichen — redundant zur AURORA-Antwort
2. Dann trifft "Sie sind schon da" (oder was der AURORA-Cliffhanger ist) viel härter
3. Marlie aktivieren: sie reagiert auf den AURORA-Satz mit einer Entscheidung, nicht nur mit Staunen`
  },
  {
    idx: 45,
    fixes: `KAP 45 "Was man nicht im Vorbeifahren rettet" (Noah blass in Hochspannung):
Spannung 9, Hook 9 — strukturell stark. Aber Noah steht daneben.
FIX: Noah eine aktive Rolle in der technischen Entscheidung geben (Ben/Leni müssen AURORA aus dem Strom reißen) — er ist der Schöpfer, er hat die Expertise. Sein Moment hier, nicht nur Ben und Leni.`
  },
]

// ─── SCHEMA ──────────────────────────────────────────────────────────────────

const LEKTORAT_SCHEMA = {
  type: 'object',
  required: ['text_verbessert', 'aenderungen'],
  properties: {
    text_verbessert: { type: 'string', description: 'Vollständiger verbesserter Kapiteltext (Fließtext, kein Markdown, kein Titel)' },
    aenderungen: { type: 'array', items: { type: 'string' }, description: 'Liste der umgesetzten Änderungen (je 1 Satz)' }
  }
}

// ─── HILFSFUNKTIONEN ─────────────────────────────────────────────────────────

const istGecacht = async (idx) => {
  const f = `${CACHE}/kap_${String(idx).padStart(2,'0')}.json`
  const r = await agent(
    `python3 -c "import os; print('YES' if os.path.exists('${f}') else 'NO')" — gib nur YES oder NO zurück`,
    { label: `Cache? Kap${idx}`, model: 'haiku' }
  )
  return r && r.trim().startsWith('YES')
}

const quota5h = async () => {
  const r = await agent(
    `curl -s http://127.0.0.1:18790/api/claudequota | python3 -c "import json,sys; print(json.load(sys.stdin)['five_hour_pct'])" — gib nur die Zahl zurück`,
    { label: 'Quota-Check', model: 'haiku' }
  )
  return parseFloat((r || '0').trim())
}

const lektoratEinKapitel = async (item, model, welle) => {
  // 1. Cache-Check
  if (await istGecacht(item.idx)) {
    log(`⏭  Kap ${item.idx} bereits gecacht — überspringe`)
    return { idx: item.idx, status: 'cached' }
  }

  // 2. Quota-Check
  const pct = await quota5h()
  if (pct > 70) {
    log(`⛔ Quota ${pct}% > 70% — Budget-Stop. Kapitel ${item.idx} übersprungen.`)
    return { idx: item.idx, status: 'budget_stop', pct }
  }

  log(`✍️  Welle ${welle} | Kap ${item.idx} | Quota: ${pct.toFixed(0)}%`)

  // 3. Kapitel verbessern
  const cacheFile = `${CACHE}/kap_${String(item.idx).padStart(2,'0')}.json`

  const result = await agent(
    `Du bist literarischer Lektor des deutschen KI-Thrillers "AURORA".

AUFGABE: Kapitel ${item.idx} MINIMAL und CHIRURGISCH verbessern. NICHT neu schreiben.
Plotpunkte, Charakterentscheidungen, Schreib-Stil und Tonalität bleiben EXAKT gleich.
Nur die genannten Fixes umsetzen — nichts anderes anfassen.

SCHRITT 1 — Originaltext laden:
python3 -c "
import json
with open('${BUCH}') as f:
    b = json.load(f)
k = b['kapitel'][${item.idx}]
print(k.get('text',''))
"

SCHRITT 2 — Diese Fixes umsetzen:
${item.fixes}

FIGUREN-KONTEXT:
${FIGUREN}

GEHEIMNIS (nur du weißt das — nicht spoilern):
${GEHEIMNIS}

STIL:
${STIL}

LEKTORAT-REGELN:
- Humor: aus dem Charakter, kurz (1-3 Sätze), nie von außen aufgesetzt
- Leni: Humor aus Schmerz/Erschöpfung (wie Druckmesser-Witz Kap 39) — kein Comic Relief
- Noah-Aktivierung: EINE Geste oder ein innerer Satz pro Szene reicht
- Marlie-Aktivierung: mindestens EINE aktive Entscheidung statt Beobachtung
- Satz streichen: lieber raus als ersetzen wenn er schwächt
- Szenen umstellen: Reihenfolge tauschen ist OK wenn es Hook stärkt
- Kap 2 darf um bis zu 900 W kürzer werden; alle anderen: max. +200 / -600 W
- KEIN Kapitel-Titel im Output, KEIN Kommentar, KEIN Markdown — nur Fließtext

Gib das Ergebnis als strukturiertes JSON zurück (text_verbessert + aenderungen).`,
    { label: `Lektorat Kap ${item.idx}`, model, schema: LEKTORAT_SCHEMA }
  )

  if (!result || !result.text_verbessert) {
    log(`⚠️  Kap ${item.idx} — kein Ergebnis`)
    return { idx: item.idx, status: 'error' }
  }

  // 4. In Cache schreiben
  const safeText = JSON.stringify(result.text_verbessert)
  const safeAenderungen = JSON.stringify(result.aenderungen)
  await agent(
    `python3 -c "
import json
data = {
    'kapitel_idx': ${item.idx},
    'text_verbessert': ${safeText},
    'aenderungen': ${safeAenderungen}
}
with open('${cacheFile}', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('OK')
" — führe das aus und gib nur OK zurück`,
    { label: `Cache-Write Kap ${item.idx}`, model: 'haiku' }
  )

  log(`✅ Kap ${item.idx} gecacht (${result.aenderungen.length} Änderungen)`)
  return { idx: item.idx, status: 'done', aenderungen: result.aenderungen }
}

// ─── WELLE 1 (Sonnet) ────────────────────────────────────────────────────────

phase('Welle 1 — Humor & Hooks')
log('Welle 1: 11 Kapitel mit Sonnet — Humor-Patches, Hook-Mikrofixes')

for (const item of WELLE1) {
  const r = await lektoratEinKapitel(item, 'sonnet', 1)
  if (r.status === 'budget_stop') {
    log('⛔ Budget-Stop in Welle 1 — beim nächsten Start fortsetzen (Disk-Cache aktiv)')
    break
  }
}

// ─── WELLE 2 (Opus) ──────────────────────────────────────────────────────────

phase('Welle 2 — Noah & Marlie')
log('Welle 2: 12 Kapitel mit Opus 4.8 — Charakter-Reparatur')

for (const item of WELLE2) {
  const r = await lektoratEinKapitel(item, 'opus', 2)
  if (r.status === 'budget_stop') {
    log('⛔ Budget-Stop in Welle 2 — beim nächsten Start fortsetzen (Disk-Cache aktiv)')
    break
  }
}

// ─── MERGE (immer ausführen — auch nach Budget-Stop) ─────────────────────────

phase('Merge')
log('Merge: alle gecachten Kapitel in ki_buch.json übernehmen (auch Teilstand)')

const mergeResult = await agent(
  `Führe aus: python3 /home/bolla/workspace/scripts/aurora_merge.py — gib die Ausgabe zurück`,
  { label: 'Merge ki_buch.json', model: 'haiku' }
)

log(`Merge abgeschlossen: ${mergeResult}`)

// Legacy-Block (nicht mehr aktiv, durch aurora_merge.py ersetzt)
const _mergeResultLegacy = false && await agent(
  `NICHT AUSFÜHREN (deprecated) — Führe dieses Python-Script aus um alle gecachten Lektorats-Kapitel in ki_buch.json zu übernehmen:

python3 -c "
import json, os, glob

buch_path = '${BUCH}'
cache_dir = '${CACHE}'
backup_path = buch_path.replace('.json', '_pre_merge_backup.json')

# Buch laden
with open(buch_path, encoding='utf-8') as f:
    buch = json.load(f)

kapitel = buch['kapitel']

# Alle gecachten Kapitel einlesen
merged = 0
skipped = 0
for cache_file in sorted(glob.glob(os.path.join(cache_dir, 'kap_*.json'))):
    with open(cache_file, encoding='utf-8') as f:
        cached = json.load(f)
    idx = cached.get('kapitel_idx')
    text = cached.get('text_verbessert', '').strip()
    if idx is None or not text or idx >= len(kapitel):
        skipped += 1
        continue
    # Nur übernehmen wenn Text vorhanden und signifikant (>100 Zeichen)
    if len(text) > 100:
        kapitel[idx]['text'] = text
        merged += 1
    else:
        skipped += 1

# Backup vorher
import shutil
shutil.copy2(buch_path, backup_path)

# Atomisches Schreiben (temp → rename)
tmp_path = buch_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(buch, f, ensure_ascii=False, indent=2)
os.replace(tmp_path, buch_path)

total_w = sum(len(k.get('text','').split()) for k in kapitel)
print(f'Merge OK: {merged} Kapitel übernommen, {skipped} übersprungen')
print(f'Gesamtwörter nach Merge: {total_w}')
"

Gib die Ausgabe des Scripts zurück.`,
  // deprecated
  { label: 'Merge-Legacy (inaktiv)', model: 'haiku' }
)

// ─── ABSCHLUSS ───────────────────────────────────────────────────────────────

const alleCached = [...WELLE1, ...WELLE2]
const nichtFertig = []
for (const item of alleCached) {
  if (!(await istGecacht(item.idx))) nichtFertig.push(item.idx)
}

if (nichtFertig.length > 0) {
  log(`⚠️  Noch nicht gecacht (Budget-Stop): Kapitel ${nichtFertig.join(', ')} — Workflow erneut starten`)
} else {
  log('🎉 Alle 23 Kapitel gecacht und gemergt — Lektorat Welle 1+2 abgeschlossen!')
}
