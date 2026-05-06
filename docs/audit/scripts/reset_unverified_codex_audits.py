#!/usr/bin/env python3
"""Reset audits whose Codex model provenance is unverified to unaudited.

Audit-lane policy (2026-05-06): all Codex audits must run on gpt-5.5 or
newer. The codex_audit_runner.py enforces this for new audits, but a
batch of pre-policy rows have auditor_family='codex-gpt-5' set by
manual apply_audit.py invocations. There are no run logs for those
audits (logs/codex-audit-runs/ was empty when the policy landed), so
we cannot programmatically verify which model they actually used.

Conservative resolution: invalidate them all and requeue. The prior
audit fields are preserved in previous_audits with a clear
invalidation_reason so the history isn't lost.

This script identifies rows where:

  1. auditor_family is below the gpt-5.5 minimum (currently codex-gpt-5,
     codex-gpt-5.4, etc.), OR a known-legacy non-canonical family that
     wasn't migrated by canonicalize_auditor_family.py;
  2. previous_auditor_family is None (= NOT a legacy-migration relabel,
     so the family was set directly at audit time and is the actual
     claim of model used);
  3. audit_status is a terminal verdict (not already unaudited).

It does NOT touch rows whose previous_auditor_family is set — those
went through the canonicalize_auditor_family.py migration and the
canonical label is a relabel, not a fresh below-minimum audit.

Usage:
  python3 docs/audit/scripts/reset_unverified_codex_audits.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

MINIMUM_CODEX_MODEL = "gpt-5.5"
INVALIDATION_REASON = "codex_model_provenance_unverified_2026-05-06"

# Audit fields to archive into previous_audits when invalidating.
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
}

_CODEX_FAMILY_RE = re.compile(r"^codex-gpt-(\d+(?:\.\d+)*)$")


def codex_family_meets_minimum(family: str, minimum: str = MINIMUM_CODEX_MODEL) -> bool:
    if not isinstance(family, str) or not family.startswith("codex-gpt-"):
        return True
    fam_match = _CODEX_FAMILY_RE.match(family)
    if not fam_match:
        return True
    fam_rank = tuple(int(p) for p in fam_match.group(1).split("."))
    min_match = re.match(r"gpt-(\d+(?:\.\d+)*)", minimum)
    if not min_match:
        return True
    min_rank = tuple(int(p) for p in min_match.group(1).split("."))
    width = max(len(fam_rank), len(min_rank))
    return (fam_rank + (0,) * (width - len(fam_rank))) >= (
        min_rank + (0,) * (width - len(min_rank))
    )


def is_unverified_audit(row: dict) -> bool:
    """Row qualifies for invalidation iff:
      - it's audited (terminal verdict)
      - auditor_family is a Codex below-minimum string
      - previous_auditor_family is unset (= not a legacy-migration relabel)
    """
    audit_status = row.get("audit_status")
    if audit_status in (None, "unaudited", "audit_in_progress"):
        return False
    fam = row.get("auditor_family") or ""
    if not fam.startswith("codex-gpt-"):
        return False
    if codex_family_meets_minimum(fam):
        return False
    if row.get("previous_auditor_family"):
        return False
    return True


def archive_and_reset(row: dict) -> dict:
    prior = {k: row.get(k) for k in ARCHIVED_FIELDS}
    prior["archived_at"] = datetime.now(timezone.utc).isoformat()
    prior["invalidation_reason"] = INVALIDATION_REASON
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
    # Don't preserve previous_auditor_family — it was None for these rows
    # by definition.
    new_row.pop("previous_auditor_family", None)
    return new_row


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would change without writing the ledger.")
    args = p.parse_args()

    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    targets: list[tuple[str, str, str]] = []
    for cid, row in rows.items():
        if is_unverified_audit(row):
            targets.append(
                (
                    cid,
                    row.get("audit_status") or "?",
                    row.get("auditor_family") or "?",
                )
            )

    print(f"Unverified-codex audits to invalidate: {len(targets)}")
    if targets[:10]:
        print("First 10:")
        for cid, status, fam in targets[:10]:
            print(f"  {cid:60s}  {status:25s}  {fam}")

    if args.dry_run:
        print("dry-run; no writes.")
        return 0

    for cid, _status, _fam in targets:
        rows[cid] = archive_and_reset(rows[cid])

    ledger["rows"] = rows
    ledger["last_unverified_codex_invalidations"] = [
        {"claim_id": cid, "prior_status": status, "prior_family": fam}
        for cid, status, fam in targets
    ]
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"  invalidated: {len(targets)} rows")
    print(f"  next: bash docs/audit/scripts/run_pipeline.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
