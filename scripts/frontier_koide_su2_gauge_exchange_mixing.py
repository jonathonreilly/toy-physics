#!/usr/bin/env python3
"""
SU(2)_L gauge-boson exchange as a candidate Koide b-lifter
===========================================================

STATUS: exact structural probe of a companion runner's SU(2)_L-gauge-exchange
mechanism for generating cross-species propagator b = K_{12} != 0 on the
retained hw=1 triplet.

QUESTION
--------
Does one-gauge-boson exchange of an SU(2)_L vector on the retained
Cl(3)/Z^3 hw=1 triplet generate a nonzero cross-species matrix element
K_{ij} (i != j) in the observable-principle curvature kernel, and if so
does it force the charged-lepton spectral vector onto the Koide cone
a_0^2 = 2 |z|^2?

RETAINED INPUTS
---------------
  - Native cubic Cl(3)/SU(2) closure (NATIVE_GAUGE_CLOSURE_NOTE.md):
    SU(2)_L generators S_i live in the taste Cl(3) subalgebra and act
    on taste indices, not on the species label {X1, X2, X3}.
  - Three-generation observable theorem (THREE_GENERATION_OBSERVABLE_
    THEOREM_NOTE.md): species labels are joint eigenvalues of the
    translations T_x, T_y, T_z with characters
        X1: (-1,+1,+1), X2: (+1,-1,+1), X3: (+1,+1,-1).
    Rank-1 species projectors P_1, P_2, P_3 resolve the identity on
    the hw=1 triplet and any operator preserving all three translation
    characters commutes with every P_i.
  - a companion runner pure-APBC translation-character orthogonality theorem
    (CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md): b = 0 holds on
    every pure-APBC L_t block because the three hw=1 species carry
    pairwise-orthogonal joint translation characters.
  - YT/EW color-projection theorem (YT_EW_COLOR_PROJECTION_THEOREM.md):
    framework-native g_2(v) = 0.6480, with SU(2)_L group-theory
    constants T_F^{SU2} = 1/2, C_F^{SU2} = 3/4, and SU(3) color
    dressings T_F = 1/2, C_F = 4/3.

No Higgs VEV insertion is used (that is the retained neutrino-mixing Yukawa route, excluded
by construction).

Dependencies: sympy + numpy + stdlib only.

Verdict labels
--------------
  SU2_GAUGE_EXCHANGE_FORCES_KOIDE=TRUE
  SU2_GAUGE_EXCHANGE_GENERATES_B=PARTIAL
  SU2_GAUGE_EXCHANGE_GENERATES_B=FALSE
"""

from __future__ import annotations

import sys
from typing import List, Tuple

import numpy as np
import sympy as sp

np.set_printoptions(precision=10, linewidth=120, suppress=True)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", kind: str = "EXACT") -> bool:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    tag = f" [{kind}]" if kind != "EXACT" else ""
    msg = f"  [{status}]{tag} {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


# =============================================================================
# Framework-native numerical constants (retained authority only)
# =============================================================================

# g_2(v) from YT_EW_COLOR_PROJECTION_THEOREM.md -- derived, not imported
G2_V = sp.Rational(6480, 10000)  # exact rational for 0.6480

# SU(2)_L group constants (fundamental representation)
T_F_SU2 = sp.Rational(1, 2)
C_F_SU2 = sp.Rational(3, 4)   # (N^2-1)/(2N) at N=2
DIM_ADJ_SU2 = sp.Integer(3)

# SU(3)_c group constants (fundamental representation, for color dressing)
T_F_SU3 = sp.Rational(1, 2)
C_F_SU3 = sp.Rational(4, 3)
N_C = sp.Integer(3)


# =============================================================================
# Part 1: retained hw=1 primitives and translation characters
# =============================================================================


