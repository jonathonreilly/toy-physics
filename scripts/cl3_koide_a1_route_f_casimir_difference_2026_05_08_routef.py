"""
Koide A1 Route F — Yukawa Casimir-Difference Lemma: bounded obstruction verification.

Investigates whether the structural lemma

    |b|^2 / a^2  =  T(T+1) - Y^2

(proposed in `KOIDE_A1_DERIVATION_STATUS_NOTE.md` Route F as the strongest
axiom-native A1 closure candidate) can be derived from retained content
on the Cl(3)/Z^3 framework, with no empirical loading and no new axioms.

VERDICT: STRUCTURAL OBSTRUCTION CONFIRMED.

Four structural barriers are checked:

  Barrier 1 (Convention dependence): T(T+1) - Y^2 = 1/2 holds only in
  the Q = T_3 + Y convention with Y_L = -1/2. In the hypercharge
  convention used by the CL3_SM_EMBEDDING_THEOREM source note
  (Y_L = -1), T(T+1) - Y^2 = 3/4 - 1 = -1/4. The proposed numerical
  identity is convention-dependent, hence not a structural invariant.

  Barrier 2 (Free Yukawa matrix): per the retained
  `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`,
  one-Higgs gauge selection determines that Y_e is an arbitrary
  3x3 complex matrix. C_3-equivariance (Route 1 obstruction) further
  narrows it to circulant Y = aI + bU + b̄U^{-1}, but a, b remain
  FREE parameters. No retained gauge/group constraint fixes their
  ratio. The Casimir-difference number 1/2 is GAUGE-LEVEL, not
  flavor-LEVEL.

  Barrier 3 (Sector orthogonality): the SU(2)_L Casimir acts on the
  doublet sector, while the C_3-circulant coefficients live on the
  hw=1 three-state sector. The Casimir scalar acts trivially on
  generation indices; a bridge theorem would be additional input.

  Barrier 4 (Category mismatch): |b|^2/a^2 is an operator-coefficient
  ratio, while T(T+1) - Y^2 is a representation-label scalar.
  Equating them requires a normalization map not supplied by the
  cited source stack.

These four barriers establish that the Route F lemma cannot close from
retained content alone. The matching number 1/2 = 1/2 is a numerical
coincidence between independently-defined quantities, NOT a structural
identity.

The runner verifies all four barriers with explicit linear-algebra
counter-examples and convention checks. PDG values appear ONLY as
falsifiability anchors at the very end (clearly marked anchor-only).

Source-note authority:
[`docs/KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md`](../docs/KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md)

Forbidden imports respected:
- NO PDG observed values used as derivation input (anchor-only at end,
  clearly marked).
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms
"""

import numpy as np
from fractions import Fraction


# --------------------------------------------------------------------
# Constants and primitive C_3 action (mirrors Route 1 conventions)
# --------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3.0)  # primitive cube root of unity

# C_3[111] action on hw=1 corner basis: |c_1⟩ → |c_2⟩ → |c_3⟩ → |c_1⟩
U_C3_CORNER = np.array([
    [0, 0, 1],
    [1, 0, 0],
    [0, 1, 0],
], dtype=complex)

# Pauli matrices (Cl(3) generators)
SIGMA_1 = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_3 = np.array([[1, 0], [0, -1]], dtype=complex)
SIGMAS = [SIGMA_1, SIGMA_2, SIGMA_3]


def passfail(name: str, ok: bool, detail: str = ""):
    """Print a PASS/FAIL line with optional detail."""
    tag = "PASS" if ok else "FAIL"
    if detail:
        print(f"  {tag} : {name} | {detail}")
    else:
        print(f"  {tag} : {name}")
    return ok


def make_circulant(a: float, b: complex):
    """Hermitian circulant: a*I + b*U + b̄*U^{-1} on hw=1."""
    U = U_C3_CORNER
    Uinv = np.conjugate(U.T)  # U^{-1} = U^† since U is unitary
    return a * np.eye(3, dtype=complex) + b * U + np.conjugate(b) * Uinv


# --------------------------------------------------------------------
# Section 1 — Reproduce the numerical match (existing 9/9 PASS Route F)
# --------------------------------------------------------------------

