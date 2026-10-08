#!/bin/bash
# HQ-Render "Aus 0 und 1 wird ein Bild": 80 Samples, f/6, Filter 0.85 -> 16:9 + TikTok-Hochkant, Ablage DistroKid-Social-Media-Ordner
P=/mnt/c/Tools/blender_proj
S="/mnt/d/OneDrive/Desktop/DistroKid/Fourteen Pairs of Eyes/Social Media"
T="/mnt/d/OneDrive/Desktop/temp"
cd /home/bolla/workspace/scripts
python3 -c "from job_status import report; report('blender-bits-hq','Blender HQ-Render: Aus 0 und 1','laeuft','336 Bilder, 80 Samples – ca. 2–3 Std.')"
/mnt/c/Tools/blender-4.5.9-windows-x64/blender.exe -b -P 'C:\Tools\blender_proj\bits2pixel_hq.py' -- anim > $P/render_hq.log 2>&1
n=$(ls $P/frames_hq/f_*.png 2>/dev/null | wc -l)
if [ "$n" -ge 336 ]; then
  A=/home/bolla/workspace/state/herbst_video/"Aus 0 und 1 wird ein Bild - Herbstferien.mp4"
  ffmpeg -y -v error -framerate 24 -i $P/frames_hq/f_%04d.png -i "$A" -map 0:v -map 1:a -c:v libx264 -pix_fmt yuv420p -crf 14 -preset slow -c:a copy -shortest -movflags +faststart "$P/hq_16x9.mp4"
  ffmpeg -y -v error -i "$P/hq_16x9.mp4" -filter_complex "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.15[bg];[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,drawtext=fontfile=/mnt/c/Windows/Fonts/segoeuib.ttf:text='Aus 0 und 1 wird ein Bild':fontsize=64:fontcolor=white:borderw=3:bordercolor=black@0.6:x=(w-text_w)/2:y=480[v]" -map "[v]" -map 0:a -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a copy -movflags +faststart "$P/hq_9x16.mp4"
  cp "$P/hq_16x9.mp4" "$S/Aus 0 und 1 wird ein Bild_16x9.mp4"
  cp "$P/hq_9x16.mp4" "$S/Aus 0 und 1 wird ein Bild_TikTok-Video.mp4"
  cp "$T/TikTok-Caption Aus 0 und 1.txt" "$S/Aus 0 und 1 wird ein Bild_TikTok-Caption.txt"
  /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Get-ChildItem 'D:\OneDrive\Desktop\DistroKid\Fourteen Pairs of Eyes\Social Media' | Out-Null" >/dev/null 2>&1
  python3 -c "from job_status import report; report('blender-bits-hq','Blender HQ-Render: Aus 0 und 1','ok','fertig: DistroKid\\\\Fourteen Pairs of Eyes\\\\Social Media (16x9 + TikTok + Caption)')"
else
  python3 -c "from job_status import report; report('blender-bits-hq','Blender HQ-Render: Aus 0 und 1','fehler','nur $n von 336 Bildern – Log render_hq.log')"
fi
