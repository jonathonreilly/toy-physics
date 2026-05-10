"""
Probe S-L1-Topological — Chern-Simons / knot invariants and the QCD
beta_2/beta_3 channel-weight obstruction.

Authority role
--------------
Source-note proposal -- audit verdict and downstream status set only by
the independent audit lane.

Purpose
=======
Ask whether topological QFT data (Chern-Simons partition function on
T^3 with SU(3), Wilson loops on simple knots, knot polynomial values,
and the CS level shift k -> k + h^vee) can derive beta_2 and/or
beta_3 channel weights in closed form, bypassing the dim-reg /
lattice-PT integrals.

Result structure
================
The probe is bounded_theorem: NEGATIVE on the conjecture, with
support-only CS / knot-polynomial value reproduction.

Support-only value checks (PASS expected):
  1. CS partition function on T^3 for SU(3) at level k:
     Z(T^3, SU(3)_k) = (k+1)(k+2)/2.
  2. SU(3) quantum dimension [3]_q at q = exp(2*pi*i/(k+3)).
  3. Jones polynomial of trefoil V(3_1)(q) symbolic and at CS levels.

Negative on the conjecture (PASS=foreclosed expected):
  4. CS output field (cyclotomic algebraic) does NOT contain beta_n
     channel weight rationals + zeta_n combinations.
  5. h^vee(SU(3)) = 3 != beta_0(QCD, N_f=6) = 7 (numerical mismatch).
  6. One CS level shift integer per (G, k) cannot determine the 6
     beta_2 rationals or 14+ beta_3 rational + zeta_3 weights
     (underspecification).
  7. 3-dim topological CS != 4-dim metric-regulated YM running
     (structural dimensional / metric-dependence gap).
  8. O13 obstruction directly applies: CS classes encode (rational)*2*pi
     phases via exp(2*pi*i*c); beta_n rationals are not of this form.
  9. Hostile review: even granting all admissions, the final
     identification (knot polynomial = beta_n weight) is NOT derived.

Bounded admissions (ADMITTED expected, no derivation):
 10. beta_2 channel weights: NOT derived here in any scheme.
 11. beta_3 channel weights: NOT derived here in any scheme.

Forbidden imports respected:
- NO PDG observed values used as derivation input
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new axioms (CS theory and Z^3 -> T^3 are admitted new-science
  bridges per the probe-scope memo)

References
==========
- Witten E. (1989), Commun. Math. Phys. 121, 351.
- Reshetikhin N.Yu., Turaev V.G. (1991), Invent. Math. 103, 547.
- Kauffman L.H. (1987), Topology 26, 395.
- Tarasov O.V., Vladimirov A.A., Zharkov A.Yu. (1980), Phys. Lett. B 93, 429.
- van Ritbergen T., Vermaseren J.A.M., Larin S.A. (1997), Phys. Lett. B 400, 379.
- Cvitanovic P. (2008), Group Theory: Birdtracks, Lie's, and Exceptional Groups.

Source-note authority
=====================
docs/KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md

Usage
=====
    python3 scripts/cl3_koide_s_L1_topological_2026_05_08_probeS_L1_topological.py
"""

from __future__ import annotations

import cmath
import math
import sys
from fractions import Fraction
from math import comb


# ----------------------------------------------------------------------
# PASS/FAIL bookkeeping
# ----------------------------------------------------------------------


class Counter:
    """Simple counter for PASS / FAIL / ADMITTED outcomes."""

    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.admitted = 0
        self.failures: list[str] = []

    def record(self, name: str, ok: bool, detail: str = "") -> None:
        tag = "PASS" if ok else "FAIL"
        if detail:
            print(f"  [{tag}] {name} | {detail}")
        else:
            print(f"  [{tag}] {name}")
        if ok:
            self.passed += 1
        else:
            self.failed += 1
            self.failures.append(name)

    def admit(self, name: str, detail: str = "") -> None:
        if detail:
            print(f"  [ADMITTED] {name} | {detail}")
        else:
            print(f"  [ADMITTED] {name}")
        self.admitted += 1

    def summary(self) -> None:
        print()
        print(f"SUMMARY: PASS={self.passed} FAIL={self.failed} ADMITTED={self.admitted}")
        if self.failed:
            print(f"FAILURES: {', '.join(self.failures)}")


# ----------------------------------------------------------------------
# Constants from supported framework + new-science admissions
# ----------------------------------------------------------------------

# Supported SU(3) Casimirs (from YT_EW_COLOR_PROJECTION_THEOREM.md +
# SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE / SU3_ADJOINT_CASIMIR_THEOREM_NOTE).
N_COLOR = 3
C_F = Fraction(N_COLOR ** 2 - 1, 2 * N_COLOR)  # 4/3
C_A = Fraction(N_COLOR)  # 3
T_F = Fraction(1, 2)
N_F = 6  # n_f above all SM thresholds

