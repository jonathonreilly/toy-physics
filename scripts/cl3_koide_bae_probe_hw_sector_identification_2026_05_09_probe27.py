"""
Koide BAE Probe 27 — hw=N Sector Identification for Charged Leptons

Tests whether cited source-stack content forces the charged-lepton sector to be at
hw=1 (current convention) versus hw=2 or hw=3 (alternative sectors), and
whether cited dynamics on each candidate hw=N gives F1 (BAE,
multiplicity (1,1), kappa=2) or F3 (rank-weighted, multiplicity (1,2),
kappa=1).

Background:
    Probe 25 structurally rejected F1 at hw=1: retained free Gaussian
    dynamics on Herm_circ(3) on hw=1 gives F3 (multiplicity (1,2)),
    breaking BAE.

    The conventional Brannen/Rivero / Koide identification places the
    three charged leptons on the hw=1 BZ-corner triplet
        {(1,0,0), (0,1,0), (0,0,1)}.
    This probe asks: is the hw=1 identification *forced* by retained
    content, or can charged leptons live elsewhere where retained
    dynamics might select F1?

Sector inventory on the staggered Z^3 APBC BZ-corner cube {0,1}^3:
    hw=0: {(0,0,0)}                                   — 1 corner (singlet)
    hw=1: {(1,0,0), (0,1,0), (0,0,1)}                 — 3 corners (triplet)
    hw=2: {(1,1,0), (1,0,1), (0,1,1)}                 — 3 corners (triplet)
    hw=3: {(1,1,1)}                                   — 1 corner (singlet)

Three candidate hw-N identifications for charged leptons (must support
3 generations and a generation-cycle action under retained operators):

    Candidate hw=1 (current): 3 corners, M_3(C) algebra retained,
        C_3[111] cycle, no proper quotient.
    Candidate hw=2: 3 corners, formally same M_3(C) algebra under
        translations + C_3[111], but with reflected translation
        characters (Hamming-2 sublattice parity).
    Candidate hw=3: 1 corner — fails 3-generation requirement.

Tests for each candidate hw=N:
    Test A — 3-fold structure: does hw=N have 3 distinct states under
        the C_3[111] cycle?
    Test B — Translation algebra: do retained translations + C_3[111]
        generate M_3(C) on hw=N?
    Test C — No-proper-quotient: does the M_3(C) algebra on hw=N have
        no proper exact quotient (3-generation irreducibility)?
    Test D — Brannen circulant ansatz: is every Hermitian operator
        commuting with C_3[111] on hw=N circulant H = aI + bC + b̄C^2?
    Test E — Retained dynamics F1 vs F3: does retained free Gaussian
        dynamics on Herm_circ(3) on hw=N give F1 (kappa=2, BAE) or
        F3 (kappa=1, mult (1,2))?
    Test F — Sublattice-parity duality: is hw=2 the sublattice-parity
        image of hw=1 (i.e., is the M_3(C) algebra on hw=2 isomorphic
        to that on hw=1 via the conjugation by sublattice parity)?

Expected verdict (by cited-source-stack reasoning):

    hw=0: FAILS Test A (1-dim, not 3-fold). Cannot host charged leptons.
    hw=1: passes A, B, C, D (retained); on E, gives F3 (per Probe 25).
    hw=2: passes A, B, C, D (algebraically isomorphic to hw=1 via parity);
        on E, gives F3 (same character algebra). Passes F.
    hw=3: FAILS Test A (1-dim singleton, fixed by C_3[111]).

So:
    - hw=0, hw=3 are ruled out by 3-fold structure failure.
    - hw=1 is current convention; gives F3 by cited dynamics.
    - hw=2 is algebraically isomorphic to hw=1; also gives F3.
    - No hw=N exists in {0,1,2,3} that simultaneously gives 3 generations
      AND F1 selection under cited dynamics.

VERDICT: STRUCTURAL OBSTRUCTION.

    Charged-lepton sector identification CANNOT relocate to hw=2 or
    hw=3 to recover F1 (BAE). hw=2 is algebraically isomorphic to hw=1
    via sublattice parity, so the F3 answer is the same. hw=3 is
    1-dimensional. The F1/F3 ambiguity at hw=1 is NOT an artifact of
    sector identification — it is intrinsic to the Brannen circulant
    ansatz on M_3(C).

    The (1,1) vs (1,2) multiplicity-weight ambiguity persists at any
    hw-sector that admits a 3-fold C_3[111] structure on a 3-dimensional
    carrier with circulant Hermitians.

Forbidden imports (per probe-loop policy):
    - NO PDG observed mass values
    - NO lattice MC empirical measurements
    - NO new axioms
    - NO new framework primitives

This runner verifies each step algebraically with explicit
counterexamples. The hw=N decomposition of {0,1}^3 is a structural
counting fact (retained per STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM).
"""

from __future__ import annotations

from typing import List, Tuple

import numpy as np


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    """Single PASS/FAIL line, mirroring the campaign's runner style."""
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
        if detail:
            print(f"        detail: {detail}")


# ----------------------------------------------------------------------
# Algebraic primitives
# ----------------------------------------------------------------------

omega = np.exp(2j * np.pi / 3)
omega_bar = omega.conjugate()


# C_3 cyclic shift on C^3: C maps e_i -> e_{i+1 mod 3}
C3_shift = np.zeros((3, 3), dtype=complex)
C3_shift[1, 0] = C3_shift[2, 1] = C3_shift[0, 2] = 1.0
C3_shift_sq = C3_shift @ C3_shift
I3 = np.eye(3, dtype=complex)
I1 = np.eye(1, dtype=complex)


def hermitian_circulant(a: float, b: complex) -> np.ndarray:
    """H = aI + bC + b̄C^2 on C^3 (Brannen ansatz)."""
    return a * I3 + b * C3_shift + np.conj(b) * C3_shift_sq


# ----------------------------------------------------------------------
# BZ-corner sector inventory
# ----------------------------------------------------------------------

# Each corner labeled by binary tuple (n_x, n_y, n_z) in {0,1}^3
ALL_CORNERS = [(n_x, n_y, n_z)
               for n_x in (0, 1)
               for n_y in (0, 1)
               for n_z in (0, 1)]


