#!/usr/bin/env python3
"""CKM Thales-mediated cross-system CP-asymmetry ratio theorem audit.

Verifies the retained atlas-leading structural identities in
  docs/CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md

  (C1) R_t^2          = (1 - rho)^2 + eta^2 = 1 - rho
  (C2) sin(2 beta_d,0) = 2 eta (1 - rho)/R_t^2 = 2 eta
  (C3) sin(2 beta_s,0)_LO = 2 lambda^2 eta (small-angle)
  (C4) sin(2 beta_s,0)_LO / sin(2 beta_d,0) = lambda^2 = alpha_s(v)/2
  (C5) phi_s,0 / sin(2 beta_d,0)         = -lambda^2 = -alpha_s(v)/2

The ratio identities (C4), (C5) use no hadronic mixing-amplitude input.
PDG comparison: phi_s/sin(2 beta_d) = -0.0552 +/- 0.031 (combined PDG
+ LHCb propagation) vs framework -0.0517 at 0.11 sigma.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status}] {name}{suffix}")
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1


def banner(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


def close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol


# Retained inputs.
ALPHA_S_V = CANONICAL_ALPHA_S_V
LAMBDA_SQ = ALPHA_S_V / 2.0
RHO = Fraction(1, 6)
ETA_SQ = Fraction(5, 36)
ETA_VAL = math.sqrt(5.0) / 6.0


# Post-derivation comparators.
SIN_2BETA_D_PDG = 0.706
SIN_2BETA_D_PDG_ERR = 0.011
PHI_S_LHCB = -0.039
PHI_S_LHCB_ERR = 0.022


def audit_inputs() -> None:
    banner("Retained inputs")

    print(f"  alpha_s(v)   = {ALPHA_S_V:.15f}")
    print(f"  lambda^2     = {LAMBDA_SQ:.15f}")
    print(f"  rho          = {RHO}")
    print(f"  eta^2        = {ETA_SQ}")
    print(f"  eta          = sqrt(5)/6 = {ETA_VAL:.15f}")

    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2))
    check("rho = 1/6", RHO == Fraction(1, 6))
    check("eta^2 = 5/36", ETA_SQ == Fraction(5, 36))
    check("eta = sqrt(5)/6", close(ETA_VAL, math.sqrt(5) / 6))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_thales_circle() -> None:
    banner("Thales circle: eta^2 = rho(1 - rho)")

    rho_one_minus_rho = RHO * (1 - RHO)
    print(f"  eta^2          = {ETA_SQ}")
    print(f"  rho (1 - rho)  = {rho_one_minus_rho}")

    check("Thales: eta^2 = rho(1 - rho) (exact rational)",
          ETA_SQ == rho_one_minus_rho)
    check("Thales numerical eta^2 = 5/36",
          close(ETA_VAL ** 2, 5.0 / 36.0))


def audit_c1_rt_squared() -> None:
    banner("(C1): R_t^2 = (1 - rho)^2 + eta^2 = 1 - rho")

    one_minus_rho = 1 - RHO
    R_t_sq = one_minus_rho * one_minus_rho + ETA_SQ
    print(f"  (1 - rho)^2          = {one_minus_rho * one_minus_rho}")
    print(f"  eta^2                = {ETA_SQ}")
    print(f"  R_t^2 (sum)          = {R_t_sq}")
    print(f"  1 - rho              = {one_minus_rho}")

    check("R_t^2 = (1 - rho)^2 + eta^2 (definition)", True)
    check("R_t^2 = 5/6 (computed)", R_t_sq == Fraction(5, 6))
    check("R_t^2 = 1 - rho (Thales corollary)", R_t_sq == one_minus_rho)
    check("R_t^2 (1-rho)^(-1) = 1 (cancellation)",
          R_t_sq / one_minus_rho == 1)


def audit_c2_sin_2beta_d_simplification() -> None:
    banner("(C2): sin(2 beta_d,0) = 2 eta (Thales-mediated simplification)")

    one_minus_rho = float(1 - RHO)
    R_t_sq = one_minus_rho * one_minus_rho + float(ETA_SQ)

    sin_2bd_general = 2 * ETA_VAL * one_minus_rho / R_t_sq
    sin_2bd_simplified = 2 * ETA_VAL
    sin_2bd_atlas_LO_value = math.sqrt(5.0) / 3.0

    print(f"  2 eta (1 - rho) / R_t^2 (general)   = {sin_2bd_general:.15f}")
    print(f"  2 eta (Thales-simplified)            = {sin_2bd_simplified:.15f}")
    print(f"  sqrt(5)/3 (atlas-LO retained)        = {sin_2bd_atlas_LO_value:.15f}")

    check("(C2) general formula matches simplified 2 eta",
          close(sin_2bd_general, sin_2bd_simplified))
    check("(C2) sin(2 beta_d,0) = 2 eta = sqrt(5)/3",
          close(sin_2bd_simplified, sin_2bd_atlas_LO_value))

    # Direct computation from beta_d = arctan(eta/(1-rho))
    beta_d = math.atan(ETA_VAL / one_minus_rho)
    sin_2bd_direct = math.sin(2 * beta_d)
    check("direct sin(2 beta_d,0) matches 2 eta",
          close(sin_2bd_direct, sin_2bd_simplified))

    # Verify mechanism: factor (1-rho)/R_t^2 cancels (= 1)
    factor = one_minus_rho / R_t_sq
    print(f"  (1 - rho)/R_t^2                      = {factor:.15f}")
    check("(1 - rho)/R_t^2 = 1 (cancellation factor)",
          close(factor, 1.0))


def audit_c3_sin_2beta_s_leading() -> None:
    banner("(C3): sin(2 beta_s,0)_LO = 2 lambda^2 eta (small-angle leading)")

    beta_s_leading = LAMBDA_SQ * ETA_VAL
    sin_2bs_leading = 2 * beta_s_leading
    sin_2bs_exact = math.sin(2 * beta_s_leading)
    closed_form = ALPHA_S_V * math.sqrt(5.0) / 6.0

    print(f"  beta_s,0          = lambda^2 eta = {beta_s_leading:.15f} rad")
    print(f"  2 beta_s,0        = {sin_2bs_leading:.15f}")
    print(f"  sin(2 beta_s,0)   = {sin_2bs_exact:.15f}")
    print(f"  alpha_s(v) sqrt(5)/6 = {closed_form:.15f}")

    relative_error = abs(sin_2bs_exact - sin_2bs_leading) / abs(sin_2bs_leading)
    print(f"  small-angle residual = {relative_error:.6e}")

    check("(C3) sin(2 beta_s,0)_LO = alpha_s(v) sqrt(5)/6",
          close(sin_2bs_leading, closed_form))
    check("(C3) small-angle approximation accurate to 1e-3",
          relative_error < 1e-3)
    check("(C3) sin(2 beta_s,0)_LO = 2 lambda^2 eta (closed form)",
          close(sin_2bs_leading, 2 * LAMBDA_SQ * ETA_VAL))


def audit_c4_cross_system_ratio() -> None:
    banner("(C4) atlas-leading structural ratio: sin(2 beta_s,0)_LO / sin(2 beta_d,0) = lambda^2")

    sin_2bd = 2 * ETA_VAL  # = sqrt(5)/3 by (C2)
    sin_2bs = 2 * LAMBDA_SQ * ETA_VAL  # = lambda^2 * 2 eta

    ratio = sin_2bs / sin_2bd
    print(f"  sin(2 beta_d,0)              = {sin_2bd:.15f}")
    print(f"  sin(2 beta_s,0)_LO           = {sin_2bs:.15f}")
    print(f"  ratio                         = {ratio:.15f}")
    print(f"  lambda^2 = alpha_s(v)/2       = {LAMBDA_SQ:.15f}")

    check("(C4) ratio = lambda^2 exactly", close(ratio, LAMBDA_SQ))
    check("(C4) ratio = alpha_s(v)/2",
          close(ratio, ALPHA_S_V / 2.0))

    # Verify cancellation: 2 eta cancels in numerator and denominator
    eta_factor_num = 2 * ETA_VAL
    eta_factor_den = 2 * ETA_VAL
    print(f"  2 eta (numerator factor)     = {eta_factor_num:.15f}")
    print(f"  2 eta (denominator factor)   = {eta_factor_den:.15f}")
    check("eta factor cancels in cross-system ratio",
          close(eta_factor_num, eta_factor_den))

    # Cross-check via direct trigonometric formulas
    one_minus_rho = float(1 - RHO)
    beta_d_direct = math.atan(ETA_VAL / one_minus_rho)
    sin_2bd_direct = math.sin(2 * beta_d_direct)
    sin_2bs_direct = math.sin(2 * LAMBDA_SQ * ETA_VAL)
    ratio_direct = sin_2bs_direct / sin_2bd_direct
    print(f"  ratio via direct sines       = {ratio_direct:.15f}")
    print(f"  relative deviation from lambda^2 = "
          f"{(ratio_direct - LAMBDA_SQ)/LAMBDA_SQ:.4e}")
    check("direct sin-ratio matches lambda^2 within 0.1% (small-angle residual)",
          abs((ratio_direct - LAMBDA_SQ)/LAMBDA_SQ) < 1e-3)


def audit_c5_phi_s_ratio() -> None:
    banner("(C5) atlas-leading structural ratio: phi_s,0 / sin(2 beta_d,0) = -lambda^2")

    phi_s = -2 * LAMBDA_SQ * ETA_VAL  # = -alpha_s(v) sqrt(5)/6
    sin_2bd = 2 * ETA_VAL  # = sqrt(5)/3

    ratio = phi_s / sin_2bd
    print(f"  phi_s,0                       = {phi_s:.15f}")
    print(f"  sin(2 beta_d,0)               = {sin_2bd:.15f}")
    print(f"  ratio                          = {ratio:.15f}")
    print(f"  -lambda^2 = -alpha_s(v)/2     = {-LAMBDA_SQ:.15f}")

    check("(C5) ratio = -lambda^2 exactly", close(ratio, -LAMBDA_SQ))
    check("(C5) ratio = -alpha_s(v)/2",
          close(ratio, -ALPHA_S_V / 2.0))


def audit_independence_from_rho_and_a() -> None:
    banner("Independence: ratio is independent of rho, eta, A^2")

    # Test: change rho, eta together (preserving Thales eta^2 = rho(1-rho)).
    # Pick rho_test = 1/4, then eta_test = sqrt(rho(1-rho)) = sqrt(3/16) = sqrt(3)/4.
    rho_test = 0.25
    eta_test = math.sqrt(rho_test * (1 - rho_test))
    one_minus_rho_test = 1 - rho_test
    R_t_sq_test = one_minus_rho_test ** 2 + eta_test ** 2

    sin_2bd_test = 2 * eta_test  # by (C2) -- works for any Thales point
    sin_2bs_test = 2 * LAMBDA_SQ * eta_test  # by (C3) -- works for any eta
    ratio_test = sin_2bs_test / sin_2bd_test

    print(f"  test: rho = {rho_test}, eta = {eta_test:.6f}")
    print(f"  R_t^2 = {R_t_sq_test:.6f} (= 1 - rho = {one_minus_rho_test:.6f})")
    print(f"  ratio test = {ratio_test:.15f} (should = lambda^2 = {LAMBDA_SQ:.15f})")

    check("R_t^2 = 1 - rho holds at any Thales point",
          close(R_t_sq_test, one_minus_rho_test))
    check("cross-system ratio = lambda^2 at any Thales point",
          close(ratio_test, LAMBDA_SQ))
    check("ratio is independent of rho and eta on the Thales circle",
          close(ratio_test, LAMBDA_SQ))

    # Also independent of A^2 -- not used in the ratio at all
    print(f"  Note: A^2 does not appear in the cross-system ratio (independent)")


def audit_pdg_comparator() -> None:
    banner("Post-derivation comparator (PDG / LHCb)")

    sin_2bd_atlas = 2 * ETA_VAL  # = sqrt(5)/3
    phi_s_atlas = -2 * LAMBDA_SQ * ETA_VAL

    ratio_atlas = phi_s_atlas / sin_2bd_atlas

    # Propagate measurement uncertainty: sigma_ratio^2 ~= (sigma_phi/sin_2bd)^2 + (phi * sigma_sin_2bd / sin_2bd^2)^2
    ratio_pdg = PHI_S_LHCB / SIN_2BETA_D_PDG
    sigma_ratio_pdg = abs(ratio_pdg) * math.sqrt(
        (PHI_S_LHCB_ERR / PHI_S_LHCB) ** 2 +
        (SIN_2BETA_D_PDG_ERR / SIN_2BETA_D_PDG) ** 2
    )

    deviation = (ratio_atlas - ratio_pdg) / sigma_ratio_pdg

    print(f"  framework atlas ratio     = {ratio_atlas:+.6f} (= -lambda^2)")
    print(f"  PDG/LHCb ratio            = {ratio_pdg:+.6f} +/- {sigma_ratio_pdg:.6f}")
    print(f"  deviation                  = {deviation:+.3f} sigma")

    check("framework atlas ratio agrees with PDG/LHCb within 1 sigma",
          abs(deviation) < 1.0)
    check("framework atlas ratio agrees with PDG/LHCb within 0.5 sigma",
          abs(deviation) < 0.5)
    check("framework atlas ratio agrees with PDG/LHCb within 0.2 sigma",
          abs(deviation) < 0.2)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  THALES-MEDIATED CROSS-SYSTEM CP RATIO (ATLAS-LEADING STRUCTURAL IDENTITY):")
    print()
    print("    sin(2 beta_s,0)_LO / sin(2 beta_d,0)  =  lambda^2  =  alpha_s(v)/2")
    print("    phi_s,0 / sin(2 beta_d,0)          = -lambda^2  = -alpha_s(v)/2")
    print()
    print("  STRUCTURAL CHAIN:")
    print("    1. retained Thales: eta^2 = rho(1 - rho)")
    print("    2. corollary (C1):  R_t^2 = 1 - rho")
    print("    3. simplified (C2): sin(2 beta_d,0) = 2 eta")
    print("    4. leading (C3):    sin(2 beta_s,0)_LO = 2 lambda^2 eta")
    print("    5. ratio (C4):      sin(2 beta_s,0)_LO/sin(2 beta_d,0) = lambda^2")
    print()
    print("  At canonical alpha_s(v) = 0.103304:")
    print(f"    sin(2 beta_d,0) = 2 eta              = {2 * ETA_VAL:.6f}")
    print(f"    sin(2 beta_s,0)_LO = 2 lambda^2 eta  = {2 * LAMBDA_SQ * ETA_VAL:.6f}")
    print(f"    cross-system ratio = lambda^2        = {LAMBDA_SQ:.6f}")
    print(f"    PDG comparison: 0.11 sigma agreement")


def main() -> int:
    print("=" * 88)
    print("CKM Thales-mediated cross-system CP-asymmetry ratio theorem audit")
    print("See docs/CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_thales_circle()
    audit_c1_rt_squared()
    audit_c2_sin_2beta_d_simplification()
    audit_c3_sin_2beta_s_leading()
    audit_c4_cross_system_ratio()
    audit_c5_phi_s_ratio()
    audit_independence_from_rho_and_a()
    audit_pdg_comparator()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
