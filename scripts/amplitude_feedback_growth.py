#!/usr/bin/env python3
"""Amplitude-feedback growth: quantum-topology coupling for emergent channels.

The key insight from the dynamic emergence test: simple local growth rules
create probabilistic barriers that CLT erases. We need TOPOLOGICAL barriers.

Hypothesis: if the graph "knows" where amplitude goes, it can reinforce
existing channels. This is physically meaningful — it's the discrete
analogue of measurement back-reaction, where geometry records which-path
information.

RULE: After each layer grows, propagate amplitude from source through
the current graph. New nodes in the next layer preferentially connect
to parents that carry MORE amplitude. This creates positive feedback:
high-amplitude paths get more connections, strengthening their channels,
while low-amplitude paths (cross-channel) get fewer connections, creating
effective topological barriers.

The coupling parameter `feedback` controls strength:
  feedback=0: uniform random DAG (no feedback)
  feedback=1: moderate feedback (test this)
  feedback=3: strong feedback (channels should emerge clearly)

This is a co-evolution: the quantum state shapes the topology, which
shapes the quantum state. The fixed point (if it exists) is a graph
with emergent channel structure.
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
K_GROWTH = 5.0  # wavenumber used during growth-phase propagation


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


def _propagate_quick(positions, adj, n, src_indices):
    """Fast amplitude propagation for growth feedback.

    Simplified: no field, no directional measure, just 1/L attenuation.
    Returns |amplitude|^2 at each node.
    """
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src_indices:
        amps[s] = 1.0 / max(1, len(src_indices))

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        for j in adj.get(i, []):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            dx, dy = x2 - x1, y2 - y1
            L = math.sqrt(dx * dx + dy * dy)
            if L < 1e-10:
                continue
            ea = cmath.exp(1j * K_GROWTH * L) / L
            amps[j] += amps[i] * ea

    return [abs(a) ** 2 for a in amps]


def generate_feedback_dag(
    n_layers: int = 20,
    nodes_per_layer: int = 25,
    y_range: float = 12.0,
    connect_radius: float = 3.0,
    rng_seed: int = 42,
    feedback: float = 2.0,
) -> tuple[list[tuple[float, float]], dict[int, list[int]], list[float]]:
    """DAG with amplitude-feedback growth.

    After each layer, propagate amplitude from source.
    Next layer's connection probabilities are biased toward
    high-amplitude parents: P ~ |amp|^feedback (normalized).

    feedback=0: uniform random
    feedback>0: amplitude-reinforced connections
    """
    rng = __import__("random").Random(rng_seed)
    positions: list[tuple[float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    amp_sq: list[float] = []  # |amplitude|^2 at each node

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes = []

        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0))
            layer_nodes.append(idx)
            amp_sq.append(1.0)
        else:
            # First: create nodes at random positions
            new_indices = []
            for _ in range(nodes_per_layer):
                y = rng.uniform(-y_range, y_range)
                idx = len(positions)
                positions.append((x, y))
                layer_nodes.append(idx)
                new_indices.append(idx)
                amp_sq.append(0.0)  # placeholder

            # Connect with amplitude-feedback bias
            for idx in new_indices:
                y = positions[idx][1]
                candidates = []

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if dist <= connect_radius:
                            # Weight by parent's amplitude
                            a = amp_sq[prev_idx]
                            w = max(a, 1e-20) ** feedback if feedback > 0 else 1.0
                            candidates.append((prev_idx, w))

                if candidates:
                    # Normalize and accept
                    max_w = max(c[1] for c in candidates)
                    if max_w > 0:
                        for prev_idx, w in candidates:
                            p = w / max_w
                            # Ensure minimum connection probability
                            p = max(p, 0.05)
                            if rng.random() < p:
                                adj[prev_idx].append(idx)

            # Re-propagate to update amplitudes
            n = len(positions)
            src = layer_indices[0]
            amp_sq = _propagate_quick(positions, adj, n, src)

        layer_indices.append(layer_nodes)

    # Final arrival times
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


# ─── Decoherence machinery (same as other tests) ──────────────────

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
        "sa": sa, "sb": sb, "bl_idx": bl_idx,
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


def measure_connectivity_bias(positions, adj, setup):
    """Measure how biased connections are toward same-y-half.

    Returns fraction of post-barrier edges that stay in same y-half.
    1.0 = perfect channel separation, 0.5 = random.
    """
    cy = setup["cy"]
    bl_idx = setup["bl_idx"]
    layers = setup["layers"]
    by_layer = setup["by_layer"]

    same_half = 0
    total = 0
    for layer_key in layers[bl_idx + 1:]:
        for i in by_layer[layer_key]:
            yi = positions[i][1]
            for j in adj.get(i, []):
                yj = positions[j][1]
                if (yi - cy) * (yj - cy) > 0:
                    same_half += 1
                total += 1

    return same_half / total if total > 0 else 0.5


def main():
    from scripts.generative_causal_dag_interference import generate_causal_dag
    from scripts.topology_families import generate_modular_dag

    print("=" * 78)
    print("AMPLITUDE-FEEDBACK GROWTH: Quantum-Topology Coupling")
    print("  Does amplitude-biased connectivity create emergent channels?")
    print(f"  CL bath lambda={LAM}, 8 seeds per N")
    print("=" * 78)
    print()

    n_layers_list = [12, 18, 25, 40]
    k_band = [3.0, 5.0, 7.0]
    n_seeds = 8

    families = [
        ("Uniform (baseline)", generate_causal_dag, {}),
        ("Modular gap=4 (target)", generate_modular_dag, {"gap": 4.0}),
        ("Feedback f=0.5", generate_feedback_dag, {"feedback": 0.5}),
        ("Feedback f=1.0", generate_feedback_dag, {"feedback": 1.0}),
        ("Feedback f=2.0", generate_feedback_dag, {"feedback": 2.0}),
        ("Feedback f=3.0", generate_feedback_dag, {"feedback": 3.0}),
        ("Feedback f=5.0", generate_feedback_dag, {"feedback": 5.0}),
    ]

    for name, gen, kwargs in families:
        t0 = time.time()

        print(f"  [{name}]")
        print(f"  {'N':>4s}  {'pur_min':>8s}  {'decoh':>8s}  {'bias':>6s}  {'n_ok':>4s}")
        print(f"  {'-' * 38}")

        for nl in n_layers_list:
            pm_all, pc_all, pcoh_all, bias_all = [], [], [], []

            for seed in range(n_seeds):
                positions, adj, _ = gen(
                    n_layers=nl, nodes_per_layer=25, y_range=12.0,
                    connect_radius=3.0, rng_seed=seed * 13 + 5, **kwargs,
                )
                setup = build_setup(positions, adj, env_depth_layers=max(1, round(nl / 6)))
                if setup is None:
                    continue

                bias = measure_connectivity_bias(positions, adj, setup)
                bias_all.append(bias)

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
                    amps_a = propagate_full(positions, adj, field, src, k, blocked | set(sb))
                    amps_b = propagate_full(positions, adj, field, src, k, blocked | set(sa))

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
                avg_bias = sum(bias_all) / len(bias_all) if bias_all else 0.5
                decoh = avg_pcoh - avg_pc
                print(f"  {nl:4d}  {avg_pm:8.4f}  {decoh:+8.4f}  "
                      f"{avg_bias:6.3f}  {len(pm_all):4d}")
            else:
                print(f"  {nl:4d}  FAIL")

        dt = time.time() - t0
        print(f"  ({dt:.0f}s)\n")

    # Summary
    print("=" * 78)
    print("KEY QUESTION: Does feedback create same-half bias > 0.6?")
    print("If yes → emergent channel structure from quantum state")
    print("If no → amplitude feedback alone is insufficient")


if __name__ == "__main__":
    main()
