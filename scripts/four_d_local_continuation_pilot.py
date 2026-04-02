#!/usr/bin/env python3
"""4D local continuation backreaction pilot on the retained modular lane.

Question
--------
Does local continuation backreaction strengthen or stabilize the distance-law
trend in the retained 4D modular lane?

Controls
--------
  - retained 4D modular DAGs only (gap=5.0)
  - same seed-generated graph for baseline and backreaction
  - fixed mass count for the b sweep
  - k=0 sanity on a representative seed
  - narrow wording if the signal is weak

This is intentionally a pilot, not a full parameter map. The goal is to see
whether the local-continuation architecture moves the 4D distance trend in a
better direction without breaking the retained controls.
"""

from __future__ import annotations

import cmath
import math
import os
import statistics
import sys
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.four_d_distance_scaling import (  # type: ignore  # noqa: E402
    BETA,
    CONNECT_RADIUS,
    MASS_COUNT,
    N_LAYERS,
    NODES_PER_LAYER,
    N_SEEDS,
    SPATIAL_RANGE,
    TARGET_BS,
    centroid_y,
    compute_field_4d,
    fit_power_law,
    generate_4d_modular_dag,
    propagate_4d,
    select_mass_nodes,
)

GAP = 5.0
K_BAND = (3.0, 5.0, 7.0)
DEPTH_WEIGHTS = (0.1, 0.3, 0.5, 0.7, 1.0)
CONTINUATION_STRENGTH = 0.08
CONTINUATION_EPS = 0.5
CONTINUATION_ALIGN_FLOOR = 0.15


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


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


def _normalize_edge_field(edge_field: dict[tuple[int, int], float]) -> dict[tuple[int, int], float]:
    if not edge_field:
        return {}
    max_abs = max(abs(v) for v in edge_field.values())
    if max_abs <= 1e-30:
        return {k: 0.0 for k in edge_field}
    return {k: v / max_abs for k, v in edge_field.items()}


def _local_continuation_signature(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    depth_weight: float,
) -> dict[int, tuple[float, tuple[float, float, float, float], float]]:
    sigs: dict[int, tuple[float, tuple[float, float, float, float], float]] = {}
    for j in range(len(positions)):
        outs = adj.get(j, [])
        if not outs:
            sigs[j] = (1.0, (0.0, 0.0, 0.0, 0.0), 0.0)
            continue

        x0, y0, z0, w0 = positions[j]
        vectors: list[tuple[float, float, float, float]] = []
        two_hop = 0.0
        for ch in outs:
            two_hop += len(adj.get(ch, []))
            dx = positions[ch][0] - x0
            dy = positions[ch][1] - y0
            dz = positions[ch][2] - z0
            dw = positions[ch][3] - w0
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L > 1e-12:
                vectors.append((dx / L, dy / L, dz / L, dw / L))

        if vectors:
            mx = sum(v[0] for v in vectors) / len(vectors)
            my = sum(v[1] for v in vectors) / len(vectors)
            mz = sum(v[2] for v in vectors) / len(vectors)
            mw = sum(v[3] for v in vectors) / len(vectors)
            coherence = math.sqrt(mx * mx + my * my + mz * mz + mw * mw)
            mean_dir = (
                mx / coherence,
                my / coherence,
                mz / coherence,
                mw / coherence,
            ) if coherence > 1e-12 else (0.0, 0.0, 0.0, 0.0)
        else:
            coherence = 0.0
            mean_dir = (0.0, 0.0, 0.0, 0.0)

        capacity = 1.0 + len(outs) + depth_weight * two_hop
        sigs[j] = (capacity, mean_dir, coherence)
    return sigs


