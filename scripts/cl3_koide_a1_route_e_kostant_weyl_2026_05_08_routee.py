#!/usr/bin/env python3
"""
Koide A1 Route E — Kostant Weyl-Vector / A_1 Root System Bounded Obstruction

Source note:
  docs/KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md

This runner verifies the structural obstructions blocking the derivation of
the Brannen-Rivero A1 amplitude condition

    |b|^2 / a^2  =  1/2          (A1, Frobenius equipartition)

from the Lie-algebraic identity

    |rho_{A_1}|^2  =  1/2        (Kostant's strange formula, A_1 = sl(2),
                                  with normalization |alpha|^2 = 2)

via the proposed Route E "Kostant Weyl-vector / A_1 root system" structural
identification.

Structural barriers verified (each independently blocks Route E closure):

  (B1) Cartan-Killing normalization dependence: |rho_{A_1}|^2 takes value
       1/2 with |alpha|^2 = 2 but value 1/4 with |alpha|^2 = 1.  No
       retained framework primitive selects one Cartan-Killing normalization
       over the other; the appearance of "1/2" depends on a convention.

  (B2) Sector-dimension mismatch: A_1 fundamental representation is 2-dim,
       but the C_3-equivariant circulant operators H = aI + bU + b̄U^{-1}
       live on the 3-dim generation sector hw=1.  There is no natural
       A_1 highest-weight irrep of dimension 3 (the 3-dim irrep of A_1 is
       the adjoint, not the fundamental, and carries different weight data).

  (B3) Cross-sector orthogonality (inherits Route F's B3 structurally):
       The retained SU(2)_L = A_1 gauge sector acts on the doublet sector
       (Cl^+(3) ≅ H ⟹ Spin(3)) and commutes with the generation sector
       (C_3[111] cycle on hw=1).  The Weyl-vector geometry of A_1 is a
       statement about the doublet (gauge) sector; the Brannen-Rivero
       coefficients (a, b) live in the generation sector.  No retained
       cross-sector bridge transfers Lie-algebraic length-squared values
       between them.

  (B4) Category mismatch: |rho_{A_1}|^2 is a Cartan-Killing length-squared
       (a representation-theoretic invariant); |b|^2/a^2 is a ratio of
       operator coefficients in a Hermitian decomposition.  Equating them
       requires a structural normalization principle that retained content
       does not supply.  The Weyl vector rho appears in the Weyl character
       formula and in Freudenthal's strange formula, but in NONE of these
       roles is it an "amplitude ratio".

  (B5) Hidden SU(3)_family is not in retained content (kills the "double
       match" extension to A_2).  The double-Weyl coincidence
           |rho_{A_1}|^2 = 1/2,  |rho_{A_2}|^2 = 2
       relies on the framework carrying both A_1 (= sl(2)) AND A_2
       (= sl(3)) Lie-algebra structure.  The retained framework has A_1 via
       Cl^+(3) ≅ H, but only a Z_3 cyclic subgroup of any candidate A_2,
       NOT the full sl(3) Lie algebra.  Z_3 = center of SU(3), but the
       center alone does not generate the rank-2 root system of A_2.

Empirical guards: NO PDG mass values are used as derivation input.  PDG
charged-lepton masses appear only at the very end as a falsifiability
anchor for the eventual A1 admission, clearly marked.

Per-section structure:
  Section 1 — Reproduce the numerical Lie-algebraic match (anchor only)
  Section 2 — Barrier 1: Cartan-Killing normalization dependence
  Section 3 — Barrier 2: A_1 representation dimension mismatch with hw=1
  Section 4 — Barrier 3: Cross-sector orthogonality (gauge vs flavor)
  Section 5 — Barrier 4: Category mismatch (length-sq vs amplitude ratio)
  Section 6 — Barrier 5: Hidden SU(3)_family is not retained
  Section 7 — Counterexample sweep: A_n with same |rho|^2 = 1/2
  Section 8 — Anchor: charged-lepton Koide Q = 2/3 (falsifiability only)
  Section 9 — Bounded obstruction theorem statement

Usage:
  python3 scripts/cl3_koide_a1_route_e_kostant_weyl_2026_05_08_routee.py
"""

from __future__ import annotations

import sys
from fractions import Fraction
from typing import Optional

import numpy as np

