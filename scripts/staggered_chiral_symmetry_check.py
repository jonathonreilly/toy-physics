"""Staggered Cl(3) Hamiltonian has chiral-symmetric spectrum: σ(H_phys) = -σ(H_phys).

By cpt_exact_note (retained), the staggered single-component lattice operator
D = Σ_μ (1/2) η_μ(x) [δ(y, x+e_μ) - δ(y, x-e_μ)] is anti-Hermitian, the
physical Hermitian Hamiltonian is H_phys = i·D, and the C operator
(sublattice parity ε(x) = (-1)^{x+y+z} as a diagonal real matrix) satisfies
exactly C·H_phys·C = -H_phys, i.e. {C, H_phys} = 0.

This block proves the spectral consequence: the spectrum of H_phys is
**symmetric around 0**:

    σ(H_phys) = -σ(H_phys)    (as multisets)

For every eigenstate |E⟩ of H_phys with eigenvalue E, the state C|E⟩ is
also an eigenstate of H_phys with eigenvalue -E. Therefore:
- positive and negative eigenvalues come in equal-multiplicity pairs (E, -E)
- the chiral-symmetry-protected zero modes can only enter as a single
  invariant subspace under C
- σ(H_phys) on a bipartite lattice is a balanced "Dirac" spectrum

This is a structural framework consequence of the retained CPT_EXACT_NOTE
that doesn't appear in the cited note's own claim list (which states
[CPT, H] = 0 and SME=0, but doesn't carry the spectrum-symmetric statement
explicitly).

Tests:
  (T1) Reconstruct staggered D and C from the cited construction
  (T2) Verify {C, H_phys} = 0 (input from cpt_exact_note)
  (T3) Compute σ(H_phys); show it's symmetric around 0
  (T4) For each eigenvalue E ≠ 0, verify -E has the same multiplicity
  (T5) Pair every eigenstate |E⟩ with C|E⟩ and verify H_phys (C|E⟩) = -E (C|E⟩)
  (T6) Spectrum sum = 0 (immediate from symmetric paired structure)
  (T7) On a 4×4×4 even periodic lattice, full structural check
"""
from __future__ import annotations

from collections import Counter

import numpy as np


def staggered_eta(mu: int, site: tuple[int, int, int]) -> float:
    """KS staggered phase: η_μ(x) = (-1)^{Σ_{ν<μ} x_ν}. Same as cpt_exact_note."""
    s = sum(site[nu] for nu in range(mu))
    return (-1.0) ** s


