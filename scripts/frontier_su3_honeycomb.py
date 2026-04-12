#!/usr/bin/env python3
"""
SU(3) from Honeycomb/3-Sublattice Lattice
==========================================

QUESTION: Does a lattice with 3 sublattices (A, B, C) produce SU(3)
gauge structure through the staggered fermion mechanism?

APPROACH:
1. Build several 3-sublattice lattices:
   a) 2D honeycomb extended to 3D (graphene layers)
   b) Kagome lattice (corner-sharing triangles)
   c) Cubic lattice with 3-site unit cell
2. Build the staggered Hamiltonian on each lattice.
3. The 3-sublattice structure means the hopping matrices are 3x3 in
   sublattice space. Check if they generate su(3).

CONTEXT: The honeycomb lattice is NOT 3-colorable -- it's bipartite
(2-colorable with A and B sublattices). But the kagome lattice IS
3-colorable. And a cubic lattice with a 3-site basis naturally has
3 sublattices.

The key insight: on a lattice with N_sub sublattices, the hopping
operator in momentum space becomes an N_sub x N_sub matrix H(k).
If N_sub = 3, this is a 3x3 matrix, and its algebra of generators
could be su(3).

Self-contained: numpy + scipy only.
"""

import sys
import time
import numpy as np
from scipy import sparse

np.set_printoptions(precision=6, linewidth=120)

# Gell-Mann matrices
GELLMANN = []
GELLMANN.append(np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
GELLMANN.append(np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex))
GELLMANN.append(np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3))


def gellmann_overlap(M):
    """Compute overlap of a 3x3 matrix with each Gell-Mann matrix."""
    overlaps = []
    for lam in GELLMANN:
        ov = abs(np.trace(M.conj().T @ lam)) / max(np.linalg.norm(M, 'fro') * np.linalg.norm(lam, 'fro'), 1e-30)
        overlaps.append(ov)
    return np.array(overlaps)


def gellmann_decompose(M):
    """Decompose a traceless Hermitian 3x3 matrix in the Gell-Mann basis."""
    coeffs = []
    for lam in GELLMANN:
        # c_a = (1/2) Tr(lambda_a M)  for standard normalization Tr(lambda_a lambda_b) = 2 delta_ab
        c = 0.5 * np.trace(lam @ M).real
        coeffs.append(c)
    return np.array(coeffs)


# ============================================================================
# Lattice 1: Kagome lattice (2D, 3 sublattices)
# ============================================================================

def build_kagome_bloch(kx, ky):
    """
    Build the Bloch Hamiltonian H(k) for the kagome lattice.

    The kagome lattice has 3 sites per unit cell. The hopping Hamiltonian
    in momentum space is a 3x3 matrix.

    Basis vectors: a1 = (1, 0), a2 = (1/2, sqrt(3)/2)
    Sublattice positions:
      A = (0, 0)
      B = (1/2, 0)
      C = (1/4, sqrt(3)/4)

    Nearest-neighbor hopping t = 1:
    H(k) = [[0, h_AB, h_AC],
             [h_AB*, 0, h_BC],
             [h_AC*, h_BC*, 0]]
    """
    # Phase factors for kagome
    # A-B bond along a1/2
    phi_AB = np.exp(1j * kx / 2)
    # A-C bond along (a1+a2)/4 direction
    phi_AC = np.exp(1j * (kx / 4 + ky * np.sqrt(3) / 4))
    # B-C bond
    phi_BC = np.exp(1j * (-kx / 4 + ky * np.sqrt(3) / 4))

    H = np.zeros((3, 3), dtype=complex)
    H[0, 1] = -1 * (phi_AB + phi_AB.conj())  # A-B
    H[0, 2] = -1 * (phi_AC + phi_AC.conj())  # A-C
    H[1, 2] = -1 * (phi_BC + phi_BC.conj())  # B-C
    H = H + H.conj().T

    return H