def local_continuation_edge_field(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    mass_nodes: list[int],
    depth_weight: float,
    strength: float = CONTINUATION_STRENGTH,
    eps: float = CONTINUATION_EPS,
) -> dict[tuple[int, int], float]:
    """Directionally weighted edge field for the 4D local-continuation pilot."""
    sx, sy, sz, sw = positions[0]
    sigs = _local_continuation_signature(positions, adj, depth_weight)
    edge_field: dict[tuple[int, int], float] = {}

    for i, outs in adj.items():
        x1, y1, z1, w1 = positions[i]
        for j in outs:
            x2, y2, z2, w2 = positions[j]
            dx, dy, dz, dw = x2 - x1, y2 - y1, z2 - z1, w2 - w1
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L < 1e-12:
                continue

            ex, ey, ez, ew = dx / L, dy / L, dz / L, dw / L
            mid_x, mid_y, mid_z, mid_w = (
                0.5 * (x1 + x2),
                0.5 * (y1 + y2),
                0.5 * (z1 + z2),
                0.5 * (w1 + w2),
            )
            cap, cont_dir, coherence = sigs.get(j, (1.0, (0.0, 0.0, 0.0, 0.0), 0.0))
            if cap <= 1e-12 or coherence <= 1e-12:
                continue

            continuity_align = max(0.0, ex * cont_dir[0] + ey * cont_dir[1] + ez * cont_dir[2] + ew * cont_dir[3])
            if continuity_align <= 0.0:
                continue

            response = 0.0
            for m in mass_nodes:
                mx, my, mz, mw = positions[m]
                u_x, u_y, u_z, u_w = mx - sx, my - sy, mz - sz, mw - sw
                u_norm = math.sqrt(u_x * u_x + u_y * u_y + u_z * u_z + u_w * u_w)
                if u_norm < 1e-12:
                    continue
                v_x, v_y, v_z, v_w = mid_x - sx, mid_y - sy, mid_z - sz, mid_w - sw
                v_norm = math.sqrt(v_x * v_x + v_y * v_y + v_z * v_z + v_w * v_w)
                if v_norm < 1e-12:
                    continue
                source_align = (u_x * v_x + u_y * v_y + u_z * v_z + u_w * v_w) / (u_norm * v_norm)
                if source_align <= 0.0:
                    continue
                r = math.sqrt((mid_x - mx) ** 2 + (mid_y - my) ** 2 + (mid_z - mz) ** 2 + (mid_w - mw) ** 2)
                if r < 1e-12:
                    continue
                response += (
                    strength
                    * source_align
                    * continuity_align
                    * max(coherence, CONTINUATION_ALIGN_FLOOR)
                    / (cap * (r + eps))
                )
            if response > 0.0:
                edge_field[(i, j)] = response

    return _normalize_edge_field(edge_field)


def propagate_edge_field_4d(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    edge_field: dict[tuple[int, int], float],
    src: list[int],
    k: float,
) -> list[complex]:
    n = len(positions)
    order = _topo_order(adj, n)
    amps = [0j] * n
    for s in src:
        amps[s] = 1.0 / len(src)

    for i in order:
        if abs(amps[i]) < 1e-30:
            continue
        x1, y1, z1, w1 = positions[i]
        for j in adj.get(i, []):
            x2, y2, z2, w2 = positions[j]
            dx, dy, dz, dw = x2 - x1, y2 - y1, z2 - z1, w2 - w1
            L = math.sqrt(dx * dx + dy * dy + dz * dz + dw * dw)
            if L < 1e-12:
                continue
            theta = math.acos(min(max(dx / L, -1.0), 1.0))
            weight = math.exp(-BETA * theta * theta)
            lf = edge_field.get((i, j), 0.0)
            dl = L * (1.0 + lf)
            ret = math.sqrt(max(dl * dl - L * L, 0.0))
            act = dl - ret
            amps[j] += amps[i] * cmath.exp(1j * k * act) * weight / L
    return amps


def _measure_shift_baseline(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
) -> float | None:
    field = compute_field_4d(positions, adj, mass_nodes)
    free_field = [0.0] * len(positions)
    seed_deltas = []
    for k in K_BAND:
        amps_m = propagate_4d(positions, adj, field, src, k)
        amps_f = propagate_4d(positions, adj, free_field, src, k)
        seed_deltas.append(centroid_y(amps_m, positions, det_list) - centroid_y(amps_f, positions, det_list))
    return _mean(seed_deltas) if seed_deltas else None


