---
name: reference-bolla-songs
description: "Schüler-Geburtstagslieder werden über die Site \"Bolla Songs\" erstellt, nicht über Claude"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2430877f-7d01-4a18-a5f2-d3b0d3b27139
---

Für Schüler-Geburtstagslieder nutzt Chris die Site **"Bolla Songs"** — nicht Claude.

**How to apply:** Wenn Chris nach Geburtstagslieder für Schüler fragt, auf Bolla Songs verweisen statt selbst Songs zu generieren.

## Songtexte kommen von Bolla (KI) via „Bolla Songs" in MP — nicht von Suno
Die **Songtexte** entstehen über „Bolla Songs" (in MP) = von **Bolla/Claude** geschrieben — deutlich besser als Sunos Auto-Lyrics. Suno liefert nur Musik/Audio-Rendering.

**How to apply (KI-Deklaration, z.B. DistroKid „Welche Teile sind KI?"):** Der Songtext ist KI-generiert (von Bolla, nicht Suno) → Haken **„Songtext von KI geschrieben" DRIN lassen**. Ehrliche Deklaration = alle drei: Songtext ✅ · Musik ✅ · ggf. Audio ✅ (KI-Transparenz ist Chris wichtig, [[user-ki-transparenz]]). **ABER:** Songwriter-/Rechte-Feld = **Christoph Mandel** (Chris beauftragt/kuratiert/hält die Rechte — das ist getrennt von der KI-Angabe). Gilt für alle Bollawave/Suno-Releases. Bezug: [[project-suno-distrokid-blocklist]].

⚠️ Lehre 23.06.: NICHT „Songtext = von Chris, Haken raus" sagen — „von dir/Bolla" heißt von einer KI, also Haken rein.

## ⚠️ DistroKid-KI-Dialog bei Songs mit Chris' eigener Suno-Voice (Lehre 28.06.2026)
Wenn Chris in Suno seine **eigene Stimme (Voice-Feature)** nutzt, ist der Gesang teils menschlich → NICHT „Das gesamte Audio (mittels KI erstellt)", sondern:
- ☑ **Songtext** (KI, von Bolla)
- ☑ **Musik** (KI, von Suno komponiert)
- ☐ Das gesamte Audio — AUS (Chris' echte Stimme ist drin)
- ☑ **Teile des Audios → Gesang** (KI-Arrangement + von Mensch/Chris gesungen)

Bei **reiner Suno-KI-Stimme** (ohne Chris' Voice) dagegen: „Das gesamte Audio (mittels KI erstellt)" ankreuzen. Also IMMER fragen/checken, ob Chris' Voice verwendet wurde, bevor man die Audio-Ebene deklariert. Songwriter-Feld bleibt in beiden Fällen Christoph Mandel.

## 🎼 DistroKid Credits-Schritt (Pflicht für Apple Music, Lehre 06.07.2026)
DistroKid verlangt pro Song einen Interpreten- UND Produzenten-Credit (sonst kein Apple Music). Immer gleich → gehört in JEDE bollawave-Checkliste (echte Dropdown-Rollen, verifiziert 06.07.2026):
- **Künstler*in:** Rolle **„Gesang & Vocals"** · Name **bollawave** (Künstlername)
- **Produzent*in:** Rolle **„Executive Producer"** · Name **Christoph Mandel** (echter Name = Rechte/Credits)
- ⚠️ Rollen sind feste Dropdown-Werte — NICHT erfinden („Interpret*in" existiert NICHT). Bei Unsicherheit Dropdown ansehen lassen.

## ⚠️ Automatisierte Checkliste war unvollständig (Lehre 10.07.2026)
Die von `distrokid_publish.py` (`/api/suno/publish`-Knopf) automatisch erzeugte `DistroKid-Checkliste.txt` hatte NUR Künstler/Songwriter/Titel/Genre/Sprache + einen pauschalen KI-Haken — es fehlten Explicit-Flag, die Voice-abhängige KI-Deklaration-Verzweigung, Credits/Rollen, Stores&Optionen, Anti-Spam-Hinweis und die Warnung „Apple-Songwriter-Credit MUSS während des Uploads eingetragen werden (danach gesperrt)". Ursache: Es gab parallel schon eine vollständige manuelle Vorlage (`Dokumente\Bolla\Suno_DistroKid\DistroKid_Upload_Checkliste.docx` bzw. `claud code - openclaw Doku\...`), die nie in den automatisierten Generator übernommen wurde. **Gefixt:** `write_checklist()` in `distrokid_publish.py` enthält jetzt ALLE Punkte aus der docx-Vorlage, 1:1 pro Song generiert. Bei künftigen Checklisten-Wünschen zuerst die docx-Vorlage als Quelle der Wahrheit gegenchecken, nicht nur den Python-Generator.
