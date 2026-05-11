#!/usr/bin/env python3
"""Apply an audit result to a row in the ledger.

Usage:
  echo '<json audit blob>' | python3 apply_audit.py
  python3 apply_audit.py --file path/to/audit.json
  python3 apply_audit.py --batch path/to/dir_of_audit_jsons/

The audit blob must include claim_id, auditor, auditor_family, and the
fields produced by AUDIT_AGENT_PROMPT_TEMPLATE.md. Enforces the hard
rules:
  - independence='weak' may not land audited_clean
  - independence='fresh_context' may land audited_clean when the audit was
    performed in a distinct clean-room session with the restricted audit inputs
  - audited_clean records the audit verdict plus auditor-owned claim_type;
    compute_effective_status.py promotes from claim_type
  - auditor identity must differ from author identity for audited_clean
  - the row's note_hash must match disk (otherwise the audit is stale)
  - fresh-context second passes over existing high/critical terminal verdicts
    record a cross-confirmation comparison before any retraction can cascade
  - non-clean re-audits of confirmed legacy clean rows record a real
    disagreement instead of treating migration-only confirmation as authority
  - third-auditor passes over cross-confirmation disagreements record the
    tiebreaker and hard-stop on genuine three-way disagreement
  - judicial third-auditor reviews over disagreements may ratify the first or
    second prior audit after reading both prior rationales, or mark the
    disagreement as irresolvable for human review
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

REQUIRED_FIELDS = {
    "claim_id",
    "verdict",
    "claim_type",
    "claim_scope",
    "auditor",
    "auditor_family",
    "auditor_model",
    "auditor_reasoning_effort",
    "independence",
}
JUDICIAL_REQUIRED_FIELDS = {
    "claim_id",
    "third_auditor",
    "auditor_family",
    "auditor_model",
    "auditor_reasoning_effort",
    "independence",
    "sided_with",
    "ratified_verdict",
    "ratified_load_bearing_step_class",
    "judgment_rationale",
    "first_auditor_error",
    "second_auditor_error",
}

# Reasoning-effort policy for incoming audits. The audit lane runs at xhigh
# only; weaker effort levels are not accepted as ratifying evidence.
REQUIRED_REASONING_EFFORT = "xhigh"

ALLOWED_VERDICTS = {
    "audited_clean",
    "audited_renaming",
    "audited_conditional",
    "audited_decoration",
    "audited_failed",
    "audited_numerical_match",
}

ALLOWED_CLAIM_TYPES = {
    "positive_theorem",
    "bounded_theorem",
    "no_go",
    "open_gate",
    "decoration",
    "meta",
}

ALLOWED_INDEPENDENCE = {"weak", "fresh_context", "cross_family", "strong", "external", "judicial_review"}
CLEAN_INDEPENDENCE = ALLOWED_INDEPENDENCE - {"weak"}

# Minimum auditor-family rank for incoming Codex audits. Existing ledger rows
# are not invalidated by this script, but every new audit blob applied after
# this policy must meet the floor. This catches manual `apply_audit.py`
# invocations that bypass the runner's model floor, e.g. a hand-written audit
# blob with auditor_family=codex-gpt-5. Set to (5, 5) so codex-gpt-5.5 and
# newer are accepted.
MIN_NEW_AUDIT_FAMILY_RANK = (5, 5)
_FAMILY_RANK_RE = re.compile(r"codex-gpt-(\d+(?:\.\d+)*)$")


def _family_rank(family: str | None) -> tuple[int, ...] | None:
    if not family:
        return None
    m = _FAMILY_RANK_RE.match(family)
    if not m:
        return None
    return tuple(int(p) for p in m.group(1).split("."))


def _family_meets_floor(family: str | None) -> bool:
    """True if family parses to a rank >= MIN_NEW_AUDIT_FAMILY_RANK.

    Non-codex families (e.g. claude-* manual reviews, legacy-confirmed-clean)
    pass the floor — only codex-gpt-* families are rank-checked. This
    keeps the door open for human / Claude judicial reviews which are
    not bound by the codex model schedule.
    """
    if not family or not family.startswith("codex-gpt-"):
        return True
    rank = _family_rank(family)
    if not rank:
        # Unparseable codex-gpt-* — refuse to bless something we can't measure.
        return False
    floor = MIN_NEW_AUDIT_FAMILY_RANK
    width = max(len(rank), len(floor))
    rank_padded = rank + (0,) * (width - len(rank))
    floor_padded = floor + (0,) * (width - len(floor))
    return rank_padded >= floor_padded

ALLOWED_JUDICIAL_SIDES = {"first", "second", "neither"}
JUDICIAL_REVIEWABLE_STATUSES = {"disagreement", "third_confirmed_first", "third_confirmed_second"}
TERMINAL_CROSS_CONFIRM_VERDICTS = {
    "audited_renaming",
    "audited_numerical_match",
    "audited_failed",
}


def clean_independence_error(independence: str, criticality: str | None = None) -> str | None:
    if independence in CLEAN_INDEPENDENCE:
        return None
    if criticality in {"critical", "high"}:
        return f"criticality={criticality} requires independence >= fresh_context for audited_clean"
    return "audited_clean requires independence != 'weak'"


def cross_confirmation_error(first: dict, audit: dict) -> str | None:
    """Return a rejection reason when the second critical audit is not independent."""
    first_auditor = first.get("auditor")
    auditor = audit.get("auditor")
    if first_auditor and first_auditor == auditor:
        return "second auditor must have a distinct auditor identity/session from the first"

    same_family = first.get("auditor_family") == audit.get("auditor_family")
    if same_family and audit.get("independence") != "fresh_context":
        return (
            "same-family second audit requires independence='fresh_context' "
            "to document a restricted-input clean-room session"
        )
    return None


def third_confirmation_error(cross_confirmation: dict, audit: dict) -> str | None:
    """Return a rejection reason when the third audit is not independent."""
    prior_auditors = {
        (cross_confirmation.get("first_audit") or {}).get("auditor"),
        (cross_confirmation.get("second_audit") or {}).get("auditor"),
    }
    prior_auditors.discard(None)
    auditor = audit.get("auditor")
    if auditor in prior_auditors:
        return "third auditor must have a distinct auditor identity/session from both prior auditors"

    prior_families = {
        (cross_confirmation.get("first_audit") or {}).get("auditor_family"),
        (cross_confirmation.get("second_audit") or {}).get("auditor_family"),
    }
    prior_families.discard(None)
    if audit.get("auditor_family") in prior_families and audit.get("independence") != "fresh_context":
        return (
            "same-family third audit requires independence='fresh_context' "
            "to document a restricted-input clean-room session"
        )
    return None


def audit_summary_from_row(row: dict) -> dict:
    """Build the restricted summary used for later comparison."""
    return {
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
    }


def audit_summary_from_blob(audit: dict) -> dict:
    return {
        "auditor": audit.get("auditor"),
        "auditor_family": audit.get("auditor_family"),
        "auditor_model": audit.get("auditor_model"),
        "auditor_reasoning_effort": audit.get("auditor_reasoning_effort"),
        "independence": audit.get("independence"),
        "audit_date": audit.get("audit_date") or datetime.now(timezone.utc).isoformat(),
        "claim_type": audit.get("claim_type"),
        "claim_scope": audit.get("claim_scope"),
        "load_bearing_step_class": audit.get("load_bearing_step_class"),
        "verdict": audit.get("verdict"),
    }


def judicial_summary_from_blob(judgment: dict) -> dict:
    summary = {
        "auditor": judgment.get("third_auditor"),
        "auditor_family": judgment.get("auditor_family"),
        "auditor_model": judgment.get("auditor_model"),
        "auditor_reasoning_effort": judgment.get("auditor_reasoning_effort"),
        "independence": judgment.get("independence"),
        "audit_date": judgment.get("audit_date") or datetime.now(timezone.utc).isoformat(),
        "claim_type": judgment.get("ratified_claim_type"),
        "claim_scope": judgment.get("ratified_claim_scope"),
        "load_bearing_step_class": judgment.get("ratified_load_bearing_step_class"),
        "verdict": judgment.get("ratified_verdict"),
        "sided_with": judgment.get("sided_with"),
        "judgment_rationale": judgment.get("judgment_rationale"),
        "first_auditor_error": judgment.get("first_auditor_error"),
        "second_auditor_error": judgment.get("second_auditor_error"),
    }
    if "runner_check_breakdown" in judgment:
        summary["runner_check_breakdown"] = judgment["runner_check_breakdown"]
    return summary


def snapshot_audit_state(row: dict, rows: dict[str, dict]) -> dict:
    deps = sorted(row.get("deps", []))
    runner_hash_value: str | None = None
    runner_path = row.get("runner_path")
    if runner_path:
        rp = REPO_ROOT / runner_path
        if rp.exists():
            import hashlib as _hashlib
            try:
                runner_hash_value = _hashlib.sha256(rp.read_bytes()).hexdigest()
            except OSError:
                runner_hash_value = None
    return {
        "deps": deps,
        "dep_effective_status": {
            d: rows.get(d, {}).get("effective_status") or "unaudited"
            for d in deps
        },
        # Per-dep claim_type and claim_scope, so invalidate_stale_audits
        # can detect upstream audit-side narrowing or retyping that
        # happens without a note-text edit (silent w.r.t. note-hash
        # drift and dep_effective_status weakening when both before and
        # after live in the retained tier).
        "dep_claim_type": {
            d: rows.get(d, {}).get("claim_type")
            for d in deps
        },
        "dep_claim_scope": {
            d: rows.get(d, {}).get("claim_scope")
            for d in deps
        },
        "criticality": row.get("criticality"),
        "load_bearing_score": row.get("load_bearing_score"),
        "transitive_descendants": row.get("transitive_descendants"),
        "runner_hash": runner_hash_value,
    }


def legacy_confirmed_clean_claim_type_reaudit(row: dict, verdict: str, xc_status: str | None) -> bool:
    """Return true when a legacy clean row only needs scoped claim typing.

    PR291 made claim_type part of the audit verdict. Older critical clean
    rows can already have confirmed cross-confirmation whose summaries predate
    claim_type, so comparing a new scoped re-audit against those missing fields
    would create a false disagreement. In that migration-only case, keep the
    existing clean cross-confirmation and let the new restricted-input audit
    own claim_type and claim_scope.

    Some rows were later left at audited_conditional while still carrying an
    already-confirmed legacy clean cross-confirmation. If the new restricted
    audit is clean and the prior confirmed summaries are clean but claim-type
    blind, treat that the same way; the current source prose/status is not the
    authority under the PR291 regime.
    """
    if row.get("claim_type_provenance") != "backfilled_pending_reaudit":
        return False
    if row.get("audit_status") not in {"audited_clean", "audited_conditional"}:
        return False
    if verdict != "audited_clean":
        return False
    if xc_status not in {"confirmed", "third_confirmed_first", "third_confirmed_second"}:
        return False
    xc = row.get("cross_confirmation") or {}
    first = xc.get("first_audit") or {}
    second = xc.get("second_audit") or {}
    third = xc.get("third_audit") or {}
    if xc_status == "third_confirmed_first":
        return (
            first.get("verdict") == "audited_clean"
            and third.get("verdict") == "audited_clean"
            and first.get("claim_type") is None
            and third.get("claim_type") is None
        )
    if xc_status == "third_confirmed_second":
        return (
            second.get("verdict") == "audited_clean"
            and third.get("verdict") == "audited_clean"
            and second.get("claim_type") is None
            and third.get("claim_type") is None
        )
    return (
        first.get("verdict") == "audited_clean"
        and second.get("verdict") == "audited_clean"
        and first.get("claim_type") is None
        and second.get("claim_type") is None
    )


def legacy_confirmed_clean_verdict_reaudit(row: dict, verdict: str, xc_status: str | None) -> bool:
    """Return true when a scoped legacy clean re-audit changes the verdict."""
    if row.get("claim_type_provenance") != "backfilled_pending_reaudit":
        return False
    if row.get("audit_status") not in {"audited_clean", "audited_conditional"}:
        return False
    if verdict == "audited_clean":
        return False
    if xc_status not in {"confirmed", "third_confirmed_first", "third_confirmed_second"}:
        return False
    xc = row.get("cross_confirmation") or {}
    first = xc.get("first_audit") or {}
    second = xc.get("second_audit") or {}
    third = xc.get("third_audit") or {}
    if xc_status == "third_confirmed_first":
        return first.get("verdict") == "audited_clean" and third.get("verdict") == "audited_clean"
    if xc_status == "third_confirmed_second":
        return second.get("verdict") == "audited_clean" and third.get("verdict") == "audited_clean"
    return first.get("verdict") == "audited_clean" and second.get("verdict") == "audited_clean"


def legacy_clean_consensus_summary(row: dict, audit: dict, xc_status: str | None) -> dict:
    """Collapse old clean confirmations into the side opposed to a new verdict."""
    xc = row.get("cross_confirmation") or {}
    if xc_status == "third_confirmed_first":
        winning = [xc.get("first_audit") or {}, xc.get("third_audit") or {}]
    elif xc_status == "third_confirmed_second":
        winning = [xc.get("second_audit") or {}, xc.get("third_audit") or {}]
    else:
        winning = [xc.get("first_audit") or {}, xc.get("second_audit") or {}]

    dates = [w.get("audit_date") for w in winning if w.get("audit_date")]
    auditors = [w.get("auditor") for w in winning if w.get("auditor")]
    families = sorted({w.get("auditor_family") for w in winning if w.get("auditor_family")})
    return {
        "auditor": "legacy-confirmed-clean-cross-confirmation",
        "auditor_family": "legacy-confirmed-clean",
        "independence": "fresh_context",
        "audit_date": max(dates) if dates else row.get("audit_date"),
        "claim_type": audit.get("claim_type"),
        "claim_scope": audit.get("claim_scope") or row.get("claim_scope"),
        "load_bearing_step_class": row.get("load_bearing_step_class"),
        "verdict": "audited_clean",
        "legacy_auditors": auditors,
        "legacy_auditor_families": families,
    }


def note_hash_drift_error(row: dict) -> str | None:
    on_disk_path = REPO_ROOT / row.get("note_path", "")
    if not on_disk_path.exists():
        return None
    import hashlib
    on_disk_hash = hashlib.sha256(
        on_disk_path.read_text(encoding="utf-8", errors="replace").encode("utf-8")
    ).hexdigest()
    if on_disk_hash != row.get("note_hash"):
        return "note_hash drift; rerun seed_audit_ledger.py before applying audit"
    return None


def validate_auditor_provenance(audit: dict) -> str | None:
    """Validate model and reasoning-effort provenance on an incoming audit."""
    auditor_model = audit.get("auditor_model")
    if not isinstance(auditor_model, str) or not auditor_model.strip():
        return "auditor_model must be a non-empty string (e.g. 'gpt-5.5')"
    auditor_reasoning = audit.get("auditor_reasoning_effort")
    if not isinstance(auditor_reasoning, str) or not auditor_reasoning.strip():
        return "auditor_reasoning_effort must be a non-empty string (e.g. 'xhigh')"
    if auditor_reasoning != REQUIRED_REASONING_EFFORT:
        return (
            f"auditor_reasoning_effort={auditor_reasoning!r} must equal "
            f"{REQUIRED_REASONING_EFFORT!r}: the audit lane only accepts "
            f"verdicts produced at {REQUIRED_REASONING_EFFORT} reasoning "
            "effort. Re-run the audit with the correct setting."
        )
    declared_family = audit.get("auditor_family")
    if isinstance(declared_family, str) and declared_family.startswith("codex-gpt-"):
        expected = f"codex-{auditor_model}"
        if declared_family != expected:
            return (
                f"auditor_family={declared_family!r} does not match "
                f"auditor_model={auditor_model!r}: expected family "
                f"{expected!r}. Either fix the family label or fix the "
                "model field; they must agree."
            )
    return None


def apply_judicial_review(ledger: dict, judgment: dict) -> tuple[bool, str]:
    missing = JUDICIAL_REQUIRED_FIELDS - set(judgment)
    if missing:
        return False, f"missing required judicial fields: {sorted(missing)}"

    cid = judgment["claim_id"]
    rows = ledger.get("rows", {})
    if cid not in rows:
        return False, f"unknown claim_id: {cid!r}"
    row = rows[cid]

    if judgment.get("independence") != "judicial_review":
        return False, "judicial third-auditor review requires independence='judicial_review'"
    provenance_error = validate_auditor_provenance(judgment)
    if provenance_error:
        return False, provenance_error
    side = judgment.get("sided_with")
    if side not in ALLOWED_JUDICIAL_SIDES:
        return False, f"sided_with {side!r} not in {sorted(ALLOWED_JUDICIAL_SIDES)}"
    ratified_verdict = judgment.get("ratified_verdict")
    if ratified_verdict not in ALLOWED_VERDICTS:
        return False, f"ratified_verdict {ratified_verdict!r} not in {sorted(ALLOWED_VERDICTS)}"
    ratified_claim_type = judgment.get("ratified_claim_type")
    if ratified_claim_type is not None and ratified_claim_type not in ALLOWED_CLAIM_TYPES:
        return False, f"ratified_claim_type {ratified_claim_type!r} not in {sorted(ALLOWED_CLAIM_TYPES)}"

    err = note_hash_drift_error(row)
    if err:
        return False, err

    cross_confirmation = row.get("cross_confirmation")
    if (
        not isinstance(cross_confirmation, dict)
        or cross_confirmation.get("status") not in JUDICIAL_REVIEWABLE_STATUSES
    ):
        return False, (
            "judicial review requires cross_confirmation.status in "
            f"{sorted(JUDICIAL_REVIEWABLE_STATUSES)}"
        )
    first = cross_confirmation.get("first_audit") or {}
    second = cross_confirmation.get("second_audit") or {}
    if not first or not second:
        return False, "judicial review requires first_audit and second_audit summaries"

    prior_auditors = {first.get("auditor"), second.get("auditor")}
    if judgment.get("third_auditor") in prior_auditors:
        return False, "judicial third auditor must differ from both prior auditors"

    third = judicial_summary_from_blob(judgment)
    row["cross_confirmation"]["third_audit"] = third
    row["cross_confirmation"]["mode"] = "judicial_third_pass"

    if side == "neither":
        row["cross_confirmation"]["status"] = "disagreement_irresolvable"
        row["blocker"] = "judicial_review_irresolvable"
        rows[cid] = row
        ledger["rows"] = rows
        return False, "judicial review found neither prior reading sufficient; human review required"

    chosen = first if side == "first" else second
    chosen_label = "first" if side == "first" else "second"
    if ratified_verdict != chosen.get("verdict"):
        return False, (
            f"ratified_verdict {ratified_verdict!r} does not match "
            f"{chosen_label}_audit verdict {chosen.get('verdict')!r}"
        )
    chosen_claim_type = chosen.get("claim_type")
    if (
        ratified_claim_type is not None
        and chosen_claim_type is not None
        and ratified_claim_type != chosen_claim_type
    ):
        return False, (
            f"ratified_claim_type {ratified_claim_type!r} does not match "
            f"{chosen_label}_audit claim_type {chosen_claim_type!r}"
        )
    ratified_class = judgment.get("ratified_load_bearing_step_class")

    row["cross_confirmation"]["status"] = (
        "third_confirmed_first" if side == "first" else "third_confirmed_second"
    )
    row["audit_status"] = ratified_verdict
    row["auditor"] = judgment["third_auditor"]
    row["auditor_family"] = judgment["auditor_family"]
    row["auditor_model"] = judgment["auditor_model"]
    row["auditor_reasoning_effort"] = judgment["auditor_reasoning_effort"]
    row["independence"] = judgment["independence"]
    row["audit_date"] = third["audit_date"]
    row["claim_type"] = ratified_claim_type or chosen_claim_type or row.get("claim_type")
    row["claim_scope"] = judgment.get("ratified_claim_scope") or chosen.get("claim_scope") or row.get("claim_scope")
    row["claim_type_provenance"] = "judicial_review"
    row["claim_type_last_reviewed"] = row["audit_date"]
    row["load_bearing_step"] = judgment.get("ratified_load_bearing_step") or row.get("load_bearing_step")
    row["load_bearing_step_class"] = ratified_class
    row["chain_closes"] = ratified_verdict == "audited_clean"
    row["chain_closure_explanation"] = judgment.get("judgment_rationale")
    row["verdict_rationale"] = judgment.get("judgment_rationale")
    if "notes_for_re_audit_if_any" in judgment:
        row["notes_for_re_audit_if_any"] = judgment.get("notes_for_re_audit_if_any")
    if "runner_check_breakdown" in judgment:
        row["runner_check_breakdown"] = judgment["runner_check_breakdown"]
    if "open_dependency_paths" in judgment:
        row["open_dependency_paths"] = judgment.get("open_dependency_paths") or []
    if ratified_verdict == "audited_clean":
        row["open_dependency_paths"] = []
        row["decoration_parent_claim_id"] = None
    row["auditor_confidence"] = judgment.get("auditor_confidence", "judicial")
    row["blocker"] = None
    row["audit_state_snapshot"] = snapshot_audit_state(row, rows)
    rows[cid] = row
    ledger["rows"] = rows
    return True, f"judicial third auditor confirmed {side} verdict"


def apply_one(ledger: dict, audit: dict) -> tuple[bool, str]:
    if "sided_with" in audit or "third_auditor" in audit:
        return apply_judicial_review(ledger, audit)

    missing = REQUIRED_FIELDS - set(audit)
    if missing:
        return False, f"missing required fields: {sorted(missing)}"

    cid = audit["claim_id"]
    rows = ledger.get("rows", {})
    if cid not in rows:
        return False, f"unknown claim_id: {cid!r}"

    row = rows[cid]

    verdict = audit["verdict"]
    if verdict not in ALLOWED_VERDICTS:
        return False, f"verdict {verdict!r} not in {sorted(ALLOWED_VERDICTS)}"

    claim_type = audit.get("claim_type")
    if claim_type not in ALLOWED_CLAIM_TYPES:
        return False, f"claim_type {claim_type!r} not in {sorted(ALLOWED_CLAIM_TYPES)}"
    claim_scope = audit.get("claim_scope")
    if not isinstance(claim_scope, str) or not claim_scope.strip():
        return False, "claim_scope must be a non-empty string"

    if verdict == "audited_clean" and claim_type in {"decoration", "meta"}:
        return False, f"audited_clean cannot ratify claim_type={claim_type!r}"
    if verdict == "audited_decoration":
        if claim_type != "decoration":
            return False, "audited_decoration requires claim_type='decoration'"
        if not audit.get("decoration_parent_claim_id"):
            return False, "audited_decoration requires decoration_parent_claim_id"

    independence = audit["independence"]
    if independence not in ALLOWED_INDEPENDENCE:
        return False, f"independence {independence!r} not in {sorted(ALLOWED_INDEPENDENCE)}"

    provenance_error = validate_auditor_provenance(audit)
    if provenance_error:
        return False, provenance_error

    # Model-floor check: incoming Codex audits must come from a codex-gpt-*
    # family at or above MIN_NEW_AUDIT_FAMILY_RANK, or a non-codex family
    # (claude-*, legacy-confirmed-clean, judicial reviews, etc.). Existing
    # sub-floor rows are left for the re-audit queue; this rejects only newly
    # applied audit blobs.
    if not _family_meets_floor(audit["auditor_family"]):
        floor_str = ".".join(str(x) for x in MIN_NEW_AUDIT_FAMILY_RANK)
        return False, (
            f"auditor_family {audit['auditor_family']!r} is below the "
            f"incoming-audit codex-gpt-{floor_str}+ floor. Codex audit blobs "
            f"must be produced by codex-gpt-{floor_str} or newer; non-codex "
            f"families remain allowed for human / judicial reviews."
        )

    criticality = row.get("criticality") or "leaf"
    if verdict == "audited_clean":
        err = clean_independence_error(independence, criticality)
        if err:
            return False, err

    # Hash drift check.
    err = note_hash_drift_error(row)
    if err:
        return False, err

    terminal_second_pass_msg: str | None = None
    terminal_second_pass_error: str | None = None
    terminal_second_pass_blocker: str | None = None
    third_pass_msg: str | None = None
    third_pass_error: str | None = None
    third_pass_blocker: str | None = None
    prior_cross_confirmation = row.get("cross_confirmation")
    prior_cross_confirmation_status = (
        prior_cross_confirmation.get("status")
        if isinstance(prior_cross_confirmation, dict)
        else prior_cross_confirmation
    )
    legacy_claim_type_reaudit = legacy_confirmed_clean_claim_type_reaudit(
        row, verdict, prior_cross_confirmation_status
    )
    legacy_verdict_reaudit = legacy_confirmed_clean_verdict_reaudit(
        row, verdict, prior_cross_confirmation_status
    )
    if legacy_verdict_reaudit:
        if criticality in {"critical", "high"} and independence == "weak":
            return False, "legacy clean verdict re-audit requires independence != 'weak'"

        first = legacy_clean_consensus_summary(row, audit, prior_cross_confirmation_status)
        second = audit_summary_from_blob(audit)
        row["cross_confirmation"] = {
            "first_audit": first,
            "second_audit": second,
            "status": "disagreement",
            "mode": "legacy_confirmed_clean_verdict_reaudit",
        }
        row["audit_status"] = "audit_in_progress"
        row["blocker"] = "cross_confirmation_disagreement"
        row["claim_type"] = claim_type
        row["claim_scope"] = claim_scope.strip()
        row["claim_type_provenance"] = "audited_pending_cross_confirmation"
        row["claim_type_last_reviewed"] = audit.get("audit_date") or datetime.now(timezone.utc).isoformat()
        rows[cid] = row
        ledger["rows"] = rows
        return True, (
            "legacy clean re-audit disagreement recorded "
            f"('audited_clean'/{first.get('claim_type')!r}/"
            f"{first.get('load_bearing_step_class')!r} vs "
            f"{second.get('verdict')!r}/{second.get('claim_type')!r}/"
            f"{second.get('load_bearing_step_class')!r}); "
            "promote to third-auditor review"
        )

    first_terminal_verdict = row.get("audit_status")
    terminal_second_pass = (
        first_terminal_verdict in TERMINAL_CROSS_CONFIRM_VERDICTS
        and criticality in {"critical", "high"}
        and prior_cross_confirmation_status in {None, "none"}
    )
    if terminal_second_pass:
        first = audit_summary_from_row(row)
        err = cross_confirmation_error(first, audit)
        if err:
            return False, err
        if independence == "weak":
            return False, "terminal cross-confirmation requires independence != 'weak'"

        second = audit_summary_from_blob(audit)
        matches = (
            first.get("verdict") == second.get("verdict")
            and first.get("claim_type") == second.get("claim_type")
            and first.get("load_bearing_step_class") == second.get("load_bearing_step_class")
        )
        row["cross_confirmation"] = {
            "first_audit": first,
            "second_audit": second,
            "status": "confirmed" if matches else "disagreement",
            "mode": "terminal_second_pass",
        }
        if matches:
            terminal_second_pass_msg = "terminal verdict cross-confirmed"
        else:
            terminal_second_pass_error = (
                "first and second audits disagree "
                f"({first.get('verdict')!r}/{first.get('claim_type')!r}/"
                f"{first.get('load_bearing_step_class')!r} vs "
                f"{second.get('verdict')!r}/{second.get('claim_type')!r}/"
                f"{second.get('load_bearing_step_class')!r}); "
                "promote to third-auditor review or human escalation"
            )
            terminal_second_pass_blocker = "cross_confirmation_disagreement"

    third_pass = prior_cross_confirmation_status == "disagreement"
    if third_pass:
        if independence == "weak":
            return False, "third-auditor confirmation requires independence != 'weak'"
        err = third_confirmation_error(prior_cross_confirmation or {}, audit)
        if err:
            return False, err

        first = (prior_cross_confirmation or {}).get("first_audit") or {}
        second = (prior_cross_confirmation or {}).get("second_audit") or {}
        third = audit_summary_from_blob(audit)
        first_verdict = first.get("verdict")
        second_verdict = second.get("verdict")
        third_verdict = third.get("verdict")
        third_matches_first = (
            third_verdict == first_verdict
            and third.get("claim_type") == first.get("claim_type")
            and third.get("load_bearing_step_class") == first.get("load_bearing_step_class")
        )
        third_matches_second = (
            third_verdict == second_verdict
            and third.get("claim_type") == second.get("claim_type")
            and third.get("load_bearing_step_class") == second.get("load_bearing_step_class")
        )
        if third_matches_first:
            row["cross_confirmation"]["third_audit"] = third
            row["cross_confirmation"]["status"] = "third_confirmed_first"
            row["cross_confirmation"]["mode"] = "terminal_third_pass"
            third_pass_msg = "third auditor confirmed first verdict"
        elif third_matches_second:
            row["cross_confirmation"]["third_audit"] = third
            row["cross_confirmation"]["status"] = "third_confirmed_second"
            row["cross_confirmation"]["mode"] = "terminal_third_pass"
            third_pass_msg = "third auditor confirmed second verdict"
        else:
            row["cross_confirmation"]["third_audit"] = third
            row["cross_confirmation"]["status"] = "three_way_disagreement"
            row["cross_confirmation"]["mode"] = "terminal_third_pass"
            third_pass_error = (
                "third auditor introduced a third verdict or claim_type "
                f"({first_verdict!r}/{first.get('claim_type')!r} vs "
                f"{second_verdict!r}/{second.get('claim_type')!r} vs "
                f"{third_verdict!r}/{third.get('claim_type')!r}); "
                "escalate to human review"
            )
            third_pass_blocker = "third_auditor_disagreement"

    critical_second_pass = (
        criticality == "critical"
        and prior_cross_confirmation_status == "awaiting_second"
    )
    if critical_second_pass:
        first = (prior_cross_confirmation or {}).get("first_audit") or {}
        err = cross_confirmation_error(first, audit)
        if err:
            return False, err

        second = audit_summary_from_blob(audit)
        row["cross_confirmation"]["second_audit"] = second
        matches = (
            first.get("verdict") == second.get("verdict")
            and first.get("claim_type") == second.get("claim_type")
            and first.get("load_bearing_step_class") == second.get("load_bearing_step_class")
        )
        if matches:
            row["cross_confirmation"]["status"] = "confirmed"
        else:
            row["cross_confirmation"]["status"] = "disagreement"
            row["audit_status"] = "audit_in_progress"
            row["blocker"] = "cross_confirmation_disagreement"
            rows[cid] = row
            ledger["rows"] = rows
            return True, (
                "cross-confirmation disagreement recorded "
                f"({first.get('verdict')!r}/{first.get('claim_type')!r}/"
                f"{first.get('load_bearing_step_class')!r} vs "
                f"{second.get('verdict')!r}/{second.get('claim_type')!r}/"
                f"{second.get('load_bearing_step_class')!r}); "
                "promote to third-auditor review"
            )

    # Cross-confirmation flow for critical claims.
    # First audit on a critical claim with audited_clean lands as
    # audit_in_progress and waits for a second independent auditor.
    # Second matching audit promotes to audited_clean.
    if (
        verdict == "audited_clean"
        and criticality == "critical"
        and not critical_second_pass
        and not third_pass
        and not legacy_claim_type_reaudit
    ):
        prior = row.get("cross_confirmation") or {}
        first = prior.get("first_audit")
        if first is None:
            row["cross_confirmation"] = {
                "first_audit": audit_summary_from_blob(audit),
                "second_audit": None,
                "status": "awaiting_second",
            }
            row["audit_status"] = "audit_in_progress"
            row["blocker"] = "awaiting_cross_confirmation"
            row["claim_type"] = claim_type
            row["claim_scope"] = claim_scope.strip()
            row["claim_type_provenance"] = "audited_pending_cross_confirmation"
            row["claim_type_last_reviewed"] = audit.get("audit_date") or datetime.now(timezone.utc).isoformat()
            rows[cid] = row
            ledger["rows"] = rows
            return True, "first audit recorded; awaiting independent second auditor"
        # We have a first audit on file; this is the second.
        err = cross_confirmation_error(first, audit)
        if err:
            return False, err
        if (
            first.get("load_bearing_step_class") != audit.get("load_bearing_step_class")
            or first.get("claim_type") != claim_type
        ):
            row["cross_confirmation"]["second_audit"] = audit_summary_from_blob(audit)
            row["cross_confirmation"]["status"] = "disagreement"
            row["audit_status"] = "audit_in_progress"
            row["blocker"] = "cross_confirmation_disagreement"
            rows[cid] = row
            ledger["rows"] = rows
            return False, (
                "first and second audits disagree on claim_type or load_bearing_step_class "
                f"({first.get('claim_type')!r}/{first.get('load_bearing_step_class')!r} vs "
                f"{claim_type!r}/{audit.get('load_bearing_step_class')!r}); "
                "promote to third-auditor review"
            )
        # Concordant second audit: promote.
        row["cross_confirmation"]["second_audit"] = audit_summary_from_blob(audit)
        row["cross_confirmation"]["status"] = "confirmed"

    # Apply the audit fields.
    row["audit_status"] = verdict
    row["auditor"] = audit["auditor"]
    row["auditor_family"] = audit["auditor_family"]
    row["auditor_model"] = audit["auditor_model"]
    row["auditor_reasoning_effort"] = audit["auditor_reasoning_effort"]
    row["independence"] = independence
    row["audit_date"] = audit.get("audit_date") or datetime.now(timezone.utc).isoformat()
    row["claim_type"] = claim_type
    row["claim_scope"] = claim_scope.strip()
    row["claim_type_provenance"] = "audited"
    row["claim_type_last_reviewed"] = row["audit_date"]
    row["notes_for_re_audit_if_any"] = audit.get("notes_for_re_audit_if_any")
    row["load_bearing_step"] = audit.get("load_bearing_step")
    row["load_bearing_step_class"] = audit.get("load_bearing_step_class")
    row["chain_closes"] = audit.get("chain_closes")
    row["chain_closure_explanation"] = audit.get("chain_closure_explanation")
    row["verdict_rationale"] = audit.get("verdict_rationale")
    row["open_dependency_paths"] = audit.get("open_dependency_paths", [])
    row["decoration_parent_claim_id"] = audit.get("decoration_parent_claim_id")
    row["auditor_confidence"] = audit.get("auditor_confidence")
    if "runner_check_breakdown" in audit:
        row["runner_check_breakdown"] = audit["runner_check_breakdown"]
    row["blocker"] = third_pass_blocker if third_pass else terminal_second_pass_blocker
    if legacy_claim_type_reaudit:
        row.setdefault("cross_confirmation", {})["claim_type_reaudit"] = audit_summary_from_blob(audit)
        row["cross_confirmation"]["mode"] = "legacy_confirmed_clean_claim_type_reaudit"

    # Snapshot the state at audit time so invalidate_stale_audits.py can
    # detect changes that warrant re-audit (dep added/removed, dep status
    # changed, criticality bumped).
    row["audit_state_snapshot"] = snapshot_audit_state(row, rows)

    rows[cid] = row
    ledger["rows"] = rows
    if terminal_second_pass_error:
        return False, terminal_second_pass_error
    if terminal_second_pass_msg:
        return True, terminal_second_pass_msg
    if third_pass_error:
        return False, third_pass_error
    if third_pass_msg:
        return True, third_pass_msg
    return True, "applied"


PROPAGATION_STEPS = (
    # Steps that depend only on the ledger's audit verdicts. We skip the
    # graph rebuild (notes weren't edited) but recompute everything an
    # audit-verdict change could shift downstream.
    ("compute_effective_status.py",        "post-apply effective_status pass"),
    ("invalidate_stale_audits.py",         "invalidate audits whose deps shifted"),
    ("compute_effective_status.py",        "post-invalidation effective_status pass"),
    ("compute_audit_queue.py",             "refresh audit queue"),
    ("compute_reaudit_candidates.py",      "refresh re-audit candidates"),
    ("render_audit_ledger.py",             "render AUDIT_LEDGER.md"),
    ("render_publication_effective_status.py", "render publication effective-status views"),
)


def run_propagation() -> int:
    """Run the propagation slice of the pipeline. Each step is a separate
    subprocess so a failure in one doesn't corrupt the others' state.
    """
    import subprocess

    scripts_dir = Path(__file__).resolve().parent
    print()
    print("Propagating audit verdicts through downstream pipeline steps...")
    failed = 0
    for script, desc in PROPAGATION_STEPS:
        script_path = scripts_dir / script
        if not script_path.exists():
            print(f"  [skip] {script} not found")
            continue
        print(f"  -> {script:42s} ({desc})")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        if result.returncode != 0:
            failed += 1
            print(f"     FAIL exit={result.returncode}", file=sys.stderr)
            if result.stderr:
                print(f"     stderr: {result.stderr.strip()[:400]}", file=sys.stderr)
    if failed:
        print(f"Propagation: {len(PROPAGATION_STEPS) - failed}/{len(PROPAGATION_STEPS)} steps OK ({failed} failed)")
        return 1
    print(f"Propagation: {len(PROPAGATION_STEPS)} steps OK")
    return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="Path to a single audit JSON file.")
    p.add_argument("--batch", help="Directory of audit JSON files (one per claim).")
    p.add_argument(
        "--no-propagate",
        action="store_true",
        help="Skip the post-write propagation pipeline. Use when applying many "
             "audits in sequence (call run_pipeline.sh manually after the batch).",
    )
    args = p.parse_args()

    if not LEDGER_PATH.exists():
        print(f"FAIL: ledger missing at {LEDGER_PATH}", file=sys.stderr)
        return 1

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))

    audits: list[dict] = []
    if args.file:
        audits.append(json.loads(Path(args.file).read_text(encoding="utf-8")))
    elif args.batch:
        for path in sorted(Path(args.batch).glob("*.json")):
            audits.append(json.loads(path.read_text(encoding="utf-8")))
    else:
        data = sys.stdin.read().strip()
        if not data:
            print("FAIL: no input on stdin and no --file/--batch given", file=sys.stderr)
            return 2
        parsed = json.loads(data)
        if isinstance(parsed, list):
            audits.extend(parsed)
        else:
            audits.append(parsed)

    applied = 0
    for a in audits:
        ok, msg = apply_one(ledger, a)
        cid = a.get("claim_id", "<unknown>")
        if ok:
            applied += 1
            print(f"OK  {cid}: {msg}")
        else:
            print(f"FAIL {cid}: {msg}", file=sys.stderr)

    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
    print(f"Applied {applied}/{len(audits)} audit(s) to {LEDGER_PATH.relative_to(REPO_ROOT)}")

    propagation_rc = 0
    if applied > 0 and not args.no_propagate:
        propagation_rc = run_propagation()

    if propagation_rc != 0:
        return 4
    return 0 if applied == len(audits) else 3


if __name__ == "__main__":
    raise SystemExit(main())
