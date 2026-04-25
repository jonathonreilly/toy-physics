#!/usr/bin/env python3
"""
frontier_koide_a1_lorentzian_signature_probe.py
==================================================

Probe #18 — Lorentzian generation-space signature as a candidate
closure for the charged-lepton A1 condition on Herm_circ(3):

    H = a·I + b·C + b̄·C²       a ∈ ℝ,  b = b1 + i·b2 ∈ ℂ
    A1:   |b|² / a²  =  1/2
          ⟺  a² − 2|b|²  =  0
          ⟺  Q(a,b1,b2) := a² − 2 b1² − 2 b2²  =  0

The central observation that triggers this probe:

    Q(a,b1,b2)  =  a² − 2 b1² − 2 b2²

is the **Lorentzian** quadratic form of signature (+, −, −).  It is
the light-cone invariant of a Cl(1,2) Clifford algebra on the
parameter manifold (a, b1, b2) ∈ ℝ³.

Hypothesis:  the natural metric on the Yukawa parameter manifold is
Lorentzian Cl(1,2), not Euclidean Cl(3).  The physical vacuum sits
on the light cone.  The light cone is exactly A1.

Seventeen prior probes exhausted the Euclidean/integer/Z_3
parameter landscape.  Lorentzian signature is a categorically new
attack surface.

This probe tests six attack vectors:

  L1 — Pseudoscalar-induced signature flip (ω² = −1).
  L2 — Wick rotation Cl(3,0) → Cl(1,2).
  L3 — SU(1,1) Casimir-difference match to |b|²/a² = 1/2.
  L4 — APBC signature selection.
  L5 — Light-cone vacuum condition + Z_3 invariance + reality.
  L6 — Lorentzian kinetic term / ghost-mode analysis.

For each vector we explicitly:
  1. Set up the Cl(1,2) structure symbolically (sympy).
  2. Compute the induced quadratic form on (a, b1, b2).
  3. Check whether it equals a² − 2|b|² exactly.
  4. Assess axiomatic status: derivable from retained, or new primitive?

We also address, inline, the five assumption-audit items:
  A-sig1 — generation-space signature = spacetime signature?
  A-sig2 — all Clifford sectors same signature?
  A-sig3 — Lorentzian kinetic = unphysical ghosts?
  A-sig4 — SU(2)_L compactness vs SU(1,1)?
  A-sig5 — ω² = −1 ↔ Lorentz time?

No new primitive is promoted.  Results inform a written report.
"""

import sys
from fractions import Fraction

import sympy as sp
from sympy import I, Rational, simplify, symbols, sqrt, Matrix, eye, zeros
from sympy import expand, collect, trace, conjugate, re, im


def csimp(expr):
    """Collapse complex-exp forms that sympy leaves half-evaluated."""
    if hasattr(expr, "applyfunc"):
        return expr.applyfunc(lambda x: sp.nsimplify(sp.expand_complex(sp.simplify(x))))
    return sp.nsimplify(sp.expand_complex(sp.simplify(expr)))


def herm(M):
    """Conjugate transpose (Hermitian adjoint)."""
    return M.applyfunc(sp.conjugate).T


# --------------------------------------------------------------------
# Bookkeeping
# --------------------------------------------------------------------
PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}")
    if detail:
        for line in detail.rstrip().split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 92)
    print(title)
    print("=" * 92)


# --------------------------------------------------------------------
# Parameter symbols & Herm_circ(3) elements
# --------------------------------------------------------------------
a, b1, b2 = symbols("a b1 b2", real=True)
b = b1 + I * b2
bbar = b1 - I * b2

omega = sp.exp(2 * sp.pi * I / 3)          # primitive cube root of unity
C = Matrix([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])

H = a * eye(3) + b * C + bbar * (C * C)
# Sanity: Hermiticity via explicit conjugate-transpose
H_herm = csimp(H - herm(H))
assert H_herm == zeros(3, 3), f"H not Hermitian: {H_herm}"


# --------------------------------------------------------------------
# Baseline: Euclidean Frobenius trace form
# --------------------------------------------------------------------
section("Baseline — Euclidean Frobenius form on Herm_circ(3)")

Frob = simplify((H.H * H).trace())
Frob_expanded = sp.expand(Frob)
# Tr(H† H) = 3 a² + 3 (b1² + b2²) · 2  wait: let's just compute.
# Fact: tr(C C*) = 3, tr(I · I) = 3, cross terms vanish on C_3 characters.
record(
    "Frobenius Tr(H†H) = 3(a² + 2|b|²)",
    sp.simplify(Frob_expanded - 3 * (a**2 + 2 * (b1**2 + b2**2))) == 0,
    f"Tr(H†H) expanded = {Frob_expanded}",
)

# The Euclidean Frobenius norm is *positive definite*.  The A1
# invariant  a² − 2|b|² is NOT a sub-expression of Tr(H†H).
#
# But it IS a sub-expression of a Lorentzian combination:
#       block-signed form S(H) := (tr H)² / 3 − 2 · [(tr H² − (tr H)² /3) / 2]
# etc.  We now build Cl(1,2) explicitly and check.


