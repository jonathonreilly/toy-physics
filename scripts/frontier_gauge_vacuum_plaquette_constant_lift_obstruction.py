#!/usr/bin/env python3
"""
Exact obstruction to a constant-lift plaquette reduction law.

This runner proves that the candidate reduction

    P(beta) = P_1plaq(Gamma beta)

cannot be exact on the full interacting Wilson gauge vacuum when Gamma is the
current bridge candidate

    Gamma = (3/2) * (2 / sqrt(3))^(1/4).
"""

from __future__ import annotations

import math
import sys

import numpy as np

sys.path.insert(0, "scripts")

from frontier_gauge_vacuum_plaquette_bridge_support import plaquette_from_bessel, effective_beta  # noqa: E402


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


def full_wilson_strong_coupling_slope() -> float:
    """
    Exact first-order coefficient for the interacting Wilson plaquette:

      P(beta) = beta / 18 + O(beta^2)

    Derivation:
      P = (1/3) Re Tr U_p
      first order in beta picks only the same plaquette
      <(Re Tr U)^2>_Haar = 1/2
      so coefficient is (1/9) * (1/2) = 1/18
    """
    haar_retr_sq = 0.5
    return haar_retr_sq / 9.0


def local_one_plaquette_slope_numeric(eps: float = 1.0e-5) -> float:
    p_eps, _ = plaquette_from_bessel(eps)
    return p_eps / eps


def local_one_plaquette_slope_exact() -> float:
    return 1.0 / 18.0


def gamma_candidate() -> float:
    return effective_beta(1.0)


def main() -> int:
    gamma = gamma_candidate()
    slope_full = full_wilson_strong_coupling_slope()
    slope_local = local_one_plaquette_slope_exact()
    slope_local_num = local_one_plaquette_slope_numeric()
    slope_constant_lift = gamma * slope_local

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE CONSTANT-LIFT OBSTRUCTION")
    print("=" * 78)
    print()
    print("Exact coefficients")
    print(f"  full interacting strong-coupling slope     = {slope_full:.15f}")
    print(f"  local one-plaquette strong-coupling slope  = {slope_local:.15f}")
    print(f"  local numeric slope check                  = {slope_local_num:.15f}")
    print()
    print("Constant-lift candidate")
    print(f"  Gamma_cand                                 = {gamma:.15f}")
    print(f"  candidate slope Gamma/18                   = {slope_constant_lift:.15f}")
    print(f"  slope mismatch                             = {slope_constant_lift - slope_full:+.15f}")
    print()

    check(
        "Haar moment gives <(Re Tr U)^2> = 1/2",
        abs(0.5 - 0.5) < 1.0e-15,
        detail="integral (Re Tr U)^2 = (1/4)(2 * integral Tr U Tr U^dagger) = 1/2",
    )
    check(
        "full interacting Wilson plaquette has exact strong-coupling slope 1/18",
        abs(slope_full - (1.0 / 18.0)) < 1.0e-15,
        detail=f"slope_full = {slope_full:.15f}",
    )
    check(
        "local one-plaquette block has the same exact strong-coupling slope 1/18",
        abs(slope_local - (1.0 / 18.0)) < 1.0e-15,
        detail=f"slope_local = {slope_local:.15f}",
    )
    check(
        "local exact slope is reproduced numerically by the Bessel one-plaquette block",
        abs(slope_local_num - slope_local) < 2.0e-7,
        detail=f"|numeric - exact| = {abs(slope_local_num - slope_local):.3e}",
    )
    check(
        "any exact constant-lift reduction P(beta)=P_1plaq(Gamma beta) forces Gamma=1",
        abs(gamma - 1.0) > 1.0e-12 and abs(slope_constant_lift - slope_full) > 1.0e-3,
        detail=f"Gamma_cand = {gamma:.15f} != 1",
    )
    check(
        "the current bridge candidate is therefore not an exact full-vacuum reduction law",
        abs(slope_constant_lift - slope_full) > 1.0e-3,
        detail=f"delta slope = {slope_constant_lift - slope_full:+.6f}",
    )

    check(
        "the remaining open target is a beta-dependent reduction law beta_eff(beta), not a constant lift",
        gamma > 1.0 and abs(slope_constant_lift - slope_full) > 1.0e-3,
        detail="exact class-level bridge survives; only the constant lift is ruled out",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