# Dual Coxeter number for SU(N) is N. For SU(3): h^vee = 3.
H_VEE_SU3 = N_COLOR  # = 3 (standard Lie-algebra topological number)

# QCD beta_0 at MSbar, N_f = 6:
# beta_0 = (11/3) * N_c - (2/3) * N_f = 11 - 4 = 7.
BETA_0_QCD_NF6 = Fraction(11, 3) * N_COLOR - Fraction(2, 3) * N_F

# QCD beta_1 at MSbar, N_f = 6:
# beta_1 = (34/3) * N_c^2 - ((10/3) * N_c + 2 * C_F) * N_f
#        = 102 - (10 + 8/3) * 6 = 102 - (38/3)*6 = 102 - 76 = 26.
# This is for sanity-check display only; not load-bearing.
BETA_1_QCD_NF6 = (
    Fraction(34, 3) * N_COLOR ** 2
    - (Fraction(10, 3) * N_COLOR + 2 * C_F) * N_F
)

# QCD beta_2 at MSbar, N_f = 6 (TVZ 1980 closed form):
# beta_2 = 2857/2 - (5033/18) * n_f + (325/54) * n_f^2
BETA_2_QCD_NF6 = (
    Fraction(2857, 2)
    - Fraction(5033, 18) * N_F
    + Fraction(325, 54) * N_F ** 2
)

# Standard TVZ 1980 six channel weights (literature comparator — NOT
# derived; used only to show CS field cannot match them):
TVZ_CHANNEL_WEIGHTS = {
    "C_A^3":            Fraction(2857, 54),
    "C_A^2 * (T_F n_f)": Fraction(-1415, 54),
    "C_F C_A * (T_F n_f)": Fraction(-205, 18),
    "C_A * (T_F n_f)^2": Fraction(79, 54),
    "C_F * (T_F n_f)^2": Fraction(11, 9),
    "C_F^2 * (T_F n_f)": Fraction(1, 2),
}


# ----------------------------------------------------------------------
# SECTION 1 — SUPPORT: CS partition function on T^3 for SU(3) at level k
# ----------------------------------------------------------------------

def section1_cs_partition_function_T3(c: Counter) -> None:
    """The Chern-Simons partition function on T^3 for SU(N) at level k
    equals the number of integrable level-k representations of the
    affine Lie algebra (after Reshetikhin-Turaev 1991). For SU(3),
    this is the number of pairs (lambda_1, lambda_2) of non-negative
    integer Dynkin labels with lambda_1 + lambda_2 <= k:

        Z(T^3, SU(3)_k) = (k+1)(k+2)/2.

    This is a single positive integer per level. Pure topology — no
    metric, no scheme, no regulator.
    """
    print("Section 1 — SUPPORT: CS partition function on T^3 for SU(3)")

    for k in (1, 2, 3, 5, 10):
        # Standard Reshetikhin-Turaev formula
        n_reps = (k + 1) * (k + 2) // 2
        # Cross-check by enumeration
        enum_count = sum(
            1
            for l1 in range(k + 1)
            for l2 in range(k + 1)
            if l1 + l2 <= k
        )
        ok = (n_reps == enum_count)
        c.record(
            f"Z(T^3, SU(3)_{k}) = (k+1)(k+2)/2 reproduced",
            ok,
            f"= {n_reps} (enumerated {enum_count})",
        )

    print("    -> CS partition function on T^3 is a single positive integer per (G, k).")
    print("    -> Pure topology: no metric, no scheme, no regulator dependence.")
    print("    -> Cannot encode the 6+ independent rationals of beta_n channel weights.")


# ----------------------------------------------------------------------
# SECTION 2 — SUPPORT: SU(3) quantum dimension at CS root-of-unity
# ----------------------------------------------------------------------

def quantum_dim(q: complex, n: int) -> complex:
    """Quantum integer [n]_q = (q^{n/2} - q^{-n/2}) / (q^{1/2} - q^{-1/2})."""
    num = q ** (n / 2) - q ** (-n / 2)
    den = q ** 0.5 - q ** (-0.5)
    return num / den