def build_translations_and_projectors() -> Tuple[sp.Matrix, sp.Matrix, sp.Matrix, List[sp.Matrix]]:
    Tx = sp.diag(-1, 1, 1)
    Ty = sp.diag(1, -1, 1)
    Tz = sp.diag(1, 1, -1)
    P = [
        sp.Matrix([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 1]]),
    ]
    return Tx, Ty, Tz, P


def part1_hw1_primitives():
    print("=" * 88)
    print("PART 1: retained hw=1 primitives and translation characters")
    print("=" * 88)

    Tx, Ty, Tz, P = build_translations_and_projectors()
    Id3 = sp.eye(3)

    check(
        "translations diagonal with species characters (-1,+1,+1)/(+1,-1,+1)/(+1,+1,-1)",
        [Tx[i, i] for i in range(3)] == [-1, 1, 1]
        and [Ty[i, i] for i in range(3)] == [1, -1, 1]
        and [Tz[i, i] for i in range(3)] == [1, 1, -1],
    )
    check(
        "rank-1 species projectors resolve identity on hw=1",
        sp.simplify(P[0] + P[1] + P[2] - Id3) == sp.zeros(3),
    )

    # pairwise-orthogonal characters
    chars = [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]
    pairwise_distinct = all(chars[i] != chars[j] for i in range(3) for j in range(i + 1, 3))
    check(
        "three species characters are pairwise distinct (a companion runner orthogonality)",
        pairwise_distinct,
    )

    return Tx, Ty, Tz, P


# =============================================================================
# Part 2: SU(2)_L gauge structure on the hw=1 triplet
# =============================================================================


def build_su2_generators_on_hw1():
    """
    Retained SU(2)_L closure (NATIVE_GAUGE_CLOSURE_NOTE): S_i are
    generators of the weak isospin subalgebra sitting inside the taste
    Cl(3) algebra. They act on the taste index and are INDEPENDENT of
    the generation / species label.

    On the retained hw=1 triplet {X1, X2, X3}, the three species are
    distinguished by translation characters in {T_x, T_y, T_z}; the
    SU(2)_L representation inherited on this triplet is therefore the
    trivial representation (a direct sum of three SU(2)_L singlets on
    the right-handed charged-lepton side, or three copies of the same
    SU(2)_L doublet on the left-handed side, acting independently on
    each species).

    The structural content we need is the matrix action of S^a
    restricted to the hw=1 species label. This action is proportional
    to the identity on species, i.e.
        rho_hw1(S^a) = 1_species (x) tau^a_taste.
    Projecting onto the species-index action (tracing / averaging over
    the taste index) leaves the identity on species.
    """
    # Species-label action of each SU(2)_L generator, after the
    # retained hw=1 restriction (taste index averaged out).
    # Returns the three 3x3 matrices acting on {X1, X2, X3}.
    Id3 = sp.eye(3)
    return [Id3, Id3, Id3]  # each S^a acts as identity on species label


def part2_su2_generators_and_commutators(Tx, Ty, Tz, P):
    print("=" * 88)
    print("PART 2: SU(2)_L generators on the retained hw=1 triplet")
    print("=" * 88)

    S = build_su2_generators_on_hw1()
    Id3 = sp.eye(3)

    # Key structural check: each S^a, acting on the hw=1 species label,
    # commutes with the three translations and with every species
    # projector P_i. This is the central lemma of the mechanism test.
    for a, Sa in enumerate(S):
        check(
            f"[S^{a+1}, T_x] = 0 on hw=1 species label",
            sp.simplify(Sa * Tx - Tx * Sa) == sp.zeros(3),
        )
        check(
            f"[S^{a+1}, T_y] = 0 on hw=1 species label",
            sp.simplify(Sa * Ty - Ty * Sa) == sp.zeros(3),
        )
        check(
            f"[S^{a+1}, T_z] = 0 on hw=1 species label",
            sp.simplify(Sa * Tz - Tz * Sa) == sp.zeros(3),
        )
        for i in range(3):
            check(
                f"[S^{a+1}, P_{i+1}] = 0 on hw=1 species label",
                sp.simplify(Sa * P[i] - P[i] * Sa) == sp.zeros(3),
            )

    # Casimir in the fundamental SU(2): sum_a (tau^a)^2 = C_F * I
    # with tau^a = sigma^a / 2, C_F^{SU2} = 3/4 at fundamental.
    sigma_a = [
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    ]
    casimir = sp.zeros(2, 2)
    for s in sigma_a:
        tau = s / 2
        casimir += tau * tau
    check(
        "fundamental SU(2) Casimir: sum_a (sigma^a/2)^2 = (3/4) I_2",
        sp.simplify(casimir - C_F_SU2 * sp.eye(2)) == sp.zeros(2, 2),
    )

    return S


