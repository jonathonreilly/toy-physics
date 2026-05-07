"""
Cl(3) → KS single-plaquette: action-form ambiguity spread in the
Hamiltonian picture.

Convention (cleaner than v1): magnetic_coeffs maps an unordered conjugate
pair {λ, λ*} (represented by canonical (p,q) with p ≤ q, or self-conjugate
(p,p)) to a real coefficient c_λ that multiplies Re χ_λ = (χ_λ + χ_{λ*})/2
in the magnetic operator.

Tested choices (all rescaled to the same continuum-matching value):

  Wilson-form (W):     {(1,0): c} only — pure fundamental
  Manton-like (M):     {(1,0): a, (1,1): b} with continuum-match constraint
  HK-like (HK):        {(1,0): a, (1,1): b, (2,0): c} truncated, Casimir-graded
"""

from __future__ import annotations

import math
import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import (
    casimir,
    dim_irrep,
    fund_tensor_pq,
    antifund_tensor_pq,
    build_basis,
    expectation_re_tr_U_over_Nc,
)


# -------------------------------------------------------------------
# General SU(3) tensor product via repeated fundamental tensoring
# -------------------------------------------------------------------

def tensor_with_fund(d):
    """d: dict {(p,q): mult}. Tensor each entry with (1,0)."""
    out = {}
    for (p, q), m in d.items():
        for x in fund_tensor_pq(p, q):
            out[x] = out.get(x, 0) + m
    return out


def tensor_with_antifund(d):
    out = {}
    for (p, q), m in d.items():
        for x in antifund_tensor_pq(p, q):
            out[x] = out.get(x, 0) + m
    return out


def subtract(d, e):
    out = dict(d)
    for k, v in e.items():
        out[k] = out.get(k, 0) - v
    return {k: v for k, v in out.items() if v != 0}


def tensor_general(lam, mu):
    """
    Decompose χ_λ ⊗ χ_μ for SU(3) using:
      (1,0) ⊗ x  -- known
      (0,1) ⊗ x  -- known
      (p,q) = (1,0) ⊗ (p-1,q) - (p-1,q-1) - ((p-2,q+1) if p>=2 else 0)
              ... etc, by Pieri/Klimyk.

    For our purposes we only need a few λ. We implement directly:

      (0,0) ⊗ μ = {μ: 1}
      (1,0) ⊗ μ = via fund_tensor_pq
      (0,1) ⊗ μ = via antifund_tensor_pq
      (1,1) ⊗ μ = (1,0)⊗(0,1)⊗μ - μ
      (2,0) ⊗ μ = (1,0)⊗(1,0)⊗μ - (0,1)⊗μ
      (0,2) ⊗ μ = (0,1)⊗(0,1)⊗μ - (1,0)⊗μ
    """
    if lam == (0, 0):
        return {mu: 1}
    if lam == (1, 0):
        return {x: 1 for x in fund_tensor_pq(*mu)} | _multi(fund_tensor_pq(*mu))
    if lam == (0, 1):
        return _multi(antifund_tensor_pq(*mu))
    if lam == (1, 1):
        # (1,0) ⊗ (0,1) ⊗ μ - μ
        step1 = _multi(antifund_tensor_pq(*mu))
        step2 = tensor_with_fund(step1)
        return subtract(step2, {mu: 1})
    if lam == (2, 0):
        # (1,0) ⊗ (1,0) ⊗ μ - (0,1) ⊗ μ
        step1 = _multi(fund_tensor_pq(*mu))
        step2 = tensor_with_fund(step1)
        sub = _multi(antifund_tensor_pq(*mu))
        return subtract(step2, sub)
    if lam == (0, 2):
        step1 = _multi(antifund_tensor_pq(*mu))
        step2 = tensor_with_antifund(step1)
        sub = _multi(fund_tensor_pq(*mu))
        return subtract(step2, sub)
    raise NotImplementedError(f"tensor_general with λ={lam}")


def _multi(seq):
    out = {}
    for x in seq:
        out[x] = out.get(x, 0) + 1
    return out


# -------------------------------------------------------------------
# Build Hamiltonian
# -------------------------------------------------------------------

def conjugate(pq):
    return (pq[1], pq[0])


def build_hamiltonian_clean(basis, g_squared, magnetic_coeffs, N_c=3):
    """
    H = (g²/2) Ĉ - (1/(g² N_c)) Σ_{λ in coeffs} c_λ Re χ_λ(U)

    magnetic_coeffs: {λ: c_λ} where λ is one canonical representative of
                     each conjugate pair (or self-conjugate). Re χ_λ
                     equals (χ_λ + χ_{λ*})/2.
    """
    n = len(basis)
    idx = {pq: i for i, pq in enumerate(basis)}
    H = np.zeros((n, n), dtype=float)

    # Electric (Casimir) term
    for i, pq in enumerate(basis):
        H[i, i] += (g_squared / 2.0) * casimir(*pq)

    # Magnetic term
    coef_overall = -(1.0 / (g_squared * N_c))

    for lam, c_lam in magnetic_coeffs.items():
        if c_lam == 0.0:
            continue
        lam_star = conjugate(lam)
        for j, mu in enumerate(basis):
            # 0.5 * (χ_λ + χ_{λ*}) * χ_μ
            for nu, m_nu in tensor_general(lam, mu).items():
                if nu in idx:
                    H[idx[nu], j] += coef_overall * c_lam * 0.5 * m_nu
            if lam_star != lam:
                for nu, m_nu in tensor_general(lam_star, mu).items():
                    if nu in idx:
                        H[idx[nu], j] += coef_overall * c_lam * 0.5 * m_nu
            else:
                # self-conjugate: Re χ_λ = χ_λ; double-count factor of 2 needed
                for nu, m_nu in tensor_general(lam, mu).items():
                    if nu in idx:
                        H[idx[nu], j] += coef_overall * c_lam * 0.5 * m_nu

    H = 0.5 * (H + H.T)
    return H


