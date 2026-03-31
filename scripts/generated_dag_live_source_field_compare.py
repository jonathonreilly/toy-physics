#!/usr/bin/env python3
"""Compare frozen and live recent-source steering on generated-DAG movers.

This probe tests the next stronger version of the current pattern-sourced
steering story:

1. keep the same mature source state used by the frozen-footprint result
2. compare a frozen field built from the recent source window against
3. a live field built from a sliding version of that same source window
   while the mover runs

This directly targets the field-to-pattern gap identified in the architecture
audit without reopening a broad parameter search.
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

from scripts.generated_dag_packet_tracking_bridge_compare import (  # noqa: E402
    CANONICAL_CONFIGS,
    CANONICAL_RULES,
    SEED_POSITIONS,
    GraphConfig,
    RuleSpec,
    _classify_outcome,
)
from scripts.generated_dag_pattern_mobility import (  # noqa: E402
    build_spatial_neighbors,
    evolve_on_graph,
)
from scripts.generated_dag_pattern_sourced_mover_probe import (  # noqa: E402
    SOURCE_RULE,
    _signed_shift_at_shared_x,
    choose_seed_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


@dataclass(frozen=True)
class LiveSourceCompareRow:
    source_mode: str
    source_window: int
    config: str
    graph_seed: int
    seed_x: float
    seed_y: float
    mover_rule: str
    source_offset_y: float
    source_status: str
    source_union_size: int
    source_live_fraction: float
    coupled_outcome: str
    signed_toward_shift: float
    mean_field_on_seed: float
    max_field_on_seed: float


@dataclass(frozen=True)
class ModeSummary:
    source_mode: str
    total: int
    viable_sources: int
    survive: int
    diffuse: int
    die: int
    positive_shifts: int
    mean_signed_shift: float

    @property
    def coherent_fraction(self) -> float:
        return self.survive / self.total if self.total else 0.0

    @property
    def directional_score(self) -> float:
        return self.coherent_fraction * max(self.mean_signed_shift, 0.0)

    def render(self) -> str:
        return (
            f"{self.source_mode}: total={self.total} viable_sources={self.viable_sources}/{self.total} "
            f"survive={self.survive} diffuse={self.diffuse} die={self.die} "
            f"positive_shifts={self.positive_shifts}/{self.total} "
            f"mean_signed_shift={self.mean_signed_shift:.4f} "
            f"directional_score={self.directional_score:.4f}"
        )


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _step_graph(
    active: frozenset[int],
    neighbors: dict[int, list[int]],
    survive: frozenset[int],
    birth: frozenset[int],
) -> frozenset[int]:
    counts: dict[int, int] = {}
    for node in active:
        for nb in neighbors.get(node, []):
            counts[nb] = counts.get(nb, 0) + 1

    new_active: set[int] = set()
    candidates = set(active)
    for node in active:
        candidates.update(neighbors.get(node, []))

    for node in candidates:
        count = counts.get(node, 0)
        if node in active:
            if count in survive:
                new_active.add(node)
        elif count in birth:
            new_active.add(node)
    return frozenset(new_active)


def _step_gradient_coupled(
    active: frozenset[int],
    neighbors: dict[int, list[int]],
    survive: frozenset[int],
    birth: frozenset[int],
    field: dict[int, float],
    coupling: float,
) -> frozenset[int]:
    counts: dict[int, int] = {}
    for node in active:
        for nb in neighbors.get(node, []):
            counts[nb] = counts.get(nb, 0) + 1

    new_active: set[int] = set()
    candidates = set(active)
    threshold_minus_one = {value - 1 for value in birth if value > 0}
    for node in active:
        candidates.update(neighbors.get(node, []))

    for node in candidates:
        count = counts.get(node, 0)
        if node in active:
            if count in survive:
                new_active.add(node)
            continue

        if count in birth:
            new_active.add(node)
            continue

        if coupling <= 0.0 or count not in threshold_minus_one:
            continue

        active_neighbors = [nb for nb in neighbors.get(node, []) if nb in active]
        if not active_neighbors:
            continue

        my_field = field.get(node, 0.0)
        mean_neighbor_field = (
            sum(field.get(nb, 0.0) for nb in active_neighbors) / len(active_neighbors)
        )
        if my_field > mean_neighbor_field + coupling * 0.01:
            new_active.add(node)
    return frozenset(new_active)


def _pre_evolve_source(
    seed: frozenset[int],
    neighbors: dict[int, list[int]],
    source_steps: int,
) -> tuple[list[frozenset[int]], frozenset[int]]:
    history: list[frozenset[int]] = []
    active = seed
    for _ in range(source_steps):
        history.append(active)
        active = _step_graph(
            active,
            neighbors,
            SOURCE_RULE.survive,
            SOURCE_RULE.birth,
        )
    return history, active


def _status_from_recent_states(
    states: list[frozenset[int]],
) -> tuple[str, frozenset[int], float]:
    recent_live = [state for state in states if state]
    source_union = frozenset().union(*recent_live) if recent_live else frozenset()
    live_fraction = len(recent_live) / max(1, len(states))
    if not recent_live:
        status = "dead"
    elif len(source_union) < 3:
        status = "collapsed"
    elif len(recent_live) == len(states):
        status = "persistent"
    else:
        status = "intermittent"
    return status, source_union, live_fraction


def _run_static_field_history(
    seed: frozenset[int],
    neighbors: dict[int, list[int]],
    survive: frozenset[int],
    birth: frozenset[int],
    field: dict[int, float],
    coupling: float,
    steps: int,
) -> list[frozenset[int]]:
    active = seed
    history: list[frozenset[int]] = []
    for _ in range(steps):
        history.append(active)
        active = _step_gradient_coupled(
            active,
            neighbors,
            survive,
            birth,
            field,
            coupling,
        )
    return history


def _run_live_field_history(
    mover_seed: frozenset[int],
    source_history: list[frozenset[int]],
    source_active: frozenset[int],
    positions: list[tuple[float, float]],
    neighbors: dict[int, list[int]],
    adj: dict[int, list[int]],
    survive: frozenset[int],
    birth: frozenset[int],
    coupling: float,
    steps: int,
    source_window: int,
    n_nodes: int,
) -> tuple[list[frozenset[int]], list[frozenset[int]]]:
    mover_active = mover_seed
    mover_history: list[frozenset[int]] = []
    live_source_history = list(source_history)
    current_source_active = source_active

    for _ in range(steps):
        mover_history.append(mover_active)
        field_nodes = frozenset().union(
            *(state for state in live_source_history[-source_window:] if state)
        )
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
        live_source_history.append(current_source_active)
        current_source_active = _step_graph(
            current_source_active,
            neighbors,
            SOURCE_RULE.survive,
            SOURCE_RULE.birth,
        )

    return mover_history, live_source_history


def _evaluate_task(
    task: tuple[
        GraphConfig,
        int,
        tuple[float, float],
        RuleSpec,
        float,
        int,
        int,
        float,
        int,
    ],
) -> list[LiveSourceCompareRow]:
    (
        config,
        graph_seed,
        seed_position,
        mover_rule,
        source_offset_y,
        steps,
        source_steps,
        coupling,
        source_window,
    ) = task
    positions, adj, _ = generate_causal_dag(
        n_layers=config.n_layers,
        nodes_per_layer=config.nodes_per_layer,
        y_range=config.y_range,
        connect_radius=config.connect_radius,
        rng_seed=graph_seed,
    )
    neighbors = build_spatial_neighbors(positions, 2.5)

    mover_seed = choose_seed_nodes(positions, *seed_position)
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
        return []

    free_live = [entry for entry in free_tracked if entry[1] is not None]
    anchor = free_live[min(12, len(free_live) - 1)]
    source_seed = choose_seed_nodes(
        positions,
        target_x=anchor[2][0] + 2.0,
        target_y=anchor[2][1] + source_offset_y,
    )

    pre_source_history, current_source_active = _pre_evolve_source(
        source_seed,
        neighbors,
        source_steps,
    )
    frozen_recent = pre_source_history[-source_window:]
    frozen_status, frozen_union, frozen_live_fraction = _status_from_recent_states(
        frozen_recent
    )
    if len(frozen_union) < 3:
        return []

    side_sign = 1.0 if source_offset_y > 0.0 else -1.0
    frozen_field = compute_field_on_dag(positions, adj, frozen_union)
    frozen_mover_history = _run_static_field_history(
        seed=mover_seed,
        neighbors=neighbors,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        field=frozen_field,
        coupling=coupling,
        steps=steps,
    )
    frozen_outcome, _, _, _, _, frozen_tracked = _classify_outcome(
        positions,
        neighbors,
        frozen_mover_history,
    )
    frozen_live = [entry for entry in frozen_tracked if entry[1] is not None]
    frozen_shift = (
        _signed_shift_at_shared_x(free_live, frozen_live, side_sign)
        if frozen_live
        else float("nan")
    )

    live_mover_history, live_source_history = _run_live_field_history(
        mover_seed=mover_seed,
        source_history=pre_source_history,
        source_active=current_source_active,
        positions=positions,
        neighbors=neighbors,
        adj=adj,
        survive=mover_rule.survive,
        birth=mover_rule.birth,
        coupling=coupling,
        steps=steps,
        source_window=source_window,
        n_nodes=len(positions),
    )
    live_recent = live_source_history[-source_window:]
    live_status, live_union, live_live_fraction = _status_from_recent_states(live_recent)
    live_outcome, _, _, _, _, live_tracked = _classify_outcome(
        positions,
        neighbors,
        live_mover_history,
    )
    live_live = [entry for entry in live_tracked if entry[1] is not None]
    live_shift = (
        _signed_shift_at_shared_x(free_live, live_live, side_sign)
        if live_live
        else float("nan")
    )
    if live_union:
        live_field = compute_field_on_dag(positions, adj, live_union)
    else:
        live_field = {node: 0.0 for node in range(len(positions))}

    return [
        LiveSourceCompareRow(
            source_mode=f"frozen_last{source_window}_union",
            source_window=source_window,
            config=config.label,
            graph_seed=graph_seed,
            seed_x=seed_position[0],
            seed_y=seed_position[1],
            mover_rule=mover_rule.label,
            source_offset_y=source_offset_y,
            source_status=frozen_status,
            source_union_size=len(frozen_union),
            source_live_fraction=frozen_live_fraction,
            coupled_outcome=frozen_outcome,
            signed_toward_shift=frozen_shift,
            mean_field_on_seed=_mean(frozen_field.get(node, 0.0) for node in mover_seed),
            max_field_on_seed=max((frozen_field.get(node, 0.0) for node in mover_seed), default=0.0),
        ),
        LiveSourceCompareRow(
            source_mode=f"live_sliding_last{source_window}",
            source_window=source_window,
            config=config.label,
            graph_seed=graph_seed,
            seed_x=seed_position[0],
            seed_y=seed_position[1],
            mover_rule=mover_rule.label,
            source_offset_y=source_offset_y,
            source_status=live_status,
            source_union_size=len(live_union),
            source_live_fraction=live_live_fraction,
            coupled_outcome=live_outcome,
            signed_toward_shift=live_shift,
            mean_field_on_seed=_mean(live_field.get(node, 0.0) for node in mover_seed),
            max_field_on_seed=max((live_field.get(node, 0.0) for node in mover_seed), default=0.0),
        ),
    ]


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
    source_steps: int,
    coupling: float,
    source_window: int,
    source_offsets: list[float],
) -> list[LiveSourceCompareRow]:
    tasks = [
        (
            config,
            graph_seed,
            seed_position,
            mover_rule,
            source_offset_y,
            steps,
            source_steps,
            coupling,
            source_window,
        )
        for config in CANONICAL_CONFIGS
        for graph_seed in seeds
        for seed_position in SEED_POSITIONS
        for mover_rule in CANONICAL_RULES
        for source_offset_y in source_offsets
    ]
    if workers <= 1:
        return [row for task in tasks for row in _evaluate_task(task)]

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return [row for rows in pool.map(_evaluate_task, tasks) for row in rows]


def summarize(rows: list[LiveSourceCompareRow]) -> list[ModeSummary]:
    summaries: list[ModeSummary] = []
    for source_mode in sorted(set(row.source_mode for row in rows)):
        subset = [row for row in rows if row.source_mode == source_mode]
        counts = Counter(row.coupled_outcome for row in subset)
        shifts = [
            row.signed_toward_shift
            for row in subset
            if math.isfinite(row.signed_toward_shift)
        ]
        summaries.append(
            ModeSummary(
                source_mode=source_mode,
                total=len(subset),
                viable_sources=sum(row.source_union_size >= 3 for row in subset),
                survive=counts.get("survive", 0),
                diffuse=counts.get("diffuse", 0),
                die=counts.get("die", 0),
                positive_shifts=sum(shift > 0.0 for shift in shifts),
                mean_signed_shift=_mean(shifts),
            )
        )
    return summaries


def _render_breakdown(
    rows: list[LiveSourceCompareRow],
    source_mode: str,
    key_name: str,
    getter,
) -> list[str]:
    lines = [f"{source_mode} breakdown by {key_name}:"]
    buckets: dict[object, list[LiveSourceCompareRow]] = defaultdict(list)
    for row in rows:
        if row.source_mode == source_mode:
            buckets[getter(row)].append(row)
    for key in sorted(buckets, key=str):
        subset = buckets[key]
        counts = Counter(row.coupled_outcome for row in subset)
        shifts = [
            row.signed_toward_shift
            for row in subset
            if math.isfinite(row.signed_toward_shift)
        ]
        lines.append(
            "  "
            f"{key}: total={len(subset)} "
            f"survive={counts.get('survive', 0)} "
            f"diffuse={counts.get('diffuse', 0)} "
            f"die={counts.get('die', 0)} "
            f"mean_signed_shift={_mean(shifts):.4f}"
        )
    return lines


def _render_paired_delta(rows: list[LiveSourceCompareRow]) -> list[str]:
    lines = ["Paired live-vs-frozen deltas (same task rows):"]
    paired: dict[tuple[object, ...], dict[str, LiveSourceCompareRow]] = defaultdict(dict)
    for row in rows:
        key = (
            row.config,
            row.graph_seed,
            row.seed_x,
            row.seed_y,
            row.mover_rule,
            row.source_offset_y,
            row.source_window,
        )
        paired[key][row.source_mode] = row
    deltas = []
    live_better = 0
    frozen_better = 0
    for pair in paired.values():
        frozen = next((row for mode, row in pair.items() if mode.startswith("frozen_")), None)
        live = next((row for mode, row in pair.items() if mode.startswith("live_")), None)
        if frozen is None or live is None:
            continue
        if math.isfinite(frozen.signed_toward_shift) and math.isfinite(live.signed_toward_shift):
            delta = live.signed_toward_shift - frozen.signed_toward_shift
            deltas.append(delta)
            if delta > 0.0:
                live_better += 1
            elif delta < 0.0:
                frozen_better += 1
    lines.append(
        "  "
        f"paired_rows={len(deltas)} mean_delta={_mean(deltas):.4f} "
        f"live_more_toward={live_better} frozen_more_toward={frozen_better}"
    )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-start", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=5)
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--source-steps", type=int, default=12)
    parser.add_argument("--source-window", type=int, default=3)
    parser.add_argument("--coupling", type=float, default=3.0)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    args = parser.parse_args()

    rows = run_rows(
        seeds=range(args.seed_start, args.seed_start + args.seed_count),
        workers=max(1, args.workers),
        steps=args.steps,
        source_steps=args.source_steps,
        coupling=args.coupling,
        source_window=args.source_window,
        source_offsets=[-3.0, 3.0],
    )
    rows.sort(
        key=lambda row: (
            row.source_mode,
            row.config,
            row.graph_seed,
            row.mover_rule,
            row.source_offset_y,
        )
    )
    summaries = summarize(rows)

    print("=" * 80)
    print("GENERATED DAG LIVE SOURCE FIELD COMPARE")
    print("=" * 80)
    print(
        f"Seeds: {args.seed_start}..{args.seed_start + args.seed_count - 1} "
        f"({args.seed_count} per config), steps={args.steps}, source_steps={args.source_steps}, "
        f"source_window={args.source_window}, coupling={args.coupling:.3f}, "
        f"workers={max(1, args.workers)}"
    )
    print(
        "Question: on the retained mover substrate, how much of the current "
        "pattern-sourced steering survives if the source keeps evolving during the run "
        f"instead of being frozen as a recent `last{args.source_window}_union` footprint?"
    )
    print()
    print("Mode summaries:")
    for summary in summaries:
        print(f"  {summary.render()}")
    print()
    for line in _render_paired_delta(rows):
        print(line)
    print()
    for source_mode in sorted(set(row.source_mode for row in rows)):
        for line in _render_breakdown(rows, source_mode, "config", lambda row: row.config):
            print(line)
        print()
        for line in _render_breakdown(rows, source_mode, "rule", lambda row: row.mover_rule):
            print(line)
        print()
    print("Interpretation:")
    print(
        "  This is a direct test of the field-to-pattern gap from the architecture "
        "audit. The frozen retained source and the live sliding source use the same "
        "mature source packet and the same recent-footprint language; the only change "
        "is whether the source field is held fixed or regenerated during the mover run."
    )
    print(
        "  If the live mode stays comparable to the frozen mode, then the retained "
        "pattern-sourced steering result already survives a stronger same-framework "
        "version. If it weakens materially, then part of the current steering story is "
        "still living on the frozen-source surrogate."
    )


if __name__ == "__main__":
    main()
