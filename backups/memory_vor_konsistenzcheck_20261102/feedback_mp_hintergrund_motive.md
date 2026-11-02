---
name: feedback-mp-hintergrund-motive
description: MP-Seiten-Hintergründe (lila Overlay-Treatment) brauchen hohen Kontrast/große Formen — keine teuren KI-Testbilder dafür
metadata:
  node_type: memory
  type: feedback
  originSessionId: ebe978dc-b29a-4e78-baa7-a6cecca3e3a8
---

Für thematische Seiten-Hintergründe in Mission Possible (MP) gilt: das Standard-Treatment ist ein **entsättigtes Foto + dunkler lila Verlauf** (`linear-gradient(rgba(15,6,24,0.55), rgba(30,10,50,0.50))`). Dieser Filter frisst feine Details und niedrigen Kontrast — nur große, klare Formen/Silhouetten bleiben erkennbar, egal ob Foto oder KI-generierte Grafik.

**Why:** Zwei getrennte Fehlversuche haben das bestätigt:
1. **23.06.2026 (Opus 4.8):** Versuch, per MAI-Image (Azure, ~0,10 €/Bild) ein KI-generiertes Musik-Motiv für die Bolla-Songs-Seite zu erzeugen (Klaviertasten-Häuserzeilen, Notenlinien-Muster). Jedes Rohbild sah für sich gut aus, aber nach dem lila Overlay "schluckte das Treatment das Thema" — dreimal in Folge unbrauchbar, jedes Mal echtes Geld verbrannt. Chris brach ab: "alles Müll, kostet mich unnötig viel Geld."
2. **10.07.2026 (Fable, general-purpose Agent):** Beim Einbau von 8 Seiten-Themen wurde für "Bolla Songs" ein reales, aber extrem dunkles DJ-Pult-Makrofoto gewählt — technisch korrekt verifiziert (Bild lädt, zeigt tatsächlich Musik-Equipment), aber im fertigen Seitenkontext (klein, von Karten verdeckt, zusätzlich abgedunkelt) nicht mehr als "Musik" erkennbar. Der Agent hatte das Rohfoto beurteilt, nicht das fertige Ergebnis im echten Layout.

Beide Male derselbe Kernfehler: das Motiv wurde isoliert bewertet, nicht im tatsächlichen MP-Kontext (klein, teilverdeckt, abgedunkelt).

**How to apply:**
- Für neue Themen-Hintergründe in MP: **kostenlose, existierende Stock-Fotos** (z.B. Unsplash) nehmen, nicht kostenpflichtig KI-generieren — freies, beliebig oft wiederholbares Durchprobieren schlägt teure Einzelversuche.
- Motiv-Kriterium: **großformatige, hochkontrastige Silhouette/Lichtquelle** (z.B. ein einzelnes Mikro im Scheinwerferkegel, eine ganze Bühnenszene) statt fein gezeichneter Details oder dunkler Makro-Nahaufnahmen.
- Vor dem finalen Einbau nicht nur die URL/das Rohbild prüfen, sondern gedanklich (oder tatsächlich) simulieren: klein, mit Karten überlagert, durch den lila Filter gedämpft — würde man das Motiv dann noch erkennen?
- Verwandt: [[project_mai_image2]] (MAI-Image-Setup), heutiger Fix in `aktuell.md`.
