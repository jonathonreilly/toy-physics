#!/usr/bin/env python3
"""
Current plaquette operator stack does not yet force unique Perron/Jacobi data.

This is the next honest obstruction theorem after Perron reduction:
the explicit source operator J plus symmetry-preserving Perron reduction still
do not determine the beta=6 Perron moments or Jacobi coefficients until the
transfer generator itself is made explicit.
"""

from __future__ import annotations

import numpy as np


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
TAU = 6.0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def recurrence_neighbors(p: int, q: int) -> list[tuple[int, int]]:
    out = []
    for a, b in [
        (p + 1, q),
        (p - 1, q + 1),
        (p, q - 1),
        (p, q + 1),
        (p + 1, q - 1),
        (p - 1, q),
    ]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def build_recurrence_matrix(nmax: int) -> tuple[np.ndarray, list[tuple[int, int]], dict[tuple[int, int], int]]:
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    jmat = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in recurrence_neighbors(p, q):
            if (a, b) in index:
                jmat[index[(a, b)], i] += 1.0 / 6.0
    return jmat, weights, index


def conjugation_swap_matrix(weights: list[tuple[int, int]], index: dict[tuple[int, int], int]) -> np.ndarray:
    s = np.zeros((len(weights), len(weights)), dtype=float)
    for w in weights:
        s[index[(w[1], w[0])], index[w]] = 1.0
    return s


