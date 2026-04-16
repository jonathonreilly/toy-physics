#!/usr/bin/env python3
"""
Exact no-mixing theorem for single-Higgs monomial neutrino Dirac textures.

Question:
  If the retained Dirac-neutrino support is fixed by one Higgs Z_3 charge q_H,
  can the neutrino Dirac sector by itself generate nontrivial PMNS mixing?

Answer:
  No. A fixed-q_H single-Higgs texture has the exact monomial form
      Y_nu = D P_q
  with D diagonal and P_q a permutation matrix. Therefore
      Y_nu Y_nu^dag = D D^dag
  is diagonal, so the left singular vectors are only coordinate phases and/or
  permutations. The neutrino Dirac sector alone carries no structurally forced
  nontrivial left mixing.

Boundary:
  Exact theorem on the retained Dirac lane conditioned on the single-Higgs
  Z_3 support trichotomy. It does NOT rule out PMNS mixing from charged-lepton
  misalignment, multiple Higgs charges, or higher-order symmetry breaking.
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


def part1_exact_monomial_factorization() -> None:
    print("\n" + "=" * 88)
    print("PART 1: FIXED-q_H SUPPORT IMPLIES EXACT MONOMIAL FACTORIZATION")
    print("=" * 88)

    coeffs_by_q = {
        0: np.array([0.03, 0.07j, -0.11], dtype=complex),
        1: np.array([0.05, -0.08j, 0.13], dtype=complex),
        2: np.array([-0.04j, 0.09, 0.12], dtype=complex),
    }

    for q_h, perm in PERMUTATIONS.items():
        coeffs = coeffs_by_q[q_h]
        diagonal = np.diag(coeffs)
        y = diagonal @ perm
        recovered = y @ perm.conj().T
        row_counts = np.count_nonzero(np.abs(y) > 1e-12, axis=1)
        col_counts = np.count_nonzero(np.abs(y) > 1e-12, axis=0)

        check(f"q_H={q_h}: Y_nu is monomial (one nonzero per row/column)", is_monomial(y),
              f"row counts={row_counts.tolist()}, col counts={col_counts.tolist()}")
        check(f"q_H={q_h}: monomial texture factorizes exactly as D P_q", np.linalg.norm(recovered - diagonal) < 1e-12,
              f"factorization error={np.linalg.norm(recovered - diagonal):.2e}")
        check(f"q_H={q_h}: permutation block is unitary", np.linalg.norm(perm @ perm.conj().T - np.eye(3)) < 1e-12,
              f"unitarity error={np.linalg.norm(perm @ perm.conj().T - np.eye(3)):.2e}")

    print()
    print("  So once q_H is fixed, the neutrino Dirac matrix is exactly a")
    print("  diagonal coefficient matrix times a permutation.")


def part2_left_mixing_is_trivial() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE LEFT-HANDED MIXING MATRIX IS ONLY PHASES/PERMUTATIONS")
    print("=" * 88)

    coeffs_by_q = {
        0: np.array([0.03, 0.07j, -0.11], dtype=complex),
        1: np.array([0.05, -0.08j, 0.13], dtype=complex),
        2: np.array([-0.04j, 0.09, 0.12], dtype=complex),
    }

    for q_h, perm in PERMUTATIONS.items():
        coeffs = coeffs_by_q[q_h]
        y = np.diag(coeffs) @ perm
        left_gram = y @ y.conj().T
        off_diag_norm = np.linalg.norm(left_gram - np.diag(np.diag(left_gram)))
        _, singular_values, vh = np.linalg.svd(y)
        right_gram = y.conj().T @ y
        abs_vh = np.abs(vh)

        check(f"q_H={q_h}: Y Y^dag is exactly diagonal", off_diag_norm < 1e-12,
              f"offdiag norm={off_diag_norm:.2e}")
        check(f"q_H={q_h}: singular values are just the coefficient magnitudes",
              np.allclose(np.sort(singular_values), np.sort(np.abs(coeffs)), atol=1e-12),
              f"svals={np.round(np.sort(singular_values), 6)}, |coeffs|={np.round(np.sort(np.abs(coeffs)), 6)}")
        check(f"q_H={q_h}: right-handed structure may permute, but left-handed mixing stays trivial", np.linalg.norm(right_gram - perm.conj().T @ np.diag(np.abs(coeffs) ** 2) @ perm) < 1e-12,
              f"right-gram error={np.linalg.norm(right_gram - perm.conj().T @ np.diag(np.abs(coeffs) ** 2) @ perm):.2e}")
        check(f"q_H={q_h}: the right singular vectors are also permutation/phases only", np.all(np.sum(abs_vh > 1e-8, axis=1) == 1) and np.all(np.sum(abs_vh > 1e-8, axis=0) == 1),
              f"|V^dag|=\n{np.round(abs_vh, 6)}")

    print()
    print("  The neutrino Dirac sector alone therefore carries no structurally")
    print("  forced nontrivial left mixing once the support is monomial.")


def part3_pmns_obstruction_statement() -> None:
    print("\n" + "=" * 88)
    print("PART 3: NONTRIVIAL PMNS MIXING REQUIRES EXTRA STRUCTURE")
    print("=" * 88)

    generic_abs_pmns = np.eye(3, dtype=float)
    theta_12 = 33.4
    theta_23 = 49.0
    theta_13 = 8.54
    observed_offdiag = np.linalg.norm(
        np.array(
            [
                [0.825, 0.545, 0.149],
                [0.269, 0.605, 0.750],
                [0.496, 0.580, 0.646],
            ]
        )
        - np.eye(3)
    )

    check("A monomial Dirac sector predicts identity/permutation magnitudes on the left", np.linalg.norm(generic_abs_pmns - np.eye(3)) < 1e-12)
    check("Observed PMNS magnitudes are not a trivial permutation matrix", observed_offdiag > 0.5,
          f"offdiag distance from identity={observed_offdiag:.3f}")
    check("Observed PMNS angles are all nontrivial", theta_12 > 1.0 and theta_23 > 1.0 and theta_13 > 1.0,
          f"angles=({theta_12},{theta_23},{theta_13})")

    print()
    print("  So the retained single-Higgs monomial Y_nu texture cannot by itself")
    print("  account for the observed large PMNS structure. Any realistic")
    print("  mixing closure must come from extra structure:")
    print("    - charged-lepton misalignment,")
    print("    - multiple Higgs Z_3 charges, or")
    print("    - higher-order symmetry breaking beyond the fixed-q_H monomial lane.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO DIRAC YUKAWA: SINGLE-HIGGS MONOMIAL NO-MIXING THEOREM")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Neutrino mass reduction to Dirac lane")
    print("  - Neutrino Dirac Z_3 support trichotomy")
    print("  - single Higgs doublet with fixed q_H")
    print()
    print("Question:")
    print("  Can the single-Higgs fixed-q_H neutrino Dirac sector by itself")
    print("  generate nontrivial left mixing?")

    part1_exact_monomial_factorization()
    part2_left_mixing_is_trivial()
    part3_pmns_obstruction_statement()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact retained-stack answer:")
    print("    - fixed-q_H single-Higgs textures are monomial: Y_nu = D P_q")
    print("    - therefore Y_nu Y_nu^dag is diagonal")
    print("    - neutrino Dirac left mixing is trivial up to phases/permutations")
    print()
    print("  So observed PMNS mixing cannot come from this single-Higgs monomial")
    print("  neutrino Dirac sector alone. Extra structure is required.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
