#!/usr/bin/env python3
"""Cumulative slit-specificity: weights accumulate over iterations.

The soft specificity (Exp previous) recomputes weights from scratch each
iteration, so the CLT erases the signal at large N. This script tests
whether CUMULATIVE weights — growing over iterations rather than
resetting — can outrun the CLT.

Mechanism:
  t=0: uniform weights w=1.0
  t=1: propagate → compute specificity → w *= (1 + alpha * spec)
  t=2: propagate with w from t=1 → new specificity → w *= (1 + alpha * spec)
  ...
  t=T: weights have accumulated T rounds of specificity reinforcement

The hypothesis: each iteration amplifies the channel signal. Even if
the specificity is weak per-step (CLT), the multiplicative accumulation
creates exponential separation between channel-specific and cross-channel
edges. This could outrun the CLT's polynomial convergence.

Also test: momentum variant where w_new = beta*w_old + (1-beta)*w_fresh.
This smooths the accumulation and prevents runaway weights.

Single-k throughout, CL bath purity.
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

BETA_DIR = 0.8  # directional measure
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


def generate_3d_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
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
    return positions, dict(adj), n_layers // 3


def propagate_weighted(positions, adj, field, src, k, blocked, edge_weights):
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    traffic = {}
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
            w = math.exp(-BETA_DIR * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            ew = edge_weights.get((i, j), 1.0)
            contrib = amps[i] * ea * ew
            amps[j] += contrib
            traffic[(i, j)] = abs(contrib)
    return amps, traffic


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


def run_cumulative(positions, adj, field, src, det_nodes, blocked, sa, sb,
                    mid, k, alpha, T, momentum=1.0):
    """Run T iterations of cumulative specificity weighting.

    momentum=1.0: pure accumulation (w *= 1 + alpha*spec)
    momentum<1.0: w = momentum*w_old + (1-momentum)*(1 + alpha*spec)
    """
    edge_weights = {}  # start uniform

    for t in range(T):
        # Propagate each slit separately to get slit-specific traffic
        _, traf_a = propagate_weighted(positions, adj, field, src, k,
                                       blocked | set(sb), edge_weights)
        _, traf_b = propagate_weighted(positions, adj, field, src, k,
                                       blocked | set(sa), edge_weights)

        # Compute specificity
        all_edges = set(list(traf_a.keys()) + list(traf_b.keys()))
        for edge in all_edges:
            ta = traf_a.get(edge, 0)
            tb = traf_b.get(edge, 0)
            total = ta + tb
            spec = abs(ta - tb) / total if total > 1e-30 else 0

            # Update weight
            fresh = 1.0 + alpha * spec
            old = edge_weights.get(edge, 1.0)
            if momentum >= 0.99:
                # Pure multiplicative accumulation
                edge_weights[edge] = old * fresh
            else:
                # Momentum-smoothed
                edge_weights[edge] = momentum * old + (1 - momentum) * fresh

    # Final measurement
    psi_a, _ = propagate_weighted(positions, adj, field, src, k,
                                   blocked | set(sb), edge_weights)
    psi_b, _ = propagate_weighted(positions, adj, field, src, k,
                                   blocked | set(sa), edge_weights)

    # d_TV
    pa = {d: abs(psi_a[d]) ** 2 for d in det_nodes}
    pb = {d: abs(psi_b[d]) ** 2 for d in det_nodes}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d] / na - pb[d] / nb) for d in det_nodes)

    # CL bath
    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
    NA_amp = sum(abs(a) ** 2 for a in ba)
    NB_amp = sum(abs(b) ** 2 for b in bb)
    Sn = S / (NA_amp + NB_amp) if (NA_amp + NB_amp) > 0 else 0.0
    D_cl = math.exp(-LAM ** 2 * Sn)
    pur_cl = cl_purity_single_k(psi_a, psi_b, D_cl, det_nodes)

    # Gravity
    field_f = [0.0] * len(positions)
    am, _ = propagate_weighted(positions, adj, field, src, k, blocked, edge_weights)
    af, _ = propagate_weighted(positions, adj, field_f, src, k, blocked, edge_weights)
    pm = sum(abs(am[d]) ** 2 for d in det_nodes)
    pf = sum(abs(af[d]) ** 2 for d in det_nodes)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_nodes) / pm
        yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_nodes) / pf
        grav = ym - yf

    # Weight statistics
    wvals = list(edge_weights.values())
    w_max = max(wvals) if wvals else 1.0
    w_min = min(wvals) if wvals else 1.0
    w_ratio = w_max / max(w_min, 1e-30)

    return {
        "dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn, "gravity": grav,
        "w_ratio": w_ratio,
    }


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
    print("=" * 110)
    print("CUMULATIVE SLIT-SPECIFICITY WEIGHTING")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print("=" * 110)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("base", 0.0, 0, 1.0),
        ("a=0.5 T=3", 0.5, 3, 1.0),
        ("a=0.5 T=10", 0.5, 10, 1.0),
        ("a=0.5 T=30", 0.5, 30, 1.0),
        ("a=1.0 T=3", 1.0, 3, 1.0),
        ("a=1.0 T=10", 1.0, 10, 1.0),
        ("a=1.0 T=30", 1.0, 30, 1.0),
        ("a=0.5 T=10 m=0.9", 0.5, 10, 0.9),
        ("a=0.5 T=30 m=0.9", 0.5, 30, 0.9),
        ("a=1.0 T=10 m=0.9", 1.0, 10, 0.9),
    ]

    for nl in [25, 40, 60]:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'config':>18s}  {'pur_cl':>8s}  {'S_norm':>8s}  {'d_TV':>8s}  "
              f"{'gravity':>10s}  {'w_ratio':>8s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 82}")

        for label, alpha, T, momentum in configs:
            t0 = time.time()
            pur_all, sn_all, dtv_all, grav_all, wr_all = [], [], [], [], []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7:
                    continue
                src = by_layer[layers[0]]
                det_nodes = by_layer[layers[-1]]
                if not det_nodes:
                    continue
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb:
                    continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                if not mass_nodes:
                    continue
                field = compute_field_3d(pos, mass_nodes)
                env_depth = max(1, round(nl / 6))
                start = bl_idx + 1
                stop = min(len(layers) - 1, start + env_depth)
                mid = []
                for layer in layers[start:stop]:
                    mid.extend(by_layer[layer])

                r = run_cumulative(pos, adj, field, src, det_nodes, blocked,
                                    sa, sb, mid, K, alpha, T, momentum)
                if r:
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    dtv_all.append(r["dtv"])
                    grav_all.append(r["gravity"])
                    wr_all.append(r["w_ratio"])

            dt = time.time() - t0
            if pur_all:
                mpur, sepur = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                mdtv, _ = _mean_se(dtv_all)
                mg, seg = _mean_se(grav_all)
                mwr, _ = _mean_se(wr_all)
                print(f"  {label:>18s}  {mpur:7.4f}±{sepur:.2f}  {msn:8.4f}  {mdtv:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {mwr:8.1f}  {len(pur_all):3d}  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  Cumulative: weights multiply each iteration (exponential growth)")
    print("  Momentum (m<1): smoothed accumulation (prevents runaway)")
    print("  w_ratio: max_weight/min_weight (channel separation strength)")
    print("  If pur_cl drops with more T: cumulative outruns CLT")
    print("  If w_ratio grows exponentially: feedback loop is real")


if __name__ == "__main__":
    main()
