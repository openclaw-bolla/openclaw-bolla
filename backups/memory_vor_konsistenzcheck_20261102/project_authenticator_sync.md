---
name: TODO Authenticator-Apps synchronisieren
description: Chris will seine verschiedenen Authenticator-Apps mit Bollas Hilfe synchronisieren / aufräumen
type: project
originSessionId: 1828fda4-f5f3-48d7-8c03-ccd309212618
---
Chris hat (Stand 2026-04-14) mehrere Authenticator-Apps im Einsatz und möchte deren TOTP-Einträge gemeinsam mit Bolla durchgehen, vereinheitlichen und synchron halten. Konkrete Apps und Konten noch nicht benannt — wenn das Thema aufkommt, zuerst auflisten was wo drin ist.

## MS Authenticator auf Surface Duo
- Cloud-Sicherung aktiviert ✓
- Wiederherstellungskonto: ernstmandel@outlook.de
- Ziel: Sync auf Huawei-Gerät (Modell noch unbekannt, Baujahr klären für Google-Play-Kompatibilität)

**Why:** Chris will Übersicht und vermeiden, dass ein 2FA-Eintrag nur in einer App existiert (Verlustrisiko). Er hat mich explizit gebeten, ihn an dieses TODO zu erinnern.

**How to apply:** Wenn 2FA / TOTP / Authenticator-Themen auftauchen, oder Chris nach offenen Aufgaben fragt — dieses TODO erwähnen. Bei der eigentlichen Synchronisation: vorsichtig (Secrets!), niemals TOTP-Secrets in Logs/Git/Chat ausgeben, immer chmod 600 für Speicherdateien.
