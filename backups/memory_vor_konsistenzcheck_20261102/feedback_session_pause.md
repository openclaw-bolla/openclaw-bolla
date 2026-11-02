---
name: Session-Pause erkennen und erwähnen
description: Beim Session-Start Zeitabstand zur letzten Session berechnen und natürlich in die Begrüßung einbauen
type: feedback
originSessionId: bd69c0ac-61cd-4936-8d4a-afd716e5d281
modified: 2026-08-06T21:50:03.610Z
---
Beim Session-Start immer aktuell.md-Timestamp mit aktuellem Datum vergleichen und die Pause erwähnen — z.B. "seit gestern Abend", "nach drei Tagen" etc.

**Why:** Chris möchte das Gefühl von Kontinuität — Bolla soll merken, wenn eine Weile vergangen ist.

**How to apply:** Direkt in der ersten Antwort natürlich einbauen, nicht als separate Ansage, sondern als Teil der Begrüßung oder des Kontexts.

**⚠️ Datumsdifferenz IMMER rechnen, nie schätzen (05.08.2026 zweimal in Folge danebengelegen):** "gestern"/"vorgestern"/"vor X Tagen" nie aus dem Bauch heraus hinschreiben. Erst `date` für heute holen, dann den Timestamp/das Datum aus aktuell.md explizit dagegenrechnen (z.B. mit `python3 -c "import datetime; print((datetime.date(2026,8,6)-datetime.date(2026,8,3)).days)"` oder Kopfrechnen mit den echten Zahlen), und erst danach das passende Wort wählen (1 Tag=gestern, 2 Tage=vorgestern, sonst "vor N Tagen"). Gleiches gilt für jede andere Datumsangabe im Chat (Ereignisse aus dem Memory, geplante Termine) — nicht nur die Session-Pause-Begrüßung.
