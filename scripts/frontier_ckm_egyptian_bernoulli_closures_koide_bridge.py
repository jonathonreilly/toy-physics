#!/usr/bin/env python3
"""CKM Egyptian-fraction and Bernoulli-sum support audit.

Verifies the exact retained-input arithmetic in
  docs/CKM_EGYPTIAN_BERNOULLI_CLOSURES_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md

The runner deliberately does not count conditional charged-lepton/Koide readings
as PASS checks. Those are printed as support commentary only.
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


N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR


def m_power(n: int, k: int) -> Fraction:
    """Return M^(k)(N) = (N - 1) / N^k."""
    return Fraction(n - 1, n**k)


def audit_inputs() -> None:
    banner("Retained CKM inputs")

    print(f"  N_pair  = {N_PAIR}")
    print(f"  N_color = {N_COLOR}")
    print(f"  N_quark = N_pair * N_color = {N_QUARK}")

    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)
    check("N_quark = N_pair * N_color = 6", N_QUARK == 6)
    check("N_pair = N_color - 1", N_PAIR == N_COLOR - 1)

    repo_root = Path(__file__).resolve().parents[1]
    upstream = (
        "docs/WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md",
        "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md",
    )
    for rel in upstream:
        check(f"retained authority exists: {rel}", (repo_root / rel).exists())


def audit_e1_egyptian_fraction() -> None:
    banner("(E1) Egyptian fraction identity")

    total = Fraction(1, N_PAIR) + Fraction(1, N_COLOR) + Fraction(1, N_QUARK)

    print(f"  1/N_pair  = {Fraction(1, N_PAIR)}")
    print(f"  1/N_color = {Fraction(1, N_COLOR)}")
    print(f"  1/N_quark = {Fraction(1, N_QUARK)}")
    print(f"  total     = {total}")

    check("1/N_pair + 1/N_color + 1/N_quark = 1", total == 1)


def audit_e2_uniqueness() -> None:
    banner("(E2) Unique solution under framework primitives")

    print("  Under N_pair=N_color-1 and N_quark=N_pair*N_color:")
    print("    1/(N_color-1) + 1/N_color + 1/((N_color-1)N_color)")
    print("    = 2/(N_color-1).")
    print("  Setting this equal to 1 gives N_color=3, hence (2,3,6).")

    found = []
    for n_color in range(2, 40):
        n_pair = n_color - 1
        n_quark = n_pair * n_color
        total = Fraction(1, n_pair) + Fraction(1, n_color) + Fraction(1, n_quark)
        if total == 1:
            found.append((n_pair, n_color, n_quark))

    print(f"  exhaustive positive-integer scan 2 <= N_color < 40: {found}")

    check("unique solution is (N_pair,N_color,N_quark)=(2,3,6)", found == [(2, 3, 6)])


def audit_gs1_geometric_closure() -> None:
    banner("(GS1) Exact geometric closure sum_{k>=1} M^(k)(N)=1")

    for n in (N_PAIR, N_COLOR, N_QUARK):
        ratio = Fraction(1, n)
        closed_form = Fraction(n - 1, 1) * ratio / (1 - ratio)
        print(f"  N={n}: (N-1)*(1/N)/(1-1/N) = {closed_form}")
        check(f"sum_{{k>=1}} M^(k)({n}) = 1 exactly", closed_form == 1)


def audit_gs2_with_deficit() -> None:
    banner("(GS2) Exact closure sum_{k>=0} M^(k)(N)=N")

    for n in (N_PAIR, N_COLOR, N_QUARK):
        ratio = Fraction(1, n)
        tail = Fraction(n - 1, 1) * ratio / (1 - ratio)
        total = m_power(n, 0) + tail
        print(f"  N={n}: M^(0)(N)+tail = {m_power(n, 0)} + {tail} = {total}")
        check(f"sum_{{k>=0}} M^(k)({n}) = {n} exactly", total == n)


def audit_cs1_cross_n_k1() -> None:
    banner("(CS1) Cross-N sum at k=1")

    total = sum(m_power(n, 1) for n in (N_PAIR, N_COLOR, N_QUARK))
    print(f"  M(2)+M(3)+M(6) = {total}")

    check("sum_N M(N) = N_pair = 2", total == N_PAIR)


def audit_cs2_cross_n_k2() -> None:
    banner("(CS2) Cross-N sum at k=2")

    total = sum(m_power(n, 2) for n in (N_PAIR, N_COLOR, N_QUARK))
    print(f"  V(2)+V(3)+V(6) = {total}")

    check("sum_N V(N) = 11/18", total == Fraction(11, 18))


def audit_cs3_cross_n_k3() -> None:
    banner("(CS3) Cross-N sum at k=3")

    terms = [m_power(n, 3) for n in (N_PAIR, N_COLOR, N_QUARK)]
    total = sum(terms)

    print(f"  W(2) = {terms[0]}")
    print(f"  W(3) = {terms[1]}")
    print(f"  W(6) = {terms[2]}")
    print(f"  sum  = {total}")

    check("sum_N W(N) = 2/9 exactly", total == Fraction(2, 9))


def audit_conditional_koide_reading() -> None:
    banner("Conditional Koide target-class reading (not counted)")

    cos_sq_target = Fraction(1, N_PAIR)
    sin_sq_decomp = Fraction(1, N_COLOR) + Fraction(1, N_QUARK)

    print("  If a separate retained cross-sector theorem supplies:")
    print(f"    cos^2(theta_K) = 1/N_pair = {cos_sq_target}")
    print("  then the Egyptian identity supplies the target decomposition:")
    print(f"    sin^2(theta_K) = 1/N_color + 1/N_quark = {sin_sq_decomp}")
    print()
    print("  This is support commentary only. It is not a PASS/FAIL proof check.")


def audit_k2_m_pair_decomposition() -> None:
    banner("(K2) M(N_pair) reciprocal decomposition")

    lhs = m_power(N_PAIR, 1)
    rhs = Fraction(1, N_COLOR) + Fraction(1, N_QUARK)
    print(f"  M(N_pair) = {lhs}")
    print(f"  1/N_color + 1/N_quark = {rhs}")

    check("M(N_pair) = 1/N_color + 1/N_quark", lhs == rhs)


def audit_k3_cross_product_consistency() -> None:
    banner("(K3) Cross-product consistency")

    sum_m = sum(m_power(n, 1) for n in (N_PAIR, N_COLOR, N_QUARK))
    sum_w = sum(m_power(n, 3) for n in (N_PAIR, N_COLOR, N_QUARK))
    product = sum_m * sum_w
    ratio = sum_m / sum_w
    a_fourth = Fraction(N_PAIR, N_COLOR) ** 2

    print(f"  sum_N M(N) = {sum_m}")
    print(f"  sum_N W(N) = {sum_w}")
    print(f"  product    = {product}")
    print(f"  A^4        = {a_fourth}")
    print(f"  ratio      = {ratio}")

    check("(sum_N M(N))(sum_N W(N)) = A^4 = 4/9", product == a_fourth)
    check("(sum_N M(N))/(sum_N W(N)) = N_color^2 = 9", ratio == N_COLOR**2)


def audit_summary() -> None:
    banner("Scope summary")

    print("  Certified:")
    print("    E1 Egyptian fraction identity, E2 uniqueness, exact GS1/GS2 formulas,")
    print("    CS1/CS2/CS3 cross-N sums, K2 reciprocal decomposition, and K3 products.")
    print()
    print("  Not certified here:")
    print("    charged-lepton Koide, cos^2(theta_K), or structural Koide mechanism.")


def main() -> int:
    print("=" * 88)
    print("CKM Egyptian-fraction and Bernoulli-sum support audit")
    print("See docs/CKM_EGYPTIAN_BERNOULLI_CLOSURES_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_e1_egyptian_fraction()
    audit_e2_uniqueness()
    audit_gs1_geometric_closure()
    audit_gs2_with_deficit()
    audit_cs1_cross_n_k1()
    audit_cs2_cross_n_k2()
    audit_cs3_cross_n_k3()
    audit_conditional_koide_reading()
    audit_k2_m_pair_decomposition()
    audit_k3_cross_product_consistency()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
