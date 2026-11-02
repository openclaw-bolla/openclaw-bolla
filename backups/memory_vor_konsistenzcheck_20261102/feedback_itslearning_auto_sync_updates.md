---
name: feedback-itslearning-auto-sync-updates
description: "Wenn ein Handout (PDF/HTML), das schon live als Ressource in itslearning-Kursen liegt, lokal aktualisiert wird -> automatisch auch dort nachziehen, ohne dass Chris extra danach fragen muss"
metadata:
  node_type: memory
  type: feedback
  originSessionId: unknown
  modified: 2026-08-25T09:17:40.064Z
---

Sobald ich eine Datei im `Handouts`-Ordner (z.B. `/mnt/d/OneDrive/Dokumente/Office/7. Klassen/Handouts/Praktikum/`)
inhaltlich ändere, IMMER kurz prüfen, ob genau diese Datei (per Basename) schon als Ressource in einem oder
mehreren itslearning-Kursen live liegt (siehe [[project_itslearning_automation]] für Skripte/Kurs-IDs/
State-Dateien wie `itslearning_kurstag2_freigabe_montag_reminder_state.json`). Falls ja: proaktiv anbieten
bzw. (nach der üblichen Freigabe für Live-Schreibaktionen, [[feedback_website_schreibzugriff]]) die
aktualisierte Version dort nachziehen — nicht warten, bis Chris von sich aus fragt "hast du das auch
upgedatet?".

**Warum:** Chris hat das am 25.08.2026 explizit so gewünscht, nachdem ich eine Elterninfo-HTML lokal
gefixt hatte, ohne von mir aus zu erwähnen, dass dieselbe Datei schon in 4 itslearning-Kursen als Ressource
hängt (Kurstag-2-Paket, hochgeladen 24.08.2026). Erst auf Nachfrage kam raus, dass dort noch die alte Version
lag.

**How to apply:** Gilt für jede Datei aus dem Handouts-Workflow (PDF/HTML), nicht nur die Elterninfo. Vor
dem "fertig, hier ist die aktualisierte Datei"-Melden immer kurz gegenchecken (grep über die
`itslearning_post_*`/`itslearning_prep_*`-Skripte nach dem Basename, oder die State-Dateien in
`config/itslearning_*state.json`), ob eine Live-Kopie existiert. **Vorsicht beim eigentlichen Ersetzen:**
Wenn die Ressource schon an eine veröffentlichte Mitteilung angehängt ist, kann simples
Löschen+Neu-Hochladen (Muster `delete_stale_pdf`/`upload_files` in
`itslearning_post_kurstag2_live.py`) den bestehenden Anhang-Link in der alten Mitteilung kaputt machen —
vor dem Löschen prüfen, ob itslearning eine direkte "Datei ersetzen"-Option auf der Ressourcen-Zeile bietet,
die die Resource-ID/den Link erhält.
