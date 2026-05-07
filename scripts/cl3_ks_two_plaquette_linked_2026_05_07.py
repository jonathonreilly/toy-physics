"""
Cl(3) → KS two-plaquette computation with LINKED INVARIANT basis extension.

The product basis χ_λ(U) χ_μ(V) cannot capture U-V correlations needed for
plaquettes that involve both links. In the dumbbell, p1 = U_BE U_AD^{-1}
gave ⟨P_1⟩ ≈ 0 in product basis (insufficient correlation expressivity).

This script extends the basis with linked gauge invariants:
    Re Tr(U V^{-1})      — basic linked invariant (= -magnetic operator)
    Re Tr(U V)           — alternative linked invariant
    |Tr(U V^{-1})|²      — degree-2 linked invariant
    χ_λ(U V^{-1})        — character of product (single-irrep)
    χ_λ(U V)             — alternative character of product

Then re-runs ground state with extended basis to see if ⟨P_1⟩ becomes
non-trivial and how the average ⟨P⟩ shifts.
"""

from __future__ import annotations

import numpy as np
from numpy.linalg import eigh

from cl3_ks_single_plaquette_2026_05_07 import casimir, dim_irrep
from cl3_ks_two_plaquette_2026_05_07 import (
    sample_su3,
    chi_pq,
    build_two_link_basis,
    diagonalize_with_gram,
)


def build_extended_basis_F(U_AD, U_BE, casimir_cutoff: float = 4.0):
    """
    Build extended basis function values at samples.

    Returns: F (n_basis × N_samples) and labels (list of strings).
    """
    irreps, pairs = build_two_link_basis(casimir_cutoff)
    N = U_AD.shape[0]

    # Pre-compute single-link characters
    chi_AD = {lam: chi_pq(U_AD, *lam) for lam in irreps}
    chi_BE = {lam: chi_pq(U_BE, *lam) for lam in irreps}

    # Pre-compute linked variables: U V^{-1} and U V
    UAD_inv = np.conj(U_AD.transpose(0, 2, 1))
    UBE_UAD_inv = np.einsum('nij,njk->nik', U_BE, UAD_inv)
    UBE_UAD = np.einsum('nij,njk->nik', U_BE, U_AD)
    UAD_UBE = np.einsum('nij,njk->nik', U_AD, U_BE)

    # Pre-compute linked characters
    chi_link_inv = {lam: chi_pq(UBE_UAD_inv, *lam) for lam in irreps}
    chi_link_dir = {lam: chi_pq(UBE_UAD, *lam) for lam in irreps}
    chi_link_dir_alt = {lam: chi_pq(UAD_UBE, *lam) for lam in irreps}

    F_list = []
    labels = []

    # Single-link products (full set)
    for a in irreps:
        for b in irreps:
            F_list.append(chi_AD[a] * chi_BE[b])
            labels.append(f"χ_{a}(AD)·χ_{b}(BE)")

    # Linked invariants: characters of UV^{-1}, UV (low irreps only)
    for lam in [(1, 0), (0, 1), (1, 1)]:
        if lam in chi_link_inv:
            F_list.append(chi_link_inv[lam])
            labels.append(f"χ_{lam}(U_BE U_AD^-1)")
            F_list.append(chi_link_dir[lam])
            labels.append(f"χ_{lam}(U_BE U_AD)")

    F = np.array(F_list)  # shape (n_basis, N_samples)
    return F, labels, U_AD, U_BE


def expectation_at_samples(psi, F, op_values):
    """⟨ψ | op | ψ⟩ where op is given by sample values."""
    psi_at = np.conj(psi) @ F
    norm = np.mean(np.abs(psi_at)**2)
    return np.mean(np.abs(psi_at)**2 * op_values) / norm


