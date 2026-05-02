#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`koide_eigenvalue_q23_surface_theorem_note_2026-04-20`
(claim_type=positive_theorem, audit_status=audited_conditional, td=69,
load_bearing_step_class=C).

The parent's load-bearing step is the strict monotonicity of

    Q_eig(beta)  =  [sum_i exp(2 beta lambda_i)] / [sum_i exp(beta lambda_i)]^2

in beta, established by the explicit derivative formula

    dQ_eig / dbeta  =  (2 / Z^3) sum_{i<j} (lambda_j - lambda_i) a_i a_j (a_j - a_i),

where a_i = exp(beta lambda_i) and Z = sum_i a_i. For beta > 0 and a
non-scalar three-eigenvalue spectrum, every summand is non-negative
and at least one is strictly positive, so dQ_eig/dbeta > 0. Hence
beta -> Q_eig(beta) is strictly increasing.

This Pattern B companion verifies the derivative formula at sympy
exact symbolic precision for n = 3 and the strict-monotonicity claim
on a concrete spectrum.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's class-(C) algebraic-calculus
content holds at exact symbolic precision.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, simplify, symbols, diff, exp, expand, factor
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
    tag = "PASS (C)" if ok else "FAIL (C)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Audit companion for koide_eigenvalue_q23_surface_theorem (td=69)")
# Goal: exact symbolic verification of the derivative formula and
# strict monotonicity of Q_eig in beta on a concrete spectrum.
# ============================================================================

beta = symbols('beta', real=True)
l1, l2, l3 = symbols('lambda_1 lambda_2 lambda_3', real=True)


# ----------------------------------------------------------------------------
section("Part 1: symbolic derivative formula dQ_eig/dbeta = ... / Z^3")
# ----------------------------------------------------------------------------
a1 = exp(beta * l1)
a2 = exp(beta * l2)
a3 = exp(beta * l3)
Z = a1 + a2 + a3
N = a1**2 + a2**2 + a3**2  # = sum exp(2 beta lambda_i)

Q_eig = N / Z**2

dQ_dbeta = simplify(diff(Q_eig, beta))

# Expected formula from the parent:
#   dQ/dbeta = (2 / Z^3) sum_{i<j} (lambda_j - lambda_i) a_i a_j (a_j - a_i)
expected_numerator = (
    (l2 - l1) * a1 * a2 * (a2 - a1)
    + (l3 - l1) * a1 * a3 * (a3 - a1)
    + (l3 - l2) * a2 * a3 * (a3 - a2)
)
expected_dQ = simplify(2 * expected_numerator / Z**3)

diff_check = simplify(dQ_dbeta - expected_dQ)
check("dQ_eig/dbeta matches parent's symbolic formula at n = 3",
      diff_check == 0,
      detail=f"diff = {diff_check}")


# ----------------------------------------------------------------------------
section("Part 2: each summand in dQ/dbeta numerator is non-negative for beta > 0")
# ----------------------------------------------------------------------------
# For lambda_j > lambda_i and beta > 0: a_j > a_i, so a_j - a_i > 0.
# Summand = (lambda_j - lambda_i) a_i a_j (a_j - a_i) > 0 for non-degenerate.
# Test on concrete ordered spectrum lambda_1 < lambda_2 < lambda_3.
sub_concrete = {l1: Rational(-1), l2: Rational(0), l3: Rational(1), beta: Rational(1, 2)}
val_12 = simplify((l2 - l1) * a1 * a2 * (a2 - a1)).subs(sub_concrete)
val_13 = simplify((l3 - l1) * a1 * a3 * (a3 - a1)).subs(sub_concrete)
val_23 = simplify((l3 - l2) * a2 * a3 * (a3 - a2)).subs(sub_concrete)

print(f"\n  At lambda = (-1, 0, 1), beta = 1/2:")
print(f"    summand (1,2): {val_12}")
print(f"    summand (1,3): {val_13}")
print(f"    summand (2,3): {val_23}")

check("summand (1,2) > 0 at concrete ordered spectrum",
      val_12 > 0,
      detail=f"value = {val_12}")
check("summand (1,3) > 0 at concrete ordered spectrum",
      val_13 > 0,
      detail=f"value = {val_13}")
check("summand (2,3) > 0 at concrete ordered spectrum",
      val_23 > 0,
      detail=f"value = {val_23}")


