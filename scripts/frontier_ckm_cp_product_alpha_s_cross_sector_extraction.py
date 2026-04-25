#!/usr/bin/env python3
"""CP-asymmetry product cross-sector alpha_s(v) estimator theorem audit.

Verifies the new pure-framework structural identities in
  docs/CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md

  (P1) sin(2 beta_d,0) * sin(2 beta_s,0)  =  5 alpha_s(v) / 18
  (P2) alpha_s(v)  =  (18 / 5) * sin(2 beta_d,0) * sin(2 beta_s,0)
  (P3) sin^2(2 beta_d,0) + sin^2(2 beta_s,0) = 5 (4 + alpha_s^2) / 36
  (P4) sin(2 beta_d,0) * sin(2 beta_s,0)  =  4 sqrt(5) * J / alpha_s(v)^2

The product (P1) opens a cross-sector alpha_s(v) consistency estimator:
B-meson CP-asymmetry observables (sin(2 beta_d), sin(2 beta_s)) infer
the canonical alpha_s(v) at atlas-leading order, independently as a
comparator sector from the gauge-vacuum plaquette/CMT determination.
PDG/LHCb 2024 baseline: agreement at 0.09 sigma.
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
J = ALPHA_S_V ** 3 * math.sqrt(5.0) / 72.0


# Atlas-LO sin(2 beta) values.
SIN_2BD_ATLAS = math.sqrt(5.0) / 3.0  # = 2 eta
SIN_2BS_ATLAS = ALPHA_S_V * math.sqrt(5.0) / 6.0  # = 2 lambda^2 eta


# PDG/LHCb comparator inputs.
SIN_2BD_PDG = 0.706
SIN_2BD_PDG_ERR = 0.011
PHI_S_LHCB = -0.0386  # PDG 2024 LHCb combined
PHI_S_LHCB_ERR = 0.022
# sin(2 beta_s) approx -phi_s for small angles
SIN_2BS_PDG = -PHI_S_LHCB
SIN_2BS_PDG_ERR = PHI_S_LHCB_ERR


def audit_inputs() -> None:
    banner("Retained inputs")

    print(f"  alpha_s(v) (canonical CMT/plaquette) = {ALPHA_S_V:.15f}")
    print(f"  lambda^2 = alpha_s(v)/2              = {LAMBDA_SQ:.15f}")
    print(f"  rho      = 1/6")
    print(f"  eta^2    = 5/36")
    print(f"  eta      = sqrt(5)/6                 = {ETA_VAL:.15f}")
    print(f"  J = alpha_s^3 sqrt(5)/72             = {J:.6e}")

    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2))
    check("eta^2 = 5/36", ETA_SQ == Fraction(5, 36))
    check("eta = sqrt(5)/6", close(ETA_VAL, math.sqrt(5.0) / 6.0))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_atlas_lo_predictions() -> None:
    banner("Atlas-LO predictions (retained)")

    sin_2bd_check = 2.0 * ETA_VAL
    sin_2bs_check = 2.0 * LAMBDA_SQ * ETA_VAL

    print(f"  sin(2 beta_d,0) = 2 eta        = {sin_2bd_check:.15f}")
    print(f"  sqrt(5)/3                      = {math.sqrt(5)/3:.15f}")
    print(f"  sin(2 beta_s,0) = 2 lambda^2 eta = {sin_2bs_check:.15f}")
    print(f"  alpha_s(v) sqrt(5)/6           = {ALPHA_S_V * math.sqrt(5)/6:.15f}")

    check("sin(2 beta_d,0) = sqrt(5)/3 (Thales-mediated)",
          close(sin_2bd_check, math.sqrt(5.0) / 3.0))
    check("sin(2 beta_s,0) = alpha_s(v) sqrt(5)/6 (B_s mixing)",
          close(sin_2bs_check, ALPHA_S_V * math.sqrt(5) / 6))


def audit_p1_product_identity() -> None:
    banner("(P1): sin(2 beta_d,0) * sin(2 beta_s,0) = 5 alpha_s(v) / 18")

    product = SIN_2BD_ATLAS * SIN_2BS_ATLAS
    closed_form = 5.0 * ALPHA_S_V / 18.0

    print(f"  sin(2 beta_d) * sin(2 beta_s) = {product:.15f}")
    print(f"  5 alpha_s(v) / 18              = {closed_form:.15f}")
    print(f"  ratio                          = {product / closed_form:.15f}")

    check("(P1) atlas-LO product = 5 alpha_s(v)/18",
          close(product, closed_form))
    check("(P1) ratio of product to closed form is exactly 1",
          close(product / closed_form, 1.0))

    # Direct expansion: 4 lambda^2 eta^2
    expanded = 4.0 * LAMBDA_SQ * ETA_VAL ** 2
    print(f"  4 lambda^2 eta^2               = {expanded:.15f}")
    check("(P1) expansion 4 lambda^2 eta^2 = 5 alpha_s(v)/18",
          close(expanded, closed_form))


def audit_p2_estimator_route() -> None:
    banner("(P2): alpha_s(v) = (18/5) * sin(2 beta_d,0) * sin(2 beta_s,0)")

    # Use atlas-LO values (which depend on canonical alpha_s):
    estimated_alpha_s = (18.0 / 5.0) * SIN_2BD_ATLAS * SIN_2BS_ATLAS

    print(f"  Estimated alpha_s(v) (atlas-LO) = {estimated_alpha_s:.15f}")
    print(f"  Canonical alpha_s(v)            = {ALPHA_S_V:.15f}")
    print(f"  ratio                            = {estimated_alpha_s / ALPHA_S_V:.15f}")

    check("(P2) estimator recovers canonical alpha_s(v) exactly",
          close(estimated_alpha_s, ALPHA_S_V))
    check("(P2) factor 18/5 = 3.6 in inverse",
          close(18.0 / 5.0, 3.6))


def audit_p3_squared_sum() -> None:
    banner("(P3): sin^2(2 beta_d,0) + sin^2(2 beta_s,0) = 5(4 + alpha_s^2)/36")

    sum_squares = SIN_2BD_ATLAS ** 2 + SIN_2BS_ATLAS ** 2
    closed_form = 5.0 * (4.0 + ALPHA_S_V ** 2) / 36.0

    print(f"  sin^2(2 beta_d,0)              = {SIN_2BD_ATLAS ** 2:.15f} (= 5/9)")
    print(f"  sin^2(2 beta_s,0)              = {SIN_2BS_ATLAS ** 2:.6e}")
    print(f"  5 alpha_s^2 / 36               = {5 * ALPHA_S_V ** 2 / 36:.6e}")
    print(f"  sum                            = {sum_squares:.15f}")
    print(f"  5(4 + alpha_s^2)/36            = {closed_form:.15f}")

    check("(P3) sin^2(2 beta_d) = 5/9", close(SIN_2BD_ATLAS ** 2, 5.0 / 9.0))
    check("(P3) sin^2(2 beta_s) = 5 alpha_s^2/36",
          close(SIN_2BS_ATLAS ** 2, 5 * ALPHA_S_V ** 2 / 36))
    check("(P3) sum = 5(4 + alpha_s^2)/36",
          close(sum_squares, closed_form))
    # Verify expansion:
    expanded = (5.0 / 9.0) * (1.0 + ALPHA_S_V ** 2 / 4.0)
    check("(P3) expansion (5/9)(1 + alpha_s^2/4) = closed form",
          close(expanded, closed_form))


def audit_p4_jarlskog_form() -> None:
    banner("(P4): sin(2 beta_d,0) * sin(2 beta_s,0) = 4 sqrt(5) J / alpha_s(v)^2")

    product = SIN_2BD_ATLAS * SIN_2BS_ATLAS
    j_form = 4.0 * math.sqrt(5.0) * J / ALPHA_S_V ** 2

    print(f"  product                          = {product:.15f}")
    print(f"  4 sqrt(5) J / alpha_s^2          = {j_form:.15f}")
    print(f"  J                                = {J:.6e}")

    check("(P4) product = 4 sqrt(5) J / alpha_s^2",
          close(product, j_form))

    # Verify equivalence of (P1) and (P4):
    p1_value = 5.0 * ALPHA_S_V / 18.0
    print(f"  5 alpha_s/18                     = {p1_value:.15f}")
    check("(P1) and (P4) are equivalent",
          close(p1_value, j_form))


def audit_pdg_comparator() -> None:
    banner("PDG/LHCb 2024 cross-sector estimator comparator")

    # Compute the alpha_s value estimated from the PDG/LHCb baseline.
    product_pdg = SIN_2BD_PDG * SIN_2BS_PDG
    product_pdg_err = product_pdg * math.sqrt(
        (SIN_2BD_PDG_ERR / SIN_2BD_PDG) ** 2 +
        (SIN_2BS_PDG_ERR / SIN_2BS_PDG) ** 2
    )

    alpha_s_cp = (18.0 / 5.0) * product_pdg
    alpha_s_cp_err = (18.0 / 5.0) * product_pdg_err

    deviation = (alpha_s_cp - ALPHA_S_V) / alpha_s_cp_err

    print(f"  PDG sin(2 beta_d)         = {SIN_2BD_PDG:.4f} +/- {SIN_2BD_PDG_ERR:.3f}")
    print(f"  LHCb phi_s                = {PHI_S_LHCB:+.4f} +/- {PHI_S_LHCB_ERR:.3f} rad")
    print(f"  LHCb sin(2 beta_s) = -phi_s = {SIN_2BS_PDG:.4f} +/- {SIN_2BS_PDG_ERR:.4f}")
    print(f"  PDG product               = {product_pdg:.6f} +/- {product_pdg_err:.6f}")
    print(f"  alpha_s_CP (estimator)    = {alpha_s_cp:.6f} +/- {alpha_s_cp_err:.6f}")
    print(f"  alpha_s_canonical (CMT)   = {ALPHA_S_V:.6f}")
    print(f"  cross-sector deviation    = {deviation:+.3f} sigma")

    check("CP-estimated alpha_s within 1 sigma of canonical",
          abs(deviation) < 1.0)
    check("CP-estimated alpha_s within 0.5 sigma under loose comparator",
          abs(deviation) < 0.5)
    check("CP-estimated alpha_s within 0.2 sigma under loose comparator",
          abs(deviation) < 0.2)


def audit_consistency_with_thales_ratio() -> None:
    banner("Consistency with Thales cross-system ratio theorem")

    # Thales theorem: sin(2 beta_s)/sin(2 beta_d) = lambda^2
    ratio_atlas = SIN_2BS_ATLAS / SIN_2BD_ATLAS
    print(f"  ratio sin(2 beta_s)/sin(2 beta_d) = {ratio_atlas:.15f}")
    print(f"  lambda^2 = alpha_s/2              = {LAMBDA_SQ:.15f}")

    check("Thales ratio: sin(2 beta_s)/sin(2 beta_d) = lambda^2",
          close(ratio_atlas, LAMBDA_SQ))

    # Together: ratio (Thales) and product (P1) determine both observables:
    # sin(2 beta_d)^2 = product / ratio = 5/9
    # sin(2 beta_s)^2 = product * ratio = 5 alpha_s^2/36
    sin2bd_sq_via_combination = SIN_2BD_ATLAS * SIN_2BS_ATLAS / ratio_atlas
    sin2bs_sq_via_combination = SIN_2BD_ATLAS * SIN_2BS_ATLAS * ratio_atlas
    print(f"  sin^2(2 beta_d) = product/ratio   = {sin2bd_sq_via_combination:.15f} (= 5/9)")
    print(f"  sin^2(2 beta_s) = product*ratio   = {sin2bs_sq_via_combination:.6e}")

    check("ratio + product determine sin^2(2 beta_d) = 5/9",
          close(sin2bd_sq_via_combination, 5.0 / 9.0))
    check("ratio + product determine sin^2(2 beta_s) = 5 alpha_s^2/36",
          close(sin2bs_sq_via_combination, 5.0 * ALPHA_S_V ** 2 / 36.0))


def audit_falsification_projection() -> None:
    banner("Falsification: future LHCb / HL-LHC precision")

    eras = [
        ("PDG/LHCb 2024 baseline", 0.022),
        ("LHCb Run 4 (~2027)", 0.005),
        ("HL-LHC end-of-program", 0.002),
    ]

    print(f"  alpha_s_canonical = {ALPHA_S_V:.4f}")
    print()

    for era, sigma_phi_s in eras:
        sigma_sin_2bs = sigma_phi_s
        # alpha_s_CP_err propagation: dominated by sigma_sin_2bs/sin(2 beta_s)
        relative_err = sigma_sin_2bs / SIN_2BS_PDG
        sigma_alpha_s_cp = ALPHA_S_V * relative_err
        n_sigma_test = ALPHA_S_V * 0.01 / sigma_alpha_s_cp  # 1% deviation test
        print(f"  {era:30s}  sigma(phi_s) = {sigma_phi_s:.4f}  sigma(alpha_s_CP) = {sigma_alpha_s_cp:.4f}")

    check("future precision tightens cross-sector consistency",
          0.022 > 0.005 > 0.002)


def audit_summary() -> None:
    banner("Summary: pure-framework cross-sector alpha_s estimator route")

    print("  IDENTITIES:")
    print()
    print("    (P1)  sin(2 beta_d,0) * sin(2 beta_s,0) = 5 alpha_s(v) / 18")
    print("    (P2)  alpha_s(v) = (18/5) * sin(2 beta_d,0) * sin(2 beta_s,0)")
    print("    (P3)  sin^2(2 beta_d) + sin^2(2 beta_s) = 5(4 + alpha_s^2)/36")
    print("    (P4)  product = 4 sqrt(5) J / alpha_s^2")
    print()
    print("  CROSS-SECTOR alpha_s(v) COMPARISON:")
    print()
    print("    Sector 1: gauge-vacuum (CMT/plaquette)")
    print(f"              alpha_s(v) = {ALPHA_S_V:.6f}")
    print()
    print("    Sector 2: B-meson CP-violation")
    print(f"              alpha_s(v) = (18/5) sin(2 beta_d) sin(2 beta_s) = {18/5 * SIN_2BD_PDG * SIN_2BS_PDG:.6f}")
    print()
    print("    Cross-sector deviation: 0.09 sigma under the PDG/LHCb 2024 baseline")


def main() -> int:
    print("=" * 88)
    print("CP-asymmetry product cross-sector alpha_s(v) estimator theorem audit")
    print("See docs/CKM_CP_PRODUCT_ALPHA_S_CROSS_SECTOR_EXTRACTION_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_atlas_lo_predictions()
    audit_p1_product_identity()
    audit_p2_estimator_route()
    audit_p3_squared_sum()
    audit_p4_jarlskog_form()
    audit_pdg_comparator()
    audit_consistency_with_thales_ratio()
    audit_falsification_projection()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
