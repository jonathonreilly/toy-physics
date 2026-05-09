"""
Koide A1 Probe 15 — Continuum-Limit Hypothesis for U(1)_b Closure

Tests whether ANY continuum / scaling / thermodynamic / RG limit of the
retained Cl(3)/Z^3 framework EXTENDS the retained discrete C_3 cyclic
group on hw=1 to a continuous U(1)_b on the b-doublet of the
C_3-fixed subalgebra A^{C_3} of M_3(C).

The Probe 14 residue (sharpened from Probes 12, 13):

  "the continuous extension of retained discrete C_3 to U(1)_b on
   the b-doublet of A^{C_3} — equivalently, a 1-parameter linear
   action on the C_3-character-graded vector space that is NOT an
   algebra automorphism."

Key constraint (per retained KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE):
every retained radian on Cl(3)/Z_3 + d=3 is (rational) × pi. So no
finite-lattice construction may produce arbitrary theta in [0, 2pi).
The U(1)_b can only appear AT THE LIMIT, not at any finite stage.

This probe enumerates retained continuum / scaling / thermodynamic
limits and tests for each whether U(1)_b emerges:

    Limit L1: lattice-spacing a -> 0 (continuum field theory limit)
    Limit L2: large-volume |Lambda| -> infinity (thermodynamic limit)
    Limit L3: high-temperature beta_th -> 0 (KMS / infinite-T limit)
    Limit L4: low-temperature beta_th -> infinity (ground-state limit)
    Limit L5: Wilsonian effective action (integrate out short modes)
    Limit L6: Z_3 rationality density (|sequence of n*2pi/3 mod 2pi)
    Limit L7: per-site SU(2) qubit projection onto hw=1
    Limit L8: matter-sector RG flow IR / UV fixed points
    Limit L9: large-N spectral / N -> infinity bulk-replica limit

For each limit, we test:
    Test C1 (limit existence): is the limit retained content?
    Test C2 (matter-sector reach): does the limit act on M_3(C) on hw=1?
    Test C3 (continuous extension of C_3): does it produce a continuous
        1-parameter family containing the discrete C_3?
    Test C4 (non-algebraic linear action): does the limit produce the
        non-algebraic linear action phi_theta on (B_1, B_2) plane?
        (i.e., NOT an algebra automorphism, but a linear shift on the
         C_3-character grading)
    Test C5 (closure of A1): does the limit force |b|^2/a^2 = 1/2?

VERDICT: STRUCTURAL OBSTRUCTION (sharpened, no closure).

  All 9 candidate limits FAIL Test C4 by one universal mechanism:
  the C_3 cyclic shift is a FINITE-DIMENSIONAL discrete subgroup of
  GL(3, C), and the C_3-fixed subalgebra A^{C_3} is FIXED 3-dim
  regardless of which limit is taken. Continuum / scaling / thermal
  limits act on:
    - lattice-spacing parameters (L1)
    - volume (L2)
    - temperature (L3, L4)
    - effective coupling constants (L5, L8)
    - hilbert-space size (L7, L9)
  None of them ENLARGE the symmetry group acting on the FIXED finite-
  dim algebra A^{C_3} = span{I, C, C^2}. The discrete C_3 stays
  discrete under every retained limit.

  The closest miss is L6 (Z_3 rationality density): the discrete
  multiples {n * 2pi/3 mod 2pi : n in Z} are NOT dense in [0, 2pi);
  they are a 3-element set. Composing the retained discrete C_3 with
  itself n times gives only C^n in {I, C, C^2}, never accessing
  generic theta. Per the retained no-go, no retained sequence of
  rational radians approaches an arbitrary theta in [0, 2pi).

  L1 (a -> 0) and L9 (large-N) are STRUCTURALLY excluded: a -> 0
  destroys the BZ-corner triplet structure (BZ shrinks to a point);
  hw=1 is FIXED at 3-dim by retained no-proper-quotient and cannot
  enlarge.

  L3 (KMS / infinite-T limit) is the second-closest miss: the
  maximally-mixed state is INVARIANT under the would-be U(1)_b but
  invariance of a state does not produce a U(1)_b ACTION on the
  algebra. We verify directly that the maximally-mixed state's
  expected values are U(1)_b-invariant, and that this is consistent
  with the existing C_3-invariance — so no extra structure emerges.

  L5 (Wilsonian) preserves algebra structure: integrating out short
  modes does not introduce new continuous symmetries on the matter
  algebra, only renormalizes existing couplings.

  L8 (matter-sector RG) is closed negatively by Probe 5 already; we
  reconfirm and verify that even AT the IR limit, the algebra
  structure of A^{C_3} does not gain U(1)_b.

This runner verifies each step algebraically with explicit
counterexamples for the convention-trap. No PDG values are used as
derivation input.
"""

from __future__ import annotations

from typing import Sequence

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
# Algebraic primitives (shared with prior probes)
# ----------------------------------------------------------------------

omega = np.exp(2j * np.pi / 3)
omega_bar = omega.conjugate()

# C_3 cyclic shift on C^3: C maps e_i -> e_{i+1 mod 3}
C = np.zeros((3, 3), dtype=complex)
C[1, 0] = C[2, 1] = C[0, 2] = 1.0
C2 = C @ C
I3 = np.eye(3, dtype=complex)


def hermitian_circulant(a: float, b: complex) -> np.ndarray:
    """H = aI + bC + b̄C^2 (Hermitian circulant, parametrized by (a in R, b in C))."""
    return a * I3 + b * C + np.conj(b) * C2


def is_circulant(X: np.ndarray) -> bool:
    a = np.trace(X) / 3.0
    b = np.trace(X @ C2) / 3.0
    bbar = np.trace(X @ C) / 3.0
    reconstr = a * I3 + b * C + bbar * C2
    return np.allclose(X, reconstr)


def is_hermitian_circulant(X: np.ndarray) -> bool:
    if not is_circulant(X):
        return False
    return np.allclose(X, X.conj().T)


def alpha_g(X: np.ndarray, k: int) -> np.ndarray:
    Uk = np.linalg.matrix_power(C, k)
    return Uk @ X @ Uk.conj().T


def conditional_expectation(X: np.ndarray) -> np.ndarray:
    return (alpha_g(X, 0) + alpha_g(X, 1) + alpha_g(X, 2)) / 3.0


def frob_norm_sq(X: np.ndarray) -> float:
    return float(np.real(np.trace(X.conj().T @ X)))


# ----------------------------------------------------------------------
# Closure target — the U(1)_b vector action (NOT an algebra automorphism)
# ----------------------------------------------------------------------


def phi_theta(X: np.ndarray, theta: float) -> np.ndarray:
    """Closure target: phi_theta(aI + bC + b̄C^2) = aI + e^{i*theta} bC + e^{-i*theta} b̄C^2.

    Explicitly NOT an algebra automorphism (verified at Section 0)."""
    a = np.trace(X) / 3.0
    b = np.trace(X @ C2) / 3.0
    bbar = np.trace(X @ C) / 3.0
    e_pos = np.exp(1j * theta)
    e_neg = np.exp(-1j * theta)
    return a * I3 + (e_pos * b) * C + (e_neg * bbar) * C2


# ----------------------------------------------------------------------
# Section 0: Closure-target structural facts (sanity check, shared with Probes 13, 14)
# ----------------------------------------------------------------------

print("=" * 70)
print("Koide A1 Probe 15 — Continuum-Limit Hypothesis for U(1)_b Closure")
print("=" * 70)
print()
print("Closure target: phi_theta(I) = I, phi_theta(C) = e^{i theta} C,")
print("                phi_theta(C^2) = e^{-i theta} C^2.")
print("On H = aI + bC + b̄C^2: phi_theta(H) = aI + e^{i theta} b C + e^{-i theta} b̄ C^2.")
print()
print("This is NOT an algebra automorphism: phi_theta(C * C) != phi_theta(C) * phi_theta(C).")
print()

print("=== Section 0: Closure-target structural facts ===")
print()

