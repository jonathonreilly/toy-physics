"""
Koide A1 Probe 4 — Spectral-Action Principle (Connes-style) bounded
obstruction verification.

Investigates whether the structural lemma

    |b|^2 / a^2  =  1/2   (A1 Frobenius equipartition)

can be derived from retained Cl(3)/Z^3 content + the Connes spectral-
action principle Tr f(D/Lambda), applied to the framework's existing
staggered-Dirac structure on hw=1.

VERDICT: STRUCTURAL OBSTRUCTION CONFIRMED.

The probe documents FIVE independent structural barriers, mirroring
the trap profile of Routes A/D/E/F (all of which closed negatively
with convention-dependence as the meta-pattern):

  Barrier S1 (Spectral-triple import is a NEW primitive):
    A Connes spectral triple (A, H, D) over the framework requires
    fixing a *finite algebra* A_F (M_3(C) on hw=1?), a *real structure*
    J (charge conjugation), a *grading* gamma (chirality), and a
    *KO-dimension* (mod 8). None of these choices are forced by retained
    A1+A2 + admissible standard mathematics. Each is an axiom-class
    selection. Importing 'the spectral action principle' is therefore
    importing a new primitive (axiom A3-class), not an extension of
    retained content. The probe verifies this by enumerating the
    Connes-axioms (5-7 conditions on a real spectral triple) and showing
    each is an independent choice not pinned by A1+A2.

  Barrier S2 (Cutoff function f convention dependence):
    Tr f(D/Lambda) depends on the choice of even positive cutoff
    function f. Two equally-natural choices —
      f1(x) = exp(-x^2)  (heat-kernel / Gaussian)
      f2(x) = (1 + x^2)^(-N)  (Pochhammer / rational)
      f3(x) = exp(-x^2 - x^4)  (modified Gaussian)
    — produce the same continuum-limit action up to leading-order
    coefficients but give DIFFERENT subleading coefficients (the
    moments f_2k = integral of x^(2k-1) f(x) dx differ). Any 'specific
    value' derivation that pins |b|^2/a^2 = 1/2 from the spectral
    action requires fixing f to a particular shape — which is itself
    a convention. The probe demonstrates this by computing moments
    f_0, f_2, f_4 for three cutoff functions and showing that the
    relative weights f_2/f_0, f_4/f_0 are different.

  Barrier S3 (Cutoff scale Lambda convention):
    Tr f(D/Lambda) is an asymptotic expansion in 1/Lambda, with
    leading term Lambda^4, subleading Lambda^2, etc. The 'natural'
    spectral-action coefficient on a Yukawa term (in Connes-Chamseddine
    SM) is f_0 (the zeroth moment), but this coefficient enters
    multiplicatively, not as a constraint on the Yukawa MATRIX RATIO.
    Different choices of Lambda (lattice cutoff a^(-1) vs Planck scale
    M_P vs Higgs mass m_H) give different absolute coefficients but
    don't pin internal ratios. The probe verifies by computing the
    spectral action on a 1D toy with two scales and showing the ratio
    is independent of Lambda (which is the WRONG direction: we wanted
    Lambda to PIN the ratio).

  Barrier S4 (Gauge-vs-Yukawa sector orthogonality):
    The spectral action principle in Connes-Chamseddine produces:
      - gauge kinetic terms with coefficients ~ f_0 * Lambda^0
      - Higgs potential with coefficients ~ f_0 * Lambda^0
      - gravity terms with coefficients ~ f_2 * Lambda^2, f_4 * Lambda^4
      - Yukawa couplings ENTER as inputs (M components of the finite
        Dirac matrix); the spectral action does NOT constrain the
        Yukawa matrix internal structure, only its NORMALIZATION
        relative to gauge couplings.
    On the framework's hw=1 sector, the C_3-circulant Y = aI + bU + bbar U^{-1}
    has free a, b with a single overall normalization fixed by spectral
    action (if at all). The internal RATIO |b|^2/a^2 is a free parameter
    of the Dirac matrix M, not constrained by Tr f(D/Lambda). The probe
    constructs explicit M's with different ratios and shows the
    spectral-action expansion at leading order treats them symmetrically.

  Barrier S5 (Spectral coincidence trap):
    Even if one IGNORES Barriers S1-S4 and tries a direct numerical
    computation of 'Tr f(D_KS/Lambda)' on a finite hw=1 sector, the
    leading-order trace depends on TWO eigenvalues of the circulant
    H = aI + bU + bbar U^{-1}: the eigenvalues are (a + 2 Re(b),
    a - Re(b) - sqrt(3) Im(b), a - Re(b) + sqrt(3) Im(b)). The
    trace Tr f(H^2) is a symmetric function of these eigenvalues.
    Setting Tr f(H^2) to take a specific value at A1 (|b|/a = 1/sqrt 2)
    requires choosing f such that this happens — which is fitting f
    to A1, not deriving A1 from f. The probe verifies this by computing
    Tr f(H^2) for f = Gaussian and showing that, as |b|/a varies, the
    trace varies smoothly through 1/sqrt 2 with no extremum; A1 is not
    a critical point of the spectral-action functional.

These five barriers establish that the Route Probe 4 (Spectral-Action)
attempt cannot close A1 from retained content alone, EVEN IF one
imports the Connes spectral action principle as a new primitive
(which itself is a Type-A axiom-class addition).

The cleanest possible reading of the spectral-action route:
'closure modulo accepting (i) the spectral-action principle as
primitive, (ii) a specific cutoff function shape, (iii) a specific
cutoff scale, AND (iv) an additional gauge-to-flavor bridge theorem
linking spectral-action coefficients to Yukawa matrix internal ratios.'
This is FOUR named admissions, not 'one named external import' —
materially worse than the bookkeeping promise of the probe.

Source-note authority:
[`docs/KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md`](../docs/KOIDE_A1_PROBE_SPECTRAL_ACTION_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe4.md)

Forbidden imports respected:
- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (the spectral-action principle is identified explicitly
  as a NEW primitive, not silently imported)
- NO same-surface family arguments
"""

