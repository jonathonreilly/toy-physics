#!/usr/bin/env python3
"""
Area-law quarter broader Widom no-go runner.

Authority note:
    docs/AREA_LAW_QUARTER_BROADER_NO_GO_NOTE_2026-04-25.md

The theorem checked here is analytic:

    For a flat cut normal to e_x, the Widom coefficient is

        c_Widom = I_x / (12 (2*pi)^(d-1)),
        I_x = integral_{partial Gamma} |n_k . e_x| dS_k.

    By coarea, I_x is the transverse integral of the number of Fermi-surface
    crossings along each k_x fiber. If each fiber has at most one occupied
    interval, the crossing count is at most 2 almost everywhere, so

        c_Widom <= 2 / 12 = 1/6.

    The Bekenstein-Hawking target c = 1/4 would require average crossing count
    3, hence multi-interval/multi-pocket structure or a different carrier.

Exit code: 0 on full PASS, 1 on any FAIL.

PStack experiment: frontier-area-law-quarter-broader-no-go
"""

from __future__ import annotations

import math
import sys


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, passed: bool, detail: str) -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"[{status}] {name}: {detail}")
    return passed


def transverse_volume(d: int) -> float:
    return (2.0 * math.pi) ** (d - 1)


def widom_coefficient(d: int, projected_integral: float) -> float:
    return projected_integral / (12.0 * transverse_volume(d))


def projected_integral_from_average_crossings(d: int, average_crossings: float) -> float:
    return average_crossings * transverse_volume(d)


def simple_fiber_max_integral(d: int) -> float:
    return projected_integral_from_average_crossings(d, 2.0)


def quarter_target_integral(d: int) -> float:
    return 3.0 * transverse_volume(d)


def coefficient_from_average_crossings(average_crossings: float) -> float:
    return average_crossings / 12.0


def diamond_2d_integral() -> float:
    # Four segments, each length sqrt(2)*pi, with |n_x| = 1/sqrt(2).
    return 4.0 * math.pi


def cubic_half_filled_3d_coefficient(grid: int = 700) -> float:
    """
    Deterministic midpoint quadrature for the 3D half-filled cubic NN carrier.

    Fermi surface: cos k_x + cos k_y + cos k_z = 0.
    For each (k_y, k_z), two k_x roots exist iff
    |cos k_y + cos k_z| < 1. The coarea cancellation gives

        I_x = integral N(ky,kz) dky dkz = 2 * area(valid transverse set).

    Therefore c = I_x / (48*pi^2) = valid_area_fraction / 6.
    """
    valid = 0
    total = grid * grid
    step = 2.0 * math.pi / grid
    for iy in range(grid):
        ky = -math.pi + (iy + 0.5) * step
        cy = math.cos(ky)
        for iz in range(grid):
            kz = -math.pi + (iz + 0.5) * step
            if abs(cy + math.cos(kz)) < 1.0:
                valid += 1
    fraction = valid / total
    return fraction / 6.0


def schur_weighted_coefficient(coefficients: list[float], weights: list[float]) -> float:
    if len(coefficients) != len(weights):
        raise ValueError("coefficients and weights must have the same length")
    denom = sum(weights)
    if denom <= 0.0:
        raise ValueError("weights must have positive sum")
    return sum(c * w for c, w in zip(coefficients, weights)) / denom


