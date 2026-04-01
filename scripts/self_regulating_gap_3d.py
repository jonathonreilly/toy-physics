#!/usr/bin/env python3
"""Self-regulating hard-gap dynamics on 3D DAGs.

Gate B of the review backlog: "the single strongest substantive gap
visible to external reviewers." The model claims an evolving network
but analyzes static graphs.

Previous attempts (2D, 9 approaches):
  - Connection bias: CLT convergence still operates
  - Node removal (fixed fraction): marginal at N=40, ceiling at N=80
  - All failed because 2D CLT ceiling kills everything at large N

This test: 3D self-regulating node removal with iterative feedback.
  1. Start with uniform 3D DAG (no imposed gap)
  2. Propagate from each slit, compute distinguishability D(i)
  3. Remove nodes below threshold D_min
  4. Re-propagate on pruned graph
  5. Repeat until stable (fixed point or max iterations)
  6. Measure decoherence on the evolved graph

The 3D CLT delay (pur_cl=0.955 at N=80 vs 2D 0.987) gives more room
for the self-regulating rule to work.

Physics: "events that don't carry which-path information are pruned
from the causal structure. The geometry evolves toward a state where
all surviving events are measurement-relevant."

PStack experiment: self-regulating-gap-3d
"""

from __future__ import annotations

import cmath
import math
import random
import statistics
from collections import defaultdict, deque

BETA = 0.8
N_YBINS = 8
LAM = 10.0


def generate_3d_uniform_dag(n_layers=20, nodes_per_layer=30, yz_range=10.0,
                            connect_radius=3.5, rng_seed=42):
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
            for _ in range(nodes_per_layer):
                y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
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
    return positions, dict(adj), layer_indices


def compute_field_3d(positions, adj, mass_ids, iterations=50):
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    ms = set(mass_ids)
    field = [1.0 if i in ms else 0.0 for i in range(n)]
    for _ in range(iterations):
        nf = [0.0] * n
        for i in range(n):
            if i in ms:
                nf[i] = 1.0
            elif undirected.get(i):
                nf[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = nf
    return field


def propagate_3d(positions, adj, field, src, k, blocked=None):
    n = len(positions)
    blocked = blocked or set()
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
            cos_theta = dx / L
            theta = math.acos(min(max(cos_theta, -1), 1))
            w = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl*dl - L*L, 0))
            act = dl - ret
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def cl_contrast(amps_a, amps_b, mid_nodes, positions):
    ys = [positions[m][1] for m in mid_nodes]
    if not ys:
        return 0.0
    y_min, y_max = min(ys)-0.01, max(ys)+0.01
    bw = (y_max - y_min) / N_YBINS
    ba = [0j] * N_YBINS
    bb = [0j] * N_YBINS
    for m in mid_nodes:
        b = max(0, min(N_YBINS-1, int((positions[m][1] - y_min) / bw)))
        ba[b] += amps_a[m]
        bb[b] += amps_b[m]
    S = sum(abs(a-b)**2 for a, b in zip(ba, bb))
    d = sum(abs(a)**2 for a in ba) + sum(abs(b)**2 for b in bb)
    return S / d if d > 0 else 0.0


def cl_purity(amps_a, amps_b, D, det_list):
    rho = {}
    for d1 in det_list:
        for d2 in det_list:
            rho[(d1, d2)] = (amps_a[d1]*amps_a[d2].conjugate() +
                             amps_b[d1]*amps_b[d2].conjugate() +
                             D * amps_a[d1]*amps_b[d2].conjugate() +
                             D * amps_b[d1]*amps_a[d2].conjugate())
    tr = sum(rho[(d, d)] for d in det_list).real
    if tr <= 1e-30:
        return math.nan
    for key in rho:
        rho[key] /= tr
    return sum(abs(v)**2 for v in rho.values()).real


