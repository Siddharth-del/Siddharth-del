"""
Generates assets/contributions.svg — a custom line/area chart of the last
30 days of GitHub contributions, styled to match the reference profile.

Real data requires a token in the GH_TOKEN environment variable (a PAT with
"read:user" scope works — see SETUP.md for how the workflow supplies this).
Without a token (e.g. running locally without secrets), the script falls
back to sample data clearly marked as such, so the pipeline never fails.
"""
import datetime
import os

import requests

from common import load_config, write_svg

GRAPHQL_URL = "https://api.github.com/graphql"
DAYS = 30

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


def fetch_real_contributions(username, token):
    to = datetime.datetime.utcnow()
    frm = to - datetime.timedelta(days=DAYS - 1)
    headers = {"Authorization": f"bearer {token}"}
    variables = {
        "login": username,
        "from": frm.isoformat() + "Z",
        "to": to.isoformat() + "Z",
    }
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": QUERY, "variables": variables},
        headers=headers,
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])

    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = []
    for week in weeks:
        for day in week["contributionDays"]:
            days.append((day["date"], day["contributionCount"]))
    days.sort(key=lambda d: d[0])
    return days[-DAYS:]


def sample_contributions():
    """Deterministic placeholder data, used only when no token is available."""
    today = datetime.date.today()
    pattern = [2, 1, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 2, 4, 6, 2, 0, 0, 0, 1, 2,
               3, 1, 0, 0, 1, 2, 1, 0, 0]
    days = []
    for i in range(DAYS):
        d = today - datetime.timedelta(days=DAYS - 1 - i)
        days.append((d.isoformat(), pattern[i % len(pattern)]))
    return days


def build_svg(days, theme, title, is_sample):
    width, height = 900, 340
    pad_l, pad_r, pad_t, pad_b = 60, 30, 60, 50
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b

    counts = [c for _, c in days]
    max_val = max(1, max(counts))
    n = len(days)

    def xy(i, val):
        x = pad_l + (plot_w * i / max(1, n - 1))
        y = pad_t + plot_h - (plot_h * val / max_val)
        return x, y

    accent = theme["accent"]
    accent_dim = theme["accent_dim"]
    grid = theme["grid"]
    text = theme["text"]
    muted = theme["muted"]
    bg = theme["bg"]

    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">',
        "<defs>",
        f'<linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{accent_dim}" stop-opacity="0.85"/>'
        f'<stop offset="100%" stop-color="{accent_dim}" stop-opacity="0"/></linearGradient>',
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{bg}" rx="16"/>',
        f'<text x="{width/2}" y="34" fill="{accent}" font-size="20" font-weight="700" '
        f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="middle">{title}</text>',
    ]

    # horizontal gridlines + y labels
    y_ticks = 4
    for t in range(y_ticks + 1):
        val = round(max_val * t / y_ticks)
        _, y = xy(0, val)
        parts.append(f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width - pad_r}" y2="{y:.1f}" '
                      f'stroke="{grid}" stroke-width="1" stroke-dasharray="3,4"/>')
        parts.append(f'<text x="{pad_l - 10}" y="{y+4:.1f}" fill="{muted}" font-size="11" '
                      f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="end">{val}</text>')

    # x labels (every ~5th day)
    for i, (date_str, _) in enumerate(days):
        if i % 5 == 0 or i == n - 1:
            x, _ = xy(i, 0)
            day_num = date_str.split("-")[-1]
            parts.append(f'<text x="{x:.1f}" y="{height - pad_b + 20}" fill="{muted}" font-size="11" '
                          f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="middle">{day_num}</text>')

    # area path
    line_pts = [xy(i, c) for i, c in enumerate(counts)]
    area_d = f"M {line_pts[0][0]:.1f},{pad_t + plot_h:.1f} "
    area_d += " ".join(f"L {x:.1f},{y:.1f}" for x, y in line_pts)
    area_d += f" L {line_pts[-1][0]:.1f},{pad_t + plot_h:.1f} Z"
    parts.append(f'<path d="{area_d}" fill="url(#areaFill)"/>')

    # line path
    line_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in line_pts)
    parts.append(f'<path d="{line_d}" fill="none" stroke="{accent}" stroke-width="2.5" '
                  f'stroke-linejoin="round" stroke-linecap="round"/>')

    # points
    for x, y in line_pts:
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#FFFFFF" '
                      f'stroke="{accent}" stroke-width="1.5"/>')

    parts.append(f'<text x="{pad_l}" y="{height - 10}" fill="{muted}" font-size="11" '
                  f'font-family="Segoe UI, Helvetica, Arial, sans-serif">Days</text>')

    if is_sample:
        parts.append(f'<text x="{width - pad_r}" y="{height - 10}" fill="{muted}" font-size="11" '
                      f'font-family="Segoe UI, Helvetica, Arial, sans-serif" text-anchor="end">'
                      f"sample data — add GH_TOKEN secret for live data</text>")

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    cfg = load_config()
    username = cfg["github_username"]
    name = cfg["identity"]["name"]
    token = os.environ.get("GH_TOKEN")

    is_sample = False
    if token:
        try:
            days = fetch_real_contributions(username, token)
        except Exception as exc:  # noqa: BLE001
            print(f"  warning: live contribution fetch failed ({exc}); using sample data")
            days = sample_contributions()
            is_sample = True
    else:
        print("  no GH_TOKEN set — using sample data (see SETUP.md)")
        days = sample_contributions()
        is_sample = True

    title = f"{name}'s Contribution Graph"
    svg = build_svg(days, cfg["theme"], title, is_sample)
    write_svg("contributions.svg", svg)


if __name__ == "__main__":
    main()
