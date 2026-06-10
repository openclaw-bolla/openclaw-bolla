export const meta = {
  name: 'aurora-nacht-lektorat',
  description: 'Nacht-Job: Lektorat Kap 10-21, Spoiler-Scan alle Kap, PDF + Git + OneDrive',
  phases: [
    { title: 'Lektorat', detail: 'Kap 10-21 parallel mit Haiku' },
    { title: 'Spoiler-Scan', detail: 'Alle ueberblicke auf verbotene Woerter pruefen' },
    { title: 'Bericht', detail: 'Lektorat-Befunde zusammenfassen + speichern' },
    { title: 'Abschluss', detail: 'PDF, Git, OneDrive' },
  ],
}

// ─── PHASE 1: LEKTORAT Kap 10-21 (Haiku, parallel) ────────────
phase('Lektorat')

const LEKT_KAP = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

const LEKT_SCHEMA = {
  type: 'object',
  properties: {
    kapitel_nummer: { type: 'number' },
    kapitel_titel: { type: 'string' },
    befunde: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          typ: { type: 'string' },
          stelle: { type: 'string' },
          problem: { type: 'string' },
          vorschlag: { type: 'string' },
        },
        required: ['typ', 'stelle', 'problem', 'vorschlag'],
      }
    },
    gesamteindruck: { type: 'string' },
    anzahl_befunde: { type: 'number' },
  },
  required: ['kapitel_nummer', 'kapitel_titel', 'befunde', 'gesamteindruck', 'anzahl_befunde'],
}

const lekt_roh = await parallel(
  LEKT_KAP.map(nr => () => agent(
    'Du bist Lektor fuer den deutschen KI-Thriller "AURORA".\n\n' +
    'SCHRITT 1: Lies /home/bolla/workspace/data/ki_buch.json. Extrahiere den Text von Kapitel ' + nr + ' (erkennbar an "Kapitel ' + nr + ':" im Titel).\n\n' +
    'AUFGABE: Lektoriere das Kapitel gruendlich. Suche:\n' +
    '- Grammatikfehler und Tippfehler (konkrete Stellen!)\n' +
    '- Stilistische Schwaechen: Wortwiederholungen im Absatz, sperrige Satzkonstruktionen, Fuellwoerter\n' +
    '- Kontinuitaets-/Timelineprobleme (wenn erkennbar)\n' +
    '- Moegliche Namen/Fakten-Fehler\n' +
    '- Spoiler im "ueberblick"-Feld des Kapitels: VERBOTEN sind "Kind", "Seele", "Mutter", "Auferstehung", "kein Es/Ding", Personennamen als AURORA-Herkunfts-Bezug\n\n' +
    'Fuer jeden Befund: typ (grammatik/tippfehler/stil/kontinuitaet/spoiler), stelle (kurzes Textzitat max 70 Zeichen), problem (was falsch), vorschlag (wie besser).\n\n' +
    'Gesamteindruck in 1-2 Saetzen. anzahl_befunde = Laenge von befunde.',
    { label: 'lektorat:Kap' + nr, phase: 'Lektorat', model: 'haiku', schema: LEKT_SCHEMA }
  ))
)

const lekt_ergebnisse = lekt_roh.filter(Boolean)
log('Lektorat: ' + lekt_ergebnisse.length + '/' + LEKT_KAP.length + ' Kapitel fertig')

// ─── PHASE 2: SPOILER-SCAN ─────────────────────────────────────
phase('Spoiler-Scan')

const SPOI_SCHEMA = {
  type: 'object',
  properties: {
    ergebnisse: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          kapitel_nummer: { type: 'number' },
          kapitel_titel: { type: 'string' },
          verstoss: { type: 'boolean' },
          gefundene_woerter: { type: 'array', items: { type: 'string' } },
          ueberblick_auszug: { type: 'string' },
        },
        required: ['kapitel_nummer', 'kapitel_titel', 'verstoss', 'gefundene_woerter', 'ueberblick_auszug'],
      }
    },
    gesamt_verstoesse: { type: 'number' },
  },
  required: ['ergebnisse', 'gesamt_verstoesse'],
}

const spoiler_scan = await agent(
  'Lies /home/bolla/workspace/data/ki_buch.json.\n\n' +
  'Prüfe das "ueberblick"-Feld JEDES Kapitels (Prolog + alle Kapitel) auf verbotene Spoiler.\n\n' +
  'VERBOTENE WOERTER/KONZEPTE (Gross-/Kleinschreibung ignorieren):\n' +
  '- "Kind", "kindlich", "wie ein Kind"\n' +
  '- "Seele" als Bezug zu AURORA\n' +
  '- "Mutter", "Vater" als Herkunfts-Bezug zu AURORA\n' +
  '- "Auferstehung"\n' +
  '- "kein Es", "kein Ding"\n' +
  '- Personennamen (z.B. "Elias", "Marie" etc.) als Basis/Ursprung von AURORA\n\n' +
  'Fuer JEDES Kapitel zurueckgeben: kapitel_nummer, kapitel_titel, verstoss (true/false), ' +
  'gefundene_woerter (leeres Array wenn keine), ueberblick_auszug (bei Verstoss die Textstelle, sonst leerer String).\n\n' +
  'gesamt_verstoesse = Anzahl Kapitel MIT mindestens einem Verstoss.',
  { label: 'spoiler-scan-alle', phase: 'Spoiler-Scan', model: 'haiku', schema: SPOI_SCHEMA }
)

