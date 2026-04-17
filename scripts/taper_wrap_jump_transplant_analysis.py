#!/usr/bin/env python3
"""Test whether the taper-wrap endpoint jump is sufficient earlier on the path."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_taper_wrap_jump_transplant_table,
    taper_wrap_jump_transplant_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"taper-wrap jump transplant started {started}", flush=True)
    total_start = time.time()
    rows = taper_wrap_jump_transplant_analysis()

    print()
    print("Taper-Wrap Jump Transplant")
    print("==========================")
    print(render_taper_wrap_jump_transplant_table(rows))
    print()
    print("Interpretation")
    print("==============")
    for row in rows:
        if row.jump_label == "full-band+1":
            print(
                f"- {row.target_variant} alpha={row.alpha:.2f}: full-band jump -> {row.outcome}, "
                f"low gap {row.low_degree_gap:+.2f}, boundary gap {row.boundary_gap:+.2f}, "
                f"crosses-midline={row.crosses_midline}, matches-endpoint={row.matches_endpoint}."
            )
    for row in rows:
        if row.jump_label.startswith("omit-"):
            print(
                f"- {row.target_variant} {row.jump_label}: endpoint leave-one-out -> {row.outcome}, "
                f"low gap {row.low_degree_gap:+.2f}, boundary gap {row.boundary_gap:+.2f}, "
                f"crosses-midline={row.crosses_midline}."
            )

    print()
    print(
        "taper-wrap jump transplant completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
