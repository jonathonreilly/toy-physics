#!/usr/bin/env python3
"""Analytical CLT ceiling: quantify how 1-pur_min scales with N.

The ceiling diagnosis showed pur_min → 1 at large N. But how fast?
If (1-pur_min) ~ 1/N^alpha, alpha determines the effective range of
the model.

This script measures pur_min at many N values with 24 seeds to get
a clean power-law fit. Also decomposes the mechanism:

1. Overlap of single-slit detector distributions:
   O = |Σ_d ψ_A*(d) ψ_B(d)|² / (Σ_d |ψ_A(d)|² × Σ_d |ψ_B(d)|²)
   O → 1 means slits become indistinguishable at detectors.

2. pur_min = function of O (derives from 2-slit density matrix).

If O follows a clean scaling law, the ceiling is analytically understood.
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
            r = math.sqrt((ix-mx)**2 + (iy-my)**2) + 0.1
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
            dx, dy = x2-x1, y2-y1
            L = math.sqrt(dx*dx + dy*dy)
            if L < 1e-10:
                continue
            lf = 0.5*(field[i]+field[j])
            dl = L*(1+lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA*theta*theta)
            ea = cmath.exp(1j*k*act)*w/L
            amps[j] += amps[i]*ea
    return amps


def run_one(nl, seed):
    """Return (pur_min, overlap) for one graph at one seed."""
    k_band = [3.0, 5.0, 7.0]

    positions, adj, _ = generate_causal_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed,
    )

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
    mass_nodes = []
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + max(1, round(nl / 6)))
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))

    pm_list = []
    overlap_list = []

    for k in k_band:
        amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
        amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

        # pur_min (D=0)
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            continue
        for key in rho:
            rho[key] /= tr
        pur_min = sum(abs(v) ** 2 for v in rho.values()).real
        pm_list.append(pur_min)

        # Overlap O = |Σ_d ψ_A*(d) ψ_B(d)|² / (NA × NB)
        inner = sum(amps_a[d].conjugate() * amps_b[d] for d in det_list)
        NA = sum(abs(amps_a[d]) ** 2 for d in det_list)
        NB = sum(abs(amps_b[d]) ** 2 for d in det_list)
        if NA > 1e-30 and NB > 1e-30:
            O = abs(inner) ** 2 / (NA * NB)
            overlap_list.append(O)

    if not pm_list:
        return None
    return {
        "pm": sum(pm_list) / len(pm_list),
        "overlap": sum(overlap_list) / len(overlap_list) if overlap_list else 0,
    }


def main():
    print("=" * 70)
    print("CLT CEILING SCALING LAW")
    print("  How fast does (1 - pur_min) shrink with N?")
    print("  24 seeds per N point")
    print("=" * 70)
    print()

    n_seeds = 24
    seeds = [s * 7 + 3 for s in range(n_seeds)]
    n_list = [12, 15, 18, 22, 25, 30, 35, 40, 50, 60, 80, 100]

    print(f"  {'N':>4s}  {'pur_min':>8s}  {'SE':>6s}  {'1-pm':>8s}  "
          f"{'overlap':>8s}  {'1-O':>8s}")
    print(f"  {'-' * 48}")

    data = {}

    for nl in n_list:
        pm_all, ov_all = [], []
        for seed in seeds:
            r = run_one(nl, seed)
            if r:
                pm_all.append(r["pm"])
                ov_all.append(r["overlap"])

        if pm_all:
            apm = sum(pm_all) / len(pm_all)
            se = (sum((p - apm) ** 2 for p in pm_all) / len(pm_all)) ** 0.5 / math.sqrt(len(pm_all))
            aov = sum(ov_all) / len(ov_all) if ov_all else 0
            data[nl] = {"pm": apm, "se": se, "ov": aov}
            print(f"  {nl:4d}  {apm:8.4f}  {se:6.4f}  {1-apm:8.4f}  "
                  f"{aov:8.4f}  {1-aov:8.4f}")
        sys.stdout.flush()

    # Power law fit: (1-pur_min) = C * N^(-alpha) for N >= 25
    print()
    print("=" * 70)
    print("SCALING LAW FITS (N >= 25)")
    print("=" * 70)

    fit_ns = [n for n in sorted(data.keys()) if n >= 25 and data[n]["pm"] < 0.999]
    if len(fit_ns) >= 4:
        # Fit (1-pur_min) vs N
        xs = [math.log(n) for n in fit_ns]
        ys = [math.log(1 - data[n]["pm"]) for n in fit_ns if 1 - data[n]["pm"] > 1e-10]
        xs = xs[:len(ys)]

        if len(xs) >= 3:
            n = len(xs)
            mx = sum(xs) / n
            my = sum(ys) / n
            sxx = sum((x - mx) ** 2 for x in xs)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
            syy = sum((y - my) ** 2 for y in ys)
            if sxx > 1e-10:
                alpha = sxy / sxx
                C = math.exp(my - alpha * mx)
                r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0

                print(f"\n  (1-pur_min) = {C:.4f} * N^{alpha:.3f}")
                print(f"  R² = {r2:.4f}")
                print()

                print(f"  {'N':>4s}  {'measured':>8s}  {'predicted':>9s}")
                print(f"  {'-' * 25}")
                for nl in fit_ns[:len(ys)]:
                    meas = 1 - data[nl]["pm"]
                    pred = C * nl ** alpha
                    print(f"  {nl:4d}  {meas:8.4f}  {pred:9.4f}")

                print()
                if alpha < -0.3:
                    print(f"  alpha = {alpha:.2f} < 0: decoherence WEAKENS with N")
                    print(f"  Half-life: pur_min reaches 0.99 at N ≈ {(0.01/C)**(1/alpha):.0f}")
                else:
                    print(f"  alpha = {alpha:.2f} ≥ 0: decoherence stable or growing")

        # Same for overlap
        xs_o = [math.log(n) for n in fit_ns]
        ys_o = [math.log(1 - data[n]["ov"]) for n in fit_ns if 1 - data[n]["ov"] > 1e-10]
        xs_o = xs_o[:len(ys_o)]

        if len(xs_o) >= 3:
            n = len(xs_o)
            mx = sum(xs_o) / n
            my = sum(ys_o) / n
            sxx = sum((x - mx) ** 2 for x in xs_o)
            sxy = sum((x - mx) * (y - my) for x, y in zip(xs_o, ys_o))
            syy = sum((y - my) ** 2 for y in ys_o)
            if sxx > 1e-10:
                alpha_o = sxy / sxx
                C_o = math.exp(my - alpha_o * mx)
                r2_o = (sxy ** 2) / (sxx * syy) if syy > 0 else 0

                print(f"\n  (1-overlap) = {C_o:.4f} * N^{alpha_o:.3f}")
                print(f"  R² = {r2_o:.4f}")
                if alpha_o < -0.3:
                    print(f"  Overlap approaches 1 as N^{alpha_o:.2f}")
                    print(f"  This drives the pur_min ceiling")

    print()
    print("INTERPRETATION:")
    print("  If (1-pur_min) ~ N^(-alpha) with alpha > 0:")
    print("    → decoherence has power-law decay, never truly zero")
    print("    → effective range of model is N < (target_decoherence / C)^(1/alpha)")


if __name__ == "__main__":
    main()
