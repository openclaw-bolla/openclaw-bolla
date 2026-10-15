#!/usr/bin/env python3
"""AURORA II — R2 (Spannung/Humor) + R3 (Kontinuität) für Kap. 1-12 nachgeholt (Chris-Go 15.10.2026), damit 1-24 einheitlich durch sind.
Nutzt Gating/Policy des Figuren-Pass (Wochen-Cap 83 %, 5h<=50 %). Kap. 1-8: s.make_allow-Regel (nur Grammatik/Tippfehler direkt, Rest als Vorschlag)."""
import os, sys
sys.path.insert(0, "/home/bolla/workspace/scripts")
import aurora2_figuren_pass as fp
s = fp.s
s.DEADLINE = fp.dt.datetime(2026, 10, 16, 18, 30)   # vor dem Freitags-Lauf 19:00

def main():
    fp.jobrep("laeuft", "R2+R3 Kap. 1-12 gestartet")
    try:
        for n in range(1, 13):
            fp.r2(n)
        fp.jobrep("laeuft", "R2 Kap. 1-12 fertig; R3")
        for n in range(1, 13):
            fp.r3(n)
        grund, st = "fertig", "ok"
    except s.Stop as e:
        grund, st = f"gestoppt: {e}", "fehler"
    except Exception as e:
        import traceback; fp.log("FEHLER r23: " + traceback.format_exc()); grund, st = "Fehler (Log)", "fehler"
    fp.jobrep(st, f"R2+R3 Kap. 1-12: {grund}")
    fp.log(f"R2/R3 Kap 1-12 Ende: {grund}")

if __name__ == "__main__":
    main()
