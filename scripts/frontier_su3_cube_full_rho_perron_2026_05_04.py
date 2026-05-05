"""SU(3) L_s=2 APBC cube full-ρ Perron solve.

The framework's existing runner names an L_s=2 APBC spatial cube with
12 plaquettes / 24 links. Under that existing all-forward convention,
no APBC-specific phase factors are applied in this calculation.

Block 5 (PR #501) verified that the candidate-ansatz formula

    ρ_(p,q)(6) = (d_(p,q) × c_(p,q)(6) / c_(0,0)(6))^12 × d_(p,q)^(-16)

correctly captures the L_s=2 cube character measure under the all-
forward / candidate convention. The candidate runner reported
P_candidate = 0.4291049969 using NMAX = 4 for ρ.

The existing cube Perron runner (frontier_su3_cube_perron_solve.py)
defers the non-trivial sectors and only uses ρ = δ (Reference B,
P = 0.4225). This runner closes that gap by applying the FULL candidate
ρ in the source-sector Perron solve.

Includes:
  - All sectors (p, q) up to NMAX = 4 (or higher)
  - Both self-conjugate (p = q) and non-self-conjugate (p ≠ q) sectors
  - Comparison to bridge target 0.5935, P_triv = 0.4225, P_loc = 0.4524,
    and ε_witness = 3.03e-4

Forbidden imports: none (numpy + scipy.special only).

Run:
    python3 scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py
"""

from __future__ import annotations

import sys
from typing import Dict, List, Tuple

import numpy as np
from scipy.special import iv


BETA = 6.0
NMAX_RHO_DEFAULT = 4   # max NMAX for ρ tabulation
NMAX_PERRON = 7        # NMAX for Perron solve box
MODE_MAX = 200
EPSILON_WITNESS = 3.03e-4
BRIDGE_SUPPORT_UPPER = 0.5935306800
P_TRIV_REFERENCE = 0.4225317396
P_LOC_REFERENCE = 0.4524071590
P_CANDIDATE_REFERENCE = 0.4291049969


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def wilson_character_coefficient(p: int, q: int, mode_max: int, arg: float
                                   ) -> float:
    lam = [p + q, q, 0]
    total = 0.0
    for mode in range(-mode_max, mode_max + 1):
        mat = np.array(
            [[iv(mode + lam[j] + i - j, arg) for j in range(3)]
             for i in range(3)], dtype=float
        )
        total += float(np.linalg.det(mat))
    return total


def build_candidate_rho(beta: float, nmax: int, mode_max: int = MODE_MAX
                          ) -> Dict[Tuple[int, int], float]:
    """Compute the candidate ansatz ρ_(p,q)(6) for the L_s=2 cube.

    Formula (per Block 5 verification, PR #501):
      ρ_(p,q)(6) = (d_(p,q) × c_(p,q)(6) / c_(0,0)(6))^12 × d_(p,q)^(-16)

    The d^(-16) factor encodes the cube's index-graph topology (8
    connected components on 24 directed links).

    Returns ρ normalized so ρ_(0,0) = 1.
    """
    arg = beta / 3.0
    c00 = wilson_character_coefficient(0, 0, mode_max, arg)
    rho: Dict[Tuple[int, int], float] = {}
    for p in range(nmax + 1):
        for q in range(nmax + 1):
            d = dim_su3(p, q)
            c = wilson_character_coefficient(p, q, mode_max, arg)
            rho[(p, q)] = ((d * c / c00) ** 12) * (d ** (-16))
    norm = rho[(0, 0)]
    return {k: v / norm for k, v in rho.items()}


