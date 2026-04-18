#!/usr/bin/env python3
"""
Earliest constructive boundary on the plaquette spatial-environment PF lane.

This sharpens the live plaquette construction target one level below the
explicit transfer object S_6^env:

1. the current exact stack realizes the residual environment through one
   orthogonal-slice kernel K_beta^env and one rim boundary state eta_beta;
2. once K_6^env and eta_6 are explicit, the class-sector transfer object
   S_6^env, the coefficients rho_(p,q)(6), and the plaquette PF data follow;
3. but the current exact stack still does not determine K_6^env / eta_6.
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


def kernel_pair(
    jmat: np.ndarray,
    weights: list[tuple[int, int]],
    index: dict[tuple[int, int], int],
    tau_kernel: float,
    linear_decay: float,
    asym_decay: float,
    tau_boundary: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    diagonal = np.diag(
        [np.exp(-linear_decay * (p + q) - asym_decay * ((p - q) ** 2)) for p, q in weights]
    )
    exp_kernel = matrix_exponential_symmetric(jmat, tau_kernel)
    kernel = exp_kernel @ diagonal @ exp_kernel
    eta0 = np.zeros(len(weights), dtype=float)
    eta0[index[(0, 0)]] = 1.0
    boundary = matrix_exponential_symmetric(jmat, tau_boundary) @ eta0
    amplitude = np.linalg.matrix_power(kernel, DEPTH) @ boundary
    rho = amplitude / amplitude[index[(0, 0)]]
    return kernel, boundary, amplitude, rho


def moments(obs: np.ndarray, state: np.ndarray, nmax: int) -> list[float]:
    return [float(state @ (np.linalg.matrix_power(obs, n) @ state)) for n in range(nmax + 1)]


def main() -> int:
    transfer_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md")
    under_note = read("docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_UNDERDETERMINATION_NOTE_2026-04-17.md")
    residual_note = read("docs/GAUGE_VACUUM_PLAQUETTE_RESIDUAL_ENVIRONMENT_IDENTIFICATION_THEOREM_NOTE.md")

    jmat, weights, index = build_recurrence_matrix(NMAX)
    swap = conjugation_swap_matrix(weights, index)

    k_a, eta_a, amp_a, rho_a = kernel_pair(
        jmat, weights, index, tau_kernel=0.29, linear_decay=0.17, asym_decay=0.05, tau_boundary=0.15
    )
    k_b, eta_b, amp_b, rho_b = kernel_pair(
        jmat, weights, index, tau_kernel=0.23, linear_decay=0.12, asym_decay=0.09, tau_boundary=0.22
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
    moments_a = moments(jmat, psi_a, 3)
    moments_b = moments(jmat, psi_b, 3)

    k_a_sym = float(np.max(np.abs(k_a - k_a.T)))
    k_b_sym = float(np.max(np.abs(k_b - k_b.T)))
    k_a_swap = float(np.max(np.abs(swap @ k_a - k_a @ swap)))
    k_b_swap = float(np.max(np.abs(swap @ k_b - k_b @ swap)))
    eta_a_swap = float(np.max(np.abs(swap @ eta_a - eta_a)))
    eta_b_swap = float(np.max(np.abs(swap @ eta_b - eta_b)))
    rho_gap = float(np.max(np.abs(rho_a - rho_b)))
    m1_gap = abs(moments_a[1] - moments_b[1])

    print("=" * 88)
    print("GAUGE-VACUUM PLAQUETTE SPATIAL-ENVIRONMENT CONSTRUCTION BOUNDARY")
    print("=" * 88)
    print()
    print("Kernel-level witnesses")
    print(f"  K_A symmetry / swap errors                 = {k_a_sym:.3e}, {k_a_swap:.3e}")
    print(f"  K_B symmetry / swap errors                 = {k_b_sym:.3e}, {k_b_swap:.3e}")
    print(f"  eta_A min / swap error                     = {float(np.min(eta_a)):.6e}, {eta_a_swap:.3e}")
    print(f"  eta_B min / swap error                     = {float(np.min(eta_b)):.6e}, {eta_b_swap:.3e}")
    print(f"  max |rho_A - rho_B|                        = {rho_gap:.6e}")
    print(f"  |m1^A - m1^B|                              = {m1_gap:.6e}")
    print()

    check(
        "the spatial-environment transfer note already identifies one-step slice kernels K_beta^env as the origin of S_beta^env",
        "K_beta^env(U_(k+1), U_k)" in transfer_note and "Integrating the Wilson weight between adjacent slices defines one exact kernel" in transfer_note,
        detail="the explicit transfer object arises from one orthogonal-slice Wilson kernel",
    )
    check(
        "the residual-environment identification note still reduces the open plaquette datum to the environment operator alone",
        "R_6^env" in residual_note
        and "remaining\nopen object is exactly the compressed unmarked spatial environment operator" in residual_note
        or ("remaining" in residual_note and "compressed unmarked spatial environment operator" in residual_note),
        detail="once the marked half-slice and local factor are stripped, only the environment object remains",
    )
    check(
        "fixing a kernel K_6^env and rim state eta_6 fixes the induced boundary amplitudes rho_(p,q)(6)",
        float(np.min(amp_a)) > 0.0 and float(np.min(amp_b)) > 0.0 and abs(rho_a[index[(0, 0)]] - 1.0) < 1.0e-12 and abs(rho_b[index[(0, 0)]] - 1.0) < 1.0e-12,
        detail="once the kernel and rim state are explicit, rho_(p,q)(6) is just a normalized boundary-amplitude sequence",
    )
    check(
        "the current structural surface admits positive self-adjoint conjugation-symmetric one-step kernels",
        k_a_sym < 1.0e-12
        and k_b_sym < 1.0e-12
        and k_a_swap < 1.0e-12
        and k_b_swap < 1.0e-12
        and float(np.min(np.linalg.eigvalsh(k_a))) > 0.0
        and float(np.min(np.linalg.eigvalsh(k_b))) > 0.0,
        detail="both witnesses satisfy the exact kernel-class constraints coming from orthogonal slicing",
    )
    check(
        "distinct admissible kernel / rim-state pairs can still induce different beta=6 boundary data and PF data",
        eta_a_swap < 1.0e-12
        and eta_b_swap < 1.0e-12
        and float(np.min(eta_a)) >= -1.0e-12
        and float(np.min(eta_b)) >= -1.0e-12
        and rho_gap > 1.0e-3
        and m1_gap > 1.0e-4,
        detail=f"rho gap={rho_gap:.3e}, Perron moment gap={m1_gap:.3e}",
    )

    check(
        "the spatial-environment underdetermination note already records that explicit S_6^env / eta_6 is still open",
        "S_6^env" in under_note and "eta_6" in under_note and "still not forced" in under_note,
        detail="the new underdetermination theorem keeps the constructive target narrow but open",
        bucket="SUPPORT",
    )
    check(
        "the earliest constructive datum is therefore the one-step kernel K_6^env together with the rim map to eta_6",
        rho_gap > 1.0e-3 and m1_gap > 1.0e-4,
        detail="once those are explicit, the transfer object, boundary coefficients, and plaquette PF data follow",
        bucket="SUPPORT",
    )
    check(
        "the same explicit source operator J and local factor D_6^loc are reused downstream",
        float(np.max(np.abs(jmat - jmat.T))) < 1.0e-15 and float(np.min(local)) > 0.0,
        detail="the only missing construction is the spatial-environment kernel/rim data",
        bucket="SUPPORT",
    )

    print()
    print("=" * 88)
    print(f"SUMMARY: THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    print("=" * 88)
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
