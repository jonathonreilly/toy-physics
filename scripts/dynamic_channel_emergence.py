#!/usr/bin/env python3
"""Dynamic channel emergence: can evolving graph rules produce modular structure?

The modular DAG's channel separation is imposed by hand (y-gap).
Can a local growth rule generate equivalent structure dynamically?

Three candidate rules:

Rule 1: LOCALITY BIAS
  Connection probability decays with y-distance: P ~ exp(-|dy|/sigma).
  Small sigma = strong locality = channels form naturally from spatial
  clustering. Large sigma = uniform random (baseline).

Rule 2: REINFORCEMENT
  Nodes prefer connecting to parents that already have high degree.
  This is preferential attachment but spatially localized.
  Creates hub-channel structures where hubs in different y-regions
  attract different slit paths.

Rule 3: REPULSIVE GROWTH
  New nodes are placed preferentially AWAY from existing nearby nodes
  (anti-clustering). This pushes nodes into two bands naturally.
  Combined with locality bias, creates emergent gap.

Metric: measure the effective "channel separation" of each generated
graph using the y-distribution of post-barrier amplitude, then run
CL bath decoherence.

If any rule produces pur_min < 0.95 at N=25 WITHOUT an imposed gap,
the channel structure is emergent.
"""

from __future__ import annotations
import math
import cmath
import sys
import os
import time
from collections import defaultdict, deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


# ─── Rule 1: Locality Bias ─────────────────────────────────────────

def generate_locality_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    sigma: float = 2.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """DAG with locality-biased connections.

    P(connect i->j) = exp(-|y_i - y_j| / sigma) if within connect_radius.
    sigma controls locality strength:
      sigma=inf: uniform random (all within radius connect)
      sigma=2.0: moderate locality (nearby y preferred)
      sigma=0.5: strong locality (almost no cross-y connections)
    """
    rng = __import__("random").Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            # Locality bias
                            dy = abs(y - py)
                            p = math.exp(-dy / sigma)
                            if rng.random() < p:
                                adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    arrival = _make_arrival(positions, dict(adj))
    return positions, dict(adj), arrival


# ─── Rule 2: Reinforcement (spatial preferential attachment) ────────

def generate_reinforcement_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    sigma: float = 2.0,
    degree_boost: float = 2.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """DAG with locality + degree reinforcement.

    P(connect) = exp(-|dy|/sigma) * (1 + degree_boost * out_degree(parent))
    normalized within connect_radius candidates.
    """
    rng = __import__("random").Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    out_degree: dict[int, int] = defaultdict(int)
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
        else:
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)

                candidates = []
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            dy = abs(y - py)
                            w = math.exp(-dy / sigma) * (1 + degree_boost * out_degree[prev_idx])
                            candidates.append((prev_idx, w))

                if candidates:
                    max_w = max(c[1] for c in candidates)
                    for prev_idx, w in candidates:
                        if rng.random() < w / max_w:
                            adj[prev_idx].append(idx)
                            out_degree[prev_idx] += 1

        layer_indices.append(layer_nodes)

    arrival = _make_arrival(positions, dict(adj))
    return positions, dict(adj), arrival


# ─── Rule 3: Repulsive placement + locality ─────────────────────────

def generate_repulsive_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    sigma: float = 2.0,
    repulsion: float = 3.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """DAG with repulsive node placement + locality-biased edges.

    New nodes are placed at y-positions that repel from existing same-layer
    nodes, creating natural clustering/gap structure.
    Edges use locality bias (exp(-|dy|/sigma)).

    For each node, sample n_candidates y-positions and pick the one
    maximizing minimum distance to existing nodes in this layer.
    """
    rng = __import__("random").Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    n_candidates = 5  # Poisson disc-like sampling

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []
        layer_ys: list[float] = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
            layer_ys.append(0.0)
        else:
            for _ in range(nodes_per_layer):
                # Repulsive placement: pick best of n_candidates
                best_y = rng.uniform(-y_range, y_range)
                best_min_dist = 0.0

                if layer_ys and repulsion > 0:
                    for _ in range(n_candidates):
                        cand_y = rng.uniform(-y_range, y_range)
                        min_dist = min(abs(cand_y - ey) for ey in layer_ys)
                        if min_dist > best_min_dist:
                            best_min_dist = min_dist
                            best_y = cand_y

                y = best_y
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)
                layer_ys.append(y)

                # Locality-biased edges
                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            dy = abs(y - py)
                            p = math.exp(-dy / sigma)
                            if rng.random() < p:
                                adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    arrival = _make_arrival(positions, dict(adj))
    return positions, dict(adj), arrival