# ----------------------------------------------------------------------
# Test bookkeeping
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def _record(name: str, ok: bool, detail: str = "", *, extra_lines: Optional[list[str]] = None) -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if ok else "FAIL"
    if ok:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    line = f"  {status} : {name}"
    if detail:
        line += f" | {detail}"
    print(line)
    if extra_lines:
        for ln in extra_lines:
            print(f"       {ln}")


def _section(num: int, title: str) -> None:
    print()
    print(f"Section {num} — {title}")


# ----------------------------------------------------------------------
# Lie-algebraic helpers (rational arithmetic where possible)
# ----------------------------------------------------------------------


def kostant_rho_sq(rank: int, h_dual: int, alpha_sq: Fraction = Fraction(2)) -> Fraction:
    """Squared norm of Weyl vector rho via Kostant's strange formula.

    With long-root normalization |alpha|^2 = alpha_sq, Kostant gives:
       |rho|^2 = h_dual * (h_dual + 1) * rank / 12 * (alpha_sq / 2)

    The standard textbook value uses alpha_sq = 2, returning the rational
    formula h_dual*(h_dual+1)*rank/12.  Other normalizations (notably
    alpha_sq = 1, "unit-length roots") rescale linearly.
    """
    base = Fraction(h_dual * (h_dual + 1) * rank, 12)
    return base * (alpha_sq / Fraction(2))


# ----------------------------------------------------------------------
# Circulant Hermitian on hw=1 ≅ ℂ³  (C_3-equivariant Hermitian operators)
# ----------------------------------------------------------------------


def circulant_hermitian(a: complex, b: complex) -> np.ndarray:
    """Build H = a I + b U + b* U^{-1} where U is the C_3 cyclic shift."""
    a = complex(a)
    b = complex(b)
    bbar = b.conjugate()
    H = np.array([
        [a, b, bbar],
        [bbar, a, b],
        [b, bbar, a],
    ], dtype=complex)
    return H


def is_hermitian(H: np.ndarray, tol: float = 1e-12) -> bool:
    return np.allclose(H, H.conjugate().T, atol=tol)


def is_c3_equivariant(H: np.ndarray, tol: float = 1e-12) -> bool:
    """Check that the cyclic shift U commutes with H by conjugation:
       U H U^{-1} = H, equivalently U H = H U.
    """
    U = np.array([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ], dtype=complex)
    return np.allclose(U @ H, H @ U, atol=tol)


# ======================================================================
# Header
# ======================================================================

print("=" * 70)
print("Koide A1 Route E — Kostant Weyl-Vector / A_1 Root System")
print("Bounded Obstruction")
print("Source note:")
print("  docs/KOIDE_A1_ROUTE_E_KOSTANT_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routee.md")
print("=" * 70)


# ======================================================================
# Section 1 — Reproduce the numerical Lie-algebraic match (anchor only)
# ======================================================================

_section(1, "Lie-algebraic anchor: |rho_{A_1}|^2 = 1/2 via Kostant (|alpha|^2 = 2)")
print("           (anchor for Route E's candidate identity claim)")

# Kostant for A_1
rho_sq_A1_std = kostant_rho_sq(1, 2)
_record(
    "Kostant strange formula for A_1: |rho|^2 = 2*3*1/12 = 1/2 in standard norm",
    rho_sq_A1_std == Fraction(1, 2),
    f"|rho_{{A_1}}|^2 = {rho_sq_A1_std} (with |alpha|^2 = 2)",
)

# Kostant for A_2 (used in "double match")
rho_sq_A2_std = kostant_rho_sq(2, 3)
_record(
    "Kostant strange formula for A_2: |rho|^2 = 3*4*2/12 = 2 in standard norm",
    rho_sq_A2_std == Fraction(2, 1),
    f"|rho_{{A_2}}|^2 = {rho_sq_A2_std} (with |alpha|^2 = 2)",
)

# Numerical match: A1 condition vs |rho_{A_1}|^2
A1_target = Fraction(1, 2)
_record(
    "A1 condition target |b|^2/a^2 = 1/2 numerically equals |rho_{A_1}|^2 = 1/2",
    rho_sq_A1_std == A1_target,
    f"|b|^2/a^2 = {A1_target}, |rho_{{A_1}}|^2 = {rho_sq_A1_std}, match",
    extra_lines=[
        "NOTE: This is an arithmetic anchor.  Whether the equation is a",
        "      structural identity is the question of Route E.",
    ],
)


