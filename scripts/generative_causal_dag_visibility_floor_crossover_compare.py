#!/usr/bin/env python3
"""Explain what pushes generated-DAG rows across the balanced-load floor.

The retained bridge is now a two-branch packet regime, not a one-scalar hunt.
This script stays bounded: it looks only at the rows near the learned
balanced-load floor and asks which within-family observable explains why some
rows cross into the balanced-load-led branch while nearby rows do not.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_visibility_family_regime_compare import (
    DEFAULT_SCENARIO,
    DENSER_SCENARIO,
    split_search,
)
from scripts.generative_causal_dag_visibility_order_parameter_compare import (
    SeedRow,
    run_rows,
)


@dataclass(frozen=True)
class ResidualThreshold:
    name: str
    direction: str
    threshold: float
    accuracy: float
    tp: int
    fp: int
    fn: int


RESIDUAL_FIELDS = [
    "center_path_balance",
    "center_balance_share",
    "center_slit_load_retimed",
    "center_slit_share",
    "center_retiming_alignment",
]


def row_mean(rows: list[SeedRow], field: str) -> float:
    return statistics.fmean(float(getattr(row, field)) for row in rows)


def scenario_counts(rows: list[SeedRow]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.scenario] = counts.get(row.scenario, 0) + 1
    return counts


def best_threshold(
    positives: list[SeedRow],
    negatives: list[SeedRow],
    field: str,
) -> ResidualThreshold | None:
    values = sorted({float(getattr(row, field)) for row in positives + negatives})
    best: ResidualThreshold | None = None
    for left, right in zip(values, values[1:]):
        threshold = (left + right) / 2.0
        for direction in (">", "<="):
            tp = sum(
                1
                for row in positives
                if (
                    float(getattr(row, field)) > threshold
                    if direction == ">"
                    else float(getattr(row, field)) <= threshold
                )
            )
            fp = sum(
                1
                for row in negatives
                if (
                    float(getattr(row, field)) > threshold
                    if direction == ">"
                    else float(getattr(row, field)) <= threshold
                )
            )
            fn = len(positives) - tp
            tn = len(negatives) - fp
            accuracy = (tp + tn) / (len(positives) + len(negatives))
            candidate = ResidualThreshold(
                name=field,
                direction=direction,
                threshold=threshold,
                accuracy=accuracy,
                tp=tp,
                fp=fp,
                fn=fn,
            )
            if best is None or candidate.accuracy > best.accuracy:
                best = candidate
    return best


def format_rule(result: ResidualThreshold) -> str:
    return f"{result.name} {result.direction} {result.threshold:.6f}"


def main() -> None:
    workers = max(1, os.cpu_count() or 1)
    default_rows = run_rows(DEFAULT_SCENARIO, range(0, 64), workers=workers, phase_steps=16)
    denser_rows = run_rows(DENSER_SCENARIO, range(64, 96), workers=workers, phase_steps=16)
    rows = default_rows + denser_rows
    rows.sort(key=lambda row: (row.scenario, row.seed))

    split = split_search(rows)
    if split is None:
        raise SystemExit("No valid family split found")
    floor = split.threshold

    low_rows = [row for row in rows if row.center_balanced_log_paths <= floor]
    high_rows = [row for row in rows if row.center_balanced_log_paths > floor]
    default_high = [row for row in high_rows if row.scenario == DEFAULT_SCENARIO.label]
    denser_low = [row for row in low_rows if row.scenario == DENSER_SCENARIO.label]
    default_low_majority = [row for row in low_rows if row.scenario == DEFAULT_SCENARIO.label]
    denser_high_majority = [row for row in high_rows if row.scenario == DENSER_SCENARIO.label]

    residual_results = [
        best_threshold(default_high, denser_low, field)
        for field in RESIDUAL_FIELDS
    ]
    residual_results = [result for result in residual_results if result is not None]
    residual_results.sort(key=lambda result: result.accuracy, reverse=True)
    best_residual = residual_results[0]

    print("=" * 72)
    print("GENERATIVE CAUSAL DAG VISIBILITY FLOOR CROSSOVER COMPARE")
    print("=" * 72)
    print(
        f"Balanced-load floor: center_balanced_log_paths <= {floor:.3f} "
        f"(low={len(low_rows)}, high={len(high_rows)})"
    )
    print(
        "Crossover rows: "
        f"default-high={len(default_high)}, denser-low={len(denser_low)}"
    )
    print()

    print("Branch composition:")
    print(f"  low branch scenarios={scenario_counts(low_rows)}")
    print(f"  high branch scenarios={scenario_counts(high_rows)}")
    print()

    print("Group means on the retained packet-family observables:")
    for label, group in (
        ("default-low majority", default_low_majority),
        ("default-high crossover", default_high),
        ("denser-low crossover", denser_low),
        ("denser-high majority", denser_high_majority),
    ):
        print(f"  {label}:")
        print(
            f"    center_path_balance={row_mean(group, 'center_path_balance'):.4f} "
            f"center_balance_share={row_mean(group, 'center_balance_share'):.4f}"
        )
        print(
            f"    center_slit_load_retimed={row_mean(group, 'center_slit_load_retimed'):.4f} "
            f"center_balanced_log_paths={row_mean(group, 'center_balanced_log_paths'):.4f}"
        )
        print(
            f"    center_slit_share={row_mean(group, 'center_slit_share'):.4f} "
            f"center_retiming_alignment={row_mean(group, 'center_retiming_alignment'):.4f}"
        )

    print()
    print("Residual crossover thresholds (default-high positive vs denser-low negative):")
    for result in residual_results:
        print(
            f"  {format_rule(result)} "
            f"accuracy={result.accuracy:.4f} tp={result.tp} fp={result.fp} fn={result.fn}"
        )

    print()
    print("Best residual discriminator:")
    print(
        f"  {format_rule(best_residual)} "
        f"accuracy={best_residual.accuracy:.4f} tp={best_residual.tp} "
        f"fp={best_residual.fp} fn={best_residual.fn}"
    )
    print()

    print("Interpretation:")
    print(
        "  The rows near the balanced-load floor are not mainly split by retimed slit "
        "load. The denser low-side crossover rows already carry slightly more retimed "
        "slit load on average than the default high-side crossover rows."
    )
    print(
        "  What changes is how jointly that load is shared across the two center slit "
        "packets. The cleanest residual cut is balance-share, with plain path balance "
        "essentially tied behind it."
    )
    print(
        "  So the current bridge is: packet completion / closure-load sets the floor, "
        "and bridge-balance-style sharing decides which near-floor rows actually cross "
        "into the balanced-load-led branch."
    )


if __name__ == "__main__":
    main()
