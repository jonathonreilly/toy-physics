#!/usr/bin/env python3
"""Diagnose the shared failure mode behind wrong-scaling env architectures.

The new architecture pass says finite-bin partial-trace environments wrong-scale
on growing DAGs. This script asks for the likely mechanism-language reason:

Do the two slit branches increasingly collapse onto the same detector-conditioned
environment support as the graph grows?

We compare three retained growing-DAG environment architectures:

1. node-label env (fine last-mass label)
2. cumulative-action env (fixed-bin cumulative phase)
3. evolving-phase env (fixed-bin evolving phase)

For each architecture we measure:
- detector-conditioned purity on the open two-slit graph
- weighted overlap between the upper-only and lower-only env distributions
- support Jaccard between the upper-only and lower-only env label sets

If overlap rises together with purity, that compresses the wrong-scaling result
into one shared support-collapse mechanism.
"""

from __future__ import annotations

from collections import defaultdict
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

from scripts.cumulative_phase_env import propagate_cumulative_env  # noqa: E402
from scripts.density_matrix_analysis import (  # noqa: E402
    build_post_barrier_setup,
    compute_detector_metrics,
    propagate_two_register_full,
)
from scripts.evolving_env_decoherence import propagate_evolving_env  # noqa: E402
from scripts.generative_causal_dag_interference import generate_causal_dag  # noqa: E402


K_BAND = [3.0, 5.0, 7.0]
N_LAYERS = [6, 8, 10, 12, 15, 18, 20, 25]


@dataclass(frozen=True)
class Row:
    architecture: str
    n_layers: int
    graph_seed: int
    purity: float
    det_prob: float
    weighted_overlap: float
    support_jaccard: float
    upper_support_size: float
    lower_support_size: float


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else float("nan")


def _corr(xs: list[float], ys: list[float]) -> float:
    if len(xs) != len(ys) or len(xs) < 2:
        return float("nan")
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / len(xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / len(ys))
    if sx <= 1e-12 or sy <= 1e-12:
        return float("nan")
    return cov / (sx * sy)


