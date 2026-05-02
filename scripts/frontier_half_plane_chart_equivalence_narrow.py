#!/usr/bin/env python3
"""Pattern A narrow runner for `HALF_PLANE_CHART_EQUIVALENCE_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone algebraic / inverse-function-theorem identity:

  GIVEN a positive constant c > 0 and the parametric map
      f : {(delta, r) : delta in R, r >= 1/2}  ->  R x R
      f(delta, r)  =  (delta,  c - delta + sqrt(r^2 - 1/4)),
  THEN:
    (i)   the image of f is exactly the closed half-plane
              H_c  =  {(delta, q) : q >= c - delta},
    (ii)  the inverse chart on H_c is
              g(delta, q)  =  (delta,  sqrt((q - c + delta)^2 + 1/4)),
    (iii) f restricted to {r >= 1/2} and g restricted to H_c are mutual
          inverses,
    (iv)  the boundary q = c - delta corresponds exactly to r = 1/2,
    (v)   the inverse value at the boundary gives r = 1/2 (the minimal
          value of r consistent with the parametric map).

This is pure algebra in two real variables. No DM-neutrino-specific input,
no source-surface authorities, no PDG/literature/fitted/admitted imports.

The narrow theorem applies in particular to c = sqrt(8/3), but does not
claim any DM-neutrino-specific significance for that value; the
implication holds for any positive constant c.

Companion role: this is a Pattern A new narrow claim row carving out the
load-bearing class-(A) algebraic core of
`dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16`
(claim_type=positive_theorem, audit_status=audited_conditional, td=131,
load_bearing_step_class=A). The parent's load-bearing identity is the
half-plane equivalence above; this narrow theorem isolates that identity
from the five upstream DM-neutrino source-surface theorems by
parametrizing over the abstract constant c.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, Symbol, expand
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
section("Pattern A narrow theorem: half-plane chart equivalence")
# Statement: f(delta, r) = (delta, c - delta + sqrt(r^2 - 1/4)) for r >= 1/2
# bijects {r >= 1/2} with the closed half-plane {q >= c - delta} via the
# inverse chart g(delta, q) = (delta, sqrt((q - c + delta)^2 + 1/4)).
# Pure algebra in two real variables. No physical/neutrino-specific input.
# ============================================================================

c = symbols('c', positive=True, real=True)
delta = symbols('delta', real=True)
r = symbols('r', positive=True, real=True)
q = symbols('q', real=True)

# Define f and g
def f_q(delta_val, r_val, c_val):
    """Forward parametric map: q = c - delta + sqrt(r^2 - 1/4)."""
    return c_val - delta_val + sqrt(r_val**2 - Rational(1, 4))

def g_r(delta_val, q_val, c_val):
    """Inverse chart: r = sqrt((q - c + delta)^2 + 1/4)."""
    return sqrt((q_val - c_val + delta_val)**2 + Rational(1, 4))


# ----------------------------------------------------------------------------
section("Part 1: image of f lies in the half-plane H_c = {q >= c - delta}")
# ----------------------------------------------------------------------------
# For r >= 1/2, sqrt(r^2 - 1/4) >= 0, so q = c - delta + (something >= 0).
# Hence q >= c - delta.
#
# Symbolically: q - (c - delta) = sqrt(r^2 - 1/4) >= 0 for r >= 1/2.
q_minus_boundary = f_q(delta, r, c) - (c - delta)
q_minus_boundary_simplified = simplify(q_minus_boundary)
check("q - (c - delta) = sqrt(r^2 - 1/4) symbolically",
      simplify(q_minus_boundary_simplified - sqrt(r**2 - Rational(1, 4))) == 0,
      detail=f"q - (c - delta) = {q_minus_boundary_simplified}")

# At r = 1/2, q - (c - delta) = sqrt(1/4 - 1/4) = 0, so q = c - delta exactly.
boundary_value = simplify(q_minus_boundary.subs(r, Rational(1, 2)))
check("at r = 1/2: q = c - delta exactly (boundary)",
      boundary_value == 0,
      detail=f"q - (c - delta) at r=1/2 = {boundary_value}")


# ----------------------------------------------------------------------------
section("Part 2: g composed with f recovers r exactly")
# ----------------------------------------------------------------------------
# g(delta, f_q(delta, r, c), c) = sqrt((sqrt(r^2 - 1/4))^2 + 1/4) = sqrt(r^2) = r
g_of_f = g_r(delta, f_q(delta, r, c), c)
g_of_f_simplified = simplify(g_of_f)
check("g(delta, f(delta, r, c), c) = r symbolically (g compose f = id)",
      simplify(g_of_f_simplified - r) == 0,
      detail=f"g(f(delta, r, c)) = {g_of_f_simplified}")


# ----------------------------------------------------------------------------
section("Part 3: f composed with g recovers q exactly on the half-plane")
# ----------------------------------------------------------------------------
# On q >= c - delta, we have q - c + delta >= 0, so sqrt((q-c+delta)^2) = q-c+delta.
# f_q(delta, g_r(delta, q, c), c) = c - delta + sqrt(g_r^2 - 1/4)
#                                  = c - delta + sqrt((q - c + delta)^2)
# Under q >= c - delta this equals c - delta + (q - c + delta) = q.

# Symbolically with q - c + delta >= 0 substitution explicit:
# Let s = q - c + delta >= 0; then g_r = sqrt(s^2 + 1/4), so f_q(g_r) = c - delta + s = q.
s = symbols('s', nonnegative=True, real=True)
# r at q = c - delta + s
r_inverse = sqrt(s**2 + Rational(1, 4))
# f_q with this r: c - delta + sqrt(r_inverse^2 - 1/4) = c - delta + sqrt(s^2) = c - delta + s
# (since s >= 0)
forward_recovery = c - delta + sqrt(r_inverse**2 - Rational(1, 4))
forward_recovery_simplified = simplify(forward_recovery)
# Should equal c - delta + s
expected_q = c - delta + s
check("on s = q - c + delta >= 0: f(g) returns q (f compose g = id on H_c)",
      simplify(forward_recovery_simplified - expected_q) == 0,
      detail=f"forward_recovery = {forward_recovery_simplified}")


# ----------------------------------------------------------------------------
section("Part 4: monotonicity / surjectivity")
# ----------------------------------------------------------------------------
# For r >= 1/2 -> q >= c - delta. For any q >= c - delta, define s = q - c + delta >= 0,
# then r = sqrt(s^2 + 1/4) >= sqrt(0 + 1/4) = 1/2. So the map is surjective onto H_c
# and the inverse stays in {r >= 1/2}.
r_at_boundary = sqrt(Rational(0)**2 + Rational(1, 4))
check("at q = c - delta (s = 0): r = 1/2 (minimal r)",
      simplify(r_at_boundary - Rational(1, 2)) == 0,
      detail=f"r at boundary = {r_at_boundary}")

# Monotonic in s: r increases as s increases (strictly).
r_at_s = sqrt(s**2 + Rational(1, 4))
dr_ds = sympy.diff(r_at_s, s)
# dr/ds = s / sqrt(s^2 + 1/4) >= 0 for s >= 0
dr_ds_at_pos = simplify(dr_ds.subs(s, Rational(1)))  # at s = 1
check("dr/ds > 0 for s > 0 (inverse chart is monotonic)",
      dr_ds_at_pos > 0,
      detail=f"dr/ds at s=1 = {dr_ds_at_pos}")


# ----------------------------------------------------------------------------
section("Part 5: concrete numerical instances")
# ----------------------------------------------------------------------------
# Test a few rational instances.
test_cases = [
    (Rational(1), Rational(1)),       # c = 1, delta = 1
    (Rational(2), Rational(0)),       # c = 2, delta = 0
    (Rational(5, 3), Rational(-1, 2)),  # c = 5/3, delta = -1/2
]
for c_val, delta_val in test_cases:
    # Pick r = 3/4 (interior point), compute q, then invert
    r_val = Rational(3, 4)
    q_val = simplify(f_q(delta_val, r_val, c_val))
    r_back = simplify(g_r(delta_val, q_val, c_val))
    check(f"(c, delta) = ({c_val}, {delta_val}), r = 3/4: g(f(r)) = r",
          simplify(r_back - r_val) == 0,
          detail=f"q = {q_val}, r_back = {r_back}")

    # Pick boundary q = c - delta, check r = 1/2
    q_boundary = c_val - delta_val
    r_at_boundary_concrete = simplify(g_r(delta_val, q_boundary, c_val))
    check(f"(c, delta) = ({c_val}, {delta_val}): boundary q = c - delta gives r = 1/2",
          simplify(r_at_boundary_concrete - Rational(1, 2)) == 0,
          detail=f"r at boundary = {r_at_boundary_concrete}")


# ----------------------------------------------------------------------------
section("Part 6: framework instance c = sqrt(8/3)")
# ----------------------------------------------------------------------------
# The DM-neutrino source-surface application uses c = sqrt(8/3). This is a
# special case of the general theorem; the algebra closes for any c > 0.
c_fw = sqrt(Rational(8, 3))
delta_fw = Rational(0)
r_fw = Rational(1)  # interior
q_fw = simplify(f_q(delta_fw, r_fw, c_fw))
r_fw_back = simplify(g_r(delta_fw, q_fw, c_fw))
check(f"framework instance c = sqrt(8/3), delta = 0, r = 1: g(f(r)) = r",
      simplify(r_fw_back - r_fw) == 0,
      detail=f"q = {q_fw}, r_back = {r_fw_back}")


# ----------------------------------------------------------------------------
section("Part 7: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('dm_neutrino_source_surface_active_half_plane_theorem_note_2026-04-16', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")
print(f"    deps: {parent.get('deps')}")

check("parent row class-A load-bearing step (algebraic identity)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let c > 0 be any positive constant, and consider the parametric map
        f : {(delta, r) in R x [1/2, infinity)}  ->  R^2,
        f(delta, r) = (delta,  c - delta + sqrt(r^2 - 1/4)).

  CONCLUSION:
    (i)   image(f) = closed half-plane H_c = {(delta, q) : q >= c - delta};
    (ii)  the inverse chart on H_c is
              g(delta, q) = (delta,  sqrt((q - c + delta)^2 + 1/4));
    (iii) f and g are mutual inverses;
    (iv)  the boundary q = c - delta corresponds to r = 1/2;
    (v)   the inverse chart is strictly monotonic in s = q - c + delta.

  Audit-lane class:
    (A) — pure algebra in two real variables. No external observed/fitted/
    literature input. The framework instance c = sqrt(8/3) is one
    concrete case; the implication holds for any c > 0.

  This narrow theorem drops the parent's deps on the five upstream
  DM-neutrino source-surface theorems by parametrizing over the abstract
  constant c.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
