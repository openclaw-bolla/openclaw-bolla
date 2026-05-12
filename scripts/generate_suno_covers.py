#!/usr/bin/env python3
"""Suno RouteNote Cover-Generator — Gemini 2.5 Flash Image, 3000×3000 JPG, kein Text im Bild."""

import json, base64, time, os, sys
from pathlib import Path
from PIL import Image
import io, urllib.request, urllib.error

FOLDER = Path("/mnt/d/OneDrive/Dokumente/Bolla/Suno_RouteNote")
CONFIG = Path("/home/bolla/workspace/config/gemini_api.json")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"

PROMPTS = {
    "Back to the Chalkboard": "A vintage green chalkboard covered in colorful chalk drawings of musical notes, stars and abstract swirls. Warm nostalgic classroom light. Photorealistic, cinematic.",
    "Classroom Chaos": "Colorful paper airplanes flying everywhere in a sunlit classroom, books tumbling, pencils in the air, joyful chaos. Vibrant pop art style.",
    "Classroom Daydreams": "A student's desk by a sunny window, soft clouds drifting in from outside, merging into a dreamy fantasy landscape with floating islands. Soft watercolor.",
    "Classroom Dreams": "Magical glowing fireflies floating through a twilight classroom, desks made of moonlight, stars visible through large windows. Dreamy, ethereal.",
    "Escuela de Vida": "A vibrant mosaic mural of diverse hands planting seeds in soil, colorful flowers blooming, a golden sunrise. Latin American folk art style.",
    "Hellish Hallways": "Dark dramatic school corridor lit by flickering red lights, long shadows, gothic architecture, mysterious fog at the end of the hall. Cinematic horror aesthetic.",
    "In der Weihnachtskinderküche": "Cozy Christmas kitchen with children baking cookies, cinnamon sticks, gingerbread, steam rising from a pot, warm candlelight, festive decorations. Illustrated storybook style.",
    "Lights Fade Slowly": "A breathtaking sunset over a calm ocean, golden and purple hues reflecting on water, silhouette of a lone figure on a beach. Cinematic photography.",
    "Pflanze die aus dem Boden wächst": "A single green sprout pushing through dark rich soil toward bright sunlight, macro photography, drops of water on leaves, dramatic light rays.",
    "School Days Groove": "Retro 70s school gymnasium turned dance floor, disco ball, funky colorful outfits, dynamic motion blur, warm orange and purple lighting.",
    "School Vibes": "Modern school rooftop at golden hour, friends sitting together, city skyline in background, cool urban aesthetic, lens flare, cinematic.",
    "School of Life": "An ancient tree with roots forming a library, books and leaves intertwined, wise owl perched on a branch, warm golden light filtering through. Fantasy illustration.",
    "School of No Rules": "Vibrant graffiti art explosion on a brick wall, bold colors, skateboard ramps, young people jumping freely, energy and freedom. Urban street art.",
    "Schoolhouse Days": "Charming vintage red brick schoolhouse surrounded by autumn trees, golden leaves falling, warm late afternoon light, nostalgic pastoral landscape.",
    "Schoolyard": "Colorful playground equipment casting long afternoon shadows, empty swings moving gently in the breeze, golden hour light, cinematic wide angle.",
}

def gemini_key():
    return json.loads(CONFIG.read_text()).get("api_key", "")

def generate_image(prompt):
    key = gemini_key()
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt + " — absolutely NO text, NO letters, NO words, NO typography in the image."}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}
    }).encode()
    req = urllib.request.Request(API_URL, data=payload,
                                  headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
    for part in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        if "inlineData" in part:
            return base64.b64decode(part["inlineData"]["data"])
    raise RuntimeError("Kein Bild in Antwort")

def save_cover(song_name, img_bytes):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    if img.size != (3000, 3000):
        img = img.resize((3000, 3000), Image.LANCZOS)
    out = FOLDER / f"{song_name}_cover.jpg"
    img.save(out, "JPEG", quality=95)
    print(f"  ✅ Gespeichert: {out.name} ({img.size[0]}×{img.size[1]})")

def main():
    # Alle alten Covers löschen
    old = list(FOLDER.glob("*_cover.jpg"))
    print(f"🗑️  Lösche {len(old)} alte Covers...")
    for f in old:
        f.unlink()
        print(f"  Gelöscht: {f.name}")

    songs = list(PROMPTS.keys())
    print(f"\n🎨 Generiere {len(songs)} neue Covers mit Gemini...\n")

    failed = []
    for i, song in enumerate(songs, 1):
        prompt = PROMPTS[song]
        print(f"[{i}/{len(songs)}] {song}")
        for attempt in range(3):
            try:
                img_bytes = generate_image(prompt)
                save_cover(song, img_bytes)
                break
            except Exception as e:
                print(f"  ⚠️  Versuch {attempt+1} fehlgeschlagen: {e}")
                if attempt < 2:
                    time.sleep(5)
                else:
                    failed.append(song)
                    print(f"  ❌ Übersprungen nach 3 Versuchen")
        time.sleep(2)  # Rate-Limit-Pause

    print(f"\n✅ Fertig! {len(songs)-len(failed)}/{len(songs)} Covers generiert.")
    if failed:
        print(f"❌ Fehlgeschlagen: {', '.join(failed)}")

if __name__ == "__main__":
    main()
