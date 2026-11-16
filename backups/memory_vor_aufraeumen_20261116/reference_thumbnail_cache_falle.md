---
name: reference-thumbnail-cache-falle
description: Windows Explorer zeigt beim Cover-Ersetzen (gleicher Dateiname) ein veraltetes Vorschaubild — Falle bei DistroKid/KDP-Uploads
metadata: 
  node_type: memory
  type: reference
  originSessionId: d29d64d4-5d32-4c20-ac78-927be5a18973
---

# Windows-Thumbnail-Cache-Falle bei Cover-Updates

**Symptom (02.07.2026, „Läuft, Sommer!"-Cover):** Explorer-Vorschau zeigte das ALTE Cover (3-beinige Marathon-Sonne), obwohl die Datei längst das neue (Strand-Läufer) enthielt. Beim Doppelklick in der Foto-App erschien das richtige Bild. Verifiziert: Original und Chris' Kopie waren **byte-identisch** (1.575.530 B) — die Datei war immer korrekt.

**Ursache:** Windows Explorer-**Thumbnail-Cache** (thumbcache). Wird eine Bilddatei durch eine neue mit **gleichem Namen** ersetzt, behält Explorer oft das alte Miniaturbild. Betrifft NICHT den Datei-Inhalt (Upload ist korrekt), nur die Vorschau. OneDrive kann's verlängern.

**How to apply:**
- Explorer-Vorschau bei ersetzten Covern **nicht trauen** — im Zweifel per Foto-App öffnen (zeigt echten Inhalt) oder Dateigröße/Datum vergleichen.
- Chris' bewährter Fix: **Kopie erstellen** (neuer Name, z.B. `-1.jpg`) → frisches Thumbnail → passt. Diese Kopie dann hochladen.
- Alternativ Thumbnail-Cache leeren (Datenträgerbereinigung → Miniaturansichten) — meist unnötig.
- **Sauberste Prävention:** neues Cover mit **neuem Dateinamen** speichern statt gleichnamig überschreiben.

Betrifft alle Cover-Updates: DistroKid ([[project_distrokid_desktop_staging]]), KDP, Aimor. Siehe auch [[feedback_bildgenerierung]].
