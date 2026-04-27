#!/usr/bin/env python3
"""Archive then delete every remote branch that has not been active in
the last 24 hours.

For every remote branch where:
  - last_commit_age_hours >= 24, AND
  - branch is not in PROTECTED, AND
  - branch is not the consolidation branch we just created,

create a lightweight tag `archive/<branch>-YYYY-MM-DD` pointing at the
branch tip, push the tag, then delete the remote branch ref.

The tag preserves the entire commit graph; recovery is one command:
  git checkout -b <name> archive/<name>-YYYY-MM-DD

Run modes:
  --dry-run    print the planned operations without executing
  --execute    push tags + push deletions
  --inventory  print the categorized list and exit (no git ops)

Always reads docs/audit/data/branch_inventory.json (must be fresh).
Re-run inventory_remote_branches.py first if the remote changed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
INVENTORY = REPO_ROOT / "docs" / "audit" / "data" / "branch_inventory.json"

KEEP_AGE_HOURS = 24
PROTECTED = {"main", "audit-lane", "HEAD", "cleanup-consolidation-2026-04-27"}


def run(cmd: list[str], check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=check,
        capture_output=capture, text=True,
    )


def remote_ref_exists(branch: str) -> bool:
    result = run(
        ["git", "rev-parse", "--verify", "--quiet", f"origin/{branch}"],
        check=False,
    )
    return result.returncode == 0


def current_age_hours(branch: str) -> float | None:
    result = run(
        ["git", "log", "-1", "--format=%cI", f"origin/{branch}"],
        check=False,
    )
    if result.returncode != 0:
        return None
    from datetime import datetime, timezone

    dt = datetime.fromisoformat(result.stdout.strip())
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0


def candidate_branches(inv: dict) -> list[dict]:
    out = []
    for b in inv["branches"]:
        if b["branch"] in PROTECTED:
            continue
        if b["last_commit_age_hours"] < KEEP_AGE_HOURS:
            continue
        out.append(b)
    return out


def archive_tag(branch: str) -> str:
    today = date.today().isoformat()
    return f"archive/{branch}-{today}"


def main() -> int:
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--inventory", action="store_true",
                   help="Print the categorized list and exit.")
    g.add_argument("--dry-run", action="store_true",
                   help="Print planned ops without executing.")
    g.add_argument("--execute", action="store_true",
                   help="Push tags, then push branch deletions.")
    p.add_argument("--limit", type=int, default=None,
                   help="Process at most N branches (for incremental runs).")
    args = p.parse_args()

    if not INVENTORY.exists():
        print("FAIL: branch_inventory.json missing; run inventory_remote_branches.py first", file=sys.stderr)
        return 1
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    cands = candidate_branches(inv)
    if args.limit:
        cands = cands[: args.limit]

    print(f"Total remote branches in inventory: {inv['branch_count']}")
    print(f"Protected (kept):                   {len(PROTECTED)}")
    active_count = sum(1 for b in inv["branches"] if b["last_commit_age_hours"] < KEEP_AGE_HOURS and b["branch"] not in PROTECTED)
    print(f"Active <{KEEP_AGE_HOURS}h (kept):                 {active_count}")
    print(f"Stale >={KEEP_AGE_HOURS}h (delete candidates):   {len(cands)}")
    print()

    if args.inventory:
        from collections import Counter
        cat_counts = Counter(b["category"] for b in cands)
        for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
            print(f"  {cat:24s}: {n}")
        return 0

    # Build the operation plan.
    ops = []
    for b in cands:
        branch = b["branch"]
        tag = archive_tag(branch)
        ops.append({
            "branch": branch,
            "tag": tag,
            "tag_target": f"origin/{branch}",
            "category": b["category"],
            "unmerged_commits": b["unmerged_commits"],
            "last_commit_age_hours": b["last_commit_age_hours"],
        })

    if args.dry_run:
        print(f"Would archive + delete {len(ops)} branches.")
        print()
        print("Sample (first 10):")
        for op in ops[:10]:
            print(f"  tag {op['tag']:80s} -> {op['tag_target']}")
            print(f"  delete origin/{op['branch']}")
        if len(ops) > 10:
            print(f"  ... and {len(ops) - 10} more")
        print()
        print("Re-run with --execute to apply.")
        return 0

    # --execute path. Push tags first, then deletions. Tags first means
    # if the deletion fails, the tag still exists and the branch ref is
    # still on the remote — fully recoverable.
    print("Refreshing origin refs and revalidating stale-branch candidates...")
    run(["git", "fetch", "--prune", "origin"])
    revalidated_ops = []
    skipped = []
    for op in ops:
        branch = op["branch"]
        if branch in PROTECTED:
            skipped.append((branch, "protected branch"))
            continue
        if not remote_ref_exists(branch):
            skipped.append((branch, "remote ref no longer exists"))
            continue
        age = current_age_hours(branch)
        if age is None:
            skipped.append((branch, "could not read current tip age"))
            continue
        if age < KEEP_AGE_HOURS:
            skipped.append((branch, f"current tip is active ({age:.2f}h old)"))
            continue
        op["last_commit_age_hours"] = round(age, 2)
        revalidated_ops.append(op)

    if skipped:
        print("Skipped during live revalidation:")
        for branch, reason in skipped[:20]:
            print(f"  {branch}: {reason}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")
        print()

    ops = revalidated_ops
    print(f"EXECUTING archive + delete for {len(ops)} branches.")
    print()

    # Step 1: create tags locally.
    print("Phase 1: creating local archive tags...")
    for i, op in enumerate(ops, 1):
        try:
            run(["git", "tag", "-f", op["tag"], op["tag_target"]])
        except subprocess.CalledProcessError as e:
            print(f"  FAIL  {op['branch']}: {e.stderr.strip()}", file=sys.stderr)
            continue
        if i % 25 == 0:
            print(f"  ... {i}/{len(ops)} tags created", file=sys.stderr)

    # Step 2: push tags.
    print(f"Phase 2: pushing {len(ops)} archive tags...")
    tag_refs = [f"refs/tags/{op['tag']}" for op in ops]
    # Push in batches of 50 to avoid argv overflow.
    BATCH = 50
    for i in range(0, len(tag_refs), BATCH):
        batch = tag_refs[i:i + BATCH]
        try:
            run(["git", "push", "origin"] + batch)
            print(f"  pushed tags {i + 1}..{i + len(batch)}")
        except subprocess.CalledProcessError as e:
            print(f"  FAIL push batch starting at {i}: {e.stderr.strip()}", file=sys.stderr)
            return 2

    # Step 3: delete remote branches.
    print(f"Phase 3: deleting {len(ops)} remote branches...")
    delete_refs = [f":refs/heads/{op['branch']}" for op in ops]
    for i in range(0, len(delete_refs), BATCH):
        batch = delete_refs[i:i + BATCH]
        try:
            run(["git", "push", "origin"] + batch)
            print(f"  deleted branches {i + 1}..{i + len(batch)}")
        except subprocess.CalledProcessError as e:
            print(f"  FAIL delete batch starting at {i}: {e.stderr.strip()}", file=sys.stderr)
            print("  Tags still exist; recovery: git push origin <tag>:refs/heads/<branch>")
            return 3

    # Step 4: prune local tracking refs that point at the now-deleted branches.
    print("Phase 4: pruning local tracking refs...")
    run(["git", "fetch", "--prune", "origin"])

    print()
    print(f"DONE: archived + deleted {len(ops)} remote branches.")
    print(f"      All recoverable via: git checkout -b <name> archive/<name>-{date.today().isoformat()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