log('Spoiler-Scan: ' + (spoiler_scan ? spoiler_scan.gesamt_verstoesse + ' Verstoesse' : 'Fehler'))

// ─── PHASE 3: BERICHT ──────────────────────────────────────────
phase('Bericht')

const gesamt_befunde = lekt_ergebnisse.reduce((s, k) => s + (k.anzahl_befunde || 0), 0)

const bericht_agent = await agent(
  'Erstelle einen lesbaren Lektorat-Bericht als Markdown.\n\n' +
  'LEKTORAT-DATEN (Kap 10-21, ' + lekt_ergebnisse.length + ' Kap, ' + gesamt_befunde + ' Befunde gesamt):\n' +
  JSON.stringify(lekt_ergebnisse.map(k => ({
    nr: k.kapitel_nummer, titel: k.kapitel_titel,
    anzahl: k.anzahl_befunde, eindruck: k.gesamteindruck,
    befunde: k.befunde
  }))) + '\n\n' +
  'SPOILER-SCAN-DATEN:\n' + JSON.stringify(spoiler_scan) + '\n\n' +
  'BERICHT-STRUKTUR:\n' +
  '# AURORA Lektorat-Bericht — 2026-06-10\n\n' +
  '## Zusammenfassung\n' +
  '(Gesamtzahl Befunde, welche 3 Kapitel die meisten Probleme haben, Spoiler-Verstoesse)\n\n' +
  '## ⚠️ Spoiler-Verstoesse\n' +
  '(Nur wenn vorhanden — detailliert mit Kapitel + Textstelle + Korrekturvorschlag)\n\n' +
  '## Lektorat-Befunde nach Kapitel\n' +
  '(Kapitel sortiert nach Anzahl Befunde absteigend, je Kapitel: Gesamteindruck + Befundliste)\n\n' +
  '## Empfehlung\n' +
  '(2-3 Saetze: Was sollte Chris zuerst angehen?)\n\n' +
  'Speichere den fertigen Bericht nach:\n' +
  '  /mnt/d/OneDrive/Desktop/AURORA_Lektorat_2026-06-10.md\n' +
  'UND nach:\n' +
  '  /home/bolla/workspace/memory/2026-06-10_lektorat.md\n\n' +
  'Bestaetigung mit Zeilenanzahl und Pfaden.',
  { label: 'bericht-schreiben', phase: 'Bericht' }
)
log('Bericht: ' + bericht_agent)

// ─── PHASE 4: ABSCHLUSS ────────────────────────────────────────
phase('Abschluss')

await agent(
  'Fuehre diese 4 Aufgaben der Reihe nach aus und bestaetge jede:\n\n' +
  '1. PDF GENERIEREN:\n' +
  '   Starte: python3 /home/bolla/workspace/scripts/buch_pdf.py\n' +
  '   Warte auf Abschluss (max 3 Min). Fehler notieren, aber weitermachen.\n\n' +
  '2. AKTUELL.MD UPDATEN (beide Kopien):\n' +
  '   Dateien: /home/bolla/workspace/memory/aktuell.md UND /home/bolla/.claude/projects/-home-bolla/memory/aktuell.md\n' +
  '   Aenderungen:\n' +
  '   - "HALBZEIT-LEKTORAT FÄLLIG" → ✅ Lektorat Kap 10-21 erledigt 2026-06-10\n' +
  '   - Lektorat-Bericht-Pfad erwaehnen: /mnt/d/OneDrive/Desktop/AURORA_Lektorat_2026-06-10.md\n' +
  '   - Gesamtstand aus ki_buch.json lesen und Wortanzahl/Kapitelanzahl aktualisieren\n' +
  '   - Kap 22/23/24 in Stand eintragen (Titel + Wortanzahl aus ki_buch.json lesen)\n\n' +
  '3. GIT COMMIT + PUSH:\n' +
  '   cd /home/bolla/workspace\n' +
  '   git add -A\n' +
  '   git commit -m "Nacht-Job 2026-06-10: Kap 22-24 geschrieben, Kap 10-21 gestrafft, Lektorat-Bericht erstellt"\n' +
  '   git push\n\n' +
  '4. ONEDRIVE-BACKUP:\n' +
  '   cp -a /home/bolla/.claude/. "/mnt/d/OneDrive/Dokumente/Bolla/claude-code/"\n\n' +
  'Am Ende alle 4 Punkte als Checkliste bestaetigen.',
  { label: 'abschluss-alle', phase: 'Abschluss' }
)

return {
  lektorat_kapitel: lekt_ergebnisse.length,
  lektorat_befunde_gesamt: gesamt_befunde,
  spoiler_verstoesse: spoiler_scan ? spoiler_scan.gesamt_verstoesse : 'n/a',
  bericht_pfad: '/mnt/d/OneDrive/Desktop/AURORA_Lektorat_2026-06-10.md',
}
