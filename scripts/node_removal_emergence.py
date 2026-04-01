#!/usr/bin/env python3
"""Node-removal emergence: prune low-distinguishability nodes to create gaps.

All 8 previous emergence approaches tried to AVOID placing nodes in
the gap zone, or to BIAS connections. All failed.

New approach: grow a UNIFORM random DAG, then REMOVE post-barrier
nodes where slit-distinguishability is low. The gap forms by subtraction.

Physics interpretation: "events that don't carry which-path information
don't persist in the causal structure." The geometry prunes itself of
measurement-ambiguous events.

This has three advantages over placement rules:
1. The removal is precise — we know exactly which nodes are confused
2. We can control how many to remove (pruning fraction)
3. The remaining graph retains its original connectivity pattern

RULE: After building a uniform DAG:
1. Propagate from each slit to all post-barrier nodes
2. Compute slit distinguishability D(i) at each node
3. Remove the fraction `prune` of post-barrier nodes with lowest D
4. Edges to/from removed nodes are deleted

Variants:
- prune by D(i) threshold
- prune by fraction of nodes
- prune only in specific layer range (near barrier vs everywhere)
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.generative_causal_dag_interference import generate_causal_dag
from scripts.topology_families import generate_modular_dag

BETA = 0.8
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


def _propagate_quick(positions, adj, n, src_set, blocked=None):
    """Quick propagation returning |amp|^2 per node."""
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src_set:
        amps[s] = 1.0 / max(1, len(src_set))
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * 5.0 * L) * w / L
            amps[j] += amps[i] * ea
    return [abs(a) ** 2 for a in amps]


def generate_removal_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    prune_frac: float = 0.2,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """Build uniform DAG, then remove low-distinguishability post-barrier nodes.

    prune_frac: fraction of post-barrier nodes to remove (those with lowest D).
    Removed nodes have all edges deleted (they become isolated).
    The barrier layer and detector layer are never pruned.
    """
    # Step 1: Build uniform random DAG
    positions, adj, arrival = generate_causal_dag(
        n_layers=n_layers, nodes_per_layer=nodes_per_layer,
        y_range=y_range, connect_radius=connect_radius,
        rng_seed=rng_seed,
    )

    n = len(positions)

    # Step 2: Identify barrier and slits
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return positions, adj, arrival

    barrier_layer = layers[len(layers) // 3]
    bi = by_layer[barrier_layer]
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)

    slit_upper = [i for i in bi if positions[i][1] > cy + 3][:3]
    slit_lower = [i for i in bi if positions[i][1] < cy - 3][:3]
    barrier_blocked = set(bi) - set(slit_upper + slit_lower)

    if not slit_upper or not slit_lower:
        return positions, adj, arrival

    # Step 3: Propagate from each slit
    blocked_for_upper = barrier_blocked | set(slit_lower)
    blocked_for_lower = barrier_blocked | set(slit_upper)

    amp_upper = _propagate_quick(positions, adj, n, by_layer[layers[0]], blocked_for_upper)
    amp_lower = _propagate_quick(positions, adj, n, by_layer[layers[0]], blocked_for_lower)

    # Step 4: Compute distinguishability at each post-barrier node
    post_barrier_nodes = []
    detector_layer = layers[-1]
    for layer_key in layers:
        if layer_key <= barrier_layer or layer_key == detector_layer:
            continue
        for i in by_layer[layer_key]:
            au = amp_upper[i]
            al = amp_lower[i]
            total = au + al
            if total > 1e-30:
                D = abs(au - al) / total
            else:
                D = 0.0
            post_barrier_nodes.append((i, D))

    # Step 5: Sort by distinguishability, remove lowest fraction
    post_barrier_nodes.sort(key=lambda x: x[1])
    n_remove = int(len(post_barrier_nodes) * prune_frac)
    remove_set = set(idx for idx, _ in post_barrier_nodes[:n_remove])

    # Step 6: Remove edges to/from pruned nodes
    new_adj = {}
    for i, nbs in adj.items():
        if i in remove_set:
            continue
        new_adj[i] = [j for j in nbs if j not in remove_set]

    return positions, new_adj, arrival


# ─── Decoherence + gravity machinery ──────────────────────────────

def compute_field(positions, mass_nodes, strength=0.1):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += strength / r
    return field


def propagate_full(positions, adj, field, src, k, blocked=None):
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
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0))
            act = dl - ret
            theta = math.atan2(abs(dy), max(dx, 1e-10))
            w = math.exp(-BETA * theta * theta)
            ea = cmath.exp(1j * k * act) * w / L
            amps[j] += amps[i] * ea
    return amps


def bin_amplitudes(amps, positions, nodes):
    bins = [0j] * N_YBINS
    bw = 24.0 / N_YBINS
    for m in nodes:
        y = positions[m][1]
        b = int((y + 12.0) / bw)
        b = max(0, min(N_YBINS - 1, b))
        bins[b] += amps[m]
    return bins


def cl_purity_triple(amps_a, amps_b, D, det_list):
    def _pur(Dv):
        rho = {}
        for d1 in det_list:
            for d2 in det_list:
                rho[(d1, d2)] = (
                    amps_a[d1].conjugate() * amps_a[d2]
                    + amps_b[d1].conjugate() * amps_b[d2]
                    + Dv * amps_a[d1].conjugate() * amps_b[d2]
                    + Dv * amps_b[d1].conjugate() * amps_a[d2]
                )
        tr = sum(rho[(d, d)] for d in det_list).real
        if tr <= 1e-30:
            return math.nan
        for key in rho:
            rho[key] /= tr
        return sum(abs(v) ** 2 for v in rho.values()).real
    return _pur(D), _pur(1.0), _pur(0.0)


def run_joint(positions, adj, k_band, n_layers):
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    if len(layers) < 7:
        return None
    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None
    all_ys = [y for _, y in positions]
    cy = sum(all_ys) / len(all_ys)
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
    stop = min(len(layers), start + env_depth)
    mid = []
    for layer in layers[start:stop]:
        mid.extend(by_layer[layer])
    field_m = compute_field(positions, mass_nodes, 0.1)
    field_f = [0.0] * len(positions)
    gd, pmv, dv = [], [], []
    for k in k_band:
        am = propagate_full(positions, adj, field_m, src, k, blocked)
        af = propagate_full(positions, adj, field_f, src, k, blocked)
        pm = sum(abs(am[d]) ** 2 for d in det_list)
        pf = sum(abs(af[d]) ** 2 for d in det_list)
        if pm > 1e-30 and pf > 1e-30:
            ym = sum(abs(am[d]) ** 2 * positions[d][1] for d in det_list) / pm
            yf = sum(abs(af[d]) ** 2 * positions[d][1] for d in det_list) / pf
            gd.append(ym - yf)
        aa = propagate_full(positions, adj, field_m, src, k, blocked | set(sb))
        ab = propagate_full(positions, adj, field_m, src, k, blocked | set(sa))
        ba = bin_amplitudes(aa, positions, mid)
        bb = bin_amplitudes(ab, positions, mid)
        S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
        NA = sum(abs(a) ** 2 for a in ba)
        NB = sum(abs(b) ** 2 for b in bb)
        Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
        D_cl = math.exp(-LAM ** 2 * Sn)
        pc, pcoh, pmin = cl_purity_triple(aa, ab, D_cl, det_list)
        if not math.isnan(pc):
            pmv.append(pmin)
            dv.append(pcoh - pc)
    if not gd or not pmv:
        return None
    return {"grav": sum(gd)/len(gd), "pm": sum(pmv)/len(pmv), "dec": sum(dv)/len(dv)}


def measure_effective_gap(positions, adj, n_layers):
    """Measure the effective y-gap in post-barrier CONNECTED nodes."""
    by_layer = defaultdict(list)
    for idx, (x, y) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer.keys())
    barrier_layer = layers[len(layers) // 3]

    # Only count nodes that have at least one edge
    connected = set()
    for i, nbs in adj.items():
        if nbs:
            connected.add(i)
        for j in nbs:
            connected.add(j)

    post_ys = sorted(
        positions[i][1] for i in connected
        if positions[i][0] > barrier_layer and positions[i][0] < layers[-1]
    )
    if len(post_ys) < 2:
        return 0.0
    max_gap = max(post_ys[i] - post_ys[i-1] for i in range(1, len(post_ys)))
    return max_gap


def main():
    print("=" * 78)
    print("NODE-REMOVAL EMERGENCE: Prune Low-Distinguishability Nodes")
    print("  Build uniform DAG, remove confused nodes, test decoherence")
    print(f"  CL bath lambda={LAM}, k-band [3,5,7], 16 seeds")
    print("=" * 78)
    print()

    k_band = [3.0, 5.0, 7.0]
    n_seeds = 16

    # Part 1: Prune fraction sweep at N=25 and N=40
    print("PART 1: Pruning fraction sweep")
    print(f"  {'prune':>6s}  {'N':>3s}  {'eff_gap':>7s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'grav':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 54}")

    for prune in [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]:
        for nl in [25, 40]:
            grav_all, pm_all, dec_all, gap_all = [], [], [], []

            for seed in range(n_seeds):
                positions, adj, _ = generate_removal_dag(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 7 + 3,
                    prune_frac=prune,
                )
                gap_all.append(measure_effective_gap(positions, adj, nl))
                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            if grav_all:
                ag = sum(grav_all) / len(grav_all)
                apm = sum(pm_all) / len(pm_all)
                adec = sum(dec_all) / len(dec_all)
                agap = sum(gap_all) / len(gap_all)
                # Compare to baseline
                better = "*" if apm < 0.943 and nl == 40 else ""
                print(f"  {prune:6.2f}  {nl:3d}  {agap:7.2f}  {apm:8.4f}  "
                      f"{adec:+8.4f}  {ag:+8.3f}  {len(grav_all):4d}  {better}")
            else:
                print(f"  {prune:6.2f}  {nl:3d}  FAIL")

    print()
    print("  * = pur_min < 0.943 (better than uniform baseline at N=40)")
    print()

    # Part 2: Compare best removal with modular and uniform
    print("PART 2: Head-to-head comparison at N=25 and N=40 (16 seeds)")
    print(f"  {'family':>30s}  {'N':>3s}  {'gap':>5s}  {'pur_min':>8s}  "
          f"{'decoh':>8s}  {'grav':>8s}")
    print(f"  {'-' * 65}")

    for nl in [25, 40]:
        families = [
            ("Uniform (baseline)", lambda nl, s: generate_causal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=s * 7 + 3)),
            ("Modular gap=4", lambda nl, s: generate_modular_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=s * 7 + 3, gap=4.0)),
            ("Removal prune=0.15", lambda nl, s: generate_removal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=s * 7 + 3, prune_frac=0.15)),
            ("Removal prune=0.30", lambda nl, s: generate_removal_dag(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=s * 7 + 3, prune_frac=0.30)),
        ]

        for name, gen_fn in families:
            grav_all, pm_all, dec_all, gap_all = [], [], [], []
            for seed in range(n_seeds):
                positions, adj, _ = gen_fn(nl, seed)
                gap_all.append(measure_effective_gap(positions, adj, nl))
                r = run_joint(positions, adj, k_band, nl)
                if r:
                    grav_all.append(r["grav"])
                    pm_all.append(r["pm"])
                    dec_all.append(r["dec"])

            if grav_all:
                ag = sum(grav_all) / len(grav_all)
                apm = sum(pm_all) / len(pm_all)
                adec = sum(dec_all) / len(dec_all)
                agap = sum(gap_all) / len(gap_all)
                print(f"  {name:>30s}  {nl:3d}  {agap:5.2f}  {apm:8.4f}  "
                      f"{adec:+8.4f}  {ag:+8.3f}")

    print()
    print("KEY: Does node removal improve decoherence over uniform baseline?")
    print("If yes → 'the geometry prunes measurement-ambiguous events'")


if __name__ == "__main__":
    main()