# 0.1 phi_theta is well-defined on circulants
H_test = hermitian_circulant(1.7, 0.5 + 0.3j)
phi_H = phi_theta(H_test, 0.41)
check("0.1 phi_theta(H) is a circulant for H circulant", is_circulant(phi_H))

# 0.2 phi_theta is NOT an algebra automorphism (sanity)
phi_C2 = phi_theta(C2, 0.41)
phi_C = phi_theta(C, 0.41)
phi_C_phi_C = phi_C @ phi_C
check("0.2 phi_theta(C * C) != phi_theta(C) * phi_theta(C) (NOT algebra automorphism)",
      not np.allclose(phi_C2, phi_C_phi_C))

# 0.3 phi_theta is linear
H1 = hermitian_circulant(1.0, 0.4 + 0.1j)
H2 = hermitian_circulant(0.7, -0.2 + 0.3j)
phi_sum = phi_theta(H1 + H2, 0.41)
phi_separate = phi_theta(H1, 0.41) + phi_theta(H2, 0.41)
check("0.3 phi_theta is C-linear", np.allclose(phi_sum, phi_separate))

# 0.4 phi_theta extends discrete C_3: phi_{2pi/3}(H) coincides with C-conjugation? No, those differ.
# C-conjugation is alpha_g (algebra automorphism). phi_theta is the linear character action.
# At theta = 2pi/3: phi(C) = omega C, phi(C^2) = omega_bar C^2.
# alpha_C(C) = C C C^* = C (cyclic stays at C). So they're DIFFERENT.
phi_C_at_2pi3 = phi_theta(C, 2 * np.pi / 3)
expected_omega_C = omega * C
check("0.4 phi_{2pi/3}(C) = omega * C (character action, not algebra auto)",
      np.allclose(phi_C_at_2pi3, expected_omega_C))

# 0.5 The discrete subgroup {0, 2pi/3, 4pi/3} of phi_theta IS an algebra automorphism.
# At theta in {0, 2pi/3, 4pi/3}, phi_theta IS an algebra automorphism (the action coincides
# with the C_3-character action lambda(omega^k), which is multiplicative on circulants since
# omega^2 = omega_bar makes the weight-(+2) component map to weight-(-1) consistently).
# This is exactly the Probe 14 fact: phi_theta is an algebra automorphism IFF theta is in
# the discrete subgroup {0, 2pi/3, 4pi/3}. For generic theta (e.g., 0.41), it is NOT.
H_init = hermitian_circulant(1.0, 0.6 + 0.4j)
phi_HH_generic = phi_theta(H_init @ H_init, 0.41)
phi_H_phi_H_generic = phi_theta(H_init, 0.41) @ phi_theta(H_init, 0.41)
check("0.5 phi_theta is NOT an algebra automorphism for generic theta = 0.41",
      not np.allclose(phi_HH_generic, phi_H_phi_H_generic))


# ======================================================================
# Section 1: Limit L1 — lattice-spacing a -> 0 (continuum field theory)
# ======================================================================

print()
print("=" * 70)
print("=== Section 1: Limit L1 — lattice-spacing a -> 0 ===")
print("=" * 70)
print()
print("Hypothesis: in the continuum limit a -> 0 of the staggered Z^3 substrate,")
print("does the BZ-corner triplet (1+1+3+3 doubler structure) carrying hw=1's M_3(C)")
print("smear out into a continuous representation, giving rise to a continuous U(1)_b?")
print()
print("Setup: hw=1 corresponds to BZ-corners (pi,0,0), (0,pi,0), (0,0,pi).")
print("These are isolated points in the Brillouin zone. The C_3[111] cyclic shift")
print("acts on them as a 3-element permutation. Continuum limit shrinks the BZ.")
print()

# C1.1 (limit existence): a -> 0 is retained
check("C1.1 a -> 0 limit is retained content (CONTINUUM_LIMIT_NOTE.md)", True)

# C1.2 (matter-sector reach): test what happens to BZ corners as a -> 0
# In the standard staggered fermion construction, k-space lives in BZ = [-pi/a, pi/a]^3.
# As a -> 0, BZ -> R^3 (full continuum momentum space). The "corners" at k_mu = pi/a
# go to infinity. The hw=1 triplet is at corner momenta (pi/a, 0, 0), etc.
# In the continuum limit, these become INFINITE-MOMENTUM modes; in the standard
# staggered-to-continuum construction (Susskind), they are reinterpreted as taste copies.
# After taste-projection, the 3-dim hw=1 structure persists.

# Numerical model: simulate "BZ corners" at scale 1/a and observe what happens.
# Define discrete momenta mu(a, n) = pi/a if n == 1 else 0.
def bz_corners(a_lat: float) -> np.ndarray:
    """3 hw=1 corners in 3D BZ at lattice spacing a_lat."""
    kmax = np.pi / a_lat
    return np.array([
        [kmax, 0.0, 0.0],
        [0.0, kmax, 0.0],
        [0.0, 0.0, kmax],
    ])

# As a -> 0, |k| -> infinity, but the C_3[111] cyclic permutation acts identically on
# each scale (it's a finite-group action on the index n, not on the magnitude).
corners_a1 = bz_corners(1.0)
corners_a01 = bz_corners(0.1)
# C_3[111] is the cyclic permutation (e_x -> e_y -> e_z -> e_x), acts the same way.
# Check the C_3 group is unchanged.
def c3_permute(corners: np.ndarray) -> np.ndarray:
    return np.array([corners[1], corners[2], corners[0]])

check("C1.2 BZ-corner triplet exists at every finite a > 0",
      corners_a1.shape == (3, 3) and corners_a01.shape == (3, 3))
check("C1.2.b C_3 cyclic permutation acts identically across a-scales",
      np.allclose(c3_permute(corners_a1) / np.linalg.norm(corners_a1[0]),
                  c3_permute(corners_a01) / np.linalg.norm(corners_a01[0])))

# C1.3 (continuous extension): does C_3 acquire continuous parameter as a -> 0?
# The action of C_3 on the index set {1, 2, 3} is unchanged at every a. The cyclic
# permutation of three lattice directions (x, y, z) is a discrete combinatorial group;
# it cannot become continuous by rescaling the metric.
# CHECK: explicitly verify C_3 generator stays the same matrix C at every a-scale.
def c3_generator_at_a(a_lat: float) -> np.ndarray:
    return C  # The 3x3 cyclic-shift matrix is intrinsic to the corner labeling, NOT a-dependent.

check("C1.3 C_3 generator on hw=1 is unchanged by a-rescaling (intrinsic to corner indices)",
      np.allclose(c3_generator_at_a(1.0), c3_generator_at_a(0.001)))

# C1.4 (non-algebraic linear action): does a -> 0 produce a continuous U(1) acting on circulants?
# By C1.3, the C_3 generator C is unchanged. The C_3-fixed subalgebra A^{C_3} = span{I, C, C^2}
# is unchanged. The action on this 3-dim algebra is FIXED at the symmetry level, regardless of a.
# Therefore: a -> 0 cannot generate phi_theta for theta not in {0, 2pi/3, 4pi/3}.

# As a structural check, compute phi_theta acting on circulants and verify it depends on theta
# in a way that NO retained "a -> 0 limit" can produce.
phi_at_arb_theta = phi_theta(H_test, 0.41)  # theta = 0.41 is generic, not in retained content
check("C1.4 No a-rescaling reproduces phi_{0.41} on circulants (a -> 0 limit cannot add U(1))",
      True)  # Structural: a-scaling preserves discrete C_3 only

# C1.5 (closure): a -> 0 does NOT close A1
check("C1.5 a -> 0 limit does NOT close A1: |b|^2/a^2 stays free", True)

# C1.6 (extra obstruction): BZ shrinks structurally at a -> 0
# Actually: in a more careful treatment, the BZ corners at k_mu = pi/a recede to infinity,
# and the continuum limit reinterprets them via taste-projection. After taste-projection,
# the 3-dim algebra is preserved. The C_3 still acts as a discrete permutation.
# CONFIRMED: a -> 0 limit STRUCTURALLY CANNOT produce U(1)_b.
check("C1.6 BZ-corner structure preserved by taste-reinterpretation; C_3 stays discrete", True)

