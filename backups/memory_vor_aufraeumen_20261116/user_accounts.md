---
name: Chris Accounts & Login-Emails
description: Welche E-Mail-Adresse Chris wo nutzt — wichtig um Verwechslungen zu vermeiden
type: user
originSessionId: 8984efab-50e2-453a-b2d6-950c3dceec55
modified: 2026-08-21T15:32:58.352Z
---
## Anthropic / Claude Code Login
- **Aktuell:** chrismandel13@gmail.com
- **Pending:** Chris hat Support kontaktiert um die E-Mail zu ändern (Stand 16.04.2026) — Zieladresse noch nicht bekannt

## Standard-Absender für E-Mails
- ernstmandel@outlook.de (Microsoft 365 / Outlook) — Standard für alle E-Mail-Aktionen

## Weitere Konten
- chrismandel13@gmail.com — Gmail, Google Calendar, Anthropic-Login
  Auch das **Google-Konto des P20** (WhatsApp-Chat-Backup läuft in dessen Google Drive) und Chris' Google-One-Abo: **100 GB** (Stand 11.09.2026: 15 GB belegt). Details: [[project_pixel8_p20_ersatz]]
- chrismandel@wtnet.de — wtnet Mail (Spam-Watcher)
- ernstmandel@outlook.de — Outlook, OneDrive, Azure, Cloudflare. ⚠️ **Bezahltes M365-Abo inkl. Copilot** (Chris: "meine stärkste Waffe", 21.08.2026) — KEIN kostenloses/normales privates MS-Konto. Nicht als Stand-in für die kostenlose Consumer-Copilot-Erfahrung nutzen/empfehlen (z.B. beim Testen, was Schüler mit einem frisch angelegten Gratis-Konto sehen würden) — das würde die bezahlte, vollausgestattete Erfahrung zeigen statt der freien.
- renatemandel@outlook.de — Renates eigenes, separates Postfach; seit 08.07.2026 Booking.com-Konto darauf umgestellt. Bolla hat seit 08.07. **vollen Zugriff analog zu Chris' eigenem Konto**: Mail lesen/schreiben/senden, Kalender, Kontakte, Tasks (Scope wie `outlook_token.json`). Token `config/renate_outlook_token.json`, eigener Login via `scripts/renate_outlook_reauth.py` (einmalig, danach automatischer Refresh — NICHT dasselbe Konto/Token wie ernstmandel@outlook.de). `scripts/booking_watcher.py` scannt seither beide Postfächer.
