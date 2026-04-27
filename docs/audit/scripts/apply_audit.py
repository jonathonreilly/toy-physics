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
  - auditor identity must differ from author identity for audited_clean
  - the row's note_hash must match disk (otherwise the audit is stale)
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

ALLOWED_INDEPENDENCE = {"weak", "cross_family", "strong", "external"}


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

    # Hard rule: weak independence cannot land audited_clean.
    if verdict == "audited_clean" and independence == "weak":
        return False, "audited_clean requires independence != 'weak'"

    # Criticality-aware independence rule.
    criticality = row.get("criticality") or "leaf"
    if verdict == "audited_clean" and criticality in {"critical", "high"} and independence == "weak":
        return False, f"criticality={criticality} requires independence >= cross_family for audited_clean"

    # Hash drift check.
    on_disk_path = REPO_ROOT / row.get("note_path", "")
    if on_disk_path.exists():
        import hashlib
        on_disk_hash = hashlib.sha256(
            on_disk_path.read_text(encoding="utf-8", errors="replace").encode("utf-8")
        ).hexdigest()
        if on_disk_hash != row.get("note_hash"):
            return False, "note_hash drift; rerun seed_audit_ledger.py before applying audit"

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
        if first.get("auditor_family") == audit["auditor_family"]:
            return False, "second auditor must be from a different auditor_family than the first"
        if first.get("load_bearing_step_class") != audit.get("load_bearing_step_class"):
            row["cross_confirmation"]["second_audit"] = {
                "auditor": audit["auditor"],
                "auditor_family": audit["auditor_family"],
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
    row["blocker"] = None

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
