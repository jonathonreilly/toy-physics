#!/usr/bin/env python3
"""Gap + intermittent normalization: combine the two best mechanisms.

The gap creates which-path information (node absence → channel separation).
Intermittent normalization prevents CLT concentration from building up
(periodic amplitude reset → Born-preserving decoherence boost).

Question: do they stack? Does gap + K=10 intermittent norm beat either alone?

If the gap's decoherence and the intermittent norm's decoherence are
independent mechanisms, their effects should combine. If they're both
fighting the same CLT, the improvement may be subadditive.

Also test: does intermittent norm on UNIFORM DAGs approach gap-level
decoherence? (If yes, intermittent norm may be a substitute for the gap.)

Head-to-head at N=12,25,40,60:
  1. uniform + linear (baseline)
  2. uniform + K=10 norm
  3. gap + linear
  4. gap + K=10 norm (combined)
  5. gap + K=5 norm
  6. gap + K=20 norm
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
GAP = 4.0


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


def generate_3d_dag(n_layers, npl, xyz_range, connect_radius, rng_seed, gap=0.0):
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
            for node_i in range(npl):
                z = rng.uniform(-xyz_range, xyz_range)
                if gap > 0 and layer > barrier_layer:
                    if node_i < npl // 2:
                        y = rng.uniform(gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, -gap / 2)
                else:
                    y = rng.uniform(-xyz_range, xyz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if gap > 0 and layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
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


def propagate_3d_intermittent(positions, adj, field, src, k, blocked=None,
                               norm_interval=0):
    """Propagate with optional intermittent normalization.

    norm_interval=0: standard linear propagation
    norm_interval=K: normalize amplitudes BETWEEN layers every K layers.
    After processing all nodes in layer L, if L is a multiple of K,
    renormalize the full amplitude vector to unit norm.
    """
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    # Group by layer for batch normalization
    by_layer = defaultdict(list)
    for i, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(i)
    layer_keys = sorted(by_layer.keys())

    # Process layer by layer
    processed = set()
    for li, lk in enumerate(layer_keys):
        # Process all nodes in this layer (in topo order)
        layer_nodes = set(by_layer[lk])
        for i in order:
            if i not in layer_nodes or i in processed:
                continue
            processed.add(i)
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

        # Intermittent normalization after this layer
        if norm_interval > 0 and (li + 1) % norm_interval == 0:
            total = sum(abs(amps[j])**2 for j in range(n))
            if total > 1e-30:
                scale = 1.0 / math.sqrt(total)
                for j in range(n):
                    amps[j] *= scale

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


def sorkin_test(positions, adj, field, src, k, blocked, sa, sb, det_list, norm_k):
    """Three-slit Sorkin test for Born rule. Returns |I3|/P."""
    # Need three slits — use sa[0], sb[0], and try to find a third
    if len(sa) < 2 or len(sb) < 1:
        return math.nan

    s1, s2, s3 = sa[0], sa[1] if len(sa) > 1 else sa[0], sb[0]
    all_slits = {s1, s2, s3}
    other_barrier = blocked - all_slits

    def prop(open_set):
        bl = other_barrier | (all_slits - open_set)
        return propagate_3d_intermittent(positions, adj, field, src, k, bl, norm_k)

    a_abc = prop({s1, s2, s3})
    a_ab = prop({s1, s2})
    a_ac = prop({s1, s3})
    a_bc = prop({s2, s3})
    a_a = prop({s1})
    a_b = prop({s2})
    a_c = prop({s3})

    I3 = 0.0
    P_abc = 0.0
    for d in det_list:
        p_abc = abs(a_abc[d])**2
        p_ab = abs(a_ab[d])**2
        p_ac = abs(a_ac[d])**2
        p_bc = abs(a_bc[d])**2
        p_a = abs(a_a[d])**2
        p_b = abs(a_b[d])**2
        p_c = abs(a_c[d])**2
        I3 += abs(p_abc - p_ab - p_ac - p_bc + p_a + p_b + p_c)
        P_abc += p_abc

    return I3 / P_abc if P_abc > 1e-30 else math.nan


def measure(positions, adj, n_layers, k_band, norm_k=0):
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

    grav_vals, pur_vals, sn_vals, born_vals = [], [], [], []
    for k in k_band:
        am = propagate_3d_intermittent(positions, adj, field_m, src, k, blocked, norm_k)
        af = propagate_3d_intermittent(positions, adj, field_f, src, k, blocked, norm_k)
        pm = sum(abs(am[d])**2 for d in det_list)
        pf = sum(abs(af[d])**2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d])**2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d])**2 * positions[d][1] for d in det_list) / pf
            grav_vals.append(ym - yf)

        aa = propagate_3d_intermittent(positions, adj, field_m, src, k, blocked | set(sb), norm_k)
        ab = propagate_3d_intermittent(positions, adj, field_m, src, k, blocked | set(sa), norm_k)
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

        # Born test (only on first k to save time)
        if k == k_band[0]:
            i3p = sorkin_test(positions, adj, field_m, src, k, blocked, sa, sb, det_list, norm_k)
            if not math.isnan(i3p):
                born_vals.append(i3p)

    if not grav_vals or not pur_vals:
        return None
    return {
        "pur_cl": sum(pur_vals) / len(pur_vals),
        "s_norm": sum(sn_vals) / len(sn_vals),
        "gravity": sum(grav_vals) / len(grav_vals),
        "born": sum(born_vals) / len(born_vals) if born_vals else math.nan,
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
    print("=" * 100)
    print("GAP + INTERMITTENT NORMALIZATION")
    print(f"  Gap={GAP}, CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("uniform+linear", 0.0, 0),
        ("uniform+K=5", 0.0, 5),
        ("uniform+K=10", 0.0, 10),
        ("uniform+K=20", 0.0, 20),
        ("gap+linear", GAP, 0),
        ("gap+K=5", GAP, 5),
        ("gap+K=10", GAP, 10),
        ("gap+K=20", GAP, 20),
    ]

    print(f"  {'N':>4s}  {'config':>16s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'|I3|/P':>8s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 80}")

    for nl in N_LAYERS_LIST:
        for label, gap, norm_k in configs:
            t0 = time.time()
            pc_all, sn_all, grav_all, born_all = [], [], [], []
            for seed in seeds:
                positions, adj = generate_3d_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed, gap)
                r = measure(positions, adj, nl, K_BAND, norm_k)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
                    if not math.isnan(r["born"]):
                        born_all.append(r["born"])
            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mborn = sum(born_all) / len(born_all) if born_all else math.nan
                born_str = f"{mborn:8.3f}" if not math.isnan(mborn) else "     nan"
                print(f"  {nl:4d}  {label:>16s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {born_str}  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  {label:>16s}  FAIL  {dt:4.0f}s")
        print()

    print("ANALYSIS:")
    print("  If gap+K=10 < gap+linear AND gap+K=10 < uniform+K=10:")
    print("    → effects stack (independent mechanisms)")
    print("  If gap+K=10 ≈ min(gap+linear, uniform+K=10):")
    print("    → subadditive (both fight same CLT)")
    print("  Born: |I3|/P < 0.01 is Born-compliant")


if __name__ == "__main__":
    main()
