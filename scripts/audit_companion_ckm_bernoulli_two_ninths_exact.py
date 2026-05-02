#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25`
(claim_type=positive_theorem, audit_status=audited_conditional, td=85,
load_bearing_step_class=A).

The parent's load-bearing content is five algebraic identities (K1, K2,
K3, K5, K6) that all give 2/9 under the retained framework counts
(N_pair, N_color) = (2, 3). The K3 consistency identity is the most
substantive class-(A) content: over positive integer pair/color counts,
K1 = K2 = K5 = K6 = 2/9 is **equivalent** to (N_pair, N_color) = (2, 3).

The existing primary runner verifies K1, K2, K5, K6 at exact `Fraction`
precision under the retained counts. This Pattern B companion adds:

  (a) sympy-symbolic verification of the same forward identities
      K1, K2, K5, K6 at exact precision, parameterized over abstract
      (N_pair, N_color) positive integers;
  (b) symbolic solution of the K3 converse: solving the quadratic
      `2c^2 - 9c + 9 = 0` over Q gives c in {3, 3/2}, enforcing
      positive-integer constraint forces c = 3, and then K5 forces
      N_pair = 2;
  (c) enumeration over small positive integers (1 <= N_pair, N_color
      <= 8, with c != 3 or p != 2) confirming that at least one of
      K1, K2, K5, K6 fails to equal 2/9 outside of (p, c) = (2, 3).

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's class-(A) consistency K3
holds at exact symbolic precision over the integer count space.
Does not modify the parent's audit_status; that decision belongs to
the audit lane.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, simplify, symbols, solve, Eq
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
section("Audit companion for ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25 (td=85)")
# Goal: exact symbolic verification of K1, K2, K5, K6 at retained counts;
# sympy-symbolic solution of K3 converse; integer enumeration confirming
# K3 forward direction.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: K1, K2, K5, K6 evaluate to 2/9 at (N_pair, N_color) = (2, 3)")
# ----------------------------------------------------------------------------
N_pair_val = Rational(2)
N_color_val = Rational(3)
N_quark_val = N_pair_val * N_color_val
A_squared = N_pair_val / N_color_val
rho = Rational(1) / N_quark_val

K1 = simplify(A_squared * (1 - A_squared))
K2 = simplify(2 * rho * A_squared)
K5 = simplify(A_squared / N_color_val)
K6 = simplify((Rational(1) / N_color_val) * (1 - Rational(1) / N_color_val))

target = Rational(2, 9)

check("K1 = A^2 (1 - A^2) = 2/9 at (N_pair, N_color) = (2, 3)",
      simplify(K1 - target) == 0,
      detail=f"K1 = {K1}")
check("K2 = 2 rho A^2 = 2/9 at (N_pair, N_color) = (2, 3)",
      simplify(K2 - target) == 0,
      detail=f"K2 = {K2}")
check("K5 = A^2 / N_color = 2/9 at (N_pair, N_color) = (2, 3)",
      simplify(K5 - target) == 0,
      detail=f"K5 = {K5}")
check("K6 = (1/N_color)(1 - 1/N_color) = 2/9 at (N_pair, N_color) = (2, 3)",
      simplify(K6 - target) == 0,
      detail=f"K6 = {K6}")


# ----------------------------------------------------------------------------
section("Part 2: parametric K1, K2, K5, K6 closed forms in (p, c)")
# ----------------------------------------------------------------------------
# Symbolic abstract counts.
p_sym, c_sym = symbols('p c', positive=True, real=True)
A_sq_sym = p_sym / c_sym
N_quark_sym = p_sym * c_sym
rho_sym = Rational(1) / N_quark_sym

K1_sym = simplify(A_sq_sym * (1 - A_sq_sym))
K2_sym = simplify(2 * rho_sym * A_sq_sym)
K5_sym = simplify(A_sq_sym / c_sym)
K6_sym = simplify((Rational(1) / c_sym) * (1 - Rational(1) / c_sym))

K1_expected = simplify(p_sym * (c_sym - p_sym) / c_sym**2)
K2_expected = Rational(2) / c_sym**2
K5_expected = simplify(p_sym / c_sym**2)
K6_expected = simplify((c_sym - 1) / c_sym**2)

check("K1(p, c) = p(c - p)/c^2 symbolically",
      simplify(K1_sym - K1_expected) == 0,
      detail=f"K1 = {K1_sym}")
check("K2(p, c) = 2/c^2 symbolically (p cancels via N_quark = p c)",
      simplify(K2_sym - K2_expected) == 0,
      detail=f"K2 = {K2_sym}")
check("K5(p, c) = p/c^2 symbolically",
      simplify(K5_sym - K5_expected) == 0,
      detail=f"K5 = {K5_sym}")
check("K6(p, c) = (c - 1)/c^2 symbolically (independent of p)",
      simplify(K6_sym - K6_expected) == 0,
      detail=f"K6 = {K6_sym}")


