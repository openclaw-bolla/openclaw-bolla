---
name: feedback-hardware-studio-massstab
description: Bei Leistungs-/Hardware-Checks IMMER das Surface Laptop Studio ("Studio") als Maßstab nehmen, nie das Surface Book und nie die WSL-Limits
metadata:
  type: feedback
---

Wenn es um Rechenleistung geht (lokale Modelle, TTS, Rendering, Machbarkeit), ist der Maßstab das **Surface Laptop Studio**: i7-13700H, 16 GB RAM, **NVIDIA RTX 4050 Laptop (~6 GB VRAM)**, Windows 11. Das Surface Book 1 ist ein altes Schulgerät (i7-6600U, 8 GB) und kein Maßstab (Chris 09.11.2026: „Studio deutlich stärker, bei solchen Checks immer nur das Studio nehmen, das Book ist uralt").
**Why:** Ich hatte WSL-Werte (4 Kerne, 5 GB RAM, keine GPU sichtbar) als Hardware des Rechners genannt; WSL ist per .wslconfig auf 6 GB/4 Kerne gedeckelt und sieht die GPU nicht. Das war falsch und stand schon in [[user_devices]].
**How to apply:** Vor Hardware-Aussagen `user_devices.md` lesen und Windows-Seite abfragen (`/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`), nicht `nproc`/`free`/`nvidia-smi` in WSL. GPU-Aufgaben unter Windows laufen lassen. Gilt auch für Cron-Prompts ([[project_hoerbuch_elevenlabs_stimme]]).
