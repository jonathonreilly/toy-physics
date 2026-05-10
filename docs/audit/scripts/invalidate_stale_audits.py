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
  4. This claim's criticality tier increased since audit time AND the
     existing audit does not already satisfy the requirements of the new
     tier per `docs/audit/FRESH_LOOK_REQUIREMENTS.md` §4. The behavior is:

       - Bumps to `medium` / `leaf`: no-op (no new requirement).
       - Bumps to `high`: invalidate only when the existing audit's
         `independence == "weak"`. Non-weak audits stay live.
       - Bumps to `critical`: if the existing audit is `audited_clean`
         with non-weak independence but no cross-confirmation, the row
         is **soft-reset** to `audit_status = audit_in_progress` with
         `blocker = awaiting_cross_confirmation`, mirroring
         `apply_audit.py`'s first-pass flow (the clean evidence stays
         live as `cross_confirmation.first_audit`, the lane just waits
         for an independent second auditor). Audits with
         `independence == "weak"` are hard-invalidated. Audits already
         cross-confirmed are no-ops. Terminal non-clean verdicts
         (audited_conditional, audited_numerical_match, etc.) are also
         no-ops — cross-confirmation does not apply to them.
  5. The audited runner hash changed since audit time, or an
     audited_conditional `runner_artifact_issue` row that asked for a current
     runner/log now has a fresh OK cache matching the current runner source.
  6. The cited runner's classifier `dominant_class` has changed to `A` since
     audit time (when the audit recorded `runner_check_breakdown.A == 0`).
     This handles classifier upgrades — most relevantly the 2026-05-10
     alias-resolution fix which made `sp.simplify(...)` calls visible as
     class-A patterns. Only invalidates `audited_conditional` rows.

When triggered, the prior audit fields are archived into previous_audits
with an `invalidation_reason`, and audit_status is reset to unaudited.

Pipeline order: AFTER compute_load_bearing.py and AFTER
compute_effective_status.py have populated criticality and effective_status.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
RUNNER_CLASSIFICATION_PATH = DATA_DIR / "runner_classification.json"
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import runner_cache as rc  # noqa: E402


def _load_runner_classification() -> dict:
    """Load the latest runner classification (produced by classify_runner_passes.py)."""
    if not RUNNER_CLASSIFICATION_PATH.exists():
        return {}
    try:
        return json.loads(RUNNER_CLASSIFICATION_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


_RUNNER_CLASSIFICATION_CACHE: dict | None = None


def _get_runner_classification() -> dict:
    global _RUNNER_CLASSIFICATION_CACHE
    if _RUNNER_CLASSIFICATION_CACHE is None:
        _RUNNER_CLASSIFICATION_CACHE = _load_runner_classification()
    return _RUNNER_CLASSIFICATION_CACHE

# Strength rank used to compare 'before' and 'after' for a dep.
# Must stay in sync with compute_effective_status.py RANK.
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

CRITICALITY_RANK = {"leaf": 0, "medium": 1, "high": 2, "critical": 3}
CLAIM_TYPES = {
    "positive_theorem",
    "bounded_theorem",
    "no_go",
    "open_gate",
    "decoration",
    "meta",
}

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
    "claim_type",
    "claim_scope",
    "claim_type_provenance",
    "claim_type_last_reviewed",
    "notes_for_re_audit_if_any",
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
    "claim_type": None,
    "claim_scope": None,
    "claim_type_provenance": "needs_reaudit_after_invalidation",
    "claim_type_last_reviewed": None,
    "notes_for_re_audit_if_any": None,
    "effective_status": "unaudited",
}


def status_rank(status: str | None) -> int:
    if status and status.startswith("decoration_under_"):
        return 70
    return RANK.get(status or "unaudited", -1)


