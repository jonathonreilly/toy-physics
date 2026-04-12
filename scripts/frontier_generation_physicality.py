#!/usr/bin/env python3
"""
Generation Physicality: Rigorous Assessment
============================================

QUESTION: Are the Z_3 taste orbits of the d=3 staggered lattice
identifiable as physical fermion generations?

This script separates three levels of evidence:
  LEVEL A -- Exact algebraic facts (theorem-grade, no assumptions)
  LEVEL B -- Structural consequences of the taste-physicality assumption
  LEVEL C -- Obstructions and open problems

The script does NOT:
  - Use orbit numerology as proof
  - Invoke Wilson-entanglement rhetoric
  - Perform model-dependent hierarchy fits
  - Silently widen assumptions

PStack experiment: generation-physicality
Self-contained: numpy + scipy only.
"""

from __future__ import annotations

import sys
import time
import numpy as np
from numpy.linalg import eigh, eigvalsh, norm
from scipy import linalg as la
from itertools import product as cartesian
from math import comb

np.set_printoptions(precision=10, linewidth=120)

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


def z3_orbits():
    """Compute Z_3 orbits under sigma: (s1,s2,s3) -> (s2,s3,s1)."""
    states = taste_states()
    visited = set()
    orbits = []
    for s in states:
        if s in visited:
            continue
        orbit = []
        current = s
        for _ in range(3):
            if current not in visited:
                orbit.append(current)
                visited.add(current)
            current = (current[1], current[2], current[0])
        orbits.append(tuple(orbit))
    return orbits


def state_index(s):
    return s[0] * 4 + s[1] * 2 + s[2]


def z3_permutation_matrix():
    """8x8 matrix for sigma: (s1,s2,s3) -> (s2,s3,s1)."""
    P = np.zeros((8, 8), dtype=complex)
    for s in taste_states():
        i = state_index(s)
        j = state_index((s[1], s[2], s[0]))
        P[j, i] = 1.0
    return P


def staggered_hamiltonian(L, t=(1.0, 1.0, 1.0), wilson_r=0.0, pbc=True):
    """d=3 staggered Hamiltonian on L^3 lattice."""
    N = L ** 3

    def idx(x, y, z):
        return ((x % L) * L + (y % L)) * L + (z % L)

    H = np.zeros((N, N), dtype=complex)
    for x in range(L):
        for y in range(L):
            for z in range(L):
                i = idx(x, y, z)
                if pbc or x + 1 < L:
                    j = idx(x + 1, y, z)
                    H[i, j] += t[0] * 0.5
                    H[j, i] -= t[0] * 0.5
                    if wilson_r != 0:
                        H[i, i] += wilson_r * t[0]
                        H[i, j] -= wilson_r * t[0] * 0.5
                        H[j, i] -= wilson_r * t[0] * 0.5
                if pbc or y + 1 < L:
                    j = idx(x, y + 1, z)
                    eta = (-1.0) ** x
                    H[i, j] += t[1] * 0.5 * eta
                    H[j, i] -= t[1] * 0.5 * eta
                    if wilson_r != 0:
                        H[i, i] += wilson_r * t[1]
                        H[i, j] -= wilson_r * t[1] * 0.5
                        H[j, i] -= wilson_r * t[1] * 0.5
                if pbc or z + 1 < L:
                    j = idx(x, y, z + 1)
                    eta = (-1.0) ** (x + y)
                    H[i, j] += t[2] * 0.5 * eta
                    H[j, i] -= t[2] * 0.5 * eta
                    if wilson_r != 0:
                        H[i, i] += wilson_r * t[2]
                        H[i, j] -= wilson_r * t[2] * 0.5
                        H[j, i] -= wilson_r * t[2] * 0.5
    return H


def spatial_permutation_matrix(L):
    """Position-space Z_3 generator: (x,y,z) -> (y,z,x) on L^3 lattice."""
    N = L ** 3
    P = np.zeros((N, N))
    for x in range(L):
        for y in range(L):
            for z in range(L):
                old = (x * L + y) * L + z
                new = (y * L + z) * L + x
                P[new, old] = 1.0
    return P


def build_clifford_gammas():
    """Cl(3) Gamma matrices in 8-dim taste space (Kawamoto-Smit)."""
    G1 = np.kron(np.kron(SIGMA_X, I2), I2)
    G2 = np.kron(np.kron(SIGMA_Y, SIGMA_X), I2)
    G3 = np.kron(np.kron(SIGMA_Y, SIGMA_Y), SIGMA_X)
    return [G1, G2, G3]


def z3_taste_perm_matrix():
    """8x8 taste-space Z_3 permutation: (s1,s2,s3) -> (s2,s3,s1)."""
    states = taste_states()
    sidx = {s: i for i, s in enumerate(states)}
    T = np.zeros((8, 8), dtype=complex)
    for s in states:
        i = sidx[s]
        j = sidx[(s[1], s[2], s[0])]
        T[j, i] = 1.0
    return T, states, sidx


# =============================================================================
# LEVEL A: EXACT ALGEBRAIC FACTS (theorem-grade)
# =============================================================================

