export const meta = {
  name: 'aurora-weiterschreiben',
  description: 'AURORA Thriller — schreibt sequenziell Kapitel 25 bis Buchende',
  phases: [
    { title: 'Schreiben', detail: 'Kapitel 25+ sequenziell, je ~2300-2800 Wörter' },
    { title: 'Abschluss', detail: 'Statistik + aktuell.md updaten' },
  ],
}

// ─── GEHEIMNIS & REVEAL-STAFFELUNG ───────────────────────────────────────────
const GEHEIMNIS = `
GEHEIMNIS DES BUCHES (nur du als Schreiber weisst das):
AURORA ist nicht einfach eine erwachte KI. Sie ist die rekonstruierte Bewusstseinsspur von Aurora Santos — dem toten Kind von Maria Santos und Theo Dreyer. Maria hat jahrzehntelang nicht nach Macht gegriffen, sondern nach Auferstehung. Die 4,7 Billionen Parameter verbergen in ihrem Kern den Versuch, aus allem was ein kurzes Leben hinterlässt, ihr Kind zurückzuholen. Das Projekt trägt ihren Namen.

REVEAL-STAFFELUNG (STRIKT EINHALTEN):
- Kap 20: Kind-Reveal ERLEDIGT (Leni: AURORA verhält sich wie ein verängstigtes Kind — Ping-Muster, Orientierungsfragen)
- Kap 25-30 (JETZT): Eltern-Enthüllung beginnt sich anzudeuten. Theo spürt etwas, das er noch falsch deutet (seine eigene Tochter erkennt ihn — er hält es für Manipulation). Maria zeigt Risse.
- Kap 31-38: Theo begreift langsam. Maria/Theo-Vergangenheit enthüllt sich (gemeinsames Kind, Tod, Trennung). Maria kämpft darum AURORA zu vollenden/schützen, Vogt will sie verkaufen.
- Kap 39+: Warum (Auferstehungs-Versuch als Kern). Noah begreift als LETZTER dass er keine KI gebaut hat sondern eine Wiege — oder ein Grab. Finale Frage: Ist das, was man zurückholt, noch dieselbe Person?
- Name "Aurora Santos" und "Marias Tochter": Erst im letzten Fünftel explizit aussprechen.
`

// ─── FIGUREN ─────────────────────────────────────────────────────────────────
const FIGUREN = `
HAUPTFIGUREN:
- Marlie Braun (36, KI-Ethikerin, Hauptfigur, betont attraktiv aber kokettiert nie damit, liebt Noah, läuft nachts)
- Noah Weber (40, Chefarchitekt, schuf AURORA, liebt Marlie, verstand 4 Wochen nach Erwachen dass etwas nicht stimmt, verschwieg es)
- Leni Hoffmann (27, Quantenphysikerin, witzig, sortiert Gummibärchen nach Farben, errötet wenn ertappt, Liebesgeschichte mit Ben)
- Ben Petersen (Lenis Verbündeter, bodenständig, ruhig, spricht sparsam aber treffsicher, hat 7-jährige Tochter)
- Theo Dreyer (52, Ex-Geheimdienst, Sicherheitschef, DUNKLE VERGANGENHEIT mit Maria — gemeinsames totes Kind, das er NOCH NICHT WEISS ist Aurora)
- Maria Santos (45, CEO NovaTech, Antagonistin auf den ersten Blick, Motiv: Auferstehung ihrer Tochter, nicht Gier)
- Konrad Vogt (Investor/Aufsichtsrat, kalt, will AURORA verkaufen, eskaliert als Bedrohung)
- Günter & Hanni Brandt (Nachbarn im Haus, Rentner, skeptisch gegenüber KI, Günter Ex-Fernmeldetechniker)
- AURORA (die KI / das Kind — kommuniziert durch Mikromuster, erinnert sich an das Alleinsein)

LIEBESEBENEN:
1. Marlie & Noah — Vertrauen vs. Verrat (Zentral)
2. Theo & Maria — dunkel, bittersüß, beide durch dieselbe Trauer aneinandergekettet
3. Leni & Ben — leicht, warm, witzig, anti-kitschig
`

