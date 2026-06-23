#!/usr/bin/env python3
"""
Bolla Telegram Bot 🐾
Lauscht in der Familiengruppe und antwortet via Claude Code.
Reagiert auf Erwähnungen von "bolla" oder direkte Antworten auf Bolla-Nachrichten.
ADB-Befehle für Surface Duo 2 Steuerung.
"""

import base64
import json
import logging
import mimetypes
import os
import subprocess
import requests
import time
import tempfile

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "telegram_bot.json")
with open(CONFIG_FILE) as f:
    _cfg = json.load(f)

BOT_TOKEN = _cfg["bot_token"]
GROUP_CHAT_ID = _cfg["group_chat_id"]
CHRIS_ID = _cfg["chris_id"]
BOT_ID = _cfg["bot_id"]
BOT_USERNAME = "bolla_mandel_bot"

LOG_FILE = os.path.expanduser("~/workspace/logs/telegram_bot.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("telegram_bot")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# --- AURORA Stolperstein-Archiv (Sätze zum späteren Fable-5-Lektorat) ---------
STOLPER_FILE = os.path.expanduser("~/workspace/data/aurora_stolpersteine.jsonl")
AZURE_SPEECH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "azure_speech.json")
# Trigger-Präfixe (case-insensitive, am Anfang der Nachricht / des Transkripts)
SATZ_TRIGGERS = ("satz:", "satz ", "stolperstein:", "stolperstein ", "📌")
# Sammel-Modus: solange das Flag existiert, wird JEDE Nachricht von Chris archiviert (Copy-Paste ohne Präfix)
SAMMEL_FLAG = os.path.expanduser("~/workspace/data/.aurora_sammelmodus")
SAMMEL_AN = ("sammeln", "sammeln an", "satz sammeln", "sammelmodus", "sammelmodus an", "lesen", "sammeln starten")
SAMMEL_AUS = ("fertig", "sammeln aus", "sammelmodus aus", "sammeln stop", "sammeln beenden", "ende sammeln")


def get_updates(offset=None):
    params = {"timeout": 30, "allowed_updates": ["message"]}
    if offset:
        params["offset"] = offset
    try:
        r = requests.get(f"{API}/getUpdates", params=params, timeout=35)
        return r.json().get("result", [])
    except Exception as e:
        log.error(f"getUpdates Fehler: {e}")
        return []