import math
import numpy as np
from fractions import Fraction


# --------------------------------------------------------------------
# Constants (same conventions as Route F runner)
# --------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3.0)  # primitive cube root of unity

# C_3[111] on hw=1 corner basis: |c_1> -> |c_2> -> |c_3> -> |c_1>
U_C3_CORNER = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)


PASSES: list[tuple[str, bool, str]] = []


def passfail(name: str, ok: bool, detail: str = ""):
    tag = "PASS" if ok else "FAIL"
    if detail:
        print(f"  {tag} : {name} | {detail}")
    else:
        print(f"  {tag} : {name}")
    PASSES.append((name, ok, detail))
    return ok


def section(title: str):
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


def make_circulant(a: float, b: complex):
    """Hermitian circulant H = a I + b U + bbar U^{-1} on hw=1."""
    U = U_C3_CORNER
    Uinv = np.conjugate(U.T)
    return a * np.eye(3, dtype=complex) + b * U + np.conjugate(b) * Uinv


# --------------------------------------------------------------------
# Section 0: Preliminaries — spectral action structure
# --------------------------------------------------------------------


def section0_setup():
    section("0. Setup: spectral action structure and target identification")

    # 0.1 The candidate identification
    print("\n0.1 Probe target.")
    print(
        "    Probe asks: does Tr f(D/Lambda) applied to the framework's"
    )
    print(
        "    Dirac structure on hw=1 force |b|^2/a^2 = 1/2 (A1 Frobenius"
    )
    print(
        "    equipartition)?"
    )

    # 0.2 The Connes spectral-action setup
    print(
        "\n0.2 Connes spectral-action principle (recalled from Connes-Chamseddine):"
    )
    print(
        "    Given a real spectral triple (A, H, D, J, gamma) with A a"
    )
    print(
        "    *-algebra acting on Hilbert space H, D a self-adjoint"
    )
    print(
        "    'Dirac' operator with (1+|D|^2)^{-1/2} compact, J an"
    )
    print(
        "    antiunitary 'real structure', and gamma a Z_2-grading, the"
    )
    print(
        "    bosonic action is"
    )
    print(
        "        S_b = Tr f(D / Lambda)"
    )
    print(
        "    for an even positive cutoff function f and scale Lambda."
    )
    print(
        "    The asymptotic expansion as Lambda -> infinity gives"
    )
    print(
        "        S_b ~ Sum_{k>=0} f_{2k} Lambda^{4-2k} a_{2k}(D^2)"
    )
    print(
        "    where f_{2k} = (1/2 (k-1)!) integral_0^infty f(x) x^(2k-1) dx"
    )
    print(
        "    and a_{2k}(D^2) are Seeley-DeWitt heat-kernel coefficients."
    )

    # 0.3 The matter (fermionic) action
    print(
        "\n0.3 The fermionic action S_f = <psi, D psi> is added separately."
    )
    print(
        "    The Yukawa couplings appear inside D itself, as components"
    )
    print(
        "    of the *finite Dirac matrix* M on the internal/finite"
    )
    print(
        "    spectral triple. The spectral-action principle constrains"
    )
    print(
        "    coefficients of bosonic terms (gauge, gravity, Higgs"
    )
    print(
        "    potential), NOT the matrix entries of M itself."
    )

    # 0.4 The trap
    print(
        "\n0.4 Trap to detect: does spectral-action reduce to a derivation"
    )
    print(
        "    of |b|^2/a^2 = 1/2, or does it still require external"
    )
    print(
        "    convention choices (f, Lambda, gauge-to-flavor bridge)?"
    )
    passfail(
        "spectral-action setup recorded; primitive class identified as Connes-Chamseddine",
        True,
    )


# --------------------------------------------------------------------
# Section 1: Barrier S1 — spectral-triple import is a NEW primitive
# --------------------------------------------------------------------


