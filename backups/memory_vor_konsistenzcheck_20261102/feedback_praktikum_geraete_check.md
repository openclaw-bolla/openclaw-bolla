---
name: feedback-praktikum-geraete-check
description: "⛔ RETIRED 01.09.2026 — KI-Tool-Verfügbarkeitscheck ist obsolet, seit gar kein KI-Tool mehr in Praktika genutzt wird. Rest (Windows-Versionsunterschiede Laptop/PC) bleibt als Kontext gültig."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 69a38b8d-d60d-499e-89a9-4518940336fa
  modified: 2026-09-02T06:13:58.420Z
---

## ⛔ RETIRED (01.09.2026)

Chris: "Den prakt Geräte-Check kannst du komplett rausnehmen, ich darf ja kein KI-Praktikum mehr
machen." Seit der Schulleiterin-Entscheidung vom 28.08.2026 ([[feedback_schulkontext_risiko_warnen]])
läuft KEIN KI-Tool mehr in den Hands-on-Übungen der 7er (auch kein AIS.chat — Chris nutzt es bewusst
nicht). Damit ist der KI-Tool-Verfügbarkeitscheck unten komplett gegenstandslos.
- Cron-Reminder `praktikum_geraete_check_reminder.py` (Di 8 Uhr) am 02.09.2026 aus der Crontab
  entfernt (`crontab -l` verifiziert — kein Treffer mehr, kritische Jobs alle noch drin). Skript-
  Datei selbst darf bei Gelegenheit gelöscht werden — nicht eilig, toter Code schadet nicht.
- Der Windows-10-vs-11/Office-2010-Teil unten (Geräte-Unterschiede PC/Laptop, unabhängig von KI)
  bleibt als Hintergrundwissen gültig, falls mal PPT-Funktionsumfang auf den Laptops relevant wird.

---

Vor JEDEM neuen Praktikum-HTML (siehe [[feedback_prakt_anleitungen]], [[project_schuljahr2627]]) prüfen,
was auf den tatsächlichen Schulgeräten zum Zeitpunkt der Nutzung wirklich funktioniert — nicht davon
ausgehen, dass eine früher beschriebene Methode noch aktuell ist. KI-Tool-Verfügbarkeit (v.a.
Bildgenerierung) ändert sich häufig (Login-Pflicht, Kontingente), Software-Stand unterscheidet sich
zwischen den Gerätetypen.

**Why:** Chris hat am 12.08.2026 PCs und Laptops der Schule getestet und dabei zwei wichtige, nicht
offensichtliche Änderungen gefunden, die ein bestehendes Praktikum (Kurstag 2) unbrauchbar gemacht
hätten, wenn er es nicht vorher geprüft hätte.

**Bekannter Geräte-Stand (Stand 12.08.2026, bei Bedarf erneut verifizieren, ändert sich):**
- **PCs:** Windows 11 (aktuelle Office-Version).
- **Laptops:** Windows 10, **Office 2010** (oder ähnlich alt) — deutlich eingeschränkter
  Funktionsumfang als moderne PowerPoint-Versionen. Bei PPT-lastigen Praktika (PowerPoint-Profi-Reihe
  ab Kurstag 7) IMMER gegenchecken, ob eine beschriebene Funktion in Office 2010 überhaupt existiert,
  bevor sie ins Praktikum geschrieben wird — sonst frustrierte Schüler an den Laptops.
- **Copilot (Edge-Integration UND Web-App):** Bildgenerierung funktioniert NICHT mehr ohne Microsoft-
  Account — die meisten Schüler haben keinen. Reine Text-/Chat-Funktion (Geschichten schreiben etc.)
  scheint weiterhin ohne Account zu gehen (nicht explizit von Chris bestätigt als Problem).
- **Bing Image Creator:** funktioniert (Stand 12.08.2026) noch OHNE Account, aber mit einer
  begrenzten Zahl kostenloser Bilder — als Ersatz für Copilot-Bildgenerierung nutzen, aber sparsam
  formulieren lassen (Schüler nicht wild experimentieren lassen, jedes Bild zählt gegen das Kontingent).

**How to apply:** Bei jedem künftigen Praktikum-HTML (neu oder bestehend, das gerade angefasst wird)
kurz gegenchecken: Welches Gerät nutzt diese Klasse/dieser Kurstag? Welche KI-Tools braucht das
Praktikum, und funktionieren die aktuell wie beschrieben ohne Schüler-Account? Bei Unsicherheit lieber
kurz bei Chris nachfragen oder ihn bitten, es selbst kurz zu testen, statt eine veraltete Methode
unverändert zu übernehmen.

**Wiederkehrender Reminder (12.08.2026 eingerichtet, 02.09.2026 wieder entfernt):** Es gab einen
Cron-Job `scripts/praktikum_geraete_check_reminder.py`, der Chris alle 14 Tage per Telegram an einen
Geräte-/KI-Tool-Check erinnert hat. Mit dem KI-Praktikum-Aus ist er gegenstandslos und wurde aus der
Crontab genommen.
