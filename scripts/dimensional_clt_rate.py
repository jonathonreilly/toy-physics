#!/usr/bin/env python3
"""Dimensional CLT rate: does higher d slow the ceiling?

3D delays the CLT ceiling ~2x vs 2D. If the rate scales as 1/d,
then d→∞ would break the ceiling entirely.

Test: generate d-dimensional causal DAGs for d=2,3,4,5,6.
Measure (1-pur_cl) vs N for each d.
Fit the CLT exponent alpha(d).
Extrapolate: does alpha → 0 as d → ∞?

Each node has d spatial coordinates + 1 causal (x).
Slit separation is always in the first spatial coordinate (y).
Extra dimensions provide independent noise.

Single-k CL bath throughout.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
N_SEEDS = 16
NPL = 30
COORD_RANGE = 12.0
CONNECT_RADIUS = 4.0
N_YBINS = 8
LAM = 10.0
N_LAYERS_LIST = [15, 25, 40, 60]


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


def generate_d_dim_dag(n_layers, npl, coord_range, connect_radius, rng_seed, d_spatial):
    """Generate d-dimensional causal DAG.

    Each node: (x, y, z1, z2, ..., z_{d-2}) where x is causal.
    Slit separation in y (coord index 1).
    """
    rng = random.Random(rng_seed)
    positions = []  # list of tuples of length d_spatial + 1
    adj = defaultdict(list)
    layer_indices = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            pos = tuple([x] + [0.0] * d_spatial)
            positions.append(pos)
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(npl):
                coords = [x] + [rng.uniform(-coord_range, coord_range) for _ in range(d_spatial)]
                idx = len(positions)
                positions.append(tuple(coords))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        pp = positions[prev_idx]
                        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(coords, pp)))
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj), n_layers // 3


def propagate_dd(positions, adj, field, src, k, blocked, d_spatial):
    """d-dimensional propagator. Directional measure uses angle from x-axis."""
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
            pi, pj = positions[i], positions[j]
            diffs = [pj[k2] - pi[k2] for k2 in range(d_spatial + 1)]
            dx = diffs[0]
            transverse_sq = sum(d ** 2 for d in diffs[1:])
            L = math.sqrt(dx * dx + transverse_sq)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(transverse_sq), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def compute_field_dd(positions, mass_nodes, d_spatial):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        pm = positions[m]
        for i in range(n):
            pi = positions[i]
            r = math.sqrt(sum((a - b) ** 2 for a, b in zip(pi, pm))) + 0.1
            field[i] += 0.1 / r
    return field


def measure_single_k(positions, adj, n_layers, k, d_spatial):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, pos in enumerate(positions):
        by_layer[round(pos[0])].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    # y is coord index 1
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None
    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    field = compute_field_dd(positions, mass_nodes, d_spatial)

    psi_a = propagate_dd(positions, adj, field, src, k, blocked | set(sb), d_spatial)
    psi_b = propagate_dd(positions, adj, field, src, k, blocked | set(sa), d_spatial)

    # d_TV
    pa = {d: abs(psi_a[d]) ** 2 for d in det_list}
    pb = {d: abs(psi_b[d]) ** 2 for d in det_list}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det_list)

    # CL bath (bin by y-coordinate)
    bins_a = [0j] * N_YBINS
    bins_b = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in mid:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins_a[b] += psi_a[m]
        bins_b[b] += psi_b[m]
    S = sum(abs(a - b) ** 2 for a, b in zip(bins_a, bins_b))
    NA_amp = sum(abs(a) ** 2 for a in bins_a)
    NB_amp = sum(abs(b) ** 2 for b in bins_b)
    Sn = S / (NA_amp + NB_amp) if (NA_amp + NB_amp) > 0 else 0.0
    D_cl = math.exp(-LAM ** 2 * Sn)

    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                psi_a[d1].conjugate() * psi_a[d2]
                + psi_b[d1].conjugate() * psi_b[d2]
                + D_cl * psi_a[d1].conjugate() * psi_b[d2]
                + D_cl * psi_b[d1].conjugate() * psi_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr < 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_cl = sum(abs(v) ** 2 for v in rho.values()).real

    return {"dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def fit_power_law(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if y > 0 and not math.isnan(y)]
    if len(pairs) < 3:
        return float('nan'), float('nan'), float('nan')
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx < 1e-10:
        return float('nan'), float('nan'), float('nan')
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return math.exp(a), b, r2


def main():
    print("=" * 100)
    print("DIMENSIONAL CLT RATE: d=2..6")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    print(f"  {'d':>3s}  {'N':>4s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
          f"{'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 48}")

    # Collect for power law fits
    fit_data = {}

    for d in [2, 3, 4, 5, 6]:
        fit_data[d] = ([], [])
        for nl in N_LAYERS_LIST:
            t0 = time.time()
            dtv_all, pur_all, sn_all = [], [], []
            for seed in seeds:
                # Scale radius with d to maintain connectivity
                # In d dimensions, need larger radius to reach same # neighbors
                scaled_radius = CONNECT_RADIUS * (1 + 0.3 * (d - 2))
                pos, adj, bl = generate_d_dim_dag(nl, NPL, COORD_RANGE, scaled_radius, seed, d)
                r = measure_single_k(pos, adj, nl, K, d)
                if r:
                    dtv_all.append(r["dtv"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
            dt = time.time() - t0
            if pur_all:
                mdtv, _ = _mean_se(dtv_all)
                mpur, _ = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                omp = 1 - mpur
                print(f"  {d:3d}  {nl:4d}  {mdtv:8.4f}  {mpur:8.4f}  {msn:8.4f}  "
                      f"{len(pur_all):3d}  {dt:4.0f}s")
                if omp > 0.001:
                    fit_data[d][0].append(nl)
                    fit_data[d][1].append(omp)
            else:
                print(f"  {d:3d}  {nl:4d}  FAIL  {dt:4.0f}s")
        print()

    # Power law fits per dimension
    print("CLT EXPONENT vs DIMENSION")
    print(f"  {'d':>3s}  {'A':>8s}  {'alpha':>8s}  {'R²':>6s}")
    print(f"  {'-' * 30}")
    alphas = []
    for d in [2, 3, 4, 5, 6]:
        ns, ys = fit_data[d]
        A, alpha, r2 = fit_power_law(ns, ys)
        if not math.isnan(alpha):
            print(f"  {d:3d}  {A:8.3f}  {alpha:8.2f}  {r2:6.3f}")
            alphas.append((d, alpha))
        else:
            print(f"  {d:3d}  insufficient data")

    print()
    if len(alphas) >= 3:
        ds = [a[0] for a in alphas]
        als = [a[1] for a in alphas]
        # Fit alpha(d) to see if it approaches 0
        print(f"  alpha vs d: {', '.join(f'd={d}→{a:.2f}' for d, a in alphas)}")
        if all(a < 0 for _, a in alphas):
            trend = "all negative (ceiling exists at all d)"
            if als[-1] > als[0]:
                trend += " but weakening with d"
        elif any(a >= 0 for _, a in alphas):
            trend = "POSITIVE exponent at high d — ceiling may break"
        else:
            trend = "mixed"
        print(f"  Trend: {trend}")


if __name__ == "__main__":
    main()
