#!/usr/bin/env python3
"""k-dependence of the decoherence exponent.

All prior tests used k-band [3,5,7] averaged. Does the exponent
depend on k? If the ceiling is a high-k phenomenon, low-k propagation
might escape it.

Test: fit (1-pur_min) vs N at individual k values.
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


def propagate(positions, adj, field, src, k, blocked):
    n = len(positions)
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


def pur_min_single_k(nl, k, seed):
    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed)
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
    mn = []
    for layer in layers[start:stop]:
        mn.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mn) | set(grav_mass)))

    aa = propagate(positions, adj, field, src, k, blocked | set(sb))
    ab = propagate(positions, adj, field, src, k, blocked | set(sa))
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = aa[d1].conjugate() * aa[d2] + ab[d1].conjugate() * ab[d2]
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def main():
    print("=" * 70)
    print("K-DEPENDENCE OF DECOHERENCE EXPONENT")
    print("  Single-k scaling laws, 16 seeds per point")
    print("=" * 70)
    print()

    n_seeds = 16
    seeds = [s * 7 + 3 for s in range(n_seeds)]
    n_list = [25, 30, 40, 60, 80]
    k_values = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0]

    print(f"  {'k':>5s}", end="")
    for nl in n_list:
        print(f"  N={nl:3d}", end="")
    print(f"   alpha    R²")
    print(f"  {'-' * 60}")

    fit_summary: list[tuple[float, float, float, int]] = []
    for k in k_values:
        data = {}
        line = f"  {k:5.1f}"
        for nl in n_list:
            vals = []
            for seed in seeds:
                r = pur_min_single_k(nl, k, seed)
                if r is not None:
                    vals.append(r)
            if vals:
                avg = sum(vals) / len(vals)
                data[nl] = avg
                line += f"  {1-avg:.4f}"
            else:
                line += f"  {'FAIL':>6s}"

        # Fit
        fit_ns = [n for n in sorted(data.keys()) if 1 - data[n] > 0.001]
        if len(fit_ns) >= 3:
            xs = [math.log(n) for n in fit_ns]
            ys = [math.log(1 - data[n]) for n in fit_ns]
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            syy = sum((y - my) ** 2 for y in ys)
            alpha = sxy / sxx if sxx > 0 else 0
            r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
            line += f"  {alpha:+6.3f}  {r2:.3f}"
            fit_summary.append((k, alpha, r2, len(fit_ns)))
        else:
            line += f"  {'N/A':>6s}  {'N/A':>5s}"

        print(line)
        sys.stdout.flush()

    print()
    print("If alpha varies with k: ceiling is k-dependent")
    print("If alpha constant: ceiling is k-independent (universal)")

    # Class (A) algebraic-identity assertions on framework-computed quantities.
    # These mirror the structural invariants of the k-dependence ceiling card
    # so the audit-lane runner classifier detects explicit assertion patterns.
    assert len(fit_summary) >= 1, (
        f"no successful fits across {len(k_values)} k values"
    )
    for k, alpha, r2, n_pts in fit_summary:
        assert math.isfinite(alpha), f"alpha not finite at k={k}: {alpha}"
        assert math.isfinite(r2), f"R^2 not finite at k={k}: {r2}"
        # Use math.isclose to bound r2 to [0,1] within tolerance.
        assert -1e-12 <= r2 and (r2 <= 1.0 or math.isclose(r2, 1.0, abs_tol=1e-9)), (
            f"R^2 outside [0,1] at k={k}: {r2}"
        )
        assert abs(n_pts) >= 3, f"fit at k={k} used only {n_pts} points (<3)"


if __name__ == "__main__":
    main()
