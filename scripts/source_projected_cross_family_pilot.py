#!/usr/bin/env python3
"""Cross-family transfer test for the source-projected distance-law seam.

Goal
----
Test whether the best current source-projected seam on retained 3D modular
DAGs transfers to at least one second 3D family under the same fixed-mass
controls.

Families:
  - retained 3D modular DAGs (reference family)
  - hierarchical 3D funnelled DAGs (second family)
  - uniform 3D DAGs (fallback control if feasible)

Review discipline:
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - same source-projected coupling strength for every family
  - keep the conclusion narrow: family-general only if the second family
    preserves the seam in the same direction under the same controls
"""

from __future__ import annotations

import cmath
import math
import os
import random
import statistics
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Callable

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.source_projected_field_pilot import (  # type: ignore  # noqa: E402
    GAP,
    K_BAND,
    MASS_COUNTS,
    MASS_COUNT_FIXED,
    MASS_LAYER_OFFSET,
    N_LAYERS,
    N_SEEDS,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    centroid_y,
    field_laplacian,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
    _select_fixed_mass_nodes,
)

PROJECTED_STRENGTH = 0.12
HIERARCHICAL_GAP = 3.0
HIERARCHICAL_LEAK = 0.05
UNIFORM_Y_RANGE = XYZ_RANGE
UNIFORM_CONNECT_RADIUS = CONNECT_RADIUS


@dataclass(frozen=True)
class FamilySpec:
    label: str
    build_graph: Callable[[int], tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _fit_power_law(xs_in: list[float], ys_in: list[float]) -> tuple[float, float, float] | None:
    pairs = [(x, y) for x, y in zip(xs_in, ys_in) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    xs = [math.log(x) for x, _ in pairs]
    ys = [math.log(y) for _, y in pairs]
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxy = sum(x * y for x, y in zip(xs, ys))
    sxx = sum(x * x for x in xs)
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-12:
        return None
    slope = (n * sxy - sx * sy) / denom
    intercept = (sy - slope * sx) / n
    ss_tot = sum((y - sy / n) ** 2 for y in ys)
    ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    r2 = 1.0 - (ss_res / ss_tot if ss_tot > 1e-30 else 0.0)
    return slope, math.exp(intercept), r2


def _topo_order(adj: dict[int, list[int]], n: int) -> list[int]:
    in_deg = [0] * n
    for nbs in adj.values():
        for j in nbs:
            in_deg[j] += 1
    q = deque(i for i in range(n) if in_deg[i] == 0)
    order: list[int] = []
    while q:
        i = q.popleft()
        order.append(i)
        for j in adj.get(i, []):
            in_deg[j] -= 1
            if in_deg[j] == 0:
                q.append(j)
    return order


def generate_3d_uniform_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = 40,
    yz_range: float = UNIFORM_Y_RANGE,
    connect_radius: float = UNIFORM_CONNECT_RADIUS,
    rng_seed: int = 42,
) -> tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]:
    """Layered 3D DAG with no channel separation."""
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
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
                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if dist <= connect_radius:
                            adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def generate_3d_hierarchical_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = 40,
    yz_range: float = XYZ_RANGE,
    connect_radius: float = CONNECT_RADIUS,
    rng_seed: int = 42,
    gap: float = HIERARCHICAL_GAP,
    channel_leak: float = HIERARCHICAL_LEAK,
) -> tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]:
    """3D funnelled / channel-separated DAG.

    Post-barrier nodes are biased into upper/lower y channels, with a small
    cross-channel leakage probability.
    """
    rng = random.Random(rng_seed)
    positions: list[tuple[float, float, float]] = []
    adj: dict[int, list[int]] = defaultdict(list)
    layer_indices: list[list[int]] = []
    barrier_layer = n_layers // 3
    use_channels = gap > 0

    for layer in range(n_layers):
        x = float(layer)
        layer_nodes: list[int] = []
        if layer == 0:
            positions.append((x, 0.0, 0.0))
            layer_nodes.append(len(positions) - 1)
        else:
            for node_i in range(nodes_per_layer):
                if use_channels and layer > barrier_layer:
                    if node_i < nodes_per_layer // 2:
                        y = rng.uniform(gap / 2, yz_range)
                    else:
                        y = rng.uniform(-yz_range, -gap / 2)
                else:
                    y = rng.uniform(-yz_range, yz_range)
                z = rng.uniform(-yz_range, yz_range)
                idx = len(positions)
                positions.append((x, y, z))
                layer_nodes.append(idx)

                for prev_layer in layer_indices[max(0, layer - 2) :]:
                    for prev_idx in prev_layer:
                        px, py, pz = positions[prev_idx]
                        dist = math.sqrt((x - px) ** 2 + (y - py) ** 2 + (z - pz) ** 2)
                        if use_channels and layer > barrier_layer and round(px) > barrier_layer:
                            same_channel = (y * py > 0)
                            if same_channel:
                                r = connect_radius
                                if dist <= r:
                                    adj[prev_idx].append(idx)
                            else:
                                r = connect_radius * 2.0
                                if dist <= r and rng.random() < channel_leak:
                                    adj[prev_idx].append(idx)
                        else:
                            if dist <= connect_radius:
                                adj[prev_idx].append(idx)
        layer_indices.append(layer_nodes)

    return positions, dict(adj), layer_indices


