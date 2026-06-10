#!/usr/bin/env python3
"""Create collages from output/ images at multiple resolutions.

Generates for each canvas size:
  - 6x5 (30 tiles each) → collage-{res}-6x5-01.png, …
  - 5x4 (20 tiles each) → collage-{res}-5x4-01.png, …
"""

import sys
from pathlib import Path
from PIL import Image

OUTPUT_DIR = Path(__file__).parent / "output"
COLLAGE_DIR = Path(__file__).parent / "collage"

CANVAS_SIZES = [
    ("1080p", 1920, 1080),
    ("4k",    3840, 2160),
]

LAYOUTS = [
    (6, 5),
    (5, 4),
]


def crop_to_tile(img: Image.Image, tile_w: int, tile_h: int) -> Image.Image:
    src_w, src_h = img.size
    scale = max(tile_w / src_w, tile_h / src_h)
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - tile_w) // 2
    top = (new_h - tile_h) // 2
    return img.crop((left, top, left + tile_w, top + tile_h))


def make_collage(images: list[Path], dest: Path, cols: int, rows: int, canvas_w: int, canvas_h: int) -> None:
    tile_w = canvas_w // cols
    tile_h = canvas_h // rows
    canvas = Image.new("RGB", (canvas_w, canvas_h))
    for idx, path in enumerate(images):
        col = idx % cols
        row = idx // cols
        with Image.open(path) as img:
            tile = crop_to_tile(img.convert("RGB"), tile_w, tile_h)
        canvas.paste(tile, (col * tile_w, row * tile_h))
    canvas.save(dest, "PNG")


def main() -> None:
    COLLAGE_DIR.mkdir(exist_ok=True)

    images = sorted(OUTPUT_DIR.glob("casal-*.png"))
    if not images:
        print("No casal-*.png files found in output/", file=sys.stderr)
        sys.exit(1)

    for res, canvas_w, canvas_h in CANVAS_SIZES:
        for cols, rows in LAYOUTS:
            per_page = cols * rows
            chunks = [images[i:i + per_page] for i in range(0, len(images), per_page)]
            grid = f"{cols}x{rows}"
            print(f"\n{res} — Layout {grid} ({cols} cols × {rows} rows, {per_page} tiles/page):")
            for n, chunk in enumerate(chunks, start=1):
                dest = COLLAGE_DIR / f"collage-{res}-{grid}-{n:02d}.png"
                make_collage(chunk, dest, cols, rows, canvas_w, canvas_h)
                print(f"  [ok] {dest.name} ({len(chunk)} tiles: {chunk[0].name} … {chunk[-1].name})")

    print("\nDone.")


if __name__ == "__main__":
    main()