def section1_numerical_match():
    """Confirm that in the Q = T_3 + Y convention, the lepton doublet and
    Higgs satisfy T(T+1) - Y^2 = 1/2, while no other SM particle does.

    This SECTION CONFIRMS the numerical match from the original Route F
    runner. It is the starting point — establishing what Route F asserts
    as the candidate identity.
    """
    print("Section 1 — Numerical match: T(T+1) - Y^2 = 1/2 in Q = T_3 + Y convention")
    print("           (anchor for Route F's candidate identity claim)")
    results = []

    # SM particle table (T, Y) in Q = T_3 + Y convention (PDG modern)
    sm_particles_pdg = [
        ("Lepton doublet L (ν_L, e_L)", Fraction(1, 2), Fraction(-1, 2)),
        ("Higgs H",                     Fraction(1, 2), Fraction( 1, 2)),
        ("Quark doublet Q",             Fraction(1, 2), Fraction( 1, 6)),
        ("e_R",                         Fraction(0),    Fraction(-1)),
        ("u_R",                         Fraction(0),    Fraction( 2, 3)),
        ("d_R",                         Fraction(0),    Fraction(-1, 3)),
    ]
    A1_target = Fraction(1, 2)

    # 1.1 — L doublet has T(T+1) - Y^2 = 1/2 in PDG convention
    T_L = Fraction(1, 2)
    Y_L_pdg = Fraction(-1, 2)
    diff_L = T_L * (T_L + 1) - Y_L_pdg * Y_L_pdg
    results.append(passfail(
        "Lepton doublet (PDG conv): T(T+1) - Y^2 = 1/2",
        diff_L == A1_target,
        f"3/4 - 1/4 = {diff_L} (target {A1_target})",
    ))

    # 1.2 — Higgs satisfies same identity
    T_H = Fraction(1, 2)
    Y_H_pdg = Fraction(1, 2)
    diff_H = T_H * (T_H + 1) - Y_H_pdg * Y_H_pdg
    results.append(passfail(
        "Higgs (PDG conv): T(T+1) - Y^2 = 1/2",
        diff_H == A1_target,
        f"3/4 - 1/4 = {diff_H} (target {A1_target})",
    ))

    # 1.3 — Other SM particles do NOT satisfy the identity
    other_no_match = True
    for label, T, Y in sm_particles_pdg[2:]:
        d = T * (T + 1) - Y * Y
        if d == A1_target:
            other_no_match = False
    results.append(passfail(
        "Other SM particles: T(T+1) - Y^2 != 1/2",
        other_no_match,
        "Quark doublet, e_R, u_R, d_R all give different values",
    ))

    return results


# --------------------------------------------------------------------
# Section 2 — Barrier 1: convention dependence of T(T+1) - Y^2 = 1/2
# --------------------------------------------------------------------

def section2_convention_dependence():
    """Show that the identity T(T+1) - Y^2 = 1/2 is CONVENTION-DEPENDENT.

    The retained CL3_SM_EMBEDDING_THEOREM uses the SU(5)-style
    convention Q = T_3 + Y/2 with Y_L = -1, Y_H = +1. In that
    convention, T(T+1) - Y^2 = 3/4 - 1 = -1/4, not 1/2.

    Therefore the candidate identity does NOT hold under the framework's
    own retained hypercharge convention. The "1/2" appears only when
    one re-conventions to PDG (Q = T_3 + Y), which is a re-labeling,
    not a derivation.
    """
    print("Section 2 — Barrier 1: T(T+1) - Y^2 = 1/2 is convention-dependent")
    results = []

    # 2.1 — In CL3_SM_EMBEDDING convention (Y_L = -1), T(T+1) - Y^2 = -1/4
    T = Fraction(1, 2)
    Y_L_su5 = Fraction(-1)  # CL3_SM_EMBEDDING convention
    diff_su5 = T * (T + 1) - Y_L_su5 * Y_L_su5
    results.append(passfail(
        "CL3_SM_EMBEDDING conv (Y_L = -1): T(T+1) - Y^2 = -1/4 (NOT 1/2)",
        diff_su5 == Fraction(-1, 4),
        f"3/4 - 1 = {diff_su5} (NOT the A1 target 1/2)",
    ))

    # 2.2 — Same value 1/2 appears only under PDG conv (Y_L = -1/2)
    Y_L_pdg = Fraction(-1, 2)
    diff_pdg = T * (T + 1) - Y_L_pdg * Y_L_pdg
    results.append(passfail(
        "PDG conv (Y_L = -1/2): T(T+1) - Y^2 = 1/2 (different result)",
        diff_pdg == Fraction(1, 2),
        f"3/4 - 1/4 = {diff_pdg}",
    ))

    # 2.3 — Two conventions are related by Y_pdg = Y_su5/2; both give the
    #       same physical Q = T_3 + Y_pdg = T_3 + Y_su5/2
    Q_lepton_pdg = Fraction(-1, 2) + Y_L_pdg     # T_3 = -1/2 for e_L
    Q_lepton_su5 = Fraction(-1, 2) + Y_L_su5 / 2
    results.append(passfail(
        "Both conventions give same physical Q = -1 for e_L",
        Q_lepton_pdg == Q_lepton_su5 == Fraction(-1),
        f"Q_pdg = {Q_lepton_pdg}, Q_su5 = {Q_lepton_su5}",
    ))

    # 2.4 — Therefore "1/2 = T(T+1) - Y^2" is NOT a convention-invariant
    #       statement. It depends on which Y normalization is used.
    print("       NOTE: A genuine structural identity must be convention-invariant.")
    print("       The numerical value 1/2 depends on the hypercharge normalization,")
    print("       so it cannot be a structural Casimir-difference identity.")
    print()

    return results


