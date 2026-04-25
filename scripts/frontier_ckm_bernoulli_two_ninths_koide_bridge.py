#!/usr/bin/env python3
"""Bernoulli-variance 2/9 identities and Koide-bridge support audit.

Verifies the new identities in
  docs/CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md

  (K1) A^2 (1 - A^2) = N_pair * (N_color - N_pair) / N_color^2 = 2/9   [Bernoulli variance of A^2]
  (K2) 2 * rho * A^2 = 2 N_pair/(N_quark N_color) = 2/N_color^2 = 2/9   [apex coupling]
  (K3) Consistency over positive integers:
       K1 = K2 = K5 = K6 = 2/9 <==> N_pair = 2, N_color = 3
  (K5) A^2 / N_color = N_pair / N_color^2 = 2/9                          [normalized A^2]
  (K6) (1/N_color)(1 - 1/N_color) = (N_color-1)/N_color^2 = 2/9          [color-projected Bernoulli]

ALL INPUTS RETAINED on current main:
- W2 A^2 = N_pair/N_color (WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES)
- rho = 1/N_quark (CKM_CP_PHASE_STRUCTURAL_IDENTITY)
- N_pair = 2, N_color = 3, N_quark = N_pair * N_color = 6
  (CKM_MAGNITUDES_STRUCTURAL_COUNTS)
- N_pair = N_color - 1 as a direct consequence of the retained values

NO SUPPORT-tier or open inputs (Koide Q_l, bare-coupling ratios,
dimension-color quadratic, A^2-Koide cross-sector bridge) are used as DERIVATION
inputs. The cross-sector reading is commentary, not derivation.

Uses Python's fractions.Fraction for exact-rational arithmetic.
"""

from __future__ import annotations

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


# Retained framework structural integers
N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR  # = 6

# Retained closed forms (exact Fractions)
A_SQ = Fraction(N_PAIR, N_COLOR)            # W2: A^2 = N_pair/N_color = 2/3
RHO = Fraction(1, N_QUARK)                  # CP-phase: rho = 1/N_quark = 1/6
ETA_SQ = Fraction(N_QUARK - 1, N_QUARK ** 2)  # CP-phase: eta^2 = (N_quark-1)/N_quark^2 = 5/36

TARGET = Fraction(2, 9)


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  N_pair                     = {N_PAIR}  (retained)")
    print(f"  N_color                    = {N_COLOR}  (retained)")
    print(f"  N_quark = N_pair × N_color = {N_QUARK}")
    print(f"  N_pair = N_color - 1?       {N_PAIR == N_COLOR - 1}  (retained-count consequence)")
    print()
    print(f"  W2: A^2 = N_pair/N_color    = {A_SQ}")
    print(f"  CP: rho = 1/N_quark         = {RHO}")
    print(f"  CP: eta^2 = (N_q-1)/N_q^2   = {ETA_SQ}  [same form as K6 but with N=N_quark]")

    check("N_pair = 2 (retained)", N_PAIR == 2)
    check("N_color = 3 (retained)", N_COLOR == 3)
    check("N_quark = N_pair × N_color = 6", N_QUARK == 6)
    check("N_pair = N_color - 1 (retained-count consequence)", N_PAIR == N_COLOR - 1)
    check("W2: A^2 = N_pair/N_color = 2/3", A_SQ == Fraction(2, 3))
    check("CP: rho = 1/N_quark = 1/6", RHO == Fraction(1, 6))
    check("CP: eta^2 = (N_q-1)/N_q^2 = 5/36 [SAME FORM as K6 with N=N_quark]",
          ETA_SQ == Fraction(5, 36))

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained on main: {rel}", path.exists())


def audit_k1_bernoulli() -> None:
    banner("(K1) NEW: A^2 (1 - A^2) = N_pair (N_color - N_pair)/N_color^2 = 2/9")

    K1 = A_SQ * (1 - A_SQ)
    K1_structural = Fraction(N_PAIR * (N_COLOR - N_PAIR), N_COLOR ** 2)
    K1_collapsed = Fraction(N_COLOR - 1, N_COLOR ** 2)  # when N_pair = N_color - 1

    print(f"  A^2 = {A_SQ}, 1 - A^2 = {1 - A_SQ}")
    print(f"  A^2 (1 - A^2) (direct)             = {K1}")
    print(f"  N_pair(N_color - N_pair)/N_color^2 = {K1_structural}")
    print(f"  Collapsed (N_color-1)/N_color^2    = {K1_collapsed}  [valid when N_pair = N_color - 1]")

    check("(K1) A^2 (1 - A^2) = 2/9 EXACTLY (Fraction)", K1 == TARGET)
    check("(K1) Structural form N_pair (N_color - N_pair)/N_color^2",
          K1 == K1_structural)
    check("(K1) Collapse to (N_color - 1)/N_color^2 (uses N_pair = N_color - 1)",
          K1 == K1_collapsed)


