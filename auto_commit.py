#!/usr/bin/env python3
"""
auto_commit.py — Keeps your GitHub contribution graph green and colorful.

Usage:
  python auto_commit.py             → commits a random amount (weighted)
  python auto_commit.py --count 4   → commits exactly 4 times
"""

import random
import subprocess
import argparse
from datetime import datetime

COMMIT_MESSAGES = [
    "refactor: improve code readability",
    "chore: update dependencies",
    "docs: update README with new details",
    "fix: minor bug fixes and improvements",
    "style: format code according to style guide",
    "perf: optimize performance",
    "chore: cleanup unused variables",
    "docs: add inline comments",
    "refactor: simplify logic",
    "chore: update .gitignore",
    "fix: resolve edge case in input handling",
    "style: consistent spacing and indentation",
    "chore: routine maintenance",
    "docs: improve documentation clarity",
    "refactor: extract helper functions",
    "fix: handle null values properly",
    "chore: remove dead code",
    "docs: clarify function purpose",
    "perf: reduce unnecessary computations",
    "style: align code with conventions",
    "fix: correct off-by-one error",
    "chore: reorganize file structure",
    "docs: update changelog",
    "refactor: rename variables for clarity",
    "perf: cache repeated lookups",
]

# GitHub uses these thresholds for shading:
# 1–3   → light green
# 4–6   → medium green
# 7–9   → dark green
# 10+   → darkest green
WEIGHT_DISTRIBUTION = {
    "light":   (1, 3),
    "medium":  (4, 6),
    "dark":    (7, 9),
    "darkest": (10, 12),
}

WEIGHTS = [50, 30, 15, 5]  # probability per tier (sums to 100)

LOG_FILE = "commit_log.txt"
ACTIVITY_FILE = "activity.md"


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def pick_commit_count() -> int:
    tier = random.choices(list(WEIGHT_DISTRIBUTION.keys()), weights=WEIGHTS, k=1)[0]
    low, high = WEIGHT_DISTRIBUTION[tier]
    count = random.randint(low, high)
    print(f"🎲 Tier: {tier} → {count} commit(s) today")
    return count


def make_single_commit(index: int, total: int) -> None:
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    msg = random.choice(COMMIT_MESSAGES)

    with open(ACTIVITY_FILE, "a") as f:
        f.write(f"- `{timestamp}` — {msg}\n")

    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] ({index}/{total}) {msg}\n")

    run(["git", "add", ACTIVITY_FILE, LOG_FILE])
    run(["git", "commit", "-m", msg])
    print(f"  ✅ [{index}/{total}] {msg}")


def run_commits(count: int) -> None:
    print(f"\n🌱 Starting {count} commit(s)...\n")
    for i in range(1, count + 1):
        make_single_commit(i, count)
    print(f"\n✨ Done! {count} commit(s) pushed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="grass-farmer — colorful commit automation")
    parser.add_argument("--count", type=int, default=None, help="Number of commits (default: random)")
    args = parser.parse_args()

    count = args.count if args.count else pick_commit_count()
    run_commits(count)