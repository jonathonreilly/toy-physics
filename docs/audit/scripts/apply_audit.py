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
  - audited_clean records the audit verdict for any allowed current_status;
    compute_effective_status.py only promotes clean proposed_* rows, so
    support/bounded/open/unknown rows keep their declared tier unless later
    re-tiered by the author
  - auditor identity must differ from author identity for audited_clean
  - the row's note_hash must match disk (otherwise the audit is stale)
  - fresh-context second passes over existing high/critical terminal verdicts
    record a cross-confirmation comparison before any retraction can cascade
  - third-auditor passes over cross-confirmation disagreements record the
    tiebreaker and hard-stop on genuine three-way disagreement
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

REQUIRED_FIELDS = {
    "claim_id",
    "verdict",
    "auditor",
    "auditor_family",
    "independence",
}

ALLOWED_VERDICTS = {
    "audited_clean",
    "audited_renaming",
    "audited_conditional",
    "audited_decoration",
    "audited_failed",
    "audited_numerical_match",
}

ALLOWED_INDEPENDENCE = {"weak", "fresh_context", "cross_family", "strong", "external"}
CLEAN_INDEPENDENCE = ALLOWED_INDEPENDENCE - {"weak"}
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
        "independence": row.get("independence"),
        "audit_date": row.get("audit_date"),
        "load_bearing_step_class": row.get("load_bearing_step_class"),
        "verdict": row.get("audit_status"),
    }


def audit_summary_from_blob(audit: dict) -> dict:
    return {
        "auditor": audit.get("auditor"),
        "auditor_family": audit.get("auditor_family"),
        "independence": audit.get("independence"),
        "audit_date": audit.get("audit_date") or datetime.now(timezone.utc).isoformat(),
        "load_bearing_step_class": audit.get("load_bearing_step_class"),
        "verdict": audit.get("verdict"),
    }


def apply_one(ledger: dict, audit: dict) -> tuple[bool, str]:
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

    independence = audit["independence"]
    if independence not in ALLOWED_INDEPENDENCE:
        return False, f"independence {independence!r} not in {sorted(ALLOWED_INDEPENDENCE)}"

    criticality = row.get("criticality") or "leaf"
    if verdict == "audited_clean":
        err = clean_independence_error(independence, criticality)
        if err:
            return False, err

    # Hash drift check.
    on_disk_path = REPO_ROOT / row.get("note_path", "")
    if on_disk_path.exists():
        import hashlib
        on_disk_hash = hashlib.sha256(
            on_disk_path.read_text(encoding="utf-8", errors="replace").encode("utf-8")
        ).hexdigest()
        if on_disk_hash != row.get("note_hash"):
            return False, "note_hash drift; rerun seed_audit_ledger.py before applying audit"

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
                f"({first.get('verdict')!r}/{first.get('load_bearing_step_class')!r} vs "
                f"{second.get('verdict')!r}/{second.get('load_bearing_step_class')!r}); "
                "promote to third-auditor review or human escalation"
            )
            terminal_second_pass_blocker = "cross_confirmation_disagreement"

    third_pass = (
        prior_cross_confirmation_status == "disagreement"
        and row.get("blocker") == "cross_confirmation_disagreement"
    )
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
        if third_verdict == first_verdict:
            row["cross_confirmation"]["third_audit"] = third
            row["cross_confirmation"]["status"] = "third_confirmed_first"
            row["cross_confirmation"]["mode"] = "terminal_third_pass"
            third_pass_msg = "third auditor confirmed first verdict"
        elif third_verdict == second_verdict:
            row["cross_confirmation"]["third_audit"] = third
            row["cross_confirmation"]["status"] = "third_confirmed_second"
            row["cross_confirmation"]["mode"] = "terminal_third_pass"
            third_pass_msg = "third auditor confirmed second verdict"
        else:
            row["cross_confirmation"]["third_audit"] = third
            row["cross_confirmation"]["status"] = "three_way_disagreement"
            row["cross_confirmation"]["mode"] = "terminal_third_pass"
            third_pass_error = (
                "third auditor introduced a third verdict "
                f"({first_verdict!r} vs {second_verdict!r} vs {third_verdict!r}); "
                "escalate to human review"
            )
            third_pass_blocker = "third_auditor_disagreement"

    # Cross-confirmation flow for critical claims.
    # First audit on a critical claim with audited_clean lands as
    # audit_in_progress and waits for a second independent auditor.
    # Second matching audit promotes to audited_clean.
    if verdict == "audited_clean" and criticality == "critical":
        prior = row.get("cross_confirmation") or {}
        first = prior.get("first_audit")
        if first is None:
            row["cross_confirmation"] = {
                "first_audit": {
                    "auditor": audit["auditor"],
                    "auditor_family": audit["auditor_family"],
                    "independence": independence,
                    "audit_date": audit.get("audit_date") or datetime.now(timezone.utc).isoformat(),
                    "load_bearing_step_class": audit.get("load_bearing_step_class"),
                    "verdict": "audited_clean",
                },
                "second_audit": None,
                "status": "awaiting_second",
            }
            row["audit_status"] = "audit_in_progress"
            row["blocker"] = "awaiting_cross_confirmation"
            rows[cid] = row
            ledger["rows"] = rows
            return True, "first audit recorded; awaiting independent second auditor"
        # We have a first audit on file; this is the second.
        err = cross_confirmation_error(first, audit)
        if err:
            return False, err
        if first.get("load_bearing_step_class") != audit.get("load_bearing_step_class"):
            row["cross_confirmation"]["second_audit"] = {
                "auditor": audit["auditor"],
                "auditor_family": audit["auditor_family"],
                "independence": independence,
                "audit_date": audit.get("audit_date") or datetime.now(timezone.utc).isoformat(),
                "load_bearing_step_class": audit.get("load_bearing_step_class"),
                "verdict": "audited_clean",
            }
            row["cross_confirmation"]["status"] = "disagreement"
            row["audit_status"] = "audit_in_progress"
            row["blocker"] = "cross_confirmation_disagreement"
            rows[cid] = row
            ledger["rows"] = rows
            return False, (
                "first and second audits disagree on load_bearing_step_class "
                f"({first.get('load_bearing_step_class')!r} vs {audit.get('load_bearing_step_class')!r}); "
                "promote to third-auditor review"
            )
        # Concordant second audit: promote.
        row["cross_confirmation"]["second_audit"] = {
            "auditor": audit["auditor"],
            "auditor_family": audit["auditor_family"],
            "independence": independence,
            "audit_date": audit.get("audit_date") or datetime.now(timezone.utc).isoformat(),
            "load_bearing_step_class": audit.get("load_bearing_step_class"),
            "verdict": "audited_clean",
        }
        row["cross_confirmation"]["status"] = "confirmed"

    # Apply the audit fields.
    row["audit_status"] = verdict
    row["auditor"] = audit["auditor"]
    row["auditor_family"] = audit["auditor_family"]
    row["independence"] = independence
    row["audit_date"] = audit.get("audit_date") or datetime.now(timezone.utc).isoformat()
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

    # Snapshot the state at audit time so invalidate_stale_audits.py can
    # detect changes that warrant re-audit (dep added/removed, dep status
    # changed, criticality bumped).
    deps = sorted(row.get("deps", []))
    row["audit_state_snapshot"] = {
        "deps": deps,
        "dep_effective_status": {
            d: rows.get(d, {}).get("effective_status")
            or rows.get(d, {}).get("current_status")
            or "unknown"
            for d in deps
        },
        "criticality": row.get("criticality"),
        "load_bearing_score": row.get("load_bearing_score"),
        "transitive_descendants": row.get("transitive_descendants"),
    }

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


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="Path to a single audit JSON file.")
    p.add_argument("--batch", help="Directory of audit JSON files (one per claim).")
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
    return 0 if applied == len(audits) else 3


if __name__ == "__main__":
    raise SystemExit(main())
