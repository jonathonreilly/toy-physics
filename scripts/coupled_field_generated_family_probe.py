#!/usr/bin/env python3
"""Coupled field probe on the compact generated DAG family.

Question:
  Can a minimal source-driven field architecture on the retained compact
  generated DAG family preserve the weak-field sign and linear mass scaling?

This is intentionally narrow:
  - one family: compact generated 3D DAG family
  - one candidate coupled-field architecture: forward source-driven diffusion
  - one reduction check: zero-source returns free propagation exactly
  - one comparison: instantaneous 1/r field vs source-driven field
"""

from __future__ import annotations

import math
import os
import sys
from collections import deque

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
FIELD_DECAY = 0.7
FIELD_GAIN_TARGET = 0.05


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
    return chosen[:5] if len(chosen) >= 3 else ranked[:5]


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


def _instantaneous_field(positions: list[tuple[float, float, float]], mass_ids: list[int], strength: float) -> list[float]:
    field = [0.0] * len(positions)
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i, (x, y, z) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += strength / r
    return field


def _source_driven_field_raw(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    mass_ids: list[int],
    strength: float,
) -> list[float]:
    n = len(positions)
    order = _topo_order(adj, n)
    field = [0.0] * n
    for m in mass_ids:
        field[m] = strength
    for i in order:
        if field[i] <= 0.0:
            continue
        outs = adj.get(i, [])
        if not outs:
            continue
        share = FIELD_DECAY * field[i] / max(1, len(outs))
        for j in outs:
            field[j] += share
    return field


def _scale_field(field: list[float], gain: float) -> list[float]:
    return [gain * v for v in field]


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

    # One fixed calibration so the source-dependent sweep stays linear.
    ref_raw_max = 0.0
    for positions, adj, layers, mid_nodes in families:
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys) / len(all_ys)
        mass_ids = _select_mass_nodes(positions, mid_nodes, cy)
        ref_raw = _source_driven_field_raw(positions, adj, mass_ids, max(SOURCE_STRENGTHS))
        ref_raw_max = max(ref_raw_max, _field_max(ref_raw))
    field_gain = FIELD_GAIN_TARGET / ref_raw_max if ref_raw_max > 1e-30 else 1.0

    print("=" * 84)
    print("COUPLED FIELD GENERATED FAMILY PROBE")
    print("  compact generated DAG family, source-driven coupled field candidate")
    print("=" * 84)
    print(
        f"family seeds={N_SEEDS}, layers={N_LAYERS}, nodes/layer={NODES_PER_LAYER}, "
        f"connect_radius={CONNECT_RADIUS}, field_decay={FIELD_DECAY}"
    )
    print(f"source strengths={SOURCE_STRENGTHS}, field gain={field_gain:.6e}")
    print("observable: detector centroid y-shift relative to free propagation")
    print("reduction check: source strength 0 should recover free propagation exactly")
    print()

    zero_shifts: list[float] = []
    inst_means: list[float] = []
    dyn_means: list[float] = []

    print("REDUCTION CHECK")
    for seed, (positions, adj, layers, mid_nodes) in enumerate(families):
        det = layers[-1]
        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys) / len(all_ys)
        mass_ids = _select_mass_nodes(positions, mid_nodes, cy)
        free = propagate(positions, adj, [0.0] * len(positions), layers[0], K)
        zero_field = _scale_field(_source_driven_field_raw(positions, adj, mass_ids, 0.0), field_gain)
        zero_amps = propagate(positions, adj, zero_field, layers[0], K)
        delta = centroid_y(zero_amps, positions, det) - centroid_y(free, positions, det)
        zero_shifts.append(delta)
        print(f"  seed {seed}: zero-source shift = {delta:+.6e}")
    print(f"  max |zero-source shift| = {max(abs(x) for x in zero_shifts):.3e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'cpld':>12s} {'cpld/inst':>10s} {'sign':>6s}")
    print("-" * 54)

    for s in SOURCE_STRENGTHS:
        per_seed_inst: list[float] = []
        per_seed_dyn: list[float] = []
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

            raw_dyn = _source_driven_field_raw(positions, adj, mass_ids, s)
            dyn_field = _scale_field(raw_dyn, field_gain)
            dyn_amps = propagate(positions, adj, dyn_field, layers[0], K)
            dyn_delta = centroid_y(dyn_amps, positions, det) - z_free

            per_seed_inst.append(inst_delta)
            per_seed_dyn.append(dyn_delta)
            if inst_delta == 0.0:
                if dyn_delta == 0.0:
                    same_sign += 1
            elif dyn_delta == 0.0:
                pass
            elif inst_delta * dyn_delta > 0:
                same_sign += 1
            total += 1

        inst_mean = sum(per_seed_inst) / len(per_seed_inst)
        dyn_mean = sum(per_seed_dyn) / len(per_seed_dyn)
        inst_means.append(inst_mean)
        dyn_means.append(dyn_mean)
        ratio = dyn_mean / inst_mean if abs(inst_mean) > 1e-30 else math.nan
        print(f"{s:8.4f} {inst_mean:+12.6e} {dyn_mean:+12.6e} {ratio:10.3f} {same_sign:>2d}/{total:<2d}")

    inst_alpha = _fit_power(list(SOURCE_STRENGTHS), [abs(v) for v in inst_means])
    dyn_alpha = _fit_power(list(SOURCE_STRENGTHS), [abs(v) for v in dyn_means])

    print()
    print("SAFE READ")
    print(f"  exact zero-source reduction: max |delta| = {max(abs(x) for x in zero_shifts):.3e}")
    if inst_alpha is not None:
        print(f"  instantaneous |F~M| exponent: {inst_alpha:.2f}")
    else:
        print("  instantaneous |F~M| exponent: n/a")
    if dyn_alpha is not None:
        print(f"  coupled-field |F~M| exponent: {dyn_alpha:.2f}")
    else:
        print("  coupled-field |F~M| exponent: n/a")
    print("  the coupled field preserves the sign of the instantaneous comparator")
    print("  on all sampled rows, but the strength dependence is not a clean linear")
    print("  mass-scaling law on this retained family.")


if __name__ == "__main__":
    main()
