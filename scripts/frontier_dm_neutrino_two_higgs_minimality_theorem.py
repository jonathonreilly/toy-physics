#!/usr/bin/env python3
"""
DM-side minimality theorem for the local neutrino two-Higgs extension.

Question:
  After the universal-Yukawa no-go and the odd-circulant CP tool, what is the
  unique minimal exact local Z3 extension that can possibly support the
  required non-diagonal Hermitian kernel for leptogenesis?

Answer:
  A neutrino two-Higgs lane with distinct Higgs charges.

  - every fixed-charge single-Higgs lane is monomial, so Y^dag Y is diagonal
  - a two-Higgs lane with repeated charge is still effectively single-Higgs
  - two distinct charges are the first exact local escape, and every such pair
    is support-equivalent to the canonical two-Higgs class A + B C
  - on that class, the DM CP-supporting odd-circulant right-Gram family is
    realized on the exact admissible subcone d >= 2 r

Boundary:
  This does not derive the two-Higgs extension from the bare axiom alone.
  It proves that once nonzero local DM CP support is required, the canonical
  two-Higgs distinct-charge lane is the unique minimal exact local escape.
"""

from __future__ import annotations

import itertools
import math
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

CYCLE = np.array(
    [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
    ],
    dtype=complex,
)


def check(name: str, condition: bool, detail: str = "") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def perm_power(q: int) -> np.ndarray:
    q %= 3
    if q == 0:
        return np.eye(3, dtype=complex)
    if q == 1:
        return CYCLE.copy()
    return CYCLE @ CYCLE


def single_higgs_y(diag_entries: np.ndarray, q: int) -> np.ndarray:
    return np.diag(np.asarray(diag_entries, dtype=complex)) @ perm_power(q)


def two_higgs_y(a: np.ndarray, qa: int, b: np.ndarray, qb: int) -> np.ndarray:
    return np.diag(np.asarray(a, dtype=complex)) @ perm_power(qa) + np.diag(np.asarray(b, dtype=complex)) @ perm_power(qb)


def canonical_two_higgs_y(x: float, y: float, delta: float) -> np.ndarray:
    return np.diag([x, x, x]).astype(complex) + np.diag([y, y, y * np.exp(1j * delta)]).astype(complex) @ CYCLE


def right_gram(y: np.ndarray) -> np.ndarray:
    return y.conj().T @ y


def shift_matrix() -> np.ndarray:
    return CYCLE.copy()


def minimal_cp_family(mu: float, nu: float, eta: float) -> np.ndarray:
    s = shift_matrix()
    return mu * np.eye(3, dtype=complex) + nu * (s + s @ s) + 1j * eta * (s - s @ s)


def canonical_rephasing_for_circulant(h: complex) -> np.ndarray:
    theta = np.angle(h)
    return np.diag([1.0, np.exp(1j * theta), np.exp(2j * theta)]).astype(complex)


def canonicalize_circulant_right_gram(k: np.ndarray) -> tuple[np.ndarray, float, float, float]:
    h = k[0, 1]
    p = canonical_rephasing_for_circulant(h)
    k_can = p @ k @ p.conj().T
    d = float(np.real(k_can[0, 0]))
    r = float(np.abs(k_can[0, 1]))
    delta = float(np.angle(k_can[2, 0]))
    return k_can, d, r, delta


def canonical_circulant_target(d: float, r: float, delta: float) -> np.ndarray:
    return np.array(
        [
            [d, r, r * np.exp(-1j * delta)],
            [r, d, r],
            [r * np.exp(1j * delta), r, d],
        ],
        dtype=complex,
    )


def symmetric_two_higgs_solution(d: float, r: float) -> tuple[float, float] | None:
    disc = d * d - 4.0 * r * r
    if disc < -1e-12:
        return None
    disc = max(disc, 0.0)
    root = math.sqrt(disc)
    x2 = 0.5 * (d + root)
    y2 = 0.5 * (d - root)
    return math.sqrt(max(x2, 0.0)), math.sqrt(max(y2, 0.0))


def permutation_matrices() -> list[np.ndarray]:
    mats: list[np.ndarray] = []
    for perm in itertools.permutations(range(3)):
        mat = np.zeros((3, 3), dtype=complex)
        for i, j in enumerate(perm):
            mat[i, j] = 1.0
        mats.append(mat)
    return mats


def part1_single_higgs_and_repeated_charge_lanes_stay_cp_empty() -> None:
    print("\n" + "=" * 88)
    print("PART 1: SINGLE-HIGGS AND REPEATED-CHARGE LANES STAY CP-EMPTY")
    print("=" * 88)

    diag_entries = np.array([0.7 + 0.1j, 1.1 - 0.2j, 0.9 + 0.3j], dtype=complex)
    all_diagonal = True
    for q in range(3):
        y = single_higgs_y(diag_entries, q)
        k = right_gram(y)
        offdiag = k - np.diag(np.diag(k))
        all_diagonal &= np.max(np.abs(offdiag)) < 1e-12

    same_charge = two_higgs_y(
        np.array([0.5 + 0.2j, 0.7 - 0.1j, 0.9 + 0.3j], dtype=complex),
        1,
        np.array([0.2 - 0.3j, 0.4 + 0.1j, 0.3 - 0.2j], dtype=complex),
        1,
    )
    k_same = right_gram(same_charge)
    offdiag_same = k_same - np.diag(np.diag(k_same))

    check(
        "Every fixed-charge single-Higgs lane gives diagonal Y^dag Y",
        all_diagonal,
        "monomial support keeps the Hermitian kernel diagonal",
    )
    check(
        "A two-Higgs lane with repeated charge is still effectively single-Higgs",
        np.max(np.abs(offdiag_same)) < 1e-12,
        f"max offdiag={np.max(np.abs(offdiag_same)):.2e}",
    )

    print()
    print("  So one Higgs is too small, and repeating the same charge does not help.")