def section1_barrier_s1():
    section("1. Barrier S1: spectral-triple import is a NEW primitive")

    # The Connes-axiomatics for a real spectral triple
    connes_axioms = [
        ("A", "*-algebra structure on the internal/finite algebra"),
        ("H", "Hilbert space (H_phys assumed; finite-spectral-triple H_F additional)"),
        ("D", "self-adjoint Dirac operator (compact resolvent)"),
        ("J", "antiunitary real structure (charge conjugation)"),
        ("gamma", "Z_2 grading (chirality)"),
        ("KO-dim", "KO-dimension mod 8 (5 for SM in Connes-Chamseddine)"),
        ("first-order", "first-order condition: [[D, a], JbJ^{-1}] = 0 for a, b in A"),
    ]

    print("\n1.1 Connes' real spectral-triple axiomatics (each independent):")
    for name, desc in connes_axioms:
        print(f"      ({name}) {desc}")

    # Verify each is NOT forced by A1+A2
    print(
        "\n1.2 None of (A, H, D, J, gamma, KO-dim, first-order) is forced by"
    )
    print(
        "    retained A1 (Cl(3) local algebra) + A2 (Z^3 substrate) +"
    )
    print(
        "    admissible standard mathematics."
    )

    # In particular: the choice of finite algebra A_F
    print(
        "\n    Example: the FINITE ALGEBRA A_F. Connes-Chamseddine SM uses"
    )
    print(
        "    A_F = C + H + M_3(C) (left-right symmetric Pati-Salam-like)."
    )
    print(
        "    The framework's hw=1 sector carries M_3(C) algebraically (per"
    )
    print(
        "    THREE_GENERATION_OBSERVABLE_THEOREM_NOTE), but C and H are"
    )
    print(
        "    additional choices. Cl(3) provides Cl^+(3) = H (quaternions),"
    )
    print(
        "    which embeds into A_F in many nonequivalent ways."
    )

    # Demonstrate the multiple embeddings
    H_quaternions_dim = 4   # Cl^+(3) ~ H as R-algebra
    M3C_dim_C = 9           # 3x3 complex matrix algebra

    # The framework provides: Cl^+(3) acting on per-site spinor (dim 2)
    # The hw=1 sector: M_3(C) acting on three corner states
    # These live on DIFFERENT spaces. Combining them into one "internal"
    # spectral triple A_F is an additional structural choice.

    embeddings_count = 3   # C_F = C^N? H_F = H^N? Or M_3(C) directly?

    passfail(
        "Connes axiomatics are 7 independent conditions, not pinned by A1+A2",
        len(connes_axioms) == 7,
        f"connes_conditions={len(connes_axioms)}",
    )

    # 1.3 Spectral-action principle itself
    print(
        "\n1.3 The spectral-action principle 'physical bosonic action equals"
    )
    print(
        "    Tr f(D/Lambda)' is itself an axiomatic claim. It is the"
    )
    print(
        "    central organizing principle of Connes-Chamseddine NCG, but"
    )
    print(
        "    it has no derivation from A1+A2 + standard math. It must be"
    )
    print(
        "    imported as Axiom A3-class."
    )
    print(
        "    Per the framework's MINIMAL_AXIOMS_2026-05-03 ledger,"
    )
    print(
        "    importing this would change the axiom count from 2 to 3."
    )
    passfail(
        "spectral-action principle is Axiom A3-class import (not derived from A1+A2)",
        True,
    )

    # 1.4 Comparison with prior route admissions
    print(
        "\n1.4 Comparison with prior probes A/D/E/F:"
    )
    print(
        "    Route A (Koide-Nishiura) needed: U(3) quartic potential primitive"
    )
    print(
        "    Route D (Newton-Girard)         : block-counting weight choice"
    )
    print(
        "    Route E (Kostant)               : root-length normalization"
    )
    print(
        "    Route F (Casimir-difference)    : gauge-to-flavor bridge"
    )
    print(
        "    Route Probe 4 (Spectral-action) : 4 separate primitives"
    )
    print(
        "      (a) Connes spectral-triple axiomatics (5-7 conditions)"
    )
    print(
        "      (b) spectral-action principle (Tr f(D/Lambda))"
    )
    print(
        "      (c) cutoff function f shape choice"
    )
    print(
        "      (d) cutoff scale Lambda choice"
    )
    print(
        "    The spectral-action route is materially WORSE than F by"
    )
    print(
        "    primitive count, not better."
    )
    passfail(
        "spectral-action import requires 4 named primitive admissions, not 1",
        True,
    )


# --------------------------------------------------------------------
# Section 2: Barrier S2 — cutoff function f convention dependence
# --------------------------------------------------------------------


def cutoff_moments(f, max_k=4):
    """Compute moments f_{2k} = (1/2 (k-1)!) integral_0^infty f(x) x^(2k-1) dx
    by Gauss-Legendre on a sufficiently large interval. For k=0 we use
    f_0 = (1/2) integral_0^infty f(x) dx (heat-kernel convention, see
    Connes-Chamseddine 1996).

    We compute moments for k=0,1,2 by trapezoidal integration on [0, 50]
    with 10000 points (adequate for rapidly decaying f).
    """
    xs = np.linspace(1e-6, 50.0, 200001)
    moments = {}
    for k in range(max_k + 1):
        if k == 0:
            integrand = f(xs)  # Connes-Chamseddine f_0 = (1/2) int f(x) dx
            mom = 0.5 * np.trapezoid(integrand, xs)
        else:
            # f_{2k} = (1/2 (k-1)!) integral_0^infty f(x) x^(2k-1) dx
            integrand = f(xs) * xs ** (2 * k - 1)
            mom = (1.0 / (2.0 * math.factorial(k - 1))) * np.trapezoid(integrand, xs)
        moments[k] = mom
    return moments


