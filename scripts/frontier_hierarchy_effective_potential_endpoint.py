#!/usr/bin/env python3
"""
Hierarchy effective-potential UV endpoint theorem on the minimal APBC hypercube.

This script takes the exact Matsubara formulas from the L_s = 2 APBC hierarchy
block and derives the exact small-m effective-potential coefficient:

    Delta f(L_t, m) = A(L_t) m^2 + O(m^4)

The remaining Part 3 question is then reframed as:

    which A(L_t) normalization is the physical EWSB normalization?

The key exact endpoint formulas are:

    A_2   = 1 / (8 u0^2)
    A_inf = 1 / (4 sqrt(3) u0^2)

so the full temporal-averaging correction on a dimension-4 potential density is

    C_inf = (A_2 / A_inf)^(-1/4) = (sqrt(3) / 2)^(1/4) = (3/4)^(1/8)

This is the exact version of the earlier numerical compression argument.
"""

from __future__ import annotations

import math
import sys

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def temporal_modes(Lt: int):
    return [(2 * n + 1) * math.pi / Lt for n in range(Lt)]


def free_energy_density(Lt: int, u0: float, mass: float) -> float:
    omegas = temporal_modes(Lt)
    return (1.0 / (2.0 * Lt)) * sum(
        math.log1p(mass**2 / (u0**2 * (3.0 + math.sin(w) ** 2))) for w in omegas
    )


def condensate_density(Lt: int, u0: float, mass: float) -> float:
    omegas = temporal_modes(Lt)
    return (mass / Lt) * sum(
        1.0 / (mass**2 + u0**2 * (3.0 + math.sin(w) ** 2)) for w in omegas
    )


def quadratic_coefficient(Lt: int, u0: float) -> float:
    omegas = temporal_modes(Lt)
    return (1.0 / (2.0 * Lt * u0**2)) * sum(
        1.0 / (3.0 + math.sin(w) ** 2) for w in omegas
    )


def exact_a2(u0: float) -> float:
    return 1.0 / (8.0 * u0**2)


def exact_a4(u0: float) -> float:
    return 1.0 / (7.0 * u0**2)


def exact_ainf(u0: float) -> float:
    return 1.0 / (4.0 * math.sqrt(3.0) * u0**2)


def exact_cond_ratio_inf_to_2(mass: float, u0: float) -> float:
    a = mass**2 + 3.0 * u0**2
    b = mass**2 + 4.0 * u0**2
    return math.sqrt(b / a)


def exact_dimension4_endpoint_factor() -> float:
    return (3.0 / 4.0) ** (1.0 / 8.0)


def test_quadratic_coefficient_matches_small_mass_limit():
    print("\n" + "=" * 78)
    print("PART 1: SMALL-M EFFECTIVE-POTENTIAL COEFFICIENT")
    print("=" * 78)

    u0 = 0.9
    max_rel = 0.0
    for Lt in [2, 4, 6, 8, 10]:
        a_exact = quadratic_coefficient(Lt, u0)
        for mass in [1e-4, 3e-4, 1e-3, 3e-3]:
            a_num = free_energy_density(Lt, u0, mass) / (mass**2)
            rel = abs(a_num - a_exact) / a_exact
            max_rel = max(max_rel, rel)
            print(
                f"  Lt={Lt}, m={mass:g}: "
                f"A_num={a_num:.12e}, A_exact={a_exact:.12e}, rel={rel:.2e}"
            )
    check(
        "quadratic coefficient matches the small-m free-energy density limit",
        max_rel < 2e-6,
        f"max relative error = {max_rel:.2e}",
    )