def self_regulating_prune(positions, adj, layer_indices, d_min=0.3,
                          max_iter=5, verbose=False):
    """Iteratively remove post-barrier nodes with low slit-distinguishability.

    Returns modified adj and statistics about the evolution.
    """
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3

    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)

    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return adj, {"converged": False, "iterations": 0, "removed": 0}

    slit_set = set(slit_a + slit_b)
    base_blocked = set(barrier) - slit_set
    blocked_a = base_blocked | set(slit_b)
    blocked_b = base_blocked | set(slit_a)
    det_set = set(layer_indices[-1])

    current_adj = dict(adj)
    total_removed = 0
    field = [0.0] * n  # flat field for distinguishability computation

    for iteration in range(max_iter):
        # Propagate from each slit
        amps_a = propagate_3d(positions, current_adj, field,
                              layer_indices[0], 5.0, blocked_a)
        amps_b = propagate_3d(positions, current_adj, field,
                              layer_indices[0], 5.0, blocked_b)

        # Compute distinguishability at post-barrier nodes
        low_d_nodes = set()
        for li in range(bl_idx + 1, n_layers - 1):
            for i in layer_indices[li]:
                if i in det_set:
                    continue
                pa = abs(amps_a[i])**2
                pb = abs(amps_b[i])**2
                total = pa + pb
                if total > 1e-30:
                    D = abs(pa - pb) / total
                else:
                    D = 0.0
                if D < d_min:
                    low_d_nodes.add(i)

        if not low_d_nodes:
            if verbose:
                print(f"    iter {iteration}: no nodes below threshold → converged")
            return current_adj, {"converged": True, "iterations": iteration,
                                 "removed": total_removed}

        # Remove low-D nodes
        new_adj = {}
        for i, nbs in current_adj.items():
            if i in low_d_nodes:
                continue
            filtered = [j for j in nbs if j not in low_d_nodes]
            if filtered:
                new_adj[i] = filtered

        removed_this = len(low_d_nodes)
        total_removed += removed_this
        current_adj = new_adj

        if verbose:
            print(f"    iter {iteration}: removed {removed_this} nodes "
                  f"(total {total_removed})")

    return current_adj, {"converged": False, "iterations": max_iter,
                         "removed": total_removed}


def measure_decoherence(positions, adj, layer_indices):
    """Measure CL bath purity on a graph."""
    k_band = [3.0, 5.0, 7.0]
    n = len(positions)
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    if not det_list or n_layers < 7:
        return math.nan

    all_ys = [positions[i][1] for i in range(n)]
    cy = sum(all_ys) / len(all_ys)

    barrier = layer_indices[bl_idx]
    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return math.nan

    blocked = set(barrier) - set(slit_a + slit_b)
    blocked_a = blocked | set(slit_b)
    blocked_b = blocked | set(slit_a)

    # Mass for CL bath
    bath_mass = []
    for li in range(bl_idx+1, min(n_layers, bl_idx+3)):
        for i in layer_indices[li]:
            if abs(positions[i][1] - cy) <= 3:
                bath_mass.append(i)
    grav_idx = 2 * n_layers // 3
    grav_mass = [i for i in layer_indices[grav_idx] if positions[i][1] > cy+1]
    all_mass = list(set(bath_mass) | set(grav_mass))
    field = compute_field_3d(positions, adj, all_mass) if all_mass else [0.0]*n

    mid_nodes = [i for li in range(bl_idx+1, n_layers-1)
                 for i in layer_indices[li]
                 if i not in blocked and i not in set(det_list)]
    if len(mid_nodes) < 4:
        return math.nan

    pur_list = []
    for k in k_band:
        aa = propagate_3d(positions, adj, field, src, k, blocked_a)
        ab = propagate_3d(positions, adj, field, src, k, blocked_b)
        Sn = cl_contrast(aa, ab, mid_nodes, positions)
        D = math.exp(-LAM**2 * Sn)
        pur = cl_purity(aa, ab, D, det_list)
        if not math.isnan(pur):
            pur_list.append(pur)

    return sum(pur_list)/len(pur_list) if pur_list else math.nan


def gap_metric(positions, adj, layer_indices):
    """Measure effective gap width from the y-distribution of active post-barrier nodes."""
    n_layers = len(layer_indices)
    bl_idx = n_layers // 3
    det_set = set(layer_indices[-1])

    ys = []
    for li in range(bl_idx+1, n_layers-1):
        for i in layer_indices[li]:
            if i in det_set:
                continue
            # Check if node is still connected (has edges)
            if i in adj or any(i in nbs for nbs in adj.values()):
                ys.append(positions[i][1])

    if len(ys) < 10:
        return 0.0

    ys.sort()
    # Find largest gap in the y-distribution
    max_gap = 0
    for i in range(1, len(ys)):
        gap = ys[i] - ys[i-1]
        if gap > max_gap:
            max_gap = gap

    return max_gap