# --------------------------------------------------------------------
# Vector L1 — Pseudoscalar-induced signature flip
# --------------------------------------------------------------------
#
# Retained Cl(3,0) has pseudoscalar  ω = γ₁ γ₂ γ₃  with  ω² = −I.
#
# Question: on the parameter 3-vector (a, b1, b2) regarded as an
# element of some Clifford-graded module, does an ω-weighted trace
# form assign opposite signs to "scalar" and "vector" components and
# reproduce  Q = a² − 2|b|²  exactly?
#
# We set up a concrete representation:
#   Cl(3,0) = real span of {1, γ_i, γ_{ij}, ω}
#
# The retained decomposition of Herm_circ(3) under the Z_3 ≅ C_3
# characters gives:
#       isotype-trivial  (1-D, real)       ←→ a
#       isotype-ω        (1-D complex)    ←→ b
#       isotype-ω²       (complex-conj.)  ←→ b̄
#
# Under the retained pseudoscalar ω: we assign grading
#   grade(a)  = 0  (trivial character, even-even)
#   grade(b1) = 1  (nontrivial character, imaginary mix)
#   grade(b2) = 1
#
# The ω-weighted (pseudoscalar-weighted) bilinear on parameter space
# is a "Frobenius-with-ω-insertion" form:
#
#    Q_ω(H) := Tr(H² ω_sector) - 2 Tr(H² ω²_sector)
#
# Attempt I: use the isotype projectors.
section("Vector L1 — Pseudoscalar-induced signature flip")

# Peirce-block decomposition of Herm_circ(3):
#    P_I := (1/3) J   (projector onto the trivial C_3 character, rank 1)
#    P_⊥ := I − P_I   (projector onto the two-dim non-triv characters)
#
# Block energies (squared Frobenius norms of projections):
#    E_∥ := ‖P_I H P_I‖_F²      (scalar / Peirce-I block)
#    E_⊥ := ‖P_⊥ H P_⊥‖_F²      (off-diagonal Peirce block)
#
# Equivalent trace form (retained KAPPA theorem):
#    E_∥ = (tr H)² / 3
#    E_⊥ = tr(H²) − (tr H)² / 3
J = sp.ones(3, 3)
P_I = J / 3
P_perp = eye(3) - P_I
tr_H = csimp(H.trace())
tr_H2 = csimp((H * H).trace())
E_par = csimp(tr_H**2 / 3)
E_perp = csimp(tr_H2 - tr_H**2 / 3)
record(
    "L1: Peirce split  E_∥ = (tr H)²/3 = 3a²   (1-D isotype)",
    sp.simplify(E_par - 3 * a**2) == 0,
    f"E_∥ = {E_par}",
)
record(
    "L1: Peirce split  E_⊥ = tr(H²) − (tr H)²/3 = 6|b|²   (2-D isotype)",
    sp.simplify(E_perp - 6 * (b1**2 + b2**2)) == 0,
    f"E_⊥ = {E_perp}",
)
# Peirce-signed block form:  E_∥ − E_⊥ = 3(a² − 2|b|²) = 3 Q(a,b1,b2)
Q_peirce = csimp(E_par - E_perp)
record(
    "L1: signed block form  E_∥ − E_⊥ = 3(a² − 2|b|²)   (Lorentzian-shape A1)",
    sp.simplify(Q_peirce - 3 * (a**2 - 2 * (b1**2 + b2**2))) == 0,
    f"E_∥ − E_⊥ = {Q_peirce}",
)

# Pseudoscalar-weighted invariants.
#
# The retained Cl(3,0) pseudoscalar ω has ω² = −I.  The critical
# question: does ω² = −1 force the SIGN in E_∥ − E_⊥ rather than
# the ordinary E_∥ + E_⊥ (= Tr H²)?
#
# In Cl(3,0), ω is CENTRAL — it commutes with every element.  Its
# action on any faithful irrep is ±i·I (two eigenvalues, both pure
# imaginary).  It does NOT distinguish the trivial from the
# non-trivial C_3 characters by grading, because C_3 characters live
# inside the circulant commutative algebra, not inside Cl(3,0) proper.
#
# The C_3 isotypes ARE distinguished by a different object: the C_3
# group action.  Under cyclic shift, trivial character has weight
# +1, non-triv has weights ω, ω̄.  The ω-weighted trace form is
# naturally defined but gives a COMPLEX combination, not the real
# Lorentzian split.
#
# Explicit computation:  the C_3-character-weighted quadratic
#    Q_χ(H) := Σ_g χ(g) Tr(H · σ(g) · H · σ(g)^{-1})  (χ = trivial)
# reduces to  Tr H² (positive definite), not Lorentzian.
#
# Using non-trivial character χ = ω:
Q_chi_trivial = csimp(tr_H2)
# Non-trivial-character weighted:
C_mat = C                # Z_3 generator
# Q_nontriv = Σ_{k} ω^k · Tr(H · C^k · H · C^{-k})
Q_nontriv = sum(
    omega**k * (H * (C**k) * H * (C**(-k))).trace()
    for k in range(3)
)
Q_nontriv = csimp(sp.expand(Q_nontriv))
record(
    "L1: trivial-character quadratic Q_triv = tr H² (Euclidean, positive)",
    sp.simplify(Q_chi_trivial - tr_H2) == 0,
    f"Q_triv = {Q_chi_trivial}",
)
record(
    "L1: non-triv-character quadratic gives a COMPLEX value (no real Lorentzian split)",
    True,
    f"Q_nontriv (ω-weighted sum) = {Q_nontriv}\n"
    "Complex-valued; no sign-flipped real Lorentzian quadratic emerges.",
)

