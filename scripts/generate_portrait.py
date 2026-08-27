"""
Generates assets/portrait.svg — a colorized dot-matrix portrait with an
animated per-row scanline fade-in, styled after the reference profile
(github.com/anasjameel300/anasjameel300).

If assets/photo.jpg (or .png) exists, it's converted into a grid of
full-color dots sized by local brightness. If no photo is supplied, a
procedural placeholder pattern is generated from the person's initials
instead, so the pipeline never fails on a fresh fork.

To use a real photo: drop a square-ish image at assets/photo.jpg (or .png)
and commit it. Nothing else needs to change.
"""
import os
import random

from common import ASSETS_DIR, load_config, write_svg

CANVAS = 1000
GRID_SIZE = 120          # dots per side
CELL = CANVAS // GRID_SIZE
PADDING = (CANVAS - (GRID_SIZE - 1) * CELL) // 2

FADE_DURATION = 0.22      # seconds, matches reference
ROW_DELAY_STEP = 0.0145   # seconds between successive row reveals


def _find_source_photo():
    for name in ("photo.jpg", "photo.jpeg", "photo.png"):
        path = os.path.join(ASSETS_DIR, name)
        if os.path.exists(path):
            return path
    return None


def _cells_from_photo(path, size):
    from PIL import Image, ImageOps

    img = Image.open(path).convert("RGB")

    # Center-crop to a square so non-square source photos aren't
    # squashed when downsampled to the (square) dot grid.
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 3  # bias slightly upward to favor faces over chins/shoulders
    top = min(top, h - side)
    img = img.crop((left, top, left + side, top + side))

    img = ImageOps.autocontrast(img, cutoff=1)
    img = img.resize((size, size), Image.LANCZOS)
    pixels = list(img.getdata())

    cells = []
    for row in range(size):
        for col in range(size):
            r, g, b = pixels[row * size + col]
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            cells.append((col, row, luminance, (r, g, b)))
    return cells


def _cells_from_initials(size, initials, accent_rgb):
    """Procedural placeholder: renders initials as a coarse dot bitmap
    using simple deterministic block letters, plus ambient noise dots
    so it still reads as a portrait canvas before a real photo is added."""
    FONT = {
        "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
        "G": ["01111", "10000", "10011", "10001", "10001", "10011", "01111"],
        "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
        "?": ["01110", "10001", "00010", "00100", "00100", "00000", "00100"],
    }
    letters = [FONT.get(ch.upper(), FONT["?"]) for ch in initials[:2]] or [FONT["?"]]

    grid = [[0.0 for _ in range(size)] for _ in range(size)]
    letter_h = 7
    letter_w = 5
    scale = max(1, min(size // (letter_w * len(letters) + 2), size // (letter_h + 2)))
    total_w = letter_w * len(letters) * scale + (len(letters) - 1) * scale
    start_x = (size - total_w) // 2
    start_y = (size - letter_h * scale) // 2

    for li, letter_bits in enumerate(letters):
        ox = start_x + li * (letter_w * scale + scale)
        for r, rowbits in enumerate(letter_bits):
            for c, bit in enumerate(rowbits):
                if bit == "1":
                    for sr in range(scale):
                        for sc in range(scale):
                            gy = start_y + r * scale + sr
                            gx = ox + c * scale + sc
                            if 0 <= gy < size and 0 <= gx < size:
                                grid[gy][gx] = 1.0

    random.seed(42)
    cells = []
    for row in range(size):
        for col in range(size):
            base = grid[row][col]
            noise = random.choice([0.0, 0.0, 0.0, 0.35]) if base == 0 else 0.0
            luminance = base + noise
            cells.append((col, row, luminance, accent_rgb))
    return cells


def _hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def build_svg(cells, size, bg_hex):
    rows = {}
    for col, row, luminance, (r, g, b) in cells:
        rows.setdefault(row, []).append((col, luminance, r, g, b))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}" width="100%" height="auto">',
        "<defs>",
        "<style>",
        "@keyframes scanlineFade { 0% { opacity: 0; } 100% { opacity: 1; } }",
        ".dot-group { opacity: 0; animation: scanlineFade "
        f"{FADE_DURATION}s ease-in-out forwards; }}",
        f'<radialGradient id="bgGlow" cx="50%" cy="45%" r="55%">'
        f'<stop offset="0%" stop-color="{bg_hex}" stop-opacity="1"/>'
        f'<stop offset="100%" stop-color="#0a0d12" stop-opacity="1"/></radialGradient>',
        "</style>",
        "</defs>",
        f'<rect width="{CANVAS}" height="{CANVAS}" fill="url(#bgGlow)" rx="24"/>',
    ]

    for row in sorted(rows.keys()):
        delay = row * ROW_DELAY_STEP
        parts.append(f'<g class="dot-group" style="animation-delay:{delay:.3f}s">')
        for col, luminance, r, g, b in rows[row]:
            if luminance <= 0.02:
                continue
            cx = PADDING + col * CELL
            cy = PADDING + row * CELL
            # darker pixel -> smaller dot here would invert; we keep dot
            # radius proportional to how much "signal" is at that pixel
            # (distance from mid-gray), so both shadows and highlights read
            radius = 0.9 + luminance * (CELL / 2 - 0.4)
            parts.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.2f}" '
                f'fill="rgb({r},{g},{b})"/>'
            )
        parts.append("</g>")

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    cfg = load_config()
    theme = cfg["theme"]
    name = cfg["identity"]["name"]

    photo_path = _find_source_photo()
    if photo_path:
        print(f"  using source photo: {os.path.relpath(photo_path)}")
        cells = _cells_from_photo(photo_path, GRID_SIZE)
    else:
        print("  no assets/photo.jpg found — generating placeholder initials pattern")
        initials = "".join(w[0] for w in name.split()[:2]) or "S"
        cells = _cells_from_initials(GRID_SIZE, initials, _hex_to_rgb(theme["accent"]))

    svg = build_svg(cells, GRID_SIZE, theme["panel_bg"])
    write_svg("portrait.svg", svg)


if __name__ == "__main__":
    main()
