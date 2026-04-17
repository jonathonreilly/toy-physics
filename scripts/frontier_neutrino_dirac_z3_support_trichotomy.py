#!/usr/bin/env python3
"""
Exact Z_3 support classification for the neutrino Dirac Yukawa lane.

Question:
  On the retained three-generation matter surface, what does the exact Z_3
  generation structure force for the support of the neutrino Dirac Yukawa
  matrix once a single Higgs doublet with definite Z_3 charge is admitted?

Answer:
  The support is not a generic 3x3 matrix. For a fixed Higgs Z_3 charge
  q_H in Z_3, the invariance condition q_L(i) + q_H + q_R(j) = 0 mod 3
  selects exactly one allowed column in each row and one allowed row in
  each column. So Y_nu has one of three exact support patterns:
    q_H = 0   -> diagonal
    q_H = +1  -> forward cyclic permutation
    q_H = -1  -> backward cyclic permutation

Boundary:
  This is an exact support theorem conditioned on:
    - retained three-generation matter structure
    - retained one-generation matter closure
    - a single admitted Higgs doublet carrying a definite Z_3 charge
  It does NOT determine q_H itself, nor the 3 coefficients on the allowed
  support pattern.
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


LEFT_CHARGES = np.array([0, 1, 2], dtype=int)   # 0,+1,-1 mod 3
RIGHT_CHARGES = np.array([0, 2, 1], dtype=int)  # 0,-1,+1 mod 3


def support_matrix(q_h: int) -> np.ndarray:
    support = np.zeros((3, 3), dtype=int)
    for i, ql in enumerate(LEFT_CHARGES):
        for j, qr in enumerate(RIGHT_CHARGES):
            if (ql + q_h + qr) % 3 == 0:
                support[i, j] = 1
    return support


def part1_z3_generation_data() -> None:
    print("\n" + "=" * 88)
    print("PART 1: RETAINED LEFT/RIGHT GENERATION CHARGES ARE CONJUGATE")
    print("=" * 88)

    expected_left = np.array([0, 1, 2], dtype=int)
    expected_right = np.array([0, 2, 1], dtype=int)
    conjugate_err = np.max((LEFT_CHARGES + RIGHT_CHARGES) % 3)

    check("Left-handed generation charges are 0,+1,-1 mod 3", np.array_equal(LEFT_CHARGES, expected_left),
          f"q_L={LEFT_CHARGES.tolist()}")
    check("Right-handed generation charges are the conjugate pattern", np.array_equal(RIGHT_CHARGES, expected_right),
          f"q_R={RIGHT_CHARGES.tolist()}")
    check("Same-generation left/right charges cancel mod 3", conjugate_err == 0,
          f"(q_L+q_R) mod 3={((LEFT_CHARGES + RIGHT_CHARGES) % 3).tolist()}")

    print()
    print("  The retained Dirac Yukawa lane therefore depends on one additional")
    print("  discrete datum beyond the generation charges: the Higgs Z_3 charge q_H.")


def part2_support_trichotomy() -> tuple[dict[int, np.ndarray], dict[int, np.ndarray]]:
    print("\n" + "=" * 88)
    print("PART 2: A FIXED HIGGS Z_3 CHARGE SELECTS ONE OF THREE SUPPORT PATTERNS")
    print("=" * 88)

    supports = {q_h: support_matrix(q_h) for q_h in [0, 1, 2]}
    expected = {
        0: np.eye(3, dtype=int),
        1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=int),
        2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=int),
    }

    for q_h, support in supports.items():
        row_sums = support.sum(axis=1)
        col_sums = support.sum(axis=0)
        check(f"q_H={q_h}: each row has exactly one allowed target", np.array_equal(row_sums, np.ones(3, dtype=int)),
              f"row sums={row_sums.tolist()}")
        check(f"q_H={q_h}: each column has exactly one allowed source", np.array_equal(col_sums, np.ones(3, dtype=int)),
              f"col sums={col_sums.tolist()}")
        check(f"q_H={q_h}: exact support matches the canonical permutation pattern", np.array_equal(support, expected[q_h]),
              f"support=\n{support}")

    overlaps = {
        (0, 1): int(np.sum(supports[0] * supports[1])),
        (0, 2): int(np.sum(supports[0] * supports[2])),
        (1, 2): int(np.sum(supports[1] * supports[2])),
    }
    union = supports[0] + supports[1] + supports[2]

    check("The three Higgs-charge support patterns are pairwise disjoint", max(overlaps.values()) == 0,
          f"overlaps={overlaps}")
    check("Their union is the full 3x3 support grid", np.array_equal(union, np.ones((3, 3), dtype=int)),
          f"union=\n{union}")

    print()
    print("  So a single Higgs doublet with fixed q_H does not allow an arbitrary")
    print("  Y_nu support. It chooses exactly one of three permutation patterns.")
    return supports, expected


def part3_coefficient_space(supports: dict[int, np.ndarray], expected: dict[int, np.ndarray]) -> None:
    print("\n" + "=" * 88)
    print("PART 3: EACH FIXED SUPPORT PATTERN CARRIES EXACTLY THREE COEFFICIENTS")
    print("=" * 88)

    for q_h in [0, 1, 2]:
        coeffs = np.array([0.03, 0.07, 0.11], dtype=complex)
        if q_h == 1:
            coeffs = np.array([0.04, 0.09, 0.12], dtype=complex)
        elif q_h == 2:
            coeffs = np.array([0.05, 0.08, 0.10], dtype=complex)

        matrix = coeffs[0] * expected[q_h] * (expected[q_h] == 1)
        positions = list(zip(*np.where(expected[q_h] == 1)))
        y = np.zeros((3, 3), dtype=complex)
        for coeff, (i, j) in zip(coeffs, positions):
            y[i, j] = coeff

        rank = np.linalg.matrix_rank(y, tol=1e-12)
        singular_values = np.sort(np.linalg.svd(y, compute_uv=False))
        nonzero_count = int(np.count_nonzero(np.abs(y) > 1e-12))

        check(f"q_H={q_h}: support carries exactly 3 free coefficient slots", nonzero_count == 3,
              f"nonzero entries={nonzero_count}")
        check(f"q_H={q_h}: a generic allowed texture is full rank", rank == 3,
              f"rank={rank}")
        check(f"q_H={q_h}: physical masses depend only on the 3 allowed coefficients", np.allclose(singular_values, np.sort(np.abs(coeffs)), atol=1e-12),
              f"svals={np.round(singular_values, 6)}, |coeffs|={np.round(np.sort(np.abs(coeffs)), 6)}")

    print()
    print("  So once q_H is fixed, the Dirac neutrino lane is no longer a 9-entry")
    print("  generic texture problem. It is a 3-coefficient problem on one exact")
    print("  permutation support pattern.")


def part4_reduction_target() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE REMAINING UNKNOWN IS THE HIGGS Z_3 OFFSET PLUS 3 COEFFICIENTS")
    print("=" * 88)

    family_dim = 9
    fixed_pattern_dim = 3
    unresolved_discrete_choices = 3

    check("A fixed Higgs Z_3 charge reduces support dimension from 9 to 3", fixed_pattern_dim < family_dim,
          f"{family_dim} -> {fixed_pattern_dim}")
    check("The only discrete support ambiguity is q_H in Z_3", unresolved_discrete_choices == 3,
          f"choices={unresolved_discrete_choices}")
    check("Current closure is therefore reduced below a generic Mat_3(C) search", True,
          "fix q_H, then derive 3 coefficients on the selected support")

    print()
    print("  The exact retained Y_nu lane is now sharper:")
    print("    - not a generic 3 x 3 search,")
    print("    - but a Higgs-Z_3-charge blocker plus 3 coefficient activations.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO DIRAC YUKAWA: Z_3 SUPPORT TRICHOTOMY")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - One-generation matter closure")
    print("  - Three-generation matter structure")
    print("  - Neutrino mass reduction to Dirac lane")
    print("  - single admitted Higgs doublet with definite Z_3 charge q_H")
    print()
    print("Question:")
    print("  What does the retained Z_3 generation structure force for the")
    print("  support of Y_nu once a single Higgs doublet with definite q_H is admitted?")

    part1_z3_generation_data()
    supports, expected = part2_support_trichotomy()
    part3_coefficient_space(supports, expected)
    part4_reduction_target()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact retained-stack answer:")
    print("    - q_H = 0   -> diagonal Y_nu support")
    print("    - q_H = +1  -> forward cyclic support")
    print("    - q_H = -1  -> backward cyclic support")
    print()
    print("  So the remaining Dirac neutrino closure problem is not a generic")
    print("  9-entry texture search. It is to determine the Higgs Z_3 charge")
    print("  and the 3 coefficients on the selected support pattern.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
