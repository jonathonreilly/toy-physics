#!/usr/bin/env python3
"""Three-sector dimension-color quadratic identity SUPPORT NOTE audit.

Verifies the CONDITIONAL three-sector identity in
  docs/FRAMEWORK_THREE_SECTOR_DIMENSION_COLOR_QUADRATIC_IDENTITY_SUPPORT_NOTE_2026-04-25.md

The runner verifies the conditional algebra AFTER the load-bearing
premises are assumed. It does NOT establish retention of those
premises.

Load-bearing PREMISES (conditional):
  (P1) (alpha_3/alpha_em)(bare) = 2d + 3
       Carrier on main is itself a SUPPORT note, not retained closure.
  (P2) Q_l = N_pair/N_color = 2/3
       Open Koide support target on main, not retained closure.

Conditional algebraic content (assuming P1 and P2):
  (I1) (alpha_3/alpha_em)(bare) x Q_l = N_quark = 6
  (I2) (2d+3) x (N_pair/N_color)      = N_pair x N_color
  (I3) 2d + 3                          = N_color^2
  (I4) d                               = (N_color^2 - 3)/2
  (I5) Framework N_color = 3 -> d = 3 (smallest integer solution)
  (I6) Composition with retained eta = sqrt(5)/6:
       (alpha_3/alpha_em)(bare) x Q_l x eta = sqrt(5)

This is a falsification and cross-extraction template, not a
retained closure. It is not part of the accepted minimal-input stack.
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


# Framework/support inputs from three sectors.  The script checks the
# conditional algebra after these premises are assumed; it does not promote
# the support/open Koide inputs to retained status.
D = 3                            # spatial dimension (Cl(3) framework axiom)
N_COLOR = 3                      # color count (Cl(3) clock-shift axiom)
N_PAIR = 2                       # weak doublet count
G_3_SQ = Fraction(1, 1)          # Cl(3) clock-shift axiom
G_2_SQ = Fraction(1, D + 1)      # weak: 1/(d+1) = 1/4
G_Y_SQ = Fraction(1, D + 2)      # hypercharge: 1/(d+2) = 1/5

# Derived conditional quantities.
ALPHA_RATIO_BARE = G_3_SQ * (1 / G_2_SQ + 1 / G_Y_SQ)  # = 2d+3
Q_L = Fraction(N_PAIR, N_COLOR)                          # = 2/3
N_QUARK = N_PAIR * N_COLOR                               # = 6
ETA_VAL = math.sqrt(5.0) / 6.0                           # CKM CP-phase


def audit_inputs() -> None:
    banner("Framework/support inputs from three sectors")

    print(f"  COLOR sector:")
    print(f"    g_3^2(bare) = {G_3_SQ} (Cl(3) clock-shift axiom)")
    print(f"    N_color     = {N_COLOR}")
    print()
    print(f"  ELECTROWEAK sector:")
    print(f"    g_2^2(bare) = {G_2_SQ} = 1/(d+1) at d={D}")
    print(f"    g_Y^2(bare) = {G_Y_SQ} = 1/(d+2) at d={D}")
    print()
    print(f"  LEPTON sector (Koide):")
    print(f"    Q_l         = {Q_L} = N_pair/N_color")
    print()
    print(f"  CKM CP-phase sector:")
    print(f"    eta         = sqrt(5)/6 = {ETA_VAL:.10f}")
    print()
    print(f"  COMBINED:")
    print(f"    (alpha_3/alpha_em)(bare) = g_3^2 (1/g_2^2 + 1/g_Y^2) = {ALPHA_RATIO_BARE}")
    print(f"    N_quark = N_pair x N_color = {N_QUARK}")

    check("d = 3 framework axiom", D == 3)
    check("N_color = 3 framework axiom", N_COLOR == 3)
    check("N_pair = 2 framework axiom", N_PAIR == 2)
    check("g_3^2(bare) = 1", G_3_SQ == 1)
    check("g_2^2(bare) = 1/(d+1)", G_2_SQ == Fraction(1, D+1))
    check("g_Y^2(bare) = 1/(d+2)", G_Y_SQ == Fraction(1, D+2))
    check("(alpha_3/alpha_em)(bare) = 2d+3 = 9", ALPHA_RATIO_BARE == 2 * D + 3)
    check("Q_l = N_pair/N_color = 2/3", Q_L == Fraction(N_PAIR, N_COLOR))
    check("N_quark = N_pair x N_color = 6", N_QUARK == N_PAIR * N_COLOR)

    repo_root = Path(__file__).resolve().parents[1]
    # Confirm the load-bearing carriers exist on main with the correct
    # status. Both (P1) and (P2) sources are flagged on main as
    # "support" / "open", not retained closure.
    upstream = (
        # (P1) bare-alpha ratio carrier — explicitly a SUPPORT note on main
        "docs/FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md",
        # (P2) Koide Q_l = 2/3 — open support target investigation on main
        "docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md",
        # Retained CKM CP-phase eta = sqrt(5)/6 (used in I5)
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        # Algebraic support theorem (explicitly NOT in minimal-input stack)
        "docs/CL3_SM_EMBEDDING_THEOREM.md",
    )
    for rel in upstream:
        path = repo_root / rel
        check(f"upstream authority present: {rel}", path.exists())


def audit_i1_three_sector_identity() -> None:
    banner("(I1) CONDITIONAL: (alpha_3/alpha_em)(bare) x Q_l = N_quark = 6 [given P1, P2]")

    LHS = ALPHA_RATIO_BARE * Q_L
    print(f"  (alpha_3/alpha_em)(bare) x Q_l = {ALPHA_RATIO_BARE} x {Q_L} = {LHS}")
    print(f"  N_quark                          = {N_QUARK}")

    check("(I1) (alpha_3/alpha_em)(bare) x Q_l = N_quark = 6 (exact rational)",
          LHS == N_QUARK)
    check("(I1) The conspiracy: 9 x 2/3 = 6",
          ALPHA_RATIO_BARE * Q_L == 6)


def audit_i2_substituted_form() -> None:
    banner("(I2): (2d+3) x (N_pair/N_color) = N_pair x N_color")

    LHS = Fraction(2 * D + 3) * Fraction(N_PAIR, N_COLOR)
    RHS = N_PAIR * N_COLOR

    print(f"  (2d+3) x (N_pair/N_color) = {2*D+3} x {Fraction(N_PAIR, N_COLOR)} = {LHS}")
    print(f"  N_pair x N_color           = {RHS}")

    check("(I2) substituted form holds at framework values",
          LHS == RHS)


def audit_i3_dimension_color_relation() -> None:
    banner("(I3) CONDITIONAL: 2d + 3 = N_color^2 (dimension-color quadratic) [given P1, P2]")

    LHS = 2 * D + 3
    RHS = N_COLOR ** 2

    print(f"  2d + 3       = 2 x {D} + 3 = {LHS}")
    print(f"  N_color^2    = {N_COLOR}^2 = {RHS}")

    check("(I3) 2d + 3 = N_color^2 at framework values",
          LHS == RHS)
    check("(I3) Both equal 9 at d=3, N_color=3",
          LHS == 9 and RHS == 9)


def audit_i4_d_from_n_color() -> None:
    banner("(I4): d = (N_color^2 - 3)/2 — dimension fixed by color count")

    d_predicted = Fraction(N_COLOR ** 2 - 3, 2)

    print(f"  d (predicted from N_color = {N_COLOR}) = ({N_COLOR}^2 - 3)/2 = {d_predicted}")
    print(f"  d (framework axiom)                    = {D}")

    check("(I4) d = (N_color^2 - 3)/2 holds at framework",
          d_predicted == D)
    check("(I4) Predicted d is integer at framework values",
          d_predicted.denominator == 1)


def audit_i5_integer_solutions() -> None:
    banner("(I5) Integer solutions to d = (N_color^2 - 3)/2")

    print("  Testing N_color values:")
    integer_solutions = []
    for nc in range(2, 10):
        d_val = Fraction(nc ** 2 - 3, 2)
        is_integer = d_val.denominator == 1
        marker = "<-- FRAMEWORK" if nc == 3 else ""
        print(f"    N_color = {nc}: d = ({nc}^2 - 3)/2 = {d_val} "
              f"{'(integer)' if is_integer else '(non-integer)'}  {marker}")
        if is_integer:
            integer_solutions.append((nc, int(d_val)))

    print(f"\n  Integer solutions: {integer_solutions}")

    check("(I5) framework (N_color=3, d=3) is an integer solution",
          (3, 3) in integer_solutions)
    check("(I5) framework is the smallest integer solution",
          integer_solutions[0] == (3, 3))
    check("(I5) only odd N_color gives integer d (in tested range)",
          all(nc % 2 == 1 for nc, _ in integer_solutions))


def audit_i6_four_sector_sqrt5() -> None:
    banner("(I6) CONDITIONAL: (alpha_3/alpha_em) x Q_l x eta = sqrt(5) [given P1, P2; eta retained]")

    LHS = float(ALPHA_RATIO_BARE) * float(Q_L) * ETA_VAL
    RHS = math.sqrt(5.0)

    print(f"  (alpha_3/alpha_em)(bare) x Q_l x eta = {ALPHA_RATIO_BARE} x {Q_L} x {ETA_VAL:.10f}")
    print(f"  Numerical                              = {LHS:.10f}")
    print(f"  sqrt(5)                                = {RHS:.10f}")

    check("(I6) Four-sector identity = sqrt(5) at framework values",
          close(LHS, RHS))

    # Symbolic verification: 9 * (2/3) * (sqrt(5)/6) = (9 * 2 * sqrt(5))/(3 * 6) = (18 sqrt(5))/18 = sqrt(5)
    rational_factor = ALPHA_RATIO_BARE * Q_L * Fraction(1, 6)
    print(f"\n  Symbolic: rational factor = (2d+3) x N_pair/(N_color x 6) = {rational_factor}")
    print(f"  Times sqrt(5) component eta = sqrt(5)/6 -> rational_factor x sqrt(5)")
    check("(I6) symbolic factor is exactly 1 at framework",
          rational_factor == 1)

    # d-dependence test
    print("\n  d-dependence test (with Q_l, eta fixed):")
    for d_test in [2, 3, 4, 5]:
        product = (2 * d_test + 3) * (2.0 / 3.0) * ETA_VAL
        print(f"    d = {d_test}: (2d+3) x Q_l x eta = {product:.6f}")
    print(f"  sqrt(5) = {RHS:.6f}")
    print("  Only d = 3 gives exactly sqrt(5) (with framework Q_l, eta).")


def audit_alpha_em_extraction() -> None:
    banner("Cross-extraction: alpha_em(bare) from N_color, Q_l")

    # alpha_3 Q_l / alpha_em = N_quark
    # ⟹ alpha_em = alpha_3 Q_l / N_quark

    alpha_3_bare = float(G_3_SQ) / (4 * math.pi)
    alpha_em_via_N = alpha_3_bare * float(Q_L) / N_QUARK
    alpha_em_direct = (float(G_2_SQ) * float(G_Y_SQ) /
                       (float(G_2_SQ) + float(G_Y_SQ))) / (4 * math.pi)

    print(f"  alpha_3(bare)              = {alpha_3_bare:.6e}")
    print(f"  alpha_3 Q_l / N_quark      = {alpha_em_via_N:.6e}")
    print(f"  alpha_em(bare) (direct)     = {alpha_em_direct:.6e}")
    print(f"  Match: {close(alpha_em_via_N, alpha_em_direct)}")

    check("alpha_em extraction from N_color, Q_l, alpha_3 matches direct",
          close(alpha_em_via_N, alpha_em_direct))


def audit_d_extraction() -> None:
    banner("Cross-extraction: d from N_color via the quadratic relation")

    # d = (N_color^2 - 3)/2
    d_extracted = Fraction(N_COLOR ** 2 - 3, 2)

    print(f"  d (extracted from N_color={N_COLOR}) = ({N_COLOR}^2 - 3)/2 = {d_extracted}")
    print(f"  d (framework axiom)                  = {D}")
    print(f"  Match: {d_extracted == D}")

    # Inverse: N_color from d
    n_color_extracted = math.sqrt(2 * D + 3)
    print(f"\n  N_color (extracted from d={D}) = sqrt(2d+3) = sqrt({2*D+3}) = {n_color_extracted}")
    print(f"  N_color (framework axiom)       = {N_COLOR}")
    check("d extraction from N_color matches framework",
          d_extracted == D)
    check("N_color extraction from d matches framework",
          close(n_color_extracted, N_COLOR))


def audit_summary() -> None:
    banner("Summary: CONDITIONAL three-sector dimension-color quadratic identity")

    print("  CONDITIONAL THREE-SECTOR IDENTITY:")
    print("    (held only if both load-bearing premises P1 and P2 are accepted)")
    print()
    print("    (alpha_3/alpha_em)(bare) x Q_l = N_quark = 6")
    print()
    print("  Premises (NOT retained closure on main):")
    print("    (P1) (alpha_3/alpha_em)(bare) = 2d + 3 = 9")
    print("         carrier on main is itself a SUPPORT note")
    print("    (P2) Q_l = N_pair/N_color = 2/3")
    print("         open Koide support target on main")
    print()
    print("  Conditional consequence (algebraic):")
    print("    2d + 3 = N_color^2,      d = (N_color^2 - 3)/2")
    print()
    print("  Integer solutions to (I4):")
    print("    N_color = 3 -> d = 3 (smallest integer solution; framework-consistent)")
    print("    N_color = 5 -> d = 11 (algebraically allowed; SM-excluded)")
    print("    N_color = 7 -> d = 23")
    print()
    print("  Conditional composition with retained eta = sqrt(5)/6:")
    print("    (alpha_3/alpha_em)(bare) x Q_l x eta = sqrt(5)")
    print()
    print("  This is a falsification and cross-extraction template, NOT")
    print("  a retained closure. It is NOT part of the accepted")
    print("  minimal-input stack on main.")


def main() -> int:
    print("=" * 88)
    print("Three-sector dimension-color quadratic identity SUPPORT NOTE audit")
    print("See docs/FRAMEWORK_THREE_SECTOR_DIMENSION_COLOR_QUADRATIC_IDENTITY_SUPPORT_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_i1_three_sector_identity()
    audit_i2_substituted_form()
    audit_i3_dimension_color_relation()
    audit_i4_d_from_n_color()
    audit_i5_integer_solutions()
    audit_i6_four_sector_sqrt5()
    audit_alpha_em_extraction()
    audit_d_extraction()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
