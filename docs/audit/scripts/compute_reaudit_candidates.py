#!/usr/bin/env python3
"""Produce re-audit candidates unblocked by newly ratified dependencies.

This detector is intentionally separate from invalidation. A dependency
getting weaker invalidates an audit; a dependency getting stronger can make a
previously conditional scoped claim worth a fresh clean-context re-audit.

Candidate policy:
  1. claim is a theorem/no-go/open-gate row, not metadata or decoration;
  2. claim has a terminal non-clean audit verdict;
  3. every current one-hop dependency is retained-grade;
  4. at least one audit-time dependency status was not retained-grade but is now.

Writes:
  - data/reaudit_candidates.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
CANDIDATES_JSON = DATA_DIR / "reaudit_candidates.json"

CRITICALITY_RANK = {"critical": 3, "high": 2, "medium": 1, "leaf": 0}
RATIFIED_DEP_STATUSES = {"retained", "retained_no_go", "retained_bounded"}
ELIGIBLE_CLAIM_TYPES = {"positive_theorem", "bounded_theorem", "no_go", "open_gate"}
ELIGIBLE_AUDIT_STATUSES = {
    "audited_conditional",
    "audited_renaming",
    "audited_decoration",
    "audited_numerical_match",
    "audited_failed",
}

# Must stay in sync with compute_effective_status.py RANK.
STATUS_RANK = {
    "retained": 100,
    "retained_no_go": 100,
    "retained_bounded": 95,
    "retained_pending_chain": 80,
    "open_gate": 40,
    "unaudited": 30,
    "audit_in_progress": 30,
    "meta": 25,
    "audited_decoration": 20,
    "audited_numerical_match": 15,
    "audited_renaming": 10,
    "audited_conditional": 10,
    "audited_failed": 0,
}


def dep_effective_status(dep_id: str, rows: dict[str, dict]) -> str:
    dep = rows.get(dep_id) or {}
    return dep.get("effective_status") or "unaudited"


def status_rank(status: str | None) -> int:
    if status and status.startswith("decoration_under_"):
        return 70
    return STATUS_RANK.get(status or "unaudited", -1)


def improved_ratified_deps(row: dict, rows: dict[str, dict]) -> list[dict]:
    snap = row.get("audit_state_snapshot") or {}
    snap_dep_status = snap.get("dep_effective_status") or {}

    improved: list[dict] = []
    for dep_id, before in sorted(snap_dep_status.items()):
        after = dep_effective_status(dep_id, rows)
        if after not in RATIFIED_DEP_STATUSES:
            continue
        if before in RATIFIED_DEP_STATUSES:
            continue
        before_rank = status_rank(before)
        after_rank = status_rank(after)
        if after_rank <= before_rank:
            continue
        improved.append(
            {
                "claim_id": dep_id,
                "before_effective_status": before,
                "after_effective_status": after,
                "rank_delta": after_rank - before_rank,
            }
        )
    return improved


def current_deps_are_ratified(row: dict, rows: dict[str, dict]) -> bool:
    deps = row.get("deps", [])
    if not deps:
        return False
    return all(dep_effective_status(dep_id, rows) in RATIFIED_DEP_STATUSES for dep_id in deps)


def candidate_entry(cid: str, row: dict, rows: dict[str, dict], improved: list[dict]) -> dict:
    criticality = row.get("criticality") or "leaf"
    return {
        "claim_id": cid,
        "note_path": row.get("note_path"),
        "runner_path": row.get("runner_path"),
        "claim_type": row.get("claim_type"),
        "claim_scope": row.get("claim_scope"),
        "audit_status": row.get("audit_status"),
        "effective_status": row.get("effective_status"),
        "criticality": criticality,
        "criticality_rank": CRITICALITY_RANK.get(criticality, 0),
        "transitive_descendants": row.get("transitive_descendants", 0),
        "direct_in_degree": row.get("direct_in_degree", 0),
        "load_bearing_score": row.get("load_bearing_score", 0.0),
        "note_hash": row.get("note_hash"),
        "deps": list(row.get("deps", [])),
        "current_dep_effective_status": {
            dep_id: dep_effective_status(dep_id, rows) for dep_id in row.get("deps", [])
        },
        "reraudit_after_claim_ids": [dep["claim_id"] for dep in improved],
        "improved_dependencies": improved,
        "candidate_reason": "all_deps_ratified_after_audit_time_dependency_strengthening",
        "audit_independence_required": (
            "fresh_context_or_stronger_with_cross_confirmation"
            if criticality == "critical"
            else "fresh_context_or_stronger"
            if criticality == "high"
            else "any_non_self"
        ),
    }


def sort_key(entry: dict) -> tuple:
    return (
        -entry["criticality_rank"],
        -entry["transitive_descendants"],
        -entry["load_bearing_score"],
        entry["claim_id"],
    )


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing")

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    candidates: list[dict] = []
    for cid, row in rows.items():
        if row.get("claim_type") not in ELIGIBLE_CLAIM_TYPES:
            continue
        if row.get("audit_status") not in ELIGIBLE_AUDIT_STATUSES:
            continue
        if not current_deps_are_ratified(row, rows):
            continue
        improved = improved_ratified_deps(row, rows)
        if not improved:
            continue
        candidates.append(candidate_entry(cid, row, rows, improved))

    candidates.sort(key=sort_key)
    for idx, entry in enumerate(candidates, 1):
        entry["generated_order"] = idx

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": "reaudit_unblocked_by_ratified_dependencies_v1",
        "policy_summary": (
            "Non-clean audited theorem/no-go/open-gate claims whose current "
            "one-hop dependencies are all retained-grade and whose audit-time "
            "dependency snapshot contains at least one dependency that has "
            "since become retained-grade."
        ),
        "eligible_claim_types": sorted(ELIGIBLE_CLAIM_TYPES),
        "eligible_audit_statuses": sorted(ELIGIBLE_AUDIT_STATUSES),
        "ratified_dependency_statuses": sorted(RATIFIED_DEP_STATUSES),
        "total_candidates": len(candidates),
        "by_criticality": {
            criticality: sum(1 for c in candidates if c["criticality"] == criticality)
            for criticality in ("critical", "high", "medium", "leaf")
        },
        "candidates": candidates,
    }

    CANDIDATES_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {CANDIDATES_JSON.relative_to(REPO_ROOT)}")
    print(f"  total candidates: {output['total_candidates']}")
    print(f"  by criticality: {output['by_criticality']}")
    if candidates:
        print("  top candidates:")
        for entry in candidates[:5]:
            print(
                "    "
                f"{entry['generated_order']}. {entry['claim_id']} "
                f"({entry['criticality']}, after "
                f"{','.join(entry['reraudit_after_claim_ids'])})"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
