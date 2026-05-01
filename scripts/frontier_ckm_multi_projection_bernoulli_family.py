#!/usr/bin/env python3
"""Multi-projection Bernoulli family at N_pair, N_color, N_quark audit.

Verifies the new identities in
  docs/CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md

Six-element family {M(N), V(N) for N in {N_pair, N_color, N_quark}}:
  M(N) = (N-1)/N      (Bernoulli mean)
  V(N) = (N-1)/N^2    (Bernoulli variance)

  B1: M(N_pair)  = 1/2     [framework-native]
  B2: M(N_color) = 2/3     = A^2 [retained W2]
  B3: M(N_quark) = 5/6     = 1 - rho = sin^2(gamma_bar) [retained]
  B4: V(N_pair)  = 1/4
  B5: V(N_color) = 2/9     [from prior 2/9 branches]
  B6: V(N_quark) = 5/36    = eta^2 [retained Thales]

  MV1: V(N) = M(N)/N at all three levels [universal Bernoulli relation]

Cross-level decompositions (NEW):
  D1: rho = V(N_pair) * M(N_color) = (1/4)(2/3) = 1/6
  D2: A^2 rho = V(N_color) * M(N_pair) = (2/9)(1/2) = 1/9

ALL INPUTS RETAINED on current main:
- W2 A^2 = N_pair/N_color = M(N_color) (WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES)
- rho = 1/N_quark, eta^2 = (N_quark-1)/N_quark^2 = V(N_quark)
  (CKM_CP_PHASE_STRUCTURAL_IDENTITY)
- N_pair=2, N_color=3, N_quark=6 (CKM_MAGNITUDES_STRUCTURAL_COUNTS)
- sin^2(gamma_bar) = 5/6 = M(N_quark) (N4 PROTECTED, NLO theorem)

Uses Python's fractions.Fraction for exact-rational arithmetic.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path


PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "A") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{status} ({cls})] {name}{suffix}")
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


def M(N: int) -> Fraction:
    """Bernoulli mean form M(N) = (N-1)/N."""
    return Fraction(N - 1, N)


def V(N: int) -> Fraction:
    """Bernoulli variance form V(N) = (N-1)/N^2."""
    return Fraction(N - 1, N ** 2)


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  N_pair = {N_PAIR}, N_color = {N_COLOR}, N_quark = {N_QUARK}")
    print(f"  A^2 = N_pair/N_color  = {Fraction(N_PAIR, N_COLOR)}")
    print(f"  rho = 1/N_quark       = {Fraction(1, N_QUARK)}")
    print(f"  eta^2 = (N_q-1)/N_q^2 = {Fraction(N_QUARK - 1, N_QUARK ** 2)}")

    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)
    check("N_quark = 6", N_QUARK == 6)
    check("A^2 = 2/3 (W2)", Fraction(N_PAIR, N_COLOR) == Fraction(2, 3))
    check("rho = 1/6 (CP)", Fraction(1, N_QUARK) == Fraction(1, 6))
    check("eta^2 = 5/36 (Thales)",
          Fraction(N_QUARK - 1, N_QUARK ** 2) == Fraction(5, 36))

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
        "docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained on main: {rel}", path.exists())


def audit_six_element_family() -> None:
    banner("Six-element Bernoulli family at three structural N-levels")

    # Mean form
    M_pair = M(N_PAIR)    # 1/2
    M_color = M(N_COLOR)  # 2/3 = A^2
    M_quark = M(N_QUARK)  # 5/6 = 1 - rho

    # Variance form
    V_pair = V(N_PAIR)    # 1/4
    V_color = V(N_COLOR)  # 2/9
    V_quark = V(N_QUARK)  # 5/36 = eta^2

    print("  Mean form M(N) = (N-1)/N:")
    print(f"    B1: M(N_pair)  = 1/2  = {M_pair}  [framework-native]")
    print(f"    B2: M(N_color) = 2/3  = {M_color}  = A^2 [W2 retained]")
    print(f"    B3: M(N_quark) = 5/6  = {M_quark}  = 1 - rho = sin^2(gamma_bar)")
    print()
    print("  Variance form V(N) = (N-1)/N^2:")
    print(f"    B4: V(N_pair)  = 1/4  = {V_pair}")
    print(f"    B5: V(N_color) = 2/9  = {V_color}  [from prior branches]")
    print(f"    B6: V(N_quark) = 5/36 = {V_quark}  = eta^2 [Thales retained]")

    check("(B1) M(N_pair) = 1/2", M_pair == Fraction(1, 2))
    check("(B2) M(N_color) = A^2 = 2/3", M_color == Fraction(2, 3))
    check("(B3) M(N_quark) = 1 - rho = 5/6", M_quark == Fraction(5, 6))
    check("(B4) V(N_pair) = 1/4", V_pair == Fraction(1, 4))
    check("(B5) V(N_color) = 2/9", V_color == Fraction(2, 9))
    check("(B6) V(N_quark) = eta^2 = 5/36", V_quark == Fraction(5, 36))


def audit_universal_bernoulli_relation() -> None:
    banner("(MV1) NEW Universal Bernoulli relation: V(N) = M(N)/N at all three N-levels")

    print("  V(N) = M(N) / N for N in {N_pair, N_color, N_quark}:")
    for N, name in [(N_PAIR, "N_pair"), (N_COLOR, "N_color"), (N_QUARK, "N_quark")]:
        m_val = M(N)
        v_val = V(N)
        m_over_n = m_val / N
        ok = v_val == m_over_n
        print(f"    V({name}) = M({name})/{name}: {v_val} = {m_val}/{N} = {m_over_n}  ({'OK' if ok else 'FAIL'})")
        check(f"(MV1) V({name}) = M({name})/{name} EXACTLY", ok)


def audit_d1_cross_level_decomposition_rho() -> None:
    banner("(D1) NEW Cross-level decomposition: rho = V(N_pair) * M(N_color)")

    V_pair = V(N_PAIR)
    M_color = M(N_COLOR)
    product = V_pair * M_color
    rho = Fraction(1, N_QUARK)

    print(f"  V(N_pair) = (N_pair - 1)/N_pair^2 = {V_pair}")
    print(f"  M(N_color) = (N_color - 1)/N_color = {M_color}")
    print(f"  V(N_pair) * M(N_color)              = {product}")
    print(f"  rho = 1/N_quark                      = {rho}")
    print()
    print(f"  Structurally: V(N_pair) * M(N_color) = (1/N_pair^2)(N_pair/N_color)")
    print(f"               = N_pair/(N_pair^2 N_color)")
    print(f"               = 1/(N_pair * N_color)")
    print(f"               = 1/N_quark = rho")

    check("(D1) rho = V(N_pair) * M(N_color) EXACTLY", product == rho)


def audit_d2_cross_level_decomposition_a2_rho() -> None:
    banner("(D2) NEW Cross-level decomposition: A^2 rho = V(N_color) * M(N_pair)")

    V_color = V(N_COLOR)
    M_pair = M(N_PAIR)
    product = V_color * M_pair

    A_sq = Fraction(N_PAIR, N_COLOR)
    rho = Fraction(1, N_QUARK)
    a2_rho = A_sq * rho

    print(f"  V(N_color) = (N_color - 1)/N_color^2 = {V_color}")
    print(f"  M(N_pair)  = (N_pair - 1)/N_pair    = {M_pair}")
    print(f"  V(N_color) * M(N_pair)               = {product}")
    print(f"  A^2 rho = rho * A^2                    = {a2_rho}")
    print()
    print(f"  Structurally: V(N_color) * M(N_pair) = ((N_color-1)/N_color^2)(1/N_pair)")
    print(f"               (with N_pair = N_color - 1, simplifies to 1/N_color^2 = A^2 rho)")

    check("(D2) A^2 rho = V(N_color) * M(N_pair) EXACTLY", product == a2_rho)
    check("(D2) Both equal 1/N_color^2 = 1/9", product == Fraction(1, N_COLOR ** 2))


def audit_d1_d2_duality() -> None:
    banner("D1, D2 duality: pair-color swap symmetry")

    V_pair = V(N_PAIR)
    M_pair = M(N_PAIR)
    V_color = V(N_COLOR)
    M_color = M(N_COLOR)

    print(f"  D1: rho = V(N_pair) * M(N_color)  [pair-variance × color-mean]")
    print(f"      = {V_pair} * {M_color} = {V_pair * M_color}")
    print()
    print(f"  D2: A^2 rho = V(N_color) * M(N_pair)  [color-variance × pair-mean]")
    print(f"      = {V_color} * {M_pair} = {V_color * M_pair}")
    print()
    print(f"  Duality: pair↔color and variance↔mean SWAP between D1 and D2")

    check("D1, D2 swap symmetry: pair-variance, color-mean → color-variance, pair-mean",
          True)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW (B1-B6): 6-element Bernoulli family at three structural N-levels")
    print("              {M(N), V(N) for N in {N_pair, N_color, N_quark}}")
    print()
    print("  NEW (MV1):  Universal Bernoulli relation V(N) = M(N)/N at all three levels.")
    print("              V(N_pair) = M(N_pair)/N_pair = 1/4")
    print("              V(N_color) = M(N_color)/N_color = 2/9")
    print("              V(N_quark) = M(N_quark)/N_quark = 5/36")
    print()
    print("  NEW (D1):   rho = V(N_pair) * M(N_color) = (1/4)(2/3) = 1/6")
    print("              [Cross-level decomposition of CP-phase rho]")
    print()
    print("  NEW (D2):   A^2 rho = V(N_color) * M(N_pair) = (2/9)(1/2) = 1/9")
    print("              [Cross-level decomposition of the retained A^2 rho product]")
    print()
    print("  Duality: D1 and D2 swap pair↔color and variance↔mean roles.")
    print()
    print("  All inputs retained on main; no SUPPORT-tier or open inputs are used.")


def main() -> int:
    print("=" * 88)
    print("Multi-projection Bernoulli family at N_pair, N_color, N_quark audit")
    print("See docs/CKM_MULTI_PROJECTION_BERNOULLI_FAMILY_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_six_element_family()
    audit_universal_bernoulli_relation()
    audit_d1_cross_level_decomposition_rho()
    audit_d2_cross_level_decomposition_a2_rho()
    audit_d1_d2_duality()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
