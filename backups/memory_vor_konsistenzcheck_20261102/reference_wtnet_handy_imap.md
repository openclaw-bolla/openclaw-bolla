---
name: reference-wtnet-handy-imap
description: wtnet-Konto am Handy (Outlook-App) als IMAP einrichten — Serverwerte; POP3 war Ursache für Geister-Spam am Duo
metadata:
  type: reference
---

Seit 05.10.2026: wtnet-Konto (chrismandel@wtnet.de) am Duo und Pixel 8 war als **POP3** eingerichtet → lokale Kopien bleiben, serverseitige Spam-Löschung (spam_watcher.py) kommt nie an. Umstellung auf IMAP beschlossen.

**Werte (von Chris bestätigt):** IMAP `mail.wtnet.de` Port 993 SSL/TLS · SMTP `mail.wtnet.de` Port **465 SSL/TLS** (NICHT 587/STARTTLS, obwohl wtnet_config.json 587 enthält) · Benutzername = volle Adresse.

**How to apply:** Bei Handy-Mail-Fragen zu wtnet immer IMAP + SMTP 465 nennen. Passwort nie im Chat. Siehe [[reference_mp_spam_regeln]].
