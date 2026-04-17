#!/usr/bin/env python3
"""Measure how distinct the corrected extended atomic backup routes really are."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    extended_atomic_route_overlap_benchmark,
    render_extended_atomic_route_overlap_table,
)


def main() -> None:
    print(
        "extended atomic route overlap analysis started "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )
    _scores, overlaps = extended_atomic_route_overlap_benchmark(
        mode_retained_weight=1.0,
        include_scores=False,
    )
    print("Extended Atomic Route Overlaps")
    print("==============================")
    print(render_extended_atomic_route_overlap_table(overlaps))
    print()
    print(
        "extended atomic route overlap analysis completed "
        + datetime.now().isoformat(timespec="seconds"),
        flush=True,
    )


if __name__ == "__main__":
    main()
