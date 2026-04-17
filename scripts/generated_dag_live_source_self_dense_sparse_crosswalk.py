#!/usr/bin/env python3
"""Crosswalk the dense/sparse self live-last6 pair against held-out self rows.

This is the config-local continuation of the live self regime compare. The
dominant `self` branch did not reduce to one strong shared law, but the two
discovery configs (`dense-25`, `sparse-25`) still looked related rather than
completely separate.

This script asks three bounded questions:

1. how well do the dense-local and sparse-local rules transfer to each other?
2. what is the smallest shared dense+sparse rule family?
3. does that shared family survive onto the held-out self rows (`long-30`,
   `wide-15`)?
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
import os
import statistics
import sys
from typing import Iterable

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


FOCAL_CONFIGS = ("dense-25", "sparse-25")
HOLDOUT_CONFIGS = ("long-30", "wide-15")


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
        f"reuse={_mean(row.last6_reuse_share for row in rows):.4f} "
        f"packet_side_gap={_mean(row.extra_packet_side_gap for row in rows):.4f}"
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

    dense_rows = [row for row in self_rows if row.config == "dense-25"]
    sparse_rows = [row for row in self_rows if row.config == "sparse-25"]
    focal_rows = [row for row in self_rows if row.config in FOCAL_CONFIGS]
    holdout_rows = [row for row in self_rows if row.config in HOLDOUT_CONFIGS]

    dense_rule = _best_config_local_rule(dense_rows)
    sparse_rule = _best_config_local_rule(sparse_rows)
    shared_source_rule = _best_single_rule(focal_rows, holdout_rows, SOURCE_FEATURES)
    shared_packet_rule = _best_single_rule(focal_rows, holdout_rows, PACKET_FEATURES)
    shared_or_rule = _best_or_rule(focal_rows, holdout_rows)
    config_source_rule = _best_single_rule(
        focal_rows,
        focal_rows,
        SOURCE_FEATURES,
    )
    config_packet_rule = _best_single_rule(
        focal_rows,
        focal_rows,
        PACKET_FEATURES,
    )

    print("=" * 80)
    print("GENERATED DAG LIVE SOURCE SELF DENSE/SPARSE CROSSWALK")
    print("=" * 80)
    print(
        f"rows={len(self_rows)} self rows total; focal={len(focal_rows)} "
        f"holdout={len(holdout_rows)} neighbor_radius={args.neighbor_radius:.1f} "
        f"coupling={args.coupling:.3f}"
    )
    print()
    print(_render_group("dense-25", dense_rows))
    print(_render_group("sparse-25", sparse_rows))
    print(_render_group("long-30", [row for row in self_rows if row.config == "long-30"]))
    print(_render_group("wide-15", [row for row in self_rows if row.config == "wide-15"]))
    print()
    print("Best config-local rules:")
    print(f"  dense-25:  {dense_rule.render().replace('discovery=', 'accuracy=').replace(', holdout=', '; holdout=')}")
    print(f"  sparse-25: {sparse_rule.render().replace('discovery=', 'accuracy=').replace(', holdout=', '; holdout=')}")
    print()
    print("Cross-transfer of config-local rules:")
    print(
        f"  dense rule on dense:  {_apply_single(dense_rows, dense_rule):.4f} | "
        f"on sparse: {_apply_single(sparse_rows, dense_rule):.4f}"
    )
    print(
        f"  sparse rule on sparse: {_apply_single(sparse_rows, sparse_rule):.4f} | "
        f"on dense: {_apply_single(dense_rows, sparse_rule):.4f}"
    )
    print()
    print("Best dense+sparse config-separating rules:")
    print(f"  source-family: {config_source_rule.render().replace('discovery=', 'pair_accuracy=').replace(', holdout=', '; holdout=')}")
    print(f"  packet-family: {config_packet_rule.render().replace('discovery=', 'pair_accuracy=').replace(', holdout=', '; holdout=')}")
    print()
    print("Best shared dense+sparse retained-branch rules:")
    print(f"  source-family: {shared_source_rule.render()}")
    print(f"  packet-family: {shared_packet_rule.render()}")
    print(f"  source-or-packet: {shared_or_rule.render()}")
    print()
    print("Held-out transfer of shared dense+sparse rules:")
    print(f"  source-family on holdout: {_apply_single(holdout_rows, shared_source_rule):.4f}")
    print(f"  packet-family on holdout: {_apply_single(holdout_rows, shared_packet_rule):.4f}")
    print(f"  source-or-packet on holdout: {_apply_or(holdout_rows, shared_or_rule):.4f}")
    print()
    print("Interpretation:")
    print(
        "  This crosswalk asks whether dense-25 and sparse-25 should be treated as "
        "separate self-branch mechanisms or as two weak views of one shared family. "
        "If their local rules cross-transfer and the dense+sparse config label itself "
        "is hard to recover, then the pair is better read as one weak source-topology "
        "plus packet-landing family whose real failure is transfer to long-30/wide-15."
    )


if __name__ == "__main__":
    main()