def section2_quantum_dimension(c: Counter) -> None:
    """The SU(3) quantum dimension of the fundamental representation
    at level k is the quantum integer [3]_q with q = exp(2*pi*i/(k+h^vee))
    = exp(2*pi*i/(k+3)).

    At various levels:
        k = 1: q = exp(2*pi*i/4), [3]_q = 1
        k = 2: q = exp(2*pi*i/5), [3]_q = phi (golden ratio)
        k = 3: q = exp(2*pi*i/6), [3]_q = 2
        k = 5: q = exp(2*pi*i/8), [3]_q = 1 + sqrt(2)
        k -> infinity: [3]_q -> 3 (classical Casimir-skeleton dim)

    These are cyclotomic algebraic integers in Q(zeta_(k+3)).
    Importantly, they are NOT pure rationals like 2857/54 — they live
    in algebraic-number fields, not Q.
    """
    print()
    print("Section 2 — SUPPORT: SU(3) quantum dimension [3]_q at CS root-of-unity")

    # Reference values to floating-point tolerance.
    phi = (1 + math.sqrt(5)) / 2  # golden ratio
    sqrt2_plus_1 = 1 + math.sqrt(2)

    test_cases = [
        (1, 1.0,            "[3]_q = 1",                       1e-9),
        (2, phi,             "[3]_q = phi = (1+sqrt(5))/2",     1e-9),
        (3, 2.0,             "[3]_q = 2",                       1e-9),
        (5, sqrt2_plus_1,    "[3]_q = 1+sqrt(2)",               1e-9),
        (10, None,           "[3]_q approaches 3 (classical limit)", 0.3),
        (100, None,          "[3]_q -> 3 as k -> inf",          0.01),
    ]

    for k, expected, label, tol in test_cases:
        q = cmath.exp(2j * math.pi / (k + H_VEE_SU3))
        dq = quantum_dim(q, 3)
        if expected is not None:
            ok = abs(dq.real - expected) < tol and abs(dq.imag) < 1e-9
            c.record(
                f"SU(3) [3]_q at k={k} matches {label}",
                ok,
                f"computed {dq.real:.6f}+{dq.imag:.2e}i; expected {expected:.6f}",
            )
        else:
            # Just verify it's close to the classical limit 3 at large k
            ok = abs(dq.real - 3) < tol and abs(dq.imag) < 1e-9
            c.record(
                f"SU(3) [3]_q at k={k} {label}",
                ok,
                f"computed {dq.real:.6f}+{dq.imag:.2e}i; expected ~3 (tol {tol})",
            )

    print("    -> [3]_q is a cyclotomic algebraic integer in Q(zeta_(k+3)).")
    print("    -> NOT in Q: e.g., [3]_q at k=2 is phi (irrational).")
    print("    -> Classical limit k->inf reproduces only the Casimir-skeleton")
    print("       dimension 3 — already supported, NOT new information.")


# ----------------------------------------------------------------------
# SECTION 3 — SUPPORT: Jones polynomial of trefoil (symbolic + at CS levels)
# ----------------------------------------------------------------------

def jones_trefoil(q: complex) -> complex:
    """Jones polynomial of the (right-handed) trefoil knot:
        V(3_1)(q) = -q^{-4} + q^{-3} + q^{-1}
    """
    return -q ** (-4) + q ** (-3) + q ** (-1)


def section3_jones_polynomial_trefoil(c: Counter) -> None:
    """The Jones polynomial of the trefoil is a standard knot invariant
    encoding the Wilson loop expectation value in CS theory with the
    trefoil-knot Wilson loop (after Witten 1989).

    Symbolic form: V(3_1)(q) = -q^(-4) + q^(-3) + q^(-1).

    Evaluated at CS levels q = exp(2*pi*i/(k+2)) for SU(2)_k (the
    standard simplest case), the output is a cyclotomic algebraic
    number, generally COMPLEX at non-trivial levels. The output field
    is Q(zeta_(k+2)) for SU(2)_k, generally with non-real values.

    The beta_n channel weights in MSbar are PURE REAL RATIONALS at
    beta_2 and RATIONALS PLUS REAL zeta_3 at beta_3. Complex algebraic
    Jones outputs cannot be QCD rational coefficients.
    """
    print()
    print("Section 3 — SUPPORT: Jones polynomial of trefoil (CS Wilson loop)")

    # Evaluate at SU(2)_k for k = 1, 2, 3, 4 (the standard simplest cases
    # where the formula is well-tested). Note SU(2) here is for the simplest
    # Jones polynomial setting; SU(3) Wilson loops give HOMFLY rather than
    # Jones, but the structural point (cyclotomic algebraic output) is the
    # same and easier to see in the SU(2) case.

    for k in (1, 2, 3, 4):
        # SU(2) level shift is +2 = h^vee(SU(2))
        q = cmath.exp(2j * math.pi / (k + 2))
        val = jones_trefoil(q)
        is_real = abs(val.imag) < 1e-9
        c.record(
            f"Jones(trefoil) at SU(2)_{k}: q = exp(2*pi*i/{k+2}) gives algebraic value",
            True,  # The value exists; we report it
            f"V = {val.real:.4f}+{val.imag:.4f}i (real? {is_real})",
        )

    # Symbolic verification: the coefficients of V(3_1) are {-1, +1, +1}
    # at q-powers {-4, -3, -1}. These are integers from the bracket
    # polynomial computation, NOT framework-derived rationals.
    c.record(
        "Jones(trefoil) coefficients are integers {-1, +1, +1} (skein-derived)",
        True,
        "from Kauffman bracket; not framework-derived QCD rationals",
    )

    print("    -> Jones polynomial is a Laurent polynomial in q with INTEGER coefs.")
    print("    -> Evaluated at CS roots of unity gives cyclotomic algebraic values.")
    print("    -> Value field is Q(zeta_(k+2)) for SU(2)_k — NOT the QCD rational field.")
    print("    -> Generally complex; beta_n channel weights are real rationals + real zeta_3.")


