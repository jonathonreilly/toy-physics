#!/usr/bin/env python3
"""Run a soft hub-exposure replacement sweep for the high-degree motif."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (
    soft_hub_exposure_benchmark,
    soft_hub_exposure_sets,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"soft hub-exposure sweep started {started}", flush=True)
    total_start = time.time()
    for exposure_set in soft_hub_exposure_sets():
        set_start = time.time()
        row = soft_hub_exposure_benchmark(
            exposure_sets=(exposure_set,),
        )[0]
        print(
            f"{row.decomposition_name}: "
            f"removed={row.removed_features} "
            f"| added={row.added_features} "
            f"| compact_parity={row.compact_parity_size}:{row.compact_parity_feature_subset} "
            f"| compact_pre={row.compact_best_prethreshold_gap:+.2f}/{row.compact_best_prethreshold_worst_gap:+.2f} "
            f"| extended_parity={row.extended_parity_size}:{row.extended_parity_feature_subset} "
            f"| extended_pre={row.extended_best_prethreshold_gap:+.2f}/{row.extended_best_prethreshold_worst_gap:+.2f} "
            f"| elapsed={time.time() - set_start:.1f}s",
            flush=True,
        )
    finished = datetime.now().isoformat(timespec="seconds")
    print(f"completed {finished} total_elapsed={time.time() - total_start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