def _make_arrival(positions, adj):
    n = len(positions)
    arrival = [float("inf")] * n
    for i in range(n):
        if positions[i][0] == 0.0:
            arrival[i] = 0.0
    order = sorted(range(n), key=lambda i: (positions[i][0], i))
    for i in order:
        if not math.isfinite(arrival[i]):
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            cand = arrival[i] + dist
            if cand < arrival[j]:
                arrival[j] = cand
    return arrival


# ─── Shared decoherence machinery ──────────────────────────────────

def compute_field(positions, adj, mass_nodes):
    n = len(positions)
    field = [0.0] * n
    for m in mass_nodes:
        mx, my = positions[m]
        for i in range(n):
            ix, iy = positions[i]
            r = math.sqrt((ix - mx) ** 2 + (iy - my) ** 2) + 0.1
            field[i] += 0.1 / r
    return field


def propagate(positions, adj, field, src, k, blocked=None):
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


def build_setup(positions, adj, env_depth_layers=1):
    n = len(positions)
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
    bl = layers[bl_idx]
    bi = by_layer[bl]
    sa = [i for i in bi if positions[i][1] > cy + 3][:3]
    sb = [i for i in bi if positions[i][1] < cy - 3][:3]
    if not sa or not sb:
        return None
    blocked = set(bi) - set(sa + sb)
    start = bl_idx + 1
    stop = min(len(layers), start + max(1, env_depth_layers))
    mass_nodes = []
    for layer in layers[start:stop]:
        mass_nodes.extend(i for i in by_layer[layer] if abs(positions[i][1] - cy) <= 3.0)
    if len(mass_nodes) < 2:
        return None
    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1]
    field = compute_field(positions, adj, list(set(mass_nodes) | set(grav_mass)))
    return {
        "by_layer": by_layer, "layers": layers, "src": src,
        "det_list": det_list, "cy": cy, "blocked": blocked, "field": field,
        "sa": [i for i in bi if positions[i][1] > cy + 3][:3],
        "sb": [i for i in bi if positions[i][1] < cy - 3][:3],
        "bl_idx": bl_idx,
    }


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


def measure_channel_separation(positions, adj, setup):
    """Measure effective channel separation of a graph.

    Propagate from each slit independently, measure y-distribution
    overlap at detectors. Low overlap = good channel separation.
    """
    blocked = setup["blocked"]
    field = setup["field"]
    src = setup["src"]
    det_list = setup["det_list"]
    sa = setup["sa"]
    sb = setup["sb"]

    amps_a = propagate(positions, adj, field, src, 5.0, blocked | set(sb))
    amps_b = propagate(positions, adj, field, src, 5.0, blocked | set(sa))

    # y-distribution at detectors for each slit
    ya = [positions[d][1] for d in det_list if abs(amps_a[d]) > 1e-20]
    yb = [positions[d][1] for d in det_list if abs(amps_b[d]) > 1e-20]

    if not ya or not yb:
        return 0.0

    mean_a = sum(ya) / len(ya)
    mean_b = sum(yb) / len(yb)

    return abs(mean_a - mean_b)


