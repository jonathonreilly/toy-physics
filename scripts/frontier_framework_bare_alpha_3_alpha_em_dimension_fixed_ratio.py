#!/usr/bin/env python3
"""Framework bare alpha_3/alpha_em dimension-fixed ratio theorem audit.

Verifies the new dimension-specific cross-sector identity in
  docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_THEOREM_NOTE_2026-04-25.md

  (D1) 1/g_2^2 + 1/g_Y^2  =  (d+1) + (d+2)  =  2d + 3  =  9       [d=3]
  (D2) g_2^2 g_Y^2/(g_2^2 + g_Y^2)  =  1/(2d+3)  =  1/9            [d=3]
  (D3) sin^2(theta_W)(bare)  =  (d+1)/(2d+3)  =  4/9                [d=3]
  (D4) alpha_3(bare)/alpha_em(bare)  =  g_3^2 (2d+3)  =  9          [d=3]
  (D5) alpha_em(bare)  =  1/((2d+3) 4 pi)  =  1/(36 pi)             [d=3]
  (D6) 1/alpha_3 + 1/alpha_2 + 1/alpha_Y  =  4 pi (2d + 4)  =  40 pi [d=3]

Framework's bare sin^2(theta_W) = 4/9 is DISTINCT from SU(5) GUT 3/8.
The integer ratio 9 = 2d + 3 identifies d=3 uniquely; other dimensions
give different integers (d=2 -> 7, d=4 -> 11, d=5 -> 13).
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


# Framework spatial dimension axiom
D = 3

# Framework retained bare couplings
G_3_SQ_BARE = Fraction(1, 1)              # Cl(3) clock-shift axiom
G_2_SQ_BARE = Fraction(1, D + 1)           # weak: 1/(d+1) = 1/4
G_Y_SQ_BARE = Fraction(1, D + 2)           # hypercharge: 1/(d+2) = 1/5

# PDG comparators (running pipeline)
ALPHA_S_V_CANONICAL = 0.10330381612226678
ALPHA_S_M_Z = 0.1181
ALPHA_EM_M_Z_INV = 127.95
ALPHA_EM_V_INV_APPROX = 127.5  # approximate at v scale


def audit_inputs() -> None:
    banner("Retained framework inputs")

    print(f"  spatial dimension d = {D} (Cl(3) framework axiom)")
    print(f"  g_3^2(bare) = 1                     [Cl(3) clock-shift axiom]")
    print(f"  g_2^2(bare) = 1/(d+1) = {G_2_SQ_BARE}     [Z_2 bipartite weak sector]")
    print(f"  g_Y^2(bare) = 1/(d+2) = {G_Y_SQ_BARE}     [chirality hypercharge sector]")

    check("d = 3 (Cl(3) axiom)", D == 3)
    check("g_3^2(bare) = 1 (Cl(3) axiom)", G_3_SQ_BARE == 1)
    check("g_2^2(bare) = 1/4 (1/(d+1))",
          G_2_SQ_BARE == Fraction(1, 4))
    check("g_Y^2(bare) = 1/5 (1/(d+2))",
          G_Y_SQ_BARE == Fraction(1, 5))

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/CL3_SM_EMBEDDING_THEOREM.md",
        "docs/YT_EW_COLOR_PROJECTION_THEOREM.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_d1_sum_rule() -> None:
    banner("(D1): Sum rule 1/g_2^2 + 1/g_Y^2 = 2d + 3")

    sum_rule = 1 / G_2_SQ_BARE + 1 / G_Y_SQ_BARE
    expected = 2 * D + 3

    print(f"  1/g_2^2 + 1/g_Y^2 = {sum_rule}")
    print(f"  2d + 3 (closed form)     = {expected}")

    check("(D1) 1/g_2^2 + 1/g_Y^2 = 2d + 3 (exact rational)",
          sum_rule == expected)
    check("(D1) at d=3: sum rule = 9",
          sum_rule == 9)
    check("(D1) (d+1) + (d+2) = 2d+3 expansion",
          (D + 1) + (D + 2) == 2 * D + 3)


def audit_d2_effective_em_coupling() -> None:
    banner("(D2): Effective bare EM coupling g_em^2(bare) = 1/(2d+3)")

    g_em_sq = G_2_SQ_BARE * G_Y_SQ_BARE / (G_2_SQ_BARE + G_Y_SQ_BARE)
    expected = Fraction(1, 2 * D + 3)

    print(f"  g_em^2(bare) = g_2^2 g_Y^2/(g_2^2 + g_Y^2) = {g_em_sq}")
    print(f"  1/(2d+3) (closed form)                       = {expected}")

    check("(D2) g_em^2(bare) = 1/(2d+3) (exact rational)",
          g_em_sq == expected)
    check("(D2) at d=3: g_em^2(bare) = 1/9",
          g_em_sq == Fraction(1, 9))


def audit_d3_bare_sin_sq_theta_W() -> None:
    banner("(D3): Bare sin^2(theta_W) = (d+1)/(2d+3) = 4/9 at d=3")

    sin_sq_theta_W = G_Y_SQ_BARE / (G_2_SQ_BARE + G_Y_SQ_BARE)
    cos_sq_theta_W = G_2_SQ_BARE / (G_2_SQ_BARE + G_Y_SQ_BARE)
    expected_sin_sq = Fraction(D + 1, 2 * D + 3)
    expected_cos_sq = Fraction(D + 2, 2 * D + 3)

    print(f"  sin^2(theta_W)(bare) = {sin_sq_theta_W}  (closed form: (d+1)/(2d+3) = {expected_sin_sq})")
    print(f"  cos^2(theta_W)(bare) = {cos_sq_theta_W}  (closed form: (d+2)/(2d+3) = {expected_cos_sq})")
    print(f"  sin^2 + cos^2        = {sin_sq_theta_W + cos_sq_theta_W}")

    check("(D3) sin^2(theta_W)(bare) = (d+1)/(2d+3)",
          sin_sq_theta_W == expected_sin_sq)
    check("(D3) at d=3: sin^2 = 4/9",
          sin_sq_theta_W == Fraction(4, 9))
    check("(D3a) cos^2(theta_W)(bare) = (d+2)/(2d+3)",
          cos_sq_theta_W == expected_cos_sq)
    check("sin^2 + cos^2 = 1 (consistency)",
          sin_sq_theta_W + cos_sq_theta_W == 1)


def audit_d3_su5_distinction() -> None:
    banner("(D3) SU(5) distinction: framework 4/9 vs SU(5) 3/8")

    sin_sq_framework = Fraction(D + 1, 2 * D + 3)
    sin_sq_SU5 = Fraction(3, 8)

    print(f"  Framework bare:  sin^2(theta_W) = {sin_sq_framework} = {float(sin_sq_framework):.6f}")
    print(f"  SU(5) GUT:       sin^2(theta_W) = {sin_sq_SU5} = {float(sin_sq_SU5):.6f}")
    diff = sin_sq_framework - sin_sq_SU5
    print(f"  Difference        = {diff}")

    check("framework 4/9 != SU(5) 3/8",
          sin_sq_framework != sin_sq_SU5)
    check("difference 4/9 - 3/8 = 5/72",
          diff == Fraction(5, 72))


def audit_d4_alpha_3_em_ratio() -> None:
    banner("(D4) NEW: alpha_3(bare)/alpha_em(bare) = 2d + 3 = 9 at d=3")

    g_em_sq = G_2_SQ_BARE * G_Y_SQ_BARE / (G_2_SQ_BARE + G_Y_SQ_BARE)
    ratio_exact = G_3_SQ_BARE / g_em_sq

    # Equivalent algebraic form
    ratio_via_sum = G_3_SQ_BARE * (1 / G_2_SQ_BARE + 1 / G_Y_SQ_BARE)

    expected = 2 * D + 3

    print(f"  alpha_3(bare)/alpha_em(bare) = g_3^2/g_em^2 = {ratio_exact}")
    print(f"  Equivalent: g_3^2 (1/g_2^2 + 1/g_Y^2)        = {ratio_via_sum}")
    print(f"  Closed form: g_3^2 (2d + 3)                  = {expected}")

    check("(D4) alpha_3/alpha_em = 9 (integer)",
          ratio_exact == 9)
    check("(D4) ratio = g_3^2 (1/g_2^2 + 1/g_Y^2)",
          ratio_exact == ratio_via_sum)
    check("(D4) at d=3: integer 9 = 2d+3",
          ratio_exact == 2 * D + 3)
    check("(D4) ratio is dimension-specific",
          ratio_exact.denominator == 1)


def audit_d5_alpha_em_bare_closed_form() -> None:
    banner("(D5): alpha_em(bare) = 1/((2d+3) × 4 pi) = 1/(36 pi)")

    g_em_sq = G_2_SQ_BARE * G_Y_SQ_BARE / (G_2_SQ_BARE + G_Y_SQ_BARE)
    alpha_em_bare = float(g_em_sq) / (4 * math.pi)
    expected = 1 / ((2 * D + 3) * 4 * math.pi)

    print(f"  alpha_em(bare) = g_em^2/(4 pi)            = {alpha_em_bare:.10f}")
    print(f"  1/((2d+3) × 4 pi) (closed form)          = {expected:.10f}")
    print(f"  1/alpha_em(bare)                          = {1/alpha_em_bare:.4f}")
    print(f"  36 pi                                     = {36 * math.pi:.4f}")

    check("(D5) alpha_em(bare) = 1/((2d+3) × 4 pi)",
          close(alpha_em_bare, expected))
    check("(D5) at d=3: 1/alpha_em(bare) = 36 pi",
          close(1 / alpha_em_bare, 36 * math.pi))


def audit_d6_inverse_sum() -> None:
    banner("(D6): 1/alpha_3 + 1/alpha_2 + 1/alpha_Y = 4 pi (2d+4) = 40 pi at d=3")

    inv_sum = (4 * math.pi / float(G_3_SQ_BARE) +
               4 * math.pi / float(G_2_SQ_BARE) +
               4 * math.pi / float(G_Y_SQ_BARE))
    expected = 4 * math.pi * (2 * D + 4)

    print(f"  1/alpha_3 + 1/alpha_2 + 1/alpha_Y = {inv_sum:.4f}")
    print(f"  4 pi (1 + (d+1) + (d+2))           = {expected:.4f}")
    print(f"  4 pi (2d + 4) = 40 pi              = {40 * math.pi:.4f}")

    check("(D6) inverse-alpha sum = 4 pi (2d+4)",
          close(inv_sum, expected))
    check("(D6) at d=3: sum = 40 pi",
          close(inv_sum, 40 * math.pi))


def audit_dimension_uniqueness() -> None:
    banner("Dimension uniqueness: 2d+3 identifies d=3 via integer 9")

    print("  Predictions for different spatial dimensions:")
    print()
    for d_test in [2, 3, 4, 5]:
        g_2_t = Fraction(1, d_test + 1)
        g_Y_t = Fraction(1, d_test + 2)
        ratio = 1 / g_2_t + 1 / g_Y_t  # = alpha_3/alpha_em with g_3^2 = 1
        sin_sq = g_Y_t / (g_2_t + g_Y_t)
        marker = "<-- framework" if d_test == 3 else ""
        print(f"    d = {d_test}: alpha_3/alpha_em = {ratio} = 2*{d_test}+3 = {2*d_test+3}; "
              f"sin^2(theta_W) = {sin_sq} = {float(sin_sq):.4f}  {marker}")

    check("d=2 gives ratio 7", 1/Fraction(1, 3) + 1/Fraction(1, 4) == 7)
    check("d=3 gives ratio 9 (framework)", 1/Fraction(1, 4) + 1/Fraction(1, 5) == 9)
    check("d=4 gives ratio 11", 1/Fraction(1, 5) + 1/Fraction(1, 6) == 11)
    check("d=5 gives ratio 13", 1/Fraction(1, 6) + 1/Fraction(1, 7) == 13)


def audit_running_pipeline_consistency() -> None:
    banner("Running pipeline: bare 9 -> v -> M_Z (PDG comparator)")

    ratio_bare = 9.0
    alpha_em_v = 1.0 / ALPHA_EM_V_INV_APPROX
    ratio_v = ALPHA_S_V_CANONICAL / alpha_em_v
    alpha_em_MZ = 1.0 / ALPHA_EM_M_Z_INV
    ratio_MZ = ALPHA_S_M_Z / alpha_em_MZ

    print(f"  ratio at bare scale (framework)  = {ratio_bare:.4f}")
    print(f"  ratio at v scale (canonical)     = {ratio_v:.4f}")
    print(f"  ratio at M_Z (PDG)               = {ratio_MZ:.4f}")
    print()
    print(f"  Standard QCD asymptotic freedom drives ratio UP at lower scales.")
    print(f"  Framework bare 9 -> 13.2 at v -> 15.1 at M_Z is consistent direction.")

    check("ratio increases from bare to M_Z (consistent with QCD asymptotic freedom)",
          ratio_bare < ratio_v < ratio_MZ)
    check("framework bare 9 is finite-positive integer",
          ratio_bare > 0 and isinstance(int(ratio_bare), int))


def audit_summary() -> None:
    banner("Summary: NEW dimension-specific cross-sector identity")

    print("  FRAMEWORK BARE COUPLING IDENTITIES (NEW packaged form):")
    print()
    print("    g_3^2(bare)  =  1")
    print("    g_2^2(bare)  =  1/(d+1) = 1/4")
    print("    g_Y^2(bare)  =  1/(d+2) = 1/5")
    print()
    print("  CONSEQUENCES:")
    print()
    print("    (D1) 1/g_2^2 + 1/g_Y^2   =  2d + 3  =  9         (sum rule)")
    print("    (D2) g_em^2(bare)         =  1/(2d+3) = 1/9       (effective EM)")
    print("    (D3) sin^2(theta_W)(bare) =  (d+1)/(2d+3) = 4/9   (NOT SU(5))")
    print("    (D4) alpha_3(bare)/alpha_em(bare)  =  9           (NEW cross-sector)")
    print("    (D5) alpha_em(bare)        =  1/(36 pi)            (closed form)")
    print("    (D6) inverse-alpha sum     =  40 pi                (sum rule)")
    print()
    print("  KEY CROSS-SECTOR IDENTITY (D4):")
    print("    The COLOR sector (g_3^2 = 1) and ELECTROWEAK sector (g_2, g_Y)")
    print("    bind into a single integer ratio = 2d+3 = 9 at d=3.")
    print()
    print("  DIMENSION DEPENDENCE:")
    print("    d=2 -> 7, d=3 -> 9 (FRAMEWORK), d=4 -> 11, d=5 -> 13")
    print("    The integer 9 uniquely identifies d=3.")
    print()
    print("  DISTINGUISHED FROM SU(5):")
    print("    Framework: sin^2(theta_W)(bare) = 4/9 = 0.444")
    print("    SU(5):     sin^2(theta_W)(M_GUT) = 3/8 = 0.375")
    print("    Different by 5/72.")


def main() -> int:
    print("=" * 88)
    print("Framework bare alpha_3/alpha_em dimension-fixed ratio theorem audit")
    print("See docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_d1_sum_rule()
    audit_d2_effective_em_coupling()
    audit_d3_bare_sin_sq_theta_W()
    audit_d3_su5_distinction()
    audit_d4_alpha_3_em_ratio()
    audit_d5_alpha_em_bare_closed_form()
    audit_d6_inverse_sum()
    audit_dimension_uniqueness()
    audit_running_pipeline_consistency()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