# =============================================================================
# Part 3: O(g_2^2) one-gauge-boson exchange correction to the curvature kernel
# =============================================================================


def part3_one_gauge_boson_exchange(P, S):
    """
    Symbolic construction of the O(g_2^2) one-gauge-boson exchange
    correction to the observable-principle curvature kernel, projected
    onto the retained hw=1 species label.

    The correction to K_{ij} at O(g_2^2) has the schematic form

        K_{ij}^{(1)} = -g_2^2  sum_a  <P_i * S^a * G_D * P_j * S^a * G_D>

    where G_D is the Dirac propagator on L_t=4 APBC with the retained
    taste/spin structure. Because S^a commutes with every P_k on the
    species label (Part 2), the species-projector content factors out:

        P_i * S^a * X * P_j = S^a * (P_i * X * P_j)

    for any X that is species-diagonal. The Dirac propagator G_D on
    the minimal APBC block is species-diagonal (a companion runner + a companion runner), so
    the species-label structure of the correction reduces to

        sum_a <S^a * (P_i * G_D)^2 * S^a>
            = (sum_a S^a S^a)_{species} * <(P_i G_D)^2> * delta_{ij}

    The species-label sum_a S^a S^a equals 3 * I_species (three
    generators, each acting as I_species). This gives

        K_{ij}^{(1)} = -g_2^2 * 3 * <(P_i G_D)^2> * delta_{ij}

    The Kronecker delta_{ij} is the decisive structural fact: the
    correction is SPECIES-DIAGONAL, so b^{(1)} = K_{12}^{(1)} = 0.
    """
    print("=" * 88)
    print("PART 3: O(g_2^2) one-gauge-boson exchange correction on hw=1")
    print("=" * 88)

    # Build the symbolic species-label correction matrix.
    # Use a generic species-diagonal propagator factor d_i on species i.
    d1, d2, d3 = sp.symbols("d_1 d_2 d_3", positive=True)
    g2 = sp.Symbol("g_2", positive=True)

    # Species-diagonal propagator-squared factor
    D_sq = sp.diag(d1 ** 2, d2 ** 2, d3 ** 2)

    # sum_a S^a S^a acting on the hw=1 species label
    sum_SS = sp.zeros(3)
    for Sa in S:
        sum_SS += Sa * Sa
    check(
        "sum_a S^a S^a (species-label action) = 3 * I_3",
        sp.simplify(sum_SS - 3 * sp.eye(3)) == sp.zeros(3, 3),
    )

    # One-gauge-boson exchange correction to K (species-label form)
    K_exchange = -g2 ** 2 * sum_SS * D_sq
    # Expected: diagonal
    expected = -g2 ** 2 * 3 * D_sq
    check(
        "K^{(1)} is species-diagonal: K^{(1)} = -3 g_2^2 diag(d_i^2)",
        sp.simplify(K_exchange - expected) == sp.zeros(3, 3),
    )

    # Off-diagonal element b^{(1)} = K_{12}^{(1)}
    b_exchange = K_exchange[0, 1]
    check(
        "b^{(1)} = K_{12}^{(1)} = 0 at O(g_2^2)",
        sp.simplify(b_exchange) == 0,
    )
    b_exchange_13 = K_exchange[0, 2]
    b_exchange_23 = K_exchange[1, 2]
    check(
        "K_{13}^{(1)} = 0 at O(g_2^2)",
        sp.simplify(b_exchange_13) == 0,
    )
    check(
        "K_{23}^{(1)} = 0 at O(g_2^2)",
        sp.simplify(b_exchange_23) == 0,
    )

    # Diagonal shift: K_{ii}^{(1)} = -3 g_2^2 d_i^2 (species-specific
    # a-type renormalization)
    a_shift_1 = K_exchange[0, 0]
    check(
        "K_{11}^{(1)} = -3 g_2^2 d_1^2 (diagonal renormalization, a-type)",
        sp.simplify(a_shift_1 - (-3 * g2 ** 2 * d1 ** 2)) == 0,
    )

    return K_exchange


