#!/usr/bin/env python3
"""Run a broader overnight sweep of the learned neighborhood-basis benchmark."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import neighborhood_basis_benchmark


CONFIGS = (
    (3, 1),
    (3, 2),
    (3, 3),
    (4, 1),
    (4, 2),
    (4, 3),
    (5, 1),
    (5, 2),
    (5, 3),
)


def summarize_family(bench_rows, basis_rows, rule_family: str) -> str:
    family_basis = [row for row in basis_rows if row.rule_family == rule_family]
    family_bench = [row for row in bench_rows if row.rule_family == rule_family]
    best = family_bench[0]
    pocket = next(
        row
        for row in family_bench
        if row.candidate_name == "pocket" and row.model_family == "ordinal-minmax-equal"
    )
    best_single = max(
        (
            row
            for row in family_bench
            if row.candidate_name in {"basis-1", "basis-2", "basis-3"}
        ),
        key=lambda row: (
            row.generated_mean_accuracy,
            row.generated_worst_accuracy,
            row.feature_subset,
        ),
    )
    basis_summary = ", ".join(
        f"{row.rank}:{row.feature_name}:{row.spread_score:.3f}"
        for row in family_basis
    )
    return (
        f"{rule_family}: basis=[{basis_summary}] | "
        f"best={best.candidate_name}/{best.feature_subset}/{best.model_family}/"
        f"{best.generated_mean_accuracy:.2f}/{best.generated_worst_accuracy:.2f} | "
        f"pocket={pocket.generated_mean_accuracy:.2f}/{pocket.generated_worst_accuracy:.2f} | "
        f"best_single={best_single.feature_subset}/{best_single.model_family}/"
        f"{best_single.generated_mean_accuracy:.2f}/{best_single.generated_worst_accuracy:.2f}"
    )


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"overnight neighborhood basis sweep started {started}", flush=True)
    print("configs:", CONFIGS, flush=True)
    total_start = time.time()

    for geometry_limit, procedural_limit in CONFIGS:
        config_start = time.time()
        print(
            f"\n=== geometry_variant_limit={geometry_limit} procedural_variant_limit={procedural_limit} ===",
            flush=True,
        )
        basis_rows, bench_rows = neighborhood_basis_benchmark(
            geometry_variant_limit=geometry_limit,
            procedural_variant_limit=procedural_limit,
        )
        elapsed = time.time() - config_start
        print(f"elapsed={elapsed:.1f}s", flush=True)
        for rule_family in ("compact", "extended"):
            print(summarize_family(bench_rows, basis_rows, rule_family), flush=True)

    total_elapsed = time.time() - total_start
    finished = datetime.now().isoformat(timespec="seconds")
    print(f"\ncompleted {finished} total_elapsed={total_elapsed:.1f}s", flush=True)


if __name__ == "__main__":
    main()
