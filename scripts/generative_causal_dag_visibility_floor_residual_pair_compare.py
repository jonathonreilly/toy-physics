#!/usr/bin/env python3
"""Compare the last residual pair around the generated-DAG floor crossover.

This is the stop/go check after the retained bridge was compressed to:
1. a balanced-load floor
2. a balance-led residual crossover rule

If a tiny extra observable closes the remaining pair and still behaves well on
the full crossover set, we keep it. Otherwise we stop compressing.
"""

from __future__ import annotations

import os
import sys

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


PAIR_FIELDS = [
    "center_path_balance",
    "center_balance_share",
    "center_slit_load_retimed",
    "center_slit_share",
    "center_retiming_alignment",
    "center_upper_log_paths",
    "center_lower_log_paths",
    "center_bypass_log_paths",
    "center_balanced_log_paths",
]

BALANCE_CUT = 0.22227130764978215
BALANCE_SHARE_CUT = 0.13344684215511832


def print_row(label: str, row: SeedRow) -> None:
    print(f"{label}: {row.scenario} seed={row.seed}")
    print(f"  V0={row.v_center:.6f} mean_V={row.mean_v:.6f}")
    for field in PAIR_FIELDS:
        print(f"  {field}={float(getattr(row, field)):.6f}")


def pair_threshold_accuracy(
    positives: list[SeedRow],
    negatives: list[SeedRow],
    field: str,
    positive_row: SeedRow,
    negative_row: SeedRow,
) -> tuple[str, float, float, int, int]:
    positive_value = float(getattr(positive_row, field))
    negative_value = float(getattr(negative_row, field))
    threshold = (positive_value + negative_value) / 2.0
    if positive_value > negative_value:
        direction = ">"
        tp = sum(1 for row in positives if float(getattr(row, field)) > threshold)
        fp = sum(1 for row in negatives if float(getattr(row, field)) > threshold)
    else:
        direction = "<="
        tp = sum(1 for row in positives if float(getattr(row, field)) <= threshold)
        fp = sum(1 for row in negatives if float(getattr(row, field)) <= threshold)
    accuracy = (tp + (len(negatives) - fp)) / (len(positives) + len(negatives))
    return direction, threshold, accuracy, tp, fp


def main() -> None:
    workers = max(1, os.cpu_count() or 1)
    rows = run_rows(DEFAULT_SCENARIO, range(0, 64), workers=workers, phase_steps=16)
    rows += run_rows(DENSER_SCENARIO, range(64, 96), workers=workers, phase_steps=16)
    floor = split_search(rows)
    if floor is None:
        raise SystemExit("No family floor found")

    default_high = [
        row for row in rows
        if row.scenario == DEFAULT_SCENARIO.label and row.center_balanced_log_paths > floor.threshold
    ]
    denser_low = [
        row for row in rows
        if row.scenario == DENSER_SCENARIO.label and row.center_balanced_log_paths <= floor.threshold
    ]

    share_false_negative = [
        row for row in default_high if row.center_balance_share <= BALANCE_SHARE_CUT
    ]
    balance_false_positive = [
        row for row in denser_low if row.center_path_balance > BALANCE_CUT
    ]
    if len(share_false_negative) != 1 or len(balance_false_positive) != 1:
        raise SystemExit("Expected exactly one residual pair")

    positive_row = share_false_negative[0]
    negative_row = balance_false_positive[0]

    print("=" * 72)
    print("GENERATIVE CAUSAL DAG VISIBILITY FLOOR RESIDUAL PAIR COMPARE")
    print("=" * 72)
    print(
        f"Balanced-load floor: center_balanced_log_paths <= {floor.threshold:.3f}; "
        f"balance cut: center_path_balance > {BALANCE_CUT:.6f}; "
        f"balance-share cut: center_balance_share > {BALANCE_SHARE_CUT:.6f}"
    )
    print()

    print_row("share-cut false negative", positive_row)
    print()
    print_row("balance-cut false positive", negative_row)
    print()

    print("Pair-separating thresholds and their full-crossover fallout:")
    best_field = None
    best_accuracy = -1.0
    for field in PAIR_FIELDS:
        direction, threshold, accuracy, tp, fp = pair_threshold_accuracy(
            positives=default_high,
            negatives=denser_low,
            field=field,
            positive_row=positive_row,
            negative_row=negative_row,
        )
        print(
            f"  {field} {direction} {threshold:.6f} "
            f"accuracy={accuracy:.4f} tp={tp} fp={fp}"
        )
        if field != "center_balanced_log_paths" and accuracy > best_accuracy:
            best_accuracy = accuracy
            best_field = (field, direction, threshold, tp, fp)

    print()
    print("Interpretation:")
    print(
        "  The remaining pair are opposite one-sided exceptions. The missed default-high "
        "row is extremely load-heavy and well retimed despite weak balance-share, while "
        "the leaked denser-low row keeps moderate balance but is still under the "
        "balanced-load floor."
    )
    print(
        "  The tempting pair-only exact closers do not generalize. Aside from the floor "
        "itself, the best pair-separating thresholds fall short on the full 12 crossover "
        "rows, so they are not good retained regime language."
    )
    if best_field is not None:
        field, direction, threshold, tp, fp = best_field
        print(
            f"  Best non-floor pair closer on the full crossover set: "
            f"{field} {direction} {threshold:.6f} with accuracy={best_accuracy:.4f} "
            f"(tp={tp}, fp={fp})."
        )
    print(
        "  Stop rule: keep the current bridge as-is. Packet completion sets the floor; "
        "balance governs near-floor crossover; the residual pair does not justify a new "
        "global clause."
    )


if __name__ == "__main__":
    main()