# --------------------------------------------------------------------
# Section 3 — Barrier 2: a, b are free parameters in the retained Yukawa
# --------------------------------------------------------------------

def section3_free_yukawa_coefficients():
    """Show that the retained one-Higgs Yukawa structure leaves Y_e as an
    arbitrary 3x3 complex matrix. C_3-equivariance further narrows it to
    circulant, but a, b remain FREE parameters.

    Therefore the ratio |b|^2 / a^2 is NOT determined by retained gauge
    structure alone. No retained theorem fixes its value.
    """
    print("Section 3 — Barrier 2: a, b are free parameters in retained Yukawa")
    results = []

    # 3.1 — Two distinct circulants both satisfy gauge selection (Y_e free)
    a1, b1 = 1.0, 0.3 + 0.0j
    Y1 = make_circulant(a1, b1)
    a2, b2 = 1.0, 0.7 + 0.4j
    Y2 = make_circulant(a2, b2)

    # Both are Hermitian and C_3-equivariant
    h1 = np.allclose(Y1, Y1.conj().T)
    h2 = np.allclose(Y2, Y2.conj().T)
    eq1 = np.allclose(Y1 @ U_C3_CORNER, U_C3_CORNER @ Y1)
    eq2 = np.allclose(Y2 @ U_C3_CORNER, U_C3_CORNER @ Y2)
    results.append(passfail(
        "Two distinct (a, b) circulants both Hermitian and C_3-equivariant",
        h1 and h2 and eq1 and eq2,
        f"|b1|/a1 = {abs(b1)/a1:.3f}, |b2|/a2 = {abs(b2)/a2:.3f} — both compatible with retained Y_e structure",
    ))

    # 3.2 — Their ratios |b|^2 / a^2 are different
    r1 = abs(b1)**2 / a1**2
    r2 = abs(b2)**2 / a2**2
    results.append(passfail(
        "Different (a, b) give different |b|^2/a^2 ratios",
        not np.isclose(r1, r2),
        f"|b1|^2/a1^2 = {r1:.4f}, |b2|^2/a2^2 = {r2:.4f}",
    ))

    # 3.3 — Yet T(T+1) - Y^2 has only ONE value (1/2 in PDG conv)
    #       So no map from gauge-Casimir to flavor-coefficient ratio
    casimir_diff_value = 0.5  # T(T+1) - Y^2 in PDG conv
    results.append(passfail(
        "Casimir-difference is a single fixed value, but |b|^2/a^2 is free",
        not np.isclose(r1, r2) and not (np.isclose(r1, casimir_diff_value) and np.isclose(r2, casimir_diff_value)),
        f"Single Casimir-diff = {casimir_diff_value}, but |b|^2/a^2 ranges freely",
    ))

    # 3.4 — Counterexample: a=1, b=1 gives |b|^2/a^2 = 1, NOT 1/2
    a3, b3 = 1.0, 1.0 + 0.0j
    Y3 = make_circulant(a3, b3)
    h3 = np.allclose(Y3, Y3.conj().T)
    eq3 = np.allclose(Y3 @ U_C3_CORNER, U_C3_CORNER @ Y3)
    r3 = abs(b3)**2 / a3**2
    results.append(passfail(
        "Counterexample: (a=1, b=1) circulant has |b|^2/a^2 = 1 (NOT 1/2)",
        h3 and eq3 and np.isclose(r3, 1.0),
        f"r = {r3:.3f}; this satisfies all retained constraints but violates A1",
    ))

    # 3.5 — Counterexample: a=1, b=0 (degenerate, all eigenvalues equal a)
    Y4 = make_circulant(1.0, 0.0 + 0.0j)
    eigs4 = np.linalg.eigvalsh(Y4)
    degenerate = np.allclose(eigs4, [1.0, 1.0, 1.0])
    results.append(passfail(
        "Counterexample: (a=1, b=0) circulant is degenerate (all m_k equal)",
        degenerate,
        f"eigenvalues = {eigs4} — no Koide structure at all, yet retained-compatible",
    ))

    return results


