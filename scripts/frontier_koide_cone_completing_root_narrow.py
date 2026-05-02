#!/usr/bin/env python3
"""Pattern A narrow runner for `KOIDE_CONE_COMPLETING_ROOT_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone polynomial-algebra identity:

  Let v, w be any positive real numbers. Define the "Koide-completing"
  amplitude

      u_small(v, w)  =  2 (v + w)  -  sqrt(3 (v^2 + 4 v w + w^2)).

  Then the triple (u_small, v, w) lies exactly on the Koide cone:

      (u_small)^2 + v^2 + w^2  =  4 (u_small * v + u_small * w + v * w),

  equivalently

      (u_small^2 + v^2 + w^2) / (u_small + v + w)^2  =  2/3.

  Moreover, the larger root of the same quadratic,

      u_large(v, w)  =  2 (v + w)  +  sqrt(3 (v^2 + 4 v w + w^2)),

  also satisfies the cone identically, so the two roots are the only
  possible u-values placing (u, v, w) on the Koide cone for given
  (v, w).

This is class-A pure polynomial algebra (quadratic-formula derivation +
identity check). No Koide / charged-lepton mass / sqrt(m) / selected-line
H_sel(m) framework input is consumed.

Companion role: this is a Pattern A new narrow claim row carving out
the load-bearing class-(A) algebraic core of
`koide_scale_selector_reparameterization_theorem_note_2026-04-20`
(claim_type=positive_theorem, audit_status=audited_conditional, td=69,
load_bearing_step_class=A). The narrow theorem isolates the
Koide-cone completing-root algebra from any selected-line / native-vs-
completed framework-specific framing.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, expand, factor, solve, Eq
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
section("Pattern A narrow theorem: Koide-cone completing-root identity")
# ============================================================================

v, w = symbols('v w', positive=True, real=True)

# Define the two roots of the Koide-cone quadratic in u
u_small = 2 * (v + w) - sqrt(3 * (v**2 + 4 * v * w + w**2))
u_large = 2 * (v + w) + sqrt(3 * (v**2 + 4 * v * w + w**2))


# ----------------------------------------------------------------------------
section("Part 1: u_small and u_large are the roots of u^2 - 4(v+w) u + (v^2 - 4vw + w^2) = 0")
# ----------------------------------------------------------------------------
# The Koide cone u^2 + v^2 + w^2 = 4(uv + uw + vw) rearranges to
#   u^2 - 4(v+w) u + (v^2 + w^2 - 4 v w) = 0
# Discriminant: 16(v+w)^2 - 4(v^2 + w^2 - 4 v w)
#             = 16 v^2 + 32 v w + 16 w^2 - 4 v^2 - 4 w^2 + 16 v w
#             = 12 v^2 + 48 v w + 12 w^2
#             = 12 (v^2 + 4 v w + w^2).
# So u = [4(v+w) +/- 2 sqrt(3 (v^2 + 4 v w + w^2))] / 2
#     = 2(v+w) +/- sqrt(3 (v^2 + 4 v w + w^2)).

quadratic = symbols('u', real=True)**2 - 4 * (v + w) * symbols('u', real=True) + (v**2 + w**2 - 4 * v * w)
roots = solve(quadratic, symbols('u', real=True))
print(f"\n  Roots of u^2 - 4(v+w) u + (v^2 + w^2 - 4 v w) = 0: {roots}")

# Verify roots match u_small and u_large.
roots_simplified = {simplify(r) for r in roots}
expected_set = {simplify(u_small), simplify(u_large)}
check("roots = {u_small, u_large} exact",
      roots_simplified == expected_set,
      detail=f"roots = {roots_simplified}")


# ----------------------------------------------------------------------------
section("Part 2: u_small satisfies the Koide cone u^2 + v^2 + w^2 = 4(uv + uw + vw)")
# ----------------------------------------------------------------------------
F_orbit_small = simplify(u_small**2 + v**2 + w**2 - 4 * (u_small * v + u_small * w + v * w))
check("F_orbit(u_small, v, w) = 0 exact (cone identity for small root)",
      F_orbit_small == 0,
      detail=f"F_orbit(u_small, v, w) = {F_orbit_small}")


# ----------------------------------------------------------------------------
section("Part 3: u_large satisfies the Koide cone too")
# ----------------------------------------------------------------------------
F_orbit_large = simplify(u_large**2 + v**2 + w**2 - 4 * (u_large * v + u_large * w + v * w))
check("F_orbit(u_large, v, w) = 0 exact (cone identity for large root)",
      F_orbit_large == 0,
      detail=f"F_orbit(u_large, v, w) = {F_orbit_large}")


# ----------------------------------------------------------------------------
section("Part 4: Vieta identities u_small + u_large = 4(v+w), u_small * u_large = v^2 + w^2 - 4 v w")
# ----------------------------------------------------------------------------
sum_roots = simplify(u_small + u_large)
expected_sum = 4 * (v + w)
check("u_small + u_large = 4 (v + w) exact (Vieta)",
      simplify(sum_roots - expected_sum) == 0,
      detail=f"sum = {sum_roots}")

prod_roots = simplify(u_small * u_large)
expected_prod = simplify(v**2 + w**2 - 4 * v * w)
check("u_small * u_large = v^2 + w^2 - 4 v w exact (Vieta)",
      simplify(prod_roots - expected_prod) == 0,
      detail=f"prod = {prod_roots}")


# ----------------------------------------------------------------------------
section("Part 5: standard Koide ratio Q = 2/3 at (u_small, v, w)")
# ----------------------------------------------------------------------------
Q_form = (u_small**2 + v**2 + w**2) / (u_small + v + w)**2
Q_form_simplified = simplify(Q_form)
# The cone-on condition implies Q = 2/3.
check("Q(u_small^2, v^2, w^2) = (sum sq)/(sum)^2 = 2/3 exact",
      simplify(Q_form_simplified - Rational(2, 3)) == 0,
      detail=f"Q = {Q_form_simplified}")


# ----------------------------------------------------------------------------
section("Part 6: concrete instance v = 1, w = 1 -- u_small = 4 - sqrt(18) = 4 - 3 sqrt(2)")
# ----------------------------------------------------------------------------
sub_concrete = {v: Rational(1), w: Rational(1)}
u_small_at_11 = simplify(u_small.subs(sub_concrete))
expected_u_small = 4 - 3 * sqrt(Rational(2))
check("u_small at (v, w) = (1, 1) = 4 - 3 sqrt(2)",
      simplify(u_small_at_11 - expected_u_small) == 0,
      detail=f"u_small = {u_small_at_11}")

u_large_at_11 = simplify(u_large.subs(sub_concrete))
expected_u_large = 4 + 3 * sqrt(Rational(2))
check("u_large at (v, w) = (1, 1) = 4 + 3 sqrt(2)",
      simplify(u_large_at_11 - expected_u_large) == 0,
      detail=f"u_large = {u_large_at_11}")


# ----------------------------------------------------------------------------
section("Part 7: u_small > 0 in the regime where the Koide-cone is physical")
# ----------------------------------------------------------------------------
# u_small > 0 iff 2(v+w) > sqrt(3 (v^2 + 4 v w + w^2))
# iff 4(v+w)^2 > 3(v^2 + 4 v w + w^2)
# iff 4 v^2 + 8 v w + 4 w^2 > 3 v^2 + 12 v w + 3 w^2
# iff v^2 - 4 v w + w^2 > 0
# This is (v - 2w)^2 - 3 w^2 > 0, equivalently |v - 2w| > w sqrt(3),
# or equivalently v/w > 2 + sqrt(3) ~ 3.73 OR v/w < 2 - sqrt(3) ~ 0.27.
# So u_small > 0 only on certain (v, w) regimes.

# Verify u_small > 0 at v = 1, w = 1: u_small = 4 - 3 sqrt(2) ~ -0.24 < 0.
# Verify u_small > 0 at v = 4, w = 1: u_small = 2(5) - sqrt(3 (16 + 16 + 1))
#                                              = 10 - sqrt(99) ~ 10 - 9.95 ~ 0.05 > 0.
sub_pos = {v: Rational(4), w: Rational(1)}
u_small_pos = simplify(u_small.subs(sub_pos))
print(f"\n  u_small at (v, w) = (4, 1) = {u_small_pos}")
check("u_small at (v, w) = (4, 1) is positive (u_small in physical regime)",
      sympy.N(u_small_pos) > 0,
      detail=f"u_small = {u_small_pos}, numerical = {sympy.N(u_small_pos)}")


# ----------------------------------------------------------------------------
section("Part 8: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('koide_scale_selector_reparameterization_theorem_note_2026-04-20', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-A load-bearing step (algebraic identity)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let v, w be any positive real numbers, and define
        u_small(v, w)  =  2(v + w)  -  sqrt(3 (v^2 + 4 v w + w^2)),
        u_large(v, w)  =  2(v + w)  +  sqrt(3 (v^2 + 4 v w + w^2)).

  CONCLUSION:
    (T1) u_small and u_large are the two roots of the quadratic
            u^2  -  4(v + w) u  +  (v^2 + w^2 - 4 v w)  =  0,
         i.e. they are the only u-values placing (u, v, w) on the Koide
         cone for given (v, w).
    (T2) (u_small, v, w) satisfies the Koide cone exactly:
            (u_small)^2 + v^2 + w^2  =  4 (u_small v + u_small w + v w);
         (u_large, v, w) satisfies the same cone exactly.
    (T3) Vieta:
            u_small + u_large  =  4 (v + w);
            u_small * u_large  =  v^2 + w^2 - 4 v w.
    (T4) Standard Koide ratio at (u_small, v, w):
            (u_small^2 + v^2 + w^2) / (u_small + v + w)^2  =  2/3.
    (T5) u_small > 0 iff |v - 2 w| > w sqrt(3); positive in regions
         like (v, w) = (4, 1) but not (1, 1).

  Audit-lane class:
    (A) — pure polynomial algebra over R^2. No Koide / charged-lepton /
    selected-line / sqrt-mass framework input.

  This narrow theorem isolates the Koide-cone completing-root algebra
  from the parent's selected-line H_sel(m) framework. The parent's
  reparameterization no-go conclusion still requires the upstream
  selected-line authority, but the underlying algebraic
  cone-completing-root identity becomes audit-able as a standalone
  primitive.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
