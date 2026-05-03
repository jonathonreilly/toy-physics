"""Native 3+1 tube staging probe for the gauge-scalar bridge program.

This runner computes K-plaquette tube Perron data on the framework
V-invariant minimal block. It is an open-gate staging probe, not a
lower-bound theorem: the L_s=2 APBC spatial cube has a specific finite
geometry and need not equal or dominate any tube member.

Forbidden imports preserved:
  - no PDG plaquette value
  - no lattice-MC plaquette value as derivation input
  - no fitted beta_eff
  - no perturbative beta-function bridge as derivation
  - no same-surface family argument
"""

from __future__ import annotations

import sys
from typing import Dict, List, Tuple

import numpy as np
from scipy.special import iv


BETA = 6.0
NMAX_DEFAULT = 7
MODE_MAX_DEFAULT = 200
BRIDGE_SUPPORT_UPPER_CANDIDATE = 0.593530679977098
EPSILON_WITNESS = 3.03e-4


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def highest_weight_triple(p: int, q: int) -> List[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: List[int], arg: float) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, arg) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int, mode_max: int, arg: float) -> float:
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-mode_max, mode_max + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam, arg)))
    return total


def weights_box(nmax: int) -> List[Tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def recurrence_neighbors(p: int, q: int) -> List[Tuple[int, int]]:
    out: List[Tuple[int, int]] = []
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


def build_j(nmax: int) -> Tuple[np.ndarray, List[Tuple[int, int]], Dict[Tuple[int, int], int]]:
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    j = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in recurrence_neighbors(p, q):
            if (a, b) in index:
                j[index[(a, b)], i] += 1.0 / 6.0
    return j, weights, index


def build_local_factor(weights, index, mode_max, beta):
    arg = beta / 3.0
    c_lam = np.array(
        [wilson_character_coefficient(p, q, mode_max, arg) for p, q in weights],
        dtype=float,
    )
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = c_lam[index[(0, 0)]]
    a_link = c_lam / (dims * c00)
    return np.diag(a_link**4), c_lam, c00


def matrix_exp_symmetric(m: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(m)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def perron_state_and_value(transfer: np.ndarray, j_op: np.ndarray) -> Tuple[float, float]:
    vals, vecs = np.linalg.eigh(transfer)
    idx = int(np.argmax(vals))
    psi = vecs[:, idx]
    if np.sum(psi) < 0.0:
        psi = -psi
    eigval = float(vals[idx])
    expectation = float(psi @ (j_op @ psi))
    return eigval, expectation


def k_plaquette_tube_perron(
    multiplier: np.ndarray,
    d_loc: np.ndarray,
    j_op: np.ndarray,
    c_lam: np.ndarray,
    c00: float,
    k: int,
) -> Tuple[float, float]:
    if k == 0:
        rho = np.ones_like(c_lam)
    else:
        rho = (c_lam / c00) ** k
    transfer = multiplier @ d_loc @ np.diag(rho) @ multiplier
    return perron_state_and_value(transfer, j_op)


def compute_pieces(beta: float, nmax: int, mode_max: int):
    j_op, weights, index = build_j(nmax)
    d_loc, c_lam, c00 = build_local_factor(weights, index, mode_max, beta)
    multiplier = matrix_exp_symmetric(j_op, beta / 2.0)
    return j_op, index, d_loc, c_lam, c00, multiplier


def driver(beta: float = BETA, nmax: int = NMAX_DEFAULT, mode_max: int = MODE_MAX_DEFAULT) -> int:
    print("=" * 78)
    print("Native 3+1 tube staging gate for <P>(beta=6)")
    print(f"  V-invariant minimal block; NMAX={nmax}, MODE_MAX={mode_max}")
    print("=" * 78)
    print()

    pass_count = 0
    support_count = 0
    fail_count = 0

    j_op, index, d_loc, c_lam, c00, multiplier = compute_pieces(beta, nmax, mode_max)

    print("--- A. Existing reference Perron solves ---")
    proj_delta = np.zeros_like(j_op)
    proj_delta[index[(0, 0)], index[(0, 0)]] = 1.0
    eig_a, p_a = perron_state_and_value(multiplier @ d_loc @ multiplier, j_op)
    eig_b, p_b = perron_state_and_value(multiplier @ d_loc @ proj_delta @ multiplier, j_op)
    print(f"  Reference A (rho = 1):     P(6) = {p_a:.10f}  eig = {eig_a:.6f}")
    print(f"  Reference B (rho = delta): P(6) = {p_b:.10f}  eig = {eig_b:.6f}")
    if abs(p_a - 0.4524071590) < 5e-10 and abs(p_b - 0.4225317396) < 5e-10:
        print("  PASS: reference solves reproduce the frozen values.")
        pass_count += 1
    else:
        print("  FAIL: reference solves drifted from frozen values.")
        fail_count += 1
    print()

    print("--- B. K-plaquette tube Perron probe ---")
    tube_values: Dict[int, float] = {}
    for k in range(7):
        eig_k, p_k = k_plaquette_tube_perron(multiplier, d_loc, j_op, c_lam, c00, k)
        tube_values[k] = p_k
        print(f"  k = {k}  ->  P(6) = {p_k:.10f}  eig = {eig_k:.6f}")
    monotone = all(tube_values[k + 1] >= tube_values[k] for k in range(6))
    finite = all(np.isfinite(v) and v > 0 for v in tube_values.values())
    if finite and monotone:
        print("  PASS: tube values are positive, finite, and monotone over k=0..6.")
        pass_count += 1
    else:
        print("  FAIL: tube probe lost positivity, finiteness, or monotonicity.")
        fail_count += 1
    print()

    print("--- C. Lower-bound guard ---")
    tube_min = min(tube_values.values())
    tube_max = max(tube_values.values())
    tube_span = tube_max - tube_min
    print(f"  Existing strict reference floor: P_delta = {p_b:.10f}")
    print(f"  Tube range over k=0..6: [{tube_min:.10f}, {tube_max:.10f}]")
    print(f"  Tube span: {tube_span:.10f}")
    print("  The tube minimum is staging data, not a physical-cube lower bound.")
    if p_b < tube_min:
        print("  PASS: strict floor remains the delta reference below the tube range.")
        pass_count += 1
    else:
        print("  FAIL: expected strict floor to remain below the tube range.")
        fail_count += 1
    print()

    print("--- D. Witness-scale comparison ---")
    support_width = BRIDGE_SUPPORT_UPPER_CANDIDATE - p_b
    tube_to_upper_gap = BRIDGE_SUPPORT_UPPER_CANDIDATE - tube_min
    print(f"  Support envelope width from existing floor: {support_width:.6f}")
    print(f"  Tube-min-to-upper gap, for orientation only: {tube_to_upper_gap:.6f}")
    print(f"  epsilon_witness from the no-go: {EPSILON_WITNESS:.3e}")
    if support_width > EPSILON_WITNESS and tube_to_upper_gap > EPSILON_WITNESS:
        print("  SUPPORT: staging data do not close the witness-scale bridge.")
        support_count += 1
    else:
        print("  FAIL: witness comparison unexpectedly claims closure.")
        fail_count += 1
    print()

    print("--- E. NMAX convergence check at k=1 ---")
    convergence: Dict[int, float] = {}
    for nm in [3, 4, 5, 6, 7]:
        j_n, _, d_n, c_n, c00_n, m_n = compute_pieces(beta, nm, mode_max)
        _, p_n = k_plaquette_tube_perron(m_n, d_n, j_n, c_n, c00_n, 1)
        convergence[nm] = p_n
        print(f"  NMAX = {nm}  ->  P(k=1, beta=6) = {p_n:.12f}")
    drift = abs(convergence[7] - convergence[6])
    print(f"  Truncation drift |P(NMAX=7) - P(NMAX=6)| = {drift:.3e}")
    if drift < 1e-6:
        print("  PASS: NMAX convergence verified for the staging probe.")
        pass_count += 1
    else:
        print("  FAIL: NMAX truncation did not converge.")
        fail_count += 1
    print()

    print("=" * 78)
    print(f"SUMMARY: STAGING PASS={pass_count} SUPPORT={support_count} FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  Tube data: P(6) in [{tube_min:.6f}, {tube_max:.6f}] for k=0..6.")
    print(f"  Strict floor unchanged: P_delta = {p_b:.6f}.")
    print("  Closure target unchanged: compute the actual L_s=2 APBC cube rho_(p,q)(6).")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