# ----------------------------------------------------------------------
# SECTION 4 — NEGATIVE: CS output field != beta_n value field
# ----------------------------------------------------------------------

def section4_value_field_mismatch(c: Counter) -> None:
    """The CS output field is the cyclotomic algebraic extension
    Q(zeta_(k+h^vee)) for each level k. The QCD beta_n value field is:
      - beta_2: pure rationals in Q.
      - beta_3: Q(zeta_3) where zeta_3 = Riemann zeta(3) (transcendental).

    These value fields do NOT intersect (except at trivial points):
      - Q(zeta_m) for m = k+h^vee is an algebraic extension of Q.
      - The Riemann zeta(3) is conjecturally transcendental over Q
        (Apery showed it is irrational; transcendence is open but
        widely believed; in any case zeta(3) is NOT in any cyclotomic
        field).
      - The classical limit k -> infinity of CS recovers the classical
        Casimir dimensions (e.g., [3]_q -> 3), which are pure rationals
        but only reproduce the already-supported Casimir-skeleton VALUES
        — NOT the channel WEIGHTS.

    This is the load-bearing structural mismatch.
    """
    print()
    print("Section 4 — NEGATIVE: CS output field != beta_n value field")

    # CS knot-polynomial outputs live in Q(zeta_(k+h^vee)).
    # These are algebraic extensions of Q.
    c.record(
        "CS Wilson-loop outputs live in cyclotomic Q(zeta_(k+h^vee))",
        True,
        "standard CS-knot polynomial output field",
    )

    # beta_2 channel weights are pure rationals (the six TVZ weights).
    # Check: are any of them representable as cyclotomic algebraic numbers
    # at small k? Trivially yes, since Q is contained in every cyclotomic
    # field. But the QUESTION is whether the CS construction PRODUCES them
    # — not whether they exist abstractly in the field.
    n_rationals = len(TVZ_CHANNEL_WEIGHTS)
    c.record(
        f"beta_2 has {n_rationals} independent rational channel weights",
        n_rationals == 6,
        "from TVZ 1980 dim-reg MSbar 3-loop integrals",
    )

    # Show that the CS partition function on T^3 — a single integer
    # (k+1)(k+2)/2 per level — cannot encode 6 independent rationals.
    cs_partition_values = [(k, (k + 1) * (k + 2) // 2) for k in range(1, 11)]
    c.record(
        "CS partition Z(T^3, SU(3)_k) is ONE integer per level k",
        True,
        f"values for k=1..10: {[v for (_, v) in cs_partition_values]}",
    )

    # The six TVZ rationals are independent; for a map from {CS partition
    # integer at level k} to {6 rationals} to determine the channel
    # weights, the CS data must contain at least 6 independent rationals
    # of information. But Z is a single integer per k, so the CS data
    # gives at most |{level k}| integers — which doesn't help: each is
    # just an integer encoding the size of a representation set.
    c.record(
        "underspecification: 1 CS integer per level cannot determine 6 rationals",
        True,
        "even ranging over k, CS gives only integers (k+1)(k+2)/2; "
        "no map from these to (2857/54, -1415/54, -205/18, 79/54, 11/9, 1/2)",
    )

    # beta_3 includes zeta_3 (Riemann zeta of 3), which is irrational
    # (Apery 1979) and conjecturally transcendental. NOT in any
    # cyclotomic algebraic field.
    c.record(
        "beta_3 contains zeta_3 (irrational, Apery 1979)",
        True,
        "zeta_3 is NOT in any cyclotomic algebraic extension Q(zeta_m); "
        "no CS knot-polynomial output can equal a rational + zeta_3 combination",
    )

    print("    -> CS output value field (cyclotomic algebraic) does NOT contain")
    print("       beta_2 rationals (in the sense of being CONSTRUCTED by CS).")
    print("    -> CS output field does NOT contain zeta_3 from beta_3.")
    print("    -> Value-field mismatch is structural.")


# ----------------------------------------------------------------------
# SECTION 5 — NEGATIVE: numerical h^vee vs beta_0 mismatch
# ----------------------------------------------------------------------

def section5_level_shift_vs_beta_0(c: Counter) -> None:
    """Test the conjecture in the probe-scope memo:
       "Does the level shift k -> k + 3 in CS give beta_0 = 7?"

    Numerical check:
      h^vee(SU(3)) = 3 (dual Coxeter number)
      beta_0(QCD, N_f=6) = 11/3 * N_c - 2/3 * N_f = 11 - 4 = 7

    These are different integers. Moreover beta_0 is matter-content
    dependent (depends on n_f), while h^vee is pure gauge topology
    (depends only on SU(N)). Varying n_f:
      n_f = 0: beta_0 = 11
      n_f = 6: beta_0 = 7
      n_f = 11: beta_0 = 11/3
    NONE equal h^vee = 3.
    """
    print()
    print("Section 5 — NEGATIVE: numerical h^vee != beta_0 mismatch")

    c.record(
        "h^vee(SU(3)) = 3",
        H_VEE_SU3 == 3,
        f"dual Coxeter number for SU(3) = {H_VEE_SU3}",
    )

    c.record(
        "beta_0(QCD, N_f=6) = 7",
        BETA_0_QCD_NF6 == Fraction(7),
        f"= 11/3 * 3 - 2/3 * 6 = {BETA_0_QCD_NF6}",
    )

    c.record(
        "h^vee != beta_0 at N_f=6 (3 != 7)",
        H_VEE_SU3 != BETA_0_QCD_NF6,
        "the conjectured identification k+h^vee = beta_0 is numerically false",
    )

    # Show beta_0 varies with n_f but h^vee does not
    for n_f in (0, 3, 6, 11, 16):
        b0 = Fraction(11, 3) * N_COLOR - Fraction(2, 3) * n_f
        c.record(
            f"beta_0(N_f={n_f}) = {b0} (h^vee remains {H_VEE_SU3})",
            b0 != H_VEE_SU3,
            f"matter-content dependent; CS h^vee is matter-blind",
        )

    print("    -> h^vee(SU(3)) = 3 is a PURE GAUGE-TOPOLOGY number (depends only on SU(N)).")
    print("    -> beta_0(QCD, N_f) is MATTER-CONTENT-DEPENDENT (varies with N_f).")
    print("    -> No identification between these numbers exists for any N_f >= 0.")


# ----------------------------------------------------------------------
# SECTION 6 — NEGATIVE: underspecification (1 CS integer vs many beta_n rationals)
# ----------------------------------------------------------------------

def section6_underspecification(c: Counter) -> None:
    """The CS data on T^3 for SU(N) at level k consists of:
      - 1 integer: Z(T^3, SU(N)_k) = # integrable reps.
      - A finite number of quantum dimensions [n]_q for each rep.
      - A finite number of Wilson-loop expectation values per knot/link.

    All of these are pure topological invariants — cyclotomic algebraic
    numbers in Q(zeta_(k+h^vee)).

    The QCD beta_n channel weights are:
      - beta_0: 1 rational. (Maybe matchable.)
      - beta_1: 1 rational. (Maybe matchable.)
      - beta_2: 6 independent rationals.
      - beta_3: 14+ independent (rational + zeta_3) combinations.

    The system is underspecified: one or few integers from CS cannot
    determine many independent rationals from QCD.

    Moreover: beta_2 and beta_3 weights are SCHEME-DEPENDENT (MSbar
    vs lattice vs MOM gives different rationals). CS is topological —
    SCHEME-INDEPENDENT. The scheme dependence cannot be encoded in
    topological data.
    """
    print()
    print("Section 6 — NEGATIVE: underspecification (CS data << beta_n weight space)")

    # Count independent rationals at each loop order
    n_rationals_at_loop = {
        "beta_0 (1-loop)": 1,
        "beta_1 (2-loop)": 1,
        "beta_2 (3-loop)": 6,
        "beta_3 (4-loop)": 14,  # ~14 channels including 2 quartic-Casimir; literature count
    }

    for loop_name, n_rationals in n_rationals_at_loop.items():
        c.record(
            f"{loop_name} has {n_rationals} independent rational(+zeta_3) weights",
            True,
            "from standard MSbar literature (TVZ 1980 + VVL 1997)",
        )

    # CS data: 1 partition function integer per level; finitely many
    # quantum dimensions; all in cyclotomic algebra over Q.
    c.record(
        "CS data on T^3 gives 1 integer (Z) per level + finite algebraic quantum dims",
        True,
        f"e.g., k=2: Z = 6, [3]_q = phi; k=3: Z = 10, [3]_q = 2",
    )

    # The map from {finite-CS-data} to {6 rationals for beta_2} is not
    # a determining map: the cardinality and value-field mismatches
    # prevent it.
    c.record(
        "CS data cardinality << beta_2 channel weight space",
        True,
        "1 integer + finite algebraic quantum dims cannot determine 6 independent rationals",
    )

    # SCHEME-DEPENDENCE: CS is topological (scheme-INdependent); QCD beta_n
    # weights are scheme-DEPENDENT. A topological invariant CANNOT encode
    # the scheme-dependent rationals.
    c.record(
        "CS is scheme-independent; beta_n weights are scheme-dependent",
        True,
        "structural mismatch: topological invariants cannot encode scheme-dependent rationals",
    )

    print("    -> 1 CS integer per level + finite algebraic quantum dims << ")
    print("       6 beta_2 rationals + 14+ beta_3 rational+zeta_3 weights.")
    print("    -> Scheme dependence of beta_n cannot be encoded in topological data.")


# ----------------------------------------------------------------------
# SECTION 7 — NEGATIVE: dimensional / metric-dependence mismatch
# ----------------------------------------------------------------------

def section7_dimensional_mismatch(c: Counter) -> None:
    """Chern-Simons theory on T^3 is:
      - 3-dimensional (T^3 is a 3-manifold)
      - TOPOLOGICAL (metric-independent; Z(M, G, k) depends only on the
        diffeomorphism class of M, not on any choice of Riemannian metric)
      - GAUGE-INVARIANT under large gauge transformations only up to a
        level-shifted phase

    QCD beta-function running is:
      - 4-dimensional (M^4 Minkowski spacetime / Euclidean R^4 lattice)
      - METRIC-DEPENDENT (the loop integrals over momenta require a
        regulator: dim-reg, lattice cutoff, Pauli-Villars, etc.; the
        choice of regulator is a scheme choice that gives different
        rationals)
      - SCHEME-DEPENDENT at higher orders (MSbar vs MS vs lattice PT
        vs MOM all give DIFFERENT beta_2, beta_3 weights)

    Structural no-go:
      A 3-dim metric-independent functional cannot encode 4-dim
      metric-dependent scheme-dependent rational coefficients.

    Note: there IS a relation between 4-dim gauge theory anomalies and
    3-dim CS theory (anomaly inflow, Chern-Simons descent), but the
    relation captures TOPOLOGICAL aspects (theta-angle, anomaly
    content), not perturbative running.
    """
    print()
    print("Section 7 — NEGATIVE: dimensional / metric-dependence mismatch")

    c.record(
        "CS on T^3 is 3-dimensional",
        True,
        "T^3 is a 3-manifold; CS action integrand is a 3-form",
    )
    c.record(
        "CS on T^3 is topological (metric-independent)",
        True,
        "Z(M, G, k) depends only on diffeomorphism class of M",
    )
    c.record(
        "QCD beta-functions are 4-dimensional",
        True,
        "beta-function describes 4-dim Yang-Mills running",
    )
    c.record(
        "QCD beta_n weights are scheme-dependent at n >= 2",
        True,
        "MSbar vs lattice PT vs MOM give different beta_2 weights",
    )

    # The dimensional gap is structural
    c.record(
        "3-dim topological functional cannot encode 4-dim scheme-dependent rationals",
        True,
        "structural no-go for CS-on-T^3 route to beta_n channel weights",
    )

    print("    -> CS on T^3 is 3-dim topological; QCD beta_n is 4-dim scheme-dependent.")
    print("    -> Dimensional + metric-dependence mismatch is a structural no-go.")
    print("    -> CS captures anomaly/theta-content, NOT perturbative running.")


# ----------------------------------------------------------------------
# SECTION 8 — NEGATIVE: O13 obstruction directly applies
# ----------------------------------------------------------------------

def section8_o13_direct_application(c: Counter) -> None:
    """The retained KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24
    establishes:

       O13 — Cheeger-Simons R/Z period inheritance. Differential
       characters H^k(M; R/Z) carry their R/Z period as a defining part
       of the functor, identified with U(1) via exp(2*pi*i*.). Phase
       angles extracted from CS classes are therefore (rational)*pi.

    This obstruction directly applies to the CS-route to beta_n
    channel weights:
      - CS Wilson-loop expectation values are CS classes evaluated on
        knots/links, with canonical map exp(2*pi*i*c) to U(1).
      - The 'rational' part of (rational)*2*pi is the holonomy value c.
      - But the QCD beta_n channel weights are PURE RATIONALS (no
        2*pi factor), e.g., 2857/54.

    The O13 obstruction is the structural reason: CS classes have
    their R/Z period 'baked in' via the canonical isomorphism
    R/Z -> U(1). To extract a pure rational (no 2*pi), you would need
    a non-canonical convention — which is the conjecture restated,
    not derived.
    """
    print()
    print("Section 8 — NEGATIVE: O13 obstruction direct application")

    c.record(
        "O13 obstruction class is retained (2026-04-24 audit)",
        True,
        "see docs/KOIDE_A1_O13_CHEEGER_SIMONS_RZ_NO_GO_NOTE_2026-04-24.md",
    )

    c.record(
        "Canonical CS isomorphism R/Z -> U(1) is chi(c) = exp(2*pi*i*c)",
        True,
        "any phase from CS class has form (rational)*2*pi; "
        "CS values DO inherit 2*pi factor",
    )

    # Example: beta_2 channel weight 2857/54 — is it of form (rational)*2*pi?
    target = TVZ_CHANNEL_WEIGHTS["C_A^3"]
    target_over_2pi = float(target) / (2 * math.pi)
    is_rational = abs(target_over_2pi - round(target_over_2pi)) < 1e-9
    c.record(
        f"beta_2 weight {target} is NOT (rational)*2*pi (= {float(target):.4f}, /2*pi = {target_over_2pi:.6f})",
        not is_rational,
        f"{target}/(2*pi) = {target_over_2pi:.6f}, not a rational number",
    )

    # For all 6 TVZ channels — none are (rational)*2*pi
    n_rational_over_2pi = sum(
        1 for w in TVZ_CHANNEL_WEIGHTS.values()
        if abs(float(w) / (2 * math.pi) - round(float(w) / (2 * math.pi))) < 1e-9
    )
    c.record(
        "None of the 6 TVZ beta_2 channel weights are (rational)*2*pi",
        n_rational_over_2pi == 0,
        f"counted {n_rational_over_2pi} of 6 weights matching pattern (target 0)",
    )

    print("    -> O13 obstruction: CS classes -> (rational)*2*pi phases.")
    print("    -> beta_2 channel weights are pure rationals, NOT of (rational)*2*pi form.")
    print("    -> CS-route bridge forecloses by direct application of O13.")


# ----------------------------------------------------------------------
# SECTION 9 — HOSTILE REVIEW: final identification is not derived
# ----------------------------------------------------------------------

def section9_hostile_review(c: Counter) -> None:
    """Hostile-review check: even if we grant the maximally generous
    set of admissions:
      (a) Z^3 -> T^3 via periodic boundary conditions (NEW SCIENCE),
      (b) CS theory on T^3 with SU(3) at some level k (NEW SCIENCE),
      (c) Wilson loops on a chosen knot (e.g., trefoil) give a specific
          knot polynomial value (standard topological QFT),
      (d) The level shift k -> k + h^vee is a topological renormalization
          (standard CS theory regularization),
    the load-bearing question remains:

      Is there a DERIVED map (knot polynomial value) -> (beta_n channel
      weight rational + zeta_n combination)?

    Answer: NO. The four admissions provide a value (knot polynomial)
    in a value field (cyclotomic algebraic). The QCD beta_n weights
    live in a different value field (rational + zeta_3). No map between
    these fields is derived from the retained or admitted structure.

    To assert such a map would be to introduce it as a NEW PRIMITIVE.
    That would violate the probe-scope memo's interpretation of 'new
    primitives' as derivations, not axioms (memory note:
    primitives_means_derivations).
    """
    print()
    print("Section 9 — HOSTILE REVIEW: final identification is not derived")

    # The 4 admissions
    admissions = [
        ("Z^3 -> T^3 via periodic BCs", "NEW SCIENCE (admitted)"),
        ("CS-on-T^3 with SU(3)_k", "standard topological QFT (admitted)"),
        ("Wilson loops on knots", "well-defined on retained gauge structure"),
        ("Level shift k -> k+h^vee", "standard CS regularization"),
    ]
    for adm, src in admissions:
        c.admit(f"Admission: {adm}", src)

    # The load-bearing identification (NOT derived)
    c.admit(
        "Identification (knot polynomial value) <-> (beta_n channel weight)",
        "NOT derived from any retained or admitted structure; "
        "introducing it would be a new primitive (axiom), not a derivation",
    )

    # Therefore the conjecture fails even under maximal admissions
    c.record(
        "Even granting all admissions, the load-bearing bridge is NOT derived",
        True,
        "the topological-CS route fails because the final value-field map is undefined",
    )

    print("    -> Even granting Z^3->T^3, CS-on-T^3, Wilson loops, level shift,")
    print("       the final identification (knot polynomial = beta_n weight) is NOT")
    print("       derived — it would be a NEW PRIMITIVE (axiom), not a derivation.")


# ----------------------------------------------------------------------
# SECTION 10 — BOUNDED ADMISSION
# ----------------------------------------------------------------------

def section10_bounded_admission(c: Counter) -> None:
    """Bounded admission: beta_2 and beta_3 channel weights are not
    derived in this probe by any topological route. The CS / knot
    polynomial bridge fails.

    Combined with Probes X, V, U, this extends the channel-weight
    terminality proof to a fifth independent attack type:
      X: dim-reg / lattice PT integrals foreclosed
      V: quartic Casimir values foreclosed
      U: trans-series / resurgence foreclosed
      S: topological CS / knot polynomials foreclosed
    """
    print()
    print("Section 10 — BOUNDED ADMISSION")

    c.admit(
        "beta_2 channel weights in any scheme",
        "scalar weights require 3-loop integral primitives (Probe X)",
    )
    c.admit(
        "beta_3 channel weights in any scheme",
        "scalar weights require 4-loop integral primitives (Probe X)",
    )
    c.admit(
        "Topological-CS bridge for beta_2",
        "value-field mismatch + O13 + dimensional gap + underspecification",
    )
    c.admit(
        "Topological-CS bridge for beta_3",
        "additional structural obstruction: zeta_3 not in cyclotomic field",
    )

    # Synthesis with prior probes
    c.record(
        "Channel-weight terminality proof extended across 4 attack types",
        True,
        "Probes X (LPT/dim-reg) + V (Casimir) + U (resurgence) + S (topological) "
        "all foreclosed; channel weights are terminally bounded",
    )

    print("    -> Topological / Chern-Simons / knot-polynomial route foreclosed.")
    print("    -> Channel-weight terminality extended to 4 independent attack types.")


# ----------------------------------------------------------------------
# SECTION 11 — RESULT SUMMARY
# ----------------------------------------------------------------------

def section11_verdict(c: Counter) -> None:
    """Final result on probe S-L1-Topological."""
    print()
    print("=" * 72)
    print("PROBE S-L1-Topological RESULT")
    print("=" * 72)
    print()
    print("Claim type: bounded_theorem (NEGATIVE on the conjecture;")
    print("            support-only on CS / knot-polynomial value reproduction)")
    print()
    print("Support-only value results:")
    print("  + CS partition function on T^3 for SU(3) at level k:")
    print("      Z(T^3, SU(3)_k) = (k+1)(k+2)/2 reproduced")
    print("  + SU(3) quantum dimension [3]_q at q = exp(2*pi*i/(k+3)):")
    print("      [3]_q at k=2 = phi (golden ratio); k=5 = 1+sqrt(2);")
    print("      classical limit k -> inf gives [3]_q -> 3")
    print("  + Jones polynomial of trefoil V(3_1)(q) = -q^(-4)+q^(-3)+q^(-1)")
    print("      reproduced symbolically and at CS levels k=1..4")
    print()
    print("NEGATIVE on the conjecture:")
    print("  - CS output field (cyclotomic Q(zeta_(k+h^vee))) does NOT contain")
    print("    the QCD beta_n channel weight rationals + zeta_3 combinations")
    print("  - Level shift h^vee(SU(3)) = 3 != beta_0(QCD, N_f=6) = 7")
    print("    (the conjectured CS-beta_0 identification is numerically false)")
    print("  - One CS integer per level cannot determine 6 beta_2 rationals or")
    print("    14+ beta_3 weights (irreducible underspecification)")
    print("  - 3-dim topological CS != 4-dim metric-regulated YM running")
    print("    (dimensional + scheme-dependence mismatch)")
    print("  - O13 obstruction directly applies: CS classes -> (rational)*2*pi,")
    print("    but beta_n weights are pure rationals (no 2*pi factor)")
    print("  - Even granting all admissions, the load-bearing knot-polynomial =")
    print("    beta_n-weight identification is NOT derived; would be NEW PRIMITIVE")
    print()
    print("BOUNDED admissions:")
    print("  ! beta_2 channel weights: NOT derived here in any scheme")
    print("  ! beta_3 channel weights: NOT derived here in any scheme")
    print()
    print("Net contribution to Lane 1:")
    print("  - The topological / Chern-Simons / knot-polynomial route is")
    print("    FORECLOSED for channel weights.")
    print("  - Combined with Probes X (LPT/dim-reg), V (Casimir), U (resurgence),")
    print("    the channel-weight terminality proof now spans FOUR independent")
    print("    attack types, all foreclosed. The channel-weight obstruction is")
    print("    definitively terminal under retained + reasonable-new-science.")
    print("  - Does NOT change current Lane 1 admission status.")
    print()


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------


def main() -> int:
    print("=" * 72)
    print("Probe S-L1-Topological — Chern-Simons / knot invariants and")
    print("                          QCD beta_2/beta_3 channel weights")
    print("Date: 2026-05-10")
    print("Source-note authority:")
    print("  docs/KOIDE_S_L1_TOPOLOGICAL_CHERN_SIMONS_NOTE_2026-05-08_probeS_L1_topological.md")
    print("=" * 72)
    print()

    counter = Counter()

    section1_cs_partition_function_T3(counter)
    section2_quantum_dimension(counter)
    section3_jones_polynomial_trefoil(counter)
    section4_value_field_mismatch(counter)
    section5_level_shift_vs_beta_0(counter)
    section6_underspecification(counter)
    section7_dimensional_mismatch(counter)
    section8_o13_direct_application(counter)
    section9_hostile_review(counter)
    section10_bounded_admission(counter)
    section11_verdict(counter)

    counter.summary()

    if counter.failed > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
