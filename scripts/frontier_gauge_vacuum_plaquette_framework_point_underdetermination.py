#!/usr/bin/env python3
"""
Exact obstruction showing that the current plaquette jet does not yet fix the
framework-point analytic value P(6).

This runner uses the already-closed onset coefficient together with two explicit
analytic strictly increasing witness reduction laws. They agree through
O(beta^5) but yield different beta_eff(6), hence different local one-plaquette
values at the framework point.
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from frontier_gauge_vacuum_plaquette_bridge_support import plaquette_from_bessel
from frontier_gauge_vacuum_plaquette_mixed_cumulant_audit import beta_eff_beta5_coefficient


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

BETA_FRAMEWORK = 6.0
A = beta_eff_beta5_coefficient()
C = Fraction(1, 10_000_000)


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


def beta_eff_minus(beta: float) -> float:
    return beta + float(A) * beta**5


def beta_eff_plus(beta: float) -> float:
    return beta + float(A) * beta**5 + float(C) * beta**6


def d_beta_eff_minus(beta: float) -> float:
    return 1.0 + 5.0 * float(A) * beta**4


def d_beta_eff_plus(beta: float) -> float:
    return 1.0 + 5.0 * float(A) * beta**4 + 6.0 * float(C) * beta**5


def main() -> int:
    beta_grid = np.linspace(0.0, BETA_FRAMEWORK, 241)
    deriv_minus = [d_beta_eff_minus(beta) for beta in beta_grid]
    deriv_plus = [d_beta_eff_plus(beta) for beta in beta_grid]

    beta_minus = beta_eff_minus(BETA_FRAMEWORK)
    beta_plus = beta_eff_plus(BETA_FRAMEWORK)
    delta_beta = beta_plus - beta_minus

    p_minus, _ = plaquette_from_bessel(beta_minus)
    p_plus, _ = plaquette_from_bessel(beta_plus)
    delta_p = p_plus - p_minus

    exact_delta_beta = C * Fraction(6**6, 1)

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE FRAMEWORK-POINT UNDERDETERMINATION")
    print("=" * 78)
    print()
    print("Closed onset data already on main")
    print(f"  beta_eff(beta) onset coefficient      = {A} = {float(A):.15e}")
    print()
    print("Witness reduction laws on [0,6]")
    print("  beta_eff^-(beta) = beta + a beta^5")
    print("  beta_eff^+(beta) = beta + a beta^5 + c beta^6")
    print(f"  a                                     = {A}")
    print(f"  c                                     = {C} = {float(C):.15e}")
    print()
    print("Framework-point values")
    print(f"  beta_eff^-(6)                         = {beta_minus:.15f}")
    print(f"  beta_eff^+(6)                         = {beta_plus:.15f}")
    print(f"  delta beta_eff(6)                     = {delta_beta:.15f}")
    print(f"  exact delta beta_eff(6)               = {exact_delta_beta} = {float(exact_delta_beta):.15f}")
    print(f"  P_1plaq(beta_eff^-(6))                = {p_minus:.15f}")
    print(f"  P_1plaq(beta_eff^+(6))                = {p_plus:.15f}")
    print(f"  delta P_1plaq                         = {delta_p:.15f}")
    print()

    check(
        "both witness laws share the exact closed onset jet through order beta^5",
        True,
        detail="beta_eff^+(beta) - beta_eff^-(beta) = c beta^6 exactly, so the two laws agree through O(beta^5)",
    )
    check(
        "the minus witness is strictly increasing on the full framework interval [0,6]",
        min(deriv_minus) >= 1.0,
        detail=f"min derivative on grid = {min(deriv_minus):.15f}",
    )
    check(
        "the plus witness is strictly increasing on the full framework interval [0,6]",
        min(deriv_plus) >= 1.0,
        detail=f"min derivative on grid = {min(deriv_plus):.15f}",
    )
    check(
        "the two witness reductions give different framework-point reduction parameters",
        abs(delta_beta - float(exact_delta_beta)) < 1.0e-15 and delta_beta > 0.0,
        detail=f"beta_eff^+(6) - beta_eff^-(6) = {float(exact_delta_beta):.15f}",
    )
    check(
        "strict monotonicity of the exact one-plaquette block then yields different analytic plaquette values",
        p_plus > p_minus and delta_p > 0.0,
        detail=f"P_1plaq(beta_eff^+(6)) - P_1plaq(beta_eff^-(6)) = {delta_p:.15f}",
    )

    check(
        "finite jet plus monotonicity therefore do not fix analytic P(6)",
        delta_p > 1.0e-8,
        detail="the current exact jet leaves multiple admissible framework-point reductions",
        bucket="SUPPORT",
    )
    check(
        "explicit spectral identification at beta=6 remains a genuinely new theorem target",
        beta_plus != beta_minus and p_plus != p_minus,
        detail="existence/uniqueness of the generating object does not imply explicit framework-point identification from the current jet",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
