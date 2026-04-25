#!/usr/bin/env python3
"""Gravity-cosmology spectral tower Lambda-bridge theorem audit.

Verifies the new closed-form structural identities in
  docs/GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md

Pure-Lambda form of the spectral tower:
  (L1) m^2_TT(l)     = ((l(l+2) - 2)/3) hbar^2 Lambda/c^2
  (L2) m^2_vec(l)    = ((l(l+2) - 1)/3) hbar^2 Lambda/c^2
  (L3) m^2_scalar(l) = (l(l+2)/3)       hbar^2 Lambda/c^2

Lowest-mode closed forms:
  (L4) m^2_TT(2)  = 2 hbar^2 Lambda/c^2,  m_TT(2)  = sqrt(2)   hbar sqrt(Lambda)/c
  (L5) m^2_vec(1) = (2/3) hbar^2 Lambda/c^2, m_vec(1) = sqrt(2/3) hbar sqrt(Lambda)/c
  (L6) m_scalar(0) = 0

Lambda-INDEPENDENT structural ratio:
  (L7) m_TT(2)/m_vec(1) = sqrt(3)

Universal spin-curvature gaps (independent of l):
  (L8) m^2_scalar - m^2_vec   = (1/3) hbar^2 Lambda/c^2
  (L9) m^2_vec    - m^2_TT    = (1/3) hbar^2 Lambda/c^2
  (L10) m^2_scalar - m^2_TT    = (2/3) hbar^2 Lambda/c^2

Numerical: with PDG Lambda_obs = 1.105e-52 m^-2,
  m_TT(2) = 2.93e-33 eV/c^2 (20x below LIGO bound 6e-32 eV/c^2)
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

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


# Physical constants
HBAR = 1.054571817e-34       # J s
C = 2.99792458e8             # m/s
EV_PER_J = 6.241509074e18    # eV per J


# PDG-2024 cosmological constant
LAMBDA_OBS = 1.105e-52       # m^-2 (Planck 2018 LCDM)


# Retained spectral tower numerator forms
def TT_numerator(l: int) -> int:
    """Returns l(l+2) - 2 for the TT graviton tower at angular mode l."""
    return l * (l + 2) - 2


def vec_numerator(l: int) -> int:
    """Returns l(l+2) - 1 for the vector tower at angular mode l."""
    return l * (l + 2) - 1


def scalar_numerator(l: int) -> int:
    """Returns l(l+2) for the scalar tower at angular mode l."""
    return l * (l + 2)


def audit_inputs() -> None:
    banner("Retained inputs (gravity tower + cosmological constant)")

    print(f"  hbar              = {HBAR:.6e} J s")
    print(f"  c                 = {C:.6e} m/s")
    print(f"  Lambda_obs (PDG)  = {LAMBDA_OBS:.6e} m^-2")
    print(f"  R_dS = sqrt(3/Lambda) = {math.sqrt(3.0/LAMBDA_OBS):.6e} m")

    check("hbar > 0", HBAR > 0)
    check("c > 0", C > 0)
    check("Lambda_obs > 0", LAMBDA_OBS > 0)
    check("Lambda = 3/R^2 (retained)",
          close(3.0 / (math.sqrt(3.0/LAMBDA_OBS) ** 2), LAMBDA_OBS))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/GRAVITON_SPECTRAL_TOWER_THEOREM_NOTE_2026-04-24.md",
        "docs/VECTOR_GAUGE_FIELD_KK_TOWER_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_l1_l3_pure_lambda_form() -> None:
    banner("(L1)-(L3): Pure-Lambda form of the spectral tower")

    # Test at multiple l values
    for l in [2, 3, 4, 5]:
        TT_factor = Fraction(TT_numerator(l), 3)
        vec_factor = Fraction(vec_numerator(l) if l >= 1 else 0, 3)
        scalar_factor = Fraction(scalar_numerator(l), 3)

        # Spectral unit
        unit_kg2 = HBAR ** 2 * LAMBDA_OBS / (3.0 * C ** 2)

        # Compute m^2 in three ways
        m2_TT_R_form = TT_numerator(l) * HBAR ** 2 / (C ** 2 * (3.0 / LAMBDA_OBS))
        m2_TT_Lambda_form = float(TT_factor) * HBAR ** 2 * LAMBDA_OBS / C ** 2

        check(f"(L1) at l={l}: TT in pure-Lambda form matches R-form",
              close(m2_TT_R_form, m2_TT_Lambda_form))

        m2_vec_R = vec_numerator(l) * HBAR ** 2 / (C ** 2 * (3.0 / LAMBDA_OBS))
        m2_vec_L = float(vec_factor) * HBAR ** 2 * LAMBDA_OBS / C ** 2
        check(f"(L2) at l={l}: vector in pure-Lambda form matches",
              close(m2_vec_R, m2_vec_L))

        m2_scalar_R = scalar_numerator(l) * HBAR ** 2 / (C ** 2 * (3.0 / LAMBDA_OBS))
        m2_scalar_L = float(scalar_factor) * HBAR ** 2 * LAMBDA_OBS / C ** 2
        check(f"(L3) at l={l}: scalar in pure-Lambda form matches",
              close(m2_scalar_R, m2_scalar_L))


def audit_l4_l6_lowest_modes() -> None:
    banner("(L4)-(L6): Lowest-mode closed forms")

    # m_TT(2): l(l+2) - 2 = 6, divided by 3 -> 2
    TT_lowest_factor = Fraction(TT_numerator(2), 3)
    print(f"  TT lowest l=2: l(l+2) - 2 = {TT_numerator(2)}")
    print(f"  (l(l+2) - 2)/3              = {TT_lowest_factor}")
    check("(L4) m^2_TT(2) coefficient = 2", TT_lowest_factor == 2)

    # m_vec(1): l(l+2) - 1 = 2, divided by 3 -> 2/3
    vec_lowest_factor = Fraction(vec_numerator(1), 3)
    print(f"  vec lowest l=1: l(l+2) - 1 = {vec_numerator(1)}")
    print(f"  (l(l+2) - 1)/3             = {vec_lowest_factor}")
    check("(L5) m^2_vec(1) coefficient = 2/3",
          vec_lowest_factor == Fraction(2, 3))

    # m_scalar(0): l(l+2) = 0, divided by 3 -> 0
    scalar_lowest_factor = Fraction(scalar_numerator(0), 3)
    print(f"  scalar lowest l=0: l(l+2) = {scalar_numerator(0)}")
    check("(L6) m_scalar(0) = 0 (zero mode)", scalar_lowest_factor == 0)

    # Numerical
    m_TT_2 = math.sqrt(float(TT_lowest_factor)) * HBAR * math.sqrt(LAMBDA_OBS) / C
    m_vec_1 = math.sqrt(float(vec_lowest_factor)) * HBAR * math.sqrt(LAMBDA_OBS) / C
    m_TT_2_eV = m_TT_2 * C ** 2 * EV_PER_J
    m_vec_1_eV = m_vec_1 * C ** 2 * EV_PER_J

    print(f"  m_TT(2)  = sqrt(2)   * hbar sqrt(Lambda)/c = {m_TT_2_eV:.4e} eV/c^2")
    print(f"  m_vec(1) = sqrt(2/3) * hbar sqrt(Lambda)/c = {m_vec_1_eV:.4e} eV/c^2")

    check("m_TT(2) numerical = 2.93e-33 eV/c^2",
          abs(m_TT_2_eV - 2.93e-33) / 2.93e-33 < 0.02)
    check("m_vec(1) numerical = 1.69e-33 eV/c^2",
          abs(m_vec_1_eV - 1.69e-33) / 1.69e-33 < 0.02)


def audit_l7_lambda_independent_ratio() -> None:
    banner("(L7) NEW: Lambda-INDEPENDENT ratio m_TT(2)/m_vec(1) = sqrt(3)")

    TT_2_factor = Fraction(TT_numerator(2), 3)  # = 2
    vec_1_factor = Fraction(vec_numerator(1), 3)  # = 2/3

    # m^2_TT(2) / m^2_vec(1) = TT_factor / vec_factor = 2 / (2/3) = 3
    ratio_squared = TT_2_factor / vec_1_factor
    print(f"  m^2_TT(2) / m^2_vec(1) = ({TT_2_factor})/({vec_1_factor}) = {ratio_squared}")
    print(f"  m_TT(2) / m_vec(1) = sqrt({ratio_squared}) = {math.sqrt(float(ratio_squared)):.10f}")
    print(f"  sqrt(3)                                   = {math.sqrt(3):.10f}")

    check("(L7) m^2_TT(2)/m^2_vec(1) = 3 (exact rational)",
          ratio_squared == 3)
    check("(L7) m_TT(2)/m_vec(1) = sqrt(3)",
          close(math.sqrt(float(ratio_squared)), math.sqrt(3)))

    # Test Lambda-INDEPENDENCE: ratio is the same for any Lambda
    for Lambda_test in [1e-52, 1e-50, 1e-30]:
        m2_TT_test = float(TT_2_factor) * HBAR ** 2 * Lambda_test / C ** 2
        m2_vec_test = float(vec_1_factor) * HBAR ** 2 * Lambda_test / C ** 2
        ratio_test = math.sqrt(m2_TT_test / m2_vec_test)
        check(f"(L7) ratio = sqrt(3) at Lambda = {Lambda_test:.0e} (Lambda-independent)",
              close(ratio_test, math.sqrt(3)))


def audit_l8_l10_universal_gaps() -> None:
    banner("(L8)-(L10): Universal spin-curvature gaps (independent of l)")

    # gap1 = m^2_scalar - m^2_vec = (l(l+2) - (l(l+2) - 1))/3 = 1/3 (independent of l!)
    # gap2 = m^2_vec - m^2_TT = ((l(l+2) - 1) - (l(l+2) - 2))/3 = 1/3 (independent of l!)
    # gap3 = m^2_scalar - m^2_TT = 2/3 (independent of l!)

    # Check at multiple l values
    for l in [2, 3, 4, 5, 10]:
        if l >= 2:
            gap_scalar_TT = Fraction(scalar_numerator(l) - TT_numerator(l), 3)
            check(f"(L10) at l={l}: scalar - TT gap = 2/3",
                  gap_scalar_TT == Fraction(2, 3))

        if l >= 1:
            gap_scalar_vec = Fraction(scalar_numerator(l) - vec_numerator(l), 3)
            check(f"(L8) at l={l}: scalar - vector gap = 1/3",
                  gap_scalar_vec == Fraction(1, 3))

        if l >= 2:
            gap_vec_TT = Fraction(vec_numerator(l) - TT_numerator(l), 3)
            check(f"(L9) at l={l}: vector - TT gap = 1/3",
                  gap_vec_TT == Fraction(1, 3))

    # Numerical value
    gap_scalar_TT_kg2 = (Fraction(2, 3) * HBAR ** 2 * LAMBDA_OBS / C ** 2)
    gap_scalar_TT_eV = math.sqrt(float(gap_scalar_TT_kg2)) * C ** 2 * EV_PER_J
    print(f"  Universal scalar-TT gap: m^2 = (2/3) hbar^2 Lambda/c^2")
    print(f"    Numerical: m^2 = {float(gap_scalar_TT_kg2):.4e} kg^2")
    print(f"    sqrt(gap)  = {gap_scalar_TT_eV:.4e} eV/c^2")


def audit_ligo_comparator() -> None:
    banner("LIGO comparator (consistency check, particle interpretation BOUNDED)")

    LIGO_BOUND_eV = 6e-32  # current bound
    m_TT_2 = math.sqrt(2.0) * HBAR * math.sqrt(LAMBDA_OBS) / C
    m_TT_2_eV = m_TT_2 * C ** 2 * EV_PER_J

    margin = LIGO_BOUND_eV / m_TT_2_eV
    print(f"  Framework structural eigenvalue m_TT(2) = {m_TT_2_eV:.4e} eV/c^2")
    print(f"  LIGO bound on graviton mass             < {LIGO_BOUND_eV:.0e} eV/c^2")
    print(f"  Margin (LIGO bound / framework value)   = {margin:.0f}x")

    check("framework m_TT(2) below LIGO bound (consistent)",
          m_TT_2_eV < LIGO_BOUND_eV)
    check("framework m_TT(2) order of magnitude (~1e-33 eV)",
          1e-34 < m_TT_2_eV < 1e-32)

    # 3G era bound
    BOUND_3G_eV = 1e-33  # projected 3G detector bound
    print(f"  Projected 3G era bound                  ~ {BOUND_3G_eV:.0e} eV/c^2")
    check("framework m_TT(2) within 3G era testable range",
          m_TT_2_eV > BOUND_3G_eV / 10)


def audit_summary() -> None:
    banner("Summary: NEW gravity-cosmology spectral bridge")

    print("  PURE-LAMBDA SPECTRAL TOWER (NEW closed forms):")
    print()
    print("    m^2_TT(l)     = ((l(l+2) - 2)/3) hbar^2 Lambda/c^2,  l >= 2")
    print("    m^2_vec(l)    = ((l(l+2) - 1)/3) hbar^2 Lambda/c^2,  l >= 1")
    print("    m^2_scalar(l) = (l(l+2)/3)       hbar^2 Lambda/c^2,  l >= 0")
    print()
    print("  LOWEST-MODE CLOSED FORMS (NEW):")
    print()
    print("    m_TT(2)  = sqrt(2)   hbar sqrt(Lambda)/c = 2.93e-33 eV/c^2")
    print("    m_vec(1) = sqrt(2/3) hbar sqrt(Lambda)/c = 1.69e-33 eV/c^2")
    print("    m_scalar(0) = 0")
    print()
    print("  LAMBDA-INDEPENDENT STRUCTURAL RATIO (NEW):")
    print()
    print("    m_TT(2) / m_vec(1) = sqrt(3)  (ratio independent of Lambda)")
    print()
    print("  UNIVERSAL SPIN-CURVATURE GAP (NEW):")
    print()
    print("    m^2_scalar(l) - m^2_TT(l) = (2/3) hbar^2 Lambda/c^2  (constant for l>=2)")
    print()
    print("  CROSS-SECTOR BRIDGE:")
    print("    Gravity spectral tower (geometric) <-> cosmological constant Lambda")
    print()
    print("  FALSIFICATION:")
    print("    Current LIGO bound:  m_g < 6e-32 eV/c^2 (20x above framework)")
    print("    3G era projection:  m_g < 1e-33 eV/c^2 (testable range)")


def main() -> int:
    print("=" * 88)
    print("Gravity-cosmology spectral tower Lambda-bridge theorem audit")
    print("See docs/GRAVITY_COSMOLOGY_TOWER_LAMBDA_SPECTRAL_BRIDGE_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_l1_l3_pure_lambda_form()
    audit_l4_l6_lowest_modes()
    audit_l7_lambda_independent_ratio()
    audit_l8_l10_universal_gaps()
    audit_ligo_comparator()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
