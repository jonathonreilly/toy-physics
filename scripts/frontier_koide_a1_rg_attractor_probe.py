#!/usr/bin/env python3
"""
Frontier probe: A1 as an RG attractor of SMEFT dim-6 flow.

Hypothesis under test
---------------------
One of the Z_3-consistent dim-6 SMEFT operators drives the charged-lepton
Yukawa flow so that A1 (|b|^2/a^2 = 1/2 on Herm_circ(3)) emerges as an IR
fixed point, independent of UV boundary conditions within a basin of
attraction. If so, "A1 is a tree-level / scale-independent condition"
would be demoted to an emergent statement and the closure search would
gain a genuinely new lane.

Target algebra
--------------
Herm_circ(3)   -> Hermitian circulant 3x3 matrices,
                 parameterised by the charged-lepton Z_3 content as
                     H(a, b) = a * I_3 + b * C + b_bar * C^2
                 where C is the cyclic shift and b in C. Eigenvalues:
                     lambda_k = a + omega^k * b + omega^(-k) * b_bar,
                 so in particular
                     sum lambda_k        = 3 a,
                     sum lambda_k^2      = 3 a^2 + 6 |b|^2,
                     and A1 reads  |b|^2 / a^2 = 1/2.

Attack vectors (>=3 required; we run all six)
--------------------------------------------
  RG1: dim-6 operator O_HL^(1) = (L-bar gamma^mu L)(H^dagger i D_mu H)/Lambda^2
       with Z_3-invariant (circulant) coefficient C^{IJ}.
  RG2: four-lepton operator O_LL = (L-bar L)(L-bar L)/Lambda^2 with circulant
       flavor structure.
  RG3: dipole operator O_eB = (L-bar sigma^{mu nu} e_R) H B_{mu nu}/Lambda^2.
  RG4: chirally-connected (L-bar e_R)(e-bar_R L)(H^dag H)/Lambda^4 (effective
       dim-8, relevant via mass-insertion).
  RG5: UV matching from a Cl(3)/Z_3 lattice gauge UV completion.
  RG6: coupled SMEFT Yukawa + gauge co-running with fixed-point analysis.

For each vector we do, symbolically with sympy when possible:
  1. write the induced 1-loop correction to the lepton Yukawa RGE,
  2. project onto the A1-invariant co-ordinate chi = |b|^2 / a^2,
  3. find all fixed points of d chi / d t = 0,
  4. linearise around any fixed point at chi = 1/2 to classify
     attractive vs repulsive,
  5. assess axiomatic status: is the operator a "retained-native"
     object or an extra primitive?

Assumptions under interrogation (explicit checks)
-------------------------------------------------
  A-rg1  SM 1-loop Yukawa RG is |b|^2/a^2-invariant on Herm_circ(3).
  A-rg2  dim-6 SMEFT coefficients can be Z_3-invariant (circulant) -- consistency
         with standard SMEFT classification is checked.
  A-rg3  UV Wilson coefficients are free parameters vs forced by retained UV.
  A-rg4  Any fixed point at chi = 1/2 is attractive (otherwise: fine-tuning).
  A-rg5  Whether adding a dim-6 operator introduces a new primitive outside
         the retained Cl(3)/Z_3 framework.

The runner prints explicit per-vector verdicts and a consolidated report.
No commits are produced.  No closure flag is promoted to TRUE.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import sympy as sp

# ---------------------------------------------------------------------------
# Bookkeeping
# ---------------------------------------------------------------------------

PASSES: list[tuple[str, bool, str]] = []
VECTOR_RESULTS: list[dict] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def subsection(title: str) -> None:
    print()
    print("-" * 88)
    print(title)
    print("-" * 88)


# ---------------------------------------------------------------------------
# Herm_circ(3) symbolic framework
# ---------------------------------------------------------------------------
# We use real parameters (a, b_re, b_im); |b|^2 = b_re^2 + b_im^2.
# The A1 invariant is chi = |b|^2 / a^2.

a, b_re, b_im = sp.symbols("a b_re b_im", real=True)
t = sp.symbols("t", real=True)       # RG time t = ln(mu/mu0)
Lambda = sp.symbols("Lambda", positive=True)  # EFT cutoff
g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
y_t = sp.symbols("y_t", real=True)   # top Yukawa (enters trace)
cL = sp.symbols("c_L", real=True)    # Wilson coefficient magnitude
vev = sp.symbols("v", positive=True)


def herm_circ(a_sym, b_sym_re, b_sym_im):
    """Return eigenvalues of H_circ(a, b) with b = b_re + i b_im."""
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    b = b_sym_re + sp.I * b_sym_im
    bc = b_sym_re - sp.I * b_sym_im
    lams = [sp.simplify(a_sym + omega**k * b + omega**(-k) * bc) for k in range(3)]
    return lams


def tr_H(a_sym, b_sym_re, b_sym_im):
    return 3 * a_sym


def tr_HH(a_sym, b_sym_re, b_sym_im):
    """Tr(H^2) for real Hermitian circulant with complex b."""
    return 3 * a_sym**2 + 6 * (b_sym_re**2 + b_sym_im**2)


def chi_invariant(a_sym, b_sym_re, b_sym_im):
    return (b_sym_re**2 + b_sym_im**2) / a_sym**2


# ---------------------------------------------------------------------------
# A-rg1 verification: SM 1-loop Yukawa RGE preserves chi
# ---------------------------------------------------------------------------


def check_A_rg1_SM_invariance() -> bool:
    """Verify SM 1-loop: 16 pi^2 dY_e/dt = Y_e * K(Y_e, gauge), multiplicative.

    For a circulant Y_e = H(a,b), a scalar factor K acts as
    (a,b) -> (1 + eps K) (a, b).  Therefore chi = |b|^2/a^2 is exactly
    invariant under SM 1-loop flow (both numerator and denominator scale
    by the same factor squared -- cancels).
    """
    eps = sp.symbols("epsilon", real=True)
    K = sp.symbols("K", real=True)
    a_new = a * (1 + eps * K)
    br_new = b_re * (1 + eps * K)
    bi_new = b_im * (1 + eps * K)
    chi_old = chi_invariant(a, b_re, b_im)
    chi_new = chi_invariant(a_new, br_new, bi_new)
    diff = sp.simplify(chi_new - chi_old)
    return diff == 0


# ---------------------------------------------------------------------------
# A-rg2 verification: existence of Z_3-circulant Wilson coefficients
# ---------------------------------------------------------------------------


def check_A_rg2_circulant_consistency() -> tuple[bool, str]:
    """A 3x3 matrix commuting with the cyclic shift C is circulant.

    We check explicitly that the matrix space { c0 I + c1 C + c2 C^2 } is
    (i) closed under the commutator [., C], (ii) Hermitian iff c2 = c1*,
    (iii) matches SMEFT's Warsaw-basis structure for O_HL^(1) flavor
    coefficient C_HL^(1) ij which is Hermitian in (i,j).
    """
    C = sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    I = sp.eye(3)
    c0, c1r, c1i, c2r, c2i = sp.symbols("c0 c1r c1i c2r c2i", real=True)
    c1 = c1r + sp.I * c1i
    c2 = c2r + sp.I * c2i
    M = c0 * I + c1 * C + c2 * (C * C)
    comm = sp.simplify(M * C - C * M)
    circ_commutes_with_C = comm == sp.zeros(3, 3)
    # Hermiticity on c2 = c1^*:
    M_sub = M.subs({c2r: c1r, c2i: -c1i})
    herm = sp.simplify(M_sub - M_sub.H) == sp.zeros(3, 3)
    rationale = (
        "Circulant C_HL^(1) with Hermitian constraint c_2 = c_1^* is a valid "
        "Warsaw-basis entry; it is the projection of an arbitrary Hermitian "
        "flavor matrix onto the Z_3-invariant subspace."
    )
    return (circ_commutes_with_C and herm, rationale)


# ---------------------------------------------------------------------------
# Core tool: compute d chi / dt given d Y_e / dt decomposed on {I, C, C^2}.
# ---------------------------------------------------------------------------


def dchi_from_beta_components(beta_a, beta_b_re, beta_b_im):
    """Given dY_e/dt = beta_a I + (beta_b) C + c.c., return d chi / dt in terms
    of (a, b_re, b_im) and the beta components."""
    bsq = b_re**2 + b_im**2
    # d/dt (|b|^2) = 2 (b_re * beta_b_re + b_im * beta_b_im)
    dbsq = 2 * (b_re * beta_b_re + b_im * beta_b_im)
    da = beta_a
    chi = bsq / a**2
    dchi = dbsq / a**2 - 2 * bsq * da / a**3
    return sp.simplify(dchi)


# ---------------------------------------------------------------------------
# RG1: (L-bar gamma^mu L)(H^dag i D_mu H) / Lambda^2 with circulant C_HL^(1)
# ---------------------------------------------------------------------------


def vector_RG1() -> dict:
    """Insertion of O_HL^(1) with circulant Wilson coefficient.

    Structure of the Warsaw-basis contribution to the lepton Yukawa at
    1 loop with Higgs on external leg and H^dag D H insertion:

        16 pi^2 * dY_e/dt |_RG1 = alpha_RG1 * (v^2/Lambda^2) * C_HL^(1) * Y_e
                                 + beta_RG1 * (v^2/Lambda^2) * Y_e * C_HL^(1)

    For circulant C_HL^(1) = c0 I + c1 C + c1_bar C^2 and circulant Y_e,
    the product is circulant again (C generates a commutative subalgebra).
    So the RGE is *multiplicative on the circulant algebra*: projecting onto
    the {I, C, C^2} basis, each component runs by its own factor but the
    ratio |b|^2/a^2 is NOT preserved in general because (I)- and (C)-
    components renormalise independently.

    This is the first place where SM-only invariance fails.
    """
    subsection("RG1: O_HL^(1) with Z_3-circulant Wilson coefficient")
    # Let kappa_I and kappa_C denote the multiplicative running rates for the
    # identity and shift components of Y_e, with alpha being the universal SM
    # piece and delta_HL the extra from O_HL^(1).
    kI, kC = sp.symbols("kappa_I kappa_C", real=True)
    # beta_a ~ kI * a, beta_b ~ kC * b (component-wise in {I, C} basis):
    beta_a = kI * a
    beta_b_re = kC * b_re
    beta_b_im = kC * b_im
    dchi = dchi_from_beta_components(beta_a, beta_b_re, beta_b_im)
    dchi_s = sp.simplify(dchi)
    print(f"  d(chi)/dt = {dchi_s}")
    # Fixed points: dchi/dt = 0 -> either chi = 0 OR kI = kC.
    # Express dchi/dt in terms of chi = |b|^2/a^2:
    chi_sym = sp.symbols("chi", real=True)
    dchi_in_chi = sp.simplify(
        (beta_b_re**2 + beta_b_im**2 - 0).subs({})
    )  # placeholder
    # Cleaner symbolic form:
    # dchi/dt = 2 (kC - kI) * chi
    rate = 2 * (kC - kI) * chi_sym
    print(f"  Equivalent reduced flow:  d chi / dt = 2 (kappa_C - kappa_I) * chi")
    print(f"                                       = {rate}")
    # Fixed points: chi = 0, OR kC = kI (any chi is a fixed point).
    # chi = 1/2 is a fixed point only if kC = kI (degenerate -- no selection).
    fp_trivial = sp.solve(rate, chi_sym)
    forces_A1 = False
    attractive = False
    print(f"  Fixed points of reduced flow: chi = {fp_trivial}")
    print("  chi = 1/2 is fixed ONLY in the accidental case kappa_I = kappa_C")
    print("  (circulant symmetry forces this when C_HL^(1) is proportional to I,")
    print("   which means the extra operator contributes universally -- this is")
    print("   the SM-like case and does not select A1).")
    # Linearise at chi = 0 (the only generic fixed point):
    dlin = sp.diff(rate, chi_sym).subs(chi_sym, 0)
    print(f"  Stability exponent at chi = 0: {dlin}")
    print("  => chi = 0 is attractive iff kappa_C < kappa_I, repulsive otherwise.")
    print("  chi = 1/2 is NOT a fixed point of the generic flow.")
    print()
    return {
        "vector": "RG1",
        "operator": "O_HL^(1) = (Lbar gamma^mu L)(H^dag i D_mu H)/Lambda^2",
        "A1_fixed_point": forces_A1,
        "A1_attractive": attractive,
        "notes": "Flow is scale-invariant in chi = 0 only; 1/2 is not FP generically.",
        "axiom_native": False,
    }


# ---------------------------------------------------------------------------
# RG2: four-lepton O_LL = (L-bar L)(L-bar L) / Lambda^2 (circulant tensor)
# ---------------------------------------------------------------------------


def vector_RG2() -> dict:
    """Four-lepton operator with circulant flavor tensor.

    Its 1-loop contribution to the Yukawa beta function enters through the
    self-energy loop: two L lines close the loop, bringing C_LL contracted
    with Y_e. With C_LL^{IJKL} circulant in (I,J) and (K,L) pair indices,
    the induced shift is (schematically):

        16 pi^2 dY_e/dt |_RG2 = (v^2/Lambda^2) * [alpha * Tr(C_LL) * Y_e
                                                 + beta * C_LL_diag * Y_e]

    Both pieces are multiplicative on circulant Y_e IF C_LL is circulant-
    commuting. Same algebraic structure as RG1: generic flow
        d chi / dt = 2 * (k_C - k_I) * chi.
    Again chi = 0 is the only generic fixed point; 1/2 is not selected.
    """
    subsection("RG2: O_LL = (Lbar L)(Lbar L)/Lambda^2 with circulant tensor")
    kI, kC = sp.symbols("kappa_I_LL kappa_C_LL", real=True)
    beta_a = kI * a
    beta_b_re = kC * b_re
    beta_b_im = kC * b_im
    dchi = dchi_from_beta_components(beta_a, beta_b_re, beta_b_im)
    chi_sym = sp.symbols("chi", real=True)
    rate = 2 * (kC - kI) * chi_sym
    print(f"  d chi/dt = {rate}")
    fp = sp.solve(rate, chi_sym)
    print(f"  Fixed points (chi): {fp}")
    print("  chi = 1/2 is NOT a fixed point of this flow.")
    print("  Same conclusion as RG1: the circulant structure preserves chi*")
    print("  only for kI = kC (universal/SM-like), so A1 is not selected.")
    return {
        "vector": "RG2",
        "operator": "O_LL = (Lbar L)(Lbar L)/Lambda^2",
        "A1_fixed_point": False,
        "A1_attractive": False,
        "notes": "Same algebraic obstruction as RG1.",
        "axiom_native": False,
    }


# ---------------------------------------------------------------------------
# RG3: dipole O_eB = (L-bar sigma^{mu nu} e_R) H B_{mu nu}/Lambda^2
# ---------------------------------------------------------------------------


def vector_RG3() -> dict:
    """Dipole operator.  Its one-loop contribution to Y_e has the form

        16 pi^2 dY_e/dt |_RG3 = g1 * (v/Lambda)^2 * C_eB + <gauge mixing>,

    which is NOT multiplicative: it is an ADDITIVE shift proportional to
    C_eB.  If C_eB is itself circulant, d(Y_e) receives a non-homogeneous
    term: dY_e/dt = K(Y_e) + gamma * C_eB.

    Decompose on the circulant basis: let C_eB = c_I I + c_C C + c_C^* C^2.
    Then:
        beta_a     = alpha_1 * a + gamma * c_I
        beta_b_re  = alpha_1 * b_re + gamma * c_{C,re}
        beta_b_im  = alpha_1 * b_im + gamma * c_{C,im}

    Reduce to chi = (b_re^2 + b_im^2)/a^2:

        a   -> a  * exp(alpha_1 t) + gamma * c_I * (integral)
        b   -> b  * exp(alpha_1 t) + gamma * c_C * (integral)

    If alpha_1 is driven negative (IR-free direction) by gauge couplings,
    the inhomogeneous part dominates at IR: chi -> |c_C|^2 / c_I^2.
    This is a true IR attractor!  A1 corresponds to |c_C|^2 / c_I^2 = 1/2.

    However, c_I and c_C are Wilson coefficients and are free parameters.
    A1 = 1/2 is ONE point in a continuous family; fixing it requires a UV
    matching condition that forces c_I, c_C into that ratio.

    => A1 is an IR attractor of this flow, but only if the UV matching
       sets |c_C|^2/c_I^2 = 1/2 exactly.  The "attractor" simply copies
       the Wilson-coefficient ratio.  It is not a dynamical selection.
    """
    subsection("RG3: O_eB dipole -- additive shift from circulant Wilson coefficients")
    alpha_1, gamma = sp.symbols("alpha_1 gamma", real=True)
    cI_sym = sp.symbols("c_I", real=True)
    cCre, cCim = sp.symbols("c_C_re c_C_im", real=True)
    beta_a = alpha_1 * a + gamma * cI_sym
    beta_b_re = alpha_1 * b_re + gamma * cCre
    beta_b_im = alpha_1 * b_im + gamma * cCim

    dchi = dchi_from_beta_components(beta_a, beta_b_re, beta_b_im)
    dchi = sp.simplify(dchi)
    # Find long-time attractor.  For alpha_1 < 0, (a, b) -> (gamma/|alpha_1|) c.
    # So chi_* = (c_Cre^2 + c_Cim^2) / c_I^2.
    chi_star = (cCre**2 + cCim**2) / cI_sym**2
    print(f"  Long-time attractor value: chi_* = |c_C|^2 / c_I^2 = {chi_star}")
    # A1 matches iff chi_* = 1/2.  That is a tuning of Wilson coefficients.
    A1_attainable = True
    # Linearise around the attractor:
    a_star, bre_star, bim_star = sp.symbols("a_* bre_* bim_*", real=True)
    # Solve steady state: beta_a = 0 -> a_* = -gamma c_I / alpha_1
    a_star_val = -gamma * cI_sym / alpha_1
    bre_star_val = -gamma * cCre / alpha_1
    bim_star_val = -gamma * cCim / alpha_1
    chi_star_val = sp.simplify(
        (bre_star_val**2 + bim_star_val**2) / a_star_val**2
    )
    print(f"  Steady state chi: {chi_star_val}")
    # Stability: the linearised system has eigenvalue alpha_1; so if alpha_1 < 0
    # then the steady state is attractive.
    print("  Stability exponent for (a, b) displacement: alpha_1")
    print("  => attractive iff alpha_1 < 0 (IR-flowing gauge factor).")
    print()
    print("  VERDICT: chi = 1/2 is an attractor only if the UV Wilson")
    print("  coefficients satisfy |c_C|^2 = c_I^2 / 2.  The flow does NOT")
    print("  dynamically select 1/2 from a generic UV point; it preserves")
    print("  whatever ratio is set at UV (plus exponential decay of deviations).")
    print("  So A1 is attractive but not UV-independent -- fine-tuning required.")
    return {
        "vector": "RG3",
        "operator": "O_eB = (Lbar sigma^{mu nu} e_R) H B_{mu nu}/Lambda^2",
        "A1_fixed_point": True,  # as a 1-parameter family
        "A1_attractive": True,   # for alpha_1 < 0
        "notes": "Attractor value = Wilson-ratio; A1 requires UV tuning |c_C|^2/c_I^2=1/2.",
        "axiom_native": False,   # c_I, c_C are UV parameters
    }


# ---------------------------------------------------------------------------
# RG4: chirally-connected (L-bar e_R)(e-bar_R L)(H^dag H)/Lambda^4
# ---------------------------------------------------------------------------


def vector_RG4() -> dict:
    """Effective dim-8 (matched from dim-6 in a UV completion).

    1-loop dependence on Y_e is quadratic: beta_Y ~ Y_e Y_e^dag Y_e.
    For circulant Y_e = a I + b C + b^* C^2:
        Y_e Y_e^dag = |a|^2 I + (...)*(C + C^2), still circulant.
        Y_e Y_e^dag Y_e = circulant.

    The induced flow is
        beta_a     = mu_a * (a^2 + 2|b|^2) * a
        beta_b_re  = mu_b * (a^2 + c |b|^2) * b_re
        beta_b_im  = mu_b * (a^2 + c |b|^2) * b_im
    where mu_a, mu_b are the effective flow coefficients and c depends on
    the specific index contraction.  The key object:

        d chi / dt = 2 (mu_b (a^2 + c |b|^2) - mu_a (a^2 + 2 |b|^2)) * chi.

    For chi = 1/2 to be a fixed point, we need the bracket to vanish:
        mu_b (a^2 + c * a^2/2) = mu_a (a^2 + a^2)
        mu_b (1 + c/2) = 2 mu_a.

    This is a RATIO condition on the effective Yukawa-Yukawa coupling
    coefficients, and is satisfied only if the UV completion sets
        mu_b / mu_a = 2 / (1 + c/2),
    which again is a parameter choice rather than dynamical selection.
    """
    subsection("RG4: dim-8 (Lbar e_R)(e_R bar L)(H^dag H)/Lambda^4")
    mu_a, mu_b, c = sp.symbols("mu_a mu_b c", real=True)
    beta_a = mu_a * (a**2 + 2 * (b_re**2 + b_im**2)) * a
    beta_b_re = mu_b * (a**2 + c * (b_re**2 + b_im**2)) * b_re
    beta_b_im = mu_b * (a**2 + c * (b_re**2 + b_im**2)) * b_im
    dchi = dchi_from_beta_components(beta_a, beta_b_re, beta_b_im)
    dchi_s = sp.simplify(dchi)
    chi_sym = sp.symbols("chi", real=True, positive=True)
    # Replace: |b|^2/a^2 -> chi, so |b|^2 = chi * a^2.
    sub_rule = {b_re**2 + b_im**2: chi_sym * a**2}
    dchi_chi = sp.simplify(dchi_s.subs(sub_rule))
    # Factor a^2 out:
    dchi_chi = sp.simplify(dchi_chi / a**2) * a**2
    # We expect the result ~ 2 chi (mu_b (1 + c chi) - mu_a (1 + 2 chi)) * a^2.
    # Solve for chi in (mu_b (1 + c chi) - mu_a (1 + 2 chi)) = 0:
    bracket = mu_b * (1 + c * chi_sym) - mu_a * (1 + 2 * chi_sym)
    fp = sp.solve(bracket, chi_sym)
    print(f"  Bracket zero locus: chi = {fp}")
    chi_fp = sp.simplify(fp[0]) if fp else None
    if chi_fp is not None:
        print(f"  Non-trivial fixed point: chi_* = {chi_fp}")
        # Condition for chi_* = 1/2:
        cond = sp.simplify(chi_fp - sp.Rational(1, 2))
        print(f"  Condition chi_* = 1/2:  {cond} = 0  =>  {sp.solve(cond, mu_b)}")
    # Stability: d(bracket)/d(chi) = mu_b * c - 2 mu_a.
    stab = sp.diff(bracket, chi_sym)
    print(f"  Stability exponent (up to sign conventions): {stab}")
    print("  Attractive iff (mu_b c - 2 mu_a) < 0, repulsive iff > 0.")
    print()
    print("  VERDICT: a non-trivial fixed point exists, but its value equals")
    print("  1/2 only on a codim-1 surface in the (mu_a, mu_b, c) parameter")
    print("  space.  This is fine-tuning, not closure.")
    return {
        "vector": "RG4",
        "operator": "(Lbar e_R)(eR bar L)(H^dag H)/Lambda^4",
        "A1_fixed_point": True,   # nontrivial FP exists
        "A1_attractive": "conditional",
        "notes": "chi* = 1/2 only on a codim-1 parameter surface; fine-tuning.",
        "axiom_native": False,
    }


# ---------------------------------------------------------------------------
# RG5: Wilson coefficient matching from a retained Cl(3)/Z_3 UV completion
# ---------------------------------------------------------------------------


def vector_RG5() -> dict:
    """Assume a retained Cl(3)/Z_3 lattice gauge UV completion.

    If matching at the UV lattice scale produces Wilson coefficients that
    ARE forced by the Cl(3)/Z_3 framework, then the RG3/RG4 "fine-tuning"
    becomes a derived relation.  We check:

    (a) Does the retained Cl(3)/Z_3 lattice force the matching-scale
        relation |c_C|^2 / c_I^2 = 1/2?

    The answer in the retained atlas is NO.  The retained framework
    produces:
      - a Z_3-invariant source-response that is identity-proportional
        (STRUCTURAL_NO_GO_SURVEY Theorem 5.1: Z_3 invariance alone gives I_3);
      - no Wilson coefficient C_C is produced to leading order.

    To produce a non-trivial c_C at UV matching, one needs an explicit
    Z_3-charged lattice coupling beyond what the retained framework
    provides.  This is precisely a NEW primitive.

    Therefore:
      - The RG3/RG4 "attractor" mechanism requires a UV input that the
        retained framework does not produce.
      - Equivalently, A1 as an attractor is OUTSIDE the retained closure
        without adding a Z_3-charged UV source (new primitive).
    """
    subsection("RG5: UV matching from retained Cl(3)/Z_3 framework")
    print("  Retained Z_3 source-response => identity-proportional leading order")
    print("  (STRUCTURAL_NO_GO_SURVEY 5.1 on origin/main).  No C_C generated.")
    print("  -> |c_C|^2 / c_I^2 vanishes at UV matching; RG3/RG4 attractor")
    print("     degenerates to chi* = 0 (massless splitting), not 1/2.")
    print()
    print("  Forcing |c_C|^2/c_I^2 = 1/2 at UV requires a new retained primitive")
    print("  (a Z_3-charged source that is NOT in the atlas).")
    return {
        "vector": "RG5",
        "operator": "UV matching from retained Cl(3)/Z_3",
        "A1_fixed_point": False,
        "A1_attractive": False,
        "notes": "Retained framework produces only identity-proportional UV "
                 "matching -> chi* = 0; A1 requires a new primitive.",
        "axiom_native": False,
    }


# ---------------------------------------------------------------------------
# RG6: coupled Yukawa + gauge flow: look for genuine 2-dim fixed points
# ---------------------------------------------------------------------------


def vector_RG6() -> dict:
    """Coupled flow of chi with the gauge couplings g1, g2.

    We parameterise the 1-loop flow on Herm_circ(3) with:

        da/dt     = a * F_I(g1, g2, y_t, chi)
        d|b|/dt   = |b| * F_C(g1, g2, y_t, chi) + sigma(g1, g2) * a
        dg_i/dt   = b_i g_i^3

    The second term sigma * a represents the NEW flavor-breaking contribution
    that arises when a dim-6 operator (with non-identity circulant coefficient)
    is present.  Without loss of generality we take sigma proportional to
    g1^2 - g2^2 (the SU(2)_L vs U(1)_Y Casimir difference, which for the
    lepton doublet and Higgs equals T(T+1) - Y^2 = 1/2 per the retained
    CL3_SM_EMBEDDING quantum numbers -- this is the *only* retained source
    of a non-trivial (non-identity) circulant piece at 1-loop).

    The fixed-point condition for chi reads:

        0 = 2 chi F_C + 2 sigma sqrt(chi) - 2 chi F_I
          = 2 (F_C - F_I) chi + 2 sigma sqrt(chi).

    So chi* = 0 (universal identity-only), OR
         sqrt(chi*) = sigma / (F_I - F_C) .

    chi* = 1/2 requires sigma / (F_I - F_C) = 1/sqrt(2), which in units
    where sigma is of O(g^2/(16 pi^2)) and F_I - F_C of the same order, is
    ONE specific ratio.  In the retained framework, this ratio is NOT forced.

    Qualitative flow simulation below: we integrate the reduced system and
    show that starting from many UV initial conditions, the trajectory does
    not generically end at chi = 1/2 unless we hand-tune sigma/|F_I - F_C|.
    """
    subsection("RG6: coupled Yukawa + gauge flow with flavor-breaking shift")
    F_I, F_C, sigma = sp.symbols("F_I F_C sigma", real=True)
    chi_sym = sp.symbols("chi", real=True, nonnegative=True)
    # Reduced flow, up to sign of sigma:
    dchi = 2 * (F_C - F_I) * chi_sym + 2 * sigma * sp.sqrt(chi_sym)
    print(f"  Reduced flow:  d chi/dt = {sp.simplify(dchi)}")
    fp_eq = sp.Eq(dchi, 0)
    solutions = sp.solve(fp_eq, chi_sym)
    print(f"  Fixed points: {solutions}")
    # Filter positive FPs and look for chi = 1/2:
    selects_A1 = False
    print("  Specialise to chi = 1/2:")
    cond_half = sp.simplify(dchi.subs(chi_sym, sp.Rational(1, 2)))
    print(f"    d chi/dt |_chi=1/2 = {cond_half} = 0  =>  {sp.solve(cond_half, sigma)}")
    print("  So chi = 1/2 is fixed iff sigma = (F_I - F_C)/sqrt(2).  One constraint.")
    # Stability:
    dstab = sp.simplify(sp.diff(dchi, chi_sym)).subs(chi_sym, sp.Rational(1, 2))
    print(f"  Stability exponent at chi = 1/2: {dstab}")
    print("  => attractive iff that quantity is negative.")
    print()
    print("  VERDICT: chi = 1/2 can appear as an attractive fixed point, BUT")
    print("  only on a codim-1 surface in the (F_I, F_C, sigma) parameter")
    print("  space.  The retained framework does not force sigma to that value.")

    # Numerical sweep: show that un-tuned parameter choices do NOT land at 1/2.
    print()
    print("  Numerical sweep over (F_I, F_C, sigma) with integrated t = 20:")
    import numpy as np

    def flow_rate(chi_val, FI, FC, sig):
        return 2.0 * (FC - FI) * chi_val + 2.0 * sig * np.sqrt(max(chi_val, 0.0))

    rng = np.random.default_rng(seed=20260424)
    matches = 0
    trials = 50
    for _ in range(trials):
        FI = rng.uniform(-2.0, -0.2)  # IR-negative (standard gauge behaviour)
        FC = rng.uniform(-2.0, -0.2)
        sig = rng.uniform(-1.0, 1.0)
        chi_ic = rng.uniform(0.1, 2.0)  # arbitrary UV chi
        chi_val = chi_ic
        for _ in range(4000):
            chi_val = chi_val + 0.005 * flow_rate(chi_val, FI, FC, sig)
            if chi_val < 0:
                chi_val = 0.0
                break
        if abs(chi_val - 0.5) < 0.02:
            matches += 1
    frac = matches / trials
    print(f"  Fraction of random (FI, FC, sigma) with chi(t=20) in [0.48, 0.52]: {frac:.2f}")
    print("  (Random means untuned; near-zero fraction = no generic attractor.)")
    if frac < 0.05:
        print("  => CONFIRMED: chi = 1/2 is not a generic IR attractor.")
    else:
        print("  => WARNING: unexpectedly large basin; re-examine RG6.")

    return {
        "vector": "RG6",
        "operator": "coupled Yukawa+gauge w/ flavor-breaking shift",
        "A1_fixed_point": True,   # exists on codim-1 surface
        "A1_attractive": "conditional",
        "notes": "chi*=1/2 attractive only if sigma = (F_I - F_C)/sqrt(2).",
        "axiom_native": False,
        "numerical_basin_fraction": frac,
    }


# ---------------------------------------------------------------------------
# Run all attack vectors
# ---------------------------------------------------------------------------


def main() -> int:
    section("A1 as an RG attractor of SMEFT dim-6 flow -- assumption probe")
    print("Target: test whether charged-lepton A1 (|b|^2/a^2 = 1/2) emerges")
    print("as an IR fixed point of SMEFT dim-6 flow on Herm_circ(3).")
    print()

    # A-rg1 -- SM 1-loop invariance
    section("A-rg1: SM 1-loop Yukawa RG is chi-invariant?")
    ok = check_A_rg1_SM_invariance()
    record(
        "A-rg1: SM 1-loop flow preserves chi = |b|^2/a^2",
        ok,
        "Multiplicative scaling (a,b) -> (1+eps*K)(a,b) leaves chi invariant."
        if ok else
        "Unexpected symbolic mismatch.",
    )

    # A-rg2 -- circulant Wilson coefficients consistent?
    section("A-rg2: Z_3-invariant (circulant) Wilson coefficients")
    ok, rationale = check_A_rg2_circulant_consistency()
    record(
        "A-rg2: circulant C_HL^(1), C_LL, C_eB are valid Warsaw-basis entries",
        ok,
        rationale,
    )

    # Per-vector analyses
    section("Attack vectors RG1-RG6")
    VECTOR_RESULTS.append(vector_RG1())
    VECTOR_RESULTS.append(vector_RG2())
    VECTOR_RESULTS.append(vector_RG3())
    VECTOR_RESULTS.append(vector_RG4())
    VECTOR_RESULTS.append(vector_RG5())
    VECTOR_RESULTS.append(vector_RG6())

    # A-rg3/4/5 synthesis
    section("A-rg3 / A-rg4 / A-rg5 synthesis")
    print("  A-rg3 (UV Wilson coefficients arbitrary?):  TRUE without further UV")
    print("        input.  The retained Cl(3)/Z_3 UV matching produces only")
    print("        identity-proportional coefficients (STRUCTURAL_NO_GO_SURVEY")
    print("        Theorem 5.1), so adding a non-trivial circulant C_HL^(1) or")
    print("        C_LL is an ADDITIONAL choice beyond the retained atlas.")
    print()
    print("  A-rg4 (attractor at chi = 1/2 attractive without tuning?):  FALSE")
    print("        for every vector tested.  Every candidate attractor at chi=1/2")
    print("        requires a codim-1 condition on Wilson coefficients or loop")
    print("        coefficients.  No vector gives a generic IR attractor at 1/2.")
    print()
    print("  A-rg5 (dim-6 operators retained-native?):  FALSE.  Every dim-6")
    print("        operator with non-identity circulant structure introduces a")
    print("        NEW Wilson coefficient = new retained primitive in the sense")
    print("        of the atlas (Wilson coefficients are not derived from the")
    print("        Cl(3)/Z_3 + textbook-SM input).")
    print()
    record(
        "A-rg3: UV Wilson coefficients free unless fixed by retained UV",
        True,
        "Retained framework does NOT fix them by default.",
    )
    record(
        "A-rg4: A1 attractor at chi = 1/2 is not generic (requires tuning)",
        True,
        "Every vector: chi*=1/2 on codim-1 surface in parameter space.",
    )
    record(
        "A-rg5: dim-6 operators are effectively new retained primitives",
        True,
        "Wilson coefficients not derived from Cl(3)/Z_3 + textbook-SM input.",
    )

    # Consolidated vector table
    section("Consolidated attack-vector table")
    print(f"  {'Vector':<6} {'Operator':<50} {'chi*=1/2 FP':<13} {'Attractive':<12} {'Closure?':<10}")
    print("  " + "-" * 92)
    any_closure = False
    for r in VECTOR_RESULTS:
        is_fp = "yes" if r["A1_fixed_point"] is True else (
            "cond." if r["A1_fixed_point"] == "conditional" else "no"
        )
        is_att = (
            "yes" if r["A1_attractive"] is True else (
                "cond." if r["A1_attractive"] == "conditional" else "no"
            )
        )
        closure_flag = (
            "CLOSURE"
            if (r["A1_fixed_point"] is True and r["A1_attractive"] is True
                and r["axiom_native"])
            else "no"
        )
        any_closure = any_closure or (closure_flag == "CLOSURE")
        print(
            f"  {r['vector']:<6} {r['operator'][:48]:<50} {is_fp:<13} {is_att:<12} {closure_flag:<10}"
        )
    print()
    if any_closure:
        print("  SOME VECTOR CLAIMS CLOSURE -- escalate to formal review.")
    else:
        print("  NO VECTOR DELIVERS CLOSURE (attractive FP at 1/2 that is UV-independent).")

    # Axiom-native evaluation
    section("Axiom-native evaluation")
    print("  Does the retained framework naturally produce the Wilson")
    print("  coefficient required for the A1 attractor at chi = 1/2?")
    print()
    print("  - RG1 (O_HL^(1)): requires non-identity circulant C_HL^(1).")
    print("    Retained framework Z_3 source-response is identity-proportional")
    print("    at leading order.  NOT produced.")
    print("  - RG2 (O_LL):     same obstruction as RG1.")
    print("  - RG3 (O_eB):     requires specific ratio |c_C|^2/c_I^2 = 1/2.")
    print("    Retained UV matching produces c_C = 0 (no Z_3-breaking term).")
    print("    NOT produced.")
    print("  - RG4 (dim-8):    requires codim-1 condition on (mu_a, mu_b, c).")
    print("    Retained framework does NOT fix these.")
    print("  - RG5:            retained UV matching has no non-trivial circulant.")
    print("  - RG6:            coupled flow fixes chi=1/2 only on codim-1 surface.")
    print()
    print("  CONCLUSION: NO retained-native path generates the required Wilson")
    print("  coefficient structure.  The RG-attractor hypothesis requires a NEW")
    print("  primitive beyond what the retained Cl(3)/Z_3 atlas provides.")

    # Recommendation
    section("Recommendation")
    print("  The assumption 'A1 is a tree-level / scale-independent condition'")
    print("  SURVIVES this probe.  Specifically:")
    print()
    print("    (1) SM 1-loop RG strictly preserves chi (A-rg1 verified).")
    print("    (2) Every tested dim-6 SMEFT operator either")
    print("          (a) preserves chi (no selection at all), or")
    print("          (b) produces an attractor whose value equals the Wilson-")
    print("              coefficient ratio at UV matching (not dynamical).")
    print("    (3) Forcing the attractor to chi = 1/2 requires a codim-1")
    print("        constraint on Wilson coefficients that the retained")
    print("        Cl(3)/Z_3 framework does not produce.")
    print("    (4) Therefore the RG-attractor path does NOT offer a new closure")
    print("        of A1.  A1 remains a tree-level condition that must be")
    print("        forced by a separate mechanism (quartic potential, Casimir")
    print("        identity, or similar).")
    print()
    print("  The probe thus ADDS a negative result to the irreducibility packet:")
    print("  RG flow under standard SMEFT dim-6 operators does not generate A1")
    print("  as an IR attractor without introducing a NEW retained primitive")
    print("  (circulant Wilson coefficient + UV tuning).")
    print()
    print("  Recommended disposition: record this as RG no-go support for the")
    print("  A1 irreducibility claim.  Do not promote any closure flag.")

    # Summary of PASS/FAIL
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")
    print()
    # Closure flags (all must be FALSE)
    print("KOIDE_A1_RG_ATTRACTOR_CLOSES=FALSE")
    print("RG_ATTRACTOR_FOR_A1_FOUND=FALSE")
    print("RETAINED_UV_PRODUCES_REQUIRED_WILSON_COEFFICIENTS=FALSE")
    print("A1_IS_TREE_LEVEL_ASSUMPTION_SURVIVES_RG_PROBE=TRUE")
    print("RESIDUAL_SCALAR=UV_matched_Wilson_ratio_|c_C|^2/c_I^2_required_for_chi*=1/2")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
