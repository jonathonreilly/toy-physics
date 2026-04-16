#!/usr/bin/env python3
"""
Bell inequality (CHSH) violation from the local tensor product axiom.

The framework axiom (SINGLE_AXIOM_HILBERT_NOTE): a local tensor product
Hilbert space H = H_1 x H_2 x ... x H_N. The graph emerges from the
Hamiltonian's support on neighboring factors. Unitarity and the Born rule
are automatic.

Bell test construction:
  - Alice owns sites {0, 1} (one even-odd pair). Her local Hilbert space
    is H_0 x H_1, dimension 2x2 = 4.
  - Bob owns sites {2, 3} (one even-odd pair). His local Hilbert space
    is H_2 x H_3, dimension 2x2 = 4.
  - [O_A, O_B] = 0 is AUTOMATIC from the tensor product structure.
    Alice's operators act on factors 0,1; Bob's on factors 2,3. They
    commute by construction.
  - Alice's qubit: the sublattice Pauli algebra on her pair (Z_A, X_A).
  - Bob's qubit: the sublattice Pauli algebra on his pair (Z_B, X_B).
  - In the fixed-particle-number sector, cross-boundary hopping is
    excluded (fermions stay in their party's region). The ONLY coupling
    between Alice and Bob is the Poisson gravitational interaction.
  - At G=0, |S| = 2.000 exactly (classical bound, no violation).
  - At G>0, the Poisson coupling creates entanglement -> |S| > 2.

Protocol:
  1. Prepare a product state (one fermion per party, each on even site)
  2. Evolve under the staggered Hamiltonian with gravitational coupling
  3. At each time step, measure CHSH using Alice's and Bob's LOCAL
     Pauli operators
  4. The entanglement is created by the framework's own dynamics

PStack experiment: frontier-bell-inequality
"""

from __future__ import annotations
import math, time
import numpy as np
from scipy.linalg import eigh, expm


# ====================================================================
# 4-site minimal Bell lattice
# ====================================================================
# Sites: 0 (even) -- 1 (odd) -- 2 (even) -- 3 (odd)
# Alice: {0, 1}, Bob: {2, 3}
# Periodic BC: also 3 -- 0 link
#
# The single-particle Hilbert space is C^4.
# For 2 distinguishable fermions (one on Alice, one on Bob), the joint
# space is C^4 x C^4 = C^16, restricted to the sector with exactly
# 1 fermion on Alice's sites and 1 on Bob's sites (dimension 4).
#
# Alice's qubit: her fermion on site 0 (even, |0>) or site 1 (odd, |1>)
# Bob's qubit: his fermion on site 2 (even, |0>) or site 3 (odd, |1>)

N_SITES = 4


def staggered_hamiltonian_1p(n=N_SITES, t_hop=1.0, mass=0.5, periodic=True):
    """Single-particle staggered Hamiltonian."""
    H = np.zeros((n, n), dtype=complex)
    for i in range(n - 1):
        H[i, i + 1] = -t_hop
        H[i + 1, i] = -t_hop
    if periodic:
        H[0, n - 1] = -t_hop
        H[n - 1, 0] = -t_hop
    for i in range(n):
        H[i, i] = mass * (1.0 if i % 2 == 0 else -1.0)
    return H


def poisson_greens_periodic(n=N_SITES):
    """Periodic Poisson Green's function on a 1D ring.
    Solves -nabla^2 G = delta - 1/N with periodic BC.
    """
    # Eigenvalues of the 1D periodic Laplacian: lambda_k = 2 - 2*cos(2*pi*k/N)
    # G(x) = (1/N) sum_{k!=0} exp(2pi i k x / N) / lambda_k
    G = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            val = 0.0
            for k in range(1, n):
                lam_k = 2.0 - 2.0 * math.cos(2.0 * math.pi * k / n)
                val += math.cos(2.0 * math.pi * k * (i - j) / n) / lam_k
            G[i, j] = val / n
    return G


# ====================================================================
# 2-fermion Hamiltonian in the Alice-1-Bob-1 sector
# ====================================================================

