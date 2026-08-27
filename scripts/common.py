"""Shared helpers used by every generate_*.py script."""
import os
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")
TEMPLATES_DIR = os.path.join(REPO_ROOT, "templates")
CONFIG_PATH = os.path.join(REPO_ROOT, "config.yml")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_svg(filename, svg_content):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"  wrote {os.path.relpath(path, REPO_ROOT)}")
    return path