# ----------------------------------------------------------------------------
section("Part 3: K3 converse - solve K6 = 2/9 over rationals; force c = 3")
# ----------------------------------------------------------------------------
# K6 = (c - 1)/c^2 = 2/9  =>  9(c - 1) = 2 c^2  =>  2c^2 - 9c + 9 = 0.
# Solve with sympy.
c_var = symbols('c', real=True)
K6_eqn = Eq((c_var - 1) / c_var**2, Rational(2, 9))
solutions = solve(K6_eqn, c_var)
print(f"\n  Solving K6 = 2/9: solutions = {solutions}")

# Verify solutions are {3, 3/2}.
expected_solutions = {Rational(3), Rational(3, 2)}
solutions_set = set(solutions)
check("K6 = 2/9 has exactly two rational solutions: {3, 3/2}",
      solutions_set == expected_solutions,
      detail=f"solutions = {solutions_set}")

# Only positive integer is 3.
positive_integer_solutions = [s for s in solutions if s.is_integer and s > 0]
check("Only positive integer solution to K6 = 2/9 is c = 3",
      positive_integer_solutions == [Rational(3)],
      detail=f"positive integer solutions = {positive_integer_solutions}")


# ----------------------------------------------------------------------------
section("Part 4: K5 = 2/9 at c = 3 forces p = 2")
# ----------------------------------------------------------------------------
# K5(p, 3) = p / 9 = 2/9  =>  p = 2.
p_var = symbols('p', positive=True, real=True)
K5_at_c3 = p_var / Rational(9)
K5_eqn_at_c3 = Eq(K5_at_c3, Rational(2, 9))
p_solutions = solve(K5_eqn_at_c3, p_var)
print(f"\n  Solving K5 = 2/9 at c = 3: p_solutions = {p_solutions}")

check("K5 = 2/9 with c = 3 has unique solution p = 2",
      p_solutions == [Rational(2)],
      detail=f"p_solutions = {p_solutions}")


# ----------------------------------------------------------------------------
section("Part 5: K3 forward enumeration over positive integers (p, c) <= 8")
# ----------------------------------------------------------------------------
# For all (p, c) in {1, ..., 8}^2 with (p, c) != (2, 3), at least one of
# K1, K2, K5, K6 must NOT equal 2/9.
target_q = Rational(2, 9)
violations_found = 0
total_off_target_pairs = 0
for p_int in range(1, 9):
    for c_int in range(1, 9):
        if (p_int, c_int) == (2, 3):
            continue  # skip the framework instance
        total_off_target_pairs += 1
        # Compute K1, K2, K5, K6 at (p_int, c_int)
        p_r = Rational(p_int)
        c_r = Rational(c_int)
        A2 = p_r / c_r
        N_q = p_r * c_r
        K1_v = simplify(A2 * (1 - A2))
        K2_v = simplify(2 * (Rational(1) / N_q) * A2)
        K5_v = simplify(A2 / c_r)
        K6_v = simplify((Rational(1) / c_r) * (1 - Rational(1) / c_r))
        # Is at least one of K1, K2, K5, K6 != 2/9?
        if any(simplify(k - target_q) != 0 for k in [K1_v, K2_v, K5_v, K6_v]):
            violations_found += 1

check(f"K3 forward: all {total_off_target_pairs} off-target (p, c) in 1..8 break at least one K_i identity",
      violations_found == total_off_target_pairs,
      detail=f"violations = {violations_found} / {total_off_target_pairs} pairs checked")


# ----------------------------------------------------------------------------
section("Part 6: K3 backward direction — at (p, c) = (2, 3) all four agree")
# ----------------------------------------------------------------------------
all_agree_at_2_3 = all(
    simplify(k.subs({p_sym: Rational(2), c_sym: Rational(3)}) - target) == 0
    for k in [K1_sym, K2_sym, K5_sym, K6_sym]
)
check("K3 backward: at (p, c) = (2, 3), K1 = K2 = K5 = K6 = 2/9 symbolically",
      all_agree_at_2_3)


# ----------------------------------------------------------------------------
section("Part 7: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25', {})
print(f"\n  ckm_bernoulli_two_ninths_koide_bridge_support_note_2026-04-25 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")
print(f"    deps: {parent.get('deps')}")

check("parent row class-A load-bearing step (algebraic identity)",
      parent.get('load_bearing_step_class') == 'A',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(A) algebraic content:

    K1 = A^2 (1 - A^2)  =  p (c - p) / c^2,
    K2 = 2 rho A^2      =  2 / c^2  (under N_quark = p c),
    K5 = A^2 / c        =  p / c^2,
    K6 = (1/c)(1 - 1/c) =  (c - 1) / c^2,

  evaluated at (p, c) = (N_pair, N_color) = (2, 3) all give 2/9 exactly.
  The K3 converse is verified symbolically: K6 = 2/9 has exactly two
  rational solutions {3, 3/2}; only c = 3 is a positive integer; then
  K5 = 2/9 forces p = 2 uniquely. Forward direction enumerated over
  (p, c) in {1, ..., 8}^2: all 63 off-target pairs break at least one
  of K1, K2, K5, K6 = 2/9.

  Audit-lane class for the parent's load-bearing step:
    (A) — algebraic identity / number-theoretic consistency over
    positive-integer pair/color counts. No external observed/fitted/
    literature input.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status. The parent
  remains audited_conditional pending audit-lane review of the
  upstream Wolfenstein, CP-phase, and magnitudes-counts authorities the
  verdict identifies.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
