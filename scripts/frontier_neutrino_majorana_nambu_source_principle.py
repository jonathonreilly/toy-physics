#!/usr/bin/env python3
"""
Majorana Nambu source principle on the unique local nu_R block.

Question:
  After the current retained stack is exhausted, is there a smallest exact
  extension principle that forces the missing charge-2 source direction into
  the local quadratic grammar rather than adding it by hand?

Answer on the local anomaly-fixed block:
  Yes, if the local quadratic source grammar is required to be closed under
  CAR-preserving canonical basis changes. On the unique two-mode nu_R block,
  the charge-zero density source and the unique charge-2 pairing source form
  one exact pseudospin su(2). The retained normal slice span{J_z} is not
  closed under those local canonical rotations, while the full Nambu-complete
  span{J_x, J_y, J_z} is.

Boundary:
  This is an exact beyond-retained-stack source principle on the unique local
  block. It forces the charge-2 source direction into the admissible local
  grammar once canonical-basis closure is imposed. It does NOT yet fix the
  absolute amplitude / staircase scale or the full A/B/epsilon texture. The
  later source-ray theorem refines the one-generation direction question.
"""

from __future__ import annotations

import math
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


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def annihilation_operators(n_modes: int) -> list[np.ndarray]:
    sigma_minus = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    ident = np.eye(2, dtype=complex)

    operators: list[np.ndarray] = []
    for mode in range(n_modes):
        op = np.array([[1.0]], dtype=complex)
        for idx in range(n_modes):
            if idx < mode:
                op = np.kron(op, sigma_z)
            elif idx == mode:
                op = np.kron(op, sigma_minus)
            else:
                op = np.kron(op, ident)
        operators.append(op)
    return operators


def unitary_from_generator(generator: np.ndarray, theta: float) -> np.ndarray:
    evals, evecs = np.linalg.eigh(generator)
    phases = np.diag(np.exp(-1j * theta * evals))
    return evecs @ phases @ evecs.conj().T


def coeffs_in_basis(operator: np.ndarray, basis: list[np.ndarray]) -> np.ndarray:
    gram = np.array(
        [[np.trace(bi.conj().T @ bj) for bj in basis] for bi in basis],
        dtype=complex,
    )
    rhs = np.array([np.trace(bi.conj().T @ operator) for bi in basis], dtype=complex)
    return np.linalg.solve(gram, rhs)


def local_block_generators() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    cs = annihilation_operators(2)
    c1, c2 = cs
    n1 = c1.conj().T @ c1
    n2 = c2.conj().T @ c2
    ident = np.eye(c1.shape[0], dtype=complex)

    pair_ann = c1 @ c2
    pair_cre = pair_ann.conj().T

    jx = 0.5 * (pair_ann + pair_cre)
    jy = (pair_cre - pair_ann) / (2.0j)
    jz = 0.5 * (n1 + n2 - ident)
    n_tot = n1 + n2
    return jx, jy, jz, n_tot, pair_ann, pair_cre


def test_pseudospin_su2_closure() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIQUE LOCAL NORMAL AND PAIRING DIRECTIONS FORM ONE SU(2)")
    print("=" * 88)

    jx, jy, jz, n_tot, pair_ann, pair_cre = local_block_generators()

    herm_err = max(
        np.linalg.norm(jx - jx.conj().T),
        np.linalg.norm(jy - jy.conj().T),
        np.linalg.norm(jz - jz.conj().T),
    )
    comm_xy = np.linalg.norm(commutator(jx, jy) - 1j * jz)
    comm_yz = np.linalg.norm(commutator(jy, jz) - 1j * jx)
    comm_zx = np.linalg.norm(commutator(jz, jx) - 1j * jy)

    charge_ann = np.linalg.norm(commutator(n_tot, pair_ann) + 2.0 * pair_ann)
    charge_cre = np.linalg.norm(commutator(n_tot, pair_cre) - 2.0 * pair_cre)
    charge_z = np.linalg.norm(commutator(n_tot, jz))

    check("Local generators J_x, J_y, J_z are Hermitian", herm_err < 1e-12,
          f"max Hermiticity error={herm_err:.2e}")
    check("The local quadratic block closes as [J_x, J_y] = i J_z", comm_xy < 1e-12,
          f"error={comm_xy:.2e}")
    check("The local quadratic block closes as [J_y, J_z] = i J_x", comm_yz < 1e-12,
          f"error={comm_yz:.2e}")
    check("The local quadratic block closes as [J_z, J_x] = i J_y", comm_zx < 1e-12,
          f"error={comm_zx:.2e}")
    check("The pairing annihilation direction carries charge -2", charge_ann < 1e-12,
          f"error={charge_ann:.2e}")
    check("The pairing creation direction carries charge +2", charge_cre < 1e-12,
          f"error={charge_cre:.2e}")
    check("The normal direction J_z is charge zero", charge_z < 1e-12,
          f"error={charge_z:.2e}")

    print()
    print("  So the local anomaly-fixed nu_R block is not naturally split into")
    print("  unrelated normal and pairing sectors. They are one exact pseudospin")
    print("  su(2) quadratic algebra.")

    return jx, jy, jz, n_tot, pair_ann, pair_cre


