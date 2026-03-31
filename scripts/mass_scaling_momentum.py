#!/usr/bin/env python3
"""Does Δky scale linearly with mass (number of persistent nodes)?

Real gravity: F ∝ M. If Δky ∝ n_mass, the model produces mass-proportional
gravitational deflection — a key bridge to known physics.

Test on rectangular grid (clean geometry) and generated DAGs.

PStack experiment: mass-scaling-momentum
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toy_event_physics import (
    RulePostulates, build_rectangular_nodes, derive_local_rule,
    derive_node_field, infer_arrival_times_from_source, build_causal_dag,
)
from scripts.generative_causal_dag_interference import generate_causal_dag


def propagate_geom(nodes, source, field, k, p):
    post = RulePostulates(phase_per_action=k, attenuation_power=p)
    rule = derive_local_rule(persistent_nodes=frozenset(), postulates=post)
    arrival = infer_arrival_times_from_source(nodes, source, rule)
    dag = build_causal_dag(nodes, arrival)
    order = sorted(arrival, key=arrival.get)
    amps = {source: 1.0+0.0j}
    for node in order:
        if node not in amps:
            continue
        a = amps[node]
        for nb in dag.get(node, []):
            L = math.dist(node, nb)
            lf = 0.5*(field.get(node, 0.0)+field.get(nb, 0.0))
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl-ret
            ea = cmath.exp(1j*k*act)/(L**p)
            if nb not in amps:
                amps[nb] = 0.0+0.0j
            amps[nb] += a*ea
    return amps


def fourier_centroid(amps, x, screen_ys):
    N = len(screen_ys)
    psi = [amps.get((x, y), 0.0+0.0j) for y in screen_ys]
    ft = []
    for n in range(N):
        s = sum(psi[m]*cmath.exp(-2j*math.pi*m*n/N) for m in range(N))
        ft.append(s)
    probs = [abs(f)**2 for f in ft]
    total = sum(probs)
    if total == 0:
        return 0.0
    centroid = sum((n if n <= N//2 else n-N)*p for n, p in enumerate(probs))
    return centroid / total


def main():
    width = 60
    height = 25
    nodes = build_rectangular_nodes(width=width, height=height)
    source = (0, 0)
    screen_ys = list(range(-height, height+1))
    free_field = {n: 0.0 for n in nodes}
    k = 2.0
    det_x = 45
    mass_x = 30
    mass_y_center = 6

    post = RulePostulates(phase_per_action=k, attenuation_power=1.0)

    print("=" * 70)
    print("MASS SCALING OF MOMENTUM DEFLECTION")
    print(f"  Grid: {width}x{2*height+1}, k={k}, det_x={det_x}")
    print(f"  Mass at x={mass_x}, centered at y={mass_y_center}")
    print("=" * 70)
    print()

    free_amps = propagate_geom(nodes, source, free_field, k, 1.0)
    ky_free = fourier_centroid(free_amps, det_x, screen_ys)

    # ================================================================
    # TEST 1: Vary number of mass nodes (column height)
    # ================================================================
    print("TEST 1: Δky vs n_mass (column at x=30, varying height)")
    print()

    print(f"  {'n_mass':>6s}  {'Δky':>10s}  {'Δky/n':>10s}  {'linear?':>8s}")
    print(f"  {'-' * 38}")

    results = []
    for n in [1, 2, 3, 4, 5, 7, 9, 11, 15, 20]:
        half = n // 2
        mn = frozenset((mass_x, y) for y in range(mass_y_center-half, mass_y_center+half+1))
        actual_n = len(mn)
        mr = derive_local_rule(persistent_nodes=mn, postulates=post)
        mf = derive_node_field(nodes, mr)
        mass_amps = propagate_geom(nodes, source, mf, k, 1.0)
        dky = fourier_centroid(mass_amps, det_x, screen_ys) - ky_free
        ratio = dky / actual_n if actual_n > 0 else 0
        results.append((actual_n, dky, ratio))
        print(f"  {actual_n:6d}  {dky:+10.4f}  {ratio:+10.4f}  {'---' if actual_n < 2 else ''}")

    # Check linearity
    if len(results) > 3:
        ns = [r[0] for r in results if r[0] >= 2]
        dkys = [r[1] for r in results if r[0] >= 2]
        n_pts = len(ns)
        mn_val = sum(ns)/n_pts
        md = sum(dkys)/n_pts
        cov = sum((n-mn_val)*(d-md) for n, d in zip(ns, dkys))/n_pts
        sn = (sum((n-mn_val)**2 for n in ns)/n_pts)**0.5
        sd = (sum((d-md)**2 for d in dkys)/n_pts)**0.5
        corr = cov/(sn*sd) if sn > 0 and sd > 0 else 0
        slope = cov/(sn**2) if sn > 0 else 0
        print(f"\n  Linear fit: Δky = {slope:.4f} × n_mass")
        print(f"  Correlation: {corr:.4f}")
        print(f"  Linear (corr > 0.95): {'YES' if corr > 0.95 else 'NO'}")

    # ================================================================
    # TEST 2: Vary mass x-position (same n_mass)
    # ================================================================
    print()
    print("TEST 2: Δky vs mass x-position (5 nodes, y=4..8)")
    print()

    print(f"  {'mass_x':>6s}  {'Δky':>10s}")
    print(f"  {'-' * 20}")

    for mx in [10, 15, 20, 25, 30, 35, 40, 45, 50]:
        mn = frozenset((mx, y) for y in range(4, 9))
        mr = derive_local_rule(persistent_nodes=mn, postulates=post)
        mf = derive_node_field(nodes, mr)
        mass_amps = propagate_geom(nodes, source, mf, k, 1.0)
        dky = fourier_centroid(mass_amps, det_x, screen_ys) - ky_free
        print(f"  {mx:6d}  {dky:+10.4f}")

    # ================================================================
    # TEST 3: On generated DAGs
    # ================================================================
    print()
    print("TEST 3: Centroid shift vs n_mass on generated DAGs (5 seeds)")
    print("  NOTE: this measures position-space centroid, not momentum-space Δky")
    print()

    def dag_centroid_y(positions, adj, mass_idx, src, det_idx, k_val):
        n = len(positions)
        field_m = [0.0]*n
        if mass_idx:
            undirected = defaultdict(set)
            for i, nbs in adj.items():
                for j in nbs:
                    undirected[i].add(j)
                    undirected[j].add(i)
            ms = set(mass_idx)
            field_m = [1.0 if i in ms else 0.0 for i in range(n)]
            for _ in range(50):
                nf = [0.0]*n
                for i in range(n):
                    if i in ms:
                        nf[i] = 1.0
                    elif undirected.get(i):
                        nf[i] = sum(field_m[j] for j in undirected[i])/len(undirected[i])
                field_m = nf

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
            if abs(amps[i]) < 1e-30:
                continue
            for j in adj.get(i, []):
                x1, y1 = positions[i]
                x2, y2 = positions[j]
                L = math.sqrt((x2-x1)**2+(y2-y1)**2)
                if L < 1e-10:
                    continue
                lf = 0.5*(field_m[i]+field_m[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                ea = cmath.exp(1j*k_val*act)/(L**1.0)
                amps[j] += amps[i]*ea

        # Centroid y at detector
        probs = {d: abs(amps[d])**2 for d in det_idx}
        total = sum(probs.values())
        if total > 0:
            return sum(positions[d][1]*p for d, p in probs.items())/total
        return 0.0

    print(f"  {'n_mass':>6s}  {'mean_shift':>10s}  {'shift/n':>10s}")
    print(f"  {'-' * 30}")

    for target_n in [2, 4, 6, 8, 12]:
        shifts = []
        for seed in range(5):
            positions, adj, _ = generate_causal_dag(
                n_layers=12, nodes_per_layer=20,
                y_range=10.0, connect_radius=3.0,
                rng_seed=seed*11+7,
            )
            n = len(positions)
            by_layer = defaultdict(list)
            for idx, (x, y) in enumerate(positions):
                by_layer[round(x)].append(idx)
            layers = sorted(by_layer.keys())
            if len(layers) < 4:
                continue
            src = by_layer[layers[0]]
            det = set(by_layer[layers[-1]])
            if not det:
                continue
            mid = len(layers)//2
            all_ys = [y for _, y in positions]
            cy = sum(all_ys)/len(all_ys)
            candidates = [i for i in by_layer[layers[mid]] if positions[i][1] > cy+1]
            mass = candidates[:target_n]
            if len(mass) < 2:
                continue

            for kv in [3.0, 5.0, 7.0]:
                cy_free = dag_centroid_y(positions, adj, [], src, det, kv)
                cy_mass = dag_centroid_y(positions, adj, mass, src, det, kv)
                shifts.append(cy_mass - cy_free)

        if shifts:
            mean = sum(shifts)/len(shifts)
            per_n = mean/target_n if target_n > 0 else 0
            print(f"  {target_n:6d}  {mean:+10.4f}  {per_n:+10.4f}")

    print()
    print("If shift/n_mass ≈ constant: gravitational deflection ∝ mass (F ∝ M)")
    print("NOTE: DAG test uses position-space centroid; grid tests 1-2 use Fourier Δky")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