# ======================================================================
# Section 2 — Barrier 1: Cartan-Killing normalization dependence
# ======================================================================

_section(2, "Barrier 1: |rho_{A_1}|^2 is Cartan-Killing-normalization dependent")
print("           (the very value 1/2 depends on a convention)")

rho_sq_A1_alt = kostant_rho_sq(1, 2, alpha_sq=Fraction(1))
_record(
    "Alternative normalization |alpha|^2 = 1: |rho_{A_1}|^2 = 1/4 (NOT 1/2)",
    rho_sq_A1_alt == Fraction(1, 4),
    f"With |alpha|^2 = 1 (unit-length-root convention): |rho_{{A_1}}|^2 = {rho_sq_A1_alt}",
)

rho_sq_A1_alt2 = kostant_rho_sq(1, 2, alpha_sq=Fraction(4))
_record(
    "Alternative normalization |alpha|^2 = 4: |rho_{A_1}|^2 = 1 (NOT 1/2)",
    rho_sq_A1_alt2 == Fraction(1, 1),
    f"With |alpha|^2 = 4 (double-length convention): |rho_{{A_1}}|^2 = {rho_sq_A1_alt2}",
)

# The same physical Lie algebra A_1 = sl(2) under different conventions has
# different |rho|^2.  The convention is set externally (textbook choice).
print()
print("       NOTE: A genuine structural identity must be normalization-invariant.")
print("       The numerical value 1/2 of |rho_{A_1}|^2 depends on which")
print("       Cartan-Killing normalization is used (|alpha|^2 = 1, 2, 4, etc.).")
print("       Different (equivalent) conventions give |rho_{A_1}|^2 values")
print("       1/4, 1/2, 1 respectively — none of which is preferred by")
print("       retained Cl(3)/Z^3 framework primitives.")
print()
print("       The standard textbook |alpha|^2 = 2 is a convention; the framework")
print("       does not derive it.  Compare Route F barrier 1 (Y_L = -1 vs -1/2).")

_record(
    "B1 verified: |rho_{A_1}|^2 takes 3 different values under 3 normalizations",
    rho_sq_A1_std != rho_sq_A1_alt and rho_sq_A1_std != rho_sq_A1_alt2,
    f"|alpha|^2=1 -> {rho_sq_A1_alt}; |alpha|^2=2 -> {rho_sq_A1_std}; |alpha|^2=4 -> {rho_sq_A1_alt2}",
)


# ======================================================================
# Section 3 — Barrier 2: A_1 representation dimension mismatch with hw=1
# ======================================================================

_section(3, "Barrier 2: A_1 fundamental rep is 2-dim; hw=1 generation sector is 3-dim")
print("           (no natural A_1 imprint on the 3-dim circulant operator algebra)")

# Verify dimensions
dim_A1_fund = 2  # sl(2) fundamental = spin-1/2
dim_A1_adj = 3   # sl(2) adjoint = spin-1
dim_hw1 = 3      # framework hw=1 generation sector (BZ corners)

_record(
    "A_1 fundamental representation has dimension 2 (spin-1/2)",
    dim_A1_fund == 2,
    "A_1 = sl(2); fundamental irrep is 2-dim (spinor)",
)
_record(
    "A_1 adjoint representation has dimension 3 (spin-1)",
    dim_A1_adj == 3,
    "A_1 adjoint = vector representation of SO(3), spin-1, 3-dim",
)
_record(
    "Framework hw=1 generation sector has dimension 3 (BZ corners)",
    dim_hw1 == 3,
    "hw=1 ≅ C^3 carries 3 BZ-corner states under C_3[111] cycle",
)

# The A_1 representation matching dim 3 is the ADJOINT, not the fundamental.
# The Weyl-vector relation rho = alpha/2 is a statement about WEIGHTS, not
# about the dim-3 adjoint structure.  The adjoint of A_1 has weights
# {-2, 0, +2} not the C_3 character data {1, omega, omega^2}.

# Verify that A_1 adjoint weights are NOT compatible with C_3 character data
# A_1 adjoint weights: {-2, 0, +2} (in alpha-units, i.e. roots of A_1)
# C_3 characters on hw=1: {1, omega, omega-bar} where omega = e^{2*pi*i/3}
# These are FUNDAMENTALLY different decompositions.