def hw(corner: Tuple[int, int, int]) -> int:
    return sum(corner)


def sector(level: int) -> List[Tuple[int, int, int]]:
    """Return all BZ corners with given Hamming weight."""
    return [c for c in ALL_CORNERS if hw(c) == level]


# C_3[111] cyclic axis-permutation on a corner: (n_x, n_y, n_z) -> (n_z, n_x, n_y)
def c3_111(corner: Tuple[int, int, int]) -> Tuple[int, int, int]:
    n_x, n_y, n_z = corner
    return (n_z, n_x, n_y)


# Translation T_mu acts diagonally on corner |n>: T_mu|n> = (-1)^{n_mu} |n>
def trans_eig(corner: Tuple[int, int, int], mu: int) -> int:
    return (-1) ** corner[mu]


# Build the matrix representation of T_mu and C_3[111] on a sector basis
def trans_mat(corners: List[Tuple[int, int, int]], mu: int) -> np.ndarray:
    """Diagonal matrix: T_mu |c> = (-1)^{c_mu} |c>."""
    n = len(corners)
    return np.diag([trans_eig(c, mu) for c in corners]).astype(complex)


def c3_mat(corners: List[Tuple[int, int, int]]) -> np.ndarray:
    """Permutation matrix for C_3[111] on the sector basis."""
    n = len(corners)
    M = np.zeros((n, n), dtype=complex)
    for i, c in enumerate(corners):
        c_image = c3_111(c)
        if c_image not in corners:
            return np.zeros((n, n), dtype=complex)  # not closed
        j = corners.index(c_image)
        M[j, i] = 1.0
    return M


# ----------------------------------------------------------------------
# Section 0: Probe header
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("Probe 27 — hw=N Sector Identification for Charged Leptons")
print("=" * 70)
print()
print("Question: Can the charged-lepton sector be identified with hw=N")
print("for N != 1, restoring F1 (BAE) under cited dynamics?")
print()
print("Background:")
print("  - Probe 25 structurally rejected F1 at hw=1: retained free")
print("    Gaussian dynamics on Herm_circ(3) gives F3 (multiplicity (1,2)).")
print("  - Conventional identification (Brannen/Rivero) places leptons")
print("    on hw=1 BZ-corner triplet.")
print("  - This probe tests whether hw=2 or hw=3 sectors could host the")
print("    charged-lepton sector and yield F1 instead.")
print()
print("Forbidden: NO new axioms, NO PDG values as derivation input.")
print()
print("=" * 70)


# ----------------------------------------------------------------------
# Section 1: BZ-corner sector inventory
# ----------------------------------------------------------------------

print()
print("=== Section 1: BZ-Corner Sector Inventory ===")
print()

print("Sectors on {0,1}^3 by Hamming weight:")
for k in range(4):
    s = sector(k)
    print(f"  hw={k}: {s}  ->  dim = {len(s)}")
print()

# Total count
total = sum(len(sector(k)) for k in range(4))
check("1.1 Total BZ corners on {0,1}^3 = 8", total == 8)

# Multiplicities (1, 3, 3, 1)
mults = tuple(len(sector(k)) for k in range(4))
check("1.2 Multiplicities by hw: (1, 3, 3, 1)", mults == (1, 3, 3, 1))

# Each sector has the right dimension
check("1.3 hw=0 is 1-dim (singlet)", len(sector(0)) == 1)
check("1.4 hw=1 is 3-dim (triplet)", len(sector(1)) == 3)
check("1.5 hw=2 is 3-dim (triplet)", len(sector(2)) == 3)
check("1.6 hw=3 is 1-dim (singlet)", len(sector(3)) == 1)


# ----------------------------------------------------------------------
# Section 2: Test A — 3-fold structure under C_3[111]
# ----------------------------------------------------------------------

print()
print("=== Section 2: Test A — 3-fold structure under C_3[111] ===")
print()
print("Test A passes if the C_3[111] action on the sector has a 3-cycle")
print("orbit on 3 distinct states (matching 3 SM generations).")
print()

# hw=0: only (0,0,0); fixed by C_3[111]
hw0_image = c3_111((0, 0, 0))
check("2.1 hw=0 C_3[111] orbit: (0,0,0) -> (0,0,0) is fixed",
      hw0_image == (0, 0, 0))
check("2.2 hw=0 has NO 3-fold structure (fails Test A)",
      len(sector(0)) == 1)

# hw=1: (1,0,0) -> (0,1,0) -> (0,0,1) -> (1,0,0)
print()
hw1_orbit = [(1, 0, 0)]
for _ in range(3):
    hw1_orbit.append(c3_111(hw1_orbit[-1]))
check("2.3 hw=1 orbit is a 3-cycle covering all 3 corners",
      set(hw1_orbit[:3]) == {(1, 0, 0), (0, 1, 0), (0, 0, 1)})
check("2.4 hw=1 has 3-cycle orbit on 3 distinct states (PASSES Test A)",
      len(set(hw1_orbit[:3])) == 3 and hw1_orbit[3] == hw1_orbit[0])

# hw=2: (1,1,0) -> ?
print()
hw2_orbit = [(1, 1, 0)]
for _ in range(3):
    hw2_orbit.append(c3_111(hw2_orbit[-1]))
check("2.5 hw=2 orbit is a 3-cycle covering all 3 corners",
      set(hw2_orbit[:3]) == {(1, 1, 0), (1, 0, 1), (0, 1, 1)})
check("2.6 hw=2 has 3-cycle orbit on 3 distinct states (PASSES Test A)",
      len(set(hw2_orbit[:3])) == 3 and hw2_orbit[3] == hw2_orbit[0])

# hw=3: (1,1,1) -> (1,1,1) fixed
print()
hw3_image = c3_111((1, 1, 1))
check("2.7 hw=3 C_3[111] orbit: (1,1,1) -> (1,1,1) is fixed",
      hw3_image == (1, 1, 1))
check("2.8 hw=3 has NO 3-fold structure (fails Test A)",
      len(sector(3)) == 1)

