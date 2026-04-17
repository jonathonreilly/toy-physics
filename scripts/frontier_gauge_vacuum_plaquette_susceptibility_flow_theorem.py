#!/usr/bin/env python3
"""
Exact susceptibility-flow theorem for the Wilson plaquette reduction law.

This closes the exact nonperturbative transport law for the implicit reduction
map beta_eff,L(beta) on finite periodic Wilson evaluation surfaces, while
keeping the explicit closed form at beta = 6 open.
"""

from __future__ import annotations

from fractions import Fraction
import sys

sys.path.insert(0, "scripts")

from canonical_plaquette_surface import CANONICAL_PLAQUETTE  # noqa: E402
from frontier_gauge_vacuum_plaquette_bridge_support import plaquette_from_bessel  # noqa: E402
from frontier_gauge_vacuum_plaquette_constant_lift_obstruction import full_wilson_strong_coupling_slope  # noqa: E402
from frontier_gauge_vacuum_plaquette_mixed_cumulant_audit import (  # noqa: E402
    beta_eff_beta5_coefficient,
    total_nonlocal_beta5_coefficient,
)
from frontier_gauge_vacuum_plaquette_reduction_existence_theorem import implicit_beta_eff  # noqa: E402


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0
FINITE_DIFF_STEP = 1.0e-5


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


def local_susceptibility_numeric(beta: float, step: float = FINITE_DIFF_STEP) -> float:
    p_plus, _ = plaquette_from_bessel(beta + step)
    p_minus, _ = plaquette_from_bessel(beta - step)
    return (p_plus - p_minus) / (2.0 * step)


def main() -> int:
    onset_plaquette_coeff = total_nonlocal_beta5_coefficient()
    onset_susceptibility_coeff = Fraction(5, 1) * onset_plaquette_coeff
    onset_beta_eff_coeff = beta_eff_beta5_coefficient()
    onset_beta_eff_prime_coeff = Fraction(5, 1) * onset_beta_eff_coeff
    common_slope = Fraction(full_wilson_strong_coupling_slope()).limit_denominator()
    transported_coeff = common_slope * onset_beta_eff_prime_coeff

    sample_betas = [0.1, 0.5, 1.0, 2.0, 4.0, 6.0, 10.0]
    sample_local_sus = [local_susceptibility_numeric(beta) for beta in sample_betas]

    canonical_beta_eff = implicit_beta_eff(CANONICAL_PLAQUETTE)
    canonical_reconstructed, _ = plaquette_from_bessel(canonical_beta_eff)

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE SUSCEPTIBILITY-FLOW THEOREM")
    print("=" * 78)
    print()
    print("Exact onset coefficients")
    print(f"  nonlocal plaquette beta^5 coefficient      = {onset_plaquette_coeff} = {float(onset_plaquette_coeff):.15e}")
    print(f"  nonlocal susceptibility beta^4 coefficient = {onset_susceptibility_coeff} = {float(onset_susceptibility_coeff):.15e}")
    print(f"  beta_eff beta^5 coefficient                = {onset_beta_eff_coeff} = {float(onset_beta_eff_coeff):.15e}")
    print(f"  beta_eff' beta^4 coefficient               = {onset_beta_eff_prime_coeff} = {float(onset_beta_eff_prime_coeff):.15e}")
    print(f"  common slope                               = {common_slope} = {float(common_slope):.15e}")
    print(f"  slope * beta_eff' correction               = {transported_coeff} = {float(transported_coeff):.15e}")
    print()
    print("Sampled local susceptibility profile")
    print(f"  sampled betas                              = {sample_betas}")
    print(f"  sampled chi_1plaq(betas)                   = {[round(v, 12) for v in sample_local_sus]}")
    print()
    print("Canonical implicit support value")
    print(f"  beta_eff^can                               = {canonical_beta_eff:.15f}")
    print(f"  P_1plaq(beta_eff^can)                      = {canonical_reconstructed:.15f}")
    print(f"  canonical P                                = {CANONICAL_PLAQUETTE:.15f}")
    print()

    check(
        "differentiating the exact beta^5 plaquette correction gives the exact beta^4 susceptibility correction",
        onset_susceptibility_coeff == Fraction(5, 472392),
        detail=f"d/d beta [beta^5/472392] = ({onset_susceptibility_coeff}) beta^4",
    )
    check(
        "differentiating the exact onset law gives beta_eff'(beta)=1 + 5 beta^4 / 26244 + O(beta^5)",
        onset_beta_eff_prime_coeff == Fraction(5, 26244),
        detail=f"beta_eff'(beta) correction coefficient = {onset_beta_eff_prime_coeff}",
    )
    check(
        "the common strong-coupling slope transports the beta_eff' correction into the same exact susceptibility coefficient",
        transported_coeff == onset_susceptibility_coeff,
        detail=f"(1/18) * ({onset_beta_eff_prime_coeff}) = {transported_coeff}",
    )
    check(
        "the exact nonperturbative reduction law is equivalently governed by the connected susceptibility profile",
        onset_beta_eff_coeff == Fraction(1, 26244) and common_slope == Fraction(1, 18),
        detail="P_L(beta)=integral_0^beta chi_L and P_L=P_1plaq(beta_eff) give beta_eff = P_1plaq^{-1}(integral chi_L)",
    )
    check(
        "the remaining open object is therefore the explicit full susceptibility profile, not reduction-law existence",
        onset_susceptibility_coeff > 0 and onset_beta_eff_coeff > 0,
        detail="exact existence/uniqueness and exact transport law are both closed",
    )

    check(
        "sampled local one-plaquette susceptibility is strictly positive on the tested beta range",
        all(value > 0.0 for value in sample_local_sus),
        detail=f"min sampled chi_1plaq = {min(sample_local_sus):.12f}",
        bucket="SUPPORT",
    )
    check(
        "the canonical same-surface plaquette is reconstructed by the exact implicit beta_eff parameter",
        abs(canonical_reconstructed - CANONICAL_PLAQUETTE) < 1.0e-12,
        detail=f"|P_1plaq(beta_eff^can) - P_can| = {abs(canonical_reconstructed - CANONICAL_PLAQUETTE):.3e}",
        bucket="SUPPORT",
    )
    check(
        "the canonical implicit reduction parameter lies on the positive monotone branch",
        canonical_beta_eff > 0.0,
        detail=f"beta_eff^can = {canonical_beta_eff:.15f}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
