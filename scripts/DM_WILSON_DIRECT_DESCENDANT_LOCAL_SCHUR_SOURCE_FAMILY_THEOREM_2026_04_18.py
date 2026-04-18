#!/usr/bin/env python3
"""
DM Wilson direct descendant local Schur source-family theorem.

Purpose:
  Verify that the direct Wilson-to-dW_e^H route is already exact at the local
  charged Schur level:
    1. the support embedding Phi_e is a structured rank-3 *-monomorphism;
    2. normalized determinant responses reduce exactly to the charged
       Schur complement L_e;
    3. first variations equal Re Tr(L_e^{-1} X);
    4. different ambient completions with the same L_e induce the same
       descended responses.
"""

from __future__ import annotations

import sys

import numpy as np


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


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)


def random_complex_matrix(shape: tuple[int, int], seed: int, scale: float = 1.0) -> np.ndarray:
    gen = rng(seed)
    return scale * (
        gen.normal(size=shape) + 1j * gen.normal(size=shape)
    )


def random_invertible_matrix(dim: int, seed: int) -> np.ndarray:
    mat = random_complex_matrix((dim, dim), seed)
    return mat + (2.5 + 0.3 * seed / 100.0) * np.eye(dim, dtype=complex)


def random_hermitian(dim: int, seed: int) -> np.ndarray:
    z = random_complex_matrix((dim, dim), seed)
    return 0.5 * (z + z.conj().T)


def block_diag(*blocks: np.ndarray) -> np.ndarray:
    total = sum(block.shape[0] for block in blocks)
    out = np.zeros((total, total), dtype=complex)
    offset = 0
    for block in blocks:
        dim = block.shape[0]
        out[offset : offset + dim, offset : offset + dim] = block
        offset += dim
    return out


def charge_support_embedding(e_dim: int, r_dim: int) -> np.ndarray:
    out = np.zeros((e_dim + r_dim, e_dim), dtype=complex)
    out[:e_dim, :e_dim] = np.eye(e_dim, dtype=complex)
    return out


def phi_minus(z: np.ndarray, e_dim: int, r_dim: int) -> np.ndarray:
    i_e = charge_support_embedding(e_dim, r_dim)
    return i_e @ z @ i_e.conj().T


def phi_full(
    z: np.ndarray, d0_dim: int, e_dim: int, r_dim: int, dplus_dim: int
) -> np.ndarray:
    return block_diag(
        np.zeros((d0_dim, d0_dim), dtype=complex),
        phi_minus(z, e_dim, r_dim),
        np.zeros((dplus_dim, dplus_dim), dtype=complex),
    )


def build_minus_completion(
    l_e: np.ndarray, r_dim: int, seed: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    b = random_complex_matrix((l_e.shape[0], r_dim), seed + 11, scale=0.3)
    c = random_complex_matrix((r_dim, l_e.shape[0]), seed + 29, scale=0.3)
    f = random_invertible_matrix(r_dim, seed + 47)
    a = l_e + b @ np.linalg.inv(f) @ c
    d_minus = np.block([[a, b], [c, f]])
    return d_minus, a, b, f


def schur_ee(
    d_minus: np.ndarray, e_dim: int
) -> np.ndarray:
    a = d_minus[:e_dim, :e_dim]
    b = d_minus[:e_dim, e_dim:]
    c = d_minus[e_dim:, :e_dim]
    f = d_minus[e_dim:, e_dim:]
    return a - b @ np.linalg.inv(f) @ c


def logabsdet(mat: np.ndarray) -> float:
    sign, logdet = np.linalg.slogdet(mat)
    if abs(sign) == 0:
        raise ValueError("matrix is singular")
    return float(np.real(logdet))


def w_of_t(d_full: np.ndarray, j_full: np.ndarray, t: float) -> float:
    return logabsdet(d_full + t * j_full) - logabsdet(d_full)


def hermitian_basis() -> list[np.ndarray]:
    e11 = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)
    e22 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=complex)
    e33 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]], dtype=complex)
    e12 = np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]], dtype=complex)
    e21 = e12.conj().T
    e23 = np.array([[0, 0, 0], [0, 0, 1], [0, 0, 0]], dtype=complex)
    e32 = e23.conj().T
    e13 = np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]], dtype=complex)
    e31 = e13.conj().T
    return [
        e11,
        e22,
        e33,
        e12 + e21,
        -1j * e12 + 1j * e21,
        e23 + e32,
        -1j * e23 + 1j * e32,
        e13 + e31,
        -1j * e13 + 1j * e31,
    ]


def gram_matrix(basis: list[np.ndarray]) -> np.ndarray:
    size = len(basis)
    out = np.zeros((size, size), dtype=float)
    for i, bi in enumerate(basis):
        for j, bj in enumerate(basis):
            out[i, j] = float(np.real(np.trace(bi @ bj)))
    return out


