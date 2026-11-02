---
name: project-itslearning-automation
description: "itslearning-Automatisierung (SH-Schulportal-SSO) — Zugangsdaten-Ort, geplanter Workflow für Kurs-Mitteilungen mit Anhängen"
metadata: 
  node_type: memory
  type: project
  originSessionId: dc5bcfc1-3712-4d32-a1d2-fbbb2cf1205b
  modified: 2026-09-28T14:23:11.313Z
---

Chris möchte, dass ich in itslearning-Kursen (Lessing-Gymnasium) automatisiert Mitteilungen mit angehängten
Ressourcen einstelle — typischer Auftrag: "erstelle eine HTML-Praktikumsdatei und lade sie mit einem netten
Text als Mitteilung in Kurs 1, 2, ... hoch". Erteilt werden solche Aufträge künftig auch über die
mp-Seite "Schuljahr 26/27" (vgl. [[feature_schuljahr_modul_auftrag]] für den bestehenden Auftrags-Mechanismus
dort — ob itslearning-Postings über denselben Watcher laufen oder eigenständig, ist noch offen).

**⚠️ Dauerregel (explizit gemacht 23.07.2026 nachts):** Jede technische Erkenntnis über itslearnings DOM/UI
(Selektoren, Fallstricke, Klickpfade) grundsätzlich sofort HIER dokumentieren, nicht nur bei expliziter
Nachfrage. itslearning ist notorisch fummelig (unsichtbare Duplikat-Elemente, Case-Sensitivity-Fallen,
mehrdeutige Buttons) — jede neu gefundene Falle spart beim naechsten Mal Zeit, jede nicht dokumentierte
kostet sie erneut.

**Login-Mechanismus:** itslearning in Schleswig-Holstein läuft NICHT über direktes itslearning-Passwort,
sondern über **Schulportal-SH SSO**. Benutzername: `cmandel`.

**Zugangsdaten-Ablage:** Passwort liegt NICHT hier in der Memory (git-getrackt, PFLICHT laut globaler
Regel), sondern sicher in `/home/bolla/workspace/config/itslearning_credentials.json` (chmod 600). Chris hat
das Passwort am 18.07.2026 im Chat genannt und darum gebeten, es sich zu merken, damit er künftig nur noch
eine Kurzform nennen muss (z.B. Anfang+Ende) und ich es aus der gesicherten Datei erkenne/nutze.

**Stand 18.07.2026 — Login+Workflow erfolgreich getestet (rein lesend, nichts veröffentlicht):**

- Login-Flow funktioniert vollautomatisch per Playwright: `portal.schule-sh.de` → Klick "Anmelden" →
  Keycloak-SSO (`login.schule-sh.de/realms/SPSH/...`) → Username/Passwort ausfüllen → landet auf
  `portal.schule-sh.de/start`. Von dort itslearning-Kachel klicken (öffnet neuen Tab/Page im selben
  Playwright-Context, `context.expect_page()` abfangen) → SSO reicht automatisch durch bis
  `moin.itslearning.com/CourseCards` (Kursliste), kein zweiter Login nötig.
- Kurse sichtbar (Schuljahr 26/27, passend zu [[project_schuljahr2627]]): Computer Basics 7a I/II, 7b I/II,
  7c I/II, 7d I/II, plus Absentismus und Unterstützungskurs. Kurs-URL-Muster:
  `moin.itslearning.com/Course/Course.aspx?CourseId=<ID>` (7a I = 190735).
  Ressourcen-Tab: `moin.itslearning.com/Resources?FolderID=<ID>` (7a I Ressourcen-Ordner = 9233802).
- Auf der Kurs-"Übersicht" gibt es den Mitteilungs-Kasten: Rich-Text-Editor, darunter Links "📄 Ressource"
  (Datei anhängen) und "🖼 Bild", Button "Optionen ▾" und grüner Button "Veröffentlichen". Das ist der
  komplette Ziel-Workflow: Text schreiben → Ressource anhängen → Veröffentlichen.
- ⚠️ **Vorsicht bei `text=Ressource`-Selektor:** Playwright matched damit sowohl den Anhänge-Link IN der
  Mitteilungsbox als auch den Kurs-Nav-Tab "Ressourcen" (Substring-Match) — je nach DOM-Reihenfolge klickt
  man den falschen. Beim echten Bauen des Post-Skripts einen präziseren Selector verwenden (z.B. Scope auf
  die Mitteilungsbox eingrenzen), sonst landet man nur auf der Ressourcen-Übersichtsseite des Kurses statt
  den Anhang-Dialog in der Mitteilung zu öffnen.
- Baseline zur Erkennung ungewollter Änderungen: Kurs "7a I" hatte am 18.07.2026 **14 Ressourcen**, alle
  datiert 07.07. oder 09.07.2026 (u.a. Ordner "Downloads", diverse .pptx/.docx/.mp3/.mp4 von Chris selbst
  hochgeladen). Ein kurz aufblitzendes "Upload-Status"-Banner beim Navigieren stellte sich als alter Toast
  aus Chris' eigener früherer Session heraus (kein neuer Eintrag, Ressourcen-Zahl blieb bei 14) — mein
  Test-Skript hat nie `set_input_files`/einen echten Upload ausgelöst, nur Navigation/Klicks.
- Test-Skripte liegen unter `/home/bolla/workspace/scripts/itslearning_login_test.py` (Login-Basis),
  `..._test2.py` (bis Kursliste), `..._test3.py` (Kurs öffnen + Nav auslesen), `..._test4.py` (Ressourcen-Tab
  ansehen). Wiederverwendbare Basis für das eigentliche Post-Skript.

**Vorgehen bei jedem konkreten Auftrag:** siehe [[feedback_website_schreibzugriff]] — Content bauen, einloggen,
alles vorbereiten, aber NIE ohne Chris' explizite Freigabe tatsächlich posten/hochladen.

## Ziel-Workflow: Mitteilung an alle 4 Kurse gemeinsam (Chris, 22.07.2026, präzisiert 22.07.2026 abends)

**⚠️ Wichtig, unbedingt merken:** Es gibt in itslearning **8 Kurse** (7a I, 7a II, 7b I, 7b II, 7c I, 7c II,
7d I, 7d II) — je Klasse zwei Gruppen, die im **4-Wochen-Rhythmus** abwechseln (siehe
[[project_schuljahr2627]], "I/II-Rhythmus ist REAL"). In einer gegebenen Woche hat aber immer nur **eine**
der beiden Gruppen pro Klasse EDV. "Alle 4 Kurse gleichzeitig beglücken" bedeutet also: **die 4 Kurse der
gerade aktiven Gruppe** (z.B. in der Woche 19./20.08.2026 alle vier „I"-Kurse: 7a I, 7b I, 7c I, 7d I — NICHT
alle 8, NICHT die „II"-Kurse). Welche Gruppe in welcher Woche aktiv ist, ergibt sich aus den `termine[]` in
`data/schuljahr2627.json`. Von der mp-Seite "Schuljahr 26/27" soll EIN Anstoß die Mitteilung **gleichzeitig an
diese 4 passenden Kurse** auslösen — nicht einzeln nacheinander beauftragt, und nicht an die falsche
Gruppen-Hälfte. Angehängt wird jeweils die **Ressource, die die Schüler für den Tag brauchen** (das PDF
und/oder die Praktikum-HTML aus dem `Handouts`-Ordner, siehe [[project_schuljahr2627]] für den
Datei-Workflow pro Kurstag) — für alle 4 Kurse identisch (gleicher Kurstag/gleiches Thema), nur der
Mitteilungstext wird pro Kurs neu formuliert (s.u.).

**Textvorgaben für jede Mitteilung (gilt dauerhaft, nicht nur einmalig):**
- **Immer neu formulieren**, nicht denselben Text an alle 4 Kurse oder über mehrere Tage hinweg kopieren —
  passt zu [[feedback_ki_texte_natuerlich]] (keine gleichen Einstiege).
- Netter, warmer Ton (Zielgruppe 7. Klasse, vgl. [[feedback_schueler_texte_ton]]).
- **⚠️ Download passiert AM Kurstag selbst, nicht vorher (Chris-Korrektur 22.07.2026 Nacht):** Die Schüler
  laden sich die Dateien erst **während/zu Beginn der jeweiligen Unterrichtsstunde** herunter, nicht schon
  Tage vorher auf eigene Initiative. Der erste Testtext hatte faelschlich "ladet euch das VORHER auf den
  Stick" formuliert — das war inhaltlich falsch und wurde deshalb komplett zurueckgezogen (Mitteilungen +
  Ressourcen aus allen 4 Kursen geloescht). **Nie wieder "vorher/schon jetzt herunterladen" formulieren** —
  entweder zeitlich neutral halten ("Hier sind die Materialien für unsere Stunde am TT.MM.") oder explizit
  auf den Stundenbeginn beziehen ("In der Stunde laden wir das gemeinsam herunter").
- **Download-Ablauf erklären? Nur am ALLERERSTEN itslearning-Kurstag sinnvoll.** Chris hat sich gefragt, ob
  die Schüler den Download-Vorgang selbst (itslearning-Datei anklicken → Herunterladen → auf den Stick
  ziehen) ueberhaupt schon kennen. Bolla-Einschaetzung: Bei ca. 60% wenig PC-Vorerfahrung
  ([[project_schuljahr2627]]) macht eine **kurze** Download-Anleitung nur beim ersten Mal Sinn (evtl. sogar
  eher als Live-Demo am Beamer statt als Text in der Mitteilung, da Tag 1 laut [[project_schuljahr2627]]
  ohnehin viele Vorbesprechungen enthaelt) — nicht bei jedem weiteren Kurstag wiederholen, sobald es einmal
  klar ist. Noch nicht final entschieden, wie genau (Text vs. Demo) — beim naechsten Anlauf mit Chris klaeren.
- **Immer mit Emojis** — Chris' explizite, dauerhafte Vorgabe ("ich liebe Emojis"), gilt für JEDE
  Schüler-Mitteilung in itslearning, nicht nur diese.

## ⏪ Rollback 22.07.2026 Nacht — Kurstag-0/1-Testlauf komplett zurückgezogen

Nach den beiden obigen Korrekturen (Text-Timing falsch, PDF-Qualitaet schlecht) hat Chris angeordnet, alles
rueckgaengig zu machen fuer einen sauberen Retest an einem anderen Tag: **alle 4 Mitteilungen geloescht**
(Options-Menue → "Löschen" → Bestaetigungsdialog "Mitteilung löschen?") UND **beide Ressourcen (PDF+HTML) aus
allen 4 Kursen geloescht** (Ressourcen-Seite → Checkbox anhaken → Bulk-Aktion "Löschen" unten → Bestaetigen).
Danach verifiziert: 7a I wieder bei den urspruenglichen 14 Ressourcen, keine Reste. Lokale PDF-Datei ebenfalls
geloescht (HTML-Datei blieb, war inhaltlich in Ordnung). **Notfall-Loesch-Skripte dauerhaft abgelegt** (fuer
den Fall, dass sowas nochmal gebraucht wird):
`/home/bolla/workspace/scripts/itslearning_delete_latest_message.py` (loescht die neueste Mitteilung je
Kurs) und `..._delete_resources.py` (loescht Ressourcen per Basisname-Liste) — vor Gebrauch jeweils
`COURSES`/`BASENAMES` oben im Skript anpassen.

