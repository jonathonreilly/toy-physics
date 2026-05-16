#!/usr/bin/env python3
"""Narrow bridge theorem runner for
`KOIDE_RETAINED_WILSON_APS_SCALAR_ACTION_ON_RANK_TWO_MULTIPLICITY_BRIDGE_NARROW_THEOREM_NOTE_2026-05-16`.

Verifies the scalar-on-`M_zeta` theorem: every operator built from the
retained Wilson/APS generators

    {D, U, U^dag} union { P_lambda(D) : lambda in Spec(D) },

when restricted to the rank-two zeta-character isotypic component
`M_zeta` of the Wilson-Dirac zero-mode subspace `V_0 = ker(D)`, acts
as a scalar `lambda_A I_2`.

Construction of `D`, `U`, `V_0`, and `M_zeta` is re-imported from the
sibling runner
    scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py,
which already audits `||D - D^dag|| ~ 0`, `||U D U^dag - D|| ~ 0`,
`dim V_0 = 4`, and `dim M_zeta = 2` for the same construction.

The bridge runner additionally checks:
  - `D|_{M_zeta} ~ 0`,
  - `U|_{M_zeta} ~ zeta I_2`, `U^dag|_{M_zeta} ~ zeta_bar I_2`,
  - `P_lambda(D)|_{M_zeta}` is scalar (`1 I_2` for `lambda = 0`, `0 I_2`
    otherwise),
  - a sample of polynomial words in `{D, U, U^dag, P_0(D)}` restricts
    to scalar `2 x 2` matrices on `M_zeta`,
  - a non-retained countermodel (rank-one projector `|line_0><line_0|`)
    is NOT scalar on `M_zeta`, confirming that the scalar property
    genuinely characterizes the retained algebra,
  - the property is `r`-independent in the certified window
    `r in {1.0, 1.425}`.

This is class-A pure operator algebra over the finite-dimensional
construction; no Koide / charged-lepton mass / sqrt(m) / PDG /
selection-principle physical identification is consumed.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent.parent

# Import the sibling runner's construction without executing its main().
SIBLING_PATH = ROOT / "scripts" / "frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py"
_spec = importlib.util.spec_from_file_location(
    "_sibling_koide_wilson", str(SIBLING_PATH)
)
_sibling = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_sibling)
build_wilson_lattice = _sibling.build_wilson_lattice
zero_character_lines = _sibling.zero_character_lines


TOL = 1e-8
PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


def restrict_to(M: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """Return basis^dag @ M @ basis for an orthonormal `basis` (columns)."""
    return basis.conj().T @ M @ basis


def is_scalar_2x2(M: np.ndarray, tol: float = TOL) -> tuple[bool, complex]:
    """Return (is_scalar, candidate scalar)."""
    if M.shape != (2, 2):
        return False, complex(0.0)
    lam = (M[0, 0] + M[1, 1]) / 2
    expected = lam * np.eye(2, dtype=complex)
    return bool(np.linalg.norm(M - expected) < tol), complex(lam)


def build_basis_M_zeta(D: np.ndarray, U: np.ndarray) -> tuple[np.ndarray, complex]:
    """Return (orthonormal 2-column basis of M_zeta, the zeta scalar)."""
    line_0, line_1, zeta = zero_character_lines(D, U)
    basis = np.stack([line_0, line_1], axis=1)
    # Sanity: orthonormality
    gram = basis.conj().T @ basis
    if np.linalg.norm(gram - np.eye(2)) > TOL:
        raise RuntimeError(f"M_zeta basis not orthonormal: gram={gram}")
    return basis, complex(zeta)


def spectral_projectors(D: np.ndarray) -> list[tuple[float, np.ndarray]]:
    """Return [(eigenvalue, orthogonal projector onto eigenspace), ...].

    Eigenspaces are coalesced by eigenvalue equality within TOL.
    """
    eigs, vecs = np.linalg.eigh(D)
    projectors: list[tuple[float, np.ndarray]] = []
    used = np.zeros(len(eigs), dtype=bool)
    for i, lam in enumerate(eigs):
        if used[i]:
            continue
        group = [i]
        used[i] = True
        for j in range(i + 1, len(eigs)):
            if (not used[j]) and abs(eigs[j] - lam) < TOL:
                group.append(j)
                used[j] = True
        block = vecs[:, group]
        P = block @ block.conj().T
        projectors.append((float(lam), P))
    return projectors


def run_for_r(r: float) -> None:
    section(f"r = {r}: build sibling Wilson construction and M_zeta")

    D, U, fixed_sites = build_wilson_lattice(r)
    check(
        f"r={r}: sibling D is Hermitian (||D - D^dag|| < tol)",
        np.linalg.norm(D - D.conj().T) < TOL,
        f"||D - D^dag|| = {np.linalg.norm(D - D.conj().T):.2e}",
    )
    check(
        f"r={r}: sibling U intertwines D (||U D U^dag - D|| < tol)",
        np.linalg.norm(U @ D @ U.conj().T - D) < TOL,
        f"||U D U^dag - D|| = {np.linalg.norm(U @ D @ U.conj().T - D):.2e}",
    )

    eigs, _ = np.linalg.eigh(D)
    zero_count = int(np.sum(np.abs(eigs) < TOL))
    check(
        f"r={r}: ker(D) has dimension 4 (sibling B.1)",
        zero_count == 4,
        f"dim ker(D) = {zero_count}",
    )

    basis_Mz, zeta = build_basis_M_zeta(D, U)
    zeta_expected = complex(math.cos(math.pi / 3), math.sin(math.pi / 3))
    check(
        f"r={r}: M_zeta is rank-two zeta-eigenspace with zeta = exp(i pi/3)",
        basis_Mz.shape == (D.shape[0], 2)
        and abs(zeta - zeta_expected) < TOL,
        f"shape={basis_Mz.shape}, zeta = {zeta}, expected = {zeta_expected}",
    )

    section(f"r = {r}: generators restrict to scalars on M_zeta")

    D_on_Mz = restrict_to(D, basis_Mz)
    is_scalar, lam_D = is_scalar_2x2(D_on_Mz)
    check(
        f"r={r}: D|_{{M_zeta}} = 0 I_2",
        is_scalar and abs(lam_D) < TOL,
        f"D|_{{M_zeta}} = \n{D_on_Mz}",
    )

    U_on_Mz = restrict_to(U, basis_Mz)
    is_scalar, lam_U = is_scalar_2x2(U_on_Mz)
    check(
        f"r={r}: U|_{{M_zeta}} = zeta I_2 with zeta = exp(i pi/3)",
        is_scalar and abs(lam_U - zeta) < TOL,
        f"U|_{{M_zeta}} = \n{U_on_Mz},  lam_U = {lam_U}",
    )

    Udag_on_Mz = restrict_to(U.conj().T, basis_Mz)
    is_scalar, lam_Udag = is_scalar_2x2(Udag_on_Mz)
    check(
        f"r={r}: U^dag|_{{M_zeta}} = zeta_bar I_2",
        is_scalar and abs(lam_Udag - np.conjugate(zeta)) < TOL,
        f"U^dag|_{{M_zeta}} = \n{Udag_on_Mz},  lam_Udag = {lam_Udag}",
    )

    # Sanity: U * U^dag = I on full space (so on M_zeta).
    check(
        f"r={r}: U is unitary (U U^dag = I on full space)",
        np.linalg.norm(U @ U.conj().T - np.eye(U.shape[0])) < TOL,
        f"||U U^dag - I|| = {np.linalg.norm(U @ U.conj().T - np.eye(U.shape[0])):.2e}",
    )

    section(f"r = {r}: spectral projectors of D restrict to scalars on M_zeta")

    proj_list = spectral_projectors(D)
    nonscalar_proj_failures = []
    P_zero = None
    for lam, P in proj_list:
        P_on_Mz = restrict_to(P, basis_Mz)
        is_scalar, lam_P = is_scalar_2x2(P_on_Mz)
        expected_scalar = 1.0 if abs(lam) < TOL else 0.0
        ok = is_scalar and abs(lam_P.real - expected_scalar) < TOL and abs(lam_P.imag) < TOL
        if not ok:
            nonscalar_proj_failures.append(
                f"lambda={lam}: P|_{{M_zeta}} = {P_on_Mz},  lam_P = {lam_P}"
            )
        if abs(lam) < TOL:
            P_zero = P
    check(
        f"r={r}: every spectral projector P_lambda(D) is scalar on M_zeta",
        len(nonscalar_proj_failures) == 0,
        (
            "all projectors scalar"
            if not nonscalar_proj_failures
            else "non-scalar failures:\n        " + "\n        ".join(nonscalar_proj_failures)
        ),
    )

    assert P_zero is not None, "P_0(D) must exist since dim ker(D) = 4"

    section(f"r = {r}: polynomial words in retained generators are scalar on M_zeta")

    Udag = U.conj().T
    words: list[tuple[str, np.ndarray]] = [
        ("D", D),
        ("U", U),
        ("U^dag", Udag),
        ("D + U", D + U),
        ("U + U^dag", U + Udag),
        ("D^2", D @ D),
        ("U^2", U @ U),
        ("U @ U^dag", U @ Udag),
        ("(U + U^dag) @ P_0", (U + Udag) @ P_zero),
        ("U^2 + D - U^dag", U @ U + D - Udag),
        ("P_0 @ U @ P_0", P_zero @ U @ P_zero),
        ("U @ D @ U^dag", U @ D @ Udag),
        ("(D + U + U^dag) @ P_0 + 3 * P_0", (D + U + Udag) @ P_zero + 3 * P_zero),
    ]
    word_failures = []
    for name, W in words:
        W_on_Mz = restrict_to(W, basis_Mz)
        is_scalar, lam_W = is_scalar_2x2(W_on_Mz)
        if not is_scalar:
            word_failures.append(f"{name}: {W_on_Mz}")
    check(
        f"r={r}: every sampled retained polynomial word is scalar on M_zeta",
        len(word_failures) == 0,
        (
            f"{len(words)}/{len(words)} retained polynomial words restrict to scalar I_2"
            if not word_failures
            else "non-scalar failures:\n        " + "\n        ".join(word_failures)
        ),
    )

    section(f"r = {r}: countermodel — a NON-retained rank-one projector is NOT scalar on M_zeta")

    line_0 = basis_Mz[:, 0]
    rank_one_proj = np.outer(line_0, line_0.conj())
    rank_one_on_Mz = restrict_to(rank_one_proj, basis_Mz)
    is_scalar_ro, lam_ro = is_scalar_2x2(rank_one_on_Mz)
    expected_diag = np.diag([1.0, 0.0]).astype(complex)
    matches_diag = np.linalg.norm(rank_one_on_Mz - expected_diag) < TOL
    check(
        f"r={r}: |line_0><line_0| restricts to diag(1, 0) on M_zeta, hence not scalar",
        (not is_scalar_ro) and matches_diag,
        f"|line_0><line_0|_{{M_zeta}} = \n{rank_one_on_Mz},  is_scalar={is_scalar_ro}",
    )
    check(
        f"r={r}: countermodel confirms the scalar property is non-trivial",
        not is_scalar_ro,
        "Some non-retained operators do distinguish the two copies of zeta; the retained ones do not.",
    )


def main() -> int:
    print("=" * 88)
    print("Narrow bridge theorem: retained Wilson/APS algebra acts as scalar on M_zeta")
    print("=" * 88)

    for r in (1.0, 1.425):
        run_for_r(r)

    print()
    print("=" * 88)
    print("Bridge theorem summary")
    print("=" * 88)
    print(
        """
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let D, U be the Wilson-Dirac operator and body-diagonal spin-lift
    permutation built by `build_wilson_lattice(r)` in
    `frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py`
    for r in {1.0, 1.425}. Let V_0 = ker(D), and M_zeta the rank-two
    zeta-eigenspace of U|_{V_0} with zeta = exp(i pi/3). Let
    A := <{D, U, U^dag} union {P_lambda(D) : lambda in Spec(D)}>
    be the retained Wilson/APS polynomial algebra.

  CONCLUSION:
    For every A in A, A|_{M_zeta} = lambda_A I_2 for some scalar
    lambda_A in C.

  Class:
    (A) finite-dimensional operator algebra over C, with the explicit
    Wilson construction re-used from the sibling no-go. No Koide /
    charged-lepton mass / sqrt(m) / PDG / selection-principle physical
    identification is consumed.

  Consequence (for the parent no-go):
    The parent runner
    `frontier_koide_delta_marked_relative_cobordism_no_go.py` previously
    asserted `retained_mark = lam * sp.eye(2)`. By the Scalar-on-M_zeta
    theorem, every retained "derived boundary mark" automatically
    restricts to such a scalar on M_zeta; the parent's downstream
    commutator/expectation/countermodel algebra is therefore valid for
    every retained mark, not just the asserted one.
"""
    )

    print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
    print(f"PASS={PASS} FAIL={FAIL}")
    return 1 if FAIL > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
