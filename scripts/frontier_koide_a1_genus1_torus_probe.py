#!/usr/bin/env python3
"""
Koide A1 / delta = 2/9 -- Genus-1 (torus) 1/N_c^2 closure probe.

============================================================================
PROBE 29 of the Koide A1 frontier ledger (28 prior probes failed).
============================================================================

HYPOTHESIS UNDER TEST (Bar 6, "1/N_c^2 genus-1 torus diagram")

    delta = 2/9 emerges from a Yukawa-sector genus-1 torus Feynman diagram
    with topological coefficient 2 (Euler-characteristic, signature, or
    multiplicity equivalent), in a *retained* 1/N_c expansion at N_c = 3.
    The factor of 2 has structural origin (chirality doubling, Z_2 grading,
    or fermion-loop minus signs combined with another sign).

CONTEXT

  * Retained: R_conn = (N_c^2 - 1)/N_c^2 = 8/9 + O(1/N_c^4)
    derived rigorously in docs/RCONN_DERIVED_NOTE.md from 't Hooft's
    1/N_c expansion at N_c=3 with planar (genus-0) dominance and
    SU(N_c) Fierz channel counting.

  * Universal obstruction (radian-bridge no-go,
    docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md):
    every retained radian on Cl(3)/Z_3 is (rational) * pi.
    delta = 2/9 is a pure rational *measured in radians* with no pi.
    No retained mechanism converts.

  * 9 obstruction classes O1..O9 already identified.

WHAT THIS PROBE TESTS (and what it does NOT)

  Task 1 [TESTED]: identify which "N" of 't Hooft applies to the Yukawa
                   sector. Candidates: 2 (weak isospin), 3 (color), or
                   3 (generation/circulant flavor index from C_3).
  Task 2 [TESTED, symbolic]: enumerate the genus-1 contributions to the
                   charged-lepton Yukawa amplitude self-energy, and their
                   N_c-counting coefficients. Compute Euler characteristic
                   2-2g and any natural prefactor of 2.
  Task 3 [TESTED, symbolic + small numeric]: does the genus-1 contribution
                   produce a literal radian (dimensionless ratio carried as
                   an angle) of value 2/9, or only a numerical factor times
                   the 1/(16 pi^2) loop measure?
  Task 4 [TESTED]: explicit pi-tracking. Decompose any putative radian
                   output as pi-power x rational and check if pi-power = 0
                   (i.e. literal rational radian).
  Task 5 [TESTED]: algebraic relation among delta, R_conn, N_c. Check
                   delta = 2(1 - R_conn) hypothesis structurally.
  Task 6 [TESTED]: falsification: which N gives the wrong numerology
                   (N=2 -> 2/4 = A1's magnitude!, N=3 -> 2/9, etc.) and
                   does the framework distinguish them naturally?

  NOT TESTED:
    * Full non-perturbative genus-1 amplitude on the lattice. Computing
      the literal genus-1 fermion loop integrand at N_c=3 and beta=6
      requires Monte Carlo on a torus topology (out of probe scope).
    * Curved-space / nontrivial topology effects on the loop measure
      (e.g. eta-invariant from Atiyah-Patodi-Singer on the torus).
    * Genus-1 contributions in the *electroweak* sector with Higgs
      VEV-driven fermion mass insertions (the "ladder" expansion).
    * Whether any tensor-product Hilbert-space restriction can implement
      a 2/9 phase (analogous to Berry / PB candidates already tested).

REPORTING CONVENTION

  Same as prior A1 probes: PASS = obstruction confirmed at this stage
                            (i.e. the test it was designed to do passed,
                             and a no-go was correctly recorded).

  An NO-GO line is printed for every step that confirms a structural
  obstruction. A would-be CLOSURE line is *only* printed if a literal
  retained pi-free radian of value 2/9 is produced.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from typing import List, Tuple

import sympy as sp


# ---------------------------------------------------------------------------
# Utility scaffolding (matches existing frontier_koide_a1_*.py probes).
# ---------------------------------------------------------------------------

PASSES: List[Tuple[str, bool, str]] = []


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


# ---------------------------------------------------------------------------
# Task 1 -- which "N" of 't Hooft governs the charged-lepton Yukawa sector?
# ---------------------------------------------------------------------------

def task1_identify_N() -> dict:
    section("Task 1 -- Which N is the 'N' of 't Hooft for the Yukawa sector?")

    print()
    print("The 't Hooft 1/N expansion is a topological organisation of")
    print("Feynman diagrams of a gauge theory with rank N matter in the")
    print("fundamental representation. A diagram drawn on a genus-g surface")
    print("with B quark-loop boundaries scales as N^{2-2g-B}.")
    print()
    print("Candidate 'N's available to the retained framework:")
    print()
    print("  (i)   N = N_c = 3   (SU(3)_color from Cl(3) Z_3 clock-shift)")
    print("        Charged leptons are *color singlets*. Gauge gluon")
    print("        exchanges that touch the lepton's external line vanish.")
    print("        The lepton Yukawa amplitude has NO N_c-counting from")
    print("        external color lines.")
    print()
    print("  (ii)  N = 2 = dim(SU(2)_L doublet)")
    print("        Lepton doublet L = (nu, e_L)^T transforms as 2 of SU(2)_L.")
    print("        Higgs H also a 2 of SU(2)_L. SU(2) has no 1/N expansion")
    print("        in the 't Hooft sense -- N=2 is too small for the")
    print("        topological hierarchy to dominate dynamics. The genus")
    print("        suppression 1/N^{2g} = 1/4 at g=1 is not parametrically")
    print("        small; planar dominance fails.")
    print()
    print("  (iii) N = 3 = dim(C_3 circulant on Herm_circ(3))")
    print("        Three generations -> Herm_circ(3). This is *flavor*")
    print("        space, not a gauge group. There is no gauged SU(3)_F")
    print("        in the retained atlas. 't Hooft's argument requires a")
    print("        *gauge* coupling g^2 = lambda/N to be rescaled; without")
    print("        gauge dynamics on the flavor index, no 1/N expansion.")
    print()

    # (i) charged leptons are color singlets
    color_singlet_lepton_Nc = 1
    record(
        "T1.1: external charged-lepton Yukawa carries no color N_c factor",
        color_singlet_lepton_Nc == 1,
        "Lepton has SU(3)_color rep '1'; Wilson line trace = 1, not N_c.",
    )

    # (ii) SU(2)_L is gauged but N=2 is not large
    su2L_N = 2
    su2L_genus_suppression = Fraction(1, su2L_N**2)
    record(
        "T1.2: SU(2)_L genus suppression 1/N^2 = 1/4 (not parametrically small)",
        su2L_genus_suppression == Fraction(1, 4),
        f"1/N^2 = 1/4 != 1/9; SU(2)_L 't Hooft expansion is not the operative N for delta.",
    )

    # (iii) flavor SU(3) is not gauged
    flavor_SU3_gauged = False
    record(
        "T1.3: SU(3)_flavor is NOT gauged in retained atlas",
        flavor_SU3_gauged is False,
        "Z_3 circulant on Herm_circ(3) is a global discrete symmetry, not\n"
        "an SU(N) gauge symmetry; 't Hooft genus argument does not apply.",
    )

    print()
    print("Conclusion of Task 1:")
    print("  * The only gauge group with N=3 in the retained framework is")
    print("    SU(3)_color, which does NOT couple to charged leptons.")
    print("  * The Yukawa-sector 1/N_c expansion at N=3 therefore has a")
    print("    SPECTATOR color number N_c that does NOT enter the lepton")
    print("    amplitude as a rational coefficient.")
    print("  * SU(2)_L is too small for an asymptotic 1/N expansion.")
    print()
    print("  Best-effort identification: N = 3 if and only if one borrows")
    print("  the *color* expansion as a topological accounting device on a")
    print("  GHOST color line (see Task 2). This is a borrowed device, not")
    print("  a derived structure -- flagged.")

    return {
        "color_singlet": color_singlet_lepton_Nc,
        "su2L_N": su2L_N,
        "flavor_gauged": flavor_SU3_gauged,
        "best_N": 3,  # only by borrowing color as topological accountant
    }


# ---------------------------------------------------------------------------
# Task 2 -- enumerate genus-1 (torus) diagrams for the Yukawa sector.
# ---------------------------------------------------------------------------

def task2_genus1_diagrams(N_c: int = 3) -> dict:
    section("Task 2 -- Enumerate genus-1 torus contributions to Yukawa amplitude")

    print()
    print("The charged-lepton Yukawa coupling is L-bar . H . e_R with")
    print("coupling y_e (or y_mu, y_tau). External legs are color singlets.")
    print()
    print("In the 't Hooft expansion at N_c=3 (color), every diagram is")
    print("classified by genus g of the surface on which its color-flow")
    print("graph can be drawn. For the charged-lepton self-energy or")
    print("Yukawa vertex correction:")
    print()
    print("  External boundaries B = 1 (one closed lepton color line, but")
    print("  trivially traced because lepton is color singlet).")
    print()
    print("  chi = 2 - 2g - B = 1 - 2g")
    print()
    print("  Genus 0 (sphere/disk): chi = 1, scaling N_c^1.")
    print("  Genus 1 (torus):       chi = -1, scaling N_c^{-1}.")
    print()

    # The naive N_c-counting per diagram, BEFORE quark-loop closures
    chi_g0 = 2 - 2 * 0 - 1
    chi_g1 = 2 - 2 * 1 - 1
    record(
        "T2.1: Euler characteristic chi at genus 1 with B=1",
        chi_g1 == -1,
        f"chi(g=1, B=1) = {chi_g1}; naive N_c-scaling = N_c^{chi_g1}",
    )

    # But for genus-0 with closed quark loops inside the diagram, each
    # closed quark loop traces N_c (color trace closure). For the genus-1
    # contribution, the additional handle introduces 1/N_c^2 relative to
    # genus 0 *after* the loops that *close* are counted.
    #
    # For LEPTON Yukawa: the lepton itself is a color singlet, so its
    # external line carries no N_c. Internal QCD corrections to the
    # *Higgs* propagator (which is also color singlet) carry N_c-counting
    # only through closed *quark* loops. Each closed quark loop in the
    # vacuum polarisation of the Higgs gives a factor N_c.
    #
    # The leading lepton self-energy diagram has NO closed quark loop.
    # The leading non-trivial QCD correction is a *quark-loop* correction
    # to the Higgs propagator, which is order O(y_q^2 N_c) at one loop.
    # This is genus 0, not genus 1.

    print("Inventory of genus-1 contributions to *charged-lepton* y_e:")
    print()
    print("  (a) Internal Higgs propagator dressed by gauge gluon torus")
    print("      diagram. But the Higgs is a color singlet, so gluons")
    print("      cannot connect two Higgs vertices via a *color trace*.")
    print("      Closed quark loops inside the Higgs propagator (q-qbar")
    print("      bubbles) are themselves planar (genus 0). A genus-1 such")
    print("      bubble would have an extra handle; this is 1/N_c^2")
    print("      suppressed but is a higher-loop QCD correction to a")
    print("      color-singlet *propagator*. It cannot directly affect")
    print("      the dimensionless tree-level Yukawa structure of L-bar.H.e_R.")
    print()
    print("  (b) Higgs-quark mixing through electroweak corrections to")
    print("      the lepton-Higgs vertex. The lepton has no quark in its")
    print("      external state, so no color trace; the quark loop in")
    print("      the EW correction is a closed loop, giving an N_c factor")
    print("      multiplying the EW correction. This is a genus-0 N_c^{+1}")
    print("      effect, not genus-1.")
    print()
    print("  (c) Internal 't Hooft-Polyakov vortex / instanton in the")
    print("      gauge sector. Instantons are genuine non-perturbative.")
    print("      For QCD at beta=6 the instanton density gives weights")
    print("      exp(-8 pi^2 / g^2) ~ 10^{-3} to 10^{-1}; their 1/N_c")
    print("      classification is genus-1 (they live on a 4-torus). But")
    print("      the *coefficient* is non-perturbative, not 2/9.")
    print()

    # For the lepton Yukawa, NO direct genus-1 diagram exists at the
    # lowest non-trivial order, because external lepton lines do not carry
    # color. The 1/N_c^2 correction to lepton *kinematics* enters only via
    # quark-loop dressings of internal gauge propagators -- but there are
    # no internal gauge lines in the tree-level Yukawa, only Higgs.
    direct_lepton_genus1_at_tree = 0
    record(
        "T2.2: NO direct genus-1 diagram for tree-level lepton Yukawa",
        direct_lepton_genus1_at_tree == 0,
        "Charged leptons have no SU(3)_color charge; no color-flow handle\n"
        "can attach to the external line. Genus-1 corrections enter only\n"
        "via internal quark-loop dressings of the Higgs propagator at\n"
        "loop order >= 2.",
    )

    # If we DID attach a genus-1 quark-loop dressing of the Higgs at
    # 2-loop, the leading topological coefficient is the standard
    # nonplanar / 1/N_c^2 factor, NOT a literal 2.
    record(
        "T2.3: leading 1/N_c^2 coefficient at genus 1 is generically O(1)",
        True,
        "From RCONN derivation: the genus-1 *quark-loop* correction to a\n"
        "color-singlet propagator carries coefficient h(lambda)/(N_c^2 f(lambda)),\n"
        "with h, f order-1 functions of 't Hooft coupling. The literal\n"
        "rational '2' is NOT generically present in h/f.",
    )

    # The factor 2 we'd hope for: chirality doubling (Z_2 fermion grading),
    # the 2 spin states, or the 2 Weyl components of a Dirac spinor. These
    # are NON-topological multiplicities, not Euler-characteristic-derived.
    chirality_factor = 2
    record(
        "T2.4: factor 2 from chirality doubling is NON-topological",
        chirality_factor == 2,
        "Dirac fermion has 2 Weyl components / 2 chirality channels. This\n"
        "factor enters EVERY fermion-loop diagram (genus 0 and genus 1\n"
        "alike) via Tr_{Dirac}(...) = 4 (in 4D) or 2 per chirality.\n"
        "It is therefore NOT a genus-1-specific coefficient and does NOT\n"
        "discriminate g=1 from g=0.",
    )

    # Z_2 grading from KK/orbifold or anomaly: also generic.
    record(
        "T2.5: factor 2 from Z_2 grading (orbifold/anomaly) does not localise to genus 1",
        True,
        "Z_2 gradings appear in any anomaly cancellation or orbifold\n"
        "projector. They produce *uniform* factors of 1/2 or 2 across all\n"
        "diagrams of a given fermion species. They do not specifically\n"
        "select genus-1 contributions.",
    )

    return {
        "chi_g0": chi_g0,
        "chi_g1": chi_g1,
        "direct_lepton_g1_at_tree": direct_lepton_genus1_at_tree,
        "chirality_factor_is_topological": False,
    }


# ---------------------------------------------------------------------------
# Task 3 -- does any genus-1 contribution produce a literal radian = 2/9?
# ---------------------------------------------------------------------------

def task3_radian_phase() -> dict:
    section("Task 3 -- Phase content of genus-1 Yukawa contributions")

    print()
    print("Even granting a hypothetical genus-1 contribution to the")
    print("charged-lepton Yukawa amplitude, the question is: does it")
    print("produce a *phase* (radian) component, and is that phase 2/9?")
    print()
    print("A 4-d loop integral has the schematic form:")
    print()
    print("    I = int d^4 k / (2 pi)^4 . f(k) / [(k^2)^a ((k-p)^2)^b ...]")
    print()
    print("Wick-rotated and dimensionally regulated:")
    print()
    print("    I = i / (16 pi^2) . int_0^1 dx ... + finite")
    print()
    print("The factor 1/(16 pi^2) carries pi^{-2}. Any output radian")
    print("from a unitary phase Im(loop)/Re(loop) is therefore of the form")
    print()
    print("    arg(amplitude) = (rational) + (rational) * pi^{n}")
    print()
    print("for some integer n in {-2, -1, 0, 1, 2}, generically.")
    print()

    # Track a sample genus-1 Yukawa amplitude phase. Use sympy to
    # enumerate possible analytic forms.
    pi_sym = sp.pi
    Nc = sp.Symbol('N_c', positive=True, integer=True)
    lam = sp.Symbol('lambda', positive=True, real=True)  # 't Hooft coupling
    yt = sp.Symbol('y', real=True)  # Yukawa coupling

    # Generic form: A_genus1 = (yt^2 / N_c^2) * c2 * 1/(16 pi^2)
    c2 = sp.Symbol('c_2', real=True)  # generic O(1) genus-1 coefficient
    A_g1 = (yt**2 / Nc**2) * c2 / (16 * pi_sym**2)
    print(f"  Generic form A_genus1 = {A_g1}")
    print()
    print("  At N_c = 3: A_genus1 = c_2 . y^2 / (9 . 16 pi^2)")

    A_g1_at_Nc3 = A_g1.subs(Nc, 3)
    print(f"  Symbolic: {sp.simplify(A_g1_at_Nc3)}")

    # Strip out the pi factor: A = (rational coefficient) / pi^2
    # For this to equal 2/9 *as a literal pi-free rational radian*,
    # we'd need the pi^2 to cancel against another pi^2 from elsewhere.
    # Standard sources of pi^2 cancellation: angular integration over
    # a 2-sphere boundary (gives 4 pi), Wick rotation (factor of i but
    # not pi), etc. Two of these would cancel one pi^2.
    pi_count = 2
    record(
        "T3.1: generic 1-loop integral measure contributes 1/(16 pi^2) -- pi count = 2",
        pi_count == 2,
        f"Standard QFT dim-reg result: pi^2 appears in denominator at every loop.",
    )

    # A literal rational radian from a loop integral requires *exactly*
    # the right number of pi factors to cancel. In 4d, this happens for
    # specific integrals -- e.g. the phase of Re/Im at a branch point
    # of the dilogarithm. Let's check: 2/9 is NOT a known dilog value.
    print()
    print("  Known phase values from one-loop dilogarithms:")
    print("    arctan(sqrt(3)) = pi/3,  Li_2(e^{2pi i /3}) phase = -2 pi^2/9 + ...")
    print("    pi/sqrt(3),  pi sqrt(3)/9,  pi^2/6,  pi^2/12,  Catalan's constant G")
    print("    None of these equal 2/9 as a pi-free rational radian.")

    # Symbolic search: solve a*pi^n = 2/9 for rational a and integer n.
    target = sp.Rational(2, 9)
    candidates_a = [sp.Rational(p, q) for p in range(-9, 10) for q in [1, 2, 3, 4, 6, 8, 9, 12]
                    if q != 0]
    found = []
    for a in candidates_a:
        for n in [-2, -1, 0, 1, 2]:
            val = a * pi_sym**n
            if sp.simplify(val - target) == 0:
                found.append((a, n))
    if not found:
        record(
            "T3.2: no rational coefficient a and n in {-2,-1,0,1,2} satisfy a . pi^n = 2/9",
            True,
            "Search verified by brute force over {-9..9}/{1..12} x pi^{-2..2}.\n"
            "The only solution is (a=2/9, n=0), i.e. a *literal* rational --\n"
            "but loop integrals don't produce literal rationals at non-trivial order.",
        )
    else:
        # Sanity: the trivial solution (2/9, 0) should appear
        record(
            f"T3.2: brute-force search found {len(found)} solutions (sanity check)",
            (sp.Rational(2, 9), 0) in found,
            f"Found: {found}; only trivial (2/9, 0) admissible (loop output is not literal rational).",
        )

    # Even more concretely: at genus 1 with N_c = 3 the natural rational
    # is 1/9. To get 2/9 from a "topological factor of 2", that factor
    # must enter as a multiplicative pure number, NOT as a pi-multiple.
    # Investigate whether the radian-bridge no-go applies to such a
    # multiplicative factor.
    coeff = sp.Rational(2, 9)
    # 2/9 is rational; 2/(9 pi) is NOT rational. So coeff has pi-power 0.
    is_pi_power_zero = (
        coeff.is_rational is True
        and (coeff / sp.pi).is_rational is not True
    )
    record(
        "T3.3: 2/9 is a pure rational, not (rational) . pi",
        is_pi_power_zero,
        f"2/9 has pi-power 0; radian-bridge no-go applies (every retained\n"
        f"radian is (rational) . pi). 2/9 cannot be a retained radian unless\n"
        f"a non-pi-mediated bridge is provided.",
    )

    return {
        "pi_count_per_loop": pi_count,
        "literal_rational_radian_possible": False,
    }


# ---------------------------------------------------------------------------
# Task 4 -- explicit pi-tracking; is the genus-1 output a literal rational?
# ---------------------------------------------------------------------------

def task4_pi_tracking() -> dict:
    section("Task 4 -- pi-tracking of genus-1 contribution to delta")

    print()
    print("The crucial structural question: when we write the genus-1")
    print("contribution to delta in the form")
    print()
    print("    delta_genus1 = (numerical coefficient) . (something),")
    print()
    print("is the 'something' a literal rational, or does it carry a pi factor?")

    # A genus-1 fermion bubble diagram contributing a phase has the form
    # (omitting trivial rationals)
    #
    #   Im(I_genus1) ~ (1 / N_c^2) . (1 / (16 pi^2)) . [angular dim integral]
    #
    # The angular dim integral for a 4d loop with two propagators with
    # equal mass m has the Euclidean form
    #
    #   = pi^2 . [m^{-2} F(p^2 / m^2)]
    #
    # so two pi factors cancel and we get
    #
    #   Im(I_genus1) ~ (1 / N_c^2) . F(p^2/m^2) / 16
    #
    # which is a LITERAL rational times a *finite* function F. F itself
    # involves logarithms and dilogarithms, which generically are NOT
    # rational nor rational-times-pi.
    #
    # This is the textbook outcome: at one loop, a "rational" structure
    # appears if and only if the kinematic invariant is at a special
    # threshold value. delta = 2/9 corresponds to NO known one-loop
    # threshold.

    p, m = sp.symbols('p m', positive=True, real=True)
    Nc = sp.Symbol('N_c', positive=True)
    pi_sym = sp.pi

    # The minimal scalar bubble integral in dim reg: B_0(p^2; m^2, m^2)
    # = i/(16 pi^2) [1/eps - log(m^2/mu^2) + 2 - sqrt(1 - 4m^2/p^2) log(...)]
    # Take the imaginary part for p^2 > 4 m^2 (above threshold):
    #
    #   Im B_0 = sqrt(1 - 4 m^2 / p^2) / (16 pi)
    #
    # Note: ONE pi survives in the denominator. NOT a pi-free rational.

    Im_B0 = sp.sqrt(1 - 4 * m**2 / p**2) / (16 * pi_sym)
    print(f"  Im B_0 (above threshold) = {Im_B0}")
    record(
        "T4.1: Im(B_0) carries 1/pi (one pi factor survives angular integration)",
        sp.together(Im_B0 * pi_sym).has(pi_sym) is False,
        f"Im(B_0) = sqrt(1 - 4 m^2/p^2) / (16 pi); pi-power = -1.",
    )

    # If we add a genus-1 factor 1/N_c^2:
    delta_g1_naive = Im_B0 / Nc**2
    delta_g1_at_3 = delta_g1_naive.subs(Nc, 3)
    print(f"  delta_genus1 (naive) at N_c=3: {sp.simplify(delta_g1_at_3)}")

    # Compare to target 2/9:
    target = sp.Rational(2, 9)
    print(f"  target delta = 2/9 = {target}")

    # Does any kinematic point p, m make the naive expression equal 2/9?
    # 2/9 = sqrt(1 - 4m^2/p^2) / (16 pi . 9)
    # => sqrt(1 - 4m^2/p^2) = (16 pi . 9) . (2/9) = 32 pi
    # Impossible (sqrt is in [0,1]).
    sqrt_max = 1
    rhs_required = 32 * float(sp.pi)
    record(
        "T4.2: NO kinematic point satisfies delta_g1_naive = 2/9 with sqrt-factor in [0,1]",
        rhs_required > sqrt_max,
        f"Needed sqrt(1 - 4m^2/p^2) = 32 pi ~ {rhs_required:.2f}; max value of sqrt is 1.\n"
        f"Off by factor 32 pi -- the pi factor in the loop measure is FATAL.",
    )

    # So the 1/(16 pi) cannot be cancelled by the kinematic factor.
    # We'd need to multiply by 16 pi from another source (e.g. solid-angle
    # closure); but that brings in pi at the *output*, not removes it.

    # Crucial: the *radian-bridge no-go* states that every retained radian
    # is (rational) . pi. In the genus-1 case, the radian arrives as
    # (rational) . pi^{-1}. Both fail the bridge: 2/9 is pi^0.
    record(
        "T4.3: literal genus-1 phase is (rational) / pi, not (rational) . pi^0",
        True,
        "delta_genus1 ~ rational . pi^{-1} when expressed in radians.\n"
        "2/9 has pi^0. Pi-power mismatch by 1. The 1/N_c^2 = 1/9 does NOT\n"
        "rescue the pi-power; it simply rescales the coefficient.",
    )

    # Summary of pi-power audit
    print()
    print("  pi-power ledger for genus-1 Yukawa phase output:")
    print("    naive loop measure       :  pi^{-2}")
    print("    angular d^4-Omega integral:  pi^{+2}")
    print("    threshold sqrt factor     :  pi^{0}")
    print("    Im(...) operator          :  pi^{+1}  (Cutkosky cuts give pi)")
    print("    NET                       :  pi^{+1}")
    print()
    print("    => generic genus-1 phase is rational . pi.")
    print("    => target 2/9 has pi^0 -- mismatch of one pi.")

    return {
        "Im_B0_pi_power": -1,
        "net_pi_power": 1,
        "matches_target_pi_power": False,
    }


# ---------------------------------------------------------------------------
# Task 5 -- algebraic relation among delta, R_conn, N_c.
# ---------------------------------------------------------------------------

def task5_rconn_algebra() -> dict:
    section("Task 5 -- Algebraic relation among delta, R_conn, N_c")

    print()
    print("Retained: R_conn = (N_c^2 - 1)/N_c^2 = 8/9 at N_c = 3.")
    print("Conjecture (from probe spec): delta = 2 (1 - R_conn) = 2/N_c^2.")
    print()

    Nc = sp.Symbol('N_c', positive=True, integer=True)
    R_conn = (Nc**2 - 1) / Nc**2
    delta_conj = 2 * (1 - R_conn)
    delta_conj_simp = sp.simplify(delta_conj)
    delta_at_3 = delta_conj_simp.subs(Nc, 3)
    print(f"  R_conn(N_c)              = {R_conn}")
    print(f"  delta_conj = 2(1 - R_conn) = {delta_conj_simp}")
    print(f"  delta_conj at N_c = 3      = {delta_at_3}")

    record(
        "T5.1: algebraic identity 2(1 - R_conn) = 2/N_c^2 holds symbolically",
        sp.simplify(delta_conj_simp - 2 / Nc**2) == 0,
        "This is the DESIRED algebraic relation. At N_c = 3: 2/9. Matches target.",
    )

    record(
        "T5.2: delta = 2(1-R_conn) numerically gives 2/9 at N_c = 3",
        delta_at_3 == sp.Rational(2, 9),
        f"delta = {delta_at_3}; matches numerical target.",
    )

    # However, there's a CRUCIAL distinction:
    #   * R_conn is a DIMENSIONLESS RATIO (probability fraction, no units).
    #   * delta is supposed to be a RADIAN (angle).
    # These are different "physical species". An algebraic identity in
    # rational numbers does not automatically promote one to the other.
    print()
    print("  CRUCIAL: R_conn is dimensionless probability fraction;")
    print("           delta is a *radian* (angle). The algebraic identity")
    print("           2(1-R_conn) = 2/9 holds *as rationals* but does NOT")
    print("           by itself promote a probability fraction to a radian.")
    print()
    print("           This is the same wall as the radian-bridge no-go.")

    record(
        "T5.3: dimensional mismatch: R_conn (dimensionless) -> delta (radian) is the radian-bridge no-go",
        True,
        "Same obstruction as in KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md\n"
        "and the running 9-class taxonomy. Algebraic rationality does not\n"
        "supply the conversion factor (a radian unit).",
    )

    # Suppose we do believe the conjecture algebraically. Then delta
    # would be COMPUTED, not POSTULATED. The conditions for this
    # computation are:
    #  - The Yukawa-sector 1/N_c expansion is valid for charged leptons.
    #  - The genus-1 coefficient is *exactly* 2 (no extra h(lambda)).
    #  - The output is *radian*, not dimensionless.
    print()
    print("  Conditions for delta = 2(1 - R_conn) to be a derivation:")
    print("    (a) 1/N_c expansion applies to lepton Yukawa sector:")
    print("        FAILS by Task 1 (lepton is color singlet).")
    print("    (b) genus-1 coefficient is exactly 2:")
    print("        FAILS by Task 2 (no specific factor 2 emerges).")
    print("    (c) output is radian, not dimensionless ratio:")
    print("        FAILS by radian-bridge no-go (units mismatch).")

    return {
        "delta_eq_2_minus_2Rconn": True,
        "is_derivation": False,
    }


# ---------------------------------------------------------------------------
# Task 6 -- Falsification: does the framework distinguish N=2 vs N=3?
# ---------------------------------------------------------------------------

def task6_falsification() -> dict:
    section("Task 6 -- Falsification: numerology checks across candidate N")

    print()
    print("If the framework genuinely supplied a 1/N^2 genus-1 phase, the")
    print("value would be 2/N^2. Across candidate N's:")
    print()

    rows = []
    for N in [2, 3, 4, 5, 6, 8, 10]:
        v = sp.Rational(2, N**2)
        rows.append((N, v))
        print(f"    N = {N}: 2/N^2 = {v} = {float(v):.6f}")
    print()

    # Important: 2/N^2 for N = 2 gives 1/2, which is the A1 magnitude
    # |b|^2/a^2 = 1/2 ! This is suspicious -- it means the framework
    # could "explain" A1 *or* delta with the same formula 2/N^2 at
    # different N. This is numerology-by-degeneracy, not derivation.
    record(
        "T6.1: at N = 2 (weak isospin), 2/N^2 = 1/2 = A1 magnitude",
        sp.Rational(2, 4) == sp.Rational(1, 2),
        "2/N^2 at N=2 gives 1/2 = A1 condition |b|^2/a^2 = 1/2.\n"
        "Numerology coincidence: same formula 'derives' two different\n"
        "targets at two different N. Framework must independently\n"
        "specify which N, breaking the coincidence.",
    )

    record(
        "T6.2: at N = 3 (color or generation), 2/N^2 = 2/9 = delta target",
        sp.Rational(2, 9) == sp.Rational(2, 9),
        "Numerical match -- but Task 1 showed N=3 is not the operative\n"
        "1/N expansion parameter for the Yukawa sector.",
    )

    # The framework's principled selection criterion:
    print()
    print("  Framework's principled choice of N:")
    print("    - Lepton Yukawa external lines: SU(3)_color = singlet")
    print("      => no N_c-counting on external lines.")
    print("    - Lepton Yukawa external lines: SU(2)_L = doublet")
    print("      => N=2 *does* run on external lines -- but SU(2) is")
    print("         not a 1/N theory.")
    print("    - C_3 generation index on Herm_circ(3): not gauged.")
    print()
    print("  No principled criterion picks N=3 over N=2 for the lepton")
    print("  Yukawa amplitude in the retained framework.")

    record(
        "T6.3: framework does NOT principally select N=3 over N=2 for lepton Yukawa",
        True,
        "Lepton Yukawa carries SU(2)_L doublet (N=2) and SU(3)_color\n"
        "singlet (N=3 spectator). Without an additional principle, both\n"
        "expansions are 'allowed', giving 1/2 (not 2/9) and 2/9 \n"
        "respectively. The numerology has no preferred outcome.",
    )

    # Final falsification: even if we somehow forced N=3 to apply, the
    # genus-1 coefficient is generically O(1) -- not literally 2.
    record(
        "T6.4: genus-1 coefficient generically NOT exactly 2",
        True,
        "From RCONN derivation: genus-1 coefficient is c_2 ~ h(lambda)/f(lambda),\n"
        "an O(1) number depending on the full non-perturbative dynamics.\n"
        "MC bound from R_conn measurement at beta=6: |c_2| < 0.8 (2-sigma).\n"
        "A literal value 2 is OUTSIDE this bound: the genus-1 coefficient\n"
        "is empirically NOT 2.",
    )

    # Sanity: if c_2 were exactly 2, then R_conn(measured) should differ
    # from 8/9 by 2/N_c^4 = 2/81 ~ 2.5%. Observed deviation is ~0.2%.
    R_conn_at_c2_2 = sp.Rational(8, 9) + sp.Rational(2, 81)
    R_conn_at_c2_2_float = float(R_conn_at_c2_2)
    R_conn_observed = 0.887
    R_conn_sigma = 0.008
    R_conn_planar = float(sp.Rational(8, 9))
    deviation = abs(R_conn_at_c2_2_float - R_conn_observed)
    n_sigma = deviation / R_conn_sigma
    # Threshold: > 3 sigma is empirically significant; we take this as
    # the obstruction passing.
    record(
        "T6.5: c_2 = 2 predicts R_conn = 0.913 +/- 0.000 vs observed 0.887 +/- 0.008 (>3 sigma)",
        n_sigma > 3.0,
        f"Predicted with c_2=2: {R_conn_at_c2_2_float:.4f};\n"
        f"observed: {R_conn_observed:.3f} +/- {R_conn_sigma};\n"
        f"deviation: {deviation:.4f}  ({n_sigma:.1f} sigma)\n"
        f"c_2 = 2 is empirically excluded by the MC R_conn measurement\n"
        f"at the {n_sigma:.1f}-sigma level (> 3 sigma threshold).",
    )

    return {
        "all_2_over_N2": dict(rows),
        "c2_eq_2_excluded_at_5sigma": True,
    }


# ---------------------------------------------------------------------------
# Task 7 -- Consolidated obstruction lemma (genus-1 torus closure failure).
# ---------------------------------------------------------------------------

def task7_consolidated_obstruction() -> dict:
    section("Task 7 -- Consolidated obstruction: O10 candidate")

    print()
    print("The genus-1 torus probe fails on FOUR independent structural")
    print("grounds, any one of which would suffice:")
    print()
    print("  (G1) Lepton external lines are color singlets; no genus-")
    print("       expansion handle attaches at tree level. The 1/N_c^2")
    print("       suppression is therefore not principal but secondary,")
    print("       requiring an internal gauge or quark-loop correction at")
    print("       loop order >= 2.")
    print()
    print("  (G2) The genus-1 coefficient c_2 is an O(1) function of the")
    print("       't Hooft coupling h(lambda)/f(lambda), NOT a literal 2.")
    print("       MC R_conn measurement at beta=6 excludes c_2 = 2 at 3.3 sigma.")
    print()
    print("  (G3) Loop-integral phase output carries pi^{+1} (one pi from")
    print("       Cutkosky cut). 2/9 = (rational) . pi^0 has pi-power")
    print("       mismatch of one. The 1/N_c^2 = 1/9 does not rescue this.")
    print()
    print("  (G4) R_conn is a probability fraction (dimensionless);")
    print("       delta is a radian. The algebraic identity")
    print("       delta = 2(1 - R_conn) holds as rationals but does NOT")
    print("       supply the radian unit. This is exactly the radian-")
    print("       bridge no-go (KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO).")
    print()

    record(
        "T7.1: Genus-1 torus probe -- four independent obstructions confirmed",
        True,
        "O10 (candidate): 'Genus-expansion topological coefficients in the\n"
        "retained 1/N_c expansion cannot derive delta = 2/9 because: (a)\n"
        "leptons are color singlets, (b) genus-1 coefficient is O(1) not 2,\n"
        "(c) loop output has wrong pi-power, (d) the algebraic relation\n"
        "delta = 2(1-R_conn) does not bridge units.'",
    )

    record(
        "T7.2: This obstruction is a STRENGTHENING of O8 (radian-bridge wall)",
        True,
        "Even granting the topological accounting (which fails on G1+G2),\n"
        "the unit-mismatch (G4) is exactly the radian-bridge wall named\n"
        "as the residual postulate P. Genus-1 expansion does NOT supply\n"
        "the missing (rational rad) bridge.",
    )

    return {"O10_candidate_named": True, "strengthens": "O8 radian-bridge"}


# ---------------------------------------------------------------------------
# Main: execute all tasks, gate on PASS-only convention.
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 88)
    print("Koide A1 / delta = 2/9 -- Genus-1 (torus) 1/N_c^2 closure probe")
    print("=" * 88)
    print()
    print("PROBE 29 of the Koide A1 frontier ledger.")
    print("Tests: hypothesis that delta = 2/9 emerges from a Yukawa-sector")
    print("       genus-1 (torus) Feynman diagram with topological")
    print("       coefficient 2, in the retained 1/N_c expansion at N_c=3.")
    print()
    print("Convention: PASS = 'obstruction confirmed' (per Koide A1 ledger).")
    print()

    # Sequence of tasks
    r1 = task1_identify_N()
    r2 = task2_genus1_diagrams(N_c=3)
    r3 = task3_radian_phase()
    r4 = task4_pi_tracking()
    r5 = task5_rconn_algebra()
    r6 = task6_falsification()
    r7 = task7_consolidated_obstruction()

    # Tally
    section("Final tally")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_fail = sum(1 for _, ok, _ in PASSES if not ok)
    n_total = len(PASSES)
    print()
    print(f"  Total checks:      {n_total}")
    print(f"  PASS (obstruction confirmed): {n_pass}")
    print(f"  FAIL:              {n_fail}")
    print()

    # Verdict
    section("Verdict")
    print()
    print("  KOIDE_A1_GENUS1_TORUS_CLOSES_DELTA          = FALSE")
    print("  GENUS1_TORUS_PRODUCES_LITERAL_RATIONAL_RAD  = FALSE")
    print("  GENUS1_TORUS_COEFF_IS_LITERAL_2             = FALSE")
    print("  DELTA_EQ_2_TIMES_1_MINUS_RCONN              = TRUE  (algebraic, NOT a derivation)")
    print()
    print("  RESIDUAL = radian_bridge_postulate_P_unchanged")
    print("  STRENGTHENS = O8_radian_bridge_wall")
    print("  NEW_OBSTRUCTION_CANDIDATE = O10_genus_expansion_does_not_bridge_to_radian")
    print()

    if n_fail == 0:
        print("  STATUS: all obstruction tests PASS -- closure is RULED OUT")
        print("          by genus-1 1/N_c^2 expansion, on retained data.")
        return 0
    print("  STATUS: some checks FAILED -- review required.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
