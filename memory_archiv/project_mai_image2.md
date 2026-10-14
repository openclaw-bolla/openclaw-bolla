---
name: MAI-Image-2 für BildGen einbauen
description: Microsoft MAI-Image in Mission Control BildGen — ERLEDIGT, scharfgeschaltet via Azure AI Foundry am 22.06.2026
type: project
originSessionId: ede5c54b-4c1a-4a8e-ad5b-4b9eb8cf6116
---
✅ **ERLEDIGT 22.06.2026:** MAI-Image-2.5 über **Azure AI Foundry** scharfgeschaltet und erfolgreich getestet.

**Setup:**
- Config: `config/mai_image.json` (chmod 600) — Felder: endpoint, api_key, default_model
- Endpoint: `https://bolla-ai-foundry.services.ai.azure.com` ⚠️ NUR die Resource-Basis, NICHT der Foundry-Projekt-Endpoint (`.../api/projects/proj-default`) — der Code hängt `/mai/v1/images/generations` selbst an
- Resource-Name: `bolla-ai-foundry`
- Code-Pfad war längst gebaut: `bildgen_mai_generate()` in mission_control_api.py + Engine-Tab „✨ MAI-Image" in index.html (BildGen). API liest config bei jedem Aufruf frisch → kein Neustart nötig.
- Kosten: ~0,08–0,13€/Bild (pay-per-use, kein Free-Tier) — steht in [[project_kosten]]

**Erster Testlauf:** brain_bg_test.png (data/bildgen_archive/) — Anbindung + Auth ok.

**⚙️ MAI-API-PARAMETER (offizielle MS-Doku, geprüft 22.06.2026 — NICHT raten, das ist verifiziert):**
- generations-Endpoint nimmt **`width` + `height` in Pixeln** — NICHT `size`, NICHT `aspect_ratio`! (Der frühere quadratische Output kam genau daher: Code schickte `size`, API ignorierte es → default 1024×1024.)
- Regeln: beide Dims **≥768**, Produkt **width×height ≤ 1.048.576** (=1024²). Output immer PNG.
- **MAI KANN non-square nativ** → kein Bildtool-Nachrüsten nötig. Aspect-Map (max. Auflösung im 1-MP-Budget, im Code `dim_map`): 1:1→1024×1024 · 16:9→1360×768 · 9:16→768×1360 · 4:3→1152×864 · 3:4→864×1152.
- edits-Endpoint (`/mai/v1/images/edits`, image-to-image): multipart, NUR model+prompt+image, KEINE width/height (behält Eingabe-Maße). Nur 2.5/2.5-Flash können edits.
- Modelle: MAI-Image-2.5 / -2.5-Flash (beide edits) / -2e (efficient, ~4× günstiger) / -2. `model` = Deployment-Name.
- Doku: learn.microsoft.com/azure/foundry/foundry-models/how-to/use-foundry-models-mai
- **Fix umgesetzt 22.06.:** `bildgen_mai_generate(prompt, model, width, height, ...)` + `dim_map` im Endpoint. Server neu gestartet. (Noch nicht mit echtem Bild getestet — Chris: keine Cents verballern; Fix folgt 1:1 der Doku.)

**Lehre:** Lag monatelang als „wartet auf Azure-Account" rum — bei verstaubten Projekt-TODOs aktiv nachhaken statt warten. ([[feedback_proaktiv_wichtig]])