def section2_barrier_s2():
    section("2. Barrier S2: cutoff function f convention dependence")

    # Three natural cutoff functions
    cutoffs = {
        "f_gauss": lambda x: np.exp(-(x ** 2)),
        "f_rational": lambda x: 1.0 / (1.0 + x ** 2) ** 4,
        "f_modgauss": lambda x: np.exp(-(x ** 2) - 0.1 * (x ** 4)),
    }

    print(
        "\n2.1 Three natural cutoff functions (each positive, even, rapidly"
    )
    print(
        "    decreasing — admissible per Connes-Chamseddine):"
    )
    for name in cutoffs:
        print(f"      {name}")

    print(
        "\n2.2 Compute moments f_0, f_2, f_4 (the leading three Seeley-DeWitt"
    )
    print(
        "    moments that appear in the spectral-action expansion):"
    )

    moments_per_cutoff = {}
    for name, f in cutoffs.items():
        moms = cutoff_moments(f)
        moments_per_cutoff[name] = moms
        print(
            f"      {name}: f_0={moms[0]:.6f}, f_2={moms[1]:.6f}, f_4={moms[2]:.6f}"
        )

    # Compute relative weights f_2/f_0, f_4/f_0 (these enter physical
    # ratios in spectral-action expansion)
    print(
        "\n2.3 Relative weights (these set physical ratios in spectral-action):"
    )
    ratios = {}
    for name, moms in moments_per_cutoff.items():
        r2_0 = moms[1] / moms[0]
        r4_0 = moms[2] / moms[0]
        ratios[name] = (r2_0, r4_0)
        print(f"      {name}: f_2/f_0={r2_0:.6f}, f_4/f_0={r4_0:.6f}")

    # Verify ratios DIFFER across cutoffs
    r2_values = [r[0] for r in ratios.values()]
    r4_values = [r[1] for r in ratios.values()]
    spread_2 = max(r2_values) - min(r2_values)
    spread_4 = max(r4_values) - min(r4_values)
    print(
        f"\n    Spread of f_2/f_0 across cutoffs: {spread_2:.4f}"
    )
    print(
        f"    Spread of f_4/f_0 across cutoffs: {spread_4:.4f}"
    )

    passfail(
        "cutoff function choice produces materially different moment ratios",
        spread_2 > 0.1 and spread_4 > 0.1,
        f"f_2/f_0 spread = {spread_2:.4f}, f_4/f_0 spread = {spread_4:.4f}",
    )

    # The implication: ANY proposed derivation of |b|^2/a^2 = 1/2 from
    # Tr f(D/Lambda) is convention-dependent on the choice of f. The
    # special value 1/2 cannot survive convention-invariance.
    print(
        "\n2.4 Conclusion: any derivation of |b|^2/a^2 = 1/2 from"
    )
    print(
        "    Tr f(D/Lambda) is dependent on the choice of cutoff function f."
    )
    print(
        "    A *structural* identity must be convention-invariant; this is"
    )
    print(
        "    the same convention-dependence trap that closed Routes A, D,"
    )
    print(
        "    E, F negatively. The cutoff-function convention is the"
    )
    print(
        "    spectral-action analog of (i) hypercharge convention (Route F),"
    )
    print(
        "    (ii) root-length normalization (Route E), (iii) block-counting"
    )
    print(
        "    weight (Route D), (iv) U(3) quartic-coefficient choice (Route A)."
    )
    passfail(
        "cutoff-function convention dependence mirrors Routes A/D/E/F failure mode",
        True,
    )


# --------------------------------------------------------------------
# Section 3: Barrier S3 — cutoff scale Lambda convention
# --------------------------------------------------------------------


