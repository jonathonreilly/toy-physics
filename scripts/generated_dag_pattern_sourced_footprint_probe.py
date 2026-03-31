#!/usr/bin/env python3
"""Compare late-source footprint choices on pattern-sourced mover steering.

The first pattern-sourced probe used the union of the last 6 live source states.
The follow-up field-bias compare suggested that the active problem is broad
late-source geometry rather than source viability. This bounded probe keeps the
same mover substrate, source rule, and coupling, and only changes how the late
source footprint is turned into a field:

- last live state
- union of last 2 live states
- union of last 3 live states
- union of last 6 live states (current baseline)
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
from scripts.generated_dag_pattern_sourced_mover_probe import (  # noqa: E402
    SOURCE_RULE,
    choose_seed_nodes,
)
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402
from scripts.generative_dag_gravity import compute_field_on_dag  # noqa: E402


FOOTPRINT_WINDOWS = [
    ("last_state", 1),
    ("last2_union", 2),
    ("last3_union", 3),
    ("last6_union", 6),
]


@dataclass(frozen=True)
class FootprintTrialRow:
    footprint: str
    config: str
    graph_seed: int
    mover_rule: str
    source_offset_y: float
    source_footprint_size: int
    coupled_outcome: str
    signed_toward_shift: float
    mean_field_on_seed: float
    max_field_on_seed: float


@dataclass(frozen=True)
class FootprintSummary:
    footprint: str
    total: int
    survive: int
    diffuse: int
    die: int
    positive_shifts: int
    mean_signed_shift: float

    @property
    def survive_fraction(self) -> float:
        return self.survive / self.total if self.total else 0.0

    @property
    def directional_score(self) -> float:
        return self.survive_fraction * max(self.mean_signed_shift, 0.0)

    def render(self) -> str:
        return (
            f"{self.footprint}: total={self.total} "
            f"survive={self.survive} diffuse={self.diffuse} die={self.die} "
            f"positive_shifts={self.positive_shifts}/{self.total} "
            f"mean_signed_shift={self.mean_signed_shift:.4f} "
            f"directional_score={self.directional_score:.4f}"
        )


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _late_footprint(
    late_live_states: list[frozenset[int]],
    window: int,
) -> frozenset[int]:
    subset = late_live_states[-window:]
    if not subset:
        return frozenset()
    return frozenset().union(*subset)


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
) -> list[FootprintTrialRow]:
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
        return []

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
    late_live_states = [state for state in source_history[-6:] if state]
    if not late_live_states:
        return []

    rows: list[FootprintTrialRow] = []
    side_sign = 1.0 if source_offset_y > 0.0 else -1.0
    for footprint_label, footprint_window in FOOTPRINT_WINDOWS:
        source_footprint = _late_footprint(late_live_states, footprint_window)
        if len(source_footprint) < 3:
            continue

        field = compute_field_on_dag(positions, adj, source_footprint)
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
            ) * side_sign
        else:
            signed_toward_shift = float("nan")

        rows.append(
            FootprintTrialRow(
                footprint=footprint_label,
                config=config.label,
                graph_seed=graph_seed,
                mover_rule=mover_rule.label,
                source_offset_y=source_offset_y,
                source_footprint_size=len(source_footprint),
                coupled_outcome=coupled_outcome,
                signed_toward_shift=signed_toward_shift,
                mean_field_on_seed=_mean(field.get(node, 0.0) for node in mover_seed),
                max_field_on_seed=max(field.get(node, 0.0) for node in mover_seed),
            )
        )
    return rows


def run_rows(
    seeds: Iterable[int],
    workers: int,
    steps: int,
    source_steps: int,
    coupling: float,
    neighbor_radius: float,
    source_offsets: list[float],
) -> list[FootprintTrialRow]:
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
        return [row for task in tasks for row in _evaluate_task(task)]

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        return [row for rows in pool.map(_evaluate_task, tasks) for row in rows]


def summarize(rows: list[FootprintTrialRow]) -> list[FootprintSummary]:
    summaries: list[FootprintSummary] = []
    for footprint in [label for label, _ in FOOTPRINT_WINDOWS]:
        subset = [row for row in rows if row.footprint == footprint]
        counts = Counter(row.coupled_outcome for row in subset)
        shifts = [row.signed_toward_shift for row in subset if math.isfinite(row.signed_toward_shift)]
        summaries.append(
            FootprintSummary(
                footprint=footprint,
                total=len(subset),
                survive=counts.get("survive", 0),
                diffuse=counts.get("diffuse", 0),
                die=counts.get("die", 0),
                positive_shifts=sum(shift > 0.0 for shift in shifts),
                mean_signed_shift=_mean(shifts),
            )
        )
    return summaries


def _render_breakdown(rows: list[FootprintTrialRow], footprint: str, key_name: str, getter) -> list[str]:
    lines = [f"{footprint} breakdown by {key_name}:"]
    buckets: dict[object, list[FootprintTrialRow]] = defaultdict(list)
    for row in rows:
        if row.footprint == footprint:
            buckets[getter(row)].append(row)
    for key in sorted(buckets, key=str):
        subset = buckets[key]
        counts = Counter(row.coupled_outcome for row in subset)
        shifts = [row.signed_toward_shift for row in subset if math.isfinite(row.signed_toward_shift)]
        lines.append(
            "  "
            f"{key}: total={len(subset)} "
            f"survive={counts.get('survive', 0)} diffuse={counts.get('diffuse', 0)} "
            f"die={counts.get('die', 0)} mean_signed_shift={_mean(shifts):.4f}"
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
    rows.sort(key=lambda row: (row.footprint, row.config, row.graph_seed, row.mover_rule, row.source_offset_y))

    summaries = summarize(rows)
    retained = max(summaries, key=lambda summary: summary.directional_score)

    print("=" * 80)
    print("GENERATED DAG PATTERN-SOURCED FOOTPRINT PROBE")
    print("=" * 80)
    print(
        f"Rows: coherent free movers only on neighbor_radius={args.neighbor_radius:.1f}, "
        f"coupling={args.coupling:.3f}, seeds={args.seed_start}..{args.seed_start + args.seed_count - 1}"
    )
    print(
        "Source family: same self-rule source, same placement, only the late-source "
        "field footprint changes"
    )
    print()
    print("Footprint sweep:")
    for summary in summaries:
        print(f"  {summary.render()}")
    print()
    print(
        f"retained_footprint={retained.footprint} "
        "(highest positive directional score while preserving mover survival)"
    )
    print()
    for line in _render_breakdown(rows, retained.footprint, "config", lambda row: row.config):
        print(line)
    print()
    for line in _render_breakdown(rows, retained.footprint, "mover_rule", lambda row: row.mover_rule):
        print(line)
    print()
    print("Interpretation:")
    print(
        "  This probe asks whether the away-shift problem is mostly caused by the "
        "broad late union used to build the source field. If a narrower recent-state "
        "footprint restores toward-source steering without collapsing the mover "
        "substrate, the active problem is field-footprint compression rather than "
        "source viability."
    )


if __name__ == "__main__":
    main()
