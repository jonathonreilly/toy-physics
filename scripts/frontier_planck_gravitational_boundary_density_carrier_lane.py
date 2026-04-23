#!/usr/bin/env python3
"""Audit the gravitational boundary-density carrier lane honestly.

This is not a closure harness. It encodes three sharp reductions:
  - no nontrivial local geometric boundary density can reproduce a universal
    area law on the admitted gravity surface;
  - horizon specialization still leaves only a constant surface-density class;
  - naive independent integer cell counting cannot give exact conventional
    a = l_P.
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/PLANCK_SCALE_GRAVITATIONAL_BOUNDARY_DENSITY_CARRIER_LANE_2026-04-23.md"


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def check(label: str, passed: bool, detail: str) -> bool:
    tag = "PASS" if passed else "FAIL"
    print(f"  [{tag}] {label}")
    print(f"         {detail}")
    return passed


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split()).lower()


def weak_field_scaling(a_phi: int, b_grad: int, c_mean: int, d_gauss: int, e_kappa: int) -> tuple[int, int]:
    """Return (mass exponent, radius exponent after area integration)."""
    mass_exp = a_phi + b_grad + e_kappa
    radius_exp = 2 - a_phi - 2 * b_grad - c_mean - 2 * d_gauss - 2 * e_kappa
    return mass_exp, radius_exp


def horizon_scaling(a_phi: int, b_grad: int, c_mean: int, d_gauss: int, e_kappa: int) -> int:
    """Return the radius exponent after area integration on a horizon family.

    On the horizon family phi_H is O(1), while grad, H, kappa ~ 1/R and
    Gaussian curvature ~ 1/R^2.
    """
    return 2 - b_grad - c_mean - 2 * d_gauss - e_kappa


def main() -> int:
    note = normalized(NOTE)
    n_pass = 0
    n_fail = 0

    print("Planck gravitational boundary-density carrier lane audit")
    print("=" * 78)

    section("PART 1: LOCAL GEOMETRIC DENSITY NO-GO")
    candidates = []
    for exps in itertools.product(range(4), repeat=5):
        mass_exp, radius_exp = weak_field_scaling(*exps)
        if mass_exp == 0 and radius_exp == 2:
            candidates.append(exps)

    p = check(
        "weak-field area-law universality leaves only the zero-degree monomial",
        candidates == [(0, 0, 0, 0, 0)],
        (
            "among exponents 0..3, the only local monomial with source-independent "
            "R^2 scaling is the constant density"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    sample = (1, 1, 0, 0, 0)
    mass_exp, radius_exp = weak_field_scaling(*sample)
    p = check(
        "a representative mixed local density fails universality",
        mass_exp > 0 or radius_exp != 2,
        (
            "phi * |partial_n phi| integrates as M^2 * R^-1, so it is neither "
            "source-independent nor area-law"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 2: HORIZON SPECIALIZATION STILL COLLAPSES TO CONSTANT DENSITY")
    horizon_candidates = []
    for exps in itertools.product(range(4), repeat=5):
        radius_exp = horizon_scaling(*exps)
        if radius_exp == 2:
            horizon_candidates.append(exps)

    only_phi_powers = all(
        (b_grad, c_mean, d_gauss, e_kappa) == (0, 0, 0, 0)
        for (_, b_grad, c_mean, d_gauss, e_kappa) in horizon_candidates
    )
    p = check(
        "on the horizon family, every surviving area-law monomial is only a power of phi_H",
        only_phi_powers,
        (
            "all inverse-radius geometric factors must vanish; the surviving "
            "class is a constant surface density times an O(1) horizon constant"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "horizon specialization does not rescue nontrivial local geometric densities",
        any(exp != (0, 0, 0, 0, 0) for exp in horizon_candidates),
        (
            "phi_H powers survive only because phi_H is already constant on the "
            "horizon family; this is still a constant-density class, not a new "
            "local geometric mechanism"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 3: NAIVE INTEGER CELL COUNTING NO-GO")
    g_required = math.exp(0.25)
    nearest_integer = round(g_required)
    p = check(
        "exact conventional Planck would require non-integer local degeneracy",
        abs(g_required - nearest_integer) > 1e-6,
        f"g_required = exp(1/4) = {g_required:.12f}, not an integer Hilbert dimension",
    )
    n_pass += int(p)
    n_fail += int(not p)

    g_min = 2
    a_over_lp = math.sqrt(4.0 * math.log(g_min))
    p = check(
        "the minimal nontrivial integer choice is Planck-order but not exact Planck",
        abs(a_over_lp - 1.0) > 1e-6 and 1.0 < a_over_lp < 2.0,
        f"for g = 2, a/l_P = 2*sqrt(ln 2) = {a_over_lp:.12f}",
    )
    n_pass += int(p)
    n_fail += int(not p)

    q_bit_hits = []
    for q_bits in range(1, 9):
        ratio = 4.0 * q_bits * math.log(2.0)
        if abs(ratio - 1.0) < 1e-12:
            q_bit_hits.append(q_bits)
    p = check(
        "no small one-bit-per-cell tensor-product variant lands exact a = l_P",
        q_bit_hits == [],
        "for g = 2^q, the required coefficient 1/4 is never reached for integer q",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("PART 4: SURVIVING CARRIER CLASS")
    p = check(
        "the note identifies a collective gravitational boundary carrier as the surviving class",
        "collective gravitational boundary carrier" in note
        and "exact effective density" in note
        and "s_* = 1/4" in note,
        (
            "the surviving target is an exact renormalized surface-density theorem, "
            "not RT/Widom, local curvature, or naive cell counting"
        ),
    )
    n_pass += int(p)
    n_fail += int(not p)

    p = check(
        "the note explicitly rules out both local curvature and naive integer cell counting",
        "not local curvature" in note and "not naive integer cell counting" in note,
        "the route narrowing is explicit rather than only implied",
    )
    n_pass += int(p)
    n_fail += int(not p)

    section("FINAL VERDICT")
    verdict = (
        "A boundary-density derivation of exact conventional Planck remains "
        "possible only in one narrow form: an exact collective gravitational "
        "surface-density theorem with effective density s_* = 1/4. The whole "
        "local geometric class and the naive independent-cell counting class "
        "are ruled out."
    )
    print(f"  {verdict}")

    print("\n" + "=" * 78)
    print(f"SCORECARD: {n_pass} pass, {n_fail} fail out of {n_pass + n_fail}")
    print("=" * 78)

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