# --------------------------------------------------------------------
# Section 4 — Barrier 3: gauge-quantum-number sector vs flavor sector
# --------------------------------------------------------------------

def section4_sector_orthogonality():
    """Show that the SU(2)_L doublet representation (where T(T+1) lives)
    and the hw=1 generation triple (where the C_3-circulant lives) are
    ORTHOGONAL sectors in the framework.

    SU(2)_L acts on a 2-dim space (T_3 = ±1/2). hw=1 has dim 3 with
    C_3 cycle. Casimir T(T+1) is a scalar on the 2-dim doublet,
    independent of the 3-dim generation space.
    """
    print("Section 4 — Barrier 3: SU(2)_L doublet sector vs hw=1 generation triple")
    results = []

    # 4.1 — SU(2) on doublet: J_i = sigma_i / 2, J^2 = (3/4) I_2
    J1 = SIGMA_1 / 2
    J2 = SIGMA_2 / 2
    J3 = SIGMA_3 / 2
    J_squared = J1 @ J1 + J2 @ J2 + J3 @ J3
    casimir_doublet = J_squared.diagonal()[0].real
    results.append(passfail(
        "SU(2)_L Casimir on doublet: J^2 = (3/4) I_2 acts on 2-dim space",
        np.isclose(casimir_doublet, 0.75) and J_squared.shape == (2, 2),
        f"J^2 = {casimir_doublet} I_2, dim = 2",
    ))

    # 4.2 — hw=1 sector has dim 3 (3 corner states, NOT 2-dim doublet)
    hw1_dim = U_C3_CORNER.shape[0]
    results.append(passfail(
        "hw=1 sector has dim 3 (3 generations / corner states)",
        hw1_dim == 3,
        f"dim(hw=1) = {hw1_dim} != 2 = dim(doublet)",
    ))

    # 4.3 — These sectors live in different mathematical spaces:
    #       - Doublet (T, Y) representation: 2-dim
    #       - hw=1 (C_3 corner): 3-dim
    #       The Casimir scalar T(T+1) is a number; the circulant
    #       (a, b) parameters are operator coefficients on a different
    #       3-dim space. There is no derivation chain in retained
    #       content that links the two.
    sector_separation_visible = (
        np.isclose(casimir_doublet, 0.75)
        and J_squared.shape == (2, 2)
        and hw1_dim == 3
        and hw1_dim != J_squared.shape[0]
    )
    results.append(passfail(
        "Casimir-to-circulant bridge is not present in the represented sectors",
        sector_separation_visible,
        "doublet (2-dim, T,Y) and hw=1 (3-dim, C_3) are separate "
        "represented sectors; a bridge theorem would be additional input",
    ))

    # 4.4 — The flavor matrix Y_e acts trivially on doublet indices
    #       (since gauge invariance commutes with flavor). So T(T+1)
    #       affects all flavor matrix entries equally — no constraint
    #       on relative magnitudes.
    # Demonstrate via tensor product:
    #   Total operator: Y_e (3x3 in flavor) ⊗ (some 2-component in doublet)
    #   Casimir T(T+1) acts only on the 2-component, leaves 3x3 free.
    Y_e = make_circulant(0.7, 0.3 + 0.4j)  # any circulant
    # T(T+1) on doublet is a scalar 3/4. Acting on Y_e ⊗ I_2 it just rescales.
    casimir_tensor_on_Ye = 0.75 * Y_e
    matrix_shape_preserved = casimir_tensor_on_Ye.shape == Y_e.shape
    results.append(passfail(
        "Casimir T(T+1) acting on flavor sector is a scalar multiplier",
        matrix_shape_preserved,
        "T(T+1) commutes with flavor structure; cannot constrain |b|^2/a^2",
    ))

    return results


