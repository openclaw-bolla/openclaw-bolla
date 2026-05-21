#!/usr/bin/env python3
"""
Aimor Photo Frame Auto-Push
Lädt ~50 Fotos aus OneDrive (Mandels) auf den Aimor-Rahmen PF1007
und löscht vorher alle vom letzten Run gesendeten Fotos.

Verwendung: python3 aimor_push.py
Cron (monatlich am 1.): 0 8 1 * * python3 /home/bolla/workspace/scripts/aimor_push.py
"""

import hashlib
import base64
import time
import json
import random
import os
import socket
import struct
import requests
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("aimor")

# ─── Konfiguration ────────────────────────────────────────────────────────────
ONEDRIVE_FOTOS  = Path("/mnt/d/OneDrive/Mandels")  # Ordner mit Familienfotos inkl. Unterordner
FOTOS_PRO_RUN   = 50

FORMALKEY    = "3b28db17-152e-4038-b60e-8502ca7626e6"
CHANNEL_ID   = "1002-2020-0001"
CLIENT_VER   = "3.9.7"
ACCOUNT_TYPE = 2   # 2 = externer Account (Outlook/Google/Apple)

IMS_ACCOUNT = "https://imsaccount.efercro.com:10548"
IMS_PHOTO   = "https://imsphotoframe.efercro.com:10549"
NETTY_HOST  = "imsconnect.efercro.com"
NETTY_PORT  = 7806

NETTY_SIGN_KEY = "948baf4f-e5b8-4bdd-a403-538ecfe8b188"

# ─── Hilfsfunktionen ──────────────────────────────────────────────────────────

def md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def calc_sign(account, account_type, pw_md5, code_key, client_ver, channel_id, timestamp) -> str:
    raw = f"{account}&{account_type}&{pw_md5}&{code_key}&{client_ver}&{channel_id}&{timestamp}"
    sha1 = hashlib.sha1(raw.encode()).digest()
    return base64.b64encode(sha1).decode()

def ok(data) -> bool:
    c = data.get("code")
    return c == 200 or c == "success"


# ─── Protobuf-Kodierung (manuell, ohne .proto-Dateien) ────────────────────────

def _varint(n: int) -> bytes:
    result = b''
    while True:
        bits = n & 0x7f
        n >>= 7
        if n:
            result += bytes([0x80 | bits])
        else:
            result += bytes([bits])
            break
    return result

def _str_field(field_num: int, s: str) -> bytes:
    enc = s.encode('utf-8')
    return _varint((field_num << 3) | 2) + _varint(len(enc)) + enc

def _bytes_field(field_num: int, b: bytes) -> bytes:
    return _varint((field_num << 3) | 2) + _varint(len(b)) + b

def _int_field(field_num: int, n: int) -> bytes:
    return _varint((field_num << 3) | 0) + _varint(n)

def _msg_field(field_num: int, payload: bytes) -> bytes:
    return _varint((field_num << 3) | 2) + _varint(len(payload)) + payload


def _iot_context(device_uid: str) -> bytes:
    """IotContext {client=CLIENT_DEVICE=3, id=deviceUid}"""
    return _int_field(1, 3) + _str_field(2, device_uid)

def _edu_connect(token: str, user_id: str) -> bytes:
    """EduConnect {client=CLIENT_MOBILE_ANDROID=1, token, sign}"""
    raw = f"{user_id}&{NETTY_SIGN_KEY}&{token}&1"
    sha1 = hashlib.sha1(raw.encode('utf-8')).digest()
    sign = base64.b64encode(sha1).decode('utf-8') + ".version-01"
    return _int_field(1, 1) + _str_field(2, token) + _str_field(3, sign)

def _edu_subscribe(device_uid: str) -> bytes:
    """EduSubscribe {iotIds=[IotId{client=CLIENT_DEVICE, id=deviceUid}]}"""
    iot_id = _int_field(1, 3) + _str_field(2, device_uid)
    return _msg_field(1, iot_id)

