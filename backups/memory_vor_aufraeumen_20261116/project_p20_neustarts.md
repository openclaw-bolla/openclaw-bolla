---
name: project-p20-neustarts
description: "Huawei P20 startet zunehmend öfter neu — Google-Speicher voll (Robins Tansania-Fotos) als Hauptverdächtiger; Kameraimport enthält aber KEINE echten Tansania-Fotos, nur Thumbnail-Cache + Chris' eigene Fotos"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4147bd30-5a2c-439c-90ca-f120ba54ac2f
  modified: 2026-09-12T09:42:10.086Z
---

Chris' Huawei P20 (kein ADB, siehe [[user_devices]]) startet zunehmend öfter von selbst neu. Kein neuer
Akku gewünscht (Investition lohnt sich für Chris bei dem Alter des Geräts nicht mehr).

**Bereits durchgegangen/ausgeschlossen:**
- Bildschirmhelligkeit reduziert — keine Besserung
- Speicherplatz auf dem Gerät: 57% belegt, unauffällig
- Software-Updates: gibt es für das P20 nicht mehr (EOL)
- Safe Mode: Standard-Kombi (Einschalten + Lautstärke-leiser halten) hat bei Chris nicht funktioniert,
  Alternative (Power-Menü → "Ausschalten" lange gedrückt halten → Dialog "Neustart im abgesicherten Modus")
  mitgegeben, Ergebnis noch offen

**Chris' eigener Verdacht (plausibel):** Google-Speicherkontingent ist randvoll durch WhatsApp-Fotos/Videos,
die Robin aus Tansania schickt (laufende Famulatur, siehe [[user_robin]]) — ca. 400 Fotos+Videos. Ständig
scheiternde Google Fotos-Hintergrund-Backups könnten Dauerlast erzeugen und die Reboots auslösen.

**Bereits umgesetzt (26.08.2026 abends):**
- WhatsApp-Medien sind auf Android identisch mit den Galerie-Dateien (keine getrennte interne Kopie) —
  Chris hatte aber schon alle ~400 Tansania-Fotos/Videos auf Studio UND Duo angeschaut, damit existieren dort
  bereits unabhängige lokale Kopien