def run_family(name, generator, n_layers_list, n_seeds=8, **gen_kwargs):
    """Run decoherence test for one dynamical rule."""
    k_band = [3.0, 5.0, 7.0]
    results = {}

    for nl in n_layers_list:
        pm_all, pc_all, pcoh_all, sep_all = [], [], [], []

        for seed in range(n_seeds):
            positions, adj, _ = generator(
                n_layers=nl, nodes_per_layer=25, y_range=12.0,
                connect_radius=3.0, rng_seed=seed * 13 + 5, **gen_kwargs,
            )
            setup = build_setup(positions, adj, env_depth_layers=max(1, round(nl / 6)))
            if setup is None:
                continue

            # Channel separation diagnostic
            sep = measure_channel_separation(positions, adj, setup)
            sep_all.append(sep)

            blocked = setup["blocked"]
            field = setup["field"]
            src = setup["src"]
            det_list = setup["det_list"]
            by_layer = setup["by_layer"]
            layers = setup["layers"]
            bl_idx = setup["bl_idx"]
            sa = setup["sa"]
            sb = setup["sb"]

            pm_k, pc_k, pcoh_k = [], [], []
            for k in k_band:
                amps_a = propagate(positions, adj, field, src, k, blocked | set(sb))
                amps_b = propagate(positions, adj, field, src, k, blocked | set(sa))

                start = bl_idx + 1
                stop = min(len(layers), start + max(1, round(nl / 6)))
                mid = []
                for layer in layers[start:stop]:
                    mid.extend(by_layer[layer])

                ba = bin_amplitudes(amps_a, positions, mid)
                bb = bin_amplitudes(amps_b, positions, mid)
                S = sum(abs(a - b) ** 2 for a, b in zip(ba, bb))
                NA = sum(abs(a) ** 2 for a in ba)
                NB = sum(abs(b) ** 2 for b in bb)
                Sn = S / (NA + NB) if (NA + NB) > 0 else 0.0
                D = math.exp(-LAM ** 2 * Sn)

                pc, pcoh, pmin = cl_purity_triple(amps_a, amps_b, D, det_list)
                if not math.isnan(pc):
                    pm_k.append(pmin)
                    pc_k.append(pc)
                    pcoh_k.append(pcoh)

            if pm_k:
                pm_all.append(sum(pm_k) / len(pm_k))
                pc_all.append(sum(pc_k) / len(pc_k))
                pcoh_all.append(sum(pcoh_k) / len(pcoh_k))

        if pm_all:
            avg_pm = sum(pm_all) / len(pm_all)
            avg_pc = sum(pc_all) / len(pc_all)
            avg_pcoh = sum(pcoh_all) / len(pcoh_all)
            avg_sep = sum(sep_all) / len(sep_all) if sep_all else 0.0
            results[nl] = {
                "pm": avg_pm, "decoh": avg_pcoh - avg_pc,
                "sep": avg_sep, "n_ok": len(pm_all),
            }

    return results


def main():
    from scripts.generative_causal_dag_interference import generate_causal_dag
    from scripts.topology_families import generate_modular_dag

    print("=" * 78)
    print("DYNAMIC CHANNEL EMERGENCE TEST")
    print("  Can evolving graph rules produce channel separation without imposed gap?")
    print(f"  CL bath lambda={LAM}, 8 seeds per N")
    print("=" * 78)
    print()

    n_layers_list = [12, 18, 25, 40]

    families = [
        ("Uniform (baseline)", generate_causal_dag, {}),
        ("Modular gap=4 (reference)", generate_modular_dag, {"gap": 4.0}),
        ("Locality sigma=1.0", generate_locality_dag, {"sigma": 1.0}),
        ("Locality sigma=1.5", generate_locality_dag, {"sigma": 1.5}),
        ("Locality sigma=2.0", generate_locality_dag, {"sigma": 2.0}),
        ("Reinforcement s=1.5 d=2", generate_reinforcement_dag,
         {"sigma": 1.5, "degree_boost": 2.0}),
        ("Reinforcement s=1.0 d=3", generate_reinforcement_dag,
         {"sigma": 1.0, "degree_boost": 3.0}),
        ("Repulsive s=1.5 r=3", generate_repulsive_dag,
         {"sigma": 1.5, "repulsion": 3.0}),
    ]

    all_results = {}

    for name, gen, kwargs in families:
        t0 = time.time()
        results = run_family(name, gen, n_layers_list, **kwargs)
        dt = time.time() - t0
        all_results[name] = results

        print(f"  [{name}]  ({dt:.0f}s)")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'decoh':>8s}  {'sep':>6s}  {'n_ok':>4s}")
        print(f"  {'-' * 38}")
        for nl in n_layers_list:
            if nl in results:
                r = results[nl]
                print(f"  {nl:4d}  {r['pm']:8.4f}  {r['decoh']:+8.4f}  "
                      f"{r['sep']:6.2f}  {r['n_ok']:4d}")
            else:
                print(f"  {nl:4d}  FAIL")
        print()

    # Summary
    print("=" * 78)
    print("SUMMARY: pur_min at N=25 (threshold: < 0.95 = emergent channel separation)")
    print(f"  {'Family':<30s}  {'pur_min':>8s}  {'sep':>6s}  {'verdict':>10s}")
    print(f"  {'-' * 60}")

    for name in all_results:
        r = all_results[name]
        if 25 in r:
            pm = r[25]["pm"]
            sep = r[25]["sep"]
            if pm < 0.95:
                verdict = "EMERGENT"
            elif pm < 0.97:
                verdict = "MARGINAL"
            else:
                verdict = "FAIL"
            print(f"  {name:<30s}  {pm:8.4f}  {sep:6.2f}  {verdict:>10s}")
        else:
            print(f"  {name:<30s}  {'N/A':>8s}")

    print()
    print("EMERGENT = pur_min < 0.95 at N=25 WITHOUT imposed gap")
    print("This would mean channel structure arises from the growth rule alone")


if __name__ == "__main__":
    main()
