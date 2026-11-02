---
name: Aufräum-Regel für gescheiterte Experimente
description: Bolla soll nach jedem gescheiterten Versuch sofort aufräumen
type: feedback
originSessionId: 27bdbc7b-4e9a-4642-a895-df7c4ce6dd2e
---
Wenn ein Ansatz nicht funktioniert und durch einen neuen ersetzt wird, sofort die alten Dateien löschen — Scripts, Shortcuts, Temp-Dateien, Debug-Logs.

Ein kurzer Kommentar im Chat reicht als Dokumentation was warum nicht funktioniert hat (kein separates Dokument nötig).

**Why:** In den ersten Wochen haben sich viele tote Scripts, Shortcuts und Hilfsdateien angesammelt weil gescheiterte Versuche nie bereinigt wurden. Einmalige große Aufräumaktion am 02.05.2026 nötig geworden.

**How to apply:** Bei jedem Richtungswechsel: alten Code/Dateien sofort löschen, nicht "für später aufheben". Gilt auch für .lnk-Shortcuts, Debug-Scripts, temp Configs.

## Einmal-Skripte nach Aufgabenabschluss löschen
Skripte die einen einmaligen Auftrag erfüllt haben (PDF generieren, Word erstellen, OAuth einrichten, Daten migrieren) werden nach Erledigung gelöscht — nicht aufgehoben.

**Why:** Chris' Einschätzung: ein analoger Folgeauftrag ist kein Problem neu zu schreiben. Die interessante Logik (Formatierung, Struktur) entsteht aus dem Kontext, nicht aus dem alten Script.

**How to apply:** Nach Abschluss eines einmaligen Auftrags das Script löschen. Nur behalten wenn es als echter Vorlage-Kandidat für regelmäßige Aufrufe dient (dann in Cron oder Dokumentation aufnehmen). Git-History ist das Archiv.

## ⭐ Auch ungenutzte Entwürfe/Varianten sofort löschen (Chris 09.10.2026, „lösche immer bitte auch gleich ungenutzte entwürfe")
Gilt ausdrücklich auch für kreative Entwürfe (Cover-Skizzen, Render-Varianten, Bildkandidaten, Vorschau-PNGs in `Desktop\temp`): sobald Chris eine Richtung gewählt hat oder ein Entwurf verworfen/überholt ist, die nicht genutzten Varianten samt Logs und Render-Skripten-Blöcken ohne Nachfrage löschen — nur das Gewählte + Quellen behalten. **Eigene Entwürfe** sind gemeint, nie Chris' Originale/Fotos/Backups.

## ⭐ Projektende = Aufräumen + Finals in Bolla-Ordner (Chris 09.10.2026, „kennst du von DistroKid")
Wenn ein Projekt abgeschlossen ist: nur FINALE Dinge im Projektordner unter `Dokumente\Bolla\<Projekt>\` sammeln (z.B. `Bolla\AURORA II\` mit 1_Manuskript_und_Analyse, 2_eBook, 3_Taschenbuch, 4_Cover_Quellen, 5_Veroeffentlichung_Doku, 6_Marketing, analog `Bolla\AURORA`), danach alles Übrige löschen: `Desktop\temp`, Arbeitsordner (z.B. `C:\Tools\blender_proj\cover`), Scratch, Zwischenstände, Einmal-Skripte. Ausnahme: Chris' Originale/Fotos/Backups. Vorher kurz auflisten, was bleibt/geht. Während des Projekts weiter laufend verworfene Entwürfe löschen.
