#!/usr/bin/env python3
"""Install the summarize-codebase skill into ~/.claude/skills/."""

import shutil
import sys
from pathlib import Path

SKILL_NAME = "summarize-codebase"


def main():
    # Locate the skill folder relative to this script
    repo_root = Path(__file__).resolve().parent
    skill_src = repo_root / SKILL_NAME

    if not (skill_src / "SKILL.md").exists():
        print(f"Error: {skill_src / 'SKILL.md'} not found.", file=sys.stderr)
        sys.exit(1)

    # Target: ~/.claude/skills/summarize-codebase/
    target = Path.home() / ".claude" / "skills" / SKILL_NAME

    if target.exists():
        print(f"Skill already installed at {target}")
        answer = input("Overwrite? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            sys.exit(0)
        shutil.rmtree(target)

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_src, target)
    print(f"Installed {SKILL_NAME} to {target}")


if __name__ == "__main__":
    main()