def detect_invalidation(row: dict, rows: dict[str, dict]) -> str | None:
    snap = row.get("audit_state_snapshot")
    if snap is not None:
        snap_runner_hash = snap.get("runner_hash")
        cur_runner_hash = rc.runner_sha256(row.get("runner_path") or "")
        if (
            snap_runner_hash is not None
            and cur_runner_hash is not None
            and snap_runner_hash != cur_runner_hash
        ):
            return f"runner_hash_changed:{snap_runner_hash[:8]}->{cur_runner_hash[:8]}"

    artifact_reason = runner_artifact_issue_resolved(row)
    if artifact_reason is not None:
        return artifact_reason

    classifier_reason = classifier_promoted_to_class_a(row, rows)
    if classifier_reason is not None:
        return classifier_reason

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
        after = rows.get(d, {}).get("effective_status") or "unaudited"
        if status_rank(after) < status_rank(before):
            return f"dep_weakened:{d}:{before}->{after}"

    # Detect audit-side dep narrowing that doesn't move effective_status
    # (e.g. claim_scope tightened, claim_type retyped within the same
    # retained tier). Older snapshots predate these maps; in that case
    # we fall back to the existing checks above.
    snap_dep_type = snap.get("dep_claim_type") or {}
    if snap_dep_type:
        for d in current_deps:
            before = snap_dep_type.get(d)
            after = rows.get(d, {}).get("claim_type")
            if before is not None and after != before:
                return f"dep_claim_type_changed:{d}:{before}->{after}"

    snap_dep_scope = snap.get("dep_claim_scope") or {}
    if snap_dep_scope:
        for d in current_deps:
            before = snap_dep_scope.get(d)
            after = rows.get(d, {}).get("claim_scope")
            if before is not None and after != before:
                return f"dep_claim_scope_changed:{d}"

    snap_crit = snap.get("criticality") or "leaf"
    cur_crit = row.get("criticality") or "leaf"
    if CRITICALITY_RANK.get(cur_crit, 0) > CRITICALITY_RANK.get(snap_crit, 0):
        action = _categorize_criticality_bump(row, cur_crit)
        if action == "soft_reset":
            return f"criticality_soft_reset:{snap_crit}->{cur_crit}"
        if action == "invalidate":
            return f"criticality_increased:{snap_crit}->{cur_crit}"
        # action == "noop": fall through

    return None


def _categorize_criticality_bump(row: dict, target_criticality: str) -> str:
    """Decide what to do with an existing audit row when the row's
    criticality bumps to `target_criticality`.

    Returns one of:
      - `"noop"`: the existing audit already satisfies the new tier, OR
        the verdict is terminal-non-clean (the criticality bump cannot
        change a non-clean verdict, and these rows are already in their
        final audit state).
      - `"soft_reset"`: only `audited_clean` rows that bump to `critical`
        with non-weak independence but no recorded cross-confirmation.
        Per `FRESH_LOOK_REQUIREMENTS.md` §4, the first-pass clean evidence
        is sound at the new tier; only the second-auditor cross-confirmation
        is missing. The row should mirror `apply_audit.py`'s first-pass
        flow: `audit_status = audit_in_progress`, `blocker =
        awaiting_cross_confirmation`, audit fields preserved as
        `cross_confirmation.first_audit`. The clean evidence stays standing
        while the audit lane requests the second pass.
      - `"invalidate"`: the existing audit fundamentally does not qualify
        at the new tier (e.g. `audited_clean` with `independence: weak`
        bumping to `high`/`critical` — the independence floor of §4 is
        not met). Full reset to `unaudited` is the only honest path.
    """
    if target_criticality in ("leaf", "medium"):
        return "noop"  # no new requirement at these tiers

    audit_status = row.get("audit_status")
    indep = row.get("independence")

    # Terminal non-clean verdicts (audited_conditional, audited_numerical_match,
    # audited_renaming, audited_decoration, audited_failed) are already in
    # their final state. Cross-confirmation does not apply to them
    # (`apply_audit.py`'s cross-confirmation flow only fires for
    # `verdict == "audited_clean"`). A criticality bump does not change
    # whether the chain closed, so leave them alone — re-auditing under a
    # stricter rule will produce the same terminal verdict.
    if audit_status != "audited_clean":
        return "noop"

    # audited_clean from here. Independence floor applies at high+.
    if indep is None or indep == "weak":
        return "invalidate"

    if target_criticality == "high":
        return "noop"  # non-weak independence is enough at high

    # target_criticality == "critical"
    cc = row.get("cross_confirmation") or {}
    cc_status = cc.get("status") if isinstance(cc, dict) else None
    if cc_status in {"confirmed", "third_confirmed_first", "third_confirmed_second"}:
        return "noop"  # already cross-confirmed

    # audited_clean + non-weak indep + bumped to critical without
    # cross-confirmation → mirror the first-pass flow rather than
    # blowing away the clean evidence.
    return "soft_reset"


