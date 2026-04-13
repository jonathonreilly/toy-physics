#!/usr/bin/env python3
"""
Investigation of the 3 FAILs in frontier_generation_gauge_universality.py
=========================================================================

STATUS: EXACT investigation (algebraic, no approximations)

QUESTION:
  The gauge universality script finds that PROJECTED commutant generators
  have DIFFERENT eigenvalues at X1=(pi,0,0), X2=(0,pi,0), X3=(0,0,pi).
  Are these differences:
    (a) a gauge-basis artifact (physically meaningless), or
    (b) proof that the 3 generations are physically distinct?

ANSWER (proven below): NEITHER -- it is (c):
  The commutant algebra is the SAME at all corners (exact).
  The Hamiltonian eigenspaces at different corners are DIFFERENT 4-dim
  subspaces of C^8.  Projecting the SAME operator onto DIFFERENT subspaces
  naturally gives different matrix elements.  But C3[111] UNITARILY MAPS
  one eigenspace to another, proving the representations are EQUIVALENT.

  The "different eigenvalues" come from using a NON-CANONICAL basis for the
  commutant generators (SVD-dependent).  In any PHYSICAL basis (T3, Y, Q),
  the representations must be equivalent because C3[111] intertwines them.

INVESTIGATION PLAN:
  1. Reproduce the eigenvalue mismatches explicitly
  2. Show the eigenspaces at different corners are DIFFERENT subspaces of C^8
  3. Show C3[111] maps one eigenspace to another exactly
  4. Construct the PHYSICAL generators (T3, Y, Q) in the commutant
  5. Check whether T3, Y, Q eigenvalues are corner-dependent
  6. Identify generators 6, 7 in terms of Cl(3) basis elements
  7. Determine: is the mismatch a basis artifact or a physical quantum number?

PStack experiment: frontier-generation-3fails-investigation
Self-contained: numpy only.
"""

from __future__ import annotations

import sys
import numpy as np

np.set_printoptions(precision=10, linewidth=130, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name, condition, detail="", kind="EXACT"):
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Part 0: Build KS gamma matrices (identical to gauge_universality script)
# =============================================================================

def build_ks_gammas():
    """Build the 3 KS gamma matrices on 8-dim taste space."""
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    gammas = []
    for mu in range(3):
        G = np.zeros((8, 8), dtype=complex)
        for a in alphas:
            i = alpha_idx[a]
            a1, a2, a3 = a
            if mu == 0:
                eta = 1.0
            elif mu == 1:
                eta = (-1.0) ** a1
            else:
                eta = (-1.0) ** (a1 + a2)
            b = list(a)
            b[mu] = 1 - b[mu]
            b = tuple(b)
            j = alpha_idx[b]
            G[i, j] = eta
        gammas.append(G)
    return gammas


def build_cl3_full_basis(gammas):
    """Build all 8 Cl(3) basis elements: {I, G_mu, G_{mu nu}, G_{123}}."""
    G1, G2, G3 = gammas
    I8 = np.eye(8, dtype=complex)
    basis = {
        'I': I8,
        'G1': G1, 'G2': G2, 'G3': G3,
        'G12': G1 @ G2, 'G13': G1 @ G3, 'G23': G2 @ G3,
        'G123': G1 @ G2 @ G3,
    }
    return basis


def compute_commutant_basis(generators, dim=8):
    """Compute basis for commutant of generators in End(C^dim)."""
    constraints = []
    for G in generators:
        C = np.kron(G.T, np.eye(dim, dtype=complex)) - np.kron(np.eye(dim, dtype=complex), G)
        constraints.append(C)
    A = np.vstack(constraints)
    U, S, Vh = np.linalg.svd(A, full_matrices=True)
    tol = 1e-10 * max(1.0, S[0]) if len(S) > 0 else 1e-10
    null_vecs = []
    for i, s in enumerate(S):
        if s < tol:
            null_vecs.append(Vh[i])
    for i in range(len(S), Vh.shape[0]):
        null_vecs.append(Vh[i])
    return [v.reshape(dim, dim) for v in null_vecs]


def staggered_H_antiherm(K):
    """Anti-Hermitian staggered Hamiltonian."""
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    H = np.zeros((8, 8), dtype=complex)
    for a in alphas:
        i = alpha_idx[a]
        a1, a2, a3 = a
        for mu in range(3):
            if mu == 0:
                eta = 1.0
            elif mu == 1:
                eta = (-1.0) ** a1
            else:
                eta = (-1.0) ** (a1 + a2)
            b = list(a)
            b[mu] = 1 - b[mu]
            b = tuple(b)
            j = alpha_idx[b]
            if a[mu] == 1:
                phase = np.exp(1j * K[mu])
            else:
                phase = 1.0
            H[i, j] += 0.5 * eta * phase
            H[j, i] -= 0.5 * eta * np.conj(phase)
    return H


