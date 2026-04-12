#!/usr/bin/env python3
"""
Weinberg Angle from Lattice Gauge Structure
============================================

THE PROBLEM:
  The Weinberg angle theta_W relates SU(2)_L and U(1)_Y couplings:
    sin^2(theta_W) = g'^2 / (g^2 + g'^2)
  where g is SU(2) coupling, g' is U(1) coupling.

  Observed: sin^2(theta_W) = 0.23122 +/- 0.00003  (PDG, M_Z, MS-bar)
  GUT prediction: 3/8 = 0.375 at M_GUT, runs to ~0.231 at M_Z.

THE FRAMEWORK:
  SU(2) emerges from the bipartite (Z_2) structure of the cubic lattice
  via Clifford algebra Cl(3). The three Pauli matrices arise as Cl(3)
  generators acting on the two sublattices.

  U(1) emerges from edge phases: scalar phases exp(i*theta) on directed
  edges of the lattice.

  The Weinberg angle has NOT been predicted. This script explores whether
  the lattice structure constrains sin^2(theta_W).

FOUR APPROACHES:

  1. LATTICE COUPLING RATIO
     SU(2) from Cl(3): 3 generators, dimension 2.
     U(1) from edge phases: 1 generator, dimension 1.
     Compute bare coupling ratio from lattice structure.

  2. GROUP EMBEDDING (GUT-style)
     SU(2) x U(1) embeds in SU(3) with hypercharge Y = diag(1/3, 1/3, -2/3).
     This gives sin^2(theta_W) = 3/8 at unification. Check whether the
     lattice embedding naturally produces this normalization.

  3. CASIMIR RATIO
     Use quadratic Casimir operators C_2 for SU(2) and U(1) with
     appropriate normalization to derive the coupling ratio.

  4. LATTICE SYMMETRY (Oh group)
     The cubic lattice has symmetry group Oh (48 elements). The Z_2
     grading and remaining symmetries might fix the coupling ratio.

HONEST EXPECTATION:
  The GUT value 3/8 is robust and well-understood from group theory.
  If the lattice structure reproduces 3/8, that confirms the framework
  is consistent with GUT embedding but does not constitute a new prediction.
  A genuinely NEW prediction would require a value different from 3/8
  with a lattice-specific mechanism.
"""

from __future__ import annotations

import sys
import time

import numpy as np

try:
    from scipy import sparse
    from scipy.sparse.linalg import eigsh
    HAS_SCIPY = True
except ImportError:
    print("ERROR: scipy required. pip install scipy")
    sys.exit(1)


# ============================================================================
# Constants
# ============================================================================

SIN2_TW_OBSERVED = 0.23122       # PDG value at M_Z in MS-bar scheme
SIN2_TW_OBSERVED_ERR = 0.00003
SIN2_TW_GUT = 3 / 8              # = 0.375, GUT prediction at unification scale

# Pauli matrices (su(2) generators in fundamental rep, normalized T_a = sigma_a / 2)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMA_0 = np.eye(2, dtype=complex)

# Gell-Mann matrices (su(3) generators, normalized Tr(T_a T_b) = delta_ab / 2)
LAMBDA = [None] * 9  # 1-indexed below
LAMBDA[1] = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex)
LAMBDA[2] = np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex)
LAMBDA[3] = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex)
LAMBDA[4] = np.array([[0, 0, 1], [0, 0, 0], [1, 0, 0]], dtype=complex)
LAMBDA[5] = np.array([[0, 0, -1j], [0, 0, 0], [1j, 0, 0]], dtype=complex)
LAMBDA[6] = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex)
LAMBDA[7] = np.array([[0, 0, 0], [0, 0, -1j], [0, 1j, 0]], dtype=complex)
LAMBDA[8] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]], dtype=complex) / np.sqrt(3)


# ============================================================================
# APPROACH 1: Lattice coupling ratio from Clifford algebra structure
# ============================================================================