def _aeezo_push_media(user_id: str, task_id: str, oss_id: str,
                      filename: str, size_byte: int, index: int = 0) -> bytes:
    """AeezoPushMedia {userId, taskId, ossId, mediaType=1, mediaSum=1, mediaInfo, index, ossType}"""
    media_info = json.dumps({
        "filename": filename,
        "sizeByte": size_byte,
        "type": 1,       # MediaType.PICTURE
        "index": index,
        "height": 0,
        "width": 0,
    })
    msg = (_str_field(1, user_id)
         + _str_field(2, task_id)
         + _str_field(3, oss_id)
         + _int_field(4, 1)           # mediaType = PICTURE
         + _int_field(6, 1)           # mediaSum = 1 photo per task
         + _str_field(7, media_info)  # mediaInfo JSON
         + _int_field(9, index)       # index
         + _str_field(10, "OSS"))     # ossType
    return msg

def _pipeline_message(device_uid: str, inner_cmd: int, inner_payload: bytes) -> bytes:
    """EduPipelineMessage {toContext, cmd=160004, msg=AeezoPushMedia}"""
    return (_msg_field(2, _iot_context(device_uid))
          + _int_field(4, inner_cmd)
          + _bytes_field(5, inner_payload))

def _netty_packet(cmd: int, payload: bytes) -> bytes:
    seq = int(time.time() * 1000) & 0x7fffffff
    return struct.pack('>iii', seq, cmd, len(payload)) + payload

def _recv_packet(sock: socket.socket):
    """Liest ein komplettes Netty-Paket (Header + Payload)."""
    hdr = b''
    while len(hdr) < 12:
        chunk = sock.recv(12 - len(hdr))
        if not chunk:
            return None, None
        hdr += chunk
    seq, cmd, length = struct.unpack('>iii', hdr)
    payload = b''
    while len(payload) < length:
        chunk = sock.recv(length - len(payload))
        if not chunk:
            break
        payload += chunk
    return cmd, payload


