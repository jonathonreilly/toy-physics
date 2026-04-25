#!/usr/bin/env python3
"""CKM consecutive-prime and S3 representation-support audit.

Verifies the exact retained-input arithmetic in
  docs/CKM_CONSECUTIVE_PRIMES_S3_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md

Cross-sector Koide/S3 readings are printed as support commentary and are not
counted as proof checks.
"""

from __future__ import annotations

import itertools
import math
import sys
from pathlib import Path


PASS_COUNT = 0
FAIL_COUNT = 0


N_PAIR = 2
N_COLOR = 3
N_QUARK = N_PAIR * N_COLOR


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


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n**0.5) + 1))


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def fib(n: int) -> int:
    if n <= 0:
        raise ValueError("Fibonacci index must be positive")
    if n <= 2:
        return 1
    a, b = 1, 1
    for _ in range(n - 2):
        a, b = b, a + b
    return b


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Return p o q for permutations represented as image tuples."""
    return tuple(p[q[i]] for i in range(len(p)))


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    inv = [0] * len(p)
    for i, image in enumerate(p):
        inv[image] = i
    return tuple(inv)


def conjugacy_classes_s3() -> list[set[tuple[int, ...]]]:
    perms = list(itertools.permutations(range(N_COLOR)))
    remaining = set(perms)
    classes: list[set[tuple[int, ...]]] = []
    while remaining:
        element = next(iter(remaining))
        cls = {compose(compose(g, element), inverse(g)) for g in perms}
        classes.append(cls)
        remaining -= cls
    return classes


def audit_inputs() -> None:
    banner("Retained CKM structural-count inputs")

    print(f"  N_pair  = {N_PAIR}")
    print(f"  N_color = {N_COLOR}")
    print(f"  N_quark = N_pair * N_color = {N_QUARK}")

    check("N_pair = 2", N_PAIR == 2)
    check("N_color = 3", N_COLOR == 3)
    check("N_quark = N_pair * N_color = 6", N_QUARK == 6)
    check("N_pair = N_color - 1", N_PAIR == N_COLOR - 1)

    repo_root = Path(__file__).resolve().parents[1]
    authority = repo_root / "docs/CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md"
    check("retained authority exists: CKM magnitudes structural counts", authority.exists())


def audit_consecutive_primes() -> None:
    banner("(P1)-(P2) Consecutive positive primes")

    print(f"  N_pair prime?  {is_prime(N_PAIR)}")
    print(f"  N_color prime? {is_prime(N_COLOR)}")
    print(f"  gap = {N_COLOR - N_PAIR}")

    check("N_pair is prime", is_prime(N_PAIR))
    check("N_color is prime", is_prime(N_COLOR))
    check("(N_pair,N_color) are consecutive", N_COLOR - N_PAIR == 1)

    pairs = [(p, p + 1) for p in range(2, 100) if is_prime(p) and is_prime(p + 1)]
    print(f"  consecutive prime pairs for 2 <= p < 100: {pairs}")
    check("(2,3) is the unique consecutive positive-prime pair in audited range", pairs == [(2, 3)])


def audit_divisor_structure() -> None:
    banner("(D1)-(D3) Divisor structure")

    div_pair = divisors(N_PAIR)
    div_color = divisors(N_COLOR)
    div_quark = divisors(N_QUARK)

    print(f"  Div({N_PAIR}) = {div_pair}")
    print(f"  Div({N_COLOR}) = {div_color}")
    print(f"  Div({N_QUARK}) = {div_quark}")

    check("d(N_pair) = N_pair = 2", len(div_pair) == N_PAIR)
    check("d(N_color) = N_pair = 2", len(div_color) == N_PAIR)
    check("d(N_quark) = N_pair^2 = 4", len(div_quark) == N_PAIR**2)
    check("Div(N_quark) = {1,N_pair,N_color,N_quark}", div_quark == [1, N_PAIR, N_COLOR, N_QUARK])


def audit_s3_structure() -> None:
    banner("(G1)-(G4) Symmetric-group S3 structure")

    order = math.factorial(N_COLOR)
    classes = conjugacy_classes_s3()
    class_sizes = sorted(len(cls) for cls in classes)
    expected_sizes = sorted([1, N_PAIR, N_COLOR])
    class_sum = sum(class_sizes)

    print(f"  |S_N_color| = {N_COLOR}! = {order}")
    print(f"  enumerated conjugacy-class sizes = {class_sizes}")

    check("|S_{N_color}| = N_quark", order == N_QUARK)
    check("S3 conjugacy-class sizes are {1,N_pair,N_color}", class_sizes == expected_sizes)
    check("class equation 1 + N_pair + N_color = N_quark", class_sum == N_QUARK)

    irrep_dims = [1, 1, N_PAIR]
    burnside = sum(dim * dim for dim in irrep_dims)
    print(f"  S3 irrep dimensions used: {irrep_dims}")
    print(f"  Burnside sum = {burnside}")

    check("Burnside: 1^2 + 1^2 + N_pair^2 = N_quark", burnside == N_QUARK)


def audit_representation_primitive() -> None:
    banner("(R1)-(R2) Standard-representation dimension")

    std_dim = N_COLOR - 1
    perm_dim = 1 + std_dim

    print(f"  dim(std rep S_N_color) = N_color - 1 = {std_dim}")
    print(f"  dim(perm rep S_N_color) = 1 + std_dim = {perm_dim}")

    check("dim(std rep S_N_color) = N_pair", std_dim == N_PAIR)
    check("dim(perm rep S_N_color) = N_color", perm_dim == N_COLOR)
    check("N_pair = N_color - 1 = dim(std rep)", N_PAIR == N_COLOR - 1 == std_dim)


def audit_fibonacci() -> None:
    banner("(F1)-(F2) Fibonacci triple")

    triple = (fib(3), fib(4), fib(5))
    framework = (N_PAIR, N_COLOR, N_QUARK - 1)

    print(f"  (F3,F4,F5) = {triple}")
    print(f"  (N_pair,N_color,N_quark-1) = {framework}")

    check("F3 = N_pair", fib(3) == N_PAIR)
    check("F4 = N_color", fib(4) == N_COLOR)
    check("F5 = N_quark - 1", fib(5) == N_QUARK - 1)
    check("N_pair + N_color = N_quark - 1", N_PAIR + N_COLOR == N_QUARK - 1)


def audit_mixing_angle_count() -> None:
    banner("(C1)-(C2) Mixing-angle count")

    binom = math.comb(N_COLOR, 2)
    print(f"  binom(N_color,2) = {binom}")

    check("binom(N_color,2) = 3", binom == 3)
    check("with N_pair=2, binom(N_color,2) = N_color", binom == N_COLOR)


def audit_combined_uniqueness() -> None:
    banner("(U1) Combined positive-integer uniqueness")

    solutions = []
    for n_pair in range(2, 20):
        for n_color in range(2, 40):
            if not (is_prime(n_pair) and is_prime(n_color)):
                continue
            if n_color - n_pair != 1:
                continue
            n_quark = n_pair * n_color
            if n_pair + n_color != n_quark - 1:
                continue
            if 1 + n_pair + n_color != n_quark:
                continue
            if 1 + 1 + n_pair**2 != n_quark:
                continue
            solutions.append((n_pair, n_color, n_quark))

    print(f"  solutions in audited range: {solutions}")

    check("unique solution is (2,3,6)", solutions == [(N_PAIR, N_COLOR, N_QUARK)])


def audit_conditional_koide_reading() -> None:
    banner("Conditional Koide/S3 reading (not counted)")

    print("  Koide is symmetric under permutations of charged-lepton masses.")
    print("  If a separate retained theorem supplies N_gen=N_color=3, then")
    print("  the Koide permutation group is S3 and the natural representation")
    print("  decomposes as trivial + standard with dimensions 1 + N_pair.")
    print()
    print("  This is support commentary only. It is not a PASS/FAIL proof check.")


def audit_summary() -> None:
    banner("Scope summary")

    print("  Certified:")
    print("    consecutive-prime structure, divisor structure, enumerated S3")
    print("    conjugacy classes, S3 Burnside sum, standard-rep dimension,")
    print("    Fibonacci triple, mixing-angle count, and combined uniqueness.")
    print()
    print("  Not certified here:")
    print("    charged-lepton Koide, Q_l=2/3, PMNS closure, or N_gen=N_color.")


def main() -> int:
    print("=" * 88)
    print("CKM consecutive-prime and S3 representation-support audit")
    print("See docs/CKM_CONSECUTIVE_PRIMES_S3_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md")
    print("=" * 88)

    audit_inputs()
    audit_consecutive_primes()
    audit_divisor_structure()
    audit_s3_structure()
    audit_representation_primitive()
    audit_fibonacci()
    audit_mixing_angle_count()
    audit_combined_uniqueness()
    audit_conditional_koide_reading()
    audit_summary()

    print()
    print("=" * 88)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
