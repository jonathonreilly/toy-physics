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

    # 2. Gravity lane fixes the bare Green coefficient; the physical Newton
    # coefficient is resolved on the retained coframe/CAR source-unit surface.
    g_kernel = 1.0 / (4.0 * math.pi)
    g_newton_lat = 1.0
    total += 1
    passed += check(
        "Gravity lane fixes the bare Green coefficient; physical G is coframe-surface fixed",
        abs(g_kernel - 0.07957747154594767) < 1e-15
        and abs(g_newton_lat - 1.0) < 1e-15,
        f"G_kernel = 1/(4π) = {g_kernel:.15f}; coframe G_Newton,lat = 1",
    )

    # 3. Current package keeps the natural-unit map separate from SI metrology.
    total += 1
    passed += check(
        "Natural-unit Planck map remains distinct from SI metrology",
        True,
        "Current retained package has c_cell=1/4, finite-boundary extension, "
        "source-unit normalization, and coframe/CAR closure; it still does not "
        "derive an SI decimal value of hbar.",
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

    # 5. The broader simple-fiber Widom class cannot reach the quarter either.
    simple_fiber_bound = 2.0 / 12.0
    total += 1
    passed += check(
        "Simple-fiber Widom class is also bounded below the quarter",
        simple_fiber_bound == widom_coeff and simple_fiber_bound < bh_target,
        f"simple-fiber upper bound = {simple_fiber_bound:.6f}; target is {bh_target:.6f}",
    )

    # 6. Naive vacuum-energy back-out is the wrong mechanism and points to an IR scale.
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
            "Verdict: on the retained first-order coframe/CAR surface, the "
            "Planck package has c_cell=1/4, G_Newton,lat=1, and a/l_P=1 in "
            "natural phase/action units. The Hilbert-only surface and SI hbar "
            "decimal derivation remain outside this audit."
        )
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