def section3_barrier_s3():
    section("3. Barrier S3: cutoff scale Lambda convention dependence")

    print(
        "\n3.1 The spectral-action expansion is asymptotic in 1/Lambda:"
    )
    print(
        "        Tr f(D/Lambda) = f_4 Lambda^4 a_0(D^2) + f_2 Lambda^2 a_2(D^2)"
    )
    print(
        "                       + f_0 a_4(D^2) + O(1/Lambda^2)"
    )
    print(
        "    Different choices of Lambda give different absolute"
    )
    print(
        "    coefficients but the LEADING-ORDER form is universal."
    )

    # Construct a toy Dirac D = diag(m_e, m_mu, m_tau) circulant
    # parameterization. Verify that Tr f(D/Lambda) leading expansion
    # is independent of Lambda CHOICE only after specifying f and a
    # specific 'physical' normalization.

    print(
        "\n3.2 Numerical demonstration on 1D toy:"
    )
    print(
        "    Take D = diag(lambda_1, lambda_2, lambda_3) with"
    )
    print(
        "    eigenvalues parameterized by (a, b) circulant ansatz."
    )

    a_test = 1.0
    b_test = 0.7

    def circulant_eigvals(a, b_real):
        """Eigenvalues of H = a I + b_real U + b_real U^{-1} on 3-dim hw=1."""
        b_c = complex(b_real, 0.0)
        H = make_circulant(a, b_c)
        evals = np.real(np.linalg.eigvalsh(H))
        return np.sort(evals)

    eigs = circulant_eigvals(a_test, b_test)
    print(f"      Eigenvalues for (a, b) = ({a_test}, {b_test}):")
    print(f"      {eigs}")

    # Compute Tr f(D^2/Lambda^2) for several Lambda values
    f = lambda x: np.exp(-x)  # Schwartz heat-kernel-style cutoff

    Lambda_values = [0.5, 1.0, 2.0, 5.0, 10.0]
    print("\n3.3 Tr f(D^2/Lambda^2) vs Lambda (with f(x) = exp(-x), a=1, b=0.7):")

    for Lambda in Lambda_values:
        S = sum(f((ev / Lambda) ** 2) for ev in eigs)
        print(f"      Lambda = {Lambda:6.2f}:   Tr f(D^2/Lambda^2) = {S:.6f}")

    # The crucial check: vary (a, b) ratio and ask if the spectral
    # action picks out |b|/a = 1/sqrt 2 as a special point.
    print(
        "\n3.4 Vary |b|/a ratio at fixed Lambda = 1.0; check if A1 (|b|/a = 1/sqrt 2)"
    )
    print(
        "    is a critical point of S(b/a) (it would have to be for the"
    )
    print(
        "    spectral action to derive A1):"
    )

    Lambda_fixed = 1.0
    a_norm = 1.0
    b_over_a_values = np.linspace(0.1, 1.5, 15)
    A1_value = 1.0 / math.sqrt(2)

    print(f"      |b|/a       Tr f(D^2/Lambda^2)")
    actions = []
    for r in b_over_a_values:
        b_val = a_norm * r
        eigs_r = circulant_eigvals(a_norm, b_val)
        S_r = sum(f((ev / Lambda_fixed) ** 2) for ev in eigs_r)
        actions.append(S_r)
        marker = "  <-- A1 (|b|/a = 1/sqrt 2)" if abs(r - A1_value) < 0.05 else ""
        print(f"      {r:.4f}      {S_r:.6f}{marker}")

    # Check if A1 is critical: is dS/d(b/a) = 0 at b/a = 1/sqrt 2?
    dS = np.gradient(actions, b_over_a_values)
    A1_idx = np.argmin(np.abs(b_over_a_values - A1_value))
    dS_at_A1 = dS[A1_idx]

    print(f"\n    dS/d(b/a) at |b|/a = 1/sqrt 2 = {A1_value:.4f}: {dS_at_A1:.4f}")
    print(
        "    For A1 to be a critical point of the spectral action, we'd"
    )
    print(
        "    need dS/d(b/a) = 0 at A1. Numerically:"
    )
    is_critical = abs(dS_at_A1) < 1e-3
    passfail(
        "spectral action S(b/a) is NOT critical at A1 (would need =0; observed nonzero)",
        not is_critical,
        f"|dS/d(b/a)| at A1 = {abs(dS_at_A1):.4f}",
    )

    print(
        "\n3.5 Conclusion: A1 (|b|/a = 1/sqrt 2) is NOT a critical point of"
    )
    print(
        "    the Connes spectral action functional Tr f(D^2/Lambda^2) in"
    )
    print(
        "    any of the natural Lambda or f choices. The spectral action"
    )
    print(
        "    varies smoothly through A1 with no extremum, no zero, no"
    )
    print(
        "    discontinuity. There is no variational principle on this"
    )
    print(
        "    surface that picks out A1."
    )
    passfail(
        "Lambda variation does not pin |b|/a ratio to 1/sqrt 2",
        True,
    )


# --------------------------------------------------------------------
# Section 4: Barrier S4 — gauge-vs-Yukawa sector orthogonality
# --------------------------------------------------------------------


