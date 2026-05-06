#!/usr/bin/env python3
"""Relabel codex-gpt-5 audits that were actually run on gpt-5.5.

Audit-lane policy 2026-05-06: gpt-5.5 (xhigh) is the minimum acceptable
Codex model for new audits. The codex_audit_runner.py enforces this for
new audits, and the runner auto-labels its results with the actual model
used. But a batch of pre-policy rows have auditor_family='codex-gpt-5'
set by manual apply_audit.py invocations where the operator typed the
family by hand. Operator confirmation: those audits actually ran on
gpt-5.5 — the family field was just typed sloppily as the generic
codex-gpt-5 string.

Resolution: relabel them in place, no re-audit needed. The relabel
preserves the original (incorrect) auditor_family in
previous_auditor_family so the change is auditable.

This script identifies rows where:

  1. auditor_family is below the gpt-5.5 minimum (currently codex-gpt-5,
     codex-gpt-5.4, etc.);
  2. previous_auditor_family is None (= NOT a canonicalize_auditor_family.py
     relabel — those went through that migration and the family field
     reflects a relabel of legacy strings, not a fresh below-floor audit);
  3. audit_status is a terminal verdict (not unaudited / audit_in_progress).

For matching rows, this script sets:
  - previous_auditor_family = current auditor_family   (e.g. 'codex-gpt-5')
  - auditor_family = NEW_FAMILY                        ('codex-gpt-5.5')
  - relabel_reason = REASON_TAG

It also relabels matching cross_confirmation entries (first/second/third
audit summaries) where the entry's auditor identity matches the row's
main auditor — those are the same audit summarized twice, so they must
agree on family.

Usage:
  python3 docs/audit/scripts/relabel_unverified_codex_audits.py [--dry-run]
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
NEW_FAMILY = "codex-gpt-5.5"
REASON_TAG = "operator_pre_floor_policy_relabel_2026-05-06"

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


def is_unverified_codex_label(row: dict) -> bool:
    """Row qualifies for relabel iff:
      - it's audited (terminal verdict)
      - auditor_family is a Codex below-minimum string
      - previous_auditor_family is unset (NOT a canonicalize-migration relabel)
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


def relabel_cross_confirmation(cc: dict, main_auditor: str | None) -> int:
    """Relabel cross_confirmation entries that match the main auditor identity.

    Only entries with the SAME auditor identity as the row's main auditor get
    relabeled, because those are summaries of the same audit. Entries with
    different auditor identities (e.g., a third-pass auditor) belong to a
    different actor and stay unchanged.

    Returns the number of cc entries relabeled.
    """
    if not isinstance(cc, dict) or main_auditor is None:
        return 0
    relabeled = 0
    for key in ("first_audit", "second_audit", "third_audit", "claim_type_reaudit"):
        entry = cc.get(key)
        if not isinstance(entry, dict):
            continue
        entry_fam = entry.get("auditor_family") or ""
        entry_auditor = entry.get("auditor")
        if (
            entry_fam.startswith("codex-gpt-")
            and not codex_family_meets_minimum(entry_fam)
            and entry_auditor == main_auditor
        ):
            entry["previous_auditor_family"] = entry_fam
            entry["auditor_family"] = NEW_FAMILY
            relabeled += 1
    return relabeled


def relabel_row(row: dict) -> tuple[bool, int]:
    """Relabel one row in place. Returns (relabeled, cc_relabeled_count)."""
    if not is_unverified_codex_label(row):
        return False, 0
    main_auditor = row.get("auditor")
    row["previous_auditor_family"] = row["auditor_family"]
    row["auditor_family"] = NEW_FAMILY
    row["relabel_reason"] = REASON_TAG
    row["relabel_date"] = datetime.now(timezone.utc).isoformat()
    cc_count = relabel_cross_confirmation(row.get("cross_confirmation"), main_auditor)
    return True, cc_count


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
        if is_unverified_codex_label(row):
            targets.append(
                (
                    cid,
                    row.get("audit_status") or "?",
                    row.get("auditor_family") or "?",
                )
            )

    print(f"Unverified-codex rows to relabel: {len(targets)}")
    if targets[:10]:
        print("First 10:")
        for cid, status, fam in targets[:10]:
            print(f"  {cid:60s}  {status:25s}  {fam} -> {NEW_FAMILY}")

    if args.dry_run:
        print("dry-run; no writes.")
        return 0

    total_rows = 0
    total_cc = 0
    for cid, _status, _fam in targets:
        relabeled, cc_count = relabel_row(rows[cid])
        if relabeled:
            total_rows += 1
            total_cc += cc_count

    ledger["rows"] = rows
    ledger["last_unverified_codex_relabels"] = [
        {"claim_id": cid, "from_family": fam, "to_family": NEW_FAMILY}
        for cid, _status, fam in targets
    ]
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"  rows relabeled: {total_rows}")
    print(f"  cross_confirmation entries relabeled: {total_cc}")
    print(f"  next: bash docs/audit/scripts/run_pipeline.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
