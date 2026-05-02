"""No per-site γ_5 chirality operator on Cl(3) Pauli rep.

For each site x ∈ Z^3, by axiom_first_cl3_per_site_uniqueness ρ : Cl(3) → M_2(C)
with γ_i ↦ σ_i. The Cl(3) volume element

    ω := γ_1 γ_2 γ_3

acts in Pauli rep as σ_1 σ_2 σ_3 = i I_2. Therefore:

    (1) ω is *central* in Cl(3) (commutes with all γ_i)
    (2) ω = i·I_2 is a scalar (proportional to identity)
    (3) NO element of Cl(3) anticommutes with all three generators γ_i
    (4) Therefore there is NO chirality operator γ_5 satisfying
        γ_5² = +I_2 and {γ_5, γ_i} = 0 for all i, on per-site Hilbert.

This is the per-site instance of the standard "no chirality in odd D"
fact (Lawson-Michelsohn): for Cl(p,q) with n = p+q odd, the volume element
is central, hence chirality requires extending the algebra (e.g. by
introducing a temporal direction, n+1 even).
"""
from __future__ import annotations

import itertools

import numpy as np


def main() -> None:
    print("=" * 72)
    print("NO PER-SITE γ_5 CHIRALITY ON Cl(3) PAULI REP")
    print("=" * 72)
    print()

    s1 = np.array([[0, 1], [1, 0]], dtype=complex)
    s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = np.array([[1, 0], [0, -1]], dtype=complex)
    I2 = np.eye(2, dtype=complex)
    sigmas = [s1, s2, s3]

    # Volume element ω = γ_1 γ_2 γ_3 = σ_1 σ_2 σ_3
    omega = s1 @ s2 @ s3
    print(f"  ω = σ_1 σ_2 σ_3 =")
    print(f"  {omega.tolist()}")
    print()

    # ----- Test 1: ω = i·I_2 -----
    print("-" * 72)
    print("TEST 1: ω = i·I_2 (scalar in Pauli rep)")
    print("-" * 72)
    target = 1j * I2
    dev = np.linalg.norm(omega - target)
    print(f"  ||ω - i·I_2|| = {dev:.3e}")
    t1_ok = dev < 1e-12
    print(f"  STATUS: {'PASS' if t1_ok else 'FAIL'}")
    print()

    # ----- Test 2: ω commutes with every σ_i (centrality) -----
    print("-" * 72)
    print("TEST 2: [ω, σ_i] = 0 for all i (ω is central in Cl(3))")
    print("-" * 72)
    max_comm = 0.0
    for i in range(3):
        comm = omega @ sigmas[i] - sigmas[i] @ omega
        d = np.linalg.norm(comm)
        max_comm = max(max_comm, d)
        print(f"  ||[ω, σ_{i+1}]|| = {d:.3e}")
    t2_ok = max_comm < 1e-12
    print(f"  STATUS: {'PASS' if t2_ok else 'FAIL'}")
    print()

    # ----- Test 3: ω² = -I_2 (since (i·I)² = -I) -----
    print("-" * 72)
    print("TEST 3: ω² = -I_2 (consistent with central scalar i·I)")
    print("-" * 72)
    omega_sq = omega @ omega
    target_sq = -I2
    dev_sq = np.linalg.norm(omega_sq - target_sq)
    print(f"  ||ω² - (-I_2)|| = {dev_sq:.3e}")
    t3_ok = dev_sq < 1e-12
    print(f"  STATUS: {'PASS' if t3_ok else 'FAIL'}")
    print()

    # ----- Test 4: NO 2x2 matrix anticommutes with all three σ_i -----
    print("-" * 72)
    print("TEST 4: No nonzero M ∈ M_2(C) anticommutes with all three σ_i")
    print("        (sweep through Pauli basis: only zero satisfies all three)")
    print("-" * 72)
    # Any M ∈ M_2(C) = a·I + b·σ_1 + c·σ_2 + d·σ_3 (Pauli basis spans M_2(C))
    # {M, σ_i} = 0 forces M to anticommute with σ_i.
    # Since {σ_i, σ_j} = 2 δ_ij I, only the scalar coefficient a contributes
    # to {M, σ_i} = 2a σ_i + (b·{σ_1,σ_i} + ...) = 2a σ_i + 2 b_i I.
    # For this to vanish for all i, need a = 0 and b = c = d = 0, i.e. M = 0.
    # Numerical sweep: try M = a I + b σ_1 + c σ_2 + d σ_3 over a basis,
    # check that requiring {M, σ_i} = 0 for all i forces M = 0.
    pauli_basis = [I2, s1, s2, s3]
    # Build the linear system: for each generator σ_i, {M, σ_i} = 0 is a
    # linear constraint on the Pauli coefficients (a, b, c, d).
    # Stack constraints: 3 generators × 4 matrix entries (real+imag) = 24 eqns
    # in 8 real unknowns (4 complex coefs).
    # Easier: compute {basis_k, σ_i} symbolically.
    constraints = []
    for i in range(3):
        for k in range(4):
            anti = pauli_basis[k] @ sigmas[i] + sigmas[i] @ pauli_basis[k]
            constraints.append(anti.flatten())
    # Stack into a 12x4 matrix where row (i, k) gives {basis_k, σ_i} as a vector
    # We want to find c = (a, b, c, d) such that Σ_k c_k · {basis_k, σ_i} = 0
    # for all i. So the constraint matrix has rows = anti_(i,k)_flat·c_k
    # Build full constraint matrix: (3·4) rows × 4 columns
    # M_ki = {basis_k, σ_i} as 2x2 matrix flattened to 4-vector
    # Constraint: Σ_k c_k · M_ki = 0 for each i ⇒ 3·4 = 12 equations.
    A = np.zeros((12, 4), dtype=complex)
    for i in range(3):
        for k in range(4):
            anti_ki = pauli_basis[k] @ sigmas[i] + sigmas[i] @ pauli_basis[k]
            A[i * 4:(i + 1) * 4, k] = anti_ki.flatten()
    # Find null space of A
    u, s, vh = np.linalg.svd(A)
    nullity = sum(1 for sv in s if sv < 1e-10)
    print(f"  rank of constraint matrix = {4 - nullity} (out of 4 unknowns)")
    print(f"  null space dim = {nullity} (only zero solution if dim = 0)")
    t4_ok = nullity == 0
    print(f"  STATUS: {'PASS' if t4_ok else 'FAIL'}")
    print()

    # ----- Test 5: No M satisfying both M² = +I_2 and {M, σ_i} = 0 -----
    print("-" * 72)
    print("TEST 5: No γ_5 candidate exists — no M satisfies (γ_5² = +I_2)")
    print("        AND {γ_5, σ_i} = 0 for all i, on Pauli per-site Hilbert.")
    print("-" * 72)
    # By Test 4, the only M satisfying {M, σ_i} = 0 for all i is M = 0.
    # M = 0 doesn't satisfy M² = +I_2. Hence no γ_5 candidate exists.
    print("  Test 4 proved: only zero anticommutes with all three σ_i.")
    print("  Zero matrix doesn't satisfy γ_5² = +I_2 (since 0² = 0 ≠ I).")
    print("  Therefore no γ_5 exists on per-site Cl(3) Hilbert.")
    t5_ok = t4_ok  # follows directly from Test 4
    print(f"  STATUS: {'PASS' if t5_ok else 'FAIL'}")
    print()

    # ----- Test 6: dim of even subalgebra = dim of odd subalgebra = 2 -----
    print("-" * 72)
    print("TEST 6: Cl(3) has 4-dim even subalgebra (span{I, σ_1σ_2, σ_2σ_3, σ_3σ_1})")
    print("        and 4-dim odd subalgebra (span{σ_1, σ_2, σ_3, σ_1σ_2σ_3 = iI})")
    print("        BUT in Pauli rep both subalgebras already span M_2(C) = 4-dim,")
    print("        so even and odd subalgebras COINCIDE on Pauli (no Z_2 grading)")
    print("-" * 72)
    # In Pauli rep:
    # Even subalgebra basis: I, σ_1σ_2 = iσ_3, σ_2σ_3 = iσ_1, σ_3σ_1 = iσ_2
    #                       → {I, iσ_1, iσ_2, iσ_3} ↔ {I, σ_1, σ_2, σ_3} as C-span
    # Odd subalgebra basis: σ_1, σ_2, σ_3, σ_1σ_2σ_3 = iI
    #                       → {σ_1, σ_2, σ_3, iI} ↔ {I, σ_1, σ_2, σ_3} as C-span
    # Both span all of M_2(C); the Z_2 grading is invisible at the C-algebra level.
    # This means there's no internal "chirality projector" P_± = (1 ± γ_5)/2.
    even_basis = [I2, 1j * s3, 1j * s1, 1j * s2]  # σ_1σ_2 = iσ_3 etc.
    odd_basis = [s1, s2, s3, 1j * I2]
    even_matrix = np.column_stack([m.flatten() for m in even_basis])
    odd_matrix = np.column_stack([m.flatten() for m in odd_basis])
    rank_even = np.linalg.matrix_rank(even_matrix, tol=1e-10)
    rank_odd = np.linalg.matrix_rank(odd_matrix, tol=1e-10)
    print(f"  rank of even subalgebra in M_2(C) = {rank_even} (full = 4)")
    print(f"  rank of odd subalgebra in M_2(C)  = {rank_odd} (full = 4)")
    t6_ok = rank_even == 4 and rank_odd == 4
    print(f"  STATUS: {'PASS' if t6_ok else 'FAIL'}")
    print()

    print("=" * 72)
    print(f"  Test 1 (ω = i·I_2):                                {'PASS' if t1_ok else 'FAIL'}")
    print(f"  Test 2 ([ω, σ_i] = 0 — ω is central):              {'PASS' if t2_ok else 'FAIL'}")
    print(f"  Test 3 (ω² = -I_2):                                {'PASS' if t3_ok else 'FAIL'}")
    print(f"  Test 4 (no M anticommutes with all σ_i):           {'PASS' if t4_ok else 'FAIL'}")
    print(f"  Test 5 (no γ_5 candidate exists):                  {'PASS' if t5_ok else 'FAIL'}")
    print(f"  Test 6 (even/odd subalgebras coincide on Pauli):   {'PASS' if t6_ok else 'FAIL'}")
    all_ok = all([t1_ok, t2_ok, t3_ok, t4_ok, t5_ok, t6_ok])
    print(f"  OVERALL: {'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