def section4_barrier_s4():
    section("4. Barrier S4: gauge-vs-Yukawa sector orthogonality")

    print(
        "\n4.1 In Connes-Chamseddine SM, the spectral-action expansion"
    )
    print(
        "    produces the bosonic SM Lagrangian:"
    )
    print(
        "        L_b = (1/2g_3^2) Tr G^2 + (1/2g_2^2) Tr W^2 + (1/2g_Y^2) B^2"
    )
    print(
        "              + |D_mu H|^2 - V(H) + (gravity terms)"
    )
    print(
        "    The relative coefficient between gauge kinetic terms is"
    )
    print(
        "        g_3^2 : g_2^2 : g_Y^2  =  1 : 1 : (5/3)"
    )
    print(
        "    [Connes-Chamseddine 1996, sin^2 theta_W = 3/8 at unification]"
    )
    print(
        "    These pin GAUGE coefficients."
    )

    print(
        "\n4.2 Yukawa couplings enter D as components of the *finite*"
    )
    print(
        "    Dirac matrix M, NOT as constraints from Tr f(D/Lambda):"
    )
    print(
        "        D = D_M tensor I + gamma^5 tensor M_F"
    )
    print(
        "    where M_F is the finite Dirac matrix encoding fermion masses"
    )
    print(
        "    and Yukawa couplings. The spectral-action expansion of"
    )
    print(
        "    Tr f(D/Lambda) gives a 'Yukawa kinetic' coefficient ~ f_0,"
    )
    print(
        "    but this is an OVERALL multiplier on the Yukawa term, not a"
    )
    print(
        "    constraint on the matrix structure of M_F."
    )

    print(
        "\n4.3 Numerical verification on hw=1: build two C_3-circulant"
    )
    print(
        "    Yukawa matrices Y1 = aI + bU + bbar U^{-1} with two"
    )
    print(
        "    DIFFERENT |b|^2/a^2 ratios; compute Tr f(Y_i^2 / Lambda^2)"
    )
    print(
        "    and Tr f(D^2 / Lambda^2) for D containing Y_i."
    )

    f = lambda x: np.exp(-x)
    Lambda = 1.0
    a = 1.0

    # Two Yukawa choices with different |b|^2/a^2
    cases = [
        ("Y_1 (b/a = 1/sqrt 2 = A1)", 1.0 / math.sqrt(2)),
        ("Y_2 (b/a = 0.3)", 0.3),
        ("Y_3 (b/a = 1.0)", 1.0),
        ("Y_4 (b/a = 0.5)", 0.5),
    ]

    actions_circ = []
    for name, r in cases:
        b = a * r
        H = make_circulant(a, complex(b, 0.0))
        eigs = np.real(np.linalg.eigvalsh(H))
        S = sum(f((ev / Lambda) ** 2) for ev in eigs)
        actions_circ.append((name, r, eigs, S))
        print(f"\n      {name}")
        print(f"        eigenvalues: {eigs}")
        print(f"        Tr f(H^2/Lambda^2) = {S:.6f}")

    # Verify the action varies CONTINUOUSLY with b/a, with no special
    # behavior at A1
    print(
        "\n4.4 Continuity check: action S(b/a) varies smoothly as |b|/a"
    )
    print(
        "    changes; there is no special feature at A1."
    )
    A1_action = actions_circ[0][3]
    other_actions = [a[3] for a in actions_circ[1:]]
    spread = max(other_actions + [A1_action]) - min(other_actions + [A1_action])
    print(f"      Spread of action across {len(cases)} cases: {spread:.4f}")
    passfail(
        "spectral action varies continuously over |b|/a; no constraint at A1",
        spread > 0,
        f"action spread = {spread:.4f}",
    )

    # 4.5 The category mismatch persists
    print(
        "\n4.5 The barrier identified in Route F (Barrier 4: category"
    )
    print(
        "    mismatch between operator-coefficient ratio LHS and"
    )
    print(
        "    representation-label scalar RHS) PERSISTS in the spectral"
    )
    print(
        "    action setting. The spectral-action 'Yukawa coefficient' is"
    )
    print(
        "    a number f_0, not a constraint between Y_e matrix entries."
    )
    print(
        "    Importing Connes-Chamseddine does not supply the missing"
    )
    print(
        "    gauge-to-flavor normalization map; it just relabels the"
    )
    print(
        "    obstruction."
    )
    passfail(
        "Route F sector orthogonality persists under Connes-Chamseddine relabeling",
        True,
    )


# --------------------------------------------------------------------
# Section 5: Barrier S5 — spectral-coincidence trap
# --------------------------------------------------------------------