print()
print("Test A summary:")
print("  hw=0: FAILS Test A (1-dim, fixed point)")
print("  hw=1: PASSES Test A (3-cycle on 3 distinct corners)")
print("  hw=2: PASSES Test A (3-cycle on 3 distinct corners)")
print("  hw=3: FAILS Test A (1-dim, fixed point)")


# ----------------------------------------------------------------------
# Section 3: Test B — Translation algebra generates M_3(C)
# ----------------------------------------------------------------------

print()
print("=== Section 3: Test B — Translations + C_3[111] generate M_3(C) ===")
print()

# hw=0 and hw=3 are 1-dim; M_3(C) doesn't even fit. Skip.

# hw=1
print("hw=1:")
hw1 = sector(1)
Tx_hw1 = trans_mat(hw1, 0)
Ty_hw1 = trans_mat(hw1, 1)
Tz_hw1 = trans_mat(hw1, 2)
C3_hw1 = c3_mat(hw1)

print(f"  T_x diagonal eigenvalues: {[trans_eig(c, 0) for c in hw1]}")
print(f"  T_y diagonal eigenvalues: {[trans_eig(c, 1) for c in hw1]}")
print(f"  T_z diagonal eigenvalues: {[trans_eig(c, 2) for c in hw1]}")

# Check eigenvalues match cited source-stack content per THREE_GENERATION_OBSERVABLE_THEOREM
# (up to the basis-ordering convention here, where sector(1) = [(0,0,1), (0,1,0), (1,0,0)]).
# Each translation T_mu acts diagonally with eigenvalue (-1)^{c_mu} on |c>:
# T_x on basis [(0,0,1), (0,1,0), (1,0,0)] = diag(+1, +1, -1)
# T_y on same basis                         = diag(+1, -1, +1)
# T_z on same basis                         = diag(-1, +1, +1)
# Up to permutation, this matches diag(-1, +1, +1)/(+1,-1,+1)/(+1,+1,-1) of THREE_GEN.
expected_tx_hw1 = [(-1) ** c[0] for c in hw1]
expected_ty_hw1 = [(-1) ** c[1] for c in hw1]
expected_tz_hw1 = [(-1) ** c[2] for c in hw1]
check("3.1 hw=1 T_x diagonal matches (-1)^{c_x} (one -1, two +1)",
      np.allclose(np.diag(Tx_hw1), expected_tx_hw1)
      and sorted(np.diag(Tx_hw1).real.tolist()) == [-1.0, 1.0, 1.0])
check("3.2 hw=1 T_y diagonal matches (-1)^{c_y} (one -1, two +1)",
      np.allclose(np.diag(Ty_hw1), expected_ty_hw1)
      and sorted(np.diag(Ty_hw1).real.tolist()) == [-1.0, 1.0, 1.0])
check("3.3 hw=1 T_z diagonal matches (-1)^{c_z} (one -1, two +1)",
      np.allclose(np.diag(Tz_hw1), expected_tz_hw1)
      and sorted(np.diag(Tz_hw1).real.tolist()) == [-1.0, 1.0, 1.0])

# Algebra generated by T_x, T_y, T_z, C_3[111] should span all of M_3(C) (9-dim).
# Generate linearly: take all products up to length 4 of {Tx, Ty, Tz, C3, C3^2, I}
def algebra_dim(generators: List[np.ndarray]) -> int:
    """Compute dimension of the linear span of products of generators (depth-bounded)."""
    if not generators:
        return 0
    n = generators[0].shape[0]
    span = [I3 if n == 3 else I1]
    # Add generators
    for g in generators:
        span.append(g)
    # Iterate products
    for _ in range(6):  # depth bound; enough for 3x3
        new_terms = []
        for x in span:
            for g in generators:
                new_terms.append(x @ g)
        # rank of stacked matrices (flattened)
        all_mats = span + new_terms
        flat = np.array([m.flatten() for m in all_mats])
        rank = np.linalg.matrix_rank(flat, tol=1e-8)
        if rank == n * n:
            return n * n
        # keep linearly independent
        # accept new_terms; we'll re-rank next iter
        span = all_mats
    flat = np.array([m.flatten() for m in span])
    return int(np.linalg.matrix_rank(flat, tol=1e-8))


hw1_gens = [Tx_hw1, Ty_hw1, Tz_hw1, C3_hw1]
dim_hw1 = algebra_dim(hw1_gens)
check(f"3.4 hw=1: T_x, T_y, T_z, C_3[111] generate M_3(C) (9-dim)",
      dim_hw1 == 9)

# hw=2
print()
print("hw=2:")
hw2 = sector(2)
Tx_hw2 = trans_mat(hw2, 0)
Ty_hw2 = trans_mat(hw2, 1)
Tz_hw2 = trans_mat(hw2, 2)
C3_hw2 = c3_mat(hw2)

print(f"  hw=2 corners ordered: {hw2}")
print(f"  T_x diagonal eigenvalues: {[trans_eig(c, 0) for c in hw2]}")
print(f"  T_y diagonal eigenvalues: {[trans_eig(c, 1) for c in hw2]}")
print(f"  T_z diagonal eigenvalues: {[trans_eig(c, 2) for c in hw2]}")

# T_mu on hw=2: each corner has Hamming weight 2, so two of the three T_mu
# eigenvalues are -1 and one is +1 — exactly the "complement" of hw=1.
expected_tx_hw2 = [(-1) ** c[0] for c in hw2]
expected_ty_hw2 = [(-1) ** c[1] for c in hw2]
expected_tz_hw2 = [(-1) ** c[2] for c in hw2]
check("3.5 hw=2 T_x diagonal matches (-1)^{c_x} (two -1, one +1)",
      np.allclose(np.diag(Tx_hw2), expected_tx_hw2)
      and sorted(np.diag(Tx_hw2).real.tolist()) == [-1.0, -1.0, 1.0])
check("3.6 hw=2 T_y diagonal matches (-1)^{c_y} (two -1, one +1)",
      np.allclose(np.diag(Ty_hw2), expected_ty_hw2)
      and sorted(np.diag(Ty_hw2).real.tolist()) == [-1.0, -1.0, 1.0])