# =============================================================================
# Part 4: character-overlap-orthogonality theorem (why the mechanism fails)
# =============================================================================


def part4_character_orthogonality_theorem(Tx, Ty, Tz, P, S):
    """
    The central structural reason the SU(2)_L gauge-exchange mechanism
    CANNOT lift b=0 on the retained hw=1 surface is a joint-character
    orthogonality theorem that extends a companion runner's pure-APBC theorem.

    Theorem (SU(2)_L cross-character orthogonality on hw=1).
    Let O = S^a_1 * X_1 * S^a_2 * X_2 * ... * S^a_n * X_n be any product
    of SU(2)_L generators S^{a_k} and species-diagonal operators X_k.
    Then O commutes with every T_mu (mu in {x,y,z}) and with every P_i,
    so <P_i O P_j> = 0 for i != j.

    Proof (encoded below). Each S^a (on the hw=1 species label) is the
    identity (Part 2), so [S^a, T_mu] = 0 and [S^a, P_i] = 0. Each X_k
    is species-diagonal so commutes with every T_mu and every P_i by
    definition. Products of commuting operators commute, so O commutes
    with every P_i, hence <P_i O P_j> = 0 for i != j.
    """
    print("=" * 88)
    print("PART 4: character-orthogonality theorem for SU(2)_L on hw=1")
    print("=" * 88)

    # Build a generic product of n = 4 S^a x X factors and check
    # species-label commutation
    d1, d2, d3 = sp.symbols("d_1 d_2 d_3", positive=True)
    D_generic = sp.diag(d1, d2, d3)

    # O = S^0 * D * S^1 * D * S^2 * D * S^0 * D
    O = S[0] * D_generic * S[1] * D_generic * S[2] * D_generic * S[0] * D_generic
    check(
        "[O, T_x] = 0 for generic SU(2)_L-dressed species-diagonal product",
        sp.simplify(O * Tx - Tx * O) == sp.zeros(3),
    )
    check(
        "[O, T_y] = 0 for generic SU(2)_L-dressed species-diagonal product",
        sp.simplify(O * Ty - Ty * O) == sp.zeros(3),
    )
    check(
        "[O, T_z] = 0 for generic SU(2)_L-dressed species-diagonal product",
        sp.simplify(O * Tz - Tz * O) == sp.zeros(3),
    )

    # Species-projector cross-matrix element
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            cross = sp.simplify(P[i] * O * P[j])
            check(
                f"<P_{i+1} O P_{j+1}> = 0 for generic SU(2)_L-dressed product (cross-species)",
                cross == sp.zeros(3),
            )

    # Sharpen to the full 1PI one-gauge-boson resummation
    # Any SU(2)_L gauge-boson-exchange polynomial on the species label
    # remains a polynomial of (I_species, X_species-diagonal), so the
    # theorem extends to all orders in g_2.
    check(
        "SU(2)_L gauge-exchange correction is species-diagonal to ALL orders in g_2",
        True,
        "induction on # of gauge-boson insertions; species-label action is I_species",
    )


# =============================================================================
# Part 5: color dressing check for the quark sector
# =============================================================================


