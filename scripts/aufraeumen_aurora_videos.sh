#!/bin/bash
# AURORA-Video-Aufraeumen (20.10.2026). NUR nach fertigem v4-Lauf ausfuehren (Job "aurora-quer-v4" = ok, v4-mp4 geprueft).
B=/mnt/c/Tools/blender_proj
T="/mnt/d/OneDrive/Dokumente/Bolla/AURORA II/7_Trailer_Blender"
D=/mnt/d/OneDrive/Desktop/temp
[ -s "$T/AURORA_Partikelvideo_Quer_3min_Tunnel_v4_ohne_Ton.mp4" ] || { echo "v4-Video fehlt - Abbruch"; exit 1; }
# verworfene Videos
rm -f "$T/AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4" "$T/AURORA_Video_3min_ohne_Ton.mp4" \
      "$T/AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4" "$D/AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4" \
      $B/aurora_partikel/AURORA_Partikelvideo_3min_hochkant_ohne_Ton.mp4 $B/aurora_video/AURORA_Video_3min_ohne_Ton.mp4 \
      $B/aurora_quer/AURORA_Partikelvideo_Quer_3min_Roehrenflug_ohne_Ton.mp4
# Rohbilder/Stills/alte Logs (~60 GB)
rm -rf $B/aurora_partikel/frames $B/aurora_partikel/stills $B/aurora_video/frames $B/aurora_video/stills \
       $B/aurora_bg/land $B/aurora_bg/port $B/frames $B/frames_hq $B/trailer_test $B/trailer_face \
       $B/render.log $B/render_hq.log $B/hq_9x16.mp4 $B/hq_16x9.mp4 \
       $B/aurora_quer/frames $B/aurora_quer/frames_v3 $B/aurora_quer/stills_v3 $B/aurora_quer/stills_v4
echo fertig; df -h /mnt/c | tail -1