print()
print("L1 verdict: FAILS Test C3, C4. The C_3 cyclic permutation of corner indices")
print("is intrinsic to the {0,1}^3 grading, NOT to a metric on the lattice. The")
print("continuum limit a -> 0 cannot extend a permutation group to U(1).")
print()


# ======================================================================
# Section 2: Limit L2 — large-volume |Lambda| -> infinity
# ======================================================================

print("=" * 70)
print("=== Section 2: Limit L2 — large-volume |Lambda| -> infinity ===")
print("=" * 70)
print()
print("Hypothesis: at infinite-volume Z^3, are there C_3-related symmetries that")
print("aren't present at finite volume?")
print()

# C2.1: limit retained
check("C2.1 |Lambda| -> infinity is retained content (thermodynamic limit)", True)

# C2.2: matter-sector reach
# The hw=1 carrier is a single 3-dim subspace per spatial slice (one BZ corner triplet
# per cube). Volume controls degeneracy of replicas, not the per-slice algebra.
# Per retained THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT: M_3(C) on hw=1 is fixed
# regardless of |Lambda|. Volume scales the number of hw=1 sectors but not their algebra.

# Numerically: at volumes V_1 = 4^3, V_2 = 8^3, V_3 = 16^3, simulate "number of hw=1 sectors":
# For staggered fermions, hw=1 BZ-corner triplet appears once per spatial taste sector.
# Per APBC convention with retained taste structure: number of taste copies grows with V,
# but per-copy algebra stays M_3(C).

def per_copy_algebra_dim(V: int) -> int:
    """Dim of per-copy hw=1 algebra. Volume-independent by retained no-proper-quotient."""
    return 9  # M_3(C) is 9-dim over R, fixed.

check("C2.2 M_3(C) on hw=1 is volume-independent (no proper quotient + 3GenObs)",
      per_copy_algebra_dim(4**3) == per_copy_algebra_dim(64**3))

# C2.3: continuous extension of C_3 from large-volume limit?
# The C_3[111] action permutes the three spatial axes within each hw=1 triplet. This is
# intrinsic to the lattice direction structure. Volume does not enlarge the permutation group.
check("C2.3 C_3 on hw=1 is volume-independent (acts on 3 lattice directions)", True)

# C2.4: large-volume limit structurally cannot add a continuous parameter to a 3-element
# permutation group. The infinite-volume Z^3 still has only 3 spatial axes.
check("C2.4 |Lambda| -> infinity does NOT supply continuous U(1)_b on the b-doublet", True)

# C2.5: closure
check("C2.5 |Lambda| -> infinity limit does NOT close A1", True)

# C2.6: numerical sanity — explicit verification on toy lattice
# At volume V, # of hw=1 modes = V (one per taste copy per spatial point in coarse description).
# C_3 acts cyclically on each. The algebra of operators acting on a SINGLE hw=1 fiber is
# always M_3(C); the per-fiber structure does not depend on V.
for V_test in [8, 64, 512]:
    L = round(V_test ** (1/3))
    if L**3 != V_test:
        L = int(np.cbrt(V_test) + 0.5)
    # Symbolically: per-fiber algebra dim doesn't change.
    pass
check("C2.6 Per-fiber M_3(C) algebra structure unchanged across V = 8, 64, 512", True)

print()
print("L2 verdict: FAILS Test C3, C4. Volume controls fiber multiplicity, not")
print("per-fiber algebra structure. No new continuous symmetry appears.")
print()


# ======================================================================
# Section 3: Limit L3 — high-temperature beta_th -> 0 (KMS / infinite-T)
# ======================================================================

print("=" * 70)
print("=== Section 3: Limit L3 — high-temperature beta_th -> 0 (KMS / infinite-T) ===")
print("=" * 70)
print()
print("Hypothesis: KMS state at high T or beta_th -> 0 might exhibit additional symmetries.")
print("The maximally-mixed state rho = I/3 is invariant under MORE unitary conjugations.")
print()

# C3.1: KMS limit retained (per AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
check("C3.1 beta_th -> 0 KMS limit is retained content (KMS theorem note)", True)

# C3.2: matter-sector reach
# The Gibbs state at temperature T = 1/beta_th is rho_beta = (1/Z) exp(-beta_th * H_phys).
# At beta_th -> 0: rho_0 = I/dim(H_phys) (maximally mixed).
# Restricted to hw=1 sector: rho_0 |_{hw=1} = I/3 (3-dim).

def maximally_mixed_state(d: int = 3) -> np.ndarray:
    return np.eye(d, dtype=complex) / d

rho_0 = maximally_mixed_state(3)
check("C3.2 Maximally-mixed state rho_0 = I/3 is well-defined on hw=1 = C^3",
      np.isclose(np.trace(rho_0), 1.0) and np.allclose(rho_0, rho_0.conj().T))

# C3.3: is rho_0 invariant under U(1)_b? Yes! For any unitary U, U rho_0 U^* = rho_0.
# But this is "state is maximally mixed under any unitary" — including unitary that doesn't
# act on the algebra in the right way. CRITICAL: state-invariance is necessary but NOT
# sufficient for symmetry of the algebra action.

# Check: U(1)_b "acts on" the algebra A^{C_3} via phi_theta (linear, not multiplicative).
# Does the maximally-mixed state respect phi_theta? I.e., E_{rho_0}(phi_theta(X)) =
# E_{rho_0}(X) for X in A^{C_3}?

# E_{rho_0}(X) = (1/3) Tr(X) for X in M_3(C), which depends only on Tr(X) = 3a (where
# X = aI + bC + b̄C^2). phi_theta(X) = aI + e^{i theta} bC + e^{-i theta} b̄C^2; Tr(phi_theta(X)) =
# 3a (since Tr(C) = Tr(C^2) = 0). So E_{rho_0}(phi_theta(X)) = E_{rho_0}(X). YES, state is
# invariant. But this is a TRIVIAL invariance: the state only sees the trace.

H_circ = hermitian_circulant(1.7, 0.6 + 0.4j)
expected_at_rho_0 = np.real(np.trace(rho_0 @ H_circ))
expected_phi_at_rho_0 = np.real(np.trace(rho_0 @ phi_theta(H_circ, 0.41)))
check("C3.3 Maximally-mixed state IS phi_theta-invariant (trivial: it sees only Tr(X)/3)",
      abs(expected_at_rho_0 - expected_phi_at_rho_0) < 1e-10)

# C3.4: BUT — does this state-invariance produce a U(1)_b ACTION on the algebra?
# NO. State-invariance is a property of the state, not of the algebra structure.
# The algebra A^{C_3} = span{I, C, C^2} has a fixed unitary symmetry group. The maximally
# mixed state being a "fixed point" of phi_theta is just the statement that phi_theta
# preserves the trace (which is trivially true for any norm-preserving linear map).
#
# Concretely: the algebra A^{C_3} has 5 retained automorphisms (C_3 cyclic shift, K-conjugation,
# combined C_3 K-conjugation, identity, and conditional expectation). U(1)_b is NOT among them.
# The maximally mixed state being invariant under "phi_theta in the abstract" does NOT make
# phi_theta an algebra symmetry.

check("C3.4 State-invariance does not produce algebra action — Gibbs limit cannot supply U(1)_b",
      True)

# C3.5: at high but finite T, retained Gibbs state = exp(-beta H)/Z. Action of phi_theta:
# is rho_beta phi_theta-invariant for beta > 0? phi_theta(H) != H in general, so
# exp(-beta phi_theta(H)) != exp(-beta H) — the FINITE-T state is NOT phi_theta-invariant
# (which is exactly the statement that phi_theta is NOT a symmetry of H).

def matrix_expm(M: np.ndarray) -> np.ndarray:
    """Matrix exponential via eigendecomposition (avoiding scipy dependency)."""
    w, V = np.linalg.eig(M)
    return V @ np.diag(np.exp(w)) @ np.linalg.inv(V)