def _select_state(
    positions: list[tuple[float, float, float]],
    layer_indices: list[list[int]],
) -> dict[str, object] | None:
    if len(layer_indices) <= MASS_LAYER_OFFSET:
        return None
    barrier_layer = len(layer_indices) // 3
    if barrier_layer >= len(layer_indices) - 1:
        return None

    barrier = list(layer_indices[barrier_layer])
    det_list = list(layer_indices[-1])
    if not barrier or not det_list:
        return None

    cy = statistics.fmean(positions[i][1] for i in range(len(positions)))
    upper = [i for i in barrier if positions[i][1] > cy + 3][:3]
    lower = [i for i in barrier if positions[i][1] < cy - 3][:3]
    if not upper or not lower:
        return None

    post_nodes = [
        i
        for li in range(barrier_layer + 1, len(layer_indices) - 1)
        for i in layer_indices[li]
    ]
    if len(post_nodes) < 4:
        return None

    return {
        "src": list(layer_indices[0]),
        "det_list": det_list,
        "layer_nodes": list(layer_indices[MASS_LAYER_OFFSET]),
        "post_nodes": post_nodes,
    }


def _select_fixed_mass_nodes(
    layer_nodes: list[int],
    positions: list[tuple[float, float, float]],
    target_y: float,
    count: int,
) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _pair_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    field_builder,
    mass_nodes: list[int],
) -> float | None:
    field_with = field_builder(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        deltas.append(centroid_y(amps_with, positions, det_list) - centroid_y(amps_without, positions, det_list))
    return _mean(deltas) if deltas else None


def _measure_family(
    name: str,
    builder: Callable[[int], tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]],
) -> dict[str, float | dict[str, float]]:
    valid_seeds = 0

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = builder(seed * 17 + 3)
        state = _select_state(positions, layer_indices)
        if state is None:
            continue
        valid_seeds += 1

        src = state["src"]  # type: ignore[assignment]
        det_list = state["det_list"]  # type: ignore[assignment]
        layer_nodes = state["layer_nodes"]  # type: ignore[assignment]
        cy = statistics.fmean(positions[i][1] for i in range(len(positions)))

    # Re-evaluate with explicit mode separation for the report.
    def _measure_mode(field_builder) -> tuple[dict[float, list[float]], dict[int, list[float]]]:
        out_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
        out_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
        for seed in range(N_SEEDS):
            positions, adj, layer_indices = builder(seed * 17 + 3)
            state = _select_state(positions, layer_indices)
            if state is None:
                continue
            src = state["src"]  # type: ignore[assignment]
            det_list = state["det_list"]  # type: ignore[assignment]
            layer_nodes = state["layer_nodes"]  # type: ignore[assignment]
            cy = statistics.fmean(positions[i][1] for i in range(len(positions)))
            for b in TARGET_BS:
                mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, cy + b, MASS_COUNT_FIXED)
                if len(mass_nodes) != MASS_COUNT_FIXED:
                    continue
                delta = _pair_delta(positions, adj, src, det_list, field_builder, mass_nodes)
                if delta is not None:
                    out_b[b].append(delta)
            mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, cy + 3.0, max(MASS_COUNTS))
            if len(mass_nodes) == max(MASS_COUNTS):
                for m in MASS_COUNTS:
                    subset = mass_nodes[:m]
                    delta = _pair_delta(positions, adj, src, det_list, field_builder, subset)
                    if delta is not None:
                        out_m[m].append(delta)
        return out_b, out_m

    lap_b, lap_m = _measure_mode(field_laplacian)
    proj_b, proj_m = _measure_mode(lambda p, a, m: field_source_projected(p, a, m, strength=PROJECTED_STRENGTH))

    lap_b_fit = _fit_power_law([b for b, vals in lap_b.items() if vals and _mean(vals) > 0], [_mean(lap_b[b]) for b, vals in lap_b.items() if vals and _mean(vals) > 0])
    proj_b_fit = _fit_power_law([b for b, vals in proj_b.items() if vals and _mean(vals) > 0], [_mean(proj_b[b]) for b, vals in proj_b.items() if vals and _mean(vals) > 0])
    lap_m_fit = _fit_power_law([m for m, vals in lap_m.items() if vals and _mean(vals) > 0], [_mean(lap_m[m]) for m, vals in lap_m.items() if vals and _mean(vals) > 0])
    proj_m_fit = _fit_power_law([m for m, vals in proj_m.items() if vals and _mean(vals) > 0], [_mean(proj_m[m]) for m, vals in proj_m.items() if vals and _mean(vals) > 0])

    return {
        "name": name,
        "valid_seeds": float(valid_seeds),
        "lap_b_fit": lap_b_fit,
        "proj_b_fit": proj_b_fit,
        "lap_m_fit": lap_m_fit,
        "proj_m_fit": proj_m_fit,
        "lap_b": lap_b,
        "proj_b": proj_b,
        "lap_m": lap_m,
        "proj_m": proj_m,
    }