**Loesch-Mechanik (DOM-Fallstricke, analog zu den Upload-Fallstricken oben):**
- Mitteilungs-Optionen-Button: `button.itsl-announcement-drop-down-menu__button` (aria-label "Optionen"),
  liegt rechts neben Autor/Zeitstempel der jeweiligen Mitteilung — bei der aktuellsten Mitteilung ist das
  `.first`, da neueste zuerst sortiert ist.
- Bestaetigungsdialog-Button ist NICHT simple per Text zu finden (mehrere unsichtbare "Löschen"-Reste im
  DOM von der geschlossenen Dropdown) — exakter Pfad: `div.prom-modal2__footer button.prom-button__destructive`.
- Ressourcen-Bulk-Loeschen: Checkbox(en) anhaken → am unteren Bildschirmrand erscheint eine Aktionsleiste mit
  Icon+Text "Löschen" — auch hier gibt es unsichtbare Text-Duplikate im DOM, daher ueber
  `get_by_role("button", name="Löschen", exact=True)` gehen und den ERSTEN **sichtbaren** Treffer nehmen
  (`is_visible()`-Check in einer Schleife), nicht blind `.first`.
- Danach wieder derselbe `div.prom-modal2__footer button.prom-button__destructive`-Bestaetigungsdialog.

## ✅ Kurstag 0/1 live durchgezogen (22.07.2026 abends) — Post-Skript funktioniert, DOM-Fallstricke dokumentiert

Erster echter Produktiv-Einsatz: PDF + `01-Praktikum.html` in alle 4 „I"-Kurse (7a/7b/7c/7d I) hochgeladen
und mit individuellem Mitteilungstext veröffentlicht. Lief unter dem MP-Anstups-Kanal, daher ohne
Vorab-Freigabe (siehe Ausnahme in [[feedback_website_schreibzugriff]]). Alle 4 im Nachhinein per Screenshot
verifiziert — Text + beide Anhänge korrekt, keine Duplikate.

**✅ Generalisiertes, dauerhaftes Skript (Stand 22.07.2026 Nacht, nach Rollback + Korrekturen überarbeitet):**
`/home/bolla/workspace/scripts/itslearning_post_kurstag.py` (Nachfolger von `..._post_kurstag01.py`, das
geloescht wurde). Vor jedem Lauf am Skriptkopf anpassen: `DAY_PREFIX` (zweistellige Tagesnummer) + die 4
`COURSES`-Einträge (Kurs-ID bleibt stabil, Text jedes Mal neu formulieren). Sammelt das **Standard-Paket
automatisch selbst** (`discover_files()`: PDF + alle HTML-Dateien mit `DAY_PREFIX-`-Präfix aus dem
Handouts-Ordner) — kein Nachdenken mehr nötig, welche Dateien dazugehören. Enthält bereits **beide
Korrekturen** aus dem Rollback (keine "vorher herunterladen"-Formulierung mehr in den Beispieltexten, sowie
alle unten dokumentierten DOM-Fallstricke).

**Datei-Upload-Flow (Ressourcen-Seite, mehrstufig verschachtelt):**
1. Kurs-Home öffnen (`main.aspx?CourseID=<ID>`) → Tab "Ressourcen" klicken (landet auf
   `Resources?FolderID=<ID>` — FolderID ist pro Kurs unterschiedlich, nicht raten, immer über den Tab-Klick
   navigieren).
2. "Hinzufügen" → "Datei oder Ordner" klicken → oeffnet eine ASP.NET-Altlast-Seite
   (`ContentArea.aspx` mit verschachteltem iframe `AddLearningToolElement.aspx`) mit einer Drop-Zone.
3. Die Drop-Zone selbst hat **kein** `<input type=file>` im DOM (auch nicht im Shadow-DOM) — Klick auf
   `button.ccl-uc-dropzone-container` (im inneren Frame) öffnet erst ein Popover "Laden Sie eine Kopie hoch
   von" mit den Optionen "Ihr Computer – Datei" / "Ihr Computer – Ordner" / "Meine Dateien". **Erst der Klick
   auf "Ihr Computer – Datei" triggert den echten `filechooser`-Event** (mit `expect_file_chooser` abfangen,
   `set_files([...])` akzeptiert eine Liste = Mehrfach-Upload in einem Schritt).
4. Nach dem Upload zeigt die Dateiliste Name+Erweiterung in **zwei separaten `<span>`-Elementen** mit
   Whitespace dazwischen im DOM — ein Locator auf den vollen Dateinamen inkl. Erweiterung (`"Name.pdf"`)
   matcht NIE. Immer nur auf den **Basisnamen ohne Erweiterung** suchen.
5. Grüner "Speichern"-Button liegt im selben inneren Frame — über alle `its.frames` suchen (nicht auf
   `frames[-1]` verlassen, der Frame-Index kann nach dem Upload verrutschen).
6. **Idempotenz:** Vor dem Upload immer erst auf der Ressourcen-Seite pruefen, ob Basisname(n) schon
   existieren (Kurs hat die Dateien dann schon) — sonst bei einem Retry Duplikate anlegen.

## 📎 Anstups-Syntax für Anhänge (Chris, 22.07.2026 Nacht) — wichtig fuer alle kuenftigen Kurstage

Chris hatte am ersten Live-Tag vergessen, dass zu Kurstag 1 auch `01-Editor-Anleitung.html` gehoert (zusaetzlich
zu PDF + Praktikum-HTML) — nicht nachgeholt (Kurs 1 ist erledigt), aber Konvention fuer die Zukunft geklaert:

- **Standard-Paket (keine Zusatzangabe im Anstups-Text noetig):** PDF **plus alle HTML-Dateien** mit der
  gleichen Tages-Nummer aus dem Handouts-Ordner — haette `01-Editor-Anleitung.html` automatisch mitgenommen,
  weil sie schon dem `NN-...`-Namensschema folgt. **Bereits umgesetzt** in
  `/home/bolla/workspace/scripts/itslearning_post_kurstag.py` (`discover_files()`), kein manuelles Nachdenken
  mehr nötig.
- **Zusatzdateien ausserhalb des Namensschemas** (ein Song, ein Video, eine zusaetzliche PPTX zum direkten
  Verteilen statt nur PDF) benennt Chris einfach im Anstups-Freitext, z.B. `"itslearning + Sommer-Song.mp3"`
  oder `"itslearning + 4 Schritte.pptx"` — Dateiname muss nicht exakt/mit Endung sein, fuzzy im Handouts-Ordner
  suchen und zusaetzlich zum Standard-Paket anhaengen. Falls NICHT das Standard-Paket + Zusatz gemeint ist,
  sondern ein Ersatz (z.B. NUR der Song), sagt Chris das explizit dazu ("nur Song") — Default-Annahme ist
  immer additiv (Standard-Paket + Ergaenzung), nicht ersetzend.

## 🗂️ Ressourcen-Reorganisation "Downloads-Plan" — alle 8 Kurse aufgeräumt (22.07.2026, spät nachts)

Chris' Auftrag ("ohne Rückfragen, habe fertig"): die unübersichtliche lose Dateisammlung in den Ressourcen
jedes Kurses in den vorhandenen `Downloads`-Ressourcenordner verschieben, diesen Ordner mit dem
vorhandenen Plan-Thema "Downloads" verknüpfen (Schüler sollen ALLE Materialien über EINEN Plan-Zugang
erreichen), Recap-Dateien unsichtbar lassen/machen — Muster an 7a I entwickelt, dann auf die übrigen 7 Kurse
(7a II, 7b I/II, 7c I/II, 7d I/II) übertragen. **Ergebnis: alle 8 Kurse erfolgreich fertig**, verifiziert per
Screenshot — jeder "Downloads"-Plan zeigt jetzt nur noch den Downloads-Ordner als einzigen Eintrag unter
"Ressourcen und Aktivitäten", jeweils mit dem korrekten kurseigenen Bild (7A I/II, 7B I/II, 7C I/II, 7D I/II —
waren von Chris schon vorher individuell pro Kurs gesetzt, nicht von mir kopiert).

**⚠️ Überraschender Fund: 7c I und 7c II waren mit "Sichtbar für Schüler*innen" = AUS.** Alle anderen 6 Kurse
hatten das an. Da nur genau diese zwei (die ganze "c"-Klasse, beide Gruppen) betroffen waren und sonst nichts
an meinem Skript-Ablauf dort abwich, ist das mit hoher Wahrscheinlichkeit **voreingestellter Altzustand**
gewesen (nicht von mir versehentlich umgeschaltet) — nach bestem Wissen korrekt eingeordnet, aber nicht 100%
sicher beweisbar. Habe es auf AN gestellt (passend zu den anderen 6 Kursen). **Chris sollte das kurz
gegenchecken**, falls 7c aus einem ihm bekannten Grund bewusst unsichtbar war.

**Workflow pro Kurs (bewaehrtes Muster fuer kuenftige Aehnliches):**
1. Ressourcen-Seite: "Alle sichtbaren auswählen" → Downloads-Ordner-Checkbox wieder abwaehlen → Bulk-Aktion
   "Verschieben nach" → im Zielbaum den Downloads-Ordner anklicken → "Verschieben".
2. Falls vorhanden: Recap-Dateien (Titel enthaelt "Recap") in der Downloads-Ordner-Ansicht per Checkbox +
   Bulk-Aktion "Ausblenden" auf "Nicht sichtbar" setzen.
3. Plan verknuepfen: Kurs-Uebersicht → Tab "Pläne" → **explizit Untertab "Thema" anklicken** (Default ist
   "Aktuell", zeigt sonst "Keine Pläne") → Kategorie "Downloads" anklicken → landet auf einer
   Themen-Uebersichtsseite mit genau einer Topic-Karte (Titel kann "Kein Titel" sein, falls Chris den nie
   ausgefuellt hat) → **auf die Checkbox-Zeile klicken (Checkbox-Bounding-Box + Offset ~300px nach rechts),
   NICHT auf den Titel-Text** (bricht bei leerem Titel), landet im eigentlichen Plan-Editor
   (`/plans/courses/<ID>/plan/<PlanID>?...`).
4. Im Plan-Editor: **es gibt oft ZWEI "Hinzufügen"-Links** — einen für die Sektion "ANFORDERUNGEN" (oben) und
   einen fuer "RESSOURCEN UND AKTIVITÄTEN" (unten, nach der bestehenden Liste). Den **letzten** `Hinzufügen`
   nehmen (`get_by_text("Hinzufügen", exact=True).last`), sonst oeffnet sich faelschlich der
   "Anforderung"-Hinzufuegen-Dialog (Checkbox "ANFORDERUNG" + "Erstellte Anforderungen" statt einer
   Dateiliste). Dann "Kurs" anklicken → im Ressourcen-Baum den Downloads-Ordner-Checkbox anhaken → Speichern.
5. Alte Einzel-Eintraege entfernen: **korrekter Selektor ist `li.its-plans-resource__block`** (NICHT
   `[draggable='true']` — das matcht hier gar nichts, fuehrte zu falschem "0 entfernt"-Erfolg ohne echte
   Wirkung). Pro Zeile: Chevron rechts anklicken (`mouse.click(1307, row_y)`) → "Aus diesem Plan entfernen".
   In einer Schleife wiederholen bis nur noch "Downloads" uebrig ist.

