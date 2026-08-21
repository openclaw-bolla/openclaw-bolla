#!/usr/bin/env bash
# EN/DE-Paritätscheck für chrismandel.de — IMMER vor jedem `wrangler pages deploy` laufen lassen.
#
# Prüft:
#   1. Jede DE-Seite (Top-Level-Ordner mit index.html) hat ein registriertes EN-Pendant.
#   2. Das EN-Pendant existiert tatsächlich als Datei.
#   3. DE ist nicht neuer (mtime) als EN, ohne dass EN nachgezogen wurde.
#
# Neue Seite hinzugefügt? -> In MAPPING unten eintragen, sonst bricht der Check ab (Absicht:
# so vergisst man die EN-Version nicht mehr).

set -uo pipefail
cd "$(dirname "$0")/.."

# DE-Ordner -> EN-Ordner (relativ zu Repo-Root). "index" = Startseite.
declare -A MAPPING=(
  ["aurora"]="en/aurora"
  ["geschichte"]="en/essay"
  ["impressum"]="en/impressum"
  ["ki-forum"]="en/dialogue"
)

fail=0

# 1) Gibt es DE-Seiten, die in MAPPING fehlen? (= neue Seite ohne EN-Registrierung)
for dir in */ ; do
  d="${dir%/}"
  [[ "$d" == "en" || "$d" == "assets" || "$d" == "scripts" ]] && continue
  [[ -f "$d/index.html" ]] || continue
  if [[ -z "${MAPPING[$d]:-}" ]]; then
    echo "❌ NEUE DE-SEITE OHNE EN-REGISTRIERUNG: '$d/index.html' — in scripts/check_en_parity.sh MAPPING eintragen und en/$d/ anlegen."
    fail=1
  fi
done
# 1b) Startseite als Sonderfall (liegt direkt im Root, kein Unterordner)
de_mtime=$(stat -c %Y "index.html")
en_mtime=$(stat -c %Y "en/index.html")
de_lines=$(wc -l < "index.html")
en_lines=$(wc -l < "en/index.html")
status="ok"
if [[ "$de_mtime" -gt "$en_mtime" ]]; then
  status="⚠️  DE neuer als EN — prüfen ob EN nachgezogen wurde!"
  fail=1
fi
diff_lines=$(( de_lines > en_lines ? de_lines - en_lines : en_lines - de_lines ))
if [[ "$diff_lines" -gt 15 ]]; then
  status="$status ⚠️  Zeilenzahl weicht stark ab (DE:$de_lines / EN:$en_lines)."
  fail=1
fi
echo "index.html <-> en/index.html : DE=$de_lines EN=$en_lines  $status"

# 2) Für jede registrierte Unterseite: existiert EN, ist EN nicht älter als DE?
for de in "${!MAPPING[@]}"; do
  en="${MAPPING[$de]}"
  de_file="$de/index.html"
  en_file="$en/index.html"
  if [[ ! -f "$de_file" ]]; then
    echo "⚠️  In MAPPING registriert, aber DE-Datei fehlt: $de_file"
    continue
  fi
  if [[ ! -f "$en_file" ]]; then
    echo "❌ EN-PENDANT FEHLT: $de_file hat kein $en_file"
    fail=1
    continue
  fi
  de_mtime=$(stat -c %Y "$de_file")
  en_mtime=$(stat -c %Y "$en_file")
  de_lines=$(wc -l < "$de_file")
  en_lines=$(wc -l < "$en_file")
  status="ok"
  if [[ "$de_mtime" -gt "$en_mtime" ]]; then
    status="⚠️  DE neuer als EN — prüfen ob EN nachgezogen wurde!"
    fail=1
  fi
  diff_lines=$(( de_lines > en_lines ? de_lines - en_lines : en_lines - de_lines ))
  if [[ "$diff_lines" -gt 15 ]]; then
    status="$status ⚠️  Zeilenzahl weicht stark ab (DE:$de_lines / EN:$en_lines) — evtl. unvollständig übersetzt."
    fail=1
  fi
  echo "$de_file <-> $en_file : DE=$de_lines EN=$en_lines  $status"
done

echo ""
if [[ "$fail" -eq 1 ]]; then
  echo "🔴 Parity-Check FEHLGESCHLAGEN — vor dem Deploy die obigen Punkte klären."
  exit 1
else
  echo "🟢 Parity-Check OK — alle DE-Seiten haben ein aktuelles EN-Pendant."
  exit 0
fi