def test_kagome_su3():
    """
    Check if the kagome Bloch Hamiltonian H(k) generates su(3) as k varies.

    If the set {H(k) : k in BZ} spans all of su(3), then the lattice
    naturally produces SU(3) gauge structure.
    """
    print("\n" + "=" * 60)
    print("LATTICE 1: Kagome lattice (2D, 3 sublattices)")
    print("=" * 60)

    # Sample H(k) at many k-points
    nk = 20
    kx_vals = np.linspace(-np.pi, np.pi, nk)
    ky_vals = np.linspace(-np.pi, np.pi, nk)

    all_H = []
    for kx in kx_vals:
        for ky in ky_vals:
            H = build_kagome_bloch(kx, ky)
            all_H.append(H)

    print(f"  Sampled {len(all_H)} k-points")

    # Extract traceless Hermitian parts
    generators = []
    for H in all_H:
        tr = np.trace(H) / 3
        H_tl = H - tr * np.eye(3)
        if np.linalg.norm(H_tl) > 0.01:
            H_tl = H_tl / np.linalg.norm(H_tl)
            generators.append(H_tl)

    # Find independent generators
    independent = []
    for g in generators:
        residual = g.copy()
        for b in independent:
            ov = np.trace(b.conj().T @ residual) / np.trace(b.conj().T @ b).real
            residual = residual - ov * b
        if np.linalg.norm(residual) > 0.1:
            residual = residual / np.linalg.norm(residual)
            independent.append(residual)

    print(f"  Independent traceless Hermitian generators: {len(independent)}")
    print(f"  su(3) needs 8 generators")

    # Check which Gell-Mann directions are covered
    gm_covered = 0
    print("\n  Gell-Mann overlap:")
    for j, lam in enumerate(GELLMANN):
        max_ov = 0
        for g in independent:
            ov = abs(np.trace(g.conj().T @ lam)) / (np.linalg.norm(g, 'fro') * np.linalg.norm(lam, 'fro'))
            max_ov = max(max_ov, ov)
        covered = max_ov > 0.3
        if covered:
            gm_covered += 1
        print(f"    lambda_{j+1}: max overlap = {max_ov:.4f} {'[COVERED]' if covered else ''}")

    print(f"  Gell-Mann directions covered: {gm_covered}/8")

    # Check commutator closure
    print("\n  Commutator closure of kagome Bloch Hamiltonians:")
    # Start with a few representative H(k) and check if commutators
    # generate new independent directions
    seed_ks = [(0, 0), (np.pi, 0), (0, np.pi), (np.pi/2, np.pi/3),
               (2*np.pi/3, 2*np.pi/3)]
    basis = []
    for kx, ky in seed_ks:
        H = build_kagome_bloch(kx, ky)
        tr = np.trace(H) / 3
        H_tl = H - tr * np.eye(3)
        if np.linalg.norm(H_tl) > 0.01:
            H_tl = H_tl / np.linalg.norm(H_tl)
            basis.append(H_tl)

    for iteration in range(5):
        new_els = []
        current = len(basis)
        for i in range(current):
            for j in range(i + 1, current):
                comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                cn = np.linalg.norm(comm)
                if cn < 1e-10:
                    continue
                comm_h = 1j * comm / cn  # Make Hermitian

                residual = comm_h.copy()
                for b in basis + new_els:
                    bn = np.trace(b.conj().T @ b).real
                    if bn < 1e-10:
                        continue
                    ov = np.trace(b.conj().T @ residual) / bn
                    residual = residual - ov * b

                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    new_els.append(residual)

        if not new_els:
            break
        basis.extend(new_els)

    algebra_dim = len(basis)
    print(f"  Algebra dimension from commutator closure: {algebra_dim}")
    if algebra_dim == 8:
        print("  MATCH: dimension 8 = su(3)!")
    elif algebra_dim == 3:
        print("  MATCH: dimension 3 = su(2)")

    # Verify su(3) structure constants
    if algebra_dim >= 8:
        print("\n  Verifying su(3) structure constants:")
        # Compute [g_i, g_j] and check if it's a linear combination of g_k
        max_residual = 0
        for i in range(min(algebra_dim, 8)):
            for j in range(i + 1, min(algebra_dim, 8)):
                comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                # Project onto basis
                residual = comm.copy()
                for b in basis:
                    bn = np.trace(b.conj().T @ b).real
                    if bn < 1e-10:
                        continue
                    ov = np.trace(b.conj().T @ residual) / bn
                    residual = residual - ov * b
                res_norm = np.linalg.norm(residual) / max(np.linalg.norm(comm), 1e-30)
                max_residual = max(max_residual, res_norm)
        print(f"  Max residual in structure constants: {max_residual:.6f}")
        print(f"  Lie algebra closure: {'YES' if max_residual < 0.1 else 'NO'}")

    return gm_covered, algebra_dim


# ============================================================================
# Lattice 2: Cubic with 3-site basis (ABC stacking)
# ============================================================================

