#!/usr/bin/env python3
"""Does attraction EMERGE as a graph grows?

Test: start with a small causal DAG (few layers), add layers one at a time.
At each stage, measure both interference and attraction.

If both phenomena emerge when connectivity crosses the deg≥3 threshold:
→ growth CREATES the conditions for physics

Uses corrected propagator (1/L^p) throughout.

PStack experiment: growing-graph-attraction-emergence
"""

from __future__ import annotations
import math
import cmath
import random
from collections import defaultdict, deque
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag


def compute_field(positions, adj, mass_indices, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_indices)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def pathsum_corrected(positions, adj, field, src, det, k,
                      barrier_idx=None, slit_idx=None):
    n = len(positions)
    blocked = set()
    if barrier_idx is not None and slit_idx is not None:
        blocked = set(barrier_idx) - set(slit_idx)

    in_deg = [0] * n
    for i, nbs in adj.items():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)

    amps = [0.0+0.0j] * n
    for s in src:
        amps[s] = 1.0/len(src)
    for i in order:
        if i in blocked or abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j*k*act) / (L**1.0)
            amps[j] += amps[i] * ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def centroid_y(probs, positions):
    total = sum(probs.values())
    if total == 0:
        return 0.0
    return sum(positions[d][1]*p for d, p in probs.items()) / total


def visibility(probs, positions):
    if not probs:
        return 0.0
    py = defaultdict(float)
    for d, p in probs.items():
        py[positions[d][1]] += p
    ys = sorted(py.keys())
    if len(ys) < 3:
        return 0.0
    vals = [py[y] for y in ys]
    peaks = [vals[i] for i in range(1, len(vals)-1)
             if vals[i] > vals[i-1] and vals[i] > vals[i+1]]
    troughs = [vals[i] for i in range(1, len(vals)-1)
               if vals[i] < vals[i-1] and vals[i] < vals[i+1]]
    if peaks and troughs:
        return (max(peaks)-min(troughs))/(max(peaks)+min(troughs))
    return 0.0


