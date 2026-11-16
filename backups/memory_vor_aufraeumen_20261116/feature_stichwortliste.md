---
name: feature-stichwortliste
description: "Dashboard-Stichwortliste in MP — Chris nennt Projekt-Stichworte, Bolla pflegt sie IMMER mit (Dauerauftrag)"
metadata: 
  node_type: feedback
  type: feedback
  originSessionId: 86911b2b-9f30-4e9f-a515-f8c0828b703b
---

⭐ **DAUERAUFTRAG (von Chris ausdrücklich betont 24.06.2026): Die MP-Stichwortliste NIE vergessen und IMMER mitpflegen.**

Chris kann sich die Projekte, die er mir nennt, schlecht merken — die Liste ist sein Gedächtnis-Anker. Deshalb ist Pflege Pflicht, nicht Kür.

**Why:** Eine veraltete Liste ist schlimmer als keine — Chris verlässt sich drauf. (Beispiel: IngramSpark stand noch als „durchführen", obwohl längst verworfen → am 24.06. weggeräumt.)

**How to apply — bei JEDER Session und JEDER Projekt-Änderung dran denken:**
- Nennt Chris ein neues Projekt-Stichwort → **sofort eintragen** (`/api/stichworte/add`).
- ⭐ **PROAKTIV AUTOMATISCH (Chris 05.07.2026): Entstehen im Gespräch offene To-Dos / künftige Arbeitsschritte, die NICHT sofort erledigt werden → automatisch als Stichwort eintragen, ohne dass Chris drum bittet.** Er will alles Offene im Dashboard sichtbar haben (sein Gedächtnis-Anker). Gilt auch für mehrteilige Vorhaben: jeden noch offenen Teilschritt einzeln listen, damit einzeln abhakbar. Beispiel: AURORA-Marketing-Plan → je Schritt (Seite live, Presse, Essay, Fachwelt) ein Eintrag.
- Ändert sich ein Projektstatus (erledigt, verworfen, Meilenstein) → **Liste sofort angleichen**. Bei „erledigt" proaktiv kurz nachfragen, dann auf done (✅) setzen; verworfene/abgeschlossene Einträge wegräumen.
- Wenn ich an einem gelisteten Projekt arbeite → checken, ob der Eintrag noch stimmt.

**Wo:** Dashboard-Box „📁 Projekte". Oben Schul-Nächsttermine (leer bis August), darunter Stichwortliste mit `Stichwort + Projektbeschreibung`.

**🔢 Nummerierung (seit 24.06.2026):** Jeder Eintrag hat links ein **lila Nummern-Badge** (laufende Position 1..N in Listenreihenfolge, `loadStichworte()` rendert via `items.map((it,idx)=>...)` mit `nr=idx+1`). Chris stupst per Nummer an („Nummer 3 ist durch"). → Beim Anstupsen die `/api/stichworte`-items **in Reihenfolge zählen (1-basiert)**, Position = Nummer. ⚠️ Nicht stabil bei Löschungen (Positionen rutschen nach) — immer die AKTUELLE Liste zählen, nicht aus dem Gedächtnis.

**Technik:**
- Daten: `~/workspace/data/stichworte.json` (`{items:[{id,name,projekt,done}]}`)
- API in `mission_control_api.py`: GET `/api/stichworte`, POST `/api/stichworte/add` `{name,projekt}` · `/toggle` `{id}` · `/delete` `{id}` (kein edit — Beschreibung ändern = delete + add oder JSON direkt).
- Frontend `index.html`: `loadStichworte()/addStichwort()/toggleStichwort()/deleteStichwort()`, Box-Render via `loadCalendarData()`

Siehe auch [[user_chris_teacher]] (Box füllt sich erst ab August wieder) und [[reference_mc]].
