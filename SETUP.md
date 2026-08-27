# Setup

This repo regenerates your GitHub profile README automatically. You edit
`config.yml`; a GitHub Action rebuilds `README.md` and everything in
`assets/*.svg` on every push and once a day.

## 1. Place this repo correctly

It must live at **`github.com/<your-username>/<your-username>`** — a repo
named exactly after your username. GitHub only renders the README on your
profile page from that specific repo.

## 2. Edit `config.yml`

This is the only file you should need to touch for day-to-day changes:
name, tagline, socials, About bullets, skills radar, tech stack, projects,
certifications, and theme colors. No script edits required.

## 3. (Optional) Add a real photo for the portrait

Drop a roughly square image at `assets/photo.jpg` (or `.png`) and commit it.
The generator will convert it into the dot-matrix portrait automatically.
Without a photo, it falls back to a procedural placeholder pattern built
from your initials, so the build never fails — but a real photo looks a lot
better.

## 4. (Optional but recommended) Enable live contribution data

The contribution graph works out of the box using **sample data** so
nothing breaks on a fresh fork. To show your real contribution history:

1. Create a **classic Personal Access Token**: GitHub → Settings →
   Developer settings → Personal access tokens → Tokens (classic) →
   Generate new token, scope: `read:user`.
2. In this repo: Settings → Secrets and variables → Actions → New repository
   secret. Name it `PROFILE_TOKEN`, paste the token as the value.
3. Re-run the workflow (Actions tab → Update Profile → Run workflow), or
   just wait for the next push/daily run.

## 5. Enable GitHub Actions

If Actions are disabled on a fresh fork, go to the **Actions** tab and
enable workflows. The `Update Profile` workflow runs:

- on every push that touches `config.yml`, `templates/`, `scripts/`, or
  `assets/photo.*`
- once a day at 03:00 UTC (keeps the contribution graph current)
- manually, via the "Run workflow" button

## 6. Fill in real links

`config.yml` has a few placeholders you should replace once you have them:

- Each project's `repo_url` (currently `REPO_LINK_HERE`)
- AgriPro's `demo_url` (currently `LIVE_DEMO_LINK_HERE`) if the live demo
  is up, or delete that line if it's not

## How it fits together

```
config.yml                 <- you edit this
   │
   ▼
scripts/generate_all.py    <- runs the four generators, then the README
   ├── generate_portrait.py       -> assets/portrait.svg
   ├── generate_skills.py         -> assets/skills.svg
   ├── generate_contributions.py  -> assets/contributions.svg
   ├── generate_bento.py          -> assets/bento.svg
   └── generate_readme.py         -> README.md (from templates/README.template.md)
   │
   ▼
.github/workflows/update-profile.yml   <- runs the above, commits the results
```

Running it locally (optional, for previewing changes before pushing):

```bash
pip install -r requirements.txt
cd scripts
python generate_all.py
```
