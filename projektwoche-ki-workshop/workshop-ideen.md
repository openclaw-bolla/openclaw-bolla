# KI-ShortTrack für Lehrerkollegen — Ideen-Sammlung

> Zentraler Sammelplatz für Chris' Workshop in der Projektwoche am Lessing-Gymnasium.
> Chris kippt laufend Einfälle ein, Bolla sortiert sie hier ein. Aus dieser Datei heraus
> entstehen dann konkrete Anweisungen ("erzeuge Folie X", "passe Y an").
>
> **Status-Tags:** `[IDEE]` = nur notiert · `[RECHERCHE]` = muss noch belegt/geprüft werden ·
> `[IN PPT]` = als Folie umgesetzt · `[FERTIG]` = abgeschlossen

---

## 📌 Eckdaten

- **Anlass:** Projektwoche am Lessing-Gymnasium, Short-Track für Lehrerkollegen
- **Thema:** Aktuelle KI-Möglichkeiten
- **Dauer:** 90 Minuten (knapp! → Fokus, nicht Vollständigkeit)
- **Zielgruppe:** Lehrerkollegen (gemischtes Vorwissen annehmen)
- **Projektwoche:** 22.06.–26.06.2026
- **Vortrag (voraussichtlich):** **Mi 24.06.2026, 13:30 Uhr**
- **Vorlauf:** ab 20.05. noch ~5 Wochen Zeit
- **Haupt-Deliverable:** PPT `KI_fuer_Lehrer.pptx` (liegt auf `D:\OneDrive\Desktop\`, aktuell nur Titelfolie)

---

## 🗂 PPT-Status

- **Datei:** `/mnt/d/OneDrive/Desktop/KI_fuer_Lehrer.pptx`
- **Stand 20.05.:** 1 Folie — Titelfolie "KI-Unterstützung für Lehrerinnen und Lehrer"
- **Werkzeug:** python-pptx ist auf dem Studio installiert → Folien können programmatisch erzeugt/angepasst werden
- Backup vor jeder Bearbeitung empfohlen (Schwaben-sicher 😄)

---

## 🧱 Themenblöcke (inhaltlich)

### 1. Meilensteine der Informationstechnologie `[IN PPT]` ✅
**Umgesetzt am 20.05. als Folie 2** in KI_fuer_Lehrer.pptx ("④ Vom Buchdruck zur KI").
- **Zeitstrahl**: Buchdruck 1450 → Telefon → Radio → TV → Computer → Internet → WWW → Smartphone → Generative KI 2022 → Quantencomputer 2025, mit Gap-Hinweisen (426 J → 23 J → 15 J → 3 J) und Farbverlauf zu Pink
- **Adoptions-Box**: "Zeit bis 1 Mio. Nutzer" — Netflix 3,5 J · Facebook 10 Mon · Spotify 5 Mon · Instagram 2,5 Mon · ChatGPT 5 Tage (konsistente Metrik!)
- Radio-38-Jahre als Fußnote/Kontext (das ist die „bis 50 Mio."-Metrik — bewusst getrennt gehalten, Ehrlichkeit)
- Speaker Notes mit Quellen/Daten für Chris hinterlegt
- Build-Script: `projektwoche-ki-workshop/build_meilenstein_folie.py` (idempotent, baut von Titelfolien-Backup)

### 2. Urheberrecht / rechtliche Fragen `[IDEE]`
Kurzer Block, kein Vortrag — Sensibilisierung.
- Beispiel **Suno** (KI-Musik) als Aufhänger
- Fragen: Wem gehört KI-generierter Content? Trainingsdaten? Nutzung im Schulkontext?
- _Chris hat hier eigene Erfahrung mit Suno/RouteNote — authentisches Beispiel_

### 3. Modell-Überblick `[IDEE]`
Welche Arten von KI-Modellen gibt es — über Text hinaus:
- **Text** (ChatGPT, Claude, Gemini, …)
- **Bild** (neu dazu) — z.B. Pollinations, Flux, …
- **Video** (neu dazu) — z.B. Kling, Luma, Hailuo (via PiAPI)
- Idee: live-Demo oder Beispiel-Outputs zeigen

### 4. Telli — Education Schleswig-Holstein `[IDEE]`
- Hinweis auf **Telli** (KI-Angebot für Bildung in Schleswig-Holstein)
- `[RECHERCHE]` Was genau ist Telli, was kann es, wie kommen Lehrer ran?

### 5. Microsoft Copilot — Lizenzierung & Einsatz `[IDEE]` ⭐ WICHTIG
Von Chris als "ganz wichtig" markiert.
- **Lizenzierungsmodelle** (welche Copilot-Varianten gibt es? M365 Copilot, Copilot Chat, Education-Lizenzen…)
- **Einsatzmöglichkeiten** im Schul-/Lehrer-Alltag
- `[RECHERCHE]` Aktuelle Lizenz-Optionen + Education-Konditionen

---

## 🎬 Folien-Backlog (was konkret in die PPT soll)

| # | Folie | Status | Notiz |
|---|-------|--------|-------|
| 1 | Titel/Infografik | vorhanden | "KI-Unterstützung für Lehrerinnen und Lehrer" |
| 2 | Meilensteine IT (Timeline) | ✅ fertig | "④ Vom Buchdruck zur KI" — Zeitstrahl + Adoptions-Box |
| 3 | Druck-Version Folie 1 | ✅ fertig | helle Print-Version (build_print_folien.py) |
| 4 | Druck-Version Folie 2 | ✅ fertig | helle Print-Version (build_print_folien.py) |
| – | Urheberrecht (Suno) | offen | siehe Block 2 |
| – | Modell-Arten (Text/Bild/Video) | offen | siehe Block 3 |
| – | Telli SH | offen | siehe Block 4 |
| – | Copilot Lizenzen + Einsatz | offen | siehe Block 5 |

---

## 🖼 Asset-Liste (zu erzeugende Bilder/Videos)
_Noch leer — hier landen generierte Grafiken (Pollinations für Bilder = kostenlos), Demo-Outputs etc._

---

## 🔍 Offene Recherche-TODOs
- [ ] Adoption-Zahlen "bis 1 Mio. Nutzer" für mehrere Technologien sauber belegen
- [ ] Telli (Education SH): Funktionsumfang + Zugang für Lehrer
- [ ] Copilot: aktuelle Lizenzmodelle + Education-Konditionen (Stand 2026)
- [x] ~~Projektwoche-Datum~~ → 22.–26.06.2026, Vortrag vrstl. 24.06. 13:30

---

## 📥 Inbox (Roh-Einwürfe, noch nicht einsortiert)
_Hier kommt rein was Chris schnell reinwirft und ich noch nicht zugeordnet habe._

---

## 📝 Änderungs-Log
- **2026-05-20:** Sammlung angelegt. Erste Inputs von Chris: PPT-Überarbeitung, Meilenstein-Folie, Urheberrecht/Suno, Bild+Video-Modelle, Telli SH, Copilot-Lizenzen.