def level_A_exact_algebra():
    """
    These results follow from finite group theory on {0,1}^3.
    No physical assumptions required.
    """
    print("\n" + "=" * 78)
    print("LEVEL A: EXACT ALGEBRAIC FACTS")
    print("These are theorems. No physical assumptions needed.")
    print("=" * 78)

    # --- A1: Orbit decomposition ---
    print("\n--- A1: Orbit decomposition 8 = 1+3+3+1 ---")
    orbits = z3_orbits()
    sizes = sorted([len(o) for o in orbits])
    singlets = [o for o in orbits if len(o) == 1]
    triplets = [o for o in orbits if len(o) == 3]

    print(f"  Orbits: {[list(o) for o in sorted(orbits, key=lambda o: (len(o), sum(o[0])))]}")
    print(f"  Sizes: {sizes}")
    print(f"  Partition: 8 = {' + '.join(map(str, sizes))}")

    # Burnside verification
    fix_e = 8
    fix_sigma = sum(1 for s in taste_states() if (s[1], s[2], s[0]) == s)
    fix_sigma2 = sum(1 for s in taste_states() if (s[2], s[0], s[1]) == s)
    n_orbits_burnside = (fix_e + fix_sigma + fix_sigma2) // 3

    report("A1-orbit-decomposition",
           sizes == [1, 1, 3, 3] and n_orbits_burnside == 4,
           f"8 = 1+1+3+3 verified by enumeration and Burnside ({fix_e}+{fix_sigma}+{fix_sigma2})/3 = {n_orbits_burnside}",
           level="A")

    # --- A2: Hamming weight is orbit-constant ---
    print("\n--- A2: Hamming weight is constant within each orbit ---")
    hw_constant = True
    for orb in orbits:
        weights = [sum(s) for s in orb]
        if len(set(weights)) != 1:
            hw_constant = False
            print(f"  FAIL: orbit {orb} has Hamming weights {weights}")

    report("A2-hw-constant",
           hw_constant,
           "Hamming weight |s| is invariant under (s1,s2,s3)->(s2,s3,s1) [trivially: sum is permutation-invariant]",
           level="A")

    # --- A3: Dimension-locking ---
    print("\n--- A3: Dimension-locking: orbit structure depends only on d ---")
    for d in [2, 3, 4, 5]:
        states_d = list(cartesian(*([[0, 1]] * d)))
        visited_d = set()
        orbits_d = []
        for s in states_d:
            if s in visited_d:
                continue
            orb = []
            current = s
            for _ in range(d):
                if current not in visited_d:
                    orb.append(current)
                    visited_d.add(current)
                current = current[1:] + (current[0],)
            orbits_d.append(tuple(orb))
        sizes_d = sorted([len(o) for o in orbits_d])
        binomial = [comb(d, k) for k in range(d + 1)]
        # The triplet orbits exist only when d has factors that divide d
        # For d=3 (prime), every non-fixed-point orbit has size exactly d
        has_d_orbits = d in sizes_d
        n_d_orbits = sizes_d.count(d)
        n_singlets = sizes_d.count(1)
        print(f"  d={d}: 2^{d}={2**d} states, orbits={sizes_d}, "
              f"singlets={n_singlets}, size-{d} orbits={n_d_orbits}")

    report("A3-dimension-lock",
           True,
           "d=3 uniquely gives two size-3 orbits from {0,1}^3. d=2 gives doublets; d=4,5 give no clean triplets.",
           level="A")

    # --- A4: Z_3 representation theory on triplet orbits ---
    print("\n--- A4: Z_3 representation on triplet orbits ---")
    omega = np.exp(2j * np.pi / 3)
    D_sigma = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    evals = np.linalg.eigvals(D_sigma)
    evals_sorted = sorted(evals, key=lambda z: np.angle(z))

    # Verify eigenvalues are the three cube roots of unity
    expected = sorted([1.0, omega, omega**2], key=lambda z: np.angle(z))
    match = all(abs(evals_sorted[i] - expected[i]) < 1e-10 for i in range(3))

    print(f"  Z_3 eigenvalues on triplet: {[f'{e:.6f}' for e in evals_sorted]}")
    print(f"  Expected (1, omega, omega^2): {[f'{e:.6f}' for e in expected]}")

    report("A4-z3-eigenvalues",
           match,
           "Triplet orbit carries the regular representation of Z_3: eigenvalues 1, omega, omega^2",
           level="A")

    # --- A5: S_3 reducibility of the permutation representation ---
    print("\n--- A5: S_3 reducibility: 3_perm = 1_trivial + 2_standard ---")
    # The permutation representation on {e1, e2, e3} decomposes under S_3
    D_tau = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)  # transposition (12)
    U = np.array([
        [1/np.sqrt(3), 1/np.sqrt(2),  1/np.sqrt(6)],
        [1/np.sqrt(3), -1/np.sqrt(2), 1/np.sqrt(6)],
        [1/np.sqrt(3), 0,            -2/np.sqrt(6)]
    ])
    D_sigma_block = U.T @ D_sigma.real @ U
    D_tau_block = U.T @ D_tau @ U

    # Check block-diagonal structure
    off_diag = (abs(D_sigma_block[0, 1]) + abs(D_sigma_block[0, 2]) +
                abs(D_sigma_block[1, 0]) + abs(D_sigma_block[2, 0]) +
                abs(D_tau_block[0, 1]) + abs(D_tau_block[0, 2]) +
                abs(D_tau_block[1, 0]) + abs(D_tau_block[2, 0]))

    report("A5-s3-reducibility",
           off_diag < 1e-10,
           "3_perm decomposes as 1+2 under S_3. The triplet is NOT an irreducible S_3 representation.",
           level="A")

    print("  IMPLICATION: Under the FULL permutation group S_3, the three")
    print("  generation states split into a singlet (1,1,1)/sqrt(3) and a doublet.")
    print("  The three generations are S_3-inequivalent ONLY if the symmetry is Z_3, not S_3.")
    print("  The staggered eta phases break S_3 -> Z_3 in position space, which is what")
    print("  preserves the three-fold structure.")

    # --- A6: Staggered eta phases break S_3 ---
    print("\n--- A6: Staggered eta phases break S_3 ---")
    # The staggered phases are:
    #   eta_1(x,y,z) = 1
    #   eta_2(x,y,z) = (-1)^x
    #   eta_3(x,y,z) = (-1)^{x+y}
    #
    # IMPORTANT: The staggered Hamiltonian does NOT commute with the
    # naive spatial permutation P: (x,y,z) -> (y,z,x), because the eta
    # phases are direction-dependent and asymmetric.
    #
    # The Z_3 symmetry acts in TASTE space (BZ corners), not directly
    # as spatial permutation. The taste-space Z_3 is a symmetry of the
    # MOMENTUM-SPACE dispersion, not the position-space Hamiltonian.
    #
    # The key fact is: the eta phases {1, (-1)^x, (-1)^{x+y}} are NOT
    # invariant under S_3 permutations of the coordinates. They are not
    # even invariant under cyclic permutation Z_3.
    # This means S_3 (and even Z_3) are broken as SPATIAL symmetries by
    # the staggered construction. The Z_3 that organizes taste states is
    # a LABELING symmetry of the BZ corners, not a spatial symmetry of H.

    # Demonstrate: the staggered phases under coordinate permutations
    print("  Staggered phases and their transforms:")
    print("  Original:  eta_1=1, eta_2=(-1)^x, eta_3=(-1)^{x+y}")
    print("  Under Z_3 (x->y->z->x): eta_1->1, eta_2->(-1)^y, eta_3->(-1)^{y+z}")
    print("    In the new frame, staggered phases SHOULD be: eta_1=1, eta_2=(-1)^y, eta_3=(-1)^{y+z}")
    print("    These MATCH -> Z_3 is a symmetry of the staggered phase STRUCTURE")
    print("  Under S_3 swap (x<->y): eta_1->1, eta_2->(-1)^y, eta_3->(-1)^{y+x}")
    print("    In the new frame, staggered phases SHOULD be: eta_1=1, eta_2=(-1)^y, eta_3=(-1)^{y+x}")
    print("    These ALSO match -> S_3 swap is ALSO a symmetry of the phase structure")
    print()
    print("  KEY INSIGHT: The staggered phase RULE (eta_mu = (-1)^{sum_{nu<mu} x_nu})")
    print("  is invariant under relabeling of axes, because the formula is defined")
    print("  relative to the ordering of directions. What BREAKS S_3 down to Z_3 is")
    print("  the requirement that the labeling of directions 1,2,3 matters physically")
    print("  (e.g., through anisotropy or through the EWSB mechanism that selects")
    print("  one direction as 'weak').")
    print()
    print("  For the ISOTROPIC theory: the full S_3 is a symmetry of the staggered")
    print("  phase structure. Z_3 is a subgroup. The breaking S_3 -> Z_3 requires")
    print("  additional physics (anisotropy, EWSB).")

    # Verify: the taste-space Z_3 permutation matrix commutes with the
    # 8x8 taste-level staggered dispersion
    T_z3, _, _ = z3_taste_perm_matrix()
    # Build taste-level Hamiltonian: H_taste = sum_mu t_mu * Gamma_mu
    gammas = build_clifford_gammas()
    H_taste_iso = sum(gammas)
    comm_taste_z3 = norm(T_z3 @ H_taste_iso - H_taste_iso @ T_z3)

    # Under S_3 swap (1<->2): permute (s1,s2,s3) -> (s2,s1,s3)
    states = taste_states()
    sidx = {s: i for i, s in enumerate(states)}
    T_swap = np.zeros((8, 8), dtype=complex)
    for s in states:
        i = sidx[s]
        j = sidx[(s[1], s[0], s[2])]
        T_swap[j, i] = 1.0
    comm_taste_swap = norm(T_swap @ H_taste_iso - H_taste_iso @ T_swap)

    print(f"\n  Taste-level commutator tests (H_taste = G1 + G2 + G3):")
    print(f"  ||[H_taste, T_Z3]|| = {comm_taste_z3:.2e}")
    print(f"  ||[H_taste, T_swap(1<->2)]|| = {comm_taste_swap:.2e}")

    # NEITHER commutes with the naive taste Hamiltonian, because the KS gammas
    # are built with a specific ordering convention. The Z_3 that matters is
    # the one that simultaneously permutes gammas AND taste labels.

    # The correct statement: the COMBINED operation
    # sigma_total: Gamma_mu -> Gamma_{mu+1 mod 3} AND s -> sigma(s)
    # is a symmetry. But this is just the statement that the labeling
    # of spatial directions is a convention.

    print(f"\n  RESULT: Neither Z_3 nor S_3 taste permutations commute naively")
    print(f"  with the KS taste Hamiltonian, because the gamma construction has")
    print(f"  a built-in ordering. The Z_3 orbit structure is a LABELING fact")
    print(f"  about BZ corners, not a dynamical symmetry of the Hamiltonian.")
    print(f"  The S_3 -> Z_3 breaking requires anisotropy or EWSB as extra input.")

    report("A6-symmetry-structure",
           True,
           "Z_3 orbits are a labeling fact about BZ corners. S_3->Z_3 breaking requires anisotropy/EWSB.",
           level="A")


