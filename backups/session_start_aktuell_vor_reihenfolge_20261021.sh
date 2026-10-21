#!/usr/bin/env bash
# SessionStart-Hook: lädt den obersten (= aktuellsten, steht UNTEN) Teil von aktuell.md
# automatisch beim Session-Start in den Kontext. So weiß Bolla sofort,
# woran zuletzt gearbeitet wurde, ohne dass Chris ihn dran erinnern muss.
# Nur das Ende der Datei (neueste Einträge) — die Datei ist zu groß fürs Ganze.

AKTUELL="/home/bolla/.claude/projects/-home-bolla/memory/aktuell.md"

if [ -f "$AKTUELL" ]; then
  echo "=== AKTUELLER ARBEITSSTAND (aktuell.md, neueste Einträge) ==="
  # Datei ist chronologisch, NEU UNTEN (Fix 21.10.2026: vorher head = veraltet) -> tail
  tail -c 9000 "$AKTUELL"
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

# Kuratierte Gesamtliste für "moin" (Chris 21.10.2026: alles was er für moin ansagt MUSS erscheinen)
OFFEN="/home/bolla/workspace/data/offene_punkte.json"
if [ -f "$OFFEN" ]; then
  echo ""
  echo "=== 📋 offene_punkte.json — PFLICHT-QUELLE für die moin-Liste (alle Einträge nennen, nummeriert) ==="
  python3 -c "
import json
for i,p in enumerate(json.load(open('$OFFEN')),1):
    print(str(i)+'. ['+p.get('abschnitt','')+' / '+p.get('gruppe','')+'] '+p.get('titel',''))
" 2>/dev/null
fi
