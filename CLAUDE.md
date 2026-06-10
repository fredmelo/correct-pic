# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Two-step pipeline for wedding photo slideshow preparation:

1. **`convert_to_png.py`** — converts every image/PDF in `input/` into a 1920×1080 PNG in `output/`, named `casal-01.png`, `casal-02.png`, …
2. **`make_collage.py`** — reads `casal-*.png` from `output/` and assembles tiled collage pages saved to `collage/`

### Frame layout (`convert_to_png.py`)

Each output frame composites two layers:
- **Background**: source image scaled to cover 1920×1080, center-cropped, Gaussian-blurred (radius 50)
- **Foreground**: source image letterboxed to fit within 1920×1080, centered on top

## Running the scripts

```bash
# Step 1 — convert input/ → output/
python3 convert_to_png.py

# Step 2 — build collages from output/ → collage/
python3 make_collage.py
```

Re-running either script overwrites existing output. If `input/` changes, clear `output/` before re-running `convert_to_png.py` to keep sequential numbering clean.

## Dependencies

```bash
pip install Pillow pillow-heif pymupdf
```

- **Pillow** — core image processing (both scripts)
- **pillow-heif** — HEIC/HEIF support, registered at import time in `convert_to_png.py`
- **pymupdf (fitz)** — PDF-to-image rendering at 2× scale (~144 dpi)

## Supported input formats

Images: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`, `.gif`, `.webp`, `.heic`, `.heif`  
Documents: `.pdf` — each page becomes its own numbered `casal-XX.png`

## Key parameters

**`convert_to_png.py`**

| Constant | Value | Purpose |
|---|---|---|
| `TARGET_W / TARGET_H` | 1920 / 1080 | Output canvas size |
| `BLUR_RADIUS` | 50 | Background blur intensity |

**`make_collage.py`**

| Variable | Default | Purpose |
|---|---|---|
| `LAYOUTS` | `[(6, 5), (5, 4)]` | Grid configurations to generate; add/remove tuples to change |
| `CANVAS_W / CANVAS_H` | 1920 / 1080 | Collage canvas size |

Each layout produces files named `collage-{cols}x{rows}-{n:02d}.png` in `collage/`. Tile size is derived automatically (`CANVAS_W // cols` × `CANVAS_H // rows`); tiles are center-cropped to fill.
