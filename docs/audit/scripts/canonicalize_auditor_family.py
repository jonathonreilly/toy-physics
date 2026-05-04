#!/usr/bin/env python3
r"""One-time migration: canonicalize legacy auditor_family strings.

The audit lane originally accumulated several ad-hoc family identifiers as the
runner evolved. The lint now enforces a canonical set via
audit_lint.CANONICAL_AUDITOR_FAMILIES, and this script normalises legacy
strings ahead of that enforcement.

Mapping rules (best-effort, conservative):

  codex-current        -> codex-gpt-5      (the runner's pre-cache fallback)
  codex-fresh          -> codex-gpt-5      (same era)
  codex-fresh-agent    -> codex-gpt-5      (same era)
  codex-fresh-context  -> codex-gpt-5      (same era; fresh_context independence)
  codex-gpt-5          -> codex-gpt-5      (already canonical)
  codex-gpt-5.5        -> codex-gpt-5.5    (already canonical)
  claude-opus          -> claude-opus      (already canonical)

Any auditor_family already matching ^codex-gpt-\d is left alone (forward-compat).

The migration:
  - rewrites the top-level row.auditor_family field
  - rewrites cross_confirmation.first_audit/second_audit/third_audit
    auditor_family fields to match
  - leaves the original value in row.previous_auditor_family for one cycle
    so a subsequent pipeline run can verify the migration

Usage:
  python3 docs/audit/scripts/canonicalize_auditor_family.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"

LEGACY_TO_CANONICAL = {
    "codex-current": "codex-gpt-5",
    "codex-fresh": "codex-gpt-5",
    "codex-fresh-agent": "codex-gpt-5",
    "codex-fresh-context": "codex-gpt-5",
}

CANONICAL_PATTERN = re.compile(r"^codex-gpt-\d")


def canonicalize(family: str | None) -> str | None:
    if family is None:
        return None
    if CANONICAL_PATTERN.match(family):
        return family
    if family in LEGACY_TO_CANONICAL:
        return LEGACY_TO_CANONICAL[family]
    return family  # leave non-codex strings alone (claude-*, human, external, ...)


def rewrite_audit_summary(summary: dict | None) -> tuple[dict | None, bool]:
    if not isinstance(summary, dict):
        return summary, False
    fam = summary.get("auditor_family")
    new_fam = canonicalize(fam)
    if new_fam == fam:
        return summary, False
    summary = dict(summary)
    summary["auditor_family"] = new_fam
    summary["previous_auditor_family"] = fam
    return summary, True


def migrate(rows: dict[str, dict]) -> Counter:
    stats = Counter()
    for cid, row in rows.items():
        old = row.get("auditor_family")
        new = canonicalize(old)
        if new != old:
            row["previous_auditor_family"] = old
            row["auditor_family"] = new
            stats[f"row:{old}->{new}"] += 1
        cc = row.get("cross_confirmation")
        if isinstance(cc, dict):
            for key in ("first_audit", "second_audit", "third_audit", "claim_type_reaudit"):
                summary = cc.get(key)
                new_summary, changed = rewrite_audit_summary(summary)
                if changed:
                    cc[key] = new_summary
                    stats[f"cc.{key}"] += 1
            row["cross_confirmation"] = cc
        for prior in row.get("previous_audits", []) or []:
            new_summary, changed = rewrite_audit_summary(prior)
            if changed:
                # in-place via dict mutation
                prior.update(new_summary)
                stats["previous_audit"] += 1
    return stats


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true",
                   help="Report what would change without writing the ledger.")
    args = p.parse_args()

    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})
    stats = migrate(rows)
    if args.dry_run:
        print("dry-run; no writes.")
    else:
        ledger["rows"] = rows
        LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")
        print(f"Wrote {LEDGER_PATH.relative_to(REPO_ROOT)}")
    print(f"Migration stats:")
    for k, v in stats.most_common():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