**Fertige Wegwerf-Skripte lagen im its2-Scratchpad dieser Session** (nicht dauerhaft uebernommen, da
Ein-Mal-Aktion): `reorganize_course.py` → `link_plans_fixed.py` → `link_plans_final.py` →
`final_cleanup2.py` (letzte, korrekte Version). Bei einer Wiederholung (z.B. neue Kurse naechstes Schuljahr)
das Muster aus dieser Notiz rekonstruieren, nicht die alten Skript-Versionen 1:1 kopieren — die ersten drei
hatten die oben beschriebenen Bugs.

## ⚠️ KORREKTUR 23.07.2026 nachts: Chris wollte doch KEINEN Downloads-Ordner, nur die flache Liste

Der obige "Downloads-Ordner+Plan-Verknuepfung"-Ansatz war fuer 7a I **nicht das Endziel** — Chris hat sich
das Ergebnis angesehen und wollte stattdessen: **alle Ressourcen des Kurses einzeln im Plan** (kein
buendelnder Ordner mehr), und explizit **keinen Ordner namens "Downloads"** (Namenskonflikt mit dem
Plan-Namen). Fuer **7a I** wurde das nachtraeglich korrekt umgesetzt:
- Der `Downloads`-Ordner wurde geleert (Inhalt zurueck auf Ressourcen-Top-Level verschoben) und dann
  umbenannt zu **"Archiv"** + auf "Nicht sichtbar" gestellt (leerer Rest, dient nur noch der
  Themen-Altlast unten).
- Alle 13 aktiven Ressourcen (3 Recap + 10 Dateien/Ordner, inkl. eines von Chris manuell angelegten
  `Sound`-Unterordners) stehen jetzt **einzeln** in "Ressourcen und Aktivitäten" des Plans.
- Der Plan hat **kein Thema-Tag mehr** ("Downloads" oder sonst was) — Chris braucht das nicht, extra
  Rueckfrage bestaetigt: er will nur die flache Ressourcenliste, das Thema-Tag ist irrelevant.

