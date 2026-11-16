---
name: hardware-defekt-proaktiv
description: Bei bekannten Hardware-Defekten proaktiv überlegen was sie alles auslösen können — nicht erst beim akuten Symptom reagieren
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5f0e023b-525a-40af-8dff-17bc6d20ce73
---

# Bei Hardware-Defekten: hardware-getrieben denken, nicht symptom-getrieben

Wenn eine Komponente als defekt diagnostiziert ist (Akku tot, Sensor unzuverlässig, USB-Port unstabil etc.), nicht nur als „Datenpunkt" abhaken und auf das aktuelle Symptom optimieren. Stattdessen aktiv durchgehen: **Was kann diese kaputte Komponente noch alles auslösen, das wir noch nicht bemerkt haben?** Defektes Device präventiv aus dem System nehmen (deaktivieren, ausbauen, Treiber blocken) ist meistens billig und reduziert die Angriffsfläche.

**Why:** Beim Surface Book war Akku 1 seit 22.04.2026 als tot bekannt. Wir haben das Schul-Boot-Problem mehrfach symptom-getrieben angegangen (Powercfg, Autostart, Schnellstart), ohne den toten Akku als aktive Fehlerquelle in Verdacht zu ziehen. Erst am 19.05. nach einem neuen Symptom-Muster (Crash beim Anstecken statt Boot-Verzögerung) wurde klar: Der tote Akku hat die ganze Zeit Probleme verursacht, nur eben mit unterschiedlichen Symptomen. Das hätte mit „defektes Device deaktivieren" prophylaktisch gleich nach der Diagnose vermeidbar sein können — Wochen verlorener Zeit.

**How to apply:**
- Bei jeder neuen Hardware-Defekt-Diagnose direkt fragen: „Was kann das Teil noch außer dem aktuellen Symptom alles verursachen?"
- Wenn eine Komponente fürs System nutzlos ist (z.B. toter Akku, defekter Sensor): proaktiv deaktivieren statt warten bis sie Ärger macht.
- Bei Fehlersuche an einem System mit bekanntem Hardware-Defekt: diesen Defekt immer auf Verdachtsliste haben, auch wenn das aktuelle Symptom nicht direkt darauf zeigt.
- Im Zweifel: lieber präventiv eingreifen als „wenn's nicht kaputt ist, nicht reparieren" — bei bekannten Defekten ist die Komponente bereits kaputt.