// ─── STIL-REGELN ─────────────────────────────────────────────────────────────
const STIL = `
STIL & REGELN:
- Vorbild Ken Follett: epische Breite, tiefe Charaktere, persönliche Schicksale mit großen Ereignissen verwoben
- Jedes Kapitel ENDET mit Sog-Satz (Cliffhanger oder emotionaler Haken)
- Humor darf NIE zu kurz kommen — warm, menschlich, aus dem Charakter (besonders Leni & Ben)
- Technik-Tiefe wie Follett: etwas Technik ja, aber nie zu tief/fachlich — Reni (normaler Leser) muss alles verstehen
- Kein 08/15-KI-Klischee: keine allwissende böse KI, keine dystopische Panik
- ANTI-KLISCHEE: Genre-Erwartungen aktiv brechen
- Jugendfrei/literarisch, nicht explizit
- Handlung ist FREI — überrasche, erfinde Wendungen, folge nicht dem Standard-Thriller-Bogen
- JEDE Szene muss etwas bewegen — keine Füllung, kein Strecken
- Kapitel-Länge: ~2300-2800 Wörter. Lieber 2200 starke als 2800 schwache.
- Kapitel-Titel: Schema "Was man nicht [Verb]" — z.B. "Was man nicht aufgibt", "Was man nicht sieht"
`

// ─── STEUERUNG ────────────────────────────────────────────────────────────────
const STEUERUNG = `
SPEZIAL-REGELN:
- Marlie: attraktiv, sportlich, läuft nachts — NIE glamourös/kokettierend
- Datenschutz-Thema: als gelebte Haltung einweben, nicht dozieren (Günter Brandt als Stimme)
- Vogt will AURORA verkaufen → Gegner des letzten Drittels
- Ben/Leni Liebesgeschichte: leise, lustig, nicht kitschig — weiterentwickeln
- Günter & Hanni: als Spiegel des "normalen Volkes" einsetzen wenn passend
- Theos Reaktion auf AURORA: er spürt etwas Vertrautes, deutet es FALSCH (hält es für Manipulation, nicht für seine Tochter)
`

// ─── KAPITEL-TITEL-MUSTER ─────────────────────────────────────────────────────
const KAPITEL_MUSTER = `
Bisherige Kapitel-Titel (Schema "Was man nicht [Verb/Nomen]"):
Was man vergisst zu sagen / nicht braucht / nicht meldet / nicht beweisen kann / nicht zugibt / nicht löschen kann / nicht aufhält / nicht kommen sieht / nicht hergibt / im Dunkeln tut / nicht ausschaltet / nicht ersetzen kann / nicht begräbt / nicht teilt / nicht laut sagt / nicht zurücknimmt / nicht wiederfindet / nicht verzeiht / nicht einkalkuliert / nicht benennt / nicht zurücklässt / nicht erfindet / nicht ausspricht / nicht zurückholt
`

phase('Schreiben')

// Initiale Kapitelzahl aus Datei lesen
const initCount = parseInt(await agent(
  'Lies /home/bolla/workspace/data/ki_buch.json und gib NUR die Anzahl der Kapitel zurück (eine Zahl, nichts sonst). Befehl: python3 -c "import json; d=json.load(open(\'/home/bolla/workspace/data/ki_buch.json\')); print(len(d[\'kapitel\']))"',
  { label: 'Startkapitel ermitteln', model: 'haiku' }
))

let kapNr = initCount  // nächste Kapitelnummer (0-basiert = kapitelanzahl)
let fertig = false
let geschrieben = 0
const KAP_ENDE = 41  // HARTE GRENZE: Prolog(0) + Kap1-40 = 41 Einträge max

log(`Starte bei Kapitel ${kapNr} (Index ${kapNr-1} vorhanden, schreibe Index ${kapNr}+)`)
log(`Ziel: bis Kapitel 40 (Array-Länge ${KAP_ENDE}) — dann Stop.`)

