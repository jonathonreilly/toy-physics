#!/usr/bin/env python3
"""Interpolate from base:taper-wrap toward recurring offender variants."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_taper_wrap_offender_interpolation_aggregate_table,
    render_taper_wrap_offender_interpolation_table,
    taper_wrap_offender_interpolation_sweep,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"taper-wrap offender interpolation started {started}", flush=True)
    total_start = time.time()
    rows, aggregate_rows = taper_wrap_offender_interpolation_sweep()

    print()
    print("Taper-Wrap Offender Interpolation")
    print("=================================")
    print(render_taper_wrap_offender_interpolation_aggregate_table(aggregate_rows))
    print()
    print("Interpolation Rows")
    print("==================")
    print(render_taper_wrap_offender_interpolation_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in aggregate_rows:
        first_dpadj = "-" if row.first_dpadj_alpha is None else f"{row.first_dpadj_alpha:.2f}"
        print(
            f"- {row.target_variant}: dpadj-only={row.dpadj_only_cases}, ge6-only={row.ge6_only_cases}, "
            f"both={row.both_cases}, neither={row.neither_cases}; "
            f"first dpadj alpha {first_dpadj}; "
            f"max gaps d/p/l={row.max_deep_gap:+.2f}/{row.max_pocket_gap:+.2f}/{row.max_low_degree_gap:+.2f}."
        )

    print()
    print(
        "taper-wrap offender interpolation completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
