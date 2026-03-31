#!/usr/bin/env python3
"""Crosswalk the held-out long/wide self pair against dense/sparse.

This mirrors the dense/sparse self crosswalk. The previous step showed that the
weak dense/sparse family does not transfer cleanly to the held-out self rows.
The next bounded question is the reverse:

1. do `long-30` and `wide-15` form one weak shared self family?
2. if so, does that family transfer back to the dense/sparse pair?
3. or are the held-out self rows already split into separate local mechanisms?
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Iterable
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_live_source_self_regime_compare import (  # noqa: E402
    PACKET_FEATURES,
    SOURCE_FEATURES,
    OrRule,
    SingleRule,
    _best_or_rule,
    _best_single_rule,
)
from scripts.generated_dag_live_source_window_geometry_compare import (  # noqa: E402
    LiveWindowRow,
    run_rows,
)


FOCAL_CONFIGS = ("long-30", "wide-15")
CONTRAST_CONFIGS = ("dense-25", "sparse-25")


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _predictions(
    rows: list[LiveWindowRow],
    feature: str,
    comparator: str,
    threshold: float,
) -> list[bool]:
    values = [float(getattr(row, feature)) for row in rows]
    if comparator == ">=":
        return [value >= threshold for value in values]
    return [value <= threshold for value in values]


def _accuracy(rows: list[LiveWindowRow], predictions: list[bool]) -> float:
    truth = [row.retained_last6 for row in rows]
    return sum(pred == target for pred, target in zip(predictions, truth)) / len(rows)


def _apply_single(rows: list[LiveWindowRow], rule: SingleRule) -> float:
    return _accuracy(rows, _predictions(rows, rule.feature, rule.comparator, rule.threshold))


def _apply_or(rows: list[LiveWindowRow], rule: OrRule) -> float:
    left = _predictions(rows, rule.source_feature, rule.source_comparator, rule.source_threshold)
    right = _predictions(rows, rule.packet_feature, rule.packet_comparator, rule.packet_threshold)
    return _accuracy(rows, [a or b for a, b in zip(left, right)])


def _best_config_local_rule(rows: list[LiveWindowRow]) -> SingleRule:
    return _best_single_rule(rows, rows, SOURCE_FEATURES + PACKET_FEATURES)


def _render_group(label: str, rows: list[LiveWindowRow]) -> str:
    retained = sum(row.retained_last6 for row in rows)
    return (
        f"{label}: total={len(rows)} retained={retained}/{len(rows)} "
        f"mean_last6_shift={_mean(row.last6_shift for row in rows):.4f} "
        f"mean_delta={_mean(row.delta_shift for row in rows):.4f} "
        f"union_size={_mean(row.last6_union_size for row in rows):.2f} "
        f"fringe_gap={_mean(row.extra_fringe_side_gap for row in rows):.4f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--neighbor-radius", type=float, default=2.5)
    parser.add_argument("--coupling", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    self_rows = [
        row
        for row in run_rows(
            seeds=range(args.seed_start, args.seed_start + args.seed_count),
            workers=max(1, args.workers),
            steps=args.steps,
            source_steps=args.source_steps,
            coupling=args.coupling,
            neighbor_radius=args.neighbor_radius,
            source_offsets=[-3.0, 3.0],
        )
        if row.mover_rule == "self"
    ]

    long_rows = [row for row in self_rows if row.config == "long-30"]
    wide_rows = [row for row in self_rows if row.config == "wide-15"]
    focal_rows = [row for row in self_rows if row.config in FOCAL_CONFIGS]
    contrast_rows = [row for row in self_rows if row.config in CONTRAST_CONFIGS]

    long_rule = _best_config_local_rule(long_rows)
    wide_rule = _best_config_local_rule(wide_rows)
    shared_source_rule = _best_single_rule(focal_rows, contrast_rows, SOURCE_FEATURES)
    shared_packet_rule = _best_single_rule(focal_rows, contrast_rows, PACKET_FEATURES)
    shared_or_rule = _best_or_rule(focal_rows, contrast_rows)
    config_source_rule = _best_single_rule(focal_rows, focal_rows, SOURCE_FEATURES)
    config_packet_rule = _best_single_rule(focal_rows, focal_rows, PACKET_FEATURES)

    print("=" * 80)
    print("GENERATED DAG LIVE SOURCE SELF HOLDOUT CROSSWALK")
    print("=" * 80)
    print(
        f"rows={len(self_rows)} self rows total; focal={len(focal_rows)} contrast={len(contrast_rows)} "
        f"neighbor_radius={args.neighbor_radius:.1f} coupling={args.coupling:.3f}"
    )
    print()
    print(_render_group("long-30", long_rows))
    print(_render_group("wide-15", wide_rows))
    print(_render_group("dense-25", [row for row in self_rows if row.config == "dense-25"]))
    print(_render_group("sparse-25", [row for row in self_rows if row.config == "sparse-25"]))
    print()
    print("Best config-local rules:")
    print(f"  long-30: {long_rule.render().replace('discovery=', 'accuracy=').replace(', holdout=', '; holdout=')}")
    print(f"  wide-15: {wide_rule.render().replace('discovery=', 'accuracy=').replace(', holdout=', '; holdout=')}")
    print()
    print("Cross-transfer of config-local rules:")
    print(
        f"  long rule on long: {_apply_single(long_rows, long_rule):.4f} | "
        f"on wide: {_apply_single(wide_rows, long_rule):.4f}"
    )
    print(
        f"  wide rule on wide: {_apply_single(wide_rows, wide_rule):.4f} | "
        f"on long: {_apply_single(long_rows, wide_rule):.4f}"
    )
    print()
    print("Best long+wide config-separating rules:")
    print(f"  source-family: {config_source_rule.render().replace('discovery=', 'pair_accuracy=').replace(', holdout=', '; holdout=')}")
    print(f"  packet-family: {config_packet_rule.render().replace('discovery=', 'pair_accuracy=').replace(', holdout=', '; holdout=')}")
    print()
    print("Best shared long+wide retained-branch rules:")
    print(f"  source-family: {shared_source_rule.render()}")
    print(f"  packet-family: {shared_packet_rule.render()}")
    print(f"  source-or-packet: {shared_or_rule.render()}")
    print()
    print("Transfer of shared long+wide rules back to dense+sparse:")
    print(f"  source-family on contrast: {_apply_single(contrast_rows, shared_source_rule):.4f}")
    print(f"  packet-family on contrast: {_apply_single(contrast_rows, shared_packet_rule):.4f}")
    print(f"  source-or-packet on contrast: {_apply_or(contrast_rows, shared_or_rule):.4f}")
    print()
    print("Interpretation:")
    print(
        "  This crosswalk asks whether the held-out self pair should be treated as "
        "one shared family whose real difference from dense/sparse is transfer, or "
        "as two separate held-out local mechanisms. If the long and wide rules "
        "cross-transfer well and the pair label is hard to recover, then the right "
        "read is one weak held-out family rather than two distinct closures."
    )


if __name__ == "__main__":
    main()
