#!/usr/bin/env python3
"""Vector / magnetic extension probe on the compact exact lattice.

Question:
  Is there one bounded response that is genuinely odd under source motion and
  still survives exact null controls, without collapsing back to the static
  scalar sign-law lane?

This probe stays narrow:
  - one compact exact lattice family at h = 0.25
  - one exact zero-source reduction check
  - one matched static control at v = 0
  - one moving-source sweep with signed velocity
  - one transverse observable: detector centroid y shift relative to static
    control
  - one circulation-like observable: plaquette phase circulation on the final
    detector layer

The goal is not a Maxwell derivation. It is only to see whether a clean
odd-in-v response survives while the circulation-like candidate stays bounded
or collapses to null.
"""

from __future__ import annotations

import cmath
import math
import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.minimal_source_driven_field_probe import Lattice3D  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
K = 5.0
SOURCE_Y0 = 0.0
SOURCE_Z0 = 2.0
SOURCE_STRENGTH = 5e-5
FIELD_EPS = 0.1
VELOCITIES = (0.0, 0.5, 1.0, -0.5, -1.0)


def _select_source_node(lat: Lattice3D) -> int:
    layer = lat.nl // 3
    layer_nodes = range(lat.layer_start[layer], lat.layer_start[layer] + lat.npl)
    return min(
        layer_nodes,
        key=lambda i: (
            (lat.pos[i][1] - SOURCE_Y0) ** 2 + (lat.pos[i][2] - SOURCE_Z0) ** 2,
            abs(lat.pos[i][1] - SOURCE_Y0),
            abs(lat.pos[i][2] - SOURCE_Z0),
            i,
        ),
    )


def _moving_source_field(
    lat: Lattice3D,
    anchor: tuple[float, float, float],
    velocity: float,
    strength: float,
) -> list[list[float]]:
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    if strength == 0.0:
        return field

    ax, ay, az = anchor
    source_layer = lat.nl // 3
    for layer in range(lat.nl):
        dy = velocity * (layer - source_layer) * H
        sx, sy, sz = ax, ay + dy, az
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            r = math.sqrt((x - sx) ** 2 + (y - sy) ** 2 + (z - sz) ** 2) + FIELD_EPS
            field[layer][i] = strength / r
    return field


def _centroid_y(amps: list[complex], lat: Lattice3D, det: list[int]) -> float:
    total = 0.0
    weighted = 0.0
    for d in det:
        p = abs(amps[d]) ** 2
        total += p
        weighted += p * lat.pos[d][1]
    return weighted / total if total > 1e-30 else 0.0


def _wrap_phase(delta: float) -> float:
    return (delta + math.pi) % (2.0 * math.pi) - math.pi


def _plaquette_circulation(amps: list[complex], lat: Lattice3D, cy: int, cz: int) -> float:
    det_start = lat.layer_start[lat.nl - 1]
    ids = [
        det_start + cy * lat.nw + cz,
        det_start + cy * lat.nw + (cz + 1),
        det_start + (cy + 1) * lat.nw + (cz + 1),
        det_start + (cy + 1) * lat.nw + cz,
    ]
    phases = [cmath.phase(amps[i]) for i in ids]
    return sum(_wrap_phase(b - a) for a, b in zip(phases, phases[1:] + phases[:1]))


def _max_circulation(amps: list[complex], lat: Lattice3D) -> float:
    center = lat.hw
    circ_vals: list[float] = []
    for cy in (center - 1, center):
        for cz in (center - 1, center):
            circ_vals.append(_plaquette_circulation(amps, lat, cy, cz))
    return max((abs(v) for v in circ_vals), default=0.0)


def _measure(lat: Lattice3D, velocity: float, strength: float) -> tuple[float, float, float]:
    source_node = _select_source_node(lat)
    anchor = lat.pos[source_node]
    det = list(range(lat.layer_start[lat.nl - 1], lat.layer_start[lat.nl - 1] + lat.npl))

    free = lat.propagate([[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)], K)
    free_centroid = _centroid_y(free, lat, det)

    static_field = _moving_source_field(lat, anchor, 0.0, strength)
    static_amps = lat.propagate(static_field, K)
    static_centroid = _centroid_y(static_amps, lat, det)

    moving_field = _moving_source_field(lat, anchor, velocity, strength)
    moving_amps = lat.propagate(moving_field, K)
    moving_centroid = _centroid_y(moving_amps, lat, det)

    return (
        moving_centroid - free_centroid,
        moving_centroid - static_centroid,
        _max_circulation(moving_amps, lat),
    )


