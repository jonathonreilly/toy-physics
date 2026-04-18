#!/usr/bin/env python3
"""
Fixed-depth plaquette beta=6 bulk reduction after the identity-rim and cyclic
bulk reductions.

This sharpens the remaining operator-side target from the whole compressed
operator, and even from the whole eta-cyclic object, to the finite Krylov block
seen from eta_6(e) up to the propagation depth d = L_perp - 1. It also proves
that the present propagated retained triple still does not determine even the
first nontrivial Krylov/Lanczos block on the current bank.
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


def krylov_basis(op: np.ndarray, eta: np.ndarray, depth: int) -> tuple[np.ndarray, np.ndarray]:
    cols = [eta]
    for n in range(1, depth + 1):
        cols.append(np.linalg.matrix_power(op, n) @ eta)
    mat = np.column_stack(cols)
    q, _ = np.linalg.qr(mat)
    keep = []
    for i in range(q.shape[1]):
        if np.linalg.norm(q[:, i]) > 1.0e-10:
            keep.append(q[:, i])
    basis = np.column_stack(keep)
    proj = basis @ basis.T
    return basis, proj


def first_lanczos_block(op: np.ndarray, eta: np.ndarray) -> np.ndarray:
    q0 = normalize(eta)
    w = op @ q0
    a0 = float(q0 @ w)
    r = w - a0 * q0
    beta1 = float(np.linalg.norm(r))
    q1 = r / beta1
    a1 = float(q1 @ (op @ q1))
    return np.array([[a0, beta1], [beta1, a1]], dtype=float)


def main() -> int:
    identity_rim = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_REDUCTION_NOTE_2026-04-17.md")
    cyclic_bulk = read("docs/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_CYCLIC_BULK_REDUCTION_NOTE_2026-04-17.md")
    propagated_nonclosure = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_PROPAGATED_RETAINED_TRIPLE_OPERATOR_SIDE_NONCLOSURE_NOTE_2026-04-17.md"
    )
    boundary = read("docs/PERRON_FROBENIUS_SELECTION_AXIOM_BOUNDARY_NOTE_2026-04-17.md")

    e3 = sample_matrix()
    _, _, vh = np.linalg.svd(e3)
    kernel = vh[-1]
    kernel_residual = float(np.max(np.abs(e3 @ kernel)))

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

    basis_p, proj_p = krylov_basis(s_p, eta, DEPTH)
    basis_q, proj_q = krylov_basis(s_q, eta, DEPTH)
    krylov_err_p = max(
        float(np.linalg.norm(np.linalg.matrix_power(proj_p @ s_p @ proj_p, n) @ eta - np.linalg.matrix_power(s_p, n) @ eta))
        for n in range(DEPTH + 1)
    )
    krylov_err_q = max(
        float(np.linalg.norm(np.linalg.matrix_power(proj_q @ s_q @ proj_q, n) @ eta - np.linalg.matrix_power(s_q, n) @ eta))
        for n in range(DEPTH + 1)
    )

    j1_p = first_lanczos_block(s_p, eta)
    j1_q = first_lanczos_block(s_q, eta)
    j1_gap = float(np.max(np.abs(j1_p - j1_q)))

    eig_p = np.linalg.eigvalsh(s_p)
    eig_q = np.linalg.eigvalsh(s_q)

    print("=" * 124)
    print("GAUGE-VACUUM PLAQUETTE BETA=6 IDENTITY-RIM FINITE-KRYLOV BULK REDUCTION")
    print("=" * 124)
    print()
    print(f"higher-orbit slice                           = {ORBITS}")
    print(f"sample matrix shape / rank                   = {e3.shape} / {np.linalg.matrix_rank(e3)}")
    print(f"kernel direction                             = {kernel}")
    print(f"kernel residual max-norm                     = {kernel_residual:.12e}")
    print()
    print(f"depth d                                      = {DEPTH}")
    print(f"eta                                          = {eta}")
    print(f"v_P                                          = {v_p}")
    print(f"v_Q                                          = {v_q}")
    print(f"max propagated triple gap                    = {triple_gap:.12e}")
    print(f"triple_P                                     = {triple_p}")
    print(f"triple_Q                                     = {triple_q}")
    print()
    print(f"Krylov reduction errors (P, Q)               = ({krylov_err_p:.3e}, {krylov_err_q:.3e})")
    print(f"2x2 Lanczos block J1^P                       =\n{j1_p}")
    print(f"2x2 Lanczos block J1^Q                       =\n{j1_q}")
    print(f"max 2x2 block gap                            = {j1_gap:.12f}")
    print(f"PSD eigenvalue floors (P, Q)                 = ({eig_p[0]:.12e}, {eig_q[0]:.12e})")
    print()

    check(
        "The identity-rim reduction note already reduces explicit class-sector beta=6 closure to bulk data together with eta_6(e), with generic W dependence already downstream through K(W)",
        "`eta_6(e)`" in identity_rim and "generic marked-holonomy dependence is already" in identity_rim,
        bucket="SUPPORT",
    )
    check(
        "The cyclic-bulk reduction note already sharpens the upstream bulk object from the whole operator to the eta_6(e)-cyclic compression",
        "`eta_6(e)`-cyclic compression of `S_6^env`" in cyclic_bulk
        and "same exact propagated retained triple" in cyclic_bulk,
        bucket="SUPPORT",
    )
    check(
        "The propagated-triple operator-side nonclosure note already says the propagated retained triple is the right finite target but not itself an operator-side closure datum",
        "correct finite *target*" in propagated_nonclosure and "not an operator-side *closure* datum" in propagated_nonclosure,
        bucket="SUPPORT",
    )
    check(
        "The main PF boundary already treats the plaquette lane as a bulk-plus-identity-rim problem rather than a generic W-family problem",
        "identity rim datum `eta_6(e)`" in boundary and "propagated retained three-sample triple" in boundary,
        bucket="SUPPORT",
    )

    check(
        "For fixed depth d, the propagated eta-orbit depends only on the finite Krylov compression Q_d S Q_d",
        krylov_err_p < 1.0e-12 and krylov_err_q < 1.0e-12,
        detail=f"errors=({krylov_err_p:.3e}, {krylov_err_q:.3e})",
    )
    check(
        "So the sharp fixed-depth bulk target is the finite eta_6(e)-generated Krylov block rather than the whole operator or even the whole cyclic object",
        basis_p.shape[1] <= DEPTH + 1 and basis_q.shape[1] <= DEPTH + 1 and krylov_err_p < 1.0e-12 and krylov_err_q < 1.0e-12,
        detail=f"Krylov dims=({basis_p.shape[1]}, {basis_q.shape[1]})",
    )
    check(
        "On the explicit four-orbit slice there are two positive propagated depth-d targets with the same exact propagated retained triple",
        kernel_residual < 1.0e-10 and np.min(v_p) > 0.0 and np.min(v_q) > 0.0 and triple_gap < 1.0e-10,
        detail=f"min(v_Q)={np.min(v_q):.12f}, triple gap={triple_gap:.3e}",
    )
    check(
        "The corresponding rank-one positive bulk witnesses realize those propagated depth-d targets from one common identity rim state eta",
        np.max(np.abs(prop_p - v_p)) < 1.0e-10
        and np.max(np.abs(prop_q - v_q)) < 1.0e-10
        and eig_p[0] > -1.0e-12
        and eig_q[0] > -1.0e-12,
        detail=f"map errors=({np.max(np.abs(prop_p - v_p)):.3e}, {np.max(np.abs(prop_q - v_q)):.3e})",
    )
    check(
        "Even with the same identity rim state and the same exact propagated retained triple, the first 2x2 Krylov/Lanczos bulk block already differs",
        j1_gap > 1.0e-6,
        detail=f"max 2x2 block gap={j1_gap:.12f}",
    )
    check(
        "Therefore the current propagated triple still does not determine even the first finite bulk matrix-element block after the identity-rim reduction",
        triple_gap < 1.0e-10 and j1_gap > 1.0e-6,
        detail="same eta, same propagated triple, different first Krylov block",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
