#!/bin/bash
# Rendert "Aus 0 und 1 wird ein Bild" (Blender 4.5.9, C:\Tools) und kodiert mp4 -> Desktop\temp
P=/mnt/c/Tools/blender_proj
cd /home/bolla/workspace/scripts
python3 -c "from job_status import report; report('blender-bits','Blender-Film: Aus 0 und 1 wird ein Bild','laeuft','Rendern 1080p, 336 Bilder – dauert ca. 1–2 Std.')"
/mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\bits2pixel.py' -- anim > $P/render.log 2>&1
n=$(ls $P/frames/f_*.png 2>/dev/null | wc -l)
if [ "$n" -ge 336 ]; then
  ffmpeg -y -v error -framerate 24 -i $P/frames/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 17 -preset medium $P/aus_0_und_1_wird_ein_bild.mp4
  cp $P/aus_0_und_1_wird_ein_bild.mp4 "/mnt/d/OneDrive/Desktop/temp/Aus 0 und 1 wird ein Bild.mp4"
  python3 -c "from job_status import report; report('blender-bits','Blender-Film: Aus 0 und 1 wird ein Bild','ok','fertig: Desktop\\\\temp\\\\Aus 0 und 1 wird ein Bild.mp4 – bitte ansehen')"
else
  python3 -c "from job_status import report; report('blender-bits','Blender-Film: Aus 0 und 1 wird ein Bild','fehler','nur $n von 336 Bildern – Log C:\\\\Tools\\\\blender_proj\\\\render.log')"
fi
