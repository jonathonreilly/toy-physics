#!/usr/bin/env python3
"""Test whether suppressor injection is pocket-wrap-specific or a generic dpadj kill switch."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_suppressor_specificity_analysis,
    render_pocket_wrap_suppressor_specificity_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor specificity started {started}", flush=True)
    total_start = time.time()
    rows = pocket_wrap_suppressor_specificity_analysis()

    total = len(rows)
    psig = [row for row in rows if row.pocket_signature]
    non_psig = [row for row in rows if not row.pocket_signature]

    def count_kills(items: list) -> tuple[int, int, int]:
        single = sum(1 for row in items if row.single_add_kills)
        pair = sum(1 for row in items if row.pair_add_kills)
        collapse = sum(1 for row in items if row.pair_matches_collapse)
        return single, pair, collapse

    psig_single, psig_pair, psig_collapse = count_kills(psig)
    non_single, non_pair, non_collapse = count_kills(non_psig)

    print()
    print("Pocket-Wrap Suppressor Specificity")
    print("==================================")
    print(
        f"rows={total} "
        f"psig={len(psig)} "
        f"non_psig={len(non_psig)} "
        f"psig(single/pair/collapse)={psig_single}/{psig_pair}/{psig_collapse} "
        f"non(single/pair/collapse)={non_single}/{non_pair}/{non_collapse}"
    )
    print(render_pocket_wrap_suppressor_specificity_table(rows))
    print()
    print(
        "pocket-wrap suppressor specificity completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
