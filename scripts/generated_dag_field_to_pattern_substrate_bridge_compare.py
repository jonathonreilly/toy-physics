#!/usr/bin/env python3
"""Bridge live source retention onto free-mover substrate observables.

This is the next bounded architecture step after the self-branch stop rule.
Instead of shaving more config-local last6 clauses directly, it asks whether
the remaining self-branch spread is better explained by:

1. source-side live-window geometry
2. free-mover packet/substrate observables
3. a small mixed rule using one source feature and one substrate feature

The retained target is the broad live `last6` branch on `mover_rule == "self"`.
Discovery stays on `dense-25` and `sparse-25`; holdout stays on `long-30` and
`wide-15`.
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

from scripts.generated_dag_live_source_field_compare import (  # noqa: E402
    _pre_evolve_source,
    _step_gradient_coupled,
    _step_graph,
)
from scripts.generated_dag_packet_tracking_bridge_compare import (  # noqa: E402
    CANONICAL_CONFIGS,
    CANONICAL_RULES,
    DISCOVERY_CONFIGS,
    EARLY_STEPS,
    HOLDOUT_CONFIGS,
    SEED_POSITIONS,
    GraphConfig,
    RuleSpec,
    _classify_outcome,
    _packet_local_metrics,
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


SOURCE_FEATURES = [
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

SUBSTRATE_FEATURES = [
    "early_live_fraction",
    "early_front_load",
    "early_front_share",
    "early_front_skew",
    "early_band_share",
    "early_ud_balance",
    "early_fringe_density",
    "early_front_completion",
]


@dataclass(frozen=True)
class BridgeRow:
    config: str
    graph_seed: int
    seed_x: float
    seed_y: float
    source_offset_y: float
    retained_last6: bool
    last6_outcome: str
    last6_shift: float
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
    early_live_fraction: float
    early_front_load: float
    early_front_share: float
    early_front_skew: float
    early_band_share: float
    early_ud_balance: float
    early_fringe_density: float
    early_front_completion: float


@dataclass(frozen=True)
class ThresholdRule:
    family: str
    feature: str
    comparator: str
    threshold: float
    discovery_accuracy: float
    holdout_accuracy: float

    def render(self) -> str:
        return (
            f"{self.family}:{self.feature} {self.comparator} {self.threshold:.4f} "
            f"(discovery={self.discovery_accuracy:.4f}, holdout={self.holdout_accuracy:.4f})"
        )


@dataclass(frozen=True)
class MixedRule:
    operator: str
    source_feature: str
    source_comparator: str
    source_threshold: float
    substrate_feature: str
    substrate_comparator: str
    substrate_threshold: float
    discovery_accuracy: float
    holdout_accuracy: float

    def render(self) -> str:
        return (
            f"{self.source_feature} {self.source_comparator} {self.source_threshold:.4f} "
            f"{self.operator} "
            f"{self.substrate_feature} {self.substrate_comparator} {self.substrate_threshold:.4f} "
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
    rows: list[BridgeRow],
    feature: str,
    comparator: str,
    threshold: float,
) -> list[bool]:
    values = [float(getattr(row, feature)) for row in rows]
    if comparator == ">=":
        return [value >= threshold for value in values]
    return [value <= threshold for value in values]


def _accuracy(rows: list[BridgeRow], predictions: list[bool]) -> float:
    truth = [row.retained_last6 for row in rows]
    return sum(pred == target for pred, target in zip(predictions, truth)) / len(rows)


def _rank_single_rules(
    discovery_rows: list[BridgeRow],
    holdout_rows: list[BridgeRow],
    family: str,
    feature_names: list[str],
    top_n: int = 5,
) -> list[ThresholdRule]:
    candidates: list[ThresholdRule] = []
    for feature in feature_names:
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
                        family=family,
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


def _best_mixed_rule(
    discovery_rows: list[BridgeRow],
    holdout_rows: list[BridgeRow],
    source_feature_names: list[str],
    substrate_feature_names: list[str],
) -> MixedRule:
    best: MixedRule | None = None
    for source_feature, substrate_feature in itertools.product(
        source_feature_names,
        substrate_feature_names,
    ):
        source_values = sorted(set(float(getattr(row, source_feature)) for row in discovery_rows))
        substrate_values = sorted(
            set(float(getattr(row, substrate_feature)) for row in discovery_rows)
        )
        for source_comparator in (">=", "<="):
            for substrate_comparator in (">=", "<="):
                for source_threshold in source_values:
                    discovery_source = _threshold_predictions(
                        discovery_rows,
                        source_feature,
                        source_comparator,
                        source_threshold,
                    )
                    holdout_source = _threshold_predictions(
                        holdout_rows,
                        source_feature,
                        source_comparator,
                        source_threshold,
                    )
                    for substrate_threshold in substrate_values:
                        discovery_substrate = _threshold_predictions(
                            discovery_rows,
                            substrate_feature,
                            substrate_comparator,
                            substrate_threshold,
                        )
                        holdout_substrate = _threshold_predictions(
                            holdout_rows,
                            substrate_feature,
                            substrate_comparator,
                            substrate_threshold,
                        )
                        for operator in ("and", "or"):
                            if operator == "and":
                                discovery_pred = [
                                    left and right
                                    for left, right in zip(
                                        discovery_source,
                                        discovery_substrate,
                                    )
                                ]
                                holdout_pred = [
                                    left and right
                                    for left, right in zip(
                                        holdout_source,
                                        holdout_substrate,
                                    )
                                ]
                            else:
                                discovery_pred = [
                                    left or right
                                    for left, right in zip(
                                        discovery_source,
                                        discovery_substrate,
                                    )
                                ]
                                holdout_pred = [
                                    left or right
                                    for left, right in zip(
                                        holdout_source,
                                        holdout_substrate,
                                    )
                                ]
                            candidate = MixedRule(
                                operator=operator,
                                source_feature=source_feature,
                                source_comparator=source_comparator,
                                source_threshold=source_threshold,
                                substrate_feature=substrate_feature,
                                substrate_comparator=substrate_comparator,
                                substrate_threshold=substrate_threshold,
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


def _evaluate_task(
    task: tuple[
        GraphConfig,
        int,
        float,
        tuple[float, float],
        float,
        int,
        int,
    ],
) -> BridgeRow | None:
    (
        config,
        graph_seed,
        neighbor_radius,
        seed_position,
        source_offset_y,
        steps,
        source_steps,
    ) = task
    mover_rule = next(rule for rule in CANONICAL_RULES if rule.label == "self")
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

    early = [entry for entry in free_tracked[:EARLY_STEPS] if entry[1] is not None]
    if early:
        metrics = [
            _packet_local_metrics(positions, neighbors, packet, packet_centroid)
            for _, packet, packet_centroid, _ in early
        ]
        early_metrics = {
            feature: _mean(metric[feature] for metric in metrics)
            for feature in SUBSTRATE_FEATURES
            if feature != "early_live_fraction"
        }
    else:
        early_metrics = {
            feature: 0.0
            for feature in SUBSTRATE_FEATURES
            if feature != "early_live_fraction"
        }

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
    last6_history = _run_live_history_with_timeline(
        mover_seed=mover_seed,
        neighbors=neighbors,
        positions=positions,
        adj=adj,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        coupling=3.0,
        steps=steps,
        source_window=6,
        source_timeline=source_timeline,
        pre_len=len(pre_source_history),
        n_nodes=len(positions),
    )
    last6_outcome, _, _, _, _, last6_tracked = _classify_outcome(
        positions,
        neighbors,
        last6_history,
    )
    last6_live = [entry for entry in last6_tracked if entry[1] is not None]
    if not last6_live:
        return None

    last6_shift = _signed_shift_at_shared_x(free_live, last6_live, side_sign)
    if not math.isfinite(last6_shift):
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

    return BridgeRow(
        config=config.label,
        graph_seed=graph_seed,
        seed_x=sx,
        seed_y=sy,
        source_offset_y=source_offset_y,
        retained_last6=(last6_outcome == "survive" and last6_shift > 0.0),
        last6_outcome=last6_outcome,
        last6_shift=last6_shift,
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
        early_live_fraction=len(early) / EARLY_STEPS,
        **early_metrics,
    )


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
    source_steps: int,
    neighbor_radius: float,
    source_offsets: list[float],
) -> list[BridgeRow]:
    tasks = [
        (
            config,
            graph_seed,
            neighbor_radius,
            seed_position,
            source_offset_y,
            steps,
            source_steps,
        )
        for config in CANONICAL_CONFIGS
        for graph_seed in seeds
        for seed_position in SEED_POSITIONS
        for source_offset_y in source_offsets
    ]
    if workers <= 1:
        return [row for row in (_evaluate_task(task) for task in tasks) if row is not None]

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return [row for row in pool.map(_evaluate_task, tasks) if row is not None]


def _render_group(rows: list[BridgeRow], label: str, predicate) -> str:
    subset = [row for row in rows if predicate(row)]
    return (
        f"{label}: total={len(subset)} "
        f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
        f"source_corridor={_mean(row.last6_corridor_share for row in subset):.4f} "
        f"extra_field_on_packet={_mean(row.extra_field_mean_on_packet for row in subset):.4f} "
        f"extra_packet_gap={_mean(row.extra_packet_side_gap for row in subset):.4f} "
        f"early_front_load={_mean(row.early_front_load for row in subset):.4f} "
        f"early_band_share={_mean(row.early_band_share for row in subset):.4f} "
        f"early_front_completion={_mean(row.early_front_completion for row in subset):.4f}"
    )


def _render_config_breakdown(rows: list[BridgeRow]) -> list[str]:
    lines = ["Config breakdown:"]
    for config in sorted({row.config for row in rows}):
        subset = [row for row in rows if row.config == config]
        retained = sum(row.retained_last6 for row in subset)
        lines.append(
            "  "
            f"{config}: retained_last6={retained}/{len(subset)} "
            f"mean_last6_shift={_mean(row.last6_shift for row in subset):.4f} "
            f"mean_front_load={_mean(row.early_front_load for row in subset):.4f} "
            f"mean_packet_gap={_mean(row.extra_packet_side_gap for row in subset):.4f}"
        )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--neighbor-radius", type=float, default=2.5)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    rows = run_rows(
        seeds=range(args.seed_start, args.seed_start + args.seed_count),
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        neighbor_radius=args.neighbor_radius,
        source_offsets=[-3.0, 3.0],
    )
    rows.sort(key=lambda row: (row.config, row.graph_seed, row.seed_x, row.seed_y, row.source_offset_y))
    discovery_rows = [row for row in rows if row.config in DISCOVERY_CONFIGS]
    holdout_rows = [row for row in rows if row.config in HOLDOUT_CONFIGS]

    source_rules = _rank_single_rules(
        discovery_rows,
        holdout_rows,
        family="source",
        feature_names=SOURCE_FEATURES,
        top_n=5,
    )
    substrate_rules = _rank_single_rules(
        discovery_rows,
        holdout_rows,
        family="substrate",
        feature_names=SUBSTRATE_FEATURES,
        top_n=5,
    )
    mixed_rule = _best_mixed_rule(
        discovery_rows,
        holdout_rows,
        source_feature_names=[rule.feature for rule in source_rules[:4]],
        substrate_feature_names=[rule.feature for rule in substrate_rules[:4]],
    )

    print("=" * 80)
    print("GENERATED DAG FIELD-TO-PATTERN SUBSTRATE BRIDGE COMPARE")
    print("=" * 80)
    print(
        f"Rows: {len(rows)} self-rule live-source trials, neighbor_radius={args.neighbor_radius:.1f}, "
        f"seeds={args.seed_start}..{args.seed_start + args.seed_count - 1}, "
        f"workers={max(1, args.workers)}"
    )
    print(
        f"Discovery configs: {sorted(DISCOVERY_CONFIGS)}; "
        f"holdout configs: {sorted(HOLDOUT_CONFIGS)}"
    )
    print()
    print(
        "Self last6 retention summary: "
        f"retained_last6={sum(row.retained_last6 for row in rows)}/{len(rows)} "
        f"mean_last6_shift={_mean(row.last6_shift for row in rows):.4f}"
    )
    print()
    print(_render_group(rows, "retained_last6", lambda row: row.retained_last6))
    print(_render_group(rows, "nonretained_last6", lambda row: not row.retained_last6))
    print()
    for line in _render_config_breakdown(rows):
        print(line)
    print()
    print("Top source-side single rules:")
    for rule in source_rules:
        print(f"  {rule.render()}")
    print()
    print("Top substrate-side single rules:")
    for rule in substrate_rules:
        print(f"  {rule.render()}")
    print()
    print("Best mixed source/substrate rule (top-feature pool):")
    print(f"  {mixed_rule.render()}")
    print()
    print("Interpretation:")
    best_source = source_rules[0]
    best_substrate = substrate_rules[0]
    if best_substrate.holdout_accuracy > best_source.holdout_accuracy:
        print(
            "  Free-mover substrate observables transfer better than live-source geometry "
            "on the self branch."
        )
    elif best_substrate.holdout_accuracy < best_source.holdout_accuracy:
        print(
            "  Live-source geometry still transfers better than free-mover substrate "
            "observables on the self branch."
        )
    else:
        print(
            "  Free-mover substrate and live-source geometry tie on holdout transfer "
            "for the self branch."
        )
    if mixed_rule.holdout_accuracy > max(
        best_source.holdout_accuracy,
        best_substrate.holdout_accuracy,
    ):
        print(
            "  A small mixed rule improves holdout transfer, so the self residual is "
            "best read as a combined substrate-plus-source effect."
        )
    else:
        print(
            "  The mixed rule does not materially beat the best single-family holdout, "
            "so the self residual still lacks a strong retained shared closure."
        )


if __name__ == "__main__":
    main()
