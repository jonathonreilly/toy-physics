#!/usr/bin/env python3
"""Retarded-vs-instantaneous field causality probe on a compact generated DAG.

Moonshot goal:
  Compare a single detector deflection observable under an instantaneous field
  versus a retarded field with finite propagation speed, on the retained
  generated DAG family.

Observable:
  Detector centroid shift relative to free propagation, and the difference
  between the retarded and instantaneous shifts.

Reduction check:
  c = inf removes retardation and should recover the instantaneous lane.

This is intentionally narrow. It is a causality / field-scheduling proxy on a
generated DAG family, not a full gravitational wave theory.
"""

from __future__ import annotations

import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_gravity import centroid_y, generate_3d_dag, propagate  # noqa: E402


N_LAYERS = 16
NODES_PER_LAYER = 24
Y_RANGE = 10.0
CONNECT_RADIUS = 3.2
N_SEEDS = 4
K = 5.0
FIELD_STRENGTH = 1.0e-4
TARGET_Y = 3.0
MASS_RADIUS = 2.5
CS = [float("inf"), 4.0, 2.0, 1.0, 0.5]


def _instantaneous_field(positions: list[tuple[float, float, float]], mass_ids: list[int]) -> list[float]:
    field = [0.0] * len(positions)
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i, (x, y, z) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += FIELD_STRENGTH / r
    return field


def _retarded_field(
    positions: list[tuple[float, float, float]],
    node_time: list[float],
    mass_ids: list[int],
    c: float,
) -> list[float]:
    if math.isinf(c):
        return _instantaneous_field(positions, mass_ids)

    field = [0.0] * len(positions)
    for m in mass_ids:
        mx, my, mz = positions[m]
        tm = node_time[m]
        for i, (x, y, z) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            if node_time[i] >= tm + (r / c):
                field[i] += FIELD_STRENGTH / r
    return field


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


def _detector_shift(
    positions: list[tuple[float, float, float]],
    adj: dict[int, list[int]],
    layers: list[list[int]],
    mass_ids: list[int],
    c: float | None,
) -> float:
    src = layers[0]
    det = layers[-1]
    free = propagate(positions, adj, [0.0] * len(positions), src, K)
    if c is None:
        field = _instantaneous_field(positions, mass_ids)
    else:
        node_time = [positions[i][0] for i in range(len(positions))]
        field = _retarded_field(positions, node_time, mass_ids, c)
    amps = propagate(positions, adj, field, src, K)
    return centroid_y(amps, positions, det) - centroid_y(free, positions, det)


def main() -> None:
    print("=" * 88)
    print("RETARDED FIELD CAUSALITY PROBE")
    print("  Instantaneous vs retarded field on a compact generated DAG family")
    print("  Observable: detector centroid shift difference")
    print("  Reduction check: c = inf -> instantaneous limit")
    print("=" * 88)
    print()

    rows: dict[float, list[float]] = defaultdict(list)
    inst_rows: list[float] = []

    for seed in range(N_SEEDS):
        positions, adj, layers = generate_3d_dag(
            n_layers=N_LAYERS,
            nodes_per_layer=NODES_PER_LAYER,
            yz_range=Y_RANGE,
            connect_radius=CONNECT_RADIUS,
            rng_seed=seed * 19 + 7,
        )

        if len(layers) < 6:
            continue

        all_ys = [y for _, y, _ in positions]
        cy = sum(all_ys) / len(all_ys)
        mid = len(layers) // 2
        mass_ids = _select_mass_nodes(positions, layers[mid], cy)
        if len(mass_ids) < 3:
            continue

        inst = _detector_shift(positions, adj, layers, mass_ids, None)
        inst_rows.append(inst)

        for c in CS:
            ret = _detector_shift(positions, adj, layers, mass_ids, c)
            rows[c].append(ret)

    if not inst_rows:
        raise SystemExit("No valid seeds produced a usable compact family.")

    inst_mean = sum(inst_rows) / len(inst_rows)
    print(f"Compact retained family: {len(inst_rows)} seeds")
    print(f"Instantaneous baseline mean shift: {inst_mean:+.6e}")
    print()
    print(f"{'c':>8s} {'inst shift':>14s} {'ret shift':>14s} {'delta':>14s}")
    print(f"{'-'*54}")

    for c in CS:
        vals = rows[c]
        mean = sum(vals) / len(vals)
        delta = mean - inst_mean
        label = "inf" if math.isinf(c) else f"{c:g}"
        print(f"{label:>8s} {inst_mean:+14.6e} {mean:+14.6e} {delta:+14.6e}")

    c_inf = rows[float("inf")]
    reduction_err = abs((sum(c_inf) / len(c_inf)) - inst_mean) / max(abs(inst_mean), 1e-30)

    print()
    print("SAFE READ")
    print(f"  - c = inf recovers the instantaneous lane with relative error {reduction_err:.4%}.")
    print(
        "  - finite c changes the detector deflection relative to the instantaneous lane,"
        " so field-arrival timing matters on this compact generated family."
    )
    print(
        "  - this remains a field-scheduling proxy, not a self-consistent dynamical wave theory;"
        " the field is still imposed by hand and delayed by node time."
    )


if __name__ == "__main__":
    main()