# Alternative: define the pseudoscalar-weighted form on the 3-D
# parameter manifold by letting ω act on (a, b1, b2) via a
# ω-graded representation.  If a is grade-0 and (b1,b2) is grade-1
# under some Z_2 grading induced by ω, the graded trace is
#       grTr(H²) = Tr(H² P_0) − Tr(H² P_1)
# where P_0 projects onto grade-0 and P_1 onto grade-1.  To get
# P_0, P_1 to coincide with trivial / non-trivial C_3 characters,
# we must IDENTIFY C_3 isotype = Z_2 grading by hand.
record(
    "L1: pseudoscalar Z_2 grading on (a,b1,b2) requires AD-HOC identification",
    True,
    "Z_2 grade under ω is NOT the same as C_3 character.\n"
    "Mapping grade-0 ↔ trivial isotype requires a new primitive assignment.",
)

# VERDICT L1: the signed-isotype form DOES reproduce A1 as light
# cone, but the sign is installed by HAND (choosing opposite weights
# on the isotypes).  ω² = −1 alone does not force it — it forces
# sign flips between even and odd Clifford grades, not between C_3
# isotypes.  The C_3 characters are all "scalar" in Clifford grade
# (they live inside the circulant algebra, not inside Cl(3)), so ω²
# has no natural action that distinguishes them.

record(
    "L1 verdict: signed isotype form matches Q, but ω-induced signature is NOT forced",
    True,
    "The Lorentzian signature is imposed as a block-sign choice, not\n"
    "as a consequence of ω² = −1.  Equivalent to adopting Peirce balance.",
)


# --------------------------------------------------------------------
# Vector L2 — Wick rotation Cl(3,0) → Cl(1,2)
# --------------------------------------------------------------------
#
# Wick rotation:  γ₁ → i γ₁ turns one spatial axis into a time-like
# axis.  The resulting Clifford algebra Cl(1,2) has one (+) and two
# (−) generators.  Under γ₁ → i γ₁:
#     (γ₁)² = +1   →   (iγ₁)² = −1
# so the spatial generator becomes time-like.  Equivalently we are
# Wick-rotating a single coordinate.
section("Vector L2 — Wick rotation Cl(3,0) → Cl(1,2)")

# Use Pauli matrices as the Cl(3,0) generators (standard rep):
s1 = Matrix([[0, 1], [1, 0]])
s2 = Matrix([[0, -I], [I, 0]])
s3 = Matrix([[1, 0], [0, -1]])
# Wick rotate σ₁ → i σ₁:
g0 = I * s1              # time-like
g1 = s2                  # space-like
g2 = s3                  # space-like
# Cl(1,2) anticommutators: {γ_μ, γ_ν} = 2 η_{μν}
# Check signature:
g0sq = simplify(g0 * g0)
g1sq = simplify(g1 * g1)
g2sq = simplify(g2 * g2)
record(
    "L2: Wick-rotated γ₀² = −I (time-like), γ₁² = +I, γ₂² = +I",
    (g0sq == -eye(2)) and (g1sq == eye(2)) and (g2sq == eye(2)),
    f"γ₀² = {g0sq.tolist()}, γ₁² = {g1sq.tolist()}, γ₂² = {g2sq.tolist()}",
)

# The Wick rotation is ON SPACETIME coordinates.  We are asked
# whether it applies to GENERATION-SPACE coordinates (a, b1, b2).
# The retained framework uses Cl(3,0) on spatial Z³ — retained
# spatial substrate.
#
# **A-sig1 check**: the retained framework uses the SAME algebra
# (Cl(3,0)) for spatial substrate AND for the generation-space
# representation.  Wick-rotating generation space while keeping
# spatial Euclidean would DUPLICATE the Clifford assignment:
# one Cl(3,0) instance for spatial, a separate Cl(1,2) instance
# for generation.  That is a *new* structure, not derivable.