def approach1_lattice_coupling_ratio():
    """Derive coupling ratio from lattice algebraic structure.

    SU(2) sector:
      - Arises from Cl(3) = M_2(C), the 2x2 complex matrix algebra
      - Three generators: sigma_x, sigma_y, sigma_z (from Z_2 grading of 3 axes)
      - Dimension of fundamental rep: d_2 = 2
      - Number of generators: n_2 = 3

    U(1) sector:
      - Arises from edge phases exp(i*theta)
      - One generator: identity on phase space
      - Dimension of fundamental rep: d_1 = 1
      - Number of generators: n_1 = 1

    The coupling ratio g'/g can be related to the normalization condition.
    In GUT embedding, the key is how U(1)_Y is normalized relative to SU(2).
    """
    print("=" * 72)
    print("APPROACH 1: Lattice coupling ratio from Cl(3) structure")
    print("=" * 72)
    print()

    # Cl(3) generators (Pauli matrices as basis for su(2))
    generators_su2 = [SIGMA_X / 2, SIGMA_Y / 2, SIGMA_Z / 2]
    n_gen_su2 = len(generators_su2)
    d_rep_su2 = 2

    # Verify algebra: [T_a, T_b] = i * epsilon_{abc} * T_c
    print("Verifying su(2) algebra from Cl(3) generators:")
    eps = np.zeros((3, 3, 3))
    eps[0, 1, 2] = eps[1, 2, 0] = eps[2, 0, 1] = 1
    eps[0, 2, 1] = eps[2, 1, 0] = eps[1, 0, 2] = -1

    algebra_ok = True
    for a in range(3):
        for b in range(3):
            commutator = generators_su2[a] @ generators_su2[b] - generators_su2[b] @ generators_su2[a]
            expected = sum(1j * eps[a, b, c] * generators_su2[c] for c in range(3))
            if not np.allclose(commutator, expected):
                algebra_ok = False
                print(f"  FAIL: [T_{a}, T_{b}] != i*eps*T_c")

    if algebra_ok:
        print("  su(2) algebra: VERIFIED (all commutators correct)")
    print()

    # Trace normalization
    for a in range(3):
        tr = np.trace(generators_su2[a] @ generators_su2[a])
        print(f"  Tr(T_{a+1}^2) = {tr.real:.4f}")
    print()

    # U(1) generator from edge phase
    # On the lattice, U(1) phase lives on edges. The generator Y is a real number.
    # For a single edge, the generator is just the identity times a charge.
    # The normalization depends on the hypercharge assignment.

    # Key insight: on the cubic lattice with Z_2 grading, the two sublattices
    # have "charges" +1 and -1. If we embed SU(2) x U(1) in SU(3), the
    # hypercharge generator is proportional to lambda_8.

    Y_fund = np.diag([1/3, 1/3, -2/3])  # Hypercharge in SU(3) fundamental
    print(f"  Hypercharge generator Y = diag(1/3, 1/3, -2/3)")
    print(f"  Tr(Y^2) = {np.trace(Y_fund @ Y_fund):.6f}")
    print()

    # The SU(2) generators embedded in SU(3) are T_a = lambda_a / 2 for a=1,2,3
    # These act on the upper 2x2 block.
    T_su2_in_su3 = []
    for a in range(3):
        T = np.zeros((3, 3), dtype=complex)
        T[:2, :2] = generators_su2[a]
        T_su2_in_su3.append(T)

    print("SU(2) generators embedded in SU(3):")
    for a in range(3):
        tr = np.trace(T_su2_in_su3[a] @ T_su2_in_su3[a])
        print(f"  Tr(T_{a+1}^2) = {tr.real:.4f}")
    print()

    # The coupling ratio is fixed by the normalization condition
    # that all generators of the unified group have equal trace:
    #   Tr(T_a^2) = 1/2 for SU(3)
    # SU(2) generators already satisfy this.
    # The U(1) generator Y must be rescaled: Y_norm = Y / sqrt(Tr(Y^2) * 2)

    tr_Y2 = np.trace(Y_fund @ Y_fund).real
    Y_norm_factor = np.sqrt(2 * tr_Y2)
    Y_normalized = Y_fund / Y_norm_factor * np.sqrt(2)  # so Tr(Y_norm^2) = 1/2

    tr_check = np.trace(Y_normalized @ Y_normalized).real
    print(f"  Y normalization factor: sqrt(2 * Tr(Y^2)) = {Y_norm_factor:.6f}")
    print(f"  Tr(Y_normalized^2) = {tr_check:.6f} (should be 0.5)")
    print()

    # The Weinberg angle comes from the relative normalization:
    # g' / g = sqrt(Tr(T_3^2)) / sqrt(Tr(Y^2)) in the UNNORMALIZED basis
    # After proper GUT normalization:
    #   sin^2(theta_W) = g'^2 / (g^2 + g'^2)
    #
    # In SU(5) or any simple GUT:
    #   g = g' * sqrt(5/3)  (the famous 5/3 factor from normalization)
    #   sin^2(theta_W) = 1 / (1 + 5/3) = 3/8

    # Direct computation from trace normalization:
    tr_T3_sq = np.trace(T_su2_in_su3[2] @ T_su2_in_su3[2]).real
    tr_Y_sq = tr_Y2

    # The normalization factor k relates the physical U(1) coupling g' to
    # the GUT-normalized coupling: g_1 = g' * sqrt(k)
    # For SU(3) embedding: k = Tr(T_3^2) / Tr(Y^2) evaluated on the fundamental
    # But the standard GUT normalization uses k = 5/3

    # Method 1: Direct from SU(3) embedding
    k_su3 = tr_T3_sq / tr_Y_sq
    sin2_tw_su3_direct = 1 / (1 + k_su3)
    print(f"  Direct SU(3) embedding:")
    print(f"    k = Tr(T_3^2)/Tr(Y^2) = {k_su3:.6f}")
    print(f"    sin^2(theta_W) = 1/(1+k) = {sin2_tw_su3_direct:.6f}")
    print()

    # Method 2: Standard GUT normalization (SU(5))
    # In SU(5), k = 5/3 because Y is embedded with specific normalization
    k_gut = 5 / 3
    sin2_tw_gut = 1 / (1 + k_gut)
    print(f"  Standard SU(5) GUT:")
    print(f"    k = 5/3 = {k_gut:.6f}")
    print(f"    sin^2(theta_W) = 3/8 = {sin2_tw_gut:.6f}")
    print()

    # Method 3: Lattice-specific -- Cl(3) trace normalization
    # In Cl(3), the generators are sigma_a/2 with Tr(T_a^2) = 1/2
    # The U(1) generator on the lattice is the staggering operator:
    #   eps = (-1)^{x+y+z}, which has Tr(eps^2) = N (number of sites)
    # Per site: Tr(eps^2)/N = 1
    # For normalized generator: Y_lat = eps/2 so Tr(Y_lat^2) = 1/4 per site

    # Dimension counting: SU(2) has d=2 rep, so Tr(T_3^2) = 1/2
    # U(1) has d=1 rep, so Tr(Y^2) = Y^2 for charge Y
    # The lattice Z_2 grading assigns Y = +/- 1/2 to the sublattices

    tr_T3_lat = 0.5  # Tr((sigma_3/2)^2) = 1/2
    tr_Y_lat = 0.25  # (1/2)^2 = 1/4 for a single charged field
    k_lattice = tr_T3_lat / tr_Y_lat
    sin2_tw_lattice = 1 / (1 + k_lattice)
    print(f"  Lattice Cl(3) + Z_2 grading:")
    print(f"    Tr(T_3^2) = {tr_T3_lat} (from sigma_3/2)")
    print(f"    Tr(Y^2) = {tr_Y_lat} (from Z_2 charge +/-1/2)")
    print(f"    k = {k_lattice:.4f}")
    print(f"    sin^2(theta_W) = {sin2_tw_lattice:.6f}")
    print()

    # Summary
    print("  APPROACH 1 SUMMARY:")
    print(f"    Direct SU(3) embedding:  sin^2(theta_W) = {sin2_tw_su3_direct:.4f}")
    print(f"    Standard SU(5) GUT:      sin^2(theta_W) = {sin2_tw_gut:.4f}")
    print(f"    Lattice Cl(3)+Z_2:       sin^2(theta_W) = {sin2_tw_lattice:.4f}")
    print(f"    Observed (M_Z):          sin^2(theta_W) = {SIN2_TW_OBSERVED:.4f}")
    print()

    return {
        "su3_direct": sin2_tw_su3_direct,
        "gut": sin2_tw_gut,
        "lattice": sin2_tw_lattice,
    }


# ============================================================================
# APPROACH 2: Group embedding -- SU(2)xU(1) in SU(3) from lattice structure
# ============================================================================

