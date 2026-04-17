#!/usr/bin/env python3
"""Compare the last non-defect interpolation state to the taper-wrap offender endpoint."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_taper_wrap_endpoint_jump_columns,
    render_taper_wrap_endpoint_jump_table,
    taper_wrap_endpoint_jump_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"taper-wrap endpoint jump analysis started {started}", flush=True)
    total_start = time.time()
    summary_rows, column_rows = taper_wrap_endpoint_jump_analysis()

    print()
    print("Taper-Wrap Endpoint Jump")
    print("========================")
    print(render_taper_wrap_endpoint_jump_table(summary_rows))
    print()
    print("Changed Columns")
    print("===============")
    print(render_taper_wrap_endpoint_jump_columns(column_rows))
    print()
    print("Interpretation")
    print("==============")
    for row in summary_rows:
        print(
            f"- {row.target_variant}: last non-defect alpha={row.prior_alpha:.2f} ({row.prior_outcome}) "
            f"to endpoint ({row.endpoint_outcome}) changes {row.changed_columns} columns at x={row.changed_xs}; "
            f"boundary gap {row.prior_boundary_gap:+.2f}->{row.endpoint_boundary_gap:+.2f}, "
            f"low gap {row.prior_low_degree_gap:+.2f}->{row.endpoint_low_degree_gap:+.2f}, "
            f"pocket gap {row.prior_pocket_gap:+.2f}->{row.endpoint_pocket_gap:+.2f}, "
            f"crosses-midline {row.prior_crosses_midline}->{row.endpoint_crosses_midline}."
        )

    print()
    print(
        "taper-wrap endpoint jump analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
