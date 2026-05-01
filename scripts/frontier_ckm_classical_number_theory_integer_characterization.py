#!/usr/bin/env python3
"""Audit classical number-theory characterizations of the retained CKM counts.

Verifies the retained CKM-only theorem in
  docs/CKM_CLASSICAL_NUMBER_THEORY_INTEGER_CHARACTERIZATION_THEOREM_NOTE_2026-04-25.md

The audited identities are:
  P1: N_quark = 1 + N_pair + N_color
  P2: sigma(N_quark) = 2 * N_quark
  P3: proper-divisor sum/product coincidence for 6
  P4: N_pair, N_color deficient; N_quark perfect
  T1: N_color = T_{N_pair}, N_quark = T_{N_color}
  L1: N_color = N_pair^2 - 1 = dim(adjoint SU(N_pair))
  M1: N_color = 2^{N_pair} - 1
  M2: N_quark = 2^{N_pair - 1} * (2^{N_pair} - 1)
  U1: five independent three-constraint uniqueness routes

All derivation inputs are retained on current main:
  N_pair = 2, N_color = 3, N_quark = N_pair * N_color = 6

Uses exact integer arithmetic and fractions.Fraction where needed.
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


def sigma(n: int) -> int:
    """Sum of all positive divisors of n."""
    return sum(d for d in range(1, n + 1) if n % d == 0)


def proper_divisors(n: int) -> list[int]:
    """Proper divisors (divisors excluding n itself)."""
    return [d for d in range(1, n) if n % d == 0]


def triangular(n: int) -> int:
    """Triangular number T_n = n(n+1)/2."""
    return n * (n + 1) // 2


def is_deficient(n: int) -> bool:
    return sigma(n) - n < n


def is_perfect(n: int) -> bool:
    return sigma(n) - n == n


def audit_inputs() -> None:
    banner("Retained inputs on current main")

    print(f"  N_pair  = {N_PAIR}")
    print(f"  N_color = {N_COLOR}")
    print(f"  N_quark = N_pair × N_color = {N_QUARK}")
    print(f"  Consecutive scaffold: N_pair = N_color - 1? {N_PAIR == N_COLOR - 1}")

    check("N_pair = 2 (retained)", N_PAIR == 2)
    check("N_color = 3 (retained)", N_COLOR == 3)
    check("N_quark = 6 (= N_pair × N_color)", N_QUARK == N_PAIR * N_COLOR)
    check("Consecutive scaffold: N_pair = N_color - 1", N_PAIR == N_COLOR - 1)

    repo_root = Path(__file__).resolve().parents[1]
    upstream = "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md"
    check(f"retained on main: {upstream}",
          (repo_root / upstream).exists())


def audit_p1_perfect_number() -> None:
    banner("(P1) NEW: Perfect number identity N_quark = 1 + N_pair + N_color")

    proper = proper_divisors(N_QUARK)
    sum_proper = sum(proper)

    print(f"  Proper divisors of N_quark = {N_QUARK}: {proper}")
    print(f"  In framework: {{1, N_pair, N_color}} = {{1, {N_PAIR}, {N_COLOR}}}")
    print(f"  Sum of proper divisors:         {sum_proper}")
    print(f"  1 + N_pair + N_color:            {1 + N_PAIR + N_COLOR}")
    print(f"  N_quark:                         {N_QUARK}")

    check("(P1) Proper divisors of N_quark are {1, N_pair, N_color}",
          proper == [1, N_PAIR, N_COLOR])
    check("(P1) N_quark = 1 + N_pair + N_color (perfect number identity)",
          N_QUARK == 1 + N_PAIR + N_COLOR)
    check("(P1) Sum of proper divisors of N_quark equals N_quark",
          sum_proper == N_QUARK)


def audit_p2_sigma_perfect() -> None:
    banner("(P2) NEW: sigma(N_quark) = 2 N_quark (sigma-perfect condition)")

    sigma_val = sigma(N_QUARK)

    print(f"  sigma(N_quark) = sigma({N_QUARK}) = {sigma_val}")
    print(f"  2 × N_quark = {2 * N_QUARK}")
    print(f"  sigma(N) = 2N is the formal definition of N as a perfect number.")

    check("(P2) sigma(N_quark) = 2 N_quark (perfect)", sigma_val == 2 * N_QUARK)


def audit_p3_sum_product_coincidence() -> None:
    banner("(P3) Sum-product coincidence for the proper divisors of 6")

    sum_prop = 1 + N_PAIR + N_COLOR
    prod_prop = 1 * N_PAIR * N_COLOR

    print(f"  Sum of proper divisors:    1 + N_pair + N_color = {sum_prop}")
    print(f"  Product of proper divisors: 1 × N_pair × N_color = {prod_prop}")
    print(f"  Both equal N_quark = {N_QUARK}")
    check("(P3) Sum of proper divisors = N_quark", sum_prop == N_QUARK)
    check("(P3) Product of proper divisors = N_quark", prod_prop == N_QUARK)
    check("(P3) Sum = Product = N_quark", sum_prop == prod_prop == N_QUARK)


def audit_p4_classification() -> None:
    banner("(P4) NEW: Deficient/Perfect classification of structural integers")

    classes = {}
    for N, name in [(N_PAIR, "N_pair"), (N_COLOR, "N_color"), (N_QUARK, "N_quark")]:
        s = sigma(N)
        deficiency = s - 2 * N  # < 0 deficient, = 0 perfect, > 0 abundant
        if deficiency < 0:
            cls = "DEFICIENT"
        elif deficiency == 0:
            cls = "PERFECT"
        else:
            cls = "ABUNDANT"
        classes[name] = cls
        proper = proper_divisors(N)
        print(f"  {name}={N}: proper divisors = {proper}, sum = {sum(proper)}, "
              f"sigma({N}) = {s}, classification: {cls}")

    check("(P4) N_pair = 2 is DEFICIENT", classes["N_pair"] == "DEFICIENT")
    check("(P4) N_color = 3 is DEFICIENT (3 is prime)",
          classes["N_color"] == "DEFICIENT")
    check("(P4) N_quark = 6 is PERFECT", classes["N_quark"] == "PERFECT")


def audit_t1_triangular_ladder() -> None:
    banner("(T1) NEW: Triangular ladder N_pair=2 -> N_color=T_2 -> N_quark=T_3")

    T_N_pair = triangular(N_PAIR)
    T_N_color = triangular(N_COLOR)

    print(f"  T_n = n(n+1)/2  triangular numbers: T_1=1, T_2=3, T_3=6, T_4=10, T_5=15, ...")
    print()
    print(f"  T_{{N_pair}}  = T_{N_PAIR} = {N_PAIR}({N_PAIR + 1})/2 = {T_N_pair}")
    print(f"  N_color                                  = {N_COLOR}")
    print(f"  Equal? {T_N_pair == N_COLOR}")
    print()
    print(f"  T_{{N_color}} = T_{N_COLOR} = {N_COLOR}({N_COLOR + 1})/2 = {T_N_color}")
    print(f"  N_quark                                  = {N_QUARK}")
    print(f"  Equal? {T_N_color == N_QUARK}")
    print()
    print(f"  Triangular ladder: N_pair = {N_PAIR} -> N_color = T_{N_PAIR} = {T_N_pair} -> N_quark = T_{N_COLOR} = {T_N_color}")

    check("(T1) N_color = T_{N_pair} (= triangular of N_pair)",
          T_N_pair == N_COLOR)
    check("(T1) N_quark = T_{N_color} (= triangular of N_color)",
          T_N_color == N_QUARK)


def audit_l1_lie_dimensional() -> None:
    banner("(L1) NEW: Lie-dimensional identity N_color = dim(adjoint SU(N_pair))")

    adj_dim = N_PAIR ** 2 - 1

    print(f"  dim(adjoint SU(N)) = N^2 - 1")
    print(f"  dim(adjoint SU(N_pair)) = N_pair^2 - 1 = {N_PAIR}^2 - 1 = {adj_dim}")
    print(f"  N_color                                = {N_COLOR}")
    print(f"  Equal? {adj_dim == N_COLOR}")
    print()
    print(f"  In particular: SU(2) has 3 generators (the Pauli matrices), and N_color = 3.")

    check("(L1) N_color = N_pair^2 - 1 = dim(adjoint SU(N_pair))",
          N_COLOR == adj_dim)


def audit_m1_m2_mersenne() -> None:
    banner("(M1)(M2) NEW: Mersenne prime and Mersenne-form perfect number")

    mersenne = 2 ** N_PAIR - 1
    print(f"  Mersenne primes: M_p = 2^p - 1 for p prime")
    print(f"    M_2 = 2^2 - 1 = {2**2 - 1}  (smallest Mersenne prime)")
    print(f"    M_3 = 2^3 - 1 = {2**3 - 1}  (next Mersenne prime)")
    print()
    print(f"  N_color = 2^{{N_pair}} - 1 = 2^{N_PAIR} - 1 = {mersenne}")
    print(f"  N_color retained = {N_COLOR}")

    check("(M1) N_color = 2^{N_pair} - 1 = M_{N_pair}", mersenne == N_COLOR)

    # Mersenne-form perfect
    p = N_PAIR
    mersenne_perfect = (2 ** (p - 1)) * (2 ** p - 1)
    print()
    print(f"  Euclid-Euler theorem: even perfect numbers = 2^(p-1) * (2^p - 1)")
    print(f"  At p = N_pair = {N_PAIR}: 2^{p-1} * (2^{p} - 1) = {mersenne_perfect}")
    print(f"  N_quark retained = {N_QUARK}")
    print(f"  N_quark IS the smallest Mersenne-form perfect number.")

    check("(M2) N_quark = 2^{N_pair-1} * (2^{N_pair} - 1) (Mersenne-form perfect)",
          mersenne_perfect == N_QUARK)


def route_solutions(route: str) -> list[tuple[int, int, int]]:
    found: list[tuple[int, int, int]] = []
    for n_pair in range(1, 10):
        for n_color in range(2, 20):
            if n_pair != n_color - 1:
                continue
            n_quark = n_pair * n_color

            if route == "c" and n_quark != 1 + n_pair + n_color:
                continue
            if route == "d" and n_quark != triangular(n_color):
                continue
            if route == "e" and (
                Fraction(1, n_pair) + Fraction(1, n_color) + Fraction(1, n_quark) != 1
            ):
                continue
            if route == "f" and n_color != n_pair**2 - 1:
                continue
            if route == "g" and n_color != 2**n_pair - 1:
                continue

            found.append((n_pair, n_color, n_quark))
    return found


def audit_u1_uniqueness_routes() -> None:
    banner("(U1) Five independent three-constraint uniqueness routes")

    routes = {
        "c": "perfect-number identity",
        "d": "triangular identity",
        "e": "Egyptian-fraction identity",
        "f": "Lie-dimensional identity",
        "g": "Mersenne-prime identity",
    }

    print("  Common scaffold:")
    print("    (a) N_pair = N_color - 1")
    print("    (b) N_quark = N_pair × N_color")
    print()
    print("  Exhaustive positive-integer search on audited ranges:")
    print("    1 <= N_pair <= 9,  2 <= N_color <= 19")

    expected = [(N_PAIR, N_COLOR, N_QUARK)]
    for key, label in routes.items():
        found = route_solutions(key)
        print()
        print(f"  Route (a)+(b)+({key}) [{label}] -> {found}")
        check(f"(U1.{key}) Unique solution (2, 3, 6) for route {key}", found == expected)


def audit_summary() -> None:
    banner("Summary of new content")

    print("  P1: N_quark = 1 + N_pair + N_color = 6.")
    print("  P2: sigma(N_quark) = 2 N_quark.")
    print("  P3: proper-divisor sum/product coincidence for 6.")
    print("  P4: N_pair, N_color deficient; N_quark perfect.")
    print("  T1: triangular ladder 2 -> 3 -> 6.")
    print("  L1: N_color = N_pair^2 - 1 = dim(adjoint SU(2)) = 3.")
    print("  M1: N_color = 2^{N_pair} - 1 = 3.")
    print("  M2: N_quark = 2^{N_pair-1}(2^{N_pair} - 1) = 6.")
    print("  U1: each of the five routes (a)+(b)+(x), x in {c,d,e,f,g},")
    print("      independently forces the unique solution (2, 3, 6).")
    print()
    print("  All inputs are retained on main.")
    print("  No cross-sector or Koide closure is claimed here.")


def main() -> int:
    print("=" * 88)
    print("Classical number-theory characterization of the retained CKM counts")
    print("See docs/CKM_CLASSICAL_NUMBER_THEORY_INTEGER_CHARACTERIZATION_THEOREM_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_p1_perfect_number()
    audit_p2_sigma_perfect()
    audit_p3_sum_product_coincidence()
    audit_p4_classification()
    audit_t1_triangular_ladder()
    audit_l1_lie_dimensional()
    audit_m1_m2_mersenne()
    audit_u1_uniqueness_routes()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