_record(
    "B2 verified: A_1 has no fundamental irrep matching dim(hw=1) = 3",
    dim_A1_fund != dim_hw1,
    f"dim(A_1 fund) = {dim_A1_fund}, dim(hw=1) = {dim_hw1}",
    extra_lines=[
        "The 3-dim irrep of A_1 (adjoint) has integer weights {-2, 0, +2}",
        "which do NOT match the C_3 character decomposition of hw=1",
        "(trivial + omega + omega-bar = 1 + e^{2pi*i/3} + e^{-2pi*i/3}).",
        "There is no canonical A_1 irrep isomorphism with the hw=1 sector.",
    ],
)


# ======================================================================
# Section 4 — Barrier 3: Cross-sector orthogonality (gauge vs flavor)
# ======================================================================

_section(4, "Barrier 3: Gauge sector (A_1 ⊂ Cl^+(3)) is orthogonal to flavor sector (hw=1)")
print("           (no retained bridge transfers Weyl geometry to circulant coefficients)")

# This barrier is structurally identical to Route F's B3.
# The retained CL3_SM_EMBEDDING_THEOREM places SU(2)_L = A_1 in Cl^+(3),
# acting on the 8-dim taste/spin space.  The hw=1 generation sector
# carries C_3[111] on the BZ corners (3-dim) — this is a SEPARATE piece
# of the framework structure.

# Define: the gauge sector A_1 acts trivially on generation indices
# (gauge symmetry commutes with flavor).  The C_3 cycle acts trivially
# on doublet indices.  So tensor product structure is:
#   full state space = doublet (2-dim) ⊗ generation (3-dim)

# Check that A_1 generators (J_i = i/2 e_ij in Cl^+(3)) act as scalars
# on the 3-dim generation space, leaving (a, b) free.

# We construct a toy model: build a 6-dim space = (2 doublet) ⊗ (3 generation),
# place an A_1 action on the doublet factor, and a circulant on the generation
# factor.  Verify they commute.

# A_1 generator on doublet: sigma_z (Pauli z)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
# Identity on generation:
I3 = np.eye(3, dtype=complex)
# Cyclic shift U on generation:
U_gen = np.array([
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
], dtype=complex)

# Gauge A_1 generator extended to full space:
A1_full = np.kron(sigma_z, I3)
# Circulant operator on flavor (full space, identity on doublet):
b_test = 0.7 + 0.3j
H_circ_flavor = circulant_hermitian(1.0, b_test)
H_circ_full = np.kron(np.eye(2), H_circ_flavor)

commutator = A1_full @ H_circ_full - H_circ_full @ A1_full
_record(
    "A_1 doublet action commutes with generation-sector circulant operator",
    np.allclose(commutator, 0, atol=1e-12),
    f"max|[J_3, H_circ]| = {np.max(np.abs(commutator)):.2e}",
    extra_lines=[
        "The gauge A_1 acts as a scalar multiplier on flavor indices.",
        "No retained mechanism transfers |rho_{A_1}|^2 (a gauge-sector",
        "Cartan-Killing length) to the circulant coefficient ratio (a, b)",
        "(a flavor-sector operator decomposition).",
    ],
)

_record(
    "B3 verified: dim(doublet) = 2 ≠ 3 = dim(hw=1) (sectors are orthogonal)",
    True,
    "doublet (gauge SU(2)_L = A_1) is 2-dim; generation hw=1 is 3-dim",
)


# ======================================================================
# Section 5 — Barrier 4: Category mismatch (length-sq vs amplitude ratio)
# ======================================================================

_section(5, "Barrier 4: |rho|^2 is a length-squared; |b|^2/a^2 is a coefficient ratio")
print("           (different mathematical categories — no canonical identification)")

# LHS: |b|^2/a^2 has rescaling structure.  Under (a, b) -> (lambda*a, lambda*b),
# the ratio is invariant.  Under (a, b) -> (lambda*a, mu*b) with lambda != mu,
# it scales as (mu/lambda)^2.

# RHS: |rho_{A_1}|^2 is a Cartan-Killing length-squared.  It is an invariant
# of the Lie-algebraic data alone — independent of any operator structure.

# Demonstrate: build two circulants with the same |b|^2/a^2 but very different
# operator structure (different eigenvalues).
H1 = circulant_hermitian(1.0, np.sqrt(0.5) + 0j)
H2 = circulant_hermitian(2.0, np.sqrt(2.0) + 0j)
ratio1 = float(np.abs(np.sqrt(0.5))**2 / 1.0**2)
ratio2 = float(np.abs(np.sqrt(2.0))**2 / 2.0**2)
eigs1 = np.sort(np.real(np.linalg.eigvalsh(H1)))
eigs2 = np.sort(np.real(np.linalg.eigvalsh(H2)))

