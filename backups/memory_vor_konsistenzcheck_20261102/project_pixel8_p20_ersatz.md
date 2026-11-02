---
name: project-pixel8-p20-ersatz
description: "Pixel 8 (refurb „Wie neu", Akku ≥80 %, 269 €, bestellt ~20.09.2026) löst das Huawei P20 ab — Setup-Plan bei Ankunft, Akku-Check nicht vergessen"
metadata:
  node_type: memory
  type: project
  originSessionId: 57d99a3d-0a20-414e-bd82-62482ad85321
  modified: 2026-09-20T09:30:00.000Z
---

Chris hat am **20.09.2026** ein **Google Pixel 8 128GB Obsidian** bei **asgoodasnew** für **269 €** bestellt
(Zustand „Wie neu", Akku ≥ 80 %; Bestellnr. agan-de-1393951, Gesamt 275,90 € inkl. 6,90 € Versand, 60 €
REMADE-Gutschein eingerechnet). **Versand: Maersk** (deren Last-Mile/Logistik-Sparte, nicht die Container-Reederei
selbst), Paketverfolgung **1MAGANEAB0056887701** — Versandbestätigung kam 21.09.2026 13:27 Uhr. Es **ersetzt das zuerst
bestellte Pixel 8a** (279 € + 6,90 €, asgoodasnew, 10.09.2026), das Chris am 20.09.2026 zurückschickt.
Wechselgrund: 8 ist etwas besser gebaut (Gorilla Glass Victus, IP68, 27 W Kabel-Laden), 20 € günstiger.
Nachteil: Updates „nur" bis ca. **Okt 2030** (8a: Mai 2031) — egal fürs P20-Ersatzgerät.

⚠️ **Zum Qi-Laden:** Chris meinte, das 8a könne nicht kabellos laden — laut Wikipedia/Datenblatt kann es
7,5 W Qi (kein Qi2). Chris' Quelle unklar (Händlerlisting? 6a-Verwechslung? selbst getestet?). Für das
Pixel 8 irrelevant: Qi-Laden ist dort sicher vorhanden (Pflichtkriterium erfüllt).

Auswahlkriterien (aus der MP-Chat-Kaufberatung): Qi-Laden Pflicht, so viel Speicher wie
preislich sinnvoll, guter Akku, Displaygröße ~P20 reicht, Kameraqualität egal (Duo ist top),
USB-C, < 300 €, lange Update-Versorgung.

## Auftrag bei Ankunft

0. **🔋 AKKU CHECKEN — Chris beim Einrichten AKTIV DARAN ERINNERN (Chris' ausdrücklicher Wunsch 20.09.2026):**
   Einstellungen → Akku → Akkuzustand (bzw. Akku-Info). Gekauft „≥ 80 %". Liegt der Wert knapp
   bei/unter 80 %, innerhalb der Rückgabefrist reklamieren. Gleichzeitig **Speicher = 128 GB** und
   **Zustand „Wie neu"** prüfen. Das gehört an den ALLERERSTEN Schritt, vor SIM/Apps/Einrichtung —
   sonst ist die Rückgabefrist ggf. verbaut.
1. **Pixel 8 wird der P20-Ersatz.** Das Huawei P20 (Android 9, [[project_p20_neustarts]])
   geht in Rente. **Duo 2 bleibt Haupthandy.**
2. **Alle Nicht-Huawei-Apps vom P20 aufs Pixel 8 bringen** — alles außer Huawei-eigenen Apps
   (AppGallery, Huawei Health, Petal Search/Maps usw.). App-Liste vom P20 per ADB ziehen
   (`adb shell pm list packages -3`), Huawei-Pakete rausfiltern, Rest aus dem Play Store installieren.
3. **Pixel 8 per ADB über Bolla verwaltbar machen** — Kabelloses Debugging (ab Android 11)
   analog Duo 2 und Renis Z Flip 3, danach in [[user_devices]] eintragen.
4. **MP-Verbindungsfeld:** In Mission Control (Studio, `index.html`) im Bereich
   „Bolla Surface" / Geräte-Verbindungen ein **Verbindungsfeld fürs Pixel 8** ergänzen —
   analog zu den Feldern für Duo / Surface-Geräte.
5. **Chat-Ansprache:** Alias **„p8"** (Chris' bisheriger Wunsch war „p8a"; beides akzeptieren).
6. **mmc-Rolle zieht mit um:** die mobile Mission Control ([[feedback_mmc]]) läuft künftig auf dem Pixel 8.
7. **SIM zieht mit um:** die P20-SIM (Nano-SIM) kommt ins Pixel 8 — **Zeitpunkt: GEGEN ENDE**
   (siehe unten), nicht zu Beginn.

