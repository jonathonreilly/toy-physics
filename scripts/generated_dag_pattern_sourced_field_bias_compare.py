#!/usr/bin/env python3
"""Compare compact-source and local field-bias observables on mover steering.

This stays tightly bounded to the retained pattern-sourced mover substrate:

1. coherent free movers only
2. `neighbor_radius = 2.5`
3. retained coupling `3.0`
4. one source rule (`self`)

The question is whether toward-source steering lives on a smaller source family:
compact recurrent late packets plus a cleaner intended-side field bias at the
free mover anchor. To reduce adaptivity, discovery uses `dense-25` and
`sparse-25`, while `wide-15` and `long-30` act as holdout.
"""

from __future__ import annotations

from collections import defaultdict
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
from scripts.generated_dag_pattern_sourced_mover_probe import (  # noqa: E402
    SOURCE_RULE,
    _source_summary,
    choose_seed_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


FEATURE_NAMES = [
    "source_union_size",
    "source_mean_size",
    "source_reuse_share",
    "source_core_share",
    "source_union_radius",
    "source_mean_state_radius",
    "source_centroid_drift",
    "source_signed_side",
    "source_x_lead",
    "source_corridor_share",
    "field_mean_on_packet",
    "field_range_on_packet",
    "packet_side_field_gap",
    "fringe_side_field_gap",
    "forward_side_field_gap",
    "fringe_forward_gap",
]

PAIR_FEATURES = [
    "source_reuse_share",
    "source_core_share",
    "source_union_radius",
    "source_centroid_drift",
    "source_corridor_share",
    "fringe_side_field_gap",
    "forward_side_field_gap",
    "field_mean_on_packet",
]


@dataclass(frozen=True)
class FieldBiasRow:
    config: str
    graph_seed: int
    mover_rule: str
    source_offset_y: float
    positive_shift: bool
    signed_toward_shift: float
    source_union_size: float
    source_mean_size: float
    source_reuse_share: float
    source_core_share: float
    source_union_radius: float
    source_mean_state_radius: float
    source_centroid_drift: float
    source_signed_side: float
    source_x_lead: float
    source_corridor_share: float
    field_mean_on_packet: float
    field_range_on_packet: float
    packet_side_field_gap: float
    fringe_side_field_gap: float
    forward_side_field_gap: float
    fringe_forward_gap: float


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


def _late_source_metrics(
    positions: list[tuple[float, float]],
    late_live_states: list[frozenset[int]],
    source_union: frozenset[int],
    anchor_centroid: tuple[float, float],
    side_sign: float,
) -> dict[str, float]:
    if not late_live_states or not source_union:
        return {
            "source_union_size": 0.0,
            "source_mean_size": 0.0,
            "source_reuse_share": 0.0,
            "source_core_share": 0.0,
            "source_union_radius": 0.0,
            "source_mean_state_radius": 0.0,
            "source_centroid_drift": 0.0,
            "source_signed_side": 0.0,
            "source_x_lead": 0.0,
            "source_corridor_share": 0.0,
        }

    union_centroid = _centroid(positions, source_union)
    core = set(late_live_states[0])
    for state in late_live_states[1:]:
        core.intersection_update(state)
    state_centroids = [_centroid(positions, state) for state in late_live_states]
    mean_state_radius = _mean(
        _radius(positions, state, center)
        for state, center in zip(late_live_states, state_centroids)
    )
    centroid_drift = _mean(
        math.dist(left, right)
        for left, right in zip(state_centroids, state_centroids[1:])
    )
    corridor_hits = sum(
        1
        for node in source_union
        if (positions[node][0] > anchor_centroid[0])
        and ((positions[node][1] - anchor_centroid[1]) * side_sign > 0.0)
    )
    return {
        "source_union_size": float(len(source_union)),
        "source_mean_size": _mean(len(state) for state in late_live_states),
        "source_reuse_share": _mean(len(state) for state in late_live_states)
        / max(1.0, float(len(source_union))),
        "source_core_share": len(core) / max(1.0, float(len(source_union))),
        "source_union_radius": _radius(positions, source_union, union_centroid),
        "source_mean_state_radius": mean_state_radius,
        "source_centroid_drift": centroid_drift,
        "source_signed_side": (union_centroid[1] - anchor_centroid[1]) * side_sign,
        "source_x_lead": union_centroid[0] - anchor_centroid[0],
        "source_corridor_share": corridor_hits / max(1.0, float(len(source_union))),
    }


def _field_bias_metrics(
    positions: list[tuple[float, float]],
    neighbors: dict[int, list[int]],
    packet: frozenset[int],
    anchor_centroid: tuple[float, float],
    field: dict[int, float],
    side_sign: float,
) -> dict[str, float]:
    packet_intended = [
        field.get(node, 0.0)
        for node in packet
        if (positions[node][1] - anchor_centroid[1]) * side_sign > 0.0
    ]
    packet_opposite = [
        field.get(node, 0.0)
        for node in packet
        if (positions[node][1] - anchor_centroid[1]) * side_sign < 0.0
    ]

    fringe_nodes = {
        nb
        for node in packet
        for nb in neighbors.get(node, [])
        if nb not in packet
    }
    fringe_intended = [
        field.get(node, 0.0)
        for node in fringe_nodes
        if (positions[node][1] - anchor_centroid[1]) * side_sign > 0.0
    ]
    fringe_opposite = [
        field.get(node, 0.0)
        for node in fringe_nodes
        if (positions[node][1] - anchor_centroid[1]) * side_sign < 0.0
    ]
    forward_intended = [
        field.get(node, 0.0)
        for node in fringe_nodes
        if (positions[node][0] > anchor_centroid[0])
        and ((positions[node][1] - anchor_centroid[1]) * side_sign > 0.0)
    ]
    forward_opposite = [
        field.get(node, 0.0)
        for node in fringe_nodes
        if (positions[node][0] > anchor_centroid[0])
        and ((positions[node][1] - anchor_centroid[1]) * side_sign < 0.0)
    ]
    fringe_forward = [
        field.get(node, 0.0)
        for node in fringe_nodes
        if positions[node][0] > anchor_centroid[0]
    ]
    fringe_backward = [
        field.get(node, 0.0)
        for node in fringe_nodes
        if positions[node][0] <= anchor_centroid[0]
    ]

    packet_fields = [field.get(node, 0.0) for node in packet]
    return {
        "field_mean_on_packet": _mean(packet_fields),
        "field_range_on_packet": max(packet_fields, default=0.0) - min(packet_fields, default=0.0),
        "packet_side_field_gap": _mean(packet_intended) - _mean(packet_opposite),
        "fringe_side_field_gap": _mean(fringe_intended) - _mean(fringe_opposite),
        "forward_side_field_gap": _mean(forward_intended) - _mean(forward_opposite),
        "fringe_forward_gap": _mean(fringe_forward) - _mean(fringe_backward),
    }


def _threshold_predictions(
    rows: list[FieldBiasRow],
    feature: str,
    comparator: str,
    threshold: float,
) -> list[bool]:
    values = [float(getattr(row, feature)) for row in rows]
    if comparator == ">=":
        return [value >= threshold for value in values]
    return [value <= threshold for value in values]


def _accuracy(
    rows: list[FieldBiasRow],
    predictions: list[bool],
) -> float:
    truth = [row.positive_shift for row in rows]
    return sum(pred == target for pred, target in zip(predictions, truth)) / len(rows)


def _top_single_rules(
    discovery_rows: list[FieldBiasRow],
    holdout_rows: list[FieldBiasRow],
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
    discovery_rows: list[FieldBiasRow],
    holdout_rows: list[FieldBiasRow],
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


def _rule_group_summary(
    rows: list[FieldBiasRow],
    feature: str,
    comparator: str,
    threshold: float,
) -> str:
    matched = [
        row
        for row in rows
        if (getattr(row, feature) >= threshold if comparator == ">=" else getattr(row, feature) <= threshold)
    ]
    unmatched = [row for row in rows if row not in matched]
    def render_group(label: str, subset: list[FieldBiasRow]) -> str:
        positive = sum(row.positive_shift for row in subset)
        return (
            f"{label}: total={len(subset)} "
            f"positive_fraction={positive / len(subset):.4f} "
            f"mean_shift={_mean(row.signed_toward_shift for row in subset):.4f}"
        )
    return f"{render_group('matched', matched)} | {render_group('unmatched', unmatched)}"


def _render_feature_means(rows: list[FieldBiasRow]) -> list[str]:
    groups = {
        "positive": [row for row in rows if row.positive_shift],
        "nonpositive": [row for row in rows if not row.positive_shift],
    }
    lines = ["Source-family and local field means:"]
    for label, subset in groups.items():
        lines.append(
            "  "
            f"{label:<11s} "
            f"reuse={_mean(row.source_reuse_share for row in subset):.4f} "
            f"core={_mean(row.source_core_share for row in subset):.4f} "
            f"union_radius={_mean(row.source_union_radius for row in subset):.4f} "
            f"drift={_mean(row.source_centroid_drift for row in subset):.4f} "
            f"corridor={_mean(row.source_corridor_share for row in subset):.4f} "
            f"fringe_side_gap={_mean(row.fringe_side_field_gap for row in subset):.4f} "
            f"forward_side_gap={_mean(row.forward_side_field_gap for row in subset):.4f}"
        )
    return lines


def _evaluate_trial(
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
        int,
    ],
) -> FieldBiasRow | None:
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
        source_window,
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
    source_history = evolve_on_graph(
        n_nodes=len(positions),
        neighbors=neighbors,
        seed=source_seed,
        survive=SOURCE_RULE.survive,
        birth=SOURCE_RULE.birth,
        steps=source_steps,
    )
    source_status, source_union, _, _, _ = _source_summary(source_history, source_window)
    if source_status == "dead" or len(source_union) < 3:
        return None

    late_live_states = [state for state in source_history[-source_window:] if state]
    source_metrics = _late_source_metrics(
        positions=positions,
        late_live_states=late_live_states,
        source_union=source_union,
        anchor_centroid=anchor_centroid,
        side_sign=side_sign,
    )
    field = compute_field_on_dag(positions, adj, source_union)
    field_metrics = _field_bias_metrics(
        positions=positions,
        neighbors=neighbors,
        packet=anchor_packet,
        anchor_centroid=anchor_centroid,
        field=field,
        side_sign=side_sign,
    )

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
    if coupled_live:
        compare_step = min(len(free_live), len(coupled_live)) - 1
        signed_toward_shift = (
            coupled_live[compare_step][2][1] - free_live[compare_step][2][1]
        ) * side_sign
    else:
        signed_toward_shift = float("nan")

    return FieldBiasRow(
        config=config.label,
        graph_seed=graph_seed,
        mover_rule=mover_rule.label,
        source_offset_y=source_offset_y,
        positive_shift=math.isfinite(signed_toward_shift) and signed_toward_shift > 0.0,
        signed_toward_shift=signed_toward_shift,
        **source_metrics,
        **field_metrics,
    )


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
    source_steps: int,
    source_window: int,
    coupling: float,
    neighbor_radius: float,
    source_offsets: list[float],
) -> list[FieldBiasRow]:
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
            source_window,
        )
        for config in CANONICAL_CONFIGS
        for graph_seed in seeds
        for seed_position in SEED_POSITIONS
        for mover_rule in CANONICAL_RULES
        for source_offset_y in source_offsets
    ]
    if workers <= 1:
        return [row for row in (_evaluate_trial(task) for task in tasks) if row is not None]

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return [row for row in pool.map(_evaluate_trial, tasks) if row is not None]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--source-window", type=int, default=6)
    parser.add_argument("--neighbor-radius", type=float, default=2.5)
    parser.add_argument("--coupling", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    rows = run_rows(
        seeds=range(args.seed_start, args.seed_start + args.seed_count),
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        source_window=args.source_window,
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
    print("GENERATED DAG PATTERN-SOURCED FIELD-BIAS COMPARE")
    print("=" * 80)
    print(
        f"Rows: {len(rows)} viable-source trials on neighbor_radius={args.neighbor_radius:.1f}, "
        f"coupling={args.coupling:.3f}"
    )
    print(
        f"Discovery configs: {sorted(DISCOVERY_CONFIGS)}; "
        f"holdout configs: {sorted(HOLDOUT_CONFIGS)}"
    )
    print()
    for line in _render_feature_means(rows):
        print(line)
    print()
    print("Top single-threshold discovery rules for toward-source shift:")
    for rule in singles:
        print(f"  {rule.render()}")
    print()
    best_single = singles[0]
    print("Best single-rule split on all viable rows:")
    print(
        "  "
        + _rule_group_summary(
            rows,
            best_single.feature,
            best_single.comparator,
            best_single.threshold,
        )
    )
    print()
    print("Best two-feature discovery rule for toward-source shift:")
    print(f"  {best_pair.render()}")
    print()
    print("Interpretation:")
    print(
        "  This compare asks whether toward-source rows are best read as a compact "
        "late-source packet family with a cleaner intended-side field bias at the "
        "free mover anchor, rather than as a generic source-survival effect."
    )


if __name__ == "__main__":
    main()
