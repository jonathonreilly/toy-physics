#!/usr/bin/env python3
"""Soft slit-specificity channels: robust version of V4.

V4 (hard slit-prune) tripled d_TV but broke connectivity on 50% of seeds.
This script uses SOFT edge weights instead of hard pruning:

For each edge (i,j), compute slit-specificity:
  spec(i,j) = |traffic_A(i,j) - traffic_B(i,j)| / (traffic_A(i,j) + traffic_B(i,j))

Then weight edges by specificity:
  w(i,j) = 1 + alpha * spec(i,j)

High-specificity edges (slit-specific) get amplified.
Low-specificity edges (cross-channel) get unchanged (not removed).
No connectivity loss.

Iterate: propagate → compute specificity → update weights → repeat.
The weights should converge to a functional channel structure.

Also test: feed the specificity back as a FIELD rather than edge weight.
Nodes in high-specificity regions get a field boost, creating a
self-consistent geometry where channels reinforce themselves.

Key question: does iterated soft weighting create enough functional
separation for genuine decoherence (measured at single-k)?
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
            layer_nodes.append(len(positions)-1)
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
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def propagate_weighted(positions, adj, field, src, k, blocked, edge_weights=None):
    n = len(positions)
    blocked = blocked or set()
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
            dx, dy, dz = x2-x1, y2-y1, z2-z1
            L = math.sqrt(dx*dx + dy*dy + dz*dz)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            ew = edge_weights.get((i, j), 1.0) if edge_weights else 1.0
            contrib = amps[i] * ea * ew
            amps[j] += contrib
            traffic[(i, j)] = abs(contrib)
    return amps, traffic


def compute_slit_specificity(positions, adj, field, src, k, blocked, sa, sb, edge_weights=None):
    """Compute per-edge slit specificity."""
    _, traf_a = propagate_weighted(positions, adj, field, src, k,
                                    blocked | set(sb), edge_weights)
    _, traf_b = propagate_weighted(positions, adj, field, src, k,
                                    blocked | set(sa), edge_weights)
    spec = {}
    for edge in set(list(traf_a.keys()) + list(traf_b.keys())):
        ta = traf_a.get(edge, 0)
        tb = traf_b.get(edge, 0)
        total = ta + tb
        spec[edge] = abs(ta - tb) / total if total > 1e-30 else 0
    return spec


def specificity_to_weights(spec, alpha):
    """Convert slit specificity to edge weights."""
    return {edge: 1.0 + alpha * s for edge, s in spec.items()}


def compute_field_3d(positions, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my, mz = positions[m]
        for i in range(n):
            ix, iy, iz = positions[i]
            r = math.sqrt((ix-mx)**2 + (iy-my)**2 + (iz-mz)**2) + 0.1
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


def measure_single_k(positions, adj, src, det_nodes, blocked, sa, sb,
                      field, k, mid, edge_weights=None):
    """Single-k measurement: d_TV, CL bath purity, gravity."""
    psi_a, _ = propagate_weighted(positions, adj, field, src, k,
                                   blocked | set(sb), edge_weights)
    psi_b, _ = propagate_weighted(positions, adj, field, src, k,
                                   blocked | set(sa), edge_weights)

    # d_TV
    pa = {d: abs(psi_a[d])**2 for d in det_nodes}
    pb = {d: abs(psi_b[d])**2 for d in det_nodes}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d]/na - pb[d]/nb) for d in det_nodes)

    # CL bath purity (single-k, genuine)
    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
    NA_amp = sum(abs(a)**2 for a in ba)
    NB_amp = sum(abs(b)**2 for b in bb)
    Sn = S / (NA_amp + NB_amp) if (NA_amp + NB_amp) > 0 else 0.0
    D_cl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det_nodes:
        for d2 in det_nodes:
            rho[(d1, d2)] = (
                psi_a[d1].conjugate() * psi_a[d2]
                + psi_b[d1].conjugate() * psi_b[d2]
                + D_cl * psi_a[d1].conjugate() * psi_b[d2]
                + D_cl * psi_b[d1].conjugate() * psi_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_nodes).real
    if tr < 1e-30:
        return None
    for key in rho:
        rho[key] /= tr
    pur_cl = sum(abs(v)**2 for v in rho.values()).real

    # Gravity
    field_f = [0.0] * len(positions)
    am, _ = propagate_weighted(positions, adj, field, src, k, blocked, edge_weights)
    af, _ = propagate_weighted(positions, adj, field_f, src, k, blocked, edge_weights)
    pm = sum(abs(am[d])**2 for d in det_nodes)
    pf = sum(abs(af[d])**2 for d in det_nodes)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        ym = sum(abs(am[d])**2 * positions[d][1] for d in det_nodes) / pm
        yf = sum(abs(af[d])**2 * positions[d][1] for d in det_nodes) / pf
        grav = ym - yf

    return {"dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn, "gravity": grav}


def _mean_se(vals):
    vals = [v for v in vals if not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals) / (len(vals)-1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 105)
    print("SOFT SLIT-SPECIFICITY CHANNELS")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print("=" * 105)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    alphas = [0.0, 0.5, 1.0, 2.0, 5.0]
    t_iterations = [0, 1, 3, 5, 10]

    for nl in [25, 40, 60]:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'alpha':>6s}  {'T':>3s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
              f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 62}")

        for alpha in alphas:
            for T in t_iterations:
                if alpha == 0 and T > 0:
                    continue  # alpha=0 is same regardless of T

                t0 = time.time()
                dtv_all, pur_all, sn_all, grav_all = [], [], [], []

                for seed in seeds:
                    pos, adj, bl = generate_3d_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                    n = len(pos)
                    by_layer = defaultdict(list)
                    for idx, (x, y, z) in enumerate(pos):
                        by_layer[round(x)].append(idx)
                    layers = sorted(by_layer.keys())
                    if len(layers) < 7: continue
                    src = by_layer[layers[0]]
                    det_nodes = by_layer[layers[-1]]
                    if not det_nodes: continue
                    cy = sum(pos[i][1] for i in range(n)) / n
                    bl_idx = len(layers) // 3
                    bi = by_layer[layers[bl_idx]]
                    sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                    sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                    if not sa or not sb: continue
                    blocked = set(bi) - set(sa + sb)
                    grav_layer = layers[2 * len(layers) // 3]
                    mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                    if not mass_nodes: continue
                    field = compute_field_3d(pos, mass_nodes)

                    env_depth = max(1, round(nl / 6))
                    start = bl_idx + 1
                    stop = min(len(layers) - 1, start + env_depth)
                    mid = []
                    for layer in layers[start:stop]:
                        mid.extend(by_layer[layer])

                    # Iterate soft weighting
                    edge_weights = None
                    for t in range(max(1, T)):
                        if alpha > 0:
                            spec = compute_slit_specificity(
                                pos, adj, field, src, K, blocked, sa, sb, edge_weights)
                            edge_weights = specificity_to_weights(spec, alpha)

                    r = measure_single_k(pos, adj, src, det_nodes, blocked,
                                         sa, sb, field, K, mid, edge_weights)
                    if r:
                        dtv_all.append(r["dtv"])
                        pur_all.append(r["pur_cl"])
                        sn_all.append(r["s_norm"])
                        grav_all.append(r["gravity"])

                dt = time.time() - t0
                if dtv_all:
                    mdtv, _ = _mean_se(dtv_all)
                    mpur, sepur = _mean_se(pur_all)
                    msn, _ = _mean_se(sn_all)
                    mg, seg = _mean_se(grav_all)
                    label_a = f"{alpha:.1f}" if alpha > 0 else "base"
                    label_t = f"{T}" if alpha > 0 else "-"
                    print(f"  {label_a:>6s}  {label_t:>3s}  {mdtv:8.4f}  "
                          f"{mpur:7.4f}±{sepur:.2f}  {msn:8.4f}  "
                          f"{mg:+7.4f}±{seg:.3f}  {len(dtv_all):3d}  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  alpha=0: baseline (no specificity weighting)")
    print("  Higher alpha: stronger slit-specific reinforcement")
    print("  More T: more iterations of specificity feedback")
    print("  pur_cl: CL bath purity (single-k, genuine)")
    print("  If pur_cl drops with alpha: soft channels create real decoherence")


if __name__ == "__main__":
    main()