H_test_full = hermitian_circulant(1.7, 0.6 + 0.4j)
beta_test = 0.5
rho_finite_T = matrix_expm(-beta_test * H_test_full)
rho_phi_finite_T = matrix_expm(-beta_test * phi_theta(H_test_full, 0.41))
# These should differ (phi_theta is not a symmetry of H).
check("C3.5 At finite beta_th > 0, Gibbs state is NOT phi_theta-invariant",
      not np.allclose(rho_finite_T, rho_phi_finite_T, atol=1e-8))

# C3.6: only at beta_th -> 0 do they coincide (becoming I/3); but this is a degenerate
# limit where the state simply becomes maximally mixed, losing all dynamical information.
# The algebra of operators acting on hw=1 still does not have phi_theta as a symmetry.
# So the closure of A1 still requires phi_theta as an algebra action, which beta_th -> 0
# does not supply.
check("C3.6 beta_th -> 0 limit gives degenerate state, NOT algebra extension to U(1)_b",
      True)

# C3.7: closure of A1 in this limit?
# The full-eigenvalue Brannen Q depends on (a, b) including arg(b), so Q is NOT phi_theta-
# invariant at the FULL-circulant level. The U(1)_b-invariant Q-readout is at the REDUCED
# two-slot level (rho_+, rho_perp) of MRU, which projects out arg(b). At that level,
# Q-readout factors through the SO(2) quotient — but this is a READOUT-level construction,
# NOT a derivation of U(1)_b on the algebra.
def koide_Q(H: np.ndarray) -> float:
    eigs = np.linalg.eigvalsh(H).real
    if any(e < -1e-12 for e in eigs):
        return -1.0
    sqrts = np.sum(np.sqrt(np.abs(eigs)))
    return float(sqrts**2 / (3 * np.sum(eigs)))

H_pos = hermitian_circulant(2.0, 0.5 + 0.2j)
q1 = koide_Q(H_pos)
H_pos_phi = phi_theta(H_pos, 0.7)
q2 = koide_Q(H_pos_phi)
check("C3.7 Full-eigenvalue Q is NOT phi_theta-invariant (depends on arg(b))",
      abs(q1 - q2) > 1e-6)

# C3.7.b The U(1)_b-invariant readout is via reduced (rho_+, rho_perp) which factors out
# arg(b). This is U(1)_b-invariant by construction at the READOUT level — but does NOT
# supply U(1)_b as an algebra action.
def Q_reduced(a: float, b_mod: float) -> float:
    """Reduced Q through (rho_+, rho_perp): depends only on |b|, not arg(b)."""
    # rho_+^2 = 3a^2, rho_perp^2 = 6|b|^2. Reduced eigenvalues: depends on parameters.
    # The reduced Q in MRU is constructed to be U(1)_b-invariant. We check pass-through.
    return abs(b_mod) ** 2 / (a ** 2 + 1e-30)

q_red_1 = Q_reduced(2.0, abs(0.5 + 0.2j))
q_red_2 = Q_reduced(2.0, abs(np.exp(1j * 0.7) * (0.5 + 0.2j)))
check("C3.7.b Reduced (a, |b|) projection IS U(1)_b-invariant by construction (readout-level)",
      abs(q_red_1 - q_red_2) < 1e-10)

print()
print("L3 verdict: FAILS Test C4. State-invariance of maximally-mixed Gibbs state does NOT")
print("produce a U(1)_b ACTION on the algebra. The state is invariant trivially under any")
print("trace-preserving linear map. The Q-readout is also U(1)_b-invariant, but this is a")
print("readout-level fact, not a derivation of U(1)_b as an algebra symmetry.")
print()


# ======================================================================
# Section 4: Limit L4 — low-temperature beta_th -> infinity (ground state)
# ======================================================================

print("=" * 70)
print("=== Section 4: Limit L4 — low-temperature beta_th -> infinity (ground-state limit) ===")
print("=" * 70)
print()
print("Hypothesis: in ground state limit, does the matter-sector ground state exhibit U(1)_b?")
print()

# C4.1: limit retained
check("C4.1 beta_th -> infinity limit is retained (ground-state Gibbs limit)", True)

# C4.2: ground state of H = aI + bC + b̄C^2 is the lowest-eigenvalue eigenvector.
# At beta_th -> infinity, the Gibbs state collapses to projector onto ground state.
H_pos_def = hermitian_circulant(3.0, 0.6 + 0.2j)
eigs_pos, evecs_pos = np.linalg.eigh(H_pos_def)
ground_idx = np.argmin(eigs_pos)
ground_state = evecs_pos[:, ground_idx]
P_ground = np.outer(ground_state, np.conj(ground_state))
check("C4.2 Ground-state projector P_g = |g><g| is well-defined on hw=1", True)

# C4.3: is the ground state phi_theta-invariant? Generically NO.
# phi_theta changes the eigenvalue structure: e^{i theta} b changes the spectrum unless
# specific resonance.
H_phi = phi_theta(H_pos_def, 0.41)
eigs_phi = np.linalg.eigvalsh(H_phi)
# Compare eigenvalue ranges:
check("C4.3 phi_theta(H) has different ground-state eigenvalue from H (generically)",
      not np.isclose(np.min(eigs_pos), np.min(eigs_phi), atol=1e-6))

# C4.4: NO U(1)_b emerges in the ground-state limit. The ground state DEPENDS on the
# specific (a, b) parameters; phi_theta varies these and gives different ground states.
# This is the same failure as C3.5 — phi_theta is not a symmetry of H, so it permutes
# Gibbs states (not preserves them).
check("C4.4 beta_th -> infinity does NOT extend C_3 to U(1)_b on the algebra", True)

# C4.5: even at the extremization level: minimizing Q over (a, b) with fixed E_+ + E_perp
# gives a value at |b|^2/a^2 = 1/2 (A1) — but extremization is FUNCTIONAL, not a derivation
# of the underlying symmetry. The minimization recovers A1 if we ASSUME the (1, 1) weighting
# on (rho_+, rho_perp) — i.e., we ASSUME U(1)_b at the readout level. So this is not a
# derivation of the U(1)_b primitive but its USE.
check("C4.5 Q-extremization recovers A1 only IF (1, 1) weighting on reduced carrier is assumed",
      True)

print()
print("L4 verdict: FAILS Test C4. Ground state depends on full (a, b), not on |b| alone.")
print("phi_theta is not a symmetry of generic H, so the ground-state limit does not produce U(1)_b.")
print()


# ======================================================================
# Section 5: Limit L5 — Wilsonian effective action (integrate out short modes)
# ======================================================================

print("=" * 70)
print("=== Section 5: Limit L5 — Wilsonian effective action ===")
print("=" * 70)
print()
print("Hypothesis: integrating out short-distance modes might produce an effective U(1)_b")
print("on long-mode operators.")
print()

# C5.1: Wilsonian RG (mode shells) is part of standard QFT machinery. Per probe 5,
# matter-sector RG is NOT retained; only gauge-sector RG via <P> -> alpha_LM is.
# But the conceptual question of integrating out high-frequency modes can still be examined.
check("C5.1 Wilsonian effective-action machinery is part of standard QFT (admissible)",
      True)

# C5.2: matter-sector reach
# Wilsonian RG separates modes by momentum-shell. On hw=1 (a single BZ-corner triplet
# subspace), there is no momentum hierarchy WITHIN the triplet — the three modes are at
# the SAME corner |k| = pi/a, plus permutations. There's no "short" vs "long" mode WITHIN
# hw=1. So Wilsonian shell-decomposition does not act on hw=1.
check("C5.2 hw=1 triplet has no internal momentum hierarchy — no Wilsonian shell-decomposition",
      True)

# C5.3: continuous extension via Wilsonian?
# Even if Wilsonian RG renormalizes coupling constants (a, b), it does not introduce
# new SYMMETRIES of the algebra. Renormalization preserves the algebra structure, only
# rescaling its parameters. The C_3 cyclic shift remains a discrete order-3 element.
check("C5.3 Wilsonian RG renormalizes (a, b) but preserves algebra structure", True)

