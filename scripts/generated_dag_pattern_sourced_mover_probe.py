#!/usr/bin/env python3
"""Probe pattern-sourced deflection on coherent generated-DAG movers.

This replaces the current hand-placed static-mass proxy with a bounded
pattern-sourced field on the exact retained mover substrate:

1. start from coherent free movers only
2. stay on the retained steering substrate (`neighbor_radius = 2.5`)
3. seed a nearby source pattern a little ahead of the free packet path
4. build the field from the union of the source pattern's late active phases
5. ask whether the mover still survives, diffuses, dies, and shifts toward the
   source side under the retained coupling

The goal is not another broad search. It is a direct bridge question:
does pattern-to-pattern deflection already work on the mover substrate, or is
source-pattern viability now the real bottleneck?
"""

from __future__ import annotations

from collections import Counter, defaultdict
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
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


SOURCE_RULE = RuleSpec("self", survive=frozenset({3, 4}), birth=frozenset({3, 4}))


@dataclass(frozen=True)
class PatternCoupledTrialRow:
    config: str
    graph_seed: int
    neighbor_radius: float
    seed_x: float
    seed_y: float
    mover_rule: str
    source_rule: str
    coupling: float
    source_offset_y: float
    source_status: str
    source_union_size: int
    source_live_fraction: float
    source_mean_size: float
    source_peak_size: int
    coupled_outcome: str
    signed_toward_shift: float
    mean_field_on_seed: float
    max_field_on_seed: float


def choose_seed_nodes(
    positions: list[tuple[float, float]],
    target_x: float,
    target_y: float,
    count: int = 5,
) -> frozenset[int]:
    ranked = sorted(
        range(len(positions)),
        key=lambda idx: (
            math.dist(positions[idx], (target_x, target_y)),
            abs(positions[idx][0] - target_x),
        ),
    )
    return frozenset(ranked[:count])


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _source_summary(
    history: list[frozenset[int]],
    source_window: int,
) -> tuple[str, frozenset[int], float, float, int]:
    late_states = history[-source_window:]
    late_live_states = [state for state in late_states if state]
    source_union = frozenset().union(*late_live_states) if late_live_states else frozenset()
    live_fraction = len(late_live_states) / max(1, source_window)
    mean_size = _mean(len(state) for state in late_live_states)
    peak_size = max((len(state) for state in late_live_states), default=0)

    if not late_live_states:
        status = "dead"
    elif len(source_union) < 3:
        status = "collapsed"
    elif len(late_live_states) == source_window:
        status = "persistent"
    else:
        status = "intermittent"
    return status, source_union, live_fraction, mean_size, peak_size


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
) -> PatternCoupledTrialRow | None:
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
    source_seed = choose_seed_nodes(
        positions,
        target_x=anchor[2][0] + 2.0,
        target_y=anchor[2][1] + source_offset_y,
    )
    source_history = evolve_on_graph(
        n_nodes=len(positions),
        neighbors=neighbors,
        seed=source_seed,
        survive=SOURCE_RULE.survive,
        birth=SOURCE_RULE.birth,
        steps=source_steps,
    )
    source_status, source_union, source_live_fraction, source_mean_size, source_peak_size = (
        _source_summary(source_history, source_window)
    )
    if source_union:
        field = compute_field_on_dag(positions, adj, source_union)
    else:
        field = {node: 0.0 for node in range(len(positions))}

    coupled_history = evolve_gradient_coupled(
        neighbors=neighbors,
        seed=mover_seed,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        field=field,
        coupling=coupling,
        steps=steps,
    )
    coupled_outcome, _, _, _, _, coupled_tracked = _classify_outcome(
        positions,
        neighbors,
        coupled_history,
    )
    coupled_live = [entry for entry in coupled_tracked if entry[1] is not None]

    if coupled_live:
        compare_step = min(len(free_live), len(coupled_live)) - 1
        signed_toward_shift = (
            coupled_live[compare_step][2][1] - free_live[compare_step][2][1]
        ) * (1.0 if source_offset_y > 0.0 else -1.0)
    else:
        signed_toward_shift = float("nan")

    return PatternCoupledTrialRow(
        config=config.label,
        graph_seed=graph_seed,
        neighbor_radius=neighbor_radius,
        seed_x=sx,
        seed_y=sy,
        mover_rule=mover_rule.label,
        source_rule=SOURCE_RULE.label,
        coupling=coupling,
        source_offset_y=source_offset_y,
        source_status=source_status,
        source_union_size=len(source_union),
        source_live_fraction=source_live_fraction,
        source_mean_size=source_mean_size,
        source_peak_size=source_peak_size,
        coupled_outcome=coupled_outcome,
        signed_toward_shift=signed_toward_shift,
        mean_field_on_seed=_mean(field.get(node, 0.0) for node in mover_seed),
        max_field_on_seed=max((field.get(node, 0.0) for node in mover_seed), default=0.0),
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
) -> list[PatternCoupledTrialRow]:
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