def main() -> None:
    nodes_per_layer = 20
    y_range = 10.0
    connect_radius = 3.0
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 5

    print("=" * 80)
    print("GROWING GRAPH: Attraction + Interference Emergence")
    print("  Add layers incrementally, measure at each stage")
    print("  Corrected propagator: 1/L^p")
    print("=" * 80)
    print()

    # ================================================================
    # Main test: grow from 4 layers to 20, measure at each step
    # ================================================================
    print(f"  {'n_layers':>8s}  {'n_nodes':>7s}  {'mean_deg':>8s}  "
          f"{'attract%':>8s}  {'mean_V':>7s}  {'interf%':>7s}")
    print(f"  {'-' * 52}")

    for n_layers in [4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20]:
        attract_count = 0
        interf_count = 0
        all_v = []
        total = 0

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                y_range=y_range, connect_radius=connect_radius,
                rng_seed=seed * 11 + 7,
            )

            n = len(positions)
            edges = sum(len(v) for v in adj.values())
            mean_deg = edges / n if n > 0 else 0

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())

            if len(layers) < 3:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            if not det:
                continue

            # Mass in middle layer(s)
            mid = len(layers) // 2
            mid_idx = by_layer[layers[mid]]
            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 1]

            if len(mass_idx) < 2:
                total += 1
                continue

            mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)
            field = compute_field(positions, adj, mass_idx)
            free_f = [0.0] * n

            # k-averaged attraction
            grav_shifts = []
            for k in k_band:
                fp = pathsum_corrected(positions, adj, free_f, src, det, k)
                mp = pathsum_corrected(positions, adj, field, src, det, k)
                fcy = centroid_y(fp, positions)
                mcy = centroid_y(mp, positions)
                grav_shifts.append(mcy - fcy)

            avg_shift = sum(grav_shifts) / len(grav_shifts)
            toward = mass_cy - center_y
            attracts = (toward > 0 and avg_shift > 0.05)
            if attracts:
                attract_count += 1

            # Interference: use barrier before mass
            if mid >= 2:
                barrier_layer = layers[mid - 2]
                barrier_idx = by_layer[barrier_layer]
                slit_above = [i for i in barrier_idx if positions[i][1] > center_y + 2]
                slit_below = [i for i in barrier_idx if positions[i][1] < center_y - 2]

                if slit_above and slit_below:
                    slit_a = slit_above[:3]
                    slit_b = slit_below[:3]
                    slit_idx = slit_a + slit_b

                    # Best V over k
                    best_v = 0
                    for k in k_band:
                        bp = pathsum_corrected(positions, adj, free_f, src, det, k,
                                              barrier_idx, slit_idx)
                        v = visibility(bp, positions)
                        if v > best_v:
                            best_v = v

                    all_v.append(best_v)
                    if best_v > 0.1:
                        interf_count += 1

            total += 1

        if total > 0:
            mean_v = sum(all_v) / len(all_v) if all_v else 0
            # Estimate mean degree from one representative
            positions, adj, _ = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                y_range=y_range, connect_radius=connect_radius,
                rng_seed=7,
            )
            n_est = len(positions)
            e_est = sum(len(v) for v in adj.values())
            deg_est = e_est / n_est if n_est > 0 else 0

            apct = f"{100*attract_count//total}%"
            ipct = f"{100*interf_count//total}%"
            print(f"  {n_layers:8d}  {n_est:7d}  {deg_est:8.1f}  "
                  f"{apct:>8s}  {mean_v:7.3f}  {ipct:>7s}")

    # ================================================================
    # Focused: at what layer count does each phenomenon first appear?
    # ================================================================
    print()
    print("=" * 80)
    print("EMERGENCE TIMELINE")
    print("  At which graph size does each phenomenon first appear?")
    print("=" * 80)
    print()

    for seed in range(3):
        grav_emerged = None
        interf_emerged = None

        for n_layers in range(3, 21):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=nodes_per_layer,
                y_range=y_range, connect_radius=connect_radius,
                rng_seed=seed * 11 + 7,
            )

            n = len(positions)
            edges = sum(len(v) for v in adj.values())
            mean_deg = edges / n if n > 0 else 0

            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 3:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            if not det:
                continue

            mid = len(layers) // 2
            mid_idx = by_layer[layers[mid]]
            all_ys = [y for _, y in positions]
            center_y = sum(all_ys) / len(all_ys)
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 1]

            if len(mass_idx) < 2:
                continue

            mass_cy = sum(positions[i][1] for i in mass_idx) / len(mass_idx)
            field = compute_field(positions, adj, mass_idx)
            free_f = [0.0] * n

            # Test attraction
            if grav_emerged is None:
                shifts = []
                for k in k_band:
                    fp = pathsum_corrected(positions, adj, free_f, src, det, k)
                    mp = pathsum_corrected(positions, adj, field, src, det, k)
                    shifts.append(centroid_y(mp, positions) - centroid_y(fp, positions))
                avg = sum(shifts) / len(shifts)
                if (mass_cy - center_y > 0 and avg > 0.05):
                    grav_emerged = n_layers

            # Test interference
            if interf_emerged is None and mid >= 2:
                bl = layers[mid - 2]
                bi = by_layer[bl]
                sa = [i for i in bi if positions[i][1] > center_y + 2][:3]
                sb = [i for i in bi if positions[i][1] < center_y - 2][:3]
                if sa and sb:
                    si = sa + sb
                    for k in k_band:
                        bp = pathsum_corrected(positions, adj, free_f, src, det, k, bi, si)
                        v = visibility(bp, positions)
                        if v > 0.1:
                            interf_emerged = n_layers
                            break

        print(f"  seed {seed}: gravity at {grav_emerged or '>20'} layers, "
              f"interference at {interf_emerged or '>20'} layers")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("If both phenomena emerge at similar layer counts:")
    print("  → growth creates conditions for BOTH gravity and interference")
    print("  → the same structural transition enables both")
    print("  → 'growth rules create the conditions for phenomena'")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