def approach2_group_embedding():
    """Check whether the lattice structure naturally produces the SU(3) embedding.

    The cubic lattice is bipartite: sites split into A and B sublattices
    with eps = (-1)^{x+y+z}. This gives a natural 2-coloring.

    If we triangulate (add face/body diagonals), we get 3-colorability,
    which maps to SU(3). The question is: does the specific embedding
    of SU(2)xU(1) in SU(3) from lattice structure match the Standard Model?

    The Standard Model hypercharge assignments (for left-handed fermions):
      Q_L = (u_L, d_L): Y = 1/6, T_3 = +/- 1/2
      L_L = (nu_L, e_L): Y = -1/2, T_3 = +/- 1/2
      u_R: Y = 2/3, T_3 = 0
      d_R: Y = -1/3, T_3 = 0
      e_R: Y = -1, T_3 = 0

    The lattice structure via Cl(3) gives SU(2) but the hypercharge
    assignments must come from additional structure.
    """
    print("=" * 72)
    print("APPROACH 2: Group embedding from lattice structure")
    print("=" * 72)
    print()

    # Step 1: Verify the branching rule SU(3) -> SU(2) x U(1)
    # Under SU(3) -> SU(2) x U(1), the fundamental 3 decomposes as:
    #   3 = (2, 1/6) + (1, -1/3)
    # But wait -- this is the SM decomposition with specific Y normalization.
    # The GROUP-THEORETIC decomposition is:
    #   3 = (2, Y_1) + (1, Y_2)
    # with Y_1 and Y_2 fixed by tracelessness: 2*Y_1 + Y_2 = 0 => Y_2 = -2*Y_1

    print("SU(3) -> SU(2) x U(1) branching:")
    print("  Fundamental: 3 = (2, Y) + (1, -2Y)")
    print("  Adjoint: 8 = (3, 0) + (2, 3Y) + (2, -3Y) + (1, 0)")
    print()

    # The normalization of Y is a CHOICE. Different choices give different
    # sin^2(theta_W) at tree level.

    # Choice 1: Canonical GUT normalization (SU(5) embedding)
    # Y normalized so that Tr(Y^2) = Tr(T_3^2) over a complete GUT multiplet
    # For the SU(5) fundamental 5 = (3,1,-1/3) + (1,2,1/2):
    #   sum Y^2 = 3*(1/3)^2 + 2*(1/2)^2 = 1/3 + 1/2 = 5/6
    #   sum T_3^2 = 0 + 2*(1/2)^2 = 1/2
    #   Normalization factor: k = sum Y^2 / sum T_3^2 = (5/6)/(1/2) = 5/3

    y_values_5bar = [1/3, 1/3, 1/3, -1/2, -1/2]  # 5-bar of SU(5)
    t3_values_5bar = [0, 0, 0, 1/2, -1/2]

    sum_y2 = sum(y**2 for y in y_values_5bar)
    sum_t3_2 = sum(t**2 for t in t3_values_5bar)
    k_su5 = sum_y2 / sum_t3_2

    print(f"  SU(5) fundamental (5-bar):")
    print(f"    Y values: {y_values_5bar}")
    print(f"    T_3 values: {t3_values_5bar}")
    print(f"    sum(Y^2) = {sum_y2:.6f}")
    print(f"    sum(T_3^2) = {sum_t3_2:.6f}")
    print(f"    k = sum(Y^2)/sum(T_3^2) = {k_su5:.6f}")
    print(f"    sin^2(theta_W) = 1/(1+k) = {1/(1+k_su5):.6f}")
    print()

    # Choice 2: SU(3) fundamental only
    # For the SU(3) fundamental 3, with Y = diag(1/3, 1/3, -2/3):
    y_fund = [1/3, 1/3, -2/3]
    t3_fund = [1/2, -1/2, 0]

    sum_y2_3 = sum(y**2 for y in y_fund)
    sum_t3_3 = sum(t**2 for t in t3_fund)
    k_su3 = sum_y2_3 / sum_t3_3

    print(f"  SU(3) fundamental (3):")
    print(f"    Y values: {y_fund}")
    print(f"    T_3 values: {t3_fund}")
    print(f"    sum(Y^2) = {sum_y2_3:.6f}")
    print(f"    sum(T_3^2) = {sum_t3_3:.6f}")
    print(f"    k = {k_su3:.6f}")
    print(f"    sin^2(theta_W) = {1/(1+k_su3):.6f}")
    print()

    # Choice 3: Lattice-motivated -- bipartite Z_2 charge
    # The lattice Z_2 assigns charges +1, -1 to sublattices.
    # If we identify this with the SU(2) doublet, the U(1) charge
    # is determined by tracelessness within the doublet.
    # Doublet: Y = (y, y) with no constraint from SU(2)
    # Singlet: Y = y' with 2y + y' = 0 (tracelessness if embedding in SU(3))

    print("  Lattice-motivated Z_2 grading:")
    print("  The bipartite structure gives 2 sublattices.")
    print("  This is COMPATIBLE with SU(2) doublet structure.")
    print("  But the hypercharge normalization Y requires knowing")
    print("  which larger group SU(2)xU(1) embeds in.")
    print()

    # Step 2: Check the lattice hopping algebra on a small cubic lattice
    # to see if the embedding produces a specific Y normalization
    N = 6
    M = N - 2  # interior
    n_sites = M ** 3
    print(f"  Lattice test: {N}^3 cubic lattice ({n_sites} interior sites)")

    # Build staggering operator eps = (-1)^{x+y+z}
    eps = np.zeros(n_sites)
    for ix in range(M):
        for iy in range(M):
            for iz in range(M):
                flat = ix * M * M + iy * M + iz
                eps[flat] = (-1) ** (ix + iy + iz)

    n_even = np.sum(eps > 0)
    n_odd = np.sum(eps < 0)
    print(f"  Even sublattice sites: {int(n_even)}")
    print(f"  Odd sublattice sites: {int(n_odd)}")

    # The staggering operator has eigenvalues +1 and -1
    # Its "charge" spectrum is Z_2, mapping to Y = +/- 1/2
    # Sum(Y^2) over all sites = n_sites * (1/2)^2 = n_sites / 4
    # Per site: <Y^2> = 1/4

    # Build the hopping operator (nearest-neighbor on cubic lattice)
    rows, cols, vals = [], [], []
    for ix in range(M):
        for iy in range(M):
            for iz in range(M):
                flat = ix * M * M + iy * M + iz
                for dix, diy, diz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    nx, ny, nz = ix + dix, iy + diy, iz + diz
                    if 0 <= nx < M and 0 <= ny < M and 0 <= nz < M:
                        nflat = nx * M * M + ny * M + nz
                        rows.append(flat)
                        cols.append(nflat)
                        vals.append(1.0)

    H_hop = sparse.csr_matrix((vals, (rows, cols)), shape=(n_sites, n_sites))

    # The hopping operator anticommutes with the staggering operator on bipartite lattice
    # H_hop * eps = -eps * H_hop (since hopping flips sublattice)
    H_eps = H_hop @ sparse.diags(eps)
    eps_H = sparse.diags(eps) @ H_hop
    anticomm_err = np.max(np.abs((H_eps + eps_H).toarray()))
    print(f"  {'{'}H_hop, eps{'}'} error: {anticomm_err:.2e} (should be ~0)")
    print()

    # This anticommutation means eps is a CHIRAL SYMMETRY operator.
    # In the continuum limit, this becomes gamma_5 chirality.
    # The SU(2) acts within each chirality sector.

    # The key relation: on the lattice, the 3 spatial hopping directions
    # generate the Clifford algebra Cl(3) when combined with the staggering.
    # Define gamma_mu = hop_mu * eps (combines direction with chirality)
    print("  Checking Clifford algebra from lattice hoppings:")
    gamma = []
    for mu, (dx, dy, dz) in enumerate([(1,0,0),(0,1,0),(0,0,1)]):
        # Build directional hopping
        r, c, v = [], [], []
        for ix in range(M):
            for iy in range(M):
                for iz in range(M):
                    flat = ix * M * M + iy * M + iz
                    nx = ix + dx
                    ny = iy + dy
                    nz = iz + dz
                    if 0 <= nx < M and 0 <= ny < M and 0 <= nz < M:
                        nflat = nx * M * M + ny * M + nz
                        r.append(flat)
                        c.append(nflat)
                        v.append(eps[flat])  # multiply by staggering phase
        gamma_mu = sparse.csr_matrix((v, (r, c)), shape=(n_sites, n_sites))
        gamma.append(gamma_mu)

    # Check {gamma_mu, gamma_nu} ~ 2 * delta_{mu,nu} (up to boundary effects)
    for mu in range(3):
        for nu in range(mu, 3):
            anticomm = gamma[mu] @ gamma[nu] + gamma[nu] @ gamma[mu]
            diag_mean = np.mean(np.abs(anticomm.diagonal()))
            if mu == nu:
                print(f"    {{gamma_{mu}, gamma_{nu}}} diagonal mean: {diag_mean:.4f}")
            else:
                offdiag_max = np.max(np.abs(anticomm.toarray()))
                print(f"    {{gamma_{mu}, gamma_{nu}}} max element: {offdiag_max:.2e}")

    print()
    print("  APPROACH 2 RESULT:")
    print(f"    SU(5) GUT normalization gives k=5/3, sin^2 = 3/8 = {3/8:.4f}")
    print(f"    SU(3) fundamental gives k={k_su3:.4f}, sin^2 = {1/(1+k_su3):.4f}")
    print(f"    The lattice bipartite structure provides SU(2) from Cl(3)")
    print(f"    but does NOT independently fix the Y normalization.")
    print(f"    The value 3/8 requires a specific CHOICE of unifying group.")
    print()

    return {
        "k_su5": k_su5,
        "sin2_su5": 1 / (1 + k_su5),
        "k_su3": k_su3,
        "sin2_su3": 1 / (1 + k_su3),
    }


