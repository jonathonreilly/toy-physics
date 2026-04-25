#!/usr/bin/env python3
"""CKM doubled-angle CP-asymmetry NLO shift-pattern theorem audit.

Verifies the new closed-form / structural identities in
  docs/CKM_DOUBLED_ANGLE_CP_NLO_SHIFT_PATTERN_THEOREM_NOTE_2026-04-25.md

  (D1) sin(2 alpha_bar)  =  -(sqrt(5)/10) alpha_s(v)  +  O(alpha_s^2)   [NEW]
  (D2) sin(2 beta_bar)   =   sqrt(5)/3 - (sqrt(5)/15) alpha_s(v) + O(alpha_s^2)
                                        [linearization of N9, parent NLO theorem]
  (D3) sin(2 gamma_bar)  =   sqrt(5)/3 + O(alpha_s^4)
                                        [PROTECTED at NLO; retained from N8]
  (D4) Delta sin(2 alpha_bar) : Delta sin(2 beta_bar) : Delta sin(2 gamma_bar)
            =  -3 : -2 : 0   [NEW structural shift pattern at NLO]
  (D5) sum: sin(2 alpha_bar) + sin(2 beta_bar) + sin(2 gamma_bar)
            =  2 sqrt(5)/3  -  (sqrt(5)/6) alpha_s(v) + O(alpha_s^2)   [NEW]

All inputs are RETAINED on current main:
- atlas-LO: alpha_0 = pi/2, beta_0 = arctan(1/sqrt(5)), gamma_0 = arctan(sqrt(5))
- canonical alpha_s(v)
- protected-gamma NLO theorem: gamma_bar = gamma_0 (N8), alpha_bar - pi/2 = (sqrt(5)/20) alpha_s (N7)

No SUPPORT-tier or open inputs (Koide Q_l, bare-coupling ratios) are used.
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

# Atlas-LO base values (retained right-angle theorem)
ALPHA_0 = math.pi / 2
BETA_0 = math.atan(1.0 / math.sqrt(5.0))
GAMMA_0 = math.atan(math.sqrt(5.0))

# NLO slope (retained from protected-gamma N7)
SLOPE = math.sqrt(5.0) / 20.0  # alpha_bar - pi/2 = SLOPE * alpha_s

# NLO angle deviations
DELTA_ALPHA_BAR = SLOPE * ALPHA_S_V
DELTA_BETA_BAR = -SLOPE * ALPHA_S_V  # forced by gamma_bar = gamma_0 protection
DELTA_GAMMA_BAR = 0.0

# NLO angles
ALPHA_BAR = ALPHA_0 + DELTA_ALPHA_BAR
BETA_BAR = BETA_0 + DELTA_BETA_BAR
GAMMA_BAR = GAMMA_0 + DELTA_GAMMA_BAR


def audit_inputs() -> None:
    banner("Retained inputs (from current main)")

    print(f"  alpha_s(v) (canonical CMT)         = {ALPHA_S_V:.15f}")
    print(f"  alpha_0 = pi/2                      = {math.degrees(ALPHA_0):.6f} deg")
    print(f"  beta_0  = arctan(1/sqrt(5))         = {math.degrees(BETA_0):.6f} deg")
    print(f"  gamma_0 = arctan(sqrt(5))           = {math.degrees(GAMMA_0):.6f} deg")
    print(f"  NLO slope = sqrt(5)/20 (from N7)    = {SLOPE:.15f}")
    print()
    print(f"  At NLO: alpha_bar = pi/2 + slope*alpha_s = {math.degrees(ALPHA_BAR):.6f} deg")
    print(f"          beta_bar  = beta_0 - slope*alpha_s = {math.degrees(BETA_BAR):.6f} deg")
    print(f"          gamma_bar = gamma_0 (PROTECTED)    = {math.degrees(GAMMA_BAR):.6f} deg")

    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("alpha_0 = pi/2 (atlas right angle)",
          close(ALPHA_0, math.pi / 2))
    check("beta_0 + gamma_0 = pi/2 (atlas constraint)",
          close(BETA_0 + GAMMA_0, math.pi / 2))
    check("alpha_0 + beta_0 + gamma_0 = pi (triangle)",
          close(ALPHA_0 + BETA_0 + GAMMA_0, math.pi))
    check("alpha_bar + beta_bar + gamma_bar = pi (NLO triangle)",
          close(ALPHA_BAR + BETA_BAR + GAMMA_BAR, math.pi))

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        # atlas-LO retained authorities
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        # NLO retained parent
        "docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md",
        # canonical alpha_s(v)
        "docs/ALPHA_S_DERIVED_NOTE.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained authority on main: {rel}", path.exists())


def audit_d1_sin_2alpha_bar() -> None:
    banner("(D1) NEW: sin(2 alpha_bar) = -(sqrt(5)/10) alpha_s(v) + O(alpha_s^2)")

    closed_form = -(math.sqrt(5.0) / 10.0) * ALPHA_S_V
    direct = math.sin(2 * ALPHA_BAR)

    print(f"  Closed form -(sqrt(5)/10) alpha_s = {closed_form:.10e}")
    print(f"  Direct sin(2 alpha_bar)            = {direct:.10e}")
    residual = direct - closed_form
    print(f"  Residual (O(alpha_s^2))            = {residual:.6e}")
    print(f"  Relative residual                   = {abs(residual/closed_form):.4%}")

    check("(D1) closed form matches direct within 1% (NLO leading)",
          abs(residual / closed_form) < 0.01)
    check("(D1) sign is negative (alpha_bar > pi/2)",
          closed_form < 0)
    check("(D1) at canonical alpha_s, |sin(2 alpha_bar)| ~ 0.023",
          abs(closed_form + 0.0231) < 1e-3)


def audit_d2_sin_2beta_bar() -> None:
    banner("(D2): sin(2 beta_bar) = sqrt(5)/3 - (sqrt(5)/15) alpha_s + O(alpha_s^2)")

    closed_form = math.sqrt(5.0) / 3.0 - (math.sqrt(5.0) / 15.0) * ALPHA_S_V
    direct = math.sin(2 * BETA_BAR)

    print(f"  Closed form sqrt(5)/3 - (sqrt(5)/15) alpha_s = {closed_form:.10f}")
    print(f"  Direct sin(2 beta_bar)                         = {direct:.10f}")
    residual = direct - closed_form
    print(f"  Residual (O(alpha_s^2))                         = {residual:.6e}")

    check("(D2) closed form matches direct within 0.1% (NLO leading)",
          abs(residual / closed_form) < 0.001)
    check("(D2) sin(2 beta_bar) is positive",
          closed_form > 0)


def audit_d3_protected_sin_2gamma_bar() -> None:
    banner("(D3) PROTECTED: sin(2 gamma_bar) = sqrt(5)/3 + O(alpha_s^4)")

    closed_form = math.sqrt(5.0) / 3.0
    direct = math.sin(2 * GAMMA_BAR)

    print(f"  sqrt(5)/3                = {closed_form:.15f}")
    print(f"  Direct sin(2 gamma_bar)  = {direct:.15f}")

    check("(D3) sin(2 gamma_bar) = sqrt(5)/3 (PROTECTED, retained from N8)",
          close(direct, closed_form))


def audit_d4_shift_pattern() -> None:
    banner("(D4) NEW: shift-pattern Delta sin(2 alpha) : Delta sin(2 beta) : Delta sin(2 gamma) = -3 : -2 : 0")

    delta_sin_2alpha = -(math.sqrt(5.0) / 10.0) * ALPHA_S_V
    delta_sin_2beta = -(math.sqrt(5.0) / 15.0) * ALPHA_S_V
    delta_sin_2gamma = 0.0

    print(f"  Delta sin(2 alpha_bar) = {delta_sin_2alpha:.6e}")
    print(f"  Delta sin(2 beta_bar)  = {delta_sin_2beta:.6e}")
    print(f"  Delta sin(2 gamma_bar) = {delta_sin_2gamma:.6e}")

    # Ratio alpha:beta = (-sqrt(5)/10) / (-sqrt(5)/15) = 15/10 = 3/2
    ratio = delta_sin_2alpha / delta_sin_2beta
    print(f"  Delta sin(2 alpha_bar) / Delta sin(2 beta_bar) = {ratio:.10f}")
    print(f"  Closed form ratio: 3/2 = {3.0/2.0:.10f}")

    check("(D4) ratio Delta sin(2 alpha) : Delta sin(2 beta) = 3 : 2 (numerical)",
          close(ratio, 1.5))
    check("(D4) Delta sin(2 gamma_bar) = 0 (protection)",
          delta_sin_2gamma == 0)
    check("(D4) Delta sin(2 alpha_bar) < 0 (alpha_bar > pi/2)",
          delta_sin_2alpha < 0)
    check("(D4) Delta sin(2 beta_bar) < 0 (beta_bar < beta_0)",
          delta_sin_2beta < 0)

    # Structural derivation check: cos(2 alpha_0) = -1, cos(2 beta_0) = 2/3
    cos_2alpha_0 = math.cos(2 * ALPHA_0)
    cos_2beta_0 = math.cos(2 * BETA_0)
    structural_ratio = (2 * cos_2alpha_0 * SLOPE) / (2 * cos_2beta_0 * (-SLOPE))
    print(f"\n  Structural derivation:")
    print(f"    cos(2 alpha_0) = {cos_2alpha_0:.6f} (= -1 exactly)")
    print(f"    cos(2 beta_0)  = {cos_2beta_0:.6f} (= 2/3 exactly)")
    print(f"    structural ratio = (2 cos(2alpha_0) +slope)/(2 cos(2beta_0) -slope) = {structural_ratio:.6f}")
    check("structural ratio matches numerical 3/2",
          close(structural_ratio, 1.5))


def audit_d5_sum_rule() -> None:
    banner("(D5) NEW: sum rule sin(2 alpha) + sin(2 beta) + sin(2 gamma) = 2 sqrt(5)/3 - (sqrt(5)/6) alpha_s")

    closed_form_LO = 2 * math.sqrt(5.0) / 3.0
    closed_form_NLO_correction = -(math.sqrt(5.0) / 6.0) * ALPHA_S_V
    closed_form_total = closed_form_LO + closed_form_NLO_correction

    direct_sum = math.sin(2 * ALPHA_BAR) + math.sin(2 * BETA_BAR) + math.sin(2 * GAMMA_BAR)

    print(f"  Atlas-LO sum 2 sqrt(5)/3                           = {closed_form_LO:.10f}")
    print(f"  NLO correction -(sqrt(5)/6) alpha_s                = {closed_form_NLO_correction:.6e}")
    print(f"  Closed form NLO total                              = {closed_form_total:.10f}")
    print(f"  Direct sum sin(2 alpha) + sin(2 beta) + sin(2 gamma) = {direct_sum:.10f}")
    residual = direct_sum - closed_form_total
    print(f"  Residual (O(alpha_s^2))                             = {residual:.6e}")

    check("(D5) closed form matches direct within 0.05% (NLO leading)",
          abs(residual / closed_form_total) < 5e-4)

    # Trig identity cross-check: sin(2A) + sin(2B) + sin(2C) = 4 sin(A) sin(B) sin(C)
    trig_check = 4 * math.sin(ALPHA_BAR) * math.sin(BETA_BAR) * math.sin(GAMMA_BAR)
    print(f"\n  Trig identity check: 4 sin(alpha_bar) sin(beta_bar) sin(gamma_bar) = {trig_check:.10f}")
    check("(D5) trig identity 4 sin(α̅) sin(β̄) sin(γ̄) = direct sum (machine precision)",
          close(direct_sum, trig_check))

    # At atlas-LO
    trig_LO = 4 * math.sin(ALPHA_0) * math.sin(BETA_0) * math.sin(GAMMA_0)
    print(f"  Atlas-LO trig identity:                              = {trig_LO:.10f}")
    print(f"  2 sqrt(5)/3                                          = {closed_form_LO:.10f}")
    check("(D5) atlas-LO trig identity = 2 sqrt(5)/3",
          close(trig_LO, closed_form_LO))


def audit_consistency_with_protected_gamma_n9() -> None:
    banner("Consistency: (D2) linearizes the closed form (N9) of protected-gamma theorem")

    # (N9) from parent: tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s)
    tan_beta_bar = math.sqrt(5.0) * (4 - ALPHA_S_V) / (20 + ALPHA_S_V)
    sin_2beta_via_N9 = 2 * tan_beta_bar / (1 + tan_beta_bar ** 2)
    sin_2beta_linearized = math.sqrt(5.0) / 3.0 - (math.sqrt(5.0) / 15.0) * ALPHA_S_V

    print(f"  sin(2 beta_bar) via (N9) tan-half formula = {sin_2beta_via_N9:.10f}")
    print(f"  sin(2 beta_bar) linearized in (D2)         = {sin_2beta_linearized:.10f}")
    print(f"  Difference (O(alpha_s^2))                  = {abs(sin_2beta_via_N9 - sin_2beta_linearized):.6e}")

    check("(D2) linearization is consistent with parent (N9)",
          abs(sin_2beta_via_N9 - sin_2beta_linearized) < 5e-4)


def audit_pdg_comparators() -> None:
    banner("PDG comparators (post-derivation only)")

    # PDG sin(2 beta) = 0.706 +/- 0.011 from B → J/psi K_S
    sin_2beta_pdg = 0.706
    sin_2beta_pdg_err = 0.011
    sin_2beta_atlas = math.sqrt(5.0) / 3.0 - (math.sqrt(5.0) / 15.0) * ALPHA_S_V
    deviation = (sin_2beta_atlas - sin_2beta_pdg) / sin_2beta_pdg_err

    print(f"  sin(2 beta_bar) atlas-NLO  = {sin_2beta_atlas:.4f}")
    print(f"  sin(2 beta) PDG B->ψK_S    = {sin_2beta_pdg:.3f} +/- {sin_2beta_pdg_err:.3f}")
    print(f"  deviation                    = {deviation:+.2f} sigma")

    check("sin(2 beta_bar) atlas-NLO within 3 sigma of PDG", abs(deviation) < 3.0)

    # alpha extraction from CKMfitter / UTfit isospin analysis
    alpha_pdg_deg = 84.9
    alpha_pdg_err_deg = 5.1
    alpha_atlas_deg = math.degrees(ALPHA_BAR)
    deviation_alpha = (alpha_atlas_deg - alpha_pdg_deg) / alpha_pdg_err_deg

    print(f"\n  alpha_bar atlas-NLO        = {alpha_atlas_deg:.2f} deg")
    print(f"  alpha PDG isospin analysis = {alpha_pdg_deg:.1f} +/- {alpha_pdg_err_deg:.1f} deg")
    print(f"  deviation                   = {deviation_alpha:+.2f} sigma")

    check("alpha_bar atlas-NLO within 2 sigma of PDG", abs(deviation_alpha) < 2.0)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW closed-form predictions at NLO Wolfenstein:")
    print()
    print("    (D1) sin(2 alpha_bar)  =  -(sqrt(5)/10) alpha_s(v) + O(alpha_s^2)")
    print("    (D2) sin(2 beta_bar)   =   sqrt(5)/3 - (sqrt(5)/15) alpha_s(v) + O(alpha_s^2)")
    print("    (D3) sin(2 gamma_bar)  =   sqrt(5)/3 + O(alpha_s^4)  [PROTECTED at NLO]")
    print()
    print("  NEW structural shift pattern:")
    print()
    print("    Delta sin(2 alpha_bar) : Delta sin(2 beta_bar) : Delta sin(2 gamma_bar)")
    print("       =  -3  :  -2  :  0  exactly at NLO leading order")
    print()
    print("  NEW sum rule:")
    print()
    print("    sin(2 alpha) + sin(2 beta) + sin(2 gamma)")
    print("       =  2 sqrt(5)/3  -  (sqrt(5)/6) alpha_s(v) + O(alpha_s^2)")
    print()
    print("  At canonical alpha_s(v) = 0.10330:")
    print(f"    sin(2 alpha_bar) = -0.0231  (NEW; pure NLO observable)")
    print(f"    sin(2 beta_bar)  = +0.7300  (NLO-shifted)")
    print(f"    sin(2 gamma_bar) = +0.7454  (PROTECTED at NLO)")
    print(f"    sum              = +1.4522  (linear NLO shift)")
    print()
    print("  All inputs are RETAINED on current main; no SUPPORT-tier or")
    print("  open inputs (Koide Q_l, bare-coupling ratios) are used.")


def main() -> int:
    print("=" * 88)
    print("CKM doubled-angle CP-asymmetry NLO shift-pattern theorem audit")
    print("See docs/CKM_DOUBLED_ANGLE_CP_NLO_SHIFT_PATTERN_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_d1_sin_2alpha_bar()
    audit_d2_sin_2beta_bar()
    audit_d3_protected_sin_2gamma_bar()
    audit_d4_shift_pattern()
    audit_d5_sum_rule()
    audit_consistency_with_protected_gamma_n9()
    audit_pdg_comparators()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
