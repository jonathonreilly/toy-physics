#!/usr/bin/env python3
"""Self-consistent source-resolved Green pocket on the compact exact lattice.

Moonshot goal:
  Take the exact Green pocket and let the source-cluster weights update from
  the propagated wave once, instead of keeping the source profile fixed by
  hand. This is the smallest serious refinement of the exact-lattice pocket.

This is intentionally narrow:
  - one compact exact lattice family at h = 0.25
  - one source-resolved Green-like kernel
  - one self-consistency update from source-cluster amplitudes
  - one comparison against the instantaneous 1/r comparator
  - one reduction check: zero source must recover free propagation exactly
"""

from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import scripts.minimal_source_driven_field_probe as m  # noqa: E402


H = 0.25
NL_PHYS = 6
PW = 3
SOURCE_CLUSTER = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
FIELD_TARGET_MAX = 0.02
CALIBRATED_GAIN = 1.7578903308081324
GREEN_EPS = 0.5
GREEN_MU = 0.08
ZERO_SOURCE_TOL = 1e-12
EXPONENT_TARGET = 1.0
EXPONENT_TOL = 5e-3
TABLE_REL_TOL = 5e-4
TABLE_ABS_TOL = 5e-8
EXPECTED_ROWS = [
    (0.0010, 1.410541e-03, 1.873799e-03, 1.328, 2.500245e-03),
    (0.0020, 2.821591e-03, 3.749686e-03, 1.329, 5.000223e-03),
    (0.0040, 5.645274e-03, 7.507807e-03, 1.330, 9.999374e-03),
    (0.0080, 1.129975e-02, 1.505023e-02, 1.332, 1.999447e-02),
]
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


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
    weights: list[float],
) -> list[list[float]]:
    """Source-resolved Green-like field with cluster weights."""
    if not source_nodes:
        return [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]

    source_pos = [lat.pos[i] for i in source_nodes]
    field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    for layer in range(lat.nl):
        ls = lat.layer_start[layer]
        for i in range(lat.npl):
            x, y, z = lat.pos[ls + i]
            val = 0.0
            for w, (mx, my, mz) in zip(weights, source_pos):
                r = math.sqrt((x - mx) ** 2 + (y - my) ** 2 + (z - mz) ** 2) + GREEN_EPS
                val += w * source_strength * math.exp(-GREEN_MU * r) / r
            field[layer][i] = val
    return field


def _field_abs_max(layers: list[list[float]]) -> float:
    return max(abs(v) for row in layers for v in row)


def _normalize_weights(vals: list[float]) -> list[float]:
    total = sum(vals)
    if total <= 1e-30:
        return [1.0 / len(vals)] * len(vals)
    return [v / total for v in vals]


def _close(actual: float, expected: float) -> bool:
    return abs(actual - expected) <= TABLE_ABS_TOL + TABLE_REL_TOL * abs(expected)