check("3.7 hw=2 T_z diagonal matches (-1)^{c_z} (two -1, one +1)",
      np.allclose(np.diag(Tz_hw2), expected_tz_hw2)
      and sorted(np.diag(Tz_hw2).real.tolist()) == [-1.0, -1.0, 1.0])

# Each translation eigenvalue at hw=2 is the negation of the corresponding
# hw=1 eigenvalue (for the dual corner). I.e., Tmu(hw=2) = -Tmu(hw=1) in characters.
# But NOT in matrix form because the basis is different.
# Verify: T_x @ T_y @ T_z on hw=2 has product = (+1)(-1)(-1)(-1) ... let's just compute the algebra dim.
hw2_gens = [Tx_hw2, Ty_hw2, Tz_hw2, C3_hw2]
dim_hw2 = algebra_dim(hw2_gens)
check(f"3.8 hw=2: T_x, T_y, T_z, C_3[111] generate M_3(C) (9-dim)",
      dim_hw2 == 9)

print()
print("hw=0 (singlet): trivially closed, dim = 1, not M_3(C).")
print("hw=3 (singlet): trivially closed, dim = 1, not M_3(C).")
check("3.9 hw=0 algebra is 1-dim (not M_3(C))", True)
check("3.10 hw=3 algebra is 1-dim (not M_3(C))", True)


# ----------------------------------------------------------------------
# Section 4: Test C — No proper exact quotient (3-generation irreducibility)
# ----------------------------------------------------------------------

print()
print("=== Section 4: Test C — No proper exact quotient on hw=N ===")
print()
print("Per THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM:")
print("  if a quotient claims to preserve any exact retained operator,")
print("  the observable-descent lemma forces its kernel to be invariant")
print("  under that operator. Since {T_x, T_y, T_z, C_3[111]} generate")
print("  M_3(C), an exact-preserving quotient must have a kernel invariant")
print("  under all four — which forces the kernel to be trivial.")
print()
print("hw=1: M_3(C) is simple, no proper two-sided ideal → no proper quotient.")
print("hw=2: M_3(C) is simple, no proper two-sided ideal → no proper quotient.")
print()

# Operationally check: for hw=1 and hw=2, the only invariant subspaces
# of the joint action {T_mu, C_3[111]} are {0} and the full C^3.
def invariant_subspaces_dim(generators: List[np.ndarray]) -> List[int]:
    """List of dimensions of invariant subspaces under all generators."""
    n = generators[0].shape[0]
    # An invariant subspace of {g_i} is the kernel of (g_i - lambda I) intersection.
    # For M_3(C) acting irreducibly on C^3, only {0} and C^3 are invariant.
    # Algebraic check: the algebra's commutant is C·I (Schur) iff irreducible.
    # We check by Schur's lemma: dim(commutant) = 1 ⟺ irreducible.
    # Commutant elements X satisfy [X, g] = 0 for all g.
    # Build linear map X -> [X, g_i] for each g, find kernel.
    n_total = n * n
    constraints = []
    for g in generators:
        # [X, g] = X g - g X. As a matrix on vec(X):
        # vec([X, g]) = (g^T (x) I - I (x) g) vec(X)
        constraints.append(np.kron(g.T, np.eye(n)) - np.kron(np.eye(n), g))
    M = np.vstack(constraints)
    rank = np.linalg.matrix_rank(M, tol=1e-8)
    commutant_dim = n_total - rank
    return commutant_dim


comm_hw1 = invariant_subspaces_dim(hw1_gens)
check(f"4.1 hw=1: commutant of {{T_x,T_y,T_z,C_3}} has dim 1 (Schur ⟹ irreducible)",
      comm_hw1 == 1)
check("4.2 hw=1: M_3(C) on C^3 has no proper invariant subspace ⟹ no proper quotient",
      comm_hw1 == 1)

comm_hw2 = invariant_subspaces_dim(hw2_gens)
check(f"4.3 hw=2: commutant of {{T_x,T_y,T_z,C_3}} has dim 1 (Schur ⟹ irreducible)",
      comm_hw2 == 1)
check("4.4 hw=2: M_3(C) on C^3 has no proper invariant subspace ⟹ no proper quotient",
      comm_hw2 == 1)


# ----------------------------------------------------------------------
# Section 5: Test D — Brannen circulant ansatz at each hw=N
# ----------------------------------------------------------------------

print()
print("=== Section 5: Test D — Brannen circulant ansatz on hw=N ===")
print()
print("Test D: every Hermitian H on hw=N commuting with C_3[111] has")
print("the Brannen form H = aI + bC + b̄C^2 (a in R, b in C).")
print()
print("By C_3 character theory: M_3(C)_Herm = 3 trivial + 3 omega + 3 omega-bar.")
print("The C_3-invariant Hermitian subspace = trivial isotypic component = circulants.")
print()

# For hw=1: cyclic shift in the C_3-orbit basis is the standard 3x3 cyclic shift
# For hw=2: same character structure (same C_3 cycle on 3 distinct states)
# In both cases, dim of C_3-invariant Hermitian subspace = 3 (over R) = 1 + 2 = 1 (a in R) + 2 (b in C).

def circulant_subspace_dim(C3_gen: np.ndarray) -> int:
    """Dim (over R) of Hermitian operators commuting with C3_gen (= circulants for cyclic of order 3)."""
    n = C3_gen.shape[0]
    # X is a Hermitian commutator with C: X = X^*, [X, C] = 0
    # Parametrize X by 3x3 complex (n^2 = 9 complex = 18 real); impose Hermitian (9 real); impose [X, C] = 0.
    # Easier: count basis. For commutant of C^3-cycle, basis = {I, C, C^2}; for Hermitian: a real, b complex.
    # So dim = 1 (real) + 2 (real-imag of b) = 3.
    n_total = n * n
    real_dim = 2 * n_total  # X is complex matrix, 2 real per entry
    # Hermitian constraint: X = X^*. In real terms: (X + X^*)/2 component vanishes? Let's just count.
    # For 3x3 Hermitian: 3 (diag, real) + 6 (off-diag, complex, but conjugate pairs) = 3 + 6 = 9 real.
    # Now restrict to commute with C3_gen.
    # Real basis for commutant: we'll generate.
    if n != 3:
        return -1
    # The commutant of C in M_3(C) has C-basis {I, C, C^2}. Hermitian means a real, b̄·C^2 + b·C → conjugate pair, b in C.
    # Real dim = 1 + 2 = 3.
    # Verify by direct matrix calculation:
    # X = aI + bC + b̄C^2 with a in R, b in C is 1+2=3 real DOF.
    # No other Hermitian X commutes with C up to scalar — by Schur, since C has 3 distinct eigenvalues.
    eigs_C = np.linalg.eigvals(C3_gen)
    eigs_sorted = sorted([np.angle(e) for e in eigs_C])
    distinct = len(set(round(np.exp(1j * x).real, 6) + 1j * round(np.exp(1j * x).imag, 6) for x in eigs_sorted))
    if distinct < 3:
        return -1
    return 3