## WhatsApp-Setup (von Chris bestätigt 20.09.2026)
- **P20 = WhatsApp-Haupthandy** (mit der SIM-Nummer). **Duo 2, Surface Book, Studio (Desktop-App) sind
  verknüpfte Geräte** — sie haben KEIN Chat-Backup, nur synchronisierte Kopien. Das P20 ist das einzige echte Backup.
- **Backup-Ziel: Chris' Google-Konto chrismandel13@gmail.com** (Google Drive, von Chris bestätigt 20.09.2026).
  Das Konto hat ein **Google-One-Abo mit 100 GB** (Stand 11.09.2026: 15 GB belegt) — Speicher ist KEIN Problem.
  Die „Google-Speicher voll"-Theorie ist widerlegt ([[project_p20_neustarts]], 11.09.2026). Trotzdem vor dem
  SIM-Wechsel im WhatsApp-Chat-Backup-Screen das Datum der letzten Sicherung prüfen; als Rückfallebene
  lokales Backup (`Android/media/com.whatsapp/WhatsApp/Databases/`) per USB-ADB aufs Studio.
- **Ablauf:** frisches Backup auf P20 **kurz vor dem SIM-Wechsel** → Nummer aufs Pixel 8 registrieren →
  „Wiederherstellen" wählen → danach **Duo, Book und Studio per QR-Code neu verknüpfen** (werden beim
  Haupthandy-Wechsel meist abgemeldet).

## Ablauf / Trigger
Chris meldet sich in einer **Terminal-Session** mit **„p8 ist da"** (oder „p8a ist da"). Das ist das
Startsignal. **Neu (20.09.2026): Chris führt Einrichtung und App-Übertragung PARALLEL mit Bolla durch**
(Chris am Handy, Bolla schrittweise anleitend + am PC per ADB zuarbeitend) — also nicht autonom
abarbeiten, sondern im Dialog, kurze Schritte.

Reihenfolge-Empfehlung:
1. Akku/Speicher/Zustand prüfen (Punkt 0).
2. P20: App-Liste per USB-ADB sichern (Backup vor Eingriffen; braucht keine SIM).
3. Pixel 8 Erst-Einrichtung per WLAN, Google-Konto, Play-Store-Apps.
4. SIM erst danach umsetzen — **Ausnahme:** Apps mit SMS-Verifizierung (WhatsApp, Bank/2FA,
   [[project_authenticator_sync]]) → SIM VOR deren Einrichtung umsetzen, und **WhatsApp-Chat-Backup
   vorher auf dem P20** machen. P20 bleibt bis dahin mit SIM lauffähig (mmc).
5. WLAN-ADB, MP-Feld, Alias, mmc-Umzug.

Beim Abarbeiten: erst Backup dann löschen, `user_devices.md` + [[feedback_mmc]] nach Abschluss
aktualisieren, P20 als „außer Dienst" markieren (nicht wegwerfen — Chris entscheidet über Verbleib).

