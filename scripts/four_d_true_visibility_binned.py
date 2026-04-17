#!/usr/bin/env python3
"""4D binned true single-vs-double-slit visibility on the retained modular lane.

This is the review-safe version of the 4D visibility check. It keeps the same
4D modular DAG family and the same propagator, but replaces exact-y detector
grouping with fixed y-bins plus a small smoothing/envelope step.

Goal:
  - Determine whether the earlier V_gain ~ 0 result was a detector-profile
    artifact or a real physics result on the retained 4D modular lane.

Metric:
  - Build coarse y-binned detector profiles for the coherent two-slit run and
    the incoherent single-slit average.
  - Smooth each profile with a tiny local envelope window before extracting
    fringe visibility.
  - Report visibility gain = V_coh - V_single.

The lane is the same 4D modular family used by the gravity/decoherence work:
  x is the causal layer, y is the slit/channel axis, and z/w are free
  transverse coordinates.
"""

from __future__ import annotations

import cmath
import math
import random
import time
from collections import defaultdict, deque

BETA = 0.8
K_BAND = [3.0, 5.0, 7.0]
N_BINS = 12
Y_MIN = -8.0
Y_MAX = 8.0
SMOOTH_RADIUS = 1


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

                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz, pw = positions[prev_idx]
                        dist = math.sqrt(
                            (x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2 + (w - pw) ** 2
                        )
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


def _binned_profile(
    probs: dict[int, float],
    positions: list[tuple[float, float, float, float]],
    det_list: list[int],
    *,
    y_min: float = Y_MIN,
    y_max: float = Y_MAX,
    n_bins: int = N_BINS,
) -> list[float]:
    bw = (y_max - y_min) / n_bins
    bins = [0.0] * n_bins
    for d in det_list:
        y = positions[d][1]
        b = int((y - y_min) / bw)
        b = max(0, min(n_bins - 1, b))
        bins[b] += probs.get(d, 0.0)
    return bins


def _smooth(profile: list[float], radius: int = SMOOTH_RADIUS) -> list[float]:
    if radius <= 0 or len(profile) < 3:
        return profile[:]
    out = []
    for i in range(len(profile)):
        lo = max(0, i - radius)
        hi = min(len(profile), i + radius + 1)
        window = profile[lo:hi]
        out.append(sum(window) / len(window))
    return out


def _profile_visibility(profile: list[float]) -> float:
    smooth = _smooth(profile)
    if len(smooth) < 3:
        return 0.0
    peaks = [
        smooth[i]
        for i in range(1, len(smooth) - 1)
        if smooth[i] > smooth[i - 1] and smooth[i] > smooth[i + 1]
    ]
    troughs = [
        smooth[i]
        for i in range(1, len(smooth) - 1)
        if smooth[i] < smooth[i - 1] and smooth[i] < smooth[i + 1]
    ]
    if not peaks or not troughs:
        return 0.0
    top = max(peaks)
    bottom = min(troughs)
    return (top - bottom) / (top + bottom) if top + bottom > 1e-30 else 0.0


def build_setup(positions, adj):
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
        "layers": layers,
        "src": src,
        "det_list": det_list,
        "cy": cy,
        "barrier": barrier,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "blocked": blocked,
        "field": field,
    }


def true_visibility_binned(positions, adj, setup):
    src = setup["src"]
    det_list = setup["det_list"]
    field = setup["field"]
    blocked = setup["blocked"]
    slit_a = setup["slit_a"]
    slit_b = setup["slit_b"]

    vis_coh_vals = []
    vis_single_vals = []

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

        coh_profile = _binned_profile(probs_both, positions, det_list)
        single_profile = _binned_profile(probs_single_avg, positions, det_list)
        vis_coh_vals.append(_profile_visibility(coh_profile))
        vis_single_vals.append(_profile_visibility(single_profile))

    if not vis_coh_vals:
        return None
    avg_coh = sum(vis_coh_vals) / len(vis_coh_vals)
    avg_single = sum(vis_single_vals) / len(vis_single_vals)
    return avg_coh, avg_single, avg_coh - avg_single


def main():
    print("=" * 78)
    print("4D TRUE VISIBILITY (BINNED): Modular DAGs")
    print("  Review-safe fixed-bin detector metric with envelope smoothing")
    print("  Goal: check whether V_gain ~ 0 survives binning")
    print("=" * 78)
    print()

    n_layers_list = [12, 18, 25, 40, 60, 80, 100]
    gaps = [3.0, 5.0]
    n_seeds = 8

    print(
        f"  {'gap':>4s}  {'N':>4s}  {'V_coh':>7s}  {'V_sng':>7s}  "
        f"{'V_gain':>8s}  {'n_ok':>4s}  verdict"
    )
    print(f"  {'-' * 60}")

    for gap in gaps:
        for nl in n_layers_list:
            coh_vals = []
            single_vals = []
            gain_vals = []
            n_ok = 0
            t0 = time.time()

            for seed in range(n_seeds):
                positions, adj, _ = generate_4d_modular_dag(
                    n_layers=nl,
                    nodes_per_layer=25,
                    spatial_range=8.0,
                    connect_radius=4.5,
                    rng_seed=seed * 13 + 5,
                    gap=gap,
                )
                setup = build_setup(positions, adj)
                if setup is None:
                    continue

                result = true_visibility_binned(positions, adj, setup)
                if result is None:
                    continue
                avg_coh, avg_single, gain = result
                coh_vals.append(avg_coh)
                single_vals.append(avg_single)
                gain_vals.append(gain)
                n_ok += 1

            dt = time.time() - t0
            if n_ok:
                mc = sum(coh_vals) / len(coh_vals)
                ms = sum(single_vals) / len(single_vals)
                mg = sum(gain_vals) / len(gain_vals)
                verdict = "PASS" if mg > 0.02 else "WEAK" if mg > 0 else "NONE"
                print(
                    f"  {gap:4.1f}  {nl:4d}  {mc:7.3f}  {ms:7.3f}  "
                    f"{mg:+8.3f}  {n_ok:4d}  {verdict}"
                )
            else:
                print(f"  {gap:4.1f}  {nl:4d}  FAIL")

    print()
    print("INTERPRETATION")
    print("  V_gain > 0 means the coherent two-slit profile differs from")
    print("  the single-slit average after binning and mild envelope smoothing.")
    print("  This is the stricter check for whether the 4D gain is real.")
    print("=" * 78)


if __name__ == "__main__":
    main()
