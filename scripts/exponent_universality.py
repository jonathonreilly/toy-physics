#!/usr/bin/env python3
"""Test universality of the decoherence exponent across graph parameters.

The claim: (1-pur_min) ~ C × N^(-alpha) with alpha ≈ 1.

If alpha is the SAME across different graph shapes (nodes_per_layer,
connect_radius, y_range), it's a property of the path-sum structure,
not the specific graph family. That makes it a theorem candidate.

If alpha varies, the exponent depends on graph geometry, and the
universality claim needs to be qualified.

Test: sweep each parameter while holding others fixed.
Fit alpha at each setting. Report alpha ± SE.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag

BETA = 0.8


def _topo_order(adj, n):
    in_deg = [0] * n
    for nbs in adj.values():
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
    return order


def compute_field(positions, adj, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def measure_pur_min(nl, npl, y_range, connect_radius, seed):
    """Compute pur_min for one graph."""
    k_band = [3.0, 5.0, 7.0]
    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=npl, y_range=y_range,
        connect_radius=connect_radius, rng_seed=seed)

    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    cy = sum(y for _, y in positions) / len(positions)
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))

    pm_vals = []
    for k in k_band:
        aa = propagate(positions, adj, field, src, k, blocked | set(sb))
        ab = propagate(positions, adj, field, src, k, blocked | set(sa))
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (aa[d1].conjugate() * aa[d2]
                                  + ab[d1].conjugate() * ab[d2])
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            continue
        for key in rho:
            rho[key] /= tr
        pm_vals.append(sum(abs(v) ** 2 for v in rho.values()).real)

    if not pm_vals:
        return None
    return sum(pm_vals) / len(pm_vals)


def fit_exponent(data):
    """Fit (1-pur_min) = C * N^alpha. Returns (alpha, C, R²)."""
    ns = sorted(data.keys())
    vals = [(n, 1 - data[n]) for n in ns if 1 - data[n] > 0.001]
    if len(vals) < 3:
        return None, None, None
    xs = [math.log(n) for n, _ in vals]
    ys = [math.log(v) for _, v in vals]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    if sxx < 1e-10:
        return None, None, None
    alpha = sxy / sxx
    C = math.exp(my - alpha * mx)
    r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
    return alpha, C, r2


def run_sweep(param_name, param_values, defaults, n_list, n_seeds=16):
    """Sweep one parameter, fit exponent at each value."""
    seeds = [s * 7 + 3 for s in range(n_seeds)]

    print(f"\n  Sweep: {param_name}")
    print(f"  {'value':>8s}  {'alpha':>7s}  {'C':>7s}  {'R²':>5s}  "
          f"{'pm@25':>6s}  {'pm@80':>6s}")
    print(f"  {'-' * 48}")

    alphas = []
    for pval in param_values:
        kwargs = dict(defaults)
        kwargs[param_name] = pval

        data = {}
        for nl in n_list:
            pm_all = []
            for seed in seeds:
                r = measure_pur_min(nl, **kwargs, seed=seed)
                if r is not None:
                    pm_all.append(r)
            if pm_all:
                data[nl] = sum(pm_all) / len(pm_all)

        alpha, C, r2 = fit_exponent(data)
        pm25 = data.get(25, float('nan'))
        pm80 = data.get(80, float('nan'))

        if alpha is not None:
            alphas.append(alpha)
            print(f"  {pval:8.1f}  {alpha:7.3f}  {C:7.3f}  {r2:5.3f}  "
                  f"{pm25:6.3f}  {pm80:6.3f}")
        else:
            print(f"  {pval:8.1f}  {'FAIL':>7s}")

        sys.stdout.flush()

    if len(alphas) >= 2:
        mean_a = sum(alphas) / len(alphas)
        std_a = (sum((a - mean_a) ** 2 for a in alphas) / len(alphas)) ** 0.5
        cv = std_a / abs(mean_a) if abs(mean_a) > 0 else 999
        print(f"\n  alpha = {mean_a:.3f} ± {std_a:.3f}  (CV = {cv:.2f})")
        if cv < 0.3:
            print(f"  → UNIVERSAL (CV < 0.3)")
        else:
            print(f"  → PARAMETER-DEPENDENT (CV > 0.3)")

    return alphas


def main():
    print("=" * 70)
    print("EXPONENT UNIVERSALITY TEST")
    print("  Does alpha in (1-pur_min) ~ C*N^alpha depend on graph params?")
    print("  16 seeds per N point, N = [25, 30, 40, 60, 80]")
    print("=" * 70)

    n_list = [25, 30, 40, 60, 80]
    defaults = {"npl": 25, "y_range": 12.0, "connect_radius": 3.0}

    # Sweep 1: nodes_per_layer
    a1 = run_sweep("npl", [10, 15, 25, 40], defaults, n_list)

    # Sweep 2: connect_radius
    a2 = run_sweep("connect_radius", [2.0, 3.0, 4.0, 5.0], defaults, n_list)

    # Sweep 3: y_range
    a3 = run_sweep("y_range", [6.0, 8.0, 12.0, 18.0], defaults, n_list)

    print()
    print("=" * 70)
    print("OVERALL UNIVERSALITY")
    print("=" * 70)
    all_alphas = a1 + a2 + a3
    if all_alphas:
        mean = sum(all_alphas) / len(all_alphas)
        std = (sum((a - mean) ** 2 for a in all_alphas) / len(all_alphas)) ** 0.5
        print(f"\n  All alphas: {', '.join(f'{a:.3f}' for a in all_alphas)}")
        print(f"  Mean alpha = {mean:.3f} ± {std:.3f}")
        print(f"  Range: [{min(all_alphas):.3f}, {max(all_alphas):.3f}]")
        cv = std / abs(mean) if abs(mean) > 0 else 999
        if cv < 0.3:
            print(f"\n  VERDICT: UNIVERSAL (CV={cv:.2f} < 0.3)")
            print(f"  The exponent alpha ≈ {mean:.2f} is a property of the path-sum,")
            print(f"  not of the specific graph geometry.")
        elif cv < 0.5:
            print(f"\n  VERDICT: WEAKLY UNIVERSAL (CV={cv:.2f})")
        else:
            print(f"\n  VERDICT: NOT UNIVERSAL (CV={cv:.2f} > 0.5)")


if __name__ == "__main__":
    main()