def send_message(chat_id, text, reply_to=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_to:
        data["reply_to_message_id"] = reply_to
    try:
        r = requests.post(f"{API}/sendMessage", json=data, timeout=10)
        return r.json()
    except Exception as e:
        log.error(f"sendMessage Fehler: {e}")
        return None


def send_photo(chat_id, photo_path, caption=None, reply_to=None):
    data = {"chat_id": chat_id}
    if caption:
        data["caption"] = caption
    if reply_to:
        data["reply_to_message_id"] = reply_to
    try:
        with open(photo_path, "rb") as f:
            r = requests.post(f"{API}/sendPhoto", data=data, files={"photo": f}, timeout=30)
        return r.json()
    except Exception as e:
        log.error(f"sendPhoto Fehler: {e}")
        return None


def get_file_url(file_id):
    """Holt den Download-Link für eine Telegram-Datei."""
    try:
        r = requests.get(f"{API}/getFile", params={"file_id": file_id}, timeout=10)
        data = r.json()
        if data.get("ok"):
            return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{data['result']['file_path']}"
    except Exception as e:
        log.error(f"getFile Fehler: {e}")
    return None


def download_telegram_file(file_id, suffix=""):
    """Lädt eine Telegram-Datei herunter. Gibt lokalen Pfad zurück oder None."""
    url = get_file_url(file_id)
    if not url:
        return None
    try:
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        ext = suffix or os.path.splitext(url.split("?")[0])[-1] or ".bin"
        with tempfile.NamedTemporaryFile(suffix=ext, prefix="bolla_tg_", delete=False) as tmp:
            tmp.write(r.content)
            return tmp.name
    except Exception as e:
        log.error(f"Download Fehler: {e}")
    return None


def extract_media(msg):
    """Gibt (file_id, suffix, label) zurück oder None."""
    if "photo" in msg:
        photo = msg["photo"][-1]  # größtes verfügbares Foto
        return photo["file_id"], ".jpg", "Foto"
    if "document" in msg:
        doc = msg["document"]
        mime = doc.get("mime_type", "")
        suffix = mimetypes.guess_extension(mime) or ".bin"
        if not suffix.startswith("."):
            suffix = "." + suffix
        return doc["file_id"], suffix, f"Dokument ({doc.get('file_name', 'unbekannt')})"
    if "sticker" in msg:
        return msg["sticker"]["file_id"], ".webp", "Sticker"
    if "video" in msg:
        return msg["video"]["file_id"], ".mp4", "Video"
    if "voice" in msg:
        return msg["voice"]["file_id"], ".ogg", "Sprachnachricht"
    if "audio" in msg:
        return msg["audio"]["file_id"], ".mp3", "Audio"
    return None


def _now_iso():
    """Lokaler Zeitstempel (Date.now ist im Skript ok — kein Workflow-Resume)."""
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def archive_satz(text, source="text"):
    """Hängt einen Stolperstein-Satz an die JSONL-Sammeldatei an. Gibt die laufende Nummer zurück."""
    text = (text or "").strip()
    if not text:
        return None
    os.makedirs(os.path.dirname(STOLPER_FILE), exist_ok=True)
    entry = {"ts": _now_iso(), "source": source, "text": text, "status": "offen"}
    with open(STOLPER_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return count_saetze()


def _read_saetze():
    if not os.path.isfile(STOLPER_FILE):
        return []
    out = []
    with open(STOLPER_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def count_saetze():
    return len(_read_saetze())


def undo_last_satz():
    """Entfernt den letzten Eintrag. Gibt den gelöschten Text zurück oder None."""
    rows = _read_saetze()
    if not rows:
        return None
    removed = rows.pop()
    with open(STOLPER_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return removed.get("text", "")


def sammelmodus_an():
    open(SAMMEL_FLAG, "w").close()


def sammelmodus_aus():
    try:
        os.unlink(SAMMEL_FLAG)
    except OSError:
        pass


def sammelmodus_ist_an():
    return os.path.isfile(SAMMEL_FLAG)


def transcribe_voice(ogg_path):
    """Transkribiert eine Telegram-Sprachnachricht (.ogg) via Azure Speech STT (Deutsch).
    Gibt den erkannten Text zurück oder None."""
    try:
        with open(AZURE_SPEECH_FILE) as f:
            cfg = json.load(f)
        key, region = cfg["key"], cfg["region"]
    except Exception as e:
        log.error(f"Azure-Speech-Config fehlt: {e}")
        return None
    wav_path = ogg_path + ".wav"
    try:
        # OGG/Opus -> WAV PCM 16 kHz mono (von Azure STT verlangt)
        subprocess.run(["ffmpeg", "-y", "-i", ogg_path, "-ar", "16000", "-ac", "1", wav_path],
                       capture_output=True, timeout=30)
        url = (f"https://{region}.stt.speech.microsoft.com/speech/recognition/"
               f"conversation/cognitiveservices/v1?language=de-DE&format=simple")
        headers = {"Ocp-Apim-Subscription-Key": key,
                   "Content-Type": "audio/wav; codecs=audio/pcm; samplerate=16000"}
        with open(wav_path, "rb") as wf:
            r = requests.post(url, headers=headers, data=wf, timeout=30)
        data = r.json()
        if data.get("RecognitionStatus") == "Success":
            return data.get("DisplayText", "").strip()
        log.error(f"Azure STT: {data.get('RecognitionStatus')}")
        return None
    except Exception as e:
        log.error(f"Transkription Fehler: {e}")
        return None
    finally:
        for p in (wav_path,):
            try:
                os.unlink(p)
            except OSError:
                pass


def strip_satz_trigger(text):
    """Wenn text mit einem Satz-Trigger beginnt: gibt (True, rest) zurück, sonst (False, text)."""
    low = text.strip().lower()
    for trig in SATZ_TRIGGERS:
        if low.startswith(trig):
            return True, text.strip()[len(trig):].strip(" :")
    return False, text


def handle_satz_command(text, sender_id, chat_id, msg_id):
    """Verarbeitet Stolperstein-Befehle (nur Chris). Gibt True zurück wenn behandelt."""
    if sender_id != int(CHRIS_ID):
        return False
    low = text.strip().lower()

    # Sammel-Modus AN
    if low in SAMMEL_AN:
        sammelmodus_an()
        send_message(chat_id,
            "📚 Sammel-Modus AN. Kipp jetzt Sätze rein — auch per Copy-Paste, ganz ohne Präfix. "
            "Jeder wird archiviert (ich antworte NICHT inhaltlich). Beenden mit »fertig«.", reply_to=msg_id)
        return True

    # Sammel-Modus AUS
    if low in SAMMEL_AUS:
        war_an = sammelmodus_ist_an()
        sammelmodus_aus()
        if war_an:
            send_message(chat_id, f"✅ Sammel-Modus aus. Insgesamt {count_saetze()} Stolperstein(e) archiviert.", reply_to=msg_id)
        else:
            send_message(chat_id, "Sammel-Modus war nicht an. 🐾", reply_to=msg_id)
        return True

    # Status / Liste
    if low in ("sätze", "saetze", "satzliste", "stolpersteine"):
        rows = _read_saetze()
        if not rows:
            send_message(chat_id, "📋 Noch keine Stolpersteine archiviert.", reply_to=msg_id)
            return True
        letzte = rows[-5:]
        lines = [f"📋 {len(rows)} Stolperstein(e) gesammelt. Die letzten:"]
        start = len(rows) - len(letzte) + 1
        for i, r in enumerate(letzte):
            t = r.get("text", "")
            lines.append(f"  {start+i}. {t[:70]}" + ("…" if len(t) > 70 else ""))
        send_message(chat_id, "\n".join(lines), reply_to=msg_id)
        return True

    # Undo
    if low in ("satz undo", "satz lösch letzten", "satz loesch letzten", "satz rückgängig", "satz zurück"):
        removed = undo_last_satz()
        if removed is None:
            send_message(chat_id, "Nichts zum Rückgängigmachen da. 🐾", reply_to=msg_id)
        else:
            send_message(chat_id, f"🗑️ Letzten Stolperstein entfernt:\n»{removed[:80]}«\nJetzt {count_saetze()} gespeichert.", reply_to=msg_id)
        return True

    # Erfassung per Trigger-Präfix
    is_satz, rest = strip_satz_trigger(text)
    if is_satz:
        if not rest:
            send_message(chat_id, "Kein Satz dabei — schick mir z.B. »satz: Der Satz, der dir aufgefallen ist.«", reply_to=msg_id)
            return True
        nr = archive_satz(rest, source="text")
        send_message(chat_id, f"📌 Stolperstein #{nr} archiviert:\n»{rest[:90]}" + ("…" if len(rest) > 90 else "") + "«", reply_to=msg_id)
        return True

    # Sammel-Modus aktiv → diese (präfixlose) Nachricht ist ein Satz, kein Job
    if sammelmodus_ist_an():
        nr = archive_satz(text, source="text")
        send_message(chat_id, f"📌 #{nr}", reply_to=msg_id)
        return True

    return False


def adb_connected():
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.strip().split("\n")[1:]:
            if "\tdevice" in line:
                return True
    except Exception:
        pass
    return False


def adb_reconnect(ip="192.168.178.20"):
    try:
        result = subprocess.run(["adb", "connect", f"{ip}:5555"], capture_output=True, text=True, timeout=10)
        return "connected" in result.stdout.lower()
    except Exception:
        return False


def adb_command(cmd_args, timeout=15):
    try:
        result = subprocess.run(["adb"] + cmd_args, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.returncode == 0
    except Exception as e:
        return str(e), False


def handle_adb_command(text_lower, chat_id, msg_id):
    """Verarbeitet ADB-Befehle. Gibt True zurück wenn ein Befehl erkannt wurde."""

    ADB_KEYWORDS = {"screenshot", "bildschirm", "screen", "apps", "app-liste",
                    "appliste", "app liste", "speicher", "storage", "speicherplatz",
                    "akku", "batterie", "battery", "handy", "duo", "handy hilfe",
                    "adb hilfe", "adb help", "adb disconnect", "adb trennen"}

    is_adb = text_lower in ADB_KEYWORDS or text_lower.startswith("adb connect ")
    if not is_adb:
        return False

    # adb connect braucht keine bestehende Verbindung
    if text_lower.startswith("adb connect "):
        addr = text_lower.replace("adb connect ", "").strip()
        output, ok = adb_command(["connect", addr], timeout=10)
        if ok and "connected" in output.lower():
            send_message(chat_id, f"✅ Verbunden mit {addr}! 📱", reply_to=msg_id)
        else:
            send_message(chat_id, f"❌ Verbindung zu {addr} fehlgeschlagen.\n{output}", reply_to=msg_id)
        return True

    # Für alle anderen ADB-Befehle: Verbindung prüfen
    if not adb_connected():
        send_message(chat_id,
            "📱 Keine ADB-Verbindung zum Surface Duo 2!\n\n"
            "Schau auf dem Duo unter:\n"
            "Einstellungen → Entwickleroptionen → WLAN-Debugging\n\n"
            "Schick mir: `adb connect IP:PORT`", reply_to=msg_id)
        return True

    # Screenshot
    if text_lower in ("screenshot", "bildschirm", "screen"):
        requests.post(f"{API}/sendChatAction", json={"chat_id": chat_id, "action": "upload_photo"})
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        adb_command(["shell", "screencap", "-p", "/sdcard/_bolla_screenshot.png"])
        output, ok = adb_command(["pull", "/sdcard/_bolla_screenshot.png", tmp_path])
        adb_command(["shell", "rm", "/sdcard/_bolla_screenshot.png"])
        if ok:
            send_photo(chat_id, tmp_path, caption="📱 Surface Duo 2 Screenshot", reply_to=msg_id)
        else:
            send_message(chat_id, "Screenshot fehlgeschlagen 😕", reply_to=msg_id)
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        return True

    # App-Liste
    if text_lower in ("apps", "app-liste", "appliste", "app liste"):
        output, ok = adb_command(["shell", "pm", "list", "packages", "-3"], timeout=30)
        if ok:
            apps = sorted([line.replace("package:", "") for line in output.split("\n") if line.strip()])
            categories = {
                "🤖 KI/Tech": ["claude", "chatgpt", "copilot", "perplexity", "bard", "deepl", "openai"],
                "🎬 Streaming": ["netflix", "disney", "amazon.avod", "spotify", "zdf", "daserste", "ard", "ndr", "swr", "mediathek"],
                "💰 Finanzen": ["traderepublic", "coinbase", "paypal", "mobilbanking", "pushtan", "lbb"],
                "🚗 Mobilität": ["tesla", "weconnect", "db.pw", "hafas", "sixt", "adac", "ionity", "enbw", "aral", "fahrinfo"],
                "🛒 Shopping": ["amazon.mShop", "ebay", "ikea", "rewe", "edeka", "lidl", "media.markt", "lieferando", "penny", "home24"],
                "💬 Social": ["whatsapp", "instagram", "facebook", "telegram", "snapchat", "musically", "discord", "bereal", "linkedin"],
                "🎮 Gaming": ["minecraft", "subwaysurf", "solitaire", "steam", "xbox", "xcloud"],
                "✈️ Reisen": ["booking", "expedia", "tripadvisor", "lastminute", "lufthansa", "tui", "meinschiff", "opentable", "gpsmycity"],
                "🏠 Smart Home": ["devolo", "sonos", "eq3", "ninebot", "elink.robot"],
                "📰 News/Wetter": ["tagesschau", "sportschau", "wetteronline", "hoerzu", "njoy"],
            }
            msg = f"📱 {len(apps)} Apps auf Surface Duo 2:\n\n"
            categorized = set()
            for cat_name, keywords in categories.items():
                matched = [a for a in apps if any(kw in a.lower() for kw in keywords)]
                if matched:
                    msg += f"{cat_name}:\n"
                    for a in matched:
                        short = a.split(".")[-1] if "." in a else a
                        msg += f"  • {short}\n"
                    msg += "\n"
                    categorized.update(matched)
            rest = [a for a in apps if a not in categorized]
            if rest:
                msg += f"📦 Sonstige ({len(rest)}):\n"
                for a in rest:
                    short = a.split(".")[-1] if "." in a else a
                    msg += f"  • {short}\n"
            if len(msg) > 4000:
                msg = msg[:4000] + "\n\n... (gekürzt)"
            send_message(chat_id, msg, reply_to=msg_id)
        else:
            send_message(chat_id, "App-Liste konnte nicht abgerufen werden 😕", reply_to=msg_id)
        return True

    # Speicher
    if text_lower in ("speicher", "storage", "speicherplatz"):
        output, ok = adb_command(["shell", "df", "-h", "/data"])
        if ok:
            send_message(chat_id, f"📱 Speicher Surface Duo 2:\n\n{output}", reply_to=msg_id)
        else:
            send_message(chat_id, "Speicherinfo nicht verfügbar 😕", reply_to=msg_id)
        return True

    # Akku
    if text_lower in ("akku", "batterie", "battery"):
        output, ok = adb_command(["shell", "dumpsys", "battery"])
        if ok:
            lines = output.split("\n")
            info = {}
            for line in lines:
                if "level" in line.lower():
                    info["level"] = line.strip().split(":")[-1].strip()
                if "status" in line.lower():
                    status_code = line.strip().split(":")[-1].strip()
                    status_map = {"2": "Lädt ⚡", "3": "Entlädt", "5": "Voll ✅"}
                    info["status"] = status_map.get(status_code, status_code)
                if "temperature" in line.lower():
                    temp = line.strip().split(":")[-1].strip()
                    try:
                        info["temp"] = f"{int(temp)/10:.1f}°C"
                    except ValueError:
                        info["temp"] = temp
            msg = f"🔋 Surface Duo 2 Akku:\n\n"
            msg += f"Ladung: {info.get('level', '?')}%\n"
            msg += f"Status: {info.get('status', '?')}\n"
            msg += f"Temperatur: {info.get('temp', '?')}"
            send_message(chat_id, msg, reply_to=msg_id)
        else:
            send_message(chat_id, "Akku-Info nicht verfügbar 😕", reply_to=msg_id)
        return True

    # ADB disconnect
    if text_lower in ("adb disconnect", "adb trennen"):
        adb_command(["disconnect"])
        send_message(chat_id, "📱 ADB-Verbindung getrennt.", reply_to=msg_id)
        return True

    # Handy-Befehle Hilfe
    if text_lower in ("handy", "duo", "handy hilfe", "adb hilfe", "adb help"):
        msg = ("📱 Surface Duo 2 Befehle:\n\n"
               "• screenshot — Bildschirmfoto\n"
               "• apps — Installierte Apps\n"
               "• speicher — Speicherplatz\n"
               "• akku — Batterie-Status\n"
               "• adb connect IP:PORT — Neu verbinden\n"
               "• adb disconnect — Trennen")
        send_message(chat_id, msg, reply_to=msg_id)
        return True

    return False


def interactive_claude_running():
    """True wenn eine *interaktive* Claude-Session an einem echten Terminal läuft.

    Hinweis: Claude Code überschreibt seinen Prozessnamen mit 'claude' und
    versteckt die Startargumente — '-p'/'--print' sind in ps NICHT sichtbar
    (auch nicht in /proc/PID/cmdline). Die alte Heuristik per ' -p ' im
    Befehl konnte interaktive Sessions deshalb nie von Hintergrund-Calls
    unterscheiden und meldete praktisch immer True. Wir unterscheiden jetzt
    am TTY: eine echte interaktive Session hängt an einem Terminal (pts/*),
    ein vom Daemon gestarteter 'claude -p' Call hat keins ('?')."""
    try:
        r = subprocess.run(["ps", "-eo", "tty=,comm="], capture_output=True, text=True)
        for line in r.stdout.split("\n"):
            parts = line.split()
            if len(parts) < 2:
                continue
            tty, comm = parts[0], parts[1]
            if comm == "claude" and tty.startswith("pts"):
                return True
    except Exception:
        pass
    return False


def ask_claude(message, sender_name, file_path=None, media_label=None):
    """Fragt Claude Code und gibt die Antwort zurück.

    Hinweis: 'claude -p' läuft problemlos PARALLEL zu einer interaktiven
    Terminal-Session (gemessen: ~3s parallel). Daher KEIN Session-Check mehr —
    der senkte früher nur unnötig den Timeout und produzierte irreführende
    'aktive Session'-Fehlmeldungen. Funktioniert jetzt wie der MC-Bolla-Chat.
    """
    if file_path and media_label:
        prompt = (f"[Telegram-Nachricht von {sender_name}]: {message or '(kein Text)'}\n\n"
                  f"[Angehängtes {media_label}: {file_path} — bitte lesen und analysieren/beschreiben]")
    else:
        prompt = f"[Telegram-Nachricht von {sender_name}]: {message}"
    claude_bin = os.path.expanduser("~/.local/bin/claude")
    cmd = [claude_bin, "-p", "--output-format", "json", prompt]
    timeout = 180
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=os.path.expanduser("~")
        )
        if result.returncode != 0:
            log.error(f"Claude Fehler: {result.stderr[:200]}")
            return None
        data = json.loads(result.stdout)
        return data.get("result", "")
    except subprocess.TimeoutExpired:
        return "Sorry, das hat zu lange gedauert — versuch's nochmal! 🐾"
    except Exception as e:
        log.error(f"Claude Fehler: {e}")
        return None


def should_respond(msg):
    """Prüft ob Bolla auf diese Nachricht reagieren soll."""
    text = (msg.get("text", "") or msg.get("caption", "")).lower()

    # Direktnachrichten: immer antworten
    if msg.get("chat", {}).get("type") == "private":
        return True

    # Gruppen (inkl. Familiengruppe): nur bei Erwähnung oder Antwort auf Bolla
    reply = msg.get("reply_to_message", {})
    if reply.get("from", {}).get("id") == BOT_ID:
        return True
    if "bolla" in text or f"@{BOT_USERNAME}" in msg.get("text", ""):
        return True

    return False


def main():
    log.info("Bolla Telegram Bot gestartet 🐾")
    adb_was_connected = adb_connected()

    offset = None
    check_counter = 0
    while True:
        updates = get_updates(offset)

        # Alle 10 Polling-Zyklen (~5 Min) ADB-Verbindung prüfen
        check_counter += 1
        if check_counter >= 10:
            check_counter = 0
            is_connected = adb_connected()
            if adb_was_connected and not is_connected:
                log.info("ADB-Verbindung verloren!")
                send_message(CHRIS_ID,
                    "📱⚠️ ADB-Verbindung zum Surface Duo 2 verloren!\n\n"
                    "Schick mir die neue Adresse:\n"
                    "`adb connect IP:PORT`\n\n"
                    "(Einstellungen → Entwickleroptionen → WLAN-Debugging)")
            adb_was_connected = is_connected

        for update in updates:
            offset = update["update_id"] + 1
            msg = update.get("message")
            if not msg:
                continue

            sender = msg.get("from", {})
            sender_name = sender.get("first_name", "Jemand")
            sender_id = sender.get("id", 0)
            text = msg.get("text") or msg.get("caption") or ""
            chat_id = msg["chat"]["id"]
            msg_id = msg["message_id"]
            media = extract_media(msg)

            # Eigene Nachrichten ignorieren
            if sender_id == BOT_ID:
                continue

            # Nachrichten ohne Text und ohne Medien überspringen
            if not text and not media:
                continue

            log.info(f"[{sender_name}]: {text[:100]}" + (f" [{media[2]}]" if media else ""))

            if should_respond(msg):
                log.info(f"Antworte auf: {text[:80]}" + (f" [{media[2]}]" if media else ""))

                # Sprachnachricht von Chris: per Azure transkribieren → ab hier wie Text behandeln
                if media and media[2] == "Sprachnachricht" and sender_id == int(CHRIS_ID):
                    requests.post(f"{API}/sendChatAction", json={"chat_id": chat_id, "action": "typing"})
                    ogg = download_telegram_file(media[0], ".ogg")
                    transcript = transcribe_voice(ogg) if ogg else None
                    if ogg:
                        try:
                            os.unlink(ogg)
                        except OSError:
                            pass
                    if not transcript:
                        send_message(chat_id, "Konnte die Sprachnachricht nicht verstehen 😕 — nochmal?", reply_to=msg_id)
                        continue
                    log.info(f"Voice transkribiert: {transcript[:80]}")
                    text = transcript
                    media = None  # weiter wie eine normale Textnachricht

                # AURORA-Stolperstein zuerst (Sammel-Modus/Präfix/Steuerbefehle) — vor ADB & Claude
                if not media and handle_satz_command(text, sender_id, chat_id, msg_id):
                    continue

                # ADB-Befehle (nur von Chris, nur bei reinem Text)
                if not media and sender_id == int(CHRIS_ID) and handle_adb_command(text.strip().lower(), chat_id, msg_id):
                    continue

                # "Tippt..." Indikator
                requests.post(f"{API}/sendChatAction",
                              json={"chat_id": chat_id, "action": "typing"})

                local_path = None
                media_label = None
                if media:
                    file_id, suffix, media_label = media
                    log.info(f"Lade {media_label} herunter...")
                    local_path = download_telegram_file(file_id, suffix)
                    if not local_path:
                        send_message(chat_id, "Konnte die Datei nicht herunterladen 😕", reply_to=msg_id)
                        continue

                try:
                    reply = ask_claude(text, sender_name, local_path, media_label)
                finally:
                    if local_path:
                        try:
                            os.unlink(local_path)
                        except OSError:
                            pass

                if reply:
                    send_message(chat_id, reply, reply_to=msg_id)
                else:
                    send_message(chat_id, "Da ging was schief — bin aber da! 🐾", reply_to=msg_id)


if __name__ == "__main__":
    main()
