# correct-pic

Two-step pipeline for wedding photo slideshow preparation.

## Pipeline

```
input/  →  convert_to_png.py  →  output/  →  make_collage.py  →  collage/
```

1. **`convert_to_png.py`** — converts every image/PDF in `input/` into a 1920×1080 PNG in `output/`, named `casal-01.png`, `casal-02.png`, …
2. **`make_collage.py`** — reads `casal-*.png` from `output/` and assembles tiled collage pages into `collage/`

## Install

```bash
pip install Pillow pillow-heif pymupdf
```

## Usage

```bash
# Step 1 — convert input/ → output/
python3 convert_to_png.py

# Step 2 — build collages from output/ → collage/
python3 make_collage.py
```

If `input/` changes, clear `output/` before re-running `convert_to_png.py` to keep the sequential numbering clean.

## Supported input formats

Images: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`, `.gif`, `.webp`, `.heic`, `.heif`  
Documents: `.pdf` — each page becomes its own numbered `casal-XX.png`

## Frame layout

Each `casal-XX.png` composites two layers:
- **Background**: source image scaled to cover 1920×1080, center-cropped, Gaussian-blurred (radius 50)
- **Foreground**: source image letterboxed to fit within 1920×1080, centered on top

## Collage output

Each run of `make_collage.py` produces collages for every combination of resolution and grid layout:

| Resolution | Grid | Tiles/page | Files |
|---|---|---|---|
| 1080p (1920×1080) | 6×5 | 30 | `collage-1080p-6x5-01.png`, … |
| 1080p (1920×1080) | 5×4 | 20 | `collage-1080p-5x4-01.png`, … |
| 4K (3840×2160) | 6×5 | 30 | `collage-4k-6x5-01.png`, … |
| 4K (3840×2160) | 5×4 | 20 | `collage-4k-5x4-01.png`, … |

To add a resolution or grid, edit `CANVAS_SIZES` or `LAYOUTS` in `make_collage.py`.
