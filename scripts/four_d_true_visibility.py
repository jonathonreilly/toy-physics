#!/usr/bin/env python3
"""4D true single-vs-double-slit visibility on the retained modular lane.

This is the disciplined visibility check for the 4D causal DAG family:
it compares the coherent two-slit detector profile against the
single-slit average profile, rather than a proxy contrast computed from
the both-slits-open distribution alone.

The lane is the same 4D modular family used by the gravity/decoherence
work: x is the causal layer, y is the slit/channel axis, and z/w are
free transverse coordinates.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from collections import defaultdict, deque

BETA = 0.8
K_BAND = [3.0, 5.0, 7.0]


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
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


def generate_4d_modular_dag(
    n_layers: int = 15,
    nodes_per_layer: int = 30,
    spatial_range: float = 8.0,
    connect_radius: float = 4.5,
    rng_seed: int = 42,
    gap: float = 5.0,
    crosslink_prob: float = 0.02,
) -> tuple[list[tuple[float, float, float, float]], dict[int, list[int]], list[list[int]]]:
    """Generate a 4D modular DAG with a y-channel gap after the barrier."""
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            idx = len(positions)
            positions.append((x, 0.0, 0.0, 0.0))
            layer_nodes.append(idx)
        else:
            for node_i in range(nodes_per_layer):
                z = rng.uniform(-spatial_range, spatial_range)
                w = rng.uniform(-spatial_range, spatial_range)
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, spatial_range)
                    else:
                        y = rng.uniform(-spatial_range, -gap / 2)
                else:
                    y = rng.uniform(-spatial_range, spatial_range)

                idx = len(positions)
                positions.append((x, y, z, w))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2):]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 + (w - pw) ** 2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_ch = (y * py > 0)
                            if same_ch:
                                if dist <= connect_radius:
                                    adj[prev_idx].append(idx)
                            else:
                                if dist <= 2 * connect_radius and rng.random() < crosslink_prob:
                                    adj[prev_idx].append(idx)
                        elif dist <= connect_radius:
                            adj[prev_idx].append(idx)

        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def compute_field_4d(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    mass_idx: list[int],
    iterations: int = 50,
) -> list[float]:
    n = len(positions)
    undirected = defaultdict(set)
    for i, nbs in adj.items():
        for j in nbs:
            undirected[i].add(j)
            undirected[j].add(i)
    mass_set = set(mass_idx)
    field = [1.0 if i in mass_set else 0.0 for i in range(n)]
    for _ in range(iterations):
        next_field = [0.0] * n
        for i in range(n):
            if i in mass_set:
                next_field[i] = 1.0
            elif undirected.get(i):
                next_field[i] = sum(field[j] for j in undirected[i]) / len(undirected[i])
        field = next_field
    return field


def propagate_4d(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    field: list[float],
    src: list[int],
    k: float,
    blocked: set[int] | None = None,
) -> list[complex]:
    n = len(positions)
    blocked = blocked or set()
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)
    for i in order:
        if abs(amps[i]) < 1e-30 or i in blocked:
            continue
        x1, y1, z1, w1 = positions[i]
        for j in adj.get(i, []):
            if j in blocked:
                continue
            x2, y2, z2, w2 = positions[j]
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            dw = w2 - w1
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L < 1e-10:
                continue
            theta = math.acos(min(max(dx / L, -1), 1))
            weight = math.exp(-BETA * theta * theta)
            lf = 0.5 * (field[i] + field[j])
            dl = L * (1 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * cmath.exp(1j * k * act) * weight / L
    return amps


def _detector_probs(amps: list[complex], det_list: list[int]) -> dict[int, float]:
    probs = {d: abs(amps[d]) ** 2 for d in det_list}
    total = sum(probs.values())
    if total > 0:
        probs = {d: p / total for d, p in probs.items()}
    return probs


def _detector_profile(probs: dict[int, float], positions, det_list: list[int]) -> list[float]:
    by_y = defaultdict(float)
    for d in det_list:
        by_y[positions[d][1]] += probs.get(d, 0.0)
    return [by_y[y] for y in sorted(by_y)]


def _profile_visibility(profile: list[float]) -> float:
    if len(profile) < 3:
        return 0.0
    peaks = [
        profile[i]
        for i in range(1, len(profile) - 1)
        if profile[i] > profile[i - 1] and profile[i] > profile[i + 1]
    ]
    troughs = [
        profile[i]
        for i in range(1, len(profile) - 1)
        if profile[i] < profile[i - 1] and profile[i] < profile[i + 1]
    ]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def build_setup(positions, adj, n_layers: int):
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    layers = sorted(by_layer)
    if len(layers) < 7:
        return None

    src = by_layer[layers[0]]
    det_list = list(by_layer[layers[-1]])
    if not det_list:
        return None

    all_ys = [pos[1] for pos in positions]
    cy = sum(all_ys) / len(all_ys)
    bl_idx = len(layers) // 3
    barrier = by_layer[layers[bl_idx]]

    slit_a = [i for i in barrier if positions[i][1] > cy + 3][:5]
    slit_b = [i for i in barrier if positions[i][1] < cy - 3][:5]
    if not slit_a or not slit_b:
        return None

    blocked = set(barrier) - set(slit_a + slit_b)

    grav_layer = layers[2 * len(layers) // 3]
    grav_mass = [i for i in by_layer[grav_layer] if positions[i][1] > cy + 1][:8]
    if not grav_mass:
        return None
    field = compute_field_4d(positions, adj, grav_mass)

    return {
        "by_layer": by_layer,
        "layers": layers,
        "src": src,
        "det_list": det_list,
        "cy": cy,
        "bl_idx": bl_idx,
        "barrier": barrier,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "blocked": blocked,
        "field": field,
    }


def interference_visibility_4d(positions, adj, field, src, det_list, blocked_both, slit_a, slit_b):
    k = 5.0
    amps_both = propagate_4d(positions, adj, field, src, k, blocked_both)
    amps_a = propagate_4d(positions, adj, field, src, k, blocked_both | set(slit_b))
    amps_b = propagate_4d(positions, adj, field, src, k, blocked_both | set(slit_a))

    probs_both = _detector_probs(amps_both, det_list)
    probs_a = _detector_probs(amps_a, det_list)
    probs_b = _detector_probs(amps_b, det_list)
    probs_single_avg = {
        d: 0.5 * probs_a.get(d, 0.0) + 0.5 * probs_b.get(d, 0.0)
        for d in det_list
    }

    coh_profile = _detector_profile(probs_both, positions, det_list)
    single_profile = _detector_profile(probs_single_avg, positions, det_list)
    vis_coh = _profile_visibility(coh_profile)
    vis_single = _profile_visibility(single_profile)
    vis_gain = vis_coh - vis_single
    return vis_coh, vis_single, vis_gain


def main():
    print("=" * 78)
    print("4D TRUE VISIBILITY: Modular DAGs")
    print("  True single-vs-double-slit metric on the retained 4D modular lane")
    print("  Coherent profile vs single-slit average, same propagator")
    print("=" * 78)
    print()

    n_layers_list = [12, 18, 25, 40, 60, 80, 100]
    gaps = [3.0, 5.0]
    n_seeds = 8

    print(f"  {'gap':>4s}  {'N':>4s}  {'V_coh':>7s}  {'V_sng':>7s}  {'V_gain':>8s}  {'n_ok':>4s}")
    print(f"  {'-' * 48}")

    for gap in gaps:
        for nl in n_layers_list:
            vis_coh_vals = []
            vis_single_vals = []
            vis_gain_vals = []
            n_ok = 0
            t0 = time.time()

            for seed in range(n_seeds):
                positions, adj, layer_indices = generate_4d_modular_dag(
                    n_layers=nl,
                    nodes_per_layer=25,
                    spatial_range=8.0,
                    connect_radius=4.5,
                    rng_seed=seed * 13 + 5,
                    gap=gap,
                )
                setup = build_setup(positions, adj, nl)
                if setup is None:
                    continue

                field = setup["field"]
                src = setup["src"]
                det_list = setup["det_list"]
                blocked = setup["blocked"]
                slit_a = setup["slit_a"]
                slit_b = setup["slit_b"]

                seed_coh = []
                seed_single = []
                seed_gain = []
                for k in K_BAND:
                    amps_both = propagate_4d(positions, adj, field, src, k, blocked)
                    amps_a = propagate_4d(positions, adj, field, src, k, blocked | set(slit_b))
                    amps_b = propagate_4d(positions, adj, field, src, k, blocked | set(slit_a))

                    probs_both = _detector_probs(amps_both, det_list)
                    probs_a = _detector_probs(amps_a, det_list)
                    probs_b = _detector_probs(amps_b, det_list)
                    probs_single_avg = {
                        d: 0.5 * probs_a.get(d, 0.0) + 0.5 * probs_b.get(d, 0.0)
                        for d in det_list
                    }
                    coh_profile = _detector_profile(probs_both, positions, det_list)
                    single_profile = _detector_profile(probs_single_avg, positions, det_list)
                    vis_coh = _profile_visibility(coh_profile)
                    vis_single = _profile_visibility(single_profile)
                    seed_coh.append(vis_coh)
                    seed_single.append(vis_single)
                    seed_gain.append(vis_coh - vis_single)

                if seed_coh:
                    n_ok += 1
                    vis_coh_vals.append(sum(seed_coh) / len(seed_coh))
                    vis_single_vals.append(sum(seed_single) / len(seed_single))
                    vis_gain_vals.append(sum(seed_gain) / len(seed_gain))

            if n_ok:
                avg_coh = sum(vis_coh_vals) / len(vis_coh_vals)
                avg_single = sum(vis_single_vals) / len(vis_single_vals)
                avg_gain = sum(vis_gain_vals) / len(vis_gain_vals)
                status = "PASS" if avg_gain > 0.02 else "WEAK" if avg_gain > 0 else "NONE"
                dt = time.time() - t0
                print(f"  {gap:4.1f}  {nl:4d}  {avg_coh:7.3f}  {avg_single:7.3f}  {avg_gain:+8.3f}  {n_ok:4d}  {status}")
            else:
                print(f"  {gap:4.1f}  {nl:4d}  FAIL")

    print()
    print("INTERPRETATION")
    print("  V_gain > 0 means the coherent two-slit profile differs from")
    print("  the single-slit average on the same 4D modular DAG.")
    print("  This is the true metric, not a contrast proxy.")
    print("=" * 78)


if __name__ == "__main__":
    main()