def _render_status_breakdown(rows: list[PatternCoupledTrialRow]) -> list[str]:
    lines = ["Source-status breakdown:"]
    buckets: dict[str, list[PatternCoupledTrialRow]] = defaultdict(list)
    for row in rows:
        buckets[row.source_status].append(row)
    for status in sorted(buckets):
        subset = buckets[status]
        shifts = [row.signed_toward_shift for row in subset if math.isfinite(row.signed_toward_shift)]
        coupled_counts = Counter(row.coupled_outcome for row in subset)
        lines.append(
            "  "
            f"{status}: total={len(subset)} "
            f"survive={coupled_counts.get('survive', 0)} "
            f"diffuse={coupled_counts.get('diffuse', 0)} "
            f"die={coupled_counts.get('die', 0)} "
            f"mean_union={_mean(row.source_union_size for row in subset):.2f} "
            f"mean_live_fraction={_mean(row.source_live_fraction for row in subset):.4f} "
            f"mean_signed_shift={_mean(shifts):.4f}"
        )
    return lines


def _render_breakdown(
    rows: list[PatternCoupledTrialRow],
    key_name: str,
    getter,
) -> list[str]:
    lines = [f"Viable-source breakdown by {key_name}:"]
    buckets: dict[object, list[PatternCoupledTrialRow]] = defaultdict(list)
    for row in rows:
        buckets[getter(row)].append(row)
    for key in sorted(buckets, key=str):
        subset = buckets[key]
        shifts = [row.signed_toward_shift for row in subset if math.isfinite(row.signed_toward_shift)]
        counts = Counter(row.coupled_outcome for row in subset)
        lines.append(
            "  "
            f"{key}: total={len(subset)} "
            f"survive={counts.get('survive', 0)} "
            f"diffuse={counts.get('diffuse', 0)} "
            f"die={counts.get('die', 0)} "
            f"mean_signed_shift={_mean(shifts):.4f}"
        )
    return lines


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

    source_offsets = [-3.0, 3.0]
    seeds = range(args.seed_start, args.seed_start + args.seed_count)
    rows = run_rows(
        seeds=seeds,
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        source_window=args.source_window,
        coupling=args.coupling,
        neighbor_radius=args.neighbor_radius,
        source_offsets=source_offsets,
    )
    rows.sort(
        key=lambda row: (
            row.config,
            row.graph_seed,
            row.seed_x,
            row.seed_y,
            row.mover_rule,
            row.source_offset_y,
        )
    )

    all_counts = Counter(row.coupled_outcome for row in rows)
    all_shifts = [row.signed_toward_shift for row in rows if math.isfinite(row.signed_toward_shift)]
    viable_rows = [row for row in rows if row.source_status != "dead" and row.source_union_size >= 3]
    viable_counts = Counter(row.coupled_outcome for row in viable_rows)
    viable_shifts = [
        row.signed_toward_shift for row in viable_rows if math.isfinite(row.signed_toward_shift)
    ]

    print("=" * 80)
    print("GENERATED DAG PATTERN-SOURCED MOVER PROBE")
    print("=" * 80)
    print(
        f"Seeds: {args.seed_start}..{args.seed_start + args.seed_count - 1} "
        f"({args.seed_count} per config), steps={args.steps}, workers={max(1, args.workers)}"
    )
    print(
        "Free substrate: coherent movers only on the retained steering substrate "
        f"(neighbor_radius={args.neighbor_radius:.1f})"
    )
    print(
        f"Coupling: retained mover value {args.coupling:.3f}; "
        f"source rule={SOURCE_RULE.label}; offsets={source_offsets}; "
        f"source_steps={args.source_steps}; late_window={args.source_window}"
    )
    print(f"Free coherent mover trials: {len(rows)}")
    print()
    print("All pattern-sourced trials:")
    print(
        "  "
        f"survive={all_counts.get('survive', 0)} "
        f"diffuse={all_counts.get('diffuse', 0)} "
        f"die={all_counts.get('die', 0)} "
        f"mean_signed_shift={_mean(all_shifts):.4f} "
        f"positive_shifts={sum(shift > 0.0 for shift in all_shifts)}/{len(all_shifts)}"
    )
    print()
    for line in _render_status_breakdown(rows):
        print(line)
    print()
    print("Viable-source subset (union >= 3 and not dead):")
    print(
        "  "
        f"total={len(viable_rows)} "
        f"survive={viable_counts.get('survive', 0)} "
        f"diffuse={viable_counts.get('diffuse', 0)} "
        f"die={viable_counts.get('die', 0)} "
        f"mean_signed_shift={_mean(viable_shifts):.4f} "
        f"positive_shifts={sum(shift > 0.0 for shift in viable_shifts)}/{len(viable_shifts)}"
    )
    print()
    for line in _render_breakdown(viable_rows, "config", lambda row: row.config):
        print(line)
    print()
    for line in _render_breakdown(viable_rows, "mover_rule", lambda row: row.mover_rule):
        print(line)
    print()
    print("Interpretation:")
    print(
        "  This bounded probe asks whether the retained mover substrate still bends "
        "once the static mass is replaced by a late-phase source pattern. The main "
        "question is whether deflection survives at all, or whether source-pattern "
        "viability becomes the dominant bottleneck."
    )
    print(
        "  The viable-source subset is the right checkpoint for that question: it "
        "filters out rows where the nearby source never supplies enough late active "
        "support to build a meaningful field on the DAG."
    )


if __name__ == "__main__":
    main()
