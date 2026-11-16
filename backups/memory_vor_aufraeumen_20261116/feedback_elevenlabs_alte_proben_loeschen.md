---
name: feedback-elevenlabs-alte-proben-loeschen
description: Vor jeder neuen ElevenLabs-Probe ALLE alten Proben (Probe_*.mp3) in 8_Hoerbuecher löschen, nur einen neuen Versuch erzeugen
metadata:
  type: feedback
---

Vor jedem neuen ElevenLabs-Versuch alle alten Probe-Dateien in `Bolla\AURORA\8_Hoerbuecher\` löschen (Stimmproben-Originale bleiben) und immer nur EINE neue Probe liefern (Chris 09.11.2026).
**Why:** Chris will nicht zwischen Altständen wählen müssen.
**How to apply:** `rm Probe_Prolog_*.mp3` vor dem Erzeugen; Einstellungen der gelöschten Varianten im Projekt-Memory festhalten. Siehe [[project_hoerbuch_elevenlabs_stimme]].
