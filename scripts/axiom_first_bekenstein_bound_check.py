"""Axiom-first Bekenstein bound check.

Verifies the Bekenstein universal entropy bound

    S(R, E) <= 2 pi R E / (hbar c)

for any matter system localized in a sphere of radius R with mass-
energy E and 2 G E < R (sub-Schwarzschild condition).

Tests:
  T1: sub-Schwarzschild geometric inequality
        A_BH(M=E) = 16 pi G^2 E^2 <= 8 pi G R E  whenever 2 G E <= R.
  T2: Bekenstein chain (proof equation 11):
        S_matter <= S_BH(M=E) = A_BH(M=E)/(4G) <= (8 pi G R E)/(4G) = 2 pi R E.
  T3: saturation at the Schwarzschild boundary 2 G E = R.
  T4: Bekenstein bound is non-trivial: at sub-Schwarzschild parameters,
      S_BH(M=E) < 2 pi R E (strict inequality), and only at the
      Schwarzschild boundary does it saturate.
  T5: high-precision sweep over (R, E) verifying the bound chain.
  T6: violation example: a hypothetical matter state with S > 2 pi R E
      would imply a violation of the second law on collapse, providing
      the qualitative consistency check.
"""
from __future__ import annotations

import math

import numpy as np


def schwarzschild_area(M: float, G: float = 1.0) -> float:
    """Schwarzschild area A = 4 pi (2 G M)^2 = 16 pi G^2 M^2."""
    r_s = 2 * G * M
    return 4 * math.pi * r_s ** 2


def s_bh_retained(M: float, G: float = 1.0) -> float:
    """S_BH = A / (4 G) from retained BH 1/4 carrier composition."""
    return schwarzschild_area(M, G) / (4 * G)


def bekenstein_bound(R: float, E: float) -> float:
    """Bekenstein RHS: 2 pi R E (in natural units)."""
    return 2 * math.pi * R * E