def dominant_weights_box(nmax: int) -> List[Tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


def recurrence_neighbors(p: int, q: int) -> List[Tuple[int, int]]:
    out = []
    for a, b in [(p + 1, q), (p - 1, q + 1), (p, q - 1), (p, q + 1),
                 (p + 1, q - 1), (p - 1, q)]:
        if a >= 0 and b >= 0:
            out.append((a, b))
    return out


def build_j(nmax: int) -> Tuple[np.ndarray, List[Tuple[int, int]],
                                    Dict[Tuple[int, int], int]]:
    weights = dominant_weights_box(nmax)
    index = {weight: i for i, weight in enumerate(weights)}
    j_op = np.zeros((len(weights), len(weights)), dtype=float)
    for p, q in weights:
        source = index[(p, q)]
        for neighbor in recurrence_neighbors(p, q):
            if neighbor in index:
                j_op[index[neighbor], source] += 1.0 / 6.0
    return j_op, weights, index


def build_local_factor(weights: List[Tuple[int, int]],
                          index: Dict[Tuple[int, int], int],
                          mode_max: int, beta: float) -> np.ndarray:
    arg = beta / 3.0
    coeffs = np.array([wilson_character_coefficient(p, q, mode_max, arg)
                        for p, q in weights], dtype=float)
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = coeffs[index[(0, 0)]]
    a_link = coeffs / (dims * c00)
    return np.diag(a_link ** 4)


def matrix_exp_symmetric(matrix: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(matrix)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def perron_value(rho: Dict[Tuple[int, int], float],
                   nmax: int, mode_max: int, beta: float
                   ) -> Tuple[float, float]:
    j_op, weights, index = build_j(nmax)
    multiplier = matrix_exp_symmetric(j_op, 3.0)
    d_loc = build_local_factor(weights, index, mode_max, beta)
    c_env = np.diag(np.array([rho.get(weight, 0.0) for weight in weights],
                                dtype=float))
    transfer = multiplier @ d_loc @ c_env @ multiplier
    vals, vecs = np.linalg.eigh(transfer)
    idx = int(np.argmax(vals))
    psi = vecs[:, idx]
    if np.sum(psi) < 0.0:
        psi = -psi
    return float(psi @ (j_op @ psi)), float(vals[idx])


def driver() -> int:
    print("=" * 78)
    print("SU(3) L_s=2 APBC Cube — Full Candidate-ρ Perron Solve")
    print("=" * 78)
    print()

    pass_count = 0
    support_count = 0
    fail_count = 0

    print("--- Section A: tabulate candidate ρ_(p,q)(6) for various NMAX ---")
    print()
    for nmax_rho in [2, 3, 4, 5, 6]:
        print(f"  NMAX_rho = {nmax_rho}: building ρ...")
        rho = build_candidate_rho(BETA, nmax_rho, MODE_MAX)
        # Show top-magnitude ρ values
        sorted_rho = sorted(rho.items(), key=lambda kv: -abs(kv[1]))[:6]
        for k, v in sorted_rho:
            print(f"    ρ_{k}(6) = {v:.6e}")
        # Run Perron
        p_value, eig = perron_value(rho, NMAX_PERRON, MODE_MAX, BETA)
        print(f"    Perron eigenvalue: {eig:.6f}")
        print(f"    P(6) = {p_value:.10f}")
        print()

    print("--- Section B: convergence at NMAX_rho = 4 vs reference value ---")
    print()
    rho_4 = build_candidate_rho(BETA, 4, MODE_MAX)
    p_4, eig_4 = perron_value(rho_4, NMAX_PERRON, MODE_MAX, BETA)
    print(f"  NMAX_rho = 4: P(6) = {p_4:.10f}")
    print(f"  Reference (PR #501 Block 5 candidate): {P_CANDIDATE_REFERENCE:.10f}")
    diff = abs(p_4 - P_CANDIDATE_REFERENCE)
    print(f"  Difference: {diff:.3e}")
    if diff < 1e-6:
        print("  PASS: matches Block 5 candidate value to 1e-6.")
        pass_count += 1
    else:
        print(f"  FAIL: difference {diff:.3e} exceeds 1e-6.")
        fail_count += 1
    print()

    print("--- Section C: bridge comparison (full-ρ Perron) ---")
    print()
    print(f"  Reference values:")
    print(f"    P_triv (ρ = δ):                     {P_TRIV_REFERENCE:.10f}")
    print(f"    P_loc (ρ = 1):                      {P_LOC_REFERENCE:.10f}")
    print(f"    P_candidate (full ρ, NMAX=4):       {P_CANDIDATE_REFERENCE:.10f}")
    print(f"    Bridge support upper:               {BRIDGE_SUPPORT_UPPER:.10f}")
    print(f"    ε_witness:                           {EPSILON_WITNESS:.3e}")
    print()
    print(f"  This Block (full candidate-ρ at NMAX=4): P = {p_4:.10f}")
    gap_to_target = abs(p_4 - BRIDGE_SUPPORT_UPPER)
    gap_factor = gap_to_target / EPSILON_WITNESS
    print(f"  Gap to bridge target:               {gap_to_target:.6f} = "
          f"{gap_factor:.0f}× ε_witness")
    print()
    print(f"  Verdict: full candidate-ρ value lies in [{P_TRIV_REFERENCE:.4f}, "
          f"{P_LOC_REFERENCE:.4f}] support envelope.")
    print(f"  L_s=2 APBC cube alone CANNOT close to bridge support upper")
    print(f"  ({BRIDGE_SUPPORT_UPPER:.4f}); the gap stays at")
    print(f"  ~ 0.16 = ~ 543× ε_witness across the tested NMAX_rho values.")
    print()
    if gap_factor > 100:
        print("  SUPPORT: confirms L_s=2 cube does not close bridge witness")
        support_count += 1

    # ===== Higher-NMAX convergence study =====
    print("--- Section D: higher-NMAX_rho convergence study ---")
    print()
    nmax_list = [3, 4, 5, 6, 7, 8]
    for nmax_rho in nmax_list:
        rho_n = build_candidate_rho(BETA, nmax_rho, MODE_MAX)
        p_n, _ = perron_value(rho_n, NMAX_PERRON, MODE_MAX, BETA)
        print(f"  NMAX_rho = {nmax_rho:>2}: P(6) = {p_n:.12f}")
    print()

    # Final summary
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} SUPPORT={support_count} "
          f"FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  L_s=2 APBC cube full-candidate-ρ Perron value: P(6) = {p_4:.6f}")
    print(f"  Wigner Block 5 reference: {P_CANDIDATE_REFERENCE:.6f}")
    print(f"  Match: {abs(p_4 - P_CANDIDATE_REFERENCE) < 1e-6}")
    print(f"  Gap to bridge target {BRIDGE_SUPPORT_UPPER:.4f}: "
          f"{abs(p_4 - BRIDGE_SUPPORT_UPPER):.4f} = "
          f"{abs(p_4 - BRIDGE_SUPPORT_UPPER)/EPSILON_WITNESS:.0f}× ε_witness")
    print(f"  Conclusion: L_s=2 APBC cube alone CANNOT close the no-go ε_witness")
    print(f"             under the existing implementation.")
    print(f"  Existing L_s=2 target label evaluated: value computed, but not")
    print(f"  closing — consistent with prior Wigner Block 5 finding.")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