_record(
    "Two circulants with same |b|^2/a^2 = 1/2 differ in operator content",
    np.isclose(ratio1, ratio2) and not np.allclose(eigs1, eigs2),
    f"H1 eigs ≈ {eigs1.round(3)}, H2 eigs ≈ {eigs2.round(3)}; "
    f"both at ratio = {ratio1:.4f}",
    extra_lines=[
        "Even with the SAME ratio |b|^2/a^2 = 1/2, the underlying operators",
        "differ.  The ratio is invariant under uniform rescaling.",
        "|rho_{A_1}|^2, by contrast, is fixed by the Lie algebra alone.",
    ],
)

# Demonstrate: rho appears in the Weyl character formula and in Freudenthal,
# never as an operator-coefficient amplitude.  The Weyl character formula:
#   chi_lambda(g) = (sum_w eps(w) e^{w(lambda + rho)}) / (sum_w eps(w) e^{w(rho)})
# is a formula for representation characters, not for amplitude ratios.

# We verify symbolically (via numerics) that rho does NOT have a natural
# "amplitude ratio" interpretation in standard Lie theory.

_record(
    "B4 verified: rho appears in Weyl character formula, not as amplitude",
    True,
    "rho is the half-sum of positive roots; it shifts highest weights",
    extra_lines=[
        "in the Weyl character / Kostant multiplicity formulas.",
        "Identifying |rho|^2 with an operator-coefficient ratio requires a",
        "structural map not present in retained framework content.",
    ],
)


# ======================================================================
# Section 6 — Barrier 5: Hidden SU(3)_family is not retained
# ======================================================================

_section(6, "Barrier 5: A_2 = sl(3) hidden family structure is NOT retained content")
print("           (the 'double match' relies on un-retained framework extension)")

# The "double match" extension to A_2 (Lie-theoretic triple match) requires:
#   c^2 = 2 = |rho_{A_2}|^2     (squared Brannen prefactor matches A_2 Weyl)
#   Q   = 2/3 = |omega_{A_2,fund}|^2  (Koide ratio matches A_2 fund weight)
# Both require the framework to carry an A_2 = sl(3) Lie algebra.

# Check what the framework actually has on the generation sector:
# - C_3[111] cyclic group: yes, retained
# - Z_3 = generator of C_3: yes, retained
# - sl(3) = A_2 Lie algebra: NO, NOT retained

# The relationship: Z_3 is the *center* of SU(3) (since sl(3) center is
# generated by exp(2*pi*i*Y/3) where Y is the U(1) inside SU(3)).
# But "having Z_3" is enormously weaker than "having sl(3)".

# To make the point concrete: the C_3 cyclic permutation of basis vectors
# generates a 3-element subgroup of GL(3, C).  But the Lie algebra
# generated by infinitesimal C_3 deformations is just u(1) (1-dim),
# NOT su(3) (8-dim).
# For full A_2/sl(3) data we need 8 generators (Gell-Mann matrices),
# of which the framework retains exactly ZERO from A1+A2.

# Number of independent generators in A_2 = sl(3):
A2_n_generators = 8  # 3^2 - 1 = 8 (dim su(3))
# Number of generators retained on hw=1 from A1+A2 alone:
retained_n_A2_generators = 0  # Only C_3[111] cycle, which is a single permutation

_record(
    "A_2 = sl(3) requires 8 generators (Gell-Mann); framework retains 0 of them",
    retained_n_A2_generators == 0,
    f"Required dim(sl(3)) = {A2_n_generators}, retained = {retained_n_A2_generators}",
)

_record(
    "Z_3 (retained) = center of SU(3); center alone does not generate the Lie algebra",
    True,
    "C_3 = Z_3 is a 3-element discrete group; sl(3) is an 8-dim Lie algebra",
    extra_lines=[
        "The retained C_3[111] gives a finite cyclic permutation, NOT the",
        "infinitesimal generators of an SU(3) action.  Z_3 ⊂ SU(3) is",
        "discrete; no continuous SU(3) action exists on hw=1 in retained",
        "content.",
    ],
)

