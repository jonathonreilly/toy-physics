#!/usr/bin/env python3
"""Layer normalization + |y|-removal: combined scaling test.

The other thread found LN+gap gives (1-pur_min) ~ N^(-0.88), R²=0.946,
with ceiling at N≈1375. Our investigation found |y|<2 removal gives the
best joint coexistence (gravity+decoherence) at N=80.

Test: does LN + |y|-removal give a cleaner scaling law than either alone?

Layer norm: after propagating through layer L, normalize the amplitudes
of all nodes in layer L+1 to unit norm. This prevents CLT concentration
from building up. It's Born-preserving because it's a linear rescaling.

The CL bath purity WILL respond to LN (unlike our Exp 7 which used
global normalization). LN changes the per-layer amplitude distribution,
which changes how single-slit amplitudes populate the y-bins.
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
NPL = 50
K_BAND = [3.0, 5.0, 7.0]
N_SEEDS = 24
N_LAYERS_LIST = [25, 40, 60, 80, 100]
Y_THRESH = 2.0


def generate_3d_dag_uniform(n_layers, npl, xyz_range, connect_radius, rng_seed):
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


def apply_y_removal(positions, adj, barrier_layer, y_thresh, protected):
    removed = set()
    for idx, (x, y, z) in enumerate(positions):
        if x <= barrier_layer or idx in protected:
            continue
        if abs(y) < y_thresh:
            removed.add(idx)
    new_adj = {}
    for i, nbs in adj.items():
        if i in removed:
            continue
        new_nbs = [j for j in nbs if j not in removed]
        if new_nbs:
            new_adj[i] = new_nbs
    return new_adj, removed


def propagate_3d_ln(positions, adj, field, src, k, blocked=None):
    """3D propagator with per-layer normalization of receiving layer."""
    n = len(positions)
    blocked = blocked or set()
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
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

        # Layer normalization: normalize next layer's amplitudes
        if li + 1 < len(layers):
            nxt = by_layer[layers[li + 1]]
            tsq = sum(abs(amps[i]) ** 2 for i in nxt)
            if tsq > 1e-30:
                norm = math.sqrt(tsq)
                for i in nxt:
                    amps[i] /= norm

    return amps


def propagate_3d(positions, adj, field, src, k, blocked=None):
    """Standard linear 3D propagator."""
    n = len(positions)
    blocked = blocked or set()
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())

    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for li, lk in enumerate(layers):
        for i in by_layer[lk]:
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


def full_measure(positions, adj, n_layers, k_list, prop_fn):
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
    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n
    grav_vals, pur_vals, sn_vals = [], [], []
    for k in k_list:
        am = prop_fn(positions, adj, field_m, src, k, blocked)
        af = prop_fn(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)
        aa = prop_fn(positions, adj, field_m, src, k, blocked | set(sb))
        ab = prop_fn(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes_3d(aa, positions, mid)
        bb = bin_amplitudes_3d(ab, positions, mid)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM ** 2 * Sn)
        pc = cl_purity(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pur_vals.append(pc)
            sn_vals.append(Sn)
    if not grav_vals or not pur_vals:
        return None
    return {
        "gravity": sum(grav_vals) / len(grav_vals),
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "_sa": sa, "_sb": sb, "_blocked": blocked,
    }


def _mean_se(vals):
    if not vals:
        return 0.0, 0.0
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, 0.0
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return m, math.sqrt(var / len(vals))


def fit_power_law(ns, ys):
    if len(ns) < 3:
        return 0, 0, 0
    lx = [math.log(n) for n in ns]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    sxx = sum((x - mx) ** 2 for x in lx)
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    if sxx < 1e-10:
        return 0, 0, 0
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(lx, ly))
    ss_tot = sum((y - my) ** 2 for y in ly)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return math.exp(a), b, r2


def main():
    print("=" * 110)
    print("LAYER NORMALIZATION + |y|-REMOVAL: COMBINED SCALING")
    print(f"  NPL={NPL}, |y|<{Y_THRESH}, CL bath lambda={LAM}, {N_SEEDS} seeds")
    print("=" * 110)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("linear", False, False, propagate_3d),
        ("linear+|y|", False, True, propagate_3d),
        ("LN", True, False, propagate_3d_ln),
        ("LN+|y|", True, True, propagate_3d_ln),
    ]

    print(f"  {'N':>4s}  {'mode':>12s}  {'gravity':>12s}  {'grav_t':>7s}  {'pur_cl':>10s}  "
          f"{'1-pur':>8s}  {'S_norm':>8s}  {'joint':>5s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 92}")

    # Collect for power law fits
    fit_data = {label: ([], []) for label, _, _, _ in configs}

    for nl in N_LAYERS_LIST:
        for label, use_ln, use_yrem, prop_fn in configs:
            t0 = time.time()
            grav_all, pur_all, sn_all = [], [], []
            n_joint = 0

            for seed in seeds:
                pos, adj, bl = generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)

                if use_yrem:
                    by_layer = defaultdict(list)
                    for idx, (x, y, z) in enumerate(pos):
                        by_layer[round(x)].append(idx)
                    layers = sorted(by_layer.keys())
                    protected = set(by_layer[layers[0]]) | set(by_layer[layers[-1]])
                    cy = sum(pos[i][1] for i in range(n)) / n
                    bl_idx = len(layers) // 3
                    bi = by_layer[layers[bl_idx]]
                    sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                    sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                    protected = protected | set(sa + sb)
                    adj, _ = apply_y_removal(pos, adj, bl, Y_THRESH, protected)

                r = full_measure(pos, adj, nl, K_BAND, prop_fn)
                if r:
                    grav_all.append(r["gravity"])
                    pur_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    if r["gravity"] > 0 and r["pur_cl"] < 0.98:
                        n_joint += 1

            dt = time.time() - t0
            if grav_all:
                mg, seg = _mean_se(grav_all)
                mpc, sepc = _mean_se(pur_all)
                msn, _ = _mean_se(sn_all)
                gt = mg / seg if seg > 0 else 0
                one_minus = 1 - mpc
                n_ok = len(grav_all)
                print(f"  {nl:4d}  {label:>12s}  {mg:+8.4f}±{seg:.3f}  {gt:+6.2f}  "
                      f"{mpc:7.4f}±{sepc:.3f}  {one_minus:8.4f}  {msn:8.4f}  "
                      f"{n_joint:3d}/{n_ok:<2d}  {n_ok:3d}  {dt:4.0f}s")
                if one_minus > 0.001:
                    fit_data[label][0].append(nl)
                    fit_data[label][1].append(one_minus)
            else:
                print(f"  {nl:4d}  {label:>12s}  FAIL  {dt:4.0f}s")

        print()

    # Power law fits
    print("POWER LAW FITS: (1-pur_cl) = A × N^alpha")
    print(f"  {'mode':>12s}  {'A':>8s}  {'alpha':>8s}  {'R²':>6s}  {'N_half':>8s}")
    print(f"  {'-' * 46}")
    for label, _, _, _ in configs:
        ns, ys = fit_data[label]
        if len(ns) >= 3:
            A, alpha, r2 = fit_power_law(ns, ys)
            n_half = (0.01 / A) ** (1 / alpha) if A > 0 and alpha < 0 else float('inf')
            print(f"  {label:>12s}  {A:8.3f}  {alpha:8.2f}  {r2:6.3f}  {n_half:8.0f}")
        else:
            print(f"  {label:>12s}  insufficient data")

    print()
    print("KEY:")
    print("  N_half = N at which (1-pur_cl) = 0.01 (pur_cl=0.99)")
    print("  Best combined: largest N_half with grav_t > 2.0")


if __name__ == "__main__":
    main()
