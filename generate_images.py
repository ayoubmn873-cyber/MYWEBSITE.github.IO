"""
BinRecipes — AI Image Generator
Uses Gemini API to generate all blog images.
Run: python generate_images.py
"""

import requests
import base64
import os
import time
import json

API_KEY = "AIzaSyB9vj0g57Agk3qwEpBi1TYFD4o5yaJ8nrI"
OUTPUT_DIR = "images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAGES = [
    {
        "file": "hero-bg.jpg",
        "prompt": "A stunning overhead flat lay of a beautiful food spread on a dark wooden table. Colorful fresh ingredients, herbs, spices, vegetables, pasta, eggs, and cooking utensils artfully arranged. Warm cinematic food photography lighting. High resolution, professional food photography style.",
    },
    {
        "file": "featured.jpg",
        "prompt": "A beautifully plated gourmet dish on a white ceramic plate. Rustic wooden table background. Soft natural window light. Professional food photography, shallow depth of field, warm tones.",
    },
    {
        "file": "breakfast-1.jpg",
        "prompt": "Perfectly plated avocado toast on sourdough bread, topped with two poached eggs with runny yolks, sprinkled with red pepper flakes, microgreens, and sesame seeds. White marble background. Bright natural daylight food photography.",
    },
    {
        "file": "breakfast-2.jpg",
        "prompt": "Stack of tall fluffy golden buttermilk pancakes drizzled with maple syrup, topped with fresh blueberries and strawberries, dusted with powdered sugar. Rustic wooden table. Warm morning light. Professional food photography.",
    },
    {
        "file": "dinner-1.jpg",
        "prompt": "Creamy pasta carbonara in a white bowl, perfectly coated spaghetti with crispy golden pancetta, freshly cracked black pepper, and grated Parmesan cheese. Dark moody restaurant-style food photography lighting.",
    },
    {
        "file": "dinner-2.jpg",
        "prompt": "Beautifully plated baked lemon herb salmon fillet on a white plate, with golden crispy skin, garnished with fresh dill, lemon slices, and roasted asparagus. Elegant fine dining food photography.",
    },
    {
        "file": "dessert-1.jpg",
        "prompt": "Individual no-bake cheesecake jar with creamy vanilla filling, fresh strawberry compote topping, graham cracker crumble, and a whole strawberry garnish. White background, bright clean food photography.",
    },
    {
        "file": "dessert-2.jpg",
        "prompt": "Rich fudgy double chocolate brownies cut into squares, dusted with cocoa powder, with a gooey melted chocolate center visible. Dark dramatic food photography, moody lighting, chocolate shavings around.",
    },
    {
        "file": "healthy-1.jpg",
        "prompt": "Colorful rainbow Buddha bowl with quinoa base, roasted chickpeas, sliced avocado, shredded purple cabbage, grated carrots, cucumber, cherry tomatoes, and tahini dressing drizzle. Bright overhead photography, white bowl.",
    },
    {
        "file": "healthy-2.jpg",
        "prompt": "Beautiful green smoothie bowl topped with kiwi slices, banana, granola, chia seeds, coconut flakes, and fresh mint leaves. Bright white background, vibrant colors, top-down food photography.",
    },
    {
        "file": "ebook-cover.jpg",
        "prompt": "Professional cookbook cover design. Title 'The BinRecipes Cookbook' in elegant typography. Beautiful collage of colorful gourmet food photos arranged in a grid. Warm orange and cream color scheme. Clean modern design. Digital book cover.",
    },
]

def generate_image(prompt, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.0-flash-preview-image-generation:generateContent"
        f"?key={API_KEY}"
    )
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        parts = data["candidates"][0]["content"]["parts"]
        for part in parts:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✅  {filename}")
                return True
        print(f"  ⚠️  No image in response for {filename}")
    except Exception as e:
        print(f"  ❌  {filename} — {e}")
    return False


def main():
    print("\n🍴  BinRecipes — AI Image Generator")
    print("=" * 42)
    total = len(IMAGES)
    ok = 0
    for i, item in enumerate(IMAGES, 1):
        print(f"[{i}/{total}] Generating {item['file']}...")
        success = generate_image(item["prompt"], item["file"])
        if success:
            ok += 1
        if i < total:
            time.sleep(2)  # avoid rate limiting
    print("=" * 42)
    print(f"\n✅  Done — {ok}/{total} images generated in ./{OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
