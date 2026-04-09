#!/usr/bin/env python3
"""Scaled mirror-symmetric DAGs: reach N=40-100.

The chokepoint mirror DAG (layer-1 only) fails at N>=40 due to
sparse connectivity. This script tests two scaling strategies:

Strategy 1: Higher NPL (75 per half = 150 total)
  Pro: maintains strict chokepoint
  Con: expensive (O(NPL^2) edge computation)

Strategy 2: Chokepoint-at-barrier-only
  Layer-1 connectivity ONLY at the barrier layer
  Layer-1+2 connectivity everywhere else
  Pro: maintains Born (bypass paths blocked at barrier)
  Con: slightly weaker chokepoint property

Strategy 3: Larger connect_radius (5.0 or 6.0)
  Pro: simple
  Con: may create too many cross-mirror edges

For each: Born check + gravity + decoherence at single-k.
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
XYZ_RANGE = 12.0
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


def generate_mirror_hybrid(n_layers, npl_half, xyz_range, connect_radius,
                            rng_seed, barrier_chokepoint=True):
    """Mirror DAG with chokepoint only at barrier layer.

    Non-barrier layers: layer-1 + layer-2 connectivity (standard)
    Barrier layer: layer-1 only (chokepoint, no bypass)
    All edges mirrored under y → -y.
    """
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

            # Determine lookback: chokepoint at barrier, normal elsewhere
            if barrier_chokepoint and layer == barrier_layer + 1:
                # This layer connects ONLY to barrier layer (chokepoint)
                lookback_start = max(0, len(layer_indices) - 1)
            else:
                # Normal: look back 2 layers
                lookback_start = max(0, len(layer_indices) - 2)

            for curr_idx in upper_nodes:
                cx, cy_val, cz = positions[curr_idx]
                for prev_layer in layer_indices[lookback_start:]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((cx-px)**2 + (cy_val-py)**2 + (cz-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(curr_idx)
                            adj[mirror_map[prev_idx]].append(mirror_map[curr_idx])

        layer_indices.append(layer_nodes)

    return positions, dict(adj), barrier_layer, mirror_map


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


def sorkin_born(positions, adj, src, k, bi, s_a, s_b, s_c, det_list, field):
    all_slits = set(s_a + s_b + s_c)
    other = set(bi) - all_slits
    probs = {}
    for key, open_set in [('abc', all_slits), ('ab', set(s_a+s_b)),
                           ('ac', set(s_a+s_c)), ('bc', set(s_b+s_c)),
                           ('a', set(s_a)), ('b', set(s_b)), ('c', set(s_c))]:
        bl = other | (all_slits - open_set)
        a = propagate_3d(positions, adj, field, src, k, bl)
        probs[key] = [abs(a[d])**2 for d in det_list]
    I3 = 0.0; P = 0.0
    for di in range(len(det_list)):
        i3 = (probs['abc'][di] - probs['ab'][di] - probs['ac'][di] - probs['bc'][di]
              + probs['a'][di] + probs['b'][di] + probs['c'][di])
        I3 += abs(i3); P += probs['abc'][di]
    return I3 / P if P > 1e-30 else math.nan


def measure_joint(positions, adj, n_layers, k):
    n = len(positions)
    by_layer = defaultdict(list)
    for idx, (x, y, z) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7: return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list: return None
    cy = sum(positions[i][1] for i in range(n)) / n
    bl_idx = len(layers) // 3
    bi = by_layer[layers[bl_idx]]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb: return None
    blocked = set(bi) - set(sa + sb)
    upper = sorted([i for i in bi if positions[i][1] > cy + 2], key=lambda i: positions[i][1])
    lower = sorted([i for i in bi if positions[i][1] < cy - 2], key=lambda i: -positions[i][1])
    middle = sorted([i for i in bi if abs(positions[i][1]-cy) <= 2], key=lambda i: abs(positions[i][1]-cy))
    grav_layer = layers[2 * len(layers) // 3]
    mass_nodes = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    if not mass_nodes: return None
    env_depth = max(1, round(n_layers / 6))
    start = bl_idx + 1
    stop = min(len(layers) - 1, start + env_depth)
    mid = []
    for layer in layers[start:stop]: mid.extend(by_layer[layer])
    field_m = compute_field_3d(positions, mass_nodes)
    field_f = [0.0] * n

    psi_a = propagate_3d(positions, adj, field_m, src, k, blocked | set(sb))
    psi_b = propagate_3d(positions, adj, field_m, src, k, blocked | set(sa))
    pa = {d: abs(psi_a[d])**2 for d in det_list}
    pb = {d: abs(psi_b[d])**2 for d in det_list}
    na_a = sum(pa.values()); nb_a = sum(pb.values())
    if na_a < 1e-30 or nb_a < 1e-30: return None
    dtv = 0.5 * sum(abs(pa[d]/na_a - pb[d]/nb_a) for d in det_list)

    ba = bin_amplitudes_3d(psi_a, positions, mid)
    bb = bin_amplitudes_3d(psi_b, positions, mid)
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    NA = sum(abs(a)**2 for a in ba); NB = sum(abs(b)**2 for b in bb)
    Sn = S / (NA+NB) if (NA+NB) > 0 else 0
    D_cl = math.exp(-LAM**2 * Sn)
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1,d2)] = (psi_a[d1].conjugate()*psi_a[d2] + psi_b[d1].conjugate()*psi_b[d2]
                            + D_cl*psi_a[d1].conjugate()*psi_b[d2] + D_cl*psi_b[d1].conjugate()*psi_a[d2])
    tr = sum(rho[(d,d)] for d in det_list).real
    if tr < 1e-30: return None
    for key in rho: rho[key] /= tr
    pur_cl = sum(abs(v)**2 for v in rho.values()).real

    am = propagate_3d(positions, adj, field_m, src, k, blocked)
    af = propagate_3d(positions, adj, field_f, src, k, blocked)
    pm = sum(abs(am[d])**2 for d in det_list); pf = sum(abs(af[d])**2 for d in det_list)
    grav = 0.0
    if pm > 1e-30 and pf > 1e-30:
        grav = (sum(abs(am[d])**2*positions[d][1] for d in det_list)/pm
                - sum(abs(af[d])**2*positions[d][1] for d in det_list)/pf)

    born = math.nan
    if upper and lower and middle:
        born = sorkin_born(positions, adj, src, k, bi, [upper[0]], [lower[0]], [middle[0]], det_list, field_f)

    return {"dtv": dtv, "pur_cl": pur_cl, "s_norm": Sn, "gravity": grav, "born": born}


def _mean_se(vals):
    vals = [v for v in vals if v is not None and not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals) / (len(vals)-1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 110)
    print("SCALED MIRROR DAGs: HYBRID CHOKEPOINT")
    print(f"  k={K}, {N_SEEDS} seeds, CL bath lambda={LAM}")
    print("=" * 110)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    configs = [
        ("S1: NPL=75, r=4", 75, 4.0),
        ("S2: NPL=25, r=5", 25, 5.0),
        ("S3: NPL=25, r=6", 25, 6.0),
        ("S4: NPL=40, r=5", 40, 5.0),
    ]

    for label, npl_h, cr in configs:
        print(f"  {label}")
        print(f"  {'N':>4s}  {'d_TV':>8s}  {'pur_cl':>8s}  {'gravity':>10s}  "
              f"{'Born':>10s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 58}")

        for nl in [25, 40, 60, 80]:
            t0 = time.time()
            dtv_all, pur_all, grav_all, born_all = [], [], [], []
            for seed in seeds:
                pos, adj, bl, _ = generate_mirror_hybrid(nl, npl_h, XYZ_RANGE, cr, seed)
                r = measure_joint(pos, adj, nl, K)
                if r:
                    dtv_all.append(r["dtv"])
                    pur_all.append(r["pur_cl"])
                    grav_all.append(r["gravity"])
                    if not math.isnan(r["born"]): born_all.append(r["born"])
            dt = time.time() - t0
            if dtv_all:
                mdtv, _ = _mean_se(dtv_all)
                mpur, sepur = _mean_se(pur_all)
                mg, seg = _mean_se(grav_all)
                mborn, _ = _mean_se(born_all)
                born_s = f"{mborn:10.2e}" if not math.isnan(mborn) else "       nan"
                print(f"  {nl:4d}  {mdtv:8.4f}  {mpur:7.4f}±{sepur:.02f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {born_s}  {len(dtv_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {nl:4d}  FAIL  {dt:4.0f}s")
        print()

    print("Born threshold: < 1e-10 = PERFECT, < 0.01 = PASS, >= 0.1 = FAIL")
    print("Joint target: pur_cl < 0.95 + gravity > 0 + Born < 0.01")


if __name__ == "__main__":
    main()
