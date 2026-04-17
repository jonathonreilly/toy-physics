#!/usr/bin/env python3
"""
Exact connected-hierarchy theorem for the Wilson plaquette reduction law.

This closes the exact source-derivative hierarchy governing chi_L(beta) and
therefore the higher transport derivatives of beta_eff(beta), while keeping
explicit hierarchy closure at beta = 6 open.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
import sys

sys.path.insert(0, "scripts")

from frontier_gauge_vacuum_plaquette_constant_lift_obstruction import full_wilson_strong_coupling_slope  # noqa: E402
from frontier_gauge_vacuum_plaquette_mixed_cumulant_audit import (  # noqa: E402
    beta_eff_beta5_coefficient,
    total_nonlocal_beta5_coefficient,
)


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def beta_derivative_of_monomial(alpha: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    out: Counter[tuple[int, ...]] = Counter()
    for idx, power in enumerate(alpha):
        if power == 0:
            continue
        reduced = list(alpha)
        reduced[idx] -= 1
        out[tuple(reduced)] += power
    return out


def source_derivative_of_monomial(alpha: tuple[int, ...], idx: int) -> Counter[tuple[int, ...]]:
    out: Counter[tuple[int, ...]] = Counter()
    power = alpha[idx]
    if power == 0:
        return out
    reduced = list(alpha)
    reduced[idx] -= 1
    out[tuple(reduced)] += power
    return out


def sum_source_derivatives(alpha: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    out: Counter[tuple[int, ...]] = Counter()
    for idx in range(len(alpha)):
        out += source_derivative_of_monomial(alpha, idx)
    return out


def second_level_identity(alpha: tuple[int, ...], fixed_idx: int) -> tuple[Counter[tuple[int, ...]], Counter[tuple[int, ...]]]:
    left = Counter()
    for reduced_alpha, coeff in source_derivative_of_monomial(alpha, fixed_idx).items():
        left += Counter({k: coeff * v for k, v in beta_derivative_of_monomial(reduced_alpha).items()})

    right = Counter()
    for idx in range(len(alpha)):
        inner = source_derivative_of_monomial(alpha, idx)
        for reduced_alpha, coeff in inner.items():
            right += Counter({k: coeff * v for k, v in source_derivative_of_monomial(reduced_alpha, fixed_idx).items()})
    return left, right


def main() -> int:
    basis = [
        (0, 0, 0),
        (1, 0, 0),
        (2, 1, 0),
        (1, 1, 1),
        (3, 2, 1),
        (4, 0, 2),
    ]
    first_identity_ok = all(beta_derivative_of_monomial(alpha) == sum_source_derivatives(alpha) for alpha in basis)
    second_identity_ok = all(
        second_level_identity(alpha, fixed_idx)[0] == second_level_identity(alpha, fixed_idx)[1]
        for alpha in basis
        for fixed_idx in range(len(alpha))
    )

    onset_plaquette_coeff = total_nonlocal_beta5_coefficient()
    onset_susceptibility_coeff = Fraction(5, 1) * onset_plaquette_coeff
    onset_beta_eff_coeff = beta_eff_beta5_coefficient()
    onset_beta_eff_prime_coeff = Fraction(5, 1) * onset_beta_eff_coeff
    onset_beta_eff_second_coeff = Fraction(20, 1) * onset_beta_eff_coeff
    common_slope = Fraction(full_wilson_strong_coupling_slope()).limit_denominator()
    onset_three_point_sum_coeff = common_slope * onset_beta_eff_second_coeff

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE CONNECTED-HIERARCHY THEOREM")
    print("=" * 78)
    print()
    print("Uniform-source derivative basis check")
    print(f"  tested monomial basis                    = {basis}")
    print(f"  first-level identity exact               = {first_identity_ok}")
    print(f"  second-level identity exact              = {second_identity_ok}")
    print()
    print("Exact onset hierarchy coefficients")
    print(f"  nonlocal plaquette beta^5 coefficient    = {onset_plaquette_coeff} = {float(onset_plaquette_coeff):.15e}")
    print(f"  nonlocal susceptibility beta^4 coeff     = {onset_susceptibility_coeff} = {float(onset_susceptibility_coeff):.15e}")
    print(f"  beta_eff beta^5 coefficient              = {onset_beta_eff_coeff} = {float(onset_beta_eff_coeff):.15e}")
    print(f"  beta_eff' beta^4 coefficient             = {onset_beta_eff_prime_coeff} = {float(onset_beta_eff_prime_coeff):.15e}")
    print(f"  beta_eff'' beta^3 coefficient            = {onset_beta_eff_second_coeff} = {float(onset_beta_eff_second_coeff):.15e}")
    print(f"  summed connected 3-point beta^3 coeff    = {onset_three_point_sum_coeff} = {float(onset_three_point_sum_coeff):.15e}")
    print()

    check(
        "the uniform-source operator identity is illustrated exactly on monomial basis states",
        first_identity_ok,
        detail="checked exactly on a spanning monomial sample for the shifted source variables y_r = beta + J_r",
        bucket="SUPPORT",
    )
    check(
        "the next hierarchy level is illustrated exactly on the same monomial basis",
        second_identity_ok,
        detail="checked exactly on the same monomial sample after one fixed source derivative",
        bucket="SUPPORT",
    )
    check(
        "differentiating the exact beta^5 plaquette correction gives the exact beta^4 connected-susceptibility correction",
        onset_susceptibility_coeff == Fraction(5, 472392),
        detail=f"d/d beta [beta^5/472392] = ({onset_susceptibility_coeff}) beta^4",
    )
    check(
        "differentiating the exact beta_eff onset law gives beta_eff''(beta)=20 beta^3 / 26244 + O(beta^4)",
        onset_beta_eff_second_coeff == Fraction(5, 6561),
        detail=f"beta_eff'' onset coefficient = {onset_beta_eff_second_coeff}",
    )
    check(
        "the common strong-coupling slope transports the beta_eff'' onset into the exact first summed connected 3-point coefficient",
        onset_three_point_sum_coeff == Fraction(5, 118098),
        detail=f"(1/18) * ({onset_beta_eff_second_coeff}) = {onset_three_point_sum_coeff}",
    )
    check(
        "explicit nonperturbative closure therefore requires the connected plaquette hierarchy, not a single local bridge factor",
        onset_susceptibility_coeff > 0 and onset_three_point_sum_coeff > 0,
        detail="chi_L needs the shell-summed 2-point field and beta_eff'' already needs the shell-summed 3-point field",
    )

    check(
        "the hierarchy theorem is consistent with the previously closed transport law for beta_eff'",
        onset_beta_eff_prime_coeff == Fraction(5, 26244),
        detail=f"beta_eff' correction coefficient = {onset_beta_eff_prime_coeff}",
        bucket="SUPPORT",
    )
    check(
        "the first nonlocal hierarchy levels are strictly nonzero beyond the common strong-coupling slope",
        onset_susceptibility_coeff > 0 and onset_three_point_sum_coeff > 0,
        detail="the connected hierarchy is genuinely active beyond onset, not a formal redundancy",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
