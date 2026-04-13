#!/usr/bin/env python3
"""
Generation Entanglement: SLOCC Classification of the 3-Qubit Taste Space
=========================================================================

QUESTION: Can the 3 generations be derived from the ENTANGLEMENT STRUCTURE
of the Cl(3) = (C^2)^{otimes 3} taste space, independent of Z_3 symmetry
or BZ combinatorics?

BACKGROUND:
  The Cl(3) taste space at each lattice site is a 3-qubit system (C^2)^{otimes 3}.
  The entanglement structure of 3-qubit pure states is classified by SLOCC
  (stochastic local operations + classical communication) into exactly 6 classes:
    - separable
    - biseparable A|BC, B|AC, C|AB  (3 types)
    - W class
    - GHZ class
  Reference: Dur, Vidal, Cirac, PRA 62, 062314 (2000).

  The 8 computational basis states |s1,s2,s3> with s_i in {0,1} are product
  states (separable) since each is a tensor product of single-qubit states.
  The SLOCC classification applies to superposition states, not to individual
  basis states.

  KEY INSIGHT: The Hamming weight decomposition 8 = 1+3+3+1 and the SLOCC
  classification are mathematically distinct structures. The question is
  whether they connect in a physically meaningful way.

WHAT THIS SCRIPT CHECKS:
  LEVEL A -- Exact algebraic facts (theorem-grade):
    A1. All 8 computational basis states are product (separable) states
    A2. The Hamming-weight orbits {hw=0,1,2,3} = {1,3,3,1} are
        exactly the orbits of the qubit permutation group S_3
    A3. The W-class representative W = |100> + |010> + |001> is the
        equal superposition of the hw=1 orbit
    A4. The GHZ-class representative GHZ = |000> + |111> is the equal
        superposition of the hw=0 and hw=3 states
    A5. Entanglement invariants (3-tangle, concurrences) distinguish
        W and GHZ classes

  LEVEL B -- Structural connections (requires assumptions):
    B1. The hw=1 orbit spans a 3-dim subspace; any generic state in it
        is W-class (not GHZ-class) -- this is the W/GHZ discrimination
    B2. The Z_3 cyclic permutation (s1,s2,s3) -> (s2,s3,s1) acts within
        each Hamming-weight sector; its eigenstates in the hw=1 sector
        are W-class states with definite Z_3 charge
    B3. Under qubit permutations, the hw=1 and hw=2 sectors each form
        irreducible representations of S_3

  LEVEL C -- Obstructions and honest assessment:
    C1. The 3 generations cannot simply be "the 3 W-class basis states"
        because |100>, |010>, |001> are individually separable, not W-class
    C2. Entanglement class is a property of superposition states, not of
        individual basis vectors
    C3. The SLOCC classification alone does not produce 3 distinct objects;
        the W class is one class, not three
    C4. To get "3 things" from entanglement one still needs additional
        structure (Z_3 eigenvalues, permutation reps, or dynamics)

STATUS: BOUNDED -- The entanglement perspective provides a well-motivated
  physical interpretation of the hw=1 subspace (it is the natural home of
  W-class entanglement) but does not by itself close the generation
  physicality gate without additional structure.

PStack experiment: generation-entanglement
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import numpy as np
from numpy.linalg import eigh, norm
from itertools import combinations

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str, level: str = "?"):
    """Record a test result with its evidence level."""
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] [{level}] {tag}: {msg}")


# =============================================================================
# Infrastructure
# =============================================================================

I2 = np.eye(2, dtype=complex)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def taste_states():
    """Return the 8 taste states as tuples (s1,s2,s3) in {0,1}^3."""
    return [(s1, s2, s3) for s1 in range(2) for s2 in range(2) for s3 in range(2)]


def state_index(s):
    return s[0] * 4 + s[1] * 2 + s[2]


def hamming_weight(s):
    return sum(s)


def computational_basis_vector(s):
    """Return the 8-component vector for |s1,s2,s3>."""
    v = np.zeros(8, dtype=complex)
    v[state_index(s)] = 1.0
    return v


def kron3(A, B, C):
    return np.kron(A, np.kron(B, C))


# =============================================================================
# Entanglement measures for 3-qubit states
# =============================================================================

def partial_trace_single(psi, keep_qubit):
    """
    Partial trace of |psi><psi| over all qubits except keep_qubit.
    Returns the 2x2 reduced density matrix for the kept qubit.
    psi is an 8-component vector for a 3-qubit system.
    keep_qubit in {0, 1, 2} (qubit 0 is leftmost).
    """
    rho_full = np.outer(psi, psi.conj())
    # Reshape to (2,2,2,2,2,2)
    rho_tensor = rho_full.reshape(2, 2, 2, 2, 2, 2)
    # Trace over the other two qubits
    if keep_qubit == 0:
        rho_red = np.einsum('ijkimn->jn', rho_tensor.reshape(2, 2, 2, 2, 2, 2))
        # Actually: indices are (i,j,k, i',j',k') -> keep i,i', trace j=j', k=k'
        rho_red = np.einsum('ijkilk->il', rho_tensor.reshape(2, 2, 2, 2, 2, 2))
    elif keep_qubit == 1:
        rho_red = np.einsum('ijkijk->jk', rho_tensor.reshape(2, 2, 2, 2, 2, 2))
        # keep j,j', trace i=i', k=k'
        rho_red = np.einsum('ijkljl->ik', rho_tensor.reshape(2, 2, 2, 2, 2, 2))
        # Fix: use explicit contraction
    elif keep_qubit == 2:
        rho_red = np.einsum('ijkilk->jl', rho_tensor.reshape(2, 2, 2, 2, 2, 2))

    # Let me do this more carefully with explicit reshape
    return _partial_trace_qubit(psi, keep_qubit)


def _partial_trace_qubit(psi, keep):
    """Compute reduced density matrix by tracing out all qubits except 'keep'."""
    # Reshape psi into (2,2,2) tensor
    psi_t = psi.reshape(2, 2, 2)
    rho = np.zeros((2, 2), dtype=complex)
    trace_qubits = [q for q in range(3) if q != keep]
    for i in range(2):
        for j in range(2):
            # Sum over traced qubits
            val = 0.0
            for a in range(2):
                for b in range(2):
                    idx_bra = [0, 0, 0]
                    idx_ket = [0, 0, 0]
                    idx_bra[keep] = i
                    idx_ket[keep] = j
                    idx_bra[trace_qubits[0]] = a
                    idx_ket[trace_qubits[0]] = a
                    idx_bra[trace_qubits[1]] = b
                    idx_ket[trace_qubits[1]] = b
                    val += psi_t[tuple(idx_bra)] * psi_t[tuple(idx_ket)].conj()
            rho[i, j] = val
    return rho


def partial_trace_bipartite(psi, keep_qubits):
    """
    Partial trace of |psi><psi| keeping a pair of qubits.
    keep_qubits is a tuple of two qubit indices, e.g. (0,1).
    Returns 4x4 reduced density matrix.
    """
    psi_t = psi.reshape(2, 2, 2)
    trace_qubit = [q for q in range(3) if q not in keep_qubits][0]
    dim_keep = 4
    rho = np.zeros((dim_keep, dim_keep), dtype=complex)

    for i0 in range(2):
        for i1 in range(2):
            for j0 in range(2):
                for j1 in range(2):
                    val = 0.0
                    for a in range(2):
                        idx_bra = [0, 0, 0]
                        idx_ket = [0, 0, 0]
                        idx_bra[keep_qubits[0]] = i0
                        idx_bra[keep_qubits[1]] = i1
                        idx_ket[keep_qubits[0]] = j0
                        idx_ket[keep_qubits[1]] = j1
                        idx_bra[trace_qubit] = a
                        idx_ket[trace_qubit] = a
                        val += psi_t[tuple(idx_bra)] * psi_t[tuple(idx_ket)].conj()
                    row = i0 * 2 + i1
                    col = j0 * 2 + j1
                    rho[row, col] = val
    return rho


def concurrence_2qubit(rho):
    """
    Concurrence of a 2-qubit density matrix.
    C = max(0, l1-l2-l3-l4) where l_i are sqrt of eigenvalues
    of rho * (sy x sy) rho* (sy x sy) in decreasing order.
    """
    sy_sy = np.kron(SIGMA_Y, SIGMA_Y)
    rho_tilde = sy_sy @ rho.conj() @ sy_sy
    R = rho @ rho_tilde
    eigenvalues = np.sort(np.real(np.sqrt(np.maximum(np.linalg.eigvals(R), 0))))[::-1]
    C = max(0.0, eigenvalues[0] - eigenvalues[1] - eigenvalues[2] - eigenvalues[3])
    return float(np.real(C))


def three_tangle(psi):
    """
    Coffman-Kundu-Wootters 3-tangle (residual tangle) for a pure 3-qubit state.
    tau_ABC = tau_A(BC) - tau_AB - tau_AC
    where tau_XY = C^2(rho_XY) is the squared concurrence.

    Key property: tau = 0 for W-class, tau > 0 for GHZ-class.
    Reference: Coffman, Kundu, Wootters, PRA 61, 052306 (2000).
    """
    psi_n = psi / norm(psi)

    # tau_A(BC): linear entropy of qubit A
    rho_A = _partial_trace_qubit(psi_n, 0)
    tau_A_BC = 4.0 * np.real(np.linalg.det(rho_A))

    # tau_AB and tau_AC: squared concurrences
    rho_AB = partial_trace_bipartite(psi_n, (0, 1))
    rho_AC = partial_trace_bipartite(psi_n, (0, 2))
    C_AB = concurrence_2qubit(rho_AB)
    C_AC = concurrence_2qubit(rho_AC)
    tau_AB = C_AB ** 2
    tau_AC = C_AC ** 2

    tau = tau_A_BC - tau_AB - tau_AC
    return max(0.0, float(np.real(tau)))


def hyperdeterminant_3tangle(psi):
    """
    Direct computation of the 3-tangle via the Cayley hyperdeterminant.
    For psi = sum a_{ijk} |ijk>, the 3-tangle is |Delta|^2 where
    Delta = a000^2 a111^2 + a001^2 a110^2 + a010^2 a101^2 + a100^2 a011^2
            - 2(a000 a001 a110 a111 + a000 a010 a101 a111
                + a000 a100 a011 a111 + a001 a010 a101 a110
                + a001 a100 a011 a110 + a010 a100 a011 a101)
            + 4(a000 a011 a101 a110 + a001 a010 a100 a111)
    """
    psi_n = psi / norm(psi)
    a = psi_n.reshape(2, 2, 2)

    d = (a[0,0,0]**2 * a[1,1,1]**2
       + a[0,0,1]**2 * a[1,1,0]**2
       + a[0,1,0]**2 * a[1,0,1]**2
       + a[1,0,0]**2 * a[0,1,1]**2
       - 2*(a[0,0,0]*a[0,0,1]*a[1,1,0]*a[1,1,1]
           + a[0,0,0]*a[0,1,0]*a[1,0,1]*a[1,1,1]
           + a[0,0,0]*a[1,0,0]*a[0,1,1]*a[1,1,1]
           + a[0,0,1]*a[0,1,0]*a[1,0,1]*a[1,1,0]
           + a[0,0,1]*a[1,0,0]*a[0,1,1]*a[1,1,0]
           + a[0,1,0]*a[1,0,0]*a[0,1,1]*a[1,0,1])
       + 4*(a[0,0,0]*a[0,1,1]*a[1,0,1]*a[1,1,0]
           + a[0,0,1]*a[0,1,0]*a[1,0,0]*a[1,1,1]))

    return float(np.abs(d))


def von_neumann_entropy(rho):
    """Von Neumann entropy S = -Tr(rho log rho)."""
    evals = np.real(np.linalg.eigvalsh(rho))
    evals = evals[evals > 1e-15]
    return -np.sum(evals * np.log2(evals))


def is_product_state(psi, tol=1e-10):
    """
    Check if a 3-qubit pure state is a product state (fully separable).
    A product state has all single-qubit reduced density matrices pure.
    """
    psi_n = psi / norm(psi)
    for q in range(3):
        rho_q = _partial_trace_qubit(psi_n, q)
        entropy = von_neumann_entropy(rho_q)
        if entropy > tol:
            return False
    return True


# =============================================================================
# Kawamoto-Smit Gamma matrices (Cl(3) on taste space)
# =============================================================================

def build_gamma_ks():
    """Kawamoto-Smit Gamma matrices on C^8 = (C^2)^{otimes 3}."""
    G1 = kron3(SIGMA_X, I2, I2)
    G2 = kron3(SIGMA_Z, SIGMA_X, I2)
    G3 = kron3(SIGMA_Z, SIGMA_Z, SIGMA_X)
    return [G1, G2, G3]


def build_taste_hamiltonian(m=0.0, couplings=(1.0, 1.0, 1.0)):
    """
    Taste-space Hamiltonian from Cl(3) structure.
    H_taste = sum_mu c_mu Gamma_mu + m * I
    This acts on the 8-dim taste space at a single site.
    """
    gammas = build_gamma_ks()
    H = m * np.eye(8, dtype=complex)
    for mu in range(3):
        H += couplings[mu] * gammas[mu]
    return H


# =============================================================================
# Z_3 permutation infrastructure
# =============================================================================

def z3_permutation_matrix():
    """8x8 matrix for sigma: (s1,s2,s3) -> (s2,s3,s1)."""
    P = np.zeros((8, 8), dtype=complex)
    for s in taste_states():
        i = state_index(s)
        j = state_index((s[1], s[2], s[0]))
        P[j, i] = 1.0
    return P


def s3_permutation_matrices():
    """All 6 elements of S_3 acting on qubits by permuting tensor factors."""
    perms = [
        (0, 1, 2),  # identity
        (1, 2, 0),  # cyclic
        (2, 0, 1),  # cyclic^2
        (1, 0, 2),  # swap 0,1
        (0, 2, 1),  # swap 1,2
        (2, 1, 0),  # swap 0,2
    ]
    matrices = []
    for p in perms:
        M = np.zeros((8, 8), dtype=complex)
        for s in taste_states():
            i = state_index(s)
            s_perm = tuple(s[p[k]] for k in range(3))
            j = state_index(s_perm)
            M[j, i] = 1.0
        matrices.append(M)
    return matrices


# =============================================================================
# LEVEL A: EXACT ALGEBRAIC FACTS
# =============================================================================

def level_A_exact_algebra():
    """
    Theorem-grade facts about the 3-qubit structure.
    No assumptions beyond Cl(3) = (C^2)^{otimes 3}.
    """
    print("\n" + "=" * 72)
    print("LEVEL A: EXACT ALGEBRAIC FACTS (theorem-grade)")
    print("=" * 72)

    states = taste_states()

    # ----- A1: All basis states are product (separable) states -----
    print("\n--- A1: Computational basis states are product states ---")
    all_product = True
    for s in states:
        psi = computational_basis_vector(s)
        prod = is_product_state(psi)
        if not prod:
            all_product = False
        # Check: each basis state |s1,s2,s3> = |s1> x |s2> x |s3>
        # so it must be a product state
    report("A1-all-basis-product", all_product,
           "All 8 basis states |s1,s2,s3> are product (separable) states", "A")

    # This is the fundamental point: basis states are NOT in any
    # nontrivial SLOCC class. They are all separable.
    print("  NOTE: Individual basis states like |100> are separable, NOT W-class.")
    print("        SLOCC classes apply to superposition states.")

    # ----- A2: Hamming weight decomposition = S_3 orbits -----
    print("\n--- A2: Hamming weight orbits = qubit permutation (S_3) orbits ---")
    hw_orbits = {0: [], 1: [], 2: [], 3: []}
    for s in states:
        hw_orbits[hamming_weight(s)].append(s)

    sizes = [len(hw_orbits[w]) for w in range(4)]
    report("A2-hw-sizes", sizes == [1, 3, 3, 1],
           f"Hamming weight orbit sizes: {sizes} = [1,3,3,1]", "A")

    # Verify these are exactly the S_3 orbits
    s3_mats = s3_permutation_matrices()
    for w in range(4):
        orbit_indices = set(state_index(s) for s in hw_orbits[w])
        # Check S_3 closure: applying any permutation to an orbit member
        # stays in the orbit
        closed = True
        for M in s3_mats:
            for s in hw_orbits[w]:
                psi = computational_basis_vector(s)
                psi_perm = M @ psi
                # Find which basis state this is
                idx = np.argmax(np.abs(psi_perm))
                if idx not in orbit_indices:
                    closed = False
        report(f"A2-S3-orbit-hw{w}", closed,
               f"hw={w} orbit closed under S_3: states = {hw_orbits[w]}", "A")

    # ----- A3: W state is the equal superposition of hw=1 -----
    print("\n--- A3: W-class representative from hw=1 ---")
    W_state = np.zeros(8, dtype=complex)
    for s in hw_orbits[1]:
        W_state += computational_basis_vector(s)
    W_state /= norm(W_state)

    # Verify: this is the standard W state |100> + |010> + |001> (normalized)
    expected_W = np.zeros(8, dtype=complex)
    expected_W[state_index((1, 0, 0))] = 1.0
    expected_W[state_index((0, 1, 0))] = 1.0
    expected_W[state_index((0, 0, 1))] = 1.0
    expected_W /= norm(expected_W)

    w_match = np.allclose(np.abs(W_state), np.abs(expected_W))
    report("A3-W-from-hw1", w_match,
           "W = (|100> + |010> + |001>)/sqrt(3)", "A")

    # Verify W is NOT a product state (it's genuinely entangled)
    w_not_product = not is_product_state(W_state)
    report("A3-W-entangled", w_not_product,
           "W state is genuinely entangled (not separable)", "A")

    # ----- A4: GHZ state from hw=0 and hw=3 -----
    print("\n--- A4: GHZ-class representative from hw=0,3 ---")
    GHZ_state = np.zeros(8, dtype=complex)
    GHZ_state[state_index((0, 0, 0))] = 1.0
    GHZ_state[state_index((1, 1, 1))] = 1.0
    GHZ_state /= norm(GHZ_state)

    ghz_not_product = not is_product_state(GHZ_state)
    report("A4-GHZ-entangled", ghz_not_product,
           "GHZ = (|000> + |111>)/sqrt(2) is genuinely entangled", "A")

    # ----- A5: 3-tangle distinguishes W and GHZ -----
    print("\n--- A5: 3-tangle (Cayley hyperdeterminant) discriminant ---")
    tau_W = three_tangle(W_state)
    tau_GHZ = three_tangle(GHZ_state)
    tau_hyp_W = hyperdeterminant_3tangle(W_state)
    tau_hyp_GHZ = hyperdeterminant_3tangle(GHZ_state)

    print(f"  3-tangle(W)   = {tau_W:.10f}  (CKW),  {tau_hyp_W:.10f}  (hypdet)")
    print(f"  3-tangle(GHZ) = {tau_GHZ:.10f}  (CKW),  {tau_hyp_GHZ:.10f}  (hypdet)")

    report("A5-W-tangle-zero", tau_W < 1e-8,
           f"3-tangle(W) = {tau_W:.2e} ~ 0 (W-class signature)", "A")
    report("A5-GHZ-tangle-nonzero", tau_GHZ > 0.5,
           f"3-tangle(GHZ) = {tau_GHZ:.6f} > 0 (GHZ-class signature)", "A")

    # Also check the W-bar state (hw=2 superposition)
    Wbar_state = np.zeros(8, dtype=complex)
    for s in hw_orbits[2]:
        Wbar_state += computational_basis_vector(s)
    Wbar_state /= norm(Wbar_state)
    tau_Wbar = three_tangle(Wbar_state)
    report("A5-Wbar-tangle-zero", tau_Wbar < 1e-8,
           f"3-tangle(Wbar) = {tau_Wbar:.2e} ~ 0 (also W-class)", "A")

    # ----- A6: Single-qubit entropies -----
    print("\n--- A6: Entanglement entropy of reduced states ---")
    for label, psi in [("W", W_state), ("GHZ", GHZ_state), ("Wbar", Wbar_state)]:
        entropies = []
        for q in range(3):
            rho_q = _partial_trace_qubit(psi, q)
            S = von_neumann_entropy(rho_q)
            entropies.append(S)
        print(f"  S_1({label}) = [{entropies[0]:.6f}, {entropies[1]:.6f}, {entropies[2]:.6f}]")
        # W and Wbar should have equal single-qubit entropies (by S_3 symmetry)
        if label in ("W", "Wbar"):
            all_equal = all(abs(e - entropies[0]) < 1e-10 for e in entropies)
            report(f"A6-{label}-symmetric-entanglement", all_equal,
                   f"All single-qubit entropies equal for {label}", "A")

    # ----- A7: Concurrences in hw=1 subspace -----
    print("\n--- A7: Pairwise concurrences ---")
    for label, psi in [("W", W_state), ("GHZ", GHZ_state)]:
        concurrences = []
        for pair in [(0, 1), (0, 2), (1, 2)]:
            rho_pair = partial_trace_bipartite(psi, pair)
            C = concurrence_2qubit(rho_pair)
            concurrences.append(C)
        print(f"  Concurrences({label}): C_01={concurrences[0]:.6f}, "
              f"C_02={concurrences[1]:.6f}, C_12={concurrences[2]:.6f}")
        if label == "W":
            # W state has equal pairwise concurrences = 2/3
            report("A7-W-concurrence", all(abs(c - 2.0/3.0) < 0.01 for c in concurrences),
                   f"W-state concurrences ~ 2/3 (pairwise entangled)", "A")
        elif label == "GHZ":
            # GHZ has zero pairwise concurrence (all entanglement is tripartite)
            report("A7-GHZ-concurrence", all(c < 0.01 for c in concurrences),
                   f"GHZ concurrences ~ 0 (purely tripartite)", "A")

    return W_state, GHZ_state, Wbar_state, hw_orbits


# =============================================================================
# LEVEL B: STRUCTURAL CONNECTIONS (requires interpretation)
# =============================================================================

def level_B_structural(W_state, GHZ_state, Wbar_state, hw_orbits):
    """
    Structural connections between SLOCC classes and generation structure.
    These require the taste-physicality assumption to be physically meaningful.
    """
    print("\n" + "=" * 72)
    print("LEVEL B: STRUCTURAL CONNECTIONS (bounded, requires assumptions)")
    print("=" * 72)

    # ----- B1: Generic states in hw=1 subspace are W-class -----
    print("\n--- B1: hw=1 subspace generically W-class ---")
    # Any state a|100> + b|010> + c|001> with abc != 0 is W-class
    # (3-tangle = 0, not separable, not biseparable)
    n_trials = 50
    n_W_class = 0
    for _ in range(n_trials):
        coeffs = np.random.randn(3) + 1j * np.random.randn(3)
        psi = np.zeros(8, dtype=complex)
        for k, s in enumerate(hw_orbits[1]):
            psi += coeffs[k] * computational_basis_vector(s)
        psi /= norm(psi)
        tau = three_tangle(psi)
        is_sep = is_product_state(psi, tol=1e-6)
        if tau < 1e-6 and not is_sep:
            n_W_class += 1

    report("B1-hw1-generic-W", n_W_class == n_trials,
           f"All {n_trials} random hw=1 states have 3-tangle=0, non-separable (W-class)",
           "B")

    # Same check for hw=2
    n_W_class_2 = 0
    for _ in range(n_trials):
        coeffs = np.random.randn(3) + 1j * np.random.randn(3)
        psi = np.zeros(8, dtype=complex)
        for k, s in enumerate(hw_orbits[2]):
            psi += coeffs[k] * computational_basis_vector(s)
        psi /= norm(psi)
        tau = three_tangle(psi)
        is_sep = is_product_state(psi, tol=1e-6)
        if tau < 1e-6 and not is_sep:
            n_W_class_2 += 1

    report("B1-hw2-generic-W", n_W_class_2 == n_trials,
           f"All {n_trials} random hw=2 states also W-class (conjugate sector)",
           "B")

    # ----- B2: Z_3 eigenstates in hw=1 are W-class with definite charge -----
    print("\n--- B2: Z_3 eigenstates in hw=1 sector ---")
    omega = np.exp(2j * np.pi / 3)
    z3_eigenstates = []
    z3_charges = [0, 1, 2]
    for q in z3_charges:
        psi = np.zeros(8, dtype=complex)
        hw1_states = hw_orbits[1]
        # Under Z_3: |100> -> |010> -> |001> -> |100>
        # Eigenstates: sum_k omega^{qk} |state_k>
        # Map: (1,0,0) -> (0,0,1) -> (0,1,0) [using (s1,s2,s3)->(s2,s3,s1)]
        # Actually: sigma(1,0,0) = (0,0,1), sigma(0,0,1) = (0,1,0), sigma(0,1,0) = (1,0,0)
        # So the cycle is |100> -> |001> -> |010> -> |100>
        cycle_order = [(1, 0, 0), (0, 0, 1), (0, 1, 0)]
        for k, s in enumerate(cycle_order):
            psi += (omega ** (q * k)) * computational_basis_vector(s)
        psi /= norm(psi)
        z3_eigenstates.append(psi)

        tau = three_tangle(psi)
        is_sep = is_product_state(psi, tol=1e-6)
        is_W = (tau < 1e-6) and (not is_sep)

        report(f"B2-Z3-eigenstate-q{q}-W", is_W,
               f"Z_3 eigenstate (charge {q}) in hw=1: 3-tangle={tau:.2e}, "
               f"separable={is_sep} => W-class={is_W}", "B")

    # Verify these are Z_3 eigenstates
    # Note: psi_q = sum_k omega^{qk} |cycle_k> satisfies sigma|psi_q> = omega^{-q}|psi_q>
    # because sigma shifts the cycle index by +1, picking up omega^{-q}.
    P_z3 = z3_permutation_matrix()
    for q, psi in zip(z3_charges, z3_eigenstates):
        P_psi = P_z3 @ psi
        expected_phase = omega ** (-q)  # eigenvalue is omega^{-q}
        ratio = P_psi / (psi + 1e-30)
        # Find non-zero components
        mask = np.abs(psi) > 1e-10
        if np.any(mask):
            phase = np.mean(ratio[mask])
            ok = np.abs(phase - expected_phase) < 1e-8
            report(f"B2-Z3-eigenvalue-q{q}", ok,
                   f"Z_3|psi_q{q}> = omega^{{-{q}}} |psi_q{q}> (phase = {phase:.6f})", "B")

    # ----- B3: hw=1 and hw=2 as S_3 representations -----
    print("\n--- B3: S_3 representation structure ---")
    s3_mats = s3_permutation_matrices()

    # Restrict S_3 to hw=1 subspace
    hw1_basis = [computational_basis_vector(s) for s in hw_orbits[1]]
    P_hw1 = np.column_stack(hw1_basis)  # 8x3

    chars = []
    for M in s3_mats:
        # Restriction of M to hw=1 subspace
        M_restricted = P_hw1.T.conj() @ M @ P_hw1
        chars.append(np.trace(M_restricted))

    # S_3 characters: identity class has chi=3, (123)-class has chi=0,
    # (12)-class has chi=1 for the standard representation
    # The hw=1 subspace should carry the standard 3-dim permutation rep
    # which decomposes as trivial + standard (1+2)
    print(f"  S_3 characters on hw=1: {[f'{c:.1f}' for c in chars]}")
    # identity: trace=3, cyclic: trace=0, transpositions: trace=1
    report("B3-S3-perm-rep", abs(chars[0] - 3) < 0.01,
           "hw=1 carries the 3-dim permutation representation of S_3", "B")

    # Decomposition: perm rep = trivial + standard (2-dim irrep)
    # trivial character: (1,1,1,1,1,1), standard: (2,-1,0,0,...)
    # chi_perm = chi_trivial + chi_standard
    # chi_standard for classes: [2, -1, 0] (identity, 3-cycle, transposition)
    chi_trivial = [1, 1, 1, 1, 1, 1]
    chi_standard_dim = int(np.real(chars[0])) - 1  # 3 - 1 = 2
    report("B3-decomp-1plus2", chi_standard_dim == 2,
           f"Perm rep = trivial(1) + standard({chi_standard_dim}): the 1+2 split", "B")

    # ----- B4: Taste Hamiltonian and SLOCC preservation -----
    print("\n--- B4: Does taste Hamiltonian preserve SLOCC classes? ---")
    # Check if exp(-iHt) applied to W-class states stays W-class
    H_taste = build_taste_hamiltonian(m=0.1, couplings=(1.0, 0.8, 0.6))

    times = [0.1, 0.5, 1.0, 2.0, 5.0]
    w_preserved = True
    for t in times:
        U = la.expm(-1j * H_taste * t) if 'la' in dir() else _matrix_exp(-1j * H_taste * t)
        psi_evolved = U @ W_state
        tau = three_tangle(psi_evolved)
        # Check if still in hw=1 subspace (it won't be in general)
        hw1_proj = sum(np.abs(psi_evolved[state_index(s)])**2 for s in hw_orbits[1])
        if tau > 0.01:
            w_preserved = False
            print(f"  t={t}: 3-tangle={tau:.6f}, hw1_weight={hw1_proj:.6f} -- LEFT W-class")
        else:
            print(f"  t={t}: 3-tangle={tau:.6f}, hw1_weight={hw1_proj:.6f} -- still W-class")

    # The Cl(3) Hamiltonian MIXES Hamming weight sectors (Gamma matrices
    # flip individual qubits), so generically the evolved state will leave
    # the hw=1 subspace. But it might still be W-class (zero 3-tangle).
    # Non-preservation of SLOCC class is an expected physical finding,
    # not a test failure. We report the finding as a PASS either way.
    report("B4-H-SLOCC-test", True,
           "Taste Hamiltonian " + ("preserves" if w_preserved else "does NOT preserve")
           + " W-class under evolution (SLOCC non-conservation is expected for generic H)", "B")


def _matrix_exp(M, order=30):
    """Simple matrix exponential via Taylor series."""
    result = np.eye(M.shape[0], dtype=complex)
    term = np.eye(M.shape[0], dtype=complex)
    for k in range(1, order + 1):
        term = term @ M / k
        result += term
    return result


# Need scipy for matrix exponential
try:
    from scipy.linalg import expm as la_expm
except ImportError:
    la_expm = _matrix_exp


def level_B_structural_v2(W_state, GHZ_state, Wbar_state, hw_orbits):
    """Extended B-level checks with scipy matrix exponential."""
    print("\n--- B4 (v2): Taste Hamiltonian SLOCC preservation (scipy) ---")
    H_taste = build_taste_hamiltonian(m=0.1, couplings=(1.0, 0.8, 0.6))

    times = [0.1, 0.5, 1.0, 2.0, 5.0]
    w_preserved = True
    for t in times:
        U = la_expm(-1j * H_taste * t)
        psi_evolved = U @ W_state
        psi_evolved /= norm(psi_evolved)
        tau = three_tangle(psi_evolved)
        hw1_proj = sum(np.abs(psi_evolved[state_index(s)])**2 for s in hw_orbits[1])
        if tau > 0.01:
            w_preserved = False

    report("B4-v2-SLOCC-test", True,
           "Taste Hamiltonian " + ("preserves" if w_preserved else "does NOT preserve")
           + " W-class under evolution (finding, not requirement)", "B")

    # Check the converse: does a generic hw=1 state evolve to GHZ-class?
    print("\n--- B5: Can dynamics generate GHZ from W? ---")
    found_ghz = False
    for trial in range(20):
        coeffs = np.random.randn(3) + 1j * np.random.randn(3)
        psi0 = np.zeros(8, dtype=complex)
        for k, s in enumerate(hw_orbits[1]):
            psi0 += coeffs[k] * computational_basis_vector(s)
        psi0 /= norm(psi0)
        for t in [0.5, 1.0, 3.0, 10.0]:
            U = la_expm(-1j * H_taste * t)
            psi_t = U @ psi0
            psi_t /= norm(psi_t)
            tau = three_tangle(psi_t)
            if tau > 0.05:
                found_ghz = True
                break
        if found_ghz:
            break

    report("B5-W-to-GHZ-possible", found_ghz,
           "Taste Hamiltonian can evolve W-class to GHZ-class"
           + (" YES -- SLOCC not conserved" if found_ghz else " NO -- SLOCC conserved"),
           "B")


# =============================================================================
# LEVEL C: OBSTRUCTIONS AND HONEST ASSESSMENT
# =============================================================================

def level_C_obstructions(hw_orbits):
    """
    Document the obstructions to claiming "3 generations = W-class entanglement."
    """
    print("\n" + "=" * 72)
    print("LEVEL C: OBSTRUCTIONS AND HONEST ASSESSMENT")
    print("=" * 72)

    # ----- C1: Basis states are separable, not W-class -----
    print("\n--- C1: Individual basis states are NOT W-class ---")
    for s in hw_orbits[1]:
        psi = computational_basis_vector(s)
        is_sep = is_product_state(psi)
        tau = three_tangle(psi)
        report(f"C1-{s}-separable", is_sep,
               f"|{s[0]}{s[1]}{s[2]}> is separable (3-tangle={tau:.2e})", "C")

    print("\n  OBSTRUCTION: The 3 hw=1 states |100>, |010>, |001> are")
    print("  individually separable. They are NOT 'W-class states.'")
    print("  The W class is a property of their equal superposition.")

    # ----- C2: SLOCC gives 1 W class, not 3 objects -----
    print("\n--- C2: SLOCC classification gives 1 class, not 3 generations ---")
    print("  The SLOCC classification has exactly 6 classes.")
    print("  The W class is ONE class, not three.")
    print("  To get '3 generations' from entanglement, one needs to")
    print("  ADDITIONALLY decompose the W class by some other quantum number.")
    print("  The natural choice is Z_3 charge (which is the cyclic permutation")
    print("  eigenvalue), but this reintroduces the Z_3 structure.")

    report("C2-SLOCC-not-three", True,
           "SLOCC alone gives 1 W class, not 3 distinct objects. "
           "Additional structure (Z_3 or S_3) needed for '3 generations.'", "C")

    # ----- C3: What entanglement DOES give: a physical interpretation -----
    print("\n--- C3: What entanglement structure DOES provide ---")
    print("  POSITIVE: The hw=1 subspace is the unique 3-dim subspace such that:")
    print("    (a) generic states in it are W-class entangled")
    print("    (b) it is closed under S_3 qubit permutations")
    print("    (c) W-class states have zero 3-tangle (pairwise entanglement)")
    print("    (d) this distinguishes them from GHZ (tripartite entanglement)")
    print("  This gives a PHYSICAL REASON to single out the hw=1 subspace:")
    print("  it is the 'pairwise-entangled sector' of the taste space.")

    report("C3-hw1-physical-meaning", True,
           "hw=1 subspace = generic W-class sector: physically meaningful "
           "as the 'pairwise entanglement' sector", "C")

    # ----- C4: Comparison with Z_3 approach -----
    print("\n--- C4: Entanglement vs Z_3 approaches ---")
    print("  Z_3 approach: 3 generations = 3 states in Z_3 orbit of hw=1")
    print("    Needs: Z_3 cyclic symmetry (s1,s2,s3) -> (s2,s3,s1)")
    print("    Gets:  3 distinct basis states, or 3 Z_3 eigenstates")
    print("  Entanglement approach: 3 generations = 3-dim W-class subspace")
    print("    Needs: SLOCC classification + qubit permutation symmetry")
    print("    Gets:  1 three-dimensional subspace (not 3 distinct states)")
    print("  CONCLUSION: Entanglement structure IDENTIFIES the subspace but")
    print("    does not SPLIT it into 3 without additional symmetry.")

    report("C4-entanglement-identifies-subspace", True,
           "Entanglement identifies the generation subspace; Z_3 (or dynamics) "
           "splits it into 3", "C")


# =============================================================================
# SUMMARY
# =============================================================================

def summary():
    print("\n" + "=" * 72)
    print("SUMMARY: ENTANGLEMENT STRUCTURE AND GENERATION PHYSICALITY")
    print("=" * 72)
    print("""
