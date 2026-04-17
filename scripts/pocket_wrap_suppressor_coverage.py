#!/usr/bin/env python3
"""Check suppressor-pair rescue coverage across pocket-signature local-morph near-misses."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_suppressor_coverage_analysis,
    render_pocket_wrap_suppressor_coverage_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap suppressor coverage started {started}", flush=True)
    total_start = time.time()
    rows = pocket_wrap_suppressor_coverage_analysis()

    pair_present = sum(1 for row in rows if row.pair_present)
    pair_rescue = sum(1 for row in rows if row.pair_rescue)
    single_rescue = sum(1 for row in rows if row.single_drop_rescue)
    target_match = sum(1 for row in rows if row.target_gap_match)

    print()
    print("Pocket-Wrap Suppressor Coverage")
    print("==============================")
    print(
        "rows="
        f"{len(rows)} "
        f"pair_present={pair_present} "
        f"pair_rescue={pair_rescue} "
        f"single_rescue={single_rescue} "
        f"target_match={target_match}"
    )
    print(render_pocket_wrap_suppressor_coverage_table(rows))
    print()
    print(
        "pocket-wrap suppressor coverage completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