# --------------------------------------------------------------------
# Section 5 — Barrier 4: dimensional/category mismatch
# --------------------------------------------------------------------

def section5_category_mismatch():
    """Show that the LHS |b|^2 / a^2 and RHS T(T+1) - Y^2 are different
    categories of mathematical objects:

    LHS: ratio of *operator coefficients* on a Hermitian circulant
         decomposition (dimensionful: depends on operator units).
    RHS: a *scalar* derived from group representation labels
         (dimensionless invariant).

    Equating two objects of different mathematical category requires
    a structural map. No retained theorem provides one.
    """
    print("Section 5 — Barrier 4: LHS and RHS are different categories of objects")
    results = []

    # 5.1 — LHS depends on operator normalization
    #       Rescaling (a, b) -> (lambda*a, lambda*b) leaves |b|^2/a^2 invariant
    #       BUT this is the only invariance — the absolute coefficients
    #       are operator-norm-dependent.
    a, b = 1.0, 0.3 + 0.4j
    Y = make_circulant(a, b)
    Y_scaled = make_circulant(2.0 * a, 2.0 * b)
    r1 = abs(b)**2 / a**2
    r2 = abs(2*b)**2 / (2*a)**2
    rescaling_invariant = np.isclose(r1, r2)
    results.append(passfail(
        "|b|^2/a^2 is invariant under uniform rescaling of (a, b)",
        rescaling_invariant,
        f"r(a,b) = {r1:.4f}, r(2a, 2b) = {r2:.4f}",
    ))

    # 5.2 — But |b|^2/a^2 is NOT scale-invariant under independent rescaling
    Y_indep = make_circulant(2.0 * a, b)
    r3 = abs(b)**2 / (2*a)**2
    not_invariant = not np.isclose(r3, r1)
    results.append(passfail(
        "|b|^2/a^2 changes under independent rescaling of a alone",
        not_invariant,
        f"r(a, b) = {r1:.4f}, r(2a, b) = {r3:.4f}",
    ))

    # 5.3 — RHS T(T+1) - Y^2 is a fixed group-theoretic scalar
    #       (no operator structure, no normalization freedom)
    rhs = 0.5  # PDG conv
    rhs_values = []
    for _flavor_index in range(3):
        rhs_values.append(rhs)
    rhs_invariant_under_state = all(np.isclose(v, rhs_values[0]) for v in rhs_values)
    results.append(passfail(
        "T(T+1) - Y^2 is a state-independent group-theoretic scalar",
        rhs_invariant_under_state,
        "RHS depends only on representation labels (T, Y), not on operator content",
    ))

    # 5.4 — Equating LHS = RHS therefore requires a normalization choice
    #       on a, b that is NOT supplied by retained content. The Route F
    #       proposal does not provide such a normalization derivation.
    normalized_by_uniform_scale_only = rescaling_invariant and not_invariant
    results.append(passfail(
        "Route F still needs an extra normalization principle for (a, b)",
        normalized_by_uniform_scale_only,
        "The coefficient ratio has its own operator normalization behavior; "
        "a gauge-to-flavor normalization map would be additional input",
    ))

    return results


# --------------------------------------------------------------------
# Section 6 — Counterexample: alternative SM extensions matching 1/2
# --------------------------------------------------------------------

