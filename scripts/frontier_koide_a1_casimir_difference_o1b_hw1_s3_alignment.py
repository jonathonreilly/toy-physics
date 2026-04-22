#!/usr/bin/env python3
"""
O1.b — hw=1 carrier S_3-irrep alignment with the C_3 character split

Lift the C_3 Plancherel/Parseval split (O1.a) from the abstract 3-dim
generation space to the retained hw=1 carrier under S_3 axis permutation.

Inputs (retained):
  - S_3 acts on C^8 = (C^2)^{otimes 3} by tensor-position permutation
  - Hamming-weight blocks split as 1 + 3 + 3 + 1
  - The hw=1 sector is the standard 3-dim permutation representation
  - That permutation rep decomposes as A_1 (trivial) + E (2-dim standard)
    (`docs/S3_TASTE_CUBE_DECOMPOSITION_NOTE.md`)

Claim: the C_3 / S_3 character projectors on the hw=1 sector coincide
with the A_1 / E projectors of section O1.a, so the mass-square-root
weights (a_0^2, |z|^2) are exactly the (A_1, E)-isotypic norms of the
hw=1 sqrt-mass vector.
"""

from __future__ import annotations

import sys
from itertools import permutations

import numpy as np


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def perm_matrix(perm: tuple[int, int, int]) -> np.ndarray:
    """3x3 permutation matrix."""
    P = np.zeros((3, 3))
    for i, p_i in enumerate(perm):
        P[i, p_i] = 1.0
    return P


