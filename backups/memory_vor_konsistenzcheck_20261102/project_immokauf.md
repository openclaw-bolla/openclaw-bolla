---
name: project-immokauf
description: "Immobilienkauf Bayern — Suchzeitraum, Regionen, Kriterien, Makler-Tracker in MC"
metadata: 
  node_type: memory
  type: project
  originSessionId: 32bacff7-d218-4c71-871f-c0cca465ccd2
  modified: 2026-07-23T13:01:06.578Z
---

# Immobilienkauf Bayern

**Käufer: Chris & Renate Mandel** — Kontakt: ernstmandel@outlook.de
**Suchstart: frühestens Herbst 2027 — evtl. erst Herbst 2028** (Chris überlegt, noch ein Jahr zu arbeiten; Stand 14.10.2026)

**Why:** Chris und Renate sind Anfang 60, Rentner. Der Kauf ist langfristig geplant, kein Stress.

**How to apply:** Keinen Druck machen, keine "jetzt handeln"-Empfehlungen. Bei Makler-Kontakten immer "Voranfrage / Interessentenliste" als Framing nutzen.

## Regionen
- Ammersee (Herrsching, Dießen) — Wunschregion
- Starnberger See / Starnberg
- Landsberg am Lech
- Weilheim in Oberbayern
- Fürstenfeldbruck
- Gilching (Landkreis Starnberg)
- **Westliche Peripherie (Germering, Puchheim)** — nur äußerste Randlagen wegen Preisen, neu ab 28.05.2026

## ⚠️ Korrektur 14.10.2026: München-Stadt ist NICHT ausgeschlossen
München West/Mitte/Süd (Pasing, Aubing, Laim …) kommen in Frage, **wenn der Preis stimmt** (siehe Suchraum unten). Kriterium „Lage München West und Südwest“ ist jetzt **must** (Kernanforderung). „ca. 100 qm“ = **ohne Terrasse**. Makler-Mail-Vorlage entsprechend angepasst. Makler-Liste um München West/Süd erweitern (offen/in Arbeit).

**Suchraum (Chris, 14.10.2026, per Karte `workspace/config/immo_suchgebiet_karte.png`):** Westen/Süden von München (West+Südwest+Süd), Nord = A8. West = Lech-Linie (Augsburg-Süd · Landsberg · Schongau · Füssen), Süd = Alpen (Garmisch/Mittenwald), Ost = Unterhaching · Holzkirchen · Bad Tölz/Lenggries. Dazu München-Stadt nur West/Südwest-Viertel (Pasing …). ⛔ **NICHT** Memmingen/Kempten/Allgäu/Sonthofen (Chris: „Sonthofen auf keinen Fall“). Tochter Steffi wohnt in Kaufering.

## Top-Kriterien (must)
- Lage: SW/S von München südlich A8, Lech-Linie bis Alpen, Ost bis Bad Tölz/Holzkirchen/Unterhaching (Karte); München-Stadt nur West/Südwest-Viertel
- Ort mit Gesundheitszentrum / Fitness + Sauna
- Penthouse inkl. Terrasse Südlage
- ca. 100 qm
- **Aufzug = Pflicht** (Chris 14.10.2026: „dafür sind wir zu alt“)
- **⛔ Etagenwohnungen sind ein No-Go** (nur Penthouse/oberste Etage mit Terrasse); bei Makler-Angeboten sofort aussortieren
- **⛔ Terrasse muss GROSS sein (Chris 21.10.2026):** Esstisch für 6, Grill, 2 Sonnenliegen, ggf. Sitzecke — Sommer-Hauptaufenthaltsort. Balkon/überdachter Balkon/Loggia = K.O., keine Alternative. In makler_angebote_triage.py (Prompt: terrasse=J nur bei echter großer Terrasse) umgesetzt. Absagen: Lieb Peißenberg (nur überdachter Balkon), deltapro (kein Penthouse/keine Terrasse, Preis viel zu hoch).

## Makler-Tracker
- Datei: `~/workspace/data/makler_status.json`
- **Stand 14.10.2026: 66 Einträge, davon 19 „nicht_interessant“ (außerhalb Karten-Suchraum, in MP unter Filter „Aussortiert“, nicht in Statistik); 42 Mails versandt, 7 Feedback.** MP-Seite 14.10. aktualisiert (Backup workspace/backups/index_vor_immo_update_20261014.html).
- (älter) **34 Makler** (10.10.2026: 8 auf Chris' Wunsch nach Tiefenprüfung entfernt: Wagner Premium, 1000 Rosen, Schnellbögl&Franke, Spindler, ROWI, Stadler, Kachelriß, LBS Germering; Backup workspace/backups/makler_status_vor_entfernung_*). Vorher 42 in 10 Regionen (Stand 06.10.2026; +5 neu: Sedlmayr, Schnellbögl&Franke, Bayerische Seen, Simone Grau, Sparkasse Landsberg; Mantz+Lechraum am 07.10. auf Chris' Wunsch entfernt)
- Status-Workflow: neu → email_gesendet → feedback_erhalten → termin / interessant / nicht_interessant

## MC-Seite
- Nav: data-page="projekte" (Sidebar: 🏡 Immobilienkauf Bayern)
- HTML: `page-projekte` in index.html
- Kriterien: `~/workspace/config/immo_criteria.json` — seit 06.10.2026 UI: ✏️ bearbeiten, 🗑️ löschen, ➕ hinzufügen, Drag&Drop

## Offen: tiefere Makler-Prüfung
**Fest eingeplant: Samstag 10.10.2026, als ERSTER Block des Samstag-Ausreizens (danach AURORA II)** — [[feedback_limit_regeln]]. Ursprünglich "irgendwann" (Budget übrig, nichts Wichtigeres) (Sonnet/Haiku-Fork, Webseiten einzeln abrufen, E-Mails/Existenz/Kontaktdaten prüfen; Lücken: Simone Grau, Schnellbögl&Franke, Bayerische Seen ohne Mail; Krusemeyer, Stadler, Sparkasse-Gilching-Eintrag unklar). Gut für Samstag-Ausreizen. Nach Lauf `geprueft` in makler_status.json setzen.

## MP-Zeitstempel
Immobilien-Seite zeigt oben "🕒 Stand" (mtime Makler-Liste + Kriterien + Feld `geprueft`), API /api/makler liefert stand_makler/stand_kriterien.

## Mail-Sync automatisch (Chris 14.10.2026)
`scripts/makler_mail_sync.py`, Cron alle 30 Min (Log `logs/makler_mail_sync.log`, Job-Status /jobs „makler-mail-sync"): Antworten → Status `feedback_erhalten`; Rückläufer (Unzustellbar) → Adresse deaktiviert, rote Box in MP (`unzustellbar` in makler_status.json) und Mail nach Outlook `Ablage/Projekte/Immos 2027-28` verschoben. Chris: „Status immer automatisch". Versand von Mails/Antworten bleibt freigabepflichtig ([[feedback_mail_freigabe]]).