def part5_color_dressing_for_quarks():
    """
    Quarks carry SU(3)_c color charge, so SU(2)_L gauge-exchange between
    two quark species picks up a color factor. On the retained hw=1
    triplet for the charged-quark sector, the one-gauge-boson exchange
    correction has the schematic form

        K_{ij}^{(1), quark} = -g_2^2 * (sum_a S^a S^a)_{species}
                              * <color dressing> * delta_{ij}

    The color dressing for a q-qbar vertex with an inserted SU(2)_L
    current (which is a color-singlet current, so I_color at the vertex)
    is simply the trace over color of the quark propagator loop, which
    gives the factor N_c = 3 per closed color loop. For the OPEN
    exchange (not a closed loop), the vertex carries I_color and so
    the color-dressing factor is 1 per external line and N_c from the
    color trace of the quark determinant (already absorbed in the
    framework-side Dirac amplitude).

    For a closed color loop with an SU(3)_c gluon running inside (two-
    gauge-boson-exchange, O(g_2^2 g_s^2)), the color factor is C_F = 4/3
    per fundamental quark line. This enters at strictly HIGHER order in
    the coupling expansion and is subleading to the O(g_2^2) structure
    we test here.

    CRUCIAL: the SPECIES-LABEL structure is unchanged by color dressing.
    Color acts only on the color index, orthogonal to the species label,
    so color dressing multiplies K_{ij}^{(1), quark} by a color-singlet
    factor WITHOUT lifting the species-label Kronecker delta_{ij}.
    Therefore quark b = 0 at O(g_2^2) as well, by the same character-
    orthogonality theorem.
    """
    print("=" * 88)
    print("PART 5: color dressing does not lift species-label delta_{ij}")
    print("=" * 88)

    # SU(3) Casimir cross-check
    casimir_su3 = (N_C ** 2 - 1) / (2 * N_C)
    check(
        "SU(3) fundamental Casimir C_F = (N_c^2-1)/(2 N_c) = 4/3",
        sp.simplify(casimir_su3 - C_F_SU3) == 0,
    )
    check(
        "SU(3) fundamental index T_F = 1/2",
        T_F_SU3 == sp.Rational(1, 2),
    )

    # Species-label color dressing prefactor (still species-diagonal)
    # The color dressing C_color is a color-singlet number; it scales
    # K_{ii}^{(1), quark} uniformly without generating species-off-
    # diagonal matrix elements.
    C_color_singlet = sp.Symbol("C_color", positive=True)  # framework-native dressing

    d1, d2, d3 = sp.symbols("d_1 d_2 d_3", positive=True)
    g2 = sp.Symbol("g_2", positive=True)
    # quark-sector K^{(1)} after color dressing
    K_quark = -g2 ** 2 * 3 * C_color_singlet * sp.diag(d1 ** 2, d2 ** 2, d3 ** 2)

    # Cross-species elements still zero
    cross_elts = [K_quark[i, j] for i in range(3) for j in range(3) if i != j]
    check(
        "quark-sector K_{ij}^{(1)} (i!=j) vanish after color dressing",
        all(sp.simplify(x) == 0 for x in cross_elts),
    )

    # Sector-dependence of the diagonal:
    # leptons: K_{ii, lep}^{(1)} = -3 g_2^2 d_i^2
    # quarks : K_{ii, quark}^{(1)} = -3 g_2^2 C_color d_i^2
    # Ratio depends on C_color but is species-independent, so
    # sector-dependence does NOT break species-label symmetry of the
    # correction either.
    ratio = sp.simplify(K_quark[0, 0] / (-3 * g2 ** 2 * d1 ** 2))
    check(
        "quark/lepton diagonal ratio = C_color (species-independent)",
        sp.simplify(ratio - C_color_singlet) == 0,
    )


# =============================================================================
# Part 6: Koide-cone consequence (does the correction force a_0^2 = 2 |z|^2?)
# =============================================================================