# -------------------------------------------------------------------
# Continuum-matching constant:
#   Σ over conjugate pairs of c_λ d_λ C_2(λ) (counting both λ and λ*)
# Wilson-form normalized to give 8 (matches old script convention).
# -------------------------------------------------------------------

def continuum_match(magnetic_coeffs):
    total = 0.0
    for lam, c_lam in magnetic_coeffs.items():
        d_lam = dim_irrep(*lam)
        c_lam_pq = casimir(*lam)
        if conjugate(lam) != lam:
            total += c_lam * (d_lam + dim_irrep(*conjugate(lam))) * c_lam_pq
            # Note: d_λ = d_{λ*} for SU(3); just × 2.
        else:
            total += c_lam * d_lam * c_lam_pq
    return total


# -------------------------------------------------------------------
# Sanity: build_hamiltonian_clean with {(1,0): 1.0} should match
# the original Wilson-form (which has Re χ_(1,0) coefficient = 1)
# -------------------------------------------------------------------

def sanity_match_wilson(cutoff=20.0):
    from cl3_ks_single_plaquette_2026_05_07 import build_hamiltonian as build_orig

    basis = build_basis(cutoff)

    H_old = build_orig(basis, 1.0)
    H_new = build_hamiltonian_clean(basis, 1.0, {(1, 0): 1.0})

    diff = np.max(np.abs(H_old - H_new))
    print(f"  Sanity: |H_old - H_new|_max = {diff:.2e}")
    if diff > 1e-10:
        print("  WARNING: convention mismatch — investigating...")
        # Print a few off-diagonals
        for (p, q), i in [(((1, 0)), 1), (((0, 1)), 2), (((1, 1)), 3)]:
            print(f"  row 0 col {i}: old={H_old[0,i]:.6f}, new={H_new[0,i]:.6f}")
    return diff


# -------------------------------------------------------------------
# Action-form spread test
# -------------------------------------------------------------------

def run_action_form_spread(g_squared=1.0, cutoff=20.0):
    basis = build_basis(cutoff)
    print(f"\n=== Cl(3) → KS single-plaquette: action-form spread ===")
    print(f"g² = {g_squared}, cutoff C_2 ≤ {cutoff}, {len(basis)} irreps\n")

    # Wilson normalized to continuum-match = 8 (old convention)
    wilson_coeffs = {(1, 0): 1.0}
    cm_W = continuum_match(wilson_coeffs)
    # Manton-like: split 70% fundamental, 30% adjoint, rescale
    # Continuum match factor for {(1,0): a, (1,1): b}:
    #   a · 2 · 3 · 4/3 + b · 8 · 3 = 8a + 24b
    # Wilson = 8 ⇒ 8a + 24b = 8 ⇒ a + 3b = 1
    # Try b = 0.1: a = 0.7
    manton_coeffs = {(1, 0): 0.7, (1, 1): 0.1}
    cm_M = continuum_match(manton_coeffs)

    # HK-like: Casimir-graded with Block-01 t=1
    a10 = 3 * math.exp(-2/3)
    a11 = 8 * math.exp(-3/2)
    a20 = 6 * math.exp(-5/3)
    raw = {(1, 0): a10, (1, 1): a11, (2, 0): a20}
    raw_match = continuum_match(raw)
    # Note for HK: (2,0) and (0,2) are conjugate pair, included via the
    # magnetic_coeffs single-entry plus the lam_star branch in builder.
    rescale = 8.0 / raw_match
    hk_coeffs = {k: v * rescale for k, v in raw.items()}
    cm_HK = continuum_match(hk_coeffs)

    cases = [
        ("Wilson (pure fundamental)", wilson_coeffs, cm_W),
        ("Manton-like (10% adjoint admix)", manton_coeffs, cm_M),
        ("HK-like (Casimir-graded, rescaled)", hk_coeffs, cm_HK),
    ]

    print(f"{'Action choice':<40}  {'cont match':>11}  {'<P>_GS':>10}  "
          f"{'E_0':>14}")
    print("-" * 84)
    results = []
    for label, coeffs, cm in cases:
        H = build_hamiltonian_clean(basis, g_squared, coeffs)
        evals, evecs = eigh(H)
        psi0 = evecs[:, 0]
        P_gs = expectation_re_tr_U_over_Nc(psi0, basis)
        results.append((label, cm, P_gs, evals[0]))
        print(f"{label:<40}  {cm:>11.6f}  {P_gs:>10.6f}  {evals[0]:>14.6f}")

    P_values = [r[2] for r in results]
    spread = max(P_values) - min(P_values)
    pct = 100 * spread / np.mean(P_values) if np.mean(P_values) != 0 else 0
    print(f"\nSpread across magnetic-operator choices: "
          f"absolute {spread:.6f}, relative {pct:.1f}%")

    return results


if __name__ == "__main__":
    print("=== Sanity: clean builder vs original ===")
    sanity_match_wilson()

    print("\n--- canonical g² = 1 ---")
    run_action_form_spread(g_squared=1.0)

    print("\n--- weaker coupling g² = 0.5 ---")
    run_action_form_spread(g_squared=0.5)

    print("\n--- stronger coupling g² = 2.0 ---")
    run_action_form_spread(g_squared=2.0)
