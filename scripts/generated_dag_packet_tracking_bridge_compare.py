#!/usr/bin/env python3
"""Bridge packet-local mover observables onto generated-DAG pattern outcomes.

This stays on the mechanism-language lane. The question is not whether a broad
new mover ladder exists, but whether a small packet-local observable family can
already explain the current three-way mover outcomes on generated DAGs:

1. coherent translating packet survives
2. packet stays alive but diffuses
3. packet dies

The retained analogy to the earlier geometry / detector-side bridge is:

- completion/load: how much forward local support the tracked packet sees
- balance/bottleneck: how narrowly that forward support is focused
- continuity guard: whether the packet survives the opening transient at all
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
import math
import multiprocessing as mp
import os
import statistics
import sys
from collections import Counter
from typing import Iterable

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generated_dag_pattern_mobility import (  # noqa: E402
    build_spatial_neighbors,
    evolve_on_graph,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


@dataclass(frozen=True)
class GraphConfig:
    label: str
    n_layers: int
    nodes_per_layer: int
    y_range: float
    connect_radius: float


@dataclass(frozen=True)
class RuleSpec:
    label: str
    survive: frozenset[int]
    birth: frozenset[int]


@dataclass(frozen=True)
class TrialRow:
    config: str
    graph_seed: int
    neighbor_radius: float
    seed_x: float
    seed_y: float
    rule: str
    outcome: str
    displacement: float
    mean_radius: float
    live_fraction: float
    tail_fraction: float
    early_front_load: float
    early_front_share: float
    early_front_skew: float
    early_band_share: float
    early_ud_balance: float
    early_fringe_density: float
    early_front_completion: float
    early_live_fraction: float


@dataclass(frozen=True)
class ThresholdRule:
    feature: str
    comparator: str
    threshold: float
    accuracy: float
    tp: int
    tn: int

    def render(self) -> str:
        return (
            f"{self.feature} {self.comparator} {self.threshold:.3f} "
            f"(accuracy={self.accuracy:.4f}, tp={self.tp}, tn={self.tn})"
        )


@dataclass(frozen=True)
class TwoFeatureRule:
    first_feature: str
    first_comparator: str
    first_threshold: float
    second_feature: str
    second_comparator: str
    second_threshold: float
    accuracy: float
    tp: int
    tn: int

    def render(self) -> str:
        return (
            f"{self.first_feature} {self.first_comparator} {self.first_threshold:.3f} and "
            f"{self.second_feature} {self.second_comparator} {self.second_threshold:.3f} "
            f"(accuracy={self.accuracy:.4f}, tp={self.tp}, tn={self.tn})"
        )


CANONICAL_CONFIGS = [
    GraphConfig("dense-25", n_layers=25, nodes_per_layer=20, y_range=8.0, connect_radius=2.5),
    GraphConfig("sparse-25", n_layers=25, nodes_per_layer=20, y_range=8.0, connect_radius=1.8),
    GraphConfig("wide-15", n_layers=15, nodes_per_layer=30, y_range=8.0, connect_radius=2.0),
    GraphConfig("long-30", n_layers=30, nodes_per_layer=15, y_range=6.0, connect_radius=2.5),
]

CANONICAL_RULES = [
    RuleSpec("life", survive=frozenset({2, 3}), birth=frozenset({3})),
    RuleSpec("self", survive=frozenset({3, 4}), birth=frozenset({3, 4})),
    RuleSpec("wide", survive=frozenset({2, 3, 4}), birth=frozenset({3})),
]

SEED_POSITIONS = [(6.0, 0.0), (6.0, 3.0), (12.0, 0.0)]
NEIGHBOR_RADII = [1.5, 2.0, 2.5]
EARLY_STEPS = 8

DISCOVERY_CONFIGS = {"dense-25", "sparse-25"}
HOLDOUT_CONFIGS = {"wide-15", "long-30"}

FEATURE_NAMES = [
    "early_live_fraction",
    "early_front_load",
    "early_front_share",
    "early_front_skew",
    "early_band_share",
    "early_ud_balance",
    "early_fringe_density",
    "early_front_completion",
]


def _connected_components(
    active: frozenset[int],
    neighbors: dict[int, list[int]],
) -> list[frozenset[int]]:
    remaining = set(active)
    components: list[frozenset[int]] = []
    while remaining:
        start = remaining.pop()
        stack = [start]
        component = {start}
        while stack:
            node = stack.pop()
            for nb in neighbors.get(node, []):
                if nb in remaining:
                    remaining.remove(nb)
                    component.add(nb)
                    stack.append(nb)
        components.append(frozenset(component))
    return components


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
    centroid: tuple[float, float],
) -> float:
    if not state:
        return 0.0
    return max(math.dist(positions[idx], centroid) for idx in state)


def _track_packet(
    positions: list[tuple[float, float]],
    neighbors: dict[int, list[int]],
    history: list[frozenset[int]],
) -> list[tuple[int, frozenset[int] | None, tuple[float, float] | None, float | None]]:
    expected = _centroid(positions, history[0])
    previous_centroid: tuple[float, float] | None = None
    tracked: list[tuple[int, frozenset[int] | None, tuple[float, float] | None, float | None]] = []

    for step, state in enumerate(history):
        candidates = [
            component
            for component in _connected_components(state, neighbors)
            if 3 <= len(component) <= 12
        ]
        if not candidates:
            tracked.append((step, None, None, None))
            continue

        packet = min(
            candidates,
            key=lambda component: (
                math.dist(_centroid(positions, component), expected),
                abs(len(component) - 5),
            ),
        )
        packet_centroid = _centroid(positions, packet)
        packet_radius = _radius(positions, packet, packet_centroid)
        tracked.append((step, packet, packet_centroid, packet_radius))

        if previous_centroid is None:
            expected = packet_centroid
        else:
            dx = packet_centroid[0] - previous_centroid[0]
            dy = packet_centroid[1] - previous_centroid[1]
            expected = (packet_centroid[0] + dx, packet_centroid[1] + dy)
        previous_centroid = packet_centroid

    return tracked


def _classify_outcome(
    positions: list[tuple[float, float]],
    neighbors: dict[int, list[int]],
    history: list[frozenset[int]],
) -> tuple[str, float, float, float, float, list[tuple[int, frozenset[int] | None, tuple[float, float] | None, float | None]]]:
    tracked = _track_packet(positions, neighbors, history)
    live = [entry for entry in tracked if entry[1] is not None]
    if not live:
        return ("die", 0.0, 0.0, 0.0, 0.0, tracked)

    displacement = math.dist(live[0][2], live[-1][2])  # type: ignore[arg-type]
    mean_radius = statistics.fmean(entry[3] for entry in live if entry[3] is not None)
    live_fraction = len(live) / len(tracked)
    tail_live = [entry for entry in live if entry[0] >= len(tracked) // 2]
    tail_fraction = len(tail_live) / max(1, len(tracked) - len(tracked) // 2)

    if tail_fraction < 0.25 or len(history[-1]) == 0:
        return ("die", displacement, mean_radius, live_fraction, tail_fraction, tracked)

    if live_fraction >= 0.65 and mean_radius <= 2.1 and displacement >= 3.0:
        return ("survive", displacement, mean_radius, live_fraction, tail_fraction, tracked)

    return ("diffuse", displacement, mean_radius, live_fraction, tail_fraction, tracked)


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _packet_local_metrics(
    positions: list[tuple[float, float]],
    neighbors: dict[int, list[int]],
    packet: frozenset[int],
    packet_centroid: tuple[float, float],
) -> dict[str, float]:
    forward = 0
    backward = 0
    band = 0
    upper = 0
    lower = 0
    fringe_nodes: set[int] = set()
    forward_x_gains: list[float] = []

    for node in packet:
        for nb in neighbors.get(node, []):
            if nb in packet:
                continue
            fringe_nodes.add(nb)
            dx = positions[nb][0] - packet_centroid[0]
            dy = positions[nb][1] - packet_centroid[1]
            if dx > 0:
                forward += 1
                forward_x_gains.append(dx)
                if dy >= 0:
                    upper += 1
                if dy <= 0:
                    lower += 1
            else:
                backward += 1
            if dx > 0 and abs(dy) <= 1.5:
                band += 1

    total = max(1, forward + backward)
    front_share = forward / total
    front_skew = (forward - backward) / total
    ud_balance = min(upper, lower) / max(upper, lower, 1)
    band_share = band / max(1, forward)
    align = 1.0 / (
        1.0 + (statistics.pstdev(forward_x_gains) if len(forward_x_gains) > 1 else 0.0)
    )
    front_load = math.log10(forward + 1.0)
    return {
        "early_front_load": front_load,
        "early_front_share": front_share,
        "early_front_skew": front_skew,
        "early_band_share": band_share,
        "early_ud_balance": ud_balance,
        "early_fringe_density": len(fringe_nodes) / max(1, len(packet)),
        "early_front_completion": front_load * front_share * align,
    }


def _evaluate_trial(
    task: tuple[GraphConfig, int, float, tuple[float, float], RuleSpec, int],
) -> TrialRow:
    config, graph_seed, neighbor_radius, seed_position, rule, steps = task
    positions, _, _ = generate_causal_dag(
        n_layers=config.n_layers,
        nodes_per_layer=config.nodes_per_layer,
        y_range=config.y_range,
        connect_radius=config.connect_radius,
        rng_seed=graph_seed,
    )
    neighbors = build_spatial_neighbors(positions, neighbor_radius)

    sx, sy = seed_position
    nearest = sorted(
        ((idx, math.dist(positions[idx], (sx, sy))) for idx in range(len(positions))),
        key=lambda item: item[1],
    )
    seed = frozenset(idx for idx, _ in nearest[:5])
    history = evolve_on_graph(
        n_nodes=len(positions),
        neighbors=neighbors,
        seed=seed,
        survive=rule.survive,
        birth=rule.birth,
        steps=steps,
    )
    outcome, displacement, mean_radius, live_fraction, tail_fraction, tracked = (
        _classify_outcome(positions, neighbors, history)
    )

    early = [entry for entry in tracked[:EARLY_STEPS] if entry[1] is not None]
    if early:
        metrics = [
            _packet_local_metrics(positions, neighbors, packet, packet_centroid)
            for _, packet, packet_centroid, _ in early
        ]
        averaged = {
            feature: _mean(metric[feature] for metric in metrics)
            for feature in metrics[0]
        }
    else:
        averaged = {feature: 0.0 for feature in FEATURE_NAMES if feature != "early_live_fraction"}

    return TrialRow(
        config=config.label,
        graph_seed=graph_seed,
        neighbor_radius=neighbor_radius,
        seed_x=sx,
        seed_y=sy,
        rule=rule.label,
        outcome=outcome,
        displacement=displacement,
        mean_radius=mean_radius,
        live_fraction=live_fraction,
        tail_fraction=tail_fraction,
        early_live_fraction=len(early) / EARLY_STEPS,
        **averaged,
    )


def _threshold_predictions(
    rows: list[TrialRow],
    feature: str,
    comparator: str,
    threshold: float,
) -> list[bool]:
    values = [float(getattr(row, feature)) for row in rows]
    if comparator == ">=":
        return [value >= threshold for value in values]
    return [value <= threshold for value in values]


def _best_single_threshold(
    rows: list[TrialRow],
    feature: str,
    positive: set[str],
) -> ThresholdRule:
    values = sorted(set(float(getattr(row, feature)) for row in rows))
    best: ThresholdRule | None = None
    truth = [row.outcome in positive for row in rows]
    for comparator in (">=", "<="):
        for threshold in values:
            pred = _threshold_predictions(rows, feature, comparator, threshold)
            tp = sum(p and t for p, t in zip(pred, truth))
            tn = sum((not p) and (not t) for p, t in zip(pred, truth))
            accuracy = (tp + tn) / len(rows)
            candidate = ThresholdRule(feature, comparator, threshold, accuracy, tp, tn)
            if best is None or candidate.accuracy > best.accuracy:
                best = candidate
    assert best is not None
    return best


def _best_two_feature_rule(
    rows: list[TrialRow],
    positive: set[str],
    first_feature: str,
    first_comparator: str,
    second_feature: str,
    second_comparator: str,
) -> TwoFeatureRule:
    first_values = sorted(set(float(getattr(row, first_feature)) for row in rows))
    second_values = sorted(set(float(getattr(row, second_feature)) for row in rows))
    truth = [row.outcome in positive for row in rows]
    best: TwoFeatureRule | None = None
    for first_threshold in first_values:
        first_pred = _threshold_predictions(rows, first_feature, first_comparator, first_threshold)
        for second_threshold in second_values:
            second_pred = _threshold_predictions(
                rows,
                second_feature,
                second_comparator,
                second_threshold,
            )
            pred = [left and right for left, right in zip(first_pred, second_pred)]
            tp = sum(p and t for p, t in zip(pred, truth))
            tn = sum((not p) and (not t) for p, t in zip(pred, truth))
            accuracy = (tp + tn) / len(rows)
            candidate = TwoFeatureRule(
                first_feature=first_feature,
                first_comparator=first_comparator,
                first_threshold=first_threshold,
                second_feature=second_feature,
                second_comparator=second_comparator,
                second_threshold=second_threshold,
                accuracy=accuracy,
                tp=tp,
                tn=tn,
            )
            if best is None or candidate.accuracy > best.accuracy:
                best = candidate
    assert best is not None
    return best


def _apply_two_feature_rule(
    rows: list[TrialRow],
    positive: set[str],
    rule: TwoFeatureRule,
) -> float:
    truth = [row.outcome in positive for row in rows]
    first_pred = _threshold_predictions(
        rows,
        rule.first_feature,
        rule.first_comparator,
        rule.first_threshold,
    )
    second_pred = _threshold_predictions(
        rows,
        rule.second_feature,
        rule.second_comparator,
        rule.second_threshold,
    )
    pred = [left and right for left, right in zip(first_pred, second_pred)]
    tp = sum(p and t for p, t in zip(pred, truth))
    tn = sum((not p) and (not t) for p, t in zip(pred, truth))
    return (tp + tn) / len(rows)


def _render_outcome_breakdown(rows: list[TrialRow], label: str) -> str:
    counts = Counter(row.outcome for row in rows)
    return (
        f"{label}: total={len(rows)} "
        f"survive={counts.get('survive', 0)} "
        f"diffuse={counts.get('diffuse', 0)} "
        f"die={counts.get('die', 0)}"
    )


def _render_feature_means(rows: list[TrialRow]) -> list[str]:
    lines = ["Outcome means on the retained packet-tracking observables:"]
    for outcome in ("survive", "diffuse", "die"):
        group = [row for row in rows if row.outcome == outcome]
        lines.append(
            "  "
            f"{outcome:<7s} "
            f"early_front_load={_mean(row.early_front_load for row in group):.4f} "
            f"early_band_share={_mean(row.early_band_share for row in group):.4f} "
            f"early_ud_balance={_mean(row.early_ud_balance for row in group):.4f} "
            f"early_fringe_density={_mean(row.early_fringe_density for row in group):.4f} "
            f"early_live_fraction={_mean(row.early_live_fraction for row in group):.4f}"
        )
    return lines


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
) -> list[TrialRow]:
    tasks = [
        (config, graph_seed, neighbor_radius, seed_position, rule, steps)
        for config in CANONICAL_CONFIGS
        for graph_seed in seeds
        for neighbor_radius in NEIGHBOR_RADII
        for seed_position in SEED_POSITIONS
        for rule in CANONICAL_RULES
    ]
    if workers <= 1:
        return [_evaluate_trial(task) for task in tasks]
    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return list(pool.map(_evaluate_trial, tasks))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    seeds = range(args.seed_start, args.seed_start + args.seed_count)
    rows = run_rows(seeds=seeds, workers=max(1, args.workers), steps=args.steps)
    rows.sort(key=lambda row: (row.config, row.graph_seed, row.neighbor_radius, row.seed_x, row.seed_y, row.rule))

    discovery_rows = [row for row in rows if row.config in DISCOVERY_CONFIGS]
    holdout_rows = [row for row in rows if row.config in HOLDOUT_CONFIGS]
    live_discovery_rows = [row for row in discovery_rows if row.outcome != "die"]
    live_holdout_rows = [row for row in holdout_rows if row.outcome != "die"]

    live_die_single = {
        feature: _best_single_threshold(discovery_rows, feature, {"survive", "diffuse"})
        for feature in FEATURE_NAMES
    }
    survive_diffuse_single = {
        feature: _best_single_threshold(live_discovery_rows, feature, {"survive"})
        for feature in FEATURE_NAMES
    }
    best_live_die_single = max(live_die_single.values(), key=lambda item: item.accuracy)
    best_survive_diffuse_single = max(
        survive_diffuse_single.values(),
        key=lambda item: item.accuracy,
    )

    live_die_rule = _best_two_feature_rule(
        discovery_rows,
        positive={"survive", "diffuse"},
        first_feature="early_live_fraction",
        first_comparator=">=",
        second_feature="early_front_load",
        second_comparator=">=",
    )
    survive_diffuse_rule = _best_two_feature_rule(
        live_discovery_rows,
        positive={"survive"},
        first_feature="early_front_load",
        first_comparator=">=",
        second_feature="early_band_share",
        second_comparator="<=",
    )

    live_die_holdout = _apply_two_feature_rule(
        holdout_rows,
        positive={"survive", "diffuse"},
        rule=live_die_rule,
    )
    survive_diffuse_holdout = _apply_two_feature_rule(
        live_holdout_rows,
        positive={"survive"},
        rule=survive_diffuse_rule,
    )

    print("=" * 80)
    print("GENERATED DAG PACKET-TRACKING BRIDGE COMPARE")
    print("=" * 80)
    print(
        f"Seeds: {args.seed_start}..{args.seed_start + args.seed_count - 1} "
        f"({args.seed_count} per config), steps={args.steps}, workers={max(1, args.workers)}"
    )
    print(
        "Canonical mover family: 4 graph configs x 3 neighbor radii x 3 seed positions x "
        "3 canonical rules"
    )
    print()
    print(_render_outcome_breakdown(rows, "all_rows"))
    print(_render_outcome_breakdown(discovery_rows, "discovery_rows"))
    print(_render_outcome_breakdown(holdout_rows, "holdout_rows"))
    print()
    for line in _render_feature_means(rows):
        print(line)
    print()
    print("Best discovery single-feature live-vs-die guards:")
    for feature in FEATURE_NAMES:
        print(f"  {live_die_single[feature].render()}")
    print()
    print("Best discovery single-feature survive-vs-diffuse selectors:")
    for feature in FEATURE_NAMES:
        print(f"  {survive_diffuse_single[feature].render()}")
    print()
    print(f"best_live_die_single={best_live_die_single.render()}")
    print(f"best_survive_diffuse_single={best_survive_diffuse_single.render()}")
    print()
    print(f"discovery_live_die_rule={live_die_rule.render()}")
    print(f"holdout_live_die_accuracy={live_die_holdout:.4f}")
    print(f"discovery_survive_diffuse_rule={survive_diffuse_rule.render()}")
    print(f"holdout_survive_diffuse_accuracy={survive_diffuse_holdout:.4f}")
    print()
    print("Interpretation:")
    print(
        "  The mover bridge is now two-stage rather than one-scalar. A packet first "
        "needs to survive the opening transient with enough local forward load, and "
        "then the live rows split again by how tightly that forward support stays "
        "focused inside the forward band."
    )
    print(
        "  In the shared mechanism vocabulary: local frontier load is the mover-side "
        "completion/load floor, while forward-band concentration is the mover-side "
        "bottleneck term that separates coherent translating packets from diffuse "
        "alive-but-smeared rows."
    )
    print(
        "  This is the packet-tracking bridge needed for the next frontier: field-to-"
        "pattern coupling on a substrate that already supports coherent translation."
    )


if __name__ == "__main__":
    main()
