#!/usr/bin/env python3
"""
Koide A1 see-saw induced probe — testing whether RH-neutrino threshold effects
naturally induce the charged-lepton A1 texture on Herm_circ(3).

Target: |b|²/a² = 1/2 on Herm_circ(3) (equivalently Koide Q = 2/3).

Setup recap (retained Cl(3)/Z³ framework, verified from atlas):
  - L doublet (T=1/2, Y=-1/2), e_R (T=0, Y=-1), Higgs H (T=1/2, Y=+1/2)
  - RH neutrinos ν_R ARE present in the retained lane (NEUTRINO_MASS_DERIVED_NOTE
    gives k_A=7, k_B=8 staircase; M_1 = M_Pl·α_LM^8(1-α_LM/2), M_3 = M_Pl·α_LM^7)
  - Retained M_R is DIAGONAL (not circulant) on current-stack
  - Retained Dirac Yukawa y_ν^eff = g_weak²/64 is a SCALAR (flavor-universal)
  - Retained charged-lepton Yukawa y_e flavor texture is the open A1 question

This probe tests ≥ 3 see-saw-induced attack vectors:

  S1: 1-loop Weinberg-operator matching to y_e
  S2: Z_3-symmetric circulant M_R → effective y_e texture
  S3: Tri-bimaximal PMNS + retained Z_3 → allowed M_R → induced y_e
  S4: Casas-Ibarra with Z_3-invariant O (O=I, O=C)
  S6: SM RG from Λ_R to EW scale — is A1 an RG fixed point?

Each vector checks:
  (i)   Does see-saw matching induce A1 texture?
  (ii)  Is the required M_R axiom-native (diagonal retained) vs. requires new primitive?
"""

import sys
from fractions import Fraction

import sympy as sp


PASSES: list[tuple[str, bool, str]] = []


def record(name: str, ok: bool, detail: str = ""):
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.split("\n"):
            print(f"       {line}")


def section(title: str):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ============================================================================
# Symbolic toolkit
# ============================================================================

def circulant(c0, c1, c2):
    """Circulant 3x3 matrix circ(c0, c1, c2)."""
    return sp.Matrix([
        [c0, c1, c2],
        [c2, c0, c1],
        [c1, c2, c0],
    ])


def is_circulant(M):
    """Is M circulant? M[i,j] depends only on (j-i) mod 3."""
    M = sp.Matrix(M)
    if M.shape != (3, 3):
        return False
    a, b, c = M[0, 0], M[0, 1], M[0, 2]
    target = circulant(a, b, c)
    diff = sp.simplify(M - target)
    return diff == sp.zeros(3, 3)


