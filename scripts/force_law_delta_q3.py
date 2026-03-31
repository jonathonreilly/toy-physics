#!/usr/bin/env python3
"""Force law with ΔQ3 = Q3(mass) - Q3(free).

Q3 alone has R²=0.20 on DAGs because random graphs have intrinsic
asymmetry. ΔQ3 removes the graph's own contribution, isolating the
mass-induced perturbation.

Also test: does the shift itself already subtract the free centroid?
If shift = cy(mass) - cy(free), and Q3_free captures the graph's
asymmetry, then ΔQ3 should correlate much better.

PStack experiment: force-law-delta-q3
"""

from __future__ import annotations
import math
import cmath
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


def compute_q3(positions, adj, field):
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
    a_above = 0.0
    a_below = 0.0
    for i, nbs in adj.items():
        for j in nbs:
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            L = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl-L*L, 0))
            act = dl - ret
            avg_y = 0.5*(y1+y2)
            if avg_y > cy:
                a_above += act
            elif avg_y < cy:
                a_below += act
    return a_above - a_below


def pathsum_shift(positions, adj, field, free_f, src, det, k):
    n = len(positions)
    def propagate(f):
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
                lf = 0.5*(f[i]+f[j])
                dl = L*(1+lf)
                ret = math.sqrt(max(dl*dl-L*L, 0))
                act = dl-ret
                ea = cmath.exp(1j*k*act)/(L**1.0)
                amps[j] += amps[i]*ea
        probs = {d: abs(amps[d])**2 for d in det}
        total = sum(probs.values())
        if total > 0:
            probs = {d: p/total for d, p in probs.items()}
        return sum(positions[d][1]*p for d, p in probs.items()) / max(sum(probs.values()), 1e-30)

    return propagate(field) - propagate(free_f)


def main() -> None:
    n_layers = 12
    npl = 20
    radius = 3.0
    y_range = 10.0
    k_test = 0.2

    print("=" * 80)
    print("FORCE LAW WITH ΔQ3 = Q3(mass) - Q3(free)")
    print("=" * 80)
    print()

    data = []
    for seed in range(20):
        positions, adj, arrival = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=npl,
            y_range=y_range, connect_radius=radius,
            rng_seed=seed*13+5,
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
        mid = len(layers)//2
        mid_idx = by_layer[layers[mid]]
        all_ys = [y for _, y in positions]
        center_y = sum(all_ys)/len(all_ys)

        free_f = [0.0]*n
        q3_free = compute_q3(positions, adj, free_f)

        for mass_sign in [+1, -1]:
            if mass_sign > 0:
                mass_idx = [i for i in mid_idx if positions[i][1] > center_y+1]
            else:
                mass_idx = [i for i in mid_idx if positions[i][1] < center_y-1]
            if len(mass_idx) < 2:
                continue

            field = compute_field(positions, adj, mass_idx)
            q3_mass = compute_q3(positions, adj, field)
            dq3 = q3_mass - q3_free

            # k-averaged shift
            shifts = []
            for k in [0.1, 0.2, 0.3]:
                shifts.append(pathsum_shift(positions, adj, field, free_f, src, det, k))
            avg_shift = sum(shifts)/len(shifts)

            data.append({
                'seed': seed, 'sign': mass_sign,
                'q3_free': q3_free, 'q3_mass': q3_mass,
                'dq3': dq3, 'q3': q3_mass,
                'shift': avg_shift,
            })

    # Regression: shift vs ΔQ3 and shift vs Q3
    print(f"  {'seed':>4s}  {'side':>5s}  {'Q3_free':>8s}  {'Q3_mass':>8s}  {'ΔQ3':>8s}  {'shift':>10s}")
    print(f"  {'-' * 50}")
    for d in data:
        side = "above" if d['sign'] > 0 else "below"
        print(f"  {d['seed']:4d}  {side:>5s}  {d['q3_free']:+8.1f}  {d['q3_mass']:+8.1f}  "
              f"{d['dq3']:+8.1f}  {d['shift']:+10.5f}")

    def regression(xs, ys, label):
        n = len(xs)
        mx = sum(xs)/n
        my = sum(ys)/n
        cov = sum((x-mx)*(y-my) for x, y in zip(xs, ys))/n
        sx = (sum((x-mx)**2 for x in xs)/n)**0.5
        sy = (sum((y-my)**2 for y in ys)/n)**0.5
        corr = cov/(sx*sy) if sx > 0 and sy > 0 else 0
        slope = cov/(sx**2) if sx > 0 else 0
        intercept = my - slope*mx
        resid = sum((y-(slope*x+intercept))**2 for x, y in zip(xs, ys))
        ss_tot = sum((y-my)**2 for y in ys)
        r2 = 1-resid/ss_tot if ss_tot > 0 else 0
        print(f"  {label}: corr={corr:+.4f}, R²={r2:.4f}, slope={slope:.8f}")

    print()
    regression([d['q3'] for d in data], [d['shift'] for d in data], "Q3 (raw)")
    regression([d['dq3'] for d in data], [d['shift'] for d in data], "ΔQ3 (mass - free)")

    # Also try: ΔQ3 normalized by graph size
    n_edges_list = []
    for seed in range(20):
        positions, adj, _ = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=npl,
            y_range=y_range, connect_radius=radius,
            rng_seed=seed*13+5,
        )
        n_edges_list.append(sum(len(v) for v in adj.values()))

    # Simple field asymmetry: Σ field(y>0) - Σ field(y<0)
    def field_asymmetry(positions, field):
        all_ys = [y for _, y in positions]
        cy = sum(all_ys)/len(all_ys)
        above = sum(field[i] for i, (x, y) in enumerate(positions) if y > cy)
        below = sum(field[i] for i, (x, y) in enumerate(positions) if y < cy)
        return above - below

    fa_data = []
    for d in data:
        positions, adj, _ = generate_causal_dag(
            n_layers=n_layers, nodes_per_layer=npl,
            y_range=y_range, connect_radius=radius,
            rng_seed=d['seed']*13+5,
        )
        n = len(positions)
        all_ys = [y for _, y in positions]
        center_y = sum(all_ys)/len(all_ys)
        mid_layer = sorted(set(round(x) for x, y in positions))[len(set(round(x) for x, y in positions))//2]
        mid_idx = [i for i, (x, y) in enumerate(positions) if round(x) == mid_layer]
        if d['sign'] > 0:
            mass_idx = [i for i in mid_idx if positions[i][1] > center_y+1]
        else:
            mass_idx = [i for i in mid_idx if positions[i][1] < center_y-1]
        if len(mass_idx) < 2:
            continue
        field = compute_field(positions, adj, mass_idx)
        fa = field_asymmetry(positions, field)
        fa_data.append((fa, d['shift']))

    if fa_data:
        regression([x for x, _ in fa_data], [y for _, y in fa_data], "Field asymmetry")

    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("If ΔQ3 >> Q3 in R²: the force law works once graph asymmetry is removed.")
    print("If both similar: the graph's intrinsic asymmetry is the dominant uncertainty.")
    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
