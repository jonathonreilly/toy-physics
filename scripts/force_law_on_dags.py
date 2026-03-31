#!/usr/bin/env python3
"""Test gravitational force law on generated DAGs.

On rectangular grid: shift = C × k² × Q3 with R²=0.91
where Q3 = total action asymmetry (above - below).

Is this universal? Test on random causal DAGs where graph structure,
edge lengths, and connectivity all vary between seeds.

If R² > 0.8 on DAGs: universal force law.
If R² << 0.8: lattice-specific (topology matters).

PStack experiment: force-law-on-dags
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


def compute_field(positions, adj, mass_idx, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_idx)
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


def compute_q3_dag(positions, adj, field):
    """Total action asymmetry on DAG: Σ(action_above) - Σ(action_below)."""
    all_ys = [y for _, y in positions]
    center_y = sum(all_ys) / len(all_ys)

    action_above = 0.0
    action_below = 0.0
    for i, nbs in adj.items():
        for j in nbs:
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            action = dl - ret
            avg_y = 0.5 * (y1 + y2)
            if avg_y > center_y:
                action_above += action
            elif avg_y < center_y:
                action_below += action

    return action_above - action_below


def pathsum_corrected(positions, adj, field, src, det, k):
    n = len(positions)
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
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j*k*act)/(L**1.0)
            amps[j] += amps[i]*ea

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


def main() -> None:
    n_layers = 12
    nodes_per_layer = 20
    connect_radius = 3.0
    y_range = 10.0
    n_seeds = 20
    k_test = 0.2  # In k² regime

    print("=" * 80)
    print("FORCE LAW ON GENERATED DAGs")
    print(f"  shift = C × k² × Q3 ?")
    print(f"  {n_layers} layers × {nodes_per_layer} nodes, radius={connect_radius}")
    print(f"  k={k_test}, {n_seeds} seeds with varying mass positions")
    print("=" * 80)
    print()

    data = []

    for seed in range(n_seeds):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=connect_radius,
            rng_seed=seed * 13 + 5,
        )

        n = len(positions)
        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        if len(layers) < 4:
            continue

        src = by_layer[layers[0]]
        det = by_layer[layers[-1]]
        if not det:
            continue

        mid = len(layers) // 2
        mid_idx = by_layer[layers[mid]]
        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)

        # Test mass above AND below for each seed
        for mass_sign in [+1, -1]:
            if mass_sign > 0:
                mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 1]
            else:
                mass_idx = [i for i in mid_idx if positions[i][1] < center_y - 1]

            if len(mass_idx) < 2:
                continue

            field = compute_field(positions, adj, mass_idx)
            free_f = [0.0] * n

            q3 = compute_q3_dag(positions, adj, field)

            # k-test shift
            fp = pathsum_corrected(positions, adj, free_f, src, det, k_test)
            mp = pathsum_corrected(positions, adj, field, src, det, k_test)
            shift = centroid_y(mp, positions) - centroid_y(fp, positions)

            data.append({
                'seed': seed,
                'sign': mass_sign,
                'q3': q3,
                'shift': shift,
                'n_mass': len(mass_idx),
            })

    # ================================================================
    # Analysis
    # ================================================================
    print(f"  {'seed':>4s}  {'side':>5s}  {'Q3':>10s}  {'shift':>10s}  {'shift/Q3':>10s}")
    print(f"  {'-' * 44}")

    for d in data:
        side = "above" if d['sign'] > 0 else "below"
        ratio = d['shift'] / d['q3'] if abs(d['q3']) > 0.01 else 0
        print(f"  {d['seed']:4d}  {side:>5s}  {d['q3']:+10.2f}  {d['shift']:+10.5f}  {ratio:+10.6f}")

    # Correlation and regression
    shifts = [d['shift'] for d in data]
    q3s = [d['q3'] for d in data]
    n = len(data)

    if n > 3:
        mean_s = sum(shifts) / n
        mean_q = sum(q3s) / n
        cov = sum((s - mean_s) * (q - mean_q) for s, q in zip(shifts, q3s)) / n
        std_s = (sum((s - mean_s) ** 2 for s in shifts) / n) ** 0.5
        std_q = (sum((q - mean_q) ** 2 for q in q3s) / n) ** 0.5
        corr = cov / (std_s * std_q) if std_s > 0 and std_q > 0 else 0

        if std_q > 0:
            slope = cov / (std_q ** 2)
            intercept = mean_s - slope * mean_q
            residuals = [(s - (slope * q + intercept)) ** 2 for s, q in zip(shifts, q3s)]
            ss_res = sum(residuals)
            ss_tot = sum((s - mean_s) ** 2 for s in shifts)
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        else:
            slope, intercept, r2 = 0, 0, 0

        print()
        print(f"  n = {n} data points")
        print(f"  Correlation: {corr:+.4f}")
        print(f"  R² = {r2:.4f}")
        print(f"  slope = {slope:.8f}")
        print(f"  intercept = {intercept:+.6f}")
        print()

        # The slope should equal C × k²
        C = slope / (k_test ** 2) if k_test > 0 else 0
        print(f"  Inferred C = slope / k² = {C:.6f}")

        # ================================================================
        # Verify k² scaling on DAGs
        # ================================================================
        print()
        print("VERIFICATION: k² scaling on DAGs")
        print("  Pick seed 0 (above mass), measure shift at multiple k")
        print()

        # Use first valid data point
        test_seed = data[0]['seed']
        test_sign = data[0]['sign']
        test_q3 = data[0]['q3']

        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=nodes_per_layer,
            y_range=y_range, connect_radius=connect_radius,
            rng_seed=test_seed * 13 + 5,
        )
        n_t = len(positions)
        by_layer = defaultdict(list)
        for idx, (x, y) in enumerate(positions):
            by_layer[round(x)].append(idx)
        layers = sorted(by_layer.keys())
        src = by_layer[layers[0]]
        det = by_layer[layers[-1]]
        mid = len(layers) // 2
        mid_idx = by_layer[layers[mid]]
        all_ys = [y for _, y in positions]
        center_y = sum(all_ys) / len(all_ys)
        if test_sign > 0:
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y + 1]
        else:
            mass_idx = [i for i in mid_idx if positions[i][1] < center_y - 1]

        field = compute_field(positions, adj, mass_idx)
        free_f = [0.0] * n_t

        print(f"  {'k':>6s}  {'shift':>10s}  {'shift/k²':>10s}  {'C_eff':>10s}")
        print(f"  {'-' * 40}")

        for k in [0.05, 0.1, 0.15, 0.2, 0.3, 0.5]:
            fp = pathsum_corrected(positions, adj, free_f, src, det, k)
            mp = pathsum_corrected(positions, adj, field, src, det, k)
            shift = centroid_y(mp, positions) - centroid_y(fp, positions)
            sk2 = shift / (k * k) if k > 0 else 0
            c_eff = shift / (k * k * test_q3) if k > 0 and abs(test_q3) > 0.01 else 0
            print(f"  {k:6.3f}  {shift:+10.5f}  {sk2:+10.4f}  {c_eff:+10.7f}")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    if n > 3 and r2 > 0.7:
        print(f"  UNIVERSAL: shift = {C:.6f} × k² × Q3 holds on random DAGs (R²={r2:.3f})")
    elif n > 3 and r2 > 0.5:
        print(f"  PARTIAL: Q3 predicts shift direction (R²={r2:.3f}) but not magnitude")
    else:
        print(f"  WEAK: force law doesn't transfer well to random DAGs (R²={r2:.3f})")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
