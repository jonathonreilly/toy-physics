#!/usr/bin/env python3
"""Source-projected cross-family transfer re-audit under strict controls.

Question
--------
Does the source-projected modular distance-law seam still transfer to a
second 3D family once we:
  - avoid the low-leak degenerate hierarchical regime,
  - use a larger seed count,
  - and require the entire b / M sweep to stay positive before fitting?

This script keeps the same fixed-position / fixed-count controls as the
earlier pilot, but tightens the fit gate so we do not report a power law if
any sweep point turns non-positive.

Families:
  - retained 3D modular DAGs (reference family)
  - hierarchical 3D DAGs with nondegenerate leak (0.20, 0.50)
  - uniform 3D DAGs as a control

Review discipline:
  - fixed graph geometry per seed
  - fixed mass count across the b sweep
  - fixed b across the mass sweep
  - same source-projected coupling strength for every family
  - only report a fit if the full sweep remains positive
"""

from __future__ import annotations

import math
import os
import random
import statistics
import sys
from collections import defaultdict
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
    NODES_PER_LAYER,
    TARGET_BS,
    XYZ_RANGE,
    CONNECT_RADIUS,
    centroid_y,
    field_laplacian,
    field_source_projected,
    generate_3d_modular_dag,
    propagate,
)
from scripts.source_projected_cross_family_pilot import (  # type: ignore  # noqa: E402
    generate_3d_hierarchical_dag,
)


N_SEEDS = 32
PROJECTED_STRENGTH = 0.12
HIERARCHICAL_GAPS = (0.20, 0.50)
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


def _fit_full_sweep_positive(means_by_key: dict[float | int, list[float]], keys: list[float | int]) -> tuple[float, float, float] | None:
    xs: list[float] = []
    ys: list[float] = []
    for key in keys:
        vals = means_by_key[key]
        if not vals:
            return None
        mean = _mean(vals)
        if not math.isfinite(mean) or mean <= 0.0:
            return None
        xs.append(float(key))
        ys.append(mean)
    if len(xs) < 3:
        return None
    return _fit_power_law(xs, ys)


def _topo_layers(positions: list[tuple[float, float, float]]) -> dict[int, list[int]]:
    by_layer: dict[int, list[int]] = defaultdict(list)
    for idx, (x, *_rest) in enumerate(positions):
        by_layer[round(x)].append(idx)
    return by_layer


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


def generate_3d_uniform_dag(
    n_layers: int = N_LAYERS,
    nodes_per_layer: int = NODES_PER_LAYER,
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


def _paired_delta(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    src: list[int],
    det_list: list[int],
    mass_nodes: list[int],
    field_builder,
) -> float | None:
    field_with = field_builder(positions, adj, mass_nodes)
    field_without = [0.0] * len(positions)
    deltas = []
    for k in K_BAND:
        amps_with = propagate(positions, adj, field_with, src, k)
        amps_without = propagate(positions, adj, field_without, src, k)
        deltas.append(
            centroid_y(amps_with, positions, det_list)
            - centroid_y(amps_without, positions, det_list)
        )
    return _mean(deltas) if deltas else None


def _measure_family(
    name: str,
    builder: Callable[[int], tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]]]],
) -> dict[str, object]:
    lap_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    lap_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    proj_b: dict[float, list[float]] = {b: [] for b in TARGET_BS}
    proj_m: dict[int, list[float]] = {m: [] for m in MASS_COUNTS}
    valid_seeds = 0

    for seed in range(N_SEEDS):
        positions, adj, layer_indices = builder(seed * 17 + 3)
        if len(layer_indices) < 7:
            continue
        src = layer_indices[0]
        det_list = list(layer_indices[-1])
        if not det_list:
            continue
        valid_seeds += 1

        center_y = statistics.fmean(positions[i][1] for i in range(len(positions)))
        layer_nodes = layer_indices[MASS_LAYER_OFFSET]

        for b in TARGET_BS:
            mass_nodes = _select_fixed_mass_nodes(layer_nodes, positions, center_y + b, MASS_COUNT_FIXED)
            if len(mass_nodes) != MASS_COUNT_FIXED:
                continue
            lap_delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_laplacian)
            proj_delta = _paired_delta(
                positions,
                adj,
                src,
                det_list,
                mass_nodes,
                lambda p, a, m: field_source_projected(p, a, m, strength=PROJECTED_STRENGTH),
            )
            if lap_delta is not None:
                lap_b[b].append(lap_delta)
            if proj_delta is not None:
                proj_b[b].append(proj_delta)

        ranked = _select_fixed_mass_nodes(layer_nodes, positions, center_y + 3.0, max(MASS_COUNTS))
        if len(ranked) == max(MASS_COUNTS):
            for m in MASS_COUNTS:
                mass_nodes = ranked[:m]
                lap_delta = _paired_delta(positions, adj, src, det_list, mass_nodes, field_laplacian)
                proj_delta = _paired_delta(
                    positions,
                    adj,
                    src,
                    det_list,
                    mass_nodes,
                    lambda p, a, m: field_source_projected(p, a, m, strength=PROJECTED_STRENGTH),
                )
                if lap_delta is not None:
                    lap_m[m].append(lap_delta)
                if proj_delta is not None:
                    proj_m[m].append(proj_delta)

    lap_b_fit = _fit_full_sweep_positive(lap_b, list(TARGET_BS))
    proj_b_fit = _fit_full_sweep_positive(proj_b, list(TARGET_BS))
    lap_m_fit = _fit_full_sweep_positive(lap_m, list(MASS_COUNTS))
    proj_m_fit = _fit_full_sweep_positive(proj_m, list(MASS_COUNTS))

    return {
        "name": name,
        "valid_seeds": valid_seeds,
        "lap_b": lap_b,
        "proj_b": proj_b,
        "lap_m": lap_m,
        "proj_m": proj_m,
        "lap_b_fit": lap_b_fit,
        "proj_b_fit": proj_b_fit,
        "lap_m_fit": lap_m_fit,
        "proj_m_fit": proj_m_fit,
    }