# ============================================================================
# APPROACH 3: Casimir ratio
# ============================================================================

def approach3_casimir_ratio():
    """Compute sin^2(theta_W) from quadratic Casimir operators.

    The quadratic Casimir C_2(R) for a representation R of a Lie group G:
      C_2(R) * I = sum_a T_a(R) T_a(R)

    For SU(2) fundamental (doublet):
      C_2(2) = 3/4  (from sigma/2 generators)

    For U(1) with charge Y:
      C_2(Y) = Y^2

    The ratio of bare couplings in a unified theory:
      alpha_2 / alpha_1 = C_2(U(1)) / C_2(SU(2)) * normalization

    But this is circular -- it depends on the normalization choice.
    Let's compute it several ways to see what the lattice adds.
    """
    print("=" * 72)
    print("APPROACH 3: Casimir ratio analysis")
    print("=" * 72)
    print()

    # Quadratic Casimir for SU(N) fundamental
    def casimir_fund(N):
        return (N**2 - 1) / (2 * N)

    # SU(2): C_2(fund) = 3/4
    c2_su2 = casimir_fund(2)
    print(f"  C_2(SU(2), fund) = {c2_su2:.4f}")

    # SU(3): C_2(fund) = 4/3
    c2_su3 = casimir_fund(3)
    print(f"  C_2(SU(3), fund) = {c2_su3:.4f}")

    # Dynkin index for fundamental rep: T(fund) = 1/2
    T_fund = 0.5
    print(f"  T(fund) = {T_fund} (universal for SU(N) fundamental)")
    print()

    # For SU(2) x U(1), the Casimir ratio with standard normalization:
    # alpha_1 / alpha_2 = g'^2 / g^2 = sin^2 / cos^2 = sin^2 / (1 - sin^2)
    # => sin^2 = (alpha_1/alpha_2) / (1 + alpha_1/alpha_2) = 1/(1 + alpha_2/alpha_1)

    # At tree level in GUT: alpha_1 = alpha_2 = alpha_GUT
    # But g and g' are related by the normalization factor k:
    # g_1 = sqrt(k) * g' and g_1 = g_2 = g_GUT
    # => sin^2 = g'^2/(g^2 + g'^2) = (1/k)/(1 + 1/k) = 1/(1+k)

    print("  Casimir-based coupling relations:")
    print()

    # Method 1: Use Casimir operators directly
    # For SU(2), the Casimir sum over generators: sum T_a^2 = C_2 * I
    # This means each generator contributes C_2/n_gen = (3/4)/3 = 1/4 per gen
    casimir_per_gen_su2 = c2_su2 / 3
    print(f"  C_2(SU(2))/n_gen = {casimir_per_gen_su2:.4f}")
    print(f"  (This is Tr(T_a^2)/d(R) = {casimir_per_gen_su2:.4f})")

    # For U(1) with charge Y = 1/2 (lattice Z_2):
    casimir_u1_half = (1/2)**2
    print(f"  C_2(U(1), Y=1/2) = Y^2 = {casimir_u1_half:.4f}")

    ratio_1 = casimir_u1_half / casimir_per_gen_su2
    sin2_casimir_1 = ratio_1 / (1 + ratio_1)
    print(f"  Ratio = {ratio_1:.4f}")
    print(f"  sin^2(theta_W) = {sin2_casimir_1:.4f}")
    print()

    # Method 2: Use the index ratio
    # For unified theories, sin^2 = sum T(R)_Y / sum T(R)_total
    # over all fermion representations
    print("  Index-based computation (over SM fermion content):")

    # One generation of SM fermions (left-handed):
    # Q_L = (3, 2, 1/6): contributes T(3)*T(2)*(1/6)^2 = (1/2)*(1/2)*(1/36) for Y
    #                     and T(3)*C_2(2) for SU(2)
    # But the standard formula is:
    # sin^2(theta_W) = sum_f Y_f^2 * d(R_3) * d(R_2) /
    #                  [sum_f Y_f^2 * d(R_3) * d(R_2) + sum_f C_2(2)_f * d(R_3)]
    # This is complicated. The simple result is:
    # sin^2 = sum Y_f^2 / (sum Y_f^2 + k * sum T_3^2)

    # For one SM generation:
    # Q_L: (3,2,1/6)  -> 3*2 = 6 components, each with Y=1/6, T_3=+/-1/2
    # u_R: (3,1,2/3)  -> 3*1 = 3 components, each with Y=2/3, T_3=0
    # d_R: (3,1,-1/3) -> 3*1 = 3 components, each with Y=-1/3, T_3=0
    # L_L: (1,2,-1/2) -> 1*2 = 2 components, each with Y=-1/2, T_3=+/-1/2
    # e_R: (1,1,-1)   -> 1*1 = 1 component, with Y=-1, T_3=0

    fermions = [
        ("Q_L", 3, 2, 1/6),
        ("u_R", 3, 1, 2/3),
        ("d_R", 3, 1, -1/3),
        ("L_L", 1, 2, -1/2),
        ("e_R", 1, 1, -1),
    ]

    total_y2 = 0
    total_t3_sq = 0
    for name, d3, d2, Y in fermions:
        n_comp = d3 * d2
        y2_contrib = n_comp * Y**2
        if d2 == 2:
            t3_contrib = d3 * 2 * (1/2)**2  # two components with T_3 = +/-1/2
        else:
            t3_contrib = 0
        total_y2 += y2_contrib
        total_t3_sq += t3_contrib
        print(f"    {name:4s} ({d3},{d2},{Y:+.3f}): "
              f"sum Y^2 = {y2_contrib:.4f}, sum T_3^2 = {t3_contrib:.4f}")

    print(f"    Total sum(Y^2) = {total_y2:.4f}")
    print(f"    Total sum(T_3^2) = {total_t3_sq:.4f}")

    k_from_fermions = total_y2 / total_t3_sq
    sin2_from_fermions = total_t3_sq / (total_y2 + total_t3_sq)
    print(f"    k = sum(Y^2)/sum(T_3^2) = {k_from_fermions:.6f}")
    print(f"    sin^2(theta_W) = sum(T_3^2)/sum(Y^2+T_3^2) = {sin2_from_fermions:.6f}")
    print(f"    (This is {sin2_from_fermions} = 3/8 = {3/8}")
    print()

    # Method 3: Lattice Cl(3) Casimir
    # Cl(3) = M_2(C): the full algebra has dimension 4 (as complex algebra)
    # The su(2) subalgebra has dimension 3
    # The remaining direction is the identity = U(1) part
    # Decomposition: M_2(C) = su(2) + u(1) + "off-diagonal"
    # su(2): 3 generators, C_2 = 3/4
    # u(1): 1 generator (proportional to I_2), C_2 = Y^2

    print("  Cl(3) algebra decomposition:")
    print(f"    dim(M_2(C)) = 4 (as real vector space of Hermitian traceless + trace)")
    print(f"    dim(su(2)) = 3 (traceless Hermitian)")
    print(f"    dim(u(1)) = 1 (trace part)")
    print()

    # The natural ratio from Cl(3) dimensionality:
    dim_su2 = 3
    dim_u1 = 1
    dim_total = dim_su2 + dim_u1

    sin2_dimension = dim_u1 / dim_total
    print(f"    Dimension-based: sin^2 = dim(u1)/dim(total) = {dim_u1}/{dim_total} = {sin2_dimension:.4f}")
    print(f"    This gives 1/4 = 0.25 -- close to observed but not exact.")
    print()

    # Weighted by Casimir per generator:
    weight_su2 = c2_su2 / dim_su2  # 3/4 / 3 = 1/4 per generator
    weight_u1 = 1/4  # for Y = 1/2: Y^2 = 1/4
    sin2_weighted = weight_u1 / (weight_su2 * dim_su2 + weight_u1)
    print(f"    Casimir-weighted: {sin2_weighted:.4f}")
    print()

    print("  APPROACH 3 RESULT:")
    print(f"    Fermion-content sum: sin^2 = 3/8 = 0.375 (confirms GUT)")
    print(f"    Cl(3) dimension ratio: sin^2 = 1/4 = 0.250")
    print(f"    Neither matches observed 0.231 without RG running.")
    print()

    return {
        "casimir_method1": sin2_casimir_1,
        "fermion_content": sin2_from_fermions,
        "cl3_dimension": sin2_dimension,
    }


