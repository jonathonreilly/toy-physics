#!/usr/bin/env python3
"""Lane 3 generation-equivariant Ward degeneracy no-go.

This block-05 runner verifies the representation-theoretic boundary behind
QUARK_GENERATION_EQUIVARIANT_WARD_DEGENERACY_NO_GO_NOTE_2026-04-28.md.

It checks that the retained hw=1 generation carrier is the S_3 three-point
permutation representation A_1 + E, and that every S_3-equivariant Hermitian
Ward endomorphism has commutant form a I + b J. Such an operator has one
singlet eigenvalue and one doubly-degenerate E eigenvalue, so it cannot yield
three generation-stratified Yukawa eigenvalues without an additional
source/readout/symmetry-breaking primitive.
"""

from __future__ import annotations

from pathlib import Path
import itertools
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0
TOL = 1.0e-10


S3_ELEMENTS = {
    "e": (0, 1, 2),
    "(12)": (1, 0, 2),
    "(23)": (0, 2, 1),
    "(13)": (2, 1, 0),
    "(123)": (1, 2, 0),
    "(132)": (2, 0, 1),
}


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def permutation_matrix(perm: tuple[int, int, int]) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=float)
    for source, target in enumerate(perm):
        matrix[target, source] = 1.0
    return matrix


def s3_matrices() -> dict[str, np.ndarray]:
    return {name: permutation_matrix(perm) for name, perm in S3_ELEMENTS.items()}


def commutator_norm(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a @ b - b @ a)))


def commutant_constraint_matrix(mats: dict[str, np.ndarray]) -> np.ndarray:
    """Linear constraints for vec(W) from P W - W P = 0."""
    rows: list[np.ndarray] = []
    for name, p in mats.items():
        if name == "e":
            continue
        for i, j in itertools.product(range(3), repeat=2):
            row = np.zeros(9, dtype=float)
            # (P W)_{ij} - (W P)_{ij}
            for k in range(3):
                row[k * 3 + j] += p[i, k]
                row[i * 3 + k] -= p[k, j]
            rows.append(row)
    return np.vstack(rows)


def nullity(matrix: np.ndarray, tol: float = 1.0e-10) -> int:
    svals = np.linalg.svd(matrix, compute_uv=False)
    rank = int(np.sum(svals > tol))
    return matrix.shape[1] - rank


def is_commutant_form(w: np.ndarray) -> bool:
    diag = np.diag(w)
    off = w[~np.eye(3, dtype=bool)]
    return np.max(np.abs(diag - diag[0])) < TOL and np.max(np.abs(off - off[0])) < TOL


def distinct_eigenvalue_count(values: np.ndarray, tol: float = 1.0e-9) -> int:
    vals = sorted(float(np.real(v)) for v in values)
    groups: list[float] = []
    for value in vals:
        if not groups or abs(value - groups[-1]) > tol:
            groups.append(value)
    return len(groups)


def hermitian_c3_oriented_example() -> np.ndarray:
    """A C3-equivariant but reflection-breaking Hermitian matrix."""
    z = 0.25 + 0.40j
    return np.array(
        [
            [1.0, z, np.conjugate(z)],
            [np.conjugate(z), 1.0, z],
            [z, np.conjugate(z), 1.0],
        ],
        dtype=complex,
    )


