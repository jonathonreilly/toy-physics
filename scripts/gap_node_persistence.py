#!/usr/bin/env python3
"""Node persistence: remove nodes that don't carry which-path information.

Gap-as-physics investigation, Experiment 6.

From Experiments 1-5c we know:
  - The gap is about NODE ABSENCE, not edge suppression
  - Soft penalties on edges cannot replicate the hard gap
  - The gap location is weakly constrained (partial profile works)

This experiment tests a physics-motivated node removal rule:
  1. Generate a UNIFORM DAG (no gap)
  2. Propagate single-slit amplitudes (slit A only, slit B only)
  3. For each post-barrier node, compute its which-path distinguishability:
       D(node) = |amp_A(node)|^2 - |amp_B(node)|^2
     Nodes near y=0 receive similar amplitude from both slits → D ≈ 0
     Nodes far from y=0 receive amplitude from one slit → |D| large
  4. Remove nodes with |D| below threshold (they don't "persist" because
     they carry no which-path information)
  5. Re-propagate on the pruned graph and measure decoherence

This is the discrete analogue of "events that don't record which-path
information are not stable" — connecting to axiom 2 (stable objects are
self-maintaining patterns) and axiom 9 (measurement is durable record
formation).

Key question: does physics-motivated node removal create an effective
gap that produces decoherence, and does it scale?

Also compare: D-threshold pruning vs the existing adaptive-quantile
approach, and vs the hard gap baseline.
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
D_THRESHOLDS = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05, 0.10]


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


def generate_3d_dag_uniform(n_layers, nodes_per_layer, xyz_range, connect_radius, rng_seed):
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
            for _ in range(nodes_per_layer):
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

    return positions, dict(adj), barrier_layer


def generate_3d_dag_modular(n_layers, nodes_per_layer, xyz_range, connect_radius, rng_seed, gap):
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
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-xyz_range, xyz_range)
                if layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
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
        layer_indices.append(layer_nodes)

    return positions, dict(adj), barrier_layer


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


def compute_node_distinguishability(positions, adj, src, blocked, sa, sb, k, field):
    """Compute per-node which-path distinguishability.

    D(node) = |amp_A(node)|^2 - |amp_B(node)|^2
    where amp_A is single-slit-A propagation, amp_B is single-slit-B.

    Returns dict: node_idx -> |D| value
    """
    aa = propagate_3d(positions, adj, field, src, k, blocked | set(sb))
    ab = propagate_3d(positions, adj, field, src, k, blocked | set(sa))

    dist = {}
    for i in range(len(positions)):
        pA = abs(aa[i])**2
        pB = abs(ab[i])**2
        dist[i] = abs(pA - pB)
    return dist


def prune_by_distinguishability(adj, positions, d_threshold, node_D,
                                 barrier_layer, src_set, det_set, slit_set):
    """Remove post-barrier nodes with |D| < threshold.
    Never remove source, detector, slit, or pre-barrier nodes.
    Returns pruned adj and set of removed nodes.
    """
    protected = src_set | det_set | slit_set
    removed = set()

    for idx, (x, y, z) in enumerate(positions):
        if idx in protected:
            continue
        if x <= barrier_layer:
            continue
        if node_D.get(idx, 0) < d_threshold:
            removed.add(idx)

    # Rebuild adj excluding removed nodes
    new_adj = {}
    for i, neighbors in adj.items():
        if i in removed:
            continue
        new_neighbors = [j for j in neighbors if j not in removed]
        if new_neighbors:
            new_adj[i] = new_neighbors

    return new_adj, removed


def measure_full(positions, adj, n_layers, k_band, label=""):
    """Full measurement pipeline: gravity + decoherence."""
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
        # Return slit info for pruning
        "_src": src, "_det": det_list, "_sa": sa, "_sb": sb,
        "_blocked": blocked, "_mass": mass_nodes, "_mid": mid,
        "_bl": bl_idx, "_layers": layers, "_by_layer": by_layer,
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
    print("NODE PERSISTENCE: PHYSICS-MOTIVATED GAP FORMATION")
    print(f"  Remove nodes with low which-path distinguishability |D|")
    print(f"  CL bath lambda={LAM}, k-band={K_BAND}, {N_SEEDS} seeds")
    print(f"  Thresholds: {D_THRESHOLDS}")
    print("=" * 95)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    for nl in N_LAYERS_LIST:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'mode':>14s}  {'pur_cl':>10s}  {'S_norm':>8s}  {'gravity':>10s}  "
              f"{'removed':>7s}  {'rem%':>5s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 78}")

        # Baselines
        for label, gen_fn in [
            ("uniform", lambda s: generate_3d_dag_uniform(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s)),
            ("hard-gap", lambda s: generate_3d_dag_modular(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, s, 4.0)),
        ]:
            t0 = time.time()
            pc_all, sn_all, grav_all = [], [], []
            for seed in seeds:
                result = gen_fn(seed)
                positions, adj = result[0], result[1]
                r = measure_full(positions, adj, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])
            dt = time.time() - t0
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                print(f"  {label:>14s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {'--':>7s}  {'--':>5s}  {len(pc_all):3d}  {dt:4.0f}s")

        # D-threshold pruning
        for d_thresh in D_THRESHOLDS:
            if d_thresh == 0.0:
                continue  # same as uniform baseline
            t0 = time.time()
            pc_all, sn_all, grav_all, rem_all = [], [], [], []

            for seed in seeds:
                positions, adj, barrier_layer = generate_3d_dag_uniform(
                    nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)

                # First pass: get slit/barrier info
                r0 = measure_full(positions, adj, nl, K_BAND)
                if not r0:
                    continue

                src = r0["_src"]
                sa, sb = r0["_sa"], r0["_sb"]
                blocked = r0["_blocked"]
                mass_nodes = r0["_mass"]
                det_set = set(r0["_det"])
                slit_set = set(sa + sb)
                src_set = set(src)

                # Compute D using middle k value
                field_m = compute_field_3d(positions, mass_nodes)
                k_probe = K_BAND[len(K_BAND) // 2]
                node_D = compute_node_distinguishability(
                    positions, adj, src, blocked, sa, sb, k_probe, field_m)

                # Prune
                adj_pruned, removed = prune_by_distinguishability(
                    adj, positions, d_thresh, node_D, barrier_layer,
                    src_set, det_set, slit_set)

                n_post = sum(1 for idx, (x, y, z) in enumerate(positions)
                             if x > barrier_layer and idx not in (src_set | det_set | slit_set))
                rem_pct = 100 * len(removed) / max(1, n_post)
                rem_all.append(rem_pct)

                # Re-measure on pruned graph
                r = measure_full(positions, adj_pruned, nl, K_BAND)
                if r:
                    pc_all.append(r["pur_cl"])
                    sn_all.append(r["s_norm"])
                    grav_all.append(r["gravity"])

            dt = time.time() - t0
            label = f"D>={d_thresh:.3f}"
            if pc_all:
                mpc, sepc = _mean_se(pc_all)
                msn, _ = _mean_se(sn_all)
                mg, seg = _mean_se(grav_all)
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {label:>14s}  {mpc:7.4f}±{sepc:.3f}  {msn:8.4f}  "
                      f"{mg:+7.4f}±{seg:.3f}  {mrem:6.1f}%  {'':>5s}  {len(pc_all):3d}  {dt:4.0f}s")
            else:
                mrem = sum(rem_all) / len(rem_all) if rem_all else 0
                print(f"  {label:>14s}  FAIL  rem={mrem:.1f}%  {dt:4.0f}s")

        print()

    # Distribution of D values (diagnostic)
    print("  D-VALUE DISTRIBUTION (N=25, seed=3)")
    print(f"  {'y_bin':>8s}  {'mean_D':>10s}  {'max_D':>10s}  {'n_nodes':>7s}")
    print(f"  {'-' * 40}")
    positions, adj, bl = generate_3d_dag_uniform(25, NPL, XYZ_RANGE, CONNECT_RADIUS, 3)
    r0 = measure_full(positions, adj, 25, K_BAND)
    if r0:
        field_m = compute_field_3d(positions, r0["_mass"])
        node_D = compute_node_distinguishability(
            positions, adj, r0["_src"], r0["_blocked"],
            r0["_sa"], r0["_sb"], K_BAND[1], field_m)

        # Bin D by y-coordinate
        y_bins = defaultdict(list)
        for idx, (x, y, z) in enumerate(positions):
            if x > bl:
                yb = int(y / 3) * 3  # 3-unit bins
                y_bins[yb].append(node_D.get(idx, 0))

        for yb in sorted(y_bins.keys()):
            vals = y_bins[yb]
            md = sum(vals) / len(vals)
            mx = max(vals)
            print(f"  {yb:>5d}..{yb+3:<3d}  {md:10.6f}  {mx:10.6f}  {len(vals):7d}")

    print()
    print("PHYSICS INTERPRETATION:")
    print("  If D peaks at |y|>>0 and is near zero at y~0:")
    print("    → Removal by D creates a y-gap naturally")
    print("    → The gap emerges from which-path physics, not geometry")
    print("  If D is uniform across y:")
    print("    → The distinguishability is not spatially structured")
    print("    → Node removal would be random, not gap-forming")


if __name__ == "__main__":
    main()
