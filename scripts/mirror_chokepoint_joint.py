#!/usr/bin/env python3
"""Mirror-symmetric chokepoint DAGs: Born + gravity + decoherence.

This is the hardened mirror companion to the exploratory mirror lane.
It generates strict chokepoint graphs with optional same-side layer-2
edges for scaling tests, while keeping the Born check on the barrier.

Canonical use:
  - strict layer-1 chokepoint connectivity
  - Born, decoherence, and gravity measured on the same graphs
  - optional sparse same-side layer-2 edges only for scaling probes

The retained mirror pocket lives in docs/MIRROR_CHOKEPOINT_NOTE.md.
"""

from __future__ import annotations
import argparse
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
NPL_HALF = 25
XYZ_RANGE = 12.0
CONNECT_RADIUS = 4.0
N_YBINS = 8
LAM = 10.0


def _same_side_layer2_ok(layer: int, barrier_layer: int) -> bool:
    """Allow layer-2 edges only when they do not jump across the barrier."""
    return layer <= barrier_layer or (layer - 2) >= barrier_layer


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


def generate_mirror_chokepoint_dag(
    n_layers,
    npl_half,
    xyz_range,
    connect_radius,
    rng_seed,
    layer2_prob=0.0,
):
    """Mirror-symmetric DAG with layer-1-only connectivity (chokepoint)."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    mirror_map = {}
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
            mirror_map[idx] = idx
        else:
            upper_nodes = []
            lower_nodes = []
            for _ in range(npl_half):
                y = rng.uniform(0.5, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx_up = len(positions)
                positions.append((x, y, z))
                upper_nodes.append(idx_up)
                idx_lo = len(positions)
                positions.append((x, -y, z))
                lower_nodes.append(idx_lo)
                mirror_map[idx_up] = idx_lo
                mirror_map[idx_lo] = idx_up

            layer_nodes = upper_nodes + lower_nodes

            # CHOKEPOINT: connect to previous layer ONLY (not layer-2)
            if layer_indices:
                prev = layer_indices[-1]
                for curr_idx in upper_nodes:
                    cx, cy_val, cz = positions[curr_idx]
                    for prev_idx in prev:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((cx-px)**2 + (cy_val-py)**2 + (cz-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(curr_idx)
                            m_prev = mirror_map[prev_idx]
                            m_curr = mirror_map[curr_idx]
                            adj[m_prev].append(m_curr)

            # Optional sparse layer-2 edges, but only when they do not jump
            # across the barrier layer.
            if layer2_prob > 0 and len(layer_indices) >= 2 and _same_side_layer2_ok(layer, barrier_layer):
                prev2 = layer_indices[-2]
                for curr_idx in upper_nodes:
                    cx, cy_val, cz = positions[curr_idx]
                    for prev_idx in prev2:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((cx-px)**2 + (cy_val-py)**2 + (cz-pz)**2)
                        if dist <= connect_radius and rng.random() < layer2_prob:
                            adj[prev_idx].append(curr_idx)
                            m_prev = mirror_map[prev_idx]
                            m_curr = mirror_map[curr_idx]
                            adj[m_prev].append(m_curr)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), n_layers // 3, mirror_map


def generate_random_chokepoint_dag(
    n_layers,
    npl_total,
    xyz_range,
    connect_radius,
    rng_seed,
    layer2_prob=0.0,
):
    """Strict chokepoint random DAG for baseline comparison."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(npl_total):
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                if layer_indices:
                    prev = layer_indices[-1]
                    for prev_idx in prev:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)

                if layer2_prob > 0 and len(layer_indices) >= 2 and _same_side_layer2_ok(layer, barrier_layer):
                    prev2 = layer_indices[-2]
                    for prev_idx in prev2:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius and rng.random() < layer2_prob:
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


def sorkin_born_test(positions, adj, src, k, bi, slit_a, slit_b, slit_c, det_list, field):
    """Three-slit Sorkin test for Born rule."""
    all_slits = set(slit_a + slit_b + slit_c)
    other = set(bi) - all_slits
    combos = {
        'abc': set(slit_a + slit_b + slit_c),
        'ab': set(slit_a + slit_b), 'ac': set(slit_a + slit_c),
        'bc': set(slit_b + slit_c),
        'a': set(slit_a), 'b': set(slit_b), 'c': set(slit_c),
    }
    I3 = 0.0
    P_abc = 0.0
    for key, open_set in combos.items():
        bl = other | (all_slits - open_set)
        a = propagate_3d(positions, adj, field, src, k, bl)
        for di, d in enumerate(det_list):
            p = abs(a[d]) ** 2
            if key == 'abc':
                P_abc += p
                I3 += p
            elif key in ('ab', 'ac', 'bc'):
                I3 -= p
            else:
                I3 += p
    return abs(I3) / P_abc if P_abc > 1e-30 else math.nan


