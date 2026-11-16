---
name: feedback-praktikum-header-bilder
description: "Praktikum-HTMLs (7. Klasse EDV) bekommen ein kleines Titelbild im Header — bewährtes Muster für Prompt+Technik, von Chris am 11.08.2026 abgesegnet"
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-08-11T15:05:13.903Z
---

Seit 11.08.2026 bekommt jede `NN-Praktikum.html` ([[feedback_prakt_anleitungen]]) standardmäßig ein kleines
thematisches Titelbild im Header (analog zu Chris' eigenen illustrierten PPT-Folien) — von Chris nach
mehreren Testrunden ausdrücklich abgesegnet ("Bilder sind jetzt ok, genauso in Zukunft").

**Bildquelle:** Pollinations.ai ([[feedback_bildgenerierung]]), kostenlos.

**Prompt-Lehren (aus mehreren fehlgeschlagenen Zwischenrunden):**
- **Nicht zu stark auf "Sticker/Chibi/Kawaii" vereinfachen** — das führte bei Mehrpersonen-Motiven dazu,
  dass das Modell nur noch EINE (oft abgeschnittene) Figur lieferte statt der gewünschten zwei, oder
  Kernelemente (z.B. das Einhorn-Horn) wegließ. Ein "cute cartoon/storybook illustration"-Stil mit klarer
  Anweisung "two full-body characters, both fully visible" funktioniert zuverlässiger für Duo-Motive.
- **Bei Charakteren explizit Kleidung vorschreiben** ("wearing colorful seashell bra tops", "fully clothed
  and child-appropriate") — ohne diese Vorgabe lieferte Pollinations bei manchen Seeds unbekleidete Figuren,
  für Schulmaterial natürlich ein No-Go, nicht nur ein Geschmacksfehler.
- **Bei Objekten (z.B. Ordner) "mascot"/"character"-Wortwahl vermeiden** — das lässt das Modell oft eine
  generische Anime-Figur statt des eigentlichen Objekts zeichnen. Besser: "a folder OBJECT with a simple
  cute face drawn on the front" + "no people, no animals, no other characters" explizit ausschließen.
- **Mehrere Seeds parallel ziehen und den saubersten nehmen** (wie bei Cover-Motiven, [[feedback_bildgenerierung]])
  — bei Bedarf 2-4 Kandidaten, dann den besten wählen statt beim ersten Treffer zu bleiben. Aber: **nicht
  endlos weiter-iterieren, wenn eine frühere Runde schon sauber war** — bei der Meerjungfrau/Einhorn-Illustration
  war der ALLERERSTE Versuch am Ende die beste Wahl, spätere "Verbesserungsversuche" wurden schlechter
  (Content-Probleme, Glitches). Im Zweifel zur bewährten früheren Variante zurück, statt stur weiter zu
  optimieren.

**Technische Einbindung (Format-Fix 11.08.2026):**
- **JPEG statt PNG einbetten** — quadratisch zuschneiden, auf ~260×260px runterskalieren (Pollinations liefert
  immer 768×768 unabhängig von den angeforderten Maßen, siehe [[feedback_bildgenerierung]]), leichtes
  UnsharpMask, Qualität ~82. Ergebnis: 6-15 KB statt 230-390 KB bei PNG mit Alpha-Kanal-Rundung — der
  Größen-Unterschied war Chris' Hauptkritik in der ersten Runde.
- **Rundung per CSS, nicht per Alpha-Maske:** `<img class="header-img" src="data:image/jpeg;base64,...">`
  mit CSS `.header-img { width:100px; height:100px; border-radius:16px; ... }` — `border-radius` rundet
  moderne Browser direkt am `<img>`-Element, kein Pillow-Alpha-Masking nötig.
  **Falle, die beim ersten Bau passiert ist:** Das `class="header-img"` muss WIRKLICH am `<img>`-Tag stehen
  — beim ersten Durchgang fehlte es (nur die CSS-Regel existierte), wodurch das Bild unskaliert/riesig
  gerendert wurde. Nach dem Einbau immer per `grep -o '<img class="header-img"'` verifizieren, dass die
  Klasse wirklich am Tag hängt.
- Header-Layout: `.header { display:flex; align-items:center; gap:18px; flex-wrap:wrap; }`, Bild links,
  `<h1>`+Zeit-Angabe rechts daneben in `.header-text { flex:1; min-width:180px; }`.

**How to apply:** Bei jedem neuen `NN-Praktikum.html`-Bau automatisch ein passendes Titelbild nach diesem
Muster generieren und einbauen — Chris muss das nicht mehr extra anstoßen, ist jetzt Standard für alle
künftigen Kurstage.
