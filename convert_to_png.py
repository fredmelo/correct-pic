#!/usr/bin/env python3
"""Convert all images in input/ to 1920x1080 PNG in output/.

Output files are named casal-01.png, casal-02.png, …

Layout per image:
  - Background: image scaled to cover 1920x1080, center-cropped, heavily blurred
  - Foreground: original image fitted (letterboxed) inside 1920x1080, centered
"""

import sys
from pathlib import Path
from PIL import Image, ImageFilter
import pillow_heif
import fitz  # pymupdf

pillow_heif.register_heif_opener()

INPUT_DIR = Path(__file__).parent / "input"
OUTPUT_DIR = Path(__file__).parent / "output"

TARGET_W, TARGET_H = 1920, 1080
BLUR_RADIUS = 50
SKIP = {".DS_Store"}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif", ".webp", ".heic", ".heif"}
PDF_EXTS = {".pdf"}


def make_1920x1080(img: Image.Image) -> Image.Image:
    base = img.convert("RGB")
    orig_w, orig_h = base.size

    scale = max(TARGET_W / orig_w, TARGET_H / orig_h)
    bg_w, bg_h = int(orig_w * scale), int(orig_h * scale)
    bg = base.resize((bg_w, bg_h), Image.LANCZOS)
    left = (bg_w - TARGET_W) // 2
    top = (bg_h - TARGET_H) // 2
    bg = bg.crop((left, top, left + TARGET_W, top + TARGET_H))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))

    fg = img.convert("RGBA") if img.mode == "RGBA" else img.convert("RGB")
    fg.thumbnail((TARGET_W, TARGET_H), Image.LANCZOS)
    fg_w, fg_h = fg.size
    paste_x = (TARGET_W - fg_w) // 2
    paste_y = (TARGET_H - fg_h) // 2

    if fg.mode == "RGBA":
        bg.paste(fg, (paste_x, paste_y), mask=fg.split()[3])
    else:
        bg.paste(fg, (paste_x, paste_y))

    return bg


def out_path(counter: int) -> Path:
    return OUTPUT_DIR / f"casal-{counter:02d}.png"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    files = sorted(f for f in INPUT_DIR.iterdir() if f.is_file() and f.name not in SKIP)
    ok = err = skipped = 0
    counter = 1

    for src in files:
        ext = src.suffix.lower()

        if ext in IMAGE_EXTS:
            dest = out_path(counter)
            try:
                with Image.open(src) as img:
                    make_1920x1080(img).save(dest, "PNG")
                print(f"  [ok] {src.name} → {dest.name}")
                counter += 1
                ok += 1
            except Exception as e:
                print(f"  [err] {src.name}: {e}", file=sys.stderr)
                err += 1

        elif ext in PDF_EXTS:
            try:
                doc = fitz.open(src)
                for page in doc:
                    mat = fitz.Matrix(2, 2)
                    pix = page.get_pixmap(matrix=mat, alpha=False)
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    dest = out_path(counter)
                    make_1920x1080(img).save(dest, "PNG")
                    print(f"  [ok] {src.name} (p{page.number + 1}) → {dest.name}")
                    counter += 1
                    ok += 1
                doc.close()
            except Exception as e:
                print(f"  [err] {src.name}: {e}", file=sys.stderr)
                err += 1

        else:
            print(f"  [skip] {src.name}")
            skipped += 1

    print(f"\nDone — {ok} converted, {err} errors, {skipped} skipped.")


if __name__ == "__main__":
    main()