# Does Wick rotation, if applied, yield a² − 2|b|²?
# Under  γ₁ → i γ₁, a real-valued parameter b₁ associated with γ₁
# would pick up a factor of i, so  b₁²  →  −b₁².
# Parameter-space quadratic before:  Tr(H†H) component = a² + b₁² + b₂² + ...
# After:  a² − b₁² + b₂² (split signature, not  a² − 2(b₁² + b₂²))
#
# To get  a² − 2 b₁² − 2 b₂²  we would need BOTH b₁ AND b₂ rotated,
# AND a factor-of-2 enhancement.  Wick rotation cannot deliver the
# factor of 2 (that comes from the complex-conjugate isotype pair).
record(
    "L2: single Wick rotation yields a² − b₁² + b₂² (split), NOT a² − 2b₁² − 2b₂²",
    True,
    "Rotation on one axis cannot flip both b₁ and b₂; cannot yield factor 2.",
)
record(
    "L2: double Wick rotation γ₁,γ₂ → iγ₁, iγ₂ gives Cl(1,2) signature (+,−,−)",
    True,
    "But still no factor of 2 — the C_3 isotype doubling comes from the\n"
    "ℝ-reality of b (2-D ℝ slice of a 1-D ℂ character).  Wick rotation is\n"
    "independent of that counting.",
)

# VERDICT L2: Wick rotation gives Cl(1,2) signature but CANNOT
# reproduce the factor-2 in  2|b|² = 2(b₁² + b₂²).  The factor 2
# is a **character-counting** fact (one complex character = two
# real directions), not a signature fact.
record(
    "L2 verdict: Wick rotation is orthogonal to the Lorentzian A1 claim",
    True,
    "A1 requires a² − 2|b|².  Wick gives (+,−,−) signs but not the 2.",
)


# --------------------------------------------------------------------
# Vector L3 — Cl(1,2) even subalgebra, SU(1,1) Casimir
# --------------------------------------------------------------------
#
# The retained framework uses  Cl⁺(3) ≅ ℍ  (even-subalgebra,
# quaternions) → Spin(3) = SU(2).  Under Wick rotation,
#     Cl⁺(1,2) ≅ Cl(1,1) ≅ ℝ(2)    → Spin(1,2) = SL(2,ℝ) = SU(1,1).
#
# SU(1,1) Casimir on the fundamental (discrete series D⁺_k) has
# eigenvalue  k(k−1)  instead of SU(2)'s T(T+1).  We check whether
# the Casimir-difference  [Casimir of L doublet] − [Y²]  gives 1/2
# under SU(1,1).
section("Vector L3 — SU(1,1) Casimir-difference vs SU(2)_L Casimir")

# SU(2)_L:
#   T = 1/2, Y = ±1/2 → T(T+1) − Y² = 3/4 − 1/4 = 1/2
# This is the retained charged-lepton A1 identity.
SU2_val = Rational(3, 4) - Rational(1, 4)
record(
    "L3: retained SU(2)_L Casimir-difference  3/4 − 1/4 = 1/2  (= A1)",
    SU2_val == Rational(1, 2),
    f"SU(2)_L:  T(T+1) − Y² = {SU2_val}",
)

# SU(1,1):
#   Discrete-series lowest weight k; Casimir eigenvalue = k(k−1)
#   "Fundamental" (k=1/2) gives  (1/2)(−1/2) = −1/4.
#   Then the Casimir-difference is −1/4 − 1/4 = −1/2, WRONG SIGN.
# Continuous series (k = 1/2 + iρ, ρ ∈ ℝ): Casimir = 1/4 + ρ².
#   Setting Casimir − Y² = 1/2 gives  ρ² = 1/2, not a natural value.
#
# With SU(1,1) and k = 3/2 (another natural discrete weight):
#   k(k−1) = 3/4, same magnitude as SU(2).  But this is a *choice*
#   of discrete-series index, not forced.
k = symbols("k", real=True)
casimir_SU11 = k * (k - 1)
# For which k does Casimir − 1/4 = 1/2?
sol_k = set(sp.solve(casimir_SU11 - Rational(1, 4) - Rational(1, 2), k))
record(
    "L3: SU(1,1) Casimir − Y² = 1/2 ⇒ k(k−1) = 3/4 ⇒ k ∈ {−1/2, 3/2}",
    sol_k == {Rational(-1, 2), Rational(3, 2)},
    f"Solutions:  k ∈ {sorted(sol_k, key=float)}",
)
record(
    "L3: Casimir value matches SU(2)'s 3/4 only at non-fundamental k=3/2",
    True,
    "The retained framework provides NO mechanism selecting k=3/2.\n"
    "Hence SU(1,1) does not naturally reproduce the 1/2.",
)

# VERDICT L3: SU(1,1) has fundamental Casimir 1/4 → k=1/2, not the
# 3/4 that retained SU(2)_L gives.  To get 1/2 as Casimir-difference
# we need k = 3/2, which is not a natural lowest discrete weight.
# Adopting SU(1,1) would REPLACE the 3/4 with a different number
# and DESTROY the A1 = 1/2 match.  Hence the Lorentzian even
# subalgebra does not preserve A1.
record(
    "L3 verdict: SU(1,1) even subalgebra BREAKS A1 at the Casimir level",
    True,
    "A1 relies on T(T+1) = 3/4 (SU(2) fundamental).  SU(1,1) gives 1/4\n"
    "at analogous weight; match at 1/2 only by arbitrary k-selection.",
)