def main() -> int:
    lat = m.Lattice3D.build(NL_PHYS, PW, H)
    source_nodes = _source_cluster_nodes(lat)
    zero_field = [[0.0 for _ in range(lat.npl)] for _ in range(lat.nl)]
    free = lat.propagate(zero_field, m.K)
    z_free = m._centroid_z(free, lat)

    print("=" * 84)
    print("SOURCE-RESOLVED EXACT GREEN SELF-CONSISTENT")
    print("  compact exact h=0.25 refinement family, one self-consistency update")
    print("  comparison: self-consistent field vs instantaneous 1/r field")
    print("=" * 84)
    print(f"h={H}, W={PW}, L={NL_PHYS}, source_cluster={len(source_nodes)} nodes")
    print(f"field kernel: exp(-mu r)/(r+eps), mu={GREEN_MU}, eps={GREEN_EPS}")
    print(f"source strengths: {m.SOURCE_STRENGTHS}")
    print(f"target max |f|: {FIELD_TARGET_MAX}")
    print(f"calibrated gain input: {CALIBRATED_GAIN:.12e}")
    print("calibration boundary: gain is a frozen input, not an independent amplitude prediction")
    print()

    base_weights = [1.0 / len(source_nodes)] * len(source_nodes)
    ref_raw = _source_resolved_green_field(lat, max(m.SOURCE_STRENGTHS), source_nodes, base_weights)
    ref_max = _field_abs_max(ref_raw)
    gain = CALIBRATED_GAIN

    zero_dyn = _source_resolved_green_field(lat, 0.0, source_nodes, base_weights)
    zero_amps = lat.propagate([[gain * v for v in row] for row in zero_dyn], m.K)
    zero_delta = m._centroid_z(zero_amps, lat) - z_free

    print("REDUCTION CHECK")
    print(f"  zero-source dynamic shift: {zero_delta:+.6e}")
    print(f"  calibration gain: {gain:.6e}")
    print(f"  calibrated base-field cap: {gain * ref_max:.6e}")
    print()

    print(f"{'s':>8s} {'inst':>12s} {'green':>12s} {'green/inst':>11s} {'max|f|':>12s}")
    print("-" * 70)

    inst_vals: list[float] = []
    green_vals: list[float] = []
    ratios: list[float] = []
    max_fields: list[float] = []

    for s in m.SOURCE_STRENGTHS:
        inst_field = m._instantaneous_field_layers(lat, s, m.SOURCE_Z)

        # One self-consistency update: build a Green field, propagate once,
        # then reweight the source cluster from the propagated amplitudes.
        green0 = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, source_nodes, base_weights)]
        amps0 = lat.propagate(green0, m.K)
        cluster_power = [abs(amps0[i]) ** 2 for i in source_nodes]
        weights_sc = _normalize_weights(cluster_power)
        green_field = [[gain * v for v in row] for row in _source_resolved_green_field(lat, s, source_nodes, weights_sc)]

        inst_amps = lat.propagate(inst_field, m.K)
        green_amps = lat.propagate(green_field, m.K)

        inst_delta = m._centroid_z(inst_amps, lat) - z_free
        green_delta = m._centroid_z(green_amps, lat) - z_free
        ratio = green_delta / inst_delta if abs(inst_delta) > 1e-30 else float("nan")

        inst_vals.append(inst_delta)
        green_vals.append(green_delta)
        ratios.append(abs(ratio))
        max_field = max(abs(v) for row in green_field for v in row)
        max_fields.append(max_field)

        print(
            f"{s:8.4f} {inst_delta:+12.6e} {green_delta:+12.6e} "
            f"{ratio:11.3f} {max_field:12.6e}"
        )

    inst_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), inst_vals)
    green_alpha = m._fit_power(list(m.SOURCE_STRENGTHS), green_vals)
    toward = sum(1 for v in green_vals if v > 0)
    mean_ratio = sum(ratios) / len(ratios)

    print()
    print("SAFE READ")
    print(f"  instantaneous F~M exponent: {inst_alpha:.2f}" if inst_alpha is not None else "  instantaneous F~M exponent: n/a")
    print(f"  self-consistent Green F~M exponent: {green_alpha:.2f}" if green_alpha is not None else "  self-consistent Green F~M exponent: n/a")
    print(f"  TOWARD rows: {toward}/{len(green_vals)}")
    print(f"  mean |green/inst| ratio: {mean_ratio:.3f}")
    print("  this is a refinement-positive pocket, not yet a self-consistent")
    print("  field theory")

    print()
    print("ASSERTION SUMMARY")
    print("-" * 84)
    record(
        "zero-source exactness is preserved",
        abs(zero_delta) <= ZERO_SOURCE_TOL,
        f"zero_delta={zero_delta:+.12e}; tolerance={ZERO_SOURCE_TOL:.1e}",
    )
    record(
        "calibrated gain is the frozen input that sets the base-field cap",
        abs(gain * ref_max - FIELD_TARGET_MAX) <= TABLE_ABS_TOL,
        f"gain={gain:.12e}; base_cap={gain * ref_max:.12e}; target={FIELD_TARGET_MAX:.12e}",
    )
    record(
        "self-consistent Green deflection has TOWARD sign in every source row",
        toward == len(green_vals),
        f"toward={toward}/{len(green_vals)}; green_deltas={[f'{v:+.6e}' for v in green_vals]}",
    )
    record(
        "instantaneous comparator remains linear in source strength",
        inst_alpha is not None and abs(inst_alpha - EXPONENT_TARGET) <= EXPONENT_TOL,
        f"alpha={inst_alpha:.6f}; target={EXPONENT_TARGET:.6f}; tolerance={EXPONENT_TOL:.1e}",
    )
    record(
        "self-consistent Green response remains linear in source strength",
        green_alpha is not None and abs(green_alpha - EXPONENT_TARGET) <= EXPONENT_TOL,
        f"alpha={green_alpha:.6f}; target={EXPONENT_TARGET:.6f}; tolerance={EXPONENT_TOL:.1e}",
    )
    row_checks: list[str] = []
    table_ok = True
    for i, expected in enumerate(EXPECTED_ROWS):
        s_exp, inst_exp, green_exp, ratio_exp, max_exp = expected
        actual = (
            m.SOURCE_STRENGTHS[i],
            inst_vals[i],
            green_vals[i],
            green_vals[i] / inst_vals[i],
            max_fields[i],
        )
        checks = [_close(a, e) for a, e in zip(actual, expected)]
        table_ok = table_ok and all(checks)
        row_checks.append(
            f"s={actual[0]:.4f}: inst={actual[1]:+.6e}, green={actual[2]:+.6e}, "
            f"ratio={actual[3]:.3f}, max|f|={actual[4]:.6e}"
        )
    record(
        "frozen numerical table is reproduced within declared tolerances",
        table_ok,
        "\n".join(row_checks),
    )

    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print()
    print(f"PASSED: {n_pass}/{n_total}")
    print("SOURCE_RESOLVED_EXACT_GREEN_SELF_CONSISTENT_ASSERTIONS=" + ("TRUE" if n_pass == n_total else "FALSE"))
    print("CALIBRATED_GAIN_IS_INPUT=TRUE")
    print("SOURCE_RESOLVED_GREEN_FULL_SELF_CONSISTENT_FIELD_THEORY=FALSE")
    print("RESIDUAL_SCOPE=fully_converged_self_consistent_field_theory_and_uncalibrated_amplitude")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
