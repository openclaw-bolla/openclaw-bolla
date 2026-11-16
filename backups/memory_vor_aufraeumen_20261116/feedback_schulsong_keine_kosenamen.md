---
name: feedback-schulsong-keine-kosenamen
description: Bolla-Songs Schulkontext — Schüler:innen nur beim Vornamen ansprechen, KEINE Kosenamen (sweet/dear/Süße/Schatz…), gilt DE und EN, weil der Song von Chris als Lehrer kommt
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-09-01T07:44:30.247Z
---

Bei den **Bolla-Songs im Schulkontext** (Geburtstagssongs für Schüler:innen, `is_school`-Zweig in
`mission_control_api.py`) darf die/der Gefeierte **nur beim Vornamen** angesprochen werden — warm,
wertschätzend, humorvoll, aber genau so, wie eine Lehrkraft mit einer Schülerin / einem Schüler
spricht. **Keine Kose- oder Zärtlichkeitswörter**, weder englisch noch deutsch: kein *sweet, dear,
darling, honey, baby, babe, sweetheart, cutie, love* (als Anrede), kein *Süße/r, Schatz, Liebling,
mein/e Liebe/r, Maus, Hase*. Nichts, was anbahnend oder romantisch klingt. Zuneigung läuft über
Anerkennung, gute Wünsche und ein Augenzwinkern, nicht über Kosenamen.

**Why:** Chris (01.09.2026) fand in der **EN-Version** eines Songs für eine Schülerin „sweet <Name>" —
als Ansprache durch ihn als Lehrer unpassend. Die englische Lyrik-Generierung greift solche
Kosefloskeln von selbst auf, wenn man sie nicht explizit verbietet; die deutsche seltener, aber
das Verbot gilt für beide Sprachen.

**How to apply:** Die Regel steht als `schul_anrede_inst` direkt hinter `jugendfrei_inst` und wird
im `is_school`-Prompt eingefügt (`{jugendfrei_inst}{schul_anrede_inst}{who}`). Bei künftigen
Umbauten am Song-Feature nicht entfernen. Scope bewusst nur Schulkontext — für Familien-/
Release-Songs ([[reference_bolla_songs]]) ist „sweet" o.ä. unkritisch. Verwandt:
[[feedback_geburtstagssong_zeitlos]] (kein Alter, zeitlos), [[feedback_schueler_texte_ton]].
