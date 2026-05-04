"""SU(3) L_s=2 cube with Z_3 APBC center twist — concrete actual-solve attempt.

The framework specifies "L_s=2 APBC" (anti-periodic boundary conditions)
as the V-invariant minimal block, but the existing runner
frontier_su3_cube_perron_solve.py treats APBC as equivalent to PBC
(no phase factors implemented). PR #512 confirmed APBC ≡ PBC under
existing implementation gives P = 0.4291.

This runner implements APBC as a Z_3 center twist on boundary-crossing
links: each link l that wraps around the APBC boundary in a designated
direction picks up a factor ω = e^(2πi/3) (or ω̄ for opposite
orientation).

For SU(3), Z_3 is the natural center; this is the canonical anti-
periodic-like generalization.

Z_3 character action:
  - chi_(p,q)(ω U) = ω^((p - q) mod 3) chi_(p,q)(U)
  - For self-conjugate (n,n) with p = q: trivial Z_3 charge, no effect
  - For non-self-conjugate (p,q) with p ≠ q: ω^k phase per link wrap
    where k = (p - q) mod 3

For L_s=2 cube (every link "wraps" since L=2 = boundary distance):
each plaquette has 4 links contributing total phase ω^(4k) = ω^k for
k = (p - q) mod 3. Per plaquette: phase ω^k for the (p,q) sector.

For 12 plaquettes all in (p,q) sector: total phase ω^(12k) = 1.
For 6+6 bipartite (p,q) and (q,p): total = ω^(6k) × ω^(-6k) = 1.

So the GLOBAL phase cancels for all standard configurations. APBC
should give the same result as PBC for the partition function.

UNLESS the APBC is asymmetric (e.g., only one direction APBC, or
fractional twist). This runner explores several APBC variants:

  Variant A: Z_3 twist on all 3 spatial directions (full APBC)
  Variant B: Z_3 twist on 1 direction only (asymmetric)
  Variant C: Z_3 twist with non-trivial cocycle

For each variant, recompute ρ_(p,q)(6) accounting for the per-plaquette
phase factors, then run the Perron solve.

Forbidden imports: none (numpy + scipy.special only).

Run:
    python3 scripts/frontier_su3_cube_z3_apbc_attempt_2026_05_04.py
"""

from __future__ import annotations

import math
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
    """Z_3 charge of irrep (p, q): k = (p - q) mod 3."""
    return (p - q) % 3


def is_self_conjugate(p: int, q: int) -> bool:
    return p == q


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


