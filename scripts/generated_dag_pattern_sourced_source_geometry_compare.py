#!/usr/bin/env python3
"""Compare source-geometry observables on pattern-sourced mover trials.

The bounded question is whether the first pattern-sourced mover result fails
because the nearby source pattern drifts off the intended side, or because the
current coupling responds differently to a valid pattern-sourced field than it
did to the earlier static-mass proxy.
"""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import argparse
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
    _signed_shift_at_shared_x,
    _source_summary,
    choose_seed_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


@dataclass(frozen=True)
class SourceGeometryRow:
    config: str
    graph_seed: int
    mover_rule: str
    source_offset_y: float
    positive_shift: bool
    signed_toward_shift: float
    source_status: str
    source_union_size: int
    source_signed_side: float
    source_x_lead: float
    mean_field_on_seed: float
    max_field_on_seed: float


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


def _best_threshold(
    rows: list[SourceGeometryRow],
    feature: str,
) -> tuple[str, float, float]:
    values = sorted(set(float(getattr(row, feature)) for row in rows))
    best_accuracy = -1.0
    best_comparator = ">="
    best_threshold = values[0]
    truth = [row.positive_shift for row in rows]
    for comparator in (">=", "<="):
        for threshold in values:
            if comparator == ">=":
                pred = [float(getattr(row, feature)) >= threshold for row in rows]
            else:
                pred = [float(getattr(row, feature)) <= threshold for row in rows]
            accuracy = sum(p == t for p, t in zip(pred, truth)) / len(rows)
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_comparator = comparator
                best_threshold = threshold
    return best_comparator, best_threshold, best_accuracy


def _evaluate_trial(
    task: tuple[GraphConfig, int, float, tuple[float, float], RuleSpec, float, float, int, int, int],
) -> SourceGeometryRow | None:
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
    anchor_centroid = anchor[2]

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

    source_centroid = _centroid(positions, source_union)
    field = compute_field_on_dag(positions, adj, source_union)
    coupled_history = evolve_gradient_coupled(
        neighbors=neighbors,
        seed=mover_seed,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        field=field,
        coupling=coupling,
        steps=steps,
    )
    _, _, _, _, _, coupled_tracked = _classify_outcome(positions, neighbors, coupled_history)
    coupled_live = [entry for entry in coupled_tracked if entry[1] is not None]
    if coupled_live:
        signed_toward_shift = _signed_shift_at_shared_x(
            free_live,
            coupled_live,
            1.0 if source_offset_y > 0.0 else -1.0,
        )
    else:
        signed_toward_shift = float("nan")

    side_sign = 1.0 if source_offset_y > 0.0 else -1.0
    return SourceGeometryRow(
        config=config.label,
        graph_seed=graph_seed,
        mover_rule=mover_rule.label,
        source_offset_y=source_offset_y,
        positive_shift=math.isfinite(signed_toward_shift) and signed_toward_shift > 0.0,
        signed_toward_shift=signed_toward_shift,
        source_status=source_status,
        source_union_size=len(source_union),
        source_signed_side=(source_centroid[1] - anchor_centroid[1]) * side_sign,
        source_x_lead=source_centroid[0] - anchor_centroid[0],
        mean_field_on_seed=_mean(field.get(node, 0.0) for node in mover_seed),
        max_field_on_seed=max(field.get(node, 0.0) for node in mover_seed),
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
) -> list[SourceGeometryRow]:
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


def _render_group(rows: list[SourceGeometryRow], label: str) -> str:
    return (
        f"{label}: total={len(rows)} "
        f"mean_shift={_mean(row.signed_toward_shift for row in rows):.4f} "
        f"mean_source_signed_side={_mean(row.source_signed_side for row in rows):.4f} "
        f"mean_source_x_lead={_mean(row.source_x_lead for row in rows):.4f} "
        f"mean_union={_mean(row.source_union_size for row in rows):.2f} "
        f"mean_field_on_seed={_mean(row.mean_field_on_seed for row in rows):.4f}"
    )


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

    positive_rows = [row for row in rows if row.positive_shift]
    nonpositive_rows = [row for row in rows if not row.positive_shift]
    print("=" * 80)
    print("GENERATED DAG PATTERN-SOURCED SOURCE GEOMETRY COMPARE")
    print("=" * 80)
    print(
        f"Rows: {len(rows)} viable-source mover trials on neighbor_radius={args.neighbor_radius:.1f}, "
        f"coupling={args.coupling:.3f}"
    )
    print()
    print(_render_group(positive_rows, "positive_shift"))
    print(_render_group(nonpositive_rows, "nonpositive_shift"))
    print()
    counts = Counter(row.config for row in positive_rows)
    print("Positive-shift counts by config:")
    for key in sorted(counts):
        print(f"  {key}: {counts[key]}")
    print()
    for feature in (
        "source_signed_side",
        "source_x_lead",
        "source_union_size",
        "mean_field_on_seed",
    ):
        comparator, threshold, accuracy = _best_threshold(rows, feature)
        print(
            f"best {feature} threshold: {feature} {comparator} {threshold:.4f} "
            f"(accuracy={accuracy:.4f})"
        )
    print()
    print("Interpretation:")
    print(
        "  If negative-shift rows still keep the source centroid on the intended side "
        "with a similar forward lead, then the current pattern-sourced result is not a "
        "simple placement failure. It means the mover responds differently to a broad "
        "late-phase source field than to the earlier static-mass proxy."
    )


if __name__ == "__main__":
    main()
