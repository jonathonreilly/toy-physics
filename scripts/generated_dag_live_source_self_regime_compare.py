#!/usr/bin/env python3
"""Compare shared-vs-config-local regime language on the live self branch.

This is the direct continuation of the live-window geometry compare. The pooled
result said the broad live `last6` branch is real, but the dominant `self`
slice still did not collapse under one strong scalar. This script asks a tighter
question:

Do the `self` rows reduce to a small two-subbranch regime built from
source-topology plus packet-landing observables, or does the current branch stay
config-local?
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import argparse
import itertools
import os
import statistics
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_live_source_window_geometry_compare import (  # noqa: E402
    LiveWindowRow,
    run_rows,
)
from scripts.generated_dag_packet_tracking_bridge_compare import (  # noqa: E402
    DISCOVERY_CONFIGS,
    HOLDOUT_CONFIGS,
)


SOURCE_FEATURES = [
    "last6_union_size",
    "last6_reuse_share",
    "last6_core_share",
    "last6_corridor_share",
    "last6_centroid_drift",
    "last6_source_signed_side",
    "last6_source_x_lead",
]

PACKET_FEATURES = [
    "extra_support_share",
    "extra_support_forward_share",
    "extra_support_corridor_share",
    "extra_field_mean_on_packet",
    "extra_field_range_on_packet",
    "extra_packet_side_gap",
    "extra_fringe_side_gap",
    "extra_forward_side_gap",
]


@dataclass(frozen=True)
class SingleRule:
    feature: str
    comparator: str
    threshold: float
    discovery_accuracy: float
    holdout_accuracy: float

    def render(self) -> str:
        return (
            f"{self.feature} {self.comparator} {self.threshold:.4f} "
            f"(discovery={self.discovery_accuracy:.4f}, holdout={self.holdout_accuracy:.4f})"
        )


@dataclass(frozen=True)
class OrRule:
    source_feature: str
    source_comparator: str
    source_threshold: float
    packet_feature: str
    packet_comparator: str
    packet_threshold: float
    discovery_accuracy: float
    holdout_accuracy: float

    def render(self) -> str:
        return (
            f"{self.source_feature} {self.source_comparator} {self.source_threshold:.4f} or "
            f"{self.packet_feature} {self.packet_comparator} {self.packet_threshold:.4f} "
            f"(discovery={self.discovery_accuracy:.4f}, holdout={self.holdout_accuracy:.4f})"
        )


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


def _best_single_rule(
    discovery_rows: list[LiveWindowRow],
    holdout_rows: list[LiveWindowRow],
    features: list[str],
) -> SingleRule:
    best: SingleRule | None = None
    for feature in features:
        values = sorted(set(float(getattr(row, feature)) for row in discovery_rows))
        for comparator in (">=", "<="):
            for threshold in values:
                discovery_pred = _predictions(discovery_rows, feature, comparator, threshold)
                holdout_pred = _predictions(holdout_rows, feature, comparator, threshold)
                candidate = SingleRule(
                    feature=feature,
                    comparator=comparator,
                    threshold=threshold,
                    discovery_accuracy=_accuracy(discovery_rows, discovery_pred),
                    holdout_accuracy=_accuracy(holdout_rows, holdout_pred),
                )
                if best is None or (
                    candidate.discovery_accuracy,
                    candidate.holdout_accuracy,
                    candidate.feature,
                    -candidate.threshold,
                ) > (
                    best.discovery_accuracy,
                    best.holdout_accuracy,
                    best.feature,
                    -best.threshold,
                ):
                    best = candidate
    assert best is not None
    return best


def _best_or_rule(
    discovery_rows: list[LiveWindowRow],
    holdout_rows: list[LiveWindowRow],
) -> OrRule:
    best: OrRule | None = None
    for source_feature in SOURCE_FEATURES:
        source_values = sorted(
            set(float(getattr(row, source_feature)) for row in discovery_rows)
        )
        for source_comparator in (">=", "<="):
            for source_threshold in source_values:
                source_discovery = _predictions(
                    discovery_rows,
                    source_feature,
                    source_comparator,
                    source_threshold,
                )
                source_holdout = _predictions(
                    holdout_rows,
                    source_feature,
                    source_comparator,
                    source_threshold,
                )
                for packet_feature in PACKET_FEATURES:
                    packet_values = sorted(
                        set(float(getattr(row, packet_feature)) for row in discovery_rows)
                    )
                    for packet_comparator in (">=", "<="):
                        for packet_threshold in packet_values:
                            packet_discovery = _predictions(
                                discovery_rows,
                                packet_feature,
                                packet_comparator,
                                packet_threshold,
                            )
                            packet_holdout = _predictions(
                                holdout_rows,
                                packet_feature,
                                packet_comparator,
                                packet_threshold,
                            )
                            discovery_pred = [
                                left or right
                                for left, right in zip(source_discovery, packet_discovery)
                            ]
                            holdout_pred = [
                                left or right
                                for left, right in zip(source_holdout, packet_holdout)
                            ]
                            candidate = OrRule(
                                source_feature=source_feature,
                                source_comparator=source_comparator,
                                source_threshold=source_threshold,
                                packet_feature=packet_feature,
                                packet_comparator=packet_comparator,
                                packet_threshold=packet_threshold,
                                discovery_accuracy=_accuracy(discovery_rows, discovery_pred),
                                holdout_accuracy=_accuracy(holdout_rows, holdout_pred),
                            )
                            if best is None or (
                                candidate.discovery_accuracy,
                                candidate.holdout_accuracy,
                                candidate.source_feature,
                                -candidate.source_threshold,
                                candidate.packet_feature,
                                -candidate.packet_threshold,
                            ) > (
                                best.discovery_accuracy,
                                best.holdout_accuracy,
                                best.source_feature,
                                -best.source_threshold,
                                best.packet_feature,
                                -best.packet_threshold,
                            ):
                                best = candidate
    assert best is not None
    return best


def _best_config_local_rule(rows: list[LiveWindowRow]) -> SingleRule:
    return _best_single_rule(rows, rows, SOURCE_FEATURES + PACKET_FEATURES)


def _render_group(rows: list[LiveWindowRow], label: str, predicate) -> str:
    subset = [row for row in rows if predicate(row)]
    return (
        f"{label}: total={len(subset)} "
        f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
        f"mean_delta={_mean(row.delta_shift for row in subset):.4f} "
        f"source_signed_side={_mean(row.last6_source_signed_side for row in subset):.4f} "
        f"extra_packet_side_gap={_mean(row.extra_packet_side_gap for row in subset):.4f}"
    )


def _render_config_breakdown(rows: list[LiveWindowRow]) -> list[str]:
    lines = ["Config breakdown:"]
    buckets: dict[str, list[LiveWindowRow]] = defaultdict(list)
    for row in rows:
        buckets[row.config].append(row)
    for config in sorted(buckets):
        subset = buckets[config]
        retained = sum(row.retained_last6 for row in subset)
        lines.append(
            "  "
            f"{config}: total={len(subset)} retained={retained}/{len(subset)} "
            f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
            f"mean_delta={_mean(row.delta_shift for row in subset):.4f}"
        )
    return lines


def _render_config_local_rules(rows: list[LiveWindowRow]) -> list[str]:
    lines = ["Best config-local single-threshold rules:"]
    buckets: dict[str, list[LiveWindowRow]] = defaultdict(list)
    for row in rows:
        buckets[row.config].append(row)
    for config in sorted(buckets):
        best = _best_config_local_rule(buckets[config])
        lines.append(f"  {config}: {best.render().replace('discovery=', 'accuracy=').replace(', holdout=', '; holdout=')}")
    return lines


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

    rows = [
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
    discovery_rows = [row for row in rows if row.config in DISCOVERY_CONFIGS]
    holdout_rows = [row for row in rows if row.config in HOLDOUT_CONFIGS]

    best_source = _best_single_rule(discovery_rows, holdout_rows, SOURCE_FEATURES)
    best_packet = _best_single_rule(discovery_rows, holdout_rows, PACKET_FEATURES)
    best_or = _best_or_rule(discovery_rows, holdout_rows)

    print("=" * 80)
    print("GENERATED DAG LIVE SOURCE SELF REGIME COMPARE")
    print("=" * 80)
    print(
        f"rows={len(rows)} mover_rule=self neighbor_radius={args.neighbor_radius:.1f} "
        f"coupling={args.coupling:.3f}"
    )
    print(
        f"Discovery configs: {sorted(DISCOVERY_CONFIGS)}; "
        f"holdout configs: {sorted(HOLDOUT_CONFIGS)}"
    )
    print()
    print(_render_group(rows, "retained_last6", lambda row: row.retained_last6))
    print(_render_group(rows, "nonretained_last6", lambda row: not row.retained_last6))
    print()
    for line in _render_config_breakdown(rows):
        print(line)
    print()
    print("Best source-topology single rule:")
    print(f"  {best_source.render()}")
    print()
    print("Best packet-landing single rule:")
    print(f"  {best_packet.render()}")
    print()
    print("Best source-topology OR packet-landing rule:")
    print(f"  {best_or.render()}")
    print()
    for line in _render_config_local_rules(rows):
        print(line)
    print()
    print("Interpretation:")
    print(
        "  This compare tests whether the dominant self-rule share of the live "
        "`last6` branch reduces to a small two-subbranch regime, or whether the "
        "current closure is still config-local. The source family stands for broad "
        "late-window topology / occupancy, while the packet family stands for where "
        "the added late support actually lands on the tracked packet."
    )


if __name__ == "__main__":
    main()
