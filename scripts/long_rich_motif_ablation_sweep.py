#!/usr/bin/env python3
"""Run a progress-logged ablation sweep over the rich neighborhood-basis motifs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import (
    neighborhood_basis_residual_benchmark,
    parity_threshold_from_residual_rows,
    rich_neighborhood_basis_ablation_sets,
    rich_neighborhood_basis_feature_names,
)


BASIS_SIZES = (3, 4, 5, 6, 7, 8)


def summarize_family(residual_rows, rule_family: str) -> str:
    family_rows = [row for row in residual_rows if row.rule_family == rule_family]
    parity_row, prethreshold_row = parity_threshold_from_residual_rows(family_rows)
    if parity_row is None:
        return (
            f"{rule_family}: no parity | "
            f"best_pre={prethreshold_row.basis_feature_subset}/"
            f"{prethreshold_row.basis_minus_pocket_mean:+.2f}/"
            f"{prethreshold_row.basis_minus_pocket_worst:+.2f}"
        )
    return (
        f"{rule_family}: parity@{parity_row.basis_size} "
        f"via {parity_row.basis_feature_subset} | "
        f"pre_gap={prethreshold_row.basis_minus_pocket_mean:+.2f}/"
        f"{prethreshold_row.basis_minus_pocket_worst:+.2f}"
    )


def main() -> None:
    all_rich_features = rich_neighborhood_basis_feature_names()
    started = datetime.now().isoformat(timespec="seconds")
    print(f"rich motif ablation sweep started {started}", flush=True)
    print("basis_sizes:", BASIS_SIZES, flush=True)
    total_start = time.time()
    for ablation_name, removed_features in rich_neighborhood_basis_ablation_sets():
        feature_names = tuple(
            feature for feature in all_rich_features if feature not in set(removed_features)
        )
        ablation_start = time.time()
        print(
            f"\n=== {ablation_name} | removed={removed_features or ('-',)} | "
            f"feature_count={len(feature_names)} ===",
            flush=True,
        )
        residual_rows = neighborhood_basis_residual_benchmark(
            geometry_variant_limit=5,
            procedural_variant_limit=3,
            basis_sizes=BASIS_SIZES,
            basis_feature_names=feature_names,
        )
        print(f"elapsed={time.time() - ablation_start:.1f}s", flush=True)
        for rule_family in ("compact", "extended"):
            print(summarize_family(residual_rows, rule_family), flush=True)
    finished = datetime.now().isoformat(timespec="seconds")
    print(f"\ncompleted {finished} total_elapsed={time.time() - total_start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