def _measure_shift_continuation(
    positions: list[tuple[float, float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    depth_weight: float,
) -> float | None:
    edge_field = local_continuation_edge_field(positions, adj, mass_nodes, depth_weight)
    free_edge_field: dict[tuple[int, int], float] = {}
    seed_deltas = []
    for k in K_BAND:
        amps_m = propagate_edge_field_4d(positions, adj, edge_field, src, k)
        amps_f = propagate_edge_field_4d(positions, adj, free_edge_field, src, k)
        seed_deltas.append(centroid_y(amps_m, positions, det_list) - centroid_y(amps_f, positions, det_list))
    return _mean(seed_deltas) if seed_deltas else None


def _fit_shift_curve(means_by_b: dict[float, list[float]]) -> tuple[float | None, float | None, float | None]:
    xs = [b for b in TARGET_BS if means_by_b[b] and _mean(means_by_b[b]) > 0]
    ys = [_mean(means_by_b[b]) for b in xs]
    fit = fit_power_law(xs, ys) if len(xs) >= 3 else None
    if fit is None:
        return None, None, None
    return fit


def _measure_family(nodes_per_layer: int, connect_radius: float, depth_weight: float) -> dict[str, float | None]:
    by_b_base: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    by_b_cont: dict[float, list[float]] = {b: [] for b in TARGET_BS}

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = generate_4d_modular_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=nodes_per_layer,
            spatial_range=SPATIAL_RANGE,
            connect_radius=connect_radius,
            rng_seed=seed * 17 + 3,
            gap=GAP,
        )
        if len(layer_indices) < 7:
            continue

        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue

        all_ys = [positions[i][1] for i in range(len(positions))]
        center_y = sum(all_ys) / len(all_ys)
        grav_idx = 2 * len(layer_indices) // 3
        mass_layer = layer_indices[grav_idx]

        for b in TARGET_BS:
            mass_nodes = select_mass_nodes(mass_layer, positions, center_y, b, MASS_COUNT)
            if not mass_nodes:
                continue
            base_delta = _measure_shift_baseline(positions, adj, src, det_list, mass_nodes)
            cont_delta = _measure_shift_continuation(positions, adj, src, det_list, mass_nodes, depth_weight)
            if base_delta is not None:
                by_b_base[b].append(base_delta)
            if cont_delta is not None:
                by_b_cont[b].append(cont_delta)

    base_fit = _fit_shift_curve(by_b_base)
    cont_fit = _fit_shift_curve(by_b_cont)

    base_alpha, base_coeff, base_r2 = base_fit if base_fit != (None, None, None) else (None, None, None)
    cont_alpha, cont_coeff, cont_r2 = cont_fit if cont_fit != (None, None, None) else (None, None, None)

    return {
        "base_alpha": base_alpha,
        "base_r2": base_r2,
        "cont_alpha": cont_alpha,
        "cont_r2": cont_r2,
        "b_delta": None if base_alpha is None or cont_alpha is None else cont_alpha - base_alpha,
        "base_nonempty": float(sum(1 for b in TARGET_BS if by_b_base[b])),
        "cont_nonempty": float(sum(1 for b in TARGET_BS if by_b_cont[b])),
        "base_means": by_b_base,
        "cont_means": by_b_cont,
    }


def _k0_sanity(nodes_per_layer: int, connect_radius: float, depth_weight: float) -> float:
    positions, adj, layer_indices = generate_4d_modular_dag(
        n_layers=N_LAYERS,
        nodes_per_layer=nodes_per_layer,
        spatial_range=SPATIAL_RANGE,
        connect_radius=connect_radius,
        rng_seed=5,
        gap=GAP,
    )
    src = layer_indices[0]
    det_list = list(layer_indices[-1])
    all_ys = [positions[i][1] for i in range(len(positions))]
    center_y = sum(all_ys) / len(all_ys)
    grav_idx = 2 * len(layer_indices) // 3
    mass_layer = layer_indices[grav_idx]

    mass_nodes = select_mass_nodes(mass_layer, positions, center_y, 5.0, MASS_COUNT)
    if not mass_nodes:
        upper = sorted([i for i in mass_layer if positions[i][1] >= center_y], key=lambda i: positions[i][1])
        mass_nodes = upper[:MASS_COUNT]
    if not mass_nodes:
        return math.nan

    field = compute_field_4d(positions, adj, mass_nodes)
    free_field = [0.0] * len(positions)
    edge_field = local_continuation_edge_field(positions, adj, mass_nodes, depth_weight)
    zero_base = centroid_y(propagate_4d(positions, adj, field, src, 0.0), positions, det_list) - centroid_y(
        propagate_4d(positions, adj, free_field, src, 0.0), positions, det_list
    )
    zero_cont = centroid_y(propagate_edge_field_4d(positions, adj, edge_field, src, 0.0), positions, det_list) - centroid_y(
        propagate_edge_field_4d(positions, adj, {}, src, 0.0), positions, det_list
    )
    return max(abs(zero_base), abs(zero_cont))


def main() -> None:
    nodes_per_layer = 40
    connect_radius = 5.1

    print("=" * 78)
    print("4D LOCAL CONTINUATION BACKREACTION PILOT")
    print("  retained modular lane: gap=5.0, nodes/layer=40, radius=5.1")
    print(f"  k-band={list(K_BAND)}, seeds={N_SEEDS}")
    print(f"  continuation strength={CONTINUATION_STRENGTH}, eps={CONTINUATION_EPS}")
    print("=" * 78)
    print()

    k0 = _k0_sanity(nodes_per_layer, connect_radius, 0.5)
    print("SANITY CHECK:")
    print(f"  k=0 delta (baseline vs continuation) = {k0:+.6e} (should be ~0)")
    print()

    print("BASELINE (Laplacian-like retained 4D modular lane)")
    base_stats = _measure_family(nodes_per_layer, connect_radius, depth_weight=0.5)
    if base_stats["base_alpha"] is None:
        print("  baseline fit unavailable")
    else:
        print(
            f"  b alpha = {base_stats['base_alpha']:+.3f}  "
            f"R^2={base_stats['base_r2']:.3f}"
        )
    print()

    print("LOCAL CONTINUATION SWEEP")
    print(f"  {'depth_w':>7s}  {'b_alpha':>8s}  {'R^2':>6s}  {'Δb':>8s}  verdict")
    print(f"  {'-' * 42}")

    rows = []
    baseline_alpha = base_stats["base_alpha"]
    baseline_r2 = base_stats["base_r2"]
    for dw in DEPTH_WEIGHTS:
        stats = _measure_family(nodes_per_layer, connect_radius, depth_weight=dw)
        cont_alpha = stats["cont_alpha"]
        cont_r2 = stats["cont_r2"]
        if cont_alpha is None or cont_r2 is None:
            print(f"  {dw:7.2f}  {'FAIL':>8s}  {'NA':>6s}  {'NA':>8s}  insufficient positive sweep")
            continue
        delta = None if baseline_alpha is None else cont_alpha - baseline_alpha
        if delta is None:
            verdict = "partial"
        elif delta < -0.05 and cont_alpha < 0:
            verdict = "helps"
        elif delta < 0:
            verdict = "nudges"
        else:
            verdict = "no"
        rows.append((dw, cont_alpha, cont_r2, delta))
        print(
            f"  {dw:7.2f}  {cont_alpha:+8.3f}  {cont_r2:6.3f}  "
            f"{(delta if delta is not None else math.nan):+8.3f}  {verdict}"
        )

    print()
    if rows and baseline_alpha is not None:
        best = min(rows, key=lambda r: r[1])
        print("BEST CONTINUATION ROW")
        print(
            f"  depth_weight={best[0]:.2f}  b alpha={best[1]:+.3f}  "
            f"R^2={best[2]:.3f}  Δb={best[3]:+.3f}"
        )
        if best[1] < baseline_alpha - 0.05:
            print("  narrow verdict: 4D local continuation helps the distance trend a bit")
        elif best[1] < baseline_alpha:
            print("  narrow verdict: 4D local continuation weakly nudges the distance trend")
        else:
            print("  narrow verdict: 4D local continuation does not improve the distance trend")
    else:
        print("  narrow verdict: continuation sweep did not produce a stable positive fit")

    print()
    print("INTERPRETATION")
    print("  If b alpha becomes more negative than baseline, the architecture helps.")
    print("  If it only shuffles weakly around the baseline, keep the claim narrow.")
    print("  If the best row is still weaker or unstable, 4D does not rescue the architecture.")
    print("=" * 78)


if __name__ == "__main__":
    main()
