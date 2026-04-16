#!/usr/bin/env python3
"""
One-generation phase-removal theorem for the local Majorana source slot.

Question:
  On the current one-generation Majorana lane, does the unique local source
  slot m carry a physical phase, or can it be rephased to one real amplitude?

Answer on the current lane:
  The phase is removable. Because the unique source acts on the gauge singlet
  nu_R, the deformation m S_unique + m^* S_unique^dag is equivalent under
  local nu_R rephasing to |m| (S_unique + S_unique^dag). The invariant local
  datum is mu = |m|.

Boundary:
  This is an exact one-generation local-form theorem. It does NOT prove the
  primitive exists or address multi-generation relative Majorana phases.
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


def number_operator(cs: list[np.ndarray]) -> np.ndarray:
    dim = cs[0].shape[0]
    out = np.zeros((dim, dim), dtype=complex)
    for c in cs:
        out += c.conj().T @ c
    return out


def rotation_from_number(n_tot: np.ndarray, theta: float) -> np.ndarray:
    evals, vecs = np.linalg.eigh(n_tot)
    phase = np.exp(1j * theta * evals)
    return vecs @ np.diag(phase) @ vecs.conj().T


def rotate(op: np.ndarray, n_tot: np.ndarray, theta: float) -> np.ndarray:
    u = rotation_from_number(n_tot, theta)
    return u @ op @ u.conj().T


def pfaffian_2x2(matrix: np.ndarray) -> complex:
    return matrix[0, 1]


def logabs_pf_2x2(matrix: np.ndarray) -> float:
    return float(np.log(abs(pfaffian_2x2(matrix))))


def build_internal_generators():
    n = 16
    generators = []

    lam = []
    lam.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    lam.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
    lam.append((1.0 / np.sqrt(3.0)) * np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex))

    for idx, matrix in enumerate(lam, start=1):
        gen = np.zeros((n, n), dtype=complex)
        t = matrix / 2.0
        gen[0:3, 0:3] = t
        gen[3:6, 3:6] = t
        gen[8:11, 8:11] = t
        gen[11:14, 11:14] = t
        generators.append((f"SU3_{idx}", gen))

    sx = np.array([[0, 1], [1, 0]], dtype=complex) / 2.0
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex) / 2.0
    sz = np.array([[1, 0], [0, -1]], dtype=complex) / 2.0
    i3 = np.eye(3, dtype=complex)

    for name, s in [("SU2_1", sx), ("SU2_2", sy), ("SU2_3", sz)]:
        gen = np.zeros((n, n), dtype=complex)
        gen[0:6, 0:6] = np.kron(s, i3)
        gen[6:8, 6:8] = s
        generators.append((name, gen))

    y = np.diag([1 / 3] * 6 + [-1] * 2 + [4 / 3] * 3 + [-2 / 3] * 3 + [-2] + [0]).astype(complex)
    generators.append(("Y", y))
    return generators


def test_nu_r_is_gauge_singlet() -> None:
    print("\n" + "=" * 88)
    print("PART 1: THE UNIQUE SLOT LIVES ON A GAUGE SINGLET")
    print("=" * 88)

    generators = build_internal_generators()
    e_nu = np.zeros((16, 1), dtype=complex)
    e_nu[15, 0] = 1.0

    residuals = [np.linalg.norm(gen @ e_nu) for _, gen in generators]
    max_residual = max(residuals)
    hypercharge = generators[-1][1][15, 15]

    check("The nu_R slot is annihilated by every SU(3)xSU(2)xU(1) generator", max_residual < 1e-10,
          f"max residual={max_residual:.2e}")
    check("The nu_R slot has Y = 0 exactly", abs(hypercharge) < 1e-12,
          f"Y={hypercharge}")

    print()
    print("  So local phase rotation on the unique source slot does not disturb")
    print("  the anomaly-fixed gauge representation data.")


def test_phase_of_m_is_removed_by_rephasing() -> None:
    print("\n" + "=" * 88)
    print("PART 2: THE COMPLEX SLOT PHASE IS REMOVABLE")
    print("=" * 88)

    cs = annihilation_operators(2)
    n_tot = number_operator(cs)
    pair_ann = cs[0] @ cs[1]
    pair_cre = pair_ann.conj().T

    m = -0.41 + 0.73j
    phi = np.angle(m)
    alpha = phi / 2.0

    deformed = m * pair_ann + np.conj(m) * pair_cre
    pair_ann_rot = rotate(pair_ann, n_tot, alpha)
    pair_cre_rot = rotate(pair_cre, n_tot, alpha)
    deformed_rot = m * pair_ann_rot + np.conj(m) * pair_cre_rot
    target = abs(m) * (pair_ann + pair_cre)

    pair_phase_err = np.linalg.norm(pair_ann_rot - np.exp(-2j * alpha) * pair_ann)
    rotated_err = np.linalg.norm(deformed_rot - target)

    check("The charge-2 bilinear picks up the exact double phase under rephasing", pair_phase_err < 1e-10,
          f"rotation error={pair_phase_err:.2e}")
    check("Choosing alpha = arg(m)/2 makes the Hermitian deformation real-amplitude", rotated_err < 1e-10,
          f"||X_rot-|m|(cc+h.c.)||={rotated_err:.2e}")

    print()
    print("  So the one-generation local source slot carries no invariant phase.")
    print("  It is equivalent to one real nonnegative amplitude mu = |m|.")


def test_pfaffian_generator_depends_only_on_magnitude() -> None:
    print("\n" + "=" * 88)
    print("PART 3: THE ONE-GENERATION PFAFFIAN BLOCK ALSO SEES ONLY |m|")
    print("=" * 88)

    j2 = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    m = 0.52 * np.exp(1.1j)
    a_complex = m * j2
    a_real = abs(m) * j2

    antisym_complex = np.linalg.norm(a_complex + a_complex.T)
    antisym_real = np.linalg.norm(a_real + a_real.T)
    pf_complex = pfaffian_2x2(a_complex)
    pf_real = pfaffian_2x2(a_real)
    generator_err = abs(logabs_pf_2x2(a_complex) - logabs_pf_2x2(a_real))
    singulars_complex = np.linalg.svd(a_complex, compute_uv=False)
    singulars_real = np.linalg.svd(a_real, compute_uv=False)
    singular_err = np.linalg.norm(singulars_complex - singulars_real)

    check("Complex and real-amplitude 2x2 pairing blocks are both antisymmetric", antisym_complex < 1e-10 and antisym_real < 1e-10,
          f"errs=({antisym_complex:.2e},{antisym_real:.2e})")
    check("Pfaffian phase changes but magnitude is |m|", abs(abs(pf_complex) - abs(m)) < 1e-10 and abs(pf_real - abs(m)) < 1e-10,
          f"|Pf_complex|={abs(pf_complex):.6f}, Pf_real={pf_real}")
    check("The CPT-even scalar generator log|Pf| depends only on |m|", generator_err < 1e-10,
          f"generator error={generator_err:.2e}")
    check("Canonical local source-block singular values depend only on |m|", singular_err < 1e-10,
          f"singular-value error={singular_err:.2e}")

    print()
    print("  This is the retained observable-side version of the same theorem:")
    print("  on the one-generation local block, the invariant datum is mu = |m|.")


def main() -> int:
    print("=" * 88)
    print("NEUTRINO MAJORANA: ONE-GENERATION PHASE REMOVAL")
    print("=" * 88)
    print()
    print("Authority stack:")
    print("  - main:docs/publication/ci3_z3/DERIVATION_ATLAS.md")
    print("  - docs/ONE_GENERATION_MATTER_CLOSURE_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_UNIQUE_SOURCE_SLOT_NOTE.md")
    print("  - docs/NEUTRINO_MAJORANA_PFAFFIAN_EXTENSION_NOTE.md")
    print()
    print("Question:")
    print("  On the current one-generation lane, does the unique local source")
    print("  slot m carry a physical phase, or can it be rephased to one real")
    print("  amplitude?")

    test_nu_r_is_gauge_singlet()
    test_phase_of_m_is_removed_by_rephasing()
    test_pfaffian_generator_depends_only_on_magnitude()

    print("\n" + "=" * 88)
    print("RESULT")
    print("=" * 88)
    print("  The one-generation local Majorana source slot has no physical")
    print("  phase. Modulo nu_R rephasing, the invariant datum is one")
    print("  nonnegative real amplitude mu = |m|.")
    print()
    print(f"  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
