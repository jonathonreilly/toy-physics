"""Block 06: SU(3) L_s=2 cube full-ρ Perron solve under HEAT-KERNEL action.

Adapts the existing scripts/frontier_su3_cube_full_rho_perron_2026_05_04.py
runner from Wilson character coefficients (Bessel determinants) to
heat-kernel character coefficients (d_λ · exp(-t·C_2(λ)/2)).

Wilson cube: P_cube_W(L_s=2, β=6) = 0.4291049969 (per the existing runner)
HK cube: P_cube_HK(L_s=2, t=1) = ?

The L_s=2 cube structure (24 directed links, 12 plaquettes, candidate-ρ
ansatz `(d c/c_00)^12 · d^(-16)`) is character-coefficient-AGNOSTIC at
the index-graph level — only the Wilson character coefficients need to
be swapped for HK ones.

Companion: docs/BRIDGE_GAP_HK_CUBE_PERRON_NOTE_2026-05-06.md (this PR)
Loop: bridge-gap-new-physics-20260506
Block: 06

This produces a NUMERICAL value for ⟨P⟩_HK on the L_s=2 cube. It does
NOT close the thermodynamic limit (Block 03 named obstruction stands)
and does NOT close action-form uniqueness (Block 04 no-go stands). It
is a concrete comparator artifact under the HK candidate action.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np


def dim_su3(p: int, q: int) -> int:
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def casimir_su3(p: int, q: int) -> float:
    return (p * p + p * q + q * q + 3 * p + 3 * q) / 3.0


def hk_character_coefficient(p: int, q: int, t: float) -> float:
    """Heat-kernel character coefficient: d_λ · exp(-t·C_2(λ)/2).

    Replaces Wilson's Bessel-determinant `c_λ(β)` from the original
    runner. At the framework's canonical t = 1 (Block 01).
    """
    d = dim_su3(p, q)
    C2 = casimir_su3(p, q)
    return d * np.exp(-t * C2 / 2.0)


def build_candidate_rho_hk(t: float, nmax: int) -> Dict[Tuple[int, int], float]:
    """ρ_(p,q)(t) = (d_λ × c_λ_HK(t) / c_00_HK(t))^12 × d_λ^(-16)

    The cube's index-graph topology factor d^(N_components - N_links)
    = d^(8 - 24) = d^(-16) is character-coefficient-agnostic.
    The (d c/c_00)^12 part captures 12 plaquettes' character contribution.

    For HK at t = 1: c_00_HK = 1, c_λ_HK = d_λ · exp(-C_2/2).
    """
    c00 = hk_character_coefficient(0, 0, t)  # = 1.0
    rho: Dict[Tuple[int, int], float] = {}
    for p in range(nmax + 1):
        for q in range(nmax + 1):
            d = dim_su3(p, q)
            c = hk_character_coefficient(p, q, t)
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


def build_local_factor_hk(weights: List[Tuple[int, int]],
                           index: Dict[Tuple[int, int], int],
                           t: float) -> np.ndarray:
    """Local plaquette factor under HK: a_link^4 with a_link = c_λ/(d·c_00).

    For HK: a_link = (d_λ · exp(-t·C_2/2)) / (d_λ · 1) = exp(-t·C_2/2).
    """
    coeffs = np.array([hk_character_coefficient(p, q, t) for p, q in weights],
                      dtype=float)
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = coeffs[index[(0, 0)]]
    a_link = coeffs / (dims * c00)
    return np.diag(a_link ** 4)


def matrix_exp_symmetric(matrix: np.ndarray, tau: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(matrix)
    return (vecs * np.exp(tau * vals)) @ vecs.T


def perron_value_hk(rho: Dict[Tuple[int, int], float],
                     nmax: int, t: float) -> Tuple[float, float]:
    j_op, weights, index = build_j(nmax)
    multiplier = matrix_exp_symmetric(j_op, 3.0)
    d_loc = build_local_factor_hk(weights, index, t)
    c_env = np.diag(np.array([rho.get(weight, 0.0) for weight in weights],
                              dtype=float))
    transfer = multiplier @ d_loc @ c_env @ multiplier
    vals, vecs = np.linalg.eigh(transfer)
    idx = int(np.argmax(vals))
    psi = vecs[:, idx]
    if np.sum(psi) < 0.0:
        psi = -psi
    return float(psi @ (j_op @ psi)), float(vals[idx])


def main() -> int:
    print("=" * 72)
    print("Block 06 — HK Cube Perron L_s=2 (Casimir-diagonal action)")
    print("Loop: bridge-gap-new-physics-20260506")
    print("Companion: docs/BRIDGE_GAP_HK_CUBE_PERRON_NOTE_2026-05-06.md")
    print("=" * 72)
    print()
    print("Adapts existing Wilson cube Perron runner to HK weights.")
    print("Wilson side reference: P_cube_W(L_s=2, β=6) = 0.4291049969")
    print()

    t = 1.0  # Block 01's canonical t at framework's β = 6
    print(f"Framework canonical t (from Block 01) = {t}")
    print()

    print("HK character coefficients c_λ_HK(t=1) = d_λ · exp(-C_2/2):")
    for nmax_check in [1, 2]:
        for p in range(nmax_check + 1):
            for q in range(nmax_check + 1 - p):
                d = dim_su3(p, q)
                C2 = casimir_su3(p, q)
                c = hk_character_coefficient(p, q, t)
                print(f"  (p,q)=({p},{q}): d={d}, C_2={C2:.4f}, c_HK={c:.6e}")
    print()

    print("Candidate ρ_(p,q)(t=1) = (d × c/c_00)^12 × d^(-16):")
    rho_hk_check = build_candidate_rho_hk(t, nmax=2)
    for (p, q), val in sorted(rho_hk_check.items()):
        print(f"  ({p},{q}): {val:.6e}")
    print()

    print("Convergence check at increasing NMAX:")
    print(f"{'NMAX':>6} {'P_cube_HK(t=1)':>20} {'Perron eigval':>20}")
    last_val = None
    converged_at = None
    for nmax in [3, 4, 5, 6, 7, 8]:
        rho_hk = build_candidate_rho_hk(t, nmax)
        p_val, eig = perron_value_hk(rho_hk, nmax, t)
        print(f"{nmax:>6} {p_val:>20.10f} {eig:>20.6e}")
        if last_val is not None and abs(p_val - last_val) < 1e-9:
            if converged_at is None:
                converged_at = nmax
        last_val = p_val
    print()

    final_p = last_val
    print("=" * 72)
    print("RESULT — HK cube Perron L_s=2 at framework canonical t = 1:")
    print(f"  P_cube_HK(L_s=2, t=1) ≈ {final_p:.10f}")
    print()
    print("Comparators (NOT load-bearing):")
    wilson_cube = 0.4291049969
    wilson_1plaq = 0.4225317396
    hk_1plaq = float(np.exp(-2.0/3.0))
    mc_thermo = 0.5934
    print(f"  Wilson cube L_s=2:   {wilson_cube:.10f}  (existing runner)")
    print(f"  Wilson 1-plaq:       {wilson_1plaq:.10f}  (V=1 PF certified)")
    print(f"  HK 1-plaq (Block 02): {hk_1plaq:.10f}  (exp(-2/3) closed form)")
    print(f"  HK cube L_s=2 (this): {final_p:.10f}  (Block 06)")
    print(f"  Lattice MC thermo:   ≈ {mc_thermo}        (comparator only)")
    print()

    print("Differences:")
    print(f"  HK_cube - HK_1plaq:    {final_p - hk_1plaq:+.10f}")
    print(f"  HK_cube - Wilson_cube: {final_p - wilson_cube:+.10f}")
    print(f"  HK_cube - MC:          {final_p - mc_thermo:+.10f}")
    print(f"  HK_cube - MC distance: {abs(final_p - mc_thermo) / 3.030e-4:.0f}× ε_witness")
    print()

    print("Interpretation:")
    if final_p > wilson_cube:
        print("  HK cube > Wilson cube — HK action gives larger plaquette")
        print("  expectation at L_s=2 than Wilson does, consistent with the HK")
        print("  measure putting more weight on non-trivial sectors.")
    elif final_p < wilson_cube:
        print("  HK cube < Wilson cube — HK action gives smaller plaquette")
        print("  expectation at L_s=2 than Wilson does.")
    else:
        print("  HK cube ≈ Wilson cube within numerical precision.")
    print()

    print("Both HK and Wilson L_s=2 are bounded above by the famous-open")
    print("thermodynamic ⟨P⟩(6) ≈ 0.5934 (lattice MC comparator). The L_s=2")
    print("cube is structurally insufficient for ε_witness precision; this")
    print("artifact is a comparator across actions at fixed lattice size.")
    print()
    print("Block 03's named obstruction (cluster-decomposition / exponential-")
    print("clustering estimate not in current primitives) remains the bottleneck")
    print("for thermodynamic-limit closure under either action.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