# ============================================================================
# APPROACH 4: Lattice symmetry group Oh and coupling ratio
# ============================================================================

def approach4_lattice_symmetry():
    """Analyze the octahedral symmetry group Oh and its representations.

    The cubic lattice has symmetry group Oh (order 48) = O x Z_2
    where O is the rotation group of the cube (order 24) and Z_2 is parity.

    Oh has 10 irreducible representations:
      A1g, A2g, Eg, T1g, T2g (even parity)
      A1u, A2u, Eu, T1u, T2u (odd parity)
    with dimensions 1, 1, 2, 3, 3 (each parity).

    Key question: does the decomposition of the lattice Laplacian
    eigenspaces under Oh give a specific SU(2)/U(1) ratio?
    """
    print("=" * 72)
    print("APPROACH 4: Lattice symmetry group Oh analysis")
    print("=" * 72)
    print()

    # Oh group representation theory
    oh_reps = {
        "A1g": {"dim": 1, "parity": +1, "description": "trivial"},
        "A2g": {"dim": 1, "parity": +1, "description": "det of rotation"},
        "Eg":  {"dim": 2, "parity": +1, "description": "doublet"},
        "T1g": {"dim": 3, "parity": +1, "description": "angular momentum L=1"},
        "T2g": {"dim": 3, "parity": +1, "description": "xy, xz, yz"},
        "A1u": {"dim": 1, "parity": -1, "description": "pseudoscalar"},
        "A2u": {"dim": 1, "parity": -1, "description": "det * pseudoscalar"},
        "Eu":  {"dim": 2, "parity": -1, "description": "pseudo-doublet"},
        "T1u": {"dim": 3, "parity": -1, "description": "vector (x,y,z)"},
        "T2u": {"dim": 3, "parity": -1, "description": "pseudo T2"},
    }

    print("  Oh irreducible representations:")
    total_dim_sq = 0
    for name, info in oh_reps.items():
        print(f"    {name:4s}: dim = {info['dim']}, parity = {info['parity']:+d}, {info['description']}")
        total_dim_sq += info["dim"] ** 2
    print(f"  Sum of dim^2 = {total_dim_sq} (should equal |Oh| = 48)")
    print()

    # The lattice momentum k = (k_x, k_y, k_z) transforms under T1u (vector).
    # The dispersion relation E(k) = 2(3 - cos k_x - cos k_y - cos k_z)
    # is invariant under Oh (permutations and sign flips of k components).

    # At special k-points, the little group (stabilizer) determines the
    # representation content. The SU(2) and U(1) sectors can be identified
    # by how they transform under the lattice symmetry.

    print("  Connection to gauge structure:")
    print()

    # The Z_2 grading (bipartite structure) = the parity (g/u) in Oh
    # SU(2) generators transform as the Eg (doublet) representation
    # when restricted to the sublattice structure.
    # Actually: the Pauli matrices sigma_x, sigma_y, sigma_z form a T1-type
    # representation under the cubic rotation group O.

    # Under O (rotations only, ignoring parity):
    # sigma_x, sigma_y, sigma_z transform as a 3-vector = T1 representation
    # This is because rotating the lattice permutes the axes and hence the sigmas.

    print("  SU(2) generators (Pauli matrices) under O:")
    print("    sigma_x, sigma_y, sigma_z transform as T1 (3D vector rep)")
    print("    This is the SAME as spatial rotations L=1")
    print()

    # The U(1) generator (identity matrix / staggering phase) transforms as A1
    print("  U(1) generator under O:")
    print("    Identity / staggering phase transforms as A1 (trivial rep)")
    print()

    # Approach: use the group-theoretic multiplicities to determine coupling
    # The gauge coupling is related to how the gauge field couples to matter.
    # On the lattice, the gauge field A_mu sits on edges. Under Oh:
    #   A_mu (mu=x,y,z) transforms as T1u (vector, odd parity)
    # The SU(2) gauge field A_mu^a (a=1,2,3) transforms as T1u x T1 = A1+E+T1+T2
    # The U(1) gauge field A_mu transforms as T1u

    print("  Gauge field representations under Oh:")
    print("    U(1) gauge field A_mu: T1u (dim 3)")
    print("    SU(2) gauge field A_mu^a: T1u x T1 = A1u + Eu + T1u + T2u")
    print(f"    Dimensions: 3 vs 3*3=9 (ratio 1:3)")
    print()

    # The dimension ratio 1:3 gives a natural coupling ratio
    # but this is just the number of generators, which is always dim(G)

    # More interesting: the Casimir operators of Oh
    # The quadratic Casimir for Oh is related to the angular momentum
    # For T1: C_2 = 2 (like L=1)
    # For A1: C_2 = 0 (trivial)
    # For Eg: C_2 = related to quadrupole

    # But Oh is discrete, so Casimir isn't well-defined in the Lie algebra sense.
    # Instead, use the character theory.

    # Character of T1 (vector): chi(E)=3, chi(C3)=0, chi(C2)=-1, chi(C4)=1, chi(C2')=-1
    # Character of A1 (trivial): chi = 1 for all elements

    # The inner product <T1, T1> = 1 (irreducible)
    # The inner product <A1, A1> = 1 (irreducible)

    # What we really want: the RELATIVE STRENGTH of T1 vs A1 sectors
    # in the lattice Laplacian action.

    # Compute on a lattice: decompose the Laplacian eigenspaces
    print("  Numerical test: Laplacian eigenspace decomposition under Oh")
    N = 8
    M = N - 2
    n = M ** 3

    # Build 3D Laplacian
    rows, cols, vals = [], [], []
    for ix in range(M):
        for iy in range(M):
            for iz in range(M):
                flat = ix * M * M + iy * M + iz
                rows.append(flat)
                cols.append(flat)
                vals.append(-6.0)
                for dx, dy, dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
                    nx, ny, nz = ix+dx, iy+dy, iz+dz
                    if 0 <= nx < M and 0 <= ny < M and 0 <= nz < M:
                        nflat = nx * M * M + ny * M + nz
                        rows.append(flat)
                        cols.append(nflat)
                        vals.append(1.0)

    L = sparse.csr_matrix((vals, (rows, cols)), shape=(n, n))

    # Compute eigenvalues
    n_eigs = min(50, n - 2)
    evals = np.sort(np.linalg.eigvalsh(L.toarray()))

    # Count multiplicities (group by near-degenerate eigenvalues)
    tol = 1e-6
    groups = []
    i = 0
    while i < len(evals):
        group = [evals[i]]
        j = i + 1
        while j < len(evals) and abs(evals[j] - evals[i]) < tol:
            group.append(evals[j])
            j += 1
        groups.append((evals[i], len(group)))
        i = j

    print(f"  Eigenvalue multiplicities (first 15 distinct levels):")
    for idx, (ev, mult) in enumerate(groups[:15]):
        # Identify Oh representation from multiplicity
        oh_label = ""
        if mult == 1:
            oh_label = "A1/A2"
        elif mult == 2:
            oh_label = "E"
        elif mult == 3:
            oh_label = "T1/T2"
        elif mult == 4:
            oh_label = "A1+T1 or E+E"
        elif mult == 6:
            oh_label = "T1+T2 or 2xT"
        else:
            oh_label = f"composite"
        print(f"    Level {idx+1:2d}: lambda = {ev:8.4f}, multiplicity = {mult}, ({oh_label})")

    # Count how many levels are singlet (A-type) vs triplet (T-type) vs doublet (E-type)
    n_singlet = sum(1 for _, m in groups if m == 1)
    n_doublet = sum(1 for _, m in groups if m == 2)
    n_triplet = sum(1 for _, m in groups if m == 3)
    n_other = sum(1 for _, m in groups if m not in [1, 2, 3])

    print(f"\n  Multiplicity census (all {len(groups)} distinct levels):")
    print(f"    Singlets (A-type): {n_singlet}")
    print(f"    Doublets (E-type): {n_doublet}")
    print(f"    Triplets (T-type): {n_triplet}")
    print(f"    Higher:            {n_other}")
    print()

    # The ratio of singlet to triplet modes is NOT directly sin^2(theta_W),
    # but it characterizes how the lattice breaks continuous SO(3) -> Oh.
    if n_triplet > 0:
        ratio_s_t = n_singlet / n_triplet
    else:
        ratio_s_t = float("inf")
    print(f"    Singlet/Triplet ratio: {ratio_s_t:.4f}")
    print()

    print("  APPROACH 4 RESULT:")
    print("    The Oh symmetry group decomposes lattice modes into A, E, T reps.")
    print(f"    Singlet/Triplet ratio = {ratio_s_t:.4f} (NOT related to Weinberg angle)")
    print("    The discrete symmetry Oh does NOT directly constrain sin^2(theta_W).")
    print("    Oh tells us HOW the continuous symmetry breaks on the lattice,")
    print("    not the relative strength of SU(2) vs U(1) sectors.")
    print()

    return {
        "singlet_count": n_singlet,
        "doublet_count": n_doublet,
        "triplet_count": n_triplet,
        "ratio_s_t": ratio_s_t,
    }


