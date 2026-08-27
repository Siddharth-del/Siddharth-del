"""
Renders templates/README.template.md -> README.md using config.yml.
Run this last, after the three asset generators, so the README can
reference assets/portrait.svg, assets/skills.svg, assets/bento.svg,
and assets/contributions.svg.
"""
import os
import re
import urllib.parse

from jinja2 import Environment, FileSystemLoader

from common import REPO_ROOT, TEMPLATES_DIR, load_config

# Known shields.io logo slugs for common technologies; falls back to a plain
# badge (no logo) for anything not in this map, so new tech in config.yml
# never breaks the build.
LOGO_MAP = {
    "Java": ("ED8B00", "openjdk", "white"),
    "Python": ("3776AB", "python", "white"),
    "JavaScript": ("F7DF1E", "javascript", "black"),
    "SQL": ("4479A1", "postgresql", "white"),
    "Spring Boot": ("6DB33F", "springboot", "white"),
    "Spring Security": ("6DB33F", "springsecurity", "white"),
    "Spring Data JPA": ("6DB33F", "spring", "white"),
    "Spring AI": ("6DB33F", "springboot", "white"),
    "REST API": ("005571", "", "white"),
    "JWT": ("000000", "jsonwebtokens", "white"),
    "OAuth": ("3C3C3D", "", "white"),
    "Microservices": ("6DB33F", "", "white"),
    "Gemini API": ("8E75B2", "googlegemini", "white"),
    "Prompt Engineering": ("333333", "", "white"),
    "Image-Based Inference": ("333333", "", "white"),
    "PostgreSQL": ("4169E1", "postgresql", "white"),
    "MySQL": ("4479A1", "mysql", "white"),
    "Git": ("F05032", "git", "white"),
    "GitHub": ("181717", "github", "white"),
    "Docker": ("2496ED", "docker", "white"),
    "Postman": ("FF6C37", "postman", "white"),
    "IntelliJ IDEA": ("000000", "intellijidea", "white"),
    "VS Code": ("007ACC", "visualstudiocode", "white"),
    "CI/CD": ("2088FF", "githubactions", "white"),
}


def badge(label):
    color, logo, logo_color = LOGO_MAP.get(label, ("333333", "", "white"))
    encoded_label = urllib.parse.quote(label.replace(" ", "_"), safe="")
    url = f"https://img.shields.io/badge/{encoded_label}-{color}?style=flat-square"
    if logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return f"![{label}]({url})"


def build_typing_lines(lines):
    encoded = [urllib.parse.quote(line) for line in lines]
    return ";".join(encoded)


def main():
    cfg = load_config()
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), trim_blocks=True, lstrip_blocks=True)
    env.globals["badge"] = badge

    template = env.get_template("README.template.md")
    rendered = template.render(
        identity=cfg["identity"],
        socials=cfg["socials"],
        about=cfg["about"],
        tech_stack=cfg["tech_stack"],
        projects=cfg["projects"],
        certifications=cfg["certifications"],
        currently_learning=cfg["currently_learning"],
        footer_statement=cfg["footer_statement"],
        typing_color=cfg["theme"]["accent"].lstrip("#"),
        typing_lines=build_typing_lines(cfg["identity"]["tagline_lines"]),
    )

    # collapse more than two consecutive blank lines left over from Jinja loops
    rendered = re.sub(r"\n{3,}", "\n\n", rendered).strip() + "\n"

    out_path = os.path.join(REPO_ROOT, "README.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"  wrote {os.path.relpath(out_path, REPO_ROOT)}")


if __name__ == "__main__":
    main()
