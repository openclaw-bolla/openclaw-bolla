---
name: reference_outlook_ordnerstruktur
description: "Chris' persönliche Outlook-Ablagestruktur (Ablage/Privat/Probleme etc.) — beim Archivieren/Einsortieren von Mails nutzen, nicht den Standard-\"Archiv\"-Ordner"
metadata: 
  node_type: memory
  type: reference
  originSessionId: ca2bc5ed-99fe-427e-ac96-7b2275407d7f
---

Chris hat in Outlook (ernstmandel@outlook.de) eine eigene Ordnerstruktur unter **Ablage** — NICHT der Standard-"Archiv"-Ordner von Outlook (der ist quasi ungenutzt). Beim "archivier das mal" IMMER hier einsortieren, nicht in den Systemordner "Archiv".

## Struktur (Stand 07.07.2026)
- **Ablage**
  - **Archiv** (eigener Unterordner, nicht der Systemordner!)
    - Amazon — Amazon-bezogene Streitfälle/Belege (z.B. Founderholics-Kieselerde gehört thematisch eigentlich hierhin, Chris wollte es aber in Probleme)
    - Career
    - Kinder
    - Schule (hat 10 weitere Unterordner)
  - **Privat**
    - eBay, Einkäufe, Events 2025, Events 2026, Fun, Gesundheit, Grüße, Kurse - AGs, **Probleme** (allgemeine Streitfälle/Ärger, z.B. Amazon-Mahnungen), Rechnungen, Registrierungen, Reni, Steuer, Studium, Support, Urlaub 2026, Versicherungen, Zertifizierungen-Serials
  - **Projekte**
    - Arthose, Augen, eBooks, Immobilien, Mandel-Tonsille, Renovierungen, Tickets, ToDos, Wärmepumpe/PV, Wohnen Ulm

## Praktische Hinweise
- Ordner-IDs sind lang und wechseln nicht — bei Bedarf per Graph API `GET /me/mailFolders` (+ `/childFolders`) neu auflösen, nicht hart im Code speichern (Text hier reicht als Gedächtnisstütze für die Namen/Pfade).
- Wenn unklar, wo eine Mail hingehört (z.B. Amazon-Ärger könnte in Ablage/Archiv/Amazon ODER Ablage/Privat/Probleme passen) — kurz nachfragen statt raten, Chris hat klare Vorstellungen davon.
- Verschieben via Graph API: `POST /me/messages/{id}/move` mit `{"destinationId": "<folderId>"}`.