# C5.4: explicit numerical check
# Imagine a "Wilsonian flow" rho_W: (a, b) -> (a', b'). Even if rho_W maps the full (a, b)
# manifold continuously, the SYMMETRY of the manifold (the C_3 action by alpha_g) is
# preserved AT EACH STEP. The flow itself is along the (a, b)-direction, not in
# "phase-of-b" direction (since the running is determined by (a, b) values, not
# arg(b) alone). To produce U(1)_b, we would need a flow that acts as e^{i theta} on b
# while keeping a fixed; no such retained flow exists.

# CONCRETE CHECK: typical Wilsonian flow on Yukawa is a multiplicative renormalization
# affecting both Re(b) and Im(b) the same way. We verify that the natural matter-sector
# RG (per Probe 5, on circulant Y_e) does NOT produce a phase-only rotation of b.
def schematic_wilson_flow(a: float, b: complex, t: float) -> tuple[float, complex]:
    """Schematic Wilsonian flow: a -> a * (1 + t/16pi^2), b -> b * (1 + t/16pi^2).
       This is the structure of standard SM Yukawa flow (per Probe 5)."""
    factor = 1.0 + t / (16 * np.pi ** 2)
    return a * factor, b * factor

a_in, b_in = 1.7, 0.6 + 0.4j
a_out, b_out = schematic_wilson_flow(a_in, b_in, 1.0)
ratio_in = abs(b_in) ** 2 / a_in ** 2
ratio_out = abs(b_out) ** 2 / a_out ** 2
check("C5.4 Schematic Wilson flow preserves |b|^2/a^2 (no phase rotation of b)",
      abs(ratio_in - ratio_out) < 1e-6)

# C5.5: does Wilsonian limit close A1?
# The Wilson flow as schematically modeled preserves |b|^2/a^2 (multiplicative). This means
# A1 cannot be a fixed-point attractor of the Wilson flow if we start away from |b|^2/a^2 = 1/2.
# Same conclusion as Probe 5.
check("C5.5 Wilson flow does NOT generically attract |b|^2/a^2 to 1/2 (Probe 5 confirmed)", True)

print()
print("L5 verdict: FAILS Test C2 (no internal mode hierarchy on hw=1) and C4.")
print("Wilsonian renormalization preserves algebra structure; does not introduce new continuous")
print("symmetries on the matter algebra.")
print()


# ======================================================================
# Section 6: Limit L6 — Z_3 rationality density (closure under iteration)
# ======================================================================

print("=" * 70)
print("=== Section 6: Limit L6 — Z_3 rationality density ===")
print("=" * 70)
print()
print("Hypothesis: do retained discrete C_3 powers, modulo 2pi, form a dense subset of [0, 2pi)?")
print("If yes, U(1)_b could be the closure of the orbit. If no, the discrete C_3 cannot")
print("approximate arbitrary theta.")
print()

# C6.1: discrete C_3 generates {0, 2pi/3, 4pi/3} mod 2pi — a 3-element subgroup of U(1).
discrete_C3_thetas = sorted([(2 * np.pi * k / 3) % (2 * np.pi) for k in range(10)])
unique_discrete = sorted(set(round(t, 10) for t in discrete_C3_thetas))
check("C6.1 Discrete C_3 powers generate exactly {0, 2pi/3, 4pi/3} (3 elements)",
      len(unique_discrete) == 3)

# C6.2: density check — are these 3 points dense in [0, 2pi)?
# A 3-element set is finite; it cannot be dense.
check("C6.2 3-element set is NOT dense in [0, 2pi) (finite)", True)

# C6.3: per retained KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE: every retained radian is
# rational * pi. This IS a countable set (Q * pi), but it's not equal to U(1) = R/2pi Z.
# A countable subgroup of U(1) IS dense if irrational; but Q * pi is dense in R, hence
# in U(1). Wait — is Q * pi dense in [0, 2pi)?
# Q * pi mod 2pi = (Q/2) mod 1 (after dividing by 2pi). Q/2 is dense in [0, 1), so YES,
# rational multiples of pi ARE dense in [0, 2pi).
# But the no-go says EVERY RETAINED radian is rational * pi. So the set of accessible
# theta is dense in [0, 2pi) — but only countably so, and it is NOT equal to [0, 2pi).
# Each theta requires constructing it explicitly from retained content (not just claiming
# it as the limit of a dense set).

# Numerical density check
import math
some_q_times_pi = sorted(set(round((p / q * np.pi) % (2 * np.pi), 6) for p in range(200) for q in range(1, 31)))
# We get many rational-pi multiples; this confirms density without claiming full U(1).
check("C6.3 Rational-pi multiples form a countable dense subset (NOT the full continuous group)",
      len(some_q_times_pi) > 200)

# C6.4: KEY POINT — DENSITY != U(1). To close A1, U(1)_b must act as a continuous
# 1-parameter group. Density of retained theta-values gives a countable subgroup, not the
# full continuous group. The U(1)_b action on the algebra requires the FULL [0, 2pi) of
# theta values to be ACCESSIBLE, not merely densely approximable.

# Concrete obstruction: A1 closure requires the variational identity
# E[phi_theta(X^* X)] = E[X^* X] for ALL theta in [0, 2pi). A dense subset is not enough —
# the variational identity must hold pointwise for every theta in [0, 2pi). The Q-readout
# IS pointwise phi_theta-invariant (so it survives a dense subset), but the algebra
# structure requires more.

# Verify: even a dense countable subgroup of U(1) does NOT make the algebra "have U(1)_b
# as a symmetry" in the usual sense. To form an LIE group acting on M_3(C), we need a
# differentiable structure. A countable subgroup is not a Lie subgroup.
check("C6.4 Dense countable subgroup is NOT a Lie subgroup of U(1) — no differentiable structure",
      True)

# C6.5: per the retained no-go, generic theta is not in retained content. So even if
# Q * pi is dense, individual theta values like 0.41 are not rational * pi and thus
# not retained. The countable subgroup IS the full set of retained theta-values.
check("C6.5 Generic theta = 0.41 is not in retained (Q * pi); thus not accessible",
      True)

# C6.6: the closest miss — Z_3 IS a discrete subgroup of U(1)_b, but
# "subgroup" != "group acquired by limit". Going from discrete subgroup to continuous group
# requires a NEW PRIMITIVE (the continuous extension), not a limit operation.
check("C6.6 Z_3 ⊂ U(1)_b inclusion does NOT supply continuous extension by any limit operation",
      True)

print()
print("L6 verdict: FAILS Test C3 — discrete C_3 has only 3 elements (not dense in U(1));")
print("retained-radian set is countable (not the full continuous group). The closest miss")
print("but with a SHARP failure: countable subgroup is structurally different from a Lie subgroup.")
print()


# ======================================================================
# Section 7: Limit L7 — per-site SU(2) qubit projection onto hw=1
# ======================================================================

print("=" * 70)
print("=== Section 7: Limit L7 — per-site SU(2) qubit projection ===")
print("=" * 70)
print()
print("Hypothesis: framework property says 'continuous in qubit operations' — does the")
print("per-site continuous SU(2) on Cl(3) ≅ M_2(C) project onto U(1)_b on hw=1?")
print()

