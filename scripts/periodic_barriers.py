#!/usr/bin/env python3
"""Periodic barriers: multiple bottlenecks to reset rank-1 convergence.

The ceiling theorem: T_N...T_1 converges to rank-1 after enough layers.
A single barrier (the slit) temporarily breaks rank-1 at that layer.
But after enough post-barrier layers, rank-1 re-establishes.

Hypothesis: periodic barriers every K layers RESET the rank-1
convergence, preventing the CLT from accumulating over long stretches.
Each barrier forces amplitude through narrow slits, which preserves
the slit-specificity of the amplitude pattern.

This is the discrete analogue of "repeated weak measurements" —
periodic bottlenecks that partially project the state onto the
slit basis without fully collapsing it.

Implementation: standard 3D DAG, but with barriers at layers
barrier_0, barrier_0+K, barrier_0+2K, etc. Each barrier has the
same slit geometry (upper/lower slits at y > +3, y < -3).

Single-k CL bath purity throughout.
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
XYZ_RANGE = 12.0
CONNECT_RADIUS = 4.0
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


def generate_3d_dag_periodic_barriers(n_layers, npl, xyz_range, connect_radius,
                                       rng_seed, barrier_period):
    """3D DAG with periodic barriers every barrier_period layers.

    Each barrier has upper/lower slits at |y| > 3.
    Nodes at the barrier with |y| <= 3 become blocked.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    first_barrier = n_layers // 3  # same as standard

    barrier_layers = set()
    bl = first_barrier
    while bl < n_layers - 1:  # don't put barrier at last layer
        barrier_layers.add(bl)
        bl += barrier_period

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for _ in range(npl):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj), first_barrier, barrier_layers


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2 + (iz - mz) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate_3d(positions, adj, field, src, k, blocked):
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
            x1, y1, z1 = positions[i]
            x2, y2, z2 = positions[j]
            dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
            L = math.sqrt(dx * dx + dy * dy + dz * dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy * dy + dz * dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def bin_amplitudes_3d(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_single_k(psi_a, psi_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                psi_a[d1].conjugate() * psi_a[d2]
                + psi_b[d1].conjugate() * psi_b[d2]
                + D * psi_a[d1].conjugate() * psi_b[d2]
                + D * psi_b[d1].conjugate() * psi_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr < 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def measure(positions, adj, n_layers, k, barrier_layers):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    cy = sum(positions[i][1] for i in range(n)) / n

    # Block nodes at ALL barrier layers (not just the first)
    blocked = set()
    sa_first, sb_first = None, None
    for bl in sorted(barrier_layers):
        if bl >= len(layers):
            continue
        bi = by_layer[layers[bl]]
        sa_bl = [i for i in bi if positions[i][1] > cy + 3][:3]
        sb_bl = [i for i in bi if positions[i][1] < cy - 3][:3]
        if not sa_bl or not sb_bl:
            continue
        blocked |= set(bi) - set(sa_bl + sb_bl)
        if sa_first is None:
            sa_first = sa_bl
            sb_first = sb_bl

    if sa_first is None or sb_first is None:
        return None

    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes:
        return None
    env_depth = max(1, round(n_layers / 6))
    bl_idx = sorted(barrier_layers)[0] if barrier_layers else len(layers) // 3
    start_idx = None
    for li, lk in enumerate(layers):
        if lk > bl_idx:
            start_idx = li
            break
    if start_idx is None:
        return None
    stop = min(len(layers) - 1, start_idx + env_depth)
    mid = []
    for layer in layers[start_idx:stop]:
        mid.extend(by_layer[layer])

    field = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n

    # Single-slit propagation (block one slit at FIRST barrier only)
    blocked_b = blocked | set(sb_first)
    blocked_a = blocked | set(sa_first)

    psi_a = propagate_3d(positions, adj, field, src, k, blocked_b)
    psi_b = propagate_3d(positions, adj, field, src, k, blocked_a)

    # d_TV
    pa = {d: abs(psi_a[d]) ** 2 for d in det_list}
    pb = {d: abs(psi_b[d]) ** 2 for d in det_list}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det_list)

    # CL bath
    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    NA_amp = sum(abs(a) ** 2 for a in ba)
    NB_amp = sum(abs(b) ** 2 for b in bb)
    Sn = S / (NA_amp + NB_amp) if (NA_amp + NB_amp) > 0 else 0.0
    D_cl = math.exp(-LAM ** 2 * Sn)
    pur_cl = cl_purity_single_k(psi_a, psi_b, D_cl, det_list)

    # Gravity
    am = propagate_3d(positions, adj, field, src, k, blocked)
    af = propagate_3d(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d]) ** 2 for d in det_list)
    pf = sum(abs(af[d]) ** 2 for d in det_list)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
        grav = ym - yf

    return {"dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn, "gravity": grav,
            "n_barriers": len(barrier_layers)}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals:
        return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 100)
    print("PERIODIC BARRIERS: MULTIPLE BOTTLENECKS TO RESET RANK-1")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    periods = [999, 10, 5, 3, 2]  # 999 = single barrier (baseline)

    print(f"  {'N':>4s}  {'period':>7s}  {'n_bar':>5s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
          f"{'d_TV':>8s}  {'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    for nl in [25, 40, 60, 80]:
        for period in periods:
            t0 = time.time()
            pur_all, sn_all, dtv_all, grav_all, nbar_all = [], [], [], [], []

            for seed in seeds:
                pos, adj, first_bl, barrier_set = generate_3d_dag_periodic_barriers(
                    nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, period)
                r = measure(pos, adj, nl, K, barrier_set)
                if r:
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    dtv_all.append(r["dtv"])
                    grav_all.append(r["gravity"])
                    nbar_all.append(r["n_barriers"])

            dt = time.time() - t0
            if pur_all:
                mpur, sepur = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                mdtv, _ = _mean_se(dtv_all)
                mg, seg = _mean_se(grav_all)
                mnbar = sum(nbar_all) / len(nbar_all)
                plabel = f"{period}" if period < 100 else "single"
                print(f"  {nl:4d}  {plabel:>7s}  {mnbar:5.1f}  {mpur:7.4f}±{sepur:.02f}  "
                      f"{msn:8.4f}  {mdtv:8.4f}  {mg:+7.4f}±{seg:.3f}  "
                      f"{len(pur_all):3d}  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  period=single: one barrier at N/3 (standard)")
    print("  period=K: barriers every K layers starting at N/3")
    print("  More barriers → more bottlenecks → more rank-1 resets")
    print("  If pur_cl drops with more barriers: periodic reset works")
    print("  Watch d_TV: should INCREASE with more barriers")


if __name__ == "__main__":
    main()