def matrix_exponential_symmetric(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def dominant_eigenpair(m: np.ndarray) -> tuple[float, np.ndarray]:
    vals, vecs = np.linalg.eigh(m)
    idx = int(np.argmax(vals))
    vec = vecs[:, idx]
    if np.sum(vec) < 0.0:
        vec = -vec
    return float(vals[idx]), vec


def lanczos_jacobi(obs: np.ndarray, start: np.ndarray, kmax: int) -> tuple[list[float], list[float]]:
    q_prev = np.zeros_like(start)
    q = start / np.linalg.norm(start)
    alpha: list[float] = []
    beta: list[float] = []
    b_prev = 0.0
    for _ in range(kmax):
        z = obs @ q
        a = float(np.dot(q, z))
        z = z - a * q - b_prev * q_prev
        b = float(np.linalg.norm(z))
        alpha.append(a)
        if b < 1.0e-12:
            break
        beta.append(b)
        q_prev = q
        q = z / b
        b_prev = b
    return alpha, beta


def moments(obs: np.ndarray, state: np.ndarray, nmax: int) -> list[float]:
    return [float(state @ (np.linalg.matrix_power(obs, n) @ state)) for n in range(nmax + 1)]


def main() -> int:
    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)

    diag_a = np.diag([0.16 * (p + q) + 0.02 * ((p - q) ** 2) for p, q in weights])
    diag_b = np.diag([0.09 * (p + q) + 0.07 * ((p - q) ** 2) for p, q in weights])
    h_a = jmat + diag_a
    h_b = jmat + diag_b
    t_a = matrix_exponential_symmetric(h_a, TAU)
    t_b = matrix_exponential_symmetric(h_b, TAU)

    lam_a, psi_a = dominant_eigenpair(t_a)
    lam_b, psi_b = dominant_eigenpair(t_b)

    moments_a = moments(jmat, psi_a, 5)
    moments_b = moments(jmat, psi_b, 5)
    al_a, be_a = lanczos_jacobi(jmat, psi_a, 6)
    al_b, be_b = lanczos_jacobi(jmat, psi_b, 6)

    diff_m1 = abs(moments_a[1] - moments_b[1])
    diff_m2 = abs(moments_a[2] - moments_b[2])
    diff_alpha0 = abs(al_a[0] - al_b[0])
    diff_beta1 = abs(be_a[0] - be_b[0]) if be_a and be_b else 0.0

    sym_a = float(np.max(np.abs(swap @ h_a - h_a @ swap)))
    sym_b = float(np.max(np.abs(swap @ h_b - h_b @ swap)))
    inv_a = float(np.linalg.norm(swap @ psi_a - psi_a))
    inv_b = float(np.linalg.norm(swap @ psi_b - psi_b))
    min_entry_a = float(np.min(t_a))
    min_entry_b = float(np.min(t_b))
    floor_a = float(np.min(psi_a))
    floor_b = float(np.min(psi_b))

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE PERRON/JACOBI UNDERDETERMINATION")
    print("=" * 78)
    print()
    print("Two admissible symmetry-preserving transfer generators on the same explicit source sector")
    print(f"  box size                              = {(NMAX + 1)} x {(NMAX + 1)} = {len(weights)} states")
    print(f"  tau                                   = {TAU:.1f}")
    print(f"  H_A symmetry error                    = {sym_a:.3e}")
    print(f"  H_B symmetry error                    = {sym_b:.3e}")
    print(f"  T_A min entry / Perron floor          = {min_entry_a:.6e} / {floor_a:.6e}")
    print(f"  T_B min entry / Perron floor          = {min_entry_b:.6e} / {floor_b:.6e}")
    print()
    print("Perron moment comparison for the same explicit source operator J")
    print(f"  m1^A, m1^B                            = {moments_a[1]:.12f}, {moments_b[1]:.12f}")
    print(f"  m2^A, m2^B                            = {moments_a[2]:.12f}, {moments_b[2]:.12f}")
    print(f"  |m1^A - m1^B|                         = {diff_m1:.6e}")
    print(f"  |m2^A - m2^B|                         = {diff_m2:.6e}")
    print()
    print("Jacobi coefficient comparison")
    print(f"  alpha0^A, alpha0^B                    = {al_a[0]:.12f}, {al_b[0]:.12f}")
    print(f"  beta1^A,  beta1^B                     = {be_a[0]:.12f}, {be_b[0]:.12f}")
    print(f"  |alpha0^A - alpha0^B|                 = {diff_alpha0:.6e}")
    print(f"  |beta1^A  - beta1^B|                  = {diff_beta1:.6e}")
    print()

    check(
        "the current structural boundary admits multiple symmetry-preserving positive transfer generators",
        sym_a < 1.0e-12 and sym_b < 1.0e-12 and min_entry_a > 0.0 and min_entry_b > 0.0,
        detail=f"min entries=({min_entry_a:.3e}, {min_entry_b:.3e})",
    )
    check(
        "each admissible generator has its own unique strictly positive Perron state",
        floor_a > 1.0e-8 and floor_b > 1.0e-8 and lam_a > 0.0 and lam_b > 0.0,
        detail=f"Perron floors=({floor_a:.3e}, {floor_b:.3e})",
    )
    check(
        "distinct admissible generators can induce different Perron moments for the same explicit source operator",
        diff_m1 > 1.0e-4 and diff_m2 > 1.0e-4,
        detail=f"moment gaps=(m1:{diff_m1:.3e}, m2:{diff_m2:.3e})",
    )
    check(
        "the symmetry-reduced Jacobi coefficients are therefore not yet forced by the current stack",
        diff_alpha0 > 1.0e-4 and diff_beta1 > 1.0e-4,
        detail=f"Jacobi gaps=(alpha0:{diff_alpha0:.3e}, beta1:{diff_beta1:.3e})",
    )

    check(
        "both Perron states remain fixed by the conjugation symmetry",
        inv_a < 1.0e-10 and inv_b < 1.0e-10,
        detail=f"invariance errors=({inv_a:.3e}, {inv_b:.3e})",
        bucket="SUPPORT",
    )
    check(
        "the same explicit plaquette-source operator J is used in both witnesses",
        float(np.max(np.abs(jmat - jmat.T))) < 1.0e-15 and float(np.max(np.abs(swap @ jmat - jmat @ swap))) < 1.0e-12,
        detail="same self-adjoint conjugation-symmetric J in both cases",
        bucket="SUPPORT",
    )
    check(
        "the obstruction is not infinitesimal on the sampled source sector",
        diff_m1 > 1.0e-2 and diff_alpha0 > 1.0e-2,
        detail=f"representative gaps=(m1:{diff_m1:.3e}, alpha0:{diff_alpha0:.3e})",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
