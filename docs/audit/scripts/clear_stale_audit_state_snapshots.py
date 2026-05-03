#!/usr/bin/env python3
"""Clear stale audit_state_snapshot fields on already-unaudited rows.

Background: `apply_audit.py` sets `audit_state_snapshot` at audit time so
`invalidate_stale_audits.py` can detect downstream changes. When an audit is
reset (note-hash drift, archived audit, or invalidate), the snapshot from
the prior audit is just historical noise — it doesn't correspond to any
active audit verdict, so any "criticality bumped since audit" warning the
lint generates against it is a false positive.

`seed_audit_ledger.py`'s `EMPTY_AUDIT` was missing `audit_state_snapshot`,
so re-seeding a row with hash drift left the prior snapshot in place. The
2026-05-03 fix (`docs/audit/scripts/seed_audit_ledger.py`) adds the field
to `EMPTY_AUDIT` so future re-seeds clear the snapshot. **This script is a
one-time cleanup for the existing rows that already accumulated stale
snapshots before the fix.**

Run this once after pulling the fix; subsequent re-seeds are self-cleaning.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
LEDGER_PATH = REPO_ROOT / "docs" / "audit" / "data" / "audit_ledger.json"


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit(f"audit_ledger.json missing at {LEDGER_PATH}")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    cleared = 0
    for cid, row in rows.items():
        if row.get("audit_status", "unaudited") not in {"unaudited", "audit_in_progress"}:
            continue  # row has an active audit verdict; snapshot is meaningful
        if row.get("audit_state_snapshot") is None:
            continue  # already clean
        row["audit_state_snapshot"] = None
        rows[cid] = row
        cleared += 1

    ledger["rows"] = rows
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n")

    print(f"clear_stale_audit_state_snapshots: scanned {len(rows)} rows")
    print(f"  cleared: {cleared} stale snapshots on already-unaudited rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
