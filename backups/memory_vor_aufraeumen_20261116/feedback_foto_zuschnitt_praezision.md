---
name: feedback-foto-zuschnitt-praezision
description: Bei Foto-Zuschnitten fürs Drucken (10x15 etc.) pixelgenau mit Lineal-Overlay messen, nicht nur Vorschau anschauen
metadata:
  node_type: memory
  type: feedback
  originSessionId: current
  modified: 2026-07-19T18:57:25.462Z
---

Beim ersten Versuch, zwei Familienfotos für 10×15-Druck zuzuschneiden (19.07.2026), sind mir beim
Tübingen-Foto zwei Fehler in Folge passiert, bis der Zuschnitt wirklich saß.

**Why:** Ich hatte den Bildausschnitt nur in einer kleinen, skalierten Vorschau "mit dem Auge" beurteilt —
dabei einmal glatt alle Köpfe abgeschnitten (100+px-Fehler in der Vorschau nicht auffällig), und beim zweiten
Versuch die falsche x-Position einer Person gecheckt (zu weit rechts im Bild gesucht), wodurch der
Sicherheitsabstand am Kopf effektiv bei Null landete. Erst ein drittes Nachmessen mit sauberem Kontext-Crop
(ganze Person sichtbar) + Lineal-Overlay (rote Gitterlinien mit Pixel-Werten eingezeichnet) brachte die
korrekten Koordinaten.

**How to apply:**
- Bei JEDEM Foto-Zuschnitt, der gedruckt oder auf ein festes Seitenverhältnis gebracht wird: vor dem
  finalen Save ein Lineal-Overlay-Bild erzeugen (Gitterlinien alle 20-50px + Pixel-Werte per PIL ImageDraw)
  und daran exakt ablesen, wo Köpfe/Füße/wichtige Kanten wirklich liegen — NICHT nur die kompakte
  Vorschau anschauen.
- Vorher die x-Position der zu prüfenden Person mit einem Kontext-Crop bestätigen (ganze Person inkl.
  eindeutig erkennbarem Kleidungsstück sichtbar), sonst prüft man am Ende die falsche Bildstelle.
- Bei randlosem Fotodruck (z.B. HP "Randlos") zusätzlich einplanen, dass der Drucker selbst nochmal ~3-5mm
  Overscan wegschneidet — ein rechnerisch "genau passender" Zuschnitt reicht NICHT, es braucht spürbaren
  Sicherheitsabstand. Wenn der durch die Bildkomposition (Personen füllen fast die ganze Höhe) nicht
  reinpasst: Chris auf "Mit Rand" statt "Randlos" hinweisen statt zu riskieren, dass was abgeschnitten wird.
- Beim Überschreiben einer bereits gezeigten/exportierten Datei mit gleichem Namen an den Windows-Explorer-
  Thumbnail-Cache denken ([[reference_thumbnail_cache_falle]]) — im Zweifel neuen Dateinamen verwenden,
  damit Chris sicher die aktuelle Version sieht.
- ⚠️ **Aber: nicht mehrere Versionen liegen lassen!** Chris hat am 19.07.2026 explizit gesagt, dass ihn
  mehrere `_v2`/`_v3`-Dateien nebeneinander verwirren — er ist unsicher, welche die richtige ist. Diesmal
  hat der Vergleich zufällig geholfen (dadurch einen Helligkeits-Fehler entdeckt), aber das ist die
  Ausnahme, kein Muster. Regel: neuen Namen nur temporär für den Cache-Bypass nutzen, und sobald Chris
  eine Version bestätigt hat, ALLE älteren Stände sofort löschen und die finale Datei ohne Versions-Suffix
  ablegen (z.B. `Foto_10x15.jpg` statt `Foto_10x15_v3.jpg`) — am Ende soll pro Foto nur EINE Datei auf dem
  Desktop liegen.

**Reine Gamma-Aufhellung erzeugt Grauschleier:** Beim selben Foto (19.07.2026) nach dem Neu-Zuschnitt
versucht, "zu dunkel" durch stärkere Gamma-Kurve (1.6 statt 1.35) zu beheben — Ergebnis sah laut Chris
"wie ein grauer Schleier über dem Bild" aus, deutlich schlechter als die vorherige Version. Gamma-Kurven
heben Schatten/Mitten an, ohne die Weißen mitzuziehen → wirkt bei ohnehin schon hellem Himmel schnell flach
und ausgewaschen. **Fix:** moderates Gamma (~1.3-1.35) NICHT weiter hochdrehen, sondern zusätzlich Kontrast
(`ImageEnhance.Contrast`, Faktor ~1.15) und etwas Sättigung (`ImageEnhance.Color`, Faktor ~1.08) drauf —
das bringt Helligkeit zurück ohne den Grauschleier-Effekt. Bei "sieht flau/grau/ausgewaschen aus"-Feedback
künftig zuerst an fehlenden Kontrastausgleich denken, nicht einfach das Gamma weiter hochschrauben.

Verwandt: [[feature_aufpeppen]] (ähnliches Präzisionsthema bei Bild/Video-Zuschnitten).
