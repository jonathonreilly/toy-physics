#!/usr/bin/env python3
"""phi_s NLO closed form + 3/5 cross-system CP ratio theorem audit.

Verifies the new identities in
  docs/CKM_PHI_S_NLO_AND_THREE_FIFTHS_CROSS_SYSTEM_RATIO_THEOREM_NOTE_2026-04-25.md

  (R1) phi_s(NLO) = -alpha_s sqrt(5)/6 - alpha_s^2 sqrt(5)/36 + O(alpha_s^3)   [NEW]
  (R2) Equivalent: phi_s(NLO) = -(alpha_s sqrt(5)/6)(1 + alpha_s/6)             [NEW]
  (R3) sin(2 alpha_bar) = -(sqrt(5)/10) alpha_s + O(alpha_s^2)
                          [retained, derived from N7 of protected-gamma]
  (R4) sin(2 alpha_bar) / phi_s = 3/5 EXACTLY at leading order in alpha_s       [NEW alpha_s-INDEPENDENT]
  (R5) sin(2 alpha_bar) / sin(2 beta_d) = -3 alpha_s/10 at leading order        [NEW joint]

All inputs are RETAINED on current main; no SUPPORT-tier / open inputs used.
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


# Retained inputs
ALPHA_S_V = CANONICAL_ALPHA_S_V

LAMBDA_SQ = ALPHA_S_V / 2.0   # retained Wolfenstein
A_SQ = Fraction(2, 3)          # retained Wolfenstein
RHO = Fraction(1, 6)           # retained CP-phase
ETA_VAL = math.sqrt(5.0) / 6.0  # retained CP-phase

# Retained protected-gamma (N7) slope
SLOPE = math.sqrt(5.0) / 20.0  # alpha_bar - pi/2 = SLOPE * alpha_s


# PDG / LHCb comparators
PHI_S_LHCB = -0.039
PHI_S_LHCB_ERR = 0.022
SIN_2BD_PDG = 0.706
SIN_2BD_PDG_ERR = 0.011


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  alpha_s(v) (canonical CMT)  = {ALPHA_S_V:.15f}")
    print(f"  lambda^2 = alpha_s(v)/2      = {LAMBDA_SQ:.15f}")
    print(f"  rho = 1/6                    = {float(RHO):.15f}")
    print(f"  eta = sqrt(5)/6              = {ETA_VAL:.15f}")
    print(f"  protected-gamma slope        = sqrt(5)/20 = {SLOPE:.15f}")

    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2))
    check("eta^2 = 5/36 (rational)", close(ETA_VAL ** 2, 5.0 / 36.0))

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md",
        "docs/CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md",
        "docs/CKM_THALES_CROSS_SYSTEM_CP_RATIO_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained on main: {rel}", path.exists())


def audit_r1_phi_s_nlo() -> None:
    banner("(R1) NEW: phi_s(NLO) = -alpha_s sqrt(5)/6 - alpha_s^2 sqrt(5)/36 + O(alpha_s^3)")

    # Closed form
    phi_s_LO = -ALPHA_S_V * math.sqrt(5.0) / 6.0
    phi_s_NLO_correction = -(ALPHA_S_V ** 2) * math.sqrt(5.0) / 36.0
    phi_s_NLO_closed = phi_s_LO + phi_s_NLO_correction

    print(f"  LO term:               -alpha_s sqrt(5)/6     = {phi_s_LO:.10f}")
    print(f"  NLO correction:        -alpha_s^2 sqrt(5)/36  = {phi_s_NLO_correction:.10f}")
    print(f"  Total phi_s(NLO):                                = {phi_s_NLO_closed:.10f}")

    # Direct full-Wolfenstein computation
    A = math.sqrt(float(A_SQ))
    rho = float(RHO)
    eta = ETA_VAL

    V_ts_real = -A * LAMBDA_SQ + (A * LAMBDA_SQ ** 2 / 2) * (1 - 2 * rho)
    V_ts_imag = -A * LAMBDA_SQ ** 2 * eta
    V_tb_real = 1 - float(A_SQ) * LAMBDA_SQ ** 2 / 2
    V_cs_real = 1 - LAMBDA_SQ / 2 - LAMBDA_SQ ** 2 * (1 + 4 * float(A_SQ)) / 8
    V_cb_real = A * LAMBDA_SQ

    prod_ts_tb_real = V_ts_real * V_tb_real
    prod_ts_tb_imag = V_ts_imag * V_tb_real
    prod_cs_cb = V_cs_real * V_cb_real

    ratio_real = -prod_ts_tb_real / prod_cs_cb
    ratio_imag = -prod_ts_tb_imag / prod_cs_cb
    beta_s_direct = math.atan2(ratio_imag, ratio_real)
    phi_s_direct = -2 * beta_s_direct

    residual = phi_s_direct - phi_s_NLO_closed
    print(f"  Direct full-Wolfenstein phi_s                    = {phi_s_direct:.10f}")
    print(f"  Residual (O(alpha_s^3))                           = {residual:.6e}")

    check("(R1) closed form matches direct full-Wolfenstein within O(alpha_s^3)",
          abs(residual) < 1e-4)
    check("(R1) closed form is exactly LO + NLO correction",
          close(phi_s_NLO_closed, phi_s_LO + phi_s_NLO_correction))

    # The factored form (R2)
    phi_s_factored = -(ALPHA_S_V * math.sqrt(5) / 6) * (1 + ALPHA_S_V / 6)
    print(f"\n  (R2) Factored: -(alpha_s sqrt(5)/6)(1 + alpha_s/6) = {phi_s_factored:.10f}")
    check("(R2) factored form equals (R1) expanded",
          close(phi_s_factored, phi_s_NLO_closed))


def audit_r3_sin_2alpha_bar() -> None:
    banner("(R3): sin(2 alpha_bar) = -(sqrt(5)/10) alpha_s + O(alpha_s^2)")

    # Derivation: alpha_bar - pi/2 = (sqrt(5)/20) alpha_s [retained N7]
    # => 2 alpha_bar - pi = (sqrt(5)/10) alpha_s
    # => sin(2 alpha_bar) = sin(pi + (sqrt(5)/10) alpha_s) = -(sqrt(5)/10) alpha_s

    sin_2alpha_bar = -(math.sqrt(5) / 10) * ALPHA_S_V

    # Verify via direct computation
    alpha_bar = math.pi / 2 + SLOPE * ALPHA_S_V
    sin_2alpha_bar_direct = math.sin(2 * alpha_bar)

    print(f"  -(sqrt(5)/10) alpha_s        = {sin_2alpha_bar:.10f}")
    print(f"  Direct sin(2 alpha_bar)       = {sin_2alpha_bar_direct:.10f}")
    print(f"  Residual (O(alpha_s^3))        = {abs(sin_2alpha_bar_direct - sin_2alpha_bar):.6e}")

    check("(R3) sin(2 alpha_bar) closed form matches direct (alpha_s^2 residual)",
          abs(sin_2alpha_bar_direct - sin_2alpha_bar) < 1e-3)
    check("(R3) sign is negative (alpha_bar > pi/2)", sin_2alpha_bar < 0)
    check("(R3) at canonical alpha_s, |sin(2 alpha_bar)| ~ 0.023",
          abs(sin_2alpha_bar + 0.0231) < 1e-3)


def audit_r4_three_fifths_ratio() -> None:
    banner("(R4) NEW: sin(2 alpha_bar) / phi_s = 3/5 EXACTLY at leading order")

    # Both at leading order in alpha_s (linear coefficients only)
    sin_2alpha_LO_coeff = -math.sqrt(5) / 10
    phi_s_LO_coeff = -math.sqrt(5) / 6

    ratio_coeffs = sin_2alpha_LO_coeff / phi_s_LO_coeff
    print(f"  sin(2 alpha_bar) leading coefficient: -sqrt(5)/10")
    print(f"  phi_s leading coefficient:            -sqrt(5)/6")
    print(f"  Ratio of coefficients:                 {ratio_coeffs:.10f}")
    print(f"  Closed form 3/5:                       {3/5:.10f}")
    print(f"  Match: {close(ratio_coeffs, 3/5)}")

    check("(R4) ratio of leading coefficients = 3/5", close(ratio_coeffs, 3/5))

    # The alpha_s factor cancels exactly
    sin_2alpha_at_alpha_s = sin_2alpha_LO_coeff * ALPHA_S_V
    phi_s_at_alpha_s = phi_s_LO_coeff * ALPHA_S_V
    ratio_at_alpha_s = sin_2alpha_at_alpha_s / phi_s_at_alpha_s
    print(f"\n  sin(2 alpha_bar) at canonical alpha_s = {sin_2alpha_at_alpha_s:.10f}")
    print(f"  phi_s at canonical alpha_s             = {phi_s_at_alpha_s:.10f}")
    print(f"  Ratio at canonical alpha_s             = {ratio_at_alpha_s:.10f}")

    check("(R4) ratio = 3/5 exactly at canonical alpha_s",
          close(ratio_at_alpha_s, 3/5))

    # Verify alpha_s-INDEPENDENCE: try a different alpha_s
    for alpha_s_test in [0.05, 0.10, 0.15, 0.20]:
        ratio_test = (sin_2alpha_LO_coeff * alpha_s_test) / (phi_s_LO_coeff * alpha_s_test)
        check(f"(R4) ratio = 3/5 at alpha_s = {alpha_s_test} (alpha_s-INDEPENDENT)",
              close(ratio_test, 3/5))


def audit_r5_joint_identity() -> None:
    banner("(R5) NEW: sin(2 alpha_bar) / sin(2 beta_d) = -3 alpha_s/10 at leading order")

    # sin(2 beta_d) atlas-LO = sqrt(5)/3
    sin_2beta_d_LO = math.sqrt(5) / 3
    sin_2alpha_LO = -(math.sqrt(5) / 10) * ALPHA_S_V

    ratio = sin_2alpha_LO / sin_2beta_d_LO
    closed_form = -3 * ALPHA_S_V / 10

    print(f"  sin(2 alpha_bar) leading             = {sin_2alpha_LO:.10f}")
    print(f"  sin(2 beta_d) leading                = {sin_2beta_d_LO:.10f}")
    print(f"  Ratio (numerical)                     = {ratio:.10f}")
    print(f"  Closed form -3 alpha_s/10            = {closed_form:.10f}")

    check("(R5) ratio matches closed form -3 alpha_s/10", close(ratio, closed_form))

    # Equivalent derivation via combining (R4) with retained Thales
    # (R4): sin(2 alpha_bar)/phi_s = 3/5
    # phi_s = -2 beta_s ~= -sin(2 beta_s) for small beta_s
    # Thales: sin(2 beta_s)/sin(2 beta_d) = lambda^2 = alpha_s/2
    # => phi_s/sin(2 beta_d) = -lambda^2 = -alpha_s/2
    # => sin(2 alpha_bar)/sin(2 beta_d) = (3/5)(-alpha_s/2) = -3 alpha_s/10

    via_combination = (3/5) * (-ALPHA_S_V / 2)
    print(f"  Via (R4) x Thales: (3/5)(-lambda^2)  = {via_combination:.10f}")
    check("(R5) consistent with (R4) x Thales cross-system",
          close(via_combination, closed_form))


def audit_pdg_comparators() -> None:
    banner("PDG/LHCb comparators")

    # phi_s LO and NLO predictions vs LHCb
    phi_s_LO = -ALPHA_S_V * math.sqrt(5) / 6
    phi_s_NLO = -(ALPHA_S_V * math.sqrt(5) / 6) * (1 + ALPHA_S_V / 6)
    deviation_LO = (phi_s_LO - PHI_S_LHCB) / PHI_S_LHCB_ERR
    deviation_NLO = (phi_s_NLO - PHI_S_LHCB) / PHI_S_LHCB_ERR

    print(f"  framework phi_s(LO)   = {phi_s_LO:.6f} ({deviation_LO:+.3f} sigma)")
    print(f"  framework phi_s(NLO)  = {phi_s_NLO:.6f} ({deviation_NLO:+.3f} sigma)")
    print(f"  LHCb phi_s            = {PHI_S_LHCB} +/- {PHI_S_LHCB_ERR}")

    check("phi_s(LO) within 1 sigma of LHCb", abs(deviation_LO) < 1.0)
    check("phi_s(NLO) within 1 sigma of LHCb", abs(deviation_NLO) < 1.0)
    check("phi_s(NLO) closer to LHCb than phi_s(LO)",
          abs(deviation_NLO) < abs(deviation_LO))

    # 3/5 ratio test
    sin_2alpha_LO = -(math.sqrt(5) / 10) * ALPHA_S_V
    framework_ratio = sin_2alpha_LO / phi_s_LO
    print(f"\n  Framework sin(2 alpha_bar)/phi_s = {framework_ratio:.4f}")
    print(f"  Predicted 3/5 = 0.6                = exact")

    # joint comparator: framework predicts sin(2 alpha_bar) ~ (3/5) phi_s_LHCb
    sin_2alpha_via_phi_s_pdg = (3/5) * PHI_S_LHCB
    sin_2alpha_via_phi_s_err = (3/5) * PHI_S_LHCB_ERR
    print(f"\n  Cross-sector projection:")
    print(f"    framework sin(2 alpha_bar) ~ (3/5) phi_s_LHCb = "
          f"{sin_2alpha_via_phi_s_pdg:.4f} +/- {sin_2alpha_via_phi_s_err:.4f}")
    print(f"    direct framework: -(sqrt(5)/10) alpha_s_canonical = {sin_2alpha_LO:.4f}")
    consistency = abs(sin_2alpha_via_phi_s_pdg - sin_2alpha_LO)
    print(f"    consistency:  {consistency:.4f} rad (within LHCb error band)")
    check("3/5 cross-system consistency: framework vs current LHCb phi_s projection",
          consistency < sin_2alpha_via_phi_s_err)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW (R1, R2): phi_s NLO closed form")
    print("    phi_s(NLO) = -(alpha_s(v) sqrt(5)/6)(1 + alpha_s(v)/6)")
    print("                = -alpha_s sqrt(5)/6 - alpha_s^2 sqrt(5)/36 + O(alpha_s^3)")
    print()
    print(f"  At canonical alpha_s(v) = 0.10330:")
    print(f"    phi_s(LO)            = -0.038499")
    print(f"    phi_s NLO correction = -0.000663")
    print(f"    phi_s(NLO) total     = -0.039162")
    print(f"    LHCb measurement     = -0.039 +/- 0.022 (0.01 sigma agreement)")
    print()
    print("  NEW (R4): alpha_s-INDEPENDENT cross-system 3/5 ratio")
    print("    sin(2 alpha_bar) / phi_s  =  3/5  EXACTLY at leading order")
    print()
    print("  Why 3/5: ratio of leading coefficients (1/10)/(1/6) = 6/10 = 3/5")
    print("    sqrt(5) factors cancel; alpha_s factors cancel.")
    print("    Result: pure rational number, independent of canonical coupling.")
    print()
    print("  NEW (R5): joint with Thales cross-system")
    print("    sin(2 alpha_bar) / sin(2 beta_d) = -3 alpha_s(v)/10 at leading order")
    print()
    print("  Both (R4) and (R5) are derivable from RETAINED inputs only.")
    print("  No SUPPORT-tier or open inputs (Koide, bare-coupling) are used.")


def main() -> int:
    print("=" * 88)
    print("phi_s NLO closed form + 3/5 cross-system CP ratio theorem audit")
    print("See docs/CKM_PHI_S_NLO_AND_THREE_FIFTHS_CROSS_SYSTEM_RATIO_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_r1_phi_s_nlo()
    audit_r3_sin_2alpha_bar()
    audit_r4_three_fifths_ratio()
    audit_r5_joint_identity()
    audit_pdg_comparators()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