def _print_family_result(result: dict[str, object]) -> None:
    name = result["name"]  # type: ignore[assignment]
    print("=" * 88)
    print(str(name).upper())
    print("=" * 88)
    print(f"  valid seeds: {int(result['valid_seeds'])}")

    lap_b = result["lap_b"]  # type: ignore[assignment]
    proj_b = result["proj_b"]  # type: ignore[assignment]
    lap_m = result["lap_m"]  # type: ignore[assignment]
    proj_m = result["proj_m"]  # type: ignore[assignment]
    lap_b_fit = result["lap_b_fit"]  # type: ignore[assignment]
    proj_b_fit = result["proj_b_fit"]  # type: ignore[assignment]
    lap_m_fit = result["lap_m_fit"]  # type: ignore[assignment]
    proj_m_fit = result["proj_m_fit"]  # type: ignore[assignment]

    print("  b-sweep")
    print(f"    {'b':>3s}  {'lap':>8s}  {'proj':>8s}  {'delta':>8s}")
    for b in TARGET_BS:
        lv = lap_b[b]
        pv = proj_b[b]
        lap_val = _mean(lv) if lv else math.nan
        proj_val = _mean(pv) if pv else math.nan
        delta = proj_val - lap_val if math.isfinite(lap_val) and math.isfinite(proj_val) else math.nan
        print(
            f"    {b:3d}  {lap_val:+8.4f}  {proj_val:+8.4f}  {delta:+8.4f}"
        )
    if lap_b_fit is not None:
        print(f"    Lap fit:  shift ~= {lap_b_fit[1]:.4f} * b^{lap_b_fit[0]:.3f}  (R^2={lap_b_fit[2]:.3f})")
    else:
        print("    Lap fit:  NA")
    if proj_b_fit is not None:
        print(f"    Proj fit: shift ~= {proj_b_fit[1]:.4f} * b^{proj_b_fit[0]:.3f}  (R^2={proj_b_fit[2]:.3f})")
    else:
        print("    Proj fit: NA")

    print("  mass-sweep")
    print(f"    {'M':>4s}  {'lap':>8s}  {'proj':>8s}  {'delta':>8s}")
    for m in MASS_COUNTS:
        lv = lap_m[m]
        pv = proj_m[m]
        lap_val = _mean(lv) if lv else math.nan
        proj_val = _mean(pv) if pv else math.nan
        delta = proj_val - lap_val if math.isfinite(lap_val) and math.isfinite(proj_val) else math.nan
        print(
            f"    {m:4d}  {lap_val:+8.4f}  {proj_val:+8.4f}  {delta:+8.4f}"
        )
    if lap_m_fit is not None:
        print(f"    Lap fit:  shift ~= {lap_m_fit[1]:.4f} * M^{lap_m_fit[0]:.3f}  (R^2={lap_m_fit[2]:.3f})")
    else:
        print("    Lap fit:  NA")
    if proj_m_fit is not None:
        print(f"    Proj fit: shift ~= {proj_m_fit[1]:.4f} * M^{proj_m_fit[0]:.3f}  (R^2={proj_m_fit[2]:.3f})")
    else:
        print("    Proj fit: NA")
    print()


