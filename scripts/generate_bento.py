"""
Generates assets/bento.svg — a bento-grid showcase of featured projects,
pulled straight from config.yml (projects list). Add/remove/edit projects
there; the grid re-flows automatically (up to 4 cards, first card is wide).
"""
import textwrap

from common import load_config, write_svg

COL_W = 280
ROW_H = 190
GAP = 16
PAD = 20


def wrap(text, width, max_lines=3):
    lines = textwrap.wrap(text, width=width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip() + "…"
    return lines


def card(x, y, w, h, project, theme, wide=False):
    accent = theme["accent"]
    text_color = theme["text"]
    muted = theme["muted"]
    panel = theme["panel_bg"]
    grid = theme["grid"]

    parts = [
        f'<g transform="translate({x},{y})">',
        f'<rect width="{w}" height="{h}" rx="14" fill="{panel}" stroke="{grid}" stroke-width="1"/>',
        f'<rect width="4" height="{h}" rx="2" fill="{accent}"/>',
    ]

    title_lines = wrap(project["name"], 30 if wide else 22, max_lines=2)
    ty = 34
    for line in title_lines:
        parts.append(f'<text x="24" y="{ty}" fill="{text_color}" font-size="17" font-weight="700" '
                      f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{line}</text>')
        ty += 22

    desc_lines = wrap(project["description"], 46 if wide else 30, max_lines=3 if wide else 4)
    dy = ty + 6
    for line in desc_lines:
        parts.append(f'<text x="24" y="{dy}" fill="{muted}" font-size="12.5" '
                      f'font-family="Segoe UI, Helvetica, Arial, sans-serif">{line}</text>')
        dy += 18

    # stack chips along the bottom
    chip_x = 24
    chip_y = h - 34
    for tech in project["stack"][:6 if wide else 4]:
        chip_w = 12 + len(tech) * 6.4
        if chip_x + chip_w > w - 16:
            break
        parts.append(f'<rect x="{chip_x:.1f}" y="{chip_y}" width="{chip_w:.1f}" height="22" rx="11" '
                      f'fill="none" stroke="{accent}" stroke-width="1" opacity="0.7"/>')
        parts.append(f'<text x="{chip_x + chip_w/2:.1f}" y="{chip_y + 15}" fill="{accent}" font-size="10.5" '
                      f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="middle">{tech}</text>')
        chip_x += chip_w + 8

    parts.append("</g>")
    return "\n".join(parts)


def build_svg(projects, theme):
    n = len(projects)
    cols = 2
    rows = (n + 1) // 2 if n > 1 else 1
    width = PAD * 2 + COL_W * cols + GAP * (cols - 1)
    height = PAD * 2 + ROW_H * rows + GAP * (rows - 1)

    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{width}" height="{height}" fill="{theme["bg"]}" rx="16"/>',
    ]

    positions = []
    if n >= 1:
        # first project spans both columns (the "hero" bento cell)
        positions.append((PAD, PAD, COL_W * 2 + GAP, ROW_H, True))
    for i, _ in enumerate(projects[1:]):
        col = i % 2
        row = 1 + i // 2
        x = PAD + col * (COL_W + GAP)
        y = PAD + row * (ROW_H + GAP)
        positions.append((x, y, COL_W, ROW_H, False))

    for (x, y, w, h, wide), project in zip(positions, projects):
        parts.append(card(x, y, w, h, project, theme, wide=wide))

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    cfg = load_config()
    svg = build_svg(cfg["projects"], cfg["theme"])
    write_svg("bento.svg", svg)


if __name__ == "__main__":
    main()