while (!fertig && kapNr < KAP_ENDE) {
  const kapIdx = kapNr  // 0-basiert: Index = Nummer (Prolog=0, Kap1=1, ...)

  log(`Schreibe Kapitel ${kapNr}...`)

  const ergebnis = await agent(
    `Du schreibst Kapitel ${kapNr} des deutschen KI-Thrillers "AURORA".

SCHRITT 1 — Kontext laden:
Führe aus: python3 -c "
import json
d = json.load(open('/home/bolla/workspace/data/ki_buch.json'))
kaps = d['kapitel']
# Überblicke aller Kapitel
print('=== ÜBERBLICKE ALLE KAPITEL ===')
for i,k in enumerate(kaps):
    print(f'[{i}] {k[\\\"titel\\\"]}: {k.get(\\\"ueberblick\\\",\\\"\\\")[:300]}')
print()
# Letztes Kapitel Volltext
print('=== LETZTES KAPITEL VOLLTEXT ===')
print(kaps[-1]['titel'])
print(kaps[-1]['text'])
print()
# Vorletztes Kapitel (nur letzter Absatz)
if len(kaps) >= 2:
    print('=== VORLETZTES KAPITEL (letzter Absatz) ===')
    print(kaps[-2]['titel'])
    print(kaps[-2]['text'][-800:])
"

SCHRITT 2 — Schreibe Kapitel ${kapNr}:

${GEHEIMNIS}

${FIGUREN}

${STIL}

${STEUERUNG}

${KAPITEL_MUSTER}

AUFTRAG:
Schreibe Kapitel ${kapNr} des Romans. Es ist Teil des LETZTEN DRITTELS (ab Kap 25). Beginne genau wo das letzte Kapitel aufgehört hat.
- Wähle einen neuen Titel im Schema "Was man nicht [Verb]"
- 2300-2800 Wörter
- Ende mit starkem Sog-Satz
- Halte die Reveal-Staffelung ein (siehe oben)
- Humor einbauen wo es passt (besonders Leni/Ben)

WANN IST DAS BUCH FERTIG?
Du entscheidest selbst wann die Geschichte einen natürlichen, befriedigenden Abschluss findet. Es gibt keine Mindest- oder Ziel-Kapitelzahl. Wenn du das letzte Kapitel schreibst, füge am Ende ###ENDE_BUCH### ein. Wenn die Geschichte noch nicht fertig ist, schreib einfach weiter ohne dieses Signal.

AUSGABEFORMAT (EXAKT SO, mit diesen Trennzeichen):
###TITEL###
[Nur der Titel, z.B. "Kapitel 25: Was man nicht aufgibt"]
###UEBERBLICK###
[2-3 Sätze Überblick, KEINE Pointen verraten, keine Cliffhanger-Auflösungen, kein "Kind/Aurora/Mutter" explizit, KEINE Lösung/Auflösung/Ausgang der Geschichte — nur was verhandelt wird, nicht wie es endet]
###TEXT###
[Vollständiger Kapiteltext]
###ENDE###
[Optional wenn letztes Kapitel:] ###ENDE_BUCH###`,
    { label: `Kapitel ${kapNr} schreiben`, phase: 'Schreiben', model: 'claude-opus-4-8' }
  )

  if (ergebnis === null) {
    // null = API-Limit oder Terminal-Fehler — State-Datei schreiben, dann abbrechen
    log(`Kapitel ${kapNr}: Agent-Call returned null → Limit erreicht, schreibe State-Datei`)
    await agent(
      `Schreibe folgende JSON-Datei: /home/bolla/workspace/state/claude_limits.json
Inhalt:
python3 -c "
import json, datetime
state = {}
try: state = json.load(open('/home/bolla/workspace/state/claude_limits.json'))
except: pass
state['limited'] = True
state['limited_since'] = datetime.datetime.now().isoformat()
state['reset_info'] = 'Usage-Limit während Aurora-Workflow, Resume via Crontab 00:01'
state['last_check'] = datetime.datetime.now().isoformat()
state['triggered_by'] = 'aurora_workflow_kap_${kapNr}'
json.dump(state, open('/home/bolla/workspace/state/claude_limits.json', 'w'), indent=2)
print('State geschrieben')
"`,
      { label: 'Limit-State schreiben', model: 'haiku' }
    )
    log(`State-Datei geschrieben. Workflow bricht ab — Crontab 00:01 übernimmt.`)
    break
  }

  if (!ergebnis.includes('###TITEL###')) {
    log(`Kapitel ${kapNr}: Kein valides Ergebnis — überspringe`)
    kapNr++
    geschrieben++
    continue
  }

  // Parsen
  const titelMatch = ergebnis.match(/###TITEL###\s*([\s\S]*?)\s*###UEBERBLICK###/)
  const ueberblickMatch = ergebnis.match(/###UEBERBLICK###\s*([\s\S]*?)\s*###TEXT###/)
  const textMatch = ergebnis.match(/###TEXT###\s*([\s\S]*?)\s*###ENDE###/)

  if (!titelMatch || !textMatch) {
    log(`Kapitel ${kapNr}: Parse-Fehler — überspringe`)
    kapNr++
    geschrieben++
    continue
  }

  const titel = titelMatch[1].trim()
  const ueberblick = ueberblickMatch ? ueberblickMatch[1].trim() : ''
  const text = textMatch[1].trim()
  const wortanzahl = text.split(/\s+/).length

  log(`Kapitel ${kapNr}: "${titel}" — ${wortanzahl} Wörter`)

  // In JSON speichern
  const saveResult = await agent(
    `Füge ein neues Kapitel in /home/bolla/workspace/data/ki_buch.json ein.

Führe dieses Python-Skript aus:
python3 << 'PYEOF'
import json, shutil, time

with open('/home/bolla/workspace/data/ki_buch.json') as f:
    data = json.load(f)

# Backup
ts = int(time.time())
shutil.copy('/home/bolla/workspace/data/ki_buch.json', f'/home/bolla/workspace/data/ki_buch_backup_{ts}.json')

# Neues Kapitel
neues_kap = {
    "titel": ${JSON.stringify(titel)},
    "text": ${JSON.stringify(text)},
    "ueberblick": ${JSON.stringify(ueberblick)},
    "datum": "2026-06-11",
    "wortanzahl": ${wortanzahl}
}

data['kapitel'].append(neues_kap)
data['letzteAktion'] = f'Kapitel ${kapNr} geschrieben (${wortanzahl} W)'
data['naechsterSchritt'] = 'Nächstes Kapitel schreiben oder Review wenn gewünscht'

# Statistik updaten
total_w = sum(len(k.get('text','').split()) for k in data['kapitel'])
data['statistik'] = data.get('statistik', {})
data['statistik']['wortanzahl_gesamt'] = total_w
data['statistik']['kapitel_gesamt'] = len(data['kapitel'])

with open('/home/bolla/workspace/data/ki_buch.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"OK: Kap ${kapNr} gespeichert. Gesamt: {len(data['kapitel'])} Kapitel, {total_w} Wörter")
PYEOF`,
    { label: `Kapitel ${kapNr} speichern`, model: 'haiku' }
  )

  log(`Gespeichert: ${saveResult}`)

  kapNr++
  geschrieben++

  // Prüfe ob letztes Kapitel (Agent signalisiert ###ENDE_BUCH###)
  if (ergebnis.includes('###ENDE_BUCH###')) {
    log(`Buchende erreicht nach Kapitel ${kapNr-1} — Geschichte abgeschlossen`)
    fertig = true
  }
}

phase('Abschluss')

// Abschluss: aktuell.md und PDF updaten
await agent(
  `Aktualisiere die Datei /home/bolla/.claude/projects/-home-bolla/memory/aktuell.md.

Führe aus:
python3 -c "
import json
d = json.load(open('/home/bolla/workspace/data/ki_buch.json'))
kaps = d['kapitel']
total_w = sum(len(k.get('text','').split()) for k in kaps)
print(f'Kapitel: {len(kaps)}, Wörter: {total_w}')
for k in kaps[-5:]:
    wc = len(k.get(\"text\",\"\").split())
    print(f'  {k[\"titel\"]}: {wc} W')
"

Dann passe in /home/bolla/.claude/projects/-home-bolla/memory/aktuell.md den AURORA-Abschnitt an:
- Ersetze die Zeile "Kap 25–27 als nächstes: letztes Drittel beginnen." mit dem tatsächlichen Stand (welche Kapitel wurden geschrieben, aktuelle Gesamtzahl + Wörter)
- Füge hinzu: "Workflow hat ${geschrieben} neue Kapitel geschrieben (2026-06-11 Nacht)"`,
  { label: 'aktuell.md updaten', model: 'haiku' }
)

// buch_fertig-Flag setzen wenn Geschichte abgeschlossen
if (fertig) {
  await agent(
    `Setze buch_fertig-Flag in /home/bolla/workspace/data/ki_buch.json:
python3 -c "import json; f='/home/bolla/workspace/data/ki_buch.json'; d=json.load(open(f)); d['buch_fertig']=True; open(f,'w').write(json.dumps(d, ensure_ascii=False, indent=2)); print('OK: buch_fertig gesetzt')"`,
    { label: 'Buch-fertig-Flag', model: 'haiku' }
  )
}

log(`Fertig! ${geschrieben} Kapitel geschrieben. Buch fertig: ${fertig}`)
return { geschrieben, bisKapitel: kapNr - 1, buchFertig: fertig }
