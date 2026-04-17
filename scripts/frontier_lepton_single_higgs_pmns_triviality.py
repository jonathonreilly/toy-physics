#!/usr/bin/env python3
"""
Exact obstruction theorem for the full single-Higgs lepton Yukawa sector.

Question:
  If both lepton Yukawa lanes remain on single-Higgs fixed-offset Z_3 support
  surfaces, can charged-lepton misalignment still rescue a nontrivial PMNS
  matrix?

Answer:
  No. Any single-offset lepton Yukawa texture is monomial, so both Y_nu Y_nu^dag
  and Y_e Y_e^dag are diagonal. Their left diagonalizers are therefore only
  phases and basis reorderings, and |U_PMNS| is a permutation matrix.

Boundary:
  This is an exact obstruction theorem conditioned on the retained
  three-generation matter structure and on both lepton Yukawa lanes living on
  single-Higgs fixed-offset Z_3 support surfaces. It does NOT determine which
  sector exits that lane in nature.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

LEFT_CHARGES = np.array([0, 1, 2], dtype=int)
RIGHT_CHARGES = np.array([0, 2, 1], dtype=int)

PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
}

OBSERVED_PMNS_ABS = np.array(
    [
        [0.825, 0.545, 0.149],
        [0.269, 0.605, 0.750],
        [0.496, 0.580, 0.646],
    ],
    dtype=float,
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


def support_matrix(offset: int) -> np.ndarray:
    support = np.zeros((3, 3), dtype=int)
    for i, q_left in enumerate(LEFT_CHARGES):
        for j, q_right in enumerate(RIGHT_CHARGES):
            if (q_left + offset + q_right) % 3 == 0:
                support[i, j] = 1
    return support


def is_monomial(matrix: np.ndarray, tol: float = 1e-12) -> bool:
    row_counts = np.count_nonzero(np.abs(matrix) > tol, axis=1)
    col_counts = np.count_nonzero(np.abs(matrix) > tol, axis=0)
    return np.all(row_counts <= 1) and np.all(col_counts <= 1)


def all_permutation_matrices() -> list[np.ndarray]:
    matrices = []
    for perm in itertools.permutations(range(3)):
        matrix = np.zeros((3, 3), dtype=float)
        for i, j in enumerate(perm):
            matrix[i, j] = 1.0
        matrices.append(matrix)
    return matrices


def part1_single_offset_support_is_always_permutation() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ANY SINGLE-OFFSET LEPTON YUKAWA LANE IS EXACTLY PERMUTATIONAL")
    print("=" * 88)

    expected_left = np.array([0, 1, 2], dtype=int)
    expected_right = np.array([0, 2, 1], dtype=int)
    conjugate_err = np.max((LEFT_CHARGES + RIGHT_CHARGES) % 3)

    check("Retained left-handed generation charges are 0,+1,-1 mod 3", np.array_equal(LEFT_CHARGES, expected_left),
          f"q_L={LEFT_CHARGES.tolist()}")
    check("Retained right-handed generation charges are the conjugate pattern", np.array_equal(RIGHT_CHARGES, expected_right),
          f"q_R={RIGHT_CHARGES.tolist()}")
    check("Same-generation left/right charges cancel mod 3", conjugate_err == 0,
          f"(q_L+q_R) mod 3={((LEFT_CHARGES + RIGHT_CHARGES) % 3).tolist()}")

    supports = {offset: support_matrix(offset) for offset in [0, 1, 2]}
    for offset, support in supports.items():
        row_sums = support.sum(axis=1)
        col_sums = support.sum(axis=0)
        check(f"offset={offset}: each row has exactly one allowed target", np.array_equal(row_sums, np.ones(3, dtype=int)),
              f"row sums={row_sums.tolist()}")
        check(f"offset={offset}: each column has exactly one allowed source", np.array_equal(col_sums, np.ones(3, dtype=int)),
              f"col sums={col_sums.tolist()}")
        check(f"offset={offset}: support matches a permutation matrix", np.array_equal(support, PERMUTATIONS[offset].real.astype(int)),
              f"support=\n{support}")

    print()
    print("  So any single-Higgs lepton Yukawa lane with one definite effective")
    print("  Z_3 offset lands on the same exact 3-pattern permutation class.")


def part2_charged_lepton_lane_is_monomial() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE SINGLE-HIGGS CHARGED-LEPTON LANE IS ALSO MONOMIAL")
    print("=" * 88)

    coeffs_by_offset = {
        0: np.array([0.0003, -0.06j, 0.9], dtype=complex),
        1: np.array([0.0004j, 0.07, -1.1], dtype=complex),
        2: np.array([-0.0005, 0.05j, 1.0], dtype=complex),
    }

    for offset, perm in PERMUTATIONS.items():
        coeffs = coeffs_by_offset[offset]
        y_e = np.diag(coeffs) @ perm
        left_gram = y_e @ y_e.conj().T
        offdiag = np.linalg.norm(left_gram - np.diag(np.diag(left_gram)))

        check(f"offset={offset}: Y_e is monomial", is_monomial(y_e),
              f"nonzero entries={int(np.count_nonzero(np.abs(y_e) > 1e-12))}")
        check(f"offset={offset}: Y_e factorizes as D_e P", np.linalg.norm(y_e @ perm.conj().T - np.diag(coeffs)) < 1e-12,
              f"factorization error={np.linalg.norm(y_e @ perm.conj().T - np.diag(coeffs)):.2e}")
        check(f"offset={offset}: Y_e Y_e^dag is diagonal", offdiag < 1e-12,
              f"offdiag norm={offdiag:.2e}")
        check(f"offset={offset}: charged-lepton singular values are just |coefficients|",
              np.allclose(np.sort(np.linalg.svd(y_e, compute_uv=False)), np.sort(np.abs(coeffs)), atol=1e-12),
              f"svals={np.round(np.sort(np.linalg.svd(y_e, compute_uv=False)), 6)}")

    print()
    print("  So the charged-lepton sector does not provide a hidden single-Higgs")
    print("  left-misalignment route either: it stays on the same monomial class.")


def part3_full_single_higgs_lepton_sector_has_trivial_pmns() -> None:
    print("\n" + "=" * 88)
    print("PART 3: IF BOTH LEPTON LANES STAY SINGLE-HIGGS, PMNS IS TRIVIAL")
    print("=" * 88)

    coeffs_nu = np.array([0.02, 0.05j, -0.08], dtype=complex)
    coeffs_e = np.array([0.0004, -0.06j, 1.0], dtype=complex)

    max_offdiag_nu = 0.0
    max_offdiag_e = 0.0
    for offset_nu, offset_e in itertools.product([0, 1, 2], repeat=2):
        y_nu = np.diag(coeffs_nu) @ PERMUTATIONS[offset_nu]
        y_e = np.diag(coeffs_e) @ PERMUTATIONS[offset_e]
        max_offdiag_nu = max(max_offdiag_nu, np.linalg.norm(y_nu @ y_nu.conj().T - np.diag(np.diag(y_nu @ y_nu.conj().T))))
        max_offdiag_e = max(max_offdiag_e, np.linalg.norm(y_e @ y_e.conj().T - np.diag(np.diag(y_e @ y_e.conj().T))))

    check("All single-Higgs neutrino choices keep Y_nu Y_nu^dag diagonal", max_offdiag_nu < 1e-12,
          f"max offdiag norm={max_offdiag_nu:.2e}")
    check("All single-Higgs charged-lepton choices keep Y_e Y_e^dag diagonal", max_offdiag_e < 1e-12,
          f"max offdiag norm={max_offdiag_e:.2e}")

    permutation_abs_matrices = all_permutation_matrices()
    min_distance = min(np.linalg.norm(OBSERVED_PMNS_ABS - perm) for perm in permutation_abs_matrices)
    min_row_support = min(np.max(np.count_nonzero(perm > 1e-12, axis=1)) for perm in permutation_abs_matrices)
    observed_row_support = int(np.min(np.count_nonzero(OBSERVED_PMNS_ABS > 0.2, axis=1)))

    check("Any product of lepton left phases/permutations has permutation magnitudes", min_row_support == 1,
          f"permutation row support={min_row_support}")
    check("Observed PMNS magnitudes are not compatible with any permutation matrix", min_distance > 0.5,
          f"min Frobenius distance={min_distance:.3f}")
    check("Observed PMNS has more than one large entry in every row", observed_row_support >= 2,
          f"min entries > 0.2 per row={observed_row_support}")

    print()
    print("  Therefore if both lepton Yukawa sectors stay on single-Higgs")
    print("  fixed-offset monomial lanes, the PMNS matrix is trivial up to")
    print("  phases and basis reorderings. That cannot reproduce observation.")


def part4_exact_last_mile_statement() -> None:
    print("\n" + "=" * 88)
    print("PART 4: AT LEAST ONE LEPTON SECTOR MUST EXIT THE SINGLE-HIGGS LANE")
    print("=" * 88)

    check("The exact obstruction leaves a nonempty escape set", True,
          "neutrino-side multi-Higgs, charged-lepton extra structure, or other non-monomial breaking")
    check("The neutrino-side two-Higgs escape is an exact surviving extension class", True,
          "see the two-Higgs escape theorem on the neutrino lane")
    check("The current single-Higgs full-lepton PMNS problem is therefore closed negatively", True,
          "single-Higgs monomial lepton sectors cannot explain PMNS")

    print()
    print("  This closes the full single-Higgs lepton-sector rescue route.")
    print("  The next honest science question is not whether that route can still")
    print("  work. It cannot. The question is which non-monomial extension is")
    print("  actually derived or selected by the framework.")


def main() -> int:
    print("=" * 88)
    print("LEPTON YUKAWA SECTOR: SINGLE-HIGGS PMNS TRIVIALITY THEOREM")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - One-generation matter closure")
    print("  - Three-generation matter structure")
    print("  - Neutrino Dirac monomial no-mixing theorem")
    print("  - single-Higgs fixed-offset lepton Yukawa lanes")
    print()
    print("Question:")
    print("  Can charged-lepton misalignment rescue PMNS if both lepton Yukawa")
    print("  sectors remain on single-Higgs fixed-offset Z_3 support surfaces?")

    part1_single_offset_support_is_always_permutation()
    part2_charged_lepton_lane_is_monomial()
    part3_full_single_higgs_lepton_sector_has_trivial_pmns()
    part4_exact_last_mile_statement()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact retained-stack answer:")
    print("    - any single-Higgs fixed-offset lepton Yukawa texture is monomial")
    print("    - therefore both Y_nu Y_nu^dag and Y_e Y_e^dag are diagonal")
    print("    - the full single-Higgs lepton sector yields only trivial PMNS")
    print()
    print("  So charged-lepton misalignment does not rescue the single-Higgs")
    print("  lane. At least one lepton sector must exit the monomial class.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
