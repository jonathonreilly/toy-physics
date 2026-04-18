#!/usr/bin/env python3
"""
Fixed-depth plaquette beta=6 bulk reduction from the finite Krylov block to its
canonical finite Jacobi packet seen from the identity rim state eta_6(e).
"""

from __future__ import annotations

import cmath
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

SAMPLES = {
    "W_A": (-13 * math.pi / 16.0, 5 * math.pi / 8.0),
    "W_B": (-5 * math.pi / 16.0, -7 * math.pi / 16.0),
    "W_C": (7 * math.pi / 16.0, -11 * math.pi / 16.0),
}
ORBITS = [(0, 2), (0, 3), (0, 4), (0, 5)]
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


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def su3_character(p: int, q: int, theta1: float, theta2: float) -> complex:
    x = [
        cmath.exp(1j * theta1),
        cmath.exp(1j * theta2),
        cmath.exp(-1j * (theta1 + theta2)),
    ]
    lam = [p + q, q, 0]
    num = np.array([[x[i] ** (lam[j] + 2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    den = np.array([[x[i] ** (2 - j) for j in range(3)] for i in range(3)], dtype=complex)
    return complex(np.linalg.det(num) / np.linalg.det(den))


def orbit_sample_row(p: int, q: int) -> np.ndarray:
    d = dim_su3(p, q)
    row = []
    for theta1, theta2 in SAMPLES.values():
        ch = su3_character(p, q, theta1, theta2)
        value = d * ch if p == q else 2.0 * (d * ch).real
        row.append(float(np.real_if_close(value)))
    return np.array(row, dtype=float)


def sample_matrix() -> np.ndarray:
    return np.column_stack([orbit_sample_row(*orbit) for orbit in ORBITS])


def normalize(vec: np.ndarray) -> np.ndarray:
    return vec / np.linalg.norm(vec)


def rank_one_bulk_from_target(v: np.ndarray, eta: np.ndarray, depth: int) -> np.ndarray:
    u = normalize(v)
    lam = (float(np.dot(v, v)) / float(np.dot(v, eta))) ** (1.0 / depth)
    return lam * np.outer(u, u)


def lanczos_packet(op: np.ndarray, start: np.ndarray, max_steps: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
        # one-pass reorthogonalization against accumulated basis keeps the packet stable
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
        jmat += np.diag(off, k=1) + np.diag(off, k=-1)
    return qmat, np.array(alpha, dtype=float), np.array(beta, dtype=float), jmat


def max_off_tridiagonal(mat: np.ndarray) -> float:
    n = mat.shape[0]
    mask = np.ones((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if abs(i - j) <= 1:
                mask[i, j] = False
    return float(np.max(np.abs(mat[mask]))) if np.any(mask) else 0.0


def moment_packet(op: np.ndarray, eta: np.ndarray, max_n: int) -> np.ndarray:
    return np.array([float(eta @ (np.linalg.matrix_power(op, n) @ eta)) for n in range(max_n + 1)], dtype=float)


def main() -> int:
    cyclic_bulk = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md")
    finite_krylov = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_KRYLOV_BULK_REDUCTION_NOTE_2026-04-17.md")
    propagated_nonclosure = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_OPERATOR_SIDE_NONCLOSURE_NOTE_2026-04-17.md"
    )
    note = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_FINITE_JACOBI_PACKET_REDUCTION_NOTE_2026-04-18.md")

    e3 = sample_matrix()
    _, _, vh = np.linalg.svd(e3)
    kernel = vh[-1]

    eta = normalize(np.ones(4, dtype=float))
    v_p = np.array([1.2, 0.9, 1.1, 0.8], dtype=float)
    v_q = v_p + 0.4 * kernel

    s_p = rank_one_bulk_from_target(v_p, eta, DEPTH)
    s_q = rank_one_bulk_from_target(v_q, eta, DEPTH)
    prop_p = np.linalg.matrix_power(s_p, DEPTH) @ eta
    prop_q = np.linalg.matrix_power(s_q, DEPTH) @ eta
    triple_p = e3 @ prop_p
    triple_q = e3 @ prop_q
    triple_gap = float(np.max(np.abs(triple_p - triple_q)))

    q_p, alpha_p, beta_p, j_p = lanczos_packet(s_p, eta, DEPTH + 1)
    q_q, alpha_q, beta_q, j_q = lanczos_packet(s_q, eta, DEPTH + 1)
    rep_p = q_p.T @ s_p @ q_p
    rep_q = q_q.T @ s_q @ q_q

    tridiag_gap_p = float(np.max(np.abs(rep_p - j_p)))
    tridiag_gap_q = float(np.max(np.abs(rep_q - j_q)))
    off_p = max_off_tridiagonal(rep_p)
    off_q = max_off_tridiagonal(rep_q)

    krylov_err_p = max(
        float(np.linalg.norm((q_p @ (np.linalg.matrix_power(j_p, n) @ np.eye(j_p.shape[0])[:, 0])) - (np.linalg.matrix_power(s_p, n) @ eta)))
        for n in range(DEPTH + 1)
    )
    krylov_err_q = max(
        float(np.linalg.norm((q_q @ (np.linalg.matrix_power(j_q, n) @ np.eye(j_q.shape[0])[:, 0])) - (np.linalg.matrix_power(s_q, n) @ eta)))
        for n in range(DEPTH + 1)
    )

    moments_p = moment_packet(s_p, eta, 2 * DEPTH)
    moments_q = moment_packet(s_q, eta, 2 * DEPTH)
    j_moments_p = np.array(
        [float(np.eye(j_p.shape[0])[0] @ (np.linalg.matrix_power(j_p, n) @ np.eye(j_p.shape[0])[:, 0])) for n in range(2 * DEPTH + 1)],
        dtype=float,
    )
    j_moments_q = np.array(
        [float(np.eye(j_q.shape[0])[0] @ (np.linalg.matrix_power(j_q, n) @ np.eye(j_q.shape[0])[:, 0])) for n in range(2 * DEPTH + 1)],
        dtype=float,
    )
    moment_err_p = float(np.max(np.abs(moments_p - j_moments_p)))
    moment_err_q = float(np.max(np.abs(moments_q - j_moments_q)))

    first_packet_gap = max(
        abs(float(alpha_p[0] - alpha_q[0])),
        abs(float(beta_p[0] - beta_q[0])) if len(beta_p) and len(beta_q) else 0.0,
    )
    first_moment_gap = max(abs(float(moments_p[1] - moments_q[1])), abs(float(moments_p[2] - moments_q[2])))

    print("=" * 124)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 IDENTITY-RIM FINITE-JACOBI PACKET REDUCTION")
    print("=" * 124)
    print()
    print(f"higher-orbit slice                           = {ORBITS}")
    print(f"sample matrix shape / rank                   = {e3.shape} / {np.linalg.matrix_rank(e3)}")
    print(f"kernel direction                             = {kernel}")
    print()
    print(f"depth d                                      = {DEPTH}")
    print(f"eta                                          = {eta}")
    print(f"v_P                                          = {v_p}")
    print(f"v_Q                                          = {v_q}")
    print(f"propagated triple gap                        = {triple_gap:.12e}")
    print()
    print(f"alpha^P                                      = {alpha_p}")
    print(f"beta^P                                       = {beta_p}")
    print(f"alpha^Q                                      = {alpha_q}")
    print(f"beta^Q                                       = {beta_q}")
    print(f"first Jacobi packet gap                      = {first_packet_gap:.12f}")
    print(f"first cyclic-moment gap                      = {first_moment_gap:.12f}")
    print()
    print(f"Lanczos tridiagonal gaps (P,Q)               = ({tridiag_gap_p:.3e}, {tridiag_gap_q:.3e})")
    print(f"off-tridiagonal residues (P,Q)               = ({off_p:.3e}, {off_q:.3e})")
    print(f"orbit reconstruction errors (P,Q)            = ({krylov_err_p:.3e}, {krylov_err_q:.3e})")
    print(f"moment reconstruction errors (P,Q)           = ({moment_err_p:.3e}, {moment_err_q:.3e})")
    print()

    check(
        "The cyclic-bulk reduction note already reformulates the reduced eta_6(e)-cyclic object in spectral / Jacobi terms",
        "spectral / Jacobi reformulation of the bulk front" in cyclic_bulk
        and "the corresponding moment sequence" in cyclic_bulk
        and "Jacobi data of `S_6^env`" in cyclic_bulk,
        bucket="SUPPORT",
    )
    check(
        "The finite-Krylov reduction note already says the sharp fixed-depth bulk target is the eta_6(e)-generated finite Krylov block",
        "finite Krylov space" in finite_krylov
        and "the sharp fixed-depth bulk target" in finite_krylov
        and ("first nontrivial matrix-element block" in finite_krylov
             or "first nontrivial finite block" in finite_krylov),
        bucket="SUPPORT",
    )
    check(
        "The propagated-triple operator-side nonclosure note already says the propagated retained triple is a finite target but not an operator-side closure datum",
        "right next finite target" in propagated_nonclosure
        and "not itself an operator-side closure theorem" in propagated_nonclosure,
        bucket="SUPPORT",
    )

    check(
        "In the Lanczos basis generated by eta, the fixed-depth Krylov compression is exactly tridiagonal, so the bulk target reduces to a finite Jacobi packet",
        off_p < 1.0e-12 and off_q < 1.0e-12 and tridiag_gap_p < 1.0e-12 and tridiag_gap_q < 1.0e-12,
        detail=f"off=({off_p:.3e}, {off_q:.3e})",
    )
    check(
        "For every n <= d, the propagated eta-orbit is reconstructed exactly from that finite Jacobi packet",
        krylov_err_p < 1.0e-12 and krylov_err_q < 1.0e-12,
        detail=f"errors=({krylov_err_p:.3e}, {krylov_err_q:.3e})",
    )
    check(
        "The finite cyclic moments are already downstream of the same Jacobi packet",
        moment_err_p < 1.0e-12 and moment_err_q < 1.0e-12,
        detail=f"errors=({moment_err_p:.3e}, {moment_err_q:.3e})",
    )
    check(
        "The explicit witness pair still has the same exact propagated retained triple",
        triple_gap < 1.0e-10 and np.min(v_q) > 0.0,
        detail=f"triple gap={triple_gap:.3e}, min(v_Q)={np.min(v_q):.12f}",
    )
    check(
        "But the same propagated retained triple already gives different first cyclic moments",
        first_moment_gap > 1.0e-6,
        detail=f"gap={first_moment_gap:.12f}",
    )
    check(
        "And therefore the same propagated retained triple already gives different first nontrivial Jacobi packets (alpha_0, beta_1)",
        first_packet_gap > 1.0e-6,
        detail=f"gap={first_packet_gap:.12f}",
    )
    check(
        "So the current propagated retained triple still does not determine even the sharp finite-Jacobi bulk packet on the current bank",
        triple_gap < 1.0e-10 and first_packet_gap > 1.0e-6,
        detail="same triple, different Jacobi packet",
    )

    check(
        "The new note records the finite-Jacobi reduction and the sharper noncollapse at the Jacobi-packet level",
        "finite **Jacobi packet**" in note
        and "first nontrivial Jacobi packet" in note
        and "fixed-depth class-sector closure depends only on the finite Jacobi packet" in note,
        bucket="SUPPORT",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