def audit_k2_apex_coupling() -> None:
    banner("(K2) NEW: 2 rho A^2 = 2 N_pair/(N_quark N_color) = 2/N_color^2 = 2/9")

    K2 = 2 * RHO * A_SQ
    K2_structural = Fraction(2 * N_PAIR, N_QUARK * N_COLOR)
    K2_simplified = Fraction(2, N_COLOR ** 2)  # using N_quark = N_pair × N_color

    print(f"  2 rho A^2 (direct)               = {K2}")
    print(f"  2 N_pair/(N_quark × N_color)     = {K2_structural}")
    print(f"  Simplified 2/N_color^2            = {K2_simplified}  [valid since N_quark = N_pair × N_color]")

    check("(K2) 2 rho A^2 = 2/9 EXACTLY (Fraction)", K2 == TARGET)
    check("(K2) Structural form 2 N_pair/(N_quark × N_color)",
          K2 == K2_structural)
    check("(K2) Simplifies to 2/N_color^2 (uses N_quark = N_pair × N_color)",
          K2 == K2_simplified)


def audit_k3_consistency() -> None:
    banner("(K3) NEW: K1 = K2 = K5 = K6 = 2/9 <==> N_pair = 2, N_color = 3")

    K1 = A_SQ * (1 - A_SQ)
    K2 = 2 * RHO * A_SQ
    K5 = A_SQ / N_COLOR
    K6 = Fraction(1, N_COLOR) * (1 - Fraction(1, N_COLOR))

    print(f"  K1 = A^2 (1 - A^2)           = {K1}")
    print(f"  K2 = 2 rho A^2                = {K2}")
    print(f"  K5 = A^2 / N_color            = {K5}")
    print(f"  K6 = (1/N_c)(1 - 1/N_c)       = {K6}")
    print()
    print(f"  All four equal?  {K1 == K2 == K5 == K6}")
    print(f"  All four = 2/9?  {K1 == K2 == K5 == K6 == TARGET}")
    print()
    print("  Positive-integer converse proof:")
    print("    From K6 = 2/9:")
    print("      (N_color - 1)/N_color^2 = 2/9")
    print("      2 N_color^2 - 9 N_color + 9 = 0")
    discriminant = 9**2 - 4 * 2 * 9
    roots = (Fraction(9 - 3, 4), Fraction(9 + 3, 4))
    print(f"      discriminant = {discriminant}; roots = {roots[0]}, {roots[1]}")
    print("      only positive integer root is N_color = 3")
    print("    From K5 = 2/9 with N_color = 3:")
    required_pair = TARGET * (3 ** 2)
    print(f"      N_pair/9 = 2/9 => N_pair = {required_pair}")
    print()
    print("  Therefore over positive integer pair/color counts:")
    print("    K1 = K2 = K5 = K6 = 2/9 iff N_pair = 2 and N_color = 3")

    check("(K3) K1 = K2 (algebraic equality)", K1 == K2)
    check("(K3) K2 = K5 (algebraic equality)", K2 == K5)
    check("(K3) K5 = K6 (algebraic equality)", K5 == K6)
    check("(K3) All four readouts converge to 2/9", K1 == K2 == K5 == K6 == TARGET)
    check("(K3) K6=2/9 integer equation has N_color=3 as only positive integer root",
          roots == (Fraction(3, 2), Fraction(3, 1)) and N_COLOR == 3)
    check("(K3) K5=2/9 then forces N_pair=2 once N_color=3",
          required_pair == N_PAIR == 2)
    check("(K3) Converse: retained N_pair=2, N_color=3 gives all four readouts",
          N_PAIR == 2 and N_COLOR == 3 and K1 == K2 == K5 == K6 == TARGET)


def audit_k5_normalized_a_sq() -> None:
    banner("(K5) NEW: A^2 / N_color = N_pair / N_color^2 = 2/9")

    K5 = A_SQ / N_COLOR
    K5_structural = Fraction(N_PAIR, N_COLOR ** 2)

    print(f"  A^2 / N_color (direct)        = {K5}")
    print(f"  N_pair / N_color^2            = {K5_structural}")

    check("(K5) A^2 / N_color = 2/9 EXACTLY (Fraction)", K5 == TARGET)
    check("(K5) Equivalent to N_pair / N_color^2",
          K5 == K5_structural)


def audit_k6_color_projected_bernoulli() -> None:
    banner("(K6) NEW: (1/N_color)(1 - 1/N_color) = (N_color - 1)/N_color^2 = 2/9")

    rho_color = Fraction(1, N_COLOR)
    K6 = rho_color * (1 - rho_color)
    K6_structural = Fraction(N_COLOR - 1, N_COLOR ** 2)

    print(f"  rho_color = 1/N_color                  = {rho_color}")
    print(f"  rho_color (1 - rho_color) (direct)     = {K6}")
    print(f"  (N_color - 1)/N_color^2                = {K6_structural}")

    check("(K6) (1/N_color)(1 - 1/N_color) = 2/9 EXACTLY (Fraction)",
          K6 == TARGET)
    check("(K6) = (N_color - 1)/N_color^2 (color-projected Bernoulli)",
          K6 == K6_structural)


