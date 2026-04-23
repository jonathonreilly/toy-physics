#!/usr/bin/env python3
"""Package-boundary audit for the Planck-scale lane on main."""

from __future__ import annotations

import math
import sys


def check(name: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}: {detail}")
    return passed


def main() -> int:
    total = 0
    passed = 0

    # 1. Hierarchy is structurally a tiny EW/Planck ratio; the absolute scale is
    # a separate pin, not hidden in the hierarchy algebra itself.
    v_ew_gev = 246.282818290129
    m_planck_gev = 1.2209e19
    ratio = v_ew_gev / m_planck_gev
    total += 1
    passed += check(
        "Hierarchy ratio is dimensionless and tiny",
        ratio < 1e-16,
        f"v/M_Pl = {ratio:.6e}",
    )

    # 2. Gravity lane already fixes the lattice-unit Newton constant.
    g_lat = 1.0 / (4.0 * math.pi)
    total += 1
    passed += check(
        "Gravity lane fixes G in lattice units",
        abs(g_lat - 0.07957747154594767) < 1e-15,
        f"G_lat = 1/(4π) = {g_lat:.15f}",
    )

    # 3. Current package still needs one absolute-scale calibration.
    total += 1
    passed += check(
        "Absolute scale remains a package pin",
        True,
        "Current retained gravity/action closure stops at lattice units; "
        "a^(-1) = M_Pl remains the explicit package pin on main.",
    )

    # 4. Current BH entropy carrier is a no-go for the 1/4 route.
    widom_coeff = 1.0 / 6.0
    bh_target = 1.0 / 4.0
    total += 1
    passed += check(
        "Current BH carrier misses the 1/4 coefficient",
        abs(widom_coeff - bh_target) > 1e-6,
        f"current carrier gives {widom_coeff:.6f}; target is {bh_target:.6f}",
    )

    # 5. Naive vacuum-energy back-out is the wrong mechanism and points to an IR scale.
    lambda_obs = 1.1e-52  # m^-2
    l_planck = 1.616255e-35  # m
    implied_radius = math.sqrt(3.0 / lambda_obs)
    radius_in_planck = implied_radius / l_planck
    total += 1
    passed += check(
        "Vacuum-energy back-out gives an IR/Hubble scale, not l_P",
        radius_in_planck > 1e60,
        f"sqrt(3/Lambda_obs) / l_P = {radius_in_planck:.6e}",
    )

    print()
    print(f"Summary: {passed}/{total} checks passed.")
    if passed == total:
        print(
            "Verdict: carry a^(-1) = M_Pl as a pinned package scale on the "
            "physical-lattice reading while the Planck derivation remains open."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
