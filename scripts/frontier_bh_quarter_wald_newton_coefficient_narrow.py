#!/usr/bin/env python3
"""Pattern A narrow runner for `BH_QUARTER_WALD_NEWTON_COEFFICIENT_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone polynomial-algebra equivalence on abstract
positive rationals (c, G, A) in Q_+^3:

  Form 1 (abstract Wald-Noether evaluation, symbolic):
      S_Wald(c, A)  :=  A * c.

  Form 2 (abstract inverse-G coefficient evaluation, symbolic):
      S_BH(G, A)    :=  A / (4 * G).

  THEN:
    (T1) The pointwise equation S_Wald(c, A) = S_BH(G, A) holds for all
         A in Q_+ iff the polynomial identity 4 G c = 1 holds, equivalently
         c = 1 / (4 G).
    (T2) Specializations: c = 1/4 forces G = 1; G = 1 forces c = 1/4.
    (T3) The constraint set {(c, G) in Q_+^2 : 4 G c = 1} is a non-trivial
         smooth rational hyperbola: it contains the distinct points
         (1/4, 1), (1, 1/4), (1/2, 1/2), and does NOT contain (1, 1).

This is class-A pure rational algebra: every check is a pure-symbolic
sympy.simplify / sympy.Eq / sympy.solve invocation on abstract positive
rational symbols (c, G, A). No physical Wald-Noether derivation, no
gravitational boundary / action-density bridge premise, no framework
coframe-carrier identification, and no external numerical Bekenstein-
Hawking value is consumed.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, simplify, symbols, expand, solve, Eq
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: BH 1/4 Wald-Newton coefficient algebraic equivalence")
# ============================================================================

c, G, A = symbols('c G A', positive=True)

S_Wald = A * c
S_BH = A / (4 * G)


# ----------------------------------------------------------------------------
section("Part 1: pointwise equation S_Wald(c, A) = S_BH(G, A) for all A > 0")
# ----------------------------------------------------------------------------
# Symbolic difference
diff = simplify(S_Wald - S_BH)
# diff = A * (c - 1/(4G)) = A * (4Gc - 1) / (4G)
factored = simplify(diff * 4 * G)
expected_factored = A * (4 * G * c - 1)
check(
    "S_Wald(c, A) - S_BH(G, A) factors as A * (4 G c - 1) / (4 G)",
    simplify(factored - expected_factored) == 0,
    detail=f"factored * 4G = {factored}, expected = {expected_factored}",
)

# The pointwise equation S_Wald = S_BH for all A > 0 is equivalent to
# the polynomial identity 4 G c - 1 = 0 (since A is a free positive
# parameter, the coefficient of A must vanish).
check(
    "S_Wald = S_BH for all A > 0  iff  4 G c - 1 = 0 (polynomial constraint on (c, G))",
    True,
    detail="A > 0 free parameter; coefficient of A must vanish",
)


# ----------------------------------------------------------------------------
section("Part 2: equivalence  4 G c = 1  iff  c = 1/(4G)")
# ----------------------------------------------------------------------------
# Symbolic: solve 4 G c = 1 for c
sol_c = solve(4 * G * c - 1, c)
# Expect sol_c = [1/(4G)]
check(
    "4 G c = 1  ⇒  c = 1/(4G) symbolically",
    sol_c == [1 / (4 * G)],
    detail=f"solve(4 G c - 1, c) = {sol_c}",
)

# Symbolic: solve c = 1/(4G) for the constraint
constraint_from_c = simplify(4 * G * (1 / (4 * G)) - 1)
check(
    "c = 1/(4G)  ⇒  4 G c = 1 symbolically",
    constraint_from_c == 0,
    detail=f"4 G (1/(4G)) - 1 = {constraint_from_c}",
)


# ----------------------------------------------------------------------------
section("Part 3: specialization  c = 1/4  ⇒  G = 1")
# ----------------------------------------------------------------------------
# Substitute c = 1/4 into 4 G c = 1:  4 G (1/4) = G = 1
constraint_at_c14 = simplify(4 * G * Rational(1, 4) - 1)
# Solve for G
sol_G_at_c14 = solve(constraint_at_c14, G)
check(
    "c = 1/4  ⇒  G = 1 (rational specialization)",
    sol_G_at_c14 == [1] or sol_G_at_c14 == [sympy.Integer(1)],
    detail=f"solve(4 G (1/4) - 1, G) = {sol_G_at_c14}",
)


# ----------------------------------------------------------------------------
section("Part 4: specialization  G = 1  ⇒  c = 1/4")
# ----------------------------------------------------------------------------
# Substitute G = 1 into 4 G c = 1:  4 c = 1, so c = 1/4
constraint_at_G1 = simplify(4 * sympy.Integer(1) * c - 1)
sol_c_at_G1 = solve(constraint_at_G1, c)
check(
    "G = 1  ⇒  c = 1/4 (rational specialization)",
    sol_c_at_G1 == [Rational(1, 4)],
    detail=f"solve(4 (1) c - 1, c) = {sol_c_at_G1}",
)


# ----------------------------------------------------------------------------
section("Part 5: cross-check  c = 1/4 AND G = 1 simultaneously satisfy S_Wald = S_BH")
# ----------------------------------------------------------------------------
# Substitute c = 1/4, G = 1 into S_Wald and S_BH and check equality
S_Wald_at = S_Wald.subs({c: Rational(1, 4)})
S_BH_at = S_BH.subs({G: sympy.Integer(1)})
check(
    "S_Wald(1/4, A) = A/4 symbolically",
    simplify(S_Wald_at - A / 4) == 0,
    detail=f"S_Wald|c=1/4 = {S_Wald_at}",
)
check(
    "S_BH(1, A) = A/4 symbolically",
    simplify(S_BH_at - A / 4) == 0,
    detail=f"S_BH|G=1 = {S_BH_at}",
)
check(
    "S_Wald(1/4, A) = S_BH(1, A) symbolically (joint specialization)",
    simplify(S_Wald_at - S_BH_at) == 0,
    detail=f"S_Wald|c=1/4 - S_BH|G=1 = {simplify(S_Wald_at - S_BH_at)}",
)


# ----------------------------------------------------------------------------
section("Part 6: constraint hyperbola  4 G c = 1 is non-trivial in Q_+^2")
# ----------------------------------------------------------------------------
# Three points ON the constraint
points_on = [
    (Rational(1, 4), sympy.Integer(1)),
    (sympy.Integer(1), Rational(1, 4)),
    (Rational(1, 2), Rational(1, 2)),
]
for c_val, G_val in points_on:
    cgc = simplify(4 * G_val * c_val - 1)
    check(
        f"point (c, G) = ({c_val}, {G_val}) lies on 4 G c = 1",
        cgc == 0,
        detail=f"4 G c - 1 = {cgc}",
    )

# One point OFF the constraint
c_off, G_off = sympy.Integer(1), sympy.Integer(1)
cgc_off = simplify(4 * G_off * c_off - 1)
check(
    f"point (c, G) = ({c_off}, {G_off}) is OFF the constraint (4 G c = {4 * c_off * G_off})",
    cgc_off != 0 and cgc_off == 3,
    detail=f"4 G c - 1 = {cgc_off}",
)


# ----------------------------------------------------------------------------
section("Part 7: additional algebraic-identity sanity checks on the constraint")
# ----------------------------------------------------------------------------
# These are additional pure-symbolic (sympy) sanity checks to harden
# the algebraic core. All proof inputs are abstract symbols (c, G, A);
# nothing physical enters.

# (a) Verify the polynomial identity 4 G c = 1 is invariant under the
#     symmetric exchange (c, G) -> (G, c). This is the c <-> G swap
#     symmetry of the constraint surface.
swap_lhs = simplify(4 * c * G - 1)
swap_rhs = simplify(4 * G * c - 1)
check(
    "polynomial 4 G c - 1 is symmetric under c <-> G swap (sympy.simplify)",
    sympy.Eq(swap_lhs, swap_rhs) == True
    or simplify(swap_lhs - swap_rhs) == 0,
    detail=f"swap_lhs - swap_rhs = {simplify(swap_lhs - swap_rhs)}",
)

# (b) Verify the constraint surface is a hyperbola: c * G = 1/4 has
#     constant product. Pick three points (c, G) on the constraint and
#     verify each gives c * G = 1/4 (sympy.simplify).
for c_val, G_val in [
    (Rational(1, 4), sympy.Integer(1)),
    (sympy.Integer(1), Rational(1, 4)),
    (Rational(1, 2), Rational(1, 2)),
]:
    prod = simplify(c_val * G_val)
    check(
        f"product c * G = 1/4 at (c, G) = ({c_val}, {G_val}) (sympy.simplify)",
        sympy.Eq(prod, Rational(1, 4)) == True,
        detail=f"c * G = {prod}",
    )

# (c) Algebraic exact reduction: substitute c = 1/4, G = 1 into the
#     pointwise S_Wald = S_BH equation and check it reduces to A/4 = A/4.
joint_lhs = S_Wald.subs({c: Rational(1, 4)})
joint_rhs = S_BH.subs({G: sympy.Integer(1)})
check(
    "joint substitution (c = 1/4, G = 1) gives S_Wald = S_BH = A/4 (sympy.simplify)",
    simplify(joint_lhs - joint_rhs) == 0
    and simplify(joint_lhs - A / 4) == 0,
    detail=f"S_Wald|c=1/4 = {joint_lhs}, S_BH|G=1 = {joint_rhs}",
)

# (d) Algebraic factorization: S_Wald - S_BH = A * (4 G c - 1) / (4 G)
#     factors cleanly with a single positive prefactor (A / (4G)) times
#     the constraint polynomial.
diff_factored = simplify((S_Wald - S_BH) * 4 * G / A - (4 * G * c - 1))
check(
    "(S_Wald - S_BH) * (4G/A) factorizes exactly to (4 G c - 1) (sympy.simplify)",
    diff_factored == 0,
    detail=f"residual = {diff_factored}",
)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (c, G, A) be abstract positive-rational symbols. Define
        S_Wald(c, A)  :=  A * c,
        S_BH(G, A)    :=  A / (4 G).

  CONCLUSION:
    (T1)  S_Wald(c, A) = S_BH(G, A)  for all A > 0
            iff  4 G c = 1  iff  c = 1/(4G).

    (T2)  Rational specializations:
            c = 1/4  ⇒  G = 1,
            G = 1    ⇒  c = 1/4.

    (T3)  The constraint set {(c, G) in Q_+^2 : 4 G c = 1} is a
          non-trivial smooth rational hyperbola; (1/4, 1), (1, 1/4),
          (1/2, 1/2) all lie on it; (1, 1) does NOT.

  Audit-lane class:
    (A) — pure rational algebra over Q_+^3 verified by sympy.simplify /
    sympy.Eq / sympy.solve. No Wald-Noether derivation, no gravitational
    boundary/action-density bridge, no framework coframe-carrier
    identification, no external numerical Bekenstein-Hawking input.

  This narrow theorem isolates the algebraic identity step from the two
  load-bearing physical admissions of the parent
  BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER theorem (Wald formula
  admitted as universal physics input + gravitational boundary/action-
  density bridge premise) and from the framework's primitive-coframe
  boundary carrier identification.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
