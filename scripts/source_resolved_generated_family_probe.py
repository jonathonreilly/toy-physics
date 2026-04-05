#!/usr/bin/env python3
"""Source-resolved Green-pocket probe on the compact generated DAG family.

Question:
  Does the source-resolved Green-like field architecture that survives on the
  exact lattice transfer to the compact generated DAG family while preserving
  zero-source reduction, TOWARD sign, and near-linear mass scaling?

This is intentionally narrow:
  - one family: compact generated 3D DAG family
  - one candidate coupled-field architecture: source-resolved Green-like kernel
  - one reduction check: zero-source returns free propagation exactly
  - one comparison: instantaneous 1/r field vs Green-kernel field
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_gravity import centroid_y, generate_3d_dag, propagate  # noqa: E402


N_LAYERS = 16
NODES_PER_LAYER = 24
Y_RANGE = 10.0
CONNECT_RADIUS = 3.2
N_SEEDS = 4
K = 5.0
TARGET_Y = 3.0
MASS_RADIUS = 2.5
SOURCE_STRENGTHS = [1e-4, 2e-4, 4e-4, 8e-4]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08


def _select_mass_nodes(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
    cy: float,
) -> list[int]:
    target_y = cy + TARGET_Y
    ranked = sorted(
        layer_nodes,
        key=lambda i: ((positions[i][1] - target_y) ** 2 + positions[i][2] ** 2, abs(positions[i][1] - target_y)),
    )
    chosen: list[int] = []
    for idx in ranked:
        if abs(positions[idx][1] - target_y) <= MASS_RADIUS:
            chosen.append(idx)
    return chosen[:4] if len(chosen) >= 4 else ranked[:4]


def _instantaneous_field(positions: list[tuple[float, float, float]], mass_ids: list[int], strength: float) -> list[float]:
    field = [0.0] * len(positions)
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i, (x, y, z) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += strength / r
    return field


def _green_field(
    positions: list[tuple[float, float, float]],
    mass_ids: list[int],
    strength: float,
) -> list[float]:
    field = [0.0] * len(positions)
    source_pos = [positions[i] for i in mass_ids]
    if not source_pos:
        return field
    for i, (x, y, z) in enumerate(positions):
        val = 0.0
        for mx, my, mz in source_pos:
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
            val += strength * math.exp(-GREEN_MU * r) / r
        field[i] = val / len(source_pos)
    return field


def _field_max(field: list[float]) -> float:
    return max(abs(v) for v in field) if field else 0.0


def _fit_power(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x > 0 and y > 0]
    if len(pairs) < 3:
        return None
    lx = [math.log(x) for x, _ in pairs]
    ly = [math.log(y) for _, y in pairs]
    mx = sum(lx) / len(lx)
    my = sum(ly) / len(ly)
    sxx = sum((x - mx) ** 2 for x in lx)
    if sxx < 1e-12:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(lx, ly))
    return sxy / sxx


def main() -> None:
    families: list[tuple[list[tuple[float, float, float]], dict[int, list[int]], list[list[int]], list[int]]] = []
    for seed in range(N_SEEDS):
        positions, adj, layers = generate_3d_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            yz_range=Y_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 19 + 7,
        )
        families.append((positions, adj, layers, layers[len(layers) // 2]))

    ref_raw_max = 0.0
    for positions, adj, layers, mid_nodes in families:
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys) / len(all_ys)
        mass_ids = _select_mass_nodes(positions, mid_nodes, cy)
        ref_raw = _green_field(positions, mass_ids, max(SOURCE_STRENGTHS))
        ref_raw_max = max(ref_raw_max, _field_max(ref_raw))
    field_gain = FIELD_TARGET_MAX / ref_raw_max if ref_raw_max > 1e-30 else 1.0

    print("=" * 84)
    print("SOURCE-RESOLVED GENERATED FAMILY PROBE")
    print("  compact generated DAG family, source-resolved Green-kernel candidate")
    print("=" * 84)
    print(
        f"family seeds={N_SEEDS}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, "
        f"connect_radius={CONNECT_RADIUS}"
    )
    print(
        f"kernel: exp(-mu r)/(r+eps), mu={GREEN_MU:.2f}, eps={GREEN_EPS:.2f}, "
        f"field gain={field_gain:.6e}"
    )
    print(f"source strengths={SOURCE_STRENGTHS}")
    print("observable: detector centroid y-shift relative to free propagation")
    print("reduction check: source strength 0 should recover free propagation exactly")
    print()

    zero_shifts: list[float] = []
    inst_means: list[float] = []
    green_means: list[float] = []

    print("REDUCTION CHECK")
    for seed, (positions, adj, layers, mid_nodes) in enumerate(families):
        det = layers[-1]
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys) / len(all_ys)
        mass_ids = _select_mass_nodes(positions, mid_nodes, cy)
        free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
        zero_field = [field_gain * v for v in _green_field(positions, mass_ids, 0.0)]
        zero_amps = propagate(positions, adj, zero_field, layers[0], K)
        delta = centroid_y(zero_amps, positions, det) - centroid_y(free, positions, det)
        zero_shifts.append(delta)
        print(f"  seed {seed}: zero-source shift = {delta:+.6e}")
    print(f"  max |zero-source shift| = {max(abs(x) for x in zero_shifts):.3e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'green':>12s} {'green/inst':>11s} {'sign':>6s}")
    print("-" * 58)

    for s in SOURCE_STRENGTHS:
        per_seed_inst: list[float] = []
        per_seed_green: list[float] = []
        same_sign = 0
        total = 0
        for positions, adj, layers, mid_nodes in families:
            det = layers[-1]
            all_ys = [y for _, y, _ in positions]
            cy = sum(all_ys) / len(all_ys)
            mass_ids = _select_mass_nodes(positions, mid_nodes, cy)

            free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
            z_free = centroid_y(free, positions, det)

            inst_field = _instantaneous_field(positions, mass_ids, s)
            inst_amps = propagate(positions, adj, inst_field, layers[0], K)
            inst_delta = centroid_y(inst_amps, positions, det) - z_free

            green_field = [field_gain * v for v in _green_field(positions, mass_ids, s)]
            green_amps = propagate(positions, adj, green_field, layers[0], K)
            green_delta = centroid_y(green_amps, positions, det) - z_free

            per_seed_inst.append(inst_delta)
            per_seed_green.append(green_delta)
            if inst_delta == 0.0:
                if green_delta == 0.0:
                    same_sign += 1
            elif green_delta == 0.0:
                pass
            elif inst_delta * green_delta > 0:
                same_sign += 1
            total += 1

        inst_mean = sum(per_seed_inst) / len(per_seed_inst)
        green_mean = sum(per_seed_green) / len(per_seed_green)
        inst_means.append(inst_mean)
        green_means.append(green_mean)
        ratio = green_mean / inst_mean if abs(inst_mean) > 1e-30 else math.nan
        print(f"{s:8.4f} {inst_mean:+12.6e} {green_mean:+12.6e} {ratio:11.3f} {same_sign:>2d}/{total:<2d}")

    inst_alpha = _fit_power(list(SOURCE_STRENGTHS), [abs(v) for v in inst_means])
    green_alpha = _fit_power(list(SOURCE_STRENGTHS), [abs(v) for v in green_means])
    toward = sum(1 for v in green_means if v > 0)
    mean_ratio = sum(abs(g / i) for g, i in zip(green_means, inst_means) if abs(i) > 1e-30) / len(SOURCE_STRENGTHS)

    print()
    print("SAFE READ")
    print(f"  exact zero-source reduction: max |delta| = {max(abs(x) for x in zero_shifts):.3e}")
    if inst_alpha is not None:
        print(f"  instantaneous F~M exponent: {inst_alpha:.2f}")
    else:
        print("  instantaneous F~M exponent: n/a")
    if green_alpha is not None:
        print(f"  Green-kernel F~M exponent: {green_alpha:.2f}")
    else:
        print("  Green-kernel F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(green_means)}")
    print(f"  mean |green/inst| ratio: {mean_ratio:.3f}")
    print("  this is a generated-family transfer test, not yet a full self-consistent")
    print("  field sector")


if __name__ == "__main__":
    main()
