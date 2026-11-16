---
name: feedback-sr-route-apostroph
description: Nie Apostrophe/Kontraktionen in SR_ROUTE-Textfeldern (index.html) verwenden — bricht den regex-Parser
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 813902cf-a4a5-48f4-aad8-c5f5b904f5ec
---

In `mission-control/index.html` liegt die Reiseplan-Datenquelle `SR_ROUTE` als Array einfach gequoteter JS-Strings (`'...'`), u.a. `tagesplan`, `highlights`, `hlInfo`. Diese werden in `scripts/mission_control_api.py` (`_reise_stationen_full()`) per Regex geparst — **kein echter JS-Parser**, der Escapes versteht, sondern ein simples `'((?:[^'\\]|\\.)*)'`-Muster.

**Nie Apostrophe/Kontraktionen** wie „wer's", „geht's", „hier's" in diese Textfelder schreiben — der literale `'` beendet den String vorzeitig, der Rest des Arrays wird stillschweigend falsch geparst (keine Fehlermeldung, einfach fehlende/leere Einträge). Immer ausschreiben: „wer es", „geht es".

**Why:** Beim Ausbau des Kaiserstuhl-Tagesplans (08.07.2026) hat ein einziges „wer's" den kompletten `tagesplan`-Array der Freiburg-Station von 5 auf 2 wirksame Einträge einbrechen lassen — bemerkt nur, weil danach testweise die Einträge gezählt wurden.

**How to apply:** Nach JEDER Textänderung an `tagesplan`/`highlights`/`hlInfo` in `SR_ROUTE` kurz per Python verifizieren, dass die erwartete Anzahl Einträge zurückkommt (`_reise_stationen_full()` aufrufen, Länge checken), bevor man die Änderung als erledigt meldet.