def build_sector_hamiltonian(H1, V_poisson, G_grav,
                             alice_sites=(0, 1), bob_sites=(2, 3)):
    """Build the 2-particle Hamiltonian restricted to the sector where
    Alice has exactly 1 fermion and Bob has exactly 1 fermion.

    Sector basis: (a, b) for a in alice_sites, b in bob_sites.
    Dimension: len(alice) * len(bob) = 4.

    The tensor product factorization H_Alice x H_Bob is manifest:
    Alice's operators act on index a, Bob's on index b.
    [O_A, O_B] = 0 by construction.
    """
    a_sites = list(alice_sites)
    b_sites = list(bob_sites)
    dim = len(a_sites) * len(b_sites)
    sector = [(a, b) for a in a_sites for b in b_sites]
    sector_idx = {(a, b): k for k, (a, b) in enumerate(sector)}

    H2 = np.zeros((dim, dim), dtype=complex)

    for k, (a, b) in enumerate(sector):
        # Diagonal: single-particle energies + interaction
        H2[k, k] = H1[a, a] + H1[b, b] + G_grav * V_poisson[a, b]

        # Alice's fermion hops: a -> a' (Bob stays at b)
        for ap in a_sites:
            if ap != a and abs(H1[a, ap]) > 1e-15:
                H2[k, sector_idx[(ap, b)]] += H1[a, ap]

        # Bob's fermion hops: b -> b' (Alice stays at a)
        for bp in b_sites:
            if bp != b and abs(H1[b, bp]) > 1e-15:
                H2[k, sector_idx[(a, bp)]] += H1[b, bp]

    return H2, sector


def build_local_paulis(alice_sites, bob_sites, sector):
    """Build Alice's and Bob's local Pauli operators in the sector basis.

    Alice's Z: sublattice parity of her fermion's site
    Alice's X: hop between her even and odd sites
    Bob's Z, X: same for his sites

    These operators act on DIFFERENT tensor factors and commute
    by construction: [O_A, O_B] = 0.
    """
    dim = len(sector)
    sector_idx = {(a, b): k for k, (a, b) in enumerate(sector)}
    a_sites = list(alice_sites)
    b_sites = list(bob_sites)

    # Alice's Z: (-1)^a
    Z_A = np.zeros((dim, dim), dtype=complex)
    for k, (a, b) in enumerate(sector):
        Z_A[k, k] = 1.0 if a % 2 == 0 else -1.0

    # Alice's X: hop between her sites
    X_A = np.zeros((dim, dim), dtype=complex)
    for k1, (a1, b1) in enumerate(sector):
        for k2, (a2, b2) in enumerate(sector):
            if b1 == b2 and a1 != a2 and a1 in a_sites and a2 in a_sites:
                if abs(a1 - a2) == 1 or abs(a1 - a2) == max(a_sites) - min(a_sites):
                    X_A[k1, k2] = 1.0

    # Bob's Z: (-1)^b
    Z_B = np.zeros((dim, dim), dtype=complex)
    for k, (a, b) in enumerate(sector):
        Z_B[k, k] = 1.0 if b % 2 == 0 else -1.0

    # Bob's X: hop between his sites
    X_B = np.zeros((dim, dim), dtype=complex)
    for k1, (a1, b1) in enumerate(sector):
        for k2, (a2, b2) in enumerate(sector):
            if a1 == a2 and b1 != b2 and b1 in b_sites and b2 in b_sites:
                if abs(b1 - b2) == 1 or abs(b1 - b2) == max(b_sites) - min(b_sites):
                    X_B[k1, k2] = 1.0

    return Z_A, X_A, Z_B, X_B


# ====================================================================
# CHSH computation
# ====================================================================

