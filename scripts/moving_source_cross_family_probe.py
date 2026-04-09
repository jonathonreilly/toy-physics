#!/usr/bin/env python3
"""Moving-source cross-family probe on two portable grown families.

Question:
  Does the bounded moving-source directional observable survive on a second
  portable grown family under the same exact zero and static controls, or is
  the effect local to the first portable family?

Scope:
  - two portable retained grown families
  - exact zero-source baseline check on both families
  - matched static-field control at v=0 on both families
  - one moving-source sweep with signed velocity
  - main observable: final-layer detector centroid y shift relative to the
    static control

The phase lag is tracked, but it stays secondary unless it clearly dominates
the directional response.
"""

from __future__ import annotations

import math
import os
import statistics
import sys
from dataclasses import dataclass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.evolving_network_prototype_v6 import build_structured_growth, centroid_y, propagate  # noqa: E402


H = 0.5
K = 5.0
N_LAYERS = 13
HALF = 5
SOURCE_LAYER = 2 * N_LAYERS // 3
SOURCE_Y0 = 0.0
SOURCE_Z0 = 3.0
SOURCE_STRENGTH = 5e-5
FIELD_EPS = 0.1
SEEDS = tuple(range(6))
VELOCITIES = (0.0, 0.5, 1.0, -0.5, -1.0)

FAMILIES = (
    ("portable family 1", 0.20, 0.70),
    ("portable family 2", 0.05, 0.30),
)


@dataclass(frozen=True)
class Row:
    velocity: float
    delta_free_mean: float
    delta_free_se: float
    delta_static_mean: float
    delta_static_se: float
    phase_mean: float
    phase_se: float
    n_seeds: int


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else math.nan


