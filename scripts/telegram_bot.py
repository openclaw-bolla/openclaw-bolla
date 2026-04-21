#!/usr/bin/env python3
"""
Bolla Telegram Bot 🐾
Lauscht in der Familiengruppe und antwortet via Claude Code.
Reagiert auf Erwähnungen von "bolla" oder direkte Antworten auf Bolla-Nachrichten.
ADB-Befehle für Surface Duo 2 Steuerung.
"""

import json
import logging
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


def ask_claude(message, sender_name):
    """Fragt Claude Code und gibt die Antwort zurück."""
    prompt = f"[Telegram-Nachricht von {sender_name}]: {message}"
    claude_bin = os.path.expanduser("~/.local/bin/claude")
    cmd = [claude_bin, "-p", "--output-format", "json", prompt]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120,
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
    text = msg.get("text", "").lower()

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
            if not msg or not msg.get("text"):
                continue

            sender = msg.get("from", {})
            sender_name = sender.get("first_name", "Jemand")
            sender_id = sender.get("id", 0)
            text = msg["text"]
            chat_id = msg["chat"]["id"]
            msg_id = msg["message_id"]

            # Eigene Nachrichten ignorieren
            if sender_id == BOT_ID:
                continue

            log.info(f"[{sender_name}]: {text[:100]}")

            if should_respond(msg):
                log.info(f"Antworte auf: {text[:80]}")

                # ADB-Befehle zuerst prüfen (nur von Chris)
                if sender_id == int(CHRIS_ID) and handle_adb_command(text.strip().lower(), chat_id, msg_id):
                    continue

                # "Tippt..." Indikator
                requests.post(f"{API}/sendChatAction",
                              json={"chat_id": chat_id, "action": "typing"})

                reply = ask_claude(text, sender_name)
                if reply:
                    send_message(chat_id, reply, reply_to=msg_id)
                else:
                    send_message(chat_id, "Da ging was schief — bin aber da! 🐾", reply_to=msg_id)


if __name__ == "__main__":
    main()
