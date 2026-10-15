#!/bin/bash
# AURORA-II-Trailer (Gesicht aus Cover Band I, Nordlicht-Farben), 30 s 1080p Eevee -> mp4 -> Desktop\temp
P=/mnt/c/Tools/blender_proj
cd /home/bolla/workspace/scripts
rm -f $P/trailer_face/f_*.png
python3 -c "from job_status import report; report('blender-trailer-face','AURORA-II-Trailer Gesicht (30 s)','laeuft','720 Bilder 1080p, ca. 10-15 Min')"
S=$(date +%s)
/mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\trailer_face.py' -- anim > $P/trailer_face_render.log 2>&1
E=$(date +%s)
n=$(ls $P/trailer_face/f_*.png 2>/dev/null | wc -l)
if [ "$n" -ge 720 ]; then
  ffmpeg -y -v error -framerate 24 -i $P/trailer_face/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16 $P/trailer_face/AURORA_II_Trailer_Gesicht_30s.mp4
  cp $P/trailer_face/AURORA_II_Trailer_Gesicht_30s.mp4 "/mnt/d/OneDrive/Desktop/temp/AURORA_II_Trailer_Gesicht_30s.mp4"
  python3 -c "from job_status import report; report('blender-trailer-face','AURORA-II-Trailer Gesicht (30 s)','ok','fertig in $((E-S)) s: Desktop\\\\temp\\\\AURORA_II_Trailer_Gesicht_30s.mp4')"
else
  python3 -c "from job_status import report; report('blender-trailer-face','AURORA-II-Trailer Gesicht (30 s)','fehler','nur $n von 720 Bildern, Log C:\\\\Tools\\\\blender_proj\\\\trailer_face_render.log')"
fi