- P20 per USB auf "Dateiübertragung" umgestellt → OneDrive-Kamera-Import-Assistent sprang automatisch an
  und hat das **komplette Kamera-Album** (nicht nur Tansania) nach `D:\OneDrive\Bilder\Kameraimporte\2026-08-26\`
  gesichert: 9.155 Dateien — mehr als die 6.256 Elemente, die Chris in der Galerie danach auswählen konnte,
  also mit hoher Sicherheit vollständige Sicherung
- Extra-Ordner `D:\OneDrive\Bilder\Robin Tansania 2026\` existiert (bisher ungenutzt/leer, da der komplette
  Kameraimporte-Weg gereicht hat)
- Chris wollte beim Löschen zusätzlich "aus Cloud + allen synchronisierten Geräten löschen" anhaken
  (bestätigt: sinnvoll) und danach den Papierkorb (Google Fotos + Huawei-Galerie, ~30-60 Tage Aufbewahrung,
  zählt bis dahin weiter gegen das Kontingent) leeren, um sofort Platz freizugeben

**Offen:**
- Ob Löschen (inkl. Cloud-Haken) + Papierkorb-Leeren durchgelaufen ist
- Ob sich die Neustarts dadurch gebessert haben
- Falls nicht: Cache-Partition leeren (Recovery-Modus) und/oder Safe-Mode-Test nachholen als nächste Schritte

**⚠️ Wichtiger Fund (27.08.2026): Kameraimport enthält NICHT Robins Tansania-Fotos.**
Analyse von `D:\OneDrive\Bilder\Kameraimporte\2026-08-26\` (9.155 Dateien) per EXIF/ffprobe-Metadaten-Scan:
- **8.452 von 9.155 Dateien (93%)** sind reine 256×256-Thumbnails aus einem Cache-Ordner (nichtssagende
  Nummern wie `100000.jpg`) — keine echten Fotos, unbrauchbar.
- Die restlichen **~745 "echten" Fotos + 25 Videos** sind ausschließlich **Chris' eigene** Kamerafotos/
  Screenshots/Videos aus 2019–2026 (BeReal, Instagram, HP-Drucker, Auto-Screenshots etc.) — kein einziges
  Datum/Namensmuster (`IMG-2026....-WA...`) passt zu Robins Reisezeitraum (01.08.–08.09.2026).
- **Grund:** OneDrive-Kamera-Import zieht nur `DCIM/Camera` + Thumbnail-Cache des Handys, NICHT den
  WhatsApp-Medienordner (`WhatsApp/Media/WhatsApp Images` bzw. `.../WhatsApp Video`), wo Robins gesendete
  Fotos/Videos tatsächlich liegen. Die sind also gar nicht mit rübergekommen.
- Extra-Ordner `D:\OneDrive\Bilder\Robin Tansania 2026\` ist entsprechend weiterhin leer/ungenutzt.
- Scan-Script liegt (bei Bedarf) unter `/tmp/claude-1000/.../scratchpad/scan_exif.py` — session-gebunden,
  ggf. neu bauen (EXIF via PIL, Video-Datum via `ffprobe -show_entries format_tags=creation_time`).

**Chris' Anweisung 27.08.2026:** "Erstmal nichts machen, alles merken für später." Kameraimport-Ordner
bleibt unangetastet (nichts verschoben, nichts gelöscht). Gewünschtes Namensschema für später vermerkt:
bei echten Tansania-Dateien Format `Kili-Exp (1).jpg` / `Kili-Exp (2).mp4` (fortlaufend nummeriert, Endung
je nach Typ) statt EXIF-Datum-Namen.

**Nächster Schritt (wenn Chris zurückkommt):** Handy nochmal per USB/Dateiübertragung verbinden, dann
direkt in den WhatsApp-Medienordner auf dem Gerät navigieren und die echten Tansania-Bilder/Videos von
dort holen (nicht nochmal über den Kamera-Import-Assistenten, der greift nur DCIM ab).

**How to apply:** Chris hat ausdrücklich gebeten, das Thema **nicht von sich aus weiterzuverfolgen** — nicht
proaktiv nachhaken, sondern abwarten, bis er selbst wieder darauf zurückkommt. Dann hier anknüpfen statt neu
anzufangen.

**11.09.2026 — Google-Speicher-Theorie widerlegt.** Chris hat alle Tansania-Fotos gelöscht (Gerätespeicher
danach 59%, kaum verändert — Gerätespeicher war eh nie der Verdächtige). Entscheidend: Google One-Abo zeigt
**15 von 100 GB belegt** — Kontingent war nie auch nur annähernd voll. Die komplette „Google-Speicher voll →
Backup-Stress → Reboot"-Theorie ist damit vom Tisch. Papierkorb-Check erübrigt sich.

**Neue Beobachtung Chris (11.09.2026):** Reboots passieren wohl im Zusammenhang mit dem Laden — nach dem
Einschalten nach einer Ladephase fragt das Handy nach der SIM-PIN (= es war ein echter Kaltstart, kein
Aufwachen aus Standby). Pixel 8a-Kauf vermutlich abgeblasen ("werde ich vermutlich doch nicht kaufen") →
P20 bleibt länger im Einsatz, Ursache lohnt sich jetzt zu klären.

**Aktueller Verdacht:** Hardware statt Software — bei dem Alter (Android 9 EOL, alter Akku) naheliegend:
- Wackelkontakt Ladebuchse/Akku, der beim Laden kurz die Stromversorgung unterbricht → Kaltstart
- Degradierter Akku (Spannungseinbruch unter Last)

**Nächste Schritte (Chris führt selbst aus):**
1. **Sicherheitscheck:** Akkudeckel/Rückseite auf Wölbung prüfen (aufgeblähter Akku = Brandrisiko, nicht nur
   Software-Ärgernis)
2. **Lade-Beobachtungstest:** Handy entsperrt lassen, Kabel einstecken, zusehen ob es während des Ladens
   sichtbar durchbootet → bestätigt Wackelkontakt-Hardwarefehler
3. Falls beides unauffällig: Safe-Mode-Test von August nachholen (Alternative: Power-Menü → "Ausschalten"
   lange halten → Dialog "Neustart im abgesicherten Modus")

**Neue Beobachtung Chris (12.09.2026):** Reboots scheinen an Ein-/Ausschalten gekoppelt zu sein — wenn
das Handy eingeschaltet bleibt und er nur eine App startet (z.B. Wetter), passiert nichts. Stärkt die
Hardware-Theorie (Wackelkontakt Ladebuchse/Akku ODER ausgeleierter/klemmender Power-Knopf, der bei
alten Androids ab ~8-10 Sek. "gehalten" versehentlich einen Zwangsneustart auslöst), spricht eher gegen
Software/App-Crash als Ursache.

**Vorgeschlagener Unterscheidungstest:** Handy rein über Power-Knopf aus-/einschalten OHNE Ladekabel
(akkubetrieben). Reboot-Verhalten auch ohne Kabel → eher Power-Knopf. Nur im Zusammenhang mit Laden →
eher Ladebuchse/Akku-Kontakt. Zusätzlich: Gefühlscheck Power-Knopf (klemmend/schwergängig vs. Lautstärke-
tasten als Vergleich).

**Testergebnis Chris (12.09.2026): Power-Knopf-Theorie widerlegt.** 10× aus-/eingeschaltet rein über
Power-Knopf, ohne Ladekabel — kein einziger Reboot. Power-Knopf ist damit raus. Übrig bleibt die
Ladebuchse/Akku-Kontakt-Theorie (Wackelkontakt beim Laden).

**Nächster Schritt:** Beim Laden am Steckerwinkel wackeln/Bildschirm beobachten (Flackern = Wackelkontakt
live erwischt), und/oder anderes Kabel/Netzteil testen (schließt Kabel als Ursache aus vs. Buchse).

**How to apply:** Ergebnis von Chris' Checks abwarten, dann hier weitermachen. Nicht von selbst nachhaken,
außer Chris bringt es wieder auf.