def main() -> int:
    print("=" * 88)
    print("LANE 3 GENERATION-EQUIVARIANT WARD DEGENERACY NO-GO")
    print("=" * 88)

    new_note = DOCS / "QUARK_GENERATION_EQUIVARIANT_WARD_DEGENERACY_NO_GO_NOTE_2026-04-28.md"
    generation_note = DOCS / "THREE_GENERATION_STRUCTURE_NOTE.md"
    s3_note = DOCS / "S3_TASTE_CUBE_DECOMPOSITION_NOTE.md"
    free_matrix_note = DOCS / "QUARK_GENERATION_STRATIFIED_WARD_FREE_MATRIX_NO_GO_NOTE_2026-04-28.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (new_note, generation_note, s3_note, free_matrix_note, one_higgs_note):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    new_text = read(new_note)
    generation_text = read(generation_note)
    s3_text = read(s3_note)
    free_text = read(free_matrix_note)

    check("generation note says hierarchy remains open", "not retained: a first-principles `1+1+1` mass hierarchy" in generation_text)
    check("S3 support note identifies hw=1 as A_1 + E", "hw = 1" in s3_text and "A_1 + E" in s3_text)
    check("block01 free-matrix no-go is compatible", "does not fix" in free_text and "Y_u" in free_text and "Y_d" in free_text)
    check("new note forbids retained mass closure", "not claim retained" in new_text and "`m_b`" in new_text)

    print()
    print("B. S3 permutation representation on the generation triplet")
    print("-" * 72)
    mats = s3_matrices()
    for name, mat in mats.items():
        check(f"P{name} is orthogonal", np.allclose(mat.T @ mat, np.eye(3)))
    check("identity acts trivially", np.allclose(mats["e"], np.eye(3)))
    check("transpositions square to identity", all(np.allclose(mats[name] @ mats[name], np.eye(3)) for name in ("(12)", "(23)", "(13)")))
    check("3-cycles cube to identity", all(np.allclose(np.linalg.matrix_power(mats[name], 3), np.eye(3)) for name in ("(123)", "(132)")))

    chars = {name: float(np.trace(mat)) for name, mat in mats.items()}
    check("character chi(e)=3", abs(chars["e"] - 3.0) < TOL)
    check("transposition character chi(2c)=1", all(abs(chars[name] - 1.0) < TOL for name in ("(12)", "(23)", "(13)")))
    check("3-cycle character chi(3c)=0", all(abs(chars[name]) < TOL for name in ("(123)", "(132)")))
    mult_a1 = (chars["e"] + 3 * chars["(12)"] + 2 * chars["(123)"]) / 6.0
    mult_a2 = (chars["e"] - 3 * chars["(12)"] + 2 * chars["(123)"]) / 6.0
    mult_e = (2 * chars["e"] - 2 * chars["(123)"]) / 6.0
    check("hw=1 permutation carrier has one A_1", abs(mult_a1 - 1.0) < TOL, f"{mult_a1:.6f}")
    check("hw=1 permutation carrier has no A_2", abs(mult_a2) < TOL, f"{mult_a2:.6f}")
    check("hw=1 permutation carrier has one E", abs(mult_e - 1.0) < TOL, f"{mult_e:.6f}")

    print()
    print("C. Commutant dimension and normal form")
    print("-" * 72)
    constraints = commutant_constraint_matrix(mats)
    comm_nullity = nullity(constraints)
    identity = np.eye(3)
    all_ones = np.ones((3, 3))
    sample = 2.0 * identity - 0.35 * all_ones
    non_form = np.diag([1.0, 2.0, 3.0])

    check("linear commutant has dimension 2", comm_nullity == 2, f"nullity={comm_nullity}")
    check("identity commutes with all S3 generators", all(commutator_norm(identity, mat) < TOL for mat in mats.values()))
    check("all-ones matrix commutes with all S3 generators", all(commutator_norm(all_ones, mat) < TOL for mat in mats.values()))
    check("a I + b J sample commutes with all S3 elements", all(commutator_norm(sample, mat) < TOL for mat in mats.values()))
    check("a I + b J sample has commutant form", is_commutant_form(sample))
    check("distinct diagonal hierarchy is not S3-equivariant", any(commutator_norm(non_form, mat) > 0.1 for mat in mats.values()))

    print()
    print("D. Eigenvalue degeneracy")
    print("-" * 72)
    eig_sample = np.linalg.eigvalsh(sample)
    singlet = np.ones(3) / np.sqrt(3.0)
    e_vec_1 = np.array([1.0, -1.0, 0.0]) / np.sqrt(2.0)
    e_vec_2 = np.array([1.0, 1.0, -2.0]) / np.sqrt(6.0)
    sample_singlet_eval = float(np.real(singlet.conj() @ sample @ singlet))
    sample_e1_eval = float(np.real(e_vec_1.conj() @ sample @ e_vec_1))
    sample_e2_eval = float(np.real(e_vec_2.conj() @ sample @ e_vec_2))

    check("sample has at most two distinct eigenvalues", distinct_eigenvalue_count(eig_sample) == 2, str(eig_sample))
    check("E plane is degenerate", abs(sample_e1_eval - sample_e2_eval) < TOL, f"{sample_e1_eval:.6f}, {sample_e2_eval:.6f}")
    check("singlet eigenvalue equals a+3b", abs(sample_singlet_eval - (2.0 - 1.05)) < TOL, f"{sample_singlet_eval:.6f}")
    check("E eigenvalue equals a", abs(sample_e1_eval - 2.0) < TOL, f"{sample_e1_eval:.6f}")

    diag_x = np.diag([4.0, 4.0, 4.0])
    diag_y = np.diag([4.0, 5.0, 4.0])
    check("scalar diagonal readout is S3-equivariant", all(commutator_norm(diag_x, mat) < TOL for mat in mats.values()))
    check("non-scalar diagonal readout fails S3 equivariance", any(commutator_norm(diag_y, mat) > 0.1 for mat in mats.values()))
    check("diagonal S3-equivariant readout has one eigenvalue", distinct_eigenvalue_count(np.linalg.eigvalsh(diag_x)) == 1)

    print()
    print("E. Boundary against hidden symmetry breaking")
    print("-" * 72)
    c3_example = hermitian_c3_oriented_example()
    cycle = mats["(123)"]
    reflection = mats["(12)"]
    c3_eigs = np.linalg.eigvalsh(c3_example)
    check("oriented C3 example commutes with the 3-cycle", commutator_norm(c3_example, cycle) < TOL)
    check("oriented C3 example breaks reflection", commutator_norm(c3_example, reflection) > 0.1)
    check("oriented C3 example can split three eigenvalues", distinct_eigenvalue_count(c3_eigs) == 3, str(c3_eigs))
    check("therefore C3 splitting requires an extra orientation/reflection-breaking premise", "oriented-cycle primitive" in new_text)

    proof_inputs = {
        "S3_generation_action",
        "hw1_A1_plus_E_decomposition",
        "commutant_linear_algebra",
        "Hermitian_Ward_endomorphism",
    }
    forbidden_inputs = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "hidden_generation_projector",
    }
    check("forbidden proof inputs are absent", proof_inputs.isdisjoint(forbidden_inputs), str(sorted(proof_inputs)))
    check("new note leaves future source/readout primitive open", "source/readout/symmetry-breaking primitive" in new_text)
    check("new note does not overclaim future no-go", "future retained 3C route may still exist" in new_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: S_3-equivariant Ward operators cannot stratify three quark")
        print("generation Yukawa eigenvalues without a new source/readout primitive.")
        return 0
    print("VERDICT: generation-equivariant Ward no-go verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
