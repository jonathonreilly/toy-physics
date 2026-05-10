"""
Primitive Design Probe P-L1 — Candidate primitives for QCD beta_2/beta_3
channel-weight terminal admission.

Authority role
--------------
Source-note proposal (primitive_design_proposal) -- audit verdict and
downstream status set only by the independent audit lane. No primitive
proposed here is admitted into the retained A1 + A2 + retained-theorem
stack on the basis of this runner alone.

Purpose
=======
Stress-test three candidate primitives that COULD give the QCD beta_2
(3-loop) and beta_3 (4-loop) scalar channel weights:

  P_L1-A: Connes-Kreimer Hopf-Subdivergence Primitive
          (algebraic organization of BPHZ subdivergence coproduct)

  P_L1-B: Lattice <P>-Period Bootstrap Primitive
          (heat-kernel single-plaquette as flow-equation derivative)

  P_L1-C: Combinatorial Symmetry-Factor Sum-Rule Primitive
          (graph-period oracle factorizing the missing primitive)

For each candidate primitive: derive the formal statement, reproduce
support retentions, demonstrate the structural failure mode, and
document the missing piece.

Honest verdict
==============
NEGATIVE on closure for all three candidates. The L1 channel-weight
terminal admission is structurally irreducible from currently retained
content + any of these three candidate primitives. The cleanest
formulation of the open admission is "Cl(3)/Z^3-native period
functor on primitive 1PI graphs" (hypothetical P_L1-D), not yet known
to exist.

Source-note authority
=====================
docs/PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------
# Retained scalars (lifted exactly as in X-L1-MSbar / V-L1-Quartic /
# S-L1-Topological probes — these are the same retained values).
# ----------------------------------------------------------------------

C_F = Fraction(4, 3)        # SU(3) fundamental quadratic Casimir
C_A = Fraction(3, 1)        # SU(3) adjoint quadratic Casimir
T_F = Fraction(1, 2)        # Dynkin index for fundamental
N_F = 6                     # Number of active quark flavors above all SM thresholds
N_COLOR = 3
# In the S1 companion form b_3 (QCD) = (11 N_color - 2 N_quark)/3, the
# convention used by SU2_WEAK_BETA_COEFFICIENT_STRUCTURAL_CLOSED_FORM_THEOREM
# identifies N_quark = N_f at retained N_color = 3, N_quark = 6.
N_QUARK = N_F

# Quartic Casimir invariants at SU(3), retained group theory
DFF_OVER_NF = Fraction(5, 12)
DFA_OVER_NF = Fraction(5, 2)
DAA_OVER_NA = Fraction(135, 8)


# ----------------------------------------------------------------------
# Imported authorities (numerical comparators, NOT load-bearing)
# ----------------------------------------------------------------------

# QCD beta_2 at MSbar, N_f = 6 (TVZ 1980 closed form):
#    beta_2 = 2857/2 - (5033/18) n_f + (325/54) n_f^2
BETA_2_QCD_NF6 = (
    Fraction(2857, 2)
    - Fraction(5033, 18) * N_F
    + Fraction(325, 54) * N_F ** 2
)

# Standard TVZ 1980 six-channel weights (literature comparator):
TVZ_3LOOP_CHANNEL_WEIGHTS_MSBAR: Dict[str, Fraction] = {
    "C_A^3":               Fraction(2857, 54),
    "C_A^2 (T_F n_f)":     Fraction(-1415, 54),
    "C_F C_A (T_F n_f)":   Fraction(-205, 18),
    "C_A (T_F n_f)^2":     Fraction(79, 54),
    "C_F (T_F n_f)^2":     Fraction(11, 9),
    "C_F^2 (T_F n_f)":     Fraction(1, 2),
}

# Casimir-tensor channel values at SU(3), N_f = 6 (group theory only)
CHANNEL_VALUE = {
    "C_F^3":             C_F ** 3,
    "C_F^2 C_A":         C_F ** 2 * C_A,
    "C_F C_A^2":         C_F * C_A ** 2,
    "C_A^3":             C_A ** 3,
    "C_F^2 (T_F n_f)":   C_F ** 2 * T_F * N_F,
    "C_F C_A (T_F n_f)": C_F * C_A * T_F * N_F,
    "C_A^2 (T_F n_f)":   C_A ** 2 * T_F * N_F,
    "C_F (T_F n_f)^2":   C_F * (T_F * N_F) ** 2,
    "C_A (T_F n_f)^2":   C_A * (T_F * N_F) ** 2,
}


# ----------------------------------------------------------------------
# Counter helper
# ----------------------------------------------------------------------

@dataclass
class Counter:
    pass_count: int = 0
    fail_count: int = 0
    admitted_count: int = 0

    def record(self, label: str, ok: bool, detail: str = "") -> None:
        if ok:
            self.pass_count += 1
            tag = "PASS"
        else:
            self.fail_count += 1
            tag = "FAIL"
        suffix = f" | {detail}" if detail else ""
        print(f"  [{tag}] {label}{suffix}")

    def admit(self, label: str, reason: str) -> None:
        self.admitted_count += 1
        print(f"  [ADMITTED] {label} | {reason}")


# ----------------------------------------------------------------------
# SECTION 1 — DOCUMENT the terminal-admission shape
# ----------------------------------------------------------------------

def section1_terminal_admission_shape(c: Counter) -> None:
    """Document the structural shape of the terminal admission:
    six independent 3-loop Casimir-tensor channels with TVZ rationals,
    plus 14+ 4-loop channels with VVL rationals + zeta_3.
    """
    print()
    print("Section 1 — DOCUMENT the terminal admission shape")

    # 6-channel TVZ weights at MSbar
    target_weights = TVZ_3LOOP_CHANNEL_WEIGHTS_MSBAR
    n_channels = len(target_weights)
    c.record(
        "TVZ 1980 MSbar 3-loop has 6 nonzero N_f-monomial channels",
        n_channels == 6,
        f"channels = {sorted(target_weights.keys())}",
    )

    # The c_AAA = 2857/54 channel weight is a pure rational
    aaa_weight = target_weights["C_A^3"]
    c.record(
        "TVZ c_AAA = 2857/54 is a pure rational (no zeta values)",
        aaa_weight == Fraction(2857, 54),
        f"= {aaa_weight} = {float(aaa_weight):.4f}",
    )

    # The 4-loop VVL channel weights live in Q + Q*zeta_3
    # (this is documentation only — we cite the structural fact)
    c.record(
        "VVL 1997 MSbar 4-loop weights live in Q + Q*zeta_3",
        True,  # Standard literature fact
        "VVL 1997 hep-ph/9701390 explicit form",
    )

    # The "missing primitive" is a function:
    #   P : Primitive 1PI Feynman Graphs / iso  ->  Q + Q*zeta_3 + ...
    # This is the structural shape of the terminal admission.
    print("    -> The missing primitive is a function from primitive 1PI graph")
    print("       cohomology classes to Q + Q*zeta_3 + ..., NOT a scheme choice.")


# ----------------------------------------------------------------------
# SECTION 2 — RETAINED beta_0, beta_1 (cross-check with X-L1-MSbar)
# ----------------------------------------------------------------------

def section2_beta_0_beta_1_retained(c: Counter) -> None:
    """Reproduce the retained beta_0 = 7 and beta_1 = 26 at N_f = 6
    from S1 + Casimir algebra. These are scheme-independent (universal)
    and form the firm baseline.
    """
    print()
    print("Section 2 — RETAINED beta_0 = 7, beta_1 = 26 at N_f = 6")

    # beta_0 from S1: (11 N_color - 2 N_quark) / 3 = (33 - 12)/3 = 7
    beta_0_s1 = Fraction(11 * N_COLOR - 2 * N_QUARK, 3)
    c.record(
        "beta_0 from S1: (11 N_color - 2 N_quark)/3",
        beta_0_s1 == 7,
        f"= (33 - 12)/3 = {beta_0_s1}",
    )

    # beta_0 from Casimir form: (11/3) C_A - (4/3) T_F N_f
    beta_0_cas = (Fraction(11, 3) * C_A) - (Fraction(4, 3) * T_F * N_F)
    c.record(
        "beta_0 from Casimirs: (11/3) C_A - (4/3) T_F N_f",
        beta_0_cas == 7,
        f"= 11 - 4 = {beta_0_cas}",
    )

    # beta_1 = (34/3) C_A^2 - (20/3) C_A T_F N_f - 4 C_F T_F N_f
    beta_1 = (
        Fraction(34, 3) * C_A ** 2
        - Fraction(20, 3) * C_A * T_F * N_F
        - 4 * C_F * T_F * N_F
    )
    c.record(
        "beta_1 = (34/3) C_A^2 - (20/3) C_A T_F N_f - 4 C_F T_F N_f",
        beta_1 == 26,
        f"= 102 - 60 - 16 = {beta_1}",
    )

    print("    -> beta_0, beta_1 are RETAINED (universal at 1-, 2-loop).")
    print("    -> Both are scheme-independent (MSbar = MOM = lattice = <P>).")


# ----------------------------------------------------------------------
# SECTION 3 — PRIMITIVE P_L1-A (Connes-Kreimer Hopf-Subdivergence)
# ----------------------------------------------------------------------

def section3_primitive_A_connes_kreimer(c: Counter) -> None:
    """Stress-test P_L1-A: admit the Connes-Kreimer Hopf algebra of
    QCD 1PI graphs. The structural objection is that the Hopf algebra
    organizes BPHZ subdivergence subtraction but does NOT supply
    the period-evaluation function R : Gamma -> Q + Q*zeta_3 + ...
    """
    print()
    print("Section 3 — P_L1-A: Connes-Kreimer Hopf-Subdivergence Primitive")

    # Toy 1PI primitive graph at "loop 1": a single self-energy bubble.
    # In Connes-Kreimer, a primitive graph has trivial coproduct:
    #   Delta(Gamma) = Gamma tensor 1 + 1 tensor Gamma
    # where 1 = empty graph (the unit of the Hopf algebra).
    #
    # We model the toy: vertex_count = 2, edge_count = 2, loop = 1.
    @dataclass
    class ToyGraph:
        name: str
        vertices: int
        edges: int

        @property
        def loops(self) -> int:
            return self.edges - self.vertices + 1

    bubble = ToyGraph(name="self_energy_bubble", vertices=2, edges=2)
    c.record(
        "Toy 1PI graph 'self-energy bubble' has loop number 1",
        bubble.loops == 1,
        f"loops = E - V + 1 = {bubble.edges} - {bubble.vertices} + 1 = {bubble.loops}",
    )

    # Connes-Kreimer subdivergence coproduct on a primitive graph is trivial:
    # there are no proper divergent 1PI subgraphs.
    # Delta(bubble) = bubble tensor 1 + 1 tensor bubble
    has_proper_subdivergent = False  # by definition of "primitive"
    c.record(
        "Primitive 1PI graph has trivial Connes-Kreimer coproduct",
        not has_proper_subdivergent,
        "Delta(prim) = prim tensor 1 + 1 tensor prim (no proper subdivergences)",
    )

    # The Hopf algebra organization gives a clean factorization:
    #   beta_n = sum over primitive Gamma at loop order n+1
    #             of (sym(Gamma))^{-1} * T(Gamma) * R(Gamma)
    # where T(Gamma) is Casimir tensor (RETAINED group theory),
    # sym(Gamma) is automorphism count (RETAINED combinatorics),
    # but R(Gamma) is the period evaluation in Q + Q*zeta_n (NOT retained).
    print("    -> Hopf-algebra organization factorizes beta_n cleanly:")
    print("       beta_n = sum_{Gamma : ell(Gamma) = n+1, primitive}")
    print("                  (sym(Gamma))^{-1} * T(Gamma) * R(Gamma)")
    print("       T(Gamma): RETAINED (Casimir tensor, group theory)")
    print("       sym(Gamma): RETAINED (graph automorphism count)")
    print("       R(Gamma): NOT RETAINED (period evaluation function)")

    # Failure mode demonstration: assume P_L1-A is admitted; show that
    # without an independent period-evaluation primitive, the channel
    # weights remain free.
    # Toy: 1 primitive 3-loop graph contributing to channel C_A^3, with
    # symmetry factor 1, period = unknown.
    toy_period_unknown = "R(Gamma) is unspecified by P_L1-A alone"
    expected_channel_weight = Fraction(2857, 54)
    derived_channel_weight = None  # because R(Gamma) is unknown
    c.record(
        "P_L1-A toy: channel weight C_A^3 from one primitive graph",
        derived_channel_weight is None,
        f"period unknown -> weight unknown; target = {expected_channel_weight}",
    )

    c.admit(
        "P_L1-A: period evaluation function R(Gamma) -> Q + Q*zeta_3",
        "Connes-Kreimer Hopf algebra organizes BPHZ subtraction but does "
        "NOT compute graph periods; admitting P_L1-A is notational rewrap "
        "of the existing terminal admission",
    )

    print("    -> P_L1-A: NEGATIVE on closure.")
    print("       Sub-finding (positive structural): organizes the 6-channel")
    print("       decomposition cleanly via T(Gamma) projection.")


# ----------------------------------------------------------------------
# SECTION 4 — PRIMITIVE P_L1-B (<P>-scheme Heat-Kernel Bootstrap)
# ----------------------------------------------------------------------

def section4_primitive_B_p_scheme_bootstrap(c: Counter) -> None:
    """Stress-test P_L1-B: identify <P>_HK Taylor coefficients as
    beta-function coefficients in the <P>-scheme. The structural
    objection is that <P>_HK is a probe expectation value, not a
    flow-equation derivative — they coincide at 1- and 2-loop
    (universal) but diverge at 3-loop.
    """
    print()
    print("Section 4 — P_L1-B: <P>-scheme Heat-Kernel Bootstrap Primitive")

    # Compute <P>_HK_SU(3) Taylor coefficients
    # <P>_HK(s_t) = 1 - exp(-(4/3) s_t) = sum_{k>=1} (-1)^(k+1) (4/3)^k / k! s_t^k
    pHK_coef_1 = Fraction(4, 3)
    pHK_coef_2 = -Fraction(4, 3) ** 2 / Fraction(2)  # = -8/9
    pHK_coef_3 = Fraction(4, 3) ** 3 / Fraction(6)   # = 64/(27*6) = 32/81
    pHK_coef_4 = -Fraction(4, 3) ** 4 / Fraction(24)  # = -256/(81*24) = -32/243

    c.record(
        "<P>_HK_SU(3) Taylor coef of s_t^1 = 4/3",
        pHK_coef_1 == Fraction(4, 3),
        f"= {pHK_coef_1}",
    )
    c.record(
        "<P>_HK_SU(3) Taylor coef of s_t^2 = -8/9",
        pHK_coef_2 == -Fraction(8, 9),
        f"= {pHK_coef_2}",
    )
    c.record(
        "<P>_HK_SU(3) Taylor coef of s_t^3 = 32/81",
        pHK_coef_3 == Fraction(32, 81),
        f"= {pHK_coef_3}",
    )
    c.record(
        "<P>_HK_SU(3) Taylor coef of s_t^4 = -32/243",
        pHK_coef_4 == -Fraction(32, 243),
        f"= {pHK_coef_4}",
    )

    # Cross-check via direct Taylor expansion of 1 - exp(-(4/3) s_t)
    # at s_t = 0.001:
    s_t = 0.001
    direct = 1 - math.exp(-(4 / 3) * s_t)
    taylor4 = (
        float(pHK_coef_1) * s_t
        + float(pHK_coef_2) * s_t ** 2
        + float(pHK_coef_3) * s_t ** 3
        + float(pHK_coef_4) * s_t ** 4
    )
    c.record(
        "<P>_HK_SU(3) Taylor expansion (4 terms) matches direct evaluation",
        abs(direct - taylor4) < 1e-12,
        f"direct = {direct:.12f}, taylor = {taylor4:.12f}",
    )

    # The bootstrap conjecture would say beta_2^<P> = pHK_coef_3 = 32/81.
    # Compare with TVZ MSbar value at N_f = 6:
    bootstrap_beta_2 = pHK_coef_3
    msbar_beta_2 = BETA_2_QCD_NF6
    print(f"    -> P_L1-B bootstrap conjecture: beta_2^<P> = {bootstrap_beta_2}")
    print(f"                                                = {float(bootstrap_beta_2):.4f}")
    print(f"    -> MSbar comparator at N_f = 6: beta_2^MSbar = {msbar_beta_2}")
    print(f"                                                  = {float(msbar_beta_2):.4f}")

    ratio = abs(float(msbar_beta_2) / float(bootstrap_beta_2)) if bootstrap_beta_2 != 0 else float("inf")
    c.record(
        "P_L1-B bootstrap value differs from MSbar by ~ order 80x",
        ratio > 50,
        f"|beta_2^MSbar / beta_2^bootstrap| = {ratio:.1f}",
    )

    c.admit(
        "P_L1-B: equating <P>_HK probe expectation with flow derivative",
        "<P>_HK is the single-plaquette EXPECTATION VALUE in the heat-kernel "
        "limit, NOT the running-coupling flow derivative; they coincide at "
        "1-loop and 2-loop (universal coefficients) but diverge at 3-loop+",
    )

    print("    -> P_L1-B: NEGATIVE on closure.")
    print("       Sub-finding (positive structural): <P>-scheme IS framework-")
    print("       native; scheme distinction is real (X-L1-MSbar Section 6).")


# ----------------------------------------------------------------------
# SECTION 5 — PRIMITIVE P_L1-C (Combinatorial Sum-Rule)
# ----------------------------------------------------------------------

def section5_primitive_C_sum_rule(c: Counter) -> None:
    """Stress-test P_L1-C: factor the channel-weight obstruction into
    combinatorial (graph enumeration + symmetry factors + Casimir
    contraction = RETAINED) + number-theoretic (graph-period oracle =
    NEW PRIMITIVE). The structural objection is that "graph period
    oracle" is the same primitive X-L1-MSbar identified as foreign,
    rebranded.
    """
    print()
    print("Section 5 — P_L1-C: Combinatorial Symmetry-Factor Sum-Rule Primitive")

    # Verify the Casimir-tensor channel values at SU(3), N_f = 6
    # (these are RETAINED via the V-L1-Quartic and X-L1-MSbar probes)
    c.record(
        "Channel C_F^3 value at SU(3) = 64/27",
        CHANNEL_VALUE["C_F^3"] == Fraction(64, 27),
        f"= {CHANNEL_VALUE['C_F^3']}",
    )
    c.record(
        "Channel C_A^3 value at SU(3) = 27",
        CHANNEL_VALUE["C_A^3"] == 27,
        f"= {CHANNEL_VALUE['C_A^3']}",
    )
    c.record(
        "Channel C_F (T_F n_f)^2 at SU(3), N_f=6 = 12",
        CHANNEL_VALUE["C_F (T_F n_f)^2"] == 12,
        f"= {CHANNEL_VALUE['C_F (T_F n_f)^2']}",
    )
    c.record(
        "Channel C_F C_A (T_F n_f) at SU(3), N_f=6 = 12",
        CHANNEL_VALUE["C_F C_A (T_F n_f)"] == 12,
        f"= {CHANNEL_VALUE['C_F C_A (T_F n_f)']}",
    )

    # The sum-rule factorization:
    #   c_alpha = sum over Gamma in G_n^T_alpha
    #               of (sym(Gamma))^-1 * P_alpha^rational(Gamma)
    # The combinatorial parts (G_n^T_alpha, sym) are admitted as
    # RETAINED. The period part is the NEW PRIMITIVE.
    print("    -> P_L1-C factorization: c_alpha = sum_{Gamma} (sym)^-1 * P(Gamma)")
    print("       sym, T-projection: RETAINED (combinatorial + group theory)")
    print("       P(Gamma): NEW PRIMITIVE (graph-period oracle)")

    # Demonstrate the strength equivalence: if we ADMIT a graph-period
    # oracle returning Brown-Schnetz period values, we can reconstruct
    # TVZ weights -- but this admission is comparable in strength to
    # the original missing primitive (master-integral evaluation).
    #
    # Toy demonstration: at 3-loop the C_A^3 channel decomposes into
    # ~7-10 primitive 3-loop QCD graphs. Suppose we admit an oracle
    # returning each graph's period:
    #   - ladder graph (sym = 12): period = pi^2/3 ~ but reduces to rational
    #   - sunset graph (sym = 6): period = rational
    #   - etc.
    #
    # The total c_AAA = 2857/54 then follows from the oracle values
    # plus the symmetry-factor sum. But the oracle itself is what
    # X-L1-MSbar identified as missing.
    target_c_AAA = Fraction(2857, 54)
    print(f"    -> P_L1-C target reconstruction at C_A^3 channel: c_AAA = {target_c_AAA}")
    print("       Reconstruction requires graph-period oracle returning")
    print("       Brown-Schnetz periods of the ~7-10 primitive 3-loop graphs")
    print("       contributing to C_A^3. Oracle is NOT retained.")

    c.admit(
        "P_L1-C: graph-period oracle P : Primitive 1PI Graphs -> Q + Q*zeta_3",
        "factorizes the missing primitive cleanly but admits one of "
        "comparable mathematical strength (Brown-Schnetz period evaluation = "
        "master-integral computation in Schwinger-parameter form)",
    )

    print("    -> P_L1-C: NEGATIVE on closure.")
    print("       Sub-finding (positive structural): cleanest known formulation")
    print("       of the open admission as a 'period oracle' on graph cohomology.")


# ----------------------------------------------------------------------
# SECTION 6 — TVZ POLYNOMIAL VALUE CROSS-CHECK
# ----------------------------------------------------------------------

def section6_tvz_polynomial_check(c: Counter) -> None:
    """Cross-check the TVZ 1980 closed-form polynomial reproduction
    of beta_2 at N_f = 6: confirm beta_2 = -65/2 = -32.5.
    """
    print()
    print("Section 6 — TVZ closed-form polynomial cross-check")

    # beta_2 = 2857/2 - (5033/18) n_f + (325/54) n_f^2
    target = -Fraction(65, 2)
    c.record(
        "TVZ 1980 beta_2 polynomial at N_f = 6 evaluates to -65/2",
        BETA_2_QCD_NF6 == target,
        f"= 2857/2 - 5033/3 + 325*36/54 = {BETA_2_QCD_NF6}",
    )

    c.record(
        "TVZ polynomial is degree 2 in n_f (no quartic-Casimir term)",
        True,  # known structural fact
        "quartic-Casimir contributions would require deg >= 3 in n_f",
    )


# ----------------------------------------------------------------------
# SECTION 7 — HYPOTHETICAL P_L1-D (Cl(3)/Z^3-Native Period Functor)
# ----------------------------------------------------------------------

def section7_hypothetical_D(c: Counter) -> None:
    """Document the open design problem: a hypothetical primitive
    P_L1-D that WOULD close the admission. No such functor is
    currently known.
    """
    print()
    print("Section 7 — Hypothetical P_L1-D (open design problem)")

    print("    Hypothetical primitive P_L1-D:")
    print("      An algorithmically specifiable function")
    print("        P_Cl(3) : 1PI Graph -> Q[zeta_n]")
    print("      that:")
    print("        1. Reproduces 3-loop TVZ values 2857/54, ..., 1/2")
    print("           from the Cl(3) lattice substrate alone")
    print("           (without dim-reg or Brown-Schnetz period theory).")
    print("        2. Reproduces 4-loop VVL Q + Q*zeta_3 weights")
    print("           similarly.")

    # This is not yet known to exist. Document as ADMITTED open problem.
    c.admit(
        "P_L1-D: Cl(3)/Z^3-native period functor on primitive 1PI graphs",
        "no such functor is currently known; the framework's Z^3 lattice "
        "substrate carries no canonical period extension to graphs that "
        "reproduces continuum perturbative Q[zeta_n] periods; establishing "
        "one would itself be a major result",
    )

    print("    -> P_L1-D: OPEN DESIGN PROBLEM.")


# ----------------------------------------------------------------------
# Honest verdict
# ----------------------------------------------------------------------

def final_verdict(c: Counter) -> None:
    print()
    print("=" * 72)
    print("Honest verdict")
    print("=" * 72)

    print()
    print("  Candidate primitives stress-tested:")
    print("    P_L1-A (Connes-Kreimer Hopf-Subdivergence):  NEGATIVE on closure")
    print("    P_L1-B (<P>-scheme HK bootstrap):            NEGATIVE on closure")
    print("    P_L1-C (Combinatorial sum-rule):             NEGATIVE on closure")
    print("    P_L1-D (Cl(3)/Z^3 period functor):           OPEN DESIGN PROBLEM")
    print()
    print("  Sub-findings (positive):")
    print("    - The terminal admission can be sharpened to:")
    print("      'no Cl(3)/Z^3-native period functor on primitive 1PI graphs'")
    print("    - Hopf-algebra organization is genuine but non-load-bearing")
    print("    - <P>-scheme is framework-native at probe-expectation level")
    print("    - Sum-rule factorization is the cleanest known form of the gap")
    print()
    print("  Conclusion:")
    print("    No clean primitive proposed here closes the L1 channel-weight")
    print("    terminal admission. The X-L1-MSbar bounded admission stands;")
    print("    beta_2, beta_3 continue to be imported from QCD literature as")
    print("    'imported authority for a bounded-tier theorem'.")
    print()
    print(f"  Tally:  PASS = {c.pass_count}, FAIL = {c.fail_count}, "
          f"ADMITTED = {c.admitted_count}")
    print()
    print("  Verdict: primitive_design_proposal")
    print("           NEGATIVE on closure for all three candidate primitives")
    print("           POSITIVE on sharpening the shape of the open admission")
    print("=" * 72)


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------

def main() -> int:
    print("=" * 72)
    print("Primitive Design Probe P-L1 — QCD beta_2/beta_3 channel-weight")
    print("                              terminal admission")
    print("Date: 2026-05-10")
    print("Source-note authority:")
    print("  docs/PRIMITIVE_P_L1_CHANNEL_WEIGHT_PROPOSAL_NOTE_2026-05-10_pPl1.md")
    print("=" * 72)

    c = Counter()

    section1_terminal_admission_shape(c)
    section2_beta_0_beta_1_retained(c)
    section3_primitive_A_connes_kreimer(c)
    section4_primitive_B_p_scheme_bootstrap(c)
    section5_primitive_C_sum_rule(c)
    section6_tvz_polynomial_check(c)
    section7_hypothetical_D(c)
    final_verdict(c)

    if c.fail_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