def compute_chsh(psi, Z_A, X_A, Z_B, X_B):
    """Compute optimal CHSH using the Horodecki formula.

    Build the 3x3 correlation matrix T_ij = <psi| sigma_i^A sigma_j^B |psi>
    then S_max = 2*sqrt(lambda_1 + lambda_2) where lambda_i are the two
    largest eigenvalues of T^T T.
    """
    Y_A = 1j * Z_A @ X_A
    Y_B = 1j * Z_B @ X_B
    ops_A = [Z_A, X_A, Y_A]
    ops_B = [Z_B, X_B, Y_B]

    T = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            T[i, j] = np.real(psi.conj() @ (ops_A[i] @ ops_B[j]) @ psi)

    TTT = T.T @ T
    evals = sorted(np.linalg.eigvalsh(TTT), reverse=True)
    S_max = 2 * math.sqrt(max(evals[0] + evals[1], 0))
    return S_max, T


# ====================================================================
# Part 1: Verify local structure
# ====================================================================

def part_1():
    print("=" * 72)
    print("PART 1: LOCAL TENSOR PRODUCT STRUCTURE")
    print("=" * 72)
    print()
    print("Framework axiom: local tensor product H = H_0 x H_1 x H_2 x H_3")
    print("Alice: factors {0, 1}. Bob: factors {2, 3}.")
    print("[O_A, O_B] = 0 by tensor product construction.")
    print()

    alice = (0, 1)
    bob = (2, 3)
    sector = [(a, b) for a in alice for b in bob]
    Z_A, X_A, Z_B, X_B = build_local_paulis(alice, bob, sector)

    # Verify Pauli algebra
    I4 = np.eye(4)
    print("  Alice Pauli algebra:")
    print(f"    Z_A^2 = I: {np.allclose(Z_A @ Z_A, I4)}")
    print(f"    X_A^2 = I: {np.allclose(X_A @ X_A, I4)}")
    print(f"    {{Z_A, X_A}} = 0: {np.allclose(Z_A @ X_A + X_A @ Z_A, 0)}")

    print(f"  Bob Pauli algebra:")
    print(f"    Z_B^2 = I: {np.allclose(Z_B @ Z_B, I4)}")
    print(f"    X_B^2 = I: {np.allclose(X_B @ X_B, I4)}")
    print(f"    {{Z_B, X_B}} = 0: {np.allclose(Z_B @ X_B + X_B @ Z_B, 0)}")

    print(f"  Commutation [O_A, O_B] = 0:")
    print(f"    [Z_A, Z_B] = 0: {np.allclose(Z_A @ Z_B, Z_B @ Z_A)}")
    print(f"    [Z_A, X_B] = 0: {np.allclose(Z_A @ X_B, X_B @ Z_A)}")
    print(f"    [X_A, Z_B] = 0: {np.allclose(X_A @ Z_B, Z_B @ X_A)}")
    print(f"    [X_A, X_B] = 0: {np.allclose(X_A @ X_B, X_B @ X_A)}")


# ====================================================================
# Part 2: Dynamical Bell violation
# ====================================================================

def part_2():
    print()
    print("=" * 72)
    print("PART 2: DYNAMICAL BELL VIOLATION")
    print("=" * 72)
    print()
    print("Product initial state -> evolve under H with gravity -> measure CHSH")
    print()

    alice = (0, 1)
    bob = (2, 3)
    sector = [(a, b) for a in alice for b in bob]
    Z_A, X_A, Z_B, X_B = build_local_paulis(alice, bob, sector)
    V = poisson_greens_periodic()

    # Sweep: mass, G, and time
    print("--- Parameter sweep ---")
    print(f"  {'mass':>6s}  {'G':>6s}  {'t':>8s}  {'|S|':>10s}  {'Bell?':>8s}  {'%Tsir':>8s}")
    print("  " + "-" * 52)

    best_overall = {"S": 0}

    for mass in [0.5, 1.0, 2.0, 5.0, 10.0]:
        for G_grav in [0.0, 1.0, 5.0, 10.0, 20.0, 50.0]:
            H1 = staggered_hamiltonian_1p(mass=mass)
            H2, sec = build_sector_hamiltonian(H1, V, G_grav)
            U_dt = expm(-1j * H2 * 0.01)

            # Initial product state: Alice on even (site 0), Bob on even (site 2)
            psi = np.zeros(4, dtype=complex)
            psi[0] = 1.0  # sector index (0,2) = Alice at 0, Bob at 2

            best_S = 0
            best_t = 0
            for step in range(1001):
                if step % 10 == 0:
                    S, T = compute_chsh(psi, Z_A, X_A, Z_B, X_B)
                    if S > best_S:
                        best_S = S
                        best_t = step * 0.01
                psi = U_dt @ psi
                psi = psi / np.linalg.norm(psi)

            viol = best_S > 2.0
            pct = (best_S - 2.0) / (2 * math.sqrt(2) - 2.0) * 100 if viol else 0
            if best_S > best_overall["S"]:
                best_overall = {"S": best_S, "mass": mass, "G": G_grav, "t": best_t}

            if viol or G_grav == 0 or mass == 5.0:
                print(f"  {mass:6.1f}  {G_grav:6.1f}  {best_t:8.3f}  {best_S:10.6f}  "
                      f"{'YES' if viol else 'no':>8s}  {pct:7.1f}%")

    return best_overall


