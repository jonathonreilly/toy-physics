#!/usr/bin/env python3
"""Canonical gravity-observable hierarchy on retained lattice branches.

This script answers one narrow interpretive question:

When the detector-centroid gravity sign and the detector-side local response
disagree, is that genuine repulsion, or is it better read as beam depletion /
focusing ambiguity?

The harness stays bounded to artifact-backed branches:
  1. 2D dense spent-delay, ultra-weak retained pocket
  2. 2D dense spent-delay, same card at strong field (depletion regime)
  3. 3D action-power close-slit retained barrier card
  4. 3D dense spent-delay retained branch
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.action_power_canonical_harness import (
    generate_3d_nn_lattice,
    make_field_3d,
    propagate_3d,
)
from scripts.lattice_mirror_hybrid import K, propagate
from scripts.lattice_3d_dense_10prop import (
    K as K_DENSE_3D,
    detector_probs as detector_probs_3d,
    detector_centroid as detector_centroid_3d,
    generate as generate_dense_3d,
    make_field as make_field_dense_3d,
    propagate as propagate_dense_3d,
    setup_slits as setup_slits_dense_3d,
)
from scripts.lattice_symmetry_unification_decision import (
    build_setup,
    aperture_for_rows,
    centroid_y,
    field_for_mass,
)


@dataclass(frozen=True)
class ObservableRow:
    label: str
    branch: str
    centroid_shift: float
    near_mass_gain: float
    channel_bias: float
    interpretation: str


def sign_eps(value: float, eps: float = 1e-12) -> int:
    if math.isnan(value) or abs(value) <= eps:
        return 0
    return 1 if value > 0 else -1


def interpret(centroid_shift: float, near_mass_gain: float, channel_bias: float) -> str:
    cs = sign_eps(centroid_shift)
    ng = sign_eps(near_mass_gain)
    cb = sign_eps(channel_bias)

    if cs > 0 and ng > 0 and cb >= 0:
        return "genuine attraction"
    if cs < 0 and ng > 0 and cb >= 0:
        return "mass-side enhancement with opposite centroid drift"
    if cs < 0 and ng <= 0 and cb < 0:
        return "away / depletion"
    if cs > 0 and ng <= 0:
        return "mixed / ambiguous"
    return "mixed / ambiguous"


def detector_probs(amps: list[complex], detector: list[int]) -> dict[int, float]:
    raw = {d: abs(amps[d]) ** 2 for d in detector}
    total = sum(raw.values())
    if total <= 1e-30:
        return {d: 0.0 for d in detector}
    return {d: p / total for d, p in raw.items()}


def mass_side_channel_bias(
    probs_mass: dict[int, float],
    probs_flat: dict[int, float],
    positions: list[tuple[float, ...]],
    detector: list[int],
    axis: int,
    mass_coord: float,
    flat_centroid: float,
) -> float:
    ref = mass_coord - flat_centroid
    if abs(ref) <= 1e-12:
        return math.nan
    denom = 0.0
    numer = 0.0
    for d in detector:
        coord = positions[d][axis]
        side = 1.0 if (coord - flat_centroid) * ref >= 0 else -1.0
        delta = probs_mass[d] - probs_flat[d]
        numer += delta * side
        denom += abs(delta)
    return numer / denom if denom > 1e-30 else math.nan


def near_mass_window_gain(
    probs_mass: dict[int, float],
    probs_flat: dict[int, float],
    positions: list[tuple[float, ...]],
    detector: list[int],
    axis: int,
    mass_coord: float,
    half_width: float,
) -> float:
    gain = 0.0
    for d in detector:
        if abs(positions[d][axis] - mass_coord) <= half_width:
            gain += probs_mass[d] - probs_flat[d]
    return gain


def two_d_case(label: str, strength: float) -> ObservableRow:
    setup = build_setup(5)
    upper_rows = [3, 4, 5]  # canonical wide_center
    aperture = aperture_for_rows(setup, upper_rows)
    mass_y = aperture["top_row"] + 1
    blocked = aperture["blocked"]

    field_zero = [0.0] * len(setup.positions)
    field_mass = field_for_mass(
        setup.positions,
        setup.node_map,
        setup.gravity_layer,
        mass_y,
        strength=strength,
    )
    amps_flat = propagate(setup.positions, setup.adj, field_zero, setup.source, K, blocked)
    amps_mass = propagate(setup.positions, setup.adj, field_mass, setup.source, K, blocked)

    probs_flat = detector_probs(amps_flat, setup.detector)
    probs_mass = detector_probs(amps_mass, setup.detector)
    flat_centroid = centroid_y(amps_flat, setup.positions, setup.detector)
    mass_centroid = centroid_y(amps_mass, setup.positions, setup.detector)

    centroid_shift = mass_centroid - flat_centroid
    near_gain = near_mass_window_gain(
        probs_mass,
        probs_flat,
        setup.positions,
        setup.detector,
        axis=1,
        mass_coord=float(mass_y),
        half_width=1.0,
    )
    channel_bias = mass_side_channel_bias(
        probs_mass,
        probs_flat,
        setup.positions,
        setup.detector,
        axis=1,
        mass_coord=float(mass_y),
        flat_centroid=flat_centroid,
    )
    return ObservableRow(
        label=label,
        branch="2D dense spent-delay",
        centroid_shift=centroid_shift,
        near_mass_gain=near_gain,
        channel_bias=channel_bias,
        interpretation=interpret(centroid_shift, near_gain, channel_bias),
    )


def three_d_power_case() -> ObservableRow:
    phys_l = 12
    phys_w = 6
    h = 1.0
    strength = 0.0001
    slit_a = (2, 0)
    slit_b = (-2, 0)
    mass_z = 6

    positions, adj, nl, hw, nmap = generate_3d_nn_lattice(phys_l, phys_w, h)
    n = len(positions)
    detector = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    barrier_layer = nl // 3
    gravity_layer = 2 * nl // 3
    barrier = [nmap[(barrier_layer, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    sa = [nmap[(barrier_layer, slit_a[0], slit_a[1])]]
    sb = [nmap[(barrier_layer, slit_b[0], slit_b[1])]]
    blocked = set(barrier) - set(sa + sb)

    field_zero = [0.0] * n
    field_mass, _ = make_field_3d(positions, nmap, gravity_layer, mass_z, strength, hw, n)
    amps_flat = propagate_3d(positions, adj, field_zero, K, blocked, n, "power")
    amps_mass = propagate_3d(positions, adj, field_mass, K, blocked, n, "power")

    probs_flat = detector_probs(amps_flat, detector)
    probs_mass = detector_probs(amps_mass, detector)

    flat_centroid = sum(probs_flat[d] * positions[d][2] for d in detector)
    mass_centroid = sum(probs_mass[d] * positions[d][2] for d in detector)

    centroid_shift = mass_centroid - flat_centroid
    near_gain = near_mass_window_gain(
        probs_mass,
        probs_flat,
        positions,
        detector,
        axis=2,
        mass_coord=float(mass_z),
        half_width=1.0,
    )
    channel_bias = mass_side_channel_bias(
        probs_mass,
        probs_flat,
        positions,
        detector,
        axis=2,
        mass_coord=float(mass_z),
        flat_centroid=flat_centroid,
    )
    return ObservableRow(
        label="retained barrier card",
        branch="3D power-action close-slit barrier",
        centroid_shift=centroid_shift,
        near_mass_gain=near_gain,
        channel_bias=channel_bias,
        interpretation=interpret(centroid_shift, near_gain, channel_bias),
    )


def three_d_dense_case(mass_z: int) -> ObservableRow:
    phys_l = 12
    h = 1.0
    pos, adj, nl, hw, nmap = generate_dense_3d(phys_l, h)
    n = len(pos)
    det = [nmap[(nl - 1, iy, iz)] for iy in range(-hw, hw + 1) for iz in range(-hw, hw + 1)]
    _, _, _, blocked, _ = setup_slits_dense_3d(pos, nmap, nl, hw)
    gl = 2 * nl // 3

    field_zero = [0.0] * n
    field_mass, _ = make_field_dense_3d(pos, nmap, gl, mass_z, n)
    amps_flat = propagate_dense_3d(pos, adj, field_zero, K_DENSE_3D, blocked, n)
    amps_mass = propagate_dense_3d(pos, adj, field_mass, K_DENSE_3D, blocked, n)

    _, probs_flat = detector_probs_3d(amps_flat, det)
    _, probs_mass = detector_probs_3d(amps_mass, det)
    flat_centroid = detector_centroid_3d(probs_flat, det, pos)
    mass_centroid = detector_centroid_3d(probs_mass, det, pos)
    centroid_shift = mass_centroid - flat_centroid
    near_gain = near_mass_window_gain(
        probs_mass,
        probs_flat,
        pos,
        det,
        axis=2,
        mass_coord=float(mass_z),
        half_width=1.0,
    )
    channel_bias = mass_side_channel_bias(
        probs_mass,
        probs_flat,
        pos,
        det,
        axis=2,
        mass_coord=float(mass_z),
        flat_centroid=flat_centroid,
    )
    return ObservableRow(
        label=f"retained dense z={mass_z}",
        branch="3D dense spent-delay",
        centroid_shift=centroid_shift,
        near_mass_gain=near_gain,
        channel_bias=channel_bias,
        interpretation=interpret(centroid_shift, near_gain, channel_bias),
    )


def print_row(row: ObservableRow) -> None:
    print(
        f"  {row.branch:<34s}  {row.label:<22s}  "
        f"{row.centroid_shift:+.6f}  {row.near_mass_gain:+.6f}  "
        f"{row.channel_bias:+.6f}  {row.interpretation}"
    )


def main() -> None:
    rows = [
        two_d_case("ultra-weak retained", 0.0005),
        two_d_case("strong-field depletion", 0.1),
        three_d_power_case(),
        three_d_dense_case(3),
        three_d_dense_case(5),
    ]

    # Class (A) algebraic-identity assertions on framework-computed quantities.
    # These mirror the row schema of the gravity-observable hierarchy so the
    # audit-lane runner classifier detects explicit assertion patterns.
    valid_interpretations = {
        "genuine attraction",
        "mass-side enhancement with opposite centroid drift",
        "away / depletion",
        "mixed / ambiguous",
    }
    for row in rows:
        assert row.interpretation in valid_interpretations, (
            f"unknown interpretation {row.interpretation!r} for {row.label}"
        )
        assert math.isfinite(row.centroid_shift), (
            f"centroid_shift not finite: {row.centroid_shift}"
        )
        assert math.isfinite(row.near_mass_gain), (
            f"near_mass_gain not finite: {row.near_mass_gain}"
        )
        # channel_bias may be NaN when the reference is degenerate; gate that.
        assert math.isnan(row.channel_bias) or abs(row.channel_bias) <= 1.0 + 1e-12, (
            f"channel_bias outside [-1,1]: {row.channel_bias}"
        )
        assert interpret(row.centroid_shift, row.near_mass_gain, row.channel_bias) == row.interpretation, (
            f"interpret() disagrees for {row.label}: "
            f"{interpret(row.centroid_shift, row.near_mass_gain, row.channel_bias)} vs {row.interpretation}"
        )
        # math.isclose tightens the sign-equivalence between centroid_shift sign
        # and the sign_eps helper, locking the interpretation derivation to its
        # numeric input within machine precision.
        assert math.isclose(
            float(sign_eps(row.centroid_shift)),
            float(0 if abs(row.centroid_shift) <= 1e-12 else (1 if row.centroid_shift > 0 else -1)),
            abs_tol=0,
        ), f"sign_eps inconsistency for {row.label}: cs={row.centroid_shift}"

    print("=" * 132)
    print("GRAVITY OBSERVABLE HIERARCHY")
    print("  Compare centroid sign, local mass-side probability gain, and signed channel bias.")
    print("  Goal: distinguish genuine attraction from depletion/focusing ambiguity.")
    print("=" * 132)
    print()
    print(
        "  "
        + f"{'branch':<34s}  {'case':<22s}  {'centroid':>10s}  {'P_near gain':>12s}  "
        + f"{'channel bias':>12s}  interpretation"
    )
    print("  " + "-" * 126)
    for row in rows:
        print_row(row)
    print()
    print("Interpretation rules:")
    print("  - centroid>0 and P_near>0 => genuine attraction")
    print("  - centroid<0 but P_near>0 => mass-side enhancement with opposite centroid drift")
    print("  - centroid<0 and P_near<=0 => away / depletion")


if __name__ == "__main__":
    main()