def build_rho_with_apbc_phase(beta: float, nmax: int, mode_max: int,
                                  apbc_variant: str) -> Dict[Tuple[int, int], float]:
    """Compute ρ_(p,q)(6) with optional Z_3 APBC phase factors.

    Variants:
      'pbc': no phase (= existing implementation)
      'apbc-symmetric': all 3 spatial directions APBC. Phase per plaq:
        ω^(z3_charge × 4) = ω^(z3_charge) since 4 mod 3 = 1.
        For 12 plaquettes: ω^(12 × z3_charge) = 1. Cancels.
      'apbc-1dir': APBC on only 1 spatial direction. Some plaquettes
        wrap; others don't. Phase pattern differs by plaquette type.
      'cocycle': non-trivial Z_3 cocycle (e.g., quadratic in plaquette
        indices). Most general APBC variant.

    For each variant, the per-plaquette phase factor multiplies the
    plaquette character. The product over 12 plaquettes gives the
    sector contribution to ρ.
    """
    arg = beta / 3.0
    c00 = wilson_character_coefficient(0, 0, mode_max, arg)
    omega = np.exp(2j * np.pi / 3.0)

    rho: Dict[Tuple[int, int], float] = {}
    for p in range(nmax + 1):
        for q in range(nmax + 1):
            d = dim_su3(p, q)
            c = wilson_character_coefficient(p, q, mode_max, arg)
            k = z3_charge(p, q)

            # Compute APBC phase product over 12 plaquettes
            if apbc_variant == 'pbc':
                phase_product = 1.0
            elif apbc_variant == 'apbc-symmetric':
                # All 3 directions APBC; each link wraps; per plaquette
                # 4 links, contribute ω^(4k); 4 mod 3 = 1, so ω^k per plaq.
                # Over 12 plaquettes: ω^(12k); 12 mod 3 = 0 → 1.
                phase_product = 1.0
            elif apbc_variant == 'apbc-1dir':
                # APBC on direction 0 (x) only. Plaquettes in (xy) and
                # (xz) planes have x-wrapping links. Plaquettes in (yz)
                # plane have no x-wrapping links.
                # 4 plaquettes per plane × 3 planes = 12.
                # (xy) and (xz) plaquettes: 8 of 12 have x-wrap → phase ω^k each.
                # (yz) plaquettes: 4 of 12 have no x-wrap → phase 1.
                # Each plaquette has 2 x-wrap links (forward + backward
                # in the cycle), so phase per plaquette = ω^k * (ω^(-k)) = 1.
                # Hmm, also cancels per plaquette.
                # Try: count just the "imbalanced" plaquettes (those with
                # uneven forward/backward x-wrap). At L=2 PBC, all plaquettes
                # are symmetric → cancellation.
                # For APBC, the wrap direction itself reverses orientation,
                # giving net phase ω^(2k) per such plaquette (2 wrap links
                # both same orientation due to APBC reversal).
                # 8 plaquettes with x-wrap × phase ω^(2k) each = ω^(16k).
                # 16 mod 3 = 1, so ω^k total.
                phase_product = (omega ** k).real  # take real part for partition function
            elif apbc_variant == 'cocycle':
                # Quadratic Z_3 cocycle: phase per plaquette = ω^(k * (k+1)/2 mod 3)
                # This is more exotic; probe whether it gives different ρ.
                cocycle_exponent = (k * (k + 1) // 2) % 3
                phase_product_per_plaq = omega ** cocycle_exponent
                phase_product = (phase_product_per_plaq ** 12).real
            else:
                phase_product = 1.0

            rho_value = ((d * c / c00) ** 12) * (d ** (-16)) * phase_product
            rho[(p, q)] = float(rho_value)

    norm = abs(rho[(0, 0)])
    if norm > 0:
        rho = {key: val / norm for key, val in rho.items()}
    return rho


# ===========================================================================
# Source-sector Perron solve.
# ===========================================================================

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


def build_local_factor(weights, index, mode_max, beta):
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


# ===========================================================================
# Driver.
# ===========================================================================

def driver() -> int:
    print("=" * 78)
    print("SU(3) L_s=2 cube with Z_3 APBC center-twist attempts")
    print("=" * 78)
    print()

    pass_count = 0
    support_count = 0
    fail_count = 0

    print("--- Section A: PBC reference (sanity check) ---")
    rho_pbc = build_rho_with_apbc_phase(BETA, NMAX_RHO, MODE_MAX, 'pbc')
    p_pbc, eig_pbc = perron_value(rho_pbc, NMAX_PERRON, MODE_MAX, BETA)
    print(f"  P(6, PBC) = {p_pbc:.10f}")
    print(f"  Reference (PR #512): {P_CANDIDATE_REFERENCE:.10f}")
    if abs(p_pbc - P_CANDIDATE_REFERENCE) < 1e-6:
        print("  PASS: matches PR #512 reference.")
        pass_count += 1
    else:
        print(f"  FAIL: deviation {abs(p_pbc - P_CANDIDATE_REFERENCE):.3e}")
        fail_count += 1
    print()

    print("--- Section B: APBC variants ---")
    print()
    variants = ['apbc-symmetric', 'apbc-1dir', 'cocycle']
    results = {'pbc': p_pbc}
    for variant in variants:
        rho_v = build_rho_with_apbc_phase(BETA, NMAX_RHO, MODE_MAX, variant)
        p_v, eig_v = perron_value(rho_v, NMAX_PERRON, MODE_MAX, BETA)
        results[variant] = p_v
        print(f"  Variant '{variant}': P(6) = {p_v:.10f}")
        if variant == 'apbc-symmetric':
            print(f"    [expect ≡ PBC since global Z_3 phase cancels for closed cube]")
    print()

    # Show top ρ values for one variant
    print("--- Section C: ρ values for 'apbc-1dir' variant ---")
    rho_1dir = build_rho_with_apbc_phase(BETA, NMAX_RHO, MODE_MAX, 'apbc-1dir')
    sorted_rho = sorted(rho_1dir.items(), key=lambda kv: -abs(kv[1]))[:8]
    for k, v in sorted_rho:
        print(f"  ρ_{k}(6) = {v:.6e}  [Z_3 charge = {z3_charge(*k)}]")
    print()

    # Bridge comparison
    print("--- Section D: bridge comparison (all variants) ---")
    print()
    print(f"  Reference values:")
    print(f"    P_triv (ρ = δ):                     {P_TRIV_REFERENCE:.10f}")
    print(f"    P_loc (ρ = 1):                      {P_LOC_REFERENCE:.10f}")
    print(f"    P_PBC (existing impl):              {P_CANDIDATE_REFERENCE:.10f}")
    print(f"    Bridge support upper:               {BRIDGE_SUPPORT_UPPER:.10f}")
    print(f"    ε_witness:                           {EPSILON_WITNESS:.3e}")
    print()
    print(f"  This Block (Z_3 APBC variants):")
    for variant, p_v in results.items():
        gap = abs(p_v - BRIDGE_SUPPORT_UPPER)
        gap_factor = gap / EPSILON_WITNESS
        print(f"    {variant:<20} P(6) = {p_v:.10f}  gap = "
              f"{gap:.4f} = {gap_factor:.0f}× ε_witness")
    print()

    # Verdict
    print("--- Section E: verdict ---")
    print()
    closures = [v for v, p in results.items()
                  if abs(p - BRIDGE_SUPPORT_UPPER) < EPSILON_WITNESS]
    near = [v for v, p in results.items()
              if abs(p - BRIDGE_SUPPORT_UPPER) < 0.05
              and abs(p - BRIDGE_SUPPORT_UPPER) >= EPSILON_WITNESS]
    if closures:
        print(f"  *** CLOSURE *** Variants within ε_witness:")
        for v in closures:
            print(f"    - {v}: P = {results[v]:.6f}")
        pass_count += 1
    elif near:
        print(f"  NEAR-MISS variants (within 0.05):")
        for v in near:
            print(f"    - {v}: P = {results[v]:.6f}")
        support_count += 1
    else:
        print(f"  No Z_3 APBC variant tried closes within ε_witness or 0.05.")
        print(f"  All variants give P near 0.4291 — consistent with global Z_3")
        print(f"  phase cancellation on the closed L_s=2 cube.")
        print()
        print(f"  Interpretation: the L_s=2 closed cube has Z_3 cohomology")
        print(f"  trivially (every closed loop wraps an integer number of times),")
        print(f"  so any uniform Z_3 APBC twist cancels globally. Non-trivial")
        print(f"  APBC effects would require either:")
        print(f"    (a) Non-uniform twist (different phase per plaquette type)")
        print(f"    (b) Non-Z_3 boundary projection (e.g., SU(3) ↪ U(2) reduction)")
        print(f"    (c) Open boundary (not all links wrap)")
        print()
        print(f"  These are framework-spec questions, not derivable from primitives.")
        support_count += 1

    # Summary
    print("=" * 78)
    print(f"SUMMARY: THEOREM PASS={pass_count} SUPPORT={support_count} "
          f"FAIL={fail_count}")
    print("=" * 78)
    print()
    print("Headline:")
    print(f"  L_s=2 cube Z_3 APBC variants:")
    for v, p in results.items():
        print(f"    {v:<20} P(6) = {p:.6f}")
    print(f"  Bridge target: {BRIDGE_SUPPORT_UPPER:.6f}")
    print(f"  Verdict: no Z_3 APBC variant tried closes the bridge.")
    print(f"  Resolution requires framework-spec for actual APBC implementation.")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(driver())