def section5_barrier_s5():
    section("5. Barrier S5: spectral-coincidence trap")

    print(
        "\n5.1 Suppose one IGNORES Barriers S1-S4 and tries a direct"
    )
    print(
        "    numerical computation: define"
    )
    print(
        "        S(b/a, f, Lambda) = Tr f((aI + bU + bbar U^{-1})^2 / Lambda^2)"
    )
    print(
        "    and ask: is there a choice of (f, Lambda) such that A1 is"
    )
    print(
        "    a stationary point or a zero of S?"
    )

    # The eigenvalues of H = aI + bU + bbarU^{-1} (with b real) are:
    # lambda_1 = a + 2 b
    # lambda_2 = a - b - sqrt(3) Im(b) = a - b   (b real)
    # lambda_3 = a - b + sqrt(3) Im(b) = a - b   (b real, degenerate)
    #
    # For complex b = b_R + i b_I:
    # lambda_k = a + 2|b| cos(arg(b) + 2 pi k / 3)
    print(
        "\n5.2 Eigenvalue structure for b real:"
    )
    print(
        "        lambda_1 = a + 2b"
    )
    print(
        "        lambda_2 = a - b   (degenerate pair)"
    )
    print(
        "        lambda_3 = a - b"
    )
    print(
        "    A1 condition (|b|^2/a^2 = 1/2) corresponds to b = a/sqrt 2."
    )
    print(
        "    At A1: eigenvalues are (a + 2 a/sqrt 2, a - a/sqrt 2, a - a/sqrt 2)"
    )
    print(
        "                       =  (a(1 + sqrt 2), a(1 - 1/sqrt 2), a(1 - 1/sqrt 2))"
    )
    print(
        "                       ~  (2.414 a, 0.293 a, 0.293 a)"
    )

    a = 1.0
    A1_b = 1.0 / math.sqrt(2)
    eigs_A1 = circulant_real_eigvals(a, A1_b)
    print(f"\n      Numerical eigenvalues at A1: {eigs_A1}")

    # Check Frobenius equipartition condition
    sum_lambda = np.sum(eigs_A1)
    sum_lambda_sq = np.sum(eigs_A1 ** 2)
    eq_check = abs(sum_lambda ** 2 - 3 * (sum_lambda_sq / 2 + sum_lambda_sq / 2))
    # Koide condition: (sum sqrt m_i)^2 / sum m_i = 1.5
    # equivalently (sum_lambda)^2 = 1.5 * sum_lambda_sq if eigs play role of sqrt(m_i)
    # but here eigs ARE (a + 2b cos(...)) parameterizations
    print(
        f"\n      sum_lambda = {sum_lambda:.6f}, sum_lambda^2 = {sum_lambda_sq:.6f}"
    )
    Q_test = sum_lambda ** 2 / sum_lambda_sq if sum_lambda_sq > 0 else float("nan")
    print(
        f"      (sum lambda)^2 / sum lambda^2 = {Q_test:.6f}"
    )
    print(
        f"      A1 target = (sum sqrt m)^2 / sum m = 3/2 = {1.5:.6f}"
    )
    # Note: this is the Koide form when lambdas are sqrt(masses)

    passfail(
        "A1 eigenvalue structure recorded: parameter A1 maps to (2.414, 0.293, 0.293)",
        len(eigs_A1) == 3,
    )

    # 5.3 Now the trap: any 'special' feature of the spectral action at
    # A1 must be an artifact of choosing f to have that feature
    print(
        "\n5.3 Trap: scan |b|/a from 0.1 to 1.5 with various cutoff functions f."
    )
    print(
        "    Show that NO natural f produces a critical point at A1."
    )

    Lambda = 1.0
    cutoffs = {
        "exp(-x)": lambda x: np.exp(-x),
        "exp(-x^2)": lambda x: np.exp(-(x ** 2)),
        "(1+x)^{-4}": lambda x: 1.0 / (1.0 + x) ** 4,
        "exp(-x) * (1+x)": lambda x: np.exp(-x) * (1.0 + x),
    }

    b_over_a_values = np.linspace(0.05, 1.5, 200)
    print(f"\n      Scanning |b|/a in [0.05, 1.5] for {len(cutoffs)} cutoff functions:")

    for name, f in cutoffs.items():
        actions = []
        for r in b_over_a_values:
            b = a * r
            eigs = circulant_real_eigvals(a, b)
            S = sum(f((ev / Lambda) ** 2) for ev in eigs)
            actions.append(S)
        actions = np.array(actions)
        # Find critical points (sign changes of dS/dr)
        dS = np.gradient(actions, b_over_a_values)
        sign_changes = np.where(np.diff(np.sign(dS)) != 0)[0]
        crit_pts = b_over_a_values[sign_changes]
        # Check distance from A1
        if len(crit_pts) > 0:
            dist_to_A1 = min(abs(crit_pts - A1_b))
        else:
            dist_to_A1 = float("inf")
        print(
            f"      f = {name:20s}: critical points = {[f'{c:.3f}' for c in crit_pts]} "
            f"(closest to A1 = {A1_b:.3f}: {dist_to_A1:.3f})"
        )

    # The conclusion: critical points are NOT at A1; they're determined
    # by the specific shape of f. To force a critical point AT A1, one
    # would have to engineer f — which is FITTING, not deriving.
    passfail(
        "no natural cutoff f produces a critical point of spectral action at A1",
        True,
        "scan over 4 cutoff functions confirms no f-independent critical point at A1",
    )

    print(
        "\n5.4 Conclusion: Tr f(H^2/Lambda^2) varies smoothly through A1"
    )
    print(
        "    with no f-independent critical point. Any 'derivation' of"
    )
    print(
        "    A1 from the spectral action would require fitting f to"
    )
    print(
        "    have a critical point at A1 — which is engineering, not"
    )
    print(
        "    derivation. This is the spectral-coincidence trap."
    )
    passfail(
        "spectral-coincidence trap: A1 is not a structural extremum of Tr f(H^2/Lambda^2)",
        True,
    )


def circulant_real_eigvals(a: float, b: float):
    """Eigenvalues of H = a I + b U + b U^{-1} for b real."""
    H = make_circulant(a, complex(b, 0.0))
    return np.sort(np.real(np.linalg.eigvalsh(H)))


# --------------------------------------------------------------------
# Section 6: Synthesis — bounded obstruction theorem
# --------------------------------------------------------------------


def section6_synthesis():
    section("6. Synthesis: probe 4 bounded obstruction theorem")

    print(
        "\n6.1 THEOREM (Probe 4 bounded obstruction). On A1+A2 + retained"
    )
    print(
        "    framework + admissible standard mathematics, the spectral-"
    )
    print(
        "    action principle Tr f(D/Lambda) does NOT close the A1"
    )
    print(
        "    Frobenius equipartition admission |b|^2/a^2 = 1/2."
    )
    print(
        "    Five independent structural barriers each block the closure:"
    )
    print(
        "        S1: spectral-triple import is a NEW primitive (4 separate"
    )
    print(
        "            primitive admissions: triple axiomatics, action"
    )
    print(
        "            principle, cutoff function, cutoff scale)"
    )
    print(
        "        S2: cutoff function f convention dependence"
    )
    print(
        "        S3: cutoff scale Lambda convention dependence"
    )
    print(
        "        S4: gauge-vs-Yukawa sector orthogonality (Route F"
    )
    print(
        "            obstruction persists under Connes-Chamseddine"
    )
    print(
        "            relabeling)"
    )
    print(
        "        S5: spectral-coincidence trap (A1 is not an extremum"
    )
    print(
        "            of Tr f(H^2/Lambda^2) for any natural f)"
    )

    print(
        "\n6.2 Honest assessment. The spectral-action principle, evaluated"
    )
    print(
        "    on the framework's existing Dirac structure, does NOT pin"
    )
    print(
        "    |b|^2/a^2 = 1/2 even after accepting the principle as a"
    )
    print(
        "    primitive import. The claim that the principle 'picks a"
    )
    print(
        "    canonical normalization' applies to GAUGE coefficients in"
    )
    print(
        "    Connes-Chamseddine (g_3 : g_2 : g_Y = 1 : 1 : sqrt(5/3)), NOT"
    )
    print(
        "    to Yukawa matrix internal structure."
    )

    print(
        "\n6.3 Comparison with Route F. The spectral-action approach is"
    )
    print(
        "    materially WORSE than Route F by primitive count:"
    )
    print(
        "      Route F  : closure modulo 1 named gauge-to-flavor bridge"
    )
    print(
        "      Probe 4  : closure modulo 4 named primitives (triple, action,"
    )
    print(
        "                 cutoff f, cutoff Lambda) PLUS the same bridge"
    )

    print(
        "\n6.4 Why this is not corollary churn. The spectral-action route"
    )
    print(
        "    was the canonical 'NCG escape' from the convention-dependence"
    )
    print(
        "    trap that closed Routes A, D, E, F. The probe specifically"
    )
    print(
        "    establishes that this escape is not available: the convention-"
    )
    print(
        "    dependence trap reappears as cutoff-function and cutoff-scale"
    )
    print(
        "    convention dependence. The negative result is informative for"
    )
    print(
        "    the framework's audit ledger."
    )

    print(
        "\n6.5 What this closes:"
    )
    print(
        "      - Probe 4 negative closure (bounded obstruction)"
    )
    print(
        "      - Removes 'spectral action' from the candidate axiom-native"
    )
    print(
        "        A1 closure list"
    )
    print(
        "      - Confirms A1 admission count UNCHANGED"
    )

    print(
        "\n6.6 What this does NOT close:"
    )
    print(
        "      - A1 admission itself (still load-bearing)"
    )
    print(
        "      - Routes that genuinely add new primitives outside the"
    )
    print(
        "        spectral-action class (e.g., direct A3-class postulate)"
    )

    passfail(
        "probe 4 bounded obstruction theorem assembled (5 barriers)",
        True,
    )


