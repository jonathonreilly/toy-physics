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
     in our category-1 restore set AND whose restored effective tier is
     at least as strong as the downstream audit's recorded `before`
     tier. This preserves downstream audits only when the dependency
     really returns to the state the downstream audit closed against.
     If the dependency restores to a still-weaker terminal verdict
     (for example `audited_numerical_match -> audited_conditional`),
     the downstream audit is left invalidated.

Other invalidation reasons (`note_hash` drift handled by
`seed_audit_ledger.py`, `runner_hash_changed`, `deps_changed`,
`dep_claim_type_changed`, `dep_claim_scope_changed`,
`runner_artifact_issue_resolved`) are NOT touched; those reflect real
state changes that genuinely invalidated the audit.

Both restoration categories also require the archived audit to satisfy
current audit-lane lint requirements (claim_type, claim_scope, repair
class prefix for audited_conditional rows, and current auditor-family
floor). Older archived audits that do not meet those requirements remain
invalidated for fresh audit.

Direct `criticality_increased:*` candidates are also checked for other
still-live invalidation reasons (dependency set drift, dependency status
weakening, dependency claim_type/scope drift). If any non-criticality
blocker would immediately re-fire, the audit remains invalidated.

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
import re
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

RANK = {
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

CLAIM_TYPE_TO_RETAINED = {
    "positive_theorem": "retained",
    "no_go": "retained_no_go",
    "bounded_theorem": "retained_bounded",
}

ALLOWED_CLAIM_TYPES = {
    "positive_theorem",
    "bounded_theorem",
    "no_go",
    "open_gate",
    "decoration",
    "meta",
}
ALLOWED_INDEPENDENCE = {"weak", "fresh_context", "cross_family", "strong", "external", "judicial_review", None}
ALLOWED_REPAIR_CLASSES = {
    "missing_dependency_edge",
    "dependency_not_retained",
    "missing_bridge_theorem",
    "scope_too_broad",
    "runner_artifact_issue",
    "compute_required",
    "other",
}
CANONICAL_AUDITOR_FAMILIES = {
    "codex-gpt-5",
    "codex-gpt-5.5",
    "codex-gpt-5.6",
    "codex-gpt-5.7",
    "codex-gpt-6",
    "claude-opus",
    "claude-sonnet",
    "human",
    "external",
    "legacy-confirmed-clean",
}
LEGACY_AUDITOR_FAMILIES = {
    "codex-current",
    "codex-fresh",
    "codex-fresh-agent",
    "codex-fresh-context",
}
TERMINAL_VERDICTS = {
    "audited_clean",
    "audited_renaming",
    "audited_conditional",
    "audited_decoration",
    "audited_failed",
    "audited_numerical_match",
}
_CODEX_FAMILY_RE = re.compile(r"^codex-gpt-(\d+(?:\.\d+)*)$")


def codex_family_meets_minimum(family: str, minimum: str = "gpt-5.5") -> bool:
    if not isinstance(family, str) or not family.startswith("codex-gpt-"):
        return True
    fam_match = _CODEX_FAMILY_RE.match(family)
    if not fam_match:
        return True
    min_match = re.match(r"gpt-(\d+(?:\.\d+)*)", minimum)
    if not min_match:
        return True
    fam_rank = tuple(int(part) for part in fam_match.group(1).split("."))
    min_rank = tuple(int(part) for part in min_match.group(1).split("."))
    width = max(len(fam_rank), len(min_rank))
    fam_padded = fam_rank + (0,) * (width - len(fam_rank))
    min_padded = min_rank + (0,) * (width - len(min_rank))
    return fam_padded >= min_padded


def repair_class_is_valid(notes: str | None) -> bool:
    if not notes:
        return False
    first_token = notes.strip().split(":", 1)[0].strip().split()[0].lower() if notes.strip() else ""
    return first_token in ALLOWED_REPAIR_CLASSES


def archived_audit_is_lint_compatible(archived: dict) -> bool:
    """True if restoring this archived audit will satisfy current audit lint.

    The restoration path should not turn old archived evidence into live
    authority when current lint would immediately queue or reject it. Rows
    that fail these checks remain invalidated and should be re-audited.
    """
    audit_status = archived.get("audit_status")
    if audit_status not in TERMINAL_VERDICTS:
        return False
    if archived.get("claim_type") not in ALLOWED_CLAIM_TYPES:
        return False
    if not archived.get("claim_scope"):
        return False
    if archived.get("independence") not in ALLOWED_INDEPENDENCE:
        return False
    if audit_status == "audited_conditional":
        if not repair_class_is_valid(archived.get("notes_for_re_audit_if_any")):
            return False

    fam = archived.get("auditor_family")
    if fam is not None:
        if fam not in CANONICAL_AUDITOR_FAMILIES and fam not in LEGACY_AUDITOR_FAMILIES:
            if not (isinstance(fam, str) and fam.startswith("codex-gpt-")):
                return False
        if fam in LEGACY_AUDITOR_FAMILIES:
            return False
        if isinstance(fam, str) and fam.startswith("codex-gpt-"):
            if not codex_family_meets_minimum(fam):
                return False

    return True


def status_rank(status: str | None) -> int:
    if status and status.startswith("decoration_under_"):
        return 70
    return RANK.get(status or "unaudited", -1)


def estimate_restored_effective_status(archived: dict) -> str:
    """Conservative effective-status estimate for an archived audit once restored.

    This is used only to decide whether a downstream `dep_weakened:*`
    invalidation can also be restored. For clean theorem/no-go/bounded rows,
    use the retained grade implied by the archived claim_type. For terminal
    non-clean audits, the effective status is the terminal verdict itself.
    Decorations are intentionally conservative: if a downstream audit expected
    `decoration_under_*`, the full pipeline should decide whether that chain
    has really re-closed.
    """
    audit_status = archived.get("audit_status")
    if audit_status == "audited_clean":
        claim_type = archived.get("claim_type")
        if claim_type == "open_gate":
            return "open_gate"
        if claim_type == "meta":
            return "meta"
        if claim_type == "decoration":
            return "audited_decoration"
        return CLAIM_TYPE_TO_RETAINED.get(claim_type, "retained_pending_chain")
    return audit_status or "unaudited"


def is_archived_terminal_failed_dep(dep: str, rows: dict[str, dict]) -> bool:
    dep_row = rows.get(dep)
    if not dep_row:
        return False
    return (
        dep_row.get("audit_status") == "audited_failed"
        and (dep_row.get("note_path") or "").startswith("archive_unlanded/")
    )


def noncritical_invalidation_after_restore(row: dict, rows: dict[str, dict]) -> str | None:
    """Return a non-criticality invalidation reason that would still apply
    after restoration, or None if the archived audit is not stale for another
    reason.

    This intentionally mirrors the dependency/dependency-metadata checks from
    `invalidate_stale_audits.detect_invalidation`. The criticality bump itself
    is handled separately by PR #907's noop/soft-reset policy; if another
    blocker remains, restoration would only create churn and should be skipped.
    """
    restored = restore_audit_from_previous(row)
    if restored is None:
        return "missing_previous_audit"

    snap = restored.get("audit_state_snapshot")
    if snap is None:
        return None

    current_deps = sorted(restored.get("deps", []))
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
    for dep_id in current_deps:
        before = snap_dep_status.get(dep_id, "unknown")
        after = rows.get(dep_id, {}).get("effective_status") or "unaudited"
        if status_rank(after) < status_rank(before):
            return f"dep_weakened:{dep_id}:{before}->{after}"

    snap_dep_type = snap.get("dep_claim_type") or {}
    if snap_dep_type:
        for dep_id in current_deps:
            before = snap_dep_type.get(dep_id)
            after = rows.get(dep_id, {}).get("claim_type")
            if before is not None and after != before:
                return f"dep_claim_type_changed:{dep_id}:{before}->{after}"

    snap_dep_scope = snap.get("dep_claim_scope") or {}
    if snap_dep_scope:
        for dep_id in current_deps:
            before = snap_dep_scope.get(dep_id)
            after = rows.get(dep_id, {}).get("claim_scope")
            if before is not None and after != before:
                return f"dep_claim_scope_changed:{dep_id}"

    return None


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
    parsed = parse_dep_weakened(reason)
    if parsed is None:
        return None
    return parsed[0]


def parse_dep_weakened(reason: str) -> tuple[str, str, str] | None:
    """Parse `dep_id`, `before`, and `after` from
    `dep_weakened:dep_id:before->after`.
    """
    if not reason.startswith("dep_weakened:"):
        return None
    parts = reason.split(":", 2)
    if len(parts) < 3:
        return None
    dep_id = parts[1] or None
    if dep_id is None or "->" not in parts[2]:
        return None
    before, after = parts[2].split("->", 1)
    before = before.strip()
    after = after.strip()
    if not before or not after:
        return None
    return dep_id, before, after


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
        `dep_weakened:*` whose dep is in `crit_set` and whose restored
        dep tier is no weaker than the archived audit's snapshot.
    """
    crit_set: dict[str, str] = {}
    crit_archived: dict[str, dict] = {}
    dep_weakened_candidates: list[tuple[str, str, str, dict]] = []

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
            if (
                action in ("noop", "soft_reset")
                and archived_audit_is_lint_compatible(archived)
                and noncritical_invalidation_after_restore(row, rows) is None
            ):
                crit_set[cid] = archived.get("audit_status") or "?"
                crit_archived[cid] = archived
            continue

        dep = parse_dep_weakened(reason)
        if dep is not None:
            if not archived_audit_is_lint_compatible(archived):
                continue
            dep_id, before_status, _after_status = dep
            dep_weakened_candidates.append((cid, dep_id, before_status, archived))
            continue

    dep_weakened_set: list[tuple[str, str, str]] = []
    for cid, dep_id, before_status, archived in dep_weakened_candidates:
        dep_archived = crit_archived.get(dep_id)
        if dep_archived is None:
            continue
        restored_dep_status = estimate_restored_effective_status(dep_archived)
        if status_rank(restored_dep_status) >= status_rank(before_status):
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