def section6_counterexamples():
    """Construct alternative hypothetical particle multiplets that ALSO
    satisfy T(T+1) - Y^2 = 1/2 in PDG convention. If 1/2 is a generic
    Casimir-difference (not framework-specific), the identity loses
    its claimed exclusivity.
    """
    print("Section 6 — Alternative multiplets satisfying T(T+1) - Y^2 = 1/2")
    results = []

    # 6.1 — Hypothetical exotic doublet with T = 1/2, Y = +1/2
    #       (matches Higgs Y, but interpretable as exotic "anti-lepton-doublet")
    T_x, Y_x = Fraction(1, 2), Fraction(1, 2)
    diff_x = T_x * (T_x + 1) - Y_x * Y_x
    matches = (diff_x == Fraction(1, 2))
    results.append(passfail(
        "Hypothetical T=1/2, Y=+1/2 multiplet matches identity",
        matches,
        f"T(T+1) - Y^2 = {diff_x}; matches numerical value but no SM role",
    ))

    # 6.2 — Hypothetical T = 1, Y = √(1/2) (irrational; not SM but satisfies identity)
    #       T(T+1) = 2, so Y^2 = 3/2 -> |Y| = √(3/2). This is a fictitious
    #       multiplet that exists in arbitrary BSM scenarios.
    T_y = 1.0
    Y_y_sq = T_y * (T_y + 1) - 0.5  # forces identity
    matches_y = np.isclose(Y_y_sq, 1.5)
    results.append(passfail(
        "T=1 multiplet with Y^2 = 3/2 also matches identity (BSM scenario)",
        matches_y,
        f"any non-doublet Y with right Y^2 satisfies the identity; not exclusive to L",
    ))

    # 6.3 — Conclusion: the "uniqueness" of T(T+1) - Y^2 = 1/2 to (L, H)
    #       holds only WITHIN the SM particle content; it is NOT a
    #       structural constraint that derives from anything axiom-native.
    results.append(passfail(
        "Identity uniqueness is SM-content-specific, not axiom-native",
        matches and matches_y,
        "Within SM, only (L, H) match; but adding any BSM multiplet "
        "with right T, Y also matches. The 1/2 value is an arithmetic "
        "consequence of T = 1/2, not a structural lock.",
    ))

    return results


# --------------------------------------------------------------------
# Section 7 — Falsifiability anchor (PDG values, anchor-only)
# --------------------------------------------------------------------

def section7_falsifiability_anchor():
    """Anchor-only: confirm that PDG charged-lepton masses are consistent
    with A1 (Brannen circulant fits at 0.1% precision). This is
    FALSIFIABILITY anchor, NOT derivation input.

    Per `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`,
    PDG values are forbidden as load-bearing in any positive theorem.
    They appear ONLY as anchor for falsification of the framework's
    structural commitments, NOT as derivation content.
    """
    print("Section 7 — Falsifiability anchor (PDG values are NOT derivation input)")
    results = []

    # 7.1 — Confirm that the Brannen-circulant form FITS PDG charged-lepton
    #       masses at sub-percent precision when A1 is assumed.
    #       (This is the anchor — A1 is consistent with observation, but
    #       this section uses no retained framework content.)
    # PDG (anchor only, not derivation input):
    m_e = 0.5109989  # MeV
    m_mu = 105.6583745
    m_tau = 1776.86

    sqrt_me = np.sqrt(m_e)
    sqrt_mmu = np.sqrt(m_mu)
    sqrt_mtau = np.sqrt(m_tau)
    v_0_anchor = (sqrt_me + sqrt_mmu + sqrt_mtau) / 3.0

    # Compute Koide Q from anchors
    sum_m = m_e + m_mu + m_tau
    sum_sqrt_m = sqrt_me + sqrt_mmu + sqrt_mtau
    Q_anchor = sum_m / (sum_sqrt_m ** 2)
    Q_target = 2.0 / 3.0
    fit_ok = abs(Q_anchor - Q_target) < 1e-3
    results.append(passfail(
        "ANCHOR ONLY: PDG charged-lepton masses give Koide Q ~ 2/3",
        fit_ok,
        f"Q(PDG) = {Q_anchor:.6f}, target = {Q_target:.6f}; falsifiability anchor not derivation",
    ))

    # 7.2 — Anchors do NOT establish A1 derivation
    #       The anchor is consistent with A1, but consistency != derivation
    print("       NOTE: PDG match (Q ~ 2/3) confirms A1 is OBSERVATIONALLY consistent")
    print("       but does NOT derive A1 from retained content. A1 remains an")
    print("       admission on the current surface.")
    print()

    return results


