"""Runs every generator in order. Used locally and by the GitHub Action."""
import generate_portrait
import generate_skills
import generate_contributions
import generate_bento
import generate_readme

STEPS = [
    ("portrait", generate_portrait.main),
    ("skills radar", generate_skills.main),
    ("contribution graph", generate_contributions.main),
    ("bento showcase", generate_bento.main),
    ("README", generate_readme.main),
]


def main():
    for label, fn in STEPS:
        print(f"[generate] {label}")
        fn()
    print("[generate] done.")


if __name__ == "__main__":
    main()
