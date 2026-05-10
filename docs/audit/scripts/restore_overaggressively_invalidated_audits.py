#!/usr/bin/env python3
"""One-shot restoration of audits over-aggressively invalidated before
PR #907's policy refinement of `criticality_increased` and the
soft-reset propagation rule in `compute_effective_status`.

Two categories of archived audits are restored:

  1. `criticality_increased:before->after` invalidations where PR #907's
     `_categorize_criticality_bump` would have returned `noop` or
     `soft_reset`. Concretely:

       - `before -> medium` / `before -> leaf` are no-op (no new
         requirement). Restored back to the archived state.
       - `before -> high` is no-op when the archived audit had
         `independence != weak`. Restored.
       - `before -> critical` is no-op when cross-confirmation was
         already on file, OR soft-reset when the archived audit was
         `audited_clean` with non-weak independence and no
         cross-confirmation. Restored in both sub-cases; the next
         pipeline run will soft-reset where appropriate.

     Bumps where the audit fundamentally fails the new tier
     (`audited_clean` + `independence == weak` -> high/critical) are
     NOT restored — `_categorize_criticality_bump` would still return
     `invalidate`.

  2. `dep_weakened:dep_id:before->after` invalidations whose `dep_id` is
     in our category-1 restore set. After restoration, the dep will go
     through soft-reset and PR #907's
     `is_criticality_bump_soft_reset` propagation will hold its
     effective_status at retained-grade. The downstream row's
     dep_weakened trigger therefore won't fire on the next pipeline
     run, so the restored audit stays clean.

Other invalidation reasons (`note_hash` drift handled by
`seed_audit_ledger.py`, `runner_hash_changed`, `deps_changed`,
`dep_claim_type_changed`, `dep_claim_scope_changed`,
`runner_artifact_issue_resolved`) are NOT touched; those reflect real
state changes that genuinely invalidated the audit.

Idempotent: only operates on currently-`unaudited` rows. Running twice
is a no-op on the second run.

Sequencing:

  1. PR #907 must be merged (the policy code that holds soft-reset
     deps at retained-grade and produces the new `criticality_soft_reset`
     reason class).
  2. Run this script (modifies the ledger).
  3. Run `bash docs/audit/scripts/run_pipeline.sh` to propagate.
     `invalidate_stale_audits.py` will see the restored audits and
     soft-reset the criticality-bumped clean rows;
     `compute_effective_status.py` will hold their effective_status at
     retained-grade so downstream rows stay valid.

Usage:
  python3 docs/audit/scripts/restore_overaggressively_invalidated_audits.py [--dry-run] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"

# Mirror of `invalidate_stale_audits.ARCHIVED_FIELDS`. These are the
# audit-owned fields that `archive_and_reset` snapshots into
# previous_audits[-1] before zeroing the live row. Restoration copies
# them back. The two metadata fields `archived_at` and
# `invalidation_reason` are not restored — they describe the archive
# itself.
ARCHIVED_FIELDS = (
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
    "claim_type",
    "claim_scope",
    "claim_type_provenance",
    "claim_type_last_reviewed",
    "notes_for_re_audit_if_any",
)


def categorize_criticality_bump_for_archived(archived: dict, target_criticality: str) -> str:
    """Mirror `invalidate_stale_audits._categorize_criticality_bump` for an
    archived audit blob (in `previous_audits`).

    MUST STAY IN SYNC with the live policy in
    `docs/audit/scripts/invalidate_stale_audits.py`.

    Returns one of `"noop"`, `"soft_reset"`, `"invalidate"`.
    """
    if target_criticality in ("leaf", "medium"):
        return "noop"
    audit_status = archived.get("audit_status")
    indep = archived.get("independence")
    if audit_status != "audited_clean":
        return "noop"
    if indep is None or indep == "weak":
        return "invalidate"
    if target_criticality == "high":
        return "noop"
    cc = archived.get("cross_confirmation") or {}
    cc_status = cc.get("status") if isinstance(cc, dict) else None
    if cc_status in {"confirmed", "third_confirmed_first", "third_confirmed_second"}:
        return "noop"
    return "soft_reset"


def parse_criticality_increased_target(reason: str) -> str | None:
    """Parse the `after` tier from `criticality_increased:before->after`."""
    if not reason.startswith("criticality_increased:"):
        return None
    payload = reason[len("criticality_increased:"):]
    if "->" not in payload:
        return None
    return payload.split("->", 1)[1].strip() or None


def parse_dep_weakened_dep_id(reason: str) -> str | None:
    """Parse `dep_id` from `dep_weakened:dep_id:before->after`."""
    if not reason.startswith("dep_weakened:"):
        return None
    parts = reason.split(":", 2)
    if len(parts) < 3:
        return None
    return parts[1] or None


def restore_audit_from_previous(row: dict) -> dict | None:
    """Pop the most recent previous_audits entry and copy its archived
    fields back to the live row. Returns the new row, or None if there's
    nothing to restore.
    """
    history = list(row.get("previous_audits") or [])
    if not history:
        return None
    archived = history.pop()
    new_row = dict(row)
    new_row["previous_audits"] = history
    for field in ARCHIVED_FIELDS:
        if field in archived:
            new_row[field] = archived[field]
    return new_row


def select_restore_candidates(rows: dict[str, dict]) -> tuple[dict[str, str], list[tuple[str, str, str]]]:
    """First pass: find rows that should be restored under PR #907's policy.

    Returns:
      - `crit_set`: dict mapping `cid` -> archived `audit_status`
        (e.g. `audited_clean`, `audited_conditional`, ...) for rows whose
        most recent invalidation was a `criticality_increased:*` that
        the new rule would have noop'd or soft_reset'd.
      - `dep_weakened_set`: list of `(cid, dep_id, archived_status)`
        tuples for rows whose most recent invalidation was a
        `dep_weakened:*` whose dep is in `crit_set`.
    """
    crit_set: dict[str, str] = {}
    dep_weakened_candidates: list[tuple[str, str, dict]] = []

    for cid, row in rows.items():
        if row.get("audit_status") != "unaudited":
            continue
        history = row.get("previous_audits") or []
        if not history:
            continue
        archived = history[-1]
        reason = archived.get("invalidation_reason") or ""

        target = parse_criticality_increased_target(reason)
        if target is not None:
            action = categorize_criticality_bump_for_archived(archived, target)
            if action in ("noop", "soft_reset"):
                crit_set[cid] = archived.get("audit_status") or "?"
            continue

        dep_id = parse_dep_weakened_dep_id(reason)
        if dep_id is not None:
            dep_weakened_candidates.append((cid, dep_id, archived))
            continue

    dep_weakened_set: list[tuple[str, str, str]] = []
    for cid, dep_id, archived in dep_weakened_candidates:
        if dep_id in crit_set:
            dep_weakened_set.append((cid, dep_id, archived.get("audit_status") or "?"))

    return crit_set, dep_weakened_set


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Restore audits over-aggressively invalidated before PR #907's "
            "criticality_increased / dep_weakened policy refinement."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Identify and report restore candidates without modifying the ledger.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap the number of rows restored (per category). For testing.",
    )
    args = parser.parse_args()

    if not LEDGER_PATH.exists():
        print(f"FAIL: ledger missing at {LEDGER_PATH}", file=sys.stderr)
        return 1

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows: dict[str, dict] = ledger.get("rows", {})

    crit_set, dep_weakened_set = select_restore_candidates(rows)

    if args.limit is not None:
        crit_items = sorted(crit_set.items())[: args.limit]
        crit_set = dict(crit_items)
        dep_weakened_set = dep_weakened_set[: args.limit]

    print(f"Identified {len(crit_set)} criticality_increased restore candidates:")
    crit_status_counts: dict[str, int] = {}
    for cid, prev_status in crit_set.items():
        crit_status_counts[prev_status] = crit_status_counts.get(prev_status, 0) + 1
    for status, n in sorted(crit_status_counts.items(), key=lambda x: -x[1]):
        print(f"    {n:5d}  was {status}")

    print(f"Identified {len(dep_weakened_set)} dep_weakened restore candidates"
          f" (cascade from criticality_increased deps):")
    dep_status_counts: dict[str, int] = {}
    for _cid, _dep, prev_status in dep_weakened_set:
        dep_status_counts[prev_status] = dep_status_counts.get(prev_status, 0) + 1
    for status, n in sorted(dep_status_counts.items(), key=lambda x: -x[1]):
        print(f"    {n:5d}  was {status}")

    if args.dry_run:
        print("\nDry run: no changes written.")
        return 0

    restored_count = 0
    for cid in crit_set:
        new_row = restore_audit_from_previous(rows[cid])
        if new_row is None:
            continue
        rows[cid] = new_row
        restored_count += 1
    for cid, _dep, _prev in dep_weakened_set:
        new_row = restore_audit_from_previous(rows[cid])
        if new_row is None:
            continue
        rows[cid] = new_row
        restored_count += 1

    ledger["rows"] = rows
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    print()
    print(f"Restored {restored_count} audits across {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print()
    print("NEXT: run `bash docs/audit/scripts/run_pipeline.sh` to propagate. "
          "PR #907 must already be live on the running branch — otherwise the "
          "next nightly will re-invalidate under the old rule.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
