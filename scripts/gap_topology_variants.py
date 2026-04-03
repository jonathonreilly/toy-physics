#!/usr/bin/env python3
"""Gap topology variants: what topological features of the gap matter?

Gap-as-physics investigation, Experiment 3.

Since the gap is fundamentally about node absence, test how the SHAPE
of the node-free region affects decoherence:

1. Two parallel gaps (three channels)
   - Gaps at y=+2 and y=-2, each width 2
   - Creates: upper (y>3), middle (-1<y<1), lower (y<-3) channels
   - Both slits reach the middle channel → partial mixing

2. Angled gap (tilted in x-y plane)
   - Gap center drifts: y_gap(x_frac) = slope * (x_frac - 0.5) * y_range
   - Tests whether the gap must be perpendicular to slit axis

3. Partial x-extent (gap only in first/last portion)
   - gap_start: gap in first 50% post-barrier only
   - gap_end: gap in last 50% post-barrier only
   - Tests where along the causal direction the gap matters

4. Gap with bridge nodes (controlled leakage)
   - Standard gap=4, but add exactly N bridge nodes per layer at y=0
   - n_bridges = {0, 1, 2, 5} per layer
   - Tests how many bridging nodes it takes to break decoherence
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


def _connect_node(idx, positions, adj, layer_indices, layer, connect_radius,
                  rng, crosslink_prob=0.02, barrier_layer=0, gap_center=0.0):
    """Connect new node to previous layers with channel-aware logic."""
    x, y, z = positions[idx]
    for prev_layer in layer_indices[max(0, layer - 2):]:
        for prev_idx in prev_layer:
            px, py, pz = positions[prev_idx]
            dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
            if layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
                # Channel logic: same side of gap_center
                same_ch = ((y - gap_center) * (py - gap_center) > 0)
                if same_ch:
                    if dist <= connect_radius:
                        adj[prev_idx].append(idx)
                else:
                    if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                        adj[prev_idx].append(idx)
            else:
                if dist <= connect_radius:
                    adj[prev_idx].append(idx)


def generate_two_gap_dag(n_layers, npl, xyz_range, connect_radius, rng_seed,
                          gap_width=2.0, gap_offset=2.0):
    """Two parallel gaps creating three channels."""
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
            for _ in range(npl):
                z = rng.uniform(-xyz_range, xyz_range)
                if layer > barrier_layer:
                    # Exclude two bands: [offset-w/2, offset+w/2] and [-offset-w/2, -offset+w/2]
                    gap1_lo, gap1_hi = gap_offset - gap_width/2, gap_offset + gap_width/2
                    gap2_lo, gap2_hi = -gap_offset - gap_width/2, -gap_offset + gap_width/2
                    while True:
                        y = rng.uniform(-xyz_range, xyz_range)
                        if not (gap1_lo <= y <= gap1_hi or gap2_lo <= y <= gap2_hi):
                            break
                else:
                    y = rng.uniform(-xyz_range, xyz_range)

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
    return positions, dict(adj)


def generate_angled_gap_dag(n_layers, npl, xyz_range, connect_radius, rng_seed,
                             gap=4.0, slope=0.0):
    """Gap center drifts linearly along causal direction."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    n_post = n_layers - barrier_layer - 1

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            if layer > barrier_layer and n_post > 0:
                x_frac = (layer - barrier_layer - 1) / max(1, n_post - 1)
                gap_center = slope * (x_frac - 0.5) * xyz_range
            else:
                gap_center = 0.0

            for node_i in range(npl):
                z = rng.uniform(-xyz_range, xyz_range)
                if layer > barrier_layer:
                    if node_i < npl // 2:
                        y = rng.uniform(gap_center + gap / 2, xyz_range)
                    else:
                        y = rng.uniform(-xyz_range, gap_center - gap / 2)
                    y = max(-xyz_range, min(xyz_range, y))
                else:
                    y = rng.uniform(-xyz_range, xyz_range)

                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if layer > barrier_layer and positions[prev_idx][0] > barrier_layer:
                            same_ch = ((y - gap_center) * (py - gap_center) > 0)
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


def generate_partial_extent_dag(n_layers, npl, xyz_range, connect_radius, rng_seed,
                                 gap=4.0, region="start"):
    """Gap exists only in first or last portion of post-barrier."""
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    barrier_layer = n_layers // 3
    n_post = n_layers - barrier_layer - 1

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            use_gap = False
            if layer > barrier_layer and n_post > 0:
                x_frac = (layer - barrier_layer - 1) / max(1, n_post - 1)
                if region == "start" and x_frac < 0.5:
                    use_gap = True
                elif region == "end" and x_frac >= 0.5:
                    use_gap = True

            for node_i in range(npl):
                z = rng.uniform(-xyz_range, xyz_range)
                if use_gap:
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
                        if use_gap and positions[prev_idx][0] > barrier_layer:
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