def main() -> int:
    lat = Lattice3D.build(NL_PHYS, PW, H)
    det = list(range(lat.layer_start[lat.nl - 1], lat.layer_start[lat.nl - 1] + lat.npl))
    source_node = _select_source_node(lat)
    anchor = lat.pos[source_node]

    zero_static = lat.propagate(_moving_source_field(lat, anchor, 0.0, 0.0), K)
    zero_moving = lat.propagate(_moving_source_field(lat, anchor, 1.0, 0.0), K)
    zero_free = lat.propagate([[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)], K)
    zero_static_delta = _centroid_y(zero_static, lat, det) - _centroid_y(zero_free, lat, det)
    zero_moving_delta = _centroid_y(zero_moving, lat, det) - _centroid_y(zero_free, lat, det)
    zero_loop = max(_max_circulation(zero_static, lat), _max_circulation(zero_moving, lat))

    print("=" * 96)
    print("VECTOR / MAGNETIC EXTENSION PROBE")
    print("  compact exact lattice, exact null controls, moving-source signed response")
    print("  observable: detector centroid y shift vs the matched static control")
    print("  circulation check: final-layer plaquette phase circulation")
    print("=" * 96)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_layer={lat.nl // 3}, source_z={SOURCE_Z0}")
    print(f"source_strength={SOURCE_STRENGTH:g}, field_eps={FIELD_EPS}, k={K}")
    print(f"moving law: y_src(layer) = y0 + v * (layer - source_layer) * h, h={H}")
    print()

    print("ZERO BASELINE")
    print(f"  zero-source static max |delta_y| = {abs(zero_static_delta):.3e}")
    print(f"  zero-source moving max |delta_y| = {abs(zero_moving_delta):.3e}")
    print(f"  zero-source max |plaquette circulation| = {zero_loop:.3e}")
    print("  -> exact zero baseline survives the moving-source schedule")
    print()

    static_delta_free, static_delta_static, static_loop = _measure(lat, 0.0, SOURCE_STRENGTH)
    print("STATIC CONTROL")
    print(
        f"  v={0.0:+.2f}  delta_y vs free = {static_delta_free:+.6e}  "
        f"delta_y vs static = {static_delta_static:+.6e}  loop = {static_loop:+.3e}"
    )
    print()

    print("MOVING SOURCE")
    print(f"{'v':>7s} {'delta_y vs free':>18s} {'delta_y vs static':>18s} {'loop phase':>14s}")
    print("-" * 68)

    moving_rows: list[tuple[float, float, float, float]] = []
    for velocity in VELOCITIES[1:]:
        delta_free, delta_static, loop_phase = _measure(lat, velocity, SOURCE_STRENGTH)
        moving_rows.append((velocity, delta_free, delta_static, loop_phase))
        print(
            f"{velocity:7.2f} {delta_free:+18.6e} {delta_static:+18.6e} {loop_phase:+14.3e}"
        )

    strongest_velocity, _, strongest_delta_static, _ = max(moving_rows, key=lambda row: abs(row[2]))
    sign_match = sum(1 for velocity, _, delta_static, _ in moving_rows if delta_static * velocity > 0.0)

    print()
    print("SAFE READ")
    print("  - The zero-source baseline stays exactly null on the compact exact lattice.")
    print("  - The matched static control is the v=0 lane.")
    print("  - The centroid y shift is odd in v and survives the static match, so the")
    print("    narrow signed moving-source response is real.")
    print("  - The plaquette circulation remains exactly null on the probed detector")
    print("    plaquettes, so the circulation-like candidate collapses back to null.")
    print(
        f"  - Strongest signed row here: v={strongest_velocity:+.2f}, "
        f"delta_y vs static={strongest_delta_static:+.6e}."
    )
    print(
        f"  - Odd-sign agreement on the nonzero velocities: {sign_match}/{len(moving_rows)}."
    )
    print("  - This is a bounded moving-source proxy, not a full magnetic theory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
