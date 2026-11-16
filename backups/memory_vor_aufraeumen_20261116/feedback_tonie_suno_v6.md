---
name: feedback-tonie-suno-v6
description: Tonie-Songs nach Suno-v6-Regeln erzeugen (Exclude-Feld, Klammer-Tags, Variety Off); Chris nutzt v6
metadata:
  type: feedback
---
Chris verwendet in Suno **v6**; Tonie-Song-Prompt (`_tonies_job` in mission_control_api.py) folgt v6-Regeln: Sektions-Tags mit Vortragsanweisung `[Verse 1 | soft warm vocal, ...]`, Style ≤~500 Zeichen ohne Verneinungen/Qualitätswörter/Künstlernamen, Negatives ins **Exclude**-Feld (≤6 Begriffe), Variety=Off, Style Influence hoch. Geräusch-Tags wie [dog barks] werden von Suno IGNORIERT (Test Chris 25.10.) – nicht mehr verwenden, nur gesungene Lautmalerei. Sektions-Anweisungen in [] funktionieren.
**Why:** Chris-Wunsch 25.10.2026; Quellen sind Blogs, nur Exclude von Suno bestätigt. **How to apply:** auch bei anderen Suno-Songs (Bolla Songs, Geburtstagssongs) v6-Regeln beachten; Ergebnis des Geräusch-Tag-Tests nachtragen. Siehe [[project_tonie_zwillinge]], [[feedback_suno_lyrics_qualitaet]].

## Mitsing-Refrain (Chris 25.10.2026)
- Song-Prompt (`_tonies_job`, scripts/mission_control_api.py) verlangt Mitsing-Refrain: 4 kurze, gleich lange, gereimte Zeilen, wortgleich wiederholt, Vorname + 1–2 Mitmach-Silben, keine Frage. Vorbild: „Weihnachtskinderküche“ (Kinder singen den Refrain bis heute mit). Mia (5) darf in den Strophen lebendiger/witziger sein (Chris fand ihren ersten Song zu seicht), Zwillinge nur Lautmalerei + Name.
- Alle 3 Songs 25.10. neu erzeugt (Backups backups/*_mitsing_*, *_vor_mitsing_*); Unsinnswörter („gerief“, „Koffeln“) von Hand korrigiert. Nach Neuerzeugung immer auf Unsinnswörter prüfen.

## Humor + Opa & Oma zusammen (Chris 25.10.2026)
- In JEDEM Tonie-Song/-Text kommen Opa (Chris) UND Oma (Reni) gemeinsam vor — „wir machen alles zusammen“. Chris ist der Spaßmacher, Mia (5) kennt ihn so.
- Mia: deutlich mehr Humor (Wortwitz, Opa als Tollpatsch, Oma trocken-konternd), Refrain kurz. Zwillinge: kein Wortwitz, nur Quatsch-Geräusche/Slapstick (Opa macht Wau/Brumm, Oma macht mit). Regel (6) im Song-Prompt von `_tonies_job`. Keine erfundenen Unsinnswörter, kein Alkohol-Bezug in Kinderliedern.
- Songs 25.10. abends damit neu erzeugt (Backups backups/*_vor_humor_oma_*).

## Mia-Song Korrekturen (Chris 25.10.2026 abends)
- Opa Chris trägt KEINE Brille (künstliche Linsen, [[user_sehvermoegen]]) → nie Brillen-Witze; Witze allgemein (Hut/Handy/Schlüssel suchen, stolpern). Steht im Song-Prompt.
- Mia-Refrain nicht zu simpel: 4–6 Zeilen mit Bild/Pointe + genau EINE wortgleiche Mitmach-Zeile („Klatsch, klatsch, hurra, Mia!“). Zwillinge bleiben bei reiner Lautmalerei-Refrain.
- Länge (25.10.): Zwillinge-Songs ca. 1:30–2 Min (≈85 Wörter) ok; Mia ca. 3 Min (3 Strophen + Bridge, ≈220 Wörter) — Prompt `_tonies_job` entsprechend.
- Reim-Regel (7) im Song-Prompt (25.10.): erst Reimpaare festlegen (AABB, echte Wörter), Reimwort ans Zeilenende, dann Zeile für Zeile prüfen (Reim, Silben ±2, normales Deutsch), keine Füllwörter, keine verwaisten Zeilen. Wirkt erst bei NEUER Erzeugung.