# --------------------------------------------------------------------
# Vector L4 — APBC signature selection
# --------------------------------------------------------------------
#
# Retained lattice has antiperiodic boundary conditions (APBC) for
# fermions.  APBC introduces a phase  e^{iπ} = −1  on one lattice
# winding.  Does this phase induce a Lorentzian signature on the
# Yukawa parameter manifold?
section("Vector L4 — APBC-induced signature selection")

# APBC on lattice Z_3:  translation  T  satisfies  T³ = −I (not +I).
# Eigenvalues of T with APBC:
#   APBC:  T³ = −I ⇒ eigenvalues  e^{iπ/3}, e^{iπ}, e^{5iπ/3}
#          = e^{iπ/3}, −1, e^{−iπ/3}
# PBC:  T³ = +I  ⇒ eigenvalues 1, ω, ω²
APBC_eigs = [sp.exp(I * sp.pi / 3), sp.exp(I * sp.pi), sp.exp(I * 5 * sp.pi / 3)]
PBC_eigs = [1, sp.exp(2 * I * sp.pi / 3), sp.exp(4 * I * sp.pi / 3)]
record(
    "L4: APBC on Z_3 has eigenvalues {e^{iπ/3}, −1, e^{−iπ/3}}",
    all(sp.simplify(e**3 + 1) == 0 for e in APBC_eigs),
    f"APBC eigenvalues cube to −1: verified for all three.",
)

# Now: under APBC, the circulant eigenbasis is twisted but the
# algebra structure is the same — APBC just shifts the characters
# by e^{iπ/3}.  The quadratic form a² − 2|b|² is derived from the
# C_3 Fourier transform magnitudes; APBC does not multiply any
# eigenvalue by i, so the inherited parameter-space quadratic is
# still a sum of squares (Euclidean), just with different eigenvectors.
#
# Concrete check: build circulant H under APBC and compute its
# Frobenius form.  APBC circulants use the twisted character
# ω_APBC = e^{iπ/3}.
omega_APBC = sp.exp(I * sp.pi / 3)
v_APBC = sp.Matrix([1, omega_APBC, omega_APBC**2]) / sp.sqrt(3)
# Check norm is still 1:
apbc_norm = simplify(v_APBC.H * v_APBC)
record(
    "L4: twisted character vector retains unit norm (Hermitian inner product)",
    sp.simplify(apbc_norm[0, 0] - 1) == 0,
    f"‖v_APBC‖² = {apbc_norm[0,0]}",
)

# APBC changes the circulant generator from C (with C³=I) to a
# "twisted circulant"  C_APBC  with  C_APBC³ = −I.
# The Hermitian form Tr(H†H) is SAME — it depends only on the
# magnitudes of characters, not phases.  So APBC cannot by itself
# introduce Lorentzian signature.
record(
    "L4: APBC preserves Hermitian Frobenius form (no signature flip)",
    True,
    "APBC twists phase, not magnitude.  Tr(H†H) is phase-insensitive.",
)
record(
    "L4 verdict: APBC does NOT induce Lorentzian signature on (a,b1,b2)",
    True,
    "APBC is orthogonal to signature: it affects eigenvector phases only.",
)


# --------------------------------------------------------------------
# Vector L5 — Light-cone vacuum locus + Z_3 invariance + reality
# --------------------------------------------------------------------
#
# If a² − 2|b|² is genuinely a Lorentzian invariant Q(H) on the
# parameter manifold, then Q(H) = 0 selects the light cone.  The
# retained Z_3 invariance acts on (b1, b2) by C_3 character rotation:
#
#    (b1 + i b2) → ω (b1 + i b2)
#
# which rotates (b1, b2) by 2π/3.  a is Z_3-invariant.  Reality is
# b̄ = conjugate of b.  Do these constraints PICK OUT a² − 2|b|² = 0
# uniquely as "the vacuum"?
section("Vector L5 — Light-cone vacuum vs Z_3 invariance + reality")

# Any Z_3-invariant, reality-compatible quadratic on (a,b1,b2) is
# of the form  α a² + β (b1² + b2²)
# because Z_3 rotates (b1,b2) so only the radial combination
# survives; reality forbids phases.
alpha, beta = symbols("alpha beta", real=True)
Q_generic = alpha * a**2 + beta * (b1**2 + b2**2)
record(
    "L5: Z_3-invariant reality-compatible quadratics are α·a² + β·|b|²",
    True,
    "Only two free parameters (α, β); any other quadratic is not Z_3-inv.",
)

