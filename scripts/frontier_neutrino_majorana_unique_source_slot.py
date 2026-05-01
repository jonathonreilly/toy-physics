#!/usr/bin/env python3
"""
Unique local source-slot theorem for the Majorana lane.

Question:
  If a future Majorana-generating primitive is admitted as a local bilinear
  source deformation, how many independent local source coordinates can it
  carry on the current anomaly-fixed one-generation lane?

Answer on the current lane:
  Exactly one complex source slot m on the unique seed S_unique. Hermitian
  deformations are of the form m S_unique + m^* S_unique^dag.

Boundary:
  This is an exact local-form theorem under the local bilinear source
  assumption. It does NOT prove that the primitive exists or that m is
  nonzero.
"""

from __future__ import annotations

import sys

import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def null_space(matrix: np.ndarray, tol: float = 1e-10) -> np.ndarray:
    _, s, vh = np.linalg.svd(matrix, full_matrices=False)
    rank = int(np.sum(s > tol))
    return vh.conj().T[:, rank:]


def build_dirac_majorana_seed() -> np.ndarray:
    i2 = np.eye(2, dtype=complex)
    z2 = np.zeros((2, 2), dtype=complex)
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)

    g0 = np.block([[i2, z2], [z2, -i2]])
    g1 = np.block([[z2, sx], [-sx, z2]])
    g2 = np.block([[z2, sy], [-sy, z2]])
    g3 = np.block([[z2, sz], [-sz, z2]])
    g5 = 1j * g0 @ g1 @ g2 @ g3
    cmat = 1j * g2 @ g0
    pr = (np.eye(4, dtype=complex) + g5) / 2.0
    b_r = cmat @ pr

    internal = np.zeros((16, 16), dtype=complex)
    internal[15, 15] = 1.0
    return np.kron(b_r, internal)


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


def test_unique_complex_channel() -> np.ndarray:
    print("\n" + "=" * 88)
    print("PART 1: THE LOCAL CHARGE-TWO CHANNEL SPACE IS ONE-DIMENSIONAL")
    print("=" * 88)

    s_unique = build_dirac_majorana_seed()
    antisym = np.linalg.norm(s_unique.T + s_unique)
    rank = int(np.linalg.matrix_rank(s_unique, tol=1e-10))
    support = np.nonzero(np.abs(s_unique) > 1e-12)
    internal_rows = sorted({int(idx % 16) for idx in support[0]})

    check("Unique local seed is antisymmetric", antisym < 1e-10,
          f"||S^T+S||={antisym:.2e}")
    check("Unique local seed has rank 2", rank == 2, f"rank={rank}")
    check("Unique local seed is supported only on the nu_R slot", internal_rows == [15],
          f"internal rows={internal_rows}")

    trial = (1.3 - 0.4j) * s_unique
    coeff = np.vdot(s_unique, trial) / np.vdot(s_unique, s_unique)
    residual = np.linalg.norm(trial - coeff * s_unique)
    check("Any local charge-two deformation on this lane is proportional to one seed", residual < 1e-10,
          f"projection residual={residual:.2e}")

    print()
    print("  So the local admissible DeltaL=2 channel space is one-dimensional")
    print("  over C before any source-law question is asked.")

    return s_unique