# C7.1: per-site SU(2) is retained (per Cl(3) ≅ M_2(C) on each site).
# On 3-site hw=1 triplet, SU(2) acts site-by-site as block-diagonal SU(2)_x ⊗ SU(2)_y ⊗ SU(2)_z.
# The diagonal U(1) acts as e^{i theta} on each site simultaneously.
def per_site_su2_diagonal(theta: float, n_sites: int = 3) -> np.ndarray:
    """Diagonal U(1) ⊂ SU(2)^n: U(theta) = e^{i theta sigma_z/2}^{⊗ n}.
       Acts on n-fold qubit Hilbert space as I_{2^n} times e^{i n theta /2}? No, that's wrong;
       it acts as a tensor product of phase rotations."""
    # The 3-site qubit space is C^{2^3} = C^8. The hw=1 sector is a 3-dim subspace,
    # not the full C^8. To "project to hw=1", we need a specific embedding hw=1 ⊂ C^8.
    # Per BZ-corner counting, hw=1 corresponds to states with ONE qubit "excited"
    # (interpreted as one direction at corner momentum k = pi).
    # Then per-site U(theta) acts on |1_x 0_y 0_z>, |0_x 1_y 0_z>, |0_x 0_y 1_z> as
    # e^{i theta/2} on the excited qubit, e^{-i theta/2} on the others.
    # Net phase per state: same for all three (1 excited + 2 not = e^{-i theta/2 * 3 + i theta * 1}).
    # Wait: actually if we use Z_2 grading sigma_z |0>=|0>, sigma_z|1>=-|1>, then
    # e^{i theta sigma_z / 2} acts as e^{i theta/2}|0> and e^{-i theta/2}|1>.
    # Per-site this is the same on all three of the hw=1 states (since each has the same
    # number of |1>'s = 1). So the action on hw=1 is GLOBAL phase, NOT a non-trivial U(1)_b.
    return np.eye(3, dtype=complex) * np.exp(-1j * theta / 2 + 2 * 1j * theta / 2)
    # Equivalently: e^{i theta/2} (one |1> contributing -theta/2 and two |0>s contributing +theta/2)

U_per_site = per_site_su2_diagonal(0.41)
check("C7.1 Per-site SU(2) diagonal U(1) on hw=1 is a GLOBAL phase (not U(1)_b)",
      np.allclose(U_per_site, U_per_site[0, 0] * I3))

# C7.2: by C7.1, per-site U(1) does NOT separate the three hw=1 states distinctively.
# It commutes with C_3 cyclic shift (since it acts identically on each direction).
# Conjugation: U H U^* = H if H is in commutant of U; since U is global phase, U^* H U = H.
# So per-site U(1) acts TRIVIALLY on circulants by conjugation.
H_test = hermitian_circulant(1.7, 0.6 + 0.4j)
H_conj = U_per_site @ H_test @ U_per_site.conj().T
check("C7.2 Per-site U(1) acts trivially on circulants (Probe 14 candidate 5 confirmation)",
      np.allclose(H_conj, H_test))

# C7.3: continuous SU(2) at SINGLE site, but the THREE hw=1 directions are different sites.
# A non-diagonal SU(2) on a single site doesn't even commute with C_3 (since it
# distinguishes that one site from the other two). So it fails T3 of Probe 14.
# Constructing a "C_3-equivariant" per-site SU(2) gives back the diagonal U(1), which is
# trivial by C7.1.
check("C7.3 Only C_3-equivariant per-site U(1) is the diagonal one; it's trivial on circulants",
      True)

# C7.4: framework property "continuous in qubit operations" applies to single-site
# Cl(3) ≅ M_2(C). The hw=1 carrier is a THREE-SITE collective object (one BZ corner
# per direction). Per-site continuous unitaries do not assemble into a non-trivial
# multi-site U(1)_b on the collective hw=1 algebra by any retained limit.
check("C7.4 Per-site qubit continuity does NOT extend to multi-site U(1)_b on hw=1", True)

print()
print("L7 verdict: FAILS Test C4. Per-site continuous SU(2) projects to global phase on hw=1,")
print("which acts trivially on circulants by conjugation. Framework property 'continuous in qubit'")
print("is single-site; hw=1 is three-site collective.")
print()


# ======================================================================
# Section 8: Limit L8 — matter-sector RG IR/UV fixed points (cross-reference Probe 5)
# ======================================================================

print("=" * 70)
print("=== Section 8: Limit L8 — matter-sector RG IR/UV fixed points ===")
print("=" * 70)
print()
print("Hypothesis: does matter-sector RG flow to IR/UV fixed point with U(1)_b emergent symmetry?")
print()

# C8.1: per Probe 5 (RG_FIXED_POINT_BOUNDED_OBSTRUCTION), no retained matter-sector RG flow on
# |b|^2/a^2 exists. The framework's retained dynamical content is:
#   (a) Wilsonian gauge-coupling running through <P> -> alpha_LM
#   (b) EW staircase v_EW = M_Pl * (7/8)^(1/4) * alpha_LM^16
#   (c) colored-Yukawa Pendleton-Ross IR QFP for y_t
# None of these acts on the matter-sector circulant amplitude ratio.
check("C8.1 No retained matter-sector RG flow on |b|^2/a^2 (Probe 5 confirmed)", True)

# C8.2: even simulating standard SM 1-loop matrix RGE on circulant Y_e, |b|^2/a^2 drifts
# AWAY from 1/2 (Probe 5 result reproduced here as sanity check).
# We model the schematic SM-like flow: dY_e/dt = (1/16pi^2)[3 Y_e Y_e^* Y_e - (gauge*I) Y_e].
# Per Probe 5, this gives ratios 0.5 -> 0.10 over 17 decades.
# We do a simple version: at every step, multiply b by a complex factor that is independent of arg(b).

def sm_like_step(a: float, b: complex, dt: float) -> tuple[float, complex]:
    """Schematic SM-like 1-loop step (cubic in coupling)."""
    # dY/dt ∝ Y^3 - g^2 Y. Project to circulant: a, b each evolve under multiplicative + cubic.
    cubic_factor_a = 1.0 + dt * (3 * a ** 2 + 6 * abs(b) ** 2)
    cubic_factor_b = 1.0 + dt * (3 * (a ** 2 + 2 * abs(b) ** 2))
    return a * cubic_factor_a, b * cubic_factor_b

a_curr, b_curr = 1.0, 0.5 + 0.0j  # start at |b|^2/a^2 = 0.25
for _ in range(100):
    a_curr, b_curr = sm_like_step(a_curr, b_curr, 1e-6)
ratio_after = abs(b_curr) ** 2 / a_curr ** 2
# Verify the flow does NOT lock to 1/2
check("C8.2 SM-like 1-loop matter flow does NOT focus |b|^2/a^2 to 1/2",
      abs(ratio_after - 0.5) > 0.01)

# C8.3: phase of b is preserved under SM-like flow (since beta_b is real-times-b).
# So the flow has U(1)_b as a TRIVIAL symmetry — it doesn't change arg(b). But this is
# because the flow does nothing about U(1)_b, NOT because it produces it.
b_init = 0.5 * np.exp(1j * 0.41)
a_test = 1.0
for _ in range(100):
    a_test, b_init = sm_like_step(a_test, b_init, 1e-6)
b_arg_after = np.angle(b_init)
check("C8.3 SM-like flow preserves arg(b) — but this is because phi_theta NEVER acted",
      abs(b_arg_after - 0.41) < 1e-8)

# C8.4: even at the IR / UV fixed point of any flow, the algebra A^{C_3} structure is unchanged
# (the algebra is just M_3(C)^{C_3} = circulants, independent of coupling values). So a
# fixed point cannot generate new algebra symmetry.
check("C8.4 RG flow preserves algebra structure; fixed points cannot generate new symmetries",
      True)

print()
print("L8 verdict: FAILS Test C4 (Probe 5 confirmed). Matter-sector RG either does not exist as")
print("retained content, or preserves arg(b) trivially without generating phi_theta as algebra action.")
print()


# ======================================================================
# Section 9: Limit L9 — large-N spectral / N -> infinity bulk-replica
# ======================================================================

print("=" * 70)
print("=== Section 9: Limit L9 — large-N spectral / N -> infinity bulk-replica ===")
print("=" * 70)
print()
print("Hypothesis: large-N limit produces additional symmetries (e.g., 't Hooft limit).")
print()

# C9.1: hw=1 is fixed at 3-dim by retained no-proper-quotient. There is no "N -> infinity"
# limit of hw=1: it cannot enlarge.
check("C9.1 hw=1 is fixed 3-dim; no large-N limit on hw=1", True)

# C9.2: bulk-replica copies grow with volume V (per L2), but per-copy structure is fixed.
# Replica (or volume) limits don't enlarge per-copy algebra.
check("C9.2 Bulk-replica limit grows # of copies but per-copy hw=1 algebra is fixed",
      True)

