#!/usr/bin/env python3
"""Thales-pinned alpha_s-independent CKM ratios theorem audit.

Verifies the new structural classification in
  docs/CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md

  (R1)  |V_ts| / |V_cb|              =  1                (atlas-LO)
  (R2)  |V_td| / |V_ub|              =  sqrt(5)          (atlas-LO)
  (R3)  |V_td V_cb*|^2 / |V_ts V_ub*|^2  =  5            (cross-row, NEW)
  (R4)  R_b^2  =  rho                                    (Thales corollary)
  (R5)  R_t^2 / R_b^2  =  (1 - rho)/rho  =  5            (atlas point)

All five identities depend ONLY on (rho, eta) at the atlas point and the
Thales relation eta^2 = rho(1 - rho). The canonical coupling alpha_s(v)
does NOT enter. This separates the framework's atlas-LO CKM predictions
into alpha_s-INDEPENDENT (geometric, this theorem) and alpha_s-DEPENDENT
(dynamical, companion theorems) classes.

PDG comparator: the three directly comparator-ready ratios (R1)-(R3)
match at < 0.2 sigma without using alpha_s(v) at all.
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


# Retained inputs (only for cross-checks; ratios don't actually need alpha_s).
ALPHA_S_V = CANONICAL_ALPHA_S_V
LAMBDA_SQ = ALPHA_S_V / 2.0
A_SQ = Fraction(2, 3)
RHO = Fraction(1, 6)
ETA_SQ = Fraction(5, 36)
ETA_VAL = math.sqrt(5.0) / 6.0


# Atlas-LO squared-magnitude EXPRESSIONS (using exact Fraction where possible).
def V_us_sq() -> float:
    return float(LAMBDA_SQ)  # alpha_s/2

def V_cb_sq() -> float:
    return float(A_SQ * LAMBDA_SQ ** 2)  # = A^2 lambda^4 = alpha_s^2/6

def V_ts_sq() -> float:
    return float(A_SQ * LAMBDA_SQ ** 2)  # = A^2 lambda^4 = alpha_s^2/6

def V_ub_sq() -> float:
    return float(A_SQ) * LAMBDA_SQ ** 3 * float(ETA_SQ + RHO ** 2)  # = A^2 lambda^6 R_b^2

def V_td_sq() -> float:
    return float(A_SQ) * LAMBDA_SQ ** 3 * float(ETA_SQ + (1 - RHO) ** 2)  # = A^2 lambda^6 R_t^2


# PDG-2024 comparators (with errors).
V_TS_PDG = 0.0407
V_TS_PDG_ERR = 0.0010
V_CB_PDG = 0.0410
V_CB_PDG_ERR = 0.0014
V_TD_PDG = 0.00858
V_TD_PDG_ERR = 0.00018
V_UB_PDG = 0.00382
V_UB_PDG_ERR = 0.00020


def audit_inputs() -> None:
    banner("Retained inputs (for cross-checks only -- ratios don't need alpha_s)")

    print(f"  rho            = {RHO}")
    print(f"  eta^2          = {ETA_SQ}")
    print(f"  Thales: eta^2  = rho(1-rho)?  {ETA_SQ == RHO * (1 - RHO)}")
    print(f"  alpha_s(v)     = {ALPHA_S_V:.6f} (not used in ratios)")

    check("rho = 1/6", RHO == Fraction(1, 6))
    check("eta^2 = 5/36", ETA_SQ == Fraction(5, 36))
    check("Thales: eta^2 = rho(1 - rho) (exact rational)",
          ETA_SQ == RHO * (1 - RHO))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_r4_r_b_squared() -> None:
    banner("(R4): R_b^2 = rho exactly (Thales corollary, NEW form)")

    R_b_sq = RHO ** 2 + ETA_SQ
    print(f"  R_b^2 = rho^2 + eta^2  = {R_b_sq}")
    print(f"  rho                    = {RHO}")

    check("(R4) R_b^2 = rho exactly (rational)", R_b_sq == RHO)
    check("R_b^2 = 1/6 (canonical)", R_b_sq == Fraction(1, 6))
    check("Thales mechanism: rho^2 + rho(1-rho) = rho",
          RHO ** 2 + RHO * (1 - RHO) == RHO)


def audit_r5_ratio_R_t_R_b() -> None:
    banner("(R5): R_t^2 / R_b^2 = (1 - rho)/rho = 5")

    R_b_sq = RHO ** 2 + ETA_SQ
    R_t_sq = (1 - RHO) ** 2 + ETA_SQ
    ratio = R_t_sq / R_b_sq
    expected = (1 - RHO) / RHO

    print(f"  R_b^2          = {R_b_sq}")
    print(f"  R_t^2          = {R_t_sq}")
    print(f"  R_t^2 / R_b^2  = {ratio}")
    print(f"  (1 - rho)/rho  = {expected}")

    check("(R5) R_t^2 / R_b^2 = (1 - rho)/rho", ratio == expected)
    check("(R5) numerical value = 5", ratio == 5)
    check("R_t^2 = 1 - rho (Thales)", R_t_sq == 1 - RHO)


def audit_r1_vts_vcb_ratio() -> None:
    banner("(R1): |V_ts| / |V_cb| = 1 exactly at atlas-LO (alpha_s-INDEPENDENT)")

    # Both = A^2 lambda^4 in framework
    ratio_sq = V_ts_sq() / V_cb_sq()
    print(f"  |V_ts|^2 / |V_cb|^2 = {ratio_sq:.15f} (numerical)")
    print(f"  Both magnitudes = A^2 lambda^4 = alpha_s^2/6")

    check("(R1) |V_ts|^2 / |V_cb|^2 = 1 exactly", close(ratio_sq, 1.0))

    # Verify alpha_s-independence by computing at a different alpha_s
    alpha_s_test = 0.05  # arbitrary different alpha_s
    V_cb_sq_test = float(A_SQ) * (alpha_s_test/2) ** 2
    V_ts_sq_test = float(A_SQ) * (alpha_s_test/2) ** 2
    ratio_test = V_ts_sq_test / V_cb_sq_test
    print(f"  At alpha_s = 0.05: |V_ts|^2/|V_cb|^2 = {ratio_test:.15f}")
    check("(R1) ratio is independent of alpha_s value",
          close(ratio_test, 1.0))


def audit_r2_vtd_vub_ratio() -> None:
    banner("(R2): |V_td| / |V_ub| = sqrt(5) exactly at atlas-LO (alpha_s-INDEPENDENT)")

    R_b_sq = RHO ** 2 + ETA_SQ
    R_t_sq = (1 - RHO) ** 2 + ETA_SQ

    # |V_td|^2 / |V_ub|^2 = R_t^2/R_b^2 (A^2 lambda^6 cancels)
    ratio_sq_exact = R_t_sq / R_b_sq
    print(f"  |V_td|^2 / |V_ub|^2 (rational, atlas-LO) = {ratio_sq_exact}")
    print(f"  sqrt(5) numerical = {math.sqrt(5):.15f}")

    check("(R2) |V_td|^2/|V_ub|^2 = 5 (exact rational)", ratio_sq_exact == 5)
    check("(R2) |V_td|/|V_ub| = sqrt(5) numerically",
          close(math.sqrt(float(ratio_sq_exact)), math.sqrt(5)))

    # Numerical verification at canonical alpha_s
    ratio_sq_numerical = V_td_sq() / V_ub_sq()
    print(f"  |V_td|^2/|V_ub|^2 (numerical, canonical alpha_s) = {ratio_sq_numerical:.15f}")
    check("(R2) numerical match exact = 5", close(ratio_sq_numerical, 5.0))

    # alpha_s-independence
    alpha_s_test = 0.05
    V_ub_sq_test = float(A_SQ) * (alpha_s_test/2) ** 3 * float(R_b_sq)
    V_td_sq_test = float(A_SQ) * (alpha_s_test/2) ** 3 * float(R_t_sq)
    ratio_test = V_td_sq_test / V_ub_sq_test
    print(f"  At alpha_s = 0.05: |V_td|^2/|V_ub|^2 = {ratio_test:.15f}")
    check("(R2) ratio is independent of alpha_s value",
          close(ratio_test, 5.0))


def audit_r3_cross_row_identity() -> None:
    banner("(R3) NEW: |V_td V_cb*|^2 / |V_ts V_ub*|^2 = 5 (cross-row)")

    # |V_td V_cb*|^2 = |V_td|^2 |V_cb|^2 = (5 alpha_s^3/72)(alpha_s^2/6) = 5 alpha_s^5/432
    # |V_ts V_ub*|^2 = |V_ts|^2 |V_ub|^2 = (alpha_s^2/6)(alpha_s^3/72) = alpha_s^5/432
    # Ratio = 5

    cross_row_num = V_td_sq() * V_cb_sq()
    cross_row_den = V_ts_sq() * V_ub_sq()
    ratio = cross_row_num / cross_row_den
    print(f"  |V_td V_cb|^2 = {cross_row_num:.6e}")
    print(f"  |V_ts V_ub|^2 = {cross_row_den:.6e}")
    print(f"  ratio          = {ratio:.15f}")

    check("(R3) ratio = 5 exactly", close(ratio, 5.0))
    check("(R3) ratio = R_t^2/R_b^2 = (1-rho)/rho",
          close(ratio, float((1 - RHO) / RHO)))

    # alpha_s-independence
    alpha_s_test = 0.20  # very different
    V_cb_t = float(A_SQ) * (alpha_s_test/2) ** 2
    V_ts_t = float(A_SQ) * (alpha_s_test/2) ** 2
    V_ub_t = float(A_SQ) * (alpha_s_test/2) ** 3 * float(RHO ** 2 + ETA_SQ)
    V_td_t = float(A_SQ) * (alpha_s_test/2) ** 3 * float((1-RHO) ** 2 + ETA_SQ)
    cross_row_t = (V_td_t * V_cb_t) / (V_ts_t * V_ub_t)
    print(f"  At alpha_s = 0.20: ratio = {cross_row_t:.15f}")
    check("(R3) alpha_s-independent (verified at alpha_s = 0.20)",
          close(cross_row_t, 5.0))

    print("  Note: this is the NEW pure-framework cross-row identity.")


def audit_alpha_s_dependent_contrast() -> None:
    banner("alpha_s-DEPENDENT contrast: ratios that DO depend on canonical coupling")

    # |V_us|^2 / |V_cb|^2 = (alpha_s/2) / (alpha_s^2/6) = 3/alpha_s
    ratio_us_cb = V_us_sq() / V_cb_sq()
    expected_ratio_us_cb = 3.0 / ALPHA_S_V
    print(f"  |V_us|^2 / |V_cb|^2 (numerical) = {ratio_us_cb:.6f}")
    print(f"  3 / alpha_s (closed form)        = {expected_ratio_us_cb:.6f}")
    check("|V_us|^2 / |V_cb|^2 = 3/alpha_s",
          close(ratio_us_cb, expected_ratio_us_cb))

    # |V_us|^2 / |V_ub|^2 = (alpha_s/2) / (alpha_s^3/72) = 36/alpha_s^2
    ratio_us_ub = V_us_sq() / V_ub_sq()
    expected_ratio_us_ub = 36.0 / ALPHA_S_V ** 2
    print(f"  |V_us|^2 / |V_ub|^2 (numerical) = {ratio_us_ub:.6f}")
    print(f"  36 / alpha_s^2 (closed form)     = {expected_ratio_us_ub:.6f}")
    check("|V_us|^2 / |V_ub|^2 = 36/alpha_s^2",
          close(ratio_us_ub, expected_ratio_us_ub))

    # |V_td|^2 / |V_cb|^2 = (5 alpha_s^3/72) / (alpha_s^2/6) = 5 alpha_s/12
    ratio_td_cb = V_td_sq() / V_cb_sq()
    expected_ratio_td_cb = 5.0 * ALPHA_S_V / 12.0
    print(f"  |V_td|^2 / |V_cb|^2 (numerical) = {ratio_td_cb:.6e}")
    print(f"  5 alpha_s/12 (closed form)       = {expected_ratio_td_cb:.6e}")
    check("|V_td|^2 / |V_cb|^2 = 5 alpha_s/12",
          close(ratio_td_cb, expected_ratio_td_cb))

    # Verify these vary with alpha_s
    alpha_s_test = 0.05
    ratio_us_cb_test = (alpha_s_test/2) / (alpha_s_test ** 2/6)
    print(f"  At alpha_s = 0.05: |V_us|^2/|V_cb|^2 = {ratio_us_cb_test:.6f} (DIFFERENT from canonical)")
    check("alpha_s-dependent ratios change with alpha_s (verified)",
          abs(ratio_us_cb_test - ratio_us_cb) > 1.0)


def audit_pdg_comparators() -> None:
    banner("PDG comparators for alpha_s-INDEPENDENT ratios")

    # (R1) |V_ts|/|V_cb|
    r1 = V_TS_PDG / V_CB_PDG
    r1_err = r1 * math.sqrt((V_TS_PDG_ERR/V_TS_PDG) ** 2 +
                            (V_CB_PDG_ERR/V_CB_PDG) ** 2)
    dev_r1 = (r1 - 1.0) / r1_err
    print(f"  (R1) |V_ts|/|V_cb| atlas = 1.0,  PDG = {r1:.4f} +/- {r1_err:.4f}")
    print(f"       deviation = {dev_r1:+.3f} sigma")
    check("(R1) |V_ts|/|V_cb| within 1 sigma of PDG", abs(dev_r1) < 1.0)

    # (R2) |V_td|/|V_ub|
    r2 = V_TD_PDG / V_UB_PDG
    r2_err = r2 * math.sqrt((V_TD_PDG_ERR/V_TD_PDG) ** 2 +
                            (V_UB_PDG_ERR/V_UB_PDG) ** 2)
    dev_r2 = (r2 - math.sqrt(5.0)) / r2_err
    print(f"  (R2) |V_td|/|V_ub| atlas = sqrt(5) = {math.sqrt(5):.4f},  "
          f"PDG = {r2:.4f} +/- {r2_err:.4f}")
    print(f"       deviation = {dev_r2:+.3f} sigma")
    check("(R2) |V_td|/|V_ub| within 1 sigma of PDG", abs(dev_r2) < 1.0)

    # (R3) cross-row
    cr_pdg = (V_TD_PDG * V_CB_PDG) ** 2 / (V_TS_PDG * V_UB_PDG) ** 2
    cr_err = cr_pdg * 2 * math.sqrt(
        (V_TD_PDG_ERR/V_TD_PDG) ** 2 + (V_CB_PDG_ERR/V_CB_PDG) ** 2 +
        (V_TS_PDG_ERR/V_TS_PDG) ** 2 + (V_UB_PDG_ERR/V_UB_PDG) ** 2)
    dev_r3 = (cr_pdg - 5.0) / cr_err
    print(f"  (R3) |V_td V_cb|^2/|V_ts V_ub|^2 atlas = 5.0,  "
          f"PDG = {cr_pdg:.4f} +/- {cr_err:.4f}")
    print(f"       deviation = {dev_r3:+.3f} sigma")
    check("(R3) cross-row identity within 1 sigma of PDG", abs(dev_r3) < 1.0)
    check("(R3) cross-row identity within 0.5 sigma of PDG", abs(dev_r3) < 0.5)


def audit_summary() -> None:
    banner("Summary: NEW alpha_s-INDEPENDENCE classification")

    print("  alpha_s-INDEPENDENT (geometric, Thales-pinned):")
    print()
    print("    (R1)  |V_ts| / |V_cb|              =  1")
    print("    (R2)  |V_td| / |V_ub|              =  sqrt(5)")
    print("    (R3)  |V_td V_cb|^2 / |V_ts V_ub|^2  =  5  (cross-row, NEW)")
    print()
    print("    Mechanism: cancellation of A^2 lambda^k factor;")
    print("               ratios depend ONLY on (rho, eta) at the atlas point")
    print("               and the Thales relation eta^2 = rho(1 - rho).")
    print()
    print("  alpha_s-DEPENDENT (dynamical):")
    print()
    print("    |V_us|^2 / |V_cb|^2   =  3 / alpha_s(v)")
    print("    |V_us|^2 / |V_ub|^2   =  36 / alpha_s(v)^2")
    print("    |V_td|^2 / |V_cb|^2   =  5 alpha_s(v) / 12")
    print()
    print("    These probe the canonical coupling itself.")
    print()
    print("  PDG comparators for the alpha_s-INDEPENDENT class:")
    print(f"    (R1) PDG: 0.993 +/- 0.042  match: -0.18 sigma")
    print(f"    (R2) PDG: 2.246 +/- 0.127  match: +0.08 sigma")
    print(f"    (R3) PDG: 5.12 +/- 0.72   match: +0.17 sigma")


def main() -> int:
    print("=" * 88)
    print("Thales-pinned alpha_s-independent CKM ratios theorem audit")
    print("See docs/CKM_THALES_PINNED_ALPHA_S_INDEPENDENT_RATIOS_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_r4_r_b_squared()
    audit_r5_ratio_R_t_R_b()
    audit_r1_vts_vcb_ratio()
    audit_r2_vtd_vub_ratio()
    audit_r3_cross_row_identity()
    audit_alpha_s_dependent_contrast()
    audit_pdg_comparators()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
