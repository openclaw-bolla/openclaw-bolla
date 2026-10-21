#!/bin/bash
# Wochen-Budget-Sperre fuer das Website-Neubau-Projekt (Chris 21.10.2026).
# Grenze = max. Wochen-Verbrauch (seven_day_pct) je Tag: Mi 50, Do 60, Fr 70, sonst 90.
# Exit 0 = weiterarbeiten, Exit 1 = STOPP (Stand sichern). Kostet keine Token.
case "$(date +%Y-%m-%d)" in
  2026-10-21) LIM=50;; 2026-10-22) LIM=60;; 2026-10-23) LIM=70;; *) LIM=90;;
esac
Q=$(curl -s --max-time 10 http://127.0.0.1:18790/api/claudequota)
python3 - "$LIM" "$Q" <<'PY'
import sys, json
lim = float(sys.argv[1])
try:
    q = json.loads(sys.argv[2])
except Exception:
    print("QUOTA-FEHLER -> vorsichtshalber STOPP"); sys.exit(1)
w, h = q["seven_day_pct"], q["five_hour_pct"]
stop = w >= lim or h >= 90
print(f"Woche {w}% (Grenze {lim:.0f}%), 5h {h}% -> {'STOPP' if stop else 'ok'}")
sys.exit(1 if stop else 0)
PY
