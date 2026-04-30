#!/usr/bin/env python3
"""Invalidate audits that are stale relative to the current ledger state.

Triggers (any of):

  1. Hash drift on the source note (already handled by seed_audit_ledger.py;
     this script does not duplicate that path).
  2. A dependency was added or removed since audit time. Removing a dependency
     solely because a terminal failed note moved to archive_unlanded/ is ignored:
     that is stale-narrative surface cleanup, not a new proof dependency.
  3. A dependency's effective_status moved to a weaker tier since audit
     time. (A dep getting stronger is fine; getting weaker means the
     audit may have relied on a now-questionable input.)
  4. This claim's criticality tier increased since audit time. A claim
     audited at criticality=medium that is now criticality=critical needs
     re-audit under the stricter cross-confirmation rule.

When triggered, the prior audit fields are archived into previous_audits
with an `invalidation_reason`, and audit_status is reset to unaudited.

Pipeline order: AFTER compute_load_bearing.py and AFTER
compute_effective_status.py have populated criticality and effective_status.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"

# Strength rank used to compare 'before' and 'after' for a dep.
RANK = {
    "retained": 100,
    "promoted": 90,
    "proposed_retained": 80,
    "proposed_promoted": 70,
    "bounded": 60,
    "support": 50,
    "open": 40,
    "unknown": 30,
    "audited_decoration": 20,
    "audited_numerical_match": 15,
    "audited_renaming": 10,
    "audited_conditional": 10,
    "audited_failed": 0,
}

CRITICALITY_RANK = {"leaf": 0, "medium": 1, "high": 2, "critical": 3}

# Audit fields archived on invalidation (mirrors seed_audit_ledger.py).
ARCHIVED_FIELDS = [
    "audit_status",
    "audit_date",
    "auditor",
    "auditor_family",
    "independence",
    "load_bearing_step",
    "load_bearing_step_class",
    "chain_closes",
    "chain_closure_explanation",
    "verdict_rationale",
    "open_dependency_paths",
    "decoration_parent_claim_id",
    "auditor_confidence",
    "runner_check_breakdown",
    "blocker",
    "audit_state_snapshot",
    "cross_confirmation",
]

EMPTY_AFTER_INVALIDATION = {
    "audit_status": "unaudited",
    "audit_date": None,
    "auditor": None,
    "auditor_family": None,
    "independence": None,
    "load_bearing_step": None,
    "load_bearing_step_class": None,
    "chain_closes": None,
    "chain_closure_explanation": None,
    "verdict_rationale": None,
    "open_dependency_paths": [],
    "decoration_parent_claim_id": None,
    "auditor_confidence": None,
    "runner_check_breakdown": {"A": 0, "B": 0, "C": 0, "D": 0, "total_pass": 0},
    "blocker": None,
    "audit_state_snapshot": None,
    "cross_confirmation": None,
}


def detect_invalidation(row: dict, rows: dict[str, dict]) -> str | None:
    snap = row.get("audit_state_snapshot")
    if snap is None:
        return None  # nothing to compare against; treat as fresh

    current_deps = sorted(row.get("deps", []))
    snap_deps = sorted(snap.get("deps", []))
    if current_deps != snap_deps:
        added = sorted(set(current_deps) - set(snap_deps))
        removed = sorted(
            dep
            for dep in set(snap_deps) - set(current_deps)
            if not is_archived_terminal_failed_dep(dep, rows)
        )
        parts = []
        if added:
            parts.append(f"dep_added:{','.join(added[:3])}")
        if removed:
            parts.append(f"dep_removed:{','.join(removed[:3])}")
        if parts:
            return "deps_changed:" + "|".join(parts)

    snap_dep_status = snap.get("dep_effective_status", {})
    for d in current_deps:
        before = snap_dep_status.get(d, "unknown")
        after = rows.get(d, {}).get("effective_status") or rows.get(d, {}).get("current_status") or "unknown"
        if RANK.get(after, -1) < RANK.get(before, -1):
            return f"dep_weakened:{d}:{before}->{after}"

    snap_crit = snap.get("criticality") or "leaf"
    cur_crit = row.get("criticality") or "leaf"
    if CRITICALITY_RANK.get(cur_crit, 0) > CRITICALITY_RANK.get(snap_crit, 0):
        return f"criticality_increased:{snap_crit}->{cur_crit}"

    return None


def is_archived_terminal_failed_dep(dep: str, rows: dict[str, dict]) -> bool:
    dep_row = rows.get(dep)
    if not dep_row:
        return False
    return (
        dep_row.get("audit_status") == "audited_failed"
        and (dep_row.get("note_path") or "").startswith("archive_unlanded/")
    )


def archive_and_reset(row: dict, reason: str) -> dict:
    prior = {k: row.get(k) for k in ARCHIVED_FIELDS}
    prior["archived_at"] = datetime.now(timezone.utc).isoformat()
    prior["invalidation_reason"] = reason
    history = list(row.get("previous_audits", []))
    history.append(prior)
    new_row = dict(row)
    new_row["previous_audits"] = history
    for k, v in EMPTY_AFTER_INVALIDATION.items():
        if isinstance(v, list):
            new_row[k] = list(v)
        elif isinstance(v, dict):
            new_row[k] = dict(v)
        else:
            new_row[k] = v
    return new_row


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    invalidated: list[tuple[str, str]] = []
    for cid, row in rows.items():
        if row.get("audit_status", "unaudited") in {"unaudited", "audit_in_progress"}:
            continue
        reason = detect_invalidation(row, rows)
        if reason is None:
            continue
        rows[cid] = archive_and_reset(row, reason)
        invalidated.append((cid, reason))

    ledger["rows"] = rows
    ledger["invalidation_run_at"] = datetime.now(timezone.utc).isoformat()
    ledger["last_invalidations"] = [{"claim_id": c, "reason": r} for c, r in invalidated]

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    print(f"invalidate_stale_audits: scanned {len(rows)} rows")
    print(f"  invalidated: {len(invalidated)}")
    for cid, reason in invalidated[:10]:
        print(f"    {cid}: {reason}")
    if len(invalidated) > 10:
        print(f"    ... and {len(invalidated) - 10} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