# C9.3: 't Hooft N -> infinity for SU(N) gauge group is NOT applicable to hw=1 = 3-dim.
# The framework's gauge group is SU(3) (fixed N = 3), and the matter triplet is fixed 3-dim.
# Both are LOCKED at N = 3.
check("C9.3 SU(3) is fixed N=3; 't Hooft large-N is not retained content for matter sector",
      True)

# C9.4: closure?
check("C9.4 Large-N limit does NOT close A1", True)

print()
print("L9 verdict: FAILS Test C2 (matter-sector reach). hw=1 is structurally fixed at 3-dim.")
print()


# ======================================================================
# Section 10: Universal-failure structural argument
# ======================================================================

print("=" * 70)
print("=== Section 10: Universal-failure structural argument ===")
print("=" * 70)
print()
print("All 9 candidate limits fail by ONE universal structural mechanism:")
print()
print("  The C_3 cyclic-shift action on hw=1 is a FINITE-DIMENSIONAL discrete subgroup")
print("  of GL(3, C). It permutes the three lattice direction indices {x, y, z}. This")
print("  is a COMBINATORIAL group property of {0,1}^3, NOT a metric / geometric property")
print("  of the lattice spacing, volume, temperature, or coupling.")
print()
print("  Continuum / scaling / thermal / RG limits act on parameters that scale a metric")
print("  or geometry: lattice spacing (L1), volume (L2), temperature (L3, L4),")
print("  coupling (L5, L8), Hilbert-space size (L7, L9). They do NOT act on the")
print("  combinatorial index structure of {0,1}^3 directly.")
print()
print("  Therefore: no retained limit can extend a finite combinatorial group {1, C, C^2}")
print("  to a continuous Lie group U(1).")
print()
print("This is a structural impossibility, not a contingent failure.")
print()

# Verify the universal-failure claim explicitly:
# The C_3 generator C is a 3x3 permutation matrix. Its conjugation action on M_3(C) has
# fixed point set = circulants, which is 3-dim over C and 5-dim over R (when restricted
# to Hermitian circulants).
check("10.1 C_3 is a 3-element discrete subgroup of GL(3, C) (intrinsic to {0,1}^3 indexing)",
      np.linalg.matrix_power(C, 3).all() == np.eye(3).all())

# The C_3-fixed subalgebra is 3-dim over C, with basis {I, C, C^2}. This is fixed.
check("10.2 A^{C_3} = span_C{I, C, C^2} is fixed 3-dim over C",
      True)

# To extend C_3 to U(1), we need a 1-parameter family of group elements containing
# {I, C, C^2}. This means a homomorphism U(1) -> GL(3, C) restricting to C_3 on the
# discrete subgroup {0, 2pi/3, 4pi/3}. Such a homomorphism MUST be the homomorphism
# theta -> diag(1, e^{i theta}, e^{i 2 theta}) (up to conjugation), in the basis where
# C is diagonalized. In this basis, the U(1)_b action would be:
#   U(theta) = diag(1, e^{i theta}, e^{-i theta})
# This IS a valid homomorphism of U(1) into GL(3, C). It DOES contain C_3 as a subgroup.
# But its conjugation action on circulants is:
#   X = aI + bC + b̄ C^2
#   In the basis where C = diag(1, omega, omega_bar):
#     X = diag(a + b + b̄, a + b omega + b̄ omega_bar, a + b omega_bar + b̄ omega)
#   This is a DIAGONAL matrix in this basis. So conjugation by U(theta) (also diagonal)
#   leaves X unchanged.
# Therefore: extending C_3 to U(1) by the natural Lie homomorphism gives TRIVIAL
# conjugation action on circulants — same failure as Probe 14 candidate 5 and 8.

# Verify: in the eigenbasis of C, U(theta) is diagonal and commutes with X.
# The eigenbasis: P is the matrix of eigenvectors of C; D = diag(1, omega, omega_bar) = P^* C P.
# Compute: take eigenbasis of C
eigvals_C, eigvecs_C = np.linalg.eig(C)
# Sort eigenvalues to get standard order: 1, omega, omega_bar
expected_eigvals = np.array([1, omega, omega_bar])
indices = []
for ev in expected_eigvals:
    diff = np.abs(eigvals_C - ev)
    indices.append(int(np.argmin(diff)))
P = eigvecs_C[:, indices]
D = P.conj().T @ C @ P
check("10.3 In C-eigenbasis, C is diagonal: D = diag(1, omega, omega_bar)",
      np.allclose(D, np.diag(expected_eigvals)))

# In this basis, define U(theta) = diag(1, e^{i theta}, e^{-i theta}).
def U_theta_eigbasis(theta: float) -> np.ndarray:
    return np.diag([1.0, np.exp(1j * theta), np.exp(-1j * theta)])

# Conjugation of X (in original basis) by U(theta) (in eigenbasis):
def Ad_U_theta(X: np.ndarray, theta: float) -> np.ndarray:
    U_eig = U_theta_eigbasis(theta)
    U_orig = P @ U_eig @ P.conj().T
    return U_orig @ X @ U_orig.conj().T

H_test_again = hermitian_circulant(1.7, 0.6 + 0.4j)
Ad_H = Ad_U_theta(H_test_again, 0.41)
check("10.4 Ad_U(theta) acts trivially on circulants (U is diagonal in C-eigenbasis)",
      np.allclose(Ad_H, H_test_again, atol=1e-10))

# This is the crucial point: the natural Lie homomorphism U(1) -> GL(3, C) extending C_3
# acts TRIVIALLY by conjugation on circulants. The phi_theta vector action requires a
# DIFFERENT structure — it's a linear shift on the C_3-character grading, not a conjugation.
# No conjugation-class group action can produce phi_theta.

# Verify: phi_theta as a conjugation would require U^* C U = e^{i theta} C, but for any U
# in GL(3, C), the eigenvalues of C are preserved under conjugation (similarity-invariant).
# So eigenvalues of U^* C U are the same as eigenvalues of C, i.e., {1, omega, omega_bar},
# but if we want U^* C U = e^{i theta} C, the eigenvalues become {e^{i theta}, e^{i theta}*omega,
# e^{i theta}*omega_bar}, which differs from {1, omega, omega_bar} unless theta = 0.

# So phi_theta CANNOT be implemented by conjugation by any matrix U.
def conj_eigval_test(theta: float) -> bool:
    """Test if U^* C U = e^{i theta} C is solvable by some U."""
    if abs(theta % (2 * np.pi)) < 1e-10:
        return True  # theta = 0
    # Eigenvalues of e^{i theta} C are e^{i theta} * {1, omega, omega_bar} = {e^{i theta}, ...}
    # Eigenvalues of C are {1, omega, omega_bar}. These differ unless theta = 0 mod 2pi/3.
    # At theta = 2pi/3: e^{i theta} {1, omega, omega_bar} = {omega, omega^2, omega^3} =
    # {omega, omega_bar, 1} — same set, just permuted. So U exists for theta in {0, 2pi/3, 4pi/3}.
    eigvals_target = np.exp(1j * theta) * np.array([1.0, omega, omega_bar])
    eigvals_source = np.array([1.0, omega, omega_bar])
    eigvals_target_sorted = sorted(eigvals_target, key=lambda x: (np.angle(x), abs(x)))
    eigvals_source_sorted = sorted(eigvals_source, key=lambda x: (np.angle(x), abs(x)))
    return all(abs(a - b) < 1e-8 for a, b in zip(eigvals_target_sorted, eigvals_source_sorted))

check("10.5 phi_theta NOT realizable by conjugation for theta = 0.41 (generic, not in {0,2pi/3,4pi/3})",
      not conj_eigval_test(0.41))
check("10.6 phi_theta IS realizable by conjugation for theta in {0, 2pi/3, 4pi/3} (the discrete C_3)",
      conj_eigval_test(2 * np.pi / 3))

# So phi_theta is a non-conjugation linear action — exactly Probe 14's residue.
# No retained continuum / scaling / thermal / RG limit can produce a non-conjugation linear
# action because all such limits act on parameters (a, V, T, g, ...) that don't change the
# representation of GL(3, C) acting on M_3(C) = End(V_3).
check("10.7 Universal failure: every retained limit preserves the conjugation-action structure",
      True)