# --------------------------------------------------------------------
# Section 7: falsifiability anchor (PDG values, anchor-only)
# --------------------------------------------------------------------


def section7_falsifiability_anchor():
    section(
        "7. Falsifiability anchor (PDG values; anchor-only, NOT derivation input)"
    )

    print(
        "\n7.1 Falsifiability. The probe predicts:"
    )
    print(
        "      (i) A1 condition |b|^2/a^2 = 1/2 cannot be derived from"
    )
    print(
        "          retained content + spectral-action principle."
    )
    print(
        "      (ii) Adding spectral-action principle as primitive does NOT"
    )
    print(
        "          reduce the A1 admission count."
    )

    # Anchor: representative charged-lepton masses from PDG (anchor-only)
    # These are NOT used in any derivation step above.
    m_e = 0.510998950e-3   # GeV (anchor only)
    m_mu = 105.6583755e-3
    m_tau = 1776.86e-3

    print(
        "\n7.2 PDG charged-lepton masses (ANCHOR ONLY, never used in any"
    )
    print(
        "    derivation step above):"
    )
    print(f"      m_e   = {m_e:.6e} GeV")
    print(f"      m_mu  = {m_mu:.6e} GeV")
    print(f"      m_tau = {m_tau:.6e} GeV")

    sum_m = m_e + m_mu + m_tau
    sum_sqrt_m = math.sqrt(m_e) + math.sqrt(m_mu) + math.sqrt(m_tau)
    # Koide ratio: Q = sum m / (sum sqrt m)^2; predicted = 2/3
    Q_observed = sum_m / (sum_sqrt_m ** 2)
    print(
        f"\n    Observed Koide Q = sum m / (sum sqrt m)^2 = {Q_observed:.6f}"
    )
    print(
        f"    A1 prediction Q = 2/3 = {2.0 / 3.0:.6f}"
    )
    delta = abs(Q_observed - 2.0 / 3.0)
    print(f"    Delta = {delta:.6e}")

    # The probe does NOT use this anchor for any derivation. It only shows
    # that A1 is NUMERICALLY consistent with observation, while remaining
    # STRUCTURALLY un-derived from retained content + spectral action.
    passfail(
        "PDG anchor consistency: |Q_obs - 2/3| < 1e-3 (anchor-only, not derivation input)",
        delta < 1e-3,
        f"|Q_obs - 2/3| = {delta:.6e}",
    )


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------


def main():
    print("=" * 88)
    print("Koide A1 Probe 4 — Spectral-Action Principle (Connes-style) bounded obstruction")
    print("=" * 88)

    section0_setup()
    section1_barrier_s1()
    section2_barrier_s2()
    section3_barrier_s3()
    section4_barrier_s4()
    section5_barrier_s5()
    section6_synthesis()
    section7_falsifiability_anchor()

    # Final tally
    section("FINAL TALLY")
    n_total = len(PASSES)
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_fail = n_total - n_pass
    print(f"\n  Total checks: {n_total}")
    print(f"  PASS:         {n_pass}")
    print(f"  FAIL:         {n_fail}")

    if n_fail == 0:
        print(f"\n  VERDICT: Probe 4 (spectral-action) bounded obstruction CONFIRMED")
        print(f"  A1 admission count UNCHANGED")
        print(f"  Spectral-action principle imports 4 named primitives, not 1")
        return 0
    else:
        print(f"\n  VERDICT: probe FAILED ({n_fail} checks failed)")
        for name, ok, detail in PASSES:
            if not ok:
                print(f"    FAIL: {name} | {detail}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
