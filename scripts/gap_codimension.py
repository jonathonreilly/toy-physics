#!/usr/bin/env python3
"""Gap codimension: does extending the gap to z help?

Gap-as-physics investigation, Experiment 4.

Current gap is 1D: exclude |y| < gap/2. Z is free. In 3D, amplitude can
"leak around" the gap in z. Does closing the z direction help?

Test:
  1D gap (baseline): |y| < 2 excluded, z free
  2D cylindrical gap: sqrt(y^2 + z^2) < R excluded
  2D rectangular gap: |y| < gy/2 AND |z| < gz/2 excluded

Match conditions by excluded AREA FRACTION of the y-z plane:
  1D gap=4: excluded fraction = 4 / 24 = 0.167 (in y only)
  2D cyl R=2.85: excluded fraction = pi*2.85^2 / (24*24) ≈ 0.044
  2D rect 4x4: excluded fraction = 16 / 576 ≈ 0.028

Actually, for fair comparison match the excluded LINEAR fraction in y:
  1D: 4/24 = 16.7% of y-range excluded
  2D cyl: same y-exclusion at z=0, but narrows at |z|>0
  2D rect: same y-exclusion for all z within |z|<gz/2

So compare: 1D gap=4 vs 2D rect(4,4) vs 2D rect(4,8) vs 2D cyl(R=2)
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
N_YBINS = 8
LAM = 10.0
CONNECT_RADIUS = 4.0
XYZ_RANGE = 12.0
NPL = 30
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 16
N_LAYERS_LIST = [12, 25, 40, 60]


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


def generate_3d_dag_gap_variant(n_layers, npl, xyz_range, connect_radius, rng_seed,
                                 gap_type="1d", gap_y=4.0, gap_z=0.0, gap_r=0.0):
    """Generate 3D DAG with various gap geometries.

    gap_type:
      "none"  - uniform (no gap)
      "1d"    - standard y-gap: exclude |y| < gap_y/2
      "rect"  - rectangular tube: exclude |y| < gap_y/2 AND |z| < gap_z/2
      "cyl"   - cylindrical tube: exclude sqrt(y^2 + z^2) < gap_r
    """
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
            placed = 0
            attempts = 0
            while placed < npl and attempts < npl * 10:
                attempts += 1
                y = rng.uniform(-xyz_range, xyz_range)
                z = rng.uniform(-xyz_range, xyz_range)

                # Apply gap exclusion post-barrier
                if layer > barrier_layer and gap_type != "none":
                    if gap_type == "1d":
                        if abs(y) < gap_y / 2:
                            continue
                    elif gap_type == "rect":
                        if abs(y) < gap_y / 2 and abs(z) < gap_z / 2:
                            continue
                    elif gap_type == "cyl":
                        if math.sqrt(y**2 + z**2) < gap_r:
                            continue

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                placed += 1

                # Connectivity
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
                            # Channel logic based on y-sign
                            same_ch = (y * py > 0)
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < 0.02:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)
    return positions, dict(adj)


def propagate_3d(positions, adj, field, src, k, blocked=None):
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


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (
                amps_a[d1].conjugate() * amps_a[d2]
                + amps_b[d1].conjugate() * amps_b[d2]
                + D * amps_a[d1].conjugate() * amps_b[d2]
                + D * amps_b[d1].conjugate() * amps_a[d2]
            )
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v) ** 2 for v in rho.values()).real


def measure(positions, adj, n_layers, k_band):
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
    cy = sum(positions[i][1] for i in range(len(positions))) / len(positions)
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
    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * len(positions)
    grav_vals, pur_vals, sn_vals = [], [], []
    for k in k_band:
        am = propagate_3d(positions, adj, field_m, src, k, blocked)
        af = propagate_3d(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)
        aa = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes_3d(aa, positions, mid)
        bb = bin_amplitudes_3d(ab, positions, mid)
        S = sum(abs(a - b)**2 for a, b in zip(ba, bb))
        NA = sum(abs(a)**2 for a in ba)
        NB = sum(abs(b)**2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM**2 * Sn)
        pc = cl_purity(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)
            sn_vals.append(Sn)
    if not grav_vals or not pur_vals:
        return None
    return {
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "gravity": sum(grav_vals) / len(grav_vals),
    }


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m)**2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 95)
    print("GAP CODIMENSION: 1D vs 2D GAP IN 3D SPACE")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    variants = [
        ("no-gap", "none", 0, 0, 0),
        ("1d-y4", "1d", 4.0, 0, 0),
        ("rect-4x4", "rect", 4.0, 4.0, 0),
        ("rect-4x8", "rect", 4.0, 8.0, 0),
        ("rect-4x16", "rect", 4.0, 16.0, 0),
        ("cyl-r2", "cyl", 0, 0, 2.0),
        ("cyl-r4", "cyl", 0, 0, 4.0),
        ("cyl-r6", "cyl", 0, 0, 6.0),
    ]

    print(f"  {'N':>4s}  {'variant':>12s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 65}")

    for nl in N_LAYERS_LIST:
        for label, gtype, gy, gz, gr in variants:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []
            for seed in seeds:
                positions, adj = generate_3d_dag_gap_variant(
                    nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed,
                    gap_type=gtype, gap_y=gy, gap_z=gz, gap_r=gr)
                r = measure(positions, adj, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                print(f"  {nl:4d}  {label:>12s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>12s}  FAIL  {dt:4.0f}s")
        print()

    print("KEY:")
    print("  1d-y4: standard gap (|y|<2 excluded)")
    print("  rect-4xZ: rectangular tube (|y|<2 AND |z|<Z/2 excluded)")
    print("  cyl-rR: cylindrical tube (sqrt(y²+z²)<R excluded)")
    print()
    print("  If rect/cyl beat 1d: z-leakage is real, blocking it helps")
    print("  If rect/cyl ≈ 1d: z dimension doesn't matter for decoherence")
    print("  If rect/cyl worse: excluding more volume hurts connectivity")


if __name__ == "__main__":
    main()
