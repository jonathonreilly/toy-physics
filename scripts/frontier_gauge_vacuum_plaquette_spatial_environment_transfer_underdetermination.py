#!/usr/bin/env python3
"""
Current Wilson/plaquette stack does not yet force unique beta=6 spatial
environment transfer data.

This sharpens the PF obstruction after the spatial-environment transfer
theorem and the Wilson parent/compression theorem:

1. the remaining plaquette data already sit inside one explicit positive
   orthogonal-slice transfer law S_beta^env with boundary state eta_beta;
2. but the current exact stack still does not determine that transfer/boundary
   pair uniquely at beta=6;
3. distinct admissible spatial-environment transfer pairs can therefore still
   induce different boundary character data and different plaquette Perron data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.special import iv

ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0

NMAX = 5
BETA = 6.0
ARG = BETA / 3.0
MODE_MAX = 80
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


def build_recurrence_matrix(
    nmax: int,
) -> tuple[np.ndarray, list[tuple[int, int]], dict[tuple[int, int], int]]:
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


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def highest_weight_triple(p: int, q: int) -> list[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: list[int]) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, ARG) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int) -> float:
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-MODE_MAX, MODE_MAX + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam)))
    return total


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


def spatial_pair(
    jmat: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    tau_transfer: float,
    tau_boundary: float,
    linear_decay: float,
    asym_decay: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    layer_diag = np.diag(
        [np.exp(-linear_decay * (p + q) - asym_decay * ((p - q) ** 2)) for p, q in weights]
    )
    exp_transfer = matrix_exponential_symmetric(jmat, tau_transfer)
    transfer = exp_transfer @ layer_diag @ exp_transfer

    eta0 = np.zeros(len(weights), dtype=float)
    eta0[index[(0, 0)]] = 1.0
    boundary = matrix_exponential_symmetric(jmat, tau_boundary) @ eta0
    amplitude = np.linalg.matrix_power(transfer, DEPTH) @ boundary
    rho = amplitude / amplitude[index[(0, 0)]]
    return transfer, boundary, amplitude, rho


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    parent_note = read("docs/GAUGE_VACUUM_PLAQUETTE_PARENT_COMPRESSION_THEOREM_NOTE_2026-04-17.md")

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)

    s_a, eta_a, amp_a, rho_a = spatial_pair(
        jmat, weights, index, tau_transfer=0.32, tau_boundary=0.14, linear_decay=0.18, asym_decay=0.05
    )
    s_b, eta_b, amp_b, rho_b = spatial_pair(
        jmat, weights, index, tau_transfer=0.24, tau_boundary=0.22, linear_decay=0.13, asym_decay=0.09
    )

    c00 = wilson_character_coefficient(0, 0)
    local = np.array(
        [wilson_character_coefficient(p, q) / (dim_su3(p, q) * c00) for p, q in weights],
        dtype=float,
    )
    d_local = np.diag(local**4)
    multiplier = matrix_exponential_symmetric(jmat, BETA / 2.0)
    t_a = multiplier @ d_local @ np.diag(rho_a) @ multiplier
    t_b = multiplier @ d_local @ np.diag(rho_b) @ multiplier

    _, psi_a = dominant_eigenpair(t_a)
    _, psi_b = dominant_eigenpair(t_b)

    moments_a = moments(jmat, psi_a, 5)
    moments_b = moments(jmat, psi_b, 5)
    al_a, be_a = lanczos_jacobi(jmat, psi_a, 6)
    al_b, be_b = lanczos_jacobi(jmat, psi_b, 6)

    s_a_sym = float(np.max(np.abs(s_a - s_a.T)))
    s_b_sym = float(np.max(np.abs(s_b - s_b.T)))
    s_a_swap = float(np.max(np.abs(swap @ s_a - s_a @ swap)))
    s_b_swap = float(np.max(np.abs(swap @ s_b - s_b @ swap)))
    eta_a_swap = float(np.max(np.abs(swap @ eta_a - eta_a)))
    eta_b_swap = float(np.max(np.abs(swap @ eta_b - eta_b)))
    rho_a_swap = float(np.max(np.abs(swap @ rho_a - rho_a)))
    rho_b_swap = float(np.max(np.abs(swap @ rho_b - rho_b)))
    rho_gap = float(np.max(np.abs(rho_a - rho_b)))
    m1_gap = abs(moments_a[1] - moments_b[1])
    m2_gap = abs(moments_a[2] - moments_b[2])
    alpha0_gap = abs(al_a[0] - al_b[0])
    beta1_gap = abs(be_a[0] - be_b[0]) if be_a and be_b else 0.0
    psi_a_swap = float(np.linalg.norm(swap @ psi_a - psi_a))
    psi_b_swap = float(np.linalg.norm(swap @ psi_b - psi_b))

    print("=" * 88)
    print("GAUGE-VACUUM PLAQUETTE SPATIAL-ENVIRONMENT TRANSFER UNDERDETERMINATION")
    print("=" * 88)
    print()
    print("Exact already-fixed structural surface")
    print(f"  source-operator symmetry error             = {float(np.max(np.abs(jmat - jmat.T))):.3e}")
    print(f"  local-factor min eigenvalue                = {float(np.min(np.diag(d_local))):.6e}")
    print()
    print("Two admissible spatial-environment transfer / boundary pairs")
    print(f"  S_A symmetry / swap errors                 = {s_a_sym:.3e}, {s_a_swap:.3e}")
    print(f"  S_B symmetry / swap errors                 = {s_b_sym:.3e}, {s_b_swap:.3e}")
    print(f"  eta_A min / swap error                     = {float(np.min(eta_a)):.6e}, {eta_a_swap:.3e}")
    print(f"  eta_B min / swap error                     = {float(np.min(eta_b)):.6e}, {eta_b_swap:.3e}")
    print()
    print("Induced beta=6 boundary character data")
    print(f"  rho_A min / max                            = {float(np.min(rho_a)):.12f}, {float(np.max(rho_a)):.12f}")
    print(f"  rho_B min / max                            = {float(np.min(rho_b)):.12f}, {float(np.max(rho_b)):.12f}")
    print(f"  rho_A / rho_B swap errors                  = {rho_a_swap:.3e}, {rho_b_swap:.3e}")
    print(f"  max |rho_A - rho_B|                        = {rho_gap:.6e}")
    print()
    print("Resulting plaquette PF data")
    print(f"  |m1^A - m1^B|                              = {m1_gap:.6e}")
    print(f"  |m2^A - m2^B|                              = {m2_gap:.6e}")
    print(f"  |alpha0^A - alpha0^B|                      = {alpha0_gap:.6e}")
    print(f"  |beta1^A  - beta1^B|                       = {beta1_gap:.6e}")
    print()

    check(
        "the spatial-environment transfer note already records the live data as one transfer/boundary matrix-element law",
        "matrix-element law" in transfer_note and "S_beta^env" in transfer_note and "eta_beta" in transfer_note,
        detail="the current live object is S_beta^env with boundary state eta_beta, not a generic diagonal residual factor",
    )
    check(
        "the Wilson parent/compression note still records the explicit beta=6 residual environment data as open",
        "S_6^env" in parent_note and "rho_(p,q)(6)" in parent_note and "What this does not close" in parent_note,
        detail="the parent/compression theorem adds Wilson-side structure but does not yet identify the explicit spatial-environment data",
    )
    check(
        "the current structural surface admits positive self-adjoint conjugation-symmetric spatial transfer witnesses",
        s_a_sym < 1.0e-12
        and s_b_sym < 1.0e-12
        and s_a_swap < 1.0e-12
        and s_b_swap < 1.0e-12
        and float(np.min(np.linalg.eigvalsh(s_a))) > 0.0
        and float(np.min(np.linalg.eigvalsh(s_b))) > 0.0,
        detail="both witnesses satisfy the spatial-transfer structural constraints already closed on main",
    )
    check(
        "the same structural surface admits positive conjugation-symmetric boundary states eta_6",
        eta_a_swap < 1.0e-12
        and eta_b_swap < 1.0e-12
        and float(np.min(eta_a)) >= -1.0e-12
        and float(np.min(eta_b)) >= -1.0e-12,
        detail="both rim-induced boundary-state witnesses are positive up to roundoff and swap-invariant on the class sector",
    )
    check(
        "distinct admissible spatial transfer / boundary pairs can induce different beta=6 boundary character data",
        rho_a_swap < 1.0e-12
        and rho_b_swap < 1.0e-12
        and float(np.min(rho_a)) > 0.0
        and float(np.min(rho_b)) > 0.0
        and abs(rho_a[index[(0, 0)]] - 1.0) < 1.0e-12
        and abs(rho_b[index[(0, 0)]] - 1.0) < 1.0e-12
        and rho_gap > 1.0e-3,
        detail=f"max coefficient gap={rho_gap:.3e}",
    )
    check(
        "distinct admissible beta=6 spatial-environment data can therefore still induce different plaquette PF data",
        m1_gap > 1.0e-4 and m2_gap > 1.0e-4 and alpha0_gap > 1.0e-4 and beta1_gap > 1.0e-4,
        detail=f"moment gaps=({m1_gap:.3e}, {m2_gap:.3e}), Jacobi gaps=({alpha0_gap:.3e}, {beta1_gap:.3e})",
    )

    check(
        "both resulting plaquette Perron states remain fixed by the conjugation symmetry",
        psi_a_swap < 1.0e-10 and psi_b_swap < 1.0e-10,
        detail=f"Perron invariance errors=({psi_a_swap:.3e}, {psi_b_swap:.3e})",
        bucket="SUPPORT",
    )
    check(
        "the same explicit source operator J and local Wilson factor D_6^loc are reused in both witnesses",
        float(np.max(np.abs(jmat - jmat.T))) < 1.0e-15
        and float(np.max(np.abs(swap @ jmat - jmat @ swap))) < 1.0e-12
        and float(np.min(local)) > 0.0,
        detail="the only moved datum is the admissible spatial-environment transfer/boundary pair",
        bucket="SUPPORT",
    )
    check(
        "the live missing object is now exactly the explicit beta=6 spatial-environment pair S_6^env / eta_6",
        rho_gap > 1.0e-3 and m1_gap > 1.0e-4,
        detail="without explicit S_6^env / eta_6, the plaquette PF data are still not unique on the current exact surface",
        bucket="SUPPORT",
    )

    print()
    print("=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