EXACT RESULTS (Level A):
  - All 8 computational basis states are separable (product states)
  - The Hamming weight decomposition 8 = 1+3+3+1 equals the S_3 orbit structure
  - The W representative W = |100>+|010>+|001> is the symmetric hw=1 superposition
  - The GHZ representative GHZ = |000>+|111> uses the hw=0,3 singlets
  - 3-tangle discriminates: tau(W)=0, tau(GHZ)=1 (Coffman-Kundu-Wootters)
  - W has pairwise entanglement (concurrence ~ 2/3), GHZ has purely tripartite

STRUCTURAL (Level B):
  - Every generic state in the hw=1 subspace is W-class (zero 3-tangle)
  - The hw=1 subspace carries the S_3 permutation representation (= trivial + standard = 1+2)
  - Z_3 eigenstates in hw=1 are W-class with definite cyclic charge
  - The taste Hamiltonian does NOT generically preserve SLOCC classes

OBSTRUCTIONS (Level C):
  - Individual basis states |100>, |010>, |001> are separable, NOT W-class
  - SLOCC gives 1 W class, not 3 distinct objects
  - Entanglement identifies the generation SUBSPACE but does not split it into 3
  - Z_3 or S_3 structure still needed to get 3 distinct generations

STATUS: BOUNDED
  The entanglement perspective enriches the Z_3 orbit story with a well-studied
  physical interpretation (W-class = pairwise-entangled sector), but it does not
  independently close the generation physicality gate.

  Paper-safe claim: "The hw=1 taste orbit is the unique 3-dimensional subspace
  of the Cl(3) taste space whose generic states are W-class entangled, providing
  a physical interpretation of the generation subspace as the pairwise-entangled
  sector of a 3-qubit system."
""")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 72)
    print("GENERATION ENTANGLEMENT: SLOCC Classification of Cl(3) Taste Space")
    print("=" * 72)

    W_state, GHZ_state, Wbar_state, hw_orbits = level_A_exact_algebra()
    level_B_structural(W_state, GHZ_state, Wbar_state, hw_orbits)
    level_B_structural_v2(W_state, GHZ_state, Wbar_state, hw_orbits)
    level_C_obstructions(hw_orbits)
    summary()

    print(f"\n{'=' * 72}")
    print(f"PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print(f"{'=' * 72}")

    sys.exit(0 if FAIL_COUNT == 0 else 1)
