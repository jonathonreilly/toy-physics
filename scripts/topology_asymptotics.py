#!/usr/bin/env python3
"""Asymptotic scaling law for modular DAG decoherence.

Push to N=80, 100, 120 with 12 seeds per point.
Fit (1 - pur_min) to power law and log forms.
Report with standard error for publication-grade error bars.

This is the locking experiment: establishes the scaling law
that defines the architecture story.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.topology_families import generate_modular_dag

BETA = 0.8
N_YBINS = 8
LAM = 10.0


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


def build_setup(positions, adj, env_depth_layers=1):
    n = len(positions)
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
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
    bl_idx = len(layers) // 3
    bl = layers[bl_idx]
    bi = by_layer[bl]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    start = bl_idx + 1
    stop = min(len(layers), start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    if len(mass_nodes) < 2:
        return None
    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))
    return {
        "by_layer": by_layer, "layers": layers, "src": src,
        "det_list": det_list, "cy": cy, "blocked": blocked, "field": field,
        "sa": sa, "sb": sb, "bl_idx": bl_idx,
    }


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_triple(amps_a, amps_b, D, det_list):
    def _pur(Dv):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + Dv * amps_a[d1].conjugate() * amps_b[d2]
                    + Dv * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def run_single_graph(nl, seed):
    """Run one graph, return per-seed metrics or None."""
    k_band = [3.0, 5.0, 7.0]
    positions, adj, _ = generate_modular_dag(
        n_layers=nl, nodes_per_layer=25, y_range=12.0,
        connect_radius=3.0, rng_seed=seed, crosslink_prob=0.02, gap=4.0,
    )
    setup = build_setup(positions, adj, env_depth_layers=max(1, round(nl / 6)))
    if setup is None:
        return None

    blocked = setup["blocked"]
    field = setup["field"]
    src = setup["src"]
    det_list = setup["det_list"]
    by_layer = setup["by_layer"]
    layers = setup["layers"]
    bl_idx = setup["bl_idx"]
    sa = setup["sa"]
    sb = setup["sb"]

    pm_k, pc_k, pcoh_k, sn_k = [], [], [], []
    for k in k_band:
        amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
        amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

        start = bl_idx + 1
        stop = min(len(layers), start + max(1, round(nl / 6)))
        mid = []
        for layer in layers[start:stop]:
            mid.extend(by_layer[layer])

        ba = bin_amplitudes(amps_a, positions, mid)
        bb = bin_amplitudes(amps_b, positions, mid)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D = math.exp(-LAM ** 2 * Sn)

        pc, pcoh, pmin = cl_purity_triple(amps_a, amps_b, D, det_list)
        if not math.isnan(pc):
            pm_k.append(pmin)
            pc_k.append(pc)
            pcoh_k.append(pcoh)
            sn_k.append(Sn)

    if not pm_k:
        return None
    return {
        "pm": sum(pm_k) / len(pm_k),
        "pc": sum(pc_k) / len(pc_k),
        "pcoh": sum(pcoh_k) / len(pcoh_k),
        "sn": sum(sn_k) / len(sn_k),
    }


def least_squares_log(xs, ys):
    """Fit log(y) = a + b*log(x) → y = exp(a) * x^b. Returns (a, b, r²)."""
    n = len(xs)
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    syy = sum((y - my) ** 2 for y in ly)
    if sxx < 1e-30:
        return 0, 0, 0
    b = sxy / sxx
    a = my - b * mx
    r2 = (sxy ** 2) / (sxx * syy) if syy > 0 else 0
    return a, b, r2


def main():
    print("=" * 74)
    print("ASYMPTOTIC SCALING LAW: Modular DAG Decoherence")
    print(f"  CL bath lambda={LAM}, gap=4.0, 12 seeds per N")
    print(f"  k-band [3,5,7], modular DAG with crosslink=0.02")
    print("=" * 74)
    print()

    n_layers_list = [12, 18, 25, 30, 40, 50, 60, 80, 100]
    n_seeds = 12
    # Use diverse seed spacing to avoid systematic bias
    seeds = [s * 13 + 5 for s in range(n_seeds)]

    print(f"  {'N':>4s}  {'pur_min':>8s}  {'SE':>6s}  {'1-pm':>7s}  "
          f"{'decoh':>8s}  {'S_norm':>8s}  {'n_ok':>4s}  {'time':>6s}")
    print(f"  {'-' * 62}")

    data = {}

    for nl in n_layers_list:
        t0 = time.time()
        results = []

        for seed in seeds:
            r = run_single_graph(nl, seed)
            if r is not None:
                results.append(r)

        dt = time.time() - t0

        if len(results) >= 3:
            pms = [r["pm"] for r in results]
            pcs = [r["pc"] for r in results]
            pcohs = [r["pcoh"] for r in results]
            sns = [r["sn"] for r in results]

            n_ok = len(results)
            avg_pm = sum(pms) / n_ok
            avg_pc = sum(pcs) / n_ok
            avg_pcoh = sum(pcohs) / n_ok
            avg_sn = sum(sns) / n_ok
            std_pm = (sum((p - avg_pm) ** 2 for p in pms) / n_ok) ** 0.5
            se_pm = std_pm / math.sqrt(n_ok)
            decoh = avg_pcoh - avg_pc
            one_minus = 1 - avg_pm

            data[nl] = {
                "pm": avg_pm, "se": se_pm, "one_minus": one_minus,
                "decoh": decoh, "sn": avg_sn, "n_ok": n_ok,
            }
            print(f"  {nl:4d}  {avg_pm:8.4f}  {se_pm:6.4f}  {one_minus:7.4f}  "
                  f"{decoh:+8.4f}  {avg_sn:8.5f}  {n_ok:4d}  {dt:5.0f}s")
        else:
            print(f"  {nl:4d}  FAIL ({len(results)} graphs)")

        sys.stdout.flush()

    # ─── Scaling law fit ───────────────────────────────────────────
    print()
    print("=" * 74)
    print("SCALING LAW FIT")
    print("=" * 74)

    # Fit (1 - pur_min) = C * N^alpha for N >= 25
    fit_ns = [n for n in sorted(data.keys()) if n >= 25 and data[n]["one_minus"] > 0]
    if len(fit_ns) >= 3:
        xs = fit_ns
        ys = [data[n]["one_minus"] for n in fit_ns]

        a, alpha, r2 = least_squares_log(xs, ys)
        C = math.exp(a)

        print(f"\n  Power law: (1 - pur_min) = {C:.4f} * N^{alpha:.3f}")
        print(f"  R² = {r2:.4f}")
        print()
        print(f"  {'N':>4s}  {'measured':>8s}  {'predicted':>9s}  {'residual':>8s}")
        print(f"  {'-' * 35}")
        for n in fit_ns:
            measured = data[n]["one_minus"]
            predicted = C * n ** alpha
            residual = measured - predicted
            print(f"  {n:4d}  {measured:8.4f}  {predicted:9.4f}  {residual:+8.4f}")

        print()
        if alpha > 0:
            print(f"  alpha = {alpha:.3f} > 0: DECOHERENCE STRENGTHENS WITH N")
            print(f"  Extrapolations:")
            for n_ext in [200, 500, 1000]:
                pred = C * n_ext ** alpha
                pm_pred = 1 - pred
                print(f"    N={n_ext:4d}: (1-pur_min) ~ {pred:.3f}  →  pur_min ~ {pm_pred:.3f}")
        elif alpha < -0.1:
            print(f"  alpha = {alpha:.3f} < 0: decoherence weakens (ceiling returns)")
        else:
            print(f"  alpha ~ 0: decoherence roughly constant with N")

    # ─── S_norm scaling ────────────────────────────────────────────
    fit_sns = [n for n in sorted(data.keys()) if n >= 25]
    if len(fit_sns) >= 3:
        xs_s = fit_sns
        ys_s = [data[n]["sn"] for n in fit_sns]
        a_s, alpha_s, r2_s = least_squares_log(xs_s, ys_s)
        C_s = math.exp(a_s)
        print(f"\n  S_norm scaling: S_norm = {C_s:.4f} * N^{alpha_s:.3f}  (R²={r2_s:.3f})")
        if alpha_s > 0:
            print(f"  Bath contrast GROWS with N (alpha_S = {alpha_s:.3f})")
        else:
            print(f"  Bath contrast shrinks with N")

    print()
    print("TEST COMPLETE")


if __name__ == "__main__":
    main()