class AimorClient:
    def __init__(self, email: str, password: str):
        self.email    = email
        self.password = password
        self.token    = None
        self.user_id  = None
        self.session  = requests.Session()
        self.session.verify = True

    def _post(self, url, body):
        ts = int(time.time() * 1000)
        headers = {"Content-Type": "application/json", "timestamp": str(ts)}
        if self.token:
            headers["token"] = self.token
        r = self.session.post(url, json=body, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()

    def login(self):
        ts     = int(time.time() * 1000)
        pw_md5 = md5(self.password + "yihengke")
        sign   = calc_sign(self.email, ACCOUNT_TYPE, pw_md5, FORMALKEY, CLIENT_VER, CHANNEL_ID, ts)
        body = {
            "account":       self.email,
            "accountType":   ACCOUNT_TYPE,
            "password":      pw_md5,
            "channelId":     CHANNEL_ID,
            "imei":          self.email,
            "os":            "android",
            "osVersion":     30,
            "model":         "Samsung Galaxy",
            "clientVersion": CLIENT_VER,
            "osToken":       "",
        }
        r = self.session.post(
            f"{IMS_ACCOUNT}/account/authen/app/user/login",
            json=body,
            headers={"sign": sign, "timestamp": str(ts), "Content-Type": "application/json"},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        log.debug("Login response: %s", json.dumps(data, indent=2))
        if not ok(data):
            raise RuntimeError(f"Login fehlgeschlagen: {data.get('message', data)}")
        self.token   = data["data"]["token"]
        self.user_id = str(data["data"].get("userId") or data["data"].get("id") or "")
        log.info("Login OK, userId=%s, token=%s...", self.user_id, self.token[:10])
        return data["data"]

    def get_my_frames(self):
        data = self._post(f"{IMS_PHOTO}/digital/photo/frame/app/contacts/my", {})
        log.debug("Frames: %s", json.dumps(data, indent=2))
        if not ok(data):
            raise RuntimeError(f"Frames abrufen fehlgeschlagen: {data}")
        d = data.get("data", {})
        return d.get("devices") or d.get("list", [])

    def get_oss_credentials(self, device_uid: str) -> dict:
        body = {"deviceUid": device_uid}
        data = self._post(f"{IMS_PHOTO}/digital/photo/frame/app/oss/credentials", body)
        if not ok(data):
            raise RuntimeError(f"OSS Credentials fehlgeschlagen: {data}")
        return data["data"]

    def send_photo(self, device_uid: str, image_path: Path) -> tuple:
        """Foto zu OSS hochladen und als Task an den Rahmen senden.
        Gibt (task_id, oss_id, filename, file_size) zurück."""
        creds    = self.get_oss_credentials(device_uid)
        filename = image_path.name
        oss_key  = f"{self.user_id}-{device_uid}/{filename}"

        self._upload_to_oss(creds, image_path, oss_key)

        oss_id    = creds.get("ossId", "")
        task_id   = f"{self.user_id}-{int(time.time()*1000)}-0"
        file_size = image_path.stat().st_size
        now_ms    = int(time.time() * 1000)

        body = {
            "attachment":  json.dumps([{"filename": filename, "sizeByte": file_size}]),
            "fromClient":  "USER",
            "fromId":      self.user_id,
            "itemCount":   1,
            "ossId":       oss_id,
            "reason":      "",
            "status":      "CREATE",
            "taskId":      task_id,
            "taskType":    "1",
            "toClient":    "DEVICE",
            "toId":        device_uid,
            "transport":   "OSS",
            "version":     "1",
            "items": [{
                "endTime":   0,
                "name":      filename,
                "ossId":     oss_id,
                "progress":  0,
                "reason":    "",
                "size":      file_size,
                "startTime": now_ms,
                "status":    "CREATE",
                "type":      "1",
            }],
        }
        data = self._post(f"{IMS_PHOTO}/digital/photo/frame/app/task/update", body)
        if not ok(data):
            raise RuntimeError(f"Task senden fehlgeschlagen: {data}")
        log.info("Task erstellt: %s → %s", image_path.name, task_id)
        return task_id, oss_id, filename, file_size

    def netty_bind_frame(self, device_uid: str, invite_code: str):
        """Rahmen als Freund hinzufügen via Netty AEEZO_BIND (cmd=160002).
        invite_code: die 12-stellige Zahl vom Rahmen-Display (ohne Leerzeichen).
        Einmalig ausführen — danach erscheinen Fotos auf dem Rahmen.
        """
        log.info("Netty Bind: code=%s → %s", invite_code, device_uid)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(20)
        try:
            sock.connect((NETTY_HOST, NETTY_PORT))

            # 1. Login
            sock.sendall(_netty_packet(110009, _edu_connect(self.token, self.user_id)))
            try:
                sock.settimeout(5)
                cmd, resp = _recv_packet(sock)
                log.info("Bind Login ACK: cmd=%s", cmd)
            except socket.timeout:
                log.warning("Kein Login-ACK (Timeout)")
            sock.settimeout(20)
            time.sleep(0.5)

            # 2. AeezoBindDevice (AEEZO_BIND = 160002) senden
            # nickName = token (so macht es die App)
            bind_msg = (_str_field(1, self.user_id)          # userId
                      + _str_field(2, self.token)            # nickName = token
                      + _str_field(3, "")                    # headIcon
                      + _varint((10 << 3) | 0)               # field 10, wire type 0 (int64)
                      + _varint(int(invite_code)))            # inviteCode
            pipeline = _pipeline_message(device_uid, 160002, bind_msg)
            sock.sendall(_netty_packet(110019, pipeline))
            log.info("Bind-Request gesendet (inviteCode=%s)", invite_code)

            # Auf ACK warten
            try:
                sock.settimeout(8)
                cmd, resp = _recv_packet(sock)
                log.info("Bind ACK: cmd=%s, len=%d", cmd, len(resp) if resp else 0)
                if cmd == 110019:
                    log.info("Bind erfolgreich! Fotos sollten jetzt auf dem Rahmen erscheinen.")
            except socket.timeout:
                log.warning("Kein Bind-ACK erhalten")
            time.sleep(1)
        except Exception as e:
            log.error("Bind Fehler: %s", e)
        finally:
            sock.close()

    def netty_push_all(self, device_uid: str, tasks: list):
        """Sendet alle Tasks per Netty TCP Push an den Rahmen.
        tasks: Liste von (task_id, oss_id, filename, file_size) Tuples
        """
        if not tasks:
            return
        log.info("Netty Push: Verbinde zu %s:%d...", NETTY_HOST, NETTY_PORT)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(20)
        try:
            sock.connect((NETTY_HOST, NETTY_PORT))
            log.info("Netty verbunden")

            # 1. Login (EduConnect, CMD=110009)
            connect_payload = _edu_connect(self.token, self.user_id)
            sock.sendall(_netty_packet(110009, connect_payload))
            log.info("Netty Login gesendet")

            # Auf Login-ACK warten
            try:
                sock.settimeout(5)
                cmd, resp = _recv_packet(sock)
                log.info("Netty Login ACK: cmd=%s, len=%d", cmd, len(resp) if resp else 0)
            except socket.timeout:
                log.warning("Kein Login-ACK erhalten (Timeout) — fahre trotzdem fort")
            sock.settimeout(20)

            # 2. Subscribe (CMD=110029)
            sub_payload = _edu_subscribe(device_uid)
            sock.sendall(_netty_packet(110029, sub_payload))
            log.info("Netty Subscribe gesendet")
            time.sleep(0.5)

            # 3. Für jeden Task eine AeezoPushMedia senden (CMD=110019)
            pushed = 0
            for task_id, oss_id, filename, file_size in tasks:
                aeezo = _aeezo_push_media(
                    user_id=self.user_id,
                    task_id=task_id,
                    oss_id=oss_id,
                    filename=filename,
                    size_byte=file_size,
                    index=0,
                )
                pipeline = _pipeline_message(device_uid, 160004, aeezo)
                sock.sendall(_netty_packet(110019, pipeline))
                pushed += 1
                log.info("Netty Push gesendet: %s (task=%s)", filename, task_id)
                time.sleep(0.3)

            log.info("Netty Push: %d/%d Fotos erfolgreich gesendet", pushed, len(tasks))
            time.sleep(1)

        except Exception as e:
            log.error("Netty Fehler: %s", e)
        finally:
            sock.close()
            log.info("Netty Verbindung geschlossen")

    def _upload_to_oss(self, creds: dict, image_path: Path, oss_key: str):
        try:
            import oss2
        except ImportError:
            raise RuntimeError("oss2 nicht installiert — pip3 install oss2")

        ak    = creds.get("key", "")
        sk    = creds.get("secret", "")
        token = creds.get("token", "")
        ep    = creds.get("endpoint", "")
        bkt   = creds.get("bucket", "")

        if not all([ak, sk, token, ep, bkt]):
            raise RuntimeError(f"Unvollständige OSS Credentials: {list(creds.keys())}")
        if not ep.startswith("http"):
            ep = "https://" + ep

        auth   = oss2.StsAuth(ak, sk, token)
        bucket = oss2.Bucket(auth, ep, bkt)
        log.info("OSS Upload: %s → %s/%s", image_path.name, bkt, oss_key)
        with open(image_path, "rb") as f:
            result = bucket.put_object(oss_key, f)
        if result.status not in (200, 201):
            raise RuntimeError(f"OSS Upload fehlgeschlagen: HTTP {result.status}")


# ─── Foto-Auswahl ─────────────────────────────────────────────────────────────

def get_random_photos(folder: Path, count: int) -> list:
    extensions = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
    all_photos = []
    for ext in extensions:
        all_photos.extend(folder.glob(ext))
        all_photos.extend(folder.glob(f"**/{ext}"))
    all_photos = list(set(all_photos))
    if not all_photos:
        raise RuntimeError(f"Keine Fotos in {folder} gefunden")
    log.info("Fotos gefunden: %d, wähle %d aus", len(all_photos), min(count, len(all_photos)))
    return random.sample(all_photos, min(count, len(all_photos)))


# ─── Konfiguration laden ──────────────────────────────────────────────────────

def load_config():
    config_path = Path.home() / ".aimor_config"
    if config_path.exists():
        cfg = {}
        for line in config_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, _, v = line.partition("=")
                cfg[k.strip()] = v.strip()
        return cfg.get("email", ""), cfg.get("password", ""), cfg.get("photo_folder", "")
    return os.environ.get("AIMOR_EMAIL", ""), os.environ.get("AIMOR_PASSWORD", ""), ""


# ─── Hauptprogramm ────────────────────────────────────────────────────────────

def main():
    import sys
    bind_code = None
    if len(sys.argv) >= 3 and sys.argv[1] == "--bind":
        bind_code = sys.argv[2].replace(" ", "")

    email, password, photo_folder_cfg = load_config()
    if not email or not password:
        print("Fehler: Kein Aimor-Account konfiguriert.")
        print("Erstelle ~/.aimor_config mit:")
        print("  email=deine@email.de")
        print("  password=deinPasswort")
        print("  photo_folder=/mnt/d/OneDrive/Bilder/Eigene Aufnahmen  # optional")
        return

    photo_folder = Path(photo_folder_cfg) if photo_folder_cfg else ONEDRIVE_FOTOS

    client = AimorClient(email, password)
    log.info("=== Aimor Photo Push gestartet ===")

    log.info("Anmelden...")
    client.login()

    log.info("Frames abrufen...")
    frames = client.get_my_frames()
    if not frames:
        log.error("Keine Frames gefunden!")
        return
    log.info("Frames: %s", [f.get("friendlyName", "?") + "/" + f.get("deviceUid", "?") for f in frames])

    frame = frames[0]
    for f in frames:
        if "PF1007" in str(f) or "Mandels" in str(f):
            frame = f
            break
    device_uid = frame.get("deviceUid") or frame.get("uid", "")
    log.info("Verwende Frame: %s (uid=%s)", frame.get("friendlyName", "?"), device_uid)

    # ── Bind-Modus: einmalig als Freund hinzufügen ────────────────────────────
    if bind_code:
        log.info("=== BIND-MODUS: Rahmen als Freund hinzufügen ===")
        client.netty_bind_frame(device_uid, bind_code)
        log.info("=== Bind abgeschlossen ===")
        return

    # Neue Fotos auswählen und senden
    log.info("Fotos aus %s laden...", photo_folder)
    photos = get_random_photos(photo_folder, FOTOS_PRO_RUN)

    task_push_infos = []
    sent   = 0
    failed = 0
    for photo in photos:
        try:
            task_id, oss_id, filename, file_size = client.send_photo(device_uid, photo)
            task_push_infos.append((task_id, oss_id, filename, file_size))
            sent += 1
            time.sleep(1)
        except Exception as e:
            log.error("Fehler bei %s: %s", photo.name, e)
            failed += 1

    log.info("REST-Upload: Gesendet=%d, Fehler=%d", sent, failed)

    # Netty Push — Frame über neue Fotos benachrichtigen
    if task_push_infos:
        log.info("Sende Netty Push für %d Fotos...", len(task_push_infos))
        client.netty_push_all(device_uid, task_push_infos)

    log.info("=== Fertig! Gesendet: %d, Fehler: %d ===", sent, failed)


if __name__ == "__main__":
    main()
