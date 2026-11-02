---
name: feedback-desktop-apps-social
description: "Chris postet Social Media über die DESKTOP-Apps (WhatsApp, Instagram, TikTok) — Material auf den Desktop legen, nicht aufs Handy schieben"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ccd54205-b6df-4469-af5e-11b5e0ed2b40
  modified: 2026-09-07T12:19:07.384Z
---

Chris arbeitet bei WhatsApp, Instagram und TikTok bevorzugt mit den **Desktop-Apps** (am Surface Laptop Studio), nicht über die Handy-Apps.

**Why:** Posten, Bilder hochladen und Captions einfügen macht er am PC. Inhalte aufs Handy zu schicken (Telegram/gClip) ist für ihn ein Umweg.

**How to apply:** Posting-Material (Bilder, Promo Cards, Videos, Caption als .txt) immer auf den **OneDrive-Desktop** (`/mnt/d/OneDrive/Desktop/`) legen, damit er es direkt in der Desktop-App nutzen kann. gClip/Telegram-Push nur als Zusatz oder wenn er ausdrücklich aufs Handy will.

**WICHTIG (25.06.):**
- Die Caption-.txt enthält **NUR den fertigen, einfügbaren Text** (inkl. Hashtags — die kommen bei TikTok/Insta direkt in die Beschreibung, kein separates Feld). **KEINE** zusätzlichen Anleitungen/KI-Label-Hinweise in die Datei mischen — Schritt-Hinweise gehören in den Chat, nicht in die Desktop-Datei.
- Wenn Chris **„fertig"** meldet: alle für diesen Zweck angelegten Dateien **wieder vom Desktop löschen** (aufräumen, Desktop sauber halten).

Plattform-Eigenheiten: TikTok am Desktop (TikTok Studio) nimmt **nur Video** — für ein Standbild ein kurzes MP4 (ffmpeg, 1080×1920) bauen; echte Foto-Posts gehen bei TikTok nur in der Handy-App. Instagram-Desktop-App kann Bilder direkt posten. Siehe [[feedback_desktop_onedrive]], [[feedback_copy_from_terminal]], [[feedback_cleanup]].

**⚠️ Instagram-Desktop hat KEIN separates "Reel"-Menü (verifiziert 07.09.2026 per WebSearch + von Chris live bestätigt):** Beim "+" gibt es nur "Beitrag" — das ist normal, Instagram behandelt Videos dort intern automatisch als Reel. Die Vorschau zeigt Hochformat-Videos (9:16) aber standardmäßig QUADRATISCH zugeschnitten. Unten links im Vorschaubild gibt es ein kleines rundes Symbol mit zwei diagonalen Pfeilen (Zuschneiden/Vergrößern) — erst ein Klick darauf wechselt auf Originalformat/Hochformat. Ohne diesen Klick wird der quadratische Ausschnitt gepostet (unterer Rand inkl. eventuellem Text fällt weg). Betrifft jeden Hochformat-Video-Upload über Insta-Desktop, nicht nur Aufpeppen-Ergebnisse. Siehe [[feature_aufpeppen]].