def test_unique_complex_pairing_slot_is_the_transverse_plane() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE CHARGE-TWO SOURCE IS EXACTLY ONE COMPLEX TRANSVERSE SLOT")
    print("=" * 88)

    jx, jy, _, _, pair_ann, pair_cre = local_block_generators()

    m = 0.37 - 0.22j
    transverse = (m.real * 2.0) * jx + (m.imag * 2.0) * jy
    rebuilt = m * pair_ann + np.conj(m) * pair_cre
    rebuild_err = np.linalg.norm(transverse - rebuilt)

    coeff_ann = np.trace(pair_ann.conj().T @ rebuilt) / np.trace(pair_ann.conj().T @ pair_ann)
    coeff_cre = np.trace(pair_cre.conj().T @ rebuilt) / np.trace(pair_cre.conj().T @ pair_cre)

    check("The transverse J_x/J_y plane is exactly the unique complex pairing slot", rebuild_err < 1e-12,
          f"rebuild error={rebuild_err:.2e}")
    check("The reconstructed Hermitian source carries one complex coefficient m", abs(coeff_ann - m) < 1e-12 and abs(coeff_cre - np.conj(m)) < 1e-12,
          f"coeff_ann={coeff_ann}, coeff_cre={coeff_cre}")

    print()
    print("  This matches the unique-source-slot theorem in a basis-closed form:")
    print("  the two real pairing directions are the transverse pseudospin plane.")


def test_normal_slice_is_not_canonically_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE RETAINED NORMAL SLICE IS NOT CLOSED UNDER LOCAL CANONICAL ROTATIONS")
    print("=" * 88)

    jx, jy, jz, _, _, _ = local_block_generators()
    theta = math.pi / 2.0
    u = unitary_from_generator(jx, theta)
    rotated = u @ jz @ u.conj().T
    coeffs = coeffs_in_basis(rotated, [jx, jy, jz])
    normal_residual = np.linalg.norm(rotated - coeffs[2] * jz)
    target_err = np.linalg.norm(rotated + jy)

    check("A local Bogoliubov rotation of J_z leaves the normal slice", normal_residual > 1e-3,
          f"residual outside span{{J_z}}={normal_residual:.6f}")
    check("At theta = pi/2, J_z rotates exactly into a pairing direction", target_err < 1e-12,
          f"target error={target_err:.2e}")

    print()
    print("  So restricting the local quadratic grammar to charge-zero J_z only")
    print("  is a basis choice, not a canonically closed local source principle.")


def test_full_nambu_span_is_canonically_closed() -> None:
    print("\n" + "=" * 88)
    print("PART 4: THE MINIMAL CANONICALLY CLOSED LOCAL SOURCE GRAMMAR IS NAMBU-COMPLETE")
    print("=" * 88)

    jx, jy, jz, _, _, _ = local_block_generators()
    basis = [jx, jy, jz]
    max_outside = 0.0
    max_norm_err = 0.0

    for generator in [jx, jy, jz]:
        for theta in [0.2, 0.7, 1.1]:
            u = unitary_from_generator(generator, theta)
            for operator in basis:
                rotated = u @ operator @ u.conj().T
                coeffs = coeffs_in_basis(rotated, basis)
                rebuilt = coeffs[0] * jx + coeffs[1] * jy + coeffs[2] * jz
                outside = np.linalg.norm(rotated - rebuilt)
                max_outside = max(max_outside, outside)
                max_norm_err = max(max_norm_err, abs(np.linalg.norm(coeffs) - 1.0))

    check("The full span{J_x, J_y, J_z} is closed under local canonical rotations", max_outside < 1e-12,
          f"max outside error={max_outside:.2e}")
    check("Those rotations act as norm-preserving SO(3) adjoint motions on the source vector", max_norm_err < 1e-12,
          f"max norm error={max_norm_err:.2e}")

    print()
    print("  So the minimal canonically closed local quadratic source family is")
    print("  the full pseudospin triplet, not the retained charge-zero slice.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: NAMBU SOURCE PRINCIPLE")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CURRENT_STACK_EXHAUSTION_NOTE.md")
    print()
    print("Question:")
    print("  Is there a smallest exact beyond-retained-stack source principle")
    print("  that forces the unique charge-2 Majorana direction into the local")
    print("  quadratic grammar on the anomaly-fixed nu_R block?")

    test_pseudospin_su2_closure()
    test_unique_complex_pairing_slot_is_the_transverse_plane()
    test_normal_slice_is_not_canonically_closed()
    test_full_nambu_span_is_canonically_closed()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Yes. Once the local quadratic source grammar is required to be")
    print("  closed under CAR-preserving canonical basis changes, the minimal")
    print("  admissible source family on the unique nu_R block is the Nambu-")
    print("  complete pseudospin span{J_x, J_y, J_z}. The current normal slice")
    print("  span{J_z} is not closed under those rotations, while the transverse")
    print("  J_x/J_y plane is exactly the unique complex charge-2 source slot.")
    print()
    print("  This forces the existence of the charge-2 source direction as part")
    print("  of the admissible local source grammar beyond the retained stack.")
    print("  What remains open is the absolute amplitude / staircase embedding,")
    print("  not the existence of the local Nambu source family.")
    print()
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 1 if FAIL_COUNT else 0


if __name__ == "__main__":
    sys.exit(main())