def _split_barrier_openings(setup: dict, positions: list[tuple[float, float]]) -> tuple[set[int], set[int], set[int]]:
    layers = setup["layers"]
    by_layer = setup["by_layer"]
    cy = setup["cy"]
    barrier_layer = layers[len(layers) // 3]
    barrier_nodes = by_layer[barrier_layer]
    upper = set([i for i in barrier_nodes if positions[i][1] > cy + 3][:3])
    lower = set([i for i in barrier_nodes if positions[i][1] < cy - 3][:3])
    return set(barrier_nodes), upper, lower


def _env_distribution(det_state: dict[tuple[int, int], complex]) -> dict[int, float]:
    weights: dict[int, float] = defaultdict(float)
    total = 0.0
    for (_, env), amp in det_state.items():
        weight = abs(amp) ** 2
        weights[env] += weight
        total += weight
    if total <= 1e-30:
        return {}
    return {
        env: weight / total
        for env, weight in weights.items()
        if weight / total > 1e-12
    }


def _weighted_overlap(left: dict[int, float], right: dict[int, float]) -> float:
    keys = set(left) | set(right)
    return sum(min(left.get(key, 0.0), right.get(key, 0.0)) for key in keys)


def _support_jaccard(left: dict[int, float], right: dict[int, float]) -> float:
    left_keys = set(left)
    right_keys = set(right)
    union = left_keys | right_keys
    if not union:
        return 0.0
    return len(left_keys & right_keys) / len(union)


def _propagate(
    architecture: str,
    positions: list[tuple[float, float]],
    adj: dict[int, list[int]],
    field: list[float] | dict[int, float],
    src: list[int],
    det: set[int],
    det_list: list[int],
    mass_set: set[int],
    blocked: set[int],
    k_value: float,
) -> tuple[float, float, dict[int, float]]:
    if architecture == "node":
        det_state = propagate_two_register_full(
            positions,
            adj,
            field,
            src,
            det,
            k_value,
            mass_set,
            blocked,
        )
    elif architecture == "cumulative":
        det_state = propagate_cumulative_env(
            positions,
            adj,
            field,
            src,
            det,
            k_value,
            mass_set,
            blocked,
            n_bins=8,
        )
    elif architecture == "evolving":
        det_state = propagate_evolving_env(
            positions,
            adj,
            field,
            src,
            det,
            k_value,
            mass_set,
            blocked,
            env_coupling=1.0,
            n_bins=12,
        )
    else:
        raise ValueError(f"Unknown architecture: {architecture}")
    purity, _, _, det_prob = compute_detector_metrics(det_state, det_list)
    return purity, det_prob, _env_distribution(det_state)


def _evaluate_task(task: tuple[int, int, int, float, float]) -> list[Row]:
    n_layers, graph_seed, nodes_per_layer, y_range, connect_radius = task
    positions, adj, _ = generate_causal_dag(
        n_layers=n_layers,
        nodes_per_layer=nodes_per_layer,
        y_range=y_range,
        connect_radius=connect_radius,
        rng_seed=graph_seed * 11 + 7,
    )
    scaled_depth = max(1, round(n_layers / 6))
    setup = build_post_barrier_setup(positions, adj, env_depth_layers=scaled_depth)
    if setup is None:
        return []

    barrier_nodes, upper_open, lower_open = _split_barrier_openings(setup, positions)
    if not upper_open or not lower_open:
        return []
    blocked_upper = barrier_nodes - upper_open
    blocked_lower = barrier_nodes - lower_open

    rows: list[Row] = []
    for architecture in ("node", "cumulative", "evolving"):
        purity_values: list[float] = []
        det_probs: list[float] = []
        overlaps: list[float] = []
        jaccards: list[float] = []
        upper_sizes: list[float] = []
        lower_sizes: list[float] = []

        for k_value in K_BAND:
            purity, det_prob, _ = _propagate(
                architecture,
                positions,
                adj,
                setup["field"],
                setup["src"],
                setup["det"],
                setup["det_list"],
                setup["mass_set"],
                setup["blocked"],
                k_value,
            )
            _, _, upper_dist = _propagate(
                architecture,
                positions,
                adj,
                setup["field"],
                setup["src"],
                setup["det"],
                setup["det_list"],
                setup["mass_set"],
                blocked_upper,
                k_value,
            )
            _, _, lower_dist = _propagate(
                architecture,
                positions,
                adj,
                setup["field"],
                setup["src"],
                setup["det"],
                setup["det_list"],
                setup["mass_set"],
                blocked_lower,
                k_value,
            )

            purity_values.append(purity)
            det_probs.append(det_prob)
            overlaps.append(_weighted_overlap(upper_dist, lower_dist))
            jaccards.append(_support_jaccard(upper_dist, lower_dist))
            upper_sizes.append(float(len(upper_dist)))
            lower_sizes.append(float(len(lower_dist)))

        rows.append(
            Row(
                architecture=architecture,
                n_layers=n_layers,
                graph_seed=graph_seed,
                purity=_mean(purity_values),
                det_prob=_mean(det_probs),
                weighted_overlap=_mean(overlaps),
                support_jaccard=_mean(jaccards),
                upper_support_size=_mean(upper_sizes),
                lower_support_size=_mean(lower_sizes),
            )
        )
    return rows


def run_rows(
    seeds: Iterable[int],
    workers: int,
    nodes_per_layer: int,
    y_range: float,
    connect_radius: float,
) -> list[Row]:
    tasks = [
        (n_layers, seed, nodes_per_layer, y_range, connect_radius)
        for n_layers in N_LAYERS
        for seed in seeds
    ]
    if workers <= 1:
        rows: list[Row] = []
        for task in tasks:
            rows.extend(_evaluate_task(task))
        return rows

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as pool:
        rows = []
        for chunk in pool.map(_evaluate_task, tasks):
            rows.extend(chunk)
        return rows


def _render_architecture(rows: list[Row], architecture: str) -> list[str]:
    subset = [row for row in rows if row.architecture == architecture]
    lines = [f"{architecture} architecture:"]
    lines.append(
        "  "
        f"{'n_layers':>8s} {'purity':>8s} {'overlap':>8s} "
        f"{'jaccard':>8s} {'sup_u':>8s} {'sup_l':>8s} {'det_P':>8s} {'n':>4s}"
    )
    lines.append("  " + "-" * 71)
    for n_layers in N_LAYERS:
        bucket = [row for row in subset if row.n_layers == n_layers]
        if not bucket:
            continue
        lines.append(
            "  "
            f"{n_layers:8d} "
            f"{_mean(row.purity for row in bucket):8.4f} "
            f"{_mean(row.weighted_overlap for row in bucket):8.4f} "
            f"{_mean(row.support_jaccard for row in bucket):8.4f} "
            f"{_mean(row.upper_support_size for row in bucket):8.2f} "
            f"{_mean(row.lower_support_size for row in bucket):8.2f} "
            f"{_mean(row.det_prob for row in bucket):8.4f} "
            f"{len(bucket):4d}"
        )
    purity_corr = _corr(
        [row.purity for row in subset],
        [row.weighted_overlap for row in subset],
    )
    jaccard_corr = _corr(
        [row.purity for row in subset],
        [row.support_jaccard for row in subset],
    )
    lines.append("")
    lines.append(
        "  "
        f"corr(purity, weighted_overlap)={purity_corr:+.4f} "
        f"corr(purity, support_jaccard)={jaccard_corr:+.4f}"
    )
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-count", type=int, default=8)
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--nodes-per-layer", type=int, default=25)
    parser.add_argument("--y-range", type=float, default=12.0)
    parser.add_argument("--connect-radius", type=float, default=3.0)
    args = parser.parse_args()

    rows = run_rows(
        seeds=range(args.seed_count),
        workers=max(1, args.workers),
        nodes_per_layer=args.nodes_per_layer,
        y_range=args.y_range,
        connect_radius=args.connect_radius,
    )
    rows.sort(key=lambda row: (row.architecture, row.n_layers, row.graph_seed))

    print("=" * 88)
    print("NON-UNITARY ENV SUPPORT OVERLAP DIAGNOSIS")
    print("=" * 88)
    print(
        f"Rows: {len(rows)} architecture/graph evaluations; seeds=0..{args.seed_count - 1}; "
        f"workers={max(1, args.workers)}"
    )
    print(
        "Question: as growing-DAG env architectures wrong-scale, do upper-only and "
        "lower-only slit branches increasingly collapse onto the same env support?"
    )
    print()
    for architecture in ("node", "cumulative", "evolving"):
        for line in _render_architecture(rows, architecture):
            print(line)
        print()
    print("Observed read:")
    for architecture in ("node", "cumulative", "evolving"):
        subset = [row for row in rows if row.architecture == architecture]
        print(
            "  "
            f"{architecture}: "
            f"mean weighted_overlap={_mean(row.weighted_overlap for row in subset):.4f}, "
            f"mean support_jaccard={_mean(row.support_jaccard for row in subset):.4f}"
        )
    print()
    print("Interpretation:")
    print(
        "  If weighted overlap or support Jaccard is already near 1, the env labels "
        "have already collapsed the two branches back onto almost the same effective "
        "support. That is immediate support collapse, not just a late-size effect."
    )
    print(
        "  If that happens across all three architectures, the wrong-scaling result "
        "compresses to one support-collapse mechanism rather than three unrelated failures."
    )


if __name__ == "__main__":
    main()