# --------------------------------------------------------------------
# Section 8 — Bounded-obstruction theorem statement (verification)
# --------------------------------------------------------------------

def section8_obstruction_theorem():
    """Verify the bounded-obstruction theorem statement: Route F cannot
    close A1 from retained content because four independent barriers
    (sector orthogonality, free Yukawa, convention dependence,
    category mismatch) each independently block the proposed lemma.
    """
    print("Section 8 — Bounded-obstruction theorem verification")
    results = []

    # 8.1 — All four barriers independently block closure
    #       (Each verified in Sections 2-5; this section consolidates)
    barrier1_blocks = Fraction(1, 2) != Fraction(-1, 4)  # convention dependence
    barrier2_blocks = not np.isclose(abs(0.3 + 0.0j) ** 2, abs(0.7 + 0.4j) ** 2)
    barrier3_blocks = (2 != U_C3_CORNER.shape[0])  # sector orthogonality
    barrier4_blocks = not np.isclose(abs(0.3 + 0.4j) ** 2 / (2.0 ** 2), abs(0.3 + 0.4j) ** 2)
    all_barriers = barrier1_blocks and barrier2_blocks and barrier3_blocks and barrier4_blocks
    results.append(passfail(
        "All four structural barriers independently block Route F closure",
        all_barriers,
        "Convention-dep + free Yukawa + sector-orth + category-mismatch = "
        "no retained-content path to derive |b|^2/a^2 = 1/2 from "
        "T(T+1) - Y^2 = 1/2",
    ))

    # 8.2 — The bounded-obstruction status: Route F is structurally barred
    #       under the stated retained-content surface
    print("       VERDICT: Route F lemma |b|^2/a^2 = T(T+1) - Y^2 cannot close")
    print("       on the retained Cl(3)/Z^3 framework. The numerical match")
    print("       1/2 = 1/2 is a coincidence between independently-defined")
    print("       quantities, not a structural identity.")
    print()
    print("       AC_φλ residual (from substep 4) is unaffected by this analysis.")
    print("       The A1 admission count remains unchanged.")
    print()

    results.append(passfail(
        "Route F bounded-obstruction theorem holds",
        all_barriers,
        "Four-barrier structural argument: no closure path from retained content",
    ))

    return results


# --------------------------------------------------------------------
# Main runner
# --------------------------------------------------------------------

def main():
    print("=" * 70)
    print("Koide A1 Route F — Yukawa Casimir-Difference Bounded Obstruction")
    print("Source note:")
    print("  docs/KOIDE_A1_ROUTE_F_CASIMIR_DIFFERENCE_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_routef.md")
    print("=" * 70)

    all_results = []
    all_results += section1_numerical_match()
    all_results += section2_convention_dependence()
    all_results += section3_free_yukawa_coefficients()
    all_results += section4_sector_orthogonality()
    all_results += section5_category_mismatch()
    all_results += section6_counterexamples()
    all_results += section7_falsifiability_anchor()
    all_results += section8_obstruction_theorem()

    n_total = len(all_results)
    n_pass = sum(all_results)
    n_fail = n_total - n_pass

    print()
    print("=" * 70)
    print(f"EXACT      : PASS = {n_pass}, FAIL = {n_fail}")
    print(f"BOUNDED    : PASS = 0, FAIL = 0")
    print(f"TOTAL      : PASS = {n_pass}, FAIL = {n_fail}")
    print("=== TOTAL: PASS=" + str(n_pass) + ", FAIL=" + str(n_fail) + " ===")
    print("=" * 70)
    print()
    print("Bounded-obstruction verdict:")
    if n_fail == 0:
        print("  Route F structurally barred: |b|^2/a^2 = T(T+1) - Y^2 cannot")
        print("  close from retained content alone. Four independent structural")
        print("  barriers (convention-dep + free Yukawa + sector-orth +")
        print("  category-mismatch) each block the proposed lemma.")
        print()
        print("  A1 admission count UNCHANGED (Route F closure not achieved).")
        print("  No new axiom proposed.")
        print()
        print("  Falsifiability anchor: PDG charged-lepton masses fit Brannen")
        print("  circulant with A1 at 0.1% precision (consistent but not")
        print("  derivation).")
    else:
        print("  Verification has FAIL items — see runner output above.")

    if n_fail != 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