def main() -> int:
    section("O1.b — hw=1 S_3-irrep alignment")

    # The 6 elements of S_3 acting by axis permutations on R^3
    s3 = list(permutations(range(3)))
    s3_mats = [perm_matrix(p) for p in s3]

    # Conjugacy classes by cycle type:
    # - 1 identity, 3 transpositions, 2 3-cycles
    cls_id = [(0, 1, 2)]
    cls_trans = [p for p in s3 if sorted(p) == [0, 1, 2] and len([i for i in range(3) if p[i] == i]) == 1]
    cls_3cyc = [p for p in s3 if all(p[i] != i for i in range(3))]

    print(f"  identity:      {cls_id}")
    print(f"  transpositions:{cls_trans}")
    print(f"  3-cycles:      {cls_3cyc}")

    # ---- A. Character of the standard 3-dim permutation rep ---------------
    section("A. Permutation-rep characters chi(g) = trace M(g)")
    chi_id = float(np.trace(perm_matrix(cls_id[0])))
    chi_trans = float(np.trace(perm_matrix(cls_trans[0])))
    chi_3cyc = float(np.trace(perm_matrix(cls_3cyc[0])))
    print(f"  chi(e)         = {chi_id}")
    print(f"  chi(transpos.) = {chi_trans}")
    print(f"  chi(3-cycle)   = {chi_3cyc}")

    record("A.1 chi(e) = 3",        chi_id == 3.0)
    record("A.2 chi(transp.) = 1",  chi_trans == 1.0)
    record("A.3 chi(3-cyc) = 0",    chi_3cyc == 0.0)

    # S_3 character table (rows: irreps A_1, A_2, E ; cols: classes e, transp, 3cyc)
    chi_A1 = np.array([1, 1, 1])
    chi_A2 = np.array([1, -1, 1])
    chi_E = np.array([2, 0, -1])
    class_sizes = np.array([1, 3, 2])
    group_order = 6
    perm_chi = np.array([chi_id, chi_trans, chi_3cyc])

    def isotype_mult(perm_chi, irrep_chi):
        # <chi_perm, chi_irrep> = (1/|G|) sum_classes |class| chi_perm chi_irrep_conj
        return int(round((class_sizes * perm_chi * irrep_chi).sum() / group_order))

    m_A1 = isotype_mult(perm_chi, chi_A1)
    m_A2 = isotype_mult(perm_chi, chi_A2)
    m_E = isotype_mult(perm_chi, chi_E)
    print(f"  multiplicities: A_1 -> {m_A1}, A_2 -> {m_A2}, E -> {m_E}")
    record(
        "A.4 hw=1 perm rep decomposes as A_1 + E (multiplicities (1,0,1))",
        (m_A1, m_A2, m_E) == (1, 0, 1),
    )

    # ---- B. Build A_1 / E projectors via the standard formula --------------
    section("B. Build A_1 and E projectors via P = (d/|G|) sum_g chi(g)* M(g)")
    P_A1 = (1 / group_order) * sum(chi_A1[c] * mat
                                    for cls, c in [(cls_id, 0), (cls_trans, 1), (cls_3cyc, 2)]
                                    for p in cls
                                    for mat in [perm_matrix(p)])
    P_E = (2 / group_order) * sum(chi_E[c] * mat
                                   for cls, c in [(cls_id, 0), (cls_trans, 1), (cls_3cyc, 2)]
                                   for p in cls
                                   for mat in [perm_matrix(p)])

    # Idempotency
    record("B.1 P_A1^2 = P_A1", np.allclose(P_A1 @ P_A1, P_A1))
    record("B.2 P_E^2 = P_E",   np.allclose(P_E @ P_E, P_E))
    record("B.3 P_A1 + P_E = 1_3", np.allclose(P_A1 + P_E, np.eye(3)))
    record("B.4 P_A1 P_E = 0",  np.allclose(P_A1 @ P_E, np.zeros((3, 3))))

    # Ranks
    record("B.5 rank(P_A1) = 1", np.linalg.matrix_rank(P_A1) == 1)
    record("B.6 rank(P_E) = 2",  np.linalg.matrix_rank(P_E) == 2)

    # ---- C. Compare to the C_3-character (Fourier) projectors --------------
    section("C. Coincidence with the C_3 character (Fourier) projectors of O1.a")
    e_plus = np.array([1, 1, 1]) / np.sqrt(3)
    omega = np.exp(2j * np.pi / 3)
    e_omega = np.array([1, omega, omega ** 2]) / np.sqrt(3)
    e_omega_bar = np.array([1, omega.conjugate(), (omega ** 2).conjugate()]) / np.sqrt(3)

    P_plus_fourier = np.outer(e_plus, e_plus.conj())
    P_E_fourier = (np.outer(e_omega, e_omega.conj())
                   + np.outer(e_omega_bar, e_omega_bar.conj()))

    record(
        "C.1 P_A1 (group-projector) = P_+ (Fourier-projector)",
        np.allclose(P_A1, P_plus_fourier.real),
    )
    record(
        "C.2 P_E (group-projector) = P_E_fourier",
        np.allclose(P_E, P_E_fourier.real),
    )

    # ---- D. Apply to a generic v in R^3, compare weights ------------------
    section("D. Generic √m vector v: weights match (a_0^2, 2|z|^2)")
    rng = np.random.default_rng(0xC15)
    v = np.abs(rng.normal(size=3)) + 0.1
    a0 = (v.sum()) / np.sqrt(3)
    z_complex = (v[0] + omega.conjugate() * v[1] + omega * v[2]) / np.sqrt(3)
    z_sq = abs(z_complex) ** 2

    w_A1 = float(v @ P_A1 @ v)
    w_E = float(v @ P_E @ v)

    record(
        "D.1 v^T P_A1 v = a_0^2",
        np.isclose(w_A1, a0 ** 2),
        f"v^T P_A1 v = {w_A1}, a_0^2 = {a0**2}",
    )
    record(
        "D.2 v^T P_E v = 2 |z|^2",
        np.isclose(w_E, 2 * z_sq),
        f"v^T P_E v = {w_E}, 2|z|^2 = {2*z_sq}",
    )
    record(
        "D.3 (a_0^2, |z|^2) = (S_3-A_1 weight, half S_3-E weight)",
        np.isclose(a0 ** 2, w_A1) and np.isclose(z_sq, w_E / 2),
    )

    # ---- E. Confirm A_2 (sign rep) is absent on hw=1 -----------------------
    section("E. Sign irrep A_2 has zero weight on the hw=1 vector v")
    P_A2 = (1 / group_order) * sum(chi_A2[c] * mat
                                    for cls, c in [(cls_id, 0), (cls_trans, 1), (cls_3cyc, 2)]
                                    for p in cls
                                    for mat in [perm_matrix(p)])
    record("E.1 P_A2 has rank 0 on hw=1 perm rep", np.allclose(P_A2, np.zeros((3, 3))))
    record("E.2 v has no A_2 content (v^T P_A2 v = 0)", np.isclose(v @ P_A2 @ v, 0.0))

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    if n_pass == n_total:
        print("VERDICT: O1.b closed. The C_3 Fourier projectors of O1.a are exactly")
        print("the S_3 isotype projectors P_A1 and P_E on the hw=1 sector. Hence")
        print("(a_0^2, 2|z|^2) are the (A_1, E)-isotypic squared norms of the")
        print("sqrt-mass vector on the retained hw=1 carrier. O1 next: O1.c lifts")
        print("this to the mass MATRIX side (Hermitian operator on the hw=1 triplet).")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