def run_extended(g_squared: float = 1.0, N_samples: int = 50000,
                 casimir_cutoff: float = 4.0, seed: int = 7, N_c: int = 3):
    print(f"\n=== Extended-basis 2-plaquette dumbbell, g²={g_squared} ===")

    U_AD = sample_su3(N_samples, seed=seed)
    U_BE = sample_su3(N_samples, seed=seed + 1)

    F, labels, U1, U2 = build_extended_basis_F(U_AD, U_BE, casimir_cutoff)
    n = F.shape[0]
    print(f"  Extended basis size: {n}")

    # Plaquette values at samples
    UAD_inv = np.conj(U_AD.transpose(0, 2, 1))
    re_tr_p1 = np.trace(np.einsum('nij,njk->nik', U_BE, UAD_inv),
                         axis1=1, axis2=2).real
    re_tr_p2 = np.trace(U_BE, axis1=1, axis2=2).real
    M_values = -(1.0 / (g_squared * N_c)) * (re_tr_p1 + re_tr_p2)

    # Build Gram and Magnetic
    print(f"  Building Gram matrix and magnetic matrix...")
    Gram = (np.conj(F) @ F.T) / N_samples
    Hmag = (np.conj(F) * M_values[np.newaxis, :]) @ F.T / N_samples

    # Build Casimir matrix in extended basis (numerical via Casimir as
    # (g²/2)(Ĉ_AD + Ĉ_BE))
    # Casimir on a single-variable function χ_λ(U) is C_2(λ) χ_λ(U).
    # On linked invariants χ_λ(UV^{±1}), Casimir on U at fixed V is more
    # complicated, but for the WHOLE-SYSTEM Casimir Ĉ_AD + Ĉ_BE on
    # χ_λ(UV^{-1}), this is also non-trivial.
    #
    # Approach: build Casimir matrix in irrep basis (single-link products
    # are eigenstates with C_2(λ) + C_2(μ)); leave linked-invariant
    # entries to be filled by numerical Monte Carlo via the relation
    # ⟨f | Ĉ | g⟩ = (g²/2) [⟨f | Ĉ_AD | g⟩ + ⟨f | Ĉ_BE | g⟩].
    #
    # This is hard analytically, so use a SIMPLER PROXY: assume linked
    # invariants χ_λ(UV^{±1}) act approximately like single-irrep
    # eigenstates with eigenvalue C_2(λ). This is true if we treat
    # the "combined" link as carrying irrep λ, which is a spin-network
    # interpretation.
    #
    # Correct treatment via spin network: the link (UV^{-1}) carries
    # irrep λ; in the spin-network basis, Ĉ_AD + Ĉ_BE acts on this state
    # giving 2 C_2(λ) (since both U and V each carry the irrep traversed
    # by the loop UV^{-1}).
    #
    # This is the relevant approximation for the linked invariants.
    print(f"  Building Casimir matrix (analytical for products,"
          f" spin-network estimate for linked)...")
    irreps, pairs = build_two_link_basis(casimir_cutoff)
    Hcas = np.zeros((n, n), dtype=complex)
    n_products = len(pairs)
    # Single-link products: diagonal
    for k, (a, b) in enumerate(pairs):
        Hcas[k, k] = (g_squared / 2.0) * (casimir(*a) + casimir(*b))
    # Linked invariants: spin-network estimate 2 C_2(λ) (one C_2 per link
    # the loop traverses)
    for k_extra in range(n_products, n):
        label = labels[k_extra]
        # Extract irrep from label: "χ_(p,q)(...)"
        import re
        m = re.search(r"\((\d+), (\d+)\)", label)
        if m:
            p, q = int(m.group(1)), int(m.group(2))
            Hcas[k_extra, k_extra] = (g_squared / 2.0) * (2 * casimir(p, q))

    H = Hcas + Hmag
    H = 0.5 * (H + np.conj(H.T))
    Gram = 0.5 * (Gram + np.conj(Gram.T))

    evals, evecs, nkeep = diagonalize_with_gram(H, Gram)
    psi0 = evecs[:, 0]

    # Compute observables
    p1_avg = expectation_at_samples(psi0, F, re_tr_p1 / N_c)
    p2_avg = expectation_at_samples(psi0, F, re_tr_p2 / N_c)
    P_avg = (p1_avg + p2_avg) / 2.0

    print(f"  E_0 = {evals[0].real:.6f}")
    print(f"  ⟨P_1⟩ = {p1_avg:.6f}")
    print(f"  ⟨P_2⟩ = {p2_avg:.6f}")
    print(f"  ⟨P⟩_avg = {P_avg:.6f}")
    print(f"  (kept {nkeep}/{n} basis modes)")

    # Show top components of ground state
    print(f"  Top 5 GS components:")
    abs_psi = np.abs(psi0)
    top = np.argsort(-abs_psi)[:5]
    for idx in top:
        if idx < len(labels):
            print(f"    {labels[idx]:<40} amplitude {psi0[idx].real:>+.4f}")

    return {
        'g2': g_squared,
        'E_0': evals[0].real,
        'P1': p1_avg,
        'P2': p2_avg,
        'P_avg': P_avg,
        'nbasis': n,
        'nkept': nkeep,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Extended basis: product characters + linked invariants")
    print("=" * 70)

    results = []
    for g2 in [0.50, 0.75, 1.00, 1.50, 2.00]:
        r = run_extended(g_squared=g2)
        results.append(r)

    print()
    print("=" * 70)
    print("Summary table:")
    print("=" * 70)
    print(f"{'g²':>6}  {'E_0':>10}  {'⟨P_1⟩':>10}  {'⟨P_2⟩':>10}  {'⟨P⟩_avg':>10}")
    for r in results:
        print(f"{r['g2']:>6.2f}  {r['E_0']:>10.6f}  {r['P1']:>10.6f}  "
              f"{r['P2']:>10.6f}  {r['P_avg']:>10.6f}")

    print()
    print("Comparison:")
    print("  Single-plaq toy (g²=1):     ⟨P⟩ = 0.218 (this is per-plaquette)")
    print("  Product-basis dumbbell:     ⟨P⟩ ≈ 0.120 (P_1 ≈ 0, basis-limited)")
    print("  Extended-basis dumbbell:    ⟨P⟩ = see table (g²=1)")