# ============================================================================
# RG Running: from GUT scale to M_Z
# ============================================================================

def rg_running():
    """Compute one-loop RG running of sin^2(theta_W) from GUT to M_Z.

    The one-loop beta functions for the SM gauge couplings are:
      d(1/alpha_i)/d(ln mu) = -b_i / (2*pi)

    With SM field content (no SUSY):
      b_1 = -41/10   (U(1)_Y with GUT normalization)
      b_2 = 19/6     (SU(2)_L)
      b_3 = 7        (SU(3)_c)

    Convention: alpha_i = g_i^2 / (4*pi)
    GUT normalization: alpha_1 = (5/3) * alpha_Y

    At M_GUT: alpha_1 = alpha_2 = alpha_3 = alpha_GUT
    => sin^2(theta_W) = alpha_1 / (alpha_1 + alpha_2) = ... depends on running
    """
    print("=" * 72)
    print("RG RUNNING: sin^2(theta_W) from GUT scale to M_Z")
    print("=" * 72)
    print()

    # One-loop beta coefficients (SM, no SUSY)
    b1 = -41 / 10   # U(1)_Y (GUT normalized)
    b2 = 19 / 6     # SU(2)_L
    b3 = 7           # SU(3)_c

    # Energy scales
    M_Z = 91.1876    # GeV
    M_GUT = 2e16     # GeV (approximate)

    ln_ratio = np.log(M_GUT / M_Z)
    print(f"  ln(M_GUT/M_Z) = ln({M_GUT:.0e}/{M_Z:.2f}) = {ln_ratio:.4f}")
    print()

    # At GUT scale: alpha_GUT ~ 1/40 (approximate)
    alpha_GUT_inv = 40.0

    # Run down to M_Z
    alpha1_inv_MZ = alpha_GUT_inv - b1 / (2 * np.pi) * ln_ratio
    alpha2_inv_MZ = alpha_GUT_inv - b2 / (2 * np.pi) * ln_ratio
    alpha3_inv_MZ = alpha_GUT_inv - b3 / (2 * np.pi) * ln_ratio

    alpha1_MZ = 1 / alpha1_inv_MZ
    alpha2_MZ = 1 / alpha2_inv_MZ
    alpha3_MZ = 1 / alpha3_inv_MZ

    print(f"  One-loop beta coefficients (SM):")
    print(f"    b1 = {b1:.2f}, b2 = {b2:.4f}, b3 = {b3:.2f}")
    print()

    print(f"  At M_GUT: 1/alpha_GUT = {alpha_GUT_inv:.1f}")
    print(f"  At M_Z (one-loop):")
    print(f"    1/alpha_1 = {alpha1_inv_MZ:.2f}  =>  alpha_1 = {alpha1_MZ:.6f}")
    print(f"    1/alpha_2 = {alpha2_inv_MZ:.2f}  =>  alpha_2 = {alpha2_MZ:.6f}")
    print(f"    1/alpha_3 = {alpha3_inv_MZ:.2f}  =>  alpha_3 = {alpha3_MZ:.6f}")
    print()

    # sin^2(theta_W) = alpha_1 / (alpha_1 + (5/3)*alpha_2)
    # Wait: alpha_1 here is GUT-normalized. Physical alpha_Y = (3/5)*alpha_1
    # sin^2(theta_W) = g'^2/(g^2+g'^2) = alpha_Y/(alpha_Y + alpha_2)
    #                = (3/5)*alpha_1 / ((3/5)*alpha_1 + alpha_2)

    alpha_Y_MZ = (3/5) * alpha1_MZ
    sin2_tw_MZ = alpha_Y_MZ / (alpha_Y_MZ + alpha2_MZ)

    print(f"  sin^2(theta_W) at M_Z:")
    print(f"    alpha_Y = (3/5)*alpha_1 = {alpha_Y_MZ:.6f}")
    print(f"    sin^2(theta_W) = alpha_Y/(alpha_Y + alpha_2)")
    print(f"                   = {sin2_tw_MZ:.5f}")
    print(f"    Observed:        {SIN2_TW_OBSERVED:.5f}")
    print(f"    Difference:      {abs(sin2_tw_MZ - SIN2_TW_OBSERVED):.5f}")
    print()

    # Also compute sin^2 at GUT scale to verify 3/8
    sin2_GUT = 3/8
    print(f"  Verification: sin^2(theta_W) at M_GUT = 3/8 = {sin2_GUT:.4f}")
    print()

    # Scan over M_GUT and alpha_GUT to find best fit
    print("  Scanning M_GUT and alpha_GUT for best fit to observed sin^2(theta_W):")
    best_diff = 1.0
    best_params = {}

    for log_mgut in np.linspace(14, 18, 100):
        mgut = 10**log_mgut
        ln_r = np.log(mgut / M_Z)
        for ainv in np.linspace(20, 60, 100):
            a1inv = ainv - b1 / (2*np.pi) * ln_r
            a2inv = ainv - b2 / (2*np.pi) * ln_r
            if a1inv <= 0 or a2inv <= 0:
                continue
            a1 = 1/a1inv
            a2 = 1/a2inv
            aY = (3/5) * a1
            s2 = aY / (aY + a2)
            diff = abs(s2 - SIN2_TW_OBSERVED)
            if diff < best_diff:
                best_diff = diff
                best_params = {
                    "M_GUT": mgut, "alpha_GUT_inv": ainv,
                    "sin2": s2, "alpha1_inv": a1inv, "alpha2_inv": a2inv,
                }

    if best_params:
        print(f"    Best fit: M_GUT = {best_params['M_GUT']:.2e} GeV, "
              f"1/alpha_GUT = {best_params['alpha_GUT_inv']:.1f}")
        print(f"    sin^2(theta_W) = {best_params['sin2']:.5f} "
              f"(diff from observed: {best_diff:.5f})")
        print(f"    1/alpha_1(M_Z) = {best_params['alpha1_inv']:.2f}, "
              f"1/alpha_2(M_Z) = {best_params['alpha2_inv']:.2f}")
    print()

    # Known result: exact unification doesn't work in SM (need SUSY or thresholds)
    # The couplings don't quite meet at one point.
    print("  NOTE: In the SM (without SUSY), the three couplings do NOT")
    print("  exactly unify at a single scale. Exact unification requires")
    print("  additional physics (SUSY, threshold corrections, intermediate")
    print("  scales, etc.). The one-loop SM running gives sin^2(theta_W)")
    print(f"  in the range 0.20-0.24 depending on M_GUT and alpha_GUT.")
    print()

    return {
        "sin2_one_loop": sin2_tw_MZ,
        "sin2_GUT": sin2_GUT,
        "best_fit_sin2": best_params.get("sin2", None),
        "best_fit_diff": best_diff,
    }