def generate_bridge_dag(n_layers, npl, xyz_range, connect_radius, rng_seed,
                         gap=4.0, n_bridges=0):
    """Standard modular gap with exactly n_bridges nodes per layer at y~0."""
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
            # Channel nodes
            for node_i in range(npl):
                z = rng.uniform(-xyz_range, xyz_range)
                if layer > barrier_layer:
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

            # Bridge nodes at y~0
            if layer > barrier_layer:
                for _ in range(n_bridges):
                    y = rng.uniform(-gap / 4, gap / 4)
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
    return positions, dict(adj)


# ---------- physics ----------

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


def run_variant(label, gen_fn, nl_list, seeds, k_band):
    """Run a topology variant across N values."""
    for nl in nl_list:
        t0 = time.time()
        pc_all, sn_all, grav_all = [], [], []
        for seed in seeds:
            positions, adj = gen_fn(nl, seed)
            r = measure(positions, adj, nl, k_band)
            if r:
                pc_all.append(r["pur_cl"])
                sn_all.append(r["s_norm"])
                grav_all.append(r["gravity"])
        dt = time.time() - t0
        if pc_all:
            mpc, sepc = _mean_se(pc_all)
            msn, _ = _mean_se(sn_all)
            mg, seg = _mean_se(grav_all)
            print(f"  {nl:4d}  {label:>18s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                  f"{mg:+7.4f}±{seg:.3f}  {len(pc_all):3d}  {dt:4.0f}s")
        else:
            print(f"  {nl:4d}  {label:>18s}  FAIL  {dt:4.0f}s")


def main():
    print("=" * 95)
    print("GAP TOPOLOGY VARIANTS")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    print(f"  {'N':>4s}  {'variant':>18s}  {'pur_cl':>10s}  {'S_norm':>8s}  "
          f"{'gravity':>10s}  {'ok':>3s}  {'time':>5s}")
    print(f"  {'-' * 72}")

    # Baselines
    run_variant("uniform",
                lambda nl, s: generate_angled_gap_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap=0, slope=0),
                N_LAYERS_LIST, seeds, K_BAND)

    run_variant("hard-gap-4",
                lambda nl, s: generate_angled_gap_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap=4, slope=0),
                N_LAYERS_LIST, seeds, K_BAND)

    print()

    # Two parallel gaps
    print("  --- TWO PARALLEL GAPS ---")
    run_variant("two-gap-w2-o2",
                lambda nl, s: generate_two_gap_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap_width=2, gap_offset=2),
                N_LAYERS_LIST, seeds, K_BAND)

    run_variant("two-gap-w2-o4",
                lambda nl, s: generate_two_gap_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap_width=2, gap_offset=4),
                N_LAYERS_LIST, seeds, K_BAND)

    print()

    # Angled gap
    print("  --- ANGLED GAP ---")
    for slope in [0.1, 0.3, 0.5]:
        run_variant(f"angled-{slope:.1f}",
                    lambda nl, s, sl=slope: generate_angled_gap_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap=4, slope=sl),
                    N_LAYERS_LIST, seeds, K_BAND)

    print()

    # Partial x-extent
    print("  --- PARTIAL X-EXTENT ---")
    run_variant("gap-start-50%",
                lambda nl, s: generate_partial_extent_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap=4, region="start"),
                N_LAYERS_LIST, seeds, K_BAND)

    run_variant("gap-end-50%",
                lambda nl, s: generate_partial_extent_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap=4, region="end"),
                N_LAYERS_LIST, seeds, K_BAND)

    print()

    # Bridge nodes
    print("  --- CONTROLLED BRIDGE NODES ---")
    for nb in [0, 1, 2, 5]:
        run_variant(f"bridge-{nb}",
                    lambda nl, s, n=nb: generate_bridge_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, gap=4, n_bridges=n),
                    N_LAYERS_LIST, seeds, K_BAND)

    print()
    print("KEY QUESTIONS:")
    print("  Two-gap: does a third (middle) channel help or hurt?")
    print("  Angled: at what tilt does the gap break?")
    print("  Partial: start vs end — where does the gap matter most?")
    print("  Bridge: how many bridge nodes to break decoherence?")


if __name__ == "__main__":
    main()
