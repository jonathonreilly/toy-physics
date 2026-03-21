#!/usr/bin/env python3
"""Apply the taper-wrap offender jump bands to non-offender mode states."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_taper_wrap_cross_context_jump_aggregate_table,
    taper_wrap_cross_context_jump_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"taper-wrap cross-context jump analysis started {started}", flush=True)
    total_start = time.time()
    _rows, aggregate_rows = taper_wrap_cross_context_jump_analysis()

    print()
    print("Taper-Wrap Cross-Context Jump")
    print("=============================")
    print(render_taper_wrap_cross_context_jump_aggregate_table(aggregate_rows))
    print()
    print("Interpretation")
    print("==============")
    for row in aggregate_rows:
        first_dpadj = "-" if row.first_dpadj_amplitude is None else f"{row.first_dpadj_amplitude:+.2f}"
        print(
            f"- {row.target_variant} on {row.mode}: dpadj-only={row.dpadj_only_cases}, "
            f"ge6-only={row.ge6_only_cases}, both={row.both_cases}, neither={row.neither_cases}; "
            f"first dpadj amplitude {first_dpadj}; "
            f"max low/bdef={row.max_low_degree_gap:+.2f}/{row.max_boundary_gap:+.2f}."
        )

    print()
    print(
        "taper-wrap cross-context jump analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
