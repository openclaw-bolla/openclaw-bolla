---
name: project-escooter-kauf
description: Chris will neuen E-Scooter; Muss-Kriterien Blinker vorn+hinten und Federung, Web-Check auf Zuruf
metadata:
  type: project
---

Chris überlegt (28.10.2026) einen neuen E-Scooter zu kaufen (Vorgänger ohne Federung/Blinker).

**Muss-Kriterien:** Blinker vorn UND hinten (Chris wundert sich, dass viele Modelle das trotz Pflicht nicht haben; Pflicht für Neuzulassungen laut scootervergleich.net ab März 2027), Federung vorn+hinten (künstliche Hüfte). Reichweite egal, nur zur Info.

**Why:** Gesundheit (Hüfte) und Gesetzeslage; Preis-Leistung zählt.

**How to apply:** Bei „moin" als Punkt in der Liste nennen (offene_punkte.json, id p_scooter). Web-Check nur auf Zuruf, dann Blinker-Position und Federung gegen Testseiten prüfen, nicht Händlerwerbung glauben. Stand 28.10.: 1. Xiaomi 6 Pro (419–499 €, Heckblinker nur Notebookcheck, 27 kg), 2. ePowerFun ePF-2 Pro 653 Wh (~680–820 €, alles belegt), 3. ePF-Pulse 960 (~1.250–1.450 €), 4. iScooter/Isinwheel T8 (~630 €, ABE unbelegt). Xiaomi 6 und 5 Max raus.

**Prüfregel (Chris 28.10.):** Beim Web-Check bei JEDEM nicht ganz sicheren Modell die Herstellerangaben (Datenblatt/Hersteller-Produktseite, Bilder, Handbuch) prüfen, nicht nur Händler-/Testtexte. Beispiel Xiaomi 6 Pro: Nur der Händlertext (expert) nennt „Blinker vorn und hinten", auf den Produktbildern sieht Chris keine. Textbehauptung allein = unbelegt. mi.com blockt WebFetch (403) → anderen Weg suchen (Handbuch-PDF, Bilder, Zubehör „Direction Indicator" auf mi.com).

**Update 02.11.2026:** Chris hat selbst recherchiert: ePF-2 Pro hat 4 Blinker (vorne+hinten) → Muss-Kriterium erfüllt, kein weiterer Beleg nötig. Fokus jetzt Gewicht + größerer Akku. Varianten laut e-roller.com (Affiliate, Herstellerangaben): 490 Wh fest 23,0 kg · 612 Wh fest 23,6 kg · 816 Wh fest 23,8 kg · 490 Wh Wechselakku 22,2 kg · 653 Wh Wechselakku 22,6 kg; UVP 749 €, ~679 € mit Code. ADAC-Test (Variante unbekannt): 22,3 kg gemessen, Note 2,1, UVP 769 €. Ausom L1 ABE raus (nur Lenkerenden-Blinker, 29 kg).

**NEUES RANKING (Chris 02.11.2026, ersetzt Stand 28.10.):**
1. **ePowerFun ePF-2 Pro 653 Wh MIT WECHSELAKKU** (22,6 kg, ~680 € mit Code, UVP 749 €) — Favorit, ganz oben.
2. ePF-2 Pro **490 Wh Wechselakku** (22,2 kg) — nur wenn echtes Schnäppchen.
3. Alle anderen Modelle (Xiaomi 6 Pro, ePF-Pulse 960, iScooter T8/iX7 …): nur relevant, wenn der Preis stimmt (Schnäppchen).
**Raus:** ePF-2 Pro 816 Wh (zu teuer), 612 Wh fest, 490 Wh fest (Chris: Wenn ePF-2 Pro, dann unbedingt mit Wechselakku); Ausom L1; Xiaomi 6 + 5 Max.
**Regel:** Wechselakku ist Pflicht bei der ePF-2 Pro. Preis-Check auf Zuruf: Angebote für 653er-Wechselakku + 490er-Wechselakku beobachten.

**Hersteller-Preise epowerfun.de (02.11.2026, per curl, ohne Rabattcode):** ePF-2 Pro 490 Wechselakku 699 € · 653 Wechselakku 829 € · 490 fest 649 €. Die „~680 € mit Code" von e-roller.com (Affiliate, pauschal für alle Varianten) passt am ehesten zur 490er-Wechselakku-Variante (699 € minus Code), NICHT zur 653er (829 €). Preisalarm `scripts/scooter_preisalarm.py` (Cron Mo/Mi/Fr 08:00, Telegram nur bei neuem Tiefstpreis) beobachtet bisher NUR die 653er (829 €, unverändert seit 30.10.). Code-Wert und echter Endpreis noch offen.

