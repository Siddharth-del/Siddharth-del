"""
Generates assets/skills.svg — an animated radar (spider) chart with a
rotating sweep line and pulsing vertices, styled like a HUD readout.

Skill levels are read from config.yml (skills_radar), on a 1-5 self-assessed
scale. Edit the list there to change what shows up here; no code edits needed.
"""
import math

from common import load_config, write_svg

SIZE = 460
CENTER = SIZE / 2
MAX_RADIUS = 165
RINGS = 5
MAX_LEVEL = 5


def polar(cx, cy, radius, angle_deg):
    angle_rad = math.radians(angle_deg - 90)  # start at top, go clockwise
    return cx + radius * math.cos(angle_rad), cy + radius * math.sin(angle_rad)


def build_svg(skills, theme):
    n = len(skills)
    step = 360 / n
    accent = theme["accent"]
    grid = theme["grid"]
    text = theme["text"]
    muted = theme["muted"]
    bg = theme["panel_bg"]

    parts = [
        f'<svg viewBox="0 0 {SIZE} {SIZE + 40}" xmlns="http://www.w3.org/2000/svg">',
        "<defs>",
        f'<radialGradient id="glow" cx="50%" cy="50%" r="60%">'
        f'<stop offset="0%" stop-color="{accent}" stop-opacity="0.25"/>'
        f'<stop offset="100%" stop-color="{accent}" stop-opacity="0"/></radialGradient>',
        "</defs>",
        f'<rect width="{SIZE}" height="{SIZE + 40}" fill="{bg}" rx="16"/>',
        f'<circle cx="{CENTER}" cy="{CENTER}" r="{MAX_RADIUS + 20}" fill="url(#glow)"/>',
    ]

    # concentric rings
    for i in range(1, RINGS + 1):
        r = MAX_RADIUS * i / RINGS
        parts.append(
            f'<circle cx="{CENTER}" cy="{CENTER}" r="{r:.1f}" fill="none" '
            f'stroke="{grid}" stroke-width="1"/>'
        )

    # spokes + axis labels
    for i, skill in enumerate(skills):
        angle = i * step
        x, y = polar(CENTER, CENTER, MAX_RADIUS, angle)
        parts.append(
            f'<line x1="{CENTER}" y1="{CENTER}" x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="{grid}" stroke-width="1"/>'
        )
        lx, ly = polar(CENTER, CENTER, MAX_RADIUS + 26, angle)
        anchor = "middle"
        if lx < CENTER - 10:
            anchor = "end"
        elif lx > CENTER + 10:
            anchor = "start"
        parts.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{text}" font-size="12" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="{anchor}" '
            f'dominant-baseline="middle">{skill["label"]}</text>'
        )

    # data polygon
    pts = []
    vertex_points = []
    for i, skill in enumerate(skills):
        angle = i * step
        r = MAX_RADIUS * (skill["level"] / MAX_LEVEL)
        x, y = polar(CENTER, CENTER, r, angle)
        pts.append(f"{x:.1f},{y:.1f}")
        vertex_points.append((x, y))

    poly = " ".join(pts)
    parts.append(
        f'<polygon points="{poly}" fill="{accent}" fill-opacity="0.18" '
        f'stroke="{accent}" stroke-width="2"/>'
    )

    for i, (x, y) in enumerate(vertex_points):
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{accent}">'
            f'<animate attributeName="r" values="3;5.5;3" dur="2.4s" '
            f'begin="{i * 0.15:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )

    # rotating radar sweep
    parts.append(
        f'<g transform="translate({CENTER},{CENTER})">'
        f'<line x1="0" y1="0" x2="0" y2="-{MAX_RADIUS}" stroke="{accent}" '
        f'stroke-width="1.5" opacity="0.7">'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'from="0" to="360" dur="6s" repeatCount="indefinite"/>'
        f"</line></g>"
    )

    parts.append(
        f'<text x="{CENTER}" y="{SIZE + 26}" fill="{muted}" font-size="12" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="middle">'
        f"self-assessed · 1-5 scale · see config.yml</text>"
    )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    cfg = load_config()
    skills = cfg["skills_radar"]
    svg = build_svg(skills, cfg["theme"])
    write_svg("skills.svg", svg)


if __name__ == "__main__":
    main()
