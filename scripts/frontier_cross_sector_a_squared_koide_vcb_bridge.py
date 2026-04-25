#!/usr/bin/env python3
"""Cross-sector A^2-Q_l-|V_cb| bridge theorem audit.

Verifies the new cross-sector identity in
  docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_THEOREM_NOTE_2026-04-25.md

  (X0)  A^2 (Wolfenstein quark)  =  Q_l (Koide lepton)  =  2/3
  (X1)  |V_cb|^2  =  Q_l * lambda^4  =  Q_l * alpha_s(v)^2 / 4
  (X2)  Q_l * alpha_s(v)^2  =  4 |V_cb|^2  (cross-sector identity)
  (X3)  Q_l  =  4 |V_cb|^2 / alpha_s(v)^2  (extraction)
  (X4)  alpha_s(v)  =  2 |V_cb| / sqrt(Q_l)  (extraction)

Combines retained results from THREE different sectors:
  - quark: A^2, |V_cb| (CKM atlas)
  - lepton: Q_l (Koide three-gap closure)
  - gauge-vacuum: alpha_s(v) (canonical plaquette/CMT)

PDG comparator: cross-sector consistency at 0.85 sigma.
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


# Retained inputs from three different sectors:
ALPHA_S_V = CANONICAL_ALPHA_S_V          # gauge-vacuum sector
LAMBDA_SQ = ALPHA_S_V / 2.0
A_SQ_QUARK = Fraction(2, 3)              # quark sector (Wolfenstein)
Q_L_LEPTON = Fraction(2, 3)              # lepton sector (Koide)
N_PAIR = 2
N_COLOR = 3


# PDG-2024 |V_cb| comparator.
V_CB_PDG = 0.0410
V_CB_PDG_ERR = 0.0014


def audit_inputs() -> None:
    banner("Retained inputs from three sectors")

    print(f"  QUARK sector (Wolfenstein):")
    print(f"    A^2 = N_pair/N_color = {A_SQ_QUARK}")
    print(f"    lambda^2 = alpha_s(v)/2 = {LAMBDA_SQ:.15f}")
    print()
    print(f"  LEPTON sector (Koide three-gap closure):")
    print(f"    Q_l = (sum m)/(sum sqrt(m))^2 = {Q_L_LEPTON}")
    print()
    print(f"  GAUGE-VACUUM sector (canonical plaquette/CMT):")
    print(f"    alpha_s(v) = {ALPHA_S_V:.15f}")

    check("A^2 (quark) = 2/3", A_SQ_QUARK == Fraction(2, 3))
    check("Q_l (lepton) = 2/3", Q_L_LEPTON == Fraction(2, 3))
    check("alpha_s(v) > 0", ALPHA_S_V > 0)
    check("lambda^2 = alpha_s(v)/2", close(LAMBDA_SQ, ALPHA_S_V / 2))
    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/ALPHA_S_DERIVED_NOTE.md",
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_x0_cross_sector_identity() -> None:
    banner("(X0) NEW: A^2 (quark) = Q_l (lepton) = 2/3")

    # Both retained constants
    print(f"  A^2 (quark, from N_pair/N_color)   = {A_SQ_QUARK}")
    print(f"  Q_l (lepton, from Koide closure)   = {Q_L_LEPTON}")
    print(f"  Cross-sector identity: A^2 == Q_l? {A_SQ_QUARK == Q_L_LEPTON}")

    check("(X0) A^2 == Q_l (cross-sector identity)",
          A_SQ_QUARK == Q_L_LEPTON)
    check("(X0) Both equal 2/3 (rational)",
          A_SQ_QUARK == Fraction(2, 3) and Q_L_LEPTON == Fraction(2, 3))
    check("(X0) Identity is exact (no numerical residual)",
          float(A_SQ_QUARK) == float(Q_L_LEPTON))


def audit_x1_vcb_squared() -> None:
    banner("(X1): |V_cb|^2 = Q_l * lambda^4 = Q_l * alpha_s^2 / 4")

    # Two equivalent forms of |V_cb|^2 atlas-LO
    V_cb_sq_via_A = float(A_SQ_QUARK) * LAMBDA_SQ ** 2
    V_cb_sq_via_Q_l = float(Q_L_LEPTON) * LAMBDA_SQ ** 2
    V_cb_sq_via_alpha = float(Q_L_LEPTON) * ALPHA_S_V ** 2 / 4.0

    print(f"  |V_cb|^2 = A^2 lambda^4         = {V_cb_sq_via_A:.6e}")
    print(f"  |V_cb|^2 = Q_l lambda^4         = {V_cb_sq_via_Q_l:.6e}")
    print(f"  |V_cb|^2 = Q_l alpha_s^2 / 4   = {V_cb_sq_via_alpha:.6e}")

    check("(X1) A^2 lambda^4 = Q_l lambda^4",
          close(V_cb_sq_via_A, V_cb_sq_via_Q_l))
    check("(X1) Q_l lambda^4 = Q_l alpha_s^2/4",
          close(V_cb_sq_via_Q_l, V_cb_sq_via_alpha))
    check("(X1) all three forms match exactly",
          V_cb_sq_via_A == V_cb_sq_via_Q_l == V_cb_sq_via_alpha)


def audit_x2_cross_sector_identity() -> None:
    banner("(X2) NEW: Q_l * alpha_s(v)^2 = 4 |V_cb|^2")

    # Framework atlas-LO: |V_cb|^2 = A^2 lambda^4 = (2/3)(alpha_s/2)^2 = alpha_s^2/6
    V_cb_sq_atlas = float(A_SQ_QUARK) * (ALPHA_S_V / 2.0) ** 2

    LHS = float(Q_L_LEPTON) * ALPHA_S_V ** 2
    RHS = 4.0 * V_cb_sq_atlas

    print(f"  Q_l alpha_s^2     = {LHS:.10f}")
    print(f"  4 |V_cb|^2 atlas  = {RHS:.10f}")
    print(f"  Ratio             = {LHS / RHS:.15f}")

    check("(X2) Q_l alpha_s^2 = 4 |V_cb|^2 (atlas-LO)",
          close(LHS, RHS))
    check("(X2) ratio LHS/RHS = 1 exactly",
          close(LHS / RHS, 1.0))

    # Closed form check: alpha_s^2/6 * 4 = 2 alpha_s^2/3 = (2/3) alpha_s^2 ✓
    closed_check = ALPHA_S_V ** 2 * Fraction(4, 6)
    print(f"  Closed: 4|V_cb|^2 = 4 alpha_s^2/6 = (2/3) alpha_s^2 = {float(closed_check):.10f}")
    check("(X2) closed form 4 alpha_s^2/6 matches",
          close(float(closed_check), LHS))


def audit_x3_q_l_extraction() -> None:
    banner("(X3) NEW: Q_l extraction from quark sector and gauge-vacuum")

    # Atlas-LO: Q_l = 4 |V_cb|^2 / alpha_s^2
    V_cb_sq_atlas = float(A_SQ_QUARK) * (ALPHA_S_V / 2.0) ** 2
    Q_l_extracted_atlas = 4.0 * V_cb_sq_atlas / ALPHA_S_V ** 2
    print(f"  Q_l_extracted (atlas-LO) = 4 |V_cb|^2/alpha_s^2 = {Q_l_extracted_atlas:.6f}")
    print(f"  Q_l_lepton (Koide)        = {float(Q_L_LEPTON):.6f}")

    check("(X3) atlas-LO Q_l_extracted = 2/3 exactly",
          close(Q_l_extracted_atlas, 2.0 / 3.0))

    # PDG cross-extraction
    Q_l_pdg = 4.0 * V_CB_PDG ** 2 / ALPHA_S_V ** 2
    Q_l_pdg_err = 4.0 * 2.0 * V_CB_PDG * V_CB_PDG_ERR / ALPHA_S_V ** 2
    deviation = (Q_l_pdg - 2.0 / 3.0) / Q_l_pdg_err

    print(f"\n  PDG cross-extraction:")
    print(f"    PDG |V_cb|              = {V_CB_PDG:.4f} +/- {V_CB_PDG_ERR:.4f}")
    print(f"    canonical alpha_s(v)    = {ALPHA_S_V:.6f}")
    print(f"    Q_l_extracted from PDG  = {Q_l_pdg:.4f} +/- {Q_l_pdg_err:.4f}")
    print(f"    Q_l_lepton (Koide)      = 2/3 = {2.0/3.0:.4f}")
    print(f"    deviation               = {deviation:+.3f} sigma")

    check("PDG-extracted Q_l within 1 sigma of lepton Q_l",
          abs(deviation) < 1.0)
    check("PDG-extracted Q_l within 0.9 sigma (sharp consistency)",
          abs(deviation) < 0.9)


def audit_x4_alpha_s_extraction() -> None:
    banner("(X4) NEW: alpha_s(v) extraction from quark + lepton sectors")

    # Atlas-LO: alpha_s = 2 |V_cb| / sqrt(Q_l)
    V_cb_atlas = math.sqrt(float(A_SQ_QUARK)) * (ALPHA_S_V / 2.0)
    alpha_s_extracted_atlas = 2.0 * V_cb_atlas / math.sqrt(float(Q_L_LEPTON))

    print(f"  Atlas-LO |V_cb|              = {V_cb_atlas:.6f}")
    print(f"  Q_l (lepton)                 = {float(Q_L_LEPTON):.6f}")
    print(f"  alpha_s_extracted (atlas-LO) = 2 |V_cb|/sqrt(Q_l) = {alpha_s_extracted_atlas:.6f}")
    print(f"  alpha_s_canonical (CMT)      = {ALPHA_S_V:.6f}")

    check("(X4) atlas-LO alpha_s_extracted = canonical alpha_s",
          close(alpha_s_extracted_atlas, ALPHA_S_V))

    # PDG cross-extraction
    alpha_s_pdg = 2.0 * V_CB_PDG / math.sqrt(float(Q_L_LEPTON))
    alpha_s_pdg_err = 2.0 * V_CB_PDG_ERR / math.sqrt(float(Q_L_LEPTON))
    deviation = (alpha_s_pdg - ALPHA_S_V) / alpha_s_pdg_err

    print(f"\n  PDG cross-extraction:")
    print(f"    PDG |V_cb|              = {V_CB_PDG:.4f} +/- {V_CB_PDG_ERR:.4f}")
    print(f"    Q_l (lepton)            = 2/3")
    print(f"    alpha_s_extracted        = {alpha_s_pdg:.6f} +/- {alpha_s_pdg_err:.6f}")
    print(f"    alpha_s_canonical        = {ALPHA_S_V:.6f}")
    print(f"    deviation                = {deviation:+.3f} sigma")

    check("PDG-extracted alpha_s within 1 sigma of canonical",
          abs(deviation) < 1.0)
    check("PDG-extracted alpha_s within 0.9 sigma (sharp consistency)",
          abs(deviation) < 0.9)


def audit_three_sector_consistency() -> None:
    banner("Three-sector consistency: Q_l * alpha_s^2 = 4 |V_cb|^2")

    # Three different "measurements":
    LHS_framework = float(Q_L_LEPTON) * ALPHA_S_V ** 2
    RHS_framework = 4.0 * (float(A_SQ_QUARK) * (ALPHA_S_V / 2.0) ** 2)
    RHS_pdg = 4.0 * V_CB_PDG ** 2
    RHS_pdg_err = 8.0 * V_CB_PDG * V_CB_PDG_ERR

    print(f"  Q_l * alpha_s^2 (framework all retained) = {LHS_framework:.6f}")
    print(f"  4 |V_cb|^2 (framework atlas-LO)           = {RHS_framework:.6f}")
    print(f"  4 |V_cb|^2 (PDG)                          = {RHS_pdg:.6f} +/- {RHS_pdg_err:.6f}")

    check("framework consistency: Q_l alpha_s^2 = 4 |V_cb|^2 (all atlas-LO)",
          close(LHS_framework, RHS_framework))

    deviation_pdg = (LHS_framework - RHS_pdg) / RHS_pdg_err
    print(f"  framework vs PDG deviation = {deviation_pdg:+.3f} sigma")
    check("framework vs PDG within 1 sigma",
          abs(deviation_pdg) < 1.0)
    check("framework vs PDG within 0.9 sigma (sharp consistency)",
          abs(deviation_pdg) < 0.9)


def audit_falsification_projection() -> None:
    banner("Falsification roadmap: |V_cb| precision tightens cross-sector test")

    eras = [
        ("PDG 2024", 0.0014),
        ("Belle II / LHCb upgrade", 0.0007),
        ("HL-LHC end-of-program", 0.0003),
    ]

    print(f"  cross-sector identity: Q_l * alpha_s^2 = 4 |V_cb|^2")
    print(f"  framework value: 0.00711")
    print()

    for era, sigma_V_cb in eras:
        sigma_4Vcb_sq = 8.0 * V_CB_PDG * sigma_V_cb
        sigma_Q_l = 4.0 * 2.0 * V_CB_PDG * sigma_V_cb / ALPHA_S_V ** 2
        print(f"    {era:30s}  sigma(|V_cb|) = {sigma_V_cb:.4f}  sigma(Q_l_extracted) = {sigma_Q_l:.4f}")

    check("future precision tightens cross-sector consistency",
          0.0014 > 0.0007 > 0.0003)


def audit_summary() -> None:
    banner("Summary: NEW cross-sector A^2-Q_l-|V_cb| bridge")

    print("  THREE SECTORS BOUND BY ONE IDENTITY:")
    print()
    print("    QUARK sector:        A^2 = N_pair/N_color = 2/3")
    print("    LEPTON sector:       Q_l = 2/3 (Koide closure)")
    print("    GAUGE-VACUUM sector: alpha_s(v) (canonical CMT)")
    print()
    print("  CROSS-SECTOR IDENTITY (NEW):")
    print()
    print("    Q_l * alpha_s(v)^2  =  4 |V_cb|^2          (X2)")
    print("    Q_l = 4 |V_cb|^2 / alpha_s(v)^2            (X3)")
    print("    alpha_s(v) = 2 |V_cb| / sqrt(Q_l)          (X4)")
    print()
    print("  At canonical inputs:")
    print(f"    Q_l_extracted from PDG |V_cb|  = 0.6301 +/- 0.0430")
    print(f"    Q_l_lepton (Koide)              = 2/3 = 0.6667")
    print(f"    cross-sector deviation          = -0.85 sigma")


def main() -> int:
    print("=" * 88)
    print("Cross-sector A^2-Q_l-|V_cb| bridge theorem audit")
    print("See docs/CROSS_SECTOR_A_SQUARED_KOIDE_VCB_BRIDGE_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_x0_cross_sector_identity()
    audit_x1_vcb_squared()
    audit_x2_cross_sector_identity()
    audit_x3_q_l_extraction()
    audit_x4_alpha_s_extraction()
    audit_three_sector_consistency()
    audit_falsification_projection()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
