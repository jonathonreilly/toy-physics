#!/usr/bin/env python3
"""Phase noise on IRREGULAR graphs: does path-length heterogeneity enable decoherence?

On regular lattice: all paths ≈ same length → noise averages uniformly → no decoherence.
On irregular graph: paths have different lengths → noise accumulates differently →
fringes shift by different amounts per realization → ensemble average washes out fringes.

Prediction: V_ensemble should drop with η on irregular graphs but NOT on regular lattice.
This would make graph irregularity the MECHANISM for decoherence.

PStack experiment: phase-noise-irregular-graph
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


def pathsum_noisy_dag(positions, adj, field, src, det, k, eta, rng,
                      barrier_idx=None, slit_idx=None):
    n = len(positions)
    blocked = set()
    if barrier_idx is not None and slit_idx is not None:
        blocked = set(barrier_idx) - set(slit_idx)

    in_deg = [0]*n
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

    amps = [0.0+0.0j]*n
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
            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            noise = eta * rng.gauss(0, 1)
            ea = cmath.exp(1j*(k*act + noise))/(L**1.0)
            amps[j] += amps[i]*ea

    probs = {d: abs(amps[d])**2 for d in det}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p/total for d, p in probs.items()}
    return probs


def visibility(probs, positions, det_indices):
    py = defaultdict(float)
    for d in det_indices:
        py[positions[d][1]] += probs.get(d, 0)
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


def measure_path_length_heterogeneity(positions, adj, src, det):
    """Estimate path length variance by sampling random walks."""
    n = len(positions)
    # BFS to find shortest paths from each source to each detector
    lengths = []
    for s in src:
        visited = {s: 0}
        queue = deque([s])
        while queue:
            node = queue.popleft()
            for nb in adj.get(node, []):
                if nb not in visited:
                    visited[nb] = visited[node] + 1
                    queue.append(nb)
        for d in det:
            if d in visited:
                lengths.append(visited[d])

    if len(lengths) < 2:
        return 0, 0
    mean = sum(lengths) / len(lengths)
    var = sum((l-mean)**2 for l in lengths) / len(lengths)
    return mean, var**0.5


def main():
    N = 40  # realizations per eta
    n_seeds = 8

    print("=" * 70)
    print("PHASE NOISE ON IRREGULAR GRAPHS")
    print(f"  {N} realizations, {n_seeds} graph seeds")
    print("  Corrected propagator (1/L^p)")
    print("=" * 70)
    print()

    # ================================================================
    # TEST 1: Compare lattice-like (small y_range) vs irregular (large y_range)
    # ================================================================

    configs = [
        ("compact (y=3, high deg)", 12, 20, 3.0, 3.0),
        ("medium (y=10, std)", 12, 20, 10.0, 3.0),
        ("spread (y=20, low deg)", 12, 20, 20.0, 3.0),
        ("sparse (r=1.5)", 12, 20, 10.0, 1.5),
        ("dense (r=5)", 12, 20, 10.0, 5.0),
    ]

    for label, n_layers, npl, y_range, radius in configs:
        print(f"  Config: {label}")

        all_v_baseline = []
        all_v_noisy = []
        all_hetero = []

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=n_layers, nodes_per_layer=npl,
                y_range=y_range, connect_radius=radius,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 5:
                continue

            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            if not det or not src:
                continue

            # Barrier for interference
            mid = len(layers)//2
            if mid < 2:
                continue
            bl = layers[mid-2]
            bi = by_layer[bl]
            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)
            sa = [i for i in bi if positions[i][1] > cy+1][:3]
            sb = [i for i in bi if positions[i][1] < cy-1][:3]
            if not sa or not sb:
                continue
            si = sa + sb

            free_f = [0.0]*n
            mean_pl, std_pl = measure_path_length_heterogeneity(positions, adj, src, det)
            all_hetero.append(std_pl)

            # Baseline V (no noise, ensemble of 1)
            probs_0 = pathsum_noisy_dag(positions, adj, free_f, src, det, 5.0, 0.0,
                                         random.Random(0), bi, si)
            v_0 = visibility(probs_0, positions, det)
            all_v_baseline.append(v_0)

            # Noisy ensemble (eta=0.5)
            avg_probs = {d: 0.0 for d in det}
            for i in range(N):
                rng = random.Random(i*31+seed*7)
                probs_n = pathsum_noisy_dag(positions, adj, free_f, src, det, 5.0, 0.5,
                                             rng, bi, si)
                for d in det:
                    avg_probs[d] += probs_n.get(d, 0)

            total = sum(avg_probs.values())
            if total > 0:
                avg_probs = {d: p/total for d, p in avg_probs.items()}
            v_ens = visibility(avg_probs, positions, det)
            all_v_noisy.append(v_ens)

        if all_v_baseline:
            mean_v0 = sum(all_v_baseline)/len(all_v_baseline)
            mean_vn = sum(all_v_noisy)/len(all_v_noisy)
            mean_h = sum(all_hetero)/len(all_hetero) if all_hetero else 0
            v_drop = mean_v0 - mean_vn
            print(f"    path_length_std: {mean_h:.2f}")
            print(f"    V_baseline: {mean_v0:.4f}")
            print(f"    V_noisy(η=0.5): {mean_vn:.4f}")
            print(f"    V_drop: {v_drop:+.4f} ({100*v_drop/mean_v0:.1f}% of baseline)" if mean_v0 > 0 else "")
        print()

    # ================================================================
    # TEST 2: η sweep on the most irregular graph
    # ================================================================
    print("=" * 70)
    print("TEST 2: η sweep on spread graph (y_range=20, most irregular)")
    print("=" * 70)
    print()

    print(f"  {'eta':>6s}  {'V_ens':>8s}  {'V_ind':>8s}  {'n_valid':>7s}")
    print(f"  {'-' * 34}")

    for eta in [0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
        all_v_ens = []
        all_v_ind = []

        for seed in range(n_seeds):
            positions, adj, arrival = generate_causal_dag(
                n_layers=12, nodes_per_layer=20,
                y_range=20.0, connect_radius=3.0,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 5:
                continue
            src = by_layer[layers[0]]
            det = by_layer[layers[-1]]
            if not det:
                continue
            mid = len(layers)//2
            if mid < 2:
                continue
            bl = layers[mid-2]
            bi = by_layer[bl]
            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)
            sa = [i for i in bi if positions[i][1] > cy+1][:3]
            sb = [i for i in bi if positions[i][1] < cy-1][:3]
            if not sa or not sb:
                continue
            si = sa + sb
            free_f = [0.0]*n

            avg_probs = {d: 0.0 for d in det}
            ind_vs = []
            for i in range(N):
                rng = random.Random(i*31+seed*7)
                probs = pathsum_noisy_dag(positions, adj, free_f, src, det, 5.0, eta,
                                          rng, bi, si)
                for d in det:
                    avg_probs[d] += probs.get(d, 0)
                ind_vs.append(visibility(probs, positions, det))

            total = sum(avg_probs.values())
            if total > 0:
                avg_probs = {d: p/total for d, p in avg_probs.items()}
            all_v_ens.append(visibility(avg_probs, positions, det))
            all_v_ind.append(sum(ind_vs)/len(ind_vs))

        if all_v_ens:
            print(f"  {eta:6.1f}  {sum(all_v_ens)/len(all_v_ens):8.4f}  "
                  f"{sum(all_v_ind)/len(all_v_ind):8.4f}  {len(all_v_ens):7d}")

    print()
    print("If V_ens drops on irregular graphs but not lattice:")
    print("  → Graph irregularity IS the decoherence mechanism")
    print("  → Path-length heterogeneity breaks phase coherence")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