def build_full_D(L: int) -> np.ndarray:
    """Anti-Hermitian staggered hopping operator D, exactly as in cpt_exact_note."""
    if L % 2 != 0:
        raise ValueError("Even L required (CPT requires bipartite lattice).")
    N = L ** 3

    def site_to_idx(x: int, y: int, z: int) -> int:
        return ((x % L) * L + (y % L)) * L + (z % L)

    def idx_to_site(idx: int) -> tuple[int, int, int]:
        z = idx % L
        y = (idx // L) % L
        x = idx // (L * L)
        return (x, y, z)

    D = np.zeros((N, N), dtype=complex)
    for idx in range(N):
        site = idx_to_site(idx)
        for mu in range(3):
            eta = staggered_eta(mu, site)
            fwd = list(site)
            fwd[mu] = (fwd[mu] + 1) % L
            j_fwd = site_to_idx(*fwd)
            bwd = list(site)
            bwd[mu] = (bwd[mu] - 1) % L
            j_bwd = site_to_idx(*bwd)
            D[idx, j_fwd] += 0.5 * eta
            D[idx, j_bwd] -= 0.5 * eta
    return D


def build_C(L: int) -> np.ndarray:
    """Sublattice parity ε(x) = (-1)^{x+y+z}. Same as cpt_exact_note."""
    N = L ** 3

    def idx_to_site(idx: int) -> tuple[int, int, int]:
        z = idx % L
        y = (idx // L) % L
        x = idx // (L * L)
        return (x, y, z)

    C = np.zeros((N, N), dtype=float)
    for idx in range(N):
        x, y, z = idx_to_site(idx)
        eps = (-1.0) ** (x + y + z)
        C[idx, idx] = eps
    return C


def main() -> None:
    print("=" * 72)
    print("STAGGERED Cl(3) H_phys SPECTRUM IS CHIRAL-SYMMETRIC: σ(H) = -σ(H)")
    print("=" * 72)
    print()

    L = 4  # Even L required
    N = L ** 3
    print(f"  Lattice: L = {L} (periodic, bipartite). N = L^3 = {N}.")
    print()

    # ----- Test 1: Reconstruct staggered D and C from cpt_exact_note construction -----
    print("-" * 72)
    print("TEST 1: Build anti-Hermitian D (staggered hopping) and diagonal C = diag(ε(x))")
    print("-" * 72)
    D = build_full_D(L)
    C = build_C(L)
    H_phys = 1j * D  # Hermitian
    # Check D anti-Hermitian
    d_anti = np.linalg.norm(D + D.conj().T)
    # Check H_phys Hermitian
    h_herm = np.linalg.norm(H_phys - H_phys.conj().T)
    print(f"  ||D + D†|| (anti-Hermitian check on D) = {d_anti:.3e}")
    print(f"  ||H_phys - H_phys†|| (Hermitian check on H = iD) = {h_herm:.3e}")
    t1_ok = d_anti < 1e-12 and h_herm < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: {C, H_phys} = 0 (input from cpt_exact_note) -----
    print("-" * 72)
    print("TEST 2: {C, H_phys} = 0 (chiral anti-commutation, from cpt_exact_note)")
    print("-" * 72)
    anticomm = C @ H_phys + H_phys @ C
    aci = np.linalg.norm(anticomm)
    print(f"  ||{{C, H_phys}}|| = {aci:.3e}")
    t2_ok = aci < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: Spectrum is symmetric around 0 -----
    print("-" * 72)
    print("TEST 3: σ(H_phys) is symmetric around 0  (σ = -σ as multisets)")
    print("-" * 72)
    eigvals = np.linalg.eigvalsh(H_phys)
    eigvals_rounded = np.round(eigvals, 8)
    mult_pos = Counter(eigvals_rounded[eigvals_rounded > 1e-8].tolist())
    mult_neg = Counter((-eigvals_rounded[eigvals_rounded < -1e-8]).tolist())
    n_zero = int(np.sum(np.abs(eigvals_rounded) < 1e-8))
    print(f"  positive eigenvalues (with multiplicity): {len(eigvals[eigvals > 1e-8])}")
    print(f"  negative eigenvalues (with multiplicity): {len(eigvals[eigvals < -1e-8])}")
    print(f"  zero eigenvalues:                          {n_zero}")
    print(f"  multisets {{+E}} = {{|−E|}} (after sign flip):")
    sym_match = (mult_pos == mult_neg)
    print(f"    {sym_match}")
    t3_ok = sym_match
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: For each eigenvalue E ≠ 0, multiplicity at -E is the same -----
    print("-" * 72)
    print("TEST 4: ∀ E ≠ 0: mult(E) = mult(-E)")
    print("-" * 72)
    eig_counter = Counter(eigvals_rounded.tolist())
    mismatches = []
    for E, m in eig_counter.items():
        if abs(E) < 1e-8:
            continue
        m_neg = eig_counter.get(round(-E, 8), 0)
        if m != m_neg:
            mismatches.append((E, m, m_neg))
    if mismatches:
        print(f"  Mismatched pairs: {mismatches[:5]} ...")
    else:
        print(f"  All non-zero eigenvalues have matching ±E multiplicities.")
    t4_ok = not mismatches
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: For each eigenstate |E⟩, C|E⟩ is eigenstate with eigenvalue -E -----
    print("-" * 72)
    print("TEST 5: H_phys (C |E⟩) = -E · (C |E⟩) for every eigenstate |E⟩ with E ≠ 0")
    print("-" * 72)
    eigvals_full, eigvecs = np.linalg.eigh(H_phys)
    max_pair_err = 0.0
    nonzero_count = 0
    for k in range(len(eigvals_full)):
        E = eigvals_full[k]
        if abs(E) < 1e-8:
            continue
        nonzero_count += 1
        v = eigvecs[:, k]
        Cv = C @ v
        # Check H_phys · Cv = -E · Cv
        residual = H_phys @ Cv - (-E) * Cv
        err = np.linalg.norm(residual)
        max_pair_err = max(max_pair_err, err)
    print(f"  Checked {nonzero_count} non-zero eigenstates.")
    print(f"  max ||H_phys (C|E⟩) - (-E)(C|E⟩)|| = {max_pair_err:.3e}")
    t5_ok = max_pair_err < 1e-10
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: Sum of spectrum = 0 (immediate from symmetry) -----
    print("-" * 72)
    print("TEST 6: Tr(H_phys) = Σ E = 0  (sum of eigenvalues vanishes by symmetry)")
    print("-" * 72)
    trace_H = np.trace(H_phys).real
    spec_sum = sum(eigvals).real
    print(f"  Tr(H_phys) = {trace_H:.3e}")
    print(f"  Σ eigenvalues = {spec_sum:.3e}")
    t6_ok = abs(spec_sum) < 1e-10
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    # ----- Test 7: Equal sublattice partition |Λ_+| = |Λ_-| = N/2 -----
    print("-" * 72)
    print(f"TEST 7: Sublattice balance |{{x : ε(x) = +1}}| = |{{x : ε(x) = -1}}| = N/2 = {N // 2}")
    print("        (necessary for C to define a balanced grading)")
    print("-" * 72)
    n_plus = int(np.sum(np.diag(C) > 0))
    n_minus = int(np.sum(np.diag(C) < 0))
    print(f"  |Λ_+| = {n_plus},  |Λ_-| = {n_minus}")
    t7_ok = n_plus == N // 2 and n_minus == N // 2
    print(f"  STATUS: {'PASS' if t7_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (D anti-Hermitian, H = iD Hermitian):     {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 ({{C, H_phys}} = 0 from CPT_EXACT_NOTE):    {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (σ(H_phys) symmetric around 0):            {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (mult(+E) = mult(-E) for E ≠ 0):           {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (C|E⟩ has eigenvalue -E for every |E⟩):    {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (Σ eigenvalues = 0):                       {'PASS' if t6_ok else 'FAIL'}")
    print(f"  Test 7 (sublattice balance |Λ_+| = |Λ_-| = N/2):  {'PASS' if t7_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok, t7_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