def _print_family_result(result: dict[str, object]) -> None:
    name = str(result["name"])
    print("=" * 88)
    print(name.upper())
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
        lap_val = _mean(lap_b[b]) if lap_b[b] else math.nan
        proj_val = _mean(proj_b[b]) if proj_b[b] else math.nan
        delta = proj_val - lap_val if math.isfinite(lap_val) and math.isfinite(proj_val) else math.nan
        print(f"    {b:3d}  {lap_val:+8.4f}  {proj_val:+8.4f}  {delta:+8.4f}")
    if lap_b_fit is not None:
        print(f"    Lap fit:  shift ~= {lap_b_fit[1]:.4f} * b^{lap_b_fit[0]:.3f}  (R^2={lap_b_fit[2]:.3f})")
    else:
        print("    Lap fit:  full-sweep-positive fit unavailable")
    if proj_b_fit is not None:
        print(f"    Proj fit: shift ~= {proj_b_fit[1]:.4f} * b^{proj_b_fit[0]:.3f}  (R^2={proj_b_fit[2]:.3f})")
    else:
        print("    Proj fit: full-sweep-positive fit unavailable")

    print("  mass-sweep")
    print(f"    {'M':>4s}  {'lap':>8s}  {'proj':>8s}  {'delta':>8s}")
    for m in MASS_COUNTS:
        lap_val = _mean(lap_m[m]) if lap_m[m] else math.nan
        proj_val = _mean(proj_m[m]) if proj_m[m] else math.nan
        delta = proj_val - lap_val if math.isfinite(lap_val) and math.isfinite(proj_val) else math.nan
        print(f"    {m:4d}  {lap_val:+8.4f}  {proj_val:+8.4f}  {delta:+8.4f}")
    if lap_m_fit is not None:
        print(f"    Lap fit:  shift ~= {lap_m_fit[1]:.4f} * M^{lap_m_fit[0]:.3f}  (R^2={lap_m_fit[2]:.3f})")
    else:
        print("    Lap fit:  full-sweep-positive fit unavailable")
    if proj_m_fit is not None:
        print(f"    Proj fit: shift ~= {proj_m_fit[1]:.4f} * M^{proj_m_fit[0]:.3f}  (R^2={proj_m_fit[2]:.3f})")
    else:
        print("    Proj fit: full-sweep-positive fit unavailable")
    print()


def main() -> None:
    print("=" * 88)
    print("SOURCE-PROJECTED TRANSFER RE-AUDIT")
    print("  Modular reference plus nondegenerate hierarchical controls")
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
                nodes_per_layer=NODES_PER_LAYER,
                xyz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
                gap=GAP,
            ),
        ),
        FamilySpec(
            label="hierarchical 3D leak=0.20",
            build_graph=lambda seed: generate_3d_hierarchical_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=NODES_PER_LAYER,
                yz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
                gap=3.0,
                channel_leak=0.20,
            ),
        ),
        FamilySpec(
            label="hierarchical 3D leak=0.50",
            build_graph=lambda seed: generate_3d_hierarchical_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=NODES_PER_LAYER,
                yz_range=XYZ_RANGE,
                connect_radius=CONNECT_RADIUS,
                rng_seed=seed,
                gap=3.0,
                channel_leak=0.50,
            ),
        ),
        FamilySpec(
            label="uniform 3D",
            build_graph=lambda seed: generate_3d_uniform_dag(
                n_layers=N_LAYERS,
                nodes_per_layer=NODES_PER_LAYER,
                yz_range=UNIFORM_Y_RANGE,
                connect_radius=UNIFORM_CONNECT_RADIUS,
                rng_seed=seed,
            ),
        ),
    ]

    results = [_measure_family(spec.label, spec.build_graph) for spec in families]
    for result in results:
        _print_family_result(result)

    print("=" * 88)
    print("COMPARISON")
    for result in results:
        name = str(result["name"])
        proj_b_fit = result["proj_b_fit"]  # type: ignore[assignment]
        proj_m_fit = result["proj_m_fit"]  # type: ignore[assignment]
        print(
            f"  {name}: "
            f"proj_b={'NA' if proj_b_fit is None else f'{proj_b_fit[0]:.3f}'} | "
            f"proj_M={'NA' if proj_m_fit is None else f'{proj_m_fit[0]:.3f}'}"
        )

    print()
    print("INTERPRETATION")
    print("  If the source-projected lane keeps a full-sweep-positive negative-b trend")
    print("  on a nondegenerate hierarchical family, the transfer story survives.")
    print("  If it only survives on the modular family, it is modular-specific.")
    print("=" * 88)


if __name__ == "__main__":
    main()