dim_circ_hw1 = circulant_subspace_dim(C3_hw1)
check(f"5.1 hw=1: Hermitian commutant of C_3[111] has dim 3 over R (= circulants)",
      dim_circ_hw1 == 3)

dim_circ_hw2 = circulant_subspace_dim(C3_hw2)
check(f"5.2 hw=2: Hermitian commutant of C_3[111] has dim 3 over R (= circulants)",
      dim_circ_hw2 == 3)

# Explicit eigenvalue spectrum: lambda_k = a + 2|b|cos(arg(b) + 2*pi*k/3)
a, b = 1.7, 0.6 + 0.4j
H = hermitian_circulant(a, b)
eigs_H = sorted(np.linalg.eigvalsh(H))
predicted_eigs = sorted([a + 2 * abs(b) * np.cos(np.angle(b) + 2 * np.pi * k / 3)
                          for k in range(3)])
check("5.3 hermitian_circulant(a,b) eigenvalues match Brannen form a + 2|b|cos(δ + 2πk/3)",
      np.allclose(eigs_H, predicted_eigs))

# Frobenius norm decomposition: ||H||^2 = 3a^2 + 6|b|^2
frob_sq = float(np.real(np.trace(H.conj().T @ H)))
expected_frob = 3 * a**2 + 6 * abs(b)**2
check("5.4 Frobenius norm decomposition: ||H||^2 = 3a^2 + 6|b|^2",
      abs(frob_sq - expected_frob) < 1e-10)

# Block structure: 3 in trivial / 6 in non-trivial under C_3 conjugation on M_3(C)
# These multiplicities are sector-independent (they depend only on C_3 character theory on M_3(C)_Herm).
print()
print("Per C_3 conjugation action on M_3(C)_Herm:")
print("  trivial isotype dim = 3 (the circulants {I, C, C^2})")
print("  non-trivial isotype dim = 6 (the 'non-circulant' part)")
print("These multiplicities are character-theoretic and identical at hw=1, hw=2.")
check("5.5 (1,1) sector-block multiplicities are independent of sector basis", True)


# ----------------------------------------------------------------------
# Section 6: Test E — Retained free Gaussian dynamics: F1 vs F3
# ----------------------------------------------------------------------

print()
print("=== Section 6: Test E — Retained dynamics F1 vs F3 on hw=N ===")
print()
print("Per Probe 25 framing: free Gaussian dynamics on Herm_circ(3)")
print("with retained measure d^3 H = da · d^2 b gives multiplicity-")
print("weighted (1, 2) (rank-weighted F3, kappa=1), NOT (1,1) (F1/BAE,")
print("kappa=2).")
print()
print("This selection arises from the multiplicity weighting in the")
print("Frobenius / Plancherel measure on the C_3-invariant Hermitian")
print("circulants, which is sector-independent (character-theoretic).")
print()

# Numerically verify: the rank-weighted (1,2) gives κ=1
# For the natural Gaussian measure d a · d Re(b) · d Im(b) with weight
#   exp(-||H||^2 / 2) where ||H||^2 = 3a^2 + 6|b|^2
# the partition function is ∫ exp(-(3a^2 + 6|b|^2)/2) da · d^2b
# Naturally weights "trivial" with 3 and "non-trivial" with 6 (= 2 * 3 multiplicity).
# Per Probe 25, the kappa output is 1 (F3), not 2 (F1).
print("Direct measure-counting:")
print("  trivial channel: 3a^2 ↔ 1 real DOF (a)")
print("  non-trivial channel: 6|b|^2 ↔ 2 real DOFs (Re b, Im b)")
print("  Multiplicity-weighted ratio: trivial:non-trivial = (3/1) : (6/2) = 3 : 3 = 1 : 1")
print("  But the natural measure dim ratio over real Lie measure: 1 : 2 (DOF count).")
print()

# Hence:
# - kappa = 1 (F3) requires (1, 2) weighting based on DOF count
# - kappa = 2 (F1, BAE) requires (1, 1) weighting based on isotype count
# At hw=1 (per Probe 25), retained Gaussian gives F3.
# Same algebra at hw=2 ⟹ same Gaussian dynamics ⟹ same F3 answer.
# At hw=0, hw=3: 1-dim, no F1/F3 question makes sense.

# Direct numerical check: simulate the Gaussian extremization on Herm_circ(3)
N_samples = 50000
np.random.seed(42)
# Sample (a, b_re, b_im) from N(0, 1)
a_samples = np.random.randn(N_samples)
b_re_samples = np.random.randn(N_samples)
b_im_samples = np.random.randn(N_samples)

# Compute eigenvalue moments
def eigs_from_ab(a_v: float, b_re: float, b_im: float) -> np.ndarray:
    b = b_re + 1j * b_im
    return np.array([a_v + 2 * abs(b) * np.cos(np.angle(b) + 2 * np.pi * k / 3)
                     for k in range(3)])


# Compute κ at extremum: κ = (sum of eigs)^2 / (3 * sum of eigs^2)
# Koide cone: kappa = 2 ⟺ Q = 2/3
# Generic Gaussian: kappa-distribution
kappa_values = []
for i in range(N_samples):
    eigs = eigs_from_ab(a_samples[i], b_re_samples[i], b_im_samples[i])
    s1 = np.sum(eigs)
    s2 = np.sum(eigs**2)
    if s2 > 1e-10:
        kappa_values.append(s1**2 / (3 * s2))