def build_abc_cubic_bloch(kx, ky, kz):
    """
    Build Bloch Hamiltonian for a cubic lattice with 3-site unit cell.

    This is a 1D chain of A-B-C-A-B-C-... extended to 3D.
    In the z-direction, we have the 3-sublattice structure.
    In x and y directions, standard cubic hopping.

    The 3x3 sublattice Hamiltonian at momentum k is:
    H(k) = h_z(kz) + h_xy(kx, ky)

    where h_z is the ABC chain hopping and h_xy is diagonal.
    """
    omega = np.exp(2j * np.pi / 3)

    # z-direction: A-B-C chain with Bloch phase
    # Hopping A->B (within cell), B->C (within cell), C->A (next cell)
    H = np.zeros((3, 3), dtype=complex)

    # Nearest-neighbor hopping in z (ABC chain)
    H[0, 1] = -1  # A -> B
    H[1, 2] = -1  # B -> C
    H[2, 0] = -np.exp(1j * kz)  # C -> A (next cell)
    H = H + H.conj().T

    # x and y hopping (same sublattice to same sublattice)
    diag_xy = -2 * (np.cos(kx) + np.cos(ky))
    H += diag_xy * np.eye(3)

    return H


def test_abc_cubic_su3():
    """
    Check if the ABC cubic lattice's Bloch Hamiltonian generates su(3).
    """
    print("\n" + "=" * 60)
    print("LATTICE 2: Cubic with 3-site basis (ABC stacking)")
    print("=" * 60)

    nk = 15
    k_vals = np.linspace(-np.pi, np.pi, nk)

    # Sample H(k) across the Brillouin zone
    all_H = []
    for kx in k_vals:
        for ky in k_vals:
            for kz in k_vals:
                H = build_abc_cubic_bloch(kx, ky, kz)
                all_H.append(H)

    print(f"  Sampled {len(all_H)} k-points")

    # Extract traceless Hermitian parts
    independent = []
    for H in all_H:
        tr = np.trace(H) / 3
        H_tl = H - tr * np.eye(3)
        if np.linalg.norm(H_tl) < 0.01:
            continue
        H_tl = H_tl / np.linalg.norm(H_tl)

        residual = H_tl.copy()
        for b in independent:
            ov = np.trace(b.conj().T @ residual) / np.trace(b.conj().T @ b).real
            residual = residual - ov * b
        if np.linalg.norm(residual) > 0.1:
            residual = residual / np.linalg.norm(residual)
            independent.append(residual)

    print(f"  Independent traceless Hermitian generators: {len(independent)}")

    # Commutator closure
    basis = list(independent[:min(len(independent), 8)])
    for iteration in range(5):
        new_els = []
        current = len(basis)
        for i in range(current):
            for j in range(i + 1, current):
                comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                cn = np.linalg.norm(comm)
                if cn < 1e-10:
                    continue
                comm_h = 1j * comm / cn

                residual = comm_h.copy()
                for b in basis + new_els:
                    bn = np.trace(b.conj().T @ b).real
                    if bn < 1e-10:
                        continue
                    ov = np.trace(b.conj().T @ residual) / bn
                    residual = residual - ov * b

                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    new_els.append(residual)

        if not new_els:
            break
        basis.extend(new_els)

    algebra_dim = len(basis)
    print(f"  Algebra dimension from commutator closure: {algebra_dim}")

    # Gell-Mann coverage
    gm_covered = 0
    for j, lam in enumerate(GELLMANN):
        max_ov = 0
        for g in basis:
            ov = abs(np.trace(g.conj().T @ lam)) / (np.linalg.norm(g, 'fro') * np.linalg.norm(lam, 'fro'))
            max_ov = max(max_ov, ov)
        if max_ov > 0.3:
            gm_covered += 1
    print(f"  Gell-Mann directions covered: {gm_covered}/8")

    return gm_covered, algebra_dim


# ============================================================================
# Lattice 3: Staggered Z_3 on cubic lattice
# ============================================================================

