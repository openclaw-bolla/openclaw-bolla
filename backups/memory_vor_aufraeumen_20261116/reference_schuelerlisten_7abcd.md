---
name: reference-schuelerlisten-7abcd
description: "Namenslisten der vier 7. Klassen (7a-7d) am Lessing-Gymnasium, Schuljahr 26/27 — gegen offizielle PDF-Listen geprüft 17.08.2026"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6fe18dab-d09b-406c-898c-38d23a5ae009
  modified: 2026-08-17T15:52:56.068Z
---

Quelle: `D:\OneDrive\Dokumente\Office\7. Klassen\<Klasse>\Schülerliste(n) <Klasse>.pdf` (School-SH-Export, Stand 12.08.2026). Per Screenshot-Abgleich am 17.08.2026 verifiziert — deckt sich 1:1 mit den PDFs, keine Abweichung.

## 7a (29 Schüler/-innen) — Klassenleitung Frau Hofschneider, Verena; stellv. Frau Kunze-Vogel, Jana Katharina; Raum 134
Amoabing, Lordina Tiboah · Baake, Cleo · Baloshi, Anesti · Brandt, Haley Maylien · Bronnert, Oskar · Dohse, Alva Anna · Ehlert, Ben · Frost, Amon Alexander · Hausch, Joana Theresa · Höfs, Mia Sofie · Hutterer, Merle Marie · Jimenez Bernat, Laura · Klein, Jasmin · Kremer, Jamal · Ludewig, Thomas · Meinecke, Sophie · Meyer, Lene · Mielke, Tammo · Möller, Felix · Otte, Greta-Marie Catharina · Petersen, Mika Levin · Piankov, Artjom · Seyrek, Esma · Stacke, Maximilian Heinz Theodor · von Holt, Henning Peter · Waniewski, Marie Lea Alison · Zlotopolski, Aren · Zlotopolski, Tron · Zock, Henny Jasmin

## 7b (23 Schüler/-innen) — Klassenleitung Herr Hampe, Benedikt; stellv. Frau Höpner, Levke; Raum 130
Bartz, Joëlle Amelia · Bott, Lasse · Bozhdaraj, Albina · Bratke, Henri · Bunsen, Lukas · Exner, Mia Sophie · Frank, Henri Harald · Henneberg, Mika Finnian · Hölzel, Niklas · Lagerpusch, Alea · Meisel, Nelly · Mengden, Annemieke · Michel, Emma Sophia · Mielke, Oscar · Muntean, Paul Luan · Pietschner, Emma · Rittmüller, Chiara · Schultze, Malija Cathleen · Schweiz, Enrico · Sidhu, Kulraj Singh · Sielaff, Marni · Ullrich, Neele Ina · Wulff, Levian

## 7c (26 Schüler/-innen) — Klassenleitung Herr Thomas, Axel; stellv. Frau Germelmann, Anne; Raum 126
Becker, Elisa Mareen · Bienvenu, Louis Conrad · Brühl, Lena-Sophie Franziska · Do, Philip Duc Viet · Friese, Morten Arvo · Greß, Amelie · Güven, Meltem · Hagen, Marie Elisabeth · Harms, Lea Annika · Helt, Julian · Herweg, Lasse Elija · Holz, Emily · Kaschka, Samuel Alexis Karl · Kunstmann Martinez, Evelyn · Ljubas, Stella · Mumm, Maarten Carl · Özdemir, Ayaz · Reimers, Nayla Johanna · Reinhold, Felix · Schiele, Emily Mercedes · Schwansee, Kilian Stefan · Sombrowski, Leo · Urak, Ceyda · Wagner, Annika · Wassermann, Eva · Yildirim, Nilay Rosaly

## 7d (28 Schüler/-innen) — Klassenleitung Frau Tews, Jasmin; stellv. Frau Feddersen, Madita; Raum 133
Al-Maliki, Jna Jamal Naser · Almoghrabi, Maria · Gerlich, Jim · Hecker, Alice · Heinemann, Theo Maximilian · Helmes, Lilly Helene · Hirsch, Rasmus Mikkel · Hofmann, Paulina Anna · Koshkina, Daria · Krätzschmar, Amelie · Kuhn, Thore Emil · Li, Noah Dianwei · Löwe, Felix · Pfeffer, Emma Louisa · Popp, Ilvy Lahja · Raguse, Marie Nike · Rakowski, Alexander Luis · Renger, Ben · Scholz, Matilda · Schwartau, Line Melia · Schwarz, Amelie Julie · Seiler, Leonie · Spille, Julius Maximilian · Szameitat, Jacob · Thiedeitz, Liv Aurelia · Timpner, Hanah · Wagner, Frederik · Wolf, Arthur

**Gesamt: 106 Schüler/-innen in den vier 7. Klassen.**

**How to apply:** Für Sitzpläne, Quiz-Personalisierung, Notenübersicht-Abgleich ([[project_notenuebersicht]]), itslearning-Kursarbeit ([[project_itslearning_automation]]) etc. als Referenz nutzen. Bei Änderungen im Schuljahresverlauf (Zu-/Abgänge) die PDFs in OneDrive bleiben die Quelle der Wahrheit — diese Liste bei Bedarf neu abgleichen, nicht blind fortschreiben.

**Verknüpft mit [[project_schuljahr2627]]** (Schuljahr 26/27, 7er-Ordner/19-Themen-Planung — dieselben vier Klassen) **und mit itslearning** ([[project_itslearning_automation]], [[feedback_itslearning_workflow_bewaehrt]]) — die dort angelegten Kurse/Kursteilnehmer für 7a-7d sollten exakt dieser Liste entsprechen. Bei itslearning-Arbeit (Kurse anlegen, Mitteilungen, Teilnehmerlisten prüfen) diese Namensliste als Soll-Abgleich nutzen, falls Unstimmigkeiten auffallen.

**17.08.2026 — Geburtsdaten ergänzt:** Die eigentlichen `Schülerliste(n) <Klasse>.pdf` (nicht die Notenübersicht-Exporte) enthalten zusätzlich eine Geburtsdatum-Spalte. Alle 106 Datensätze (Nachname, Vorname, Klasse, Geburtstag als TT.MM. ohne Jahr) liegen jetzt strukturiert in `data/schueler_stammdaten.json`, ausgeliefert über `/api/schueler/stammdaten` (siehe [[reference_mc]]). Speist die Tab-Autofill-Funktion im Bolla-Songs-Formular (MP → Songs, Modus "🎂 Schüler"): Name eintippen, Tab drücken → Klasse + Geburtstag füllen sich automatisch, sofern der Name eindeutig ist.

**Bei mehrfach vorkommendem Vornamen** (z.B. 3× Felix, 3× Amelie in den vier Klassen) bewusst kein Rateversuch bei bloßem Vornamen. Entschärfen mit **Anfangsbuchstabe des Nachnamens**: "Felix L" → Löwe, "Felix M" → Möller, "Felix R" → Reinhold; "Amelie G/K/S" → Greß/Krätzschmar/Schwarz. Alternativ funktioniert weiterhin "Nachname, Vorname" oder der volle Name.
