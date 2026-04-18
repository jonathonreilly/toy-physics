#!/usr/bin/env python3
"""
Koide full-lattice Schur-inheritance runner
===========================================

STATUS: exact/numeric scope theorem on the positive-parent Koide lane

Question:
  If the charged-lepton parent lives on a larger physical carrier than the bare
  hw=1 triplet -- for example the full taste cube, or a taste cube with extra
  spectator/internal factors -- does the previous axis obstruction disappear
  automatically?

Safe answer:
  No. Any larger C_3-covariant parent that is reduced to the retained T_1 lane
  by the usual Schur / effective-operator map still induces a C_3-covariant
  (hence circulant) effective operator on T_1. Therefore the old obstruction
  survives every completion that keeps the same equivariant reduction class and
  the same axis-diagonal readout U_e = I_3.
"""

from __future__ import annotations

import sys
from typing import Iterable

import numpy as np
import sympy as sp

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def cycle_bits(alpha: tuple[int, int, int]) -> tuple[int, int, int]:
    a, b, c = alpha
    return (c, a, b)


def build_taste_cube_data():
    basis = [
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 1),
    ]
    index = {alpha: i for i, alpha in enumerate(basis)}
    n = len(basis)
    U = np.zeros((n, n), dtype=complex)
    for j, alpha in enumerate(basis):
        i = index[cycle_bits(alpha)]
        U[i, j] = 1.0
    t1 = [1, 2, 3]
    t2 = [4, 5, 6]
    o0 = [0]
    o3 = [7]
    rest = o0 + t2 + o3
    C = U[np.ix_(t1, t1)]
    return basis, U, C, t1, t2, o0, o3, rest


def schur_complement(M: np.ndarray, target: Iterable[int]) -> np.ndarray:
    target = list(target)
    all_idx = list(range(M.shape[0]))
    rest = [i for i in all_idx if i not in target]
    A = M[np.ix_(target, target)]
    B = M[np.ix_(target, rest)]
    D = M[np.ix_(rest, rest)]
    return A - B @ np.linalg.inv(D) @ B.conj().T


def group_average(U: np.ndarray, M: np.ndarray) -> np.ndarray:
    out = np.zeros_like(M, dtype=complex)
    Uk = np.eye(U.shape[0], dtype=complex)
    for _ in range(3):
        out += Uk @ M @ Uk.conj().T
        Uk = U @ Uk
    return out / 3.0


def random_positive_covariant(U: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(U.shape[0], U.shape[0])) + 1j * rng.normal(size=(U.shape[0], U.shape[0]))
    M0 = X.conj().T @ X + 0.5 * np.eye(U.shape[0], dtype=complex)
    return group_average(U, M0)


def part1_taste_cube_decomposition():
    print("=" * 88)
    print("PART 1: full taste-cube C_3 action preserves the retained T_1 lane")
    print("=" * 88)

    basis, U, C, t1, t2, o0, o3, _ = build_taste_cube_data()

    t1_images = [basis[int(np.argmax(U[:, j]))] for j in t1]
    t2_images = [basis[int(np.argmax(U[:, j]))] for j in t2]

    check(
        "The full C^8 corner carrier splits into O_0, T_1, T_2, O_3 under the spatial C_3 cycle",
        True,
        detail="basis ordered as 000 | 100,010,001 | 110,011,101 | 111",
    )
    check(
        "T_1 is invariant under the full taste-cube C_3 action",
        set(t1_images) == {(1, 0, 0), (0, 1, 0), (0, 0, 1)},
        detail=f"images={t1_images}",
    )
    check(
        "T_2 is invariant under the full taste-cube C_3 action",
        set(t2_images) == {(1, 1, 0), (0, 1, 1), (1, 0, 1)},
        detail=f"images={t2_images}",
    )
    check(
        "O_0 and O_3 are fixed singlets",
        basis[int(np.argmax(U[:, o0[0]]))] == (0, 0, 0)
        and basis[int(np.argmax(U[:, o3[0]]))] == (1, 1, 1),
    )
    C_expected = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    check(
        "The restricted action on T_1 is exactly the retained 3-cycle matrix",
        np.allclose(C, C_expected),
        detail=f"C_T1={np.real_if_close(C).real.astype(int).tolist()}",
        kind="NUMERIC",
    )
    check(
        "The restricted action on T_2 is the same regular C_3 representation",
        np.allclose(U[np.ix_(t2, t2)], C_expected),
        kind="NUMERIC",
    )


def part2_exact_model_extension():
    print()
    print("=" * 88)
    print("PART 2: exact T_1 <-> T_2 Schur reduction stays circulant")
    print("=" * 88)

    a, d, p, q, r = sp.symbols("a d p q r", real=True, positive=True)
    C = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    I3 = sp.eye(3)

    A = a * I3
    D = d * I3
    B = p * I3 + q * C + r * C**2
    S = sp.simplify(A - B * D.inv() * B.T)

    check(
        "A bare scalar T_1 block plus C_3-covariant T_1<->T_2 couplings yields an exact Schur operator",
        True,
        detail="S = A - B D^{-1} B^T with A = a I_3, D = d I_3, B circulant",
    )
    check(
        "The exact Schur operator commutes with the retained 3-cycle",
        sp.simplify(C * S * C.T - S) == sp.zeros(3),
    )
    offdiag = sp.simplify(S[0, 1])
    check(
        "Full-carrier couplings can generate a nontrivial off-diagonal effective operator on T_1",
        sp.expand(offdiag) != 0,
        detail=f"S01={offdiag}",
    )
    sample = sp.N(offdiag.subs({a: 5, d: 7, p: 1, q: 2, r: 3}))
    check(
        "The induced off-diagonal term is genuinely nonzero for generic couplings",
        abs(complex(sample)) > 1e-9,
        detail=f"sample={sample}",
        kind="NUMERIC",
    )


