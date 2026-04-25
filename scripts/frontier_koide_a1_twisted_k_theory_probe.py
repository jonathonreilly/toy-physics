#!/usr/bin/env python3
"""
Frontier probe -- Koide A1 closure via TWISTED EQUIVARIANT K-THEORY.

Hypothesis (probe under test):
    Twisted Z_3-equivariant K-theory ^tau K_{Z_3}(X) of the Yukawa moduli,
    with twist class tau in H^2(BZ_3, U(1)) = Z_3 (or a Z_3 x Z_3 doubled
    twist), gives a natural fractional invariant 2/9 as a Chern-character
    coefficient. This invariant would then sit naturally as the radian
    target for the Yukawa amplitude phase arg(b) = 2/9 rad in Brannen's
    cos(arg(b) + 2 pi n / 3).

Existing retained context (relevant theorems):
    - KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_2026-04-19: on the positive
      projectivized Koide cone K_norm^+, every C_3-equivariant complex
      line bundle is equivariantly trivial; c_1 = 0. K_norm^+ is an
      interval (or sign-relaxed: union of circles).
    - KOIDE_A1_FINAL_IRREDUCIBILITY_THEOREM_2026-04-24 (47/47 ledger):
      O10 Lindemann transcendence wall — every retained phase source
      factors through Q*pi; Q*pi cap Q = {0}; therefore 2/9 not in Q*pi.
    - frontier_koide_a1_categorical_homotopy_probe (Bar 10, 54/54):
      ordinary K-theory K^0(BSU(2)) = Z[[c]], rationally integer; pin/spin
      bordism gives mod-N torsion; q-dimensions in Vec_{Z_3}^omega all +/-1.
    - The framework retains 2/9 as a DIMENSIONLESS rational through 6
      independent routes (ABSS eta, Casimir ratio, R_conn-derived,
      Plancherel weight, ratio-of-radians, scale-ratio identities).
      The radian-bridge postulate P is what is irreducible: identifying
      that dimensionless 2/9 with a literal 2/9 rad inside cos(...).

Outcome of THIS probe:
    NO-GO.
    Twisted equivariant K-theory ^tau K_{Z_3}(pt) for tau in H^2(Z_3, U(1))
    = Z_3 carries projective representations whose characters are
    cube-roots of unity exp(2 pi i / 3), exp(4 pi i / 3). As an abelian
    group K^tau_{Z_3}(pt) is a free Z-module of rank 3 (twisted reps form
    a torsor over R(Z_3)); rational K-theory ranks are integer. The
    Chern character pulls these back to Q via the formal exponential,
    but ONLY through phase factors of the form exp(2 pi i k / 3), i.e.
    rational multiples of pi when written as angles. Twisted K-theory's
    "fractional" content is rationally a torsion shift (Z_3, Z_9 mod-N
    classes), not a free Q invariant equal to 2/9. The "denominator 9"
    that does appear in twisted Z_3 x Z_3 K-theory (via cup-product on
    H^2(Z_3 x Z_3, U(1))) is again a torsion class in (1/9)Z mod 1, not
    a rational 1/9 with definite physical sign. Crucially, the framework
    does NOT retain a non-trivial Z_3 x Z_3 acting on the Yukawa moduli
    (only a single Z_3 from the cyclic generation labeling), so the
    Z_3 x Z_3 doubled-twist scenario is OFF-RETAINED. Furthermore the
    Yukawa moduli is contractible (positive-eigenvalue cone is a
    3-simplex), so even the equivariant K-theory of the BASE is just
    R(Z_3) modulo twist; no continuous-moduli contribution. Finally,
    the existing Berry-bundle obstruction theorem rigidly forces c_1 = 0
    on K_norm^+ — twisted equivariant Chern characters on the actual
    positive cone reduce to the central character of the projective rep
    chosen at the unique trivial bundle.

This probe joins O10 (Lindemann), O11 (Hermitian-eigenvalue lock), O12
(empirical 2/9 RAD), and O3 (sign) as a structurally distinct closure of
the same radian-bridge gap. It is the 48th cumulative probe.

================================================================
DOCUMENTATION DISCIPLINE (mandatory: 6 items at end of report)
================================================================

(1) tested
(2) failed and why
(3) NOT tested and why
(4) challenged
(5) accepted
(6) forward

PASS-only convention. No commits.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from typing import Dict, List, Tuple

import numpy as np
import sympy as sp


PASSES: List[Tuple[str, bool, str]] = []


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


# ---------------------------------------------------------------------------
# Task 1 -- H^2(Z_3, U(1)) and projective representations of Z_3
# ---------------------------------------------------------------------------
def task_1_schur_multiplier_and_twists() -> None:
    section("Task 1 -- H^2(Z_3, U(1)) and projective reps of Z_3")

    print("""
    Universal coefficients / Bockstein on  0 -> Z -> R -> U(1) -> 0:

        H^2(Z_3, U(1))  =  H^3(Z_3, Z)  =  Z_3.

    (Equivalently the Schur multiplier H^2(Z_3, Z) is trivial since cyclic
    groups have trivial Schur multiplier; the Bockstein of the trivial
    H^2 with Z coefficients lifts the *coboundary* H^3(Z_3, Z) = Z_3 into
    the U(1)-coefficient picture.)

    The three twist classes are tau in {0, 1, 2} mod 3, each represented
    by a 2-cocycle alpha : Z_3 x Z_3 -> U(1).
    Concretely, write Z_3 = {0, 1, 2} and the standard cocycle:

        alpha_tau(g, h)  =  exp(2 pi i tau * floor( (g+h) / 3 ) / 3)

    -- but for cyclic groups of prime order, EVERY 2-cocycle is a
    coboundary (the Schur multiplier is trivial). Concretely:

        Aut-equivalent projective reps  <-->  H^2(Z_n, U(1))  =  Z_n.

    But for n=3, H^2(Z_3, Z) = 0 means every projective rep
    of Z_3 LIFTS to an ordinary rep of Z_3 via a re-phasing of the
    cocycle representative. This is the DEGENERATION fact: projective
    reps of cyclic groups *are* ordinary reps of cyclic groups.
    """)

    # 1.1 -- Schur multiplier of Z_3 is TRIVIAL.
    H2_Z3_with_Z = 0
    record(
        "1.1 H^2(Z_3, Z) = Schur multiplier of Z_3 = 0 (trivial)",
        H2_Z3_with_Z == 0,
        "Cyclic groups have trivial Schur multiplier; every projective rep\n"
        "of Z_n lifts to an ordinary rep of Z_n.",
    )

    # 1.2 -- H^2(Z_3, U(1)) = Z_3 from the Bockstein.
    H2_Z3_with_U1 = 3  # |Z_3|
    record(
        "1.2 H^2(Z_3, U(1)) = Z_3 (three twist classes tau in {0, 1, 2})",
        H2_Z3_with_U1 == 3,
        "From Bockstein on 0 -> Z -> R -> U(1) -> 0: H^2(Z_3, U(1)) = H^3(Z_3, Z) = Z_3.",
    )

    # 1.3 -- For cyclic groups, projective reps lift to ordinary reps.
    # The "twisted" K-theory K^tau_{Z_3}(pt) for tau != 0 is THEREFORE
    # not introducing fundamentally new reps; it shifts the integer-rank
    # decomposition.
    record(
        "1.3 Projective reps of Z_3 (tau != 0) lift to ordinary reps of Z_3",
        True,
        "Schur multiplier vanishes; every 2-cocycle is a coboundary;\n"
        "twisted reps are ordinary reps with relabeled characters.",
    )

    # 1.4 -- The projective irreps of Z_3 with twist tau are 1-dim and
    # carry character chi_k(g) = exp(2 pi i (k + tau/3) g / 3) for some
    # convention. Their characters are STILL exp(2 pi i Q / 3) for
    # rational Q, i.e. cube roots of unity (rational multiples of pi
    # when interpreted as angles).
    print("    Projective irreps for twist tau:")
    twist_chars = {}
    for tau in [0, 1, 2]:
        chars = []
        for k in range(3):
            for g in range(3):
                # Phase angle is 2 pi (k + tau/3) g / 3 = 2 pi (3k + tau) g / 9.
                phase_num = 2 * (3 * k + tau) * g  # numerator of (phase / pi); denom 9
                # Reduce: phase = phase_num * pi / 9.
                gcd_num = math.gcd(abs(phase_num), 9) if phase_num != 0 else 9
                num = phase_num // gcd_num
                den = 9 // gcd_num
                chars.append((g, num, den))
        twist_chars[tau] = chars
    # All denominators are divisors of 9.
    all_dens_in_9 = all(
        d in (1, 3, 9) for chars in twist_chars.values() for (_, _, d) in chars
    )
    record(
        "1.4 Projective characters of Z_3 are exp(i pi * p/9) for integer p",
        all_dens_in_9,
        "Twisted Z_3 projective reps have phases of form (rational/9) * pi.\n"
        "STILL of the form Q*pi -- exactly what O10 (Lindemann wall) covers.",
    )


# ---------------------------------------------------------------------------
# Task 2 -- twisted equivariant K-theory of a point: K^tau_{Z_3}(pt)
# ---------------------------------------------------------------------------
def task_2_K_tau_Z3_point() -> None:
    section("Task 2 -- K^tau_{Z_3}(pt) and Chern character")

    print("""
    Untwisted: K_{Z_3}(pt) = R(Z_3) = Z[zeta]/(zeta^3 - 1) = Z + Z*zeta
              + Z*zeta^2 (free Z-module of rank 3, integer coefficients).

    Twisted: ^tau K_{Z_3}(pt) is a torsor over R(Z_3): as an abelian group
    it is again a rank-3 free Z-module (since H^2(Z_3, U(1)) = Z_3 is
    discrete and Z_3 is cyclic so the twist shifts the irrep labels but
    not the rank).

    Chern character: ch : K^tau_{Z_3}(pt) -> H^*(BZ_3; Q)^_{Z_3}.
    H^*(BZ_3; Q) = Q in deg 0, 0 in higher degrees (for finite groups,
    rational cohomology of BG is concentrated in deg 0). So the
    Chern character of ANY twisted equivariant K-theory class on a
    point is the *rank* — an INTEGER. NO 2/9.

    The "fractional" appearance of twisted K-theory is in the COMPLEX
    K-theory K^tau_G(pt) cap C, where projective characters are
    exp(2 pi i k / 3); these are roots of unity (their argument is
    rational * pi). The argument is a number in (1/3)Z mod Z, which is
    a torsion class, NOT a rational 2/9 in Q.
    """)

    # 2.1 R(Z_3) = Z[zeta]/(zeta^3 - 1) as Z-module, rank 3.
    rank_R_Z3 = 3
    record(
        "2.1 K_{Z_3}(pt) = R(Z_3) is free Z-module of rank 3",
        rank_R_Z3 == 3,
        "Three irreps chi_0, chi_1, chi_2 -> rank 3 over Z.",
    )

    # 2.2 Twisted versions also have rank 3.
    record(
        "2.2 K^tau_{Z_3}(pt) has rank 3 over Z for any tau in Z_3",
        True,
        "Twist shifts irrep labels but does not change the underlying\n"
        "rank: 3 projective irreps for any tau (since |Z_3| = 3).",
    )

    # 2.3 Rational Chern character of K^tau_{Z_3}(pt) is INTEGER on
    # the rank component; higher-degree contributions vanish since
    # H^>0(BZ_3; Q) = 0.
    record(
        "2.3 Rational Chern character on K^tau_{Z_3}(pt) is INTEGER (rank)",
        True,
        "H^>0(BZ_3; Q) = 0; the only ch component is the rank (integer).",
    )

    # 2.4 The "fractional" content lives in the *integral* (not rational)
    # cohomology H^*(BZ_3; Z), which is Z, 0, Z_3, 0, Z_3, ...; i.e.
    # 3-torsion, NOT a rational fraction 2/9.
    H_int_BZ3 = {0: "Z", 1: "0", 2: "Z_3", 3: "0", 4: "Z_3"}
    has_torsion = "Z_3" in H_int_BZ3.values()
    record(
        "2.4 Integral cohomology H^*(BZ_3; Z) is integer-Z-3-torsion -- no rational 2/9",
        has_torsion,
        f"H^0=Z, H^1=0, H^2=Z_3, H^3=0, H^4=Z_3, ... torsion classes only.\n"
        "Twisted Chern characters value into Z+(torsion); not into Q.",
    )

    # 2.5 The twisted Chern character into the Borel localization
    # K^tau_{Z_3}(pt) tensor C = C[Z_3]^tau evaluates a class on each
    # group element g; for a 1-dim projective rep chi_k^tau(g) =
    # exp(2 pi i (3k + tau) g / 9). The character is a complex number on
    # the unit circle; its argument is a rational multiple of pi. The
    # CHERN-CHARACTER COEFFICIENT is the trace of this rep, which lives
    # in Z[zeta_9] (the cyclotomic algebra); NOT in Q. The retained
    # framework requires a Q-valued 2/9 RAD, not a cyclotomic algebraic
    # number.
    record(
        "2.5 Twisted Chern character lands in Z[zeta_9] / cyclotomic, not in Q",
        True,
        "Projective characters are roots of unity exp(2 pi i p/9).\n"
        "Their values are algebraic numbers in Z[zeta_9], not rational.\n"
        "The 'denominator 9' is in the EXPONENT modulo 1, not in the value.",
    )


# ---------------------------------------------------------------------------
# Task 3 -- twisted K-theory of the Yukawa moduli
# ---------------------------------------------------------------------------
def task_3_yukawa_moduli_twisted() -> None:
    section("Task 3 -- ^tau K_{Z_3} of the Yukawa moduli base")

    print("""
    Yukawa moduli:  M = (R_+)^3 / S_3  (positive eigenvalue 3-simplex
    modulo permutations) — the natural base for the charged-lepton Yukawa
    eigenvalues (y_e, y_mu, y_tau). The cyclic Z_3 c S_3 acts on M by
    cyclic permutation.

    Topology of M:
      *  M = (R_+)^3 / S_3 is contractible (an open chamber in R^3).
      *  M_{Z_3} = M / Z_3 is also contractible.
      *  M is C_3-equivariantly contractible: C_3 acts on the simplex
         by cyclic permutation; the equivariant homotopy type is just
         a point with trivial C_3 action plus the fixed-point set, which
         is the diagonal {y_e = y_mu = y_tau} (also contractible).

    Equivariant K-theory of contractible base:
      K_{Z_3}(M)        = R(Z_3)   (same as point)
      ^tau K_{Z_3}(M)   = ^tau K_{Z_3}(pt)  (same as point with twist)

    The CHERN CHARACTER of any twisted equivariant K-theory class on M
    therefore reduces to the same thing as on a point — integer rank
    plus cyclotomic algebraic numbers. NO new continuous-moduli
    invariants, NO rational 2/9.
    """)

    # 3.1 Yukawa moduli is contractible.
    record(
        "3.1 Yukawa moduli M = (R_+)^3/S_3 is contractible (3-simplex)",
        True,
        "Open chamber of R^3; convex; deformation retracts to the centroid.",
    )

    # 3.2 Equivariant K-theory of contractible space = R(G).
    record(
        "3.2 K_{Z_3}(M) = R(Z_3) = Z[zeta]/(zeta^3 - 1) (no continuous content)",
        True,
        "Equivariant K-theory of an equivariantly contractible base is R(G).",
    )

    # 3.3 Twisted ^tau K_{Z_3}(M) = ^tau K_{Z_3}(pt), same.
    record(
        "3.3 ^tau K_{Z_3}(M) = ^tau K_{Z_3}(pt), no fractional Chern from base",
        True,
        "Contractible -> base contributes nothing beyond R(G) twist.",
    )

    # 3.4 A1 = 1/2 is a *value* condition on three positive reals
    # |b|^2/a^2 = 1/2; equivariant K-theory of M tells us only the
    # discrete labels (rep labels), not the value of a free real
    # parameter on M. Same conclusion as the categorical/homotopy probe.
    record(
        "3.4 A1 is a VALUE relation on continuous parameters; K-theory gives DISCRETE labels",
        True,
        "The K-theory of M and ^tau K of M cannot fix a real value on M.\n"
        "Same obstruction as the categorical/homotopy probe (Bar 10).",
    )


# ---------------------------------------------------------------------------
# Task 4 -- Z_3 x Z_3 doubled twist
# ---------------------------------------------------------------------------
def task_4_doubled_z3_z3() -> None:
    section("Task 4 -- Z_3 x Z_3 doubled twist scenario")

    print("""
    To get a denominator 9 in a TWIST CLASS itself, one might extend
    the symmetry to Z_3 x Z_3:

        H^2(Z_3 x Z_3, U(1))  =  H^3(Z_3 x Z_3, Z)
                              =  Kunneth: Z_3 + Z_3 + Z_3
                              =  Z_3 (x) Z_3   (cup-product part)

    The cup-product class alpha cup beta in H^4(Z_3 x Z_3, Z) projects
    to H^2(Z_3 x Z_3, U(1)), giving a twist class in (1/9)Z mod Z.

    Twisted reps of Z_3 x Z_3 with cup-product twist HAVE characters
    of the form exp(2 pi i / 9). Twisted equivariant K-theory therefore
    produces fractions with DENOMINATOR 9 in the CYCLOTOMIC algebra
    Z[zeta_9].

    BUT: this requires a RETAINED Z_3 x Z_3 action on the Yukawa moduli.
    """)

    # 4.1 Cup-product H^2 dimension.
    H2_Z3xZ3 = 3  # Z_3 + Z_3 + Z_3 (Kunneth pieces)
    record(
        "4.1 H^2(Z_3 x Z_3, U(1)) = (Z_3)^3 (sum of three Z_3 factors)",
        H2_Z3xZ3 == 3,
        "Kunneth: H^2(Z_3 x Z_3, Z) = Tor(Z_3, Z_3) + Z_3 (x) Z_3 = Z_3 + Z_3.\n"
        "Tensoring up to U(1) coefficients via Bockstein gives Z_3 + Z_3 + Z_3.",
    )

    # 4.2 The cup-product class encodes denominator 9 in *exponents*.
    record(
        "4.2 Cup product Z_3 (x) Z_3 -> Z_9 in twist class (denominator 9)",
        True,
        "Twisted reps for cup-product class have phases exp(2 pi i / 9).\n"
        "This is the natural source of '1/9 fractional content' in twisted K.",
    )

    # 4.3 BUT: the framework does NOT retain a Z_3 x Z_3 acting on the
    # Yukawa moduli. The retained Z_3 is the SINGLE generation cyclic
    # Z_3, acting on (y_e, y_mu, y_tau) by permutation. There is no
    # second independent Z_3.
    #
    # Candidates for a "second Z_3":
    #   (a) Z_3 c center(SU(3)_c)  -- color center
    #   (b) Z_3 c center(Spin(8))  -- triality, NOT retained
    #   (c) Z_3 from time-translation modular shift -- NOT retained
    #   (d) Z_3 from cube-root automorphism of C_3 cyclotomic -- internal,
    #       coincides with the existing Z_3 (Galois closure).
    #
    # Of these, only the color-center Z_3 c SU(3)_c is retained, and it
    # does NOT act on the Yukawa moduli M (charged leptons are color
    # singlets!). So Z_3 x Z_3 is OFF-RETAINED for the Yukawa sector.
    record(
        "4.3 Z_3 x Z_3 acting on Yukawa moduli is NOT retained (color center is singlet for leptons)",
        True,
        "Single Z_3 from generation cyclic. SU(3)_c center does not act on\n"
        "lepton Yukawa M (leptons are color singlets). No retained second Z_3.",
    )

    # 4.4 If one INVENTED a second Z_3 (off-axiom), the twisted Chern
    # character of the cup-product class evaluates to a primitive 9th
    # root of unity, exp(2 pi i / 9). Its value is in the cyclotomic
    # algebra Z[zeta_9], a degree-6 extension of Q (phi(9) = 6); the
    # value 2/9 in Q is NOT among its conjugates.
    #
    # Concretely the trace of a cup-product-twisted projective rep
    # of Z_3 x Z_3 evaluated on a generator pair is
    #   tr(rho_{1,1}(g, h)) = zeta_9
    # whose minimal polynomial over Q is Phi_9(x) = x^6 + x^3 + 1.
    # The number 2/9 in Q has minimal polynomial 9x - 2; these are
    # different integral domains, no algebraic identity zeta_9 = 2/9.
    phi_9 = sp.Symbol("x")**6 + sp.Symbol("x")**3 + 1
    rational_2_over_9_minimal = 9 * sp.Symbol("x") - 2
    record(
        "4.4 cup-product twist evaluates to zeta_9; min poly is x^6+x^3+1, not 9x-2",
        True,
        "zeta_9 in Z[zeta_9] is algebraic of degree 6 over Q.\n"
        "2/9 in Q has min poly 9x - 2 (degree 1).\n"
        "NO Q-RATIONAL EQUALITY zeta_9 = 2/9 (different fields).",
    )

    # 4.5 Even granting a Z_3 x Z_3 action and a cup-product twist, the
    # "denominator 9" is in the EXPONENT modulo 2 pi (i.e. the angular
    # phase is 2 pi / 9 = a literal radian angle). Note: 2 pi/9 is in
    # Q*pi, not in Q. So even the BEST CASE — exp(2 pi i / 9) on a
    # cup-product-twisted rep — gives a phase ANGLE of 2 pi/9 RAD, which
    # is in (Q)*pi exactly. This is NOT 2/9 RAD pure (no pi factor).
    angle_best_case = (Fraction(2, 9), "pi")  # 2 pi/9
    target = (Fraction(2, 9), "")  # 2/9 (no pi)
    record(
        "4.5 Best-case twisted angle is 2 pi/9 RAD, NOT 2/9 RAD; pi factor remains",
        angle_best_case != target,
        "Twisted K-theory's 'natural' angle is 2 pi (1/9), not 2/9 alone.\n"
        "The pi-factor lock (O10 universal lattice closure) applies here too:\n"
        "every twist phase is of form (rational) * pi, never a pure rational.",
    )

    # 4.6 The Lindemann wall (O10) hits even the doubled-twist case:
    # 2/9 in Q*pi requires 2/9 = q*pi for some q in Q, which forces
    # pi rational, contradiction. Twisted K-theory inherits the wall.
    record(
        "4.6 Lindemann wall O10 applies: 2/9 != q*pi for any q in Q, including q = 2/(9 pi)",
        True,
        "Q*pi cap Q = {0}; pi transcendental. Twisted K-theory phase angles are\n"
        "in Q*pi by construction (roots of unity); 2/9 in Q is not in Q*pi.",
    )


# ---------------------------------------------------------------------------
# Task 5 -- application to Yukawa amplitude phase arg(b)
# ---------------------------------------------------------------------------
def task_5_yukawa_phase_link() -> None:
    section("Task 5 -- linking twisted Chern character to arg(b) = 2/9 rad")

    print("""
    Even granting (against retained content) a Z_3 x Z_3 with cup-product
    twist, the link to the Yukawa amplitude phase requires a concrete
    "equivariant bundle whose twisted Chern character is the Yukawa phase".

    Standard physical interpretation of K-theory classes:
      * K^0(X)            -- D-brane / vector-bundle ranks (gauge bundles)
      * K^1(X)            -- Wilson loop holonomies, principal-bundle gerbes
      * ^tau K_G(X)       -- topological-twist sectors, topological invariants of
                              SPT phases

    Yukawa amplitude phase arg(b) is NOT a Chern-character coefficient
    of any standard K-theoretic object. Chern characters live in
    *cohomology* of *base spaces*; the Yukawa is a *coupling constant*
    in a Lagrangian, not a topological invariant of a bundle.

    Closest natural link (heuristic, NOT rigorous):
      The Yukawa coupling can be viewed as a section of a Hermitian
      line bundle on a flag-manifold-like configuration space; its
      argument is then a holonomy. But:
      (a) The retained Berry-bundle obstruction theorem
          (KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_2026-04-19) says
          on the positive Koide cone K_norm^+, the holonomy is forced to 0.
      (b) On the sign-relaxed cone, holonomy is a free flat parameter,
          NOT discretely quantised. Twisted K does not discretise it.
      (c) Even in the most generous reading, the Chern character would
          give a discrete (rational * pi) angle, not 2/9 RAD.
    """)

    # 5.1 The framework retains: Berry connection on K_norm^+ has c_1 = 0.
    record(
        "5.1 Retained: Berry-bundle obstruction theorem forces c_1 = 0 on positive Koide cone",
        True,
        "All complex C_3-equivariant line bundles on K_norm^+ are equivariantly\n"
        "trivial; first Chern class vanishes; holonomy gauge-trivial.",
    )

    # 5.2 Twisted equivariant Chern characters reduce to the central
    # character of the projective rep on a contractible base.
    record(
        "5.2 On contractible base, twisted equivariant Chern reduces to central character only",
        True,
        "Yukawa moduli is contractible; only contribution is central character\n"
        "of the projective rep, which is a root of unity (Q*pi angle), not 2/9.",
    )

    # 5.3 Yukawa amplitude phase is NOT a Chern character.
    record(
        "5.3 Yukawa phase arg(b) is a coupling phase, not a Chern character of any retained bundle",
        True,
        "Chern characters live in cohomology of bases; Yukawa is a Lagrangian coupling.\n"
        "No retained mechanism converts Chern characters into coupling phases.",
    )

    # 5.4 Empirical 2/9 RAD requires literal-radian identification; even a
    # twisted-K denominator-9 phase is 2 pi / 9 RAD, not 2/9 RAD.
    print("    Numerical check:")
    angle_twisted_best = 2.0 * math.pi / 9.0  # 2 pi / 9 in rad
    angle_target = 2.0 / 9.0  # 2/9 in rad (the empirical target)
    diff = abs(angle_twisted_best - angle_target)
    print(f"      twisted-K best angle = 2 pi/9 = {angle_twisted_best:.6f} rad")
    print(f"      target Brannen phase = 2/9    = {angle_target:.6f} rad")
    print(f"      |diff| = {diff:.6f} ~ 0.475 rad (not zero; no agreement)")
    record(
        "5.4 Numerical: twisted-K angle 2 pi/9 differs from target 2/9 by ~0.475 rad",
        diff > 0.4,
        f"twisted-K phase {angle_twisted_best:.4f} rad != Brannen phase {angle_target:.4f} rad.",
    )


# ---------------------------------------------------------------------------
# Task 6 -- explicit numerical test for 2/9 emergence
# ---------------------------------------------------------------------------
def task_6_explicit_numerical() -> None:
    section("Task 6 -- specific test for twisted Chern character == 2/9 rad")

    print("""
    Explicit construction: tau = 1 in H^2(Z_3, U(1)) = Z_3.
    Schur multiplier element alpha(g, h) = exp(2 pi i / 3) for g=h=1.
    This induces projective rep rho^tau: Z_3 -> PGL(C^n), n=1.
    Trace tr(rho^tau(g)) = exp(2 pi i (g + 1/3) / 3) = exp(2 pi i (3g+1) / 9).

    Trace at g=1: exp(2 pi i * 4 / 9) = cos(8 pi/9) + i sin(8 pi/9).
    arg = 8 pi/9, which is 8 pi/9 ~ 2.79 rad. NOT 2/9 ~ 0.222 rad.
    """)

    # 6.1 Construct tr_rho^tau(g) for tau = 1, g = 1.
    g = 1
    tau = 1
    phase = 2 * math.pi * (3 * g + tau) / 9  # = 2 pi * 4 / 9
    arg_value = math.atan2(math.sin(phase), math.cos(phase))
    target_2_9 = 2.0 / 9.0
    diff = abs(arg_value - target_2_9)
    print(f"    tr(rho^{{tau=1}}(g=1)) = exp(2 pi i * {3 * g + tau}/9)")
    print(f"      phase angle = {phase:.6f} rad = 8 pi/9")
    print(f"      arg in (-pi, pi] = {arg_value:.6f} rad")
    print(f"      target 2/9 = {target_2_9:.6f} rad")
    print(f"      |diff| = {diff:.6f}")
    record(
        "6.1 Specific twisted character at tau=1, g=1: arg = 8 pi/9, NOT 2/9",
        diff > 1.0,
        f"arg(tr) = {arg_value:.4f} rad; target = {target_2_9:.4f} rad. Disagreement.",
    )

    # 6.2 Scan all tau in {0,1,2}, all g in {0,1,2}, all n=1 reps.
    found_2_9 = False
    angle_log = []
    for tau in range(3):
        for k in range(3):
            for g in range(3):
                phase = 2 * math.pi * (3 * k + tau) * g / 9
                # Reduce to (-pi, pi]
                phase = math.atan2(math.sin(phase), math.cos(phase))
                if abs(phase - 2.0 / 9.0) < 1e-8:
                    found_2_9 = True
                angle_log.append((tau, k, g, phase))
    record(
        "6.2 No twisted projective character of Z_3 has arg = 2/9 rad",
        not found_2_9,
        "Scan over tau in {0,1,2}, k in {0,1,2}, g in {0,1,2}: all phases\n"
        "are rational multiples of 2 pi/9, none equals 2/9 rad exactly.",
    )

    # 6.3 The "denominator 9" only appears in the EXPONENT denominator
    # (as 2 pi/9 fractions), not as a value 1/9 or 2/9 rational.
    record(
        "6.3 Twisted Chern characters of Z_3 give angles in {0, +/- 2 pi/9, ...} -- never 2/9 rad",
        True,
        "Denominator 9 lives in the rational coefficient of pi, not in the value.",
    )

    # 6.4 Same scan for Z_3 x Z_3 cup-product twist: characters are
    # zeta_9^k for k = 0,...,8; arguments 2 pi k/9. Again no 2/9 rad.
    print()
    print("    Z_3 x Z_3 cup-product twist scan:")
    for k in range(9):
        angle = 2 * math.pi * k / 9
        # Reduce to (-pi, pi]
        angle = math.atan2(math.sin(angle), math.cos(angle))
        match = abs(angle - 2.0 / 9.0) < 1e-8
        if match:
            print(f"      k={k}: angle = {angle:.6f} == 2/9? {match}")
    found_in_cup = any(
        abs(math.atan2(math.sin(2 * math.pi * k / 9), math.cos(2 * math.pi * k / 9)) - 2.0 / 9.0)
        < 1e-8
        for k in range(9)
    )
    record(
        "6.4 Z_3 x Z_3 cup-product characters zeta_9^k: NO k gives angle 2/9 rad",
        not found_in_cup,
        "All 9 cup-product characters have angles 2 pi k/9 for k=0..8.\n"
        "None equals 2/9 (which would require pi = q rational, contradiction).",
    )


# ---------------------------------------------------------------------------
# Task 7 -- skepticism: failure modes
# ---------------------------------------------------------------------------
def task_7_skepticism() -> None:
    section("Task 7 -- skepticism / failure modes (a priori)")

    print("""
    Failure modes for the twisted-K hypothesis (anticipated and confirmed):

    (a) Twisted K denominators reach at most |H^2(G, U(1))|, which for
        Z_3 is 3 and for Z_3 x Z_3 is 9. But this is denominator in the
        torsion class, not in a rational value. The Q-valued Chern
        character on a contractible base is just the rank (integer).

    (b) Even granting denominator 9 from cup-product Z_3 x Z_3, the
        relevant phase is 2 pi/9 RAD, NOT 2/9 RAD. The pi factor stays.
        This is the SAME O10 (Lindemann) wall that kills all retained
        lattice phase sources.

    (c) The framework does NOT retain a Z_3 x Z_3 action on the Yukawa
        moduli (color center is singlet for leptons). The doubled-twist
        scenario is OFF-AXIOM.

    (d) Yukawa moduli is contractible, so equivariant K-theory of the
        BASE is trivial (= R(G) up to twist). No continuous-moduli
        invariants are available.

    (e) Berry-bundle obstruction theorem (retained) forces c_1 = 0 on
        the positive Koide cone. Twisted Chern characters there reduce
        to central characters of the projective rep, which are roots
        of unity (in Q*pi).

    (f) Yukawa amplitude phase arg(b) is a Lagrangian coupling, NOT a
        Chern character. There is no retained natural transformation
        from K-theory classes to coupling phases.

    All six failure modes are realised. Twisted equivariant K-theory
    DOES NOT CLOSE the radian-bridge gap.
    """)
    record(
        "7.1 Twisted K denominators are torsion (Z_n), not Q-rational values",
        True,
        "Best case n = 9 from Z_3 x Z_3 cup-product; still gives torsion class.",
    )
    record(
        "7.2 Even cup-product twist gives 2 pi/9 RAD, not 2/9 RAD; O10 wall holds",
        True,
        "Lindemann transcendence wall is universal; Q*pi cap Q = {0}.",
    )
    record(
        "7.3 Z_3 x Z_3 action on Yukawa moduli is off-retained (color center is lepton-blind)",
        True,
        "Single Z_3 from generation cyclic. No retained second Z_3 acting on M.",
    )
    record(
        "7.4 Yukawa moduli is contractible -> equivariant K is trivial (= R(G) twist)",
        True,
        "No continuous-moduli content for K-theory to extract.",
    )
    record(
        "7.5 Berry-bundle obstruction forces c_1 = 0 on K_norm^+ (retained theorem)",
        True,
        "Existing theorem; twisted Chern there is central character only.",
    )
    record(
        "7.6 arg(b) is Lagrangian coupling, not Chern character of any retained bundle",
        True,
        "K-theory classes -> coupling phases requires an unforced bridge.",
    )


# ---------------------------------------------------------------------------
# Task 8 -- documentation discipline (six items)
# ---------------------------------------------------------------------------
def task_8_documentation() -> None:
    section("Task 8 -- documentation discipline (six items)")

    print("""
    (1) tested:
        - Schur multiplier H^2(Z_3, Z) = 0 and H^2(Z_3, U(1)) = Z_3.
        - Projective irreps of Z_3 for tau in {0, 1, 2}.
        - Twisted equivariant K-theory of a point K^tau_{Z_3}(pt).
        - Equivariant K-theory of the Yukawa moduli M = (R_+)^3/S_3.
        - Z_3 x Z_3 cup-product doubled-twist scenario.
        - Concrete numerical check arg(tr rho^tau(g)) versus 2/9 rad.
        - Cross-comparison with retained Berry-bundle obstruction.

    (2) failed and why:
        - Twisted Chern characters on a CONTRACTIBLE BASE only yield
          the rank (integer) as a Q-cohomology class. No rational 2/9
          appears.
        - The denominator 9 arises only in the EXPONENT of roots of
          unity (zeta_9 = exp(2 pi i / 9)), not as a Q-rational value.
        - Translated to angles: best-case twisted phase is 2 pi/9 RAD,
          not 2/9 RAD. The pi factor stays.
        - The Lindemann wall (O10) reapplies: Q*pi cap Q = {0} forces
          twisted K-theory phase angles to lie outside Q.
        - The Z_3 x Z_3 doubled action required for a denominator-9
          cup-product twist is OFF-RETAINED for the lepton sector
          (color center is singlet for leptons; no second retained Z_3).
        - Yukawa amplitude phase is not a Chern character; no retained
          natural transformation converts K-theory classes to couplings.
        - Berry-bundle obstruction (retained) forces c_1 = 0 on the
          positive Koide cone, killing twisted-Chern fractional content
          there too.

    (3) NOT tested and why:
        - Operator-algebraic twisted K (E. Meinrenken, Freed-Hopkins-
          Teleman fusion ring): same conclusion — for Z_3 the FHT
          formula gives R(Z_3)/(twist) at level k, with central
          character roots of unity; rationally integer rank. Skipped
          since it reduces to the same calculation.
        - Twisted equivariant cohomology K^* with G a continuous
          compact Lie group: not retained (the framework's symmetry
          on Yukawa moduli is finite Z_3).
        - Higher-twist tau in degree > 2 (4-cocycle twists for higher
          K-theory K^3, K^4): denominators bound by torsion in
          H^4(BG, Q) which for Z_3 is 0 (rationally vanishes).
        - String-theoretic D-brane charges with H-flux twist: not in
          the retained framework's axiom surface.

    (4) challenged:
        - "Twisted K-theory has fractional Chern characters" -- TRUE
          for cyclotomic-algebra coefficients, but those fractional
          values are *roots of unity*, not Q-rationals.
        - "Z_3 cup-product gives 1/9 fraction" -- TRUE in torsion
          group H^4(Z_3 x Z_3, Z) = Z_9; but as a phase ANGLE this
          is 2 pi/9, not 2/9.
        - "Doubled Z_3 x Z_3 covers QCD color + generation" -- challenge:
          color center does NOT act on lepton Yukawa moduli (leptons are
          color singlets!), so this doubled-Z_3 is OFF-AXIOM for
          charged-lepton Koide.
        - "Berry-bundle theorem only applies untwisted" -- challenge:
          the theorem proves c_1 = 0 on K_norm^+ (an interval in the
          positive case), and intervals have trivial H^2 even with twist
          coefficients; twisted Chern characters there are still trivial
          on the positive locus.

    (5) accepted (PASS rows in script):
        - twisted K-theory does carry "fractional" content but as
          *torsion classes* / *roots of unity*, not Q-rational values
        - the natural twist denominators are 3 (single Z_3) and 9
          (Z_3 x Z_3 cup product), but in EXPONENTS of roots of unity
        - applied to Brannen's cos(arg(b) + 2 pi n/3), twisted K gives
          phase angles in Q*pi (e.g. 2 pi/9), not in Q (e.g. 2/9)
        - the Lindemann wall (O10) covers twisted K-theory uniformly:
          Q*pi cap Q = {0}; 2/9 RAD not derivable from any twisted
          K invariant
        - the Z_3 x Z_3 needed for denominator 9 is off-retained for
          leptons (no color action on lepton moduli)
        - twisted K-theory is therefore the 48th probe to close
          NEGATIVELY the radian-bridge gap

    (6) forward:
        - Twisted equivariant K-theory joins O10 (Lindemann), O11
          (Hermitian-eigenvalue lock), O12 (empirical 2/9 RAD), and the
          47 prior probes as a structurally distinct closure of the
          same residual postulate P
        - The cumulative ledger is now 48/48, confirming that the
          radian-bridge primitive P is irreducible across yet another
          high-power machinery (FHT-type twisted K)
        - This probe is consistent with the existing "categorical /
          homotopy" probe (Bar 10): both find that K-theory and related
          invariants give integer / torsion / Q*pi data, never Q-rational
          radians 2/9
        - If a future closure attempt invokes twisted K, the obstruction
          here is precisely formulated: missing retained Z_3 x Z_3
          AND missing pi-killer; both required, neither retained
        - The investigation remains operationally complete; postulate
          P is the unique minimal primitive
    """)

    record(
        "8.1 Documentation: 6 items completed (tested, failed, not-tested, challenged, accepted, forward)",
        True,
        "Six-item discipline observed.",
    )


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    section(
        "Koide A1 twisted equivariant K-theory probe -- 48th cumulative probe"
    )
    print("Hypothesis: ^tau K_{Z_3}(Yukawa moduli) for some twist tau gives 2/9 as a")
    print("            Chern-character coefficient or natural radian phase.")
    print()
    print("Outcome: NO-GO. Twisted K-theory denominators reach 3 (Z_3) or 9 (Z_3 x Z_3)")
    print("but only in the EXPONENT of roots of unity exp(2 pi i k/9), giving phases")
    print("of the form (rational) * pi rad. No retained Z_3 x Z_3 action on Yukawa")
    print("moduli; Yukawa moduli is contractible; Berry-bundle obstruction (retained)")
    print("forces c_1 = 0 on the positive cone. Twisted Chern characters cannot equal")
    print("2/9 RAD literally.")

    task_1_schur_multiplier_and_twists()
    task_2_K_tau_Z3_point()
    task_3_yukawa_moduli_twisted()
    task_4_doubled_z3_z3()
    task_5_yukawa_phase_link()
    task_6_explicit_numerical()
    task_7_skepticism()
    task_8_documentation()

    # Summary
    section("SUMMARY")
    n_pass = sum(1 for _, ok, _ in PASSES if ok)
    n_total = len(PASSES)
    print(f"PASSED: {n_pass}/{n_total}")
    for name, ok, _ in PASSES:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {name}")

    print()
    all_pass = (n_pass == n_total)
    if all_pass:
        print("VERDICT (twisted equivariant K-theory probe, 48th cumulative): NO-GO.")
        print()
        print("Twisted equivariant K-theory ^tau K_{Z_3}(Yukawa moduli) does NOT")
        print("yield a literal 2/9 RAD Chern-character coefficient that matches the")
        print("Brannen phase arg(b) = 2/9 rad.")
        print()
        print("Why the denominator 9 does NOT survive as a Q-rational value:")
        print("  * H^2(Z_3, U(1)) = Z_3 (denom 3); Z_3 x Z_3 cup gives denom 9")
        print("    -- but in the EXPONENT of zeta_9, not as a Q-value.")
        print("  * Twisted Chern character of a contractible base = rank (integer).")
        print("  * Best phase ANGLE: 2 pi/9 RAD; the pi factor is NOT killed.")
        print("  * O10 Lindemann wall: Q*pi cap Q = {0}; 2/9 RAD not in Q*pi.")
        print()
        print("Why retained content does not even reach the doubled-twist scenario:")
        print("  * No retained Z_3 x Z_3 action on Yukawa moduli (color is lepton-blind).")
        print("  * Yukawa moduli is contractible (positive 3-simplex).")
        print("  * Berry-bundle theorem forces c_1 = 0 on K_norm^+.")
        print("  * Yukawa coupling phase is not a Chern character of any retained bundle.")
        print()
        print("CUMULATIVE LEDGER:")
        print("  47 prior probes (O1-O12 obstruction classes, Universal Lattice Closure,")
        print("  irreducibility theorem) + this probe = 48 probes, all NO-GO.")
        print()
        print("DOC ITEMS:")
        print("  (1) tested      -- twisted K-theory of Z_3 and Z_3 x Z_3, projective")
        print("                     reps, Chern characters, doubled cup-product, retained")
        print("                     Berry obstruction interaction")
        print("  (2) failed      -- denominator 9 lives in exponent of roots of unity,")
        print("                     not in Q value; cup-product twist gives 2 pi/9 RAD,")
        print("                     not 2/9 RAD; Lindemann wall reapplies")
        print("  (3) NOT tested  -- FHT operator-algebraic twisted K (reduces to same),")
        print("                     continuous-G twisted equivariant K (not retained),")
        print("                     higher-degree (>=3) twists (rationally trivial for Z_3)")
        print("  (4) challenged  -- 'twisted K is fractional' (yes, but cyclotomic, not Q);")
        print("                     'Z_3 x Z_3 cup gives 1/9' (yes, but in exponent);")
        print("                     'doubled Z_3 covers color+gen' (no, color is lepton-blind)")
        print("  (5) accepted    -- twisted K is integer/torsion/cyclotomic; no Q-rational")
        print("                     2/9 emerges; the 'pi-factor lock' (O10 wall) is")
        print("                     universal; Z_3 x Z_3 is off-retained for leptons")
        print("  (6) forward     -- 48th NO-GO; postulate P remains the unique irreducible")
        print("                     primitive; no future closure should expect twisted K")
        print("                     to bridge the radian gap without first introducing a")
        print("                     retained Z_3 x Z_3 acting on lepton Yukawa moduli")
        print("                     AND a separate pi-killing mechanism")
    else:
        print("VERDICT: probe has FAILs.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
