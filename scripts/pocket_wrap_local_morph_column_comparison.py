#!/usr/bin/env python3
"""Show the exact column deltas against the closest pocket-wrap near-misses."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    pocket_wrap_local_morph_column_comparison_analysis,
    render_pocket_wrap_local_morph_column_comparison_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"pocket-wrap local-morph column comparison started {started}", flush=True)
    total_start = time.time()
    rows = pocket_wrap_local_morph_column_comparison_analysis()

    print()
    print("Pocket-Wrap Local-Morph Column Comparisons")
    print("==========================================")
    print(render_pocket_wrap_local_morph_column_comparison_table(rows))
    print()
    print(
        "pocket-wrap local-morph column comparison completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
