#!/usr/bin/env python3
"""Effective-distance gravity diagnostic on the retained modular family.

Question:
  Can an induced distance extracted from the graph or path ensemble rescue
  the gravity distance law, without changing propagation?

Scope:
  - Keep propagation fixed to the corrected 4D modular gravity lane.
  - Use one or two plausible induced-distance observables:
      1) source-to-mass graph geodesic distance
      2) detector-ensemble weighted mass exposure distance
  - Compare the gravity shift against physical impact parameter b and
    against the induced distances.
  - Report whether any cleaner falloff emerges.

This script is intentionally narrow and review-safe:
  - It stays on the retained modular family.
  - It does not modify propagation.
  - It uses paired per-seed deltas and paired induced-distance observables.

PStack experiment: effective-metric-distance-law
"""

from __future__ import annotations

import heapq
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.four_d_distance_scaling import (
    GAPS,
    K_BAND,
    MASS_COUNT,
    MEAN_OFFSET_TOL,
    N_LAYERS,
    N_SEEDS,
    NODES_PER_LAYER,
    SPATIAL_RANGE,
    TARGET_BS,
    compute_field_4d,
    generate_4d_modular_dag,
    propagate_4d,
    select_mass_nodes,
)


def topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    """Topological order for the forward DAG."""
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = [i for i in range(n) if in_deg[i] == 0]
    order: list[int] = []
    head = 0
    while head < len(q):
        i = q[head]
        head += 1
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def edge_len(p1: tuple[float, float, float, float], p2: tuple[float, float, float, float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


def directed_source_distances(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src_nodes: list[int],
) -> list[float]:
    """Shortest forward-path distance from the source layer to every node."""
    n = len(positions)
    order = topo_order(adj, n)
    dist = [math.inf] * n
    for s in src_nodes:
        dist[s] = 0.0
    for i in order:
        if not math.isfinite(dist[i]):
            continue
        for j in adj.get(i, []):
            cand = dist[i] + edge_len(positions[i], positions[j])
            if cand < dist[j]:
                dist[j] = cand
    return dist


def undirected_mass_distances(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
) -> list[float]:
    """Shortest undirected graph distance from the mass cluster to every node."""
    n = len(positions)
    undirected: dict[int, list[int]] = defaultdict(list)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].append(j)
            undirected[j].append(i)

    dist = [math.inf] * n
    heap: list[tuple[float, int]] = []
    for m in mass_nodes:
        dist[m] = 0.0
        heapq.heappush(heap, (0.0, m))

    while heap:
        d, i = heapq.heappop(heap)
        if d != dist[i]:
            continue
        for j in undirected.get(i, []):
            cand = d + edge_len(positions[i], positions[j])
            if cand < dist[j]:
                dist[j] = cand
                heapq.heappush(heap, (cand, j))
    return dist


def centroid_y(amps, positions, det_list):
    total = 0.0
    wy = 0.0
    for d in det_list:
        p = abs(amps[d]) ** 2
        total += p
        wy += p * positions[d][1]
    return wy / total if total > 1e-30 else 0.0


def fit_power_law(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    n = len(lx)
    sx = sum(lx)
    sy = sum(ly)
    sxy = sum(x * y for x, y in zip(lx, ly))
    sxx = sum(x * x for x in lx)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    alpha = (n * sxy - sx * sy) / denom
    intercept = (sy - alpha * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ly)
    ss_res = sum((y - (alpha * x + intercept)) ** 2 for x, y in zip(lx, ly))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return alpha, math.exp(intercept), r2


def run_gap(gap: float) -> None:
    print(f"[4D modular gap={gap}]")
    print(
        f"{'b':>6s}  {'shift':>10s}  {'SE':>8s}  {'t':>6s}  "
        f"{'src_dist':>10s}  {'eff_dist':>10s}  {'n_ok':>5s}"
    )
    print(f"{'-' * 78}")

    mean_shifts: list[float] = []
    mean_src_dists: list[float] = []
    mean_eff_dists: list[float] = []
    used_bs: list[float] = []

    for target_b in TARGET_BS:
        per_seed_shift: list[float] = []
        per_seed_src: list[float] = []
        per_seed_eff: list[float] = []

        for seed in range(N_SEEDS):
            positions, adj, layer_indices = generate_4d_modular_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=NODES_PER_LAYER,
                spatial_range=SPATIAL_RANGE,
                connect_radius=4.5,
                rng_seed=seed * 13 + 5,
                gap=gap,
            )
            src = layer_indices[0]
            det_list = list(layer_indices[-1])
            if not det_list:
                continue

            all_ys = [positions[i][1] for i in range(len(positions))]
            center_y = sum(all_ys) / len(all_ys)
            grav_idx = 2 * len(layer_indices) // 3
            mass_nodes = select_mass_nodes(
                layer_indices[grav_idx],
                positions,
                center_y,
                target_b,
                MASS_COUNT,
            )
            if not mass_nodes:
                continue

            src_dist = directed_source_distances(positions, adj, src)
            mass_src_dists = [src_dist[m] for m in mass_nodes]
            if any(not math.isfinite(d) for d in mass_src_dists):
                continue
            seed_src_dist = sum(mass_src_dists) / len(mass_src_dists)

            mass_graph_dist = undirected_mass_distances(positions, adj, mass_nodes)

            field_with = compute_field_4d(positions, adj, mass_nodes)
            field_without = [0.0] * len(positions)

            seed_shift_vals: list[float] = []
            seed_eff_vals: list[float] = []

            for k in K_BAND:
                amps_with = propagate_4d(positions, adj, field_with, src, k)
                amps_without = propagate_4d(positions, adj, field_without, src, k)

                probs_without = {d: abs(amps_without[d]) ** 2 for d in det_list}
                tot_without = sum(probs_without.values())
                if tot_without <= 1e-30:
                    continue

                y_with = centroid_y(amps_with, positions, det_list)
                y_without = centroid_y(amps_without, positions, det_list)
                seed_shift_vals.append(y_with - y_without)

                det_weighted = 0.0
                wsum = 0.0
                for d, p in probs_without.items():
                    if not math.isfinite(mass_graph_dist[d]):
                        continue
                    w = p / tot_without
                    det_weighted += w * mass_graph_dist[d]
                    wsum += w
                if wsum > 1e-30:
                    seed_eff_vals.append(det_weighted / wsum)

            if not seed_shift_vals or not seed_eff_vals:
                continue

            per_seed_shift.append(sum(seed_shift_vals) / len(seed_shift_vals))
            per_seed_src.append(seed_src_dist)
            per_seed_eff.append(sum(seed_eff_vals) / len(seed_eff_vals))

        if not per_seed_shift:
            print(f"{target_b:6.2f}  FAIL")
            continue

        n_ok = len(per_seed_shift)
        shift = sum(per_seed_shift) / n_ok
        se = math.sqrt(sum((d - shift) ** 2 for d in per_seed_shift) / n_ok) / math.sqrt(n_ok) if n_ok > 1 else 0.0
        t = shift / se if se > 1e-12 else 0.0
        print(
            f"{target_b:6.2f}  {shift:+10.4f}  {se:8.4f}  {t:+6.2f}  "
            f"{sum(per_seed_src) / n_ok:10.4f}  {sum(per_seed_eff) / n_ok:10.4f}  {n_ok:5d}"
        )

        mean_shifts.append(shift)
        mean_src_dists.append(sum(per_seed_src) / n_ok)
        mean_eff_dists.append(sum(per_seed_eff) / n_ok)
        used_bs.append(target_b)

    print()
    fit_b = fit_power_law(used_bs, mean_shifts)
    fit_src = fit_power_law(mean_src_dists, mean_shifts)
    fit_eff = fit_power_law(mean_eff_dists, mean_shifts)

    if fit_b is None:
        print("b-fit unavailable.")
    else:
        alpha, coeff, r2 = fit_b
        print(f"Physical b fit: shift ~= {coeff:.4f} * b^{alpha:.3f}  (R^2={r2:.3f})")

    if fit_src is None:
        print("Source-geodesic fit unavailable.")
    else:
        alpha, coeff, r2 = fit_src
        print(f"Source geodesic fit: shift ~= {coeff:.4f} * d_src^{alpha:.3f}  (R^2={r2:.3f})")

    if fit_eff is None:
        print("Effective-detector fit unavailable.")
    else:
        alpha, coeff, r2 = fit_eff
        print(f"Detector-ensemble fit: shift ~= {coeff:.4f} * d_eff^{alpha:.3f}  (R^2={r2:.3f})")

    print("Interpretation:")
    print("  If the induced-distance fits are materially cleaner than b,")
    print("  then the graph/path ensemble is supplying a better effective metric.")
    print("  If not, the distance-law failure remains structural.")


def main() -> None:
    print("=" * 78)
    print("EFFECTIVE METRIC DISTANCE LAW")
    print("  Can an induced distance extracted from the retained modular family")
    print("  rescue the gravity distance law without changing propagation?")
    print("  Observables: source geodesic and detector-ensemble mass exposure.")
    print("=" * 78)
    print()

    for gap in GAPS:
        run_gap(gap)
        print()

    print("=" * 78)
    print("CONCLUSION")
    print("=" * 78)
    print("  Compare the physical-b fit against the induced-distance fits above.")
    print("  A rescue would require a materially cleaner falloff in the induced metric.")
    print("  Otherwise the b-independence remains structural.")
    print("=" * 78)


if __name__ == "__main__":
    main()