**Preisalarm erweitert 02.11.2026 ~17:00:** beobachtet jetzt 653W (Start 829 €) UND 490W Wechselakku (Start 699 €), getrennte Tiefstpreise je Modell im selben State (data/scooter_preisalarm.json, altes Format migriert). Backups backups/scooter_preisalarm*_vor_490_20261102.*

## ⌨️ Kürzel „escooter“ (Chris 16.11.2026) — IMMER bei Eingabe von „escooter“
Nicht nur Status nennen, sondern **jedes Mal prüfen** (1) ob es ein neues/anderes Modell gibt, das zu den Kriterien passt (Blinker vorn+hinten, Federung vorn+hinten, ABE; Wechselakku nur bei ePF-2 Pro Pflicht; Gewicht/Akku zählen), und (2) ob der bevorzugte **ePF-2 Pro (653 Wh Wechselakku, Zweit: 490 Wh)** gerade rabattiert ist (Black Week 23.–30.11., Black Friday 27.11.2026; Code „e-roller.com“ wird oft genannt, Höhe unbelegt). Quellen: epowerfun.de (curl), data/scooter_preisalarm.json, Web. Herstellerangaben vor Händlertexten ([[feedback_keine_geratenen_infos]]).

**Check 16.11.2026 11:15:** epowerfun.de zeigt noch REGULÄRPREIS (653W 829 €, 490W 699 €, unverändert seit 28.10./02.11.), kein Black-Week-Preis, Deals-Seite nur Frühjahrsdeal (bis 31.3.26: ePF-2 PRO ab 499 € → Preis kann deutlich fallen) + Warehouse-Deal Pulse 960 gebraucht 889 €. Preisalarm Mo/Mi/Fr 08:00 deckt Black Week ab (23./25./27./30.11.), meldet bei neuem Tiefstpreis. Neue Modelle: kein belegter Treffer. Kandidaten nur aus Händler-/Affiliate-Texten (Blinker-POSITION unbelegt → Chris-Prüfregel): iScooter iX7 (~599 €, Vollfederung, „Blinker ab Werk“, ABE), iScooter R3 (~459 €, Blinker, Vollfederung), iScooter T8 (720 Wh, kein Wechselakku), Egret GT (Wechselakku, 1.599 €+, hinten Federung unbelegt), ePF-Pulse+ (Blinker laut Text, Vollfederung). Blinker-Pflicht-Datum widersprüchlich in Quellen (neu genehmigte Modelle ab 01.04.2026 vs. ab 2027) — ungeklärt.

**Hersteller-Prüfung 16.11.2026 11:35 (Chris: „ja“):** 
- **ePF-PULSE+ (epowerfun.de, Herstellerangabe, wörtlich):** „Sehr helle Blinker vorne und hinten“, „Federung vorne und hinten“, ABE P474, 26 kg (960 Wh) / 25,1 kg (720 Wh), 140 kg Zuladung, 960er 1.199 € — aktuell ausverkauft, Vorbestellung „Liefertermin spätestens 09.12.26“; Preis 720er nicht gelistet; Wechselakku: Seite sagt nichts. → erfüllt Blinker+Federung BELEGT, aber 3–4 kg schwerer als ePF-2 Pro 653 Wechselakku (22,6 kg) und 1,5× so teuer.
- **iScooter iX7 (Basis):** 26 kg, Akku NICHT entnehmbar, Blinker laut Testportal (Position unbelegt), Federung beim Basismodell unbelegt (Quellen meist iX7 Pro) → praktisch raus.
- **Preisalarm Black Week:** Cron `0 8 20-30 11 *` (täglich 20.–30.11., Mo/Mi/Fr doppelt harmlos) war schon gesetzt; Meldungen laufen über MC-Jobs (nicht Telegram). Nur „neuer Tiefstpreis“ wird gemeldet.
**Black Friday 27.11.2026:** Zusatzläufe 14:00 + 20:00 zusätzlich zum täglichen 08:00 (Cron gesetzt 16.11.).
