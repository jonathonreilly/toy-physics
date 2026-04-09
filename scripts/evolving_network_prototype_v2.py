#!/usr/bin/env python3
"""Bounded Gate B prototype: generated vs imposed structure on 3D DAGs.

This script is intentionally narrow. It compares a local, self-regulating
hard-gap rule against a same-budget imposed control on the same 3D DAG family.

The goal is not to prove the full axioms. The goal is to separate:

  - generated structure: nodes removed by a local distinguishability rule
  - imposed structure: the same removal budget applied as a hand-imposed band

If the generated rule consistently produces a larger gap and lower purity than
the imposed control, that is a real Gate B signal. If not, that is still a
useful bounded negative result.

The prototype reuses the 3D uniform DAG / decoherence helpers from the existing
hard-gap lane, but keeps the comparison itself self-contained and conservative.
"""

from __future__ import annotations

import math
import random
import time
from collections import defaultdict
from dataclasses import dataclass
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.self_regulating_gap_3d import (
    generate_3d_uniform_dag,
    gap_metric,
    measure_decoherence,
    self_regulating_prune,
)


@dataclass
class TrialResult:
    n_layers: int
    d_min: float
    seed: int
    baseline_pur: float
    generated_pur: float
    imposed_pur: float
    baseline_gap: float
    generated_gap: float
    imposed_gap: float
    removed: int
    converged: bool


def prune_imposed_band_control(positions, adj, layer_indices, removed_count, seed):
    """Impose the same removal budget as the generated rule, but as a band.

    This is the clean control condition: same graph family, same budget,
    but the removal is imposed by hand as a geometric band around the center.
    It is less destructive than random removal and is easier to compare against
    the self-regulated rule.
    """

    if removed_count <= 0:
        return dict(adj)

    n_layers = len(layer_indices)
    bl_idx = n_layers // 3

    candidates = []
    for li in range(bl_idx + 1, n_layers - 1):
        candidates.extend(layer_indices[li])

    if not candidates:
        return dict(adj)

    cy = sum(positions[i][1] for i in candidates) / len(candidates)
    rng = random.Random(seed)
    ranked = sorted(
        candidates,
        key=lambda i: (abs(positions[i][1] - cy), rng.random()),
    )
    chosen = set(ranked[: min(removed_count, len(ranked))])
    new_adj = {}
    for i, nbs in adj.items():
        if i in chosen:
            continue
        kept = [j for j in nbs if j not in chosen]
        if kept:
            new_adj[i] = kept
    return new_adj


def summarize(values):
    values = [v for v in values if v is not None and not math.isnan(v)]
    if not values:
        return math.nan
    return sum(values) / len(values)


def main() -> None:
    started = time.time()
    seeds = [5, 18, 31, 44, 57, 70]
    layer_sizes = [20, 30, 40]
    thresholds = [0.10, 0.20, 0.30]

    print("=" * 84)
    print("EVOLVING NETWORK PROTOTYPE V2")
    print("  Gate B: generated structure vs imposed structure")
    print("  Comparison: self-regulating hard-gap pruning vs same-budget imposed band")
    print("=" * 84)
    print()

    all_rows: list[TrialResult] = []

    for n_layers in layer_sizes:
        print(f"[n_layers={n_layers}]")
        print(
            f"{'d_min':>6s}  {'baseline_pur':>12s}  {'generated_pur':>13s}  "
            f"{'imposed_pur':>11s}  {'generated_gap':>13s}  {'imposed_gap':>11s}  "
            f"{'removed':>7s}  {'conv':>5s}"
        )
        print("-" * 92)

        for d_min in thresholds:
            baseline_purs = []
            generated_purs = []
            imposed_purs = []
            baseline_gaps = []
            generated_gaps = []
            imposed_gaps = []
            removed_vals = []
            conv_vals = []

            for seed in seeds:
                positions, adj0, layer_indices = generate_3d_uniform_dag(
                    n_layers=n_layers,
                    nodes_per_layer=30,
                    yz_range=10.0,
                    connect_radius=3.5,
                    rng_seed=seed * 13 + 5,
                )

                baseline_pur = measure_decoherence(positions, adj0, layer_indices)
                if not math.isnan(baseline_pur):
                    baseline_purs.append(baseline_pur)
                    baseline_gaps.append(gap_metric(positions, adj0, layer_indices))

                if d_min <= 0:
                    adj_gen = dict(adj0)
                    removed = 0
                    converged = True
                else:
                    adj_gen, stats = self_regulating_prune(
                        positions,
                        adj0,
                        layer_indices,
                        d_min=d_min,
                        max_iter=5,
                    )
                    removed = int(stats["removed"])
                    converged = bool(stats["converged"])

                adj_imp = prune_imposed_band_control(positions, adj0, layer_indices, removed, seed * 101 + 7)

                pur_gen = measure_decoherence(positions, adj_gen, layer_indices)
                pur_imp = measure_decoherence(positions, adj_imp, layer_indices)
                gap_gen = gap_metric(positions, adj_gen, layer_indices)
                gap_imp = gap_metric(positions, adj_imp, layer_indices)

                generated_purs.append(pur_gen)
                imposed_purs.append(pur_imp)
                generated_gaps.append(gap_gen)
                imposed_gaps.append(gap_imp)
                removed_vals.append(removed)
                conv_vals.append(1.0 if converged else 0.0)

                all_rows.append(
                    TrialResult(
                        n_layers=n_layers,
                        d_min=d_min,
                        seed=seed,
                        baseline_pur=baseline_pur,
                        generated_pur=pur_gen,
                        imposed_pur=pur_imp,
                        baseline_gap=gap_metric(positions, adj0, layer_indices),
                        generated_gap=gap_gen,
                        imposed_gap=gap_imp,
                        removed=removed,
                        converged=converged,
                    )
                )

            bp = summarize(baseline_purs)
            gp = summarize(generated_purs)
            ip = summarize(imposed_purs)
            gg = summarize(generated_gaps)
            ig = summarize(imposed_gaps)
            mr = summarize(removed_vals)
            cv = summarize(conv_vals)

            print(
                f"{d_min:6.2f}  {bp:12.4f}  {gp:13.4f}  {ip:11.4f}  "
                f"{gg:13.2f}  {ig:11.2f}  {mr:7.1f}  {cv:5.2f}"
            )

        print()

    print("=" * 84)
    print("PAIRWISE READ")
    print("=" * 84)
    print()

    # Compact pairwise summary: compare generated minus imposed by n_layers.
    for n_layers in layer_sizes:
        rows = [r for r in all_rows if r.n_layers == n_layers]
        if not rows:
            continue
        for d_min in thresholds:
            rs = [r for r in rows if abs(r.d_min - d_min) < 1e-9]
            if not rs:
                continue
            pur_delta = summarize([r.generated_pur - r.imposed_pur for r in rs])
            gap_delta = summarize([r.generated_gap - r.imposed_gap for r in rs])
            print(
                f"  N={n_layers:2d}, d_min={d_min:0.2f}: "
                f"Δpur={pur_delta:+.4f}, Δgap={gap_delta:+.2f}"
            )

    print()
    print("READ:")
    print("  - Generated structure means local pruning by distinguishability.")
    print("  - Imposed structure means the same removal budget applied randomly.")
    print("  - Negative Δpur with positive Δgap would be the cleanest Gate B win.")
    print("  - If the deltas are small or mixed, that is a bounded negative result,")
    print("    not a failure of the review-hardening lane.")
    print()
    print(f"Total time: {time.time() - started:.1f}s")
    print("=" * 84)


if __name__ == "__main__":
    main()