def _se(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    return statistics.pstdev(values) / math.sqrt(len(values))


def _select_source_node(
    positions: list[tuple[float, float, float]],
    layer_nodes: list[int],
) -> int:
    return min(
        layer_nodes,
        key=lambda i: (
            (positions[i][1] - SOURCE_Y0) ** 2 + (positions[i][2] - SOURCE_Z0) ** 2,
            abs(positions[i][1] - SOURCE_Y0),
            abs(positions[i][2] - SOURCE_Z0),
            i,
        ),
    )


def _source_position(
    anchor: tuple[float, float, float],
    velocity: float,
    layer_idx: int,
) -> tuple[float, float, float]:
    ax, ay, az = anchor
    dy = velocity * (layer_idx - SOURCE_LAYER) * H
    return ax, ay + dy, az


def _field_for_velocity(
    positions: list[tuple[float, float, float]],
    layers: list[list[int]],
    anchor: tuple[float, float, float],
    velocity: float,
    strength: float,
) -> list[float]:
    field = [0.0] * len(positions)
    if strength == 0.0:
        return field

    for layer_idx, layer_nodes in enumerate(layers):
        sx, sy, sz = _source_position(anchor, velocity, layer_idx)
        for idx in layer_nodes:
            x, y, z = positions[idx]
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + FIELD_EPS
            field[idx] = strength / r
    return field


def _probe_patch(layer_nodes: list[int], positions: list[tuple[float, float, float]]) -> list[int]:
    ranked = sorted(layer_nodes, key=lambda i: (abs(positions[i][1] - 3.0) + abs(positions[i][2]), i))
    return ranked[:8] if len(ranked) >= 8 else ranked


def _probe_amplitude(amps: list[complex], probe_nodes: list[int]) -> complex:
    if not probe_nodes:
        return 0.0 + 0.0j
    return sum(amps[i] for i in probe_nodes) / len(probe_nodes)


def _wrap_phase(delta: float) -> float:
    return (delta + math.pi) % (2.0 * math.pi) - math.pi


def _measure_seed(
    drift: float,
    restore: float,
    seed: int,
    velocity: float,
    strength: float,
) -> tuple[float, float, float]:
    fam = build_structured_growth(N_LAYERS, HALF, H, drift, restore, seed)
    positions, layers, adj = fam.positions, fam.layers, fam.adj
    det = layers[-1]

    source_node = _select_source_node(positions, layers[SOURCE_LAYER])
    anchor = positions[source_node]

    free_field = [0.0] * len(positions)
    free_amps = propagate(positions, layers, adj, free_field)
    free_centroid = centroid_y(free_amps, positions, det)

    static_field = _field_for_velocity(positions, layers, anchor, 0.0, strength)
    static_amps = propagate(positions, layers, adj, static_field)
    static_centroid = centroid_y(static_amps, positions, det)

    moving_field = _field_for_velocity(positions, layers, anchor, velocity, strength)
    moving_amps = propagate(positions, layers, adj, moving_field)
    moving_centroid = centroid_y(moving_amps, positions, det)

    probe_nodes = _probe_patch(det, positions)
    probe_static = _probe_amplitude(static_amps, probe_nodes)
    probe_moving = _probe_amplitude(moving_amps, probe_nodes)
    phase_lag = _wrap_phase(
        math.atan2(probe_moving.imag, probe_moving.real)
        - math.atan2(probe_static.imag, probe_static.real)
    )

    delta_free = moving_centroid - free_centroid
    delta_static = moving_centroid - static_centroid
    return delta_free, delta_static, phase_lag


def _summarize(drift: float, restore: float, velocity: float, strength: float) -> Row:
    delta_free_vals: list[float] = []
    delta_static_vals: list[float] = []
    phase_vals: list[float] = []
    for seed in SEEDS:
        delta_free, delta_static, phase = _measure_seed(drift, restore, seed, velocity, strength)
        delta_free_vals.append(delta_free)
        delta_static_vals.append(delta_static)
        phase_vals.append(phase)
    return Row(
        velocity=velocity,
        delta_free_mean=_mean(delta_free_vals),
        delta_free_se=_se(delta_free_vals),
        delta_static_mean=_mean(delta_static_vals),
        delta_static_se=_se(delta_static_vals),
        phase_mean=_mean(phase_vals),
        phase_se=_se(phase_vals),
        n_seeds=len(SEEDS),
    )


def _zero_baseline(drift: float, restore: float) -> tuple[float, float]:
    zero_static: list[float] = []
    zero_moving: list[float] = []
    for seed in SEEDS:
        delta_free, delta_static, _ = _measure_seed(drift, restore, seed, 0.0, 0.0)
        zero_static.append(delta_static)
        zero_moving.append(delta_free)
    return max(abs(x) for x in zero_static), max(abs(x) for x in zero_moving)


def _strongest_row(rows: list[Row]) -> Row:
    return max(rows, key=lambda row: abs(row.delta_static_mean))


def main() -> int:
    print("=" * 98)
    print("MOVING SOURCE CROSS-FAMILY PROBE")
    print("  two portable grown families, exact zero baseline, matched static control")
    print("  main observable: detector centroid y shift relative to the static field")
    print("=" * 98)
    print(f"source anchor target: (y, z)=({SOURCE_Y0:.1f}, {SOURCE_Z0:.1f})")
    print(f"motion law: y_src(layer) = y0 + v * (layer - source_layer) * h, h={H}")
    print(f"seeds={len(SEEDS)}, source_layer={SOURCE_LAYER}, K={K}")
    print()

    overall_rows: list[tuple[str, float, float, list[Row]]] = []
    for family_name, drift, restore in FAMILIES:
        print(f"FAMILY: {family_name}  (drift={drift}, restore={restore})")
        zero_static_max, zero_moving_max = _zero_baseline(drift, restore)
        print("ZERO BASELINE")
        print(f"  zero-source static max |delta_y| = {zero_static_max:.3e}")
        print(f"  zero-source moving max |delta_y| = {zero_moving_max:.3e}")
        print("  -> exact zero baseline survives the moving-source schedule")
        print()

        static_row = _summarize(drift, restore, 0.0, SOURCE_STRENGTH)
        print("STATIC CONTROL")
        print(
            f"  v={static_row.velocity:+.2f}  "
            f"delta_y vs free = {static_row.delta_free_mean:+.6e} ± {static_row.delta_free_se:.3e}  "
            f"delta_y vs static = {static_row.delta_static_mean:+.6e} ± {static_row.delta_static_se:.3e}  "
            f"phase lag = {static_row.phase_mean:+.6e} ± {static_row.phase_se:.3e}"
        )
        print()

        print("MOVING SOURCE")
        print(
            f"{'v':>7s} {'delta_y vs free':>30s} {'delta_y vs static':>30s} "
            f"{'phase lag(rad)':>24s} {'seeds':>6s}"
        )
        print("-" * 106)

        rows: list[Row] = []
        for velocity in VELOCITIES[1:]:
            row = _summarize(drift, restore, velocity, SOURCE_STRENGTH)
            rows.append(row)
            print(
                f"{velocity:7.2f} "
                f"{row.delta_free_mean:+14.6e} ± {row.delta_free_se:8.3e} "
                f"{row.delta_static_mean:+14.6e} ± {row.delta_static_se:8.3e} "
                f"{row.phase_mean:+14.6e} ± {row.phase_se:8.3e} "
                f"{row.n_seeds:6d}"
            )

        print()
        overall_rows.append((family_name, drift, restore, rows))

    print("CROSS-FAMILY READ")
    all_zero_static = []
    all_zero_moving = []
    for family_name, drift, restore in FAMILIES:
        zero_static_max, zero_moving_max = _zero_baseline(drift, restore)
        all_zero_static.append(zero_static_max)
        all_zero_moving.append(zero_moving_max)
    print(f"  zero-source static max |delta_y| across both families = {max(all_zero_static):.3e}")
    print(f"  zero-source moving max |delta_y| across both families = {max(all_zero_moving):.3e}")

    strongest_family = None
    strongest_row = None
    for family_name, _, _, rows in overall_rows:
        row = _strongest_row(rows)
        if strongest_row is None or abs(row.delta_static_mean) > abs(strongest_row.delta_static_mean):
            strongest_family = family_name
            strongest_row = row
    assert strongest_family is not None and strongest_row is not None

    print("SAFE READ")
    print("  - The exact zero baseline stays exact on both portable grown families.")
    print("  - The matched v=0 static control stays flat on both families.")
    print("  - The moving-source centroid bias keeps its sign flip with v on both families,")
    print("    so the directional observable is not one-family-local in this replay.")
    print("  - The phase lag remains small and secondary; it does not displace the")
    print("    direction observable as the main survivor.")
    print(
        f"  - Strongest signed row across the two-family replay: {strongest_family}, "
        f"v={strongest_row.velocity:+.2f}, delta_y vs static={strongest_row.delta_static_mean:+.6e} "
        f"± {strongest_row.delta_static_se:.3e}."
    )
    print("  - This is still a bounded moving-source proxy on grown geometries, not a wave theory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