def reconstruct_hermitian_from_responses(
    basis: list[np.ndarray], responses: np.ndarray
) -> np.ndarray:
    gram = gram_matrix(basis)
    coeffs = np.linalg.solve(gram, responses)
    out = np.zeros_like(basis[0], dtype=complex)
    for c, b in zip(coeffs, basis):
        out += c * b
    return out


def jordan(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return 0.5 * (a @ b + b @ a)


def lie(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return (a @ b - b @ a) / (2j)


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT DESCENDANT LOCAL SCHUR SOURCE-FAMILY THEOREM")
    print("=" * 88)

    d0_dim = 2
    e_dim = 3
    r_dim = 2
    dplus_dim = 2

    l_e = random_invertible_matrix(e_dim, 7)
    d_minus_1, _, _, _ = build_minus_completion(l_e, r_dim, 101)
    d_minus_2, _, _, _ = build_minus_completion(l_e, r_dim, 211)
    d0_1 = random_invertible_matrix(d0_dim, 13)
    d0_2 = random_invertible_matrix(d0_dim, 17)
    dplus_1 = random_invertible_matrix(dplus_dim, 19)
    dplus_2 = random_invertible_matrix(dplus_dim, 23)
    d_full_1 = block_diag(d0_1, d_minus_1, dplus_1)
    d_full_2 = block_diag(d0_2, d_minus_2, dplus_2)

    i_e = charge_support_embedding(e_dim, r_dim)
    p_e = i_e @ i_e.conj().T
    z1 = random_complex_matrix((e_dim, e_dim), 29)
    z2 = random_complex_matrix((e_dim, e_dim), 31)
    x = random_hermitian(e_dim, 37)
    y = random_hermitian(e_dim, 41)

    phi_z1 = phi_minus(z1, e_dim, r_dim)
    phi_z2 = phi_minus(z2, e_dim, r_dim)

    print("\n" + "=" * 88)
    print("PART 1: THE CHARGED SUPPORT EMBEDDING IS ALREADY A STRUCTURED RANK-3 MAP")
    print("=" * 88)
    check(
        "Phi_e is multiplicative on arbitrary complex matrices",
        np.linalg.norm(phi_z1 @ phi_z2 - phi_minus(z1 @ z2, e_dim, r_dim)) < 1e-12,
        f"defect={np.linalg.norm(phi_z1 @ phi_z2 - phi_minus(z1 @ z2, e_dim, r_dim)):.2e}",
    )
    check(
        "Phi_e is *-preserving",
        np.linalg.norm(phi_minus(z1.conj().T, e_dim, r_dim) - phi_z1.conj().T) < 1e-12,
        f"defect={np.linalg.norm(phi_minus(z1.conj().T, e_dim, r_dim) - phi_z1.conj().T):.2e}",
    )
    check(
        "The unit image is the rank-3 charged support projector",
        np.linalg.matrix_rank(phi_minus(np.eye(e_dim, dtype=complex), e_dim, r_dim)) == 3
        and np.linalg.norm(phi_minus(np.eye(e_dim, dtype=complex), e_dim, r_dim) - p_e) < 1e-12,
        f"rank={np.linalg.matrix_rank(phi_minus(np.eye(e_dim, dtype=complex), e_dim, r_dim))}",
    )
    check(
        "The Hermitian restriction preserves Jordan products",
        np.linalg.norm(
            phi_minus(jordan(x, y), e_dim, r_dim) - jordan(phi_minus(x, e_dim, r_dim), phi_minus(y, e_dim, r_dim))
        ) < 1e-12,
        f"defect={np.linalg.norm(phi_minus(jordan(x, y), e_dim, r_dim) - jordan(phi_minus(x, e_dim, r_dim), phi_minus(y, e_dim, r_dim))):.2e}",
    )
    check(
        "The Hermitian restriction preserves Lie products",
        np.linalg.norm(
            phi_minus(lie(x, y), e_dim, r_dim) - lie(phi_minus(x, e_dim, r_dim), phi_minus(y, e_dim, r_dim))
        ) < 1e-12,
        f"defect={np.linalg.norm(phi_minus(lie(x, y), e_dim, r_dim) - lie(phi_minus(x, e_dim, r_dim), phi_minus(y, e_dim, r_dim))):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE NORMALIZED DETERMINANT RESPONSE REDUCES EXACTLY TO THE SCHUR BLOCK")
    print("=" * 88)
    l_from_d1 = schur_ee(d_minus_1, e_dim)
    l_from_d2 = schur_ee(d_minus_2, e_dim)
    check(
        "Both ambient completions realize the prescribed charged Schur complement",
        np.linalg.norm(l_from_d1 - l_e) < 1e-12 and np.linalg.norm(l_from_d2 - l_e) < 1e-12,
        f"errs=({np.linalg.norm(l_from_d1 - l_e):.2e},{np.linalg.norm(l_from_d2 - l_e):.2e})",
    )
    t = 0.07
    jx_full = phi_full(x, d0_dim, e_dim, r_dim, dplus_dim)
    ratio_err_1 = abs(
        np.linalg.det(d_full_1 + t * jx_full) / np.linalg.det(d_full_1)
        - np.linalg.det(l_e + t * x) / np.linalg.det(l_e)
    )
    ratio_err_2 = abs(
        np.linalg.det(d_full_2 + t * jx_full) / np.linalg.det(d_full_2)
        - np.linalg.det(l_e + t * x) / np.linalg.det(l_e)
    )
    check(
        "The full determinant ratio matches the reduced Schur determinant ratio for completion 1",
        ratio_err_1 < 1e-10,
        f"err={ratio_err_1:.2e}",
    )
    check(
        "The full determinant ratio matches the reduced Schur determinant ratio for completion 2",
        ratio_err_2 < 1e-10,
        f"err={ratio_err_2:.2e}",
    )
    w1 = w_of_t(d_full_1, jx_full, t)
    w2 = w_of_t(d_full_2, jx_full, t)
    w_red = logabsdet(l_e + t * x) - logabsdet(l_e)
    check(
        "The normalized observable response equals the local Schur response for completion 1",
        abs(w1 - w_red) < 1e-10,
        f"err={abs(w1 - w_red):.2e}",
    )
    check(
        "The normalized observable response equals the local Schur response for completion 2",
        abs(w2 - w_red) < 1e-10,
        f"err={abs(w2 - w_red):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE FIRST VARIATION IS EXACTLY Re Tr(L_e^{-1} X)")
    print("=" * 88)
    eps = 1.0e-7
    fd = (w_of_t(d_full_1, jx_full, eps) - w_of_t(d_full_1, jx_full, -eps)) / (2.0 * eps)
    analytic = float(np.real(np.trace(np.linalg.inv(l_e) @ x)))
    check(
        "The derivative of the full observable response matches Re Tr(L_e^{-1} X)",
        abs(fd - analytic) < 1e-6,
        f"fd={fd:.8f}, analytic={analytic:.8f}",
    )
    h_e = 0.5 * (np.linalg.inv(l_e) + np.linalg.inv(l_e).conj().T)
    hermitian_trace = float(np.real(np.trace(h_e @ x)))
    check(
        "For Hermitian probes the same derivative equals Tr(H_e X)",
        abs(analytic - hermitian_trace) < 1e-10,
        f"err={abs(analytic - hermitian_trace):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 4: NINE HERMITIAN PROBES RECONSTRUCT THE DESCENDED H_e EXACTLY")
    print("=" * 88)
    basis = hermitian_basis()
    responses = np.array(
        [float(np.real(np.trace(h_e @ b))) for b in basis],
        dtype=float,
    )
    h_reconstructed = reconstruct_hermitian_from_responses(basis, responses)
    check(
        "The standard 9-channel Hermitian probe family reconstructs H_e exactly",
        np.linalg.norm(h_reconstructed - h_e) < 1e-10,
        f"err={np.linalg.norm(h_reconstructed - h_e):.2e}",
    )
    check(
        "The reconstructed H_e is Hermitian",
        np.linalg.norm(h_reconstructed - h_reconstructed.conj().T) < 1e-12,
        f"err={np.linalg.norm(h_reconstructed - h_reconstructed.conj().T):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 5: AMBIENT COMPLETION UNCERTAINTY DOES NOT CHANGE THE LOCAL DESCENDANT LAW")
    print("=" * 88)
    y_full = phi_full(y, d0_dim, e_dim, r_dim, dplus_dim)
    fd_1_y = (w_of_t(d_full_1, y_full, eps) - w_of_t(d_full_1, y_full, -eps)) / (2.0 * eps)
    fd_2_y = (w_of_t(d_full_2, y_full, eps) - w_of_t(d_full_2, y_full, -eps)) / (2.0 * eps)
    check(
        "Different ambient completions with the same L_e give the same first variation on X",
        abs(
            (w_of_t(d_full_1, jx_full, eps) - w_of_t(d_full_1, jx_full, -eps))
            - (w_of_t(d_full_2, jx_full, eps) - w_of_t(d_full_2, jx_full, -eps))
        ) < 1e-12,
        f"err={abs((w_of_t(d_full_1, jx_full, eps) - w_of_t(d_full_1, jx_full, -eps)) - (w_of_t(d_full_2, jx_full, eps) - w_of_t(d_full_2, jx_full, -eps))):.2e}",
    )
    check(
        "Different ambient completions with the same L_e give the same first variation on Y",
        abs(fd_1_y - fd_2_y) < 1e-6,
        f"err={abs(fd_1_y - fd_2_y):.2e}",
    )
    check(
        "The two ambient completions are genuinely different matrices",
        np.linalg.norm(d_full_1 - d_full_2) > 1.0,
        f"matrix_diff={np.linalg.norm(d_full_1 - d_full_2):.3f}",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