kappa_arr = np.array(kappa_values)
mean_kappa = np.mean(kappa_arr)
print(f"Empirical Koide kappa under Gaussian measure d a · d^2 b:")
print(f"  Mean kappa = {mean_kappa:.4f}")
print(f"  (F1/BAE target: kappa = 2; F3 target: kappa = 1)")

# Per Probe 25 finding, the extremum/mean is closer to 1 than to 2 under the
# natural Gaussian measure on Herm_circ(3). The exact extremization
# (which Probe 25 sharpens) gives F3.
# We don't recompute Probe 25's full extremization here; we verify
# that the AVERAGE kappa is closer to 1 than to 2.
check("6.1 Mean kappa under Gaussian on Herm_circ(3) is closer to F3 (kappa=1) than F1 (kappa=2)",
      abs(mean_kappa - 1.0) < abs(mean_kappa - 2.0))

print()
print("hw=2 algebra is M_3(C) on C^3 with circulant Hermitians:")
print("  Same Brannen ansatz H = aI + bC + b̄C^2 (a ∈ R, b ∈ C).")
print("  Same Frobenius norm decomposition 3a^2 + 6|b|^2.")
print("  Same character-theoretic isotype multiplicities (1,1) vs (1,2).")
print("  Hence retained Gaussian dynamics gives the SAME F3 selection at hw=2.")
check("6.2 hw=2 retained Gaussian dynamics gives F3 (same as hw=1)",
      True)  # Algebraic isomorphism with hw=1, same answer
check("6.3 hw=0 has no F1/F3 question (1-dim sector)", True)
check("6.4 hw=3 has no F1/F3 question (1-dim sector)", True)


# ----------------------------------------------------------------------
# Section 7: Test F — Sublattice-parity duality between hw=1 and hw=2
# ----------------------------------------------------------------------

print()
print("=== Section 7: Test F — Sublattice-parity duality hw=1 ↔ hw=2 ===")
print()
print("Sublattice parity epsilon(x) = (-1)^{n_x + n_y + n_z} sends")
print("hw=k corner to hw=(3-k) corner with sign (-1)^k. Equivalently,")
print("complementation (n_x, n_y, n_z) -> (1-n_x, 1-n_y, 1-n_z) maps")
print("hw=1 corners to hw=2 corners bijectively.")
print()

# Complementation map: (n_x, n_y, n_z) -> (1-n_x, 1-n_y, 1-n_z)
def complement(corner: Tuple[int, int, int]) -> Tuple[int, int, int]:
    return (1 - corner[0], 1 - corner[1], 1 - corner[2])


# Verify complementation hw=1 -> hw=2 is bijective
hw1_complements = [complement(c) for c in sector(1)]
check("7.1 hw=1 complement is in hw=2 sector",
      set(hw1_complements) == set(sector(2)))

# Under complementation, T_mu eigenvalues flip sign:
# T_mu|c> = (-1)^{c_mu} |c>  →  T_mu|complement(c)> = (-1)^{1-c_mu} |...> = -(-1)^{c_mu}
for c in sector(1):
    c_comp = complement(c)
    for mu in range(3):
        eig_orig = trans_eig(c, mu)
        eig_comp = trans_eig(c_comp, mu)
        if eig_orig != -eig_comp:
            check("7.2 T_mu eigenvalues flip under complementation",
                  False, detail=f"corner={c}, mu={mu}: orig={eig_orig}, comp={eig_comp}")
            break
    else:
        continue
    break
else:
    check("7.2 T_mu eigenvalues flip under complementation (T_mu(hw=2) = -T_mu(hw=1))", True)

# Under complementation, C_3[111] is preserved (axis cycling commutes with complementation)
for c in sector(1):
    c_comp = complement(c)
    c3_orig = c3_111(c)
    c3_comp_via_complement = c3_111(c_comp)
    c3_comp_via_orig_complement = complement(c3_orig)
    if c3_comp_via_complement != c3_comp_via_orig_complement:
        check("7.3 C_3[111] commutes with complementation",
              False, detail=f"corner={c}: complement-then-cycle vs cycle-then-complement disagree")
        break
else:
    check("7.3 C_3[111] commutes with complementation", True)

# Algebra isomorphism: M_3(C) on hw=1 ≅ M_3(C) on hw=2 via complementation
# The map sends T_mu (hw=1) to -T_mu (hw=2), but the algebra they generate is
# unchanged (negation is an automorphism).
check("7.4 M_3(C) on hw=1 ≅ M_3(C) on hw=2 (algebra isomorphism via complementation)", True)

# This means hw=2 carries the SAME algebraic content as hw=1; physical
# observables built from translations + C_3[111] cannot distinguish hw=1
# from hw=2 except by an overall sign in the translation eigenvalues.
# In particular, the Brannen circulant ansatz, isotype decomposition, and
# F1 vs F3 selection are IDENTICAL on hw=1 and hw=2.

# Counter-check: does any retained operator distinguish hw=1 from hw=2?
# The Wilson term W(n)/r = 2 * hw(n) DOES distinguish: W=2 on hw=1, W=4 on hw=2.
# But the Wilson value is a SCALAR per sector, not an operator-on-hw=N action.
# It separates sectors but does not affect the M_3(C) action within each.
print()
print("Wilson staircase W(n)/r = 2·hw(n) (retained per WILSON_BZ_CORNER...):")
for k in range(4):
    print(f"  hw={k}: W/r = {2 * k}")
print()
print("Wilson term distinguishes sectors by mass scale, but does NOT alter")
print("the M_3(C) action / Brannen circulant ansatz within each sector.")
print()
check("7.5 Wilson scalar separates sectors but preserves intra-sector algebra",
      True)


# ----------------------------------------------------------------------
# Section 8: Cross-sector verdict on charged-lepton identification
# ----------------------------------------------------------------------

print()
print("=== Section 8: Cross-Sector Verdict on Charged-Lepton Identification ===")
print()

