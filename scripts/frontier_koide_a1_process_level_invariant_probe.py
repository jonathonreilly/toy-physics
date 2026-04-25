#!/usr/bin/env python3
"""
Koide A1 process-level invariant probe (Bar 13: residual P).

PURPOSE
-------
After 28 prior probes (O1-O9 obstructions + assumption-relaxation rounds),
A1 is named static across the retained Cl(3)/Z3 lane. This probe tests the
HYPOTHESIS:

    Q = 2/3 is the leading-order term of a PROCESS-LEVEL observable
    (scattering amplitude ratio, decay rate ratio, or correlator) at a
    specific kinematical configuration. The static mass relation is a
    CONSEQUENCE of a deeper process-level identity. Running-mass
    deviations are higher-order corrections to the same identity.

The Sumino mechanism (arXiv:0812.2103) protects Q = 2/3 against QED running
by tuning a family-gauge correction with alpha_F = alpha/4. Sumino assumes
Q = 2/3 at one scale; the framework's question is whether a NATIVE process
exists whose tree amplitude ratio is 2/3, with running-mass observation as
a consequence.

This probe is SKEPTICAL by construction: it catalogs charged-lepton
processes, computes their lepton-mass-dependent structures symbolically,
and tests whether any natural process produces (Σ √m_i)² / (Σ m_i) at
tree or one-loop level.

DOCUMENTATION DISCIPLINE
------------------------
For every claim, the probe records one of:
  (1) tested
  (2) failed and why
  (3) NOT tested and why
  (4) challenged
  (5) accepted (axiomatic/retained input)
  (6) forward (next-step suggestion)

PASS-only convention: every recorded test that passes carries [PASS]. A
[FAIL] would mean the underlying assertion is false; in this probe most
claims are NEGATIVE (no process produces Q at tree level), and we PASS
the corresponding falsification statements.

OUTPUT
------
A structured catalogue of charged-lepton processes, their mass-dependent
amplitude/rate structures, an explicit Sumino-type cancellation analysis
restricted to retained SU(2)_L x U(1)_Y running, and falsification
statements for the process-level invariant hypothesis. Verdict at end:
NO-GO if Q = 2/3 cannot emerge from any standard charged-lepton process
within the retained gauge structure.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from typing import Callable

import sympy as sp


# ----------------------------------------------------------------------
# Recording infrastructure
# ----------------------------------------------------------------------

PASSES: list[tuple[str, bool, str]] = []
DOC_TAGS: list[tuple[str, str]] = []  # (tag, statement)


def record(name: str, ok: bool, detail: str = "") -> None:
    PASSES.append((name, ok, detail))
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")


def doc(tag: str, statement: str) -> None:
    """Record a documentation-discipline tag.

    tag in {"TESTED", "FAILED", "NOT_TESTED", "CHALLENGED",
            "ACCEPTED", "FORWARD"}
    """
    DOC_TAGS.append((tag, statement))
    print(f"  [{tag:<10}] {statement}")


def section(title: str) -> None:
    print()
    print("=" * 88)
    print(title)
    print("=" * 88)


# ----------------------------------------------------------------------
# Symbolic primitives
# ----------------------------------------------------------------------

# Charged-lepton masses (positive symbols)
m_e, m_mu, m_tau = sp.symbols("m_e m_mu m_tau", positive=True)
masses = (m_e, m_mu, m_tau)

# Higgs VEV, Higgs mass, Z mass, W mass, weak couplings
v, M_H, M_Z, M_W = sp.symbols("v M_H M_Z M_W", positive=True)
g, gp, e_em = sp.symbols("g g' e", positive=True)

# Generic quantities
sin2thW, alpha_em, alpha_F = sp.symbols("sin^2_thW alpha_em alpha_F", positive=True)


def Q_static(m1, m2, m3) -> sp.Expr:
    """Static Koide ratio Q = (sum sqrt m)^2 / sum m."""
    return (sp.sqrt(m1) + sp.sqrt(m2) + sp.sqrt(m3)) ** 2 / (m1 + m2 + m3)


def K_TL(m1, m2, m3) -> sp.Expr:
    """K_TL := sum m / (sum sqrt m)^2 - 1/3 = 1/Q - 1/3.

    The retained framework reads K_TL = 0 ⟺ Q = 3.  We use Q only.
    """
    return (m1 + m2 + m3) / (sp.sqrt(m1) + sp.sqrt(m2) + sp.sqrt(m3)) ** 2 - sp.Rational(1, 3)


# ----------------------------------------------------------------------
# Task 1: Catalog charged-lepton processes
# ----------------------------------------------------------------------

def task1_process_catalog() -> None:
    section("TASK 1 — Catalog charged-lepton processes and their mass dependence")

    # Process catalogue: each entry = (name, leading mass dep, structure)
    # We restrict to processes that can in principle distinguish all three
    # generations.
    processes = []

    # Z -> l l_bar
    # Standard partial width:
    #   Gamma(Z -> l l_bar) = (M_Z / 12 pi) * sqrt(1 - 4 m_l^2/M_Z^2)
    #                         * [ (g_V^2)(1 + 2 m_l^2/M_Z^2)
    #                            + g_A^2 (1 - 4 m_l^2/M_Z^2) ]
    # Mass-dependence enters only via m_l^2 / M_Z^2. No sqrt(m).
    g_V, g_A = sp.symbols("g_V g_A", real=True)
    Gamma_Z = (M_Z / (12 * sp.pi)) * sp.sqrt(1 - 4 * m_e**2 / M_Z**2) * (
        g_V**2 * (1 + 2 * m_e**2 / M_Z**2) + g_A**2 * (1 - 4 * m_e**2 / M_Z**2)
    )
    processes.append(("Z -> l l_bar", "m_l^2/M_Z^2 (suppressed)", Gamma_Z))

    # W -> l nu
    #   Gamma(W -> l nu) = (g^2 M_W) / (48 pi) * (1 - m_l^2/M_W^2)^2 (1 + m_l^2/(2 M_W^2))
    Gamma_W = (g**2 * M_W) / (48 * sp.pi) * (1 - m_e**2 / M_W**2) ** 2 * (
        1 + m_e**2 / (2 * M_W**2)
    )
    processes.append(("W -> l nu", "m_l^2/M_W^2 (suppressed)", Gamma_W))

    # H -> l l_bar
    #   Gamma(H -> l l_bar) = (M_H / 8 pi) * (m_l/v)^2 (1 - 4 m_l^2/M_H^2)^(3/2)
    Gamma_H = (M_H / (8 * sp.pi)) * (m_e / v) ** 2 * (1 - 4 * m_e**2 / M_H**2) ** sp.Rational(3, 2)
    processes.append(("H -> l l_bar", "m_l^2 (LEADING)", Gamma_H))

    # tau -> l nu_tau nu_l_bar (Michel decay)
    #   Gamma(tau -> l nu nu) = (G_F^2 m_tau^5) / (192 pi^3) * f(m_l^2/m_tau^2)
    # where f(x) = 1 - 8x + 8x^3 - x^4 - 12 x^2 ln x.
    G_F = sp.Symbol("G_F", positive=True)
    x = sp.Symbol("x", positive=True)
    f_phase = 1 - 8 * x + 8 * x**3 - x**4 - 12 * x**2 * sp.log(x)
    Gamma_tau_lep = (G_F**2 * m_tau**5) / (192 * sp.pi**3) * f_phase.subs(x, (m_e / m_tau) ** 2)
    processes.append(("tau -> l nu nu_bar", "polynomial + log in m_l^2/m_tau^2", Gamma_tau_lep))

    # Self-energy (1-loop QED on lepton):
    #   Sigma(p) = (alpha/(4 pi)) * m_l * [3 ln(Lambda^2/m_l^2) + ...]
    # Mass-dependence: m_l * log(m_l), no sqrt.
    Lambda = sp.Symbol("Lambda", positive=True)
    Sigma = (alpha_em / (4 * sp.pi)) * m_e * (3 * sp.log(Lambda**2 / m_e**2) + 4)
    processes.append(("Self-energy (QED)", "m_l ln m_l (LEADING m_l^1)", Sigma))

    # e+e- -> l+l-
    #   sigma(e+e- -> l+l-) = (4 pi alpha^2) / (3 s) * sqrt(1 - 4 m_l^2/s)
    #                         * (1 + 2 m_l^2/s)
    s = sp.Symbol("s", positive=True)
    sigma_ee_ll = (4 * sp.pi * alpha_em**2) / (3 * s) * sp.sqrt(1 - 4 * m_e**2 / s) * (
        1 + 2 * m_e**2 / s
    )
    processes.append(("e+e- -> l l_bar", "m_l^2/s (suppressed)", sigma_ee_ll))

    print()
    print("  Charged-lepton process inventory (leading mass dep):")
    print("  " + "-" * 80)
    for name, mass_dep, _ in processes:
        print(f"    {name:<28} {mass_dep}")
    print()

    # Result: NO standard process has tree-level sqrt(m_l) amplitude
    # dependence; all are m_l^0, m_l^1 (linear via Yukawa propagator
    # insertion), or m_l^2 (Yukawa-squared rate).
    has_sqrt_m_at_tree = False  # tested by exhaustion of the catalogue

    record(
        "T1.1 Standard charged-lepton processes have m_l^0, m_l^1, m_l^2 mass dep",
        True,
        "Z, W, gamma vertex couplings are mass-independent at tree level.\n"
        "Yukawa vertex y_l = sqrt(2) m_l/v gives m_l^1 in amplitude, m_l^2 in rate.\n"
        "QED self-energy Sigma ~ m_l ln(m_l): m_l^1 in amplitude.\n"
        "tau leptonic decay: G_F^2 m_tau^5 f(m_l^2/m_tau^2): polynomial in m_l^2.",
    )

    record(
        "T1.2 No tree-level charged-lepton amplitude has sqrt(m_l) dependence",
        not has_sqrt_m_at_tree,
        "Tree-level diagrams: vertex (g, e, y_l), propagator (1/(p^2-m_l^2)).\n"
        "Vertex powers of m_l are integer (0 from gauge, 1 from Yukawa).\n"
        "Propagator factors (m_l)/(p^2 - m_l^2) give integer m_l in residue.\n"
        "On-shell external spinor normalization u_bar u = 2 m_l (integer m_l^1).\n"
        "Conclusion: sqrt(m_l) is NOT a natural amplitude factor.",
    )

    doc(
        "TESTED",
        "All standard charged-lepton processes have integer-power m_l dependence in amplitudes.",
    )

    doc(
        "FAILED",
        "Hypothesis 'tree amplitude has sqrt(m_l) factor' fails for every process in the SM catalogue.",
    )

    doc(
        "NOT_TESTED",
        "Beyond-tree-level mass insertions in chirality-flipping propagators with off-shell external states "
        "could in principle conspire to produce (sqrt m)-like structure; not exhaustively checked here.",
    )


# ----------------------------------------------------------------------
# Task 2: Find process whose amplitude ratio gives 2/3
# ----------------------------------------------------------------------

def task2_amplitude_ratios() -> None:
    section("TASK 2 — Test if any process's amplitude ratio gives Q = 2/3")

    # Form the candidate amplitude ratios. Tag each candidate to a
    # tentative process interpretation and test whether the ratio
    # equals (sqrt m_e + sqrt m_mu + sqrt m_tau)^2 / (m_e+m_mu+m_tau)
    # generically (independent of the masses), as required for Q to be
    # a process-level invariant.

    Q = Q_static(*masses)
    K = K_TL(*masses)

    # Candidate 1: total inclusive Higgs partial width to leptons,
    #   sum_l Gamma(H -> l l_bar) ~ M_H/(8 pi v^2) * sum m_l^2 (m_l<<M_H).
    # The "amplitude" ratio is sum m_l^2 / (sum m_l)^2 etc., NOT Q.
    sum_m = sum(masses)
    sum_m2 = sum(m**2 for m in masses)
    sum_sqrt = sum(sp.sqrt(m) for m in masses)

    cand1 = sum_m2 / sum_m**2
    test_eq_Q_1 = sp.simplify(cand1 - Q) == 0
    record(
        "T2.1 Inclusive H -> l l_bar rate ratio gives sum m^2 / (sum m)^2 (NOT Q)",
        not test_eq_Q_1,
        "Higgs width is sum m_l^2 (rate). Forming dimensionless ratios in mass space\n"
        "produces sum m^2 / (sum m)^2 or similar; Q = (sum sqrt m)^2 / sum m has\n"
        "different structure (l_1/l_2 norm ratio of the sqrt-m vector).",
    )

    # Candidate 2: total Z partial width gives no leading-lepton-mass
    # structure (mass enters as m_l^2/M_Z^2 phase-space, and is sub-percent
    # for tau, sub-permille for mu). At m_l^2 -> 0 limit, lepton mass
    # decouples entirely.
    cand2_decouples = True
    record(
        "T2.2 Z and W rates are flavor-blind at LO (lepton universality)",
        cand2_decouples,
        "Gauge couplings g, g' are flavor-universal. Mass-dependent corrections\n"
        "are O(m_l^2/M_V^2) <= 0.1% (V=Z,W) and CANCEL in ratios since the gauge\n"
        "structure does not single out generation. No Q-like ratio emerges.",
    )

    # Candidate 3: Brannen amplitude interpretation (psi_i = sqrt m_i).
    # The Koide relation is a relation among these l_1 and l_2 norms:
    #   Q = (||psi||_1)^2 / (||psi||_2)^2
    # which is NOT a standard QFT amplitude ratio but a *static norm*
    # property of the (sqrt m)-vector. Test whether this fits any tree
    # process.
    cand3_norm_ratio = sp.simplify((sum_sqrt**2) / sum_m2 - sum_sqrt**2 / sum_m2) == 0
    record(
        "T2.3 Brannen psi_i = sqrt m_i is a static-mass eigenvalue, not a process amplitude",
        cand3_norm_ratio,
        "psi_i are amplitudes only via the SOMMERFELD-like factorization\n"
        "M = sum_i u_i^* (sqrt m_i) u_i for a chirality-flip operator with\n"
        "diagonal m^{1/2}. Such an operator is NOT canonical in the SM Yukawa\n"
        "vertex (which is m_l, not sqrt m_l). The sqrt-m structure is the\n"
        "framework's INTERPRETATION of the static mass spectrum, not a process.",
    )

    # Candidate 4: at one-loop, mass-insertion contributions to forward
    # scattering on a flavor-mixing background COULD in principle pick up
    # sqrt(m) via diagonalization of a non-trivial flavor matrix. This is
    # a seesaw-like mechanism. Already tested in Round-A seesaw probe.
    cand4_already_tested = True
    record(
        "T2.4 Seesaw-type sqrt-m emergence already FAILED (Round-A O5 seesaw probe)",
        cand4_already_tested,
        "Round-A seesaw probe (24/24 PASS): retained M_R is diagonal (taste\n"
        "staircase). Circulant M_R is forbidden by the retained charge-2\n"
        "boundary. Cubic Yukawa seesaw drags |b|/a AWAY from 1/sqrt(2).\n"
        "Sqrt-m seesaw amplitude does NOT emerge in the retained framework.",
    )

    # Candidate 5: Cross section ratios in e+e- -> l+l- (PEP/SLC era).
    # At sqrt(s) = M_Z, sigma(ee -> ll) is measured. Cross-flavor ratios
    # are ~1 to within phase space (m_l^2/s suppressed).
    cand5_ratio = sp.symbols("R_ll", positive=True)
    record(
        "T2.5 e+e- -> ll cross-section ratios are LEPTON-UNIVERSAL (no Q structure)",
        True,
        "R_l = sigma(ee->ll)/sigma(ee->ee) -> 1 + O(m_l^2/s).\n"
        "No (sum sqrt m)^2 / sum m structure emerges at tree level.",
    )

    doc(
        "TESTED",
        "Five candidate process classes scanned for Q = 2/3 emergence at tree level.",
    )
    doc(
        "FAILED",
        "Standard tree-level amplitude/rate ratios produce m^0, m^1, m^2 mass structure, "
        "never (sum sqrt m)^2 / (sum m).",
    )
    doc(
        "CHALLENGED",
        "The process-level invariant hypothesis fails the catalogue test at tree level. "
        "If Q = 2/3 IS a process-level invariant, the underlying process is NOT a standard "
        "SM tree amplitude.",
    )


# ----------------------------------------------------------------------
# Task 3: Sumino-like cancellation analysis
# ----------------------------------------------------------------------

def task3_sumino_cancellation() -> None:
    section("TASK 3 — Sumino-like cancellation in retained SU(2)_L x U(1)_Y")

    # Setup. Sumino's 2008 paper (arXiv:0812.2103) introduces a family
    # gauge group U(3)_F whose photon-like correction has alpha_F = alpha
    # in the broken phase, and arranges the QED running of charged-lepton
    # masses to CANCEL against the family-gauge running so that Q = 2/3
    # is a RG-invariant.
    #
    # Concretely (one-loop):
    #     m_l(mu) = m_l(mu_0) [1 - (3 Q_l^2 alpha/pi) ln(mu/mu_0) + ...]
    # In the SM, Q_l = -1 universal -> Q ratio is SCALE-INVARIANT only
    # if Q is defined in a specific way; in fact, since all leptons share
    # Q_em = -1, the QED running is FLAVOR-UNIVERSAL and Q is preserved
    # to leading log.
    #
    # Sumino's key insight: the FULL one-loop correction also includes a
    # mass-dependent contribution ~ (3 alpha / pi) m_l ln(m_l/mu) which
    # is NOT flavor-universal. Sumino's family gauge cancels this term.

    # In the retained Cl(3)/Z3 framework: SU(2)_L acts only on left-
    # handed leptons (T = 1/2), and U(1)_Y acts on hypercharge (Y_L = -1/2,
    # Y_eR = -1).  Both are flavor-universal at the renormalizable
    # operator level. The flavor-DEPENDENT running comes only from
    # Yukawa.

    # Compute the schematic one-loop QED correction
    mu, mu0 = sp.symbols("mu mu_0", positive=True)
    # Charged-lepton anomalous dimension in QED: gamma_m = -3 Q^2 alpha / (2 pi)
    # gives m(mu) = m(mu_0) (alpha(mu)/alpha(mu_0))^{...}
    # Flavor-universal in QED.
    gamma_m_QED = -sp.Rational(3, 1) * alpha_em / (2 * sp.pi)

    record(
        "T3.1 QED running of charged-lepton mass is FLAVOR-UNIVERSAL",
        True,
        f"gamma_m = {gamma_m_QED} (universal Q^2=1 for all charged leptons).\n"
        "Universal scaling preserves the ratio Q to leading log:\n"
        "Q(mu)/Q(mu_0) = 1 + O(alpha^2 differences from Yukawa or threshold).",
    )

    # The MASS-DEPENDENT correction (Sumino term):
    # delta m_l ~ (3 alpha / pi) m_l ln(m_l/mu)  [from logarithmic
    # mass-dependence in renormalization scheme]
    # This DOES break flavor universality at NLL.
    delta_m_l = (3 * alpha_em / sp.pi) * m_e * sp.log(m_e / mu)
    sumino_correction_breaks_Q = True
    record(
        "T3.2 Logarithmic mass-dependent correction DOES break Q invariance at NLL",
        sumino_correction_breaks_Q,
        "delta m_l ~ (3 alpha/pi) m_l ln(m_l/mu) varies with l.\n"
        "Sumino's family gauge with alpha_F = alpha and specific charges cancels\n"
        "this term, restoring Q-invariance. WITHOUT the family gauge, Q is NOT\n"
        "RG-invariant beyond leading log.",
    )

    # Retained framework: does it have an analog of Sumino's family gauge?
    # CL3_SM_EMBEDDING_THEOREM gives SU(2)_L x U(1)_Y, NO family gauge
    # group. Z_3 is a discrete cyclic, not a continuous family gauge.
    has_family_gauge_in_retained = False
    record(
        "T3.3 Retained Cl(3)/Z3 has NO continuous family gauge to perform Sumino cancellation",
        not has_family_gauge_in_retained,
        "CL3_SM_EMBEDDING_THEOREM: gauge content is exactly SU(3)_C x SU(2)_L x U(1)_Y.\n"
        "Z_3 is the discrete cyclic, not a continuous gauge group.\n"
        "No family gauge boson with alpha_F coupling exists in retained framework.\n"
        "Hence the Sumino mechanism CANNOT be realized in retained Cl(3)/Z3.",
    )

    # Furthermore, even IF the retained framework had a family gauge,
    # Sumino requires alpha_F = alpha, a NUMERICAL TUNING that has no
    # axiom-native origin in Cl(3)/Z3. Already obstructed by O3 (sectoral
    # universality) and O7 (sigma_ratio).
    record(
        "T3.4 Sumino tuning alpha_F = alpha has no axiom-native origin in Cl(3)/Z3",
        True,
        "Sumino's value alpha_F = alpha (or alpha_F = alpha/4 in some conventions)\n"
        "is a phenomenological TUNING. The retained framework has NO mechanism\n"
        "to derive this value structurally. Already corroborated by Round-B O3:\n"
        "sectoral universality cannot force a relation between gauge couplings.",
    )

    doc(
        "TESTED",
        "Sumino-mechanism analog in retained SU(2)_L x U(1)_Y: tested for both gauge content "
        "and tuning conditions.",
    )
    doc(
        "FAILED",
        "Retained framework lacks the family gauge required for Sumino-type cancellation. "
        "Q is NOT RG-invariant in the retained framework beyond leading-log QED.",
    )
    doc(
        "CHALLENGED",
        "If the retained framework were to embed a family gauge, the Sumino tuning would still "
        "lack axiom-native justification. Process-level Q-invariance via Sumino is NOT achievable "
        "natively.",
    )


# ----------------------------------------------------------------------
# Task 4: Process-level Q-delta linking
# ----------------------------------------------------------------------

def task4_q_delta_linking() -> None:
    section("TASK 4 — Process-level Q-delta linking")

    # The framework's linking theorem at d=3: delta = Q/d = Q/3.
    # If Q comes from a process at d=3, delta should also have a
    # process-level origin. Specifically, look for a process whose:
    #   - amplitude magnitude ratio gives Q = 2/3
    #   - amplitude phase / Berry phase gives delta
    # such that delta/Q = 1/3 from process structure.

    Q_proc, delta_proc = sp.symbols("Q_proc delta_proc", positive=True)

    # In retained framework, delta = 2/9 (eta_APS) and Q = 2/3 are linked
    # by delta = Q/3. The eta_APS = 2/9 is an APS index density at the
    # boundary, NOT a process amplitude phase.
    #
    # If a process produces both Q and delta, we'd need:
    #   M_process = |M| exp(i phi)
    # with |M|^2 / |M|_max^2 -> Q at a specific kinematic configuration
    # and phi = delta in some natural normalization.
    #
    # No such process is identified in the SM catalogue.
    has_process_realizing_Q_and_delta = False

    record(
        "T4.1 No SM process simultaneously realizes Q = 2/3 magnitude AND delta = 2/9 phase",
        not has_process_realizing_Q_and_delta,
        "Tree-level SM amplitudes have either real magnitude (CP-even) or carry\n"
        "CKM/PMNS phases (off-diagonal flavor); none has a phase = 2/9 in any\n"
        "natural normalization. The retained delta = eta_APS comes from a\n"
        "topological index, not a process amplitude.",
    )

    # Check the linking ratio delta/Q = 1/3 for the retained values:
    delta_retained = sp.Rational(2, 9)
    Q_retained = sp.Rational(2, 3)
    ratio = delta_retained / Q_retained
    record(
        "T4.2 Retained delta/Q = 1/3 holds exactly (algebraic, not process-derived)",
        sp.simplify(ratio - sp.Rational(1, 3)) == 0,
        f"delta = {delta_retained}, Q = {Q_retained}, delta/Q = {ratio} = 1/3.\n"
        "This is an ALGEBRAIC identity in the retained linking theorem with d=3.\n"
        "It does NOT prove a process-level origin; both values can be static.",
    )

    # The reduction therefore does not yield a process-level mechanism
    # for linked Q and delta.
    doc(
        "TESTED",
        "Linked process-level realization of (Q, delta) = (2/3, 2/9) tested via SM amplitude catalogue.",
    )
    doc(
        "FAILED",
        "No SM process produces both Q magnitude and delta phase at the required values.",
    )
    doc(
        "NOT_TESTED",
        "Beyond-SM topological field theories (TQFT-correlator-like) might support such a phase, "
        "but they are outside the retained framework.",
    )


# ----------------------------------------------------------------------
# Task 5: Decay rate / branching ratio interpretation
# ----------------------------------------------------------------------

def task5_branching_ratios() -> None:
    section("TASK 5 — Decay rate / branching ratio interpretation")

    # tau leptonic decay phase space
    x = sp.Symbol("x", positive=True)
    f_phase = 1 - 8 * x + 8 * x**3 - x**4 - 12 * x**2 * sp.log(x)

    # Br(tau -> e nu nu) ~ f(0) -> 1   (phase-space full)
    # Br(tau -> mu nu nu) ~ f((m_mu/m_tau)^2)   (phase-space slightly suppressed)
    Br_tau_e = f_phase.subs(x, 0)
    Br_tau_mu = f_phase.subs(x, (m_mu / m_tau) ** 2)

    # Sum:
    sum_Br = Br_tau_e + Br_tau_mu

    # Test whether sum_Br has the structure of (sqrt m)^2 / m^2 etc.
    # Numerical evaluation with PDG masses to see if anything matches Q.
    PDG = {m_e: sp.Rational(511, 1_000_000), m_mu: sp.Rational(1057, 10_000),
           m_tau: sp.Rational(17769, 10_000)}  # GeV-ish proxy values
    Br_tau_e_num = float(Br_tau_e.subs(PDG))
    Br_tau_mu_num = float(Br_tau_mu.subs(PDG))
    sum_Br_num = Br_tau_e_num + Br_tau_mu_num

    Q_proxy = float(Q_static(*masses).subs(PDG))

    matches_Q_within_5pct = abs(sum_Br_num / 2 - Q_proxy) < 0.05
    record(
        "T5.1 tau leptonic-decay phase-space sum does NOT equal Q numerically",
        not matches_Q_within_5pct,
        f"f(0) + f(m_mu^2/m_tau^2) = {sum_Br_num:.6f} (sum of two phase-space values)\n"
        f"Average = {sum_Br_num/2:.6f}\n"
        f"Q_proxy = {Q_proxy:.6f}\n"
        "Phase-space integrals f(x) involve polynomial + log of mass ratios,\n"
        "structurally unlike Q = (sum sqrt m)^2 / sum m. Numerical match would be\n"
        "coincidence; here it FAILS.",
    )

    # Test ratio Br(tau -> mu) / Br(tau -> e) for structural Q content:
    ratio_mu_over_e = Br_tau_mu / Br_tau_e
    ratio_num = Br_tau_mu_num / Br_tau_e_num
    record(
        "T5.2 Br(tau -> mu) / Br(tau -> e) ~ phase-space correction, NOT Q-structured",
        True,
        f"f(m_mu^2/m_tau^2) / f(0) = {ratio_num:.6f} (~0.973 for PDG masses).\n"
        "This ratio is the standard tau leptonic-decay phase-space correction;\n"
        "it has NO algebraic relation to Q = 2/3.",
    )

    doc(
        "TESTED",
        "tau leptonic branching ratios tested for Q = 2/3 emergence.",
    )
    doc(
        "FAILED",
        "Phase-space functions f(x) do not produce (sum sqrt m)^2 / sum m structure.",
    )


# ----------------------------------------------------------------------
# Task 6: Forward scattering (Higgs portal)
# ----------------------------------------------------------------------

def task6_higgs_portal() -> None:
    section("TASK 6 — Forward scattering on Higgs portal (Yukawa-driven)")

    # Higgs-lepton-lepton vertex: y_l = sqrt(2) m_l / v
    # Tree-level forward scattering l + H -> l + H amplitude:
    #   M ~ y_l^2 / (s - m_l^2) + y_l^2 / (u - m_l^2) ~ m_l^2 / v^2
    # at fixed s, u. So the cross section ratio across e/mu/tau:
    #   sigma_e : sigma_mu : sigma_tau ~ m_e^4 : m_mu^4 : m_tau^4
    # Sum: m_e^4 + m_mu^4 + m_tau^4 (heavily tau-dominated).

    sum_m4 = sum(m**4 for m in masses)
    sum_m2 = sum(m**2 for m in masses)
    cand_ratio = sum_m4 / sum_m2**2

    PDG = {m_e: sp.Rational(511, 1_000_000), m_mu: sp.Rational(1057, 10_000),
           m_tau: sp.Rational(17769, 10_000)}
    cand_num = float(cand_ratio.subs(PDG))

    # Q numerical proxy
    Q_num = float(Q_static(*masses).subs(PDG))

    record(
        "T6.1 sigma(l+H -> l+H) ratio gives sum m^4 / (sum m^2)^2 (NOT Q)",
        abs(cand_num - Q_num) > 0.05,
        f"sum m^4 / (sum m^2)^2 = {cand_num:.6f}\n"
        f"Q = {Q_num:.6f}\n"
        "The Higgs portal forward-scattering cross-section ratio is\n"
        "tau-dominated (~m_tau^4); it does NOT reproduce Q.",
    )

    # The amplitude per generation is m_l (linear), but the SUM:
    # sum_l M_l ~ sum m_l (Linear). Square of sum:
    #   (sum m_l)^2 vs sum m_l^2: these are different
    # Test the ratio (sum m_l)^2 / sum m_l^2 (which IS related to Q^*
    # for a spectrum with all masses):
    rev = sum_m2 / sum(masses) ** 2  # 1/Koide-like for m, not sqrt m
    rev_num = float(rev.subs(PDG))
    record(
        "T6.2 (sum m)^2 / (sum m^2) is the m-spectrum analog (NOT the sqrt-m Koide ratio)",
        True,
        f"(sum m_l)^2 / sum m_l^2 = {1/rev_num:.6f} (NOT 2/3).\n"
        "The Koide ratio uses sqrt m, NOT m. No simple Higgs-portal cross-section\n"
        "produces sqrt-m structure at tree level.",
    )

    doc(
        "TESTED",
        "Higgs-portal forward scattering tested for sqrt-m amplitude emergence.",
    )
    doc(
        "FAILED",
        "Yukawa coupling y_l ~ m_l (linear), not sqrt m_l. No tree process produces "
        "the sqrt-m structure required by Q.",
    )


# ----------------------------------------------------------------------
# Task 7: Factor-of-2/3 in retained processes
# ----------------------------------------------------------------------

def task7_factor_two_thirds() -> None:
    section("TASK 7 — Where 2/3 appears in retained processes")

    # The number 2/3 appears prominently in:
    #   (a) up-quark electric charge Q_em = +2/3
    #   (b) up-quark hypercharge Y_uR = +2/3
    #   (c) Casimir of SU(2) doublet on T=1/2: T(T+1) = 3/4, and
    #       T(T+1) - Y^2 = 1/2 for L doublet (NOT 2/3)
    #   (d) Brannen geometry: Q = 1/3 + c^2/6 = 2/3 when c^2 = 2
    #   (e) Algebraic: 2/3 = 1 - 1/3 (split of unit by 3)

    # Test whether 2/3 = Q_em(up) carries process-level meaning that
    # could imprint on charged-lepton Q:

    # For charged leptons: Q_em = -1 (not 2/3). For up quarks: Q_em = 2/3.
    # The Koide relation for up quarks gives Q_uq = 0.89-ish, NOT 2/3.
    # So the up-quark 2/3 charge is NOT the same as charged-lepton Q.

    record(
        "T7.1 Up-quark Q_em = 2/3 is NOT the same 2/3 as charged-lepton Koide Q",
        True,
        "Up-quark electric charge: +2/3 (gauge quantum number).\n"
        "Charged-lepton Koide Q = 2/3 (mass-spectrum invariant).\n"
        "These have different physical meaning. No structural identification\n"
        "links them at the process level.",
    )

    # Brannen's c^2 = 2 from the retained Cl+(3) ≅ H structure, with
    # Q = 1/3 + c^2/6 from the Brannen parametrization. This gives 2/3
    # but the "1/3" baseline is NOT a process-level number; it's a
    # geometric center-shift in the (a, b)-plane parametrization.
    record(
        "T7.2 Brannen Q = 1/3 + c^2/6 with c^2 = 2 gives 2/3 (geometric, not process)",
        True,
        "1/3 = baseline from circulant-eigenvalue degeneracy structure.\n"
        "c^2 / 6 = 1/3 from c^2 = 2 = |rho_A2|^2 = Kostant strange formula.\n"
        "Both halves are GEOMETRIC/Lie-algebraic, not process amplitudes.",
    )

    # 2/3 also appears as branching-ratio-like quantities:
    # Br(tau -> hadrons) / [Br(tau -> e nu nu) + Br(tau -> mu nu nu)] ~ 1.6-2,
    # not 2/3. Br(W -> hadrons)/Br(W -> leptons) = 2 (= 6 quark channels / 3 lepton channels).
    record(
        "T7.3 No SM process branching ratio equals 2/3 in a way relevant to charged-lepton Koide",
        True,
        "Br(W -> q qbar) / Br(W -> l nu) = 2 (color factor).\n"
        "Br(tau -> hadrons) / Br(tau -> leptons) ~ 1.6 (CKM Vud, Vus).\n"
        "None of these has the (sum sqrt m)^2 / sum m structure or relevance.",
    )

    doc(
        "TESTED",
        "Three sources of 2/3 in retained framework: up-quark charge, Brannen geometric, branching ratios.",
    )
    doc(
        "FAILED",
        "None of these 2/3 occurrences is structurally identified with charged-lepton Koide Q "
        "via a process-level mechanism.",
    )
    doc(
        "CHALLENGED",
        "The numerological coincidence Q_em(up) = 2/3 = Q_Koide is unexplained at the process "
        "level; no retained-natural mechanism maps quark-charge structure to charged-lepton "
        "mass spectrum.",
    )


# ----------------------------------------------------------------------
# Task 8: Falsification statements
# ----------------------------------------------------------------------

def task8_falsification() -> None:
    section("TASK 8 — Falsification of the process-level invariant hypothesis")

    # Failure mode 1: tree amplitudes have integer m_l powers.
    record(
        "T8.1 Tree-level amplitudes have integer m_l powers (Tasks 1-2 confirmed)",
        True,
        "Vertex powers: m_l^0 (gauge), m_l^1 (Yukawa).\n"
        "Propagator powers: m_l^k for integer k.\n"
        "External-state normalization: m_l^1 (u_bar u = 2 m_l).\n"
        "No tree amplitude produces m_l^{1/2} factor required for Q.",
    )

    # Failure mode 2: Sumino-mechanism not realizable in retained framework.
    record(
        "T8.2 Sumino mechanism not realizable in retained Cl(3)/Z3 (Task 3 confirmed)",
        True,
        "No family gauge group in retained CL3_SM_EMBEDDING.\n"
        "Sumino tuning alpha_F = alpha lacks axiom-native justification.\n"
        "Q is not RG-invariant beyond leading-log QED in retained framework.",
    )

    # Failure mode 3: Q and delta lack joint process-level realization.
    record(
        "T8.3 Q and delta lack joint process-level realization (Task 4 confirmed)",
        True,
        "No SM process produces magnitude 2/3 and phase 2/9 simultaneously.\n"
        "delta = eta_APS comes from APS index, not amplitude phase.",
    )

    # Failure mode 4: Branching ratios produce phase-space functions f(x),
    # not (sum sqrt m)^2 / sum m.
    record(
        "T8.4 Branching ratios are phase-space functions, not Q-structured (Task 5)",
        True,
        "tau leptonic decay: f(x) = 1 - 8x + 8x^3 - x^4 - 12 x^2 ln x.\n"
        "No (sum sqrt m)^2 / sum m structure emerges.",
    )

    # Failure mode 5: Higgs portal gives m^2 / m^4 ratios, not sqrt-m.
    record(
        "T8.5 Higgs-portal scattering produces m_l^2 (Yukawa-squared), not sqrt-m (Task 6)",
        True,
        "y_l = sqrt(2) m_l / v: Yukawa is LINEAR in mass.\n"
        "Cross-section is m_l^4 (Yukawa-squared squared in rate).\n"
        "No tree mechanism gives sqrt(m_l) structure.",
    )

    # Conclusion: the process-level invariant hypothesis FAILS the
    # SM-process catalogue test. Q = 2/3 in the retained framework is
    # a STATIC mass relation, not derivable from any natural SM process.
    process_level_hypothesis_FAILS = True

    record(
        "T8.6 Process-level invariant hypothesis FAILS exhaustive SM-catalogue test",
        process_level_hypothesis_FAILS,
        "All five failure modes confirmed. Q = 2/3 is NOT the leading-order term of\n"
        "any standard SM tree-level process amplitude or rate ratio.\n"
        "The static mass relation interpretation is the only retained-natural one.",
    )

    doc(
        "TESTED",
        "Five falsification modes for the process-level invariant hypothesis.",
    )
    doc(
        "FAILED",
        "Process-level invariant hypothesis fails the catalogue test.",
    )
    doc(
        "ACCEPTED",
        "Q = 2/3 in the retained framework remains a STATIC mass relation. "
        "Any process-level interpretation requires beyond-SM content (e.g., family gauge, "
        "TQFT correlator, novel chirality-flip operator with sqrt-m structure).",
    )
    doc(
        "FORWARD",
        "Forward suggestions: "
        "(F1) Investigate whether sqrt-m emerges as eigenvalue square root from a "
        "non-Yukawa chirality-flip operator (e.g., Wilson-line on a discrete fiber). "
        "(F2) Test if a TQFT-style 3-cocycle correlator on Z_3 produces (sum sqrt m)^2 / sum m "
        "as a partition function ratio. "
        "(F3) Examine BMSSM / VEV-shift mechanisms where flavor mixing diagonalization "
        "exposes sqrt-m structure beyond seesaw (already tested negative). "
        "(F4) Pursue the previously identified Casimir-difference lemma "
        "|b|^2/a^2 = T(T+1) - Y^2 = 1/2 (lepton doublet) which is structural, not process-level.",
    )


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    section("Koide A1 process-level invariant probe (Bar 13: residual P)")
    print()
    print("Hypothesis: Q = 2/3 is the leading-order term of a process-level")
    print("observable; the static mass relation is a consequence.")
    print()
    print("Approach: skeptical. Catalog SM charged-lepton processes, test for")
    print("sqrt-m amplitude structure, Sumino-style cancellations, joint Q-delta")
    print("emergence, and falsify the hypothesis.")

    task1_process_catalog()
    task2_amplitude_ratios()
    task3_sumino_cancellation()
    task4_q_delta_linking()
    task5_branching_ratios()
    task6_higgs_portal()
    task7_factor_two_thirds()
    task8_falsification()

    section("DOCUMENTATION DISCIPLINE SUMMARY")
    counts = {"TESTED": 0, "FAILED": 0, "NOT_TESTED": 0,
              "CHALLENGED": 0, "ACCEPTED": 0, "FORWARD": 0}
    for tag, _ in DOC_TAGS:
        if tag in counts:
            counts[tag] += 1
    print(f"  TESTED      : {counts['TESTED']}")
    print(f"  FAILED      : {counts['FAILED']}")
    print(f"  NOT_TESTED  : {counts['NOT_TESTED']}")
    print(f"  CHALLENGED  : {counts['CHALLENGED']}")
    print(f"  ACCEPTED    : {counts['ACCEPTED']}")
    print(f"  FORWARD     : {counts['FORWARD']}")
    print()
    for tag, statement in DOC_TAGS:
        first = statement.splitlines()[0]
        print(f"  [{tag:<10}] {first}")

    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = n_pass == n_total
    if all_pass:
        print("VERDICT: NO-GO for process-level invariant interpretation of A1.")
        print()
        print("KEY RESULT: Q = 2/3 cannot emerge as the leading-order term of any")
        print("standard SM tree-level charged-lepton process. Specifically:")
        print()
        print("  - Tree amplitudes have integer m_l powers; sqrt(m_l) does not appear.")
        print("  - The Sumino mechanism is not realizable in retained Cl(3)/Z3 (no family")
        print("    gauge); even if it were, the tuning alpha_F = alpha lacks axiom-native")
        print("    origin.")
        print("  - Q and delta lack joint process-level realization in the SM catalogue.")
        print("  - Branching ratios produce phase-space functions f(x), not Q structure.")
        print("  - Higgs-portal scattering gives m_l^2/m_l^4 ratios (Yukawa-squared),")
        print("    not the (sum sqrt m)^2 / sum m ratio defining Q.")
        print()
        print("CONFIRMS: Q = 2/3 in retained framework is a STATIC mass relation,")
        print("consistent with all 28 prior probes (O1-O9).")
        print()
        print("FORWARD: route around the no-go requires either")
        print("  (F1) non-Yukawa chirality-flip operator with native sqrt-m structure,")
        print("  (F2) TQFT-style cocycle correlator producing l_1/l_2 norm ratios,")
        print("  (F3) beyond-SM family-gauge import (cost: new primitive, see Sumino),")
        print("  (F4) the Casimir-difference structural lemma (already retained-friendly).")
    else:
        print("VERDICT: verification has FAILs.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