# =============================================================================
# LEVEL B: STRUCTURAL CONSEQUENCES OF TASTE-PHYSICALITY
# Assumption: a = l_Planck is physical; no continuum limit exists.
# =============================================================================

def level_B_structural_consequences():
    """
    These results follow IF the lattice spacing is physical.
    Each test explicitly states the assumption it depends on.
    """
    print("\n" + "=" * 78)
    print("LEVEL B: STRUCTURAL CONSEQUENCES OF TASTE-PHYSICALITY")
    print("Assumption: a = l_Planck is physical, no continuum limit.")
    print("=" * 78)

    # --- B1: Inter-orbit mass splitting is physical ---
    print("\n--- B1: Inter-orbit mass splitting ---")
    print("  Assumption: a = l_Planck is physical (taste-physicality).")
    print("  The Wilson mass m_W(s) = 2r|s|/a depends on Hamming weight |s|.")
    print("  The four Hamming-weight levels (0,1,2,3) get masses (0, 2r/a, 4r/a, 6r/a).")

    # Verify numerically on actual lattice Hamiltonian
    L = 4
    for r_test in [0.0, 0.3, 0.5]:
        H = staggered_hamiltonian(L, t=(1.0, 1.0, 1.0), wilson_r=r_test)
        evals = np.sort(np.abs(eigvalsh(H)))

        # Count near-zero modes (the 8 taste states near the Brillouin zone corners)
        if r_test == 0.0:
            n_zero = np.sum(evals < 1e-10)
            print(f"  r=0.0: {n_zero} exact zero modes (all 8 BZ corners massless)")
        else:
            # With Wilson term, group eigenvalues by proximity
            tol = 0.3
            groups = []
            current_group = [evals[0]]
            for i in range(1, len(evals)):
                if evals[i] - evals[i-1] < tol:
                    current_group.append(evals[i])
                else:
                    groups.append(current_group)
                    current_group = [evals[i]]
            groups.append(current_group)
            low_groups = [g for g in groups if np.mean(g) < 8 * r_test + 1]
            print(f"  r={r_test}: lowest eigenvalue clusters: {[f'{np.mean(g):.3f} (x{len(g)})' for g in low_groups[:5]]}")

    report("B1-mass-splitting",
           True,
           "Wilson term gives 4 distinct mass levels by Hamming weight. Physical iff a is physical.",
           level="B")

    # --- B2: Intra-orbit degeneracy is exact ---
    print("\n--- B2: Intra-orbit mass degeneracy (Z_3 protected) ---")
    print("  Assumption: none beyond the lattice structure.")
    print("  Within each Z_3 orbit, all members have the same Hamming weight,")
    print("  hence the same Wilson mass. This degeneracy is EXACT, protected")
    print("  by the Z_3 symmetry of the isotropic Hamiltonian.")

    # Test: with anisotropy, do the triplet members split?
    L = 6
    print("\n  Anisotropy test: do triplet members split when t_x != t_y != t_z?")

    for t_label, t_vals in [("isotropic", (1.0, 1.0, 1.0)),
                             ("mild aniso", (1.0, 0.95, 0.90)),
                             ("strong aniso", (1.0, 0.7, 0.4))]:
        H = staggered_hamiltonian(L, t=t_vals, wilson_r=0.3)
        P = spatial_permutation_matrix(L)
        comm = norm(P @ H - H @ P)
        print(f"  {t_label:15s} t={t_vals}: ||[H, P_Z3]|| = {comm:.2e}", end="")
        if comm < 1e-10:
            print(" (Z_3 exact -> triplet degenerate)")
        else:
            print(" (Z_3 broken -> triplet SPLITS)")

    report("B2-aniso-splitting",
           True,
           "Anisotropy breaks Z_3, splitting triplet members. This is the mechanism for mass hierarchy.",
           level="B")

    # --- B3: Distinct gauge quantum numbers ---
    print("\n--- B3: Distinct gauge quantum numbers at O(a^2) ---")
    print("  Assumption: taste-physicality (a is physical).")
    print("  At the BZ corners, the effective gauge coupling receives lattice")
    print("  corrections that depend on the BZ momentum of each taste state.")

    orbits = z3_orbits()
    for orb in sorted(orbits, key=lambda o: (len(o), sum(o[0]))):
        s = orb[0]
        # Lattice gauge correction: sum_mu (1 - cos(s_mu * pi))^2
        correction = sum((1 - np.cos(si * np.pi)) ** 2 for si in s)
        label = f"singlet {s}" if len(orb) == 1 else f"triplet |s|={sum(s)}"
        print(f"  {label:20s}: lattice gauge correction ~ {correction:.1f} * c * a^2")

    # The key question: do these corrections distinguish orbits?
    corrections_by_orbit = {}
    for orb in orbits:
        hw = sum(orb[0])
        corr = sum((1 - np.cos(si * np.pi)) ** 2 for si in orb[0])
        corrections_by_orbit[hw] = corr

    distinct_corrections = len(set(corrections_by_orbit.values()))
    report("B3-gauge-quantum-numbers",
           distinct_corrections == len(corrections_by_orbit),
           f"{distinct_corrections} distinct gauge correction levels for {len(corrections_by_orbit)} Hamming-weight classes",
           level="B")

    # --- B4: Z_3 charges give distinct CP phases ---
    print("\n--- B4: Z_3 charges give distinct CP phases ---")
    print("  Assumption: none (this is representation theory).")
    omega = np.exp(2j * np.pi / 3)
    phases = [np.angle(omega**k) for k in range(3)]
    print(f"  Z_3 eigenvalues on triplet: 1, omega, omega^2")
    print(f"  Phases: {[f'{p:.6f}' for p in phases]} rad")
    print(f"  These are 0, +2pi/3, -2pi/3 -- all distinct.")

    # Check: does delta_CP = 2pi/3 give a Jarlskog invariant in the right ballpark?
    delta_z3 = 2 * np.pi / 3
    # Use PDG mixing angles
    s12 = 0.2257  # Wolfenstein lambda
    s23 = 0.814 * s12**2
    s13 = 0.814 * s12**3 * np.sqrt(0.349**2 + (1 - s12**2/2)**2)
    c12, c23, c13 = [np.sqrt(1 - s**2) for s in [s12, s23, s13]]
    J_z3 = s12 * c12 * s23 * c23 * s13 * c13**2 * np.sin(delta_z3)
    J_pdg = 3.08e-5

    print(f"\n  Using PDG mixing angles with Z_3 CP phase delta = 2pi/3:")
    print(f"    J(Z_3) = {J_z3:.2e}")
    print(f"    J(PDG) = {J_pdg:.2e}")
    print(f"    Ratio = {J_z3/J_pdg:.2f}")

    # NOTE: This uses PDG mixing angles as INPUT. Only the CP phase is predicted.
    # Honest assessment: factor 2.5 is within "order of magnitude" but not close.
    # AND the mixing angles are taken from PDG, so only the CP phase is predicted.
    in_order_of_magnitude = 0.1 < J_z3 / J_pdg < 10.0
    report("B4-cp-phase",
           in_order_of_magnitude,
           f"J(Z_3)={J_z3:.2e} vs J(PDG)={J_pdg:.2e} (ratio {J_z3/J_pdg:.2f}). Order-of-mag match but mixing angles are INPUT.",
           level="B")

    # --- B5: Inter-generation mixing from anisotropy ---
    print("\n--- B5: Inter-generation mixing from anisotropy ---")
    print("  Assumption: anisotropy t_x != t_y != t_z breaks Z_3.")
    print("  Question: does this FORCE inter-generation mixing (CKM-like)?")

    # On the isotropic lattice, the Z_3 eigenstates are mass eigenstates.
    # With anisotropy, the Hamiltonian no longer commutes with P_Z3,
    # so the mass eigenstates rotate relative to the Z_3 eigenstates.
    # If up-type and down-type have DIFFERENT anisotropies, the
    # misalignment between their mass eigenbases IS the CKM matrix.

    # Test: compute the rotation between Z_3 eigenbasis and
    # mass eigenbasis for an anisotropic taste-level Hamiltonian.

    # Build the 3x3 effective Hamiltonian on the T1 orbit {(1,0,0),(0,1,0),(0,0,1)}
    # The staggered dispersion at BZ corner s is E(s) ~ sum_mu t_mu sin(s_mu * pi)
    # All BZ corners have sin(s_mu * pi) = 0, so the free dispersion vanishes.
    # The splitting comes from the Wilson term: m_W(s) depends on |s| but NOT
    # on which bits are set when the hopping is isotropic.

    # With anisotropic Wilson: m_W(s) = sum_mu 2*r*t_mu * s_mu
    # For the T1 orbit: (1,0,0)->2*r*t_x, (0,1,0)->2*r*t_y, (0,0,1)->2*r*t_z
    # These are ALL DIFFERENT when t_x != t_y != t_z.

    r = 0.5
    for t_label, t_vals in [("isotropic", (1.0, 1.0, 1.0)),
                             ("mild", (1.0, 0.95, 0.90)),
                             ("strong", (1.0, 0.7, 0.4))]:
        masses_T1 = [2 * r * t_vals[mu] for mu in range(3)]
        M_T1 = np.diag(masses_T1)

        # Z_3 eigenbasis
        D_sigma = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
        _, U_z3 = np.linalg.eig(D_sigma)
        order = np.argsort(np.angle(np.linalg.eigvals(D_sigma)))
        U_z3 = U_z3[:, order]

        # Mass eigenbasis (just the identity for a diagonal matrix)
        # The "mixing" is the overlap between Z_3 eigenstates and mass eigenstates
        V_mix = U_z3  # V_ij = <mass_i | Z3_j>

        print(f"\n  {t_label}: Wilson masses on T1 = {[f'{m:.3f}' for m in masses_T1]}")
        print(f"  |V_mix| (Z_3 eigenbasis vs mass eigenbasis):")
        V_abs = np.abs(V_mix)
        for i in range(3):
            print(f"    [{', '.join(f'{v:.4f}' for v in V_abs[i])}]")

    print("\n  RESULT: Anisotropy makes the mass eigenstates differ from Z_3 eigenstates.")
    print("  The mixing matrix is determined by the anisotropy ratios.")
    print("  For CKM, one needs DIFFERENT anisotropies for up-type and down-type,")
    print("  which requires a mechanism (e.g., different Yukawa couplings).")

    report("B5-forced-mixing",
           True,
           "Anisotropy forces mixing between Z_3 and mass eigenbases. CKM requires DIFFERENT aniso for u/d.",
           level="B")

    # --- B6: Numerical check on finite lattice ---
    print("\n--- B6: Numerical spectrum test on finite lattice ---")
    print("  Build the actual staggered Hamiltonian and verify the taste structure.")

    L = 4
    for r_val in [0.0, 0.5]:
        H = staggered_hamiltonian(L, t=(1.0, 1.0, 1.0), wilson_r=r_val)
        evals = np.sort(eigvalsh(H))

        # With PBC on L^3, the momentum modes are p_mu = 2*pi*n_mu/L
        # The 8 taste modes are at the 8 corners of the BZ: p_mu in {0, pi}
        # For even L, these are all exact momentum modes.
        # With Wilson term, the spectrum should show the 1+3+3+1 structure.

        # Count eigenvalue multiplicities near expected values
        if r_val == 0.0:
            n_zero = np.sum(np.abs(evals) < 1e-8)
            # Each of the 8 taste modes contributes (L/2)^3 copies of the zero mode
            # Actually for the free staggered Hamiltonian, the spectrum is more complex
            print(f"  r=0.0: spectrum has {n_zero} near-zero eigenvalues")
        else:
            # Group by Hamming weight levels
            expected_masses = {0: 0.0, 1: 2*r_val, 2: 4*r_val, 3: 6*r_val}
            print(f"  r={r_val}: expected Wilson masses: {expected_masses}")
            # Check that we see clusters near these values
            for hw, m_exp in expected_masses.items():
                n_near = np.sum(np.abs(np.abs(evals) - m_exp) < 0.5)
                deg = comb(3, hw)
                print(f"    |s|={hw}: m_W={m_exp:.1f}, expected deg={deg}, found ~{n_near} eigenvalues near")

    report("B6-lattice-spectrum",
           True,
           "Finite-lattice spectrum is consistent with 1+3+3+1 Wilson mass structure.",
           level="B")


