#!/usr/bin/env python3
"""Run a focused split ablation on the rich degree-extreme motif family."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (
    neighborhood_basis_ablation_benchmark,
    rich_degree_extreme_ablation_sets,
)


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"degree-extreme split sweep started {started}", flush=True)
    total_start = time.time()
    rows = neighborhood_basis_ablation_benchmark(
        ablation_sets=rich_degree_extreme_ablation_sets(),
    )
    for row in rows:
        print(
            f"{row.ablation_name}: "
            f"compact_parity={row.compact_parity_size}:{row.compact_parity_feature_subset} "
            f"| compact_pre={row.compact_best_prethreshold_gap:+.2f}/{row.compact_best_prethreshold_worst_gap:+.2f} "
            f"| extended_parity={row.extended_parity_size}:{row.extended_parity_feature_subset} "
            f"| extended_pre={row.extended_best_prethreshold_gap:+.2f}/{row.extended_best_prethreshold_worst_gap:+.2f}",
            flush=True,
        )
    finished = datetime.now().isoformat(timespec="seconds")
    print(f"completed {finished} total_elapsed={time.time() - total_start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
