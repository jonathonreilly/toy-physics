#!/usr/bin/env python3
"""Inventory every remote branch and classify it for cleanup.

Read-only. Produces docs/audit/data/branch_inventory.json with one entry
per remote branch and the following fields:

  - branch:                    name (without 'origin/' prefix)
  - last_commit_iso:           UTC timestamp
  - last_commit_age_hours:     hours since last commit
  - last_commit_subject:       first line of last commit message
  - unmerged_commits:          # commits not on origin/main
  - merged_into_main:          true iff every commit is reachable from main
  - touches_files:             count of files changed across unmerged commits
  - touches_audit_lane:        true iff branch modifies docs/audit/
  - novel_paths:               files added by this branch that don't exist
                               on origin/main (likely-novel science)
  - existing_paths_modified:   files modified by this branch that DO exist
                               on origin/main (likely already-superseded)
  - category:                  one of:
       active_24h           - last commit < 24h ago, keep as-is
       fully_merged         - every commit on main, safe to delete ref
       likely_squash_merged - all touched files exist on main with newer
                              content; branch's work probably landed via
                              squash-merge, archive then delete
       has_novel_paths      - branch adds paths not on main; consolidate
       massive_divergent    - >500 unmerged commits AND >24h old; archive
                              tag only, do not consolidate (these are
                              overnight runs that diverged wholesale)
       small_stale          - 1-500 unmerged commits, >24h old, no novel
                              paths; archive then delete
       worktree_or_special  - matches a known special prefix
       audit_lane           - the current branch holding the audit work
                              (special-cased, never deleted)
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
OUTPUT_PATH = DATA_DIR / "branch_inventory.json"

ACTIVE_HOURS_CUTOFF = 24
MASSIVE_COMMIT_CUTOFF = 500
PROTECTED_BRANCHES = {"main", "audit-lane", "HEAD"}


def run(cmd: list[str], **kwargs) -> str:
    """Run a git command; return stdout. Raises on nonzero exit."""
    return subprocess.run(
        cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=True, **kwargs
    ).stdout


def list_remote_branches() -> list[str]:
    out = run(["git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/"])
    branches = []
    for line in out.splitlines():
        line = line.strip()
        if not line or line.endswith("/HEAD"):
            continue
        if line.startswith("origin/"):
            line = line[len("origin/"):]
        branches.append(line)
    return branches


def last_commit_info(branch: str) -> tuple[str, str]:
    """Return (iso_timestamp_utc, subject_line) for branch's last commit."""
    iso = run(["git", "log", "-1", "--format=%cI", f"origin/{branch}"]).strip()
    subj = run(["git", "log", "-1", "--format=%s", f"origin/{branch}"]).strip()
    return iso, subj


def hours_since(iso: str) -> float:
    if not iso:
        return float("inf")
    dt = datetime.fromisoformat(iso)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - dt
    return delta.total_seconds() / 3600.0


def unmerged_commits(branch: str) -> list[str]:
    try:
        out = run(["git", "log", "--format=%H", f"origin/main..origin/{branch}"])
    except subprocess.CalledProcessError:
        return []
    return [h for h in out.splitlines() if h.strip()]


def files_touched(branch: str) -> set[str]:
    """Files modified across all unmerged commits on branch."""
    try:
        out = run(["git", "diff", "--name-only", f"origin/main...origin/{branch}"])
    except subprocess.CalledProcessError:
        return set()
    return {p.strip() for p in out.splitlines() if p.strip()}


def file_exists_on_main(path: str) -> bool:
    """Cheaper check than running git cat-file every time: use git ls-tree once."""
    return path in MAIN_FILES


MAIN_FILES: set[str] = set()


def populate_main_files():
    global MAIN_FILES
    out = run(["git", "ls-tree", "-r", "--name-only", "origin/main"])
    MAIN_FILES = {p.strip() for p in out.splitlines() if p.strip()}


def categorize(b: str, info: dict) -> str:
    if b in PROTECTED_BRANCHES:
        return "audit_lane" if b == "audit-lane" else "protected"
    if info["merged_into_main"]:
        return "fully_merged"
    if info["last_commit_age_hours"] < ACTIVE_HOURS_CUTOFF:
        return "active_24h"
    # All checks below require >24h age and unmerged commits.
    if (b.startswith("worktree-") or b.startswith("frontier/")
            or b.startswith("review/")):
        return "worktree_or_special"
    if info["unmerged_commits"] > MASSIVE_COMMIT_CUTOFF:
        return "massive_divergent"
    if info["novel_paths"]:
        return "has_novel_paths"
    # No novel paths: every file the branch touches already exists on
    # main. Likely the work was squash-merged or superseded.
    return "likely_squash_merged"


def inventory() -> list[dict]:
    populate_main_files()
    branches = list_remote_branches()
    out = []
    for i, b in enumerate(sorted(branches), 1):
        if i % 25 == 0:
            print(f"  ... processed {i}/{len(branches)}", file=sys.stderr)
        try:
            iso, subj = last_commit_info(b)
        except subprocess.CalledProcessError:
            continue
        commits = unmerged_commits(b)
        files = files_touched(b)
        novel = sorted(p for p in files if p not in MAIN_FILES)
        existing = sorted(p for p in files if p in MAIN_FILES)
        info = {
            "branch": b,
            "last_commit_iso": iso,
            "last_commit_age_hours": round(hours_since(iso), 2),
            "last_commit_subject": subj,
            "unmerged_commits": len(commits),
            "merged_into_main": len(commits) == 0,
            "touches_files": len(files),
            "touches_audit_lane": any(p.startswith("docs/audit/") for p in files),
            "novel_paths": novel,
            "novel_path_count": len(novel),
            "existing_paths_modified": existing,
            "existing_path_count": len(existing),
        }
        info["category"] = categorize(b, info)
        out.append(info)
    return out


def main() -> int:
    print(f"Inventorying remote branches in {REPO_ROOT}...", file=sys.stderr)
    inv = inventory()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "active_hours_cutoff": ACTIVE_HOURS_CUTOFF,
        "massive_commit_cutoff": MASSIVE_COMMIT_CUTOFF,
        "branch_count": len(inv),
        "category_counts": {},
        "branches": inv,
    }
    for b in inv:
        c = b["category"]
        payload["category_counts"][c] = payload["category_counts"].get(c, 0) + 1
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  branches: {len(inv)}")
    for cat, n in sorted(payload["category_counts"].items(), key=lambda x: -x[1]):
        print(f"  {cat:24s}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