# ====================================================================
# Part 3: Ground-state Bell violation
# ====================================================================

def part_3():
    print()
    print("=" * 72)
    print("PART 3: GROUND-STATE BELL VIOLATION")
    print("=" * 72)
    print()

    alice = (0, 1)
    bob = (2, 3)
    sector = [(a, b) for a in alice for b in bob]
    Z_A, X_A, Z_B, X_B = build_local_paulis(alice, bob, sector)
    V = poisson_greens_periodic()

    print(f"  {'mass':>6s}  {'G':>6s}  {'|S|':>10s}  {'Bell?':>8s}  {'%Tsir':>8s}  {'E_gs':>10s}")
    print("  " + "-" * 54)

    best_overall = {"S": 0}

    for mass in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
        for G_grav in [0.0, 5.0, 10.0, 20.0, 50.0, 100.0]:
            H1 = staggered_hamiltonian_1p(mass=mass)
            H2, sec = build_sector_hamiltonian(H1, V, G_grav)
            evals, evecs = eigh(H2)
            gs = evecs[:, 0]

            S, T = compute_chsh(gs, Z_A, X_A, Z_B, X_B)
            viol = S > 2.0
            pct = (S - 2.0) / (2 * math.sqrt(2) - 2.0) * 100 if viol else 0

            if S > best_overall["S"]:
                best_overall = {"S": S, "mass": mass, "G": G_grav, "E_gs": evals[0]}

            if viol or G_grav == 0:
                print(f"  {mass:6.1f}  {G_grav:6.1f}  {S:10.6f}  {'YES' if viol else 'no':>8s}  "
                      f"{pct:7.1f}%  {evals[0]:10.4f}")

    return best_overall


# ====================================================================
# Main
# ====================================================================

def main():
    t0 = time.time()

    part_1()
    best_dyn = part_2()
    best_gs = part_3()

    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    print()

    if best_dyn["S"] > 2.0:
        print(f"  DYNAMICAL Bell violation: |S| = {best_dyn['S']:.6f}")
        print(f"    mass={best_dyn['mass']}, G={best_dyn['G']}, t={best_dyn['t']:.3f}")
    else:
        print(f"  No dynamical Bell violation (best |S| = {best_dyn['S']:.6f})")

    if best_gs["S"] > 2.0:
        print(f"  GROUND STATE Bell violation: |S| = {best_gs['S']:.6f}")
        print(f"    mass={best_gs['mass']}, G={best_gs['G']}")
    else:
        print(f"  No ground-state Bell violation (best |S| = {best_gs['S']:.6f})")

    any_viol = best_dyn["S"] > 2.0 or best_gs["S"] > 2.0
    if any_viol:
        print()
        print("  BELL VIOLATION CONFIRMED with:")
        print("    - Spatially separated Alice/Bob (disjoint site pairs)")
        print("    - Local Pauli algebras per party")
        print("    - [O_A, O_B] = 0 from tensor product structure")
        print("    - Periodic Poisson coupling (retained framework surface)")
        print("    - Product initial state -> dynamics create entanglement")

    elapsed = time.time() - t0
    print(f"\n  Time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
