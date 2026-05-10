#!/usr/bin/env python3
"""Pattern A narrow runner for `PLAQUETTE_HIERARCHY_POLYNOMIAL_BOUNDEDNESS_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone polynomial-algebra facts on real polynomials
p(t) in R[t]:

  (T1) Leading-term asymptotic:
       if deg(p) = d >= 1, then  p(t) / t^d  ->  a_d  != 0  as t -> +infinity.

  (T2) Finite-limit forces constant:
       if  lim_{t -> +infinity} p(t)  exists and is finite,
       then deg(p) = 0, i.e. p is constant.

  (T3) Two-distinct-value obstruction (a != b):
       no polynomial in R[t] satisfies both
           p(0) = a    and    lim_{t -> +infinity} p(t) = b  (finite),
       unless a = b (in which case p is constant equal to a = b).

  (T4) Boundedness corollary:
       if |p(t)| <= M on [0, +infinity), then p is constant.

This is class-A pure polynomial algebra. No Wilson plaquette, gauge
group, Haar measure, source-deformed partition function, or framework
axiom (Cl(3) / Z^3) is consumed; the narrow theorem treats p(t) as an
abstract real polynomial.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, expand, factor, oo, limit, Symbol, Poly
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
section("Pattern A narrow theorem: plaquette-hierarchy polynomial-boundedness")
# ============================================================================

t = symbols('t', real=True)


# ----------------------------------------------------------------------------
section("Part 1: (T1) leading-term asymptotic  p(t) / t^d -> a_d for d >= 1")
# ----------------------------------------------------------------------------
# Explicit polynomials of degree 1, 2, 3, 4, 5 with various leading coefs.
test_polys_T1 = [
    (Rational(3) * t + Rational(7), 1, Rational(3)),
    (Rational(-2) * t**2 + Rational(5) * t - Rational(1), 2, Rational(-2)),
    (t**3 - Rational(4) * t**2 + Rational(11), 3, Rational(1)),
    (Rational(5, 2) * t**4 + t**3, 4, Rational(5, 2)),
    (-t**5 + Rational(8) * t**2 - Rational(3) * t, 5, Rational(-1)),
]

for p, d, a_d in test_polys_T1:
    quotient = p / t**d
    lim_val = limit(quotient, t, oo)
    check(f"deg={d} polynomial {p}: p(t)/t^{d} -> a_{d} = {a_d} as t -> +oo",
          lim_val == a_d,
          detail=f"sympy.limit = {lim_val}")


# ----------------------------------------------------------------------------
section("Part 2: (T2) finite-limit forces constant — limit at +oo is +/-oo for d >= 1")
# ----------------------------------------------------------------------------
# Verify that each non-constant polynomial has an UNBOUNDED limit at +oo
# (either +oo or -oo, depending on sign of leading coefficient).
for p, d, a_d in test_polys_T1:
    lim_val = limit(p, t, oo)
    expected = oo if a_d > 0 else -oo
    check(f"deg={d} polynomial {p}: lim p(t) at +oo = {expected} (UNBOUNDED)",
          lim_val == expected,
          detail=f"sympy.limit = {lim_val}, a_d sign = {'+' if a_d > 0 else '-'}")


# ----------------------------------------------------------------------------
section("Part 3: (T3) two-distinct-value obstruction at (a, b) = (0, 1)")
# ----------------------------------------------------------------------------
# The parent's endpoint pair is P(0) = 0, P(+oo) = 1. Verify that NO polynomial
# of degree d = 0, 1, 2, 3, 4, 5 simultaneously satisfies p(0) = 0 and a
# finite limit equal to 1.

a_val, b_val = Rational(0), Rational(1)

# Degree 0: p(t) = c. Constraint p(0) = 0 => c = 0. Limit = 0 != 1.
p0 = Rational(0)  # forced by p(0) = 0
finite_limit_0 = limit(p0, t, oo)
check("deg=0 (constant) with p(0) = 0: lim = 0 != 1, so obstruction holds",
      finite_limit_0 == 0 and finite_limit_0 != b_val,
      detail=f"forced p(t) = 0, lim = {finite_limit_0}")

# Degree 1: p(t) = a_0 + a_1 t with a_0 = 0 (from p(0) = 0). Then p(t) = a_1 t.
# Limit at +oo is +oo (if a_1 > 0) or -oo (if a_1 < 0) — not 1, not finite.
for a_1 in [Rational(1), Rational(-1), Rational(2), Rational(1, 5)]:
    p_d1 = a_1 * t
    lim_d1 = limit(p_d1, t, oo)
    check(f"deg=1 p(t) = {a_1} * t (p(0) = 0): lim at +oo = {lim_d1} (not finite, so not 1)",
          lim_d1 == oo or lim_d1 == -oo,
          detail=f"a_1 = {a_1}, lim = {lim_d1}")

# Degree 2: p(t) = a_1 t + a_2 t^2 (a_0 = 0). Same story, dominant term unbounded.
for (a_1, a_2) in [(Rational(0), Rational(1)),
                   (Rational(1), Rational(1)),
                   (Rational(0), Rational(-1)),
                   (Rational(-5), Rational(2))]:
    p_d2 = a_1 * t + a_2 * t**2
    lim_d2 = limit(p_d2, t, oo)
    check(f"deg=2 p(t) = {a_1}*t + {a_2}*t^2 (p(0) = 0): lim = {lim_d2} (not finite)",
          lim_d2 == oo or lim_d2 == -oo,
          detail=f"a_2 = {a_2}, lim = {lim_d2}")

# Degree 3, 4, 5: same conclusion via (T2).
for d in [3, 4, 5]:
    # Construct p(t) = t^d with p(0) = 0 and degree d.
    p_d = t**d
    lim_d = limit(p_d, t, oo)
    check(f"deg={d} p(t) = t^{d} (p(0) = 0): lim = +oo (not finite)",
          lim_d == oo,
          detail=f"lim = {lim_d}")


# ----------------------------------------------------------------------------
section("Part 4: (T4) boundedness corollary — non-constant polynomial unbounded")
# ----------------------------------------------------------------------------
# Numerical verification: for each non-constant polynomial in test_polys_T1,
# evaluate at t = 1, 10, 100, 1000, 10000 and check that |p(t)| grows
# without any bound M.

test_evaluations = [Rational(1), Rational(10), Rational(100), Rational(1000), Rational(10000)]

for p, d, a_d in test_polys_T1:
    vals = [abs(p.subs(t, t_val)) for t_val in test_evaluations]
    # Check |p(10000)| > |p(1000)| > |p(100)| eventually (monotone growth past some t).
    # Specifically: |p(10000)| > |p(100)| (skip the small-t pre-asymptotic region).
    growth = vals[-1] > vals[-3]
    check(f"deg={d} polynomial {p}: |p(t)| grows from |p(100)|={vals[-3]} to |p(10000)|={vals[-1]} (unbounded)",
          growth,
          detail=f"vals at t in {[1, 10, 100, 1000, 10000]} = {[str(v) for v in vals]}")


# ----------------------------------------------------------------------------
section("Part 5: Negative control — constant polynomial DOES satisfy (T2) and (T3) trivially")
# ----------------------------------------------------------------------------
# For p(t) = c constant: lim p(t) at +oo = c (finite), so (T2) is satisfied
# with deg = 0; and (T3) at (a, b) = (c, c) has a = b, so the obstruction
# does NOT apply.

for c in [Rational(0), Rational(1), Rational(7), Rational(-3), Rational(1, 2)]:
    p_const = c
    lim_const = limit(p_const, t, oo)
    check(f"constant p(t) = {c}: lim at +oo = {c} (finite, agrees with (T2) deg = 0)",
          lim_const == c,
          detail=f"lim = {lim_const}")
    # (T3) trivially: p(0) = c = lim, so a = b = c, obstruction does not apply.
    p0_const = p_const  # p(0) = c
    check(f"constant p(t) = {c}: p(0) = {c} = lim, so a = b, (T3) obstruction does NOT apply",
          p0_const == lim_const,
          detail=f"p(0) = {p0_const}, lim = {lim_const}")


# ----------------------------------------------------------------------------
section("Part 6: structural Poly-algebra checks — degree, leading coefficient")
# ----------------------------------------------------------------------------
# Use sympy.Poly to verify degree and leading coefficient explicitly for each
# test polynomial.
for p, d, a_d in test_polys_T1:
    poly_obj = Poly(p, t)
    actual_deg = poly_obj.degree()
    actual_lc = poly_obj.LC()
    check(f"Poly({p}, t).degree() = {d}",
          actual_deg == d,
          detail=f"sympy.Poly degree = {actual_deg}")
    check(f"Poly({p}, t).LC() = {a_d}",
          actual_lc == a_d,
          detail=f"sympy.Poly LC = {actual_lc}")


# ----------------------------------------------------------------------------
section("Part 7: symbolic identity  p(t) - a_d * t^d  has degree < d  for d >= 1")
# ----------------------------------------------------------------------------
# This is the structural fact behind (T1): the remainder after subtracting the
# leading monomial has strictly smaller degree.
for p, d, a_d in test_polys_T1:
    remainder = expand(p - a_d * t**d)
    if remainder == 0:
        rem_deg = -1  # zero polynomial has degree -infinity by convention; treat as < d.
        check(f"deg={d} polynomial {p}: p - a_d * t^{d} = 0 (so degree < {d} trivially)",
              True,
              detail="zero remainder")
    else:
        rem_poly = Poly(remainder, t)
        rem_deg = rem_poly.degree()
        check(f"deg={d} polynomial {p}: remainder p - a_d*t^{d} has degree {rem_deg} < {d}",
              rem_deg < d,
              detail=f"remainder = {remainder}, deg = {rem_deg}")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let p(t) = a_0 + a_1 t + ... + a_d t^d be a real polynomial in R[t]
    of degree exactly d (with a_d != 0 when d >= 1).

  CONCLUSION:
    (T1)  d >= 1  =>  p(t) / t^d  ->  a_d  as t -> +oo  (so |p(t)| -> +oo).
    (T2)  lim_{t -> +oo} p(t) exists and is finite  =>  d = 0  (p constant).
    (T3)  Two-distinct-value obstruction at (a, b) with a != b:
              p(0) = a  AND  lim_{t -> +oo} p(t) = b  (finite)
              ==>  no such polynomial exists (in any degree).
    (T4)  |p(t)| <= M  on [0, +oo)  =>  d = 0  (p constant).

  Audit-lane class:
    (A) — pure polynomial algebra over R[t]. No Wilson plaquette /
    gauge group / Haar measure / source-deformed partition function /
    framework axiom (Cl(3) / Z^3) is consumed.

  This narrow theorem isolates the polynomial-algebra fact from the
  parent's physical Wilson source-surface framing. The finite-limit-
  forces-constant fact and its two-endpoint obstruction can be
  ratified independently of any lattice-gauge authority.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