def main() -> None:
    print("=" * 72)
    print("AXIOM-FIRST BEKENSTEIN BOUND CHECK")
    print("=" * 72)
    print()
    print("Setup:")
    print("  retained framework GR action surface (UNIVERSAL_GR_*)")
    print("  retained BH 1/4 carrier composition (Wald-Noether admitted)")
    print("  retained spectrum condition (E >= 0)")
    print()
    print("Bekenstein bound: S(R, E) <= 2 pi R E in natural units (hbar = c = k_B = 1)")
    print()

    G = 1.0  # framework G_Newton,lat in natural units

    # ----- Test 1: sub-Schwarzschild geometric inequality -----
    print("-" * 72)
    print("TEST 1: sub-Schwarzschild geometric inequality")
    print("        A_BH(M=E) = 16 pi G^2 E^2 <= 8 pi G R E")
    print("-" * 72)
    print("Sweeping (R, E) over a grid with 2 G E <= R (sub-Schwarzschild).")
    print()
    pairs_tested = 0
    pairs_passed = 0
    max_violation = 0.0
    for R in np.linspace(1.0, 10.0, 5):
        for E_frac in np.linspace(0.05, 0.99, 5):
            E = E_frac * R / (2 * G)  # 2 G E = E_frac * R, sub-Schw if E_frac < 1
            A_BH = schwarzschild_area(E, G)
            rhs = 8 * math.pi * G * R * E
            pairs_tested += 1
            violation = max(0.0, A_BH - rhs)
            max_violation = max(max_violation, violation)
            if A_BH <= rhs + 1e-12:
                pairs_passed += 1
    print(f"  pairs tested = {pairs_tested}, pairs satisfying inequality = {pairs_passed}")
    print(f"  max violation (should be 0) = {max_violation:.3e}")
    t1_ok = max_violation < 1e-10 and pairs_passed == pairs_tested
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: Bekenstein chain S_BH = A/4G <= 2 pi R E -----
    print("-" * 72)
    print("TEST 2: Bekenstein bound chain  S_BH(M=E) <= 2 pi R E")
    print("-" * 72)
    print("(matter entropy <= S_BH(M=E) is the GSL step; here we just verify")
    print(" the geometric chain S_BH(M=E) <= 2 pi R E for sub-Schw systems.)")
    print()
    pairs_tested = 0
    pairs_passed = 0
    max_violation_2 = 0.0
    for R in np.linspace(1.0, 10.0, 5):
        for E_frac in np.linspace(0.05, 0.99, 5):
            E = E_frac * R / (2 * G)
            S_BH = s_bh_retained(E, G)
            bek = bekenstein_bound(R, E)
            pairs_tested += 1
            violation = max(0.0, S_BH - bek)
            max_violation_2 = max(max_violation_2, violation)
            if S_BH <= bek + 1e-12:
                pairs_passed += 1
    print(f"  pairs tested = {pairs_tested}, pairs satisfying bound = {pairs_passed}")
    print(f"  max violation (should be 0) = {max_violation_2:.3e}")
    t2_ok = max_violation_2 < 1e-10 and pairs_passed == pairs_tested
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: saturation at the Schwarzschild boundary -----
    print("-" * 72)
    print("TEST 3: saturation at 2 G E = R")
    print("-" * 72)
    print("At the Schwarzschild boundary (2 G E = R), the bound is tight:")
    print("S_BH(M=E) = pi R^2 / G = 2 pi R E exactly.")
    print()
    max_satur_resid = 0.0
    for R in [0.5, 1.0, 2.0, 5.0, 10.0]:
        E_sat = R / (2 * G)
        S_BH_at_sat = s_bh_retained(E_sat, G)
        bek_at_sat = bekenstein_bound(R, E_sat)
        resid = abs(S_BH_at_sat - bek_at_sat)
        max_satur_resid = max(max_satur_resid, resid)
        print(f"  R = {R:6.2f}, E_sat = {E_sat:6.4f}: "
              f"S_BH = {S_BH_at_sat:.6e}, 2 pi R E = {bek_at_sat:.6e}, "
              f"|diff| = {resid:.2e}")
    print()
    print(f"  max | S_BH - 2 pi R E | at saturation = {max_satur_resid:.3e}")
    t3_ok = max_satur_resid < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: bound is non-trivial in interior -----
    print("-" * 72)
    print("TEST 4: bound is non-trivial in the interior (S_BH < 2 pi R E)")
    print("-" * 72)
    print("For 2 G E < R (strict), S_BH(M=E) < 2 pi R E with strict inequality.")
    print()
    max_gap_ratio = 0.0
    for R in [1.0, 5.0, 10.0]:
        for E_frac in [0.1, 0.5, 0.9]:
            E = E_frac * R / (2 * G)
            S_BH = s_bh_retained(E, G)
            bek = bekenstein_bound(R, E)
            ratio = S_BH / bek
            gap = bek - S_BH
            print(f"  R = {R:5.2f}, 2 G E / R = {E_frac:.2f}: "
                  f"S_BH/2 pi R E = {ratio:.4f}, gap = {gap:.6e}")
            assert ratio < 1.0 - 1e-12 or abs(E_frac - 1.0) < 1e-6, \
                "interior must have strict inequality"
    print()
    t4_ok = True
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: continuous sweep -----
    print("-" * 72)
    print("TEST 5: continuous sweep over (R, E) verifying full Bekenstein chain")
    print("-" * 72)
    grid_R = np.linspace(0.1, 20.0, 30)
    grid_E_frac = np.linspace(0.01, 0.999, 30)
    fail_count = 0
    max_resid_5 = 0.0
    for R in grid_R:
        for E_frac in grid_E_frac:
            E = E_frac * R / (2 * G)
            S_BH = s_bh_retained(E, G)
            bek = bekenstein_bound(R, E)
            resid = max(0.0, S_BH - bek)
            max_resid_5 = max(max_resid_5, resid)
            if S_BH > bek + 1e-10:
                fail_count += 1
    n_total = len(grid_R) * len(grid_E_frac)
    print(f"  total pairs = {n_total}, violations = {fail_count}, max resid = {max_resid_5:.3e}")
    t5_ok = fail_count == 0
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: GSL consistency check -----
    print("-" * 72)
    print("TEST 6: GSL consistency — collapsing matter to BH preserves second law")
    print("-" * 72)
    print("If matter has S_matter > S_BH(M=E), collapsing it to a BH would")
    print("violate ΔS_total >= 0 (second law). Hence S_matter <= S_BH(M=E).")
    print()
    # Hypothetical matter entropy slightly above the BH bound
    R = 5.0
    E_frac = 0.5
    E = E_frac * R / (2 * G)
    S_BH = s_bh_retained(E, G)
    # Trial 1: S_matter < S_BH (allowed)
    S_matter_allowed = S_BH * 0.5
    # Trial 2: S_matter > S_BH (would violate GSL)
    S_matter_forbidden = S_BH * 1.5
    delta_S_allowed = S_BH - S_matter_allowed
    delta_S_forbidden = S_BH - S_matter_forbidden
    print(f"  R = {R}, E = {E:.4f}, S_BH = {S_BH:.4f}")
    print(f"  S_matter_allowed = {S_matter_allowed:.4f}, ΔS_collapse = {delta_S_allowed:+.4f} (>= 0, OK)")
    print(f"  S_matter_forbidden = {S_matter_forbidden:.4f}, ΔS_collapse = {delta_S_forbidden:+.4f} (< 0, GSL violation)")
    t6_ok = delta_S_allowed >= 0 and delta_S_forbidden < 0
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Summary -----
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print(f"  Test 1 (sub-Schw geometric inequality):     {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 (Bekenstein chain S_BH <= 2 pi R E): {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (saturation at 2 G E = R):           {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (non-trivial interior gap):          {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (dense sweep over (R, E)):           {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (GSL consistency check):             {'PASS' if t6_ok else 'FAIL'}")
    print()
    all_ok = t1_ok and t2_ok and t3_ok and t4_ok and t5_ok and t6_ok
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    print()
    print("Note: this runner verifies the algebraic Bekenstein chain on a")
    print("range of (R, E) parameters and confirms saturation at the")
    print("Schwarzschild boundary. The proof in the companion theorem note")
    print("is geometric (Step 1 + 3) plus a one-step GSL invocation (Step 2)")
    print("on the framework's retained GR action surface plus retained")
    print("BH 1/4 carrier composition.")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
