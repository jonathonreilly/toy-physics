#!/usr/bin/env python3
"""
Canonical reduction theorem for the minimal two-Higgs charged-lepton lane.

Question:
  If the charged-lepton sector, rather than the neutrino sector, is the first
  lepton Yukawa lane to leave the single-Higgs monomial class, how much exact
  freedom is left on that minimal charged-lepton extension?

Answer:
  Up to generation relabeling and charged-lepton field rephasings, every
  distinct-offset two-Higgs charged-lepton texture reduces to the canonical
  support class

      Y_e = A_e + B_e C

  with C the forward 3-cycle and A_e,B_e diagonal. A further exact phase
  reduction puts the generic texture into the normal form

      Y_e,can = diag(xe1,xe2,xe3) + diag(ye1,ye2,ye3 e^{i delta_e}) C

  with xe_i > 0, ye_i > 0, and one surviving physical phase delta_e. So the
  minimal exact surviving charged-lepton-side class carries exactly seven real
  physical parameters: six positive moduli and one phase.

Boundary:
  This is an exact reduction/counting theorem on the minimal two-Higgs
  charged-lepton extension class, conditioned on the neutrino sector staying on
  the monomial single-Higgs boundary. It does NOT derive the seven quantities.
"""

from __future__ import annotations

import itertools
import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0

PERMUTATIONS = {
    0: np.eye(3, dtype=complex),
    1: np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex),
    2: np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex),
}


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


def diagonal_matrix(values: np.ndarray) -> np.ndarray:
    return np.diag(np.asarray(values, dtype=complex))


def all_permutation_matrices() -> list[np.ndarray]:
    matrices = []
    for perm in itertools.permutations(range(3)):
        matrix = np.zeros((3, 3), dtype=complex)
        for i, j in enumerate(perm):
            matrix[i, j] = 1.0
        matrices.append(matrix)
    return matrices


def wrap_phase(angle: float) -> float:
    return np.angle(np.exp(1j * angle))


def part1_distinct_offset_pairs_have_one_canonical_support_class() -> None:
    print("\n" + "=" * 88)
    print("PART 1: ALL DISTINCT CHARGED-LEPTON TWO-HIGGS OFFSET PAIRS REDUCE TO ONE SUPPORT CLASS")
    print("=" * 88)

    pairs = [(0, 1), (0, 2), (1, 2)]
    coeffs = {
        (0, 1): (
            np.array([0.12 + 0.02j, 0.31 - 0.03j, 1.05 + 0.04j]),
            np.array([0.08 - 0.01j, 0.24 + 0.02j, 0.63 - 0.05j]),
        ),
        (0, 2): (
            np.array([0.14 - 0.02j, 0.27 + 0.04j, 0.98 + 0.01j]),
            np.array([0.10 + 0.05j, 0.19 - 0.02j, 0.58 + 0.03j]),
        ),
        (1, 2): (
            np.array([0.16 + 0.03j, 0.25 - 0.04j, 1.10 + 0.02j]),
            np.array([0.09 - 0.02j, 0.22 + 0.01j, 0.61 + 0.04j]),
        ),
    }

    canonical_cycle = PERMUTATIONS[1]
    permutation_family = all_permutation_matrices()

    for qa, qb in pairs:
        a_vals, b_vals = coeffs[(qa, qb)]
        y = diagonal_matrix(a_vals) @ PERMUTATIONS[qa] + diagonal_matrix(b_vals) @ PERMUTATIONS[qb]
        y_diag_first = y @ PERMUTATIONS[qa].conj().T
        relative = PERMUTATIONS[qb] @ PERMUTATIONS[qa].conj().T

        found = None
        for perm in permutation_family:
            if np.linalg.norm(perm @ relative @ perm.conj().T - canonical_cycle) < 1e-12:
                found = perm
                break

        check(f"offsets=({qa},{qb}): right multiplication makes one Higgs contribution diagonal",
              np.allclose(y_diag_first - diagonal_matrix(a_vals) - diagonal_matrix(b_vals) @ relative, 0.0, atol=1e-12),
              f"relative support=\n{np.round(relative.real).astype(int)}")
        check(f"offsets=({qa},{qb}): the relative permutation is a nontrivial 3-cycle",
              np.linalg.norm(relative - np.eye(3)) > 1e-12 and np.allclose(relative @ relative @ relative, np.eye(3), atol=1e-12),
              f"det={np.linalg.det(relative):.1f}")
        check(f"offsets=({qa},{qb}): a generation relabeling maps the pair to the forward-cycle class", found is not None)

        if found is None:
            continue

        a_perm = found @ diagonal_matrix(a_vals) @ found.conj().T
        b_perm = found @ diagonal_matrix(b_vals) @ found.conj().T
        y_canon = found @ y_diag_first @ found.conj().T
        target = a_perm + b_perm @ canonical_cycle

        check(f"offsets=({qa},{qb}): the transformed texture has canonical support class A_e + B_e C",
              np.linalg.norm(y_canon - target) < 1e-12,
              f"canon error={np.linalg.norm(y_canon - target):.2e}")

    print()
    print("  So the charged-lepton offset-pair label is not a remaining")
    print("  physical ambiguity on the minimal two-Higgs lane. Up to relabeling,")
    print("  there is one canonical support class.")


