#!/usr/bin/env python3
"""Summarize which taper-wrap pre-jump contexts are sensitive to the endpoint jump."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_taper_wrap_jump_context_aggregate_table,
    taper_wrap_jump_context_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"taper-wrap jump context analysis started {started}", flush=True)
    total_start = time.time()
    _rows, aggregate_rows = taper_wrap_jump_context_analysis()

    print()
    print("Taper-Wrap Jump Context")
    print("=======================")
    print(render_taper_wrap_jump_context_aggregate_table(aggregate_rows))
    print()
    print("Interpretation")
    print("==============")
    for row in aggregate_rows:
        print(
            f"- {row.target_variant} {row.outcome}: cases={row.cases}, modes={row.modes}, "
            f"mean cvar={row.mean_center_variation:.2f}, boundary_roughness={row.mean_boundary_roughness:.2f}, "
            f"mirror asym={row.mean_mirror_center_asymmetry:.2f}, "
            f"band center/high={row.mean_changed_band_center:+.2f}/{row.mean_changed_band_high:+.2f}, "
            f"crossing cases={row.crossing_cases}."
        )

    print()
    print(
        "taper-wrap jump context analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
