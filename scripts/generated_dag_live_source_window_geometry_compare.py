#!/usr/bin/env python3
"""Compare late-support geometry on the live last3-vs-last6 source seam.

This is the direct follow-on to the live-vs-frozen source compare. The bounded
question is:

Which late-support observables explain when the currently retained live
`last6` source window stays coherent and toward-source, versus when the same
broad live source window collapses back into nonpositive steering or diffusion?

To keep the comparison honest, each row reuses the exact same deterministic
source history and free mover path, then only changes the sliding live source
window from 3 to 6.
"""

from __future__ import annotations

from collections import Counter, defaultdict
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

from scripts.generated_dag_live_source_field_compare import (  # noqa: E402
    _pre_evolve_source,
    _step_gradient_coupled,
    _step_graph,
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
    _late_source_metrics,
)
from scripts.generated_dag_pattern_sourced_mover_probe import (  # noqa: E402
    SOURCE_RULE,
    _signed_shift_at_shared_x,
    choose_seed_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


FEATURE_NAMES = [
    "last6_union_size",
    "last6_reuse_share",
    "last6_core_share",
    "last6_corridor_share",
    "last6_centroid_drift",
    "last6_source_signed_side",
    "last6_source_x_lead",
    "extra_support_share",
    "extra_support_forward_share",
    "extra_support_corridor_share",
    "extra_support_radius",
    "extra_field_mean_on_packet",
    "extra_field_range_on_packet",
    "extra_packet_side_gap",
    "extra_fringe_side_gap",
    "extra_forward_side_gap",
]

PAIR_FEATURES = [
    "last6_corridor_share",
    "last6_source_signed_side",
    "extra_support_corridor_share",
    "extra_support_forward_share",
    "extra_field_mean_on_packet",
    "extra_packet_side_gap",
    "extra_forward_side_gap",
]


@dataclass(frozen=True)
class LiveWindowRow:
    config: str
    graph_seed: int
    mover_rule: str
    source_offset_y: float
    last3_outcome: str
    last6_outcome: str
    last3_shift: float
    last6_shift: float
    delta_shift: float
    retained_last6: bool
    last6_beats_last3: bool
    last6_union_size: float
    last6_reuse_share: float
    last6_core_share: float
    last6_corridor_share: float
    last6_centroid_drift: float
    last6_source_signed_side: float
    last6_source_x_lead: float
    extra_support_share: float
    extra_support_forward_share: float
    extra_support_corridor_share: float
    extra_support_radius: float
    extra_field_mean_on_packet: float
    extra_field_range_on_packet: float
    extra_packet_side_gap: float
    extra_fringe_side_gap: float
    extra_forward_side_gap: float


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


def _extend_source_timeline(
    source_history: list[frozenset[int]],
    source_active: frozenset[int],
    neighbors: dict[int, list[int]],
    steps: int,
) -> list[frozenset[int]]:
    timeline = list(source_history)
    current = source_active
    for _ in range(steps):
        timeline.append(current)
        current = _step_graph(
            current,
            neighbors,
            SOURCE_RULE.survive,
            SOURCE_RULE.birth,
        )
    return timeline


def _run_live_history_with_timeline(
    mover_seed: frozenset[int],
    neighbors: dict[int, list[int]],
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    survive: frozenset[int],
    birth: frozenset[int],
    coupling: float,
    steps: int,
    source_window: int,
    source_timeline: list[frozenset[int]],
    pre_len: int,
    n_nodes: int,
) -> list[frozenset[int]]:
    mover_active = mover_seed
    mover_history: list[frozenset[int]] = []
    for step in range(steps):
        mover_history.append(mover_active)
        window_states = source_timeline[max(0, pre_len + step - source_window) : pre_len + step]
        field_nodes = frozenset().union(*(state for state in window_states if state))
        if field_nodes:
            field = compute_field_on_dag(positions, adj, field_nodes)
        else:
            field = {node: 0.0 for node in range(n_nodes)}
        mover_active = _step_gradient_coupled(
            mover_active,
            neighbors,
            survive,
            birth,
            field,
            coupling,
        )
    return mover_history


def _threshold_predictions(
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


def _top_single_rules(
    discovery_rows: list[LiveWindowRow],
    holdout_rows: list[LiveWindowRow],
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
    discovery_rows: list[LiveWindowRow],
    holdout_rows: list[LiveWindowRow],
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


def _best_local_single_rule(rows: list[LiveWindowRow]) -> ThresholdRule:
    best: ThresholdRule | None = None
    for feature in FEATURE_NAMES:
        values = sorted(set(float(getattr(row, feature)) for row in rows))
        for comparator in (">=", "<="):
            for threshold in values:
                predictions = _threshold_predictions(rows, feature, comparator, threshold)
                accuracy = _accuracy(rows, predictions)
                candidate = ThresholdRule(
                    feature=feature,
                    comparator=comparator,
                    threshold=threshold,
                    discovery_accuracy=accuracy,
                    holdout_accuracy=accuracy,
                )
                if best is None or (
                    candidate.discovery_accuracy,
                    candidate.feature,
                    -candidate.threshold,
                ) > (
                    best.discovery_accuracy,
                    best.feature,
                    -best.threshold,
                ):
                    best = candidate
    assert best is not None
    return best


def _render_group(rows: list[LiveWindowRow], label: str, predicate) -> str:
    subset = [row for row in rows if predicate(row)]
    return (
        f"{label}: total={len(subset)} "
        f"mean_last3_shift={_mean(row.last3_shift for row in subset):.4f} "
        f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
        f"mean_delta={_mean(row.delta_shift for row in subset):.4f} "
        f"extra_share={_mean(row.extra_support_share for row in subset):.4f} "
        f"extra_corridor={_mean(row.extra_support_corridor_share for row in subset):.4f} "
        f"extra_field_on_packet={_mean(row.extra_field_mean_on_packet for row in subset):.4f} "
        f"extra_forward_gap={_mean(row.extra_forward_side_gap for row in subset):.4f}"
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
) -> LiveWindowRow | None:
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
    free_outcome, _, _, _, _, free_tracked = _classify_outcome(
        positions,
        neighbors,
        free_history,
    )
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
    pre_source_history, current_source_active = _pre_evolve_source(
        source_seed,
        neighbors,
        source_steps,
    )
    source_timeline = _extend_source_timeline(
        pre_source_history,
        current_source_active,
        neighbors,
        steps,
    )

    last3_history = _run_live_history_with_timeline(
        mover_seed=mover_seed,
        neighbors=neighbors,
        positions=positions,
        adj=adj,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        coupling=coupling,
        steps=steps,
        source_window=3,
        source_timeline=source_timeline,
        pre_len=len(pre_source_history),
        n_nodes=len(positions),
    )
    last6_history = _run_live_history_with_timeline(
        mover_seed=mover_seed,
        neighbors=neighbors,
        positions=positions,
        adj=adj,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        coupling=coupling,
        steps=steps,
        source_window=6,
        source_timeline=source_timeline,
        pre_len=len(pre_source_history),
        n_nodes=len(positions),
    )

    last3_outcome, _, _, _, _, last3_tracked = _classify_outcome(
        positions,
        neighbors,
        last3_history,
    )
    last6_outcome, _, _, _, _, last6_tracked = _classify_outcome(
        positions,
        neighbors,
        last6_history,
    )
    last3_live = [entry for entry in last3_tracked if entry[1] is not None]
    last6_live = [entry for entry in last6_tracked if entry[1] is not None]
    if not last3_live or not last6_live:
        return None

    last3_shift = _signed_shift_at_shared_x(free_live, last3_live, side_sign)
    last6_shift = _signed_shift_at_shared_x(free_live, last6_live, side_sign)
    if not math.isfinite(last3_shift) or not math.isfinite(last6_shift):
        return None

    recent3 = [state for state in source_timeline[-3:] if state]
    recent6 = [state for state in source_timeline[-6:] if state]
    last3_union = frozenset().union(*recent3) if recent3 else frozenset()
    last6_union = frozenset().union(*recent6) if recent6 else frozenset()
    if len(last3_union) < 3 or len(last6_union) < 3:
        return None

    last6_source_metrics = _late_source_metrics(
        positions=positions,
        late_live_states=recent6,
        source_union=last6_union,
        anchor_centroid=anchor_centroid,
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

    last3_field = compute_field_on_dag(positions, adj, last3_union)
    last6_field = compute_field_on_dag(positions, adj, last6_union)
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

    return LiveWindowRow(
        config=config.label,
        graph_seed=graph_seed,
        mover_rule=mover_rule.label,
        source_offset_y=source_offset_y,
        last3_outcome=last3_outcome,
        last6_outcome=last6_outcome,
        last3_shift=last3_shift,
        last6_shift=last6_shift,
        delta_shift=last6_shift - last3_shift,
        retained_last6=(last6_outcome == "survive" and last6_shift > 0.0),
        last6_beats_last3=last6_shift > last3_shift,
        last6_union_size=last6_source_metrics["source_union_size"],
        last6_reuse_share=last6_source_metrics["source_reuse_share"],
        last6_core_share=last6_source_metrics["source_core_share"],
        last6_corridor_share=last6_source_metrics["source_corridor_share"],
        last6_centroid_drift=last6_source_metrics["source_centroid_drift"],
        last6_source_signed_side=last6_source_metrics["source_signed_side"],
        last6_source_x_lead=last6_source_metrics["source_x_lead"],
        extra_support_share=extra_share,
        extra_support_forward_share=extra_forward_share,
        extra_support_corridor_share=extra_corridor_share,
        extra_support_radius=_radius(positions, extra_support, extra_center),
        extra_field_mean_on_packet=extra_field_metrics["field_mean_on_packet"],
        extra_field_range_on_packet=extra_field_metrics["field_range_on_packet"],
        extra_packet_side_gap=extra_field_metrics["packet_side_field_gap"],
        extra_fringe_side_gap=extra_field_metrics["fringe_side_field_gap"],
        extra_forward_side_gap=extra_field_metrics["forward_side_field_gap"],
    )


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
    source_steps: int,
    coupling: float,
    neighbor_radius: float,
    source_offsets: list[float],
) -> list[LiveWindowRow]:
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

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return [row for row in pool.map(_evaluate_task, tasks) if row is not None]


def _render_rule_breakdown(rows: list[LiveWindowRow]) -> list[str]:
    lines = ["Rule breakdown:"]
    buckets: dict[str, list[LiveWindowRow]] = defaultdict(list)
    for row in rows:
        buckets[row.mover_rule].append(row)
    for rule in sorted(buckets):
        subset = buckets[rule]
        retained = sum(row.retained_last6 for row in subset)
        lines.append(
            "  "
            f"{rule}: total={len(subset)} retained_last6={retained}/{len(subset)} "
            f"mean_last3_shift={_mean(row.last3_shift for row in subset):.4f} "
            f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
            f"mean_delta={_mean(row.delta_shift for row in subset):.4f}"
        )
    return lines


def _render_rule_local_rules(rows: list[LiveWindowRow]) -> list[str]:
    lines = ["Rule-local best single-threshold rules:"]
    buckets: dict[str, list[LiveWindowRow]] = defaultdict(list)
    for row in rows:
        buckets[row.mover_rule].append(row)
    for rule in sorted(buckets):
        subset = buckets[rule]
        best = _best_local_single_rule(subset)
        retained = sum(row.retained_last6 for row in subset)
        lines.append(
            "  "
            f"{rule}: retained_last6={retained}/{len(subset)} "
            f"{best.feature} {best.comparator} {best.threshold:.4f} "
            f"(local_accuracy={best.discovery_accuracy:.4f})"
        )
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
    print("GENERATED DAG LIVE SOURCE WINDOW GEOMETRY COMPARE")
    print("=" * 80)
    print(
        f"Rows: {len(rows)} paired live-window trials, neighbor_radius={args.neighbor_radius:.1f}, "
        f"coupling={args.coupling:.3f}, seeds={args.seed_start}..{args.seed_start + args.seed_count - 1}, "
        f"workers={max(1, args.workers)}"
    )
    print(
        f"Discovery configs: {sorted(DISCOVERY_CONFIGS)}; "
        f"holdout configs: {sorted(HOLDOUT_CONFIGS)}"
    )
    print()
    print(
        "Paired window summary: "
        f"last3_positive={sum(row.last3_shift > 0.0 for row in rows)}/{len(rows)} "
        f"last6_positive={sum(row.last6_shift > 0.0 for row in rows)}/{len(rows)} "
        f"last6_retained={sum(row.retained_last6 for row in rows)}/{len(rows)} "
        f"last6_beats_last3={sum(row.last6_beats_last3 for row in rows)}/{len(rows)} "
        f"mean_last3_shift={_mean(row.last3_shift for row in rows):.4f} "
        f"mean_last6_shift={_mean(row.last6_shift for row in rows):.4f} "
        f"mean_delta={_mean(row.delta_shift for row in rows):.4f}"
    )
    print()
    print(_render_group(rows, "retained_last6", lambda row: row.retained_last6))
    print(
        _render_group(
            rows,
            "nonretained_last6",
            lambda row: not row.retained_last6,
        )
    )
    print()
    for line in _render_rule_breakdown(rows):
        print(line)
    print()
    for line in _render_rule_local_rules(rows):
        print(line)
    print()
    print("Top single-threshold discovery rules for retained live last6 steering:")
    for rule in singles:
        print(f"  {rule.render()}")
    print()
    print("Best two-feature discovery rule for retained live last6 steering:")
    print(f"  {best_pair.render()}")
    print()
    print("Interpretation:")
    print(
        "  This compare keeps the source evolution fixed and only widens the live "
        "source window from 3 to 6. The target is the current retained branch itself: "
        "which late-support geometry lets the broader live `last6` window stay both "
        "coherent and toward-source, instead of collapsing back into nonpositive "
        "steering or diffusion."
    )


if __name__ == "__main__":
    main()
