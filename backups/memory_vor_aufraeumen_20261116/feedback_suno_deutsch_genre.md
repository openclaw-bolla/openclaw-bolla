---
name: feedback-suno-deutsch-genre
description: Suno — deutscher Gesang + Singalong-Shuffle = Schlager-Falle; für DE feel-good lieber Rap/Reggae
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3f696bca-1fae-44a2-97bf-c746cbc047c1
  modified: 2026-08-19T15:44:09.347Z
---

# Suno: deutsche Songs nicht in die Schlager-Falle laufen

**Erkenntnis (29.06.2026):** Style-Bauweise „jug-band/skiffle shuffle + bouncy major key + gesungener
Da-da-da-Singalong-Refrain" klingt auf **Englisch** nach retro feel-good — auf **Deutsch** kippt sie sofort
ins **Schlagerhafte**. Erste DE-Version "Der Sommer ruft" (Pop) = von Chris als „schrott / zu schlagerhaft" verworfen.

**Why:** Deutscher Gesang + eingängiger Singalong-Refrain triggert beim Hörer sofort Schlager-Assoziation,
egal wie modern der Text ist.

**How to apply:** Für deutsche Feel-good-Songs Genre bewusst weg vom gesungenen Pop-Singalong wählen:
- **Summer-Deutschrap** (gerappte Strophen + gesungener Hook, ~85–90 BPM) ← Chris' Wahl, funktioniert
- Reggae/Dancehall, Afrobeats/Amapiano, Dance/House sind die sicheren Alternativen
Im Zweifel Chris die Richtung wählen lassen, BEVOR generiert wird (spart Fehl-Takes).

Siehe [[feedback_suno_style_no_names]], [[project_distrokid_desktop_staging]].

**19.08.2026 — Code-Fix bestätigt wirksam.** Konkreter Fall Niklas/7b, Hitwunsch "Hey Baby" (DJ Ötzi) — kuratiertes DE-Mapping selbst schon Schlager-/Ballermann-typisch (Akkordeon, Crowd-Singalong, festive). In `mission_control_api.py` (`/api/suno/generate`) zwang der Prompt bei "bekannten Songs" bisher "Kerncharakteristik MUSS erhalten bleiben" — Widerspruch zur Schlager-Vermeidung hier. Fix: neue Prüfung `_hit_is_schlager_prone` (sprache=="de" + Mapped-Style enthält Schlager-Marker) gibt dem Modell dann Freiheit, Richtung summer deutschrap/reggae/dancehall/afrobeats/amapiano/house zu tauschen statt originalgetreu zu bleiben. Chris' Rückmeldung nach Neugenerierung: "viel besser - songs waren ok". Restliche Qualitätslücke vermutlich v5.5-Grundrauschen (Community-bekannt), nicht Text/Style — siehe [[feedback_suno_lyrics_qualitaet]] A/B-Test 17.08.

**How to apply:** Bei künftigen "Song klingt schlecht"-Meldungen mit deutschem Hitwunsch zuerst prüfen, ob der gemappte Style in `_DE_SONG_STYLE_MAP` Schlager-Marker enthält (accordion/crowd sing-along/festive/volksmusik/oompah/schlager/party pop) — falls ja, greift der Fix bereits automatisch. Erst danach an Modellwahl (v5.5) denken.
