#!/usr/bin/env python3
"""
Minimal two-Higgs escape from the single-Higgs monomial no-mixing theorem.

Question:
  What is the smallest exact neutrino-side extension that can evade the
  single-Higgs fixed-q_H monomial no-mixing theorem?

Answer:
  A two-Higgs Z_3 sector with distinct Higgs charges. If
      Y_nu = D_a P_a + D_b P_b
  with P_a != P_b coming from two distinct Higgs Z_3 charges, then Y_nu is no
  longer monomial. Generically Y_nu Y_nu^dag acquires off-diagonal terms, so
  nontrivial left mixing becomes available.

Boundary:
  This is an exact extension-class theorem. It identifies the minimal exact
  neutrino-side escape from the single-Higgs obstruction, but does not derive
  the actual Higgs charges or coefficients.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


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


PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
}


def is_monomial(matrix: np.ndarray, tol: float = 1e-12) -> bool:
    nonzero_rows = np.count_nonzero(np.abs(matrix) > tol, axis=1)
    nonzero_cols = np.count_nonzero(np.abs(matrix) > tol, axis=0)
    return np.all(nonzero_rows <= 1) and np.all(nonzero_cols <= 1)


def part1_single_higgs_is_exactly_obstructed() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ONE FIXED HIGGS CHARGE STAYS ON THE MONOMIAL NO-MIXING LANE")
    print("=" * 88)

    coeffs = np.array([0.03, 0.07, 0.11], dtype=complex)

    for q_h, perm in PERMUTATIONS.items():
        y = np.diag(coeffs) @ perm
        gram = y @ y.conj().T
        offdiag = np.linalg.norm(gram - np.diag(np.diag(gram)))
        check(f"q_H={q_h}: single-Higgs texture is monomial", is_monomial(y))
        check(f"q_H={q_h}: single-Higgs Y Y^dag is diagonal", offdiag < 1e-12,
              f"offdiag norm={offdiag:.2e}")

    print()
    print("  So no one-Higgs fixed-q_H case can escape the exact monomial")
    print("  no-mixing theorem.")


def part2_two_distinct_higgs_charges_break_monomiality() -> None:
    print("\n" + "=" * 88)
    print("PART 2: TWO DISTINCT HIGGS CHARGES GENERICALLY BREAK MONOMIALITY")
    print("=" * 88)

    pairs = [(0, 1), (0, 2), (1, 2)]
    coeff_sets = {
        (0, 1): (np.array([0.03, 0.07, 0.11], dtype=complex), np.array([0.05, 0.04, 0.09], dtype=complex)),
        (0, 2): (np.array([0.03, 0.08, 0.12], dtype=complex), np.array([0.06, 0.05, 0.07], dtype=complex)),
        (1, 2): (np.array([0.04, 0.09, 0.13], dtype=complex), np.array([0.05, 0.02, 0.10], dtype=complex)),
    }

    for qa, qb in pairs:
        da, db = coeff_sets[(qa, qb)]
        ya = np.diag(da) @ PERMUTATIONS[qa]
        yb = np.diag(db) @ PERMUTATIONS[qb]
        y = ya + yb
        support_size = int(np.count_nonzero(np.abs(y) > 1e-12))
        cross_perm = PERMUTATIONS[qa] @ PERMUTATIONS[qb].conj().T
        diag_err = np.linalg.norm(np.diag(np.diag(cross_perm)))

        check(f"q_H=({qa},{qb}): two-Higgs texture is not monomial", not is_monomial(y),
              f"support size={support_size}")
        check(f"q_H=({qa},{qb}): union support has 6 exact slots", support_size == 6,
              f"support size={support_size}")
        check(f"q_H=({qa},{qb}): relative permutation is off-diagonal", diag_err < 1e-12,
              f"diag norm={diag_err:.2e}")

    print()
    print("  Distinct Higgs charges therefore form the smallest support-level")
    print("  escape from the monomial lane.")


def part3_two_higgs_generically_induce_left_mixing() -> None:
    print("\n" + "=" * 88)
    print("PART 3: TWO-HIGGS TEXTURES GENERICALLY GIVE NONTRIVIAL LEFT MIXING")
    print("=" * 88)

    pairs = [(0, 1), (0, 2), (1, 2)]
    coeff_sets = {
        (0, 1): (np.array([0.03, 0.07, 0.11], dtype=complex), np.array([0.05, 0.04, 0.09], dtype=complex)),
        (0, 2): (np.array([0.03, 0.08, 0.12], dtype=complex), np.array([0.06, 0.05, 0.07], dtype=complex)),
        (1, 2): (np.array([0.04, 0.09, 0.13], dtype=complex), np.array([0.05, 0.02, 0.10], dtype=complex)),
    }

    for qa, qb in pairs:
        da, db = coeff_sets[(qa, qb)]
        y = np.diag(da) @ PERMUTATIONS[qa] + np.diag(db) @ PERMUTATIONS[qb]
        gram = y @ y.conj().T
        offdiag = np.linalg.norm(gram - np.diag(np.diag(gram)))
        u, _, _ = np.linalg.svd(y)
        abs_u = np.abs(u)
        max_row_nonzero = np.max(np.sum(abs_u > 1e-4, axis=1))
        max_col_nonzero = np.max(np.sum(abs_u > 1e-4, axis=0))

        check(f"q_H=({qa},{qb}): Y Y^dag is generically non-diagonal", offdiag > 1e-6,
              f"offdiag norm={offdiag:.6f}")
        check(f"q_H=({qa},{qb}): left singular vectors are not just permutations/phases",
              max_row_nonzero > 1 and max_col_nonzero > 1,
              f"|U|=\n{np.round(abs_u, 6)}")

    print()
    print("  So a two-Higgs neutrino Dirac sector with distinct Z_3 charges is")
    print("  the minimal exact extension class that can evade the one-Higgs")
    print("  no-mixing obstruction on the neutrino side.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO DIRAC YUKAWA: TWO-HIGGS MINIMAL ESCAPE")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Neutrino Dirac Z_3 support trichotomy")
    print("  - Neutrino Dirac monomial no-mixing theorem")
    print("  - two Higgs doublets with distinct Z_3 charges")
    print()
    print("Question:")
    print("  What is the smallest exact neutrino-side extension that can evade")
    print("  the single-Higgs monomial no-mixing theorem?")

    part1_single_higgs_is_exactly_obstructed()
    part2_two_distinct_higgs_charges_break_monomiality()
    part3_two_higgs_generically_induce_left_mixing()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact extension-class answer:")
    print("    - one fixed Higgs charge: exact no-mixing obstruction")
    print("    - two distinct Higgs charges: minimal support-level escape")
    print("    - generically, two-Higgs textures produce nontrivial left mixing")
    print()
    print("  So the smallest exact neutrino-side extension class that survives")
    print("  the current no-mixing chain is a two-Higgs Z_3 sector.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