# ----------------------------------------------------------------------------
section("Part 3: dQ/dbeta > 0 strict on concrete ordered non-scalar spectrum")
# ----------------------------------------------------------------------------
dQ_concrete = simplify(dQ_dbeta.subs(sub_concrete))
print(f"\n  dQ/dbeta at concrete spectrum = {dQ_concrete}")
check("dQ/dbeta > 0 on concrete ordered non-scalar spectrum (strict monotonicity)",
      dQ_concrete > 0,
      detail=f"dQ/dbeta = {dQ_concrete}")


# ----------------------------------------------------------------------------
section("Part 4: degenerate (scalar) spectrum gives dQ/dbeta = 0")
# ----------------------------------------------------------------------------
# When lambda_1 = lambda_2 = lambda_3, all summands have (lambda_j - lambda_i) = 0,
# so dQ/dbeta = 0.
sub_scalar = {l1: Rational(1), l2: Rational(1), l3: Rational(1), beta: Rational(1, 2)}
dQ_scalar = simplify(dQ_dbeta.subs(sub_scalar))
check("dQ/dbeta = 0 on scalar (degenerate) spectrum",
      dQ_scalar == 0,
      detail=f"dQ/dbeta on scalar = {dQ_scalar}")


# ----------------------------------------------------------------------------
section("Part 5: Q_eig at beta = 0 equals 1/n (= 1/3 for n = 3)")
# ----------------------------------------------------------------------------
# At beta = 0: a_i = 1 for all i, so N = n, Z = n, Q = n / n^2 = 1/n.
Q_at_0 = simplify(Q_eig.subs(beta, 0))
check("Q_eig(beta = 0) = 1/3 exact (uniform initial value)",
      simplify(Q_at_0 - Rational(1, 3)) == 0,
      detail=f"Q_eig(0) = {Q_at_0}")


# ----------------------------------------------------------------------------
section("Part 6: Q_eig at large beta saturates near 1 (single-largest dominant)")
# ----------------------------------------------------------------------------
# For lambda_1 < lambda_2 < lambda_3, large beta gives a_3 >> a_1, a_2,
# so Q ~ a_3^2 / a_3^2 = 1. Verify at concrete large beta numerically.
sub_large_beta = {l1: Rational(-1), l2: Rational(0), l3: Rational(1), beta: Rational(20)}
Q_large = sympy.N(Q_eig.subs(sub_large_beta), 50)
print(f"\n  Q_eig at beta = 20 (lambda = (-1, 0, 1)): {Q_large}")
# At beta = 20: a_3 = e^20 dominates; Q ~ e^40 / e^40 = 1, with corrections
# of order e^(-20) ~ 2e-9. Use a tolerance of 1e-7 to be safe.
check("Q_eig saturates near 1 for large beta on ordered spectrum",
      abs(Q_large - 1) < Rational(1, 10**7),
      detail=f"Q_eig(20) = {Q_large}, distance from 1 = {abs(Q_large - 1)}")


# ----------------------------------------------------------------------------
section("Part 7: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('koide_eigenvalue_q23_surface_theorem_note_2026-04-20', {})
print(f"\n  koide_eigenvalue_q23_surface_theorem_note_2026-04-20 current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-C load-bearing step (calculus / monotonicity)",
      parent.get('load_bearing_step_class') == 'C')


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(C) calculus content:

    derivative formula dQ_eig/dbeta at n = 3 matches:
      (2 / Z^3) sum_{i<j} (lambda_j - lambda_i) a_i a_j (a_j - a_i),

    each summand (lambda_j - lambda_i) a_i a_j (a_j - a_i) > 0
    for ordered non-degenerate spectrum and beta > 0;

    strict monotonicity dQ/dbeta > 0 on concrete spectrum (-1, 0, 1)
    at beta = 1/2;

    degenerate (scalar) spectrum gives dQ/dbeta = 0;

    Q_eig(0) = 1/3 exact (uniform start);

    Q_eig saturates near 1 at large beta.

  Audit-lane class for the parent's load-bearing step:
    (C) — first-principles calculus / strict-monotonicity argument.
    No external observed/fitted/literature input.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status. The parent
  remains audited_conditional pending audit-lane review of the
  upstream selected-line H_sel(m) construction and the physical
  beta_*/m_* selector inputs.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