## 🆕 Update 21.09.2026 (Chris): P20 funktioniert „immer weniger", Pixel 8 kommt vermutlich erst **Mi/Do (23./24.09.)**
Chris fragte: wie kommt Bolla an App-Liste + App-Daten (Wallets, Authenticator) vom P20? Antwort/Plan: **App-Daten (v. a. TOTP-Secrets, Wallet-Karten) sind per ADB NICHT auslesbar**
(Android 9, kein Root; `adb backup` scheitert bei Apps mit allowBackup=false, außerdem Secrets nie in Chat/Logs) → nur über die Apps selbst sichern. **Jetzt, solange das P20 noch läuft:**
(1) Google-Sicherung anstoßen (Einstellungen → System → Sichern → Jetzt sichern; Konto chrismandel13@gmail.com, 100 GB); (2) WhatsApp-Chat-Backup auf Google Drive JETZT (nicht erst vor SIM-Wechsel);
(3) **Authenticator zuerst**: pro App Cloud-Backup/Export prüfen (MS Authenticator → Einstellungen → Cloud-Sicherung [Duo hat sie an], Google Authenticator → Konten exportieren/Sync), Liste WAS wo drin ist
([[project_authenticator_sync]]); (4) Wallet/Google Pay: Karten neu hinzufügen nötig, Bonus-/Tickets meist kontobasiert. App-Liste: `adb shell pm list packages -3` per USB-ADB
(P20 hat kein WLAN-ADB; USB-Debugging aktivieren; aus WSL bräuchte es usbipd — sonst Play-Store-„Meine Apps → Nicht auf diesem Gerät" auf dem Pixel als Ersatz). Aktuell hängt an adb nur ein anderes Gerät (192.168.178.20, vermutl. Duo 2).

## 🆕 Duo 2 als Quelle fürs P8 (Chris 21.09.2026: „Duo ist die bessere Wahl", Apps laufen dort besser; Bolla hat Duo per WLAN-ADB read-only inventarisiert)
Duo 2 = Android 12, >170 Drittanbieter-Apps (Superset des P20). **Empfehlung:** Pixel-Einrichtung „Von Android-Gerät kopieren" mit Duo als Quelle (Apps/Kontakte/SMS, KEINE App-Anmeldungen/Secrets); Duo bleibt unverändert = Netz.
Konten auf dem Duo: Google chrismandel13 + **renate.mandel13@gmail.com** (klären ob aufs P8), MS ernstmandel@outlook.de + Work-Konten (lg-n.de / LGNorderstedt.onmicrosoft.com), WhatsApp (nur verknüpft), Telegram, Facebook/Insta/Runtastic.
**Authenticator:** `com.azure.authenticator` (Cloud-Backup an → Wiederherstellen mit ernstmandel@outlook.de; Schul-Konten neu), **`org.fedorahosted.freeotp` = KEIN Backup → Dienste neu einrichten, größtes Risiko**, `com.excelsecu.esauthenticator.thetis` (FIDO-Key-Begleiter).
Passwortmanager vermutl. mSecure (`com.mseven.barolo`) → Sync/Export prüfen. Wallets: `com.google.android.apps.walletnfcrel`, `eu.yourpass.wallet`. Banking geräte-gebunden: `com.db.pwcc.dbmobile` (BestSign vermutl. integriert), `com.starfinanz.smob.android.bwmobilbanking` + `bwpushtan` (pushTAN → Neuregistrierung, evtl. Brief/Tage), `com.s_payment.mobiles_bezahlen`, `de.traderepublic.app` (PIN 4-stellig, [[reference_trade_republic_pin]]), PayPal ([[reference_paypal_2fa]]), Coinbase.
Regel: geräte-gebundene Apps nur aufs P8 holen wenn nötig — Neuregistrierung kann das Duo abmelden; Reihenfolge: erst P8 registrieren, wenn Duo als Fallback funktioniert.
Dateimanager+ = `com.alphainventor.filemanager` (auf Duo), aufs P8 nicht nötig (Google „Dateien" da). mmp/mmc laufen in Chrome (bolla.chrismandel.de, Cloudflare-Access-Magic-Link, Mikrofon-Erlaubnis für mmc, Startbildschirm-Verknüpfung neu). OneDrive: Kamera-Upload → `Bilder/Eigene Aufnahmen` wieder aktivieren ([[project_foto_organisation]]). WhatsApp: P20 = Haupt (SIM-Nummer), Gruppen kommen mit Nummer, Verlauf nur per Google-Drive-Backup; danach Duo/Book/Studio neu verknüpfen.

## ✅ Chris' Vorgaben 21.09.2026 (verbindlich) — Einrichtung Mi 23./Do 24.09., „Schritt für Schritt erklärt"
- **Bolla begleitet die Einrichtung aktiv, Schritt für Schritt, und ERINNERT AKTIV daran** (Chris' ausdrücklicher Wunsch). Cron-Reminder per Telegram läuft: `scripts/pixel8_setup_reminder.py`
  (Di 22.09. 18 Uhr Duo-Vorbereitung, Mi 23.09. 15 Uhr Einrichtungstag, Do 24.09. 15 Uhr Nachfrage; State `config/pixel8_setup_reminder_state.json`; stoppen mit `"p8_done": true` sobald Chris „p8 fertig" sagt).
  Start immer mit 🔋 Akku-Check.
- **Kopieren vom Duo:** Renate-Google-Konto (renate.mandel13@gmail.com) **kommt mit**. **Dateimanager+ NICHT** installieren. Abwählen (Vorschlag, Chris entscheidet): Spiele (Subway Surfers, Minecraft, Solitaire, Google Play Games, Xbox-Apps ×3, Steam), evtl. Microsoft-Spielereien (Whiteboard, Math, Loop). Später jederzeit nachinstallierbar (Play Store → Meine Apps → Nicht auf diesem Gerät).
- **FreeOTP enthält NUR IONOS** → IONOS-2FA am P8 neu einrichten (Duo bleibt zum Anmelden, im IONOS-Login unter Sicherheit neuen Authenticator hinzufügen; MS Authenticator → Wiederherstellen).
- **Zahlkarten (Google Wallet):** Chris hilft Bolla beim Wiedereinbinden. ⚠️ Bolla KENNT die Karten NICHT (nicht per ADB lesbar) → Chris nennt sie (Bank/Kartenart) bei der Vorbereitung am Duo; Chris hat sie genannt (21.09.). Pro Karte: Wallet → Zahlungsmethode hinzufügen → Bank-Bestätigung (SMS/App).
- **Banking: beides aktivieren, als Backup auf dem P8 (Duo bleibt aktiv):** pushTAN (Starfinanz-App) **und** Deutsche Bank BestSign. Deutsche Bank: Freischaltung laut Chris über die App auf dem Duo. Beim Schritt PRÜFEN ob die Bank das Duo dabei abmeldet — wenn ja, stoppen und Chris fragen.
- **mmp/mmc-Links:** aufs P8 erst möglich wenn das Gerät da ist; vorbereitet: beide Links im gclip (Clipboard-Tab in mmp): `https://bolla.chrismandel.de/m` (mmp/mmc, mobile.html) + `/f` (Renis Fotos). Am P8: Chrome öffnen → Link → Cloudflare-Access-Magic-Link (ernstmandel@outlook.de) → ⋮ „Zum Startbildschirm hinzufügen"; für mmc Mikrofon in Chrome erlauben.
- **„App-Gruppen" (Chris meinte NICHT WhatsApp-Gruppen)** = Startbildschirm-/App-Ordner wie „Microsoft" auf dem Duo. Duo nutzt **Microsoft Launcher** (`com.microsoft.launcher`) → am Duo vorher Launcher → Einstellungen → Sichern und Wiederherstellen → sichern; am P8 Microsoft Launcher aus dem Play Store installieren, als Standard setzen, wiederherstellen (Ordner bleiben, nicht installierte Apps fallen raus; Layout kann abweichen, Duo hat 2 Displays). Sonst Ordner am Pixel Launcher von Hand neu anlegen.

## ✅ Update 21.09.2026 (Chris): Wallet-Inhalt + Launcher-Entscheidung
- **Google Wallet auf dem Duo:** Deutsche Bank **Card Plus** (Zahlkarte), **Allianz Privatschutzcard**, **Gesundheitskarte**, **Rusta**, **Lindt & Sprüngli** (Kundenkarten). Kundenkarten/Pässe hängen meist am Google-Konto → am P8 ERST nachsehen, was automatisch erscheint; Zahlkarte (DB Card Plus) IMMER neu: Wallet → Hinzufügen → Zahlungskarte, Bestätigung über Deutsche-Bank-App/SMS (ggf. „Zu Google Wallet hinzufügen" direkt in der DB-App). Fehlendes über App der jeweiligen Firma/Barcode einscannen → echte Karten bereithalten.
- **YourPass (`eu.yourpass.wallet`):** enthält nur ADAC (paar alte Tickets, nicht nötig) → **NICHT aufs P8 kopieren** (ADAC-Mitgliedsnachweis notfalls in der ADAC-App).
- **Microsoft Launcher: Chris will ihn NICHT** → Pixel-Launcher (Android/Google). App-Gruppen/Ordner (z. B. „Microsoft") am P8 von Hand neu anlegen; Bolla kann helfen: Ordner-Inhalte vom Duo auflisten (Chris nennt sie oder Screenshot vom Duo-Startbildschirm nach Rückfrage). Ältere Notiz zum Launcher-Backup ist damit hinfällig.
- **Update 21.09.2026 (Chris):** MS-Authenticator-**Cloud-Sicherung ist durch ✅**. **App-Ordner legt Chris selbst neu an** (Bolla muss Duo-Ordner NICHT erfassen/Screenshot) — am P8 nur kurz unterstützen falls er fragt. Reminder-Text entsprechend gekürzt (nur Karten bereitlegen + „p8 ist da").
- **Update 21.09.2026 (Chris):** **Spiele + Xbox-Apps + Microsoft-Spielereien werden MITGENOMMEN** (spielt selten, will sie haben 'man weiss ja nie' und den Schülern zeigen). Abgewählt werden NUR Dateimanager+ und YourPass. Hinweis: Spielstände/Minecraft-Welten sind lokal auf dem Duo und kommen beim Kopieren i. d. R. NICHT mit — nur sichern falls Chris das will (er hat es nicht verlangt).

## 🆕 Update 06.10.2026 (Chris): P8 ist da und in Benutzung — läuft mit **Android 17**
Chris nutzt das Pixel 8 bereits (Circle to Search, Face Unlock, adaptive Benachrichtigungen besprochen). Menüpfade/Funktionen daher für **Android 17** nennen (z. B. „Adaptive Benachrichtigungen" heißt dort evtl. anders/ist umgezogen → Einstellungs-Suche empfehlen). Navigation: **Gestennavigation** (Leiste unten nur dünner Strich, zeitweise unsichtbar). Chris trägt **keine Brille** (künstliche Linsen in beiden Augen) — nie Brille unterstellen.
