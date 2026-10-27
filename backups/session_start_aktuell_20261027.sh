#!/usr/bin/env bash
# SessionStart-Hook: lädt den obersten (= aktuellsten, steht UNTEN) Teil von aktuell.md
# automatisch beim Session-Start in den Kontext. So weiß Bolla sofort,
# woran zuletzt gearbeitet wurde, ohne dass Chris ihn dran erinnern muss.
# Nur das Ende der Datei (neueste Einträge) — die Datei ist zu groß fürs Ganze.

# Kuratierte Gesamtliste für "moin" (Chris 21.10.2026: alles was er für moin ansagt MUSS erscheinen)
OFFEN="/home/bolla/workspace/data/offene_punkte.json"
if [ -f "$OFFEN" ]; then
  echo ""
  echo "=== 📋 offene_punkte.json — PFLICHT-QUELLE für die moin-Liste (alle Einträge nennen, nummeriert) ==="
  python3 -c "
import json, datetime
# Montags-Reminder (Chris 26.10.2026): nur wenn in dieser Woche Kurstage laut schuljahr2627.json (Ferien sind dort schon ausgenommen)
t = datetime.date.today()
if t.weekday() == 0:
    try:
        ter = json.load(open('/home/bolla/workspace/data/schuljahr2627.json')).get('termine', [])
        wk = [x for x in ter if 0 <= (datetime.date.fromisoformat(x['datum']) - t).days <= 6]
        if wk:
            tage = sorted({x['datum'][8:10]+'.'+x['datum'][5:7]+'. '+x['wochentag']+' (Kurstag '+x['thema'].split(' ')[0]+', Gr. '+x['gruppe']+')' for x in wk})
            print('>>> MONTAGS-ERINNERUNG (als ERSTER Punkt der moin-Liste, Kategorie Zuerst): itslearning-Mitteilung steht an. Kurse diese Woche: '+'; '.join(tage))
    except Exception as e:
        pass
# Dienstags-Eintrag (Chris 26.10.2026): Mitteilung wird immer DIENSTAG der Kurstag-Woche gepostet
if t.weekday() == 1:
    try:
        ter = json.load(open('/home/bolla/workspace/data/schuljahr2627.json')).get('termine', [])
        wk = [x for x in ter if 1 <= (datetime.date.fromisoformat(x['datum']) - t).days <= 3]
        if wk:
            print('>>> DIENSTAGS-ERINNERUNG (als ERSTER Punkt der moin-Liste): HEUTE itslearning-Mitteilung posten (Kurstag '+wk[0]['thema'].split(' ')[0]+', Gr. '+wk[0]['gruppe']+'; Kurse Mi/Do). Status prüfen: Post-Cron gelaufen? (Telegram-Rückmeldung / Log workspace/logs/itslearning_kurstag*_cron.log), sonst jetzt posten.')
    except Exception as e:
        pass
# Sortiert nach prio (1 = wichtigste); Nummern = Reihenfolge der Ausgabe
items = sorted(json.load(open('$OFFEN')), key=lambda p: int(p.get('prio', 99)))
for i, p in enumerate(items, 1):
    print(str(i)+'. [prio '+str(p.get('prio'))+' | '+p.get('abschnitt','')+' / '+p.get('gruppe','')+'] '+p.get('titel',''))
" 2>/dev/null
fi

AKTUELL="/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md"

if [ -f "$AKTUELL" ]; then
  echo "=== AKTUELLER ARBEITSSTAND (aktuell.md, neueste Einträge) ==="
  # Datei ist chronologisch, NEU UNTEN (Fix 21.10.2026: vorher head = veraltet) -> tail
  tail -c 3500 "$AKTUELL"
  echo ""
  echo "=== (aktuell.md gekürzt — bei Bedarf komplett lesen) ==="
fi

# Anstups-Queue (Projekt-Board): von Chris via MP angestoßene Projekte anzeigen
NUDGES="/home/bolla/workspace/data/board_nudges.json"
if [ -f "$NUDGES" ]; then
  COUNT=$(python3 -c "import json;print(len(json.load(open('$NUDGES')).get('nudges',[])))" 2>/dev/null || echo 0)
  if [ -n "$COUNT" ] && [ "$COUNT" != "0" ]; then
    echo ""
    echo "=== 📌 ANSTUPS-QUEUE ($COUNT) — Chris hat diese Projekte via MP-Board angestoßen, bitte abarbeiten ==="
    python3 -c "
import json
for n in json.load(open('$NUDGES')).get('nudges',[]):
    print('• ' + n.get('title','') + '  (' + n.get('ts','') + ')')
    print(n.get('prompt',''))
    print('---')
" 2>/dev/null
    echo "=== Nach Erledigung Queue leeren: data/board_nudges.json auf {\"nudges\":[]} setzen ==="
  fi
fi