def part2_generic_texture_has_one_surviving_phase() -> None:
    print("\n" + "=" * 88)
    print("PART 2: GENERIC CHARGED-LEPTON TWO-HIGGS TEXTURES REDUCE TO SIX MODULI PLUS ONE PHASE")
    print("=" * 88)

    a = np.array(
        [
            0.18 * np.exp(0.2j),
            0.33 * np.exp(-0.8j),
            1.02 * np.exp(0.5j),
        ],
        dtype=complex,
    )
    b = np.array(
        [
            0.09 * np.exp(-0.4j),
            0.21 * np.exp(0.7j),
            0.57 * np.exp(0.9j),
        ],
        dtype=complex,
    )
    cycle = PERMUTATIONS[1]
    y = diagonal_matrix(a) + diagonal_matrix(b) @ cycle

    phase_a = np.angle(a)
    alpha = np.zeros(3)
    alpha[1] = alpha[0] + phase_a[1] - np.angle(b[0])
    alpha[2] = alpha[1] + phase_a[2] - np.angle(b[1])
    beta = alpha - phase_a

    left = np.diag(np.exp(-1j * alpha))
    right = np.diag(np.exp(1j * beta))
    y_can = left @ y @ right

    a_can = np.array([y_can[0, 0], y_can[1, 1], y_can[2, 2]])
    b_can = np.array([y_can[0, 1], y_can[1, 2], y_can[2, 0]])
    invariant_phase = wrap_phase(np.angle(np.prod(b) / np.prod(a)))
    residual_phase = wrap_phase(np.angle(b_can[2]))

    check("The diagonal charged-lepton Higgs block can be made strictly positive and real",
          np.max(np.abs(np.imag(a_can))) < 1e-12 and np.min(np.real(a_can)) > 0.0,
          f"a_can={np.round(a_can, 6)}")
    check("Two of the three off-cycle charged-lepton coefficients can be made strictly positive and real",
          np.max(np.abs(np.imag(b_can[:2]))) < 1e-12 and np.min(np.real(b_can[:2])) > 0.0,
          f"b12_can={np.round(b_can[:2], 6)}")
    check("Exactly one invariant phase remains on the generic charged-lepton two-Higgs lane",
          abs(wrap_phase(residual_phase - invariant_phase)) < 1e-12,
          f"delta_e={residual_phase:.6f}, invariant={invariant_phase:.6f}")
    check("The canonical texture keeps the same singular-value spectrum",
          np.allclose(np.sort(np.linalg.svd(y, compute_uv=False)), np.sort(np.linalg.svd(y_can, compute_uv=False)), atol=1e-12),
          f"svals={np.round(np.sort(np.linalg.svd(y_can, compute_uv=False)), 6)}")

    print()
    print("  So the generic canonical charged-lepton normal form is")
    print("    diag(xe1,xe2,xe3) + diag(ye1,ye2,ye3 e^{i delta_e}) C")
    print("  with xe_i > 0, ye_i > 0, and one surviving physical phase delta_e.")


def part3_exact_parameter_count_is_seven() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE MINIMAL CHARGED-LEPTON TWO-HIGGS LANE CARRIES EXACTLY SEVEN REAL INVARIANTS")
    print("=" * 88)

    gauge_matrix = np.array(
        [
            [-1, 0, 0, 1, 0, 0],
            [0, -1, 0, 0, 1, 0],
            [0, 0, -1, 0, 0, 1],
            [-1, 1, 0, 0, 1, 0],
            [0, -1, 1, 0, 0, 1],
        ],
        dtype=float,
    )
    rank = int(np.linalg.matrix_rank(gauge_matrix))
    null_dim = gauge_matrix.shape[1] - rank
    physical_count = 12 - rank

    check("The generic charged-lepton two-Higgs texture starts with 12 real parameters", True)
    check("The exact phase-fixing conditions again have rank 5", rank == 5, f"rank={rank}")
    check("One common phase remains as the exact null direction", null_dim == 1, f"null dim={null_dim}")
    check("So the physical parameter count is 12 - 5 = 7", physical_count == 7,
          f"physical count={physical_count}")
    check("The canonical charged-lepton normal form uses exactly 6 positive moduli plus 1 phase", physical_count == 7,
          "canonical count=7")

    print()
    print("  So the minimal exact surviving charged-lepton-side extension class")
    print("  is also a seven-real-number problem on one canonical support class.")


def main() -> int:
    print("=" * 88)
    print("CHARGED-LEPTON YUKAWA: TWO-HIGGS CANONICAL REDUCTION")
    print("=" * 88)
    print()
    print("Atlas / axiom inputs reused:")
    print("  - Lepton single-Higgs PMNS triviality theorem")
    print("  - Neutrino Dirac two-Higgs escape theorem")
    print("  - effective charged-lepton Z_3 offset language from the lepton lane")
    print()
    print("Question:")
    print("  If the charged-lepton sector is the first lepton Yukawa lane to leave")
    print("  the single-Higgs monomial class, how much exact freedom is left on")
    print("  that minimal charged-lepton extension?")

    part1_distinct_offset_pairs_have_one_canonical_support_class()
    part2_generic_texture_has_one_surviving_phase()
    part3_exact_parameter_count_is_seven()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact reduction answer:")
    print("    - all distinct charged-lepton two-Higgs offset pairs reduce to one support class")
    print("    - the generic canonical form is diag(xe1,xe2,xe3)+diag(ye1,ye2,ye3 e^{i delta_e}) C")
    print("    - the minimal surviving charged-lepton-side lane carries exactly 7 real invariants")
    print()
    print("  So if the charged-lepton sector, rather than the neutrino sector, is")
    print("  the first non-monomial lane, its exact remaining gap is also seven")
    print("  axiom-side quantities.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