def main() -> None:
    print("=" * 88)
    print("SOURCE-PROJECTED CROSS-FAMILY PILOT")
    print("  Retained 3D modular seam vs a second 3D family under fixed-mass controls")
    print("=" * 88)
    print()
    print(f"  seeds per family: {N_SEEDS}")
    print(f"  projected strength: {PROJECTED_STRENGTH}")
    print(f"  k-band: {K_BAND}")
    print(f"  fixed mass count for b-sweep: {MASS_COUNT_FIXED}")
    print(f"  fixed b for mass-sweep: 3.0")
    print(f"  mass counts: {MASS_COUNTS}")
    print()

    families = [
        FamilySpec(
            label="retained 3D modular",
            build_graph=lambda seed: generate_3d_modular_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=40,
                xyz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
                gap=GAP,
            ),
        ),
        FamilySpec(
            label="hierarchical 3D",
            build_graph=lambda seed: generate_3d_hierarchical_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=40,
                yz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
            ),
        ),
        FamilySpec(
            label="uniform 3D",
            build_graph=lambda seed: generate_3d_uniform_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=40,
                yz_range=UNIFORM_Y_RANGE,
                connect_radius=UNIFORM_CONNECT_RADIUS,
                rng_seed=seed,
            ),
        ),
    ]

    results = []
    for spec in families:
        results.append(_measure_family(spec.label, spec.build_graph))

    for result in results:
        _print_family_result(result)

    print("=" * 88)
    print("COMPARISON")
    for result in results:
        name = str(result["name"])
        lap_b_fit = result["lap_b_fit"]  # type: ignore[assignment]
        proj_b_fit = result["proj_b_fit"]  # type: ignore[assignment]
        lap_m_fit = result["lap_m_fit"]  # type: ignore[assignment]
        proj_m_fit = result["proj_m_fit"]  # type: ignore[assignment]
        print(
            f"  {name}: "
            f"lap_b={'NA' if lap_b_fit is None else f'{lap_b_fit[0]:.3f}'} | "
            f"proj_b={'NA' if proj_b_fit is None else f'{proj_b_fit[0]:.3f}'} | "
            f"lap_M={'NA' if lap_m_fit is None else f'{lap_m_fit[0]:.3f}'} | "
            f"proj_M={'NA' if proj_m_fit is None else f'{proj_m_fit[0]:.3f}'}"
        )

    print()
    print("INTERPRETATION")
    print(
        "  If the source-projected lane preserves the distance-trend improvement "
        "and positive mass scaling on a non-modular 3D family, the seam is family-general."
    )
    print(
        "  If the improvement only survives on the retained modular family, it is modular-specific."
    )
    print("=" * 88)


if __name__ == "__main__":
    main()