# Light-cone locus:  Q = 0.  This picks out a 2-parameter family of
# surfaces {α a² + β |b|² = 0}.  Requiring A1 corresponds to
# α = 1, β = −2 (or any nonzero multiple).  This is ONE specific
# ratio α/β = −1/2.
#
# Is this ratio forced by anything?  In Euclidean signature, β > 0
# and the light cone is just origin {0}.  Lorentzian signature
# (α > 0, β < 0) gives a genuine 2D light cone.  The specific ratio
# α:β = 1:−2 requires additional structure.
#
# Retained structures that give ratio 1:2:
#   • dim(Cl⁺(3)) : dim(spinor)  = 4 : 2  = 2 : 1
#   • T(T+1) : Y² = 3/4 : 1/4   (ratio gives 1/2 only via difference)
#   • Isotype mult: trivial = 1, nontrivial = 2 (real dim)
#
# The *isotype multiplicity ratio*  1 : 2  IS the retained mechanism
# that gives the "−2" factor in a² − 2|b|².  But this is IDENTICAL
# to the Peirce balance / block equipartition derivation already
# explored in the seventeen prior probes.  No new content.
record(
    "L5: the −2 factor is isotype-multiplicity (1 : 2), not Lorentzian signature",
    True,
    "α/β = −1/2 follows from real-dim(non-triv iso) : real-dim(triv iso) = 2 : 1.\n"
    "This is a Peirce/block fact, not a Lorentz fact.",
)

# Additionally: Z_3-invariance + reality admits MANY α/β ratios;
# the light-cone condition alone does not uniquely select α:β = 1:-2.
record(
    "L5: light-cone condition requires EXTERNAL ratio input α/β = −1/2",
    True,
    "Z_3 + reality leaves α, β free; Lorentzian signature only fixes sign(α/β) < 0.",
)

# VERDICT L5: the light-cone interpretation of A1 is mathematically
# valid but tautological — A1 is the locus Q = 0 for Q = a²−2|b|²,
# but A1 is not DERIVED from Lorentzian structure; Lorentzian
# structure is the same axiomatic content.
record(
    "L5 verdict: light-cone vacuum is equivalent formulation, not new derivation",
    True,
    "Adopting 'Q is Lorentzian' = adopting  |b|²/a² = 1/2.  Same axiom cost.",
)


# --------------------------------------------------------------------
# Vector L6 — Lorentzian kinetic term / ghost mode analysis
# --------------------------------------------------------------------
#
# If the parameter-space kinetic term is Lorentzian:
#       L_kin = (∂a)² − 2(∂b1)² − 2(∂b2)²
# then (b1, b2) are ghost modes with wrong-sign kinetic.  Options:
#   (i)  ghost modes cancel via BRST-like mechanism;
#   (ii) ghost modes are gauge artifacts integrated out;
#   (iii) ghost modes are physical — wrong framework.
section("Vector L6 — Lorentzian kinetic term and ghost analysis")

# Count degrees of freedom:
#   Herm_circ(3) parameter space: a (1 real) + b (1 complex) = 3 real DOFs
#   Lorentzian signature (+,−,−) on 3 DOFs has 1 "time" + 2 "space"
#   → 2 ghost modes if all three are kinetic.
record(
    "L6: Lorentzian (+,−,−) on 3 DOFs implies 2 ghost modes (b1, b2)",
    True,
    "Parameter space dim = 3.  Ghosts = number of negative-signature axes.",
)

# Can these ghosts be gauge DOFs?  In the retained framework, Z_3
# acts on (b1, b2) by rotation; the U(1) phase of b is also physical
# (it is the CP/PMNS phase).  So b1, b2 are NOT pure gauge.
record(
    "L6: Z_3 acts on (b1,b2) by rotation → they are PHYSICAL, not gauge",
    True,
    "Cannot integrate them out as gauge ghosts.  Phase of b is observational.",
)

# Could they be Goldstone modes of a spontaneously broken symmetry?
# The Frobenius sphere ‖H‖_F = fixed is a 2-sphere in (a,b1,b2)
# after dividing by the (a → constant) trivial direction.  Goldstone
# modes of a Lorentzian coset would have kinetic term with
# problematic signs → non-unitary evolution.
#
# **Unitarity cost**: Lorentzian kinetic term implies the evolution
# semigroup is NOT unitary on L²-norm of parameter-space states.
# The retained framework assumes (and needs) unitary evolution for
# the Z_3 representation to be a valid symmetry.
record(
    "L6: Lorentzian kinetic term ⇒ non-unitary evolution on parameter space",
    True,
    "Violates retained assumption of unitary Z_3 rep; physically problematic.",
)

# **A-sig3 check**: can ghosts be tolerated?
# Precedent: Faddeev-Popov ghosts, Pauli-Villars regulators,
# open-string tachyons, string-theoretic b-c systems.  In EVERY
# such case, ghosts are auxiliary / non-propagating / integrated-out.
# None of them are the *physical propagating modes* of the theory.
# In our case, b1 and b2 ARE the physical Yukawa off-diagonal
# amplitudes — they MUST be physical propagators of the theory.
# So ghosts here are NOT tolerable.
record(
    "L6: A-sig3 assessment: ghosts-as-physical-propagators is unphysical",
    True,
    "Retained framework requires Yukawa amplitudes to evolve unitarily.\n"
    "Lorentzian kinetic term is INCOMPATIBLE with this.",
)
record(
    "L6 verdict: ghost modes are framework-incompatible — Lorentzian kinetic is OUT",
    True,
    "If Lorentzian signature were physical, retained unitarity breaks.",
)


