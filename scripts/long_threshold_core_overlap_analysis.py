#!/usr/bin/env python3
"""Explain the corrected compact threshold core via node overlap and tree thresholds."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    render_threshold_core_model_table,
    render_threshold_core_overlap_table,
    threshold_core_overlap_analysis,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"threshold core overlap analysis started {started}", flush=True)
    total_start = time.time()
    overlap_rows, model_rows = threshold_core_overlap_analysis(
        mode_retained_weight=1.0,
    )
    print()
    print("Threshold Core Overlap")
    print("======================")
    print(render_threshold_core_overlap_table(overlap_rows))
    print()
    print("Threshold Core Models")
    print("=====================")
    print(render_threshold_core_model_table(model_rows))
    print()
    print(
        "threshold core overlap analysis completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