def test_staggered_z3_su3():
    """
    Build a staggered fermion Hamiltonian with Z_3 phases on a cubic lattice
    with a 3-site unit cell. Check the 3x3 sublattice structure.

    The staggered phase eta_mu depends on the sublattice assignment.
    With 3 sublattices, eta_mu(x) = omega^{f_mu(sublattice(x))}
    where f_mu assigns a Z_3 phase per direction and sublattice.
    """
    print("\n" + "=" * 60)
    print("LATTICE 3: Staggered Z_3 fermions on 3-sublattice cubic")
    print("=" * 60)

    omega = np.exp(2j * np.pi / 3)

    # Momentum-space Hamiltonian for staggered Z_3 fermions
    # The 3x3 matrix at momentum k:
    # H(k) = sum_mu [ eta_mu * T_mu * e^{i k_mu} + h.c. ]
    # where T_mu are 3x3 hopping matrices with Z_3 structure

    # Direction x: T_x = diag(1, omega, omega^2)  (clock matrix)
    T_x = np.diag([1, omega, omega**2])

    # Direction y: T_y = permutation matrix (shift)
    T_y = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)

    # Direction z: T_z = T_x @ T_y (combination)
    T_z = T_x @ T_y

    T_mu = [T_x, T_y, T_z]

    print("  Hopping matrices per direction:")
    for mu, (T, lab) in enumerate(zip(T_mu, ["T_x", "T_y", "T_z"])):
        print(f"    {lab}:")
        print(f"      {T[0]}")
        print(f"      {T[1]}")
        print(f"      {T[2]}")

    # Sample Bloch Hamiltonian
    nk = 15
    k_vals = np.linspace(-np.pi, np.pi, nk)

    independent = []
    for kx in k_vals:
        for ky in k_vals:
            for kz in k_vals:
                H = np.zeros((3, 3), dtype=complex)
                for mu, (T, k) in enumerate(zip(T_mu, [kx, ky, kz])):
                    H += T * np.exp(1j * k) + T.conj().T * np.exp(-1j * k)

                tr = np.trace(H) / 3
                H_tl = H - tr * np.eye(3)
                # Make Hermitian
                H_tl = (H_tl + H_tl.conj().T) / 2
                if np.linalg.norm(H_tl) < 0.01:
                    continue
                H_tl = H_tl / np.linalg.norm(H_tl)

                residual = H_tl.copy()
                for b in independent:
                    ov = np.trace(b.conj().T @ residual) / np.trace(b.conj().T @ b).real
                    residual = residual - ov * b
                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    independent.append(residual)

    print(f"\n  Independent generators from H(k): {len(independent)}")

    # Also add anti-Hermitian parts of H(k)
    for kx in k_vals[::3]:
        for ky in k_vals[::3]:
            for kz in k_vals[::3]:
                H = np.zeros((3, 3), dtype=complex)
                for mu, (T, k) in enumerate(zip(T_mu, [kx, ky, kz])):
                    H += T * np.exp(1j * k) + T.conj().T * np.exp(-1j * k)
                # Anti-Hermitian part -> Hermitian generator
                ah = (H - H.conj().T) / (2j)
                tr = np.trace(ah) / 3
                ah_tl = ah - tr * np.eye(3)
                if np.linalg.norm(ah_tl) < 0.01:
                    continue
                ah_tl = ah_tl / np.linalg.norm(ah_tl)

                residual = ah_tl.copy()
                for b in independent:
                    ov = np.trace(b.conj().T @ residual) / np.trace(b.conj().T @ b).real
                    residual = residual - ov * b
                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    independent.append(residual)

    print(f"  After adding anti-Hermitian parts: {len(independent)}")

    # Commutator closure
    basis = list(independent[:min(len(independent), 10)])
    for iteration in range(5):
        new_els = []
        current = len(basis)
        for i in range(current):
            for j in range(i + 1, current):
                comm = basis[i] @ basis[j] - basis[j] @ basis[i]
                cn = np.linalg.norm(comm)
                if cn < 1e-10:
                    continue
                comm_h = 1j * comm / cn

                residual = comm_h.copy()
                for b in basis + new_els:
                    bn = np.trace(b.conj().T @ b).real
                    if bn < 1e-10:
                        continue
                    ov = np.trace(b.conj().T @ residual) / bn
                    residual = residual - ov * b

                if np.linalg.norm(residual) > 0.1:
                    residual = residual / np.linalg.norm(residual)
                    new_els.append(residual)

        if not new_els:
            break
        basis.extend(new_els)

    algebra_dim = len(basis)
    print(f"  Algebra dimension from commutator closure: {algebra_dim}")

    # Gell-Mann coverage
    gm_covered = 0
    print("\n  Gell-Mann overlap:")
    for j, lam in enumerate(GELLMANN):
        max_ov = 0
        for g in basis:
            ov = abs(np.trace(g.conj().T @ lam)) / (np.linalg.norm(g, 'fro') * np.linalg.norm(lam, 'fro'))
            max_ov = max(max_ov, ov)
        covered = max_ov > 0.3
        if covered:
            gm_covered += 1
        print(f"    lambda_{j+1}: max overlap = {max_ov:.4f} {'[COVERED]' if covered else ''}")
    print(f"  Gell-Mann directions covered: {gm_covered}/8")

    # Decompose generators in Gell-Mann basis
    print("\n  Generator decomposition in Gell-Mann basis:")
    for i, g in enumerate(basis[:min(len(basis), 8)]):
        coeffs = gellmann_decompose(g * np.linalg.norm(g, 'fro'))
        nonzero = [(j+1, c) for j, c in enumerate(coeffs) if abs(c) > 0.01]
        desc = " + ".join([f"{c:.3f}*L{j}" for j, c in nonzero])
        print(f"    g_{i}: {desc}")

    return gm_covered, algebra_dim