def part2_two_distinct_charges_are_the_first_local_escape() -> None:
    print("\n" + "=" * 88)
    print("PART 2: TWO DISTINCT HIGGS CHARGES ARE THE FIRST LOCAL ESCAPE")
    print("=" * 88)

    y = two_higgs_y(
        np.array([0.9 + 0.1j, 0.6 - 0.2j, 1.0 + 0.3j], dtype=complex),
        0,
        np.array([0.3 - 0.1j, 0.5 + 0.4j, 0.7 - 0.2j], dtype=complex),
        1,
    )
    k = right_gram(y)
    offdiag = k - np.diag(np.diag(k))
    support = np.abs(y) > 1e-12

    check(
        "A generic two-distinct-charge lane is not monomial",
        np.count_nonzero(support) == 6,
        f"support count={np.count_nonzero(support)}",
    )
    check(
        "Its right-Gram kernel is generically non-diagonal",
        np.max(np.abs(offdiag)) > 1e-6,
        f"max offdiag={np.max(np.abs(offdiag)):.6f}",
    )

    print()
    print("  So two distinct Higgs charges are the first exact local class that can")
    print("  support the non-diagonal Hermitian kernel leptogenesis needs.")


def part3_every_distinct_charge_pair_is_canonical_up_to_relabeling() -> None:
    print("\n" + "=" * 88)
    print("PART 3: EVERY DISTINCT-CHARGE PAIR REDUCES TO THE CANONICAL CLASS")
    print("=" * 88)

    perms = permutation_matrices()
    canonical = CYCLE
    all_reduce = True
    pairs = [(0, 1), (0, 2), (1, 2)]
    details = []
    for qa, qb in pairs:
        relative = perm_power(qb) @ perm_power(qa).conj().T
        found = any(np.allclose(p @ relative @ p.conj().T, canonical, atol=1e-12) for p in perms)
        details.append(f"{(qa, qb)}->{int(found)}")
        all_reduce &= found

    check(
        "Every distinct Higgs-charge pair is support-equivalent to A + B C",
        all_reduce,
        ", ".join(details),
    )

    print()
    print("  So the local escape is not an uncontrolled family of charge-pair cases.")
    print("  It is one canonical two-Higgs class up to relabeling.")


def part4_the_dm_cp_target_is_realized_on_that_unique_minimal_escape() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE DM CP TARGET LIVES ON THAT UNIQUE MINIMAL ESCAPE")
    print("=" * 88)

    mu = 1.0
    nu = 0.20
    eta = 0.10
    y_cp = minimal_cp_family(mu, nu, eta)
    k_cp = right_gram(y_cp)
    k_can, d, r, delta = canonicalize_circulant_right_gram(k_cp)
    solution = symmetric_two_higgs_solution(d, r)
    assert solution is not None
    x, y = solution
    y_two_higgs = canonical_two_higgs_y(x, y, delta)
    k_two_higgs = right_gram(y_two_higgs)
    single = single_higgs_y(np.array([math.sqrt(d), math.sqrt(d), math.sqrt(d)], dtype=complex), 0)
    k_single = right_gram(single)

    check(
        "The sample odd-circulant CP-supporting kernel lies on the admissible subcone",
        d >= 2.0 * r,
        f"d={d:.6f}, 2r={2.0*r:.6f}",
    )
    check(
        "That kernel is realized exactly on the canonical two-Higgs lane",
        np.linalg.norm(k_can - k_two_higgs) < 1e-10,
        f"realization error={np.linalg.norm(k_can - k_two_higgs):.2e}",
    )
    check(
        "The same kernel cannot come from the single-Higgs universal bridge",
        np.max(np.abs(k_can - k_single)) > 1e-3 and np.max(np.abs(k_can - np.diag(np.diag(k_can)))) > 1e-6,
        f"single-higgs mismatch={np.max(np.abs(k_can-k_single)):.6f}",
    )

    print()
    print("  So once nonzero local DM CP support is required, the canonical")
    print("  two-Higgs distinct-charge class is not just allowed. It is the unique")
    print("  minimal exact local escape on the current stack.")


def main() -> int:
    print("=" * 88)
    print("DM NEUTRINO TWO-HIGGS MINIMALITY THEOREM")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - DM leptogenesis universal-Yukawa no-go")
    print("  - DM minimal Z3 circulant CP tool")
    print("  - neutrino Dirac two-Higgs escape theorem")
    print("  - DM neutrino two-Higgs right-Gram bridge")
    print()
    print("Question:")
    print("  What is the unique minimal exact local Z3 extension that can supply")
    print("  the non-diagonal Hermitian kernel DM leptogenesis now needs?")

    part1_single_higgs_and_repeated_charge_lanes_stay_cp_empty()
    part2_two_distinct_charges_are_the_first_local_escape()
    part3_every_distinct_charge_pair_is_canonical_up_to_relabeling()
    part4_the_dm_cp_target_is_realized_on_that_unique_minimal_escape()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact DM-side minimality answer:")
    print("    - one Higgs is too small")
    print("    - repeated charges are still too small")
    print("    - two distinct Higgs charges are the unique minimal exact local escape")
    print("    - that escape is canonical up to relabeling")
    print("    - the DM CP-supporting right-Gram target already lives on it")
    print()
    print("  So the branch no longer needs to ask whether some other smaller local")
    print("  extension might rescue the denominator. There is no smaller exact one.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())

