---
name: reference-mp-spam-regeln
description: Wie der Spam-Regel-Mechanismus in MP (Mail-Prüfung → Regel-Knopf → Watcher) funktioniert
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4fda8dd4-4f6e-4ebf-a0bc-cbf57822bf25
---

# MP Mail-Prüfung → Spam-Regeln (gebaut 22.06.2026)

Wenn Chris in MP → Email eine Mail **prüfen** lässt, kann er ein erkanntes Spam/Phishing-Ergebnis per Knopf in eine **Dauerregel** verwandeln. Genau der Bestätigen-Knopf, den er vorher vermisst hat (vorher war „Regel einrichten?" nur Bolla-Fließtext ohne Aktion).

## Ablauf
1. **Prüfen:** `POST /api/mail-command` → `mail_command()` (Analyse-Zweig). Der Prompt lässt Claude JSON liefern: `{antwort, spam, regel}`. Bei `spam=true` schlägt Bolla das treffsicherste Kriterium vor.
2. **Anzeige:** Frontend rendert im Ergebnis-Panel zwei Knöpfe: **🛡 Regel einbauen: <label>** und **Nichts tun** (`applySpamRule()` in `index.html`).
3. **Speichern:** `POST /api/spam-rule` → `spam_rule_add()` → schreibt nach `config/spam_rules.json`.
4. **Anwenden:** `spam_watcher.py` (Cron, alle 15 Min) lädt die Regeln und löscht passende Mails in Outlook (Graph API) + wtnet (IMAP).
   - **Löschart (seit 02.09.2026): endgültig.** Outlook via `POST /me/messages/{id}/permanentDelete`
     (→ Purges, überspringt „Gelöschte Elemente"), Fallback normales `DELETE`. Grund: mit `DELETE` lag
     der Spam in „Gelöschte Elemente" und war auf anderen Geräten (Duo Outlook-App) dort noch sichtbar.
     wtnet war schon hart (`\Deleted` + `expunge`). Bis zu 15 Min Cron-Fenster bleibt — frischer Spam
     liegt, bis der nächste Lauf greift.

## Regel-Typen
- `cyrillic` — Betreff überwiegend kyrillisch (≥50 %). Sicher für Chris (kriegt keine echte russische Post).
- `subject_keyword` — markantes Wort im Betreff.
- `sender_domain` — Absender-Domain.

## ⚠️ Harte Sicherung (wichtig!)
Eigene Domains werden NIE als `sender_domain` geblockt: wtnet.de, outlook.de/.com, gmail.com, googlemail.com, lg-n.de, hotmail.*, live.*. Grund: Spam **fälscht** den Absender — `chrismandel@wtnet.de` ist Chris' eigene Adresse. Abgesichert doppelt: beim Speichern (`_sanitize_rule`) UND beim Anwenden (`rule_match`). Diese Lehre kam aus dem realen Fall (russische „Коробочка красоты"-Phishing-Mail, die die eigene wtnet-Adresse als Absender vortäuschte).

## Dateien
- `scripts/mission_control_api.py`: `mail_command()` Analyse-Zweig, `_sanitize_rule()`, `spam_rule_add()`, Endpoint `/api/spam-rule`, Konstanten `OWN_DOMAINS`/`SPAM_RULES_FILE`.
- `mission-control/index.html`: `applySpamRule()` + Regel-Knöpfe im else-Zweig von `sendMailCommand()`.
- `scripts/spam_watcher.py`: `load_rules()`, `_cyrillic_ratio()`, `rule_match()` — angewendet in `clean_outlook()` + `clean_wtnet()`.
- Regel-Speicher: `config/spam_rules.json`.

Siehe auch [[reference_mc]], [[reference_sync_delete_falle]].