def main():
    n_seeds = 16

    print("=" * 74)
    print("SELF-REGULATING HARD-GAP DYNAMICS ON 3D DAGs")
    print("  Gate B: does iterative node removal create emergent gap structure?")
    print("  3D CLT delay gives more room than 2D (pur_cl=0.955 vs 0.987 at N=80)")
    print("=" * 74)
    print()

    # Compare: uniform baseline vs self-regulated at different thresholds
    for d_min in [0.0, 0.1, 0.2, 0.3, 0.5]:
        label = "Uniform baseline" if d_min == 0 else f"Self-regulated d_min={d_min}"
        print(f"  [{label}]")
        print(f"  {'N':>4s}  {'pur_cl':>8s}  {'gap':>6s}  {'removed':>8s}  {'conv':>5s}  {'n':>3s}")
        print(f"  {'-'*42}")

        for nl in [15, 20, 25, 30, 40]:
            pur_list = []
            gap_list = []
            removed_list = []
            conv_list = []

            for seed in range(n_seeds):
                positions, adj_orig, layer_indices = generate_3d_uniform_dag(
                    n_layers=nl, nodes_per_layer=30, yz_range=10.0,
                    connect_radius=3.5, rng_seed=seed*13+5)

                if d_min > 0:
                    adj_evolved, stats = self_regulating_prune(
                        positions, adj_orig, layer_indices, d_min=d_min, max_iter=5)
                    removed_list.append(stats["removed"])
                    conv_list.append(1 if stats["converged"] else 0)
                else:
                    adj_evolved = adj_orig
                    removed_list.append(0)
                    conv_list.append(1)

                pur = measure_decoherence(positions, adj_evolved, layer_indices)
                if not math.isnan(pur):
                    pur_list.append(pur)
                    gap_list.append(gap_metric(positions, adj_evolved, layer_indices))

            if pur_list:
                mp = sum(pur_list) / len(pur_list)
                mg = sum(gap_list) / len(gap_list) if gap_list else 0
                mr = sum(removed_list) / len(removed_list)
                mc = sum(conv_list) / len(conv_list)
                print(f"  {nl:4d}  {mp:8.4f}  {mg:6.2f}  {mr:8.1f}  {mc:5.2f}  {len(pur_list):3d}")
            else:
                print(f"  {nl:4d}  FAIL")

        print()

    # Paired comparison at N=30
    print("PAIRED COMPARISON at N=30 (16 seeds)")
    print(f"  {'rule':>25s}  {'pur_cl':>8s}  {'delta':>8s}  {'gap':>6s}")
    print(f"  {'-'*52}")

    baseline_purs = []
    for d_min in [0.0, 0.1, 0.2, 0.3, 0.5]:
        purs = []
        gaps = []
        for seed in range(n_seeds):
            positions, adj_orig, layer_indices = generate_3d_uniform_dag(
                n_layers=30, nodes_per_layer=30, yz_range=10.0,
                connect_radius=3.5, rng_seed=seed*13+5)

            if d_min > 0:
                adj_e, _ = self_regulating_prune(
                    positions, adj_orig, layer_indices, d_min=d_min, max_iter=5)
            else:
                adj_e = adj_orig

            pur = measure_decoherence(positions, adj_e, layer_indices)
            if not math.isnan(pur):
                purs.append(pur)
                gaps.append(gap_metric(positions, adj_e, layer_indices))

        if purs:
            mp = sum(purs) / len(purs)
            mg = sum(gaps) / len(gaps)
            if d_min == 0:
                baseline_purs = purs
                delta = 0.0
            else:
                delta = mp - (sum(baseline_purs)/len(baseline_purs) if baseline_purs else 0)
            label = "Uniform" if d_min == 0 else f"Self-reg d_min={d_min}"
            print(f"  {label:>25s}  {mp:8.4f}  {delta:+8.4f}  {mg:6.2f}")

    print()
    print("=" * 74)
    print("INTERPRETATION:")
    print("  delta < 0: self-regulation improves decoherence (lower purity)")
    print("  gap > 0: pruning creates spatial separation in y-distribution")
    print("  Converged: the rule reaches a fixed point (all remaining nodes")
    print("             carry which-path information)")
    print()
    print("  SUCCESS: delta < -0.02 at N=30-40 with gap > 1.0")
    print("  FAILURE: delta ≈ 0 or positive, or gap too small/large")
    print("=" * 74)


if __name__ == "__main__":
    main()
