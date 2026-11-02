---
name: feedback-python-mutable-default-arg
description: "Python-Falle — Default-Parameterwerte werden einmalig bei Funktionsdefinition gebunden, nicht bei jedem Aufruf"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 813902cf-a4a5-48f4-aad8-c5f5b904f5ec
---

Bei `def token(tokf=TOKF):` wird `TOKF` (ein Modul-Global) **einmalig beim Import** in den Default gebunden. Ein späteres `modul.TOKF = anderer_pfad` ändert diesen Default NICHT mehr — jeder Aufruf `modul.token()` ohne explizites Argument nutzt weiterhin den alten Wert.

**Why:** Beim Einrichten von Renis Outlook-Zugriff (08.07.2026) habe ich genau das übersehen: ein Ad-hoc-Testskript setzte `bw.TOKF = Path('renate_outlook_token.json')` und rief dann `bw.token()` ohne Argument auf, in der Annahme, das würde jetzt Renis Token nehmen. Tat es nicht — jede Prüfung lief weiter gegen Chris' Konto (`outlook_token.json`, der ursprüngliche Default). Das sah aus wie ein wiederholt fehlschlagender Login und hat zu **fünf unnötigen Wiederholungs-Logins** bei Chris und Reni geführt, bis der eigentliche Bug (in meinem Testcode, nicht im Login) gefunden wurde.

**How to apply:** Bei jeder Funktion mit einem Default-Parameter, der von einem Modul-Global abgeleitet ist (Pfade, Konfig-Objekte, o.ä.) — IMMER das Argument explizit übergeben, wenn ein anderer Wert als der ursprüngliche Default gebraucht wird, nie auf eine nachträgliche Neuzuweisung des globalen Namens verlassen. Gilt genauso für die klassische Falle mit mutable defaults (`def f(x=[])`). Bei unerklärlichem, konsistent falschem Verhalten über mehrere Wiederholungen hinweg (wie hier: immer dasselbe falsche Konto) zuerst das eigene Prüf-/Testskript verdächtigen, bevor man dem externen Prozess (hier: Login) die Schuld gibt.
