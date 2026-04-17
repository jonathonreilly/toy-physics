#!/usr/bin/env python3
"""Compare the extra late support that flips `last3_union` steering.

The retained source footprint is now `last3_union`, while `last6_union`
reliably flips the mean steering sign back to away-shift. This bounded compare
keeps only rows where `last3_union` already steers toward the source, then asks
which observables of the added `last4-6` support predict whether `last6_union`
still stays toward-source or flips back away.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import itertools
import math
import multiprocessing as mp
import os
import statistics
import sys
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_field_coupled_mover_probe import (  # noqa: E402
    evolve_gradient_coupled,
)
from scripts.generated_dag_packet_tracking_bridge_compare import (  # noqa: E402
    CANONICAL_CONFIGS,
    CANONICAL_RULES,
    DISCOVERY_CONFIGS,
    HOLDOUT_CONFIGS,
    GraphConfig,
    RuleSpec,
    SEED_POSITIONS,
    _classify_outcome,
)
from scripts.generated_dag_pattern_mobility import (  # noqa: E402
    build_spatial_neighbors,
    evolve_on_graph,
)
from scripts.generated_dag_pattern_sourced_field_bias_compare import (  # noqa: E402
    _field_bias_metrics,
)
from scripts.generated_dag_pattern_sourced_mover_probe import (  # noqa: E402
    SOURCE_RULE,
    _signed_shift_at_shared_x,
    _union_last_steps,
    choose_seed_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


FEATURE_NAMES = [
    "extra_support_size",
    "extra_support_share",
    "extra_support_signed_side",
    "extra_support_forward_share",
    "extra_support_corridor_share",
    "extra_support_radius",
    "extra_field_mean_on_packet",
    "extra_field_range_on_packet",
    "extra_packet_side_gap",
    "extra_fringe_side_gap",
    "extra_forward_side_gap",
    "extra_fringe_forward_gap",
]

PAIR_FEATURES = [
    "extra_support_share",
    "extra_support_corridor_share",
    "extra_support_radius",
    "extra_fringe_side_gap",
    "extra_forward_side_gap",
    "extra_field_mean_on_packet",
]


@dataclass(frozen=True)
class FlipRow:
    config: str
    graph_seed: int
    mover_rule: str
    source_offset_y: float
    last3_shift: float
    last6_shift: float
    flipped: bool
    extra_support_size: float
    extra_support_share: float
    extra_support_signed_side: float
    extra_support_forward_share: float
    extra_support_corridor_share: float
    extra_support_radius: float
    extra_field_mean_on_packet: float
    extra_field_range_on_packet: float
    extra_packet_side_gap: float
    extra_fringe_side_gap: float
    extra_forward_side_gap: float
    extra_fringe_forward_gap: float


@dataclass(frozen=True)
class ThresholdRule:
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
class TwoFeatureRule:
    first_feature: str
    first_comparator: str
    first_threshold: float
    second_feature: str
    second_comparator: str
    second_threshold: float
    discovery_accuracy: float
    holdout_accuracy: float

    def render(self) -> str:
        return (
            f"{self.first_feature} {self.first_comparator} {self.first_threshold:.4f} and "
            f"{self.second_feature} {self.second_comparator} {self.second_threshold:.4f} "
            f"(discovery={self.discovery_accuracy:.4f}, holdout={self.holdout_accuracy:.4f})"
        )


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _centroid(
    positions: list[tuple[float, float]],
    state: frozenset[int],
) -> tuple[float, float]:
    if not state:
        return (0.0, 0.0)
    xs = [positions[idx][0] for idx in state]
    ys = [positions[idx][1] for idx in state]
    return (sum(xs) / len(xs), sum(ys) / len(ys))


def _radius(
    positions: list[tuple[float, float]],
    state: frozenset[int],
    center: tuple[float, float],
) -> float:
    if not state:
        return 0.0
    return max(math.dist(positions[idx], center) for idx in state)


def _run_coupled_shift(
    positions: list[tuple[float, float]],
    neighbors: dict[int, list[int]],
    mover_seed: frozenset[int],
    mover_rule: RuleSpec,
    field: dict[int, float],
    coupling: float,
    steps: int,
    free_live: list[tuple[int, frozenset[int] | None, tuple[float, float] | None, float | None]],
    side_sign: float,
) -> float:
    coupled_history = evolve_gradient_coupled(
        neighbors=neighbors,
        seed=mover_seed,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        field=field,
        coupling=coupling,
        steps=steps,
    )
    _, _, _, _, _, coupled_tracked = _classify_outcome(
        positions,
        neighbors,
        coupled_history,
    )
    coupled_live = [entry for entry in coupled_tracked if entry[1] is not None]
    if not coupled_live:
        return float("nan")
    return _signed_shift_at_shared_x(free_live, coupled_live, side_sign)


def _threshold_predictions(
    rows: list[FlipRow],
    feature: str,
    comparator: str,
    threshold: float,
) -> list[bool]:
    values = [float(getattr(row, feature)) for row in rows]
    if comparator == ">=":
        return [value >= threshold for value in values]
    return [value <= threshold for value in values]


def _accuracy(rows: list[FlipRow], predictions: list[bool]) -> float:
    truth = [row.flipped for row in rows]
    return sum(pred == target for pred, target in zip(predictions, truth)) / len(rows)


def _top_single_rules(
    discovery_rows: list[FlipRow],
    holdout_rows: list[FlipRow],
    top_n: int = 5,
) -> list[ThresholdRule]:
    candidates: list[ThresholdRule] = []
    for feature in FEATURE_NAMES:
        values = sorted(set(float(getattr(row, feature)) for row in discovery_rows))
        for comparator in (">=", "<="):
            for threshold in values:
                discovery_pred = _threshold_predictions(
                    discovery_rows,
                    feature,
                    comparator,
                    threshold,
                )
                holdout_pred = _threshold_predictions(
                    holdout_rows,
                    feature,
                    comparator,
                    threshold,
                )
                candidates.append(
                    ThresholdRule(
                        feature=feature,
                        comparator=comparator,
                        threshold=threshold,
                        discovery_accuracy=_accuracy(discovery_rows, discovery_pred),
                        holdout_accuracy=_accuracy(holdout_rows, holdout_pred),
                    )
                )
    candidates.sort(
        key=lambda rule: (
            rule.discovery_accuracy,
            rule.holdout_accuracy,
            rule.feature,
            -rule.threshold,
        ),
        reverse=True,
    )
    unique: list[ThresholdRule] = []
    seen: set[tuple[str, str, float]] = set()
    for candidate in candidates:
        key = (candidate.feature, candidate.comparator, round(candidate.threshold, 4))
        if key in seen:
            continue
        seen.add(key)
        unique.append(candidate)
        if len(unique) >= top_n:
            break
    return unique


def _best_two_feature_rule(
    discovery_rows: list[FlipRow],
    holdout_rows: list[FlipRow],
) -> TwoFeatureRule:
    best: TwoFeatureRule | None = None
    for first_feature, second_feature in itertools.combinations(PAIR_FEATURES, 2):
        first_values = sorted(set(float(getattr(row, first_feature)) for row in discovery_rows))
        second_values = sorted(set(float(getattr(row, second_feature)) for row in discovery_rows))
        for first_comparator in (">=", "<="):
            for second_comparator in (">=", "<="):
                for first_threshold in first_values:
                    first_discovery = _threshold_predictions(
                        discovery_rows,
                        first_feature,
                        first_comparator,
                        first_threshold,
                    )
                    first_holdout = _threshold_predictions(
                        holdout_rows,
                        first_feature,
                        first_comparator,
                        first_threshold,
                    )
                    for second_threshold in second_values:
                        second_discovery = _threshold_predictions(
                            discovery_rows,
                            second_feature,
                            second_comparator,
                            second_threshold,
                        )
                        second_holdout = _threshold_predictions(
                            holdout_rows,
                            second_feature,
                            second_comparator,
                            second_threshold,
                        )
                        discovery_pred = [
                            left and right
                            for left, right in zip(first_discovery, second_discovery)
                        ]
                        holdout_pred = [
                            left and right
                            for left, right in zip(first_holdout, second_holdout)
                        ]
                        candidate = TwoFeatureRule(
                            first_feature=first_feature,
                            first_comparator=first_comparator,
                            first_threshold=first_threshold,
                            second_feature=second_feature,
                            second_comparator=second_comparator,
                            second_threshold=second_threshold,
                            discovery_accuracy=_accuracy(discovery_rows, discovery_pred),
                            holdout_accuracy=_accuracy(holdout_rows, holdout_pred),
                        )
                        if best is None or (
                            candidate.discovery_accuracy,
                            candidate.holdout_accuracy,
                        ) > (
                            best.discovery_accuracy,
                            best.holdout_accuracy,
                        ):
                            best = candidate
    assert best is not None
    return best


def _render_group(rows: list[FlipRow], label: str, predicate) -> str:
    subset = [row for row in rows if predicate(row)]
    return (
        f"{label}: total={len(subset)} "
        f"mean_last3_shift={_mean(row.last3_shift for row in subset):.4f} "
        f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
        f"extra_share={_mean(row.extra_support_share for row in subset):.4f} "
        f"extra_corridor={_mean(row.extra_support_corridor_share for row in subset):.4f} "
        f"extra_forward_gap={_mean(row.extra_forward_side_gap for row in subset):.4f} "
        f"extra_fringe_gap={_mean(row.extra_fringe_side_gap for row in subset):.4f}"
    )


def _evaluate_task(
    task: tuple[
        GraphConfig,
        int,
        float,
        tuple[float, float],
        RuleSpec,
        float,
        float,
        int,
        int,
    ],
) -> FlipRow | None:
    (
        config,
        graph_seed,
        neighbor_radius,
        seed_position,
        mover_rule,
        coupling,
        source_offset_y,
        steps,
        source_steps,
    ) = task
    positions, adj, _ = generate_causal_dag(
        n_layers=config.n_layers,
        nodes_per_layer=config.nodes_per_layer,
        y_range=config.y_range,
        connect_radius=config.connect_radius,
        rng_seed=graph_seed,
    )
    neighbors = build_spatial_neighbors(positions, neighbor_radius)

    sx, sy = seed_position
    mover_seed = choose_seed_nodes(positions, sx, sy)
    free_history = evolve_on_graph(
        n_nodes=len(positions),
        neighbors=neighbors,
        seed=mover_seed,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        steps=steps,
    )
    free_outcome, _, _, _, _, free_tracked = _classify_outcome(positions, neighbors, free_history)
    if free_outcome != "survive":
        return None

    free_live = [entry for entry in free_tracked if entry[1] is not None]
    anchor = free_live[min(12, len(free_live) - 1)]
    anchor_packet = anchor[1]
    anchor_centroid = anchor[2]
    side_sign = 1.0 if source_offset_y > 0.0 else -1.0

    source_seed = choose_seed_nodes(
        positions,
        target_x=anchor_centroid[0] + 2.0,
        target_y=anchor_centroid[1] + source_offset_y,
    )
    # Pre-evolve the nearby source before launching the mover, then freeze its
    # late-time footprint into a static field for the probe.
    source_history = evolve_on_graph(
        n_nodes=len(positions),
        neighbors=neighbors,
        seed=source_seed,
        survive=SOURCE_RULE.survive,
        birth=SOURCE_RULE.birth,
        steps=source_steps,
    )
    if sum(1 for state in source_history[-6:] if state) < 3:
        return None

    last3_union = _union_last_steps(source_history, 3)
    last6_union = _union_last_steps(source_history, 6)
    if len(last3_union) < 3 or len(last6_union) < 3:
        return None

    last3_field = compute_field_on_dag(positions, adj, last3_union)
    last6_field = compute_field_on_dag(positions, adj, last6_union)
    last3_shift = _run_coupled_shift(
        positions=positions,
        neighbors=neighbors,
        mover_seed=mover_seed,
        mover_rule=mover_rule,
        field=last3_field,
        coupling=coupling,
        steps=steps,
        free_live=free_live,
        side_sign=side_sign,
    )
    if not math.isfinite(last3_shift) or last3_shift <= 0.0:
        return None

    last6_shift = _run_coupled_shift(
        positions=positions,
        neighbors=neighbors,
        mover_seed=mover_seed,
        mover_rule=mover_rule,
        field=last6_field,
        coupling=coupling,
        steps=steps,
        free_live=free_live,
        side_sign=side_sign,
    )

    extra_support = frozenset(node for node in last6_union if node not in last3_union)
    extra_center = _centroid(positions, extra_support)
    extra_size = float(len(extra_support))
    extra_share = extra_size / max(1.0, float(len(last6_union)))
    extra_forward_share = sum(
        positions[node][0] > anchor_centroid[0] for node in extra_support
    ) / max(1.0, extra_size)
    extra_corridor_share = sum(
        (positions[node][0] > anchor_centroid[0])
        and ((positions[node][1] - anchor_centroid[1]) * side_sign > 0.0)
        for node in extra_support
    ) / max(1.0, extra_size)
    extra_field = {
        node: last6_field.get(node, 0.0) - last3_field.get(node, 0.0)
        for node in range(len(positions))
    }
    extra_field_metrics = _field_bias_metrics(
        positions=positions,
        neighbors=neighbors,
        packet=anchor_packet,
        anchor_centroid=anchor_centroid,
        field=extra_field,
        side_sign=side_sign,
    )

    return FlipRow(
        config=config.label,
        graph_seed=graph_seed,
        mover_rule=mover_rule.label,
        source_offset_y=source_offset_y,
        last3_shift=last3_shift,
        last6_shift=last6_shift,
        flipped=math.isfinite(last6_shift) and last6_shift <= 0.0,
        extra_support_size=extra_size,
        extra_support_share=extra_share,
        extra_support_signed_side=(extra_center[1] - anchor_centroid[1]) * side_sign,
        extra_support_forward_share=extra_forward_share,
        extra_support_corridor_share=extra_corridor_share,
        extra_support_radius=_radius(positions, extra_support, extra_center),
        extra_field_mean_on_packet=extra_field_metrics["field_mean_on_packet"],
        extra_field_range_on_packet=extra_field_metrics["field_range_on_packet"],
        extra_packet_side_gap=extra_field_metrics["packet_side_field_gap"],
        extra_fringe_side_gap=extra_field_metrics["fringe_side_field_gap"],
        extra_forward_side_gap=extra_field_metrics["forward_side_field_gap"],
        extra_fringe_forward_gap=extra_field_metrics["fringe_forward_gap"],
    )


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
    source_steps: int,
    coupling: float,
    neighbor_radius: float,
    source_offsets: list[float],
) -> list[FlipRow]:
    tasks = [
        (
            config,
            graph_seed,
            neighbor_radius,
            seed_position,
            mover_rule,
            coupling,
            source_offset_y,
            steps,
            source_steps,
        )
        for config in CANONICAL_CONFIGS
        for graph_seed in seeds
        for seed_position in SEED_POSITIONS
        for mover_rule in CANONICAL_RULES
        for source_offset_y in source_offsets
    ]
    if workers <= 1:
        return [row for row in (_evaluate_task(task) for task in tasks) if row is not None]

    try:
        ctx = mp.get_context("fork")
        with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
            return [row for row in pool.map(_evaluate_task, tasks) if row is not None]
    except PermissionError:
        return [row for row in (_evaluate_task(task) for task in tasks) if row is not None]


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

    rows = run_rows(
        seeds=range(args.seed_start, args.seed_start + args.seed_count),
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        coupling=args.coupling,
        neighbor_radius=args.neighbor_radius,
        source_offsets=[-3.0, 3.0],
    )
    rows.sort(key=lambda row: (row.config, row.graph_seed, row.mover_rule, row.source_offset_y))
    discovery_rows = [row for row in rows if row.config in DISCOVERY_CONFIGS]
    holdout_rows = [row for row in rows if row.config in HOLDOUT_CONFIGS]

    singles = _top_single_rules(discovery_rows, holdout_rows, top_n=5)
    best_pair = _best_two_feature_rule(discovery_rows, holdout_rows)

    print("=" * 80)
    print("GENERATED DAG LATE-SUPPORT FLIP COMPARE")
    print("=" * 80)
    print(
        f"Rows: {len(rows)} trials where last3_union already steers toward-source, "
        f"neighbor_radius={args.neighbor_radius:.1f}, coupling={args.coupling:.3f}"
    )
    print(
        f"Discovery configs: {sorted(DISCOVERY_CONFIGS)}; "
        f"holdout configs: {sorted(HOLDOUT_CONFIGS)}"
    )
    print()
    print(_render_group(rows, "stable_toward", lambda row: not row.flipped))
    print(_render_group(rows, "flip_to_away", lambda row: row.flipped))
    print()
    print("Top single-threshold discovery rules for the sign flip:")
    for rule in singles:
        print(f"  {rule.render()}")
    print()
    print("Best two-feature discovery rule for the sign flip:")
    print(f"  {best_pair.render()}")
    print()
    print("Interpretation:")
    print(
        "  This compare isolates the extra late support added by `last6_union` beyond "
        "the retained `last3_union` footprint. The target is the sign flip itself: "
        "which added-support observable predicts when the broader footprint turns a "
        "toward-source mover back into away-shift or retiming."
    )


if __name__ == "__main__":
    main()