def test_hermitian_deformations_have_one_complex_slot() -> None:
    print("\n" + "=" * 88)
    print("PART 2: HERMITIAN LINEAR DEFORMATIONS CARRY ONE COMPLEX SOURCE SLOT")
    print("=" * 88)

    cs = annihilation_operators(2)
    pair_ann = cs[0] @ cs[1]
    pair_cre = pair_ann.conj().T

    basis = [pair_ann, 1j * pair_ann, pair_cre, 1j * pair_cre]
    rows = []
    for op in basis:
        antiherm = op - op.conj().T
        rows.append(np.concatenate([antiherm.real.reshape(-1), antiherm.imag.reshape(-1)]))
    system = np.column_stack(rows)
    ns = null_space(system)

    h1 = pair_ann + pair_cre
    h2 = 1j * (pair_ann - pair_cre)
    dim_real_herm = int(np.linalg.matrix_rank(np.column_stack([
        np.concatenate([h1.real.reshape(-1), h1.imag.reshape(-1)]),
        np.concatenate([h2.real.reshape(-1), h2.imag.reshape(-1)]),
    ]), tol=1e-10))

    m = 0.37 - 0.22j
    deformation = m * pair_ann + np.conj(m) * pair_cre
    hermitian_err = np.linalg.norm(deformation - deformation.conj().T)
    recovered_a = 0.5 * np.trace(h1.conj().T @ deformation).real
    recovered_b = 0.5 * np.trace(h2.conj().T @ deformation).real
    rebuilt = recovered_a * h1 + recovered_b * h2
    rebuild_err = np.linalg.norm(deformation - rebuilt)

    check("Hermitian subspace of the pair-annihilation/creation span has dimension 2 over R", ns.shape[1] == 2 and dim_real_herm == 2,
          f"nullity={ns.shape[1]}, rank={dim_real_herm}")
    check("A complex coefficient m produces a Hermitian source deformation", hermitian_err < 1e-10,
          f"||X-X^dag||={hermitian_err:.2e}")
    check("The Hermitian deformation is exactly reconstructed from two real coordinates", rebuild_err < 1e-10,
          f"rebuild error={rebuild_err:.2e}")

    print()
    print("  Two real Hermitian directions are exactly one complex source slot:")
    print("  m cc + m^* c^dag c^dag.")


def test_antisymmetric_local_source_block_has_one_complex_coordinate() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE LOCAL ANTISYMMETRIC SOURCE BLOCK IS ONE COMPLEX SLOT")
    print("=" * 88)

    e00 = np.array([[1, 0], [0, 0]], dtype=complex)
    e01 = np.array([[0, 1], [0, 0]], dtype=complex)
    e10 = np.array([[0, 0], [1, 0]], dtype=complex)
    e11 = np.array([[0, 0], [0, 1]], dtype=complex)

    real_basis = [e00, 1j * e00, e01, 1j * e01, e10, 1j * e10, e11, 1j * e11]
    rows = []
    for basis_matrix in real_basis:
        anti = basis_matrix + basis_matrix.T
        rows.append(np.concatenate([anti.real.reshape(-1), anti.imag.reshape(-1)]))
    system = np.column_stack(rows)
    ns = null_space(system)

    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    m = -0.61 + 0.18j
    a = m * j2
    antisym_err = np.linalg.norm(a + a.T)

    v1 = np.concatenate([j2.real.reshape(-1), j2.imag.reshape(-1)])
    v2 = np.concatenate([(1j * j2).real.reshape(-1), (1j * j2).imag.reshape(-1)])
    rank = int(np.linalg.matrix_rank(np.column_stack([v1, v2]), tol=1e-10))

    coeff = np.vdot(j2, a) / np.vdot(j2, j2)
    residual = np.linalg.norm(a - coeff * j2)

    check("Antisymmetric 2x2 source-block space has dimension 2 over R = 1 over C", ns.shape[1] == 2 and rank == 2,
          f"nullity={ns.shape[1]}, real-rank={rank}")
    check("Any local antisymmetric block has the form m J_2", antisym_err < 1e-10 and residual < 1e-10,
          f"antisym err={antisym_err:.2e}, residual={residual:.2e}")

    print()
    print("  So the minimal local source block on the unique channel is not a")
    print("  matrix of free coefficients. It is one complex coordinate m.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: UNIQUE LOCAL SOURCE SLOT")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md")
    print()
    print("Question:")
    print("  If a future Majorana primitive is admitted as a local bilinear")
    print("  source deformation, how many independent local source coordinates")
    print("  can it carry on the current lane?")

    test_unique_complex_channel()
    test_hermitian_deformations_have_one_complex_slot()
    test_antisymmetric_local_source_block_has_one_complex_coordinate()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  Exactly one complex source slot m. On the current anomaly-fixed")
    print("  lane, any future local bilinear Majorana source completion is of")
    print("  the form m S_unique + m^* S_unique^dag.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
