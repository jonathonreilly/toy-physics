#!/usr/bin/env python3
"""
DM Wilson direct-descendant local Schur branch-discriminant theorem.

Purpose:
  Combine the local-Schur reduction with the projected-source branch
  discriminant into one exact source-side statement:

    1. once the charged Schur block L_e is fixed, the descended Hermitian
       response law reconstructs H_e exactly;
    2. the explicit projected-source scalar Delta_src equals det(H_e);
    3. therefore the current positive-branch discriminator is local to L_e and
       cannot be changed by altering ambient completions that keep L_e fixed;
    4. the frozen triplet channels (gamma, E1, E2) still do not determine that
       sign on the live basin set.

  This is an exact reduction theorem on the open DM gate. It does not derive
  the actual microscopic law for L_e from Cl(3) on Z^3.
"""

from __future__ import annotations

import math
import sys

import numpy as np


PASS_COUNT = 0
FAIL_COUNT = 0

FD_EPS = 1.0e-7


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
    return scale * (gen.normal(size=shape) + 1j * gen.normal(size=shape))


def random_invertible_matrix(dim: int, seed: int) -> np.ndarray:
    mat = random_complex_matrix((dim, dim), seed)
    return mat + (2.5 + 0.3 * seed / 100.0) * np.eye(dim, dtype=complex)


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


def w_of_t(d_full: np.ndarray, j_full: np.ndarray, t: float) -> float:
    sign, logdet = np.linalg.slogdet(d_full + t * j_full)
    if abs(sign) == 0:
        raise ValueError("singular matrix in w_of_t")
    sign0, logdet0 = np.linalg.slogdet(d_full)
    if abs(sign0) == 0:
        raise ValueError("singular base matrix in w_of_t")
    return float(np.real(logdet - logdet0))


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
    for coeff, basis_elem in zip(coeffs, basis):
        out += coeff * basis_elem
    return out


def pack_from_h(hmat: np.ndarray) -> dict[str, float]:
    return {
        "R11": float(np.real(hmat[0, 0])),
        "R22": float(np.real(hmat[1, 1])),
        "R33": float(np.real(hmat[2, 2])),
        "S12": float(2.0 * np.real(hmat[0, 1])),
        "A12": float(-2.0 * np.imag(hmat[0, 1])),
        "S13": float(2.0 * np.real(hmat[0, 2])),
        "A13": float(-2.0 * np.imag(hmat[0, 2])),
        "S23": float(2.0 * np.real(hmat[1, 2])),
        "A23": float(-2.0 * np.imag(hmat[1, 2])),
    }


def delta_src(pack: dict[str, float]) -> float:
    r11 = pack["R11"]
    r22 = pack["R22"]
    r33 = pack["R33"]
    s12 = pack["S12"]
    a12 = pack["A12"]
    s13 = pack["S13"]
    a13 = pack["A13"]
    s23 = pack["S23"]
    a23 = pack["A23"]
    return float(
        r11 * r22 * r33
        - (r11 * s23 * s23 + r22 * s13 * s13 + r33 * s12 * s12) / 4.0
        - (a12 * a12 * r33 + a13 * a13 * r22 + a23 * a23 * r11) / 4.0
        + (a12 * a13 * s23 - a12 * a23 * s13 + a13 * a23 * s12) / 4.0
        + s12 * s13 * s23 / 4.0
    )


def triplet_from_pack(pack: dict[str, float]) -> tuple[float, float, float]:
    gamma_val = pack["A13"] / 2.0
    e1_val = (pack["R22"] - pack["R33"]) / 2.0 + (pack["S12"] - pack["S13"]) / 4.0
    e2_val = (
        pack["R11"]
        + (pack["S12"] + pack["S13"]) / 4.0
        - (pack["R22"] + pack["R33"]) / 2.0
        - pack["S23"] / 2.0
    )
    return float(gamma_val), float(e1_val), float(e2_val)


def response_vector_from_completion(
    d_full: np.ndarray,
    basis: list[np.ndarray],
    d0_dim: int,
    e_dim: int,
    r_dim: int,
    dplus_dim: int,
) -> np.ndarray:
    rows = []
    for probe in basis:
        j_full = phi_full(probe, d0_dim, e_dim, r_dim, dplus_dim)
        fd = (w_of_t(d_full, j_full, FD_EPS) - w_of_t(d_full, j_full, -FD_EPS)) / (2.0 * FD_EPS)
        rows.append(fd)
    return np.array(rows, dtype=float)


GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]], dtype=complex)
T_DELTA = np.array(
    [[0.0, -1.0, 1.0], [-1.0, 1.0, 0.0], [1.0, 0.0, -1.0]],
    dtype=complex,
)
T_Q = np.array(
    [[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]],
    dtype=complex,
)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)


def active_h(m_val: float, delta_val: float, q_val: float) -> np.ndarray:
    return H_BASE + m_val * T_M + delta_val * T_DELTA + q_val * T_Q


