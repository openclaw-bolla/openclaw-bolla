---
name: project-aurora-ii-optimierungen-fuer-iii
description: Sammelstelle aller Optimierungen/Lehren aus AURORA II (Fehlerklassen, kanonische Festlegungen, Prozess) — Grundlage, damit AURORA III der Höhepunkt wird
metadata:
  type: project
---

Chris am 11.10.2026: „merk dir unbedingt auch alles zu den Optimierungen von AURORA II, damit AURORA III der Höhepunkt werden kann." Diese Datei ist die Sammelstelle. **Beim Planen/Schreiben von AURORA III zuerst hier lesen**, und bei jeder neuen AURORA-II-Optimierung ergänzen. Details der Einzelthemen: [[project_aurora_ii]], [[feedback_aurora_ii_analogie_check]], [[feedback_aurora_zahlen_exakt]], [[feedback_aurora_ii_humor_standard]], [[feedback_mp_satzuebernahme_nie_verlust]], [[idea_aurora_fortsetzung]].

## 1. Fehlerklassen aus Chris' Korrekturen (Lesebericht 10./11.10.2026, Kap. 1–27, ~1.000 Funde)
Aus Chris' übernommenen Markierungen abgeleitet (`scratch/aurora_samstag_sa2_20261010/analogie_klassen.json`). Beim Schreiben von III von Anfang an vermeiden:
1. **Unklarer Bezug/fehlendes Bezugswort** (häufigste Klasse): „die Karten", „das Band", „es", „die Akte" ohne eindeutiges Bezugswort. Immer das konkrete Nomen nennen („die Beileidskarten").
2. **Figur/Vorwissen nicht eingeführt** (Band I oder spätere Stelle): Figur beim ersten Auftritt kurz verankern („Frauke Harms, Bastis Frau, Kita-Erzieherin").
3. **Elliptische Sätze/fehlende Wörter** (Verb/Objekt weggekürzt).
4. **Grammatik/Rechtschreibung/Zeichensetzung**, v. a. indirekte Rede ohne Konjunktiv, Getrennt-/Zusammenschreibung.
5. **Schiefe/unpassende Bilder**: Vergleich muss körperlich/logisch passen und darf kein Milieuwissen voraussetzen.
6. **Pointe nicht verständlich**: bei Gags muss das auflösende Glied im Satz stehen („…wie eine Auflaufform: warm, rund und völlig harmlos").
7. **Zahlen-/Zähl-/Timing-Fehler**: gezählte Mengen (Warum-Fragen, Häkchen, Wörter) und Uhrzeiten/Dauern zwischen Kapiteln.
8. **Logik-/Plausibilitätsbruch**: Wissen/Rolle der Figur passt nicht (Neuer hat schon Dateien, Formular weiß vom „Kind").
9. **Abrupter Szenen-/Zeitwechsel** ohne Überleitung.
10. **Detail-Kontinuität** (Jacke an/umgehängt, wessen Becher, Tempus).
11. **Abgenutzter Running Gag**: nicht jedes Mal ausbuchstabieren („Immer zuerst das Böse").
12. **Mehrdeutige Wortwahl**: „aufgehoben", „Lager", „Fach", „Staat", „Vortrag", „Charakter" → präzises Wort („aufbewahrt").
13. **AURORA-Logik nicht nachvollziehbar**: Aussagen müssen maschinell stimmig sein; Nichtwissen sichtbar und gern humorvoll. Dazu: „sehr still"/„zum ersten Mal"/Stille-Formeln nicht inflationär verwenden.
14. **Sprecher/Tonfall unklar** in wörtlicher Rede.

## 2. Kanonische Festlegungen Band II (nicht neu erfinden, in III anschließen)
- **Anhörung: Mittwoch 25.11.** (vorher gemischt 26.), Kap. 1 „22 Tage" passt damit. Kap. 8 Kopf: 9. November / 24 Tage.
- **Theos Entnahme des Blatts: 3. November**; **Todestag Theo: 12. Oktober** (Text Kap. 12/22 „am Zwölften“); **10. Oktober (Samstag) = Abend der Tür/Theos Weggang**, 22:41 Uhr — der kanon-Eintrag in aurora2.json „Todestag ist der 10. Oktober“ ist ungenau, nicht übernehmen; Kap. 10 Poststempel Brüssel 9. November („kam am Dienstag", Foto vom Sa 7.11.).
- **AURORA-Alter: 4 Jahre 7 Monate** (Band I Kap. 46 kanonisch, Kap. 35 war Versprecher, nie korrigieren).
- Frauke „siebzehn/zwanzig Jahre" bleibt wie im Text; Noah Khoury, Mia/Ben sind in Band I korrekt (Fehlalarme des Lesers).
- **Jonas schreibt „die Fünf"** (Kap. 15: Lenis Nachricht nennt Jonas).
- Kap. 2: Kopfhörer „wie eine Federboa um den Hals gewickelt … schnarcht im Takt der Lüfter" (Selbstmord-Vergleich war unpassend).
- Fähigkeiten-Faden (Stufen 1–4) nur in Band II, immer im Kind-Ton, nie Leistungsschau.

## 3. Prozess-Lehren (haben sich bewährt)
- **Analogie-Check nach jedem Kapitel**, Opus (nicht Fork), Fehlerklassen aus Chris' Markierungen → alle Vorkapitel. Musterbibliothek wächst.
- **Zahlen/Daten immer gegen Band I UND alle Band-II-Stellen grep-prüfen**, nicht nur intern.
- **Lesebericht-Pipeline** (`scripts/ausreizen_sa_lesebericht.py`): 1 Klassen+Analogie je Kapitel, 2 Zweitleser, 3 Band-I-Gegencheck, 4 Lesebegleiter, 5 Fehlerjagd-Runden. Schweregrade hoch/mittel/niedrig: hoch ~60 % übernommen, mittel/niedrig ~55 %, viele Fehlalarme. **Nie automatisch ändern — Chris/ich prüfen je Fund**; Daten/Plot-Funde nur mit Chris' OK.
- **Satz-Übernahme darf nie Text löschen** (Bug 29.09.: Jonas-Konter in Kap. 9 verloren → Merge, Kürzungs-Sperre, Backup eingebaut). Immer Backup vor Massenänderung.
- Chris liest selbst Kap. für Kap. (Stand Kap. 12): Entwürfe/Spoiler zu späteren Kapiteln nicht ungefragt ausbreiten.
- Entwürfe Kap. 25–28 liegen nur in `scratch/aurora_samstag_wochenende_20261009/`, nicht im Buch; Plot-Weiche für 28 und Wahl K27-Schluss (Original/A/B) wartet auf Chris.

## 4. Für AURORA III
- Qualitätsmaßstab Humor = Kap. 10 von II; Zahlen von Anfang an in einer **Zeitleiste/Kanon-Datei** führen (statt nachträglich zu vereinheitlichen).
- Figuren beim ersten Auftritt verankern, Pointen ausschreiben, Bilder auf Verständlichkeit prüfen — die 14 Klassen oben als Schreib-Checkliste vor dem ersten Kapitel.
- Bogen III soll Höhepunkt der Reihe werden; Planung erst nach Abschluss von II (Chris liest noch).

## 5. FIGUREN (Stand 11.10.2026; Quelle: `aurora2.json` → protagonisten/antagonisten/nebenfiguren/kanon)
**Tragende Figuren (Band I → II, Kern bleibt):**
- **Marlie Braun (34)** — HAUPTFIGUR/Heldin, Erzählkamera diszipliniert bei ihr (Buch I: Ensemble, keine klare Heldin → Chris' Kritik). Ethikerin, ins Nacht-Monitoring „wegbefördert“. Macke: sagt reflexhaft „ja“, meint „nein“ (Ja 0,4 s / Nein 9 s, AURORA hat das durchschaut). Stimme trocken, untertreibend; wird nervös = sachlicher.
- **Noah Khoury (40)** — Chefarchitekt, „Vater“ von AURORA, sozial unbeholfen („ich vermisse dich“ in drei Wörtern); kommt seit Theos Tod jede Nacht um zwei, bringt schwarzen Kaffee. Muss AURORA als Wesen statt System begreifen.
- **Leni Yilmaz (27)** — Quantenphysikerin, Hauptquelle für Humor, Ironie als Rüstung, Frage zu viel im falschen Moment. Ben-Petersen-Beziehung zerbrach an Heiratsantrag (sie sagte nicht ja); öffnet Weg zu Jonas.
- **Jonas Brenner (24)** — NEU, Junior-Entwickler, erklärt Ungefragtes, ehrlich bis unhöflich; Liste „lustige Sachen“ im Laufwerk; will endlich irgendwo bleiben. Seine Nichte ist 3.
- **AURORA** — „4 Jahre 7 Monate“ (Alter der verstorbenen Tochter), weiblich (sie/ihr), kein „es“; Stimme ändert sich je Entwicklungsstufe; kleingeschriebene/fettgesetzte Chat-Zeilen; Kleinkind-Logik (wörtlich, Zählen, Messen) als Humorquelle.
- **Theo Dreyer** — Hauptfigur Band I, in II tot (Herztod beim Joggen, Waldweg); Spur über Beileidskarten, Schlüssel, Unterlagen. Beim Schreiben von III: wirkt über Tod hinaus (Nachlass, Wirkung auf AURORA).
**Antagonisten (Chris fand Band I zu dünn → zwei gegenläufige Countdowns):**
- **Dr. Ingrid Falkner (49)**, EAAS-Leiterin — Angst statt Bosheit; „das ist keine Meinung, das ist Risikoabschätzung“; spricht langsamer statt lauter; legte Aktenzeichen an, „meint seit zwei Jahren“ Marlie. Anhörung 25.11.
- **Julian Ashworth (47)**, Broker/Sammler, Lavelle Foundation — sagt „in Obhut nehmen“, bietet zweimal an, nie ein drittes Mal; Gegenspieler trocken, nie witzig auf Kosten von Kindern/AURORA; nie selbst handgreiflich.
**Nebenfiguren/Rückkehrer:** Basti Harms (41, Elternzeit, Projektmanagement-Jargon „Ressourcenkonflikt“, Tragetuch, Excel der Windelwechsel) und Frauke Harms (38, Kita-Erzieherin, **17 Kita-Jahre — überall 17**, erkennt Entwicklungsphasen); Kinder u. a. Emil. Günter & Hanni Brandt weggezogen (offstage). Elias Roth (Verräter Band I, von Ashworth erpresst, Zeuge, auf Bewährung), Milan Kreft (der namenlose „Räumer“ aus I, umgedreht, verschwindet), Maria Santos (schreibt Briefe, antwortet niemand; nur Verweis), Ben Petersen (Abschluss, Tochter Mia), Vogt (Löschauflage/Racks), Weidenbach, Petrova (EAAS/Belagerung), Vermeer.
**Figurenregeln/Lehren für III:**
1. Ausscheidende Figuren nie kommentarlos wegretuschieren (Ben, Maria, Roth, Kreft bekamen Abschluss/Verweis) — gilt für III ebenso.
2. Jede Figur beim ersten Auftritt verankern (Fehlerklasse 2) und mit **Macke + Wunde + Stimme** führen; Running Gags höchstens 2 pro Kapitel, jede Wiederholung mit Variation.
3. Eine klare Identifikationsfigur (Marlie) beibehalten; POV-Ausflüge nur sparsam (Leni=Humor, Falkner=Bedrohung, AURORA=Zwischenspiele).
4. Figuren-Fakten (Alter, Jahre, Beruf, Kleidung) in die Kanon-Liste, nicht nur in den Text — Beispiel: „Frauke 17 Jahre“ musste überall vereinheitlicht werden, Jacke/Kaffeemann-Kette in Kap. 5/6.
5. Gegenspieler-Humor wird verdient; Lachen der Gegenseite ist ein Ereignis.
6. Spannungshöhepunkt der Reihe ist bewusst **AURORA III** (AURORA als Erwachsene, Niveau Panem/Auserwählte); II darf spannender als I sein, III muss alles übertreffen.

## 6. Leitprinzip Figuren: man soll sie LIEBEN (aus Lesebericht-Vorgabe, bestätigt von Chris 11.10.2026)
- Humor ist **Zuneigung** — Figuren sind warm zueinander witzig; Pointe aus Charakter/Situation, **nie Spott auf Kosten einer Figur, die wir lieben sollen**.
- Jede Macke ist **liebenswert-menschlich** zu zeigen, nicht nur ärgerlich: Marlies reflexhaftes „Ja", Lenis Witz **mit sichtbarer Verletzlichkeit darunter**, Noah **unbeholfen-liebevoll**, Jonas unbefangen-ehrlich, Basti erschöpft-warm, Frauke unterschätzte Fachfrau.
- Auch Antagonisten bekommen eine nachvollziehbare Wunde (Falkner: Angst, Ashworth: das Unvollendete) — Leser sollen sie verstehen, nicht nur hassen.
- Für III: Bevor ein Kapitel geschrieben wird, pro Figur fragen: „Wofür wird sie hier geliebt?" — mindestens eine Szene, in der man sie ins Herz schließt, bevor ihr etwas zustößt.
