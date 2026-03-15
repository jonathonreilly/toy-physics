#!/usr/bin/env python3
"""Run a progress-logged residual pocket-vs-basis sweep on the stronger ensemble."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from toy_event_physics import neighborhood_basis_benchmark


BASIS_SIZES = (3, 4, 5, 6, 7, 8)


def best_rows(bench_rows, rule_family: str):
    family_rows = [row for row in bench_rows if row.rule_family == rule_family]
    pocket_row = max(
        (row for row in family_rows if row.candidate_name == "pocket"),
        key=lambda row: (
            row.generated_mean_accuracy,
            row.generated_worst_accuracy,
            row.model_family,
        ),
    )
    basis_row = max(
        (
            row
            for row in family_rows
            if row.candidate_name != "pocket"
            and "pocket_fraction" not in row.feature_subset
        ),
        key=lambda row: (
            row.generated_mean_accuracy,
            row.generated_worst_accuracy,
            row.candidate_name,
            row.feature_subset,
            row.model_family,
        ),
    )
    combo_row = max(
        (
            row
            for row in family_rows
            if row.candidate_name != "pocket"
            and "pocket_fraction" in row.feature_subset
        ),
        key=lambda row: (
            row.generated_mean_accuracy,
            row.generated_worst_accuracy,
            row.candidate_name,
            row.feature_subset,
            row.model_family,
        ),
    )
    return pocket_row, basis_row, combo_row


def summarize(rule_family: str, bench_rows) -> str:
    pocket_row, basis_row, combo_row = best_rows(bench_rows, rule_family)
    return (
        f"{rule_family}: "
        f"pocket={pocket_row.generated_mean_accuracy:.2f}/{pocket_row.generated_worst_accuracy:.2f} "
        f"| basis={basis_row.candidate_name}/{basis_row.feature_subset}/{basis_row.model_family}/"
        f"{basis_row.generated_mean_accuracy:.2f}/{basis_row.generated_worst_accuracy:.2f} "
        f"(delta={basis_row.generated_mean_accuracy - pocket_row.generated_mean_accuracy:+.2f}/"
        f"{basis_row.generated_worst_accuracy - pocket_row.generated_worst_accuracy:+.2f}) "
        f"| combo={combo_row.candidate_name}/{combo_row.feature_subset}/{combo_row.model_family}/"
        f"{combo_row.generated_mean_accuracy:.2f}/{combo_row.generated_worst_accuracy:.2f} "
        f"(delta_vs_basis={combo_row.generated_mean_accuracy - basis_row.generated_mean_accuracy:+.2f}/"
        f"{combo_row.generated_worst_accuracy - basis_row.generated_worst_accuracy:+.2f})"
    )


def main() -> None:
    started = datetime.now().isoformat(timespec="seconds")
    print(f"residual sweep started {started}", flush=True)
    print("basis_sizes:", BASIS_SIZES, flush=True)
    total_start = time.time()
    for basis_size in BASIS_SIZES:
        basis_start = time.time()
        print(f"\n=== basis_size={basis_size} ===", flush=True)
        _basis_rows, bench_rows = neighborhood_basis_benchmark(
            geometry_variant_limit=5,
            procedural_variant_limit=3,
            basis_size=basis_size,
        )
        print(f"elapsed={time.time() - basis_start:.1f}s", flush=True)
        for rule_family in ("compact", "extended"):
            print(summarize(rule_family, bench_rows), flush=True)
    finished = datetime.now().isoformat(timespec="seconds")
    print(f"\ncompleted {finished} total_elapsed={time.time() - total_start:.1f}s", flush=True)


if __name__ == "__main__":
    main()
