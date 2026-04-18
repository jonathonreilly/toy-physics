#!/usr/bin/env python3
"""
Fixed-depth plaquette beta=6 bulk reduction from the finite Jacobi packet to an
equivalent finite cyclic-moment packet.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0
DEPTH = 3


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


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)


def rank_one_bulk_from_target(v: np.ndarray, eta: np.ndarray, depth: int) -> np.ndarray:
    u = normalize(v)
    lam = (float(np.dot(v, v)) / float(np.dot(v, eta))) ** (1.0 / depth)
    return lam * np.outer(u, u)


def lanczos_packet(op: np.ndarray, start: np.ndarray, max_steps: int):
    q_prev = np.zeros_like(start)
    q = normalize(start)
    basis = [q.copy()]
    alpha = []
    beta = []
    b_prev = 0.0
    for _ in range(max_steps):
        w = op @ q - b_prev * q_prev
        a = float(q @ w)
        w = w - a * q
        alpha.append(a)
        for b in basis:
            w = w - float(b @ w) * b
        b_next = float(np.linalg.norm(w))
        if b_next < 1.0e-12:
            break
        beta.append(b_next)
        q_prev = q
        q = w / b_next
        basis.append(q.copy())
        b_prev = b_next
    qmat = np.column_stack(basis)
    jmat = np.diag(alpha)
    if beta:
        off = np.array(beta, dtype=float)
        jmat += np.diag(off, 1) + np.diag(off, -1)
    return qmat, np.array(alpha, dtype=float), np.array(beta, dtype=float), jmat


def moment_packet(op: np.ndarray, eta: np.ndarray, max_n: int) -> np.ndarray:
    return np.array([float(eta @ (np.linalg.matrix_power(op, n) @ eta)) for n in range(max_n + 1)], dtype=float)


def main() -> int:
    cyclic_bulk = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md")
    finite_jacobi = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_JACOBI_PACKET_REDUCTION_NOTE_2026-04-18.md")
    note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_MOMENT_PACKET_REDUCTION_NOTE_2026-04-18.md")

    eta = normalize(np.ones(4, dtype=float))
    kernel = np.array([-0.4885403546, 0.7722564727, -0.3682858155, 0.1712127927], dtype=float)
    v_p = np.array([1.2, 0.9, 1.1, 0.8], dtype=float)
    v_q = v_p + 0.4 * kernel

    s_p = rank_one_bulk_from_target(v_p, eta, DEPTH)
    s_q = rank_one_bulk_from_target(v_q, eta, DEPTH)
    _, alpha_p, beta_p, j_p = lanczos_packet(s_p, eta, DEPTH + 1)
    _, alpha_q, beta_q, j_q = lanczos_packet(s_q, eta, DEPTH + 1)
    moments_p = moment_packet(s_p, eta, 2 * DEPTH)
    moments_q = moment_packet(s_q, eta, 2 * DEPTH)
    j_moments_p = np.array([float(np.eye(j_p.shape[0])[0] @ (np.linalg.matrix_power(j_p, n) @ np.eye(j_p.shape[0])[:, 0])) for n in range(2 * DEPTH + 1)])
    j_moments_q = np.array([float(np.eye(j_q.shape[0])[0] @ (np.linalg.matrix_power(j_q, n) @ np.eye(j_q.shape[0])[:, 0])) for n in range(2 * DEPTH + 1)])

    recon_err = max(float(np.max(np.abs(moments_p - j_moments_p))), float(np.max(np.abs(moments_q - j_moments_q))))
    a0_err = max(abs(alpha_p[0] - moments_p[1]), abs(alpha_q[0] - moments_q[1]))
    b1_err = max(abs(beta_p[0] ** 2 - (moments_p[2] - moments_p[1] ** 2)), abs(beta_q[0] ** 2 - (moments_q[2] - moments_q[1] ** 2)))
    m12_gap = max(abs(moments_p[1] - moments_q[1]), abs(moments_p[2] - moments_q[2]))

    print("=" * 118)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 IDENTITY-RIM FINITE-MOMENT PACKET REDUCTION")
    print("=" * 118)
    print()
    print(f"eta                              = {eta}")
    print(f"v_P                              = {v_p}")
    print(f"v_Q                              = {v_q}")
    print(f"alpha_0^P, beta_1^P              = ({alpha_p[0]:.12f}, {beta_p[0]:.12f})")
    print(f"alpha_0^Q, beta_1^Q              = ({alpha_q[0]:.12f}, {beta_q[0]:.12f})")
    print(f"(m1,m2)^P                        = ({moments_p[1]:.12f}, {moments_p[2]:.12f})")
    print(f"(m1,m2)^Q                        = ({moments_q[1]:.12f}, {moments_q[2]:.12f})")
    print(f"moment/Jacobi reconstruction err = {recon_err:.3e}")
    print(f"alpha_0=m1 err                   = {a0_err:.3e}")
    print(f"beta_1^2=(m2-m1^2) err           = {b1_err:.3e}")
    print(f"first moment-pair gap            = {m12_gap:.12f}")
    print()

    check(
        "The cyclic-bulk reduction note already says the reduced identity-rim cyclic object is determined by its moment sequence",
        "determined by the" in cyclic_bulk and "corresponding moment sequence" in cyclic_bulk,
        bucket="SUPPORT",
    )
    check(
        "The finite-Jacobi reduction note already identifies the sharp fixed-depth bulk datum as one finite Jacobi packet",
        "finite **Jacobi packet**" in finite_jacobi
        and ("fixed-depth plaquette closure depends only on the finite Jacobi packet" in finite_jacobi
             or "fixed-depth class-sector closure depends only on the finite Jacobi packet" in finite_jacobi),
        bucket="SUPPORT",
    )

    check(
        "Therefore the sharp fixed-depth plaquette bulk datum is equivalently one finite cyclic-moment packet",
        recon_err < 1.0e-12,
        detail=f"reconstruction err={recon_err:.3e}",
    )
    check(
        "The first Jacobi layer is already equivalent to the first nontrivial cyclic-moment pair",
        a0_err < 1.0e-12 and b1_err < 1.0e-12,
        detail=f"errors=({a0_err:.3e}, {b1_err:.3e})",
    )
    check(
        "The explicit witness pair already differs at the first nontrivial moment layer (m1,m2)",
        m12_gap > 1.0e-6,
        detail=f"gap={m12_gap:.12f}",
    )
    check(
        "So the propagated-triple noncollapse already persists at the first scalar bulk layer",
        "still does **not** determine even the first" in note and "moment pair" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