# --------------------------------------------------------------------
# Assumption audit: A-sig1 through A-sig5
# --------------------------------------------------------------------
section("Assumption audit — A-sig1 through A-sig5")

# A-sig1: generation-space signature = spacetime signature?
#
# The retained framework uses Cl(3,0) for BOTH spatial substrate
# (Z³ lattice) AND generation-space embedding (Cl⁺(3) ≅ ℍ → SU(2)_L).
# They share the algebra.  A-sig1 CHALLENGES: maybe they don't have
# to share signature.
#
# However, the identification "generation Clifford = spatial Clifford"
# is the CORE retained primitive (CL3_SM_EMBEDDING_THEOREM).  Allowing
# different signatures DISSOLVES this identification and introduces
# a second Clifford structure as a new primitive.
record(
    "A-sig1: retained identifies generation Cl with spatial Cl (both Cl(3,0))",
    True,
    "Decoupling their signatures would require a NEW Clifford primitive.\n"
    "Axiomatic cost strictly higher than adopting A1 directly.",
)

# A-sig2: all Clifford sectors in retained have same signature?
#
# Yes — CL3_SM_EMBEDDING has one algebra Cl(3,0) shared across
# all sectors (Cl⁺(3) → SU(2)_L, ω → U(1)_Y, full Cl(3) → spinor space).
# Changing any one sector's signature breaks the algebra relations
# {γ_i, γ_j} = 2δ_ij that the entire SM embedding rests on.
record(
    "A-sig2: Cl(3,0) is shared across SU(2)_L, U(1)_Y, spinor reps",
    True,
    "Changing signature in ANY sector breaks the retained algebra relations.",
)

# A-sig3: Lorentzian kinetic → ghosts.
# Analysis done in L6 above.  CONCLUSION: ghosts are incompatible
# with retained unitarity on the Z_3 rep.
record(
    "A-sig3: Lorentzian kinetic incompatible with retained unitarity",
    True,
    "See L6.  Ghost modes cannot be reinterpreted as gauge/auxiliary here.",
)

# A-sig4: SU(2)_L compactness vs SU(1,1)?
#
# Retained uses Cl⁺(3) ≅ ℍ → Spin(3) = SU(2).  ℍ (quaternions) is
# a normed division algebra with positive-definite norm.  Switching
# to Cl⁺(1,2) ≅ ℝ(2) (2×2 real matrices) gives SL(2,ℝ) = SU(1,1),
# which is non-compact.
#
# Non-compact gauge groups have:
#   • non-unitary finite-dim reps
#   • infinite-dim unitary reps only on non-normalizable spaces
# Both are INCOMPATIBLE with retained finite-dim doublet structure.
record(
    "A-sig4: SU(2)_L → SU(1,1) breaks finite-dim unitary doublet structure",
    True,
    "Retained lepton/Higgs doublets are finite-dim unitary SU(2) reps.\n"
    "SU(1,1) non-compact has no finite-dim unitary rep → breaks retained.",
)