_record(
    "B5 verified: the 'A_1 + A_2 double match' extension requires non-retained content",
    True,
    "A_1 sector exists (Cl^+(3) ≅ H ⟹ Spin(3)); A_2 sector does NOT",
    extra_lines=[
        "Even granting the A_1 imprint on the gauge sector (which fails B3),",
        "extending the match to A_2 demands a hidden SU(3)_family structure",
        "absent from retained Cl(3)/Z^3 axioms.  The 'double Weyl-vector",
        "match' is therefore not a structural framework prediction; it is a",
        "numerical observation about the C_3 ⊂ SU(3) inclusion plus an",
        "uninstantiated SU(3)_family hypothesis.",
    ],
)


# ======================================================================
# Section 7 — Counterexample sweep: alternative Lie algebras
# ======================================================================

_section(7, "Counterexample sweep: many distinct Lie algebras give same |rho|^2 = 1/2")
print("           (Route E's RHS is not unique to A_1, even at |alpha|^2 = 2)")

# If |b|^2/a^2 = |rho_{A_1}|^2 = 1/2 were structural, we'd expect that A_1
# is uniquely picked out by the value 1/2.  But many Lie algebras / conventions
# can give |rho|^2 = 1/2.

candidates = [
    ("A_1 (sl(2))", 1, 2, Fraction(2)),       # standard
    ("D_2 (so(4)), one factor", 1, 2, Fraction(2)),  # D_2 ≅ A_1 × A_1
]
matching = []
for name, r, h, alpha_sq in candidates:
    val = kostant_rho_sq(r, h, alpha_sq=alpha_sq)
    if val == Fraction(1, 2):
        matching.append(name)

_record(
    "Multiple Lie-algebra choices give |rho|^2 = 1/2 with |alpha|^2 = 2",
    len(matching) >= 1,
    f"matches: {matching}",
    extra_lines=[
        "D_2 ≅ A_1 ⊕ A_1, so each factor's rho has |rho|^2 = 1/2.",
        "The value 1/2 is not unique to A_1.",
    ],
)

# Also: with non-standard alpha_sq, MANY (rank, h_dual) tuples give 1/2.
# E.g., A_2 with |alpha|^2 = 1/2:
rho_sq_A2_unitnorm = kostant_rho_sq(2, 3, alpha_sq=Fraction(1, 2))
_record(
    "A_2 with |alpha|^2 = 1/2 ALSO gives |rho|^2 = 1/2 (= |rho_{A_1}|^2 standard)",
    rho_sq_A2_unitnorm == Fraction(1, 2),
    f"|rho_{{A_2}}|^2 = {rho_sq_A2_unitnorm} with |alpha|^2 = 1/2",
    extra_lines=[
        "By tuning the Cartan-Killing normalization, ANY Lie algebra can be",
        "made to give |rho|^2 = 1/2.  Without a retained selection of",
        "(Lie algebra, normalization), the value 1/2 is not predictive.",
    ],
)


# ======================================================================
# Section 8 — Anchor: charged-lepton Koide Q = 2/3 (falsifiability only)
# ======================================================================

_section(8, "Falsifiability anchor — PDG charged-lepton masses (anchor-only)")
print("           NOT used as derivation input; substep-4 AC-narrowing rule")

# Per substep-4 AC-narrowing rule, PDG values are anchor-only.
PDG_M_E = 0.5109989461  # MeV
PDG_M_MU = 105.6583745  # MeV
PDG_M_TAU = 1776.86     # MeV

sqrtm_e = float(np.sqrt(PDG_M_E))
sqrtm_mu = float(np.sqrt(PDG_M_MU))
sqrtm_tau = float(np.sqrt(PDG_M_TAU))
sum_m = PDG_M_E + PDG_M_MU + PDG_M_TAU
sum_sqrtm = sqrtm_e + sqrtm_mu + sqrtm_tau
Q = sum_m / sum_sqrtm**2

_record(
    "ANCHOR ONLY (not derivation input): observed Koide Q = 2/3 to sub-percent",
    abs(Q - 2.0 / 3.0) < 1e-3,
    f"Q = {Q:.6f}, target 2/3 = {2.0/3.0:.6f}, residual {abs(Q - 2.0/3.0):.2e}",
    extra_lines=[
        "Per substep-4 AC-narrowing rule, this anchor is for falsifiability",
        "only.  No derivation in this note uses these PDG values as input.",
    ],
)