def measure_joint(positions, adj, n_layers, k):
    """Measure d_TV, CL purity, gravity, and Born."""
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

    # Three slits for Born test
    upper = sorted([i for i in bi if positions[i][1] > cy + 2], key=lambda i: positions[i][1])
    lower = sorted([i for i in bi if positions[i][1] < cy - 2], key=lambda i: -positions[i][1])
    middle = sorted([i for i in bi if abs(positions[i][1] - cy) <= 2],
                    key=lambda i: abs(positions[i][1] - cy))

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

    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n

    # Single-slit propagation
    psi_a = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
    psi_b = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))

    # d_TV
    pa = {d: abs(psi_a[d])**2 for d in det_list}
    pb = {d: abs(psi_b[d])**2 for d in det_list}
    na_amp = sum(pa.values())
    nb_amp = sum(pb.values())
    if na_amp < 1e-30 or nb_amp < 1e-30:
        return None
    dtv = 0.5 * sum(abs(pa[d]/na_amp - pb[d]/nb_amp) for d in det_list)

    # CL bath
    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
    NA = sum(abs(a)**2 for a in ba)
    NB = sum(abs(b)**2 for b in bb)
    Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
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

    # Gravity
    am = propagate_3d(positions, adj, field_m, src, k, blocked)
    af = propagate_3d(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d])**2 for d in det_list)
    pf = sum(abs(af[d])**2 for d in det_list)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
        yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
        grav = ym - yf

    # Born test
    born = math.nan
    if upper and lower and middle:
        born = sorkin_born_test(positions, adj, src, k, bi,
                                [upper[0]], [lower[0]], [middle[0]],
                                det_list, field_f)

    # k=0 gravity control
    am0 = propagate_3d(positions, adj, field_m, src, 0.0, blocked)
    af0 = propagate_3d(positions, adj, field_f, src, 0.0, blocked)
    pm0 = sum(abs(am0[d])**2 for d in det_list)
    pf0 = sum(abs(af0[d])**2 for d in det_list)
    grav_k0 = 0.0
    if pm0 > 1e-30 and pf0 > 1e-30:
        ym0 = sum(abs(am0[d])**2 * positions[d][1] for d in det_list) / pm0
        yf0 = sum(abs(af0[d])**2 * positions[d][1] for d in det_list) / pf0
        grav_k0 = ym0 - yf0

    return {
        "dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn,
        "gravity": grav, "born": born, "grav_k0": grav_k0,
    }


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals) / (len(vals)-1)
    return m, math.sqrt(var / len(vals))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-layers", nargs="+", type=int, default=[15, 25, 40, 60, 80, 100])
    parser.add_argument("--npl-half", type=int, default=NPL_HALF)
    parser.add_argument("--xyz-range", type=float, default=XYZ_RANGE)
    parser.add_argument("--connect-radius", type=float, default=CONNECT_RADIUS)
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--layer2-prob", nargs="+", type=float, default=[0.0])
    args = parser.parse_args()

    print("=" * 110)
    print("MIRROR-SYMMETRIC CHOKEPOINT: Born + Gravity + Decoherence")
    print(f"  NPL_HALF={args.npl_half} (total {2*args.npl_half}), k={K}, {args.n_seeds} seeds")
    print(f"  Chokepoint barrier (layer-1 only connectivity)")
    print("=" * 110)
    print()

    seeds = [s * 7 + 3 for s in range(args.n_seeds)]

    print(f"  {'N':>4s}  {'cfg':>10s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'Born':>10s}  {'k=0':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 96}")

    configs = [("random", None, 0.0)] + [
        (f"mirror p2={p2:g}", "mirror", p2) for p2 in args.layer2_prob
    ]

    for nl in args.n_layers:
        for label, kind, p2 in configs:
            t0 = time.time()
            dtv_all, pur_all, sn_all, grav_all, born_all, k0_all = [], [], [], [], [], []

            for seed in seeds:
                if kind == "mirror":
                    pos, adj, bl, _ = generate_mirror_chokepoint_dag(
                        nl, args.npl_half, args.xyz_range, args.connect_radius, seed, p2)
                else:
                    pos, adj, bl = generate_random_chokepoint_dag(
                        nl, 2 * args.npl_half, args.xyz_range, args.connect_radius, seed, p2)
                r = measure_joint(pos, adj, nl, K)
                if r:
                    dtv_all.append(r["dtv"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
                    if not math.isnan(r["born"]):
                        born_all.append(r["born"])
                    k0_all.append(r["grav_k0"])

            dt = time.time() - t0
            if dtv_all:
                mdtv, _ = _mean_se(dtv_all)
                mpur, sepur = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mborn, _ = _mean_se(born_all)
                mk0, _ = _mean_se(k0_all)
                born_str = f"{mborn:10.2e}" if not math.isnan(mborn) else "       nan"
                print(f"  {nl:4d}  {label:>10s}  {mdtv:8.4f}  {mpur:7.4f}±{sepur:.02f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {born_str}  {mk0:+10.2e}  "
                      f"{len(dtv_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>10s}  FAIL  {dt:4.0f}s")
        print()

    print()
    print("VALIDATION CRITERIA:")
    print("  Born: |I3|/P < 1e-10 = machine precision (PASS)")
    print("  k=0: must be 0 (phase-mediated gravity)")
    print("  pur_cl < 0.95 at N=60+: decoherence ceiling broken")
    print("  gravity > 0 with grav_t > 2: significant attraction")


if __name__ == "__main__":
    main()