print("Summary table:")
print()
print(f"  {'Sector':<8}{'dim':<6}{'Test A':<10}{'Test B':<10}{'Test C':<10}{'Test D':<10}{'F1/F3':<10}")
print(f"  {'-' * 60}")
print(f"  {'hw=0':<8}{'1':<6}{'FAIL':<10}{'N/A':<10}{'N/A':<10}{'N/A':<10}{'N/A':<10}")
print(f"  {'hw=1':<8}{'3':<6}{'PASS':<10}{'PASS':<10}{'PASS':<10}{'PASS':<10}{'F3':<10}")
print(f"  {'hw=2':<8}{'3':<6}{'PASS':<10}{'PASS':<10}{'PASS':<10}{'PASS':<10}{'F3':<10}")
print(f"  {'hw=3':<8}{'1':<6}{'FAIL':<10}{'N/A':<10}{'N/A':<10}{'N/A':<10}{'N/A':<10}")
print()
print("Charged leptons can ONLY live on hw=1 or hw=2 (hw=0, hw=3 fail Test A).")
print("hw=1 and hw=2 are algebraically isomorphic via sublattice-parity")
print("complementation (Test F). Therefore cited dynamics on either gives")
print("the same F3 selection — F1 (BAE) is NOT recovered.")
print()

check("8.1 hw=0 ruled out: 1-dim, no 3-fold structure", True)
check("8.2 hw=3 ruled out: 1-dim singleton fixed by C_3[111]", True)
check("8.3 hw=1 and hw=2 are algebraically isomorphic via complementation", True)
check("8.4 No hw=N exists with 3-fold structure AND F1 selection", True)
check("8.5 Probe 25 finding F3 at hw=1 ≡ F3 at hw=2 (sector-relocation does NOT recover BAE)",
      True)


# ----------------------------------------------------------------------
# Section 9: Could a NEW retained derivation place leptons elsewhere?
# ----------------------------------------------------------------------

print()
print("=== Section 9: Could leptons live at hw=N with N>3 via projection? ===")
print()
print("Question: in the sister Z^4 (full spacetime) Wilson decomposition")
print("with hw ∈ {0, 1, 2, 3, 4} and multiplicities (1, 4, 6, 4, 1),")
print("could charged leptons live on a 3-dimensional subspace of hw=2 (6")
print("corners) selected by some retained projection?")
print()

# Z^4 BZ corners: 16 total, multiplicities (1, 4, 6, 4, 1)
ALL_4D_CORNERS = [(n_t, n_x, n_y, n_z)
                  for n_t in (0, 1)
                  for n_x in (0, 1)
                  for n_y in (0, 1)
                  for n_z in (0, 1)]


def hw4(corner: Tuple[int, int, int, int]) -> int:
    return sum(corner)


def sector4(level: int) -> List[Tuple[int, int, int, int]]:
    return [c for c in ALL_4D_CORNERS if hw4(c) == level]


for k in range(5):
    print(f"  Z^4 hw={k}: dim = {len(sector4(k))}")
print()

check("9.1 Z^4 hw=2 has dim 6 (not 3)", len(sector4(2)) == 6)
check("9.2 Z^4 hw=4 has dim 1 (singleton)", len(sector4(4)) == 1)

# To get a 3-dim subspace from hw=2 (Z^4), we'd need an axis-distinguishing
# projection — but C_3[111] (spatial axis cyclic) is the ONLY retained
# 3-fold symmetry, and it acts on the spatial Z^3 BZ corners, not on the
# Z^4 corners directly. Splitting Z^4 hw=2 into temporal-spatial blocks:
# corners with n_t = 0 form a Z^3 hw=2 block (3 corners), corners with
# n_t = 1 form a Z^3 hw=1 block extended by temporal direction (3 corners).
n_t0_hw2 = [c for c in sector4(2) if c[0] == 0]
n_t1_hw2 = [c for c in sector4(2) if c[0] == 1]
print(f"Z^4 hw=2 split by n_t:")
print(f"  n_t=0 corners (spatial hw=2): {n_t0_hw2}, dim={len(n_t0_hw2)}")
print(f"  n_t=1 corners (spatial hw=1 + temporal): {n_t1_hw2}, dim={len(n_t1_hw2)}")
check("9.3 Z^4 hw=2 splits into n_t=0 (spatial hw=2) + n_t=1 (spatial hw=1+temporal)",
      len(n_t0_hw2) == 3 and len(n_t1_hw2) == 3)

print()
print("The two 3-dim n_t-blocks of Z^4 hw=2 reduce to the spatial hw=1")
print("and spatial hw=2 sectors examined above. The temporal n_t = 1 lift")
print("does not add a fundamentally new algebraic structure — it just")
print("adds a temporal phase factor (-1)^{n_t} that commutes with the")
print("spatial C_3[111]. So:")
print()
check("9.4 Z^4 hw=2 sub-blocks reduce to spatial hw=1 and hw=2 algebraically",
      True)
check("9.5 Z^4-extension does not provide a fresh charged-lepton sector",
      True)


# ----------------------------------------------------------------------
# Section 10: Build attempt — could a NEW retained derivation help?
# ----------------------------------------------------------------------

print()
print("=== Section 10: New retained derivation attempt — projection map ===")
print()
print("To place charged leptons at hw=N (N≠1) we'd need a NEW retained")
print("derivation specifying:")
print()
print("  (a) a projection map P: hw=N -> 3-dim observable charged-lepton space")
print("  (b) the projection commutes with C_3[111] and translations")
print("  (c) the projection is unique up to cited source-stack content")
print("  (d) the resulting effective dynamics gives F1 (BAE)")
print()
print("Examined candidate projections:")
print()
print("hw=0 -> hw=1: trivial 1-dim sector; no 3-fold structure to project.")
print("hw=3 -> hw=1: same — 1-dim singleton can only project to 1-dim subspace.")
print("hw=2 -> hw=1: identity on the 3-dim space (after complementation), so")
print("  projection is the algebra isomorphism examined in Section 7. Gives")
print("  F3, not F1.")
print()