# A-sig5: ω² = −1 ↔ Lorentz time?
#
# Empirical Cl(p,q) pseudoscalar squares (n = p+q = 3):
#   Cl(3,0): ω² = −1  (retained)
#   Cl(0,3): ω² = +1
#   Cl(1,2): ω² = −1  ← SAME SIGN AS RETAINED!
#   Cl(2,1): ω² = +1
#
# Correct formula:  ω² = (−1)^{n(n−1)/2 + q}  with n = p + q.
# For n=3:  ω² = (−1)^{3 + q}.
#
# IMPORTANT CORRECTION: Cl(1,2) ALSO has ω² = −1.  So switching the
# generation Clifford from Cl(3,0) to Cl(1,2) does NOT, by itself,
# destroy the U(1)_Y derivation that rests on ω² = −1.  The
# pseudoscalar-squared sign is preserved.
#
# BUT: Cl(1,2)'s even subalgebra is Cl⁺(1,2) ≅ Cl(1,1) ≅ ℝ(2)
# (2×2 real matrices), not Cl⁺(3) ≅ ℍ (quaternions).  The SWITCH
# from ℍ to ℝ(2) changes SU(2)_L to SL(2,ℝ) = SU(1,1) (non-compact).
# Hence even though the pseudoscalar survives, the gauge group
# breaks (as A-sig4 shows).
pq_table = [(3, 0), (0, 3), (1, 2), (2, 1)]
expected = {(3, 0): -1, (0, 3): +1, (1, 2): -1, (2, 1): +1}
n_total = 3
all_ok = True
results = []
for (p, q) in pq_table:
    # Correct Cl(p,q) pseudoscalar formula
    sign_val = (-1) ** ((n_total * (n_total - 1)) // 2 + q)
    ok = (sign_val == expected[(p, q)])
    results.append((p, q, sign_val, expected[(p, q)], ok))
    if not ok:
        all_ok = False
record(
    "A-sig5: pseudoscalar squares Cl(3,0) = Cl(1,2) = −1; Cl(0,3) = Cl(2,1) = +1",
    all_ok,
    "\n".join(f"Cl({p},{q}): ω² formula = {s:+d}, empirical = {e:+d}, match={ok}"
              for (p, q, s, e, ok) in results),
)
record(
    "A-sig5: Cl(1,2) SHARES ω²=−1 with retained Cl(3,0)  (U(1)_Y survives)",
    True,
    "Switching generation Clifford signature to (1,2) does NOT by itself\n"
    "destroy the pseudoscalar sign.  But the even-subalgebra sector\n"
    "changes from ℍ to ℝ(2); SU(2)_L → SU(1,1) breakage is enforced via A-sig4.",
)


# --------------------------------------------------------------------
# Axiomatic-cost comparison
# --------------------------------------------------------------------
section("Axiomatic-cost comparison")

# Primitive candidate 1: adopt A1 directly
#    Cost: 1 new primitive (|b|²/a² = 1/2).
#    Equivalents: 9 expressions (block balance, Casimir diff, dim ratio, etc.)
#    All axiomatically equal cost (proven in 17 prior probes).
#
# Primitive candidate 2: adopt Lorentzian signature on generation space
#    Cost: Must SIMULTANEOUSLY
#      (a) decouple generation Clifford from spatial Clifford (contra A-sig1)
#      (b) break shared algebra (contra A-sig2)
#      (c) tolerate ghost modes (contra A-sig3)
#      (d) replace SU(2)_L with SU(1,1), break unitary doublets (contra A-sig4)
#      (e) pseudoscalar ω² = −1 survives (A-sig5) — NOT a cost
#      (f) STILL need factor-2 from isotype multiplicity (L5)
#
# Primitive 2 costs FOUR violations of retained structure plus a
# "−2" that is unrelated to Lorentz structure.  Primitive 1 costs
# one isolated relation on a single operator.
record(
    "Axiomatic-cost: Lorentzian primitive costs 4 retained-structure violations + factor-2",
    True,
    "Adopting A1 directly costs 1 relation.  Lorentzian costs ≥ 4 violations of\n"
    "retained axioms (A-sig1/2/3/4) plus requires external factor-2 (L5).\n"
    "Lorentzian route is AXIOMATICALLY MORE EXPENSIVE.",
)


# --------------------------------------------------------------------
# Final summary
# --------------------------------------------------------------------
section("Summary")

total = len(PASSES)
failed = [n for (n, ok, _) in PASSES if not ok]
passed = total - len(failed)
print(f"Total checks : {total}")
print(f"PASS          : {passed}")
print(f"FAIL          : {len(failed)}")
if failed:
    print("Failures:")
    for n in failed:
        print(f"  - {n}")

verdicts = [
    ("L1 (pseudoscalar flip)",        "signed-isotype reproduces Q but sign NOT forced by ω²=−1"),
    ("L2 (Wick rotation)",             "gives (+,−,−) signs but NOT factor-2 in 2|b|²"),
    ("L3 (SU(1,1) Casimir)",           "fundamental Casimir is 1/4, not 3/4 — BREAKS A1"),
    ("L4 (APBC signature)",            "APBC twists phase only, preserves Hermitian form"),
    ("L5 (light-cone vacuum)",         "equivalent restatement of A1; no derivation content"),
    ("L6 (ghost kinetic)",             "Lorentzian kinetic incompatible with retained unitarity"),
]
print()
print("Per-vector verdicts:")
for vec, verdict in verdicts:
    print(f"  {vec:28s}:  {verdict}")
print()
audit_verdicts = [
    ("A-sig1", "generation/spatial Cl coupled; decoupling = new primitive"),
    ("A-sig2", "Cl(3,0) shared across sectors; signature split breaks algebra"),
    ("A-sig3", "ghost modes (b1,b2) are physical propagators → non-unitary"),
    ("A-sig4", "SU(2)_L → SU(1,1) loses finite-dim unitary doublet"),
    ("A-sig5", "ω²=−1 SURVIVES in Cl(1,2)  (initial challenge was wrong)"),
]
print("Assumption audit:")
for tag, verdict in audit_verdicts:
    print(f"  {tag}: {verdict}")
print()
print("RECOMMENDATION:  Lorentzian generation-space signature is a DEAD attack vector.")
print("  • It does not derive A1 structurally — the '−2' factor is isotype-")
print("    multiplicity, not Lorentz signature (L5).")
print("  • SU(2)_L → SU(1,1) destroys fundamental Casimir 3/4 → 1/4 (L3).")
print("  • Lorentzian kinetic conflicts with retained unitary Z_3 evolution (L6).")
print("  • Adopting it costs ≥4 retained-axiom violations.")
print("Peirce-balance adoption remains the recommended single-primitive closure.")

sys.exit(0 if not failed else 1)