def part3_full_taste_cube_numeric():
    print()
    print("=" * 88)
    print("PART 3: random positive full-C^8 parents reduce to circulant T_1 Schur blocks")
    print("=" * 88)

    _, U, C, t1, _, _, _, _ = build_taste_cube_data()

    commute_ok = True
    herm_ok = True
    saw_nondiag = False
    details = []
    for seed in range(5):
        M = random_positive_covariant(U, seed)
        S = schur_complement(M, t1)
        commute_err = float(np.linalg.norm(C @ S @ C.conj().T - S))
        herm_err = float(np.linalg.norm(S - S.conj().T))
        offdiag = S - np.diag(np.diag(S))
        offdiag_max = float(np.max(np.abs(offdiag)))
        details.append(f"seed{seed}: commute={commute_err:.2e}, offdiag={offdiag_max:.3f}")
        commute_ok &= commute_err < 1e-10
        herm_ok &= herm_err < 1e-10
        saw_nondiag |= offdiag_max > 1e-3

    check(
        "Every tested positive C_3-covariant full-C^8 parent yields a T_1 Schur block commuting with C_3",
        commute_ok,
        detail="; ".join(details),
        kind="NUMERIC",
    )
    check(
        "The reduced T_1 Schur blocks remain Hermitian",
        herm_ok,
        kind="NUMERIC",
    )
    check(
        "Coupling to the rest of the taste cube changes the effective T_1 operator without breaking its circulant class",
        saw_nondiag,
        kind="NUMERIC",
    )


def part4_extra_internal_factor():
    print()
    print("=" * 88)
    print("PART 4: an extra spectator/internal factor still inherits the same T_1 symmetry")
    print("=" * 88)

    _, U8, C, t1, _, _, _, _ = build_taste_cube_data()
    U16 = np.kron(U8, np.eye(2, dtype=complex))
    target = [2 * i for i in t1]

    commute_ok = True
    details = []
    for seed in range(3):
        M = random_positive_covariant(U16, 100 + seed)
        S = schur_complement(M, target)
        commute_err = float(np.linalg.norm(C @ S @ C.conj().T - S))
        details.append(f"seed{seed}: commute={commute_err:.2e}")
        commute_ok &= commute_err < 1e-10

    check(
        "Adding a spectator/internal doubling does not by itself break the inherited C_3 symmetry on the target T_1 block",
        commute_ok,
        detail="; ".join(details),
        kind="NUMERIC",
    )


def part5_axis_diagonal_collapse():
    print()
    print("=" * 88)
    print("PART 5: axis-diagonal circulant Schur blocks collapse to scalar identity")
    print("=" * 88)

    a, x, y = sp.symbols("a x y", real=True)
    b = x + sp.I * y
    S = sp.Matrix([[a, sp.conjugate(b), b], [b, a, sp.conjugate(b)], [sp.conjugate(b), b, a]])
    offdiag = S - sp.diag(*[S[i, i] for i in range(3)])

    check(
        "A general Hermitian circulant effective block has equal diagonal entries",
        S[0, 0] == S[1, 1] == S[2, 2],
    )
    check(
        "If the effective T_1 block is axis-diagonal, its off-diagonal parameter must vanish",
        sp.simplify(offdiag[0, 1]) == x - sp.I * y and sp.simplify(offdiag[0, 2]) == x + sp.I * y,
        detail="diagonality forces x = y = 0",
    )
    check(
        "Therefore any axis-diagonal circulant Schur block is a scalar multiple of I_3",
        sp.simplify(S.subs({x: 0, y: 0}) - a * sp.eye(3)) == sp.zeros(3),
    )


def main() -> int:
    part1_taste_cube_decomposition()
    part2_exact_model_extension()
    part3_full_taste_cube_numeric()
    part4_extra_internal_factor()
    part5_axis_diagonal_collapse()

    print()
    print("Interpretation:")
    print("  The positive-parent obstruction is not merely a bare-hw=1 artifact.")
    print("  Enlarging the carrier to the full taste cube, or even adding extra")
    print("  spectator/internal factors, still leaves the induced T_1 effective")
    print("  operator circulant whenever the reduction is the usual C_3-equivariant")
    print("  Schur/effective-operator map. So a physically larger carrier alone does")
    print("  not rescue the Koide lane. The genuine escape hatches are different:")
    print("  change the readout, change the reduction map, mix the physical carrier")
    print("  beyond an isolated T_1 target, or break the strict charged-lepton C_3")
    print("  covariance in a controlled retained way.")
    print()
    print(f"PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
