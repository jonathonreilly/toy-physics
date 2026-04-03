#!/usr/bin/env python3
"""Dynamical topology: graph evolves in response to amplitude flow.

The ceiling theorem says: on FIXED connected DAGs, the transfer matrix
product converges to rank-1. The only way to break this is to change
the transfer matrices themselves — i.e., change the graph.

Approach: propagate, measure per-edge amplitude traffic, prune low-traffic
edges (they don't carry the quantum state), reinforce high-traffic edges.
Re-propagate on modified graph. Iterate.

The hypothesis: amplitude-driven topology evolution creates channel
separation naturally. High-traffic edges form persistent channels.
Low-traffic cross-channel edges get pruned. The result is an emergent
gap-like structure.

Key difference from prior emergence attempts (9 failures):
- Those tried to generate topology from LOCAL rules during construction
- This modifies an existing graph based on GLOBAL amplitude information
- The amplitude already "knows" where the channels are — we just reinforce

Four variants:
  V1: Edge pruning only (remove low-traffic)
  V2: Edge weight reinforcement (multiply high-traffic edge weights)
  V3: Combined prune + reinforce
  V4: Separate-slit pruning (prune based on which slit contributes more
      traffic — creates explicit channel separation)

Measurement: d_TV and pur_min at single-k after T iterations.
Also: cross-channel edge fraction to verify gap emergence.
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
NPL = 30
XYZ_RANGE = 12.0
CONNECT_RADIUS = 4.0
T_STEPS = 10
PRUNE_FRAC = 0.3  # Remove bottom 30% of edges by traffic


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


def generate_3d_dag(n_layers, npl, xyz_range, connect_radius, rng_seed):
    rng = random.Random(rng_seed)
    positions = []
    adj = defaultdict(list)
    layer_indices = []
    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions)-1)
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
                        dist = math.sqrt((x-px)**2 + (y-py)**2 + (z-pz)**2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)
    return positions, dict(adj), n_layers // 3


def propagate_weighted(positions, adj, field, src, k, blocked, edge_weights=None):
    """Propagate with optional per-edge weights."""
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    traffic = {}  # (i,j) -> |amp_i * kernel|
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
            ew = edge_weights.get((i, j), 1.0) if edge_weights else 1.0
            contrib = amps[i] * ea * ew
            amps[j] += contrib
            traffic[(i, j)] = abs(contrib)
    return amps, traffic


def prune_edges(adj, traffic, prune_fraction, protected_nodes):
    """Remove bottom prune_fraction of edges by traffic."""
    all_edges = [(i, j, traffic.get((i, j), 0)) for i in adj for j in adj[i]]
    if not all_edges:
        return adj
    # Sort by traffic
    all_edges.sort(key=lambda x: x[2])
    n_prune = int(len(all_edges) * prune_fraction)
    prune_set = set()
    for i, j, t in all_edges[:n_prune]:
        # Don't prune edges to/from protected nodes
        if i not in protected_nodes and j not in protected_nodes:
            prune_set.add((i, j))

    new_adj = {}
    for i, nbs in adj.items():
        new_nbs = [j for j in nbs if (i, j) not in prune_set]
        if new_nbs:
            new_adj[i] = new_nbs
    return new_adj


def reinforce_edges(traffic, alpha=0.5):
    """Create edge weights that reinforce high-traffic edges."""
    if not traffic:
        return {}
    max_t = max(traffic.values())
    if max_t < 1e-30:
        return {}
    return {(i, j): 1.0 + alpha * t / max_t for (i, j), t in traffic.items()}


def compute_cross_channel_fraction(adj, positions, barrier_layer):
    """Fraction of post-barrier edges that cross y=0."""
    n_cross = 0
    n_total = 0
    for i, nbs in adj.items():
        if positions[i][0] <= barrier_layer:
            continue
        for j in nbs:
            if positions[j][0] <= barrier_layer:
                continue
            n_total += 1
            if positions[i][1] * positions[j][1] < 0:
                n_cross += 1
    return n_cross / max(1, n_total)


def check_connected(adj, src, det_nodes, n):
    visited = set()
    queue = deque(src)
    for s in src:
        visited.add(s)
    while queue:
        node = queue.popleft()
        for nb in adj.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return all(d in visited for d in det_nodes)


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


def measure_dtv_pur(positions, adj, src, det_nodes, blocked, sa, sb, field, k,
                     edge_weights=None):
    """Measure d_TV and pur_min at single k."""
    psi_a, _ = propagate_weighted(positions, adj, field, src, k,
                                   blocked | set(sb), edge_weights)
    psi_b, _ = propagate_weighted(positions, adj, field, src, k,
                                   blocked | set(sa), edge_weights)
    pa = {d: abs(psi_a[d])**2 for d in det_nodes}
    pb = {d: abs(psi_b[d])**2 for d in det_nodes}
    na = sum(pa.values())
    nb = sum(pb.values())
    if na < 1e-30 or nb < 1e-30:
        return float('nan'), float('nan')
    dtv = 0.5 * sum(abs(pa[d]/na - pb[d]/nb) for d in det_nodes)
    total = sum(pa[d] + pb[d] for d in det_nodes)
    pur = sum((pa[d] + pb[d])**2 for d in det_nodes) / total**2
    return dtv, 1 - pur


def _mean_se(vals):
    vals = [v for v in vals if not math.isnan(v)]
    if not vals: return float('nan'), float('nan')
    m = sum(vals) / len(vals)
    if len(vals) < 2: return m, 0.0
    var = sum((v-m)**2 for v in vals) / (len(vals)-1)
    return m, math.sqrt(var / len(vals))


def main():
    print("=" * 100)
    print("DYNAMICAL TOPOLOGY: AMPLITUDE-DRIVEN GRAPH EVOLUTION")
    print(f"  k={K}, {N_SEEDS} seeds, T={T_STEPS} iterations, prune_frac={PRUNE_FRAC}")
    print("=" * 100)
    print()

    seeds = [s * 7 + 3 for s in range(N_SEEDS)]

    for nl in [25, 40]:
        print(f"  N_LAYERS = {nl}")
        print(f"  {'variant':>14s}  {'d_TV':>8s}  {'1-pur':>8s}  {'cross%':>7s}  "
              f"{'edges':>7s}  {'ok':>3s}  {'time':>5s}")
        print(f"  {'-' * 62}")

        variants = [
            ("baseline", "none"),
            ("V1-prune", "prune"),
            ("V2-reinforce", "reinforce"),
            ("V3-combined", "combined"),
            ("V4-slit-prune", "slit_prune"),
        ]

        for label, variant in variants:
            t0 = time.time()
            dtv_all, pur_all, cross_all, edge_all = [], [], [], []

            for seed in seeds:
                pos, adj, bl = generate_3d_dag(nl, NPL, XYZ_RANGE, CONNECT_RADIUS, seed)
                n = len(pos)
                by_layer = defaultdict(list)
                for idx, (x, y, z) in enumerate(pos):
                    by_layer[round(x)].append(idx)
                layers = sorted(by_layer.keys())
                if len(layers) < 7: continue
                src = by_layer[layers[0]]
                det_nodes = by_layer[layers[-1]]
                if not det_nodes: continue
                cy = sum(pos[i][1] for i in range(n)) / n
                bl_idx = len(layers) // 3
                bi = by_layer[layers[bl_idx]]
                sa = [i for i in bi if pos[i][1] > cy + 3][:3]
                sb = [i for i in bi if pos[i][1] < cy - 3][:3]
                if not sa or not sb: continue
                blocked = set(bi) - set(sa + sb)
                grav_layer = layers[2 * len(layers) // 3]
                mass_nodes = [i for i in by_layer[grav_layer] if pos[i][1] > cy + 1]
                if not mass_nodes: continue

                field = compute_field_3d(pos, mass_nodes)
                protected = set(src) | set(det_nodes) | set(sa + sb)
                edge_weights = None

                if variant == "none":
                    # Baseline — no evolution
                    pass
                else:
                    # Iterate topology evolution
                    for t in range(T_STEPS):
                        # Propagate both-slits-open
                        _, traffic = propagate_weighted(pos, adj, field, src, K, blocked, edge_weights)

                        if variant == "prune":
                            adj = prune_edges(adj, traffic, PRUNE_FRAC / T_STEPS, protected)
                        elif variant == "reinforce":
                            edge_weights = reinforce_edges(traffic, alpha=0.5)
                        elif variant == "combined":
                            adj = prune_edges(adj, traffic, PRUNE_FRAC / T_STEPS, protected)
                            edge_weights = reinforce_edges(traffic, alpha=0.5)
                        elif variant == "slit_prune":
                            # Propagate each slit separately, prune edges that
                            # serve both slits equally (low slit-specificity)
                            _, traf_a = propagate_weighted(pos, adj, field, src, K,
                                                           blocked | set(sb), edge_weights)
                            _, traf_b = propagate_weighted(pos, adj, field, src, K,
                                                           blocked | set(sa), edge_weights)
                            # Slit-specificity: |traf_a - traf_b| / (traf_a + traf_b)
                            slit_spec = {}
                            for edge in set(list(traf_a.keys()) + list(traf_b.keys())):
                                ta = traf_a.get(edge, 0)
                                tb = traf_b.get(edge, 0)
                                total = ta + tb
                                slit_spec[edge] = abs(ta - tb) / total if total > 0 else 0

                            # Remove low-specificity edges (serve both slits equally)
                            all_edges = [(i, j, slit_spec.get((i, j), 0))
                                         for i in adj for j in adj[i]]
                            all_edges.sort(key=lambda x: x[2])
                            n_prune = int(len(all_edges) * PRUNE_FRAC / T_STEPS)
                            prune_set = set()
                            for i, j, s in all_edges[:n_prune]:
                                if i not in protected and j not in protected:
                                    prune_set.add((i, j))
                            new_adj = {}
                            for i, nbs in adj.items():
                                new_nbs = [j for j in nbs if (i, j) not in prune_set]
                                if new_nbs: new_adj[i] = new_nbs
                            adj = new_adj

                        # Check connectivity
                        if not check_connected(adj, src, det_nodes, n):
                            break

                # Measure on final graph
                dtv, omp = measure_dtv_pur(pos, adj, src, det_nodes, blocked,
                                           sa, sb, field, K, edge_weights)
                if not math.isnan(dtv):
                    dtv_all.append(dtv)
                    pur_all.append(omp)
                    cross_all.append(compute_cross_channel_fraction(adj, pos, bl))
                    edge_all.append(sum(len(v) for v in adj.values()))

            dt = time.time() - t0
            if dtv_all:
                mdtv, _ = _mean_se(dtv_all)
                mpur, _ = _mean_se(pur_all)
                mcross = sum(cross_all) / len(cross_all)
                medge = sum(edge_all) / len(edge_all)
                print(f"  {label:>14s}  {mdtv:8.4f}  {mpur:8.4f}  {mcross:6.1%}  "
                      f"{medge:7.0f}  {len(dtv_all):3d}  {dt:4.0f}s")
            else:
                print(f"  {label:>14s}  FAIL  {dt:4.0f}s")

        print()

    print("KEY:")
    print("  d_TV higher = more slit distinguishability")
    print("  1-pur higher = more decoherence headroom")
    print("  cross% lower = more channel separation (gap-like)")
    print("  If V4 (slit-prune) creates low cross% AND high d_TV:")
    print("    → Amplitude-driven gap emergence confirmed")


if __name__ == "__main__":
    main()
