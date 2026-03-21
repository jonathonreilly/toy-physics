#!/usr/bin/env python3
"""Widen the local-morph family and track pocket-signature defections."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (  # noqa: E402
    local_morph_pocket_ladder_analysis,
    render_local_morph_pocket_ladder_aggregate_table,
    render_local_morph_pocket_ladder_table,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"local-morph pocket ladder started {started}", flush=True)
    total_start = time.time()
    rows, aggregate_rows = local_morph_pocket_ladder_analysis()

    print()
    print("Local-Morph Pocket Ladder Aggregate")
    print("===================================")
    print(render_local_morph_pocket_ladder_aggregate_table(aggregate_rows))
    print()
    print("Local-Morph Pocket Ladder Cases")
    print("===============================")
    print(render_local_morph_pocket_ladder_table(rows))
    print()
    print(
        "local-morph pocket ladder completed "
        + datetime.now().isoformat(timespec="seconds")
        + f" total_elapsed={time.time() - total_start:.1f}s",
        flush=True,
    )


if __name__ == "__main__":
    main()
