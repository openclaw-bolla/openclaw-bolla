---
name: feedback-ui-prompt-iteration-deutsch
description: Wiederverwendbares MP-UI-Muster — Chris feilt auf Deutsch iterativ an einem englischen/technischen KI-Prompt, ohne ihn selbst anzufassen
metadata:
  node_type: memory
  type: feedback
  originSessionId: 0deb2e12-ac31-4014-8964-1e949e1f41e9
  modified: 2026-09-10T20:30:55.686Z
---

# UI-Muster „deutsch iterativ am Prompt feilen" — bewährt 10.09.2026

Chris' O-Ton: „jetzt klappt das Chatten, meine Wünsche werden eingebaut, wir arbeiten eben am
optimalen Prompt. Merk dir mal diesen Prozess bzw. die Abbildung in MP — vielleicht brauchen wir
das nochmal an anderer Stelle."

## Das Muster (3 Knöpfe + 2 Felder)
1. **„📝 Vorschlag holen"** → Server (claude, gratis) erzeugt die erste technische/englische
   Fassung aus dem Kontext (Titel, Text, …). Landet in einem **read-only Feld** (gestrichelter
   Rahmen, sichtbarer Hinweis „musst du nicht anfassen"). In JS-Var gecacht.
2. **Deutsches ✏️-Feld** + **„🔧 In den … einbauen (gratis)"** → Server nimmt
   `prev = <gecachte Fassung>` + `wunsch = <deutscher Text>` und baut die Änderung ein
   (claude, gratis, **kein teurer Schritt**). Read-only Feld wird aktualisiert, ✏️-Feld geleert.
   Beliebig oft wiederholbar. Ohne vorherigen Vorschlag baut es die erste Fassung aus dem Wunsch.
3. **„▶️ Ausführen"** (hier: „🎨 Cover erzeugen" gratis / „🌟 Finale in HD" ~10 ct) → nimmt die
   aktuelle Fassung aus dem read-only Feld und führt die teure/finale Aktion aus.

## Warum
- Chris' Englisch reicht nicht, um einen EN-Prompt selbst zu editieren („mein Englisch ist nicht
  gut genug"), er will solche Sachen **in MP statt im Terminal** machen.
- Zufalls-Neugenerierung bei jedem Klick verbrennt Geld — das billige „Einbauen" (claude-Text,
  kein Bild/keine teure API) trennt das Feilen sauber vom teuren Ausführen.
- Chris sieht den Prompt (Kontrolle, Nachvollziehbarkeit), muss ihn aber nie tippen.

## How to apply
Wenn irgendwo in MP ein KI-Artefakt iterativ verfeinert werden soll (Bild-Prompt, Suno-Style,
Mail-Entwurf, Anschreiben, Bewerbungstext, Aufgabenblatt-Prompt …) und die „rohe" Fassung
technisch/englisch/lang ist: **dieses Muster nachbauen**, nicht ein Freitextfeld mit englischem
Prompt. Referenz-Implementierung: Suno „🎵 Song herunterladen + Cover erstellen", Schritt 3.
- Endpunkte-Vorbild: `POST /api/suno/cover-prompt` (Vorschlag), `POST /api/suno/cover-wish` mit
  `render:false` (deutsche Änderung einbauen, kein Ergebnis), `POST /api/suno/cover-render`
  (ausführen). Prompt-Bau-Helper: `_suno_cover_prompt_from_wish(title, ctx, wish, prev_prompt="")`
  in `mission_control_api.py` — Instruktion an claude: „nimm CURRENT prompt, bau die auf Deutsch
  formulierte Änderung ein, behalte was gut war, gib EINE Fassung zurück".
- JS-Vorbild: `sunoCoverSuggest()` / `sunoCoverRefine()` / `sunoCoverRenderNow()` in `index.html`.

Verwandt: [[project_bolla_songs_cover_deutsch]], [[feedback_mp_chat_feedback]],
[[feedback_ki_texte_natuerlich]].