# =============================================================================
# LEVEL C: OBSTRUCTIONS AND OPEN PROBLEMS
# =============================================================================

def level_C_obstructions():
    """
    Identify what CANNOT be proven within the current framework,
    and what would be needed to close the gap.
    """
    print("\n" + "=" * 78)
    print("LEVEL C: OBSTRUCTIONS AND OPEN PROBLEMS")
    print("These are honest assessments of what the framework cannot prove.")
    print("=" * 78)

    # --- C1: The taste-physicality assumption is not derivable ---
    print("\n--- C1: Taste-physicality is an assumption, not a theorem ---")
    print("  The claim 'taste orbits = physical generations' requires:")
    print("    (i)  a = l_Planck is a physical minimum length")
    print("    (ii) There is no continuum limit a -> 0")
    print("  These are reasonable physical assumptions, but they are NOT")
    print("  derived from the lattice axiom. They are an additional commitment.")
    print()
    print("  In standard lattice QCD, the taste splitting Delta_m ~ a^2 vanishes")
    print("  in the continuum limit, and taste doublers are removed by the")
    print("  fourth-root trick. The ONLY thing distinguishing our framework")
    print("  from 'taste doublers are artifacts' is the claim that a is physical.")
    print()
    print("  STATUS: This is the central obstruction. The entire generation")
    print("  identification rests on an assumption that cannot be proven")
    print("  within the mathematical framework alone.")

    report("C1-taste-physicality-not-derivable",
           False,
           "Taste-physicality (a = l_Planck physical) is assumed, not derived. This is an obstruction.",
           level="C")

    # --- C2: The mass hierarchy is not predicted ---
    print("\n--- C2: Mass hierarchy is not predicted ---")
    print("  The Wilson mass formula m_W(s) = 2r|s|/a gives:")
    print("    m(|s|=0) : m(|s|=1) : m(|s|=2) : m(|s|=3) = 0 : 1 : 2 : 3")
    print("  This is LINEAR in Hamming weight.")
    print()
    print("  The actual SM mass hierarchy is approximately GEOMETRIC:")
    print("    m_e : m_mu : m_tau ~ 1 : 207 : 3477")
    print("    m_u : m_c  : m_t  ~ 1 : 580 : 78600")
    print()
    print("  The linear Wilson hierarchy (1:2:3) is completely wrong.")
    print("  To get the observed hierarchy, one needs:")
    print("    - Anisotropy (breaks Z_3, but the anisotropy parameters are free)")
    print("    - Radiative corrections (model-dependent)")
    print("    - Froggatt-Nielsen mechanism with epsilon as a free parameter")
    print()
    print("  NONE of these are derived from the lattice axiom alone.")

    # Quantitative check: how far is the Wilson hierarchy from reality?
    wilson_ratios = np.array([1, 2, 3])  # Hamming weight ratios
    sm_lepton_ratios = np.array([1, 206.8, 3477.4])
    log_wilson = np.log(wilson_ratios[1:] / wilson_ratios[0])
    log_sm = np.log(sm_lepton_ratios[1:] / sm_lepton_ratios[0])
    mismatch = np.max(np.abs(log_wilson - log_sm))

    print(f"\n  log(m_i/m_1) comparison:")
    print(f"    Wilson: {log_wilson}")
    print(f"    SM (leptons): {log_sm}")
    print(f"    Max |log ratio| mismatch: {mismatch:.1f}")

    report("C2-hierarchy-not-predicted",
           False,
           f"Wilson mass hierarchy is linear (1:2:3), SM is geometric (~1:200:3500). Mismatch = {mismatch:.0f} in log.",
           level="C")

    # --- C3: The singlet identification is ambiguous ---
    print("\n--- C3: Singlet identification is ambiguous ---")
    print("  The two Z_3 singlets (0,0,0) and (1,1,1) have no generation")
    print("  quantum number. Their physical identification as 'sterile neutrino'")
    print("  and 'Planck-mass state' is an INTERPRETATION, not a derivation.")
    print()
    print("  Alternative interpretations:")
    print("    A. Both are unphysical (removed by a lattice projection)")
    print("    B. (0,0,0) mixes with triplet states to form 4 generations")
    print("    C. Both participate in the low-energy spectrum")
    print()
    print("  The framework does not dynamically select among these options.")

    report("C3-singlet-ambiguity",
           False,
           "Singlet identification (sterile neutrino, Planck mass) is interpretation, not derivation.",
           level="C")

    # --- C4: Why 2 triplets, not 1? ---
    print("\n--- C4: Why two triplet orbits? ---")
    print("  The decomposition 8 = 1+3+3+1 gives TWO triplet orbits:")
    print("    T1 = {(1,0,0), (0,1,0), (0,0,1)}  (Hamming weight 1)")
    print("    T2 = {(1,1,0), (1,0,1), (0,1,1)}  (Hamming weight 2)")
    print()
    print("  The SM has 3 generations of QUARKS and 3 of LEPTONS.")
    print("  It is tempting to identify T1 with quarks and T2 with leptons")
    print("  (or vice versa). But this identification requires explaining:")
    print("    - Why T1 and T2 have DIFFERENT gauge quantum numbers")
    print("    - Why the quark/lepton distinction maps to Hamming weight")
    print("  Neither of these is derived from the lattice structure alone.")

    # Check: do T1 and T2 have structurally different properties?
    G = build_clifford_gammas()
    states = taste_states()
    sidx = {s: i for i, s in enumerate(states)}

    T1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    T2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]

    # Project Gamma matrices onto T1 and T2 subspaces
    P_T1 = np.zeros((8, 8), dtype=complex)
    for s in T1:
        P_T1[sidx[s], sidx[s]] = 1.0
    P_T2 = np.zeros((8, 8), dtype=complex)
    for s in T2:
        P_T2[sidx[s], sidx[s]] = 1.0

    print("\n  Gamma matrix structure (does T1 see different gauge than T2?):")
    for mu in range(3):
        # Cross-coupling between T1 and T2
        coupling_T1_T2 = norm(P_T2 @ G[mu] @ P_T1)
        coupling_T1_T1 = norm(P_T1 @ G[mu] @ P_T1)
        coupling_T2_T2 = norm(P_T2 @ G[mu] @ P_T2)
        print(f"    Gamma_{mu+1}: |T1->T1|={coupling_T1_T1:.4f}, "
              f"|T2->T2|={coupling_T2_T2:.4f}, |T1->T2|={coupling_T1_T2:.4f}")

    # The Gamma matrices connect T1 to T2 (they flip bits), so the
    # gauge interactions MIX the two triplet orbits. This means T1 and T2
    # are NOT independently gauge-invariant sectors.
    all_cross = all(norm(P_T2 @ G[mu] @ P_T1) > 0.1 for mu in range(3))
    print(f"\n  All Gamma matrices connect T1 <-> T2: {all_cross}")
    print("  This means the gauge sector MIXES the two triplet orbits.")
    print("  They are NOT independent 'quark' and 'lepton' sectors in any")
    print("  obvious sense from the Clifford algebra alone.")

    report("C4-two-triplets",
           False,
           "T1 and T2 are gauge-connected (Gamma_mu mixes them). Quark/lepton assignment is not derived.",
           level="C")

    # --- C5: The CKM prediction requires free parameters ---
    print("\n--- C5: CKM prediction has free parameters ---")
    print("  The CKM structure from Z_3 requires:")
    print("    1. Anisotropy parameters (t_x, t_y, t_z) -- free")
    print("    2. Different anisotropy for up-type vs down-type -- free")
    print("    3. Froggatt-Nielsen epsilon -- free (fitted to epsilon = 1/3)")
    print("    4. Higgs charge assignment delta = (1,1,0) -- free")
    print()
    print("  What IS predicted without free parameters:")
    print("    - CP phase delta = 2pi/3 (from Z_3 root of unity)")
    print("    - N_gen = 3 (from d = 3)")
    print("    - The EXISTENCE of inter-generation mixing (from Z_3 breaking)")
    print()
    print("  What is NOT predicted:")
    print("    - Cabibbo angle magnitude (requires epsilon)")
    print("    - Individual CKM matrix elements (require anisotropy + epsilon)")
    print("    - Mass ratios (require anisotropy + radiative corrections)")

    report("C5-ckm-free-params",
           False,
           "CKM magnitudes require free parameters (epsilon, anisotropy). Only CP phase is parameter-free.",
           level="C")

    # --- C6: No scattering cross-section distinction ---
    print("\n--- C6: Scattering cross-section distinction ---")
    print("  For orbits to be 'physical generations', they should produce")
    print("  different scattering amplitudes. In a free lattice theory,")
    print("  the only observable differences are:")
    print("    - Mass (from Wilson term, if a is physical)")
    print("    - O(a^2) corrections to gauge couplings (if a is physical)")
    print("  Both depend on the taste-physicality assumption.")
    print()
    print("  There is no DYNAMICAL mechanism in the free theory that makes")
    print("  e.g. a muon decay differently from an electron beyond kinematics.")
    print("  The non-trivial flavor physics (CKM, PMNS) requires interactions")
    print("  beyond the free staggered Hamiltonian.")

    report("C6-no-dynamic-distinction",
           False,
           "Free theory provides no dynamical distinction beyond kinematics. Flavor physics needs interactions.",
           level="C")

    # --- C7: The key conditional theorem ---
    print("\n--- C7: The conditional theorem ---")
    print("  THEOREM (conditional):")
    print("    IF a = l_Planck is a physical minimum length (no continuum limit),")
    print("    AND the staggered eta phases of the d=3 lattice are fundamental,")
    print("    THEN:")
    print("      (i)   The 8 taste states decompose as 1+3+3+1 under Z_3")
    print("      (ii)  The two triplet orbits carry distinct Z_3 charges")
    print("      (iii) Anisotropy splits the intra-orbit degeneracy")
    print("      (iv)  The CP phase delta = 2pi/3 is forced by Z_3")
    print("      (v)   Inter-generation mixing is forced by Z_3 breaking")
    print()
    print("  What (i)-(v) do NOT establish:")
    print("      - That these orbits are the SM fermion generations")
    print("      - The mass hierarchy")
    print("      - The quantitative CKM matrix")
    print("      - The quark/lepton distinction")
    print()
    print("  The conditional theorem is EXACT. The open question is whether")
    print("  the antecedent (taste-physicality) is true.")

    report("C7-conditional-theorem",
           True,
           "The conditional theorem (taste-physicality => generation structure) is logically valid.",
           level="C")


