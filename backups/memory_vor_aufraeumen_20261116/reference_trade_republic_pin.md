---
name: reference-trade-republic-pin
description: "Trade Republic PIN ist 4-stellig, nicht 5-stellig wie andere Banken — bei HBCI/WISO-Anmeldungen warnen"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 00128d31-85df-4b33-963d-11d5cdd28af8
  modified: 2026-08-12T07:07:58.120Z
---

Trade Republics Online-PIN (für HBCI/FinTS-Zugriff, z.B. in WISO Mein Geld) ist **4-stellig** — anders als bei Chris' anderen Banken, wo 5-stellige PINs üblich sind.

**Why:** Beim WISO-Trade-Republic-Depotsync-Problem (12.08.2026) tippte Chris versehentlich eine 5-stellige PIN ein (Gewohnheit von anderen Banken), was die Meldung "Falsche PIN/Telefonnummer" auslöste. Nach Umstellung auf 4-stellig lief die Anmeldung durch.

**How to apply:** Wenn Chris künftig bei Trade Republic (WISO-HBCI-Einrichtung, Zugangsart neu ermitteln o.ä.) eine PIN eingeben muss und es zu Anmeldefehlern kommt, proaktiv an die 4-Stelligkeit erinnern — nicht erst wenn der Fehler schon auftritt.
