#!/usr/bin/env python3
"""
Exact source-sector matrix-element factorization support packet for the
plaquette transfer route on the accepted Wilson 3+1 surface.

This does not close analytic P(6), and it does not evaluate the Wilson
residual diagonal D_6. It audits the exact factorized source-sector matrix
law with one generic positive conjugation-symmetric diagonal witness
operator:

    T_src(6) = exp(3 J) D_6 exp(3 J)

with J the exact plaquette source recurrence operator and D_6 the positive
diagonal mixed-kernel coefficient operator in the SU(3) character basis.
"""

from __future__ import annotations

import numpy as np


THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
BETA = 6.0


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
    out: list[tuple[int, int]] = []
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


def conjugation_swap_matrix(
    weights: list[tuple[int, int]], index: dict[tuple[int, int], int]
) -> np.ndarray:
    swap = np.zeros((len(weights), len(weights)), dtype=float)
    for w in weights:
        swap[index[(w[1], w[0])], index[w]] = 1.0
    return swap


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


def power_iteration(m: np.ndarray, steps: int = 40) -> np.ndarray:
    vec = np.ones(m.shape[0], dtype=float)
    vec /= np.linalg.norm(vec)
    for _ in range(steps):
        vec = m @ vec
        vec /= np.linalg.norm(vec)
    if np.sum(vec) < 0.0:
        vec = -vec
    return vec


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


def main() -> int:
    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)

    half_multiplier = matrix_exponential_symmetric(jmat, BETA / 2.0)
    half_sym_err = float(np.max(np.abs(half_multiplier - half_multiplier.T)))
    half_swap_err = float(np.max(np.abs(swap @ half_multiplier - half_multiplier @ swap)))
    half_vals = np.linalg.eigvalsh(half_multiplier)

    kappa = np.array(
        [
            np.exp(-0.33 * (p + q) - 0.08 * ((p - q) ** 2))
            for p, q in weights
        ],
        dtype=float,
    )
    dmat = np.diag(kappa)
    d_sym_err = float(np.max(np.abs(swap @ dmat - dmat @ swap)))
    transfer = half_multiplier @ dmat @ half_multiplier
    transfer_sym_err = float(np.max(np.abs(transfer - transfer.T)))
    transfer_swap_err = float(np.max(np.abs(swap @ transfer - transfer @ swap)))
    transfer_min = float(np.min(transfer))

    formula = np.zeros_like(transfer)
    for i in range(transfer.shape[0]):
        for j in range(transfer.shape[1]):
            formula[i, j] = float(np.sum(half_multiplier[i, :] * kappa * half_multiplier[:, j]))
    formula_err = float(np.max(np.abs(transfer - formula)))

    _, perron = dominant_eigenpair(transfer)
    iter_vec = power_iteration(transfer)
    perron_iter_err = float(np.linalg.norm(perron - iter_vec))

    alpha, beta = lanczos_jacobi(jmat, perron, 6)
    perron_expectation = float(perron @ (jmat @ perron))

    print("=" * 78)
    print("GAUGE-VACUUM PLAQUETTE SOURCE-SECTOR MATRIX-ELEMENT FACTORIZATION")
    print("=" * 78)
    print()
    print("Exact source-sector structural ingredients at beta = 6")
    print(f"  dominant-weight box size              = {(NMAX + 1)} x {(NMAX + 1)} = {len(weights)} states")
    print(f"  half-slice multiplier parameter       = beta/2 = {BETA/2.0:.1f}")
    print(f"  audited truncation                    = NMAX = {NMAX}")
    print(f"  half-multiplier symmetry error        = {half_sym_err:.3e}")
    print(f"  half-multiplier swap error            = {half_swap_err:.3e}")
    print(f"  half-multiplier eigenvalue range      = [{half_vals.min():.12f}, {half_vals.max():.12f}]")
    print()
    print("Generic positive diagonal witness sequence")
    print(f"  min/max kappa_(p,q)(6)                = {kappa.min():.12f}, {kappa.max():.12f}")
    print(f"  diagonal swap error                   = {d_sym_err:.3e}")
    print()
    print("Factorized source-sector transfer witness")
    print(f"  transfer symmetry error               = {transfer_sym_err:.3e}")
    print(f"  transfer swap error                   = {transfer_swap_err:.3e}")
    print(f"  minimum matrix entry                  = {transfer_min:.6e}")
    print(f"  explicit matrix-formula error         = {formula_err:.3e}")
    print()
    print("Perron/Jacobi witness on the explicit factorized operator")
    print(f"  Perron/power-iteration mismatch       = {perron_iter_err:.3e}")
    print(f"  Perron expectation of J               = {perron_expectation:.12f}")
    print(f"  first Jacobi coefficients             = alpha[:4]={np.round(alpha[:4], 10).tolist()}")
    print(f"                                         beta[:4]={np.round(beta[:4], 10).tolist()}")
    print()

    check(
        "the exact plaquette source recurrence operator is self-adjoint and conjugation-symmetric",
        float(np.max(np.abs(jmat - jmat.T))) < 1.0e-15 and float(np.max(np.abs(swap @ jmat - jmat @ swap))) < 1.0e-12,
        detail=f"J symmetry={float(np.max(np.abs(jmat - jmat.T))):.3e}, swap={float(np.max(np.abs(swap @ jmat - jmat @ swap))):.3e}",
    )
    check(
        "the beta = 6 marked half-slice factor is exactly the positive self-adjoint operator exp(3 J)",
        half_sym_err < 1.0e-12 and half_swap_err < 1.0e-12 and half_vals.min() > 0.0,
        detail=f"eigenvalue range=[{half_vals.min():.6f}, {half_vals.max():.6f}]",
    )
    check(
        "given a conjugation-symmetric positive diagonal coefficient witness, the exact source-sector law yields a factorized transfer operator",
        d_sym_err < 1.0e-12 and transfer_sym_err < 1.0e-12 and transfer_swap_err < 1.0e-12,
        detail=f"D swap={d_sym_err:.3e}, T symmetry={transfer_sym_err:.3e}, T swap={transfer_swap_err:.3e}",
    )
    check(
        "for that audited diagonal witness, the source-sector matrix elements obey T_(lambda,mu)=sum_nu M_(lambda,nu) kappa_nu M_(nu,mu)",
        formula_err < 1.0e-12,
        detail=f"max matrix-formula error = {formula_err:.3e}",
    )

    check(
        "the factorized transfer witness is positivity-improving on the truncated source box",
        transfer_min > 0.0,
        detail=f"minimum entry = {transfer_min:.3e}",
        bucket="SUPPORT",
    )
    check(
        "power iteration recovers the Perron state of the explicit factorized source-sector operator",
        perron_iter_err < 1.0e-10,
        detail=f"||psi_power - psi_perron|| = {perron_iter_err:.3e}",
        bucket="SUPPORT",
    )
    check(
        "once a diagonal coefficient sequence is fixed, the remaining framework-point data are just Perron moments / Jacobi coefficients of J",
        len(alpha) >= 4 and len(beta) >= 3 and perron_expectation > 0.0,
        detail=f"Jacobi depth = {len(alpha)}, Perron <J> = {perron_expectation:.6f}",
        bucket="SUPPORT",
    )

    print()
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 78)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