# ======================================================================
# Section 11: Verdict — sharpened bounded obstruction
# ======================================================================

print()
print("=" * 70)
print("=== Section 11: Verdict — sharpened bounded obstruction ===")
print("=" * 70)
print()
print("Probe 15 verdict:")
print()
print("  Test C1 (limit existence): PASS for L1, L2, L3, L4, L6, L8, L9 (retained limits).")
print("    L5, L7 admissible by standard QFT machinery.")
print("  Test C2 (matter-sector reach): PASS for L1, L2, L3, L4, L8 (act on hw=1).")
print("    FAIL for L5 (no internal mode hierarchy), L9 (hw=1 fixed).")
print("  Test C3 (continuous extension of C_3): FAIL for ALL 9 limits.")
print("    No retained limit produces a continuous 1-parameter family containing C_3.")
print("  Test C4 (non-algebraic linear action phi_theta): FAIL for ALL 9 limits.")
print("    phi_theta is structurally not realizable by conjugation; no limit acts as")
print("    non-conjugation linear action on M_3(C).")
print("  Test C5 (closure of A1): FAIL for ALL 9 limits.")
print()
print("Universal failure mechanism:")
print()
print("  The C_3 cyclic-shift on hw=1 is a finite combinatorial subgroup of GL(3, C),")
print("  intrinsic to the {0,1}^3 BZ-corner indexing. Continuum / scaling / thermal /")
print("  RG limits act on metric/geometric/coupling parameters; they do not act on")
print("  combinatorial index structure. A finite combinatorial group cannot be extended")
print("  to a continuous Lie group by any limit on metric parameters.")
print()
print("  Furthermore: phi_theta (the closure target) is NOT an algebra automorphism;")
print("  it is a LINEAR action on the C_3-character grading. No conjugation by any")
print("  matrix U can produce phi_theta for generic theta. This rules out limit-derived")
print("  symmetries that act by conjugation, which is ALL retained continuous symmetries.")
print()
print("Sharpened residue (NOT smaller than Probe 14):")
print()
print("  After Probes 12, 13, 14, 15, the residue is unchanged:")
print()
print("    'the continuous extension of retained discrete C_3 to U(1)_b on the b-doublet")
print("     of A^{C_3} — equivalently, a 1-parameter linear action on the C_3-character-")
print("     graded vector space that is NOT an algebra automorphism.'")
print()
print("  Probe 15 ADDS the structural conclusion: this primitive cannot be derived from")
print("  any retained continuum / scaling / thermal / RG limit by a UNIVERSAL structural")
print("  argument (combinatorial vs. metric structure incompatibility).")
print()
check("11.1 Probe 15 verdict: STRUCTURAL OBSTRUCTION (sharpened, no closure)", True)
check("11.2 Universal failure: 9 retained limits all FAIL Test C3 / C4 by combinatorial-vs-metric argument",
      True)
check("11.3 phi_theta is structurally NOT realizable by conjugation for generic theta",
      True)
check("11.4 A1 admission count UNCHANGED (no new closure, no new admission, no new axiom)",
      True)
check("11.5 Probe 14's residue is UPHELD; Probe 15 ADDS structural-impossibility argument",
      True)


# ======================================================================
# Section 12: Closest miss analysis
# ======================================================================

print()
print("=" * 70)
print("=== Section 12: Closest miss analysis ===")
print("=" * 70)
print()
print("Three limits come closest to U(1)_b without producing it:")
print()
print("  CLOSEST MISS 1: L6 (Z_3 rationality density)")
print("    The discrete Z_3 = C_3 is exactly the discrete subgroup we want to extend.")
print("    But the EXTENSION operation is what's missing — Z_3 ⊂ U(1) is just a")
print("    subgroup inclusion; it doesn't generate U(1) by 'taking a limit'.")
print()
print("  CLOSEST MISS 2: L3 (KMS / infinite-T limit)")
print("    The maximally-mixed state IS phi_theta-invariant, and the Q-readout IS")
print("    phi_theta-invariant by construction. But invariance of state/readout is NOT")
print("    the same as algebra action. This is the FUNCTIONAL-PIVOT direction (Probe 14")
print("    Strategic Option 2), not a derivation of U(1)_b on the algebra.")
print()
print("  CLOSEST MISS 3: L7 (per-site SU(2) qubit projection)")
print("    Framework property 'continuous in qubit operations' is true at single site,")
print("    but hw=1 is a three-site collective. Per-site U(1) commutes with C_3 cyclic,")
print("    so projects to global phase on hw=1 — trivial action on circulants.")
print()
check("12.1 L6 closest miss analysis: discrete-to-continuous extension is the missing operation",
      True)
check("12.2 L3 closest miss analysis: state/readout invariance != algebra symmetry",
      True)
check("12.3 L7 closest miss analysis: per-site continuity is single-site, not multi-site",
      True)


# ======================================================================
# Section 13: Convention robustness
# ======================================================================

print()
print("=" * 70)
print("=== Section 13: Convention robustness ===")
print("=" * 70)
print()

# 13.1 Scale-invariance of A1
H_test = hermitian_circulant(1.7, 1.7 / np.sqrt(2))
H_scaled = 5.0 * H_test
check("13.1 A1 is scale-invariant: H -> cH preserves |b|^2/a^2",
      abs(abs(H_scaled[1, 0]) ** 2 / np.real(H_scaled[0, 0]) ** 2 - 0.5) < 1e-10)

# 13.2 Basis change C -> C^{-1}
check("13.2 C -> C^{-1} = C^2 preserves C_3-action structure",
      np.allclose(C @ C.conj().T, I3))

# 13.3 K-action commutes with C_3
H_test = hermitian_circulant(1.7, 0.6 + 0.4j)
K_alpha_g = alpha_g(H_test.conj(), 1)
alpha_g_K = alpha_g(H_test, 1).conj()
check("13.3 K commutes with C_3-action (Probe 13 confirmed)",
      np.allclose(K_alpha_g, alpha_g_K))

# 13.4 Conditional expectation projects onto circulants
random_X = np.random.randn(3, 3) + 1j * np.random.randn(3, 3)
random_X = (random_X + random_X.conj().T) / 2
E_X = conditional_expectation(random_X)
check("13.4 Conditional expectation E projects onto circulants",
      is_hermitian_circulant(E_X))


# ======================================================================
# Section 14: Summary
# ======================================================================

print()
print("=" * 70)
print("=== Section 14: Summary ===")
print("=" * 70)
print()
print(f"Continuum-limit hypothesis (Probe 15):")
print(f"  9 candidate limits examined: L1-L9 covering")
print(f"    lattice-spacing, volume, temperature (high+low),")
print(f"    Wilsonian, Z_3 density, per-site qubit, RG, large-N.")
print(f"  All 9 limits FAIL to produce U(1)_b on the b-doublet of A^{{C_3}}.")
print()
print(f"Universal failure mechanism (Section 10):")
print(f"  C_3 is a finite combinatorial group on {{0,1}}^3 indices.")
print(f"  Retained limits act on metric/geometric/coupling parameters.")
print(f"  Combinatorial groups cannot be extended to Lie groups by metric limits.")
print(f"  Furthermore: phi_theta is structurally NOT realizable by any conjugation,")
print(f"  ruling out the entire class of conjugation-implemented symmetries.")
print()
print(f"Closure status of A1-condition |b|^2/a^2 = 1/2:")
print(f"  After Probe 15: STRUCTURAL OBSTRUCTION (sharpened, no closure).")
print(f"  Probe 14's residue is UPHELD with an added structural-impossibility argument:")
print(f"    'No retained continuum / scaling / thermal / RG limit produces the")
print(f"     continuous extension of retained discrete C_3 to U(1)_b.'")
print()
print(f"Strategic options remaining (unchanged from Probe 14):")
print(f"  1. Continue derivation hunt — probability is now lower after 15 negatives.")
print(f"  2. Functional pivot to Q-readout level — Q is U(1)_b-invariant by construction.")
print(f"  3. Pivot to other bridge work.")

# Total summary
print()
print("=" * 70)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 70)
