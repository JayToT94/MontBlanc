"""
generate.py  -  Travel App Builder
====================================
Run this before converting to APK.
Scans your image folders and embeds everything into data.js.

Usage:  python generate.py

Folders config: edit FOLDERS below to rename or add folders.
"""

import os, json, base64, mimetypes, re
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
FOLDERS = [
    {"id": "folder1", "name": "Folder 1", "path": "folder1"},
    {"id": "folder2", "name": "Folder 2", "path": "folder2"},
]
OUTPUT_FILE       = "data.js"
IMAGE_EXTENSIONS  = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

# ── Helpers ───────────────────────────────────────────────────────────────────
def filename_to_title(filename):
    name = Path(filename).stem
    name = name.replace("_", " ").replace("-", " ")
    name = re.sub(r"\s+", " ", name).strip()
    return name.capitalize()

def encode_image(filepath):
    mime, _ = mimetypes.guess_type(str(filepath))
    if not mime:
        mime = "image/jpeg"
    with open(filepath, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def scan_folder(cfg):
    p = Path(cfg["path"])
    images = []
    if not p.exists():
        print(f"  [!] Not found, skipping: {p}")
        return images
    for f in sorted(f for f in p.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS):
        print(f"    + {f.name}")
        images.append({"title": filename_to_title(f.name), "file": f.name, "src": encode_image(f)})
    return images

# ── Main ──────────────────────────────────────────────────────────────────────
print("\n=== Travel App Builder ===\n")
all_folders = []
for cfg in FOLDERS:
    print(f"Scanning {cfg['path']}/")
    imgs = scan_folder(cfg)
    all_folders.append({"id": cfg["id"], "name": cfg["name"], "images": imgs})
    print(f"  -> {len(imgs)} image(s)\n")

output = f"// AUTO-GENERATED — run generate.py to rebuild.\nconst FOLDERS = {json.dumps(all_folders, ensure_ascii=False)};\n"
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(output)

size_kb = Path(OUTPUT_FILE).stat().st_size / 1024
print(f"Done! data.js written ({size_kb:.0f} KB)")
print("Open index.html to preview, then convert to APK.\n")
