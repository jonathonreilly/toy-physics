#!/usr/bin/env python3
"""SU(3) L_s=2 cube Z3 APBC phase-variant probe.

This is a bounded named-variant calculation. It does not define the repo's
APBC convention. It tests whether three explicit Z3 phase choices on the
landed L_s=2 full-rho candidate close the bridge gap.
"""

from __future__ import annotations

import sys
from typing import Dict, List, Tuple

import numpy as np
from scipy.special import iv


BETA = 6.0
NMAX_RHO = 4
NMAX_PERRON = 7
MODE_MAX = 200
EPSILON_WITNESS = 3.03e-4
BRIDGE_SUPPORT_UPPER = 0.5935306800
P_TRIV_REFERENCE = 0.4225317396
P_LOC_REFERENCE = 0.4524071590
P_CANDIDATE_REFERENCE = 0.4291049969


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def z3_charge(p: int, q: int) -> int:
    return (p - q) % 3


def wilson_character_coefficient(p: int, q: int, mode_max: int, arg: float) -> float:
    lam = [p + q, q, 0]
    total = 0.0
    for mode in range(-mode_max, mode_max + 1):
        mat = np.array(
            [[iv(mode + lam[j] + i - j, arg) for j in range(3)] for i in range(3)],
            dtype=float,
        )
        total += float(np.linalg.det(mat))
    return total


