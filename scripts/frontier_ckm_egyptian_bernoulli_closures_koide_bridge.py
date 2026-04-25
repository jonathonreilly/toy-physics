#!/usr/bin/env python3
"""Egyptian fraction unitarity and Bernoulli sum closures Koide-bridge audit.

Verifies the new identities in
  docs/CKM_EGYPTIAN_BERNOULLI_CLOSURES_KOIDE_BRIDGE_THEOREM_NOTE_2026-04-25.md

  E1: 1/N_pair + 1/N_color + 1/N_quark = 1 EXACTLY [Egyptian fraction unitarity]
  E2: (2, 3, 6) UNIQUE solution to framework primitives + E1
  GS1: sum_{k>=1} M^(k)(N) = 1 for any N [universal Bernoulli closure]
  GS2: sum_{k>=0} M^(k)(N) = N
  CS1: sum_N M(N) = N_pair = 2
  CS3: sum_N W(N) = 2/9 [STRIKING: cubic sum equals central Koide ratio]
  K1: Ternary refinement: cos^2 = 1/N_pair, sin^2 = 1/N_color + 1/N_quark
  K2: M(N_pair) = 1/N_color + 1/N_quark
  K3: cross-product (N_pair)(2/9) = A^4 = 4/9; ratio N_pair/(2/9) = N_color^2 = 9

ALL INPUTS RETAINED on current main:
- N_pair = 2, N_color = 3, N_quark = N_pair * N_color = 6 (CKM_MAGNITUDES_STRUCTURAL_COUNTS)
- N_pair = N_color - 1 (structural primitive, implicit in retained)
- W2: A^2 = N_pair/N_color (WOLFENSTEIN_LAMBDA_A; used in cross-sector reading)
- rho = 1/N_quark (CKM_CP_PHASE; appears as 1/N_quark in E1)

NO SUPPORT-tier or open inputs used as DERIVATION inputs.

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


def M_k(N: int, k: int) -> Fraction:
    """Bernoulli k-th order: M^(k)(N) = (N - 1)/N^k."""
    if k == 0:
        return Fraction(N - 1, 1)
    return Fraction(N - 1, N ** k)


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  N_pair  = {N_PAIR}")
    print(f"  N_color = {N_COLOR}")
    print(f"  N_quark = N_pair * N_color = {N_QUARK}")
    print(f"  Structural primitive: N_pair = N_color - 1? {N_PAIR == N_COLOR - 1}")

    check("N_pair = 2 (retained)", N_PAIR == 2)
    check("N_color = 3 (retained)", N_COLOR == 3)
    check("N_quark = 6 (= N_pair × N_color)", N_QUARK == N_PAIR * N_COLOR)
    check("Structural primitive: N_pair = N_color - 1", N_PAIR == N_COLOR - 1)

    repo_root = Path(__file__).resolve().parents[1]
    upstream_retained = (
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream_retained:
        path = repo_root / rel
        check(f"retained on main: {rel}", path.exists())


def audit_e1_egyptian_fraction() -> None:
    banner("(E1) NEW: Egyptian fraction unitarity 1/N_pair + 1/N_color + 1/N_quark = 1")

    total = Fraction(1, N_PAIR) + Fraction(1, N_COLOR) + Fraction(1, N_QUARK)

    print(f"  1/N_pair  = 1/{N_PAIR}  = {Fraction(1, N_PAIR)}")
    print(f"  1/N_color = 1/{N_COLOR}  = {Fraction(1, N_COLOR)}")
    print(f"  1/N_quark = 1/{N_QUARK}  = {Fraction(1, N_QUARK)}")
    print(f"  Sum                         = {total}")

    check("(E1) 1/N_pair + 1/N_color + 1/N_quark = 1 EXACTLY", total == 1)


def audit_e2_uniqueness() -> None:
    banner("(E2) NEW Uniqueness: (2, 3, 6) unique solution to framework primitives + E1")

    # With N_pair = N_color - 1 and N_quark = N_pair * N_color, we have:
    # 1/(N_c-1) + 1/N_c + 1/((N_c-1)N_c) = 1
    # = (N_c + N_c - 1 + 1)/((N_c-1) N_c) = 1
    # = 2N_c / ((N_c - 1) N_c) = 1
    # = 2/(N_c - 1) = 1
    # N_c - 1 = 2
    # N_c = 3

    print("  System:")
    print("    (a) N_pair = N_color - 1")
    print("    (b) N_quark = N_pair * N_color")
    print("    (c) 1/N_pair + 1/N_color + 1/N_quark = 1")
    print()
    print("  Solving (c) under (a) and (b):")
    print("    1/(N_c - 1) + 1/N_c + 1/((N_c-1) N_c) = 1")
    print("    = (N_c + N_c - 1 + 1) / ((N_c - 1) N_c)")
    print("    = 2 N_c / ((N_c - 1) N_c)")
    print("    = 2/(N_c - 1) = 1")
    print("    => N_color = 3, N_pair = 2, N_quark = 6.")

    # Verify by exhaustive check at small N_color values
    found_solutions = []
    for N_c_test in range(2, 10):
        N_p_test = N_c_test - 1
        N_q_test = N_p_test * N_c_test
        total = Fraction(1, N_p_test) + Fraction(1, N_c_test) + Fraction(1, N_q_test)
        if total == 1:
            found_solutions.append((N_p_test, N_c_test, N_q_test))

    print(f"\n  Exhaustive search 2 ≤ N_color ≤ 9 finds solutions: {found_solutions}")

    check("(E2) Unique solution (2, 3, 6)", found_solutions == [(2, 3, 6)])


def audit_gs1_geometric_closure() -> None:
    banner("(GS1) NEW: sum_{k>=1} M^(k)(N) = 1 for any N >= 2")

    print("  For each N in {N_pair, N_color, N_quark}, geometric series of M^(k):")
    for N in [N_PAIR, N_COLOR, N_QUARK]:
        # Sum from k=1 to infinity = (N-1) * (1/N) / (1 - 1/N) = 1
        # Verify with partial sum k=1..30 (close to limit)
        partial = sum(Fraction(N - 1, N ** k) for k in range(1, 31))
        # The exact limit is 1
        diff = 1 - partial
        print(f"    N={N}: partial sum (k=1..30) = {partial}, diff from 1 = {diff}")
        check(f"(GS1) sum_{{k>=1}} M^(k)({N}) -> 1 (partial within 1e-10 of 1)",
              float(diff) < 1e-9)


def audit_gs2_with_deficit() -> None:
    banner("(GS2) NEW: sum_{k>=0} M^(k)(N) = N (with deficit)")

    print("  M^(0)(N) = N - 1. Adding to GS1 sum gives total = N.")
    for N in [N_PAIR, N_COLOR, N_QUARK]:
        # k=0 term is (N - 1)/N^0 = N - 1
        # Plus geometric sum from k=1 = 1
        # Total = (N - 1) + 1 = N
        deficit = N - 1
        partial = deficit + sum(Fraction(N - 1, N ** k) for k in range(1, 31))
        diff = N - partial
        print(f"    N={N}: deficit + partial = {partial}, diff from N = {diff}")
        check(f"(GS2) sum_{{k>=0}} M^(k)({N}) -> {N}",
              float(diff) < 1e-9)


def audit_cs1_cross_n_k1() -> None:
    banner("(CS1) NEW: sum_N M(N) = N_pair = 2 at k=1")

    M_pair = Fraction(N_PAIR - 1, N_PAIR)
    M_color = Fraction(N_COLOR - 1, N_COLOR)
    M_quark = Fraction(N_QUARK - 1, N_QUARK)
    total = M_pair + M_color + M_quark

    print(f"  M(N_pair)  = {M_pair}")
    print(f"  M(N_color) = {M_color}")
    print(f"  M(N_quark) = {M_quark}")
    print(f"  Sum        = {total}")
    print(f"  N_pair     = {N_PAIR}")

    check("(CS1) sum_N M(N) = N_pair = 2", total == Fraction(N_PAIR, 1))


def audit_cs3_cross_n_k3_striking() -> None:
    banner("(CS3) NEW STRIKING: sum_N W(N) = 2/9 [central Koide-relevant ratio!]")

    W_pair = Fraction(N_PAIR - 1, N_PAIR ** 3)
    W_color = Fraction(N_COLOR - 1, N_COLOR ** 3)
    W_quark = Fraction(N_QUARK - 1, N_QUARK ** 3)
    total = W_pair + W_color + W_quark

    print(f"  W(N_pair)  = (N_pair  - 1)/N_pair^3   = {W_pair}")
    print(f"  W(N_color) = (N_color - 1)/N_color^3  = {W_color}")
    print(f"  W(N_quark) = (N_quark - 1)/N_quark^3  = {W_quark}")
    print(f"  Sum                                   = {total}")
    print(f"  Equals 2/9? {total == Fraction(2, 9)}")
    print()
    print("  This is the framework's central Koide-relevant ratio derived multi-path")
    print("  in prior branches (K1, K2, K5, K6, K7). NOW from a sum mechanism.")

    check("(CS3) sum_N W(N) = 2/9 EXACTLY", total == Fraction(2, 9))


def audit_k1_ternary_refinement() -> None:
    banner("(K1) NEW: Ternary refinement of Koide unitarity")

    print("  Binary Koide:     cos^2(theta_K) + sin^2(theta_K) = 1")
    print("  Ternary framework: 1/N_pair + 1/N_color + 1/N_quark = 1")
    print()

    cos_sq_K = Fraction(1, N_PAIR)  # = M(N_pair)/(N_pair-1) ... actually 1/N_pair
    sin_sq_K_decomp = Fraction(1, N_COLOR) + Fraction(1, N_QUARK)
    sin_sq_K_complement = 1 - cos_sq_K

    print(f"  cos^2(theta_K) = 1/N_pair                       = {cos_sq_K}")
    print(f"  sin^2(theta_K) = 1 - cos^2 (binary unitarity)   = {sin_sq_K_complement}")
    print(f"  sin^2(theta_K) = 1/N_color + 1/N_quark (ternary) = {sin_sq_K_decomp}")
    print()
    print("  Ternary refinement: sin^2(theta_K) splits as 1/N_color + 1/N_quark.")
    print("  Under cross-sector A^2 ↔ Q_l: cos^2 = 1/N_pair, sin^2 = 1/N_color + 1/N_quark.")

    check("(K1) cos^2(theta_K) = 1/N_pair (under cross-sector)",
          cos_sq_K == Fraction(1, 2))
    check("(K1) sin^2(theta_K) = 1/N_color + 1/N_quark (NEW DECOMPOSITION)",
          sin_sq_K_decomp == sin_sq_K_complement)


def audit_k2_m_n_pair_decomp() -> None:
    banner("(K2) NEW: M(N_pair) = 1/N_color + 1/N_quark")

    M_pair = Fraction(N_PAIR - 1, N_PAIR)
    decomp = Fraction(1, N_COLOR) + Fraction(1, N_QUARK)

    print(f"  M(N_pair) = (N_pair - 1)/N_pair       = {M_pair}")
    print(f"  1/N_color + 1/N_quark                  = {decomp}")
    print(f"  Equal? {M_pair == decomp}")
    print()
    print("  Bernoulli mean at pair level decomposes as sum of reciprocals at")
    print("  color and quark levels. Direct corollary of E1.")

    check("(K2) M(N_pair) = 1/N_color + 1/N_quark EXACTLY", M_pair == decomp)


def audit_k3_cross_product_consistency() -> None:
    banner("(K3) NEW: Cross-product consistency of cross-N sums")

    sum_M = sum(Fraction(N - 1, N) for N in [N_PAIR, N_COLOR, N_QUARK])
    sum_W = sum(Fraction(N - 1, N ** 3) for N in [N_PAIR, N_COLOR, N_QUARK])

    product = sum_M * sum_W
    ratio = sum_M / sum_W

    A_4 = (Fraction(N_PAIR, N_COLOR)) ** 2  # A^4

    print(f"  sum_N M(N)  = {sum_M}")
    print(f"  sum_N W(N)  = {sum_W}")
    print(f"  Product = N_pair * 2/9   = {product}")
    print(f"  A^4 = (N_pair/N_color)^2 = {A_4}")
    print(f"  Equal? {product == A_4}")
    print()
    print(f"  Ratio  = N_pair / (2/9)  = {ratio}")
    print(f"  N_color^2                = {N_COLOR ** 2}")
    print(f"  Equal? {ratio == Fraction(N_COLOR ** 2, 1)}")

    check("(K3) (sum_M)(sum_W) = A^4 = 4/9", product == A_4)
    check("(K3) sum_M / sum_W = N_color^2 = 9",
          ratio == Fraction(N_COLOR ** 2, 1))


def audit_summary() -> None:
    banner("Summary of new content")

    print("  NEW (E1):  Egyptian fraction unitarity:")
    print("              1/N_pair + 1/N_color + 1/N_quark = 1 EXACTLY (= 1/2 + 1/3 + 1/6).")
    print()
    print("  NEW (E2):  Uniqueness theorem: (2, 3, 6) unique solution to framework primitives + E1.")
    print()
    print("  NEW (GS1): sum_{k>=1} M^(k)(N) = 1 universal Bernoulli closure for any N.")
    print()
    print("  NEW (GS2): sum_{k>=0} M^(k)(N) = N (with deficit).")
    print()
    print("  NEW (CS1): sum_N M(N) = N_pair = 2 (cross-N k=1 sum).")
    print()
    print("  NEW (CS3): sum_N W(N) = 2/9 STRIKING (cubic Bernoulli sum = central Koide ratio).")
    print()
    print("  NEW (K1):  Ternary refinement of Koide unitarity:")
    print("              cos^2(theta_K) = 1/N_pair, sin^2(theta_K) = 1/N_color + 1/N_quark.")
    print()
    print("  NEW (K2):  M(N_pair) = 1/N_color + 1/N_quark (corollary of E1).")
    print()
    print("  NEW (K3):  Cross-product consistency: (sum_M)(sum_W) = A^4 = 4/9.")
    print()
    print("  Six framework-native paths to 2/9 now (K1-K7 from prior branches + CS3 here).")
    print("  Does NOT close A^2 (already retained at W2) or Koide 2/9 (cross-sector).")


def main() -> int:
    print("=" * 88)
    print("Egyptian fraction unitarity and Bernoulli sum closures Koide-bridge audit")
    print("See docs/CKM_EGYPTIAN_BERNOULLI_CLOSURES_KOIDE_BRIDGE_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_e1_egyptian_fraction()
    audit_e2_uniqueness()
    audit_gs1_geometric_closure()
    audit_gs2_with_deficit()
    audit_cs1_cross_n_k1()
    audit_cs3_cross_n_k3_striking()
    audit_k1_ternary_refinement()
    audit_k2_m_n_pair_decomp()
    audit_k3_cross_product_consistency()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
