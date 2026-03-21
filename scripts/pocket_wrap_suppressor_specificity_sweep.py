#!/usr/bin/env python3
"""Sweep suppressor-specificity rules over deeper local-morph ladders."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import pocket_wrap_suppressor_specificity_analysis  # noqa: E402


LIMITS = (40, 48, 56)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor specificity sweep started {started}", flush=True)
    total_start = time.time()

    print()
    print("Pocket-Wrap Suppressor Specificity Sweep")
    print("========================================")
    print(
        "limit | rows | old(tp/fp/fn) | any-overlap(tp/fp/fn) | "
        "pair-kill rows | strict-rule fn rows"
    )
    print(
        "------+------|---------------|-----------------------|"
        "-------------------------------|----------------------------"
    )

    for limit in LIMITS:
        rows = pocket_wrap_suppressor_specificity_analysis(variant_limit=limit)

        tp_old = sum(1 for r in rows if r.pair_targets_deep_cells and r.pair_add_kills)
        fp_old = sum(1 for r in rows if r.pair_targets_deep_cells and not r.pair_add_kills)
        fn_old = sum(1 for r in rows if (not r.pair_targets_deep_cells) and r.pair_add_kills)

        tp_any = sum(1 for r in rows if (r.deep_overlap_count > 0) and r.pair_add_kills)
        fp_any = sum(1 for r in rows if (r.deep_overlap_count > 0) and not r.pair_add_kills)
        fn_any = sum(1 for r in rows if (r.deep_overlap_count == 0) and r.pair_add_kills)

        pair_kill_rows = [r.source_name.encode("unicode_escape").decode("ascii") for r in rows if r.pair_add_kills]
        strict_fn_rows = [
            r.source_name.encode("unicode_escape").decode("ascii")
            for r in rows
            if (not r.pair_targets_deep_cells) and r.pair_add_kills
        ]

        print(
            f"{limit:>5} | "
            f"{len(rows):>4} | "
            f"{tp_old:>2}/{fp_old:<2}/{fn_old:<2}        | "
            f"{tp_any:>2}/{fp_any:<2}/{fn_any:<2}                  | "
            f"{','.join(pair_kill_rows) or '-':<29.29} | "
            f"{','.join(strict_fn_rows) or '-'}"
        )

    print()
    print(
        "pocket-wrap suppressor specificity sweep completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