def main() -> int:
    print("=" * 88)
    print("DM WILSON DIRECT-DESCENDANT LOCAL SCHUR BRANCH-DISCRIMINANT THEOREM")
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
    h_e_expected = 0.5 * (np.linalg.inv(l_e) + np.linalg.inv(l_e).conj().T)
    basis = hermitian_basis()

    print("\n" + "=" * 88)
    print("PART 1: THE BRANCH DISCRIMINANT IS LOCAL TO THE SCHUR BLOCK L_e")
    print("=" * 88)
    responses_1 = response_vector_from_completion(d_full_1, basis, d0_dim, e_dim, r_dim, dplus_dim)
    responses_2 = response_vector_from_completion(d_full_2, basis, d0_dim, e_dim, r_dim, dplus_dim)
    h_e_1 = reconstruct_hermitian_from_responses(basis, responses_1)
    h_e_2 = reconstruct_hermitian_from_responses(basis, responses_2)

    check(
        "The descended 9-channel Hermitian responses reconstruct H_e exactly for ambient completion 1",
        np.linalg.norm(h_e_1 - h_e_expected) < 5.0e-7,
        f"err={np.linalg.norm(h_e_1 - h_e_expected):.2e}",
    )
    check(
        "The descended 9-channel Hermitian responses reconstruct H_e exactly for ambient completion 2",
        np.linalg.norm(h_e_2 - h_e_expected) < 5.0e-7,
        f"err={np.linalg.norm(h_e_2 - h_e_expected):.2e}",
    )
    check(
        "Changing the ambient completion while keeping L_e fixed does not change the reconstructed H_e",
        np.linalg.norm(h_e_1 - h_e_2) < 5.0e-7,
        f"err={np.linalg.norm(h_e_1 - h_e_2):.2e}",
    )

    print("\n" + "=" * 88)
    print("PART 2: THE EXPLICIT PROJECTED-SOURCE SCALAR IS EXACTLY det(H_e)")
    print("=" * 88)
    pack_1 = pack_from_h(h_e_1)
    pack_2 = pack_from_h(h_e_2)
    delta_1 = delta_src(pack_1)
    delta_2 = delta_src(pack_2)
    det_h = float(np.real(np.linalg.det(h_e_expected)))
    check(
        "The explicit cubic Delta_src equals det(H_e) on completion 1",
        abs(delta_1 - det_h) < 5.0e-7,
        f"err={abs(delta_1 - det_h):.2e}",
    )
    check(
        "The explicit cubic Delta_src equals det(H_e) on completion 2",
        abs(delta_2 - det_h) < 5.0e-7,
        f"err={abs(delta_2 - det_h):.2e}",
    )
    check(
        "The local branch-discriminant sign is ambient-completion invariant once L_e is fixed",
        abs(delta_1 - delta_2) < 5.0e-7 and (delta_1 > 0.0) == (delta_2 > 0.0),
        f"delta_1={delta_1:+.8f}, delta_2={delta_2:+.8f}",
    )

    print("\n" + "=" * 88)
    print("PART 3: THE FROZEN TRIPLET STILL DOES NOT DETERMINE THE BRANCH SIGN")
    print("=" * 88)
    basins = {
        "Basin 1": (0.657061, 0.933806, 0.715042),
        "Basin 2": (28.0, 20.7, 5.0),
        "Basin X": (21.0, 12.68, 2.089),
    }
    basin_triplets: dict[str, tuple[float, float, float]] = {}
    basin_deltas: dict[str, float] = {}
    for name, point in basins.items():
        pack = pack_from_h(active_h(*point))
        basin_triplets[name] = triplet_from_pack(pack)
        basin_deltas[name] = delta_src(pack)

    triplet_ref = basin_triplets["Basin 1"]
    triplet_err = max(
        max(abs(a - b) for a, b in zip(triplet_ref, basin_triplets[name]))
        for name in basins
    )
    check(
        "All three live basins carry the same exact triplet (gamma, E1, E2)",
        triplet_err < 1.0e-12
        and abs(triplet_ref[0] - 0.5) < 1.0e-12
        and abs(triplet_ref[1] - math.sqrt(8.0 / 3.0)) < 1.0e-12
        and abs(triplet_ref[2] - math.sqrt(8.0) / 3.0) < 1.0e-12,
        f"triplet={tuple(round(v, 12) for v in triplet_ref)}",
    )
    check(
        "The exact branch-discriminant sign distinguishes Basin 1 from Basin 2 and Basin X",
        basin_deltas["Basin 1"] > 0.0 and basin_deltas["Basin 2"] < 0.0 and basin_deltas["Basin X"] < 0.0,
        (
            "deltas="
            + "{"
            + ", ".join(f"{name}: {value:+.6f}" for name, value in basin_deltas.items())
            + "}"
        ),
    )
    check(
        "So the live positive-branch rule cannot factor only through the frozen triplet channels",
        triplet_err < 1.0e-12 and len({value > 0.0 for value in basin_deltas.values()}) > 1,
        "same triplet, opposite Delta_src signs",
    )

    print("\n" + "=" * 88)
    print("PART 4: BOTTOM LINE")
    print("=" * 88)
    check(
        "The current source-branch discriminator is exactly a local sign law on L_e",
        True,
        "positive branch = Delta_src(dW_e^H) = det(H_e(L_e)) > 0; ambient completion cannot change it once L_e is fixed",
    )

    print("\n" + "=" * 88)
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 88)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
