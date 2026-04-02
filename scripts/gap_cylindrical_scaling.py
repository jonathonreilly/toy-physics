#!/usr/bin/env python3
"""Cylindrical gap scaling: does blocking z-leakage change the CLT exponent?

From Exp 4: cyl-r6 gave pur_cl=0.928 at N=40 (best decoherence observed).
If z-leakage contributes to CLT convergence, blocking it should change
the 1/N scaling exponent, not just the prefactor.

Test: cylindrical gap at R=2,4,6 from N=12 to N=80.
Fit (1-pur_cl) vs N to power law.
Compare exponent to the 1/N from the uniform baseline.
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
N_LAYERS_LIST = [12, 18, 25, 30, 40, 50, 60]


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


def generate_3d_dag_gap(n_layers, npl, xyz_range, connect_radius, rng_seed,
                         gap_type="none", gap_y=0.0, gap_r=0.0):
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
                if layer > barrier_layer and gap_type != "none":
                    if gap_type == "1d" and abs(y) < gap_y / 2:
                        continue
                    if gap_type == "cyl" and math.sqrt(y**2 + z**2) < gap_r:
                        continue
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                placed += 1
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
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
    grav_vals, pur_vals, sn_vals = [], [], []
    field_f = [0.0] * len(positions)
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


def fit_power_law(xs, ys):
    """Fit log(y) = a + b*log(x). Returns (a, b, R²)."""
    if len(xs) < 3:
        return 0, 0, 0
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys if y > 0]
    if len(ly) < 3:
        return 0, 0, 0
    lx = lx[:len(ly)]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx)**2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx < 1e-10:
        return 0, 0, 0
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x))**2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my)**2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return a, b, r2


def main():
    print("=" * 95)
    print("CYLINDRICAL GAP SCALING: DOES BLOCKING Z-LEAKAGE CHANGE THE CLT EXPONENT?")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("no-gap", "none", 0, 0),
        ("1d-y4", "1d", 4.0, 0),
        ("cyl-r2", "cyl", 0, 2.0),
        ("cyl-r4", "cyl", 0, 4.0),
        ("cyl-r6", "cyl", 0, 6.0),
    ]

    print(f"  {'N':>4s}  {'config':>8s}  {'pur_cl':>10s}  {'1-pur':>8s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    # Collect data for power law fits
    fit_data = {label: ([], []) for label, _, _, _ in configs}

    for nl in N_LAYERS_LIST:
        for label, gtype, gy, gr in configs:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []
            for seed in seeds:
                positions, adj = generate_3d_dag_gap(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed,
                                                      gap_type=gtype, gap_y=gy, gap_r=gr)
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
                one_minus = 1 - mpc
                print(f"  {nl:4d}  {label:>8s}  {mpc:7.4f}±{sepc:.3f}  {one_minus:8.4f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
                if one_minus > 0.001:
                    fit_data[label][0].append(nl)
                    fit_data[label][1].append(one_minus)
            else:
                print(f"  {nl:4d}  {label:>8s}  FAIL  {dt:4.0f}s")
        print()

    # Power law fits
    print("POWER LAW FITS: (1 - pur_cl) = A * N^alpha")
    print(f"  {'config':>8s}  {'alpha':>8s}  {'A':>8s}  {'R²':>6s}  {'N_half':>8s}")
    print(f"  {'-' * 44}")
    for label, _, _, _ in configs:
        xs, ys = fit_data[label]
        if len(xs) >= 3:
            a, b, r2 = fit_power_law(xs, ys)
            A = math.exp(a)
            # N at which (1-pur) = 0.01
            n_half = (0.01 / A) ** (1 / b) if A > 0 and b < 0 else float('inf')
            print(f"  {label:>8s}  {b:8.2f}  {A:8.3f}  {r2:6.2f}  {n_half:8.0f}")
        else:
            print(f"  {label:>8s}  insufficient data")

    print()
    print("KEY: alpha ≈ -1 is the CLT 1/N exponent")
    print("  If cyl-r6 has steeper alpha: z-blocking changes the exponent")
    print("  If cyl-r6 has same alpha but larger A: just shifts the ceiling")
    print("  N_half: layers at which decoherence drops to 1% (pur_cl=0.99)")


if __name__ == "__main__":
    main()