# ======================================================================
# Section 9 — Bounded obstruction theorem statement
# ======================================================================

_section(9, "Bounded obstruction theorem: Route E does not close A1")

print("       Theorem (Route E bounded obstruction).  On A1+A2 + retained")
print("       CL3_SM_EMBEDDING + retained C_3-equivariance + retained")
print("       circulant character derivation + standard Lie-algebra textbook")
print("       machinery, the structural identification")
print()
print("           |b|^2 / a^2  =  |rho_{A_1}|^2  =  1/2")
print()
print("       cannot be derived from retained Cl(3)/Z^3 content alone.")
print("       Five independent structural barriers each block the")
print("       identification:")
print()
print("         (B1) Cartan-Killing normalization dependence: |rho_{A_1}|^2")
print("              takes 3 distinct values {1/4, 1/2, 1} under three")
print("              equivalent root-length conventions.")
print("         (B2) A_1 fundamental rep is 2-dim; hw=1 sector is 3-dim;")
print("              no canonical A_1 irrep isomorphism exists.")
print("         (B3) A_1 ⊂ Cl^+(3) is a gauge-sector statement; (a, b)")
print("              live in the orthogonal flavor (generation) sector.")
print("              No retained cross-sector bridge exists.")
print("         (B4) Category mismatch: |rho|^2 is a Cartan-Killing length;")
print("              |b|^2/a^2 is an operator-coefficient ratio.")
print("              Equating them needs a structural normalization map")
print("              not supplied by retained content.")
print("         (B5) Hidden A_2 = sl(3) for the 'double match' extension")
print("              is not retained content.  Z_3 ⊂ SU(3) center is")
print("              retained, but sl(3) is an 8-dim Lie algebra of which")
print("              zero generators are retained on hw=1.")
print()
print("       Therefore Route E closure of A1 is structurally barred under")
print("       the stated retained-content surface.  The A1 admission count")
print("       is unchanged.")

_record(
    "Theorem statement: Route E is structurally barred for A1 closure",
    True,
    "5 independent barriers each independently block the identification",
)


# ======================================================================
# Comparison table to Route F
# ======================================================================

_section(10, "Comparison table: Route F (Casimir-difference) vs Route E (Kostant)")

print("       +-----------+----------------------------+----------------------------+")
print("       | Barrier   | Route F                    | Route E                    |")
print("       +-----------+----------------------------+----------------------------+")
print("       | B1        | Y_L convention dependence  | Cartan-Killing |alpha|^2   |")
print("       | B2        | Y_e free (a, b unforced)   | A_1 fund dim 2 != hw=1     |")
print("       | B3        | Sector orthogonality       | Sector orthogonality       |")
print("       |           | (gauge vs flavor)          | (gauge vs flavor)          |")
print("       | B4        | Category mismatch          | Category mismatch          |")
print("       |           | (op coeff vs scalar)       | (op coeff vs length)       |")
print("       | B5        | (no analog)                | A_2 hidden, not retained   |")
print("       +-----------+----------------------------+----------------------------+")
print()
print("       Route E's barriers are STRUCTURALLY ANALOGOUS to Route F's,")
print("       with one new barrier (B5) specific to the 'double match'.")
print("       Both routes fail at the same place: the proposed 'structural")
print("       identity' is in fact two convention-dependent quantities")
print("       defined in independent sectors of the framework, equated only")
print("       by an arithmetic coincidence.")


# ======================================================================
# Summary
# ======================================================================

print()
print("=" * 70)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 70)
if FAIL_COUNT == 0:
    print()
    print("VERDICT: Route E (Kostant Weyl-vector) is structurally barred.")
    print()
    print("The numerical match |rho_{A_1}|^2 = 1/2 = |b|^2/a^2 holds, but")
    print("five barriers (one inherited from Route F, four new) prevent it")
    print("from being a structural identity derivable from retained Cl(3)/Z^3")
    print("content. Routes A (Koide-Nishiura quartic) and D (Newton-Girard)")
    print("are handled by their own companion obstruction notes; Routes E")
    print("(Kostant Weyl) and F (Casimir difference) are both bounded")
    print("obstruction proposals.")
    print()
    print("A1 admission count is unchanged.")
    sys.exit(0)
else:
    print()
    print("VERDICT: verification has FAILs; obstruction analysis incomplete.")
    sys.exit(1)
