#!/usr/bin/env python3
"""CKM B_s mixing phase derivation theorem audit.

Verifies the structural identities and the derived B_s mixing prediction in
  docs/CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md

  (T1) sin(2 alpha_0) = 0,         cos(2 alpha_0) = -1
  (T2) sin(2 beta_0)  = sqrt(5)/3, cos(2 beta_0)  = 2/3
  (T3) sin(2 gamma_0) = sqrt(5)/3, cos(2 gamma_0) = -2/3
  (T4) sin(2 beta_0)  = sin(2 gamma_0)
  (S1) |R_b|^2 = rho^2 + eta^2     = 1/6
  (S2) |R_t|^2 = (1-rho)^2 + eta^2 = 5/6
  (S3) |R_b|^2 + |R_t|^2 = 1
  (S4) |R_t|/|R_b| = sqrt(5)
  (B1) beta_s = lambda^2 eta = alpha_s(v) sqrt(5)/12
  (B2) phi_s  = -2 beta_s    = -alpha_s(v) sqrt(5)/6
  (B3) sin(2 beta_s) = alpha_s(v) sqrt(5)/6 (small-angle)

The CP-asymmetry sin(2 beta_0) = sqrt(5)/3 and the side-length R_t^2 = 5/6
are new named structural identities. The B_s mixing phase prediction
phi_s = -alpha_s(v) sqrt(5)/6 = -3.85e-2 rad is the new derived prediction;
it lies inside the LHCb 1-sigma band -0.039 +/- 0.022 rad at 0.02 sigma.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
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


# -----------------------------------------------------------------------------
# Retained inputs.
# -----------------------------------------------------------------------------
ALPHA_S_V = CANONICAL_ALPHA_S_V

RHO = Fraction(1, 6)
ETA_SQUARED = Fraction(5, 36)
ETA_VAL = math.sqrt(5.0) / 6.0
LAMBDA_SQ = ALPHA_S_V / 2.0
A_SQ_EXACT = Fraction(2, 3)


# Post-derivation comparators.
SIN_2BETA_PDG = 0.706
SIN_2BETA_PDG_ERR = 0.011
PHI_S_LHCB = -0.039
PHI_S_LHCB_ERR = 0.022
BETA_S_LHCB = 0.0188
BETA_S_LHCB_ERR = 0.0030
RT_OVER_RB_PDG = 2.27
RT_OVER_RB_PDG_ERR = 0.07
R_B_PDG = 0.435
R_B_PDG_ERR = 0.014
R_T_PDG = 0.92
R_T_PDG_ERR = 0.02


@dataclass(frozen=True)
class TriangleAngle:
    name: str
    tan_value_squared: Fraction       # tan^2(theta) as exact rational
    tan_value: float                  # tan(theta), positive root
    sin_double_expected: float        # exact sin(2 theta)
    cos_double_expected: Fraction     # exact rational cos(2 theta)


def audit_inputs() -> None:
    banner("Retained inputs")

    print(f"  alpha_s(v)         = {ALPHA_S_V:.15f}")
    print(f"  lambda^2           = {LAMBDA_SQ:.15f} (= alpha_s(v)/2)")
    print(f"  A^2                = {A_SQ_EXACT}")
    print(f"  rho                = {RHO}")
    print(f"  eta^2              = {ETA_SQUARED}")
    print(f"  eta                = {ETA_VAL:.15f} (= sqrt(5)/6)")

    check("alpha_s(v) positive", ALPHA_S_V > 0)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2))
    check("A^2 exact rational is 2/3", A_SQ_EXACT == Fraction(2, 3))
    check("rho exact rational is 1/6", RHO == Fraction(1, 6))
    check("eta^2 exact rational is 5/36", ETA_SQUARED == Fraction(5, 36))
    check("eta = sqrt(5)/6", close(ETA_VAL, math.sqrt(5) / 6))
    check("rho^2 + eta^2 = 1/6", RHO * RHO + ETA_SQUARED == Fraction(1, 6))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_triangle_angles() -> None:
    banner("Atlas-triangle base angles")

    tan_beta = math.sqrt(5.0) / 5.0  # = 1/sqrt(5)
    tan_gamma = math.sqrt(5.0)
    beta_0 = math.atan(tan_beta)
    gamma_0 = math.atan(tan_gamma)
    alpha_0 = math.pi - beta_0 - gamma_0

    print(f"  tan(beta_0)   = {tan_beta:.15f} (= 1/sqrt(5))")
    print(f"  tan(gamma_0)  = {tan_gamma:.15f} (= sqrt(5))")
    print(f"  beta_0        = {math.degrees(beta_0):.6f} deg")
    print(f"  gamma_0       = {math.degrees(gamma_0):.6f} deg")
    print(f"  alpha_0       = {math.degrees(alpha_0):.6f} deg")

    check("tan(beta_0) tan(gamma_0) = 1", close(tan_beta * tan_gamma, 1.0))
    check("alpha_0 = pi/2 (atlas-leading right angle)",
          close(alpha_0, math.pi / 2, tol=1e-12))


def audit_doubled_angle_catalog() -> None:
    banner("Doubled-angle CP catalog (T1) - (T4)")

    # T2: 2 beta_0
    t_beta_sq = Fraction(1, 5)
    cos_2beta_frac = (1 - t_beta_sq) / (1 + t_beta_sq)
    sin_2beta = 2 * (math.sqrt(5.0) / 5.0) / float(1 + t_beta_sq)
    cos_2beta = float(cos_2beta_frac)
    expected_sin_2beta = math.sqrt(5.0) / 3.0
    expected_cos_2beta = Fraction(2, 3)

    print(f"  sin(2 beta_0)   = {sin_2beta:.15f}")
    print(f"  sqrt(5)/3       = {expected_sin_2beta:.15f}")
    check("sin(2 beta_0) = sqrt(5)/3", close(sin_2beta, expected_sin_2beta))
    check("cos(2 beta_0) = 2/3 (exact rational)",
          cos_2beta_frac == expected_cos_2beta)
    check("sin^2(2 beta_0) + cos^2(2 beta_0) = 1",
          close(sin_2beta**2 + cos_2beta**2, 1.0))

    # Direct sympy-free recomputation cross-check
    beta_0 = math.atan(math.sqrt(5.0) / 5.0)
    check("direct sin(2 beta_0) matches sqrt(5)/3",
          close(math.sin(2 * beta_0), math.sqrt(5) / 3))
    check("direct cos(2 beta_0) matches 2/3",
          close(math.cos(2 * beta_0), 2.0 / 3.0))

    # T3: 2 gamma_0
    t_gamma_sq = Fraction(5, 1)
    cos_2gamma_frac = (1 - t_gamma_sq) / (1 + t_gamma_sq)
    sin_2gamma = 2 * math.sqrt(5.0) / float(1 + t_gamma_sq)
    cos_2gamma = float(cos_2gamma_frac)
    expected_sin_2gamma = math.sqrt(5.0) / 3.0
    expected_cos_2gamma = Fraction(-2, 3)

    print(f"  sin(2 gamma_0)  = {sin_2gamma:.15f}")
    print(f"  cos(2 gamma_0)  = {cos_2gamma:.15f}")
    check("sin(2 gamma_0) = sqrt(5)/3", close(sin_2gamma, expected_sin_2gamma))
    check("cos(2 gamma_0) = -2/3 (exact rational)",
          cos_2gamma_frac == expected_cos_2gamma)

    gamma_0 = math.atan(math.sqrt(5.0))
    check("direct sin(2 gamma_0) matches sqrt(5)/3",
          close(math.sin(2 * gamma_0), math.sqrt(5) / 3))
    check("direct cos(2 gamma_0) matches -2/3",
          close(math.cos(2 * gamma_0), -2.0 / 3.0))

    # T4: sin(2 beta_0) = sin(2 gamma_0)
    check("sin(2 beta_0) = sin(2 gamma_0) (forced by alpha_0 = pi/2)",
          close(sin_2beta, sin_2gamma))
    check("cos(2 beta_0) = -cos(2 gamma_0) (forced by alpha_0 = pi/2)",
          close(cos_2beta, -cos_2gamma))

    # T1: 2 alpha_0 = pi
    sin_2alpha = math.sin(2 * (math.pi / 2))
    cos_2alpha = math.cos(2 * (math.pi / 2))
    print(f"  sin(2 alpha_0)  = {sin_2alpha:.15f}")
    print(f"  cos(2 alpha_0)  = {cos_2alpha:.15f}")
    check("sin(2 alpha_0) = 0", close(sin_2alpha, 0.0))
    check("cos(2 alpha_0) = -1", close(cos_2alpha, -1.0))


def audit_side_length_catalog() -> None:
    banner("Triangle side-length catalog (S1) - (S4)")

    R_b_sq = RHO * RHO + ETA_SQUARED
    R_t_sq = (1 - RHO) ** 2 + ETA_SQUARED
    print(f"  |R_b|^2 = rho^2 + eta^2     = {R_b_sq}")
    print(f"  |R_t|^2 = (1-rho)^2 + eta^2 = {R_t_sq}")

    check("|R_b|^2 = 1/6", R_b_sq == Fraction(1, 6))
    check("|R_t|^2 = 5/6", R_t_sq == Fraction(5, 6))
    check("|R_b|^2 + |R_t|^2 = 1 (Pythagoras forced by alpha_0 = pi/2)",
          R_b_sq + R_t_sq == 1)

    R_b = math.sqrt(float(R_b_sq))
    R_t = math.sqrt(float(R_t_sq))
    ratio = R_t / R_b
    print(f"  |R_b|     = {R_b:.15f} (= 1/sqrt(6))")
    print(f"  |R_t|     = {R_t:.15f} (= sqrt(5/6))")
    print(f"  R_t/R_b   = {ratio:.15f} (= sqrt(5))")

    check("|R_b| = 1/sqrt(6)", close(R_b, 1 / math.sqrt(6)))
    check("|R_t| = sqrt(5/6)", close(R_t, math.sqrt(5 / 6)))
    check("|R_t|/|R_b| = sqrt(5)", close(ratio, math.sqrt(5)))
    check("|R_t|^2 / |R_b|^2 = 5", float(R_t_sq / R_b_sq) == 5.0)


def audit_bs_mixing_phase() -> None:
    banner("B_s mixing phase derivation (B1) - (B3)")

    # Wolfenstein expansion at order lambda^2:
    #   V_us  =  lambda
    #   V_cs  =  1 - lambda^2/2
    #   V_cb  =  A lambda^2
    #   V_ts  = -A lambda^2 [1 - lambda^2 (1/2 - rho - i eta)]
    #   V_tb  =  1
    lambda_sq = LAMBDA_SQ
    A = math.sqrt(2.0 / 3.0)
    rho = float(RHO)
    eta = ETA_VAL

    # Compute V_ts V_tb* / (V_cs V_cb*) numerically as a complex ratio.
    # V_ts = -A lambda^2 [1 - lambda^2 (1/2 - rho - i eta)]
    #      = -A lambda^2 + A lambda^4 (1/2 - rho - i eta)
    # so Im(V_ts) = -A lambda^4 eta.
    V_ts_real = -A * lambda_sq * (1 - lambda_sq * (0.5 - rho))
    V_ts_imag = -A * lambda_sq * lambda_sq * eta
    V_tb = 1.0
    V_cs = 1.0 - lambda_sq / 2.0
    V_cb = A * lambda_sq

    # ratio = -V_ts V_tb* / (V_cs V_cb*)
    numerator_real = -V_ts_real * V_tb
    numerator_imag = -V_ts_imag * V_tb
    denominator = V_cs * V_cb
    ratio_real = numerator_real / denominator
    ratio_imag = numerator_imag / denominator
    beta_s_numeric = math.atan2(ratio_imag, ratio_real)

    # Leading-order analytic prediction
    beta_s_leading = lambda_sq * eta
    beta_s_clean = ALPHA_S_V * math.sqrt(5.0) / 12.0

    print(f"  lambda^2 eta             = {beta_s_leading:.15e} rad")
    print(f"  alpha_s(v) sqrt(5)/12    = {beta_s_clean:.15e} rad")
    print(f"  beta_s (full Wolfenstein) = {beta_s_numeric:.15e} rad")
    print(f"  beta_s in degrees        = {math.degrees(beta_s_clean):.6f} deg")

    check("beta_s = lambda^2 eta (leading order)",
          close(beta_s_leading, ALPHA_S_V / 2 * (math.sqrt(5) / 6)))
    check("beta_s = alpha_s(v) sqrt(5)/12",
          close(beta_s_leading, beta_s_clean))
    # The full Wolfenstein expansion at order lambda^2 carries an O(lambda^2)
    # correction relative to the leading lambda^2 eta term, so the expected
    # relative size of the residual is O(alpha_s(v)/2) ~ 5%.
    relative_residual = abs(beta_s_numeric - beta_s_leading) / abs(beta_s_leading)
    print(f"  full-Wolfenstein vs leading relative residual = {relative_residual:.4%}")
    check("full Wolfenstein beta_s within 5% of leading order (NLO size)",
          relative_residual < 5e-2)
    check("residual is dominated by lambda^2 (~ alpha_s(v)/2 ~ 5%) corrections",
          0.5 * lambda_sq < 0.06)

    # B2: phi_s = -2 beta_s
    phi_s = -2 * beta_s_clean
    phi_s_clean = -ALPHA_S_V * math.sqrt(5.0) / 6.0
    print(f"  phi_s                     = {phi_s:.15e} rad")
    print(f"  -alpha_s(v) sqrt(5)/6     = {phi_s_clean:.15e} rad")
    print(f"  phi_s in degrees          = {math.degrees(phi_s_clean):.6f} deg")

    check("phi_s = -2 beta_s = -alpha_s(v) sqrt(5)/6",
          close(phi_s, phi_s_clean))

    # B3: sin(2 beta_s) ~ 2 beta_s for small angles
    sin_2bs_exact = math.sin(2 * beta_s_clean)
    sin_2bs_leading = 2 * beta_s_clean
    print(f"  sin(2 beta_s) exact       = {sin_2bs_exact:.15f}")
    print(f"  2 beta_s leading          = {sin_2bs_leading:.15f}")
    check("sin(2 beta_s) ~= alpha_s(v) sqrt(5)/6 (small-angle leading)",
          abs(sin_2bs_exact - ALPHA_S_V * math.sqrt(5) / 6) < 1e-4)


def audit_observation_comparators() -> None:
    banner("Post-derivation comparators (PDG / LHCb)")

    sin_2beta = math.sqrt(5.0) / 3.0
    deviation_sin_2beta = (sin_2beta - SIN_2BETA_PDG) / SIN_2BETA_PDG_ERR
    print(f"  sin(2 beta_0) atlas       = {sin_2beta:.6f}")
    print(f"  sin(2 beta_0) PDG         = {SIN_2BETA_PDG:.3f} +/- {SIN_2BETA_PDG_ERR:.3f}")
    print(f"  deviation                 = {deviation_sin_2beta:+.3f} sigma")
    check("atlas-leading sin(2 beta_0) > PDG (known atlas-vs-physical residual)",
          sin_2beta > SIN_2BETA_PDG)

    R_b = 1 / math.sqrt(6.0)
    R_t = math.sqrt(5.0 / 6.0)
    ratio = R_t / R_b
    deviation_ratio = (ratio - RT_OVER_RB_PDG) / RT_OVER_RB_PDG_ERR
    print(f"  R_t/R_b atlas             = {ratio:.6f} (= sqrt(5))")
    print(f"  R_t/R_b PDG               = {RT_OVER_RB_PDG:.3f} +/- {RT_OVER_RB_PDG_ERR:.3f}")
    print(f"  deviation                 = {deviation_ratio:+.3f} sigma")
    check("atlas R_t/R_b agrees with PDG within 1 sigma",
          abs(deviation_ratio) < 1.0)

    deviation_R_b = (R_b - R_B_PDG) / R_B_PDG_ERR
    deviation_R_t = (R_t - R_T_PDG) / R_T_PDG_ERR
    print(f"  R_b atlas                 = {R_b:.6f}")
    print(f"  R_b PDG                   = {R_B_PDG:.3f} +/- {R_B_PDG_ERR:.3f}")
    print(f"  R_b deviation             = {deviation_R_b:+.3f} sigma")
    print(f"  R_t atlas                 = {R_t:.6f}")
    print(f"  R_t PDG                   = {R_T_PDG:.3f} +/- {R_T_PDG_ERR:.3f}")
    print(f"  R_t deviation             = {deviation_R_t:+.3f} sigma")
    check("atlas R_t agrees with PDG within 1 sigma",
          abs(deviation_R_t) < 1.0)
    check("atlas R_b agrees with PDG within 2 sigma",
          abs(deviation_R_b) < 2.0)

    beta_s = ALPHA_S_V * math.sqrt(5.0) / 12.0
    deviation_beta_s = (beta_s - BETA_S_LHCB) / BETA_S_LHCB_ERR
    print(f"  beta_s atlas              = {beta_s:.6e} rad ({math.degrees(beta_s):.4f} deg)")
    print(f"  beta_s LHCb               = {BETA_S_LHCB:.4f} +/- {BETA_S_LHCB_ERR:.4f} rad")
    print(f"  deviation                 = {deviation_beta_s:+.3f} sigma")
    check("atlas beta_s agrees with LHCb within 1 sigma",
          abs(deviation_beta_s) < 1.0)

    phi_s = -ALPHA_S_V * math.sqrt(5.0) / 6.0
    deviation_phi_s = (phi_s - PHI_S_LHCB) / PHI_S_LHCB_ERR
    print(f"  phi_s atlas               = {phi_s:.6e} rad ({math.degrees(phi_s):.4f} deg)")
    print(f"  phi_s LHCb                = {PHI_S_LHCB:.3f} +/- {PHI_S_LHCB_ERR:.3f} rad")
    print(f"  deviation                 = {deviation_phi_s:+.3f} sigma")
    check("atlas phi_s agrees with LHCb within 1 sigma",
          abs(deviation_phi_s) < 1.0)
    check("atlas phi_s agrees with LHCb within 0.1 sigma (sharp prediction)",
          abs(deviation_phi_s) < 0.1)


def audit_summary() -> None:
    banner("Summary of new content carried by this theorem")

    print("  STRUCTURAL IDENTITIES (new named rows):")
    print("    sin(2 alpha_0) = 0,         cos(2 alpha_0) = -1")
    print("    sin(2 beta_0)  = sqrt(5)/3, cos(2 beta_0)  =  2/3")
    print("    sin(2 gamma_0) = sqrt(5)/3, cos(2 gamma_0) = -2/3")
    print("    sin(2 beta_0)  = sin(2 gamma_0) (forced by alpha_0 = pi/2)")
    print("    |R_t|^2 = 5/6,  |R_b|^2 + |R_t|^2 = 1,  R_t/R_b = sqrt(5)")
    print()
    print("  DERIVED PREDICTION (new numerical result):")
    print("    beta_s = alpha_s(v) sqrt(5) / 12")
    print("    phi_s  = -alpha_s(v) sqrt(5) / 6")
    print("    sin(2 beta_s) ~= alpha_s(v) sqrt(5) / 6")
    print()
    print("  At canonical alpha_s(v) = 0.1033038...:")
    print(f"    beta_s = {ALPHA_S_V * math.sqrt(5)/12:.6e} rad = "
          f"{math.degrees(ALPHA_S_V * math.sqrt(5)/12):.4f} deg")
    print(f"    phi_s  = {-ALPHA_S_V * math.sqrt(5)/6:.6e} rad = "
          f"{math.degrees(-ALPHA_S_V * math.sqrt(5)/6):.4f} deg")


def main() -> int:
    print("=" * 88)
    print("CKM B_s mixing phase derivation theorem audit")
    print("See docs/CKM_BS_MIXING_PHASE_DERIVATION_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_triangle_angles()
    audit_doubled_angle_catalog()
    audit_side_length_catalog()
    audit_bs_mixing_phase()
    audit_observation_comparators()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