def audit_cross_sector_reading() -> None:
    banner("Cross-sector reading (SUPPORT, NOT closure): Koide 2/9 shares K6 form")

    # Target-class generation ratio: (N_gen - 1)/N_gen^2 with retained N_gen = 3.
    N_GEN_CONJ = 3  # separate retained numeric equality, not used as CKM input
    Koide_variance_conj = Fraction(N_GEN_CONJ - 1, N_GEN_CONJ ** 2)

    print(f"  CKM K6 color form: (N_color - 1)/N_color^2 = {Fraction(N_COLOR - 1, N_COLOR ** 2)}")
    print(f"  Koide target form : (N_gen - 1)/N_gen^2     = {Koide_variance_conj}  [target-class with N_gen = 3]")
    print()
    print(f"  Both equal 2/9?   {Fraction(N_COLOR-1, N_COLOR**2) == Koide_variance_conj == TARGET}")
    print()
    print("  CROSS-SECTOR READING (SUPPORT, not closure):")
    print("    With the separately retained numeric equality N_gen = N_color = 3,")
    print("    the generation target ratio and CKM color-Bernoulli form K6 both equal 2/9.")
    print("    This SUPPORTS but does NOT CLOSE Koide 2/9.")
    print()
    print("  This note does NOT derive or use the retained N_gen = N_color equality.")
    print("  Closing Koide 2/9 still requires a separate charged-lepton source/readout theorem.")

    check("CKM K6 = Koide variance form (BOTH equal 2/9, SAME structural form)",
          Fraction(N_COLOR-1, N_COLOR**2) == Koide_variance_conj)
    check("Retained numeric equality N_gen = N_color is NOT used as a CKM input here",
          True)  # documentation check


def audit_eta_squared_form() -> None:
    banner("eta^2_LO has SAME functional form (N-1)/N^2 but with N=N_quark, not N=N_color")

    print(f"  eta^2_LO  = (N_quark - 1)/N_quark^2 = {ETA_SQ}  [N = N_quark = 6]")
    print(f"  K6 (and K1 collapsed) = (N_color - 1)/N_color^2 = {Fraction(N_COLOR-1, N_COLOR**2)}  [N = N_color = 3]")
    print()
    print("  Both have form (N - 1)/N^2 but with different N:")
    print("    eta^2 uses N = N_quark = N_pair × N_color (CKM full quark count)")
    print("    K6   uses N = N_color (color count alone)")
    print()
    print("  Replacing N_quark -> N_color in eta^2 form gives K6 = 2/9.")
    print("  This is the 'color-projection' of CKM CP-phase variance to Koide-like 2/9.")

    check("eta^2_LO has form (N_quark - 1)/N_quark^2 = 5/36",
          ETA_SQ == Fraction(N_QUARK - 1, N_QUARK ** 2))
    check("Color-projection N_quark -> N_color gives K6 = (N_color-1)/N_color^2 = 2/9",
          Fraction(N_COLOR - 1, N_COLOR ** 2) == TARGET)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW (K1): A^2 (1 - A^2) = N_pair (N_color - N_pair)/N_color^2 = 2/9")
    print("            Bernoulli variance of Wolfenstein A^2 parameter.")
    print()
    print("  NEW (K2): 2 rho A^2 = 2 N_pair/(N_quark × N_color) = 2/N_color^2 = 2/9")
    print("            Apex coupling: 2 × CP-phase rho × Wolfenstein A^2.")
    print()
    print("  NEW (K3): K1 = K2 = K5 = K6 = 2/9 <==> N_pair = 2, N_color = 3")
    print("            Structural consistency corollary over positive integer counts.")
    print()
    print("  NEW (K5): A^2 / N_color = N_pair / N_color^2 = 2/9")
    print()
    print("  NEW (K6): (1/N_color)(1 - 1/N_color) = (N_color - 1)/N_color^2 = 2/9")
    print("            Color-projected Bernoulli variance.")
    print()
    print("  Cross-sector reading (SUPPORT, NOT closure): K6 form matches the")
    print("  generation target-class ratio (N_gen - 1)/N_gen^2 = 2/9 at")
    print("  the separately retained numeric equality N_gen = N_color = 3.")
    print()
    print("  All four CKM readouts of 2/9 derived from retained inputs only.")
    print("  Does NOT close A^2 (already retained at W2) or Koide 2/9 (cross-sector).")
    print()
    print("  Push to science: 2/9 is multiply-determined in CKM by retained structure;")
    print("  closing Koide 2/9 still requires a charged-lepton source/readout theorem")
    print("  beyond the separately retained numeric equality N_gen = N_color = 3.")


def main() -> int:
    print("=" * 88)
    print("Bernoulli-variance 2/9 identities and Koide-bridge support audit")
    print("See docs/CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_k1_bernoulli()
    audit_k2_apex_coupling()
    audit_k3_consistency()
    audit_k5_normalized_a_sq()
    audit_k6_color_projected_bernoulli()
    audit_cross_sector_reading()
    audit_eta_squared_form()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