def main():
    t0 = time.time()

    print("=" * 80)
    print("SU(3) FROM HONEYCOMB / 3-SUBLATTICE LATTICES")
    print("=" * 80)

    # Test 1: Kagome
    gm_kagome, dim_kagome = test_kagome_su3()

    # Test 2: ABC cubic
    gm_abc, dim_abc = test_abc_cubic_su3()

    # Test 3: Staggered Z_3
    gm_z3, dim_z3 = test_staggered_z3_su3()

    # ---- VERDICT ----
    print(f"\n{'='*80}")
    print("VERDICT")
    print(f"{'='*80}")

    elapsed = time.time() - t0

    print(f"""
  SUMMARY TABLE:
  +--------------------------+---------+----------+---------+
  | Lattice                  | Algebra | Gell-Mann| su(3)?  |
  |                          | dim     | covered  |         |
  +--------------------------+---------+----------+---------+
  | Kagome (2D, 3-sublatt)   | {dim_kagome:>7} | {gm_kagome:>5}/8   | {'YES' if dim_kagome == 8 else 'NO':>7} |
  | ABC cubic (3-sublatt)    | {dim_abc:>7} | {gm_abc:>5}/8   | {'YES' if dim_abc == 8 else 'NO':>7} |
  | Staggered Z_3 (cubic)    | {dim_z3:>7} | {gm_z3:>5}/8   | {'YES' if dim_z3 == 8 else 'NO':>7} |
  +--------------------------+---------+----------+---------+

  KEY FINDINGS:

  1. KAGOME LATTICE (2D): The Bloch Hamiltonian H(k) on the kagome lattice
     is a 3x3 matrix. As k varies over the Brillouin zone, H(k) traces out
     a submanifold of the space of 3x3 Hermitian matrices. The algebra
     generated has dimension {dim_kagome}.
     {'This IS su(3)!' if dim_kagome == 8 else 'This is NOT su(3).' if dim_kagome < 8 else ''}

  2. ABC CUBIC LATTICE: The 3-sublattice cubic lattice in 3D has a 3x3
     Bloch Hamiltonian. The algebra generated has dimension {dim_abc}.
     {'This IS su(3)!' if dim_abc == 8 else 'This is NOT su(3).' if dim_abc < 8 else ''}

  3. STAGGERED Z_3: Using Z_3 phases (clock and shift matrices) as the
     hopping matrices produces an algebra of dimension {dim_z3}.
     {'This IS su(3)!' if dim_z3 == 8 else 'This is NOT su(3).' if dim_z3 < 8 else ''}

  INTERPRETATION:
  - Any lattice with a 3-site unit cell has a 3x3 Bloch Hamiltonian.
  - The question is whether the SPECIFIC form of H(k) spans all 8
    dimensions of su(3), or only a subalgebra.
  - The staggered Z_3 construction (using clock and shift matrices as
    hopping operators) is the most promising, because clock-shift
    generates all of gl(3), and their traceless Hermitian combinations
    span su(3).

  BOTTOM LINE: The 3-sublattice structure provides the 3x3 matrix space
  needed for su(3). Whether the FULL su(3) is generated depends on the
  hopping matrices having enough structure (at least 2 non-commuting
  3x3 matrices that together span 8 dimensions).

  Time: {elapsed:.1f}s
""")


if __name__ == "__main__":
    main()