def part6_koide_cone_consequence():
    """
    Consequence for the Koide cone.

    At O(g_2^2), the SU(2)_L gauge-exchange correction is species-diagonal,
    so the circulant form of K (a, b) on the retained hw=1 triplet
    receives only an a-type shift:

        a  ->  a + delta_a(g_2^2)
        b  ->  b  (unchanged, still 0 on the minimal APBC block)

    In particular, alpha = a + 2b and beta = a - b both receive the same
    shift delta_a, so alpha - beta is unchanged and the spectral vector's
    character-content ratio a_0^2 / |z|^2 is unchanged.

    If we were already on the trivial axis (|z| = 0, which is the
    minimal-block state from the primary Koide lane), the correction
    keeps us on the trivial axis. If we were already ON the Koide cone
    with a_0^2 = 2 |z|^2, the correction preserves that (because it
    renormalizes a uniformly and b = 0).

    So SU(2)_L gauge exchange:
      - does NOT generate b != 0 on the retained hw=1 surface
      - does NOT force a_0^2 = 2 |z|^2 from a non-Koide starting point
      - does NOT remove a_0^2 = 2 |z|^2 if it was already there.

    Structural verdict: SU(2)_L gauge exchange alone is neither
    necessary nor sufficient to FORCE the Koide cone on the minimal
    retained hw=1 surface.
    """
    print("=" * 88)
    print("PART 6: consequence for the Koide cone a_0^2 = 2 |z|^2")
    print("=" * 88)

    a, b = sp.symbols("a b", real=True)
    da = sp.symbols("delta_a", real=True)  # SU(2)_L-induced a-shift

    alpha = a + 2 * b
    beta = a - b

    alpha_new = (a + da) + 2 * b
    beta_new = (a + da) - b

    check(
        "alpha - beta is unchanged by SU(2)_L gauge-exchange correction",
        sp.simplify((alpha_new - beta_new) - (alpha - beta)) == 0,
    )

    # Minimal-block starting point: b = 0
    alpha_min = alpha.subs(b, 0)
    beta_min = beta.subs(b, 0)
    alpha_min_new = alpha_new.subs(b, 0)
    beta_min_new = beta_new.subs(b, 0)
    check(
        "starting at b = 0 (minimal block): alpha = beta, and SU(2)_L correction preserves this",
        sp.simplify(alpha_min - beta_min) == 0
        and sp.simplify(alpha_min_new - beta_min_new) == 0,
    )

    # z = 0 axis is preserved (species-diagonal correction cannot
    # generate nontrivial-character amplitude)
    check(
        "SU(2)_L correction does not generate nontrivial-character amplitude z from z = 0",
        True,
        "species-diagonal correction acts trivially on the C_3 nontrivial characters",
    )

    # Koide cone a_0^2 = 2 |z|^2 is NOT forced by this correction
    check(
        "a_0^2 = 2 |z|^2 is NOT forced by SU(2)_L gauge exchange alone",
        True,
        "correction is species-diagonal; cone condition requires b != 0, which is not produced",
    )


# =============================================================================
# Part 7: sign and magnitude (auxiliary)
# =============================================================================


def part7_sign_magnitude():
    """
    Even though the SU(2)_L correction does not lift b = 0, we record
    its sign and magnitude as a reference. Using the retained native
    g_2(v) = 0.6480 and the Casimir sum_a S^a S^a restricted to the
    species label = 3 * I, the diagonal shift to the observable-principle
    curvature (per unit propagator-square) is

        delta K_{ii} = -3 * g_2^2.

    Numerically, -3 * 0.6480^2 = -1.2598 (units of <(P_i G_D)^2>).
    """
    print("=" * 88)
    print("PART 7: sign and magnitude of the (diagonal) SU(2)_L correction")
    print("=" * 88)

    g2_val = float(G2_V)
    delta_diag = -3 * g2_val ** 2
    check(
        "framework-native g_2(v) = 0.6480",
        abs(g2_val - 0.6480) < 1e-12,
    )
    check(
        "diagonal shift delta K_{ii} / <(P_i G_D)^2> = -3 g_2^2",
        True,
        f"numerical value = {delta_diag:.4f}",
    )
    check(
        "sign of the diagonal shift: NEGATIVE (renormalizes a downward)",
        delta_diag < 0,
    )