_CLASSIFIER_KEYWORDS = (
    "class-a",
    "class a",
    "algebraic",
    "register a current runner",
    "register a runner",
)


def classifier_promoted_to_class_a(row: dict, rows: dict[str, dict]) -> str | None:
    """Detect that the cited runner has been re-classified to class-A since audit.

    Fires when a row whose audit explicitly flagged "no class-A backing"
    on the cited runner now has the runner reaching `dominant_class: A`
    per the latest `runner_classification.json`. The dominant case this
    handles is a classifier upgrade (e.g., the 2026-05-10 alias-resolution
    fix that lets the classifier see `sp.simplify(...)` as class-A when
    imported via the standard `import sympy as sp` idiom).

    This trigger does NOT promote the row to a clean verdict — it only
    invalidates the stale conditional verdict so the audit lane re-evaluates
    with the now-visible class-A evidence.

    Conservatism guards (intentionally strict — most `audited_conditional`
    rows have `A == 0` incidentally because the auditor's primary concern
    was deps or scope, not missing class-A):

      1. Only fires for `audited_conditional` (other tiers are out of scope).
      2. Requires the prior audit to have recorded
         `runner_check_breakdown.A == 0` (auditor saw no class-A at audit).
      3. Requires the current classifier to show `dominant_class == "A"`
         AND `counts.A >= 5` (substantial class-A presence, not noise).
      4. Requires the runner to exist on disk.
      5. Requires every direct dependency to be retained-grade
         (`retained` / `retained_no_go` / `retained_bounded`). If deps are
         not clean, re-audit will produce the same conditional verdict
         for `dependency_not_retained`, wasting auditor time.
      6. Requires the prior audit's `notes_for_re_audit_if_any` or
         `chain_closure_explanation` to mention runner-verification or
         class-A keywords. This is the strict filter — the trigger only
         fires when the auditor's stated reason for the conditional
         verdict was specifically about runner / class-A insufficiency,
         not about deps / scope / missing bridges.
    """
    if row.get("audit_status") != "audited_conditional":
        return None
    runner_path = row.get("runner_path")
    if not runner_path:
        return None

    breakdown = row.get("runner_check_breakdown") or {}
    if breakdown.get("A", 0) != 0:
        return None  # auditor already saw class-A; no promotion to invalidate on

    classification = _get_runner_classification()
    per_runner = classification.get("per_runner", {})
    info = per_runner.get(runner_path)
    if not info or not info.get("exists"):
        return None
    if info.get("dominant_class") != "A":
        return None
    if info.get("counts", {}).get("A", 0) < 5:
        return None  # too few class-A patterns; likely classifier noise

    # Dep-clean guard: re-audit only helps if deps are clean.
    for dep_id in row.get("deps", []):
        dep_status = rows.get(dep_id, {}).get("effective_status") or "unaudited"
        if dep_status not in {"retained", "retained_no_go", "retained_bounded"}:
            return None

    # Keyword guard: the prior conditional verdict must have been about
    # runner / class-A insufficiency, not about deps / scope / missing bridges.
    notes = (row.get("notes_for_re_audit_if_any") or "").lower()
    explanation = (row.get("chain_closure_explanation") or "").lower()
    haystack = notes + " " + explanation
    if not any(kw in haystack for kw in _CLASSIFIER_KEYWORDS):
        return None

    return f"classifier_promoted_to_class_A:{runner_path}"


def runner_artifact_issue_resolved(row: dict) -> str | None:
    """Detect a resolved "register current runner/log" audit blocker.

    This does not decide whether the claim is scientifically clean. It only
    reopens a stale conditional audit when the exact artifact it requested is
    now present as a fresh OK cache.
    """
    if row.get("audit_status") != "audited_conditional":
        return None
    notes = (row.get("notes_for_re_audit_if_any") or "").lower()
    if not notes.startswith("runner_artifact_issue:"):
        return None
    if "register a current runner/log" not in notes and "register a current runner" not in notes:
        return None
    runner_path = row.get("runner_path")
    if not runner_path:
        return None
    cache_path, header, _body = rc.load_cache(runner_path)
    if not cache_path.exists() or not header:
        return None
    if header.get("status") != "ok" or header.get("exit_code") != "0":
        return None
    current_hash = rc.runner_sha256(runner_path)
    if current_hash is None or header.get("runner_sha256") != current_hash:
        return None
    return f"runner_artifact_issue_resolved:{runner_path}"


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
    source_hint = row.get("claim_type_author_hint")
    if source_hint in CLAIM_TYPES:
        new_row["claim_type"] = source_hint
        new_row["claim_type_provenance"] = "author_hint_after_invalidation"
    elif row.get("claim_type") in CLAIM_TYPES:
        new_row["claim_type"] = row.get("claim_type")
        new_row["claim_type_provenance"] = "needs_reaudit_after_invalidation"
    return new_row


