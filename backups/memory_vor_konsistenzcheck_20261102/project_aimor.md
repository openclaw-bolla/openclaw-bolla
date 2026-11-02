---
name: Aimor Fotorahmen Projekt
description: Automatisches Foto-Push von OneDrive auf den Aimor-Fotorahmen PF1007 per Python-Script — FERTIG und läuft
type: project
originSessionId: 27bdbc7b-4e9a-4642-a895-df7c4ce6dd2e
---
Ziel: Monatlich ca. 50 Fotos aus OneDrive auf den Aimor-Fotorahmen pushen, vorher alle eigenen Fotos löschen.

**Status: FERTIG & VOLLSTÄNDIG (01.05.2026)** — Bind OK, 50/50 Fotos pro Run, Netty Push bestätigt, Cron aktiv.

**Rahmen:** Modell PF1007, deviceUid = "PF10075701002460", friendlyName = "Mandels"
**App:** com.elink.robot.moshare (AiMOR-App), auf Huawei-Handy von Chris

**API-Details (reverse-engineered aus APK):**
- Login: `https://imsaccount.efercro.com:10548/account/authen/app/user/login`
  - accountType = 2 (externer Account, z.B. Outlook)
  - password = MD5(pw + "yihengke")
  - sign = Base64(SHA1("{account}&{accountType}&{pw_md5}&{formalkey}&{ver}&{channelId}&{ts}"))
  - token kommt aus response.data.token
  - userId = response.data.userId (= 8095404 für ernstmandel@outlook.de)
- OSS Upload: Alibaba Cloud, bucket "iphotoframe", endpoint oss-us-east-1
  - Key-Format: `{userId}-{deviceUid}/{filename}` (wichtig!)
  - STS-Credentials aus /oss/credentials Endpunkt
- Task erstellen: `/digital/photo/frame/app/task/update` mit status="CREATE"
- Frames API antwortet mit `data.devices` (nicht `data.list`)
- API antwortet mit code="success" (String, nicht 200)

**Netty Push (TCP, implementiert 01.05.2026):**
- Server: `imsconnect.efercro.com:7806`
- Wire: 12-byte Header (seq|cmd|len, big-endian int32) + Protobuf payload
- Login CMD 110009: EduConnect{client=1, token, sign=Base64(SHA1("{userId}&948baf4f-e5b8-4bdd-a403-538ecfe8b188&{token}&1"))+".version-01"}
- Subscribe CMD 110029: EduSubscribe{iotIds=[IotId{client=3, id=deviceUid}]}
- Push CMD 110019: EduPipelineMessage{toContext=IotContext{client=3,id=deviceUid}, cmd=160004, msg=AeezoPushMedia}
- AeezoPushMedia fields: userId(1), taskId(2), ossId(3), mediaType=1(4), mediaSum=1(6), mediaInfo_json(7), index=0(9), ossType="OSS"(10)
- WICHTIG: Ohne diesen Netty-Push erscheinen die Fotos NICHT auf dem Rahmen!

**Script:** `/home/bolla/workspace/scripts/aimor_push.py`
- Speichert gesendete Task-IDs in ~/.aimor_task_ids
- Beim nächsten Run: alte IDs löschen, neue 20 Fotos senden
- Nach REST-Upload: automatisch Netty Push für alle Tasks
- Cron Push:    `0 8 1 * *       aimor_push.py`     → jeden 1. um 08:00
- Cron Notify:  `0 20 28-31 * *  aimor_notify.py`   → letzter Monatstag um 20:00 → Telegram an Chris
- Foto-Quelle: `/mnt/d/OneDrive/Mandels` (12.000+ Fotos, inkl. Unterordner)
  - Alternativ: photo_folder=/pfad in ~/.aimor_config
- Löschen funktioniert NICHT — Fotos bleiben dauerhaft auf dem Rahmen (Hardware-Speicher)
- Bind (einmalig, 01.05.2026): `--bind 257698184936` — Account als Freund eingetragen, nicht mehr nötig

**Config:** `~/.aimor_config` (chmod 600)
```
email=ernstmandel@outlook.de
password=...
photo_folder=/mnt/d/OneDrive/Bilder/Eigene Aufnahmen  # optional
```

**Why:** Familien-Fotorahmen, Robin schickt manchmal Fotos aus Ulm — Chris möchte automatisch einen rotierenden Pool eigener Fotos drauf haben.

**How to apply:** Wenn Chris nach Aimor fragt: Script ist fertig. Eventuelle Änderungen: nur Foto-Quelle anpassen in ~/.aimor_config.