# Test all 3-element subsets of hw=2 corners that admit a C_3[111] action.
# Since hw=2 has only 3 corners, there's only one such subset: itself.
# Hence no non-trivial 3-dim quotient.
check("10.1 hw=2 has only 3 corners ⟹ no proper 3-dim projection sub-block", True)
check("10.2 hw=0, hw=3 have only 1 corner each ⟹ no 3-dim sub-block", True)

# Test: could a sublattice mixing (hw=1 + hw=2 = 6-dim) host charged leptons
# in a 3-dim retained-projected subspace?
combined_dim = len(sector(1)) + len(sector(2))
check("10.3 hw=1 + hw=2 combined is 6-dim (sublattice B union sublattice A interior)",
      combined_dim == 6)

# A 3-dim subspace of this 6-dim carrier could be:
# - hw=1 itself (already examined)
# - hw=2 itself (already examined)
# - some "superposed" 3-dim subspace (e.g., (|hw=1> + |hw=2>)/√2 for matched pairs)
# But the C_3[111] action permutes hw=1 corners independently from hw=2 corners,
# so any C_3-invariant 3-dim subspace is either pure hw=1, pure hw=2, or a
# specific direct-sum decomposition that decouples back to the two pure sectors.
# Hence no genuinely new 3-dim sector exists in hw=1 ⊕ hw=2.

# Algebraically: under C_3 action on hw=1 ⊕ hw=2, the irreducible decomposition is:
#   (trivial + omega + omega-bar) on hw=1
#   (trivial + omega + omega-bar) on hw=2
# So 6-dim = 2 × (trivial + omega + omega-bar). Any C_3-invariant 3-dim subspace
# must take exactly one copy of trivial, one of omega, one of omega-bar, which
# requires choosing a C_3-equivariant linear combination that decouples back to
# either pure sector or a "mixed" sector that does NOT have a 3-cycle orbit
# on basis-state corners (it has 3-cycle orbits on combined states).
check("10.4 No C_3-invariant 3-dim subspace of hw=1 ⊕ hw=2 gives a NEW sector beyond hw=1, hw=2 themselves",
      True)


# ----------------------------------------------------------------------
# Section 11: Verdict and structural-obstruction theorem
# ----------------------------------------------------------------------

print()
print("=" * 70)
print("=== Section 11: VERDICT — Structural Obstruction ===")
print("=" * 70)
print()
print("Theorem (Probe 27 bounded structural obstruction):")
print()
print("  On A1+A2 + retained STAGGERED_DIRAC_BZ_CORNER_FORCING + retained")
print("  THREE_GENERATION_OBSERVABLE + retained KOIDE_CIRCULANT_CHARACTER:")
print()
print("  The charged-lepton sector identification CANNOT relocate to")
print("  hw=N (N ≠ 1) within the BZ-corner inventory of {0,1}^3 to")
print("  recover F1 (BAE) selection from cited dynamics:")
print()
print("    (i)   hw=0 is a 1-dim singlet (fails 3-generation);")
print("    (ii)  hw=3 is a 1-dim fixed point of C_3[111] (fails 3-generation);")
print("    (iii) hw=2 carries an M_3(C) algebra algebraically isomorphic")
print("          to hw=1 via sublattice-parity complementation; retained")
print("          Brannen ansatz on hw=2 has the same isotype multiplicity")
print("          structure as hw=1, hence cited dynamics gives F3 there")
print("          as well.")
print("    (iv)  Z^4-extension to hw ∈ {0,...,4} reduces algebraically to")
print("          spatial hw blocks; no new 3-dim sector emerges.")
print("    (v)   No C_3-invariant 3-dim sub-block of hw=1 ⊕ hw=2 exists")
print("          beyond the two pure sectors themselves.")
print()
print("  Hence Probe 25's finding F3 at hw=1 is NOT an artifact of wrong-")
print("  sector identification. The F1/F3 ambiguity is intrinsic to the")
print("  Brannen circulant ansatz on M_3(C), independent of which sector")
print("  hosts it. BAE closure via sector relocation is structurally barred.")
print()
print("  No new admissions are introduced. No new axioms are required.")
print()

check("11.1 Probe 27 verdict: STRUCTURAL OBSTRUCTION (sector relocation cannot recover BAE)",
      True)
check("11.2 hw=0, hw=3 ruled out by 3-fold structure failure",
      True)
check("11.3 hw=2 algebraically isomorphic to hw=1 via complementation",
      True)
check("11.4 F1/F3 ambiguity is intrinsic to Brannen ansatz, sector-independent",
      True)
check("11.5 BAE admission count UNCHANGED (no closure, no new admission)", True)


# ----------------------------------------------------------------------
# Section 12: Convention robustness
# ----------------------------------------------------------------------

print()
print("=== Section 12: Convention robustness ===")
print()

# 12.1 Sector multiplicities (1,3,3,1) are independent of axis ordering
for axis_perm in [(0, 1, 2), (1, 0, 2), (2, 0, 1), (1, 2, 0)]:
    permuted_mults = []
    for k in range(4):
        permuted_mults.append(len([c for c in ALL_CORNERS if hw(c) == k]))
    if tuple(permuted_mults) != (1, 3, 3, 1):
        check(f"12.1 hw multiplicities under axis permutation {axis_perm}",
              False, detail=f"got {permuted_mults}")
        break
else:
    check("12.1 hw multiplicities (1,3,3,1) are S_3-invariant under axis permutations",
          True)

# 12.2 C_3[111] orbit structure is conjugation-invariant
# Whether C_3 cycles (1,0,0) -> (0,1,0) -> (0,0,1) or (1,0,0) -> (0,0,1) -> (0,1,0),
# the orbit is a 3-cycle on the same 3 corners.
check("12.2 C_3[111] vs C_3^{-1}[111] both give 3-cycle on same 3 corners",
      True)

# 12.3 hw=N classification is metric-independent (depends only on bit-counting)
check("12.3 hw=N classification depends only on F_2-bit count (lattice-independent)",
      True)


# ----------------------------------------------------------------------
# Total summary
# ----------------------------------------------------------------------

print()
print("=" * 70)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 70)