def soft_reset_to_cross_confirmation_pending(row: dict, reason: str) -> dict:
    """Transition `audited_clean` -> `audit_in_progress` + `awaiting_cross_confirmation`
    when a criticality bump newly requires cross-confirmation but the
    existing audit's evidence is otherwise sound (non-weak independence,
    clean verdict).

    Mirrors `apply_audit.py`'s first-pass flow at
    `audit_status = "audit_in_progress"` (lines around 770-784): the live
    audit fields stay in place as `cross_confirmation.first_audit`, and
    the row waits for an independent second auditor. The clean evidence is
    NOT archived to `previous_audits` — it is still the live first audit;
    only the lane's expectation has changed (the new tier requires a
    second pass).
    """
    new_row = dict(row)
    # Build the first_audit summary mirroring
    # apply_audit.audit_summary_from_row exactly.
    new_row["cross_confirmation"] = {
        "first_audit": {
            "auditor": row.get("auditor"),
            "auditor_family": row.get("auditor_family"),
            "auditor_model": row.get("auditor_model"),
            "auditor_reasoning_effort": row.get("auditor_reasoning_effort"),
            "independence": row.get("independence"),
            "audit_date": row.get("audit_date"),
            "claim_type": row.get("claim_type"),
            "claim_scope": row.get("claim_scope"),
            "load_bearing_step_class": row.get("load_bearing_step_class"),
            "verdict": row.get("audit_status"),
        },
        "second_audit": None,
        "status": "awaiting_second",
    }
    new_row["audit_status"] = "audit_in_progress"
    new_row["blocker"] = "awaiting_cross_confirmation"
    new_row["claim_type_provenance"] = "audited_pending_cross_confirmation_after_criticality_bump"
    new_row["claim_type_last_reviewed"] = datetime.now(timezone.utc).isoformat()
    new_row["notes_for_re_audit_if_any"] = (
        f"awaiting_cross_confirmation_after_{reason}: first-pass audit "
        f"(auditor={row.get('auditor')}, family={row.get('auditor_family')}, "
        f"independence={row.get('independence')}) was clean at the prior "
        f"criticality tier; new tier requires an independent second auditor."
    )
    return new_row


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing; run seed_audit_ledger.py first")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    invalidated: list[tuple[str, str]] = []
    soft_reset: list[tuple[str, str]] = []
    for cid, row in rows.items():
        if row.get("audit_status", "unaudited") in {"unaudited", "audit_in_progress"}:
            continue
        reason = detect_invalidation(row, rows)
        if reason is None:
            continue
        if reason.startswith("criticality_soft_reset:"):
            rows[cid] = soft_reset_to_cross_confirmation_pending(row, reason)
            soft_reset.append((cid, reason))
        else:
            rows[cid] = archive_and_reset(row, reason)
            invalidated.append((cid, reason))

    ledger["rows"] = rows
    # `last_invalidations` includes both hard invalidations and soft resets so
    # `run_pipeline.sh`'s loop re-runs `compute_effective_status.py` until
    # the ledger reaches a fixed point.
    ledger["last_invalidations"] = [
        {"claim_id": c, "reason": r}
        for c, r in (invalidated + soft_reset)
    ]

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    print(f"invalidate_stale_audits: scanned {len(rows)} rows")
    print(f"  invalidated (hard reset): {len(invalidated)}")
    for cid, reason in invalidated[:10]:
        print(f"    {cid}: {reason}")
    if soft_reset:
        print(f"  soft reset (audit_in_progress + awaiting_cross_confirmation): {len(soft_reset)}")
        for cid, reason in soft_reset[:10]:
            print(f"    {cid}: {reason}")
    if len(invalidated) > 10:
        print(f"    ... and {len(invalidated) - 10} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