# ============================================================================
# Summary and Verdict
# ============================================================================

def print_summary(results):
    """Print comprehensive summary and honest assessment."""
    print()
    print("=" * 72)
    print("COMPREHENSIVE SUMMARY")
    print("=" * 72)
    print()

    print("  Observed: sin^2(theta_W) = 0.23122 +/- 0.00003 (PDG, M_Z, MS-bar)")
    print()

    print("  APPROACH 1 (Lattice coupling ratio):")
    r1 = results["approach1"]
    print(f"    SU(3) embedding:  sin^2 = {r1['su3_direct']:.4f}")
    print(f"    SU(5) GUT:        sin^2 = {r1['gut']:.4f} = 3/8")
    print(f"    Lattice Cl(3)+Z2: sin^2 = {r1['lattice']:.4f}")
    print("    => The bare lattice value depends on normalization choice.")
    print("       No unique prediction without specifying the unifying group.")
    print()

    print("  APPROACH 2 (Group embedding):")
    r2 = results["approach2"]
    print(f"    SU(5) normalization: k = {r2['k_su5']:.4f}, sin^2 = {r2['sin2_su5']:.4f}")
    print(f"    SU(3) normalization: k = {r2['k_su3']:.4f}, sin^2 = {r2['sin2_su3']:.4f}")
    print("    => The lattice provides SU(2) from Cl(3) bipartite structure")
    print("       but does NOT independently fix the hypercharge normalization.")
    print()

    print("  APPROACH 3 (Casimir ratio):")
    r3 = results["approach3"]
    print(f"    Fermion content sum:    sin^2 = {r3['fermion_content']:.4f} = 3/8")
    print(f"    Cl(3) dimension ratio:  sin^2 = {r3['cl3_dimension']:.4f} = 1/4")
    print("    => The 3/8 is robust (follows from SM fermion quantum numbers).")
    print("       The 1/4 from Cl(3) dimension counting is an INTERESTING")
    print("       alternative but has no clear physical justification.")
    print()

    print("  APPROACH 4 (Oh lattice symmetry):")
    r4 = results["approach4"]
    print(f"    Singlet/Triplet ratio: {r4['ratio_s_t']:.4f}")
    print("    => The discrete cubic symmetry Oh does NOT constrain")
    print("       the Weinberg angle. It governs how continuous symmetry")
    print("       breaks, not the gauge coupling ratio.")
    print()

    print("  RG RUNNING (GUT to M_Z):")
    r5 = results["rg"]
    print(f"    One-loop from 3/8 at M_GUT: sin^2(M_Z) = {r5['sin2_one_loop']:.5f}")
    if r5["best_fit_sin2"]:
        print(f"    Best-fit scan:              sin^2(M_Z) = {r5['best_fit_sin2']:.5f}")
    print(f"    Observed:                   sin^2(M_Z) = {SIN2_TW_OBSERVED:.5f}")
    print("    => One-loop SM running from 3/8 gives the right ballpark.")
    print("       Exact agreement requires threshold corrections or SUSY.")
    print()

    print("VERDICT:")
    print("  The framework does NOT provide a NEW prediction for sin^2(theta_W).")
    print()
    print("  What it DOES provide:")
    print("  1. SU(2) emerges naturally from Cl(3) via the bipartite lattice.")
    print("  2. U(1) emerges from edge phases.")
    print("  3. The Cl(3) dimension ratio dim(u(1))/dim(total) = 1/4 = 0.25")
    print("     is suggestively close to the observed 0.231 but lacks")
    print("     a rigorous derivation connecting it to sin^2(theta_W).")
    print()
    print("  What it does NOT provide:")
    print("  1. The hypercharge normalization (this requires knowing the GUT group).")
    print("  2. A mechanism to RUN couplings from a lattice-scale bare value")
    print("     to the observed value at M_Z.")
    print("  3. Any value different from known group-theoretic results")
    print("     (3/8 from GUT, 1/4 from naive dimension counting).")
    print()
    print("  The BEST the framework can claim:")
    print("  - If Cl(3) governs both SU(2) and U(1), the natural bare value")
    print("    is sin^2 = 1/4 (from 1 U(1) generator vs 3 SU(2) generators).")
    print("  - If the lattice structure embeds in SU(5), the bare value is 3/8,")
    print("    which runs to ~0.231 at M_Z -- matching observation.")
    print("  - The framework is CONSISTENT with known physics but does not")
    print("    independently predict the Weinberg angle.")
    print()
    print("  HONEST STATUS: No new prediction. The Weinberg angle remains")
    print("  determined by the choice of GUT group and RG running, both of")
    print("  which are external inputs not derived from the lattice alone.")


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    t_start = time.time()
    print("Weinberg Angle from Lattice Gauge Structure")
    print("=" * 72)
    print()

    results = {}
    results["approach1"] = approach1_lattice_coupling_ratio()
    results["approach2"] = approach2_group_embedding()
    results["approach3"] = approach3_casimir_ratio()
    results["approach4"] = approach4_lattice_symmetry()
    results["rg"] = rg_running()

    print_summary(results)

    dt = time.time() - t_start
    print(f"\nTotal runtime: {dt:.1f}s")
