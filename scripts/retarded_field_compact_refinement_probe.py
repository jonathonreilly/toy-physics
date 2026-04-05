#!/usr/bin/env python3
"""Retarded-field compact refinement probe on retained generated DAG families.

Goal:
  test whether the retarded-vs-instantaneous deflection split survives one
  compact refinement or alternate retained family without collapsing into a
  pure scheduling artifact.

Observable:
  detector centroid shift under an instantaneous field vs a finite-speed
  retarded field.

Reduction check:
  the instantaneous row is the c = inf limit. The finite-speed row should
  reduce toward it as retardation is removed.

This is intentionally narrow. It does not try to be a full wave theory.
It is a compact causality / scheduling smoke probe on a retained DAG family.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.causal_field_gravity import centroid_y, generate_3d_dag, propagate  # noqa: E402


FIELD_STRENGTH = 1.0e-4
K_BAND = (3.0, 5.0, 7.0)
N_SEEDS = 6
MASS_COUNT = 5
RETARDED_C = 4.0
TARGET_BS = (1, 2, 3, 4, 6)


@dataclass(frozen=True)
class Family:
    name: str
    n_layers: int
    nodes_per_layer: int
    y_range: float
    connect_radius: float


FAMILIES = (
    Family("compact", n_layers=16, nodes_per_layer=20, y_range=10.0, connect_radius=3.2),
    Family("refined", n_layers=16, nodes_per_layer=28, y_range=10.0, connect_radius=3.2),
)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    return statistics.stdev(values) / math.sqrt(len(values))


def _select_mass_nodes(layer_nodes: list[int], positions, target_y: float, count: int) -> list[int]:
    ranked = sorted(
        layer_nodes,
        key=lambda i: (abs(positions[i][1] - target_y), abs(positions[i][2]), i),
    )
    return ranked[:count] if len(ranked) >= count else []


def _instantaneous_field(positions, mass_ids: list[int]) -> list[float]:
    field = [0.0] * len(positions)
    for m in mass_ids:
        mx, my, mz = positions[m]
        for i, (x, y, z) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            field[i] += FIELD_STRENGTH / r
    return field


def _retarded_field(positions, arrival: list[float], mass_ids: list[int], c: float) -> list[float]:
    if math.isinf(c):
        return _instantaneous_field(positions, mass_ids)

    field = [0.0] * len(positions)
    for m in mass_ids:
        mx, my, mz = positions[m]
        tm = arrival[m]
        for i, (x, y, z) in enumerate(positions):
            r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + 0.1
            if arrival[i] >= tm + (r / c):
                field[i] += FIELD_STRENGTH / r
    return field


def _shift_for_field(positions, adj, layers, field, k: float) -> float:
    src = layers[0]
    det = layers[-1]
    free = propagate(positions, adj, [0.0] * len(positions), src, k)
    amps = propagate(positions, adj, field, src, k)
    return centroid_y(amps, positions, det) - centroid_y(free, positions, det)


def _measure_seed(
    family: Family,
    seed: int,
    b: int,
) -> tuple[float, float] | None:
    positions, adj, layer_indices = generate_3d_dag(
        n_layers=family.n_layers,
        nodes_per_layer=family.nodes_per_layer,
        yz_range=family.y_range,
        connect_radius=family.connect_radius,
        rng_seed=seed * 19 + 7,
    )
    if len(layer_indices) <= 2:
        return None

    # The layer index itself is the causal arrival proxy for this compact probe.
    arrival = [pos[0] for pos in positions]
    mid = len(layer_indices) // 2
    layer_nodes = layer_indices[mid]
    if not layer_nodes:
        return None

    ys = [y for _, y, _ in positions]
    cy = sum(ys) / len(ys)
    mass_ids = _select_mass_nodes(layer_nodes, positions, cy + b, MASS_COUNT)
    if len(mass_ids) < MASS_COUNT:
        return None

    inst_field = _instantaneous_field(positions, mass_ids)
    ret_field = _retarded_field(positions, arrival, mass_ids, RETARDED_C)

    inst_shifts = []
    ret_shifts = []
    for k in K_BAND:
        inst_shifts.append(_shift_for_field(positions, adj, layer_indices, inst_field, k))
        ret_shifts.append(_shift_for_field(positions, adj, layer_indices, ret_field, k))

    return _mean(inst_shifts), _mean(ret_shifts)


def _measure_family(family: Family) -> dict[int, dict[str, list[float]]]:
    rows: dict[int, dict[str, list[float]]] = {
        b: {"inst": [], "ret": []} for b in TARGET_BS
    }
    for seed in range(N_SEEDS):
        for b in TARGET_BS:
            measured = _measure_seed(family, seed, b)
            if measured is None:
                continue
            inst, ret = measured
            rows[b]["inst"].append(inst)
            rows[b]["ret"].append(ret)
    return rows


def _print_family(family: Family, rows: dict[int, dict[str, list[float]]]) -> tuple[int, int]:
    print(f"[{family.name}]")
    print(
        f"  family: layers={family.n_layers}, nodes/layer={family.nodes_per_layer}, "
        f"y_range={family.y_range}, connect_radius={family.connect_radius}"
    )
    print(f"  {'b':>3s}  {'inst':>10s}  {'ret':>10s}  {'split':>10s}  {'ret/inst':>9s}  {'SE':>8s}")
    print(f"  {'-' * 62}")

    survive_rows = 0
    total_rows = 0
    for b in TARGET_BS:
        inst_vals = rows[b]["inst"]
        ret_vals = rows[b]["ret"]
        if not inst_vals or not ret_vals:
            print(f"  {b:3d}  {'FAIL':>10s}")
            continue

        inst = _mean(inst_vals)
        ret = _mean(ret_vals)
        split = inst - ret
        ratio = ret / inst if abs(inst) > 1e-30 else float("nan")
        se = _se([i - r for i, r in zip(inst_vals, ret_vals)])
        print(f"  {b:3d}  {inst:+10.6e}  {ret:+10.6e}  {split:+10.6e}  {ratio:9.4f}  {se:8.2e}")
        total_rows += 1
        if ret < inst:
            survive_rows += 1

    if total_rows:
        split_vals = [
            _mean(rows[b]["inst"]) - _mean(rows[b]["ret"])
            for b in TARGET_BS
            if rows[b]["inst"] and rows[b]["ret"]
        ]
        mean_split = _mean(split_vals)
        print()
        print(f"  mean split (inst-ret): {mean_split:+.6e}")
        print(f"  retarded below instantaneous on {survive_rows}/{total_rows} b-rows")
    print()
    return survive_rows, total_rows


def main() -> None:
    print("=" * 88)
    print("RETARDED FIELD COMPACT REFINEMENT PROBE")
    print("  Instantaneous vs finite-speed retarded field on retained DAG families")
    print("  Observable: detector centroid shift")
    print("  Reduction check: instantaneous row is the c=inf limit")
    print("=" * 88)
    print()
    print(f"seeds={N_SEEDS}, k-band={K_BAND}, mass_count={MASS_COUNT}, retarded_c={RETARDED_C}")
    print(f"b-targets={TARGET_BS}")
    print()

    overall_survive = 0
    overall_rows = 0
    for family in FAMILIES:
        rows = _measure_family(family)
        survive_rows, total_rows = _print_family(family, rows)
        overall_survive += survive_rows
        overall_rows += total_rows

    print("=" * 88)
    print("SAFE READ")
    if overall_rows and overall_survive == overall_rows:
        print(
            "  - The retarded field remains below the instantaneous field on every"
            " retained b-row in both the compact and refined families."
        )
        print(
            "  - The split therefore survives one compact refinement and does not"
            " collapse to a pure scheduling artifact in this replay."
        )
    elif overall_rows and overall_survive > 0:
        print(
            "  - The retarded field still differs from the instantaneous field on"
            " the retained families, but the split is not uniform across all rows."
        )
        print(
            "  - Treat this as a partial survival, not a full refinement-stable result."
        )
    else:
        print(
            "  - No stable retarded-vs-instantaneous split survived the compact"
            " refinement replay."
        )
        print(
            "  - Treat the retarded-field lane as a clean negative at this family."
        )


if __name__ == "__main__":
    main()
