#!/usr/bin/env python3
"""Invalidate every audit row whose verdict was minted below the
gpt-5.5 codex floor. The audit lane policy as of 2026-05-06 is:

    All new audit verdicts must be minted by codex-gpt-5.5 (or newer)
    at xhigh reasoning effort.

This script enforces the policy retroactively against the existing
ledger:

  - For each row whose CURRENT auditor_family is sub-floor codex
    (e.g. codex-gpt-5, codex-gpt-5.4, codex-gpt-4.x), or any
    cross_confirmation tier (first/second/third audit) was minted
    below the floor, archive the prior audit fields into
    `previous_audits` and reset the row to `unaudited`.

  - The row's note text and runner stay untouched. Only the audit-
    side state is rolled back.

  - The audit-loop will pick the row up naturally on its next batch
    and re-mint the verdict via codex-gpt-5.5+ at xhigh.

This is destructive in the sense that publication-tier `audited_clean`
status is temporarily revoked while the re-audit runs — that is
intentional. Per the policy, those rows should never have been
ratified by sub-floor evidence.

Approved families (NOT invalidated):

  - codex-gpt-5.5 and any newer codex-gpt-* (rank >= (5, 5))
  - non-codex families (claude-*, legacy-confirmed-clean,
    judicial-review-*, human-*) — these are not bound by the codex
    model schedule. The user can list-narrow further via
    --extra-invalidate-family.

Sub-floor families that ARE invalidated by default:

  - codex-gpt-5, codex-gpt-5.4, codex-gpt-5.3, codex-gpt-5.2,
    codex-gpt-4.x, etc.
  - opaque codex-* families that don't parse to a numeric version
    (codex-current, codex-fresh-agent, codex-legacy, codex-cli)

Usage
-----
    # Dry-run (show counts, no mutation)
    python3 scripts/invalidate_sub_floor_audits.py --dry-run

    # Apply
    python3 scripts/invalidate_sub_floor_audits.py

    # Restrict to specific families
    python3 scripts/invalidate_sub_floor_audits.py --only-family codex-gpt-5

    # Add to the invalidate set (e.g., a one-off audit-id you want gone)
    python3 scripts/invalidate_sub_floor_audits.py \
        --extra-invalidate-family codex-fresh-agent

After this script runs, run the pipeline to refresh effective_status
and the audit queue:

    bash docs/audit/scripts/run_pipeline.sh
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

MIN_CODEX_FAMILY_RANK = (5, 5)
CODEX_FAMILY_RE = re.compile(r"^codex-gpt-(\d+(?:\.\d+)?)$")

# Audit fields archived on invalidation (mirror of seed_audit_ledger.AUDIT_FIELDS).
AUDIT_FIELDS = [
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
]
EMPTY_AUDIT = {
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
    "runner_check_breakdown": None,
    "blocker": None,
    "audit_state_snapshot": None,
    "cross_confirmation": None,
    "claim_type": None,
    "claim_scope": None,
}


def family_rank(family: str | None) -> tuple[int, ...] | None:
    if not family:
        return None
    m = CODEX_FAMILY_RE.match(family)
    if not m:
        return None
    return tuple(int(p) for p in m.group(1).split("."))


def family_is_codex(family: str | None) -> bool:
    if not family:
        return False
    return bool(family.startswith("codex-")) or bool(family.startswith("openai-"))


def codex_family_meets_floor(family: str | None) -> bool:
    """True iff family is codex-gpt-X.Y at rank >= MIN_CODEX_FAMILY_RANK."""
    if not family:
        return False
    rank = family_rank(family)
    if not rank:
        return False
    floor = MIN_CODEX_FAMILY_RANK
    width = max(len(rank), len(floor))
    rank_padded = rank + (0,) * (width - len(rank))
    floor_padded = floor + (0,) * (width - len(floor))
    return rank_padded >= floor_padded


def is_sub_floor_codex(family: str | None,
                       extra_invalidate: set[str]) -> bool:
    """True iff this family triggers invalidation under the default policy.

    Extra-invalidate families are also caught (operator opt-in).
    """
    if not family:
        return False
    if family in extra_invalidate:
        return True
    # codex-gpt-X.Y below floor
    rank = family_rank(family)
    if rank:
        return not codex_family_meets_floor(family)
    # Opaque codex-* (no parseable version) — treat as sub-floor by default.
    if family.startswith("codex-") and family not in {
        "codex-gpt-5.5",  # exact match handled by rank above; defensive
    }:
        return True
    return False


def should_invalidate(row: dict, extra_invalidate: set[str],
                      only_families: set[str] | None) -> tuple[bool, str]:
    """Return (invalidate, reason) for one ledger row."""
    cur_family = row.get("auditor_family")
    if only_families:
        # Operator-restricted set: invalidate only rows whose CURRENT
        # auditor_family matches one of these. Cross-confirmation
        # tiers are not checked in this mode.
        if cur_family in only_families:
            return True, f"current_family={cur_family!r} in --only-family"
        return False, ""

    if is_sub_floor_codex(cur_family, extra_invalidate):
        return True, f"current_family={cur_family!r} is sub-floor"

    # Cross-confirmation tiers: any sub-floor tier invalidates the row.
    xc = row.get("cross_confirmation") or {}
    for slot in ("first_audit", "second_audit", "third_audit"):
        a = xc.get(slot) or {}
        f = a.get("auditor_family")
        if is_sub_floor_codex(f, extra_invalidate):
            return True, f"cross_confirmation.{slot}.auditor_family={f!r} is sub-floor"

    return False, ""


def invalidate_row(row: dict, reason: str) -> dict:
    """Archive the prior audit into previous_audits, reset to unaudited."""
    prior = {k: row.get(k) for k in AUDIT_FIELDS}
    prior["archived_at"] = datetime.now(timezone.utc).isoformat()
    prior["archived_for_note_hash"] = row.get("note_hash")
    prior["invalidation_reason"] = reason
    prior["invalidated_by"] = "invalidate_sub_floor_audits.py"
    history = list(row.get("previous_audits", []))
    history.append(prior)
    new_row = dict(row)
    new_row["previous_audits"] = history
    for k, v in EMPTY_AUDIT.items():
        new_row[k] = v if not isinstance(v, list) else list(v)
    return new_row


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Print counts and per-row reasons; do not mutate.")
    p.add_argument("--only-family", action="append", default=[],
                   help="Restrict to rows with this exact auditor_family. "
                        "Repeatable. When set, the cross-confirmation "
                        "checks are skipped — only current-family is used.")
    p.add_argument("--extra-invalidate-family", action="append", default=[],
                   help="Add a family name to the invalidate set on top "
                        "of the default sub-floor codex check. Repeatable.")
    args = p.parse_args()

    if not LEDGER_PATH.exists():
        print(f"Ledger missing: {LEDGER_PATH}")
        return 1

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})
    if not rows:
        print("Ledger has no rows")
        return 1

    only_families = set(args.only_family) if args.only_family else None
    extra_invalidate = set(args.extra_invalidate_family)

    plan: list[tuple[str, str]] = []
    family_counts: Counter = Counter()
    status_counts: Counter = Counter()
    for cid, r in rows.items():
        do_inv, reason = should_invalidate(r, extra_invalidate, only_families)
        if do_inv:
            plan.append((cid, reason))
            family_counts[r.get("auditor_family")] += 1
            status_counts[r.get("audit_status")] += 1

    print(f"Total rows considered: {len(rows)}")
    print(f"To invalidate:         {len(plan)}")
    print()
    print("Current auditor_family distribution among invalidations:")
    for f, n in family_counts.most_common(15):
        print(f"  {n:5d}  {f}")
    print()
    print("Current audit_status distribution among invalidations:")
    for s, n in status_counts.most_common():
        print(f"  {n:5d}  {s}")

    if args.dry_run:
        print()
        print("[dry-run] First 20 candidates:")
        for cid, reason in plan[:20]:
            print(f"  {cid[:60]:<60}  {reason}")
        if len(plan) > 20:
            print(f"  ... and {len(plan) - 20} more")
        return 0

    if not plan:
        print("\nNothing to invalidate. exit 0.")
        return 0

    print(f"\nApplying invalidation to {len(plan)} rows ...")
    for cid, reason in plan:
        rows[cid] = invalidate_row(rows[cid], reason)

    ledger["rows"] = rows
    LEDGER_PATH.write_text(
        json.dumps(ledger, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print()
    print("Next steps:")
    print("  1. Run the pipeline to refresh effective_status / queue:")
    print("       bash docs/audit/scripts/run_pipeline.sh")
    print("  2. Commit the regenerated ledger + downstream files.")
    print("  3. Run the audit-loop; the invalidated rows are now in the queue:")
    print("       python3 scripts/codex_audit_runner.py --n 50")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
