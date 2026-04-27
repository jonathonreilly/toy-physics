#!/usr/bin/env python3
"""Science archaeology: snapshot every novel file from to-be-deleted
branches into the consolidation tree.

Reads docs/audit/data/branch_inventory.json. For every branch that:
  - has age >= 24h, AND
  - is not the audit-lane / main / a kept branch, AND
  - has at least one novel_path (a file added that does not exist on
    origin/main),

copies that branch's version of each novel file into:
  archive_unlanded/<branch_safe_name>/<original_path>

Also writes a top-level archive_unlanded/MANIFEST.md listing every
branch, its novel files, last commit date, and last commit subject.

Run from the consolidation branch (`cleanup-consolidation-...`); the
script writes into the working tree only.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
INVENTORY = DATA_DIR / "branch_inventory.json"
PAIRS = DATA_DIR / "branch_pairs.json"
DEST_ROOT = REPO_ROOT / "archive_unlanded"
MANIFEST = DEST_ROOT / "MANIFEST.md"

KEEP_AGE_HOURS = 24


def safe_branch_name(branch: str) -> str:
    return branch.replace("/", "__").replace(" ", "_")


def run(cmd: list[str]) -> str:
    return subprocess.run(
        cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout


def file_at_branch(branch: str, path: str) -> bytes | None:
    try:
        out = subprocess.run(
            ["git", "show", f"origin/{branch}:{path}"],
            cwd=REPO_ROOT, capture_output=True, check=True,
        )
        return out.stdout
    except subprocess.CalledProcessError:
        return None


def main() -> int:
    inv = json.loads(INVENTORY.read_text(encoding="utf-8"))
    pairs = json.loads(PAIRS.read_text(encoding="utf-8")) if PAIRS.exists() else None

    pair_classification: dict[str, str] = {}
    if pairs:
        for entry in pairs.get("branches", []):
            pair_classification[entry["branch"]] = entry["classification"]

    DEST_ROOT.mkdir(parents=True, exist_ok=True)

    snapshot_log: list[dict] = []
    files_written = 0

    for b in inv["branches"]:
        if b["last_commit_age_hours"] < KEEP_AGE_HOURS:
            continue
        if b["branch"] in {"audit-lane", "main", "HEAD"}:
            continue
        if not b["novel_paths"]:
            continue

        branch = b["branch"]
        slug = safe_branch_name(branch)
        per_branch_dir = DEST_ROOT / slug
        per_branch_dir.mkdir(parents=True, exist_ok=True)
        branch_files = []

        for path in b["novel_paths"]:
            content = file_at_branch(branch, path)
            if content is None:
                continue
            target = per_branch_dir / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            files_written += 1
            branch_files.append(path)

        snapshot_log.append({
            "branch": branch,
            "last_commit_iso": b["last_commit_iso"],
            "last_commit_age_hours": b["last_commit_age_hours"],
            "last_commit_subject": b["last_commit_subject"],
            "unmerged_commits": b["unmerged_commits"],
            "category": b["category"],
            "pair_classification": pair_classification.get(branch),
            "novel_files_snapshotted": branch_files,
            "novel_file_count": len(branch_files),
            "snapshot_path": f"archive_unlanded/{slug}/",
        })

    # Group by classification for the manifest.
    by_classification: dict[str, list[dict]] = {}
    for entry in snapshot_log:
        cls = entry.get("pair_classification") or "other"
        by_classification.setdefault(cls, []).append(entry)

    # Write a JSON sidecar.
    log_path = DEST_ROOT / "snapshot_log.json"
    log_path.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "branch_count": len(snapshot_log),
        "files_written": files_written,
        "branches": sorted(snapshot_log, key=lambda x: x["branch"]),
    }, indent=2, sort_keys=True) + "\n")

    # Write the human-readable manifest.
    md_lines = [
        "# archive_unlanded — Science Archaeology Snapshot",
        "",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}  ",
        f"**Source:** every remote branch with `last_commit_age_hours >= "
        f"{KEEP_AGE_HOURS}` whose `git diff origin/main...<branch>` adds "
        "files that do not exist on `origin/main`.",
        "",
        f"**Branches snapshotted:** {len(snapshot_log)}  ",
        f"**Unique files preserved:** {files_written}",
        "",
        "Each branch's novel content is preserved verbatim under "
        "`archive_unlanded/<branch_safe_name>/<original_path>`. The "
        "branches themselves are scheduled for archival (tag + delete) "
        "after this commit lands. Recovery of any individual branch "
        "remains possible via `git checkout archive/<branch>-<date>`.",
        "",
        "## Reading guide",
        "",
        "- `pair_classification: is_codex_review_or_land` — branch is "
        "  itself a Codex review/land branch; preserves the post-review "
        "  version of the science.",
        "- `pair_classification: reviewed_unlanded` — Claude proposal "
        "  that has a Codex review partner; both versions preserved here "
        "  (look for the matching `codex/...` slug).",
        "- `pair_classification: unreviewed_unlanded` — Claude proposal "
        "  with no Codex review partner; this is the highest-priority "
        "  bucket for the audit lane to triage.",
        "",
    ]
    for cls in (
        "unreviewed_unlanded",
        "reviewed_unlanded",
        "is_codex_review_or_land",
        "other",
    ):
        entries = by_classification.get(cls, [])
        if not entries:
            continue
        md_lines.append(f"## {cls} ({len(entries)} branches)")
        md_lines.append("")
        md_lines.append(
            "| branch | files | age (h) | last commit subject |"
        )
        md_lines.append("|---|---:|---:|---|")
        for e in sorted(entries, key=lambda x: x["branch"]):
            subj = (e["last_commit_subject"] or "").replace("|", "\\|")[:80]
            md_lines.append(
                f"| `{e['branch']}` | {e['novel_file_count']} | "
                f"{e['last_commit_age_hours']:.0f} | {subj} |"
            )
        md_lines.append("")

    MANIFEST.write_text("\n".join(md_lines) + "\n")

    print(f"Wrote {DEST_ROOT.relative_to(REPO_ROOT)}/")
    print(f"  branches snapshotted: {len(snapshot_log)}")
    print(f"  files preserved:      {files_written}")
    print(f"  manifest:             {MANIFEST.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