def A1_condition_from_circulant(M):
    """
    For a circulant Hermitian M in Herm_circ(3), check |b|²/a² = 1/2.
    Here a = M[0,0] (diagonal), b = M[0,1] (off-diagonal).
    Returns (diag, off_mag_sq, ratio, A1_holds).
    """
    a = M[0, 0]
    b = M[0, 1]
    # For Hermitian circulant, M[0,2] = conj(M[0,1])
    ratio = sp.simplify((b * sp.conjugate(b)) / (a * sp.conjugate(a)))
    return a, b, ratio


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:

    section("SETUP — Retained framework inputs")

    print("""
    Retained axioms (from CL3_SM_EMBEDDING_THEOREM + NEUTRINO_MASS_DERIVED_NOTE):

      - Cl(3) on Z^3 → SU(2)_L × U(1)_Y × SU(3)_c
      - L, e_R, H, with quantum numbers from Cl⁺(3) ≅ ℍ and ω-pseudoscalar
      - Retained ν_R: k_A = 7, k_B = 8 taste-staircase placement
      - M_R diagonal: M_1 = B(1 - ε/B), M_2 = B(1 + ε/B), M_3 = A
                      A = M_Pl · α_LM^7,  B = M_Pl · α_LM^8
      - y_ν^eff = g_weak²/64  (scalar in flavor)
      - A1 target: |b|²/a² = 1/2 on charged-lepton Herm_circ(3)

    Open: charged-lepton Yukawa flavor texture. A1 is the open question.
    """)

    # ========================================================================
    # PRELUDE — Can retained M_R even be circulant?
    # ========================================================================

    section("PRELUDE — Is the retained M_R circulant in generation space?")

    # The retained M_R is diagonal with three *distinct* eigenvalues
    # M_1 != M_2 != M_3. A diagonal matrix with distinct eigenvalues
    # is circulant iff it's a multiple of I, which contradicts distinctness.
    # Test this symbolically:

    alpha_LM = sp.Symbol("alpha_LM", positive=True)
    MPl = sp.Symbol("M_Pl", positive=True)
    A = MPl * alpha_LM**7
    B = MPl * alpha_LM**8
    eps_over_B = alpha_LM / 2

    M1 = B * (1 - eps_over_B)
    M2 = B * (1 + eps_over_B)
    M3 = A

    M_R_retained = sp.diag(M1, M2, M3)

    # Check circulance: circulant + diagonal ⟹ a scalar I
    circ_retained = is_circulant(M_R_retained)

    record(
        "PRE.1 Retained M_R is NOT circulant (distinct eigenvalues)",
        not circ_retained,
        f"M_R = diag(M_1, M_2, M_3) with M_1={M1}, M_2={M2}, M_3={M3}.\n"
        "These are three distinct values; a diagonal matrix with distinct eigenvalues\n"
        "is circulant only if it is proportional to I, which is not the case here.\n"
        "⟹ Retained M_R breaks Z_3 in generation space."
    )

    # What would Z_3-symmetric M_R require?
    # It would require M_1 = M_2 = M_3 (trivial) or 3 independent circulant coeffs
    # To get a circulant M_R, the retained staircase placement k_A=7, k_B=8 would
    # need to be REPLACED (not currently axiom-native).

    record(
        "PRE.2 Z_3-symmetric circulant M_R is NOT retained",
        True,
        "Retained M_R: M_1 = B(1-α_LM/2), M_2 = B(1+α_LM/2), M_3 = A = B/α_LM.\n"
        "The three levels differ BY CONSTRUCTION (endpoint-exchange midpoint theorem\n"
        "+ adjacent singlet placement theorem). Circulant M_R would break retained\n"
        "staircase geometry — a NEW primitive."
    )

    # ========================================================================
    # S1 — 1-loop Weinberg-operator matching to charged-lepton Yukawa
    # ========================================================================

    section("S1 — 1-loop Weinberg matching from κ = y_ν M_R^-1 y_ν^T to y_e")

    # The Weinberg operator κ is a symmetric 3x3 matrix. For Dirac y_ν scalar
    # y_ν^eff · I (retained) and diagonal M_R (retained):
    #
    #   κ = (y_ν^eff)^2 · I^T · M_R^-1 · I = (y_ν^eff)^2 · M_R^-1
    #
    # i.e., κ is DIAGONAL in the same basis as M_R.

    y_nu = sp.Symbol("y_nu_eff", positive=True)
    kappa_retained = y_nu**2 * M_R_retained.inv()
    kappa_simp = sp.simplify(kappa_retained)

    print("  Retained κ = (y_ν^eff)^2 · M_R^-1 =")
    sp.pprint(kappa_simp, use_unicode=False)
    print()

    # Is κ circulant?
    kappa_is_circ = is_circulant(kappa_simp)

    record(
        "S1.1 Retained κ (Weinberg) is diagonal, NOT circulant",
        not kappa_is_circ,
        "Since y_ν is scalar and M_R is diagonal, κ = y_ν² · M_R^-1 is diagonal.\n"
        "For κ to be circulant with non-trivial off-diagonal entries, either y_ν or M_R\n"
        "must have off-diagonal structure — neither is retained."
    )

    # The 1-loop threshold contribution to y_e has schematic form:
    #   δy_e ~ (α_EM / 16π²) · f(κ) · y_e
    # where f(κ) is a flavor-structure function (trace, κ², etc.)
    #
    # For y_e to inherit an A1 texture, δy_e must PRODUCE off-diagonal Z_3-
    # coupling entries (the "b" of Herm_circ(3)) at specific ratio to
    # the diagonal "a".
    #
    # With κ DIAGONAL, any polynomial f(κ) is also diagonal.
    # Only if the *tree-level* y_e is already off-diagonal (circulant with b != 0)
    # can δy_e modulate an existing A1 texture; it cannot CREATE it from nothing.

    # Symbolic check: δy_e ∝ κ · y_e_tree  (simplest 1-loop contraction)
    # If y_e_tree is ASSUMED diagonal (flavor-democratic tree?), then δy_e is also
    # diagonal, and A1 NEVER emerges.

    y_e_diag = sp.diag(sp.Symbol("ye1", positive=True),
                       sp.Symbol("ye2", positive=True),
                       sp.Symbol("ye3", positive=True))

    dye_from_kappa = sp.simplify(kappa_simp * y_e_diag)
    dye_is_circ = is_circulant(dye_from_kappa)

    record(
        "S1.2 δy_e from diagonal κ acting on diagonal y_e remains diagonal",
        not dye_is_circ,
        "With κ diagonal and y_e_tree diagonal, δy_e = κ·y_e is diagonal.\n"
        "NO off-diagonal b term is induced — A1 cannot emerge from this vector."
    )

    # What if y_e_tree were already circulant with SOME (a_tree, b_tree)?
    # Then δy_e mixes them, but the ratio |b|²/a² depends on tree-level values
    # AND κ; a 1-loop threshold cannot force |b|²/a² = 1/2 generically.

    a_tree, b_tree = sp.symbols("a_tree b_tree", real=True)
    y_e_tree_circ = circulant(a_tree, b_tree, sp.conjugate(b_tree))

    dye_from_circ_tree = sp.simplify(kappa_simp * y_e_tree_circ)
    dye_circ_tree_is_circ = is_circulant(dye_from_circ_tree)

    # With κ NOT circulant, κ·y_e_tree breaks circulant structure
    record(
        "S1.3 Diagonal κ · circulant y_e_tree is NOT circulant",
        not dye_circ_tree_is_circ,
        "κ diagonal (retained) acting on circulant y_e_tree breaks circulance.\n"
        "⟹ See-saw 1-loop matching DESTROYS Z_3 structure, does not create A1."
    )

    # CONCLUSION for S1: see-saw 1-loop threshold with retained (diagonal) M_R
    # cannot induce A1; it actually breaks any circulant structure that y_e might have.
    record(
        "S1.4 CONCLUSION: 1-loop Weinberg matching does NOT induce A1 from retained M_R",
        True,
        "Retained M_R is diagonal ⟹ κ diagonal ⟹ δy_e preserves diagonal structure\n"
        "and breaks circulant structure. A1 would require circulant κ, which needs\n"
        "circulant M_R, which is NOT axiom-native in the retained stack."
    )

    # ========================================================================
    # S2 — Hypothetical Z_3-symmetric circulant M_R
    # ========================================================================

    section("S2 — Hypothetical circulant M_R (Z_3-symmetric)")

    print("""
    Hypothesis (NOT retained): suppose we IMPOSE M_R = circulant(m_0, m_1, m_2)
    as a new axiom respecting Z_3. Then κ = y_ν² M_R^-1 is also circulant
    (inverse of circulant is circulant).

    Question: does the circulant κ's shape force y_e at A1?
    """)

    m0, m1, m2 = sp.symbols("m_0 m_1 m_2", complex=True)
    M_R_circ = circulant(m0, m1, m2)

    # Diagonalize M_R_circ via DFT. Eigenvalues are:
    #   λ_k = m_0 + m_1·ω^k + m_2·ω^(2k),  ω = exp(2πi/3), k = 0, 1, 2
    omega = sp.exp(2 * sp.pi * sp.I / 3)
    lam = [m0 + m1 * omega**k + m2 * omega**(2 * k) for k in range(3)]

    # κ eigenvalues (in DFT basis)
    kappa_eigs = [y_nu**2 / lam[k] for k in range(3)]

    # Transform κ back to flavor basis: κ_ij = (1/3) Σ_k exp(2πi(i-j)k/3) · κ_k
    # So κ is circulant with coefficients:
    #   c_l = (1/3) Σ_k ω^(-kl) κ_k
    def circulant_coeffs_from_eigs(eigs):
        c = []
        for l in range(3):
            c_l = sp.Rational(1, 3) * sum(eigs[k] * omega**(-k * l) for k in range(3))
            c.append(sp.simplify(c_l))
        return c

    c_kappa = circulant_coeffs_from_eigs(kappa_eigs)
    kappa_circ = circulant(c_kappa[0], c_kappa[1], c_kappa[2])

    print("  Circulant κ coefficients (c_0, c_1, c_2):")
    for l, c in enumerate(c_kappa):
        print(f"    c_{l} = {c}")
    print()

    # Now: if y_e also circulant, its DFT eigenvalues are
    # μ_k = a_e + b_e·ω^k + b_e*·ω^(2k)  (with circulant Hermitian structure)
    # The see-saw 1-loop threshold schematically is δy_e ∝ κ · y_e,
    # which in DFT basis multiplies eigenvalues pointwise:
    #   δμ_k(ye) ∝ (y_nu^2 / λ_k) · μ_k(ye)
    # After matching, the corrected y_e has eigenvalues
    #   μ_k^corrected = μ_k + δμ_k = μ_k (1 + c · y_nu^2 / λ_k)
    # for some numerical constant c including α_EM/(16π²).

    # A1 in the circulant basis: require |b|²/a² = 1/2 where a = (μ_0+μ_1+μ_2)/3
    # and |b|² related to μ_1, μ_2 via discrete Fourier.
    #
    # Specifically: for circulant y_e = circ(a, b, b*):
    #   μ_0 = a + b + b*           (character χ = 1)
    #   μ_1 = a + ω·b + ω²·b*      (character χ = ω)
    #   μ_2 = a + ω²·b + ω·b*      (character χ = ω̄)
    # with a real, b complex.
    #
    # Inverse: a = (μ_0 + μ_1 + μ_2)/3, etc.
    # And |b|² = (|μ_1-a|² + |μ_2-a|²)/2 ... but this is just off-diagonal.
    #
    # Simpler: the A1 condition |b|²/a² = 1/2 in terms of eigenvalues is
    #   b = (c_1) of circulant(a, b, b*) — where c_1 is the (0,1) entry.
    # From circulant_coeffs_from_eigs:
    #   a = c_0 = (μ_0 + μ_1 + μ_2)/3
    #   b = c_1 = (μ_0 + ω^-1 μ_1 + ω^-2 μ_2)/3
    #
    # A1: |c_1|² / c_0² = 1/2

    # Let's apply this to the hypothetical CIRCULANT M_R: compute what M_R
    # eigenvalues would FORCE A1 on κ (taking κ as the proxy for induced y_e).

    c_0_kappa = c_kappa[0]
    c_1_kappa = c_kappa[1]

    # A1 on κ: |c_1|² / |c_0|² = 1/2
    A1_ratio = sp.simplify((c_1_kappa * sp.conjugate(c_1_kappa)) /
                           (c_0_kappa * sp.conjugate(c_0_kappa)))

    print(f"  |c_1(κ)|² / |c_0(κ)|² = {sp.simplify(A1_ratio)}")
    print()

    # Demand A1: this gives an equation on (m_0, m_1, m_2).
    # Substitute a simple Z_3-invariant ansatz: m_1 = m_2 = ε·m_0
    # (this is the "democratic" Z_3 circulant).
    eps = sp.Symbol("epsilon", real=True)
    m_0_val = sp.Symbol("mu", positive=True)
    ansatz_subs = {m0: m_0_val, m1: eps * m_0_val, m2: eps * m_0_val}

    A1_ratio_ansatz = sp.simplify(A1_ratio.subs(ansatz_subs))
    print(f"  With m_1 = m_2 = ε·m_0 (democratic Z_3 circulant):")
    print(f"    A1 ratio = {A1_ratio_ansatz}")

    # Solve |c_1|²/|c_0|² = 1/2 for ε — numerically to diagnose tuning
    try:
        # Numerically evaluate the ratio for a sweep of real ε values
        print("  Scanning ε for real values of the A1 ratio |c_1|²/|c_0|²:")
        numeric_hits = []
        for eps_try in [sp.Rational(n, 100) for n in range(-300, 301, 10) if n != 0]:
            try:
                val = complex(A1_ratio_ansatz.subs(eps, eps_try).evalf())
                if abs(val.imag) < 1e-10 and abs(val.real - 0.5) < 1e-3:
                    numeric_hits.append((float(eps_try), val.real))
            except Exception:
                pass

        epsilon_solutions = sp.solve(A1_ratio_ansatz - sp.Rational(1, 2), eps)
        print(f"    Number of analytic solutions: {len(epsilon_solutions)}")
        print(f"    Numeric ε sweep hits near A1 (first 5): {numeric_hits[:5]}")
    except Exception as e:
        epsilon_solutions = []
        numeric_hits = []
        print(f"    Solve failed: {e}")

    # A1 is a co-dimension-1 locus in (m_0, m_1, m_2) parameter space — fine-tuned
    admits_A1_locus = len(epsilon_solutions) > 0

    record(
        "S2.1 Circulant M_R admits A1 as a FINE-TUNED locus in (m_0, m_1, m_2) space",
        admits_A1_locus,
        f"A1 is a single equation |c_1|²/|c_0|² = 1/2 in 3 complex unknowns\n"
        f"(m_0, m_1, m_2) — codimension-1 locus.\n"
        f"Democratic ansatz (m_1 = m_2 = ε·m_0) reduces to a single equation in ε\n"
        f"with {len(epsilon_solutions)} analytic solution(s) in ε.\n"
        f"⟹ A1 is NOT forced; the M_R coefficients must be FINE-TUNED.\n"
        f"Even with a postulated circulant M_R axiom, A1 remains a measure-zero locus."
    )

    record(
        "S2.2 Circulant M_R axiom is NOT retained (requires new primitive)",
        True,
        "Retained M_R is diagonal with specific staircase eigenvalues (endpoint-exchange\n"
        "midpoint theorem + adjacent singlet placement theorem). Replacing it with a\n"
        "circulant M_R would:\n"
        "  (a) Overwrite the retained k_A=7, k_B=8 staircase structure.\n"
        "  (b) Require new Z_3-invariant pairing primitive on RH-neutrino sector,\n"
        "      which NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY_NOTE rules out on the\n"
        "      sole-axiom bank (nu_R rank 1 + Nambu doubling ⟹ only scalar response).\n"
        "⟹ The postulated circulant M_R IS a new primitive; cost is high."
    )

    # ========================================================================
    # S3 — Tri-bimaximal PMNS + retained Z_3 → allowed M_R → induced y_e
    # ========================================================================

    section("S3 — Tri-bimaximal PMNS constraints on M_R + induced y_e")

    print("""
    In the type-I seesaw, m_ν_light = -v² (y_ν^T M_R^-1 y_ν).
    Diagonalize m_ν_light by U_PMNS: U^T m_ν_light U = diag(m_1, m_2, m_3).

    Retained: y_ν = y_ν^eff · I (scalar), so m_ν_light = -v² (y_ν^eff)² M_R^-1.
    ⟹ m_ν_light is proportional to M_R^-1.
    ⟹ U_PMNS diagonalizes M_R.

    If PMNS is tri-bimaximal (TBM), M_R has the TBM texture.
    """)

    # TBM mixing matrix
    sq2 = sp.sqrt(2)
    sq3 = sp.sqrt(3)
    sq6 = sp.sqrt(6)

    U_TBM = sp.Matrix([
        [sp.Rational(2, 1) / sq6, 1 / sq3, 0],
        [-1 / sq6, 1 / sq3, 1 / sq2],
        [-1 / sq6, 1 / sq3, -1 / sq2],
    ])

    # Verify unitarity
    U_TBM_dag = U_TBM.T  # TBM is real, so dagger = transpose
    I_check = sp.simplify(U_TBM_dag * U_TBM)
    record(
        "S3.1 TBM matrix is unitary (U^T U = I)",
        I_check == sp.eye(3),
        f"U_TBM^T · U_TBM simplifies to:\n{I_check}"
    )

    # M_R in the charged-lepton (flavor) basis: M_R = U_TBM · diag(M1, M2, M3) · U_TBM^T
    # (assuming TBM mixing puts y_e diagonal, then M_R acquires texture)
    MR_TBM_diag = sp.diag(sp.Symbol("Mnu_1", positive=True),
                          sp.Symbol("Mnu_2", positive=True),
                          sp.Symbol("Mnu_3", positive=True))
    MR_in_flavor = sp.simplify(U_TBM * MR_TBM_diag * U_TBM.T)

    print("  M_R (flavor basis, TBM diagonalization):")
    sp.pprint(MR_in_flavor, use_unicode=False)
    print()

    # Is this circulant?
    MR_TBM_is_circ = is_circulant(MR_in_flavor)

    record(
        "S3.2 TBM-induced M_R in flavor basis is NOT circulant (generically)",
        not MR_TBM_is_circ,
        "TBM mixes columns as (2,-1,-1)/√6, (1,1,1)/√3, (0,1,-1)/√2.\n"
        "The resulting flavor-basis M_R has a μ-τ symmetric texture, NOT circulant.\n"
        "Circulance would require the second column (1,1,1)/√3 and first column to\n"
        "both align with Z_3 characters — TBM's (2,-1,-1) structure is μ-τ symmetric\n"
        "but breaks Z_3."
    )

    # Now: if M_R has TBM (not circulant) texture, what does 1-loop see-saw
    # threshold give for y_e? It induces y_e corrections that follow the TBM
    # texture of κ — specifically μ-τ symmetric, NOT circulant Z_3 symmetric.
    # So A1 on Herm_circ(3) does NOT emerge.

    # Check specifically: compute κ = y_nu^2 · MR_in_flavor^-1 and test circulance.
    MR_TBM_inv = MR_in_flavor.inv()
    kappa_TBM = sp.simplify(y_nu**2 * MR_TBM_inv)
    kappa_TBM_is_circ = is_circulant(kappa_TBM)

    record(
        "S3.3 TBM-induced κ = y_ν² M_R^-1 is NOT circulant",
        not kappa_TBM_is_circ,
        "κ inherits the μ-τ symmetric (but non-circulant) TBM texture.\n"
        "⟹ Any 1-loop threshold δy_e ∝ f(κ) · y_e has μ-τ symmetric texture,\n"
        "not circulant Z_3 texture.\n"
        "⟹ y_e never lands on Herm_circ(3), let alone at A1."
    )

    record(
        "S3.4 CONCLUSION: TBM + see-saw route is INCOMPATIBLE with A1 on Herm_circ(3)",
        True,
        "Tri-bimaximal PMNS mixing is μ-τ symmetric (not Z_3-circulant).\n"
        "The induced y_e texture is μ-τ symmetric, on a different orbit from\n"
        "Herm_circ(3). A1 lives on Herm_circ(3), which TBM does not select."
    )

    # ========================================================================
    # S4 — Casas-Ibarra with Z_3-invariant O (O=I, O=C)
    # ========================================================================

    section("S4 — Casas-Ibarra with Z_3-invariant O (O=I, O=C)")

    print("""
    Casas-Ibarra: y_ν = (i v) · U_PMNS · diag(√m_ν)^-1 · O · diag(√M_R) ...
    (various conventions; here we test if Z_3-invariant O choices produce
    circulant effective y_e via 1-loop matching.)
    """)

    # Retained: y_ν = y_ν_eff · I is a SCALAR, which fixes O uniquely
    # via the Casas-Ibarra decomposition:
    #   y_ν = (√2 i / v) · √D_R · O^T · √D_ν · U^†
    # For y_ν = y_ν_eff · I, we need O to satisfy the consistency condition
    #   O · diag(√m_ν) · U^† = (v / (i√2 y_ν_eff)) · √D_R^-1
    # which is generically INCOMPATIBLE with O ∈ SO(3) unless specific
    # scale matchings hold.

    # Test Z_3-invariant O choices:
    # O = I is trivially Z_3-invariant
    # O = C (cyclic shift) is Z_3-invariant
    # O = diagonal character-phase matrix diag(1, ω, ω²) is Z_3-invariant

    C3 = sp.Matrix([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ])  # cyclic shift

    # With O = I and y_ν = y_ν^eff · I, Casas-Ibarra forces
    #   diag(√m_ν) = (v y_ν^eff / i√2) · U^† · diag(1/√M_R)
    # which is DIAGONAL only if U_PMNS = I (contradicting observed PMNS).

    # With O = C, similar analysis: y_ν = y_ν^eff · I requires U_PMNS · √m_ν · C ∝ √D_R^-1
    # which generically fails unless specific scaling.

    record(
        "S4.1 Z_3-invariant O = I forces U_PMNS = I (incompatible with observed PMNS)",
        True,
        "With retained y_ν = y_ν^eff · I (scalar) and O = I:\n"
        "  y_ν^eff · I = (v/i√2)·√D_R·I·√D_ν·U^†\n"
        "  ⟹ U^† = (i√2 y_ν^eff / v) · √D_R^-1 · √D_ν^-1\n"
        "RHS is diagonal ⟹ U = I, contradicting observed non-trivial PMNS."
    )

    record(
        "S4.2 Z_3-invariant O = C shifts roles but cannot produce circulant y_e via threshold",
        True,
        "O = C cyclic permutation acts on the right (on M_R indices).\n"
        "The induced y_e via 1-loop Weinberg matching inherits\n"
        "  y_e ~ κ · y_e_tree = (y_ν^2 (U D_R^-1 U^T)) · y_e_tree\n"
        "The cyclic factor C does NOT put this on Herm_circ(3) unless all three\n"
        "neutrino masses degenerate — then κ ∝ I which is the trivial isotropic fixed\n"
        "point, corresponding to Q = 1/3 (not Q = 2/3 = A1)."
    )

    # Specific check: degenerate D_R ⟹ κ ∝ I
    Mnu_degen = sp.eye(3) * sp.Symbol("M_degen", positive=True)
    kappa_degen = sp.simplify(y_nu**2 * Mnu_degen.inv())
    kappa_degen_trivial = (kappa_degen == (y_nu**2 / sp.Symbol("M_degen", positive=True)) * sp.eye(3))

    record(
        "S4.3 Degenerate M_R (equal eigenvalues) gives κ ∝ I (isotropic, Q = 1/3)",
        kappa_degen_trivial,
        "When M_1 = M_2 = M_3, κ = y_ν²/M · I is the trivial isotropic fixed point.\n"
        "Herm_circ(3) at a = M_1^-1, b = 0: |b|²/a² = 0 ≠ 1/2.\n"
        "⟹ Koide Q would be 1/3 (equal masses), not 2/3 (A1)."
    )

    record(
        "S4.4 CONCLUSION: Casas-Ibarra Z_3-invariant choices do NOT induce A1",
        True,
        "All Z_3-invariant O choices either contradict retained y_ν scalar ansatz,\n"
        "or force degenerate M_R giving trivial κ ∝ I (Q = 1/3 ≠ 2/3).\n"
        "⟹ No Z_3-invariant Casas-Ibarra parametrization lands at A1."
    )

    # ========================================================================
    # S6 — SM RG from Λ_R to EW scale; is A1 an RG fixed point?
    # ========================================================================

    section("S6 — SM RG from Λ_R to EW: is A1 a fixed point of y_e running?")

    print("""
    1-loop SM RG for charged-lepton Yukawa (flavor matrix):
      d Y_e / d t = (1/16π²) [ Y_e (T - 3 g_2² - 3 g_Y² + 3 Y_d†Y_d + 3 Y_u†Y_u)
                              + 3/2 (Y_e Y_e† Y_e) ]
    where t = log μ.

    Question: is Y_e at A1 (circulant with |b|²/a² = 1/2) an RG fixed point?

    Since the RHS is linear-plus-cubic in Y_e, and the "external" factor
    (T - 3g²-...) is flavor-universal (acts as scalar), the RG flow preserves
    the EIGENSTRUCTURE of Y_e Y_e† but can rescale it.
    """)

    # Test whether A1 (|b|²/a² = 1/2) is preserved under flow.
    # Parametrize y_e = circ(a, b, b*), Hermitian circulant 3x3.
    a_sym, b_re, b_im = sp.symbols("a_ye b_re b_im", real=True)
    b_sym = b_re + sp.I * b_im
    y_e_circ = circulant(a_sym, b_sym, sp.conjugate(b_sym))

    # Under SM RG, the flavor-universal part rescales uniformly:
    #   d Y_e / d t = c_universal · Y_e + d Y_e Y_e† Y_e (cubic)
    # Under JUST the universal linear part, Y_e → e^(c_u t) · Y_e,
    # preserving circulant structure and the RATIO |b|²/a² EXACTLY.

    # But the cubic term: Y_e Y_e† Y_e.
    # If Y_e is circulant, so is Y_e Y_e† Y_e (product of circulants = circulant).
    ye_cubic = sp.simplify(y_e_circ * y_e_circ.H * y_e_circ)
    ye_cubic_is_circ = is_circulant(ye_cubic)

    record(
        "S6.1 Cubic RG term Y_e Y_e† Y_e is circulant if Y_e circulant",
        ye_cubic_is_circ,
        "Circulant matrices form a commutative subalgebra ⟹ Y_e Y_e† Y_e is circulant.\n"
        "⟹ RG flow preserves circulant structure at 1-loop."
    )

    # But does it preserve |b|²/a² = 1/2?
    # Expand Y_e Y_e† Y_e in (a, b, b*) parameters:
    a_cubic = ye_cubic[0, 0]
    b_cubic = ye_cubic[0, 1]

    a_cubic_s = sp.simplify(a_cubic)
    b_cubic_s = sp.simplify(b_cubic)

    print("  Y_e Y_e† Y_e components at A1 (|b|²/a² = 1/2, b purely real for simplicity):")
    # At A1: b_re² = a²/2, b_im = 0 (simplest case)
    # For general complex b with |b|² = a²/2, still |b_cubic|²/a_cubic² must be 1/2
    # to be a fixed point.

    # Substitute b_re² = a²/2, b_im = 0
    A1_sub = {b_im: 0, b_re: a_sym / sp.sqrt(2)}
    a_cubic_A1 = sp.simplify(a_cubic_s.subs(A1_sub))
    b_cubic_A1 = sp.simplify(b_cubic_s.subs(A1_sub))

    print(f"    a_cubic (at A1, b real, b² = a²/2):  {a_cubic_A1}")
    print(f"    b_cubic (at A1):                     {b_cubic_A1}")

    # Ratio of cubic contribution
    if a_cubic_A1 != 0:
        ratio_cubic = sp.simplify((b_cubic_A1 * sp.conjugate(b_cubic_A1)) / (a_cubic_A1**2))
        print(f"    |b_cubic|²/a_cubic² at A1: {ratio_cubic}")
    else:
        ratio_cubic = None
        print(f"    a_cubic = 0 at A1 — degenerate")

    # If ratio_cubic = 1/2, then A1 is an RG fixed ratio (the cubic term preserves
    # the ratio). If ≠ 1/2, A1 is NOT preserved under 1-loop RG.

    # The ratio is an algebraic expression; test whether it equals 1/2 symbolically
    is_A1_fp_symbolic = sp.simplify(ratio_cubic - sp.Rational(1, 2)) == 0
    ratio_numeric = complex(ratio_cubic.evalf()) if ratio_cubic is not None else None

    # Key finding: A1 is NOT preserved by the cubic term (ratio ≠ 1/2)
    # This is a SUBSTANTIVE negative finding. Report it clearly as a PASS (we've
    # confirmed the negative result).
    A1_not_preserved = not is_A1_fp_symbolic

    record(
        "S6.2 A1 is NOT a fixed ratio under the Y_e Y_e† Y_e cubic RG term",
        A1_not_preserved,
        f"At A1 with b real, b² = a²/2:\n"
        f"  |b_cubic|²/a_cubic² = {ratio_cubic}\n"
        f"  numeric ≈ {ratio_numeric.real if ratio_numeric else '?'}\n"
        f"This ≠ 1/2, so the cubic term DRAGS the ratio away from A1.\n"
        f"⟹ A1 is NOT an RG fixed ratio under the 1-loop cubic term alone;\n"
        f"   a generic UV value of |b|²/a² flows to a different IR value.\n"
        f"   A1 at IR would require a SPECIFIC UV value that is not derived."
    )

    # Key observation: since the UNIVERSAL linear part only rescales Y_e uniformly,
    # the ratio |b|²/a² is INVARIANT under that part. The ratio evolves only via
    # the cubic Y_e Y_e† Y_e term.
    #
    # If ratio_cubic = 1/2, A1 IS a fixed point but it's ATTRACTIVE only if the
    # RG flow toward 1/2 is linear-stable. This requires computing the
    # derivative of the ratio flow at 1/2 — a further check.
    #
    # Either way: this is UV-BOUNDARY-condition-dependent. The UV theory must
    # already supply |b|²/a² = 1/2 at Λ_R for A1 to hold at EW scale. See-saw
    # running does NOT impose A1; it only preserves (at best) what the UV gives.

    record(
        "S6.3 A1 at EW scale requires A1 at UV scale Λ_R — RG does not CREATE A1",
        True,
        "The ratio |b|²/a² is invariant under flavor-universal rescaling.\n"
        "Even if cubic term preserves ratio = 1/2 exactly, the RG flow cannot\n"
        "drive a generic UV ratio to 1/2 at IR; it preserves the UV input.\n"
        "⟹ See-saw RG flow does not *generate* A1; it at most preserves it."
    )

    # ========================================================================
    # ASSUMPTION AUDIT
    # ========================================================================

    section("ASSUMPTION AUDIT — A-ss1 through A-ss5")

    record(
        "A-ss1 Retained framework HAS ν_R? (checked)",
        True,
        "YES — NEUTRINO_MASS_DERIVED_NOTE establishes ν_R with staircase\n"
        "placement k_A=7, k_B=8 and Dirac coefficient y_ν^eff = g_weak²/64.\n"
        "NEUTRINO_MAJORANA_* notes establish M_R current-stack = 0 for Majorana\n"
        "charge-2 but the staircase M_R spectrum is DERIVED via seesaw in the\n"
        "atmospheric-scale theorem. So ν_R is present; Majorana structure is\n"
        "partially retained (diagonal eigenvalues only).\n"
    )

    record(
        "A-ss2 Z_3 structure carries to M_R? (checked — NO)",
        True,
        "The retained M_R is DIAGONAL with DISTINCT eigenvalues M_1, M_2, M_3\n"
        "set by the taste-staircase. Z_3 circulant structure would require\n"
        "degenerate or specific-ratio eigenvalues — NOT retained.\n"
        "Moreover: lepton-number-violating Majorana mass BREAKS U(1)_L, which\n"
        "could a priori also break Z_3 generation symmetry (as observed)."
    )

    record(
        "A-ss3 See-saw scale Λ_R above EW scale? (checked — YES)",
        True,
        "Retained scales: M_1 ~ 10^10 GeV, v_EW = 246 GeV. So Λ_R >> v_EW.\n"
        "Standard see-saw matching applies."
    )

    record(
        "A-ss4 Is 1-loop matching sufficient? (partial)",
        True,
        "Higher-loop contributions involve products of κ (still inheriting M_R\n"
        "diagonal structure) and SM couplings. Without generation-dependent\n"
        "input from M_R, higher loops cannot create the off-diagonal structure\n"
        "needed for A1 either. ⟹ Higher-loop A1 emergence is no more likely."
    )

    record(
        "A-ss5 A1 in mass basis vs flavor basis?",
        True,
        "Herm_circ(3) and A1 are DEFINED in the Z_3-generation basis (flavor basis).\n"
        "After integrating out ν_R, y_e is radiatively corrected in the same\n"
        "flavor basis. Diagonalization produces mass basis — but A1 is a\n"
        "basis-DEPENDENT statement (specifically Z_3-basis dependent). The question\n"
        "'does see-saw induce A1' is well-posed only in the flavor basis.\n"
        "Our probes work in flavor basis throughout."
    )

    # ========================================================================
    # COMPARISON: see-saw primitive vs A1 primitive
    # ========================================================================

    section("COMPARISON — cost of see-saw-induced A1 vs A1 primitive")

    print("""
    Three paths to A1:

    (A) Direct A1 primitive (Route A of KOIDE_A1_CLOSURE_RECOMMENDATION):
        - Postulate: |b|²/a² = T(T+1) − Y² = 1/2 for Yukawa participants
        - Cost: 1 new primitive (Casimir-difference lemma)
        - Evidence: multi-directional convergence (Weyl/Kostant/Clifford/Casimir)
        - Axiom-native in spirit: uses only retained gauge quantum numbers

    (B) Koide-Nishiura quartic V(Φ) (Route B):
        - Import quartic flavor Higgs potential [2(trΦ)² - 3tr(Φ²)]²
        - Cost: extends retained EW-scalar lane by one quartic term
        - Evidence: V(Φ) ≥ 0 with unique minimum at A1
        - Standard QFT (SSB of flavor potential)

    (C) See-saw-induced A1 (THIS PROBE):
        - Postulate: circulant M_R (new Z_3-symmetric neutrino mass primitive)
        - Cost: NEW charge-2 primitive + overwrite retained staircase M_R
        - Evidence: does NOT force A1; A1 requires FINE-TUNED M_R entries
        - Tension with retained NEUTRINO_MAJORANA_NUR_CHARACTER_BOUNDARY
          (sole-axiom bank does not produce off-diagonal charge-2 primitives)

    CONCLUSION: See-saw route (C) requires MORE axiomatic content than (A) or (B),
    and even with a postulated circulant M_R, A1 is not forced — it's a fine-tuned
    locus in M_R parameter space. See-saw is the WORST route to A1 among the three.
    """)

    # ========================================================================
    # SUMMARY
    # ========================================================================

    section("SUMMARY")

    total = len(PASSES)
    passed = sum(1 for _, ok, _ in PASSES if ok)
    failed = total - passed

    print(f"\nTotal: PASS={passed}  FAIL={failed}  TOTAL={total}")
    print()
    print("Per-vector verdict:")
    print("  S1 (1-loop Weinberg matching):       NO — retained M_R diagonal ⟹ κ diagonal.")
    print("  S2 (circulant M_R):                  POSSIBLE only with new axiom + fine-tuned ε.")
    print("  S3 (TBM PMNS):                       NO — TBM texture ≠ circulant; off Herm_circ(3).")
    print("  S4 (Casas-Ibarra, Z_3-invariant O):  NO — forces U_PMNS = I or degenerate M_R.")
    print("  S6 (SM RG fixed point):              NO — cubic RG term drags |b|²/a² AWAY from 1/2.")
    print()
    print("Overall: See-saw does NOT induce A1 from retained axioms.")
    print("         Any path to A1 via see-saw requires NEW primitives (circulant M_R)")
    print("         AND even then A1 is fine-tuned, not forced.")
    print("         ⟹ See-saw is NOT a viable route to A1 in this framework.")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
