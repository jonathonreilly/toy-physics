#!/usr/bin/env python3
"""CKM NLO barred-triangle and protected-gamma theorem audit.

Verifies the structural identities and the new NLO closed-form predictions in
  docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md

  (N1)  rho_bar = (4 - alpha_s)/24
  (N2)  eta_bar = sqrt(5)(4 - alpha_s)/24
  (N3)  rho_bar^2 + eta_bar^2 = (4 - alpha_s)^2/96
  (N4)  tan(gamma_bar) = sqrt(5) = tan(gamma_0)            [PROTECTED]
  (N5)  tan(beta_bar)  = sqrt(5)(4 - alpha_s)/(20 + alpha_s)
  (N6)  alpha_bar      = pi - gamma_0 - beta_bar
  (N7)  alpha_bar - pi/2 = (sqrt(5)/20) alpha_s + O(alpha_s^2)
  (N8)  sin(2 gamma_bar) = sqrt(5)/3                       [PROTECTED]
        cos(2 gamma_bar) = -2/3                            [PROTECTED]
  (N9)  sin/cos(2 beta_bar) closed forms in alpha_s

The protected-gamma identity gamma_bar = gamma_0 = arctan(sqrt(5)) is the
structural invariant of the NLO barred-apex map. Numerical comparator readouts
land within 2.2 sigma of the listed PDG bands without any free parameter;
gamma_bar matches the listed comparator at 0.13 sigma.
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


# Cited inputs.
ALPHA_S_V = CANONICAL_ALPHA_S_V
LAMBDA_SQ = ALPHA_S_V / 2.0
RHO = Fraction(1, 6)
ETA_VAL = math.sqrt(5.0) / 6.0
GAMMA_0 = math.atan(math.sqrt(5.0))
BETA_0 = math.atan(1.0 / math.sqrt(5.0))


# Post-derivation comparators.
GAMMA_PDG_DEG = 65.4
GAMMA_PDG_ERR_DEG = 3.8
BETA_PDG_DEG = 22.2
BETA_PDG_ERR_DEG = 0.7
ALPHA_PDG_DEG = 85.2
ALPHA_PDG_ERR_DEG = 4.8
SIN_2BETA_PDG = 0.706
SIN_2BETA_PDG_ERR = 0.011


def audit_inputs() -> None:
    banner("Cited inputs")

    print(f"  alpha_s(v)       = {ALPHA_S_V:.15f}")
    print(f"  lambda^2         = {LAMBDA_SQ:.15f}")
    print(f"  rho              = {RHO}  (= {float(RHO):.15f})")
    print(f"  eta              = sqrt(5)/6 (= {ETA_VAL:.15f})")
    print(f"  gamma_0          = arctan(sqrt(5)) = {math.degrees(GAMMA_0):.6f} deg")
    print(f"  beta_0           = arctan(1/sqrt(5)) = {math.degrees(BETA_0):.6f} deg")

    check("alpha_s(v) positive", ALPHA_S_V > 0)
    check("alpha_s(v) ~ 0.103 (canonical)",
          abs(ALPHA_S_V - 0.10330381612227) < 1e-13)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2))
    check("rho = 1/6", RHO == Fraction(1, 6))
    check("eta^2 = 5/36", close(ETA_VAL ** 2, 5 / 36))
    check("gamma_0 + beta_0 = pi/2 (atlas right angle)",
          close(GAMMA_0 + BETA_0, math.pi / 2))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_n1_n2_apex() -> None:
    banner("(N1), (N2): closed forms for rho_bar, eta_bar")

    nlo_factor = 1.0 - ALPHA_S_V / 4.0
    rho_bar_direct = float(RHO) * nlo_factor
    eta_bar_direct = ETA_VAL * nlo_factor

    rho_bar_closed = (4.0 - ALPHA_S_V) / 24.0
    eta_bar_closed = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / 24.0

    print(f"  (1 - alpha_s/4)         = {nlo_factor:.12f}")
    print(f"  rho_bar (direct)        = {rho_bar_direct:.12f}")
    print(f"  rho_bar = (4-alpha_s)/24 = {rho_bar_closed:.12f}")
    print(f"  eta_bar (direct)        = {eta_bar_direct:.12f}")
    print(f"  eta_bar = sqrt(5)(4-a)/24 = {eta_bar_closed:.12f}")

    check("rho_bar closed form matches direct computation",
          close(rho_bar_direct, rho_bar_closed))
    check("eta_bar closed form matches direct computation",
          close(eta_bar_direct, eta_bar_closed))
    check("rho_bar > 0 (apex inside upper half plane)", rho_bar_closed > 0)
    check("eta_bar > 0 (CP-violating apex)", eta_bar_closed > 0)


def audit_n3_radius() -> None:
    banner("(N3): rho_bar^2 + eta_bar^2 = (4 - alpha_s)^2 / 96")

    rho_bar = (4.0 - ALPHA_S_V) / 24.0
    eta_bar = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / 24.0
    radius_sq = rho_bar ** 2 + eta_bar ** 2
    closed = (4.0 - ALPHA_S_V) ** 2 / 96.0

    print(f"  rho_bar^2 + eta_bar^2     = {radius_sq:.15f}")
    print(f"  (4 - alpha_s)^2 / 96      = {closed:.15f}")

    check("(N3) holds at canonical alpha_s", close(radius_sq, closed))
    check("NLO radius < atlas-leading 1/6",
          radius_sq < 1.0 / 6.0,
          f"NLO {radius_sq:.6f} < LO {1/6:.6f}")


def audit_n4_protected_gamma() -> None:
    banner("(N4) PROTECTED INVARIANT: gamma_bar = gamma_0 = arctan(sqrt(5))")

    rho_bar = (4.0 - ALPHA_S_V) / 24.0
    eta_bar = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / 24.0
    tan_gamma_bar = eta_bar / rho_bar
    gamma_bar = math.atan(tan_gamma_bar)

    print(f"  tan(gamma_bar) = eta_bar/rho_bar = {tan_gamma_bar:.15f}")
    print(f"  sqrt(5)                          = {math.sqrt(5):.15f}")
    print(f"  gamma_bar                        = {math.degrees(gamma_bar):.10f} deg")
    print(f"  gamma_0                          = {math.degrees(GAMMA_0):.10f} deg")

    check("(N4) tan(gamma_bar) = sqrt(5) [protected]",
          close(tan_gamma_bar, math.sqrt(5.0)))
    check("(N4) gamma_bar = gamma_0 [protected]",
          close(gamma_bar, GAMMA_0))
    check("the (4 - alpha_s)/24 factor cancels in eta_bar/rho_bar",
          close(tan_gamma_bar - math.sqrt(5.0), 0.0))


def audit_n5_tan_beta_bar() -> None:
    banner("(N5): closed form for tan(beta_bar)")

    rho_bar = (4.0 - ALPHA_S_V) / 24.0
    eta_bar = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / 24.0
    tan_beta_direct = eta_bar / (1.0 - rho_bar)
    tan_beta_closed = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / (20.0 + ALPHA_S_V)
    beta_bar = math.atan(tan_beta_closed)

    print(f"  tan(beta_bar) direct        = {tan_beta_direct:.15f}")
    print(f"  sqrt(5)(4-alpha_s)/(20+alpha_s) = {tan_beta_closed:.15f}")
    print(f"  beta_bar                    = {math.degrees(beta_bar):.6f} deg")

    check("(N5) closed form matches direct eta_bar/(1-rho_bar)",
          close(tan_beta_direct, tan_beta_closed))
    check("beta_bar < beta_0 (NLO reduces beta from atlas-leading)",
          beta_bar < BETA_0)
    check("beta_bar within 2 deg of atlas-leading beta_0",
          abs(math.degrees(beta_bar) - math.degrees(BETA_0)) < 2.0)


def audit_n6_n7_alpha_bar_deviation() -> None:
    banner("(N6), (N7): alpha_bar and linear deviation theorem")

    tan_beta = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / (20.0 + ALPHA_S_V)
    beta_bar = math.atan(tan_beta)

    alpha_bar = math.pi - GAMMA_0 - beta_bar
    alpha_bar_minus_half_pi = alpha_bar - math.pi / 2.0
    linear_pred = math.sqrt(5.0) / 20.0 * ALPHA_S_V

    print(f"  alpha_bar                   = {math.degrees(alpha_bar):.10f} deg")
    print(f"  alpha_bar - pi/2 (rad)      = {alpha_bar_minus_half_pi:.15f}")
    print(f"  alpha_bar - pi/2 (deg)      = {math.degrees(alpha_bar_minus_half_pi):.10f}")
    print(f"  (sqrt(5)/20) alpha_s        = {linear_pred:.15f}")
    print(f"  (sqrt(5)/20) alpha_s (deg)  = {math.degrees(linear_pred):.10f}")
    relative_error = abs(alpha_bar_minus_half_pi - linear_pred) / abs(linear_pred)
    print(f"  relative error              = {relative_error:.6e}")

    check("(N6) alpha_bar = pi - gamma_0 - beta_bar (positive)",
          alpha_bar > 0)
    check("(N7) linear deviation matches exact within 1e-3 (NLO accuracy)",
          relative_error < 1e-3)
    check("alpha_bar > pi/2 (apex angle increases with alpha_s)",
          alpha_bar > math.pi / 2.0)
    check("alpha_bar within 1 deg of pi/2 at canonical alpha_s",
          abs(math.degrees(alpha_bar_minus_half_pi)) < 1.0)


def audit_n8_protected_doubled_gamma() -> None:
    banner("(N8) PROTECTED: sin/cos(2 gamma_bar) = sqrt(5)/3, -2/3")

    sin_2gamma_bar = math.sin(2 * GAMMA_0)
    cos_2gamma_bar = math.cos(2 * GAMMA_0)
    expected_sin = math.sqrt(5.0) / 3.0
    expected_cos = -2.0 / 3.0

    print(f"  sin(2 gamma_bar)   = {sin_2gamma_bar:.15f}")
    print(f"  sqrt(5)/3          = {expected_sin:.15f}")
    print(f"  cos(2 gamma_bar)   = {cos_2gamma_bar:.15f}")
    print(f"  -2/3               = {expected_cos:.15f}")

    check("(N8) sin(2 gamma_bar) = sqrt(5)/3 [protected]",
          close(sin_2gamma_bar, expected_sin))
    check("(N8) cos(2 gamma_bar) = -2/3 [protected]",
          close(cos_2gamma_bar, expected_cos))
    check("sin^2 + cos^2 = 1",
          close(sin_2gamma_bar ** 2 + cos_2gamma_bar ** 2, 1.0))


def audit_n9_doubled_beta_closed_forms() -> None:
    banner("(N9): closed forms for sin(2 beta_bar), cos(2 beta_bar)")

    a = ALPHA_S_V
    num_sin = 2.0 * math.sqrt(5.0) * (4.0 - a) * (20.0 + a)
    den = (20.0 + a) ** 2 + 5.0 * (4.0 - a) ** 2
    num_cos = (20.0 + a) ** 2 - 5.0 * (4.0 - a) ** 2
    sin_2beta_closed = num_sin / den
    cos_2beta_closed = num_cos / den

    tan_beta = math.sqrt(5.0) * (4.0 - a) / (20.0 + a)
    beta_bar = math.atan(tan_beta)
    sin_2beta_direct = math.sin(2 * beta_bar)
    cos_2beta_direct = math.cos(2 * beta_bar)

    print(f"  sin(2 beta_bar) closed = {sin_2beta_closed:.15f}")
    print(f"  sin(2 beta_bar) direct = {sin_2beta_direct:.15f}")
    print(f"  cos(2 beta_bar) closed = {cos_2beta_closed:.15f}")
    print(f"  cos(2 beta_bar) direct = {cos_2beta_direct:.15f}")

    check("(N9) sin(2 beta_bar) closed matches direct",
          close(sin_2beta_closed, sin_2beta_direct))
    check("(N9) cos(2 beta_bar) closed matches direct",
          close(cos_2beta_closed, cos_2beta_direct))
    check("sin^2 + cos^2 = 1",
          close(sin_2beta_closed ** 2 + cos_2beta_closed ** 2, 1.0))
    check("sin(2 beta_bar) < sin(2 beta_0) (NLO reduces sin(2 beta))",
          sin_2beta_closed < math.sqrt(5.0) / 3.0)


def audit_lo_recovery() -> None:
    banner("Cross-check: alpha_s -> 0 recovers atlas-leading triangle")

    a = 0.0
    rho_bar = (4.0 - a) / 24.0
    eta_bar = math.sqrt(5.0) * (4.0 - a) / 24.0
    tan_beta = math.sqrt(5.0) * (4.0 - a) / (20.0 + a)
    tan_gamma = math.sqrt(5.0)
    alpha_bar = math.pi - math.atan(tan_gamma) - math.atan(tan_beta)

    print(f"  rho_bar(0)        = {rho_bar:.15f} (= 1/6 = {1/6:.15f})")
    print(f"  eta_bar(0)        = {eta_bar:.15f} (= sqrt(5)/6 = {math.sqrt(5)/6:.15f})")
    print(f"  tan(beta_bar)(0)  = {tan_beta:.15f} (= 1/sqrt(5) = {1/math.sqrt(5):.15f})")
    print(f"  alpha_bar(0)      = {math.degrees(alpha_bar):.10f} deg (= 90.0)")

    check("rho_bar(0) = 1/6 (atlas-leading)", close(rho_bar, 1.0 / 6.0))
    check("eta_bar(0) = sqrt(5)/6 (atlas-leading)",
          close(eta_bar, math.sqrt(5.0) / 6.0))
    check("tan(beta_bar)(0) = 1/sqrt(5) (atlas-leading)",
          close(tan_beta, 1.0 / math.sqrt(5.0)))
    check("alpha_bar(0) = pi/2 (atlas right angle recovered)",
          close(alpha_bar, math.pi / 2.0))


def audit_pdg_comparators() -> None:
    banner("Post-derivation comparators (PDG)")

    tan_beta = math.sqrt(5.0) * (4.0 - ALPHA_S_V) / (20.0 + ALPHA_S_V)
    beta_bar = math.atan(tan_beta)
    alpha_bar = math.pi - GAMMA_0 - beta_bar
    sin_2beta_bar = math.sin(2 * beta_bar)

    gamma_bar_deg = math.degrees(GAMMA_0)
    beta_bar_deg = math.degrees(beta_bar)
    alpha_bar_deg = math.degrees(alpha_bar)

    dev_gamma = (gamma_bar_deg - GAMMA_PDG_DEG) / GAMMA_PDG_ERR_DEG
    dev_beta = (beta_bar_deg - BETA_PDG_DEG) / BETA_PDG_ERR_DEG
    dev_alpha = (alpha_bar_deg - ALPHA_PDG_DEG) / ALPHA_PDG_ERR_DEG
    dev_sin_2beta = (sin_2beta_bar - SIN_2BETA_PDG) / SIN_2BETA_PDG_ERR

    print(f"  gamma_bar atlas-NLO = {gamma_bar_deg:.4f} deg [protected]")
    print(f"    PDG               = {GAMMA_PDG_DEG:.1f} +/- {GAMMA_PDG_ERR_DEG:.1f} deg")
    print(f"    deviation         = {dev_gamma:+.3f} sigma")
    print(f"  beta_bar  atlas-NLO = {beta_bar_deg:.4f} deg")
    print(f"    PDG               = {BETA_PDG_DEG:.1f} +/- {BETA_PDG_ERR_DEG:.1f} deg")
    print(f"    deviation         = {dev_beta:+.3f} sigma")
    print(f"  alpha_bar atlas-NLO = {alpha_bar_deg:.4f} deg")
    print(f"    PDG               = {ALPHA_PDG_DEG:.1f} +/- {ALPHA_PDG_ERR_DEG:.1f} deg")
    print(f"    deviation         = {dev_alpha:+.3f} sigma")
    print(f"  sin(2 beta_bar)     = {sin_2beta_bar:.6f}")
    print(f"    PDG               = {SIN_2BETA_PDG:.3f} +/- {SIN_2BETA_PDG_ERR:.3f}")
    print(f"    deviation         = {dev_sin_2beta:+.3f} sigma")

    check("gamma_bar within 1 sigma of PDG", abs(dev_gamma) < 1.0)
    check("beta_bar within 2 sigma of PDG", abs(dev_beta) < 2.0)
    check("alpha_bar within 2 sigma of PDG", abs(dev_alpha) < 2.0)
    check("sin(2 beta_bar) reduces atlas-LO 3.6 sigma to NLO 2.2 sigma",
          abs(dev_sin_2beta) < 2.5)
    sin_2beta_LO = math.sqrt(5.0) / 3.0
    dev_LO = (sin_2beta_LO - SIN_2BETA_PDG) / SIN_2BETA_PDG_ERR
    check("NLO sin(2 beta) is closer to PDG than LO",
          abs(dev_sin_2beta) < abs(dev_LO),
          f"NLO {dev_sin_2beta:+.2f} sigma vs LO {dev_LO:+.2f} sigma")


def audit_summary() -> None:
    banner("Summary of new content")

    print("  PROTECTED INVARIANTS (new structural content at NLO):")
    print("    gamma_bar = gamma_0 = arctan(sqrt(5))")
    print("    sin(2 gamma_bar) = sqrt(5)/3")
    print("    cos(2 gamma_bar) = -2/3")
    print()
    print("  CLOSED-FORM NLO PREDICTIONS (new explicit content):")
    print("    rho_bar          = (4 - alpha_s) / 24")
    print("    eta_bar          = sqrt(5)(4 - alpha_s) / 24")
    print("    tan(beta_bar)    = sqrt(5)(4 - alpha_s) / (20 + alpha_s)")
    print("    alpha_bar - pi/2 = (sqrt(5)/20) alpha_s + O(alpha_s^2)")
    print()
    print("  At canonical alpha_s(v) = 0.103304:")
    print(f"    rho_bar          = {(4 - ALPHA_S_V)/24:.6f}")
    print(f"    eta_bar          = {math.sqrt(5)*(4 - ALPHA_S_V)/24:.6f}")
    print(f"    gamma_bar        = {math.degrees(GAMMA_0):.4f} deg [PROTECTED]")
    tan_beta = math.sqrt(5)*(4 - ALPHA_S_V)/(20 + ALPHA_S_V)
    beta_bar = math.atan(tan_beta)
    alpha_bar = math.pi - GAMMA_0 - beta_bar
    print(f"    beta_bar         = {math.degrees(beta_bar):.4f} deg")
    print(f"    alpha_bar        = {math.degrees(alpha_bar):.4f} deg")
    print(f"    sin(2 beta_bar)  = {math.sin(2*beta_bar):.6f}")


def main() -> int:
    print("=" * 88)
    print("CKM NLO barred-triangle and protected-gamma theorem audit")
    print("See docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_n1_n2_apex()
    audit_n3_radius()
    audit_n4_protected_gamma()
    audit_n5_tan_beta_bar()
    audit_n6_n7_alpha_bar_deviation()
    audit_n8_protected_doubled_gamma()
    audit_n9_doubled_beta_closed_forms()
    audit_lo_recovery()
    audit_pdg_comparators()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
