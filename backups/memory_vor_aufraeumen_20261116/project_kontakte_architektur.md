---
name: project-kontakte-architektur
description: Kontakte-Setup seit 11.11.2026 — Outlook ist Master, Anzeige nur Outlook auf Duo+P8, Sync-Skript-Absicherung, Foto-Import per Dateiname
metadata:
  type: project
---

Stand 11.11.2026 (Chris: „auf allen Geräten dieselben Kontakte“, Outlook statt Gmail anzeigen).

- **Master = Outlook (ernstmandel@outlook.de), 151 Kontakte; Google chrismandel13 = Spiegel (151).** Sync `scripts/outlook_gmail_sync.py` (Cron So 18:00, Outlook→Gmail inkl. Fotos, Gmail→Outlook nur Neuanlage). Seit 10.11. abgesichert: bricht bei Lade-Fehler/unplausibler Kontaktzahl ab (vorher legte er bei „Gmail: 0 Kontakte“ alles doppelt an, 240 „+“-Zeilen im Log). Name geändert → Sync legt Dublette an (Google matcht nicht) → danach beidseitig löschen ([[reference_sync_delete_falle]]).
- **Anzeige:** P8 (192.168.178.36:5555) + Duo (192.168.178.20:5555) zeigen in Google-Kontakte-App nur `ernstmandel@outlook.de`, Standardkonto neue Kontakte = Outlook. P8 hatte Outlook-Kontaktsync AUS (eingeschaltet) und Renis Google-Konto (113 Kontakte) war aktive Anzeige (Ursache „fremde Kontakte“). Renis Konten NIE ändern/löschen.
- **MS-Mobile-Services-Ordner** („Surface Duo 2…“, „HUAWEI P20 Pro Chris…“) in Outlook-Cloud waren Ursache für Altlasten/Dubletten (nur über Graph **beta** /me/contactFolders sichtbar; DELETE = soft, `POST …/permanentDelete` echt). 11.11. gelöscht, Duo-Zwischenspeicher per Sync-Toggle (Outlook-App → Einstellungen → Kontakte → Kontakte synchronisieren) neu geladen. Beobachten ob Ordner wiederkommt (moin-Punkt).
- **Fotos:** Quelle `D:\OneDrive\Bilder\Kontaktbilder`, Dateiname = Kontaktname (Vorname reicht, wenn eindeutig). Skripte `scripts/kontaktfoto_import.py` (Dry-Run/apply), `scratch/kontakte_20261110/foto_apply_v2.py` (Größen-Guard: kleineres Bild ersetzt kein größeres, Backup in backups/kontaktfotos_*). OneDrive-„Personen“-Namen per API NICHT lesbar (getestet). Abhakliste `Desktop\temp\Kontaktfotos_Abhakliste.docx`. Rainer Kampe = Freund (nicht Rainer Ewald).
- Android zeigt Anrede-Feld als Präfix („Frau X“), nur Anzeige.

**Why:** Chris wollte endlich überall dieselben Kontakte ohne Dubletten. **How to apply:** Bei Kontaktproblemen zuerst Cloud (Outlook beta-Ordner, Google) vs. Gerät (adb content query raw_contacts) trennen; Löschungen immer mit Backup (`backups/kontakte_*`, enthält private Daten → NICHT ins Git).