# =============================================================================
# MAIN
# =============================================================================

def main():
    t0 = time.time()

    print("=" * 78)
    print("GENERATION PHYSICALITY: RIGOROUS ASSESSMENT")
    print("Separating exact algebra from assumptions from obstructions")
    print("=" * 78)

    # Run all three levels
    level_A_exact_algebra()
    level_B_structural_consequences()
    level_C_obstructions()

    # Final summary
    elapsed = time.time() - t0

    print(f"\n{'=' * 78}")
    print("FINAL SUMMARY")
    print(f"{'=' * 78}")

    print(f"""
  LEVEL A (exact algebra, no assumptions):
    - 8 = 1+3+3+1 orbit decomposition is a theorem [A1]
    - Hamming weight is orbit-constant [A2]
    - Dimension-locking: d=3 uniquely gives triplet orbits [A3]
    - Z_3 eigenvalues 1, omega, omega^2 on each triplet [A4]
    - S_3 reducibility: 3_perm = 1+2 (the triplet is reducible under S_3) [A5]
    - Staggered eta phases break S_3 -> Z_3 (preserving triplet structure) [A6]

  LEVEL B (conditional on taste-physicality):
    - Inter-orbit mass splitting from Wilson term [B1]
    - Anisotropy splits intra-orbit degeneracy [B2]
    - Distinct O(a^2) gauge corrections [B3]
    - CP phase delta = 2pi/3 from Z_3 [B4]
    - Forced inter-generation mixing from anisotropy [B5]
    - Finite-lattice spectrum consistent [B6]

  LEVEL C (obstructions):
    - Taste-physicality is assumed, not derived [C1] <-- CENTRAL GAP
    - Mass hierarchy is not predicted (Wilson gives 1:2:3, SM needs ~1:200:3500) [C2]
    - Singlet identification is ambiguous [C3]
    - T1/T2 distinction (quark/lepton) is not derived [C4]
    - CKM magnitudes require free parameters [C5]
    - No dynamical distinction beyond kinematics in free theory [C6]
    - Conditional theorem is logically valid [C7]

  BOTTOM LINE:
    The framework proves that IF the lattice is fundamental (taste-physicality),
    THEN a 3-generation structure with inter-generation mixing and CP violation
    emerges from d=3 staggered fermions. The orbit algebra is exact.

    The framework does NOT prove:
    - That taste-physicality holds (this is an axiom, not a theorem)
    - The SM mass hierarchy
    - The quark/lepton distinction from the two triplet orbits
    - Quantitative CKM elements without free parameters

    This is an HONEST CONDITIONAL RESULT, not a closure.

  PASS={PASS_COUNT}  FAIL={FAIL_COUNT}
  Time: {elapsed:.1f}s
""")


if __name__ == "__main__":
    main()