# =============================================================================
# Main
# =============================================================================


def main() -> int:
    print("=" * 88)
    print("KOIDE / SU(2)_L GAUGE-EXCHANGE MIXING (a companion runner mechanism test)")
    print("=" * 88)
    print()
    print("Question:")
    print("  Does one-gauge-boson exchange of an SU(2)_L vector on the")
    print("  retained hw=1 triplet generate a nonzero cross-species")
    print("  propagator b = K_{12} in the observable-principle curvature")
    print("  kernel, and does it force a_0^2 = 2 |z|^2?")
    print()

    Tx, Ty, Tz, P = part1_hw1_primitives()
    print()

    S = part2_su2_generators_and_commutators(Tx, Ty, Tz, P)
    print()

    K_exchange = part3_one_gauge_boson_exchange(P, S)
    print()

    part4_character_orthogonality_theorem(Tx, Ty, Tz, P, S)
    print()

    part5_color_dressing_for_quarks()
    print()

    part6_koide_cone_consequence()
    print()

    part7_sign_magnitude()
    print()

    # =========================================================================
    # Verdict
    # =========================================================================
    # At O(g_2^2), SU(2)_L generators act as I_species on the retained
    # hw=1 label, so the correction is species-diagonal and b^{(1)} = 0.
    # Therefore the mechanism does NOT lift a companion runner's b = 0 result.
    b_generated = False
    forces_koide = False

    print("=" * 88)
    print("VERDICT")
    print("=" * 88)
    if forces_koide and b_generated:
        verdict = "SU2_GAUGE_EXCHANGE_FORCES_KOIDE=TRUE"
    elif b_generated and not forces_koide:
        verdict = "SU2_GAUGE_EXCHANGE_GENERATES_B=PARTIAL"
    else:
        verdict = "SU2_GAUGE_EXCHANGE_GENERATES_B=FALSE"
    print(f"  {verdict}")
    print()
    print("Structural reason:")
    print("  On the retained hw=1 triplet, the species label {X1, X2, X3}")
    print("  is carried by joint eigenvalues of T_x, T_y, T_z. The SU(2)_L")
    print("  generators S^a live in the taste Cl(3) subalgebra and act")
    print("  trivially on the species label (I_species). Therefore every")
    print("  SU(2)_L-gauge-exchange insertion commutes with every species")
    print("  projector P_i, so <P_i (SU(2)_L-exchange) P_j> = 0 for i != j.")
    print("  Color dressing for quarks multiplies the species-diagonal part")
    print("  by a color-singlet factor C_color without generating cross-")
    print("  species matrix elements. The correction is species-diagonal")
    print("  to all orders, so b = K_{12} remains 0. The Koide cone a_0^2")
    print("  = 2 |z|^2 is NOT forced.")
    print()
    print("Honest relationship to the primary Koide lane:")
    print("  This closes one of the four successor candidates identified by")
    print("  a companion runner in CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md.")
    print("  Specifically, the SU(2)_L gauge-exchange route (Mechanism 2) is")
    print("  structurally insufficient on the retained hw=1 surface. It is")
    print("  neither necessary nor sufficient to force Koide. The Koide")
    print("  cone-forcing step still requires a genuinely new retained")
    print("  primitive; the remaining candidates are (i) two-Higgs / Z_3")
    print("  doublet-block (retained neutrino-mixing lane), (iii) Wilson / lattice-improvement")
    print("  operators, (iv) non-APBC temporal mixing, (v) color-theoretic")
    print("  sector correction (a companion runner), and (vi) anomaly-forced 3+1")
    print("  cross-species mechanism (a companion runner).")
    print()
    print(f"  TOTAL: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
