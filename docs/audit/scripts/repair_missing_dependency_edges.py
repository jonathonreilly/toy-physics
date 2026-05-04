#!/usr/bin/env python3
"""Repair concrete missing dependency edges named by conditional audits.

This script is intentionally mechanical. It reads audit ledger metadata only:
claim ids, note paths, direct deps, audit status, and open_dependency_paths.
It does not inspect prior verdict rationales or decide any audit verdict.

When an audited_conditional row names an existing docs/*.md note in
open_dependency_paths, but that note is not a direct dependency, the script can
append an explicit markdown link to the source note. The normal audit pipeline
then picks up the new edge, changes the source note hash, and resets that row
for fresh re-audit.
"""

from __future__ import annotations

import argparse
import collections
import json
import os
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
MARKER = "## Audit dependency repair links"
INTRO = (
    "This graph-bookkeeping section records explicit dependency links named by "
    "a prior conditional audit so the audit citation graph can track them. It "
    "does not promote this note or change the audited claim scope."
)


def is_repairable_note_path(path: str) -> bool:
    return (
        path.startswith("docs/")
        and not path.startswith("docs/audit/")
        and not path.startswith("docs/ai_methodology/")
        and (REPO_ROOT / path).exists()
    )


def load_rows() -> dict[str, dict]:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return ledger.get("rows", {})


def build_resolvers(rows: dict[str, dict]) -> tuple[dict[str, str], dict[str, list[str]]]:
    path_to_id: dict[str, str] = {}
    stem_to_ids: dict[str, list[str]] = collections.defaultdict(list)
    for cid, row in rows.items():
        note_path = row.get("note_path") or ""
        if not is_repairable_note_path(note_path):
            continue
        path_to_id[note_path.lower()] = cid
        stem_to_ids[PurePosixPath(note_path).stem.lower()].append(cid)
    return path_to_id, stem_to_ids


def resolve_open_dependency_path(
    raw_path: object,
    rows: dict[str, dict],
    path_to_id: dict[str, str],
    stem_to_ids: dict[str, list[str]],
) -> str | None:
    raw = str(raw_path).strip()
    if not raw:
        return None
    raw = raw.replace("_not_registered_one_hop", "")
    if " -> " in raw:
        raw = raw.split(" -> ", 1)[0]
    if not raw.lower().endswith(".md"):
        return None

    cid = path_to_id.get(raw.lower())
    if cid is None:
        matches = stem_to_ids.get(PurePosixPath(raw).stem.lower(), [])
        if len(matches) != 1:
            return None
        cid = matches[0]

    if not is_repairable_note_path(rows[cid].get("note_path") or ""):
        return None
    return cid


def candidate_repairs(rows: dict[str, dict]) -> dict[str, list[str]]:
    path_to_id, stem_to_ids = build_resolvers(rows)
    repairs: dict[str, list[str]] = {}
    for cid, row in rows.items():
        if row.get("audit_status") != "audited_conditional":
            continue
        if not is_repairable_note_path(row.get("note_path") or ""):
            continue

        direct_deps = set(row.get("deps") or [])
        targets: list[str] = []
        for open_path in row.get("open_dependency_paths") or []:
            target = resolve_open_dependency_path(open_path, rows, path_to_id, stem_to_ids)
            if target and target != cid and target not in direct_deps and target not in targets:
                targets.append(target)
        if targets:
            repairs[cid] = targets
    return repairs


def bullet_for(source_path: Path, target_id: str, target_path: Path) -> str:
    rel = os.path.relpath(target_path, source_path.parent).replace(os.sep, "/")
    return f"- [{target_id}]({rel})"


def apply_repairs(rows: dict[str, dict], repairs: dict[str, list[str]], apply: bool) -> tuple[int, int]:
    changed_files = 0
    added_edges = 0
    for source_id, targets in sorted(repairs.items()):
        source_path = REPO_ROOT / rows[source_id]["note_path"]
        text = source_path.read_text(encoding="utf-8")
        bullets: list[str] = []
        for target_id in targets:
            target_path = REPO_ROOT / rows[target_id]["note_path"]
            bullet = bullet_for(source_path, target_id, target_path)
            link_fragment = bullet.rsplit("](", 1)[1].rstrip(")")
            if bullet not in text and f"]({link_fragment})" not in text:
                bullets.append(bullet)
        if not bullets:
            continue

        changed_files += 1
        added_edges += len(bullets)
        if not apply:
            continue

        addition = "\n".join(bullets) + "\n"
        if MARKER in text:
            next_text = text.rstrip() + "\n" + addition
        else:
            next_text = text.rstrip() + f"\n\n{MARKER}\n\n{INTRO}\n\n{addition}"
        source_path.write_text(next_text, encoding="utf-8")
    return changed_files, added_edges


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write repair links; without this flag, only report candidates",
    )
    args = parser.parse_args()

    rows = load_rows()
    repairs = candidate_repairs(rows)
    changed_files, added_edges = apply_repairs(rows, repairs, args.apply)
    mode = "applied" if args.apply else "dry_run"
    print(f"repair_missing_dependency_edges: {mode}")
    print(f"  candidate_rows: {len(repairs)}")
    print(f"  changed_files: {changed_files}")
    print(f"  dependency_edges: {added_edges}")
    if args.apply:
        print("  next: bash docs/audit/scripts/run_pipeline.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
