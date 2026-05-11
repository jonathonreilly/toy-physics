#!/usr/bin/env python3
"""Source-resolved Green-pocket probe on a small exact lattice.

Moonshot goal:
  Try a self-generated field architecture that is distinct from the telegraph
  recurrence and the edge-carried transport rule, while still preserving the
  weak-field lane on an exact lattice.

This probe is intentionally narrow:
  - one exact lattice family, kept small enough for a quick feasibility check
  - one source-resolved Green-like kernel built from a fixed source cluster
  - one comparison against the instantaneous 1/r comparator
  - one reduction check: zero source must recover free propagation exactly

The architecture is linear in source strength, so the hard question is not
whether the response exists, but whether it keeps the sign and approximate
Newtonian mass scaling while remaining nontrivially sized.
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


# Small exact lattice for a fast feasibility probe.
H = 0.5
NL_PHYS = 20
PW = 3
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
FIELD_TARGET_MAX = 0.02
GREEN_EPS = 0.5
GREEN_MU = 0.08


def _source_cluster_nodes(lat: m.Lattice3D) -> list[int]:
    gl = lat.nl // 3
    src_y = lat.hw
    src_z = lat.hw + round(m.SOURCE_Z / lat.h)
    nodes: list[int] = []
    for dy, dz in SOURCE_CLUSTER:
        y = src_y + dy
        z = src_z + dz
        if 0 <= y < lat.nw and 0 <= z < lat.nw:
            nodes.append(lat.nmap[(gl, y - lat.hw, z - lat.hw)])
    return nodes


def _source_resolved_green_field(
    lat: m.Lattice3D,
    source_strength: float,
    source_nodes: list[int],
) -> list[list[float]]:
    """Static source-resolved Green-like field on the exact lattice."""
    if not source_nodes:
        return [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    source_pos = [lat.pos[i] for i in source_nodes]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for mx, my, mz in source_pos:
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val / len(source_pos)
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row)


def main() -> None:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 84)
    print("SOURCE-RESOLVED EXACT GREEN POCKET")
    print("  small exact lattice, source-resolved Green-like field")
    print("  comparison: source-resolved field vs instantaneous 1/r field")
    print("=" * 84)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print()

    ref_raw = _source_resolved_green_field(lat, max(m.SOURCE_STRENGTHS), source_nodes)
    ref_max = _field_abs_max(ref_raw)
    gain = FIELD_TARGET_MAX / ref_max if ref_max > 1e-30 else 1.0

    zero_dyn = _source_resolved_green_field(lat, 0.0, source_nodes)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_dyn], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'green':>12s} {'green/inst':>11s} {'max|f|':>12s}")
    print("-" * 70)

    inst_vals: list[float] = []
    green_vals: list[float] = []
    ratios: list[float] = []

    for s in m.SOURCE_STRENGTHS:
        inst_field = m._instantaneous_field_layers(lat, s, m.SOURCE_Z)
        green_field = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, source_nodes)]

        inst_amps = lat.propagate(inst_field, m.K)
        green_amps = lat.propagate(green_field, m.K)

        inst_delta = m._centroid_z(inst_amps, lat) - z_free
        green_delta = m._centroid_z(green_amps, lat) - z_free
        ratio = green_delta / inst_delta if abs(inst_delta) > 1e-30 else float("nan")

        inst_vals.append(inst_delta)
        green_vals.append(green_delta)
        ratios.append(abs(ratio))

        print(
            f"{s:8.4f} {inst_delta:+12.6e} {green_delta:+12.6e} "
            f"{ratio:11.3f} {max(abs(v) for row in green_field for v in row):12.6e}"
        )

    inst_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), inst_vals)
    green_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), green_vals)
    toward = sum(1 for v in green_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  green-kernel F~M exponent: {green_alpha:.2f}" if green_alpha is not None else "  green-kernel F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(green_vals)}")
    print(f"  mean |green/inst| ratio: {mean_ratio:.3f}")
    print("  this is a feasibility pocket, not yet a full-size exact-lattice theory")

    # Hard-bar assertions on the load-bearing observables.
    # Per docs/SOURCE_RESOLVED_EXACT_GREEN_POCKET_NOTE.md "Hard-bar runner assertions" table.
    print()
    print("HARD-BAR ASSERTIONS")
    n_pass = 0
    n_fail = 0

    # Bar 1: zero-source reduction at machine precision.
    if abs(zero_delta) <= 1e-12:
        print(f"  PASS: zero-source reduction |zero_delta|={abs(zero_delta):.3e} <= 1e-12")
        n_pass += 1
    else:
        print(f"  FAIL: zero-source reduction |zero_delta|={abs(zero_delta):.3e} > 1e-12")
        n_fail += 1

    # Bar 2: TOWARD sign 4/4.
    expected_rows = len(green_vals)
    if toward == expected_rows:
        print(f"  PASS: TOWARD sign {toward}/{expected_rows}")
        n_pass += 1
    else:
        print(f"  FAIL: TOWARD sign {toward}/{expected_rows}")
        n_fail += 1

    # Bar 3: green F~M exponent in [0.95, 1.05].
    if green_alpha is not None and 0.95 <= green_alpha <= 1.05:
        print(f"  PASS: green F~M exponent {green_alpha:.3f} in [0.95, 1.05]")
        n_pass += 1
    else:
        ga = f"{green_alpha:.3f}" if green_alpha is not None else "None"
        print(f"  FAIL: green F~M exponent {ga} not in [0.95, 1.05]")
        n_fail += 1

    # Bar 4: mean |green/inst| ratio in [1.10, 1.40].
    if 1.10 <= mean_ratio <= 1.40:
        print(f"  PASS: mean |green/inst| ratio {mean_ratio:.3f} in [1.10, 1.40]")
        n_pass += 1
    else:
        print(f"  FAIL: mean |green/inst| ratio {mean_ratio:.3f} not in [1.10, 1.40]")
        n_fail += 1

    # Bar 5: calibration gain finiteness.
    if 0.0 < gain < 100.0:
        print(f"  PASS: calibration gain {gain:.6e} in (0, 100)")
        n_pass += 1
    else:
        print(f"  FAIL: calibration gain {gain:.6e} not in (0, 100)")
        n_fail += 1

    print(f"  === TOTAL: PASS={n_pass}, FAIL={n_fail} ===")
    if n_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
