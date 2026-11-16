---
name: OneDrive Foto-Organisation
description: Wie Fotos von den Handys in OneDrive landen und wo aufgeräumt werden soll
type: project
originSessionId: 27bdbc7b-4e9a-4642-a895-df7c4ce6dd2e
modified: 2026-08-23T17:52:09.566Z
---
## Foto-Eingang: alles landet in einem Ordner

Beide Huawei-Handys (Duo + P20) haben in der **OneDrive-App** folgendes eingestellt:
- Zielordner: **`OneDrive/Bilder/Eigene Aufnahmen/`**
- Geräteordner aktiv: Camera, Screenshots, BeReal, DCIM

**Ergebnis:** Alle Fotos, Screenshots, WhatsApp-Bilder und Videos landen automatisch in `Eigene Aufnahmen` — an einem einzigen Ort.

## Was NICHT gebraucht wird
- `Bilder/Kameraimporte/` → überflüssig, nur 3 einmalige USB-Import-Sessions (Okt/Nov 2025, Jan 2026), seitdem nichts mehr. Kann irgendwann gelöscht werden.

## Aufräum-Struktur (in Arbeit)
- `Eigene Aufnahmen/Sonstiges/` → 550 Dateien (alte unsortierte/unbenannte Fotos)
- `Eigene Aufnahmen/` direkt → noch 76 Dateien lose drin (noch nicht eingeordnet)
- `Eigene Aufnahmen_Backup/` → hat Unterordner: Familie, Reisen, Events, Natur, Renate, Robin

**Ziel:** Chris will regelmäßig (periodisch) aufgeräumt bekommen — ich darf das automatisieren sobald er das Chaos überblickt hat. **Erst wenn Chris grünes Licht gibt.**

**Why:** Alles an einem Ort macht Aufräumen und den Aimor-Push einfacher.
**How to apply:** Nie eigenmächtig Fotos verschieben oder löschen ohne explizite Freigabe.

## Stand 19.07.2026 — Größenordnung bestätigt, Chris will demnächst ran

Anlass: Chris suchte ein Foto (Anne+Bene+Robin+Reni+Chris zusammen) — Suche in den benannten Backup-Ordnern
(`Eigene Aufnahmen_Backup/Familie` + `.../Events und Feiern`, ~140 Dateien mit beschreibenden Namen wie
`robin_und_anne_ausflug.jpg`) erfolglos, Bene taucht in keinem beschrifteten Dateinamen auf. Dabei aufgefallen:
die Namensbeschriftung reicht nur bis ca. 27.03.2026, danach nichts mehr einsortiert — `Eigene Aufnahmen/Familie`
und `.../Events und Feiern` (die "aktiven", nicht-Backup-Ordner) sind komplett LEER, Kategorisierung ist
offenbar mittendrin steckengeblieben. Ungesichtet/unsortiert zusätzlich: `WhatsApp Images` (2113 Dateien),
`Eigene Aufnahmen/` direkt (66 lose Dateien, IMG_*-Rohnamen ohne Beschriftung).

**Chris bestätigt (19.07.2026): Gesamtbestand >60.000 Fotos in OneDrive.** Explizit als **eigenes Projekt
gemerkt** — er sucht das aktuelle Foto erstmal selbst, aber „demnächst" soll das große Aufräumen + die
laufend neu ankommenden (noch unsortierten) Fotos angegangen werden. Kein Termin, kein grünes Licht für
automatisches Verschieben — nur als anstehendes Vorhaben notiert. Bei Gelegenheit anstupsen, nicht von
selbst loslegen. Verwandt: [[project_foto_analyse]] (KI-Suche existiert, aber `photo_analysis.json` ist
leer — noch nie ein Lauf gestartet).

## ✅ 23.08.2026 — OneDrive „Personen"-Gesichtserkennung ist bei Chris schon aktiv, Robin bereits getaggt

Bei der Kilimanjaro-Foto-Archivierung ([[project_handy_foto_zwischenablage]]) rausgekommen: **OneDrive Fotos hat
ein "Personen"-Feature** (automatische Gesichtserkennung über die ganze Bibliothek, lokal+Cloud, Rollout zuletzt
01.08.2026 aktualisiert) — bei Chris **läuft es bereits**, viele Personen sind schon benannt, u.a. Robin. Stammt
laut Chris vermutlich noch aus der alten Windows-10-„Fotos"-App (Legacy), die lokales Gesichts-Tagging konnte —
per Websuche bestätigt: Microsoft hat genau diese Funktion aus der neuen Windows-11-Fotos-App rausgenommen und
in die OneDrive-Cloud verlagert, alte Tags sind mitgewandert.

**Praktische Konsequenz für künftige Foto-Suchen:** Für "Fotos mit Person X" NICHT erst die lokale KI-Fotosuche
([[project_foto_analyse]], nur generische Bildbeschreibungen, keine Gesichtserkennung) vorschlagen — stattdessen
zuerst auf **OneDrive Fotos → Personen → [Name]** verweisen, das ist die eigentlich passende, bereits fertige
Lösung. Einschränkung: greift nur auf Fotos, die schon in OneDrive liegen (z.B. Chris' eigene Aufnahmen) — NICHT
auf Medien, die nur auf dem Handy in WhatsApp liegen und noch nicht archiviert wurden.

## Stand 26.07.2026 (Abend) — REMINDER: Chris ist "insgesamt unzufrieden", will Lösung erst zuhause angehen

Chris meldet sich unterwegs (Sommerreise, Hotel-WLAN) explizit unzufrieden mit der gesamten Foto-Situation
("blicke das nicht mehr wirklich"). Bewusste Entscheidung: das eigentliche Aufräumen/Neuordnen NICHT jetzt
im Hotel anpacken (WLAN zu instabil/unsicher für so ein größeres Vorhaben), sondern erst zuhause. Ich hab
ihm knapp den Überblick über alle Baustellen gespiegelt (dieses File + [[project_foto_analyse]] +
[[project_aimor]] + [[project_handy_foto_zwischenablage]]) und nichts weiter unternommen. **Nächster
Schritt: Chris meldet sich von zuhause aus proaktiv, was genau er als erstes angehen will — nicht von mir
aus vorschlagen, er will die Richtung selbst vorgeben.**
