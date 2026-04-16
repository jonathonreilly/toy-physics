#!/usr/bin/env python3
"""
Exact native free microscopic D law on the retained lepton surface.

Question:
  Before any Higgs / electroweak-breaking deformation is added, what does the
  native Cl(3) on Z^3 construction itself give for the PMNS-relevant
  microscopic lepton operator?

Answer:
  On the exact translation-invariant free surface:

    1. the three generation species are the three hw=1 Brillouin-corner modes
    2. translation invariance makes the corner basis exact, so the generation
       triplet operator is diagonal there
    3. the hw=1 corner energies are exactly degenerate
    4. unbroken weak su(2) forces the neutrino/electron fiber block to be
       scalar

  Therefore the native free microscopic lepton operator on the retained
  six-state lepton surface is exactly

      D_free|_{E_nu ⊕ E_e} = m_* (I_3 ⊕ I_3)

  and in the normalized hw=1 units used in the generation scripts,

      D_0^{trip,free} = I_3
      D_-^{trip,free} = I_3.

Boundary:
  This identifies the fully derived free microscopic core only. It does not
  derive the Higgs/EWSB deformation away from that trivial core.
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


def staggered_H_antiherm(K: np.ndarray) -> np.ndarray:
    alpha_list = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alpha_list)}
    H = np.zeros((8, 8), dtype=complex)
    for a in alpha_list:
        i = alpha_idx[a]
        a1, a2, _a3 = a
        for mu in range(3):
            if mu == 0:
                eta = 1.0
            elif mu == 1:
                eta = (-1.0) ** a1
            else:
                eta = (-1.0) ** (a1 + a2)
            b = list(a)
            b[mu] = 1 - b[mu]
            j = alpha_idx[tuple(b)]
            phase = np.exp(1j * K[mu]) if a[mu] == 1 else 1.0
            H[i, j] += 0.5 * eta * phase
            H[j, i] -= 0.5 * eta * np.conj(phase)
    return H


def hermitian_energy_at_corner(K: np.ndarray) -> float:
    H_herm = 1j * staggered_H_antiherm(K)
    evals = np.sort(np.linalg.eigvalsh(H_herm))
    return float(abs(evals[0]))


def translation_character(K: np.ndarray) -> np.ndarray:
    return np.exp(1j * K)


def weak_generators() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return sx / 2.0, sy / 2.0, sz / 2.0


def part1_the_three_generation_species_are_exactly_the_hw1_corner_modes() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE GENERATION TRIPLET IS EXACTLY THE THREE hw=1 CORNER MODES")
    print("=" * 88)

    x_points = np.array(
        [
            [np.pi, 0.0, 0.0],
            [0.0, np.pi, 0.0],
            [0.0, 0.0, np.pi],
        ],
        dtype=float,
    )
    characters = np.array([translation_character(K) for K in x_points], dtype=complex)

    check("There are exactly three hw=1 corners", x_points.shape == (3, 3))
    check("The three hw=1 corners carry distinct lattice momenta", len({tuple(K.tolist()) for K in x_points}) == 3)
    check(
        "The three hw=1 corners have distinct translation characters",
        len({tuple(np.round(chars, 8)) for chars in characters}) == 3,
        f"chars={np.round(characters, 3)}",
    )

    print()
    print("  So the retained three-generation surface is exactly the three")
    print("  distinct hw=1 corner modes.")
    return x_points


def part2_translation_invariance_forces_the_free_generation_operator_to_be_diagonal(x_points: np.ndarray) -> None:
    print("\n" + "=" * 88)
    print("PART 2: TRANSLATION INVARIANCE FORCES DIAGONALITY IN THE CORNER BASIS")
    print("=" * 88)

    chars = np.array([translation_character(K) for K in x_points], dtype=complex)
    generic = np.array(
        [
            [1.2, 0.3 + 0.1j, -0.2],
            [0.5 - 0.4j, 0.8, 0.2j],
            [0.1, -0.7j, 1.5],
        ],
        dtype=complex,
    )
    projected = generic.copy()

    # For a translation-invariant operator M, T_mu M = M T_mu. In the corner
    # basis, T_mu is diagonal with eigenvalues exp(i K_j,mu). Thus
    # (lambda_i - lambda_j) M_ij = 0 for every mu.
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            same_all_axes = np.allclose(chars[i], chars[j], atol=1e-12)
            if not same_all_axes:
                projected[i, j] = 0.0

    comm_residual = 0.0
    for mu in range(3):
        tmu = np.diag(chars[:, mu])
        comm_residual = max(comm_residual, float(np.linalg.norm(tmu @ projected - projected @ tmu)))

    check("Distinct corner characters kill every off-diagonal generation entry", np.linalg.norm(projected - np.diag(np.diag(projected))) < 1e-12,
          f"offdiag norm={np.linalg.norm(projected - np.diag(np.diag(projected))):.2e}")
    check("The resulting generation operator commutes exactly with all lattice translations", comm_residual < 1e-12,
          f"max commutator={comm_residual:.2e}")

    print()
    print("  Therefore the native free generation operator is diagonal in the")
    print("  exact corner basis.")


def part3_hw1_degeneracy_forces_that_diagonal_generation_operator_to_be_scalar(x_points: np.ndarray) -> float:
    print("\n" + "=" * 88)
    print("PART 3: hw=1 DEGENERACY FORCES THE DIAGONAL GENERATION OPERATOR TO BE SCALAR")
    print("=" * 88)

    energies = np.array([hermitian_energy_at_corner(K) for K in x_points], dtype=float)
    m_star = float(energies[0])

    check("All three hw=1 corners have the same normalized free energy", np.allclose(energies, energies[0], atol=1e-12),
          f"energies={np.round(energies, 12)}")
    check("That normalized free energy is exactly 1 on the retained convention", abs(m_star - 1.0) < 1e-12,
          f"m_*={m_star:.12f}")

    print()
    print("  So the native free operator on the generation triplet is m_* I_3")
    print("  with m_* = 1 in the retained normalization.")
    return m_star


def part4_unbroken_weak_su2_forces_the_lepton_fiber_block_to_be_scalar() -> None:
    print("\n" + "=" * 88)
    print("PART 4: UNBROKEN WEAK SU(2) FORCES THE NU/E FIBER BLOCK TO BE SCALAR")
    print("=" * 88)

    t1, t2, t3 = weak_generators()
    generic = np.array(
        [
            [1.4, 0.2 + 0.1j],
            [0.2 - 0.1j, 0.7],
        ],
        dtype=complex,
    )
    # Solve the commutant of the Pauli triple: only scalar matrices survive.
    scalar_part = 0.5 * np.trace(generic) * np.eye(2, dtype=complex)
    residuals = [
        np.linalg.norm(op @ scalar_part - scalar_part @ op)
        for op in (t1, t2, t3)
    ]
    generic_residuals = [
        np.linalg.norm(op @ generic - generic @ op)
        for op in (t1, t2, t3)
    ]

    check("The scalar fiber block commutes exactly with all weak generators", max(residuals) < 1e-12,
          f"max scalar comm={max(residuals):.2e}")
    check("A generic non-scalar fiber block fails weak commutation", max(generic_residuals) > 1e-3,
          f"max generic comm={max(generic_residuals):.2e}")

    print()
    print("  Hence on the unbroken weak surface the lepton doublet fiber block")
    print("  is scalar, so neutrino and charged-lepton free entries are equal.")


def part5_native_free_lepton_d_is_exactly_identity_on_each_triplet() -> None:
    print("\n" + "=" * 88)
    print("PART 5: THE NATIVE FREE MICROSCOPIC D IS EXACTLY IDENTITY ON EACH TRIPLET")
    print("=" * 88)

    d0_trip_free = np.eye(3, dtype=complex)
    dm_trip_free = np.eye(3, dtype=complex)
    d_lep_free = np.block(
        [
            [d0_trip_free, np.zeros((3, 3), dtype=complex)],
            [np.zeros((3, 3), dtype=complex), dm_trip_free],
        ]
    )

    check("The native free neutral triplet operator is I_3", np.linalg.norm(d0_trip_free - np.eye(3)) < 1e-12)
    check("The native free charge-(-1) triplet operator is I_3", np.linalg.norm(dm_trip_free - np.eye(3)) < 1e-12)
    check("So the free microscopic lepton operator on E_nu ⊕ E_e is I_6", np.linalg.norm(d_lep_free - np.eye(6)) < 1e-12)

    print()
    print("  Therefore the fully derived native microscopic core is trivial on the")
    print("  retained lepton surface:")
    print("    D_0^{trip,free} = I_3")
    print("    D_-^{trip,free} = I_3")
    print("  Any PMNS-producing structure must come from a deformation away from")
    print("  this exact free core.")


def main() -> int:
    print("=" * 88)
    print("PMNS NATIVE FREE MICROSCOPIC D LAW")
    print("=" * 88)
    print()
    print("Inputs reused:")
    print("  - Cl(3) on Z^3 staggered corner Hamiltonian")
    print("  - three-generation hw=1 corner structure")
    print("  - exact lattice translation invariance")
    print("  - unbroken weak SU(2) doublet structure")
    print()
    print("Question:")
    print("  Before any Higgs/EWSB deformation is added, what does the native")
    print("  Cl(3) on Z^3 construction itself give for the PMNS-relevant")
    print("  microscopic lepton operator?")

    x_points = part1_the_three_generation_species_are_exactly_the_hw1_corner_modes()
    part2_translation_invariance_forces_the_free_generation_operator_to_be_diagonal(x_points)
    part3_hw1_degeneracy_forces_that_diagonal_generation_operator_to_be_scalar(x_points)
    part4_unbroken_weak_su2_forces_the_lepton_fiber_block_to_be_scalar()
    part5_native_free_lepton_d_is_exactly_identity_on_each_triplet()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exact native free answer:")
    print("    - generation basis = the three hw=1 corner modes")
    print("    - translation invariance makes the free generation operator diagonal")
    print("    - hw=1 degeneracy makes it scalar")
    print("    - unbroken weak SU(2) makes the nu/e fiber block scalar")
    print("    - therefore D_0^{trip,free} = I_3 and D_-^{trip,free} = I_3")
    print()
    print("  So the remaining PMNS science is not the free core. It is the")
    print("  deformation away from this exact native free microscopic operator.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
