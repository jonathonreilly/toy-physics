#!/usr/bin/env python3
"""Mirror-symmetric DAGs: Z₂ symmetry prevents rank-1 convergence.

THEORETICAL PREDICTION: If the graph has exact y → -y symmetry, the
transfer matrices T_l commute with the reflection operator R. The
product T_N...T_1 also commutes with R, so it decomposes into even/odd
sectors. Each sector has its own rank-1 limit, but the FULL matrix
maintains rank-2 (one SV per sector).

Slit A (y>0) maps to the odd sector under R. Slit B (y<0) maps to
the even sector. In the Z₂ basis, the two slits are ORTHOGONAL BY
SYMMETRY — they can never converge. This gives d_TV > 0 at all N.

If this works, the decoherence ceiling is broken by SYMMETRY rather
than by modifying the propagator or bath. The linear propagator and
Born rule are untouched.

Implementation:
  1. Place nodes at random (x, y, z) with y > 0
  2. Mirror each node to (x, -y, z)
  3. Connect: if edge (i, j) exists, also add edge (mirror(i), mirror(j))
  4. Cross-mirror edges with controlled probability p_cross
  5. Barrier has symmetric slits at y > +3 and y < -3

Single-k CL bath purity + d_TV + spectral analysis of T product.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import random
import time
from collections import defaultdict, deque

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BETA = 0.8
K = 5.0
N_SEEDS = 16
NPL_HALF = 15  # Nodes per layer per half (total = 2*NPL_HALF)
XYZ_RANGE = 12.0
CONNECT_RADIUS = 4.0
N_YBINS = 8
LAM = 10.0
N_LAYERS_LIST = [15, 25, 40, 60, 80]


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


def generate_mirror_dag(n_layers, npl_half, xyz_range, connect_radius,
                         rng_seed, p_cross=0.0):
    """Generate Z₂-symmetric 3D DAG.

    Each node at (x, y, z) has a mirror at (x, -y, z).
    Edges are mirrored: (i,j) exists iff (mirror(i), mirror(j)) exists.
    Cross-mirror edges added with probability p_cross.
    """
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}  # node_idx -> mirror_node_idx

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            # Source at origin (self-mirror)
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
            mirror_map[idx] = idx
        else:
            # Place upper-half nodes and their mirrors
            upper_nodes = []
            lower_nodes = []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)  # y > 0 (avoid y=0)
                z = rng.uniform(-xyz_range, xyz_range)

                # Upper node
                idx_up = len(positions)
                positions.append((x, y, z))
                upper_nodes.append(idx_up)

                # Mirror node
                idx_lo = len(positions)
                positions.append((x, -y, z))
                lower_nodes.append(idx_lo)

                mirror_map[idx_up] = idx_lo
                mirror_map[idx_lo] = idx_up

            layer_nodes = upper_nodes + lower_nodes

            # Connect to previous layers (mirrored connections)
            for prev_layer in layer_indices[max(0, layer - 2):]:
                for prev_idx in prev_layer:
                    px, py, pz = positions[prev_idx]
                    for curr_idx in upper_nodes:
                        cx, cy_val, cz = positions[curr_idx]
                        dist = math.sqrt((cx-px)**2 + (cy_val-py)**2 + (cz-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(curr_idx)
                            # Mirror connection
                            m_prev = mirror_map[prev_idx]
                            m_curr = mirror_map[curr_idx]
                            adj[m_prev].append(m_curr)

                    # Cross-mirror edges (break exact Z₂ weakly)
                    if p_cross > 0:
                        for curr_idx in upper_nodes:
                            m_curr = mirror_map[curr_idx]
                            cx, cy_val, cz = positions[m_curr]
                            dist = math.sqrt((cx-px)**2 + (cy_val-py)**2 + (cz-pz)**2)
                            if dist <= connect_radius and rng.random() < p_cross:
                                adj[prev_idx].append(m_curr)
                                m_prev = mirror_map[prev_idx]
                                adj[m_prev].append(curr_idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), n_layers // 3, mirror_map


def generate_random_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    """Standard random DAG (no symmetry) for comparison."""
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
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
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

    # Single slit propagations
    psi_a = propagate_3d(positions, adj, field, src, k, blocked | set(sb))
    psi_b = propagate_3d(positions, adj, field, src, k, blocked | set(sa))

    # d_TV
    pa = {d: abs(psi_a[d])**2 for d in det_list}
    pb = {d: abs(psi_b[d])**2 for d in det_list}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d]/na - pb[d]/nb) for d in det_list)

    # CL bath
    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
    NA_amp = sum(abs(a)**2 for a in ba)
    NB_amp = sum(abs(b)**2 for b in bb)
    Sn = S / (NA_amp + NB_amp) if (NA_amp + NB_amp) > 0 else 0.0
    D_cl = math.exp(-LAM**2 * Sn)

    # Purity
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

    # Gravity
    am = propagate_3d(positions, adj, field, src, k, blocked)
    af = propagate_3d(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d])**2 for d in det_list)
    pf = sum(abs(af[d])**2 for d in det_list)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
        grav = ym - yf

    return {"dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn, "gravity": grav}


def compute_spectral_gap(positions, adj, k, by_layer, layers, blocked):
    """Compute top-2 singular values of the transfer matrix product."""
    # Extract transfer matrices
    matrices = []
    field = [0.0] * len(positions)

    for li in range(len(layers) - 1):
        from_nodes = by_layer[layers[li]]
        to_nodes = by_layer[layers[li + 1]]
        n_from = len(from_nodes)
        n_to = len(to_nodes)
        if n_from == 0 or n_to == 0:
            continue
        from_map = {node: i for i, node in enumerate(from_nodes)}
        to_map = {node: j for j, node in enumerate(to_nodes)}
        T = np.zeros((n_to, n_from), dtype=complex)
        for i_global in from_nodes:
            if i_global in blocked:
                continue
            i_local = from_map[i_global]
            for j_global in adj.get(i_global, []):
                if j_global in to_map and j_global not in blocked:
                    j_local = to_map[j_global]
                    x1, y1, z1 = positions[i_global]
                    x2, y2, z2 = positions[j_global]
                    dx, dy, dz = x2-x1, y2-y1, z2-z1
                    L = math.sqrt(dx*dx + dy*dy + dz*dz)
                    if L < 1e-10:
                        continue
                    theta = math.atan2(math.sqrt(dy*dy + dz*dz), max(dx, 1e-10))
                    w = math.exp(-BETA * theta * theta)
                    ea = cmath.exp(1j * k * (L - math.sqrt(max(L*L - L*L, 0)))) * w / L
                    T[j_local, i_local] += ea
        matrices.append(T)

    if not matrices:
        return float('nan'), float('nan')

    # Product via SVD stabilization
    common_size = max(T.shape[1] for T in matrices)
    product = np.eye(common_size, dtype=complex)
    log_sum = 0.0
    for T in matrices:
        T_sq = np.zeros((common_size, common_size), dtype=complex)
        r = min(T.shape[0], common_size)
        c = min(T.shape[1], common_size)
        T_sq[:r, :c] = T[:r, :c]
        product = T_sq @ product
        norm = np.linalg.norm(product)
        if norm > 1e-30:
            log_sum += math.log(norm)
            product /= norm

    try:
        s = np.linalg.svd(product, compute_uv=False)
        if len(s) >= 2 and s[0] > 1e-30:
            s1 = math.log(s[0]) + log_sum
            s2 = math.log(s[1]) + log_sum if s[1] > 1e-30 else -float('inf')
            return s1, s1 - s2
        return float('nan'), float('nan')
    except Exception:
        return float('nan'), float('nan')


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v) and not math.isinf(v)]
    if not vals:
        return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 105)
    print("MIRROR-SYMMETRIC DAGs: Z₂ SYMMETRY vs RANK-1 CONVERGENCE")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print(f"  NPL_HALF={NPL_HALF} (total {2*NPL_HALF} per layer)")
    print("=" * 105)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("random", None),
        ("mirror p=0", 0.0),
        ("mirror p=0.02", 0.02),
        ("mirror p=0.1", 0.1),
    ]

    print(f"  {'N':>4s}  {'config':>14s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'gap':>8s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 82}")

    for nl in N_LAYERS_LIST:
        for label, p_cross in configs:
            t0 = time.time()
            dtv_all, pur_all, sn_all, grav_all, gap_all = [], [], [], [], []

            for seed in seeds:
                if p_cross is None:
                    # Random baseline
                    pos, adj, bl = generate_random_dag(nl, 2*NPL_HALF, XYZ_RANGE, CONNECT_RADIUS, seed)
                else:
                    pos, adj, bl, _ = generate_mirror_dag(nl, NPL_HALF, XYZ_RANGE, CONNECT_RADIUS, seed, p_cross)

                r = measure_single_k(pos, adj, nl, K)
                if r:
                    dtv_all.append(r["dtv"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])

                    # Spectral gap (first 4 seeds only — expensive)
                    if seed in seeds[:4]:
                        n = len(pos)
                        by_layer = defaultdict(list)
                        for idx, (x, y, z) in enumerate(pos):
                            by_layer[round(x)].append(idx)
                        layers = sorted(by_layer.keys())
                        cy = sum(pos[i][1] for i in range(n)) / n
                        bl_idx = len(layers) // 3
                        bi = by_layer[layers[bl_idx]]
                        blocked = set(bi) - set([i for i in bi if abs(pos[i][1] - cy) > 3][:6])
                        _, gap = compute_spectral_gap(pos, adj, K, by_layer, layers, blocked)
                        if not math.isnan(gap) and not math.isinf(gap):
                            gap_all.append(gap)

            dt = time.time() - t0
            if dtv_all:
                mdtv, _ = _mean_se(dtv_all)
                mpur, sepur = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mgap, _ = _mean_se(gap_all)
                gap_str = f"{mgap:8.2f}" if not math.isnan(mgap) else "     nan"
                print(f"  {nl:4d}  {label:>14s}  {mdtv:8.4f}  {mpur:7.4f}±{sepur:.02f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {gap_str}  {len(dtv_all):3d}  {dt:4.0f}s")

        print()

    print("PREDICTIONS:")
    print("  Mirror p=0: d_TV should NOT decay with N (Z₂ symmetry prevents convergence)")
    print("  Mirror p>0: cross-mirror edges break symmetry, d_TV decays (slower than random)")
    print("  Random: d_TV decays as N^(-0.5) (CLT baseline)")
    print("  Spectral gap: mirror should be SMALLER (near-degenerate SVs)")


if __name__ == "__main__":
    main()