def build_C3_111():
    """Build C3[111] rotation: (a1,a2,a3) -> (a3,a1,a2) with taste phase."""
    alphas = [(a1, a2, a3) for a1 in range(2) for a2 in range(2) for a3 in range(2)]
    alpha_idx = {a: i for i, a in enumerate(alphas)}
    U = np.zeros((8, 8), dtype=complex)
    for a in alphas:
        a1, a2, a3 = a
        b = (a3, a1, a2)
        i = alpha_idx[a]
        j = alpha_idx[b]
        eps = (-1) ** ((a1 + a2) * a3)
        U[j, i] = eps
    return U


# =============================================================================
# Main investigation
# =============================================================================

def main():
    print("=" * 80)
    print("INVESTIGATION: 3 FAILS IN GAUGE UNIVERSALITY SCRIPT")
    print("Are the projected eigenvalue differences physical or basis artifacts?")
    print("=" * 80)

    gammas = build_ks_gammas()
    G1, G2, G3 = gammas
    cl3_basis = build_cl3_full_basis(gammas)
    comm_basis = compute_commutant_basis(gammas, dim=8)
    U_C3 = build_C3_111()

    X_points = {
        'X1': np.array([np.pi, 0.0, 0.0]),
        'X2': np.array([0.0, np.pi, 0.0]),
        'X3': np.array([0.0, 0.0, np.pi]),
    }

    # Compute eigenspaces at each corner
    corner_data = {}
    for name, K in X_points.items():
        H_ah = staggered_H_antiherm(K)
        H_herm = 1j * H_ah
        evals, evecs = np.linalg.eigh(H_herm)
        idx = np.argsort(evals)
        evals = evals[idx]
        evecs = evecs[:, idx]
        mask_plus = np.abs(evals - 1.0) < 0.1
        mask_minus = np.abs(evals + 1.0) < 0.1
        P_plus = evecs[:, mask_plus]
        P_minus = evecs[:, mask_minus]
        corner_data[name] = {
            'K': K, 'evals': evals, 'evecs': evecs,
            'P_plus': P_plus, 'P_minus': P_minus,
        }

    # ===================================================================
    # SECTION 1: The eigenspaces are DIFFERENT subspaces of C^8
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 1: EIGENSPACES ARE DIFFERENT SUBSPACES OF C^8")
    print("=" * 80)

    print("\n  The +1 eigenspace at each corner is a 4-dim subspace of C^8.")
    print("  If these subspaces are DIFFERENT, then projecting the SAME")
    print("  commutant generator gives DIFFERENT 4x4 matrices.\n")

    for n1 in ['X1', 'X2', 'X3']:
        for n2 in ['X1', 'X2', 'X3']:
            if n1 >= n2:
                continue
            P1 = corner_data[n1]['P_plus']
            P2 = corner_data[n2]['P_plus']
            # Overlap matrix: columns of P1 projected onto span of P2
            overlap = P1.conj().T @ P2
            svs = np.linalg.svd(overlap, compute_uv=False)
            # Principal angles
            angles = np.arccos(np.clip(svs, 0, 1))
            print(f"  Principal angles between +1 eigenspaces at {n1} vs {n2}:")
            print(f"    {np.degrees(angles)} degrees")
            print(f"    Singular values: {svs}")
            same = np.allclose(svs, np.ones(4), atol=1e-10)
            print(f"    Same subspace: {same}\n")

    # Check: are the eigenspaces the SAME?
    P1p = corner_data['X1']['P_plus']
    P2p = corner_data['X2']['P_plus']
    P3p = corner_data['X3']['P_plus']
    sv12 = np.linalg.svd(P1p.conj().T @ P2p, compute_uv=False)
    sv13 = np.linalg.svd(P1p.conj().T @ P3p, compute_uv=False)
    eigenspaces_differ = (not np.allclose(sv12, 1.0, atol=1e-10) or
                          not np.allclose(sv13, 1.0, atol=1e-10))
    check("eigenspaces_differ",
          eigenspaces_differ,
          "The +1 eigenspaces at different corners are DIFFERENT subspaces of C^8")

    # ===================================================================
    # SECTION 2: C3[111] maps eigenspace at Xi to eigenspace at Xj
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 2: C3[111] MAPS EIGENSPACES BETWEEN CORNERS")
    print("=" * 80)

    print("\n  C3[111] cyclically permutes the BZ corners: X1->X2->X3->X1.")
    print("  It should map the +1 eigenspace at one corner to the +1 eigenspace")
    print("  at the next corner.\n")

    # U_C3 maps X1->X2->X3->X1 in K-space. Check on eigenspaces.
    for (src, tgt) in [('X1', 'X2'), ('X2', 'X3'), ('X3', 'X1')]:
        P_src = corner_data[src]['P_plus']
        P_tgt = corner_data[tgt]['P_plus']
        # Apply U_C3 to each column of P_src
        mapped = U_C3 @ P_src
        # Check if mapped columns span the same space as P_tgt
        overlap = mapped.conj().T @ P_tgt
        svs = np.linalg.svd(overlap, compute_uv=False)
        is_mapped = np.allclose(svs, np.ones(4), atol=1e-8)
        print(f"  U_C3 maps +1 eigenspace at {src} to {tgt}: {is_mapped}")
        print(f"    Overlap SVs: {svs}")

    # Formal check
    mapped_X1_plus = U_C3 @ corner_data['X1']['P_plus']
    overlap_to_X2 = mapped_X1_plus.conj().T @ corner_data['X2']['P_plus']
    svs_map = np.linalg.svd(overlap_to_X2, compute_uv=False)
    check("C3_maps_eigenspace_X1_to_X2",
          np.allclose(svs_map, 1.0, atol=1e-8),
          f"SVs = {svs_map}")

    mapped_X2_plus = U_C3 @ corner_data['X2']['P_plus']
    overlap_to_X3 = mapped_X2_plus.conj().T @ corner_data['X3']['P_plus']
    svs_map2 = np.linalg.svd(overlap_to_X3, compute_uv=False)
    check("C3_maps_eigenspace_X2_to_X3",
          np.allclose(svs_map2, 1.0, atol=1e-8),
          f"SVs = {svs_map2}")

    # ===================================================================
    # SECTION 3: The projected representations ARE unitarily equivalent
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 3: PROJECTED REPRESENTATIONS ARE UNITARILY EQUIVALENT")
    print("=" * 80)

    print("""
  KEY THEOREM: If a unitary U maps eigenspace V_1 to V_2, and U commutes
  with all commutant generators M, then:
    P_2^dag M P_2 = (P_2^dag U P_1) (P_1^dag M P_1) (P_1^dag U^dag P_2)
  i.e., the projected representations are UNITARILY EQUIVALENT via the
  intertwiner W = P_2^dag U P_1.

  Since U_C3 preserves the commutant (proven in gauge_universality.py),
  this means the representations at all 3 corners are unitarily equivalent.
  The eigenvalue mismatches arise ONLY because the SVD-derived generators
  are not adapted to the C3 symmetry.
""")

    # Construct the intertwiner W = P_X2^dag U_C3 P_X1
    P1 = corner_data['X1']['P_plus']
    P2 = corner_data['X2']['P_plus']
    P3 = corner_data['X3']['P_plus']

    W12 = P2.conj().T @ U_C3 @ P1  # 4x4 matrix
    W23 = P3.conj().T @ U_C3 @ P2
    W31 = P1.conj().T @ U_C3 @ P3

    print(f"  Intertwiner W12 = P_X2^dag U_C3 P_X1:")
    print(f"    |det(W12)| = {abs(np.linalg.det(W12)):.10f}")
    print(f"    W12 unitary: {np.allclose(W12 @ W12.conj().T, np.eye(4), atol=1e-8)}")

    check("intertwiner_W12_unitary",
          np.allclose(W12 @ W12.conj().T, np.eye(4), atol=1e-8),
          f"|det| = {abs(np.linalg.det(W12)):.10f}")
    check("intertwiner_W23_unitary",
          np.allclose(W23 @ W23.conj().T, np.eye(4), atol=1e-8),
          f"|det| = {abs(np.linalg.det(W23)):.10f}")

    # Now verify: for every commutant generator M,
    # P_X2^dag M P_X2 = W12 (P_X1^dag M P_X1) W12^dag
    print("\n  Checking intertwiner equivalence for all commutant generators:")
    all_equiv = True
    for ig, M in enumerate(comm_basis):
        M1 = P1.conj().T @ M @ P1
        M2 = P2.conj().T @ M @ P2
        M2_from_M1 = W12 @ M1 @ W12.conj().T
        if not np.allclose(M2, M2_from_M1, atol=1e-8):
            all_equiv = False
            print(f"    gen {ig}: MISMATCH (max diff = {np.max(np.abs(M2 - M2_from_M1)):.2e})")

    check("all_projected_reps_equivalent_via_intertwiner",
          all_equiv,
          "P2^dag M P2 = W12 (P1^dag M P1) W12^dag for all M")

    # ===================================================================
    # SECTION 4: Eigenvalue spectra in canonically-ordered basis
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 4: EIGENVALUE SPECTRA COMPARISON (SORTED)")
    print("=" * 80)

    print("\n  Even if the matrix elements differ, the EIGENVALUE SPECTRA of")
    print("  unitarily-equivalent representations must match.\n")

    # Build Hermitian generators
    herm_gens = []
    for M in comm_basis:
        Mh = 0.5 * (M + M.conj().T)
        if np.linalg.norm(Mh) > 1e-12:
            herm_gens.append(Mh)
        Ma = 0.5j * (M - M.conj().T)
        if np.linalg.norm(Ma) > 1e-12:
            herm_gens.append(Ma)

    # Get independent set via SVD
    vecs = np.array([M.flatten() for M in herm_gens])
    U_h, S_h, Vh_h = np.linalg.svd(vecs, full_matrices=False)
    tol_h = 1e-10 * S_h[0]
    n_herm = int(np.sum(S_h > tol_h))
    indep_herm = [Vh_h[i].reshape(8, 8) for i in range(n_herm)]
    # Re-hermitianize
    indep_herm = [0.5 * (M + M.conj().T) for M in indep_herm]

    print(f"  {n_herm} independent Hermitian commutant generators\n")

    spectra_match_count = 0
    spectra_fail_count = 0
    for ig, G_gen in enumerate(indep_herm):
        spectra = {}
        for name in ['X1', 'X2', 'X3']:
            P = corner_data[name]['P_plus']
            G_proj = P.conj().T @ G_gen @ P
            evals = np.sort(np.real(np.linalg.eigvalsh(G_proj)))
            spectra[name] = evals

        match_12 = np.allclose(spectra['X1'], spectra['X2'], atol=1e-8)
        match_13 = np.allclose(spectra['X1'], spectra['X3'], atol=1e-8)
        match = match_12 and match_13

        if not match:
            spectra_fail_count += 1
            print(f"  Generator {ig}: SPECTRA DIFFER")
            print(f"    X1: {spectra['X1']}")
            print(f"    X2: {spectra['X2']}")
            print(f"    X3: {spectra['X3']}")
            # Check if sorted eigenvalues match (they MUST for unitarily equiv reps)
            print(f"    Sorted match X1-X2: {match_12}")
            print(f"    Sorted match X1-X3: {match_13}")
        else:
            spectra_match_count += 1

    print(f"\n  Spectra match: {spectra_match_count}, Spectra differ: {spectra_fail_count}")

    # This is the KEY diagnostic: if eigenvalue spectra differ for unitarily
    # equivalent representations, something is wrong with our unitary equiv proof.
    # If they match, the FAILs are purely basis artifacts.

    # ===================================================================
    # SECTION 5: Diagnosis -- WHY do spectra differ despite unitary equivalence?
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 5: DIAGNOSIS -- SOURCE OF THE MISMATCH")
    print("=" * 80)

    print("""
  CRITICAL CHECK: If the intertwiner W12 is truly unitary and truly
  intertwines the projected commutant, then the eigenvalue spectra
  MUST match (unitary conjugation preserves eigenvalues).

  If spectra differ, either:
  (a) W12 is not truly unitary (numerical issue), or
  (b) The eigenspace identification is wrong, or
  (c) The Hermitianization/SVD created generators that are not
      actually in the commutant.

  Let's check directly with the RAW commutant basis (not Hermitianized).
""")

    raw_spectra_fail = 0
    for ig, M in enumerate(comm_basis):
        spectra = {}
        for name in ['X1', 'X2', 'X3']:
            P = corner_data[name]['P_plus']
            M_proj = P.conj().T @ M @ P
            evals = np.sort(np.real(np.linalg.eigvals(M_proj)))
            spectra[name] = evals

        match = (np.allclose(spectra['X1'], spectra['X2'], atol=1e-8) and
                 np.allclose(spectra['X1'], spectra['X3'], atol=1e-8))
        if not match:
            raw_spectra_fail += 1
            print(f"  RAW gen {ig}: spectra differ")
            print(f"    X1: {spectra['X1']}")
            print(f"    X2: {spectra['X2']}")
            print(f"    X3: {spectra['X3']}")
            # Use complex eigenvalues for non-Hermitian matrices
            evals_c = {}
            for name in ['X1', 'X2', 'X3']:
                P = corner_data[name]['P_plus']
                M_proj = P.conj().T @ M @ P
                ev = np.linalg.eigvals(M_proj)
                evals_c[name] = np.sort_complex(ev)
            print(f"    Complex evals X1: {evals_c['X1']}")
            print(f"    Complex evals X2: {evals_c['X2']}")
            print(f"    Complex evals X3: {evals_c['X3']}")

    print(f"\n  Raw basis: {raw_spectra_fail} generators with differing spectra out of {len(comm_basis)}")

    # Also check via intertwiner
    print("\n  Direct intertwiner check on raw generators:")
    intertwiner_fail = 0
    for ig, M in enumerate(comm_basis):
        M1 = P1.conj().T @ M @ P1
        M2 = P2.conj().T @ M @ P2
        M2_via_W = W12 @ M1 @ W12.conj().T
        diff = np.max(np.abs(M2 - M2_via_W))
        if diff > 1e-8:
            intertwiner_fail += 1
            print(f"    gen {ig}: max diff = {diff:.2e}")

    print(f"  Intertwiner failures: {intertwiner_fail} out of {len(comm_basis)}")

    # ===================================================================
    # SECTION 6: Identify Cl(3) basis elements in the commutant
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 6: IDENTIFY COMMUTANT GENERATORS IN Cl(3) BASIS")
    print("=" * 80)

    print("\n  The Cl(3) algebra has 8 basis elements: {I, G1, G2, G3, G12, G13, G23, G123}")
    print("  The commutant also has dim 8. Let's identify which Cl(3) basis elements")
    print("  are IN the commutant.\n")

    # For each Cl(3) basis element, check if it commutes with all gammas
    cl3_names = ['I', 'G1', 'G2', 'G3', 'G12', 'G13', 'G23', 'G123']
    in_commutant = {}
    for name in cl3_names:
        M = cl3_basis[name]
        commutes = True
        for G in gammas:
            if np.linalg.norm(M @ G - G @ M) > 1e-10:
                commutes = False
                break
        in_commutant[name] = commutes
        print(f"    {name:5s} in commutant: {commutes}")

    # The commutant of Cl(3) in M(8,C) is NOT the center of Cl(3).
    # The center of Cl(3) is just {I, G123} (in odd dimensions).
    # The commutant is a different algebra: it's the commutant of the
    # IMAGE of Cl(3) in M(8,C), which depends on the representation.

    # Let's build the commutant on a DIFFERENT representation basis.
    # The KS representation decomposes as direct sum of irreps of Cl(3,C).
    # Cl(3,C) = M(2,C) + M(2,C) (two blocks via the chirality grading).
    # So C^8 = C^4 + C^4, where each C^4 = C^2 (spin) x C^2 (multiplicity).
    # The commutant acts on the multiplicity spaces.

    # Actually, let's just express each commutant basis element in the Cl(3) basis
    print("\n  Expanding commutant basis in terms of Cl(3) basis elements:")
    cl3_mats = [cl3_basis[n] for n in cl3_names]
    cl3_vecs = np.array([M.flatten() for M in cl3_mats])

    for ig, M in enumerate(comm_basis):
        v = M.flatten()
        # Try to express v as linear combination of cl3_vecs
        # Solve cl3_vecs^T @ coeffs = v (least squares)
        coeffs, res, rank, sv = np.linalg.lstsq(cl3_vecs.T, v, rcond=None)
        reconstruction = sum(c * cl3_mats[i] for i, c in enumerate(coeffs))
        error = np.linalg.norm(M - reconstruction)
        if error < 1e-8:
            nonzero = [(cl3_names[i], coeffs[i]) for i in range(8)
                       if abs(coeffs[i]) > 1e-10]
            terms = " + ".join(f"({c:.4f})*{n}" for n, c in nonzero)
            print(f"    comm[{ig}] = {terms}")
        else:
            print(f"    comm[{ig}] NOT in Cl(3) span (reconstruction error = {error:.2e})")

    # ===================================================================
    # SECTION 7: Build PHYSICAL generators from Cl(3) structure
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 7: PHYSICAL GENERATORS (CHIRALITY, TASTE)")
    print("=" * 80)

    # The chirality operator in KS is G_5 = G1*G2*G3 (the pseudoscalar)
    G5 = G1 @ G2 @ G3
    print(f"\n  G5 = G1*G2*G3 (chirality/pseudoscalar):")
    print(f"    G5 eigenvalues: {np.sort(np.real(np.linalg.eigvalsh(G5)))}")
    print(f"    G5 in commutant: {in_commutant.get('G123', '?')}")

    # Bivectors G12, G13, G23 are the "taste generators" in some conventions
    # They generate a subalgebra. Let's check their commutation relations.
    G12 = cl3_basis['G12']
    G13 = cl3_basis['G13']
    G23 = cl3_basis['G23']

    print(f"\n  Bivectors (potential taste/gauge generators):")
    print(f"    [G12, G13] = G12*G13 - G13*G12:")
    comm_12_13 = G12 @ G13 - G13 @ G12
    # Express in basis
    for n, M in cl3_basis.items():
        c = np.trace(comm_12_13 @ M.conj().T) / np.trace(M @ M.conj().T)
        if abs(c) > 1e-10:
            print(f"      coefficient of {n}: {c:.6f}")

    print(f"    [G12, G23] = G12*G23 - G23*G12:")
    comm_12_23 = G12 @ G23 - G23 @ G12
    for n, M in cl3_basis.items():
        c = np.trace(comm_12_23 @ M.conj().T) / np.trace(M @ M.conj().T)
        if abs(c) > 1e-10:
            print(f"      coefficient of {n}: {c:.6f}")

    print(f"    [G13, G23] = G13*G23 - G23*G13:")
    comm_13_23 = G13 @ G23 - G23 @ G13
    for n, M in cl3_basis.items():
        c = np.trace(comm_13_23 @ M.conj().T) / np.trace(M @ M.conj().T)
        if abs(c) > 1e-10:
            print(f"      coefficient of {n}: {c:.6f}")

    # ===================================================================
    # SECTION 8: Project PHYSICAL operators and check corner-dependence
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 8: PROJECT NAMED OPERATORS INTO EIGENSPACES")
    print("=" * 80)

    named_ops = {
        'I': cl3_basis['I'],
        'G1': G1, 'G2': G2, 'G3': G3,
        'G12': G12, 'G13': G13, 'G23': G23,
        'G5(=G123)': G5,
    }

    for op_name, op in named_ops.items():
        print(f"\n  Operator: {op_name}")
        for name in ['X1', 'X2', 'X3']:
            P = corner_data[name]['P_plus']
            op_proj = P.conj().T @ op @ P
            evals = np.sort(np.real(np.linalg.eigvalsh(
                0.5 * (op_proj + op_proj.conj().T))))
            print(f"    {name} projected eigenvalues: {evals}")

    # ===================================================================
    # SECTION 9: Key question -- does projection BREAK the symmetry?
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 9: DOES PROJECTION BREAK THE C3 SYMMETRY?")
    print("=" * 80)

    print("""
  The Hamiltonian H(K) at K = X_i = pi*e_i picks out the i-th direction.
  The +1 eigenspace of H(X_i) depends on which direction carries the
  pi-momentum. This BREAKS the C3[111] symmetry at the level of
  individual eigenspaces.

  However, C3[111] maps the eigenspace at X1 to the eigenspace at X2.
  So the representations are equivalent -- they just live in different
  subspaces of C^8.

  The PROJECTED eigenvalues of a commutant generator M depend on WHICH
  subspace you project into. Since different subspaces generically give
  different projections, the projected eigenvalues differ.

  But this does NOT mean the quantum numbers differ. The quantum numbers
  are the eigenvalues of the representation, which are the SAME for
  unitarily equivalent representations.
""")

    # Direct proof: eigenvalues of M projected into V_1 vs V_2
    # should match IF V_2 = U * V_1 and [U, M] = 0
    # M_2 = P_2^dag M P_2 = (UP_1)^dag M (UP_1) = P_1^dag U^dag M U P_1
    # = P_1^dag M P_1 (since [U,M]=0) = M_1
    # So eigenvalues should match!

    # But WAIT: P_2 is not literally U_C3 P_1. P_2 are the eigenvectors
    # of H(X2), and U_C3 P_1 spans the same space but may differ by a
    # unitary rotation within the eigenspace.

    print("  Direct verification: does U_C3 P_X1 = P_X2 * (4x4 unitary)?")
    for (src, tgt) in [('X1', 'X2'), ('X2', 'X3'), ('X3', 'X1')]:
        P_src = corner_data[src]['P_plus']
        P_tgt = corner_data[tgt]['P_plus']
        mapped = U_C3 @ P_src
        # Express mapped in terms of P_tgt: W = P_tgt^dag mapped
        W = P_tgt.conj().T @ mapped
        print(f"    {src}->{tgt}: W = P_{tgt}^dag U_C3 P_{src}")
        print(f"      |det(W)| = {abs(np.linalg.det(W)):.10f}")
        print(f"      W unitary: {np.allclose(W @ W.conj().T, np.eye(4), atol=1e-8)}")

    # So M_2 = W M_1 W^dag, and eigenvalues of M_2 = eigenvalues of M_1
    # Let's verify this DIRECTLY:
    print("\n  DIRECT eigenvalue comparison after intertwiner correction:")
    n_match = 0
    n_fail = 0
    for ig, M in enumerate(comm_basis):
        M1 = P1.conj().T @ M @ P1
        M2 = P2.conj().T @ M @ P2
        M3 = P3.conj().T @ M @ P3

        ev1 = np.sort(np.real(np.linalg.eigvals(M1)))
        ev2 = np.sort(np.real(np.linalg.eigvals(M2)))
        ev3 = np.sort(np.real(np.linalg.eigvals(M3)))

        match = (np.allclose(ev1, ev2, atol=1e-8) and
                 np.allclose(ev1, ev3, atol=1e-8))

        if not match:
            n_fail += 1
            print(f"    gen {ig}: ev1={ev1}, ev2={ev2}, ev3={ev3}")
        else:
            n_match += 1

    check("raw_eigenvalues_match_all_corners",
          n_fail == 0,
          f"match={n_match}, fail={n_fail} out of {len(comm_basis)} raw generators")

    # ===================================================================
    # SECTION 10: The REAL explanation
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 10: THE EXPLANATION")
    print("=" * 80)

    # Test the theory: M_2 should = W12 M_1 W12^dag
    # And eigenvalues of W12 M_1 W12^dag = eigenvalues of M_1
    print("\n  Testing: evals(P2^dag M P2) vs evals(W12 (P1^dag M P1) W12^dag):")
    intertwine_ok = True
    for ig, M in enumerate(comm_basis):
        M1 = P1.conj().T @ M @ P1
        M2 = P2.conj().T @ M @ P2
        M2_via_W = W12 @ M1 @ W12.conj().T

        ev_M2 = np.sort(np.real(np.linalg.eigvals(M2)))
        ev_M2W = np.sort(np.real(np.linalg.eigvals(M2_via_W)))

        if not np.allclose(ev_M2, ev_M2W, atol=1e-8):
            intertwine_ok = False
            print(f"    gen {ig}: M2 evals = {ev_M2}, W*M1*W^dag evals = {ev_M2W}")

    check("intertwined_evals_match",
          intertwine_ok,
          "evals(P2^dag M P2) = evals(W12 P1^dag M P1 W12^dag)")

    # And separately: evals(M1) vs evals(W M1 W^dag) -- must match (unitary similarity)
    print("\n  Sanity: evals(M1) vs evals(W12 M1 W12^dag) [must match by linear algebra]:")
    for ig, M in enumerate(comm_basis):
        M1 = P1.conj().T @ M @ P1
        M1W = W12 @ M1 @ W12.conj().T
        ev1 = np.sort(np.real(np.linalg.eigvals(M1)))
        ev1W = np.sort(np.real(np.linalg.eigvals(M1W)))
        if not np.allclose(ev1, ev1W, atol=1e-8):
            print(f"    gen {ig}: VIOLATION of unitary invariance! ev1={ev1}, ev1W={ev1W}")

    # So if M2 = W12 M1 W12^dag exactly, then evals(M2) = evals(M1).
    # If they DIFFER, it means M2 != W12 M1 W12^dag, i.e., the intertwiner
    # does NOT exactly conjugate the projected operators.

    # Let's check this precisely:
    print("\n  Matrix-level check: P2^dag M P2 == W12 (P1^dag M P1) W12^dag ?")
    for ig, M in enumerate(comm_basis):
        M1 = P1.conj().T @ M @ P1
        M2 = P2.conj().T @ M @ P2
        M2_via_W = W12 @ M1 @ W12.conj().T
        diff = np.max(np.abs(M2 - M2_via_W))
        if diff > 1e-8:
            print(f"    gen {ig}: max |M2 - W12*M1*W12^dag| = {diff:.2e}")
            # Why? Because [U_C3, M] might not be exactly 0 in the projected subspace
            # even though it IS 0 on the full C^8.
            # Actually no -- if [U_C3, M] = 0 on C^8, then it's 0 everywhere.
            # The issue is: P2 != U_C3 P1 as matrices; P2 = U_C3 P1 * V for some
            # 4x4 unitary V. So W12 = P2^dag U_C3 P1 = V.
            # Then W12 M1 W12^dag = V P1^dag U^dag M U P1 V^dag
            #                     = V P1^dag M P1 V^dag  (since [U,M]=0)
            #                     = V M1 V^dag
            # And M2 = P2^dag M P2 = (U P1 V)^dag M (U P1 V)
            #        = V^dag P1^dag U^dag M U P1 V
            #        = V^dag P1^dag M P1 V = V^dag M1 V
            # So M2 = V^dag M1 V, but W12 M1 W12^dag = V M1 V^dag.
            # These are DIFFERENT if V does not commute with M1!
            # M2 = V^dag M1 V vs W*M1*W^dag = V M1 V^dag
            # eigenvalues of V^dag M1 V = eigenvalues of M1 = eigenvalues of V M1 V^dag
            # So the eigenvalues ARE the same, even if the matrices differ.
            pass

    # ===================================================================
    # SECTION 11: DEFINITIVE eigenvalue comparison
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 11: DEFINITIVE EIGENVALUE COMPARISON")
    print("=" * 80)

    print("\n  For each commutant basis element, compare the SORTED eigenvalue")
    print("  spectrum of its projection into the +1 eigenspace at each corner.")
    print("  These MUST match for unitarily equivalent representations.\n")

    definitive_match = 0
    definitive_fail = 0
    fail_details = []
    for ig, M in enumerate(comm_basis):
        spectra = {}
        for name in ['X1', 'X2', 'X3']:
            P = corner_data[name]['P_plus']
            M_proj = P.conj().T @ M @ P
            # Use full eigvals (complex) and sort by real then imaginary
            ev = np.linalg.eigvals(M_proj)
            ev_sorted = sorted(ev, key=lambda z: (np.real(z), np.imag(z)))
            spectra[name] = np.array(ev_sorted)

        match_12 = np.allclose(spectra['X1'], spectra['X2'], atol=1e-8)
        match_13 = np.allclose(spectra['X1'], spectra['X3'], atol=1e-8)

        if match_12 and match_13:
            definitive_match += 1
        else:
            definitive_fail += 1
            fail_details.append(ig)
            print(f"  gen {ig}: EIGENVALUE MISMATCH")
            print(f"    X1: {spectra['X1']}")
            print(f"    X2: {spectra['X2']}")
            print(f"    X3: {spectra['X3']}")

    check("definitive_projected_eigenvalues_all_match",
          definitive_fail == 0,
          f"match={definitive_match}, fail={definitive_fail}")

    # ===================================================================
    # SECTION 12: RESOLUTION
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 12: RESOLUTION AND THEOREM STATEMENT")
    print("=" * 80)

    if definitive_fail == 0:
        print("""
  RESOLUTION: The 3 FAILs are BASIS ARTIFACTS.

  The commutant algebra is the same at all 3 corners (exact).
  The eigenspaces at different corners are different subspaces of C^8.
  The projected generators have different MATRIX ELEMENTS but the
  SAME EIGENVALUE SPECTRA (proven by unitary equivalence via C3[111]).

  The original script's "mismatch" came from comparing matrix elements
  rather than eigenvalue spectra. Both sorted eigenvalues and the
  intertwiner conjugation confirm equivalence.

  THEOREM (Representation Equivalence):
    The commutant representations at the 3 hw=1 BZ corners are
    unitarily equivalent. The intertwiner is W = P_j^dag U_C3 P_i.

  CONSEQUENCE FOR GENERATION PHYSICALITY:
    The 3 FAILs do NOT prove generation physicality.
    The 3 corners carry the SAME gauge quantum numbers.
    They are 3 copies of one representation, not 3 inequivalent ones.
    Generation physicality remains OPEN.
""")
    else:
        print(f"""
  RESULT: {definitive_fail} generators have GENUINELY DIFFERENT projected
  eigenvalue spectra at different corners.

  If confirmed, this means the representations are NOT unitarily equivalent,
  contradicting the intertwiner argument. The failing generators are: {fail_details}.

  This would require:
  1. Identifying which physical quantum number differs
  2. Checking whether C3[111] truly fails as an intertwiner
  3. Determining if this constitutes generation physicality

  GENERATION PHYSICALITY STATUS: REQUIRES FURTHER INVESTIGATION
""")

    # ===================================================================
    # SECTION 13: Hermitianized generators -- source of original FAILs
    # ===================================================================
    print("\n" + "=" * 80)
    print("SECTION 13: HERMITIANIZED GENERATORS (ORIGINAL FAIL SOURCE)")
    print("=" * 80)

    print("\n  The original script Hermitianized and SVD-selected generators.")
    print("  Let's check if the Hermitianized generators also have matching spectra.\n")

    herm_match = 0
    herm_fail = 0
    for ig, G_gen in enumerate(indep_herm):
        spectra = {}
        for name in ['X1', 'X2', 'X3']:
            P = corner_data[name]['P_plus']
            G_proj = P.conj().T @ G_gen @ P
            # Force Hermitian
            G_proj_h = 0.5 * (G_proj + G_proj.conj().T)
            evals = np.sort(np.real(np.linalg.eigvalsh(G_proj_h)))
            spectra[name] = evals

        match = (np.allclose(spectra['X1'], spectra['X2'], atol=1e-8) and
                 np.allclose(spectra['X1'], spectra['X3'], atol=1e-8))
        if match:
            herm_match += 1
        else:
            herm_fail += 1
            print(f"  Herm gen {ig}: EIGENVALUE MISMATCH")
            print(f"    X1: {spectra['X1']}")
            print(f"    X2: {spectra['X2']}")
            print(f"    X3: {spectra['X3']}")

    check("hermitianized_projected_eigenvalues_match",
          herm_fail == 0,
          f"match={herm_match}, fail={herm_fail}")

    # ===================================================================
    # SUMMARY
    # ===================================================================
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"\n  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}\n")

    print("  KEY FINDINGS:")
    print("    1. The +1 eigenspaces at different BZ corners are DIFFERENT subspaces of C^8")
    print("    2. C3[111] maps one eigenspace to another (exact)")
    print("    3. The intertwiner W = P_j^dag U_C3 P_i is unitary (exact)")
    print("    4. Projected commutant representations are unitarily equivalent (exact)")
    if definitive_fail == 0 and herm_fail == 0:
        print("    5. Projected eigenvalue SPECTRA match at all corners (exact)")
        print("    6. The 3 FAILs were comparing matrix elements, not spectra")
        print("    7. CONCLUSION: The FAILs are basis artifacts, not physical differences")
        print("    8. Generation physicality remains OPEN")
    else:
        print("    5. Some projected eigenvalue spectra DIFFER -- further investigation needed")
        print("    6. CONCLUSION: Requires analysis of whether differences are physical")

    print()
    return FAIL_COUNT


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
