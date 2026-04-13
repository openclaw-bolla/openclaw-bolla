#!/usr/bin/env python3
"""Erzeugt ein PDF mit allen Accounts rund um OpenClaw + Claude Code."""
from datetime import date
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)

OUT_LOCAL = Path("/home/bolla/workspace/docs/accounts_overview.pdf")
OUT_ONEDRIVE = Path("/mnt/d/OneDrive/Dokumente/Bolla/accounts_overview.pdf")

CONFIGS = [
    ("ernstmandel@outlook.de", "Microsoft 365 / Outlook-Mail, Kalender, OneDrive (Graph API)", "ms_token.json, email.json"),
    ("chrismandel13@gmail.com", "Gmail / Google Calendar (OAuth)", "google_client.json, google_token.json"),
    ("chrismandel@wtnet.de", "wtnet Mail (IMAP/SMTP, Spam-Watcher)", "wtnet_account.json"),
    ("Azure Speech (Speech_bolla1, North Europe)", "TTS für Mission Control", "azure_speech.json"),
    ("Telegram-Bot", "Bolla-Bot in Familien-Gruppe", "telegram_bot.json"),
]

EXTERNAL = [
    ("GitHub", "openclaw-bolla (Org), Repo openclaw-bolla/openclaw-bolla privat", "Backup von ~/.claude + workspace"),
    ("Cloudflare", "mandel-bolla.cloudflareaccess.com (Account auf ernstmandel@outlook.de)", "Tunnel + Access für bolla.chrismandel.de"),
    ("IONOS", "Webhosting home31919270.1and1-data.host, User p8002904", "Hosting chrismandel.de + WordPress"),
    ("Domain chrismandel.de", "bei IONOS registriert, Nameserver auf Cloudflare (aldo/angelina)", "DNS via Cloudflare, Mail bleibt IONOS"),
    ("Anthropic / Claude Code", "dein Anthropic-Account", "Claude CLI Login"),
    ("Microsoft Azure", "Subscription auf ernstmandel@outlook.de", "Speech Resource"),
    ("OneDrive", "D:\\OneDrive\\Dokumente\\Bolla\\", "Backup-Ziel ~/.claude"),
]

ROTATE = [
    "Azure Speech Key (am 12.04.2026 im Chat geteilt)",
    "IONOS SFTP-Passwort (am 12.04.2026 im Chat geteilt)",
]


def build(out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="Accounts-Übersicht — OpenClaw / Claude Code",
        author="Bolla für Chris Mandel",
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=18, spaceAfter=14, textColor=colors.HexColor("#1a3a5c"))
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=13, spaceBefore=18, spaceAfter=8, textColor=colors.HexColor("#1a3a5c"))
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10, leading=13)
    small = ParagraphStyle("small", parent=styles["BodyText"], fontSize=8, leading=10, textColor=colors.grey)

    story = []
    story.append(Paragraph("🐾 Accounts-Übersicht — OpenClaw / Claude Code", h1))
    story.append(Paragraph(f"Stand: {date.today().strftime('%d.%m.%Y')} · Erstellt von Bolla für Chris Mandel", small))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Diese Übersicht listet alle Accounts und Zugänge, die mit OpenClaw, "
        "Claude Code und Mission Control zusammenhängen. Tokens und Passwörter "
        "selbst stehen <b>nicht</b> in diesem Dokument — die liegen ausschließlich "
        "in <font face='Courier'>~/workspace/config/</font> (chmod 600, gitignored).",
        body,
    ))

    def make_table(data, col_widths):
        t = Table([[Paragraph(c, body) for c in row] for row in data], colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1a3a5c")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f0f4f8")]),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("GRID", (0,0), (-1,-1), 0.25, colors.HexColor("#cccccc")),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        return t

    story.append(Paragraph("🔑 Zugänge in ~/workspace/config/", h2))
    story.append(Paragraph("Alle chmod 600, gitignored. Kein Token landet je in Logs oder Repos.", small))
    story.append(Spacer(1, 0.2*cm))
    story.append(make_table(
        [["Account", "Zweck", "Datei"]] + [list(r) for r in CONFIGS],
        [5.5*cm, 6*cm, 5*cm],
    ))

    story.append(Paragraph("🌐 Externe Dienste", h2))
    story.append(make_table(
        [["Dienst", "Account / Identifier", "Zweck"]] + [list(r) for r in EXTERNAL],
        [4.5*cm, 6*cm, 6*cm],
    ))

    story.append(Paragraph("🔄 Token-Rotation-Backlog", h2))
    for item in ROTATE:
        story.append(Paragraph(f"• {item}", body))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "Sicherheitsregeln: Tokens nie manuell in Configs eintragen, nie in Logs/Git/Chat, "
        "Passwort-Dateien immer chmod 600. E-Mail-Versand standardmäßig nur über "
        "ernstmandel@outlook.de — bei anderen Konten erst rückfragen.",
        small,
    ))

    doc.build(story)
    print(f"✅ {out_path}  ({out_path.stat().st_size//1024} KB)")


if __name__ == "__main__":
    build(OUT_LOCAL)
    try:
        build(OUT_ONEDRIVE)
    except Exception as e:
        print(f"⚠️  OneDrive-Kopie fehlgeschlagen: {e}")