def test_endpoint_formulas():
    print("\n" + "=" * 78)
    print("PART 2: EXACT ENDPOINT FORMULAS")
    print("=" * 78)

    u0 = 0.9
    a2 = quadratic_coefficient(2, u0)
    a4 = quadratic_coefficient(4, u0)
    a40 = quadratic_coefficient(40, u0)
    a2_exact = exact_a2(u0)
    a4_exact = exact_a4(u0)
    ainf_exact = exact_ainf(u0)

    print(f"  A_2 direct   = {a2:.12e}")
    print(f"  A_2 exact    = {a2_exact:.12e}")
    print(f"  A_4 direct   = {a4:.12e}")
    print(f"  A_4 exact    = {a4_exact:.12e}")
    print(f"  A_40 direct  = {a40:.12e}")
    print(f"  A_inf exact  = {ainf_exact:.12e}")

    check(
        "A_2 = 1 / (8 u0^2)",
        abs(a2 - a2_exact) < 1e-15,
        f"absolute error = {abs(a2 - a2_exact):.2e}",
    )
    check(
        "A_4 = 1 / (7 u0^2)",
        abs(a4 - a4_exact) < 1e-15,
        f"absolute error = {abs(a4 - a4_exact):.2e}",
    )
    check(
        "A_Lt approaches A_inf = 1 / (4 sqrt(3) u0^2)",
        abs(a40 - ainf_exact) < 2e-4,
        f"absolute error at Lt=40 = {abs(a40 - ainf_exact):.2e}",
    )


def test_condensate_ratio_formula():
    print("\n" + "=" * 78)
    print("PART 3: EXACT CONDENSATE ENDPOINT RATIO")
    print("=" * 78)

    u0 = 0.9
    max_rel = 0.0
    for mass in [1e-4, 1e-3, 1e-2, 1e-1]:
        c2 = condensate_density(2, u0, mass)
        c80 = condensate_density(80, u0, mass)
        ratio_num = c80 / c2
        ratio_exact = exact_cond_ratio_inf_to_2(mass, u0)
        rel = abs(ratio_num - ratio_exact) / ratio_exact
        max_rel = max(max_rel, rel)
        print(
            f"  m={mass:g}: ratio_num={ratio_num:.12f}, "
            f"ratio_exact={ratio_exact:.12f}, rel={rel:.2e}"
        )
    check(
        "cond(Lt->inf) / cond(Lt=2) = sqrt((m^2+4u0^2)/(m^2+3u0^2))",
        max_rel < 4e-4,
        f"max relative error using Lt=80 = {max_rel:.2e}",
    )


def test_dimension4_endpoint_factor():
    print("\n" + "=" * 78)
    print("PART 4: DIMENSION-4 ENDPOINT CORRECTION")
    print("=" * 78)

    alpha_bare = 1.0 / (4.0 * math.pi)
    m_planck = 1.2209e19
    plaquette = 0.5934
    u0 = plaquette ** 0.25
    alpha_lm = alpha_bare / u0
    c_obs = 246.22 / (m_planck * alpha_lm**16)
    c_inf = exact_dimension4_endpoint_factor()
    c_none = 1.0

    print(f"  C_obs       = {c_obs:.12f}")
    print(f"  C_none      = {c_none:.12f}")
    print(f"  C_inf^(4D)  = {c_inf:.12f}")

    check(
        "observed prefactor lies inside the exact 3+1 endpoint band [C_inf, 1]",
        c_inf < c_obs < c_none,
        f"C_inf={c_inf:.12f} < C_obs={c_obs:.12f} < 1",
    )
    check(
        "dimension-4 endpoint factor is within 1% of the observed prefactor",
        abs(c_inf - c_obs) < 0.01,
        f"|C_inf-C_obs| = {abs(c_inf - c_obs):.6f}",
    )


def main():
    print("Hierarchy effective-potential endpoint theorem")
    print("=" * 78)
    test_quadratic_coefficient_matches_small_mass_limit()
    test_endpoint_formulas()
    test_condensate_ratio_formula()
    test_dimension4_endpoint_factor()
    print("\n" + "=" * 78)
    print(f"SCORECARD: {PASS_COUNT} pass, {FAIL_COUNT} fail out of {PASS_COUNT + FAIL_COUNT}")
    print("=" * 78)
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
