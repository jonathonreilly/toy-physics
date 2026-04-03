#!/usr/bin/env python3
"""Tree-lattice interpolation: find the sweet spot for decoherence.

On a tree: unique paths → no CLT, but also no interference.
On a lattice: many paths → CLT kills decoherence, but interference exists.

Parameter p controls the transition:
  p=0: spanning tree of the DAG (minimal edges for connectivity)
  p=1: full lattice (all edges within connect_radius)

At some intermediate p, there should be enough paths for interference
but few enough that the CLT doesn't dominate.

Also: does the mirror symmetry combine with tree-like sparsity?
Test mirror + tree-lattice interpolation.

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


def generate_interpolated_dag(n_layers, npl, xyz_range, connect_radius,
                               rng_seed, p_extra):
    """Generate DAG interpolating between tree and lattice.

    Step 1: Place nodes (same as standard generator).
    Step 2: Build spanning tree — each non-source node connects to
            ONE nearest parent (previous-layer node within radius).
    Step 3: Add extra edges with probability p_extra for each
            potential edge within connect_radius.

    p_extra=0: tree (each node has exactly one parent)
    p_extra=1: full lattice (all edges within radius)
    """
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

                # Find all potential parents within radius
                candidates = []
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            candidates.append((prev_idx, dist))

                if not candidates:
                    continue

                # Tree edge: connect to nearest parent (guaranteed)
                candidates.sort(key=lambda x: x[1])
                adj[candidates[0][0]].append(idx)

                # Extra edges: each additional candidate with probability p_extra
                for prev_idx, dist in candidates[1:]:
                    if rng.random() < p_extra:
                        adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), n_layers // 3


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
            amps[j] += amps[i] * ea
    return amps


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


def measure_single_k(positions, adj, n_layers, k):
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
    field = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n

    psi_a = propagate_3d(positions, adj, field, src, k, blocked | set(sb))
    psi_b = propagate_3d(positions, adj, field, src, k, blocked | set(sa))

    pa = {d: abs(psi_a[d])**2 for d in det_list}
    pb = {d: abs(psi_b[d])**2 for d in det_list}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d]/na - pb[d]/nb) for d in det_list)

    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
    NA_amp = sum(abs(a)**2 for a in ba)
    NB_amp = sum(abs(b)**2 for b in bb)
    Sn = S / (NA_amp + NB_amp) if (NA_amp + NB_amp) > 0 else 0.0
    D_cl = math.exp(-LAM**2 * Sn)

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
    pur_cl = sum(abs(v)**2 for v in rho.values()).real

    am = propagate_3d(positions, adj, field, src, k, blocked)
    af = propagate_3d(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d])**2 for d in det_list)
    pf = sum(abs(af[d])**2 for d in det_list)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
        grav = ym - yf

    # Count edges
    n_edges = sum(len(v) for v in adj.values())

    return {"dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn, "gravity": grav,
            "n_edges": n_edges}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals) / (len(vals)-1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 100)
    print("TREE-LATTICE INTERPOLATION")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print(f"  p_extra=0: tree, p_extra=1: lattice")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]
    p_values = [0.0, 0.05, 0.1, 0.2, 0.5, 1.0]

    print(f"  {'N':>4s}  {'p':>5s}  {'edges':>6s}  {'d_TV':>8s}  {'pur_cl':>8s}  "
          f"{'S_norm':>8s}  {'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    for nl in [25, 40, 60]:
        for p in p_values:
            t0 = time.time()
            dtv_all, pur_all, sn_all, grav_all, edge_all = [], [], [], [], []

            for seed in seeds:
                pos, adj, bl = generate_interpolated_dag(
                    nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, p)
                r = measure_single_k(pos, adj, nl, K)
                if r:
                    dtv_all.append(r["dtv"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
                    edge_all.append(r["n_edges"])

            dt = time.time() - t0
            if dtv_all:
                mdtv, _ = _mean_se(dtv_all)
                mpur, sepur = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                medge = sum(edge_all) / len(edge_all)
                print(f"  {nl:4d}  {p:5.2f}  {medge:6.0f}  {mdtv:8.4f}  {mpur:7.4f}±{sepur:.02f}  "
                      f"{msn:8.4f}  {mg:+7.4f}±{seg:.3f}  {len(dtv_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {p:5.2f}  FAIL  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  p=0.00: tree (1 parent per node, minimal paths)")
    print("  p=1.00: full lattice (all edges within radius)")
    print("  Sweet spot: highest d_TV with pur_cl < 0.98")
    print("  Tree should have high d_TV but low S_norm (no env info)")
    print("  Lattice should have low d_TV but high S_norm (CLT)")


if __name__ == "__main__":
    main()