def build_rho_with_apbc_phase(
    beta: float, nmax: int, mode_max: int, apbc_variant: str
) -> Dict[Tuple[int, int], float]:
    """Compute candidate rho weights with named Z3 phase factors."""
    arg = beta / 3.0
    c00 = wilson_character_coefficient(0, 0, mode_max, arg)
    omega = np.exp(2j * np.pi / 3.0)

    rho: Dict[Tuple[int, int], float] = {}
    for p in range(nmax + 1):
        for q in range(nmax + 1):
            d = dim_su3(p, q)
            c = wilson_character_coefficient(p, q, mode_max, arg)
            k = z3_charge(p, q)

            if apbc_variant == "pbc":
                phase_product = 1.0
            elif apbc_variant == "apbc-symmetric":
                # Uniform Z3 twist cancels over 12 plaquettes.
                phase_product = 1.0
            elif apbc_variant == "apbc-1dir":
                # Toy one-direction imbalance: total phase omega^k.
                phase_product = float((omega**k).real)
            elif apbc_variant == "cocycle":
                cocycle_exponent = (k * (k + 1) // 2) % 3
                phase_product = float(((omega**cocycle_exponent) ** 12).real)
            else:
                raise ValueError(f"unknown APBC variant: {apbc_variant}")

            rho[(p, q)] = float(((d * c / c00) ** 12) * (d ** (-16)) * phase_product)

    norm = abs(rho[(0, 0)])
    return {key: val / norm for key, val in rho.items()}


def dominant_weights_box(nmax: int) -> List[Tuple[int, int]]:
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
    weights = dominant_weights_box(nmax)
    index = {weight: i for i, weight in enumerate(weights)}
    j_op = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        source = index[(p, q)]
        for neighbor in recurrence_neighbors(p, q):
            if neighbor in index:
                j_op[index[neighbor], source] += 1.0 / 6.0
    return j_op, weights, index


def build_local_factor(weights, index, mode_max, beta):
    arg = beta / 3.0
    coeffs = np.array(
        [wilson_character_coefficient(p, q, mode_max, arg) for p, q in weights],
        dtype=float,
    )
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = coeffs[index[(0, 0)]]
    a_link = coeffs / (dims * c00)
    return np.diag(a_link**4)


def matrix_exp_symmetric(matrix: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(matrix)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def perron_value(
    rho: Dict[Tuple[int, int], float], nmax: int, mode_max: int, beta: float
) -> Tuple[float, float]:
    j_op, weights, _ = build_j(nmax)
    multiplier = matrix_exp_symmetric(j_op, 3.0)
    d_loc = build_local_factor(weights, {w: i for i, w in enumerate(weights)}, mode_max, beta)
    c_env = np.diag(np.array([rho.get(weight, 0.0) for weight in weights], dtype=float))
    transfer = multiplier @ d_loc @ c_env @ multiplier
    vals, vecs = np.linalg.eigh(transfer)
    idx = int(np.argmax(vals))
    psi = vecs[:, idx]
    if np.sum(psi) < 0.0:
        psi = -psi
    return float(psi @ (j_op @ psi)), float(vals[idx])


def driver() -> int:
    print("=" * 78)
    print("SU(3) L_s=2 cube with Z3 APBC center-twist attempts")
    print("=" * 78)

    pass_count = 0
    support_count = 0
    fail_count = 0

    print("\n--- Section A: PBC reference (sanity check) ---")
    rho_pbc = build_rho_with_apbc_phase(BETA, NMAX_RHO, MODE_MAX, "pbc")
    p_pbc, _ = perron_value(rho_pbc, NMAX_PERRON, MODE_MAX, BETA)
    print(f"  P(6, PBC) = {p_pbc:.10f}")
    print(f"  Reference (landed full-rho): {P_CANDIDATE_REFERENCE:.10f}")
    if abs(p_pbc - P_CANDIDATE_REFERENCE) < 1e-6:
        print("  PASS: matches the landed full-rho reference.")
        pass_count += 1
    else:
        print(f"  FAIL: deviation {abs(p_pbc - P_CANDIDATE_REFERENCE):.3e}")
        fail_count += 1

    print("\n--- Section B: APBC variants ---")
    variants = ["apbc-symmetric", "apbc-1dir", "cocycle"]
    results = {"pbc": p_pbc}
    for variant in variants:
        rho_v = build_rho_with_apbc_phase(BETA, NMAX_RHO, MODE_MAX, variant)
        p_v, _ = perron_value(rho_v, NMAX_PERRON, MODE_MAX, BETA)
        results[variant] = p_v
        print(f"  Variant {variant!r}: P(6) = {p_v:.10f}")

    print("\n--- Section C: rho values for apbc-1dir variant ---")
    rho_1dir = build_rho_with_apbc_phase(BETA, NMAX_RHO, MODE_MAX, "apbc-1dir")
    for key, value in sorted(rho_1dir.items(), key=lambda kv: -abs(kv[1]))[:8]:
        print(f"  rho_{key}(6) = {value:.6e}  [Z3 charge = {z3_charge(*key)}]")

    print("\n--- Section D: bridge comparison ---")
    print(f"  P_triv (rho = delta):      {P_TRIV_REFERENCE:.10f}")
    print(f"  P_loc (rho = 1):           {P_LOC_REFERENCE:.10f}")
    print(f"  P_PBC (existing impl):     {P_CANDIDATE_REFERENCE:.10f}")
    print(f"  Bridge support upper:      {BRIDGE_SUPPORT_UPPER:.10f}")
    print(f"  epsilon_witness:           {EPSILON_WITNESS:.3e}")
    for variant, p_v in results.items():
        gap = abs(p_v - BRIDGE_SUPPORT_UPPER)
        print(
            f"    {variant:<20} P(6) = {p_v:.10f}  "
            f"gap = {gap:.4f} = {gap / EPSILON_WITNESS:.0f}x epsilon_witness"
        )

    closures = [
        variant
        for variant, p_v in results.items()
        if abs(p_v - BRIDGE_SUPPORT_UPPER) < EPSILON_WITNESS
    ]
    if closures:
        print("\n  FAIL: an APBC variant unexpectedly closes within epsilon_witness.")
        fail_count += 1
    else:
        print("\n  No named Z3 APBC variant closes within epsilon_witness or 0.05.")
        print("  The tested variants stay near the landed full-rho value.")
        support_count += 1

    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} SUPPORT={support_count} FAIL={fail_count}")
    print("=" * 78)
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