**🔑 Wichtigste technische Erkenntnis (von Chris selbst verifiziert):** Ein **Thema (Topic-Tag) im Planer
zu erstellen/verbinden erzeugt automatisch einen gleichnamigen Ordner in den Ressourcen** — das ist keine
Bastelloesung von mir, sondern itslearnings eingebautes Verhalten (bestaetigt durch den Dialog "Ressourcen
verschieben? ... werden ... nach Downloads verschoben" beim Neuanlegen eines Themas "Downloads"). Umgekehrt:
ein Ordner, der mit einem Thema verbunden ist, **laesst sich nicht direkt loeschen** (UI blockiert das mit
der Meldung "Ordner, die im Planer mit einem Thema verbunden sind, können nicht gelöscht ... werden").

**✅ Der eigentliche, saubere Loeschweg (von Chris selbst gefunden, 23.07.2026 nachts):** Nicht den Ordner
einzeln umbenennen/verstecken versuchen (mein Workaround, unnoetig kompliziert) — stattdessen **das ganze
Plan/Thema-Element selbst loeschen** (in der Pläne-Uebersicht das jeweilige Thema/den Plan-Eintrag per
Kontextmenue entfernen). Das loescht automatisch/kaskadierend auch den verknuepften Ressourcen-Ordner mit,
OHNE Umbenennen-Umweg. So wurden die liegengebliebenen leeren "Downloads"- und "Archiv"-Ordner in 7a I
restlos entfernt (Endzustand verifiziert: genau 13 Ressourcen, keine Reste, Haupt-Plan mit allen 13 Eintraegen
intakt und ohne Thema-Tag — Chris braucht kein Thema, das ist bewusst so gewollt).
**Konsequenz fuer die Zukunft:** Wenn ein ungewollter Thema-verknuepfter Ordner entstanden ist: NICHT
umbenennen/verstecken, sondern das zugehoerige Plan/Thema-Element in der Pläne-Uebersicht direkt loeschen —
das ist der korrekte, vollstaendige Weg (raeumt Ordner UND Thema-Eintrag in einem Schritt weg).

**⚠️ Offener Punkt:** Die anderen 7 Kurse (7a II, 7b I/II, 7c I/II, 7d I/II) haben noch den AELTEREN Stand
(ein Downloads-Ordner als gebuendelter Plan-Eintrag, siehe Abschnitt oben) — NICHT die flache Einzel-Liste
wie jetzt bei 7a I. Ob Chris das auch auf die anderen 7 uebertragen haben moechte, ist noch nicht gesagt/
geklaert — vor einer Wiederholung des Musters auf die anderen Kurse explizit nachfragen, nicht automatisch
annehmen dass es gewuenscht ist.

## 📁 "Bibliothek" = persönliche Dateiablage am Account (28.09.2026, Recherche für Handy→PC-Dateitransfer)

Chris suchte einen Weg, wie Schüler Dateien vom Handy auf den Schul-PC bekommen (Alternative zu Stick+OTG).
Live getestet (Browser, Lehrer-Account cmandel):
- **Selbst-Nachricht funktioniert NICHT:** In der privaten Nachrichten-Personensuche (gleiches Feature wie
  bei `itslearning_send_private_song.py`) taucht der eigene Name nicht als Treffer auf — man kann sich nicht
  selbst als Empfänger waehlen.
- **Aber: Top-Nav-Punkt "Bibliothek"** (neben Kurse/Updates/Gruppen/Kalender/Links) ist eine **persoenliche,
  account-gebundene Dateiablage**, URL bestaetigt es: `.../IntermediatePage.aspx?PageToRedirect=MyLibrary&
  Item=l-menu-mylibrary`. Nicht kursgebunden, sondern am eigenen Login haengend — genau das, was fuer
  Handy-Upload → PC-Download gebraucht wird (Handy-App hochladen, am PC im Browser wieder abrufen).
- **Offen/nicht getestet:** Ob der Upload-Weg in der itslearning-**Mobile-App** genauso einfach zur Bibliothek
  fuehrt (z.B. direkt ein Foto aus der Galerie hochladen) — nur der Browser-Zugriffspunkt wurde verifiziert.
  Vor Einsatz im Praktikum einmal selbst am Handy durchklicken.

**✅ App-Login-Falle geloest (28.09.2026, Chris live getestet auf P8 + Duo):** Die itslearning-Mobile-App
fragt beim ersten Start nach der Schule/Institution ("Site suchen"). **Den Schulnamen selbst
("Lessing Gymnasium" o.ae.) NICHT eingeben — wird nicht gefunden!** SH-Schulen haengen alle an EINEM
gemeinsamen Schulportal-SH-Tenant (wie im Browser: `portal.schule-sh.de`-SSO). **Richtiger Suchbegriff:
"Schleswig-Holstein"** — danach kommt der normale Schulportal-SH-Login (User+Passwort). Bestaetigt
funktionierend auf dem Pixel 8 (Codename `shiba`, Chat-Alias „p8"); danach auch am Surface Duo 2 erfolgreich
nachgezogen (vorher generischer Fehler "Zur Zeit gibt es Probleme" — war derselbe falsche Site-Sucheintrag).

## Mitteilungs-Box (Ressource anhängen + veröffentlichen):
- Compose-Box eindeutig scopen über `li.itsl-light-bulletins-new-item-listitem` (der reine Text "Ressource"
  matcht sonst auch den Kurs-Nav-Tab, s.o.).
- Editor ist `[contenteditable='true']` (Klasse `prom-srtf-container`) — normales `.fill(text)` reicht,
  kein Tippen pro Zeichen nötig (Emojis funktionieren darin problemlos).
- Klick auf "Ressource" in der Box öffnet einen Dialog "Link zu Ressource hinzufügen" mit Checkboxen für
  alle Kurs-Ressourcen (nicht kursübergreifend, nur die des aktuellen Kurses). Checkbox-Klick per
  `element.evaluate("el => el.click()")` (nativer JS-Klick) statt Playwright-`.click()` — Playwright meldet
  faelschlich "outside of viewport" wegen des verschachtelten Modal-Scroll-Containers.
- **Falle:** Der Bestaetigungs-Button im Dialog heisst zwar "Hinzufügen", ist aber ein
  `<input value="Hinzufügen">`, kein `<button>` — UND es gibt eine gleichnamige, unsichtbare Ueberschrift
  "Hinzufügen" anderswo im DOM, die ein simpler `text=Hinzufügen`-Locator faelschlich zuerst trifft (Dialog
  bleibt dann zu, kein Fehler, einfach nichts passiert). Immer gezielt `input[value='Hinzufügen']` matchen.
- "Veröffentlichen"-Button danach normal per Text klickbar (kein Frame-/Shadow-Problem an dieser Stelle).

## ✅ 23.07.2026 (Vormittag/Mittag): 7a II, 7b I, 7b II auf flachen Zustand umgestellt (Nachfolgeauftrag zu 7a I)

Chris' Auftrag: die restlichen Kurse der aktiven "I"/"II"-Rotation genauso wie 7a I auf den flachen
Ressourcen-Zustand umstellen. Wichtige Praezisierung waehrend der Umsetzung: Der Endzustand muss
**strukturell 1:1 identisch zu 7a I** sein — gleiche Reihenfolge der Ressourcen im Plan UND gleiche
Sichtbarkeit jeder einzelnen Ressource, nicht nur grob "aufgeraeumt".

**Ergebnis:**
- **7a II war schon fast fertig** (kein Downloads-Ordner mehr, 9 der 13 Ressourcen schon im Plan) —
  aber in FALSCHER Reihenfolge, OHNE die 3 Recap-Dateien + den Sound-Ordner im Plan, UND die 3 Recap-
  Dateien standen faelschlich auf "Sichtbar" statt "Nicht sichtbar". Alles korrigiert, jetzt 1:1 wie 7a I
  (13 Eintraege in identischer Reihenfolge, Recaps korrekt ausgeblendet).
- **7b I und 7b II hingen noch am alten gebuendelten Downloads-Ordner** (14 bzw. 13 Dateien drin). Beide
  komplett umgestellt: Ordner geleert, Thema geloescht, Plan neu in 7a-I-Kernreihenfolge aufgebaut
  (Curriculum, Agenda, 1-Begruessung, 4 Schritte, 0-Halloween, St. Nicholas [pptx+mp4], Fun I/II, Memory),
  kursspezifische Extras ohne 7a-I-Entsprechung ans Ende angehaengt.
- **7b I hat KEIN Sound/keine Recap-Dateien** (existieren dort schlicht noch nicht, nur bei den "a"-Kursen
  angelegt) — daher bei 7b I/II kein 1:1-Vollabgleich moeglich, nur die vorhandene Schnittmenge sortiert.
- **7b I hat ein glasklares Duplikat: zwei Dateien namens "4 Schritte.pptx"** (eine vom 07.07., eine vom
  22.07.2026) — NICHT eigenmaechtig geloescht (Ressourcen-Loeschung ist Content-Entscheidung, nicht Teil
  des Struktur-Umbaus), beide direkt hintereinander im Plan belassen. **Chris sollte das pruefen und die
  veraltete Version selbst entfernen.**
- **7b II hatte 3 Dateien faelschlich auf "Nicht sichtbar"** (Curriculum, Agenda, 1-Begruessung — bei allen
  anderen Kursen sind genau diese sichtbar) — korrigiert auf "Sichtbar" zwecks 1:1-Abgleich mit 7a I.

**🔑 Neue technische Erkenntnisse (wichtig fuers naechste Mal, v.a. fuer die noch offenen 7c I/II, 7d I/II):**

1. **Thema von einem Plan loesen geht OHNE den Plan/Thema-Umweg aus der 7a-I-Nacht-Session:** Im
   Plan-Editor steht unter "THEMA" ein Chip mit Themen-Namen + einem kleinen **"X"-Button direkt daneben**
   (Klick per Koordinaten: `mouse.click(chip_box.x + chip_box.width + 15, chip_box.y + chip_box.height/2)`,
   da der Chip textuell sehr schmal/kompakt ist). Das loest die Thema-Verknuepfung sofort vom Plan (Chip
   verschwindet, "Thema erstellen"/"Thema hinzufügen" erscheint wieder) — **spart den kompletten
   Kontextmenue-Umweg** aus der 7a-I-Doku oben.
2. **ABER: das loescht das Thema-Objekt selbst noch NICHT**, nur die Verknuepfung zum Plan. Der zugehoerige
   Ressourcen-Ordner bleibt bestehen und laesst sich weiterhin NICHT direkt loeschen (Fehlermeldung: "Ordner,
   die im Planer mit einem Thema verbunden sind, können nicht gelöscht ... werden" — das Thema existiert
   als eigenstaendiges Objekt weiter, auch wenn kein Plan mehr draufzeigt). Um es endgueltig loszuwerden:
   Pläne-Übersicht → Tab **"Thema (n)"** → dort erscheint das Thema jetzt als Karte mit **"Keine Pläne"** →
   Checkbox anhaken (`input[type=checkbox]` ist meist unsichtbar/0px, `.evaluate("el => el.click()")`
   nutzen statt normalem Playwright-Klick) → **"Aktionen"-Dropdown-Button (NICHT die "..." oben rechts)** →
   "Löschen" → Bestaetigungsdialog `div.prom-modal2__footer button.prom-button__destructive`. Danach ist
   sowohl Thema als auch der verknuepfte Ordner weg. Erst NACH diesem Schritt laesst sich der (jetzt schon
   vorher aus dem Plan entfernte) leere "Downloads"-Eintrag in den Ressourcen normal per Checkbox+"Löschen"
   entfernen.
3. **Pläne-Tab-Struktur ist nicht bei jedem Kurs gleich:** 7a I/7a II hatten "Aktuell/Vergangen/Ohne
   Datum/Thema" grob wie erwartet, aber 7b I/7b II zeigen die Tabs **"Aktuell (0) / Vergangen (0) / Ohne
   Datum (1) / Thema (1)"** — der Haupt-Plan mit den Ressourcen liegt unter **"Ohne Datum"**, nicht unter
   "Alle Pläne". Vor dem Plan-Oeffnen immer den Tab pruefen statt "Alle Pläne" blind anzunehmen.
4. **Bulk-Aktionen "Ausblenden"/"Sichtbar machen" in der Ressourcen-Liste zeigen IMMER einen
   Bestaetigungsdialog** ("Bitte bestätigen — Sind Sie sicher, dass Sie die ausgewählten Elemente
   deaktivieren/aktivieren möchten?" mit Ja/Nein) — nicht vergessen, den Dialog abzuschliessen
   (`div.prom-modal2__footer button.prom-button__primary` fuer "Ja"), sonst bleibt die Aenderung aus,
   obwohl der urspruengliche Klick fehlerfrei durchlief.
5. **⚠️ Grosse DOM-Falle im "Ressource hinzufügen"-Dialog (Plan-Editor → Hinzufügen → Kurs):** Der Dialog
   zeigt eine feste Baumliste aller Kurs-Ressourcen mit Checkboxen. Bei Text-basierter Suche
   (`get_by_text(name)`) gibt es haeufig **einen zusaetzlichen unsichtbaren Treffer** irgendwo im DOM
   (analog zur "Hinzufügen"-Ueberschrift-Falle von 22.07.). Nimmt man davon `.first`, landet
   `xpath=preceding::input[@type=checkbox][1]` bei der FALSCHEN Checkbox (z.B. bei der
   "Sichtbar für Schüler*innen"-Toggle-Checkbox der Plan-Sichtbarkeit, die zufaellig davor im DOM liegt) —
   das fuehrt zu stillen Fehlschlaegen (Speichern hat keinen Effekt) oder sogar zum ungewollten Schliessen
   des Dialogs. **Sicherer Weg:** Dialog scopen mit `its.locator("[role=dialog] input[type=checkbox]")`
   (liefert exakt die N Checkboxen in fester Baum-Reihenfolge, entspricht der Ressourcen-Upload-Reihenfolge)
   und **per Index ansprechen** statt per Text. Vorher einmal per Screenshot die Baum-Reihenfolge ablesen,
   dann Ziel-Ressourcen auf Index mappen. Genauso fuer den eigentlichen Ressourcen-Auswahl-Dialog beim
   Datei-Anhaengen an Mitteilungen relevant, falls dort aehnliche Symptome auftreten.
6. **Ressourcen einzeln in Ziel-Reihenfolge in den Plan bringen = alle Eintraege zuerst entfernen (`li.its-
   plans-resource__block`, Chevron per Mausklick auf `x = row_right_edge - 20`, dann "Aus diesem Plan
   entfernen"), dann EINEN nach dem anderen per obigem Index-Dialog wieder hinzufuegen** — jeder
   "Hinzufügen"-Durchlauf haengt genau einen Eintrag ans Ende der Liste an, das ergibt zuverlaessig die
   gewuenschte Reihenfolge (getestet: 13-14 Eintraege nacheinander, 100% Trefferquote sobald obige
   Index-Falle vermieden wird).

**Offen fuer die naechste Wiederholung:** 7c I/II und 7d I/II sind weiterhin nicht angefasst (siehe auch
den 7c-Sichtbarkeits-Fund vom 22.07. oben) — vor Beginn dort pruefen, ob Recap-Dateien/Sound-Ordner
inzwischen auch fuer die "b"/"c"/"d"-Kurse existieren (Stand 23.07. nur bei "a" vorhanden), das aendert die
erreichbare Ziel-Reihenfolge.

## ✅ 23.07.2026 (Mittag/Nachmittag): ALLE 8 KURSE fertig — 7c I/II, 7d I/II umgestellt + 7b I/II Sound-Ordner nachgezogen

Rest-Auftrag abgeschlossen: **7c I, 7c II, 7d I, 7d II** auf den flachen 7a-I-Zustand umgestellt (gleiches
Muster wie beim 7a-II/7b-Lauf), **zusaetzlich** 7b I/7b II nachtraeglich mit einem "Sound"-Ordner
ausgestattet (fehlte dort bisher, Sommer-Song-Dateien lagen lose im Plan). **Damit sind jetzt alle 8 Kurse
strukturell auf 7a I ausgerichtet**, soweit die jeweils vorhandenen Ressourcen das zulassen.

**⚠️⚠️ KRITISCHER FAST-DATENVERLUST — Regel fuer alle kuenftigen Wiederholungen:** Beim automatisierten
"Verschieben nach"-Schritt (Downloads-Inhalt auf Ressourcen-Top-Level raeumen) den Zielordner **NICHT per
Text** anklicken (`get_by_text("Computer Basics X (26/27)")` o.ae.) — Kurstitel sind **uneinheitlich
formatiert** (manche "Computer Basics 7c II (26/27)", 7d I aber schlicht **"Computer Basics - 7d I"** ohne
Jahres-Suffix, mit Bindestrich). Ein textbasierter Match schlaegt dann fehl oder trifft den falschen Knoten.
**Robuster Selektor:** Der Wurzel-Ordner im "Verschieben nach"-Baum ist immer eindeutig ueber
`li.itsl-tree-view-item__container` mit einem Kind-Element der Klasse `itsl-tree-view-item__icon--root`
identifizierbar — auf das `span` darin klicken, NICHT auf `get_by_role("treeitem").first` (klickt je nach
Trefferpunkt evtl. nur das Icon/Chevron und toggelt Aufklappen statt zu selektieren — das fuehrte bei 7d I
zu einem stillen "Verschieben nach sich selbst", d.h. die Dateien blieben faktisch IN Downloads).
- **Konsequenz, die fast schiefging:** Weil der Root-Klick fehlschlug, blieben bei 7d I alle 11 Dateien in
  Downloads. Die nachfolgenden Schritte (Thema vom Plan loesen, Downloads-Block aus Plan entfernen, **Thema
  endgueltig loeschen**) liefen aber trotzdem durch — und das Loeschen des Themas **loescht kaskadierend den
  verknuepften Ordner MIT SEINEM GESAMTEN INHALT**, nicht nur einen leeren Ordner! Alle 11 Original-Dateien
  waren damit weg (nur "Sound" blieb, weil separat schon vorher rausbewegt).
- **Rettung/Recovery-Weg (falls das nochmal passiert):** Kurs → Ressourcen → **Papierkorb** → dort gibt es
  **ZWEI separate Tabs: "Ressourcen" und "Pläne"**. Das geloeschte Thema (samt Ordner+Inhalt) landet im
  **"Pläne"-Tab**, nicht im "Ressourcen"-Tab (dort erscheinen nur einzeln geloeschte Dateien). Checkbox
  anhaken (`input[type=checkbox]` in der Zeile, `.evaluate("el => el.click()")`) → Button "Wiederherstellen"
  → **Bestaetigungsdialog erscheint als eigenes `.prom-modal2__wrapper`** mit einem GLEICHNAMIGEN
  "Wiederherstellen"-Button — den in der sichtbaren Modal-Instanz treffen (`.prom-modal2__wrapper` kann bei
  Retries mehrfach im DOM liegen, nur den sichtbaren nehmen: `is_visible()`-Check), sonst klickt man
  faelschlich den Hintergrund-Button der Seite (Fehler "backdrop intercepts pointer events"). Nach
  erfolgreichem Wiederherstellen ist der Ordner MIT allen urspruenglichen Dateien UND der
  Thema-Verknuepfung wieder da — 1:1 Ausgangszustand, kein Datenverlust.
- **✅ Daueregel:** Vor dem Loeschen eines Themas **IMMER** erst explizit verifizieren, dass der verknuepfte
  Ordner wirklich leer ist (`its.get_by_text("Dieser Ordner ist leer").count() > 0` o.ae. abfragen/per
  Screenshot), NICHT blind davon ausgehen dass der vorherige "Verschieben"-Schritt geklappt hat.

**Weitere neue DOM-Erkenntnisse:**
- **"Aus diesem Plan entfernen"-Button:** Bei mehreren Ressourcen-Zeilen im Plan hat JEDE Zeile ihr eigenes
  (meist verstecktes) Dropdown mit demselben Menuepunkt-Text im DOM → `get_by_text("Aus diesem Plan
  entfernen")` wirft "strict mode violation" mit 10+ Treffern. Stattdessen `get_by_role("button", name="Aus
  diesem Plan entfernen")` verwenden (matcht zuverlaessig nur den aktuell offenen/sichtbaren Menuepunkt).
- **Pläne-Tab-Layout ist pro Kurs unterschiedlich** (bestaetigt noch einmal): 7d I zeigte z.B. nur "Thema
  (n) / Alle Pläne (n)" (kein "Aktuell/Vergangen/Ohne Datum" wie bei anderen Kursen) — beim Oeffnen eines
  Plans immer mit Fallback-Tab-Liste arbeiten (["Ohne Datum","Alle Pläne","Aktuell"], jeweils pruefen ob
  vorhanden), niemals einen bestimmten Tab-Namen hart voraussetzen.
- **Ergebnis pro Kurs:**
  - **7c I** (16 Ausgangs-Ressourcen, Sonderfall): hat als einziger Kurs zusaetzlich zum 7a-I-Kern ein
    **weiteres echtes Duplikat "4 Schritte.pptx"** (zwei verschiedene LearningToolElementIds, beide
    22.07.2026) UND einen **eigenen Recap-Namen "16-9 Powerpoint Recap.pptx"** (Singular, anders benannt als
    7a I's drei "PowerPoint Recap - ..."-Dateien) — NICHT geloescht (Content-Entscheidung), Duplikat direkt
    hintereinander im Plan platziert, Recap analog zu 7a I auf "Nicht sichtbar" gestellt. Finale
    Plan-Reihenfolge: Curriculum, Agenda, 1-Begrüßung, 4 Schritte ×2, 0-Halloween pptx, St. Nicholas pptx,
    Fun I/II, Memory, Sound (Summertimes-Callin.mp3, Läuft-Sommer.mp3, St.-Nicholas-mp4), 0-Halloween-mp4
    (Extra), Summertime's-jpg (Extra), Recap (versteckt) — 14 Eintraege total.
  - **7c II, 7d I, 7d II** (jeweils 14 Ausgangs-Ressourcen, untereinander identisch): kein Duplikat, kein
    Recap. Finale Plan-Reihenfolge: die 7a-I-Kernreihenfolge (9 Eintraege) + Sound-Ordner + 2
    kursspezifische Extras (0-Halloween-mp4, Summertime's-jpg) = 12 Eintraege. **Kurioser Fund:** Die
    Ressourcen-Dateinamen in 7d I/II tragen weiterhin das Kuerzel **"7c"** im Namen (z.B. "St. Nicholas Day
    7c.mp4" *im 7d-I-Kurs*) — offenbar hat Chris dieselben Quelldateien fuer c und d verwendet ohne
    umzubenennen. Bewusst NICHT umbenannt (Content, nicht Struktur) — nur als Kuriosum vermerkt.
  - **7b I** (nachtraeglich Sound-Ordner ergaenzt): hatte noch KEINEN Sound-Ordner (nur bei "a" und jetzt "c"/
    "d" vorhanden), Sommer-Song-Dateien (2× mp3 + St.-Nicholas-mp4) lagen lose im Plan. Neu angelegt +
    verschoben, Plan neu sortiert: 9 Kern-Eintraege (inkl. weiterhin unangetastetem "4 Schritte.pptx"-Dublikat
    aus dem letzten Lauf) + Sound + Summertime's-jpg = 12 Eintraege.
  - **7b II:** gleiches Vorgehen, kein Duplikat vorhanden. 11 Eintraege final (9 Kern + Sound + Summertime's-
    jpg).
- **7c I/7c II "Sichtbar für Schüler*innen"-Toggle (Plan-Ebene) diesmal bei BEIDEN auf AN verifiziert** — keine
  Wiederholung der Anomalie vom 22.07. (damals war's aus, wurde korrigiert). Kein weiterer Handlungsbedarf.
- **Nicht angefasst (bewusste Content-Entscheidungen, liegen bei Chris):** Duplikat "4 Schritte.pptx" in
  sowohl 7b I als auch jetzt neu in 7c I; die "7c"-Namensreste in 7d I/II Dateinamen.

**Damit ist der komplette 8-Kurse-Angleichungs-Auftrag (begonnen 22.07. nachts, praezisiert 23.07.) fertig.**
Kuenftige Wiederholungen (z.B. naechstes Schuljahr neue Kurse) koennen sich an diesem Abschnitt + dem
"KORREKTUR 23.07.2026"-Abschnitt oben orientieren; die Root-Selektor- und Thema-Loesch-Fallstricke hier sind
die wichtigsten neuen Erkenntnisse.

## ✅ 23.07.2026 (Nachmittag): Recap-Dateien 7a I → 6 weitere Kurse kopiert (Audit + Fertigstellung nach abgebrochenem Vorlauf)

Ein vorheriger Fork-Auftrag ("3 Recap-Dateien aus 7a I nach 7b I/7b II/7c II/7d I/7d II kopieren, in Plan
einsortieren, auf Nicht sichtbar stellen") kam mit einer kryptischen Abbruch-Meldung zurueck und hatte weder
diese Datei noch aktuell.md aktualisiert. Dieser Nachfolge-Durchgang hat zuerst per Screenshot-Audit den
tatsaechlichen Ist-Zustand aller 5 Kurse geprueft, BEVOR irgendwas veraendert wurde — Ergebnis: der alte Lauf
war weiter gekommen als die Abbruch-Meldung vermuten liess.

**Audit-Ergebnis (vor Korrektur):**
- Alle 5 Kurse hatten die 3 Recap-Dateien bereits korrekt in den Ressourcen UND im Plan (richtige Position:
  direkt nach "Sound", am Ende) — **kein einziges Duplikat**, der Upload/Kopier-Schritt war also vollstaendig
  durchgelaufen.
- **7b I:** bereits 100% korrekt (Recaps im Plan, "Nicht sichtbar").
- **7b II:** Recaps im Plan vorhanden, aber faelschlich auf "Sichtbar" stehengeblieben — das war die einzige
  echte Luecke, passend zur Abbruch-Meldung des alten Laufs.
- **7c II, 7d I, 7d II:** bereits 100% korrekt, kein Handlungsbedarf.
- Behoben: 7b II Recaps per Bulk-"Ausblenden" auf "Nicht sichtbar" gesetzt, verifiziert.

**Zusatzauftrag waehrend der Arbeit (Chris live in 7b I entdeckt):** Die Datei "Summertime's Callin'.jpg" lag
lose im Plan **außerhalb** des Sound-Ordners, obwohl der Sound-Ordner bereits eine gleichnamige
"Summertimes-Callin.mp3" enthaelt (⚠️ Chris sprach von "einer mp3", es handelte sich aber tatsaechlich um die
JPG-Coverdatei — im Bericht transparent gemacht, nicht stillschweigend "korrigiert interpretiert"). Fix: JPG
in den Ressourcen per "Verschieben nach" in den Sound-Unterordner verschoben (dabei NICHT den Root-Knoten
anklicken, sondern den sichtbaren "Sound"-Eintrag im Baum-Dialog direkt — bei Zielordner = Unterordner ist
das der richtige Klick-Punkt, anders als beim Rausbewegen AUS einem Ordner), danach den verwaisten
Standalone-Plan-Eintrag ueber Chevron → "Aus diesem Plan entfernen" geloescht. Ergebnis: 7b I jetzt 14
Plan-Eintraege (kein loser Doppel-Verweis mehr), Sound-Ordner-Eintrag deckt die JPG mit ab.

**Nachtraeglicher Auftrag (Chris waehrend der Arbeit, Planaenderung):** 7c I sollte ENTGEGEN der urspruenglichen
Anweisung DOCH die 3 "a"-Recaps bekommen — zusaetzlich zur bereits vorhandenen eigenen "16-9 Powerpoint
Recap.pptx" (nicht als Ersatz). Umgesetzt: 3 Dateien kopiert, in den Plan direkt nach der eigenen Recap-Datei
eingefuegt, auf "Nicht sichtbar" gestellt. **7c I hat damit als einziger Kurs 4 Recap-Dateien total (3
"a"-Recaps + 1 eigene) — das ist gewollt, kein Fehler.**

**🔑 Zwei wichtige neue technische Erkenntnisse fuer kuenftige Wiederholungen:**

1. **Es gibt eine native "Kopie an"-Funktion** im Ressourcen-"Aktionen"-Menue (neben "Verschieben nach") —
   einfacher als Download+Reupload! Ablauf: Checkbox(en) anhaken → Aktionen → "Kopie an" → Dropdown
   "Zielbereich waehlen" (`select.select_option(label="Computer Basics X (26/27)")`) → im Ordnerbaum den
   **Root-Knoten** anklicken (robuster Selektor wie gehabt: `li.itsl-tree-view-item__container` mit Kind
   `itsl-tree-view-item__icon--root`) → Button **`get_by_role("button", name="Kopieren", exact=True)`**
   klicken (ein simpler `text=Kopieren`-Match trifft haeufig einen falschen/unsichtbaren Treffer und tut
   nichts). Die Sichtbarkeit der Quelldatei wird beim Kopieren **mit uebernommen** (war die Recap-Datei in
   7a I schon "Nicht sichtbar", ist die Kopie im Zielkurs es auch — sofort nach dem Kopieren, ohne
   Extra-Schritt).
2. **⚠️ Falle: Eine Ressource zu einem Plan hinzuzufuegen setzt ihre Sichtbarkeit zurueck auf "Sichtbar"** —
   selbst wenn sie vorher (z.B. durch die "Kopie an"-Uebernahme) schon "Nicht sichtbar" war! Das kostete bei
   7c I einen Extra-Durchgang (Recaps kopiert → korrekt "Nicht sichtbar" → nach Plan-Hinzufuegen ploetzlich
   wieder "Sichtbar" → erneut per Bulk-"Ausblenden" korrigiert). **Reihenfolge fuer kuenftige Laeufe:** immer
   ERST alle Ressourcen in den Plan einsortieren, DANN als allerletzten Schritt die Sichtbarkeit pruefen/setzen
   — nie umgekehrt, sonst wird der Sichtbarkeits-Schritt vom Plan-Hinzufuegen wieder ueberschrieben.

**Lektion zur Kommunikation:** Chris' Beschreibung "eine mp3 liegt lose" traf technisch nicht exakt zu (es war
eine JPG) — trotzdem war die zugrundeliegende Struktur-Idee (Datei duppelt Sound-Ordner-Inhalt, gehoert dort
rein) korrekt und wurde entsprechend umgesetzt. Bei Abweichungen zwischen Nutzerbeschreibung und tatsaechlichem
Datei-Befund: umsetzen was strukturell gemeint war, aber die Abweichung explizit im Bericht nennen statt sie zu
verschweigen.

**Ergebnis: Alle 6 Kurse (7b I, 7b II, 7c I, 7c II, 7d I, 7d II) jetzt vollstaendig verifiziert fertig** —
Recap-Dateien vorhanden, korrekt im Plan positioniert (direkt nach Sound), korrekt "Nicht sichtbar"
(7c I mit der bewussten 4-statt-3-Ausnahme). Kein weiterer Handlungsbedarf zu diesem Auftrag.

## 23.07.2026 (spaeter Nachmittag): 7b I "kaputtes Planbild" — echtes Problem, von Chris selbst in Sekunden gefixt

Chris meldete per Screenshot ein kaputtes-Bild-Icon in der Bildbox des Plan-Editors von 7b I (Plan "Hier
findet Ihr PPTs, Music …") statt des dort erwarteten Minecraft-Kursbilds. Der ausloesende Fork wurde vom
Anthropic-Sitzungslimit abgewuergt und hatte nur das Kurs-Ebene-Bild geprueft ("laedt einwandfrei nach
Hard-Reload") — das war aber nicht dieselbe Stelle wie Chris' Screenshot (Plan-Editor-Bildbox), daher
falsche Entwarnung von Bolla. **Tatsaechlich war die Bild-Verknuepfung im Plan-Editor echt kaputt.**
Chris hat es selbst manuell neu gesetzt ("dauerte Sekunden") — kein Automatisierungs-Aufwand noetig, reines
Klick-Fix im itslearning-UI (Bild in der Plan-Editor-Bildbox neu auswaehlen/hochladen). Kein weiterer
Handlungsbedarf, aber Lektion: bei Bild-/Anzeige-Bugs immer die EXAKTE Stelle aus dem Screenshot pruefen,
nicht eine plausibel klingende Nachbar-Stelle (Kurs-Ebene vs. Plan-Editor sind zwei getrennte UI-Orte).

## 23.07.2026 (Abend): Echter End-zu-Ende-Test — Kurstag 1 an alle 4 "I"-Kurse live gepostet

Chris wollte vor der 17-Tage-Sommerreise (Start 24.07.) noch einen echten Vollzugstest des etablierten
Anstups-Workflows machen. `itslearning_post_kurstag.py` mit 4 frisch formulierten Mitteilungstexten
(DAY_PREFIX="01", COURSES-Array direkt im Skript aktualisiert) fuer **7a I, 7b I, 7c I, 7d I** ausgefuehrt.

**Ergebnis: Alle 4 Kurse erfolgreich, verifiziert per Screenshot:**
- Standard-Paket automatisch korrekt erkannt: `01-Editor-Anleitung.html`, `01-Praktikum.html`,
  `01-The Basics - Grundbegriffe - I.pdf` (alle 3 "01-"-praefigierten Dateien).
- Alle 4 Mitteilungen veroeffentlicht mit individuellem Text + allen 3 Anhaengen korrekt sichtbar.
- Plan-Bilder (7A I/7B I/7C I/7D I) unveraendert intakt, Ressourcen-Ordner nicht durcheinandergebracht.
- Kein Skript-Fehler, kein DOM-Fallstrick-Neuland — die bekannten Selektoren aus fruehreren Laeufen
  griffen alle einwandfrei.

**Kleine Beobachtung, kein Fehler:** Der "Letzte Aenderungen"-Feed zeigt bei manchen Kursen "17/18
Ressourcen hinzugefuegt" statt der erwarteten 3 — das ist offenbar itslearnings eigenes Aktivitaets-Log,
das mehrere juengere Aktionen in einem Eintrag buendelt (Plan-Materialienzahl blieb bei den erwarteten
12-13, kein tatsaechliches Duplikat entstanden).

**⚠️ Status bei Abschluss dieses Forks: Die 4 Mitteilungen + Anhaenge sind LIVE und noch NICHT
zurueckgerollt.** Chris wollte selbst live nachschauen/testen, bevor der Rueckbau (bekannte Skripte
`itslearning_delete_latest_message.py` + `itslearning_delete_resources.py`) ausgefuehrt wird. Falls diese
Session abbricht, bevor der Rueckbau passiert ist: das ist ein bewusster Zwischenzustand, kein Fehler —
erst nach Chris' Rueckmeldung entfernen.

## 23.07.2026 (Abend, 2): Testlauf sauber zurueckgerollt — Chris hat live bestaetigt ("perfekt, top")

Rueckbau ausgefuehrt: `itslearning_delete_latest_message.py` (4 Mitteilungen geloescht) dann
`itslearning_delete_resources.py` (BASENAMES vorher um `01-Editor-Anleitung` ergaenzt, war im Skript
urspruenglich nur mit 2 der 3 Testdateien befuellt — jetzt dauerhaft auf alle 3 Standard-Tag-1-Dateien
korrigiert) — je 3 Ressourcen pro Kurs geloescht. Per Screenshot + Text-Suche verifiziert: alle 3
Test-Dateien in allen 4 Kursen (7a I, 7b I, 7c I, 7d I) mit 0 Treffern bestaetigt, Kurse zurueck auf
Ausgangszustand vor dem heutigen Test. Kein Datenverlust, keine Abweichungen.

**Bewaehrt:** Der komplette Post-Workflow (`itslearning_post_kurstag.py`) lief beim heutigen Live-Test
fehlerfrei durch — Chris braucht ihn 19× im Schuljahr 26/27 (siehe [[feedback_itslearning_workflow_bewaehrt]]).
Fuer kuenftige Laeufe: `itslearning_delete_resources.py`s BASENAMES-Default steht jetzt auf den 3
Standard-Tag-1-Dateien (war vorher unvollstaendig) — bei anderen Kurstagen vor Gebrauch anpassen.

## 🔑 Trigger-Konvention (11.08.2026, von Chris bestätigt): EIN Termin-Auftragsfeld → alle 4 Klassen

Chris will den itslearning-Post NICHT jedes Mal neu beschreiben oder pro Klasse einzeln anstupsen. Der
Anstoß kommt aus dem **schon bestehenden Termine-Auftragsfeld** auf der mp-Seite "Schuljahr 26/27"
(`schuljahr_update_termin` speichert Freitext je Termin in `data/schuljahr2627.json` → `termine[].auftrag`;
📌-Klick ruft `schuljahr_nudge_termin` auf, das daraus einen Prompt baut und in `data/board_nudges.json`
queued — landet automatisch beim nächsten Session-Start via SessionStart-Hook, siehe
[[feature_projekt_board]]). Es gibt **kein eigenes Feld pro Klasse (7a/7b/7c/7d)** und braucht auch keins —
Chris' Formulierung "aus der 7a I anstupsen" meint genau dieses eine Termin-Feld, nicht eine neue UI.

**Feste Regel ab jetzt:** Enthält der Auftragstext eines Termins sinngemäß "itslearning" (z.B. "Bitte
itslearning", auch Tippfehler/Kurzform), bedeutet das IMMER: den kompletten, bewährten
`itslearning_post_kurstag.py`-Workflow für **alle 4 Klassen der aktiven Gruppe** ausführen — ohne
Rückfrage, welche Klassen gemeint sind. Ableitung der Parameter, komplett automatisch aus dem Termin-Objekt:
- **Gruppe (I/II)** = `termin["gruppe"]` → Kurse `Computer Basics 7a <Gruppe>`, `7b <Gruppe>`, `7c <Gruppe>`,
  `7d <Gruppe>` (Kurs-IDs siehe bisherige Skript-Läufe/`itslearning_post_kurstag.py`-Historie).
- **DAY_PREFIX** = führende Zahl in `termin["thema"]` vor " – ", zweistellig mit führender Null
  (z.B. "3 – Basics Office: Tastatur" → `03`; "0/1 – Begrüßung, Intro …" → **Sonderfall `01`**, siehe
  Tag-1-Live-Test oben, der 00-präfigierte Datei bewusst NICHT ins Standard-Paket aufgenommen hat).
- **Standard-Paket** = automatisch via `discover_files()` (PDF + alle `NN-*.html` im Handouts-Ordner) —
  kein manuelles Zusammenstellen nötig.
- **4 Mitteilungstexte** jedes Mal neu formulieren (nie kopieren, [[feedback_ki_texte_natuerlich]]), Ton/
  Emoji-Vorgaben wie oben dokumentiert ("Textvorgaben für jede Mitteilung").
- **Keine Extra-Freigabe vor dem Veröffentlichen nötig** — das Anstupsen selbst ist bereits die Freigabe
  (Ausnahme-Regel für den MP-Anstups-Kanal, siehe [[feedback_website_schreibzugriff]] und den Tag-1-Live-Test
  oben, der ohne Vorab-Freigabe lief).

**How to apply:** Sobald eine Session mit einem Anstups-Prompt startet, der aus einem Schuljahr-2627-Termin
mit "itslearning" im Auftragstext stammt (Titel-Muster `▸ Schuljahr 26/27: <Thema>`), sofort obige
Ableitung durchführen und den Post-Lauf für alle 4 Klassen starten — nicht erst nachfragen, welche Klassen
oder welcher Kurstag gemeint sind, das steht schon vollständig im Termin-Objekt.

## 📅 "Eure [ersten/nächsten] Termine"-Mitteilung — eigenes, wiederkehrendes Format (bestätigt 12.08.2026)

Getrennt vom Kurstag-Materialien-Post (`itslearning_post_kurstag.py`, oben) gibt es eine ZWEITE Art
Mitteilung, die Chris schon letztes Schuljahr manuell verwendet hat und ab 26/27 im selben Format
fortsetzen will: eine reine Text-Ankündigung der naechsten 4 Kalendertermine (kein Datei-Anhang). Format
(aus Screenshots vor der Löschung der Alt-Mitteilungen am 12.08.2026 rekonstruiert, in allen 4 Klassen
identisch, nur Daten/Zeit unterschiedlich):

```
Eure ersten Termine 📅:

Mi. 19.08.26
Mi. 26.08.26
Mi. 02.09.26
Mi. 09.09.26

immer 1./2. Stunde 07:50 Uhr

Ich freue mich sehr auf Euch 😊
```

**Wichtige Eigenheiten (aus dem Vorjahres-Vergleich abgeleitet, nicht frei erfunden):**
- **Grundformat bleibt fix** (Termine als Zeilen, "immer X./Y. Stunde HH:MM Uhr", Freuensatz am Ende)
  — das ist Chris' eigene Formulierung von letztem Jahr, die Kernstruktur ändert sich nicht.
  **Korrektur 14.09.2026:** anders als ursprünglich angenommen will Chris die 4 Klassen-Texte NICHT
  mehr zwingend 1:1 wortgleich — auf expliziten Wunsch ("vlt varianten im text wenn es geht") wurden
  beim Post für Gruppe I nach den Herbstferien Einleitung/Schlusssatz pro Klasse leicht variiert
  (z.B. "Eure nächsten Termine 📅:" / "Hier eure nächsten Termine 📅:" / "...im Überblick 📅:",
  Schlusssatz "Ich freue mich sehr auf Euch 😊" / "Bis bald, ich freue mich auf Euch 😊" / etc.).
  **Regel jetzt:** Varianten in Einleitung/Schluss sind ok und sogar erwünscht, wenn schnell machbar
  — nur Termine/Uhrzeit exakt gleich lassen. Reiner Fallback (falls Chris zu einem künftigen Lauf
  nichts dazu sagt): leichte Varianten bauen, nicht mehr stur 1:1 kopieren.
- **⚠️ FALSCH, Chris-Korrektur 12.08.2026:** Im ersten Live-Lauf (12.08.2026) habe ich I- und II-Kurs
  derselben Klasse denselben Text (dieselben 4 Termine der Gruppe I) posten lassen — abgeleitet aus dem
  Vorjahres-Screenshot-Vergleich, wo 7a I und 7a II ebenfalls wortgleich waren. Chris hat das als Fehler
  erkannt: **das war schon LETZTES Jahr falsch**, kein gewolltes Muster. Jeder Kurs (I und II) muss die
  Termine SEINER EIGENEN Gruppe zeigen — Gruppe II startet nach dem ersten 4-Wochen-Block von Gruppe I,
  hat also andere (spätere) erste 4 Termine. Korrektur-Skript:
  `scripts/itslearning_fix_gruppe2_termine.py` (löscht die falsche Mitteilung in den 4 II-Kursen, postet
  die echten II-Termine). **Lehre für alle künftigen Läufe:** beim Ableiten der Termine für so eine
  Ankündigung IMMER nach `klasse` UND `gruppe` aus `data/schuljahr2627.json` filtern, nie nur nach `klasse`
  — auch wenn ein Vorjahres-Beispiel etwas anderes suggeriert, im Zweifel die Logik (I zuerst, dann II)
  über das beobachtete Altbeispiel stellen.
- **Wiederkehrend, nicht einmalig:** "Eure ersten Termine" nur beim allerersten Block des Schuljahres.
  Am Ende jedes 4-Wochen-Blocks (I/II-Wechsel, siehe [[project_schuljahr2627]]) folgt eine neue Mitteilung
  "Eure nächsten Termine 📅:" mit den nächsten 4 Terminen der dann aktiven Gruppe — bisher noch nicht
  automatisiert (nur der Post selbst, nicht das Erinnern), Chris stößt das pro Block manuell/im Chat an.
  ca. 9-10× im Schuljahr fällig.
  **Erinnerung eingerichtet (12.08.2026):** Cron-Job `itslearning_naechste_termine_reminder.py`
  (`0 7-11 * * *`, datumsbasiert/einmalig ab 05.09.2026, State-Datei
  `config/itslearning_naechste_termine_reminder_state.json`) schickt Chris per Telegram eine Erinnerung
  kurz bevor der erste Block endet (09./10.09.2026). Nur für DIESEN einen Block-Wechsel — für alle
  künftigen Wechsel im Schuljahr muss vorher jeweils ein neuer, gleich gestrickter Reminder mit
  passendem `FIRE_FROM`-Datum angelegt werden (Datum aus `data/schuljahr2627.json` ableiten, wenn der
  jeweils vorherige Block feststeht).
- Datumsformat: `Wochentag-Kürzel. TT.MM.JJ` (deutsches 2-stelliges Jahr, mit Punkt), eine Zeile pro Termin,
  keine Aufzählungszeichen.
- Die 4 Termine + die Uhrzeit lassen sich direkt aus `data/schuljahr2627.json` (`termine[]`, gefiltert nach
  `klasse` + `gruppe`) ableiten, s. [[project_schuljahr2627]] für die Feld-Struktur (`klasse`/`uhrzeit`
  seit 12.08.2026 vorhanden).
- Skript für den ersten Block 26/27: `scripts/itslearning_post_erste_termine.py` (alle 8 Kurse in einem
  Lauf, mit den oben gezeigten fest eingetragenen Texten). Für künftige Blockwechsel: gleiches Muster
  (Text-only, `post_text()`-Funktion), neue Daten aus der JSON ziehen, keine Datei-Anhänge.

## ⚠️ 17.08.2026: Neu hochgeladene Datei fehlt kurzzeitig im "Ressource hinzufügen"-Dialog (Timing, kein echter Fehler)

Beim Kurstag-1-Post (4 Dateien: 3× HTML aus `Praktikum/` + 1× PDF) liefen 7a I und 7b I sauber durch,
bei 7c I und 7d I meldete `post_message()` `"Datei '01-Download-Anleitung' im Ressource-Dialog nicht
gefunden"` — obwohl `upload_files()` direkt zuvor im selben Lauf erfolgreich "4 Datei(en) hochgeladen"
gemeldet hatte. Nachgeprüft: Datei war tatsächlich schon korrekt in den Ressourcen des Kurses (Tab
"Ressourcen" zeigte sie sofort) — nur der **"Ressource hinzufügen"-Auswahldialog in der Mitteilungsbox
hat einen eigenen, kurzzeitig hinterherhinkenden Cache/Index**, der eine Sekunden zuvor hochgeladene
Datei noch nicht kennt.

**Fix:** Kein Code-Bug, reines Timing. `post_message()` für den/die betroffenen Kurs(e) **isoliert
erneut aufrufen** (nicht den ganzen Upload+Post-Lauf wiederholen — Dateien sind ja schon da, ein
erneuter `upload_files()`-Versuch wäre unnötig/riskiert Duplikate). Beim erneuten Aufruf einige Minuten
nach dem Upload war die Datei im Dialog zuverlässig sichtbar (per gezieltem Locator-Test bestätigt:
`its.locator("[role=dialog]").get_by_text("01-", exact=False)` fand alle 4 Dateien).

**Konsequenz fürs nächste Mal:** Bei einem `"... im Ressource-Dialog nicht gefunden"`-Fehler NICHT von
einem strukturellen Problem ausgehen (Datei-Idempotenz-Check vor dem Upload greift ja schon,
siehe oben) — einfach kurz warten (ca. 1-2 Minuten reichen erfahrungsgemäß) und `post_message()` gezielt
für den fehlgeschlagenen Kurs erneut aufrufen. Betrifft vermutlich eher frisch hochgeladene Dateien mit
noch keiner Historie im Kurs (bei bereits mehrfach verwendeten Standarddateien wie der Editor-Anleitung
trat der Fehler nicht auf).

## ✅ 25.08.2026: "Datei ersetzen"-Weg gefunden — Ressource updaten OHNE die Resource-ID zu verlieren

Bisher dokumentiertes Muster für ein Datei-Update war immer Löschen+Neu-Hochladen (`delete_stale_pdf` +
`upload_files`) — das erzeugt aber intern eine NEUE Resource-ID. Wenn die alte Ressource schon an eine
bereits veröffentlichte Mitteilung angehängt ist, bricht dieser Anhang-Link dabei (verweist dann auf eine
gelöschte Ressource). Für den Anlass "`02-Elterninfo-MS-Konto.html` lokal inhaltlich korrigiert, lag aber
schon live+verlinkt in 4 Kursen" wurde ein besserer Weg gesucht und gefunden: **echtes Ersetzen unter
Beibehaltung der Resource-ID.**

**Ablauf (verifiziert an allen 4 "I"-Kursen, 25.08.2026):**
1. Ressourcen-Tab → Zeile der Ziel-Datei → **"..."-Optionsmenü am rechten Zeilenrand** anklicken (Selektor:
   Zeile über `xpath=ancestor::tr[1]` der Basename-Zelle finden, darin `tr.locator("button").last` — das
   `text=...`-Selektor-Muster aus älteren Skripten funktioniert hier NICHT, es gibt keinen reinen
   "..."-Text-Locator, der Button hat keinen sichtbaren Text-Inhalt).
2. Im aufklappenden Menü **"Bearbeiten"** anklicken — ⚠️ Standard-DOM-Falle wie immer: mehrere unsichtbare
   "Bearbeiten"-Duplikate im DOM (andere Zeilen), IMMER `is_visible()`-Filter verwenden, nie blind `.first`.
   → landet auf einer Detailseite (`ViewLearningToolElement.aspx`) mit Titel, "Herunterladen"-Button und
   einem zweiten, kleineren **"Bearbeiten"-Link** (Stift-Icon).
3. Dieser zweite "Bearbeiten"-Link sitzt in einem VERSCHACHTELTEN Frame (`resource.itslearning.com/File/
   View.aspx`) — mit reinem `page.get_by_text()` nicht erreichbar, muss über `page.frames` gezielt in genau
   diesem Frame gesucht werden. Klick darauf navigiert den Frame zu `resource.itslearning.com/File/
   AddEdit.aspx` — das ist derselbe Upload-Control-Baustein (`ccl-uc-*`-Klassen) wie beim normalen
   Datei-Upload, aber diesmal im EDIT-Kontext, an die bestehende `LearningObjectId`/
   `LearningObjectInstanceId` gebunden.
4. Im `AddEdit.aspx`-Frame: bestehende Datei-Anlage per **`button[aria-label='Delete']`** entfernen (Klasse
   `ccl-fl-item-remove-enabled`).
5. Danach **`button.ccl-uc-dropzone-container`** anklicken — anders als beim Erst-Upload-Flow (siehe oben,
   "Datei-Upload-Flow") öffnet das im LEEREN Zustand (nach dem Delete) den **nativen Dateidialog direkt**
   (`page.expect_file_chooser()` funktioniert sofort), OHNE den Zwischenschritt über ein Popover mit "Ihr
   Computer – Datei"/"Ihr Computer – Ordner"/"Meine Dateien". **Robuste Reihenfolge für künftige Skripte:**
   erst `expect_file_chooser` direkt um den Dropzone-Klick legen (kurzer Timeout ~4s); schlägt das fehl,
   dann erst auf den Popover-Weg mit `#local-picker` ausweichen (id-Selektor, robuster als der
   Text-Selektor `"Ihr Computer – Datei"` aus dem alten Upload-Flow).
6. `set_files([neuer_lokaler_pfad])` auf das File-Chooser-Objekt — Dateiname erscheint sofort in der Zeile
   (Anzeige liegt aber wieder AUSSERHALB des Edit-Frames, im mittleren `ViewLearningToolElement.aspx`-Frame).
7. **"Speichern"-Button klicken — liegt selbst NICHT im Außenrahmen, sondern im `AddEdit.aspx`-Frame!**
   (Naheliegender erster Reflex "Speichern liegt bestimmt außen wie bei anderen Formularen" war hier falsch
   und kostete einen Fehlversuch mit `count()==0`.) Robuste Lösung: über alle `page.frames` UND die äußere
   Seite selbst loopen, `get_by_text("Speichern", exact=True)`, ersten sichtbaren Treffer nehmen.
8. Erfolg zeigt sich als Toast **"Die Datei wurde ersetzt."**

**🔑 Verifiziert per Re-Download + "Letzte Änderungen"-Feed:** Der Kurs-Aktivitätsfeed auf der
Kursübersicht zeigt danach `"Mandel, Christoph hat eine Ressource **aktualisiert**"` (nicht "hinzugefügt")
— eindeutiger Beweis, dass `LearningObjectId`/`LearningObjectInstanceId` unverändert bleiben. Ein
Re-Download der Ressource direkt danach enthielt zuverlässig den neuen Inhalt (getestet über einen
eindeutigen Text-Marker aus der Änderung). **Konsequenz:** Dieser Weg ist ab sofort das **bevorzugte Muster
für jedes künftige Datei-Update einer bereits live verlinkten/verwendeten Ressource** — das alte
Löschen+Neu-Hochladen-Muster (`delete_stale_pdf`) nur noch verwenden, wenn eine Ressource wirklich neu
angelegt werden soll oder noch an KEINE Mitteilung angehängt ist.

**Offen/nicht getestet:** Ob dieser Weg auch bei PDF-Ressourcen (nicht nur HTML) genauso funktioniert —
das MS-Konto-PDF war in diesem Fall bewusst nicht live (Chris druckt es selbst aus), daher kein Testfall
verfügbar. Vor einer PDF-Ersetzung diesen Ablauf erst an einem Testkurs verifizieren, nicht blind annehmen.

**Neue Dauerregel (Chris, 25.08.2026):** Wird eine Handout-Datei lokal aktualisiert, die bereits als
Ressource live in itslearning liegt, IMMER automatisch auch dort nachziehen (ersetzen, nicht neu posten) —
ohne extra nachzufragen, ob "auch itslearning" gemeint ist. Siehe `feedback_handout_update_itslearning_sync`.

## ✅ 08.09.2026: Kurstag 4 „The Basics: Codierung" — alle 4 Mitteilungen live (7c I mit Umweg)

DAY_PREFIX="04", Gruppe I. Paket (`discover_files("04")`): **`04-Praktikum.html` + `04-The Basics -
Codierung.pdf`** — nur 2 Dateien (KEINE `04-Praktikum.pdf`, s. Dauerregel unten). PDF vorher frisch aus
der (von Chris minimal geänderten) PPTX erzeugt (`scripts/pptx_to_pdf.ps1`), Alt/Neu seitenweise
verglichen: inhaltlich identisch, nur Folie 2/3/12 Layout-Mikroverschiebung.

- **7d I (190860), 7b I (190741), 7a I (190735):** im `itslearning_post_kurstag.py`-Lauf glatt durch,
  je 1 Mitteilung + beide Anhänge, keine Dups. Verifiziert.
- **7c I (190861):** `upload_files` meldete Erfolg, aber itslearning brauchte server-seitig mehrere
  Minuten, bis das `04-`-Paket in den Ressourcen auftauchte (Banner „Die Dateien werden hinzugefügt.
  Sobald der Vorgang abgeschlossen ist, benachrichtigen wir Sie."). `post_message` schlug in diesem
  Fenster fehl (`FAIL_190861_attachpicker.png`). Ein Auto-Retry-Skript, das die Sichtbarkeit über
  `its.goto("…/Resources?FolderID=%s" % CourseID)` prüfte, lief 6×60 s ins Leere — **weil diese URL
  zwischendurch „Das Objekt ist nicht vorhanden, oder der Zugriff wurde verweigert." lieferte
  (FolderID ≠ CourseID, alte bekannte Falle).** Danach sauber geprüft (Kurs-Home → Ressourcen-Tab
  klicken statt FolderID raten): Upload WAR längst durch (30 Ressourcen, `04-`-Paket je 1×, kein Dup),
  nur die Mitteilung fehlte. `post_message(its, 190861, text, files)` einzeln nachgezogen → OK.

**🔑 Lehren:**
1. **Bei „… im Ressource-Dialog nicht gefunden" NICHT mit einer FolderID-URL nachpollen.** Immer über
   Kurs-Home → Ressourcen-**Tab-Klick** verifizieren (`get_by_role("link", name="Ressourcen")`). Die
   `Resources?FolderID=<X>`-Direkt-URL ist unzuverlässig (FolderID ist pro Kurs eigen, nicht = CourseID).
2. **Retry nur mit `post_message`**, nie den ganzen Upload-Lauf wiederholen (Dup-Gefahr). Wartefenster
   ruhig großzügiger (5–10 Min) als die bisher dokumentierten 1–2 Min — der Upload-Index kann bei
   einzelnen Kursen deutlich länger hinterherhängen.
3. „count == 2" für einen Anhang-Dateinamen im Home-Feed nach dem Post ist NORMAL (1× in der
   Mitteilung, 1× in „Letzte Änderungen"), kein Duplikat.

## 📌 Dauerregel (Chris, 08.09.2026): Praktikum-HTMLs kommen NIE als PDF ins itslearning-Paket

Chris: „wir hatten doch vereinbart, dass ich das Praktikum nie als PDF brauche." Das Praktikum läuft
ausschließlich über die interaktive `NN-Praktikum.html` (Q&A-Format mit Lösungs-Toggles — als PDF
exportiert würde es die Lösungen leaken). **Nur die Folien-Präsentation** (`NN-<Thema>.pdf`, aus der
PPTX) kommt als PDF ins Paket. → Nie wieder eine `NN-Praktikum.pdf` bauen, suchen oder im
`discover_files`-Ergebnis vermissen. (Ältere Kurstage 1–3 haben teils noch eine `0N-Praktikum.pdf` in
den Ressourcen liegen — Altbestand, nicht nachträglich anfassen, aber für neue Kurstage nicht mehr
erzeugen.) Verwandt: [[feedback_prakt_anleitungen]].

## ✅ 21.09.2026: Ersetz-Skript + PDF-Ersetzen bestätigt
`scripts/itslearning_replace_resource.py <basename> <lokaler_pfad> <"7d II,7b II"|all>` setzt den 25.08.-Ablauf um (Menü „…" →
Bearbeiten → 2. Bearbeiten im Frame `File/View` → Delete → Dropzone/File-Chooser → Speichern im `AddEdit`-Frame). **Funktioniert auch
bei PDFs** (4/4 Kurse, Toast „Die Datei wurde ersetzt."). Der Toast erscheint erst nach dem Speichern-Klick verzögert — Screenshot
(`/tmp/its_debug/replace_<CourseID>.png`) prüfen statt sich auf den sofortigen Text-Check zu verlassen. Bricht bei >1 Treffer für den Basename ab.

## ⚠️ Chris' EIGENE zwei Identitäten in itslearning — nicht verwechseln (28.09.2026)

Chris hat in itslearning **zwei verschiedene Anzeigenamen für sich selbst**, je nachdem mit welchem
Schulportal-Login er sich anmeldet — beides sind seine eigenen echten Accounts, kein Schüler-Fake:

- **Login `cmandel`** (Standard, s.o.) → erscheint als **„Mandel, Christoph"**, Rolle **Lehrkraft**.
- **Login `cmandel2`** (Chris' eigener Test-/Zweitaccount) → erscheint als **„Mandel, Chris"**, Rolle
  **Schüler*in**.

**Warum wichtig:** Bei der Suche nach einem Nachrichten-Empfänger (private Mitteilungen, siehe
Geburtstagssong-Automatisierung) taucht „Mandel, Chris" wie ein ganz normaler Schüler in der
Empfänger-Suche auf (Suche nach `cmandel2` selbst findet NICHTS, die Empfänger-Suche geht nach
Anzeigename, nicht Login-Name — nur `mandel` als Suchbegriff führt hin). Nicht verwechseln mit einem
echten Schüler gleichen/ähnlichen Namens. Bei jedem künftigen Test mit dem Zweitaccount: Zielperson ist
„Mandel, Chris" (Schüler-Rolle), nicht „Mandel, Christoph".

## ✅ 28.09.2026: Private 1:1-Nachrichten (Geburtstagssong-Automatisierung) — erster Testversand erfolgreich

Neues Terrain (bisher nur Kurs-Mitteilungen automatisiert) — Skript `scripts/itslearning_send_private_song.py`
funktioniert jetzt zuverlässig. Wichtigste DOM-/Verhaltens-Fallstricke:

- **Compose-UI:** Sprechblasen-Icon oben rechts (`its.mouse.click(1417, 27)`) → „Neue Nachricht" → Empfänger-
  Suchfeld `get_by_placeholder("Personen, Kurse oder Projekte suchen")`.
- **Empfänger-Suche geht nach ANZEIGENAME, nicht Login-Name** (s.o., Identitäten-Falle). ZWEI zusätzliche
  DOM-Fallen dabei: (1) `get_by_text(name, exact=False)` matcht auch einen unsichtbaren „Obermengen"-Treffer
  irgendwo im DOM (z.B. Chris' eigenes Profil-Badge „Mandel, Christoph" bei Suche nach „Mandel, Chris").
  (2) Das sichtbare Dropdown-Ergebnis hat einen unsichtbaren Zusatzpunkt im textContent
  (`"Mandel, Chris."` statt `"Mandel, Chris"`) — `exact=True` matcht deshalb NIE. **Robuster Weg:** alle
  `exact=False`-Treffer holen, nur das SICHTBARE Element per `is_visible()` nehmen, und mit
  `.startswith(name)` statt `==` vergleichen.
- **Anhänge: Büroklammer öffnet ein Mini-Menü**, kein direkter Datei-Dialog — zwei Optionen: „Ihr Computer –
  Datei" (lokale Datei hochladen, das ist der richtige Weg) vs. „Meine Dateien" (itslearnings EIGENE
  Dateiablage — dort liegt nichts, wenn die Datei noch nie hochgeladen wurde; führte bei Chris' erstem
  manuellen Testversand dazu, dass gar kein Anhang ankam). `fc.set_files([...])` akzeptiert auch mehrere
  Pfade auf einmal (Mehrfachauswahl funktioniert technisch), s.u. aber zur Zustellung.
- **⚠️ Text + JEDER Anhang werden beim Senden als SEPARATE Nachrichten-Blasen verschickt**, nicht als eine
  Nachricht mit N Anhängen. Die Uploads laufen sequenziell NACH dem Klick auf „Senden" (nicht schon beim
  Auswählen der Datei/en) — bestätigt per Netzwerk-Mitschnitt: pro Anhang ein eigener
  `POST .../instantmessages/attachment/v1`. Bei 2 Videos (~13 MB zusammen) dauerte der komplette Ablauf
  bis zu ~15-20s. **Ein zu kurzer Fixwartezeit-Check nach „Senden" meldet fälschlich Erfolg, obwohl der
  zweite Anhang noch fehlt** (live erlebt: erster Testlauf kam nur mit Text an, gar kein Anhang — zweiter
  Testlauf mit 3s Wartezeit killte in Wahrheit nur einen Fehlklick auf den „X"-Button eines Anhangs, weil
  Koordinaten-Klicks bei wechselnder Anhangzahl die Position verschieben). **Fix:** NIE Koordinaten-Klicks
  für Anhang-/Senden-Button verwenden — stabile `aria-label`-Selektoren nehmen:
  `button[aria-label='Dateien an diese Nachricht anhängen']` und `button[aria-label='Senden']` (Position
  unabhängig vom Panel-Inhalt). Nach dem Senden GEDULDIG pollen (bis zu ~40s in 2s-Schritten), bis der
  Platzhalter des Nachrichtenfelds von „Nachricht schreiben" zu „Nachricht schreiben an &lt;Empfänger&gt;"
  wechselt — das ist der zuverlässige Beleg, dass alles (Text + alle Anhänge) durch ist.
- **Keine Lösch-Funktion für einzelne private Nachrichten:** Das „..."-Optionsmenü pro Nachricht bietet nur
  „Weiterleiten" und „Als ungelesen markieren", kein „Löschen". Fehlversuche beim Testen bleiben im Verlauf
  stehen (bei Testaccounts unkritisch, bei echten Schülern also besonders sorgfältig vorher testen).
- **Test erfolgreich verifiziert** (28.09.2026, Empfänger „Mandel, Chris"/cmandel2, Songs von Tammo/7a):
  finale Nachricht + beide mp4-Anhänge kamen korrekt als 3 aufeinanderfolgende Blasen an.

## 📅 Geburtstagssong-Workflow — feste wöchentliche Routine (ab 28.09.2026)

- **Jeden Montag** (Cron `itslearning_geburtstagssong_namen_montag_reminder.py`, 7-11 Uhr,
  feuert max. 1× pro Kalenderwoche) erinnert ein Telegram-Reminder Chris daran, die **2 Namen für
  Mittwoch + 2 Namen für Donnerstag** dieser Woche zu liefern — aber NUR wenn diese Woche laut
  `data/schuljahr2627.json` (`termine[]`) überhaupt Unterricht ist (Ferienwochen werden automatisch
  übersprungen, kein manuelles Prüfen nötig).
- **⚠️ Dauerregel: Versand IMMER erst nachmittags, ab 14:00 Uhr** (Präsentation ist vormittags,
  Songs gehen erst danach raus) — Chris sagt das ab jetzt nicht mehr explizit dazu, ist Standard.
  `itslearning_send_private_song.py` hat dafür eine harte Zeitsperre im `__main__`-Block eingebaut
  (bricht vor 14:00 Uhr sofort ab, kein versehentliches Vormittags-Senden möglich).
- Ablauf pro Name: Klassenordner nach den beiden Song-mp4s durchsuchen (Muster wie bei Tammo:
  „Happy Birthday &lt;Name&gt; &lt;Datum&gt;.mp4" + „&lt;Name&gt;'s Birthday Beat....mp4" o.ä. — Schema
  kann variieren, mit `find` verifizieren statt zu raten), Empfänger-Anzeigename in itslearning
  ermitteln (Schülerlisten [[reference_schuelerlisten_7abcd]] oder Chris fragen), Skript-Header
  (EMPFAENGER/MESSAGE/SONGS) anpassen, ab 14:00 Uhr laufen lassen.
