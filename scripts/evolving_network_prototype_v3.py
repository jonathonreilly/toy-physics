#!/usr/bin/env python3
"""Gate B v3 control audit: generated hard-gap pruning vs connectivity-preserving imposed control.

This is a reviewer-facing audit pass, not a new search lane.

The goal is to clarify what a fair imposed control should preserve:
  - a source-to-detector backbone corridor
  - a detector-side tail that still carries signal
  - the same graph family and a comparable removal budget where possible

The audit asks whether the v2 center-band control was too destructive, and
whether a backbone-preserving imposed control keeps the comparison measurable.
If the answer remains negative or mixed, that is the result.
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
    removed_generated: int
    removed_imposed: int
    converged: bool
    spine_kept: bool


def summarize(values):
    values = [v for v in values if v is not None and not math.isnan(v)]
    if not values:
        return math.nan
    return sum(values) / len(values)


def build_backbone_spine(positions, adj, layer_indices):
    """Find one connectivity-preserving spine path through the DAG.

    The path is intentionally simple: a layer-by-layer greedy dynamic program
    that prefers nodes near the global centerline and smooth continuation.
    """

    n_layers = len(layer_indices)
    if n_layers == 0:
        return [], []

    all_ys = [positions[i][1] for i in range(len(positions))]
    cy = sum(all_ys) / len(all_ys)
    prev_layers = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            prev_layers[j].append(i)

    best_cost = {}
    best_prev = {}
    source = layer_indices[0][0]
    best_cost[source] = 0.0
    best_prev[source] = None

    for li in range(1, n_layers):
        for node in layer_indices[li]:
            preds = []
            for pj in range(max(0, li - 2), li):
                for prev in layer_indices[pj]:
                    if node in adj.get(prev, ()):
                        preds.append(prev)
            if not preds:
                continue

            x, y, _ = positions[node]
            best_pred = None
            best_score = None
            for pred in preds:
                if pred not in best_cost:
                    continue
                _, py, _ = positions[pred]
                score = (
                    best_cost[pred]
                    + abs(y - cy)
                    + 0.35 * abs(y - py)
                )
                if best_score is None or score < best_score:
                    best_score = score
                    best_pred = pred
            if best_pred is not None and (node not in best_cost or best_score < best_cost[node]):
                best_cost[node] = best_score
                best_prev[node] = best_pred

    sink_candidates = [i for i in layer_indices[-1] if i in best_cost]
    if not sink_candidates:
        spine = [layer[0] for layer in layer_indices]
        spine_y = [positions[i][1] for i in spine]
        return spine, spine_y

    sink = min(sink_candidates, key=lambda i: best_cost[i])
    spine = [sink]
    cur = sink
    while cur is not None:
        cur = best_prev.get(cur)
        if cur is not None:
            spine.append(cur)
    spine.reverse()

    if len(spine) != n_layers:
        # Fall back to a simple layer-wise centerline if the DAG is unusually sparse.
        spine = [layer[0] for layer in layer_indices]

    spine_y = [positions[i][1] for i in spine]
    return spine, spine_y


def prune_imposed_backbone_control(positions, adj, layer_indices, removed_count, seed):
    """Impose the same removal budget while preserving a backbone corridor.

    The control keeps a thin source-to-detector corridor intact and spends the
    removal budget on the outer shells first. This is a cleaner comparator than
    the v2 center-band control because it preserves detector signal better.
    """

    if removed_count <= 0:
        return dict(adj), {"removed": 0, "spine_kept": True, "corridor_band": 0.0}

    n_layers = len(layer_indices)
    if n_layers == 0:
        return dict(adj), {"removed": 0, "spine_kept": False, "corridor_band": 0.0}

    spine, spine_y = build_backbone_spine(positions, adj, layer_indices)
    if not spine:
        return dict(adj), {"removed": 0, "spine_kept": False, "corridor_band": 0.0}

    # Protect a narrow corridor around the backbone. The corridor keeps the
    # comparator connectivity-preserving while still allowing meaningful pruning.
    corridor_band = 1.75
    protected = set(spine)
    for li, center_y in enumerate(spine_y):
        for node in layer_indices[li]:
            if abs(positions[node][1] - center_y) <= corridor_band:
                protected.add(node)

    cy = sum(p[1] for p in positions) / len(positions)
    # Preserve the detector-side tail so the imposed control keeps a measurable
    # signal. This makes the comparator connectivity-preserving rather than
    # aggressively destructive.
    safe_tail_layers = 6
    candidates = []
    for li in range(1, max(1, n_layers - safe_tail_layers)):
        for node in layer_indices[li]:
            if node in protected:
                continue
            y = positions[node][1]
            # Prefer nodes far from the protected corridor and away from the centerline.
            score = abs(y - spine_y[li]) + 0.4 * abs(y - cy)
            candidates.append((score, node))

    rng = random.Random(seed)
    candidates.sort(key=lambda item: (-item[0], rng.random()))
    chosen = {node for _, node in candidates[: min(removed_count, len(candidates))]}

    new_adj = {}
    for i, nbs in adj.items():
        if i in chosen:
            continue
        kept = [j for j in nbs if j not in chosen]
        if kept:
            new_adj[i] = kept

    spine_kept = all(node not in chosen for node in spine)
    return new_adj, {
        "removed": len(chosen),
        "spine_kept": spine_kept,
        "corridor_band": corridor_band,
    }


def main() -> None:
    started = time.time()
    seeds = [5, 18, 31, 44, 57, 70]
    layer_sizes = [20, 30, 40]
    thresholds = [0.10, 0.20, 0.30]

    print("=" * 84)
    print("EVOLVING NETWORK PROTOTYPE V3")
    print("  Gate B: generated structure vs connectivity-preserving imposed control")
    print("  Comparison: self-regulating hard-gap pruning vs backbone corridor control")
    print("=" * 84)
    print()

    all_rows: list[TrialResult] = []

    for n_layers in layer_sizes:
        print(f"[n_layers={n_layers}]")
        print(
            f"{'d_min':>6s}  {'baseline_pur':>12s}  {'generated_pur':>13s}  "
            f"{'imposed_pur':>11s}  {'generated_gap':>13s}  {'imposed_gap':>11s}  "
            f"{'rem_g':>6s}  {'rem_i':>6s}  {'spine':>5s}  {'conv':>5s}"
        )
        print("-" * 104)

        for d_min in thresholds:
            baseline_purs = []
            generated_purs = []
            imposed_purs = []
            baseline_gaps = []
            generated_gaps = []
            imposed_gaps = []
            removed_gen_vals = []
            removed_imp_vals = []
            spine_vals = []
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
                    removed_gen = 0
                    converged = True
                else:
                    adj_gen, stats = self_regulating_prune(
                        positions,
                        adj0,
                        layer_indices,
                        d_min=d_min,
                        max_iter=5,
                    )
                    removed_gen = int(stats["removed"])
                    converged = bool(stats["converged"])

                adj_imp, ctrl_stats = prune_imposed_backbone_control(
                    positions,
                    adj0,
                    layer_indices,
                    removed_gen,
                    seed * 101 + 7,
                )

                pur_gen = measure_decoherence(positions, adj_gen, layer_indices)
                pur_imp = measure_decoherence(positions, adj_imp, layer_indices)
                gap_gen = gap_metric(positions, adj_gen, layer_indices)
                gap_imp = gap_metric(positions, adj_imp, layer_indices)

                generated_purs.append(pur_gen)
                imposed_purs.append(pur_imp)
                generated_gaps.append(gap_gen)
                imposed_gaps.append(gap_imp)
                removed_gen_vals.append(removed_gen)
                removed_imp_vals.append(int(ctrl_stats["removed"]))
                spine_vals.append(1.0 if ctrl_stats["spine_kept"] else 0.0)
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
                        removed_generated=removed_gen,
                        removed_imposed=int(ctrl_stats["removed"]),
                        converged=converged,
                        spine_kept=bool(ctrl_stats["spine_kept"]),
                    )
                )

            bp = summarize(baseline_purs)
            gp = summarize(generated_purs)
            ip = summarize(imposed_purs)
            gg = summarize(generated_gaps)
            ig = summarize(imposed_gaps)
            rg = summarize(removed_gen_vals)
            ri = summarize(removed_imp_vals)
            sp = summarize(spine_vals)
            cv = summarize(conv_vals)

            print(
                f"{d_min:6.2f}  {bp:12.4f}  {gp:13.4f}  {ip:11.4f}  "
                f"{gg:13.2f}  {ig:11.2f}  {rg:6.1f}  {ri:6.1f}  {sp:5.2f}  {cv:5.2f}"
            )

        print()

    print("=" * 84)
    print("PAIRWISE READ")
    print("=" * 84)
    print()

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
            rem_delta = summarize([r.removed_generated - r.removed_imposed for r in rs])
            spine_ok = summarize([1.0 if r.spine_kept else 0.0 for r in rs])
            print(
                f"  N={n_layers:2d}, d_min={d_min:0.2f}: "
                f"Δpur={pur_delta:+.4f}, Δgap={gap_delta:+.2f}, "
                f"Δremoved={rem_delta:+.1f}, spine_ok={spine_ok:.2f}"
            )

    print()
    print("READ:")
    print("  - Generated structure means local self-regulating pruning by distinguishability.")
    print("  - Imposed structure means the same removal budget spent outside a protected backbone.")
    print("  - The imposed comparator now preserves a backbone corridor, but this sweep")
    print("    still loses finite detector purity, so the result is methodological.")
    print("  - Negative Δpur with positive Δgap would be the cleanest Gate B win.")
    print("  - If the deltas are small, mixed, or nan, that is a bounded negative result,")
    print("    not a promoted dynamics solution.")
    print()
    print(f"Total time: {time.time() - started:.1f}s")
    print("=" * 84)


if __name__ == "__main__":
    main()