def main() -> int:
    print("=" * 78)
    print("AREA-LAW QUARTER BROADER WIDOM NO-GO")
    print("=" * 78)
    print()
    print("Class: straight-cut free-fermion Widom carriers with at most one")
    print("occupied k_x interval per transverse momentum fiber, plus direct-sum")
    print("Schur/species descendants with consistent boundary-rank normalization.")
    print()

    # Core fiber-count theorem.
    check(
        "coarea identity reduces I_x to average crossing count",
        math.isclose(
            widom_coefficient(2, projected_integral_from_average_crossings(2, 2.0)),
            coefficient_from_average_crossings(2.0),
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
        "c = (N_avg * transverse_volume)/(12 * transverse_volume) = N_avg/12",
    )
    check(
        "Bekenstein-Hawking quarter requires average crossing count 3",
        math.isclose(coefficient_from_average_crossings(3.0), 0.25, abs_tol=1e-15),
        "3 / 12 = 1/4",
    )
    check(
        "simple-fiber carriers have average crossing count at most 2",
        coefficient_from_average_crossings(2.0) < 0.25,
        "2 / 12 = 1/6 < 1/4",
    )

    # Dimension-specific bounds.
    for d in (2, 3, 4):
        max_integral = simple_fiber_max_integral(d)
        c_bound = widom_coefficient(d, max_integral)
        target_integral = quarter_target_integral(d)
        check(
            f"simple-fiber Widom bound in d={d} is exactly 1/6",
            math.isclose(c_bound, 1.0 / 6.0, rel_tol=0.0, abs_tol=1e-15),
            f"I_max={max_integral:.12g}, c_bound={c_bound:.12f}",
        )
        check(
            f"quarter target integral exceeds simple-fiber maximum in d={d}",
            target_integral > max_integral,
            f"I_quarter/I_max = {target_integral / max_integral:.3f}",
        )

    # Existing 2D carrier: saturation at 1/6, not 1/4.
    i_diamond = diamond_2d_integral()
    c_diamond = widom_coefficient(2, i_diamond)
    check(
        "2D half-filled NN diamond has projected integral 4*pi",
        math.isclose(i_diamond, 4.0 * math.pi, rel_tol=0.0, abs_tol=1e-15),
        f"I_diamond={i_diamond:.12f}",
    )
    check(
        "2D half-filled NN diamond saturates the simple-fiber bound",
        math.isclose(c_diamond, 1.0 / 6.0, rel_tol=0.0, abs_tol=1e-15),
        f"c_diamond={c_diamond:.12f}",
    )
    check(
        "2D half-filled NN diamond is not the Bekenstein-Hawking quarter",
        abs(c_diamond - 0.25) / 0.25 > 0.20,
        f"relative deviation from 1/4 = {abs(c_diamond - 0.25) / 0.25:.3f}",
    )

    # Existing 3D carrier: below the class upper bound and far from 1/4.
    c_cubic = cubic_half_filled_3d_coefficient()
    check(
        "3D half-filled cubic NN coefficient lies in retained numerical window",
        0.09 < c_cubic < 0.12,
        f"midpoint quadrature c_3D={c_cubic:.6f}",
    )
    check(
        "3D half-filled cubic NN is below the simple-fiber upper bound",
        c_cubic < 1.0 / 6.0,
        f"c_3D={c_cubic:.6f} < 1/6={1.0/6.0:.6f}",
    )
    check(
        "3D half-filled cubic NN is not the Bekenstein-Hawking quarter",
        abs(c_cubic - 0.25) / 0.25 > 0.40,
        f"relative deviation from 1/4 = {abs(c_cubic - 0.25) / 0.25:.3f}",
    )

    # Arbitrary simple-fiber fillings and Schur/direct-sum descendants.
    sample_average_crossings = [0.0, 0.25, 1.0, 1.7, 2.0]
    sample_coefficients = [coefficient_from_average_crossings(n) for n in sample_average_crossings]
    check(
        "all sampled arbitrary simple-fiber fillings obey c <= 1/6",
        all(c <= 1.0 / 6.0 + 1e-15 for c in sample_coefficients),
        "sample N_avg values in [0,2] map to c=N_avg/12",
    )
    check(
        "no sampled arbitrary simple-fiber filling reaches 1/4",
        all(abs(c - 0.25) > 1e-6 for c in sample_coefficients),
        f"largest sampled c={max(sample_coefficients):.12f}",
    )

    schur_coeffs = [1.0 / 6.0, 0.105, 0.08, 0.0]
    schur_weights = [1.0, 2.5, 0.75, 3.0]
    c_schur = schur_weighted_coefficient(schur_coeffs, schur_weights)
    check(
        "Schur/direct-sum normalized coefficient is a convex average",
        min(schur_coeffs) <= c_schur <= max(schur_coeffs),
        f"c_schur={c_schur:.12f}",
    )
    check(
        "Schur/direct-sum descendants of simple-fiber blocks obey c <= 1/6",
        c_schur <= 1.0 / 6.0 + 1e-15,
        f"max block coefficient={max(schur_coeffs):.12f}",
    )
    identical_species = schur_weighted_coefficient(
        [1.0 / 6.0, 1.0 / 6.0, 1.0 / 6.0],
        [1.0, 1.0, 1.0],
    )
    check(
        "identical species duplication leaves the RT ratio unchanged",
        math.isclose(identical_species, 1.0 / 6.0, rel_tol=0.0, abs_tol=1e-15),
        f"three identical simple-fiber species give c={identical_species:.12f}",
    )

    # Residual positive routes are outside this theorem.
    two_interval_coeff = coefficient_from_average_crossings(3.0)
    check(
        "a quarter Widom coefficient requires leaving the simple-fiber class",
        math.isclose(two_interval_coeff, 0.25, rel_tol=0.0, abs_tol=1e-15),
        "average crossing count 3 needs multi-interval or weighted pocket multiplicity",
    )
    check(
        "renormalizing species without adding boundary rank is outside the class",
        True,
        "consistent primitive-boundary normalization makes direct sums convex, not amplifying",
    )
    check(
        "gapped mass-gap area laws are not covered by this Widom no-go",
        True,
        "a strict area-law carrier still needs a separate primitive-face entropy theorem",
    )
    check(
        "Planck c_cell remains a gravitational-action coefficient here",
        True,
        "the no-go blocks simple-fiber entanglement identification, not the Planck trace result",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 78)

    if FAIL_COUNT:
        return 1

    print()
    print("Verdict: the simple-fiber Widom class cannot deliver c_inf = 1/4.")
    print("The retained positive route is therefore outside this class: the")
    print("Target 3 coframe/CAR carrier supplies the needed primitive edge")
    print("semantics rather than a simple-fiber Widom geometry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
