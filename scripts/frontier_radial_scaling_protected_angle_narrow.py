#!/usr/bin/env python3
"""Pattern A narrow runner for `RADIAL_SCALING_PROTECTED_ANGLE_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone Euclidean-geometry / similar-triangles identity:

  Let (rho, eta) be a point in the open first quadrant (rho > 0, eta > 0)
  and mu > 0 a positive scaling factor. Define the radially scaled point
      (rho_bar, eta_bar)  =  (mu * rho, mu * eta).

  THEN:
    (i)    the angle from the positive rho-axis to (rho_bar, eta_bar)
           equals the angle to (rho, eta):
               arctan(eta_bar / rho_bar)  =  arctan(eta / rho);
    (ii)   the doubled angle is preserved exactly:
               sin(2 * gamma_bar)  =  sin(2 * gamma),
               cos(2 * gamma_bar)  =  cos(2 * gamma);
    (iii)  the radial distance scales as mu:
               sqrt(rho_bar^2 + eta_bar^2)  =  mu * sqrt(rho^2 + eta^2);
    (iv)   the angle at (1, 0) (i.e. arctan(eta_bar / (1 - rho_bar))) does
           NOT in general equal the original angle at (1, 0); it is moved
           by the radial scaling.

This is class-A pure plane geometry / similar-triangles identity. No
CKM-specific input, no Wolfenstein / atlas-triangle / alpha_s / CP-phase
authority is consumed; the narrow theorem treats (rho, eta, mu) as
abstract real symbols.

Companion role: this is a Pattern A new narrow claim row carving out the
load-bearing class-(A) protected-angle invariant of
`ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25`
(claim_type=positive_theorem, audit_status=audited_conditional, td=96,
load_bearing_step_class=A). The narrow theorem isolates the protected-
angle / radial-scaling identity from any CKM-specific upstream framing,
so it can be audit-ratified independently.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, atan, sin, cos, pi, nsimplify
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
section("Pattern A narrow theorem: radial-scaling protected angle")
# Statement: a positive radial scaling (rho, eta) -> (mu rho, mu eta)
# preserves the angle at the origin from positive rho-axis exactly. Pure
# plane geometry of similar triangles.
# ============================================================================

# Symbolic abstract variables
rho, eta, mu = symbols('rho eta mu', positive=True, real=True)
rho_bar = mu * rho
eta_bar = mu * eta


# ----------------------------------------------------------------------------
section("Part 1: ratio eta_bar / rho_bar = eta / rho symbolically")
# ----------------------------------------------------------------------------
ratio_bar = simplify(eta_bar / rho_bar)
ratio_orig = simplify(eta / rho)
check("eta_bar / rho_bar = eta / rho exact (radial-scaling preserves slope at origin)",
      simplify(ratio_bar - ratio_orig) == 0,
      detail=f"ratio_bar = {ratio_bar}")


# ----------------------------------------------------------------------------
section("Part 2: arctan(eta_bar / rho_bar) = arctan(eta / rho)")
# ----------------------------------------------------------------------------
gamma_bar = atan(eta_bar / rho_bar)
gamma_orig = atan(eta / rho)
# Check both are equal as expressions
diff = simplify(gamma_bar - gamma_orig)
check("arctan(eta_bar / rho_bar) = arctan(eta / rho) exact",
      diff == 0,
      detail=f"gamma_bar - gamma = {diff}")


# ----------------------------------------------------------------------------
section("Part 3: doubled-angle preservation sin(2 gamma) and cos(2 gamma)")
# ----------------------------------------------------------------------------
# Use double-angle formulas: sin(2 gamma) = 2 t / (1 + t^2),
# cos(2 gamma) = (1 - t^2) / (1 + t^2), where t = tan(gamma) = eta / rho.
t_orig = eta / rho
t_bar = eta_bar / rho_bar  # = eta / rho

sin_2gamma_orig = simplify(2 * t_orig / (1 + t_orig**2))
sin_2gamma_bar = simplify(2 * t_bar / (1 + t_bar**2))
cos_2gamma_orig = simplify((1 - t_orig**2) / (1 + t_orig**2))
cos_2gamma_bar = simplify((1 - t_bar**2) / (1 + t_bar**2))

check("sin(2 gamma_bar) = sin(2 gamma) exact (doubled-angle preserved)",
      simplify(sin_2gamma_bar - sin_2gamma_orig) == 0,
      detail=f"sin(2 gamma_bar) = {sin_2gamma_bar}")
check("cos(2 gamma_bar) = cos(2 gamma) exact (doubled-angle preserved)",
      simplify(cos_2gamma_bar - cos_2gamma_orig) == 0,
      detail=f"cos(2 gamma_bar) = {cos_2gamma_bar}")


# ----------------------------------------------------------------------------
section("Part 4: radial distance scales as mu")
# ----------------------------------------------------------------------------
r_bar = simplify(sqrt(rho_bar**2 + eta_bar**2))
r_orig = simplify(sqrt(rho**2 + eta**2))
expected_r_bar = mu * r_orig
check("sqrt(rho_bar^2 + eta_bar^2) = mu * sqrt(rho^2 + eta^2)",
      simplify(r_bar - expected_r_bar) == 0,
      detail=f"r_bar = {r_bar}")


# ----------------------------------------------------------------------------
section("Part 5: angle at (1, 0) is NOT preserved (counter-illustrates non-protection)")
# ----------------------------------------------------------------------------
# The angle from (1, 0) to (rho_bar, eta_bar):
#   tan(beta_bar) = eta_bar / (1 - rho_bar)
# is NOT equal to tan(beta) = eta / (1 - rho) when mu != 1, in general.
beta_orig_tan = simplify(eta / (1 - rho))
beta_bar_tan = simplify(eta_bar / (1 - rho_bar))

# Try a concrete substitution to confirm they differ.
diff_at_concrete = simplify((beta_bar_tan - beta_orig_tan).subs(
    {rho: Rational(1, 6), eta: sqrt(Rational(5)) / 6, mu: Rational(1) - Rational(1, 100)}
))
# diff_at_concrete should not be 0 (because beta is moved by mu).
check("tan(beta_bar) != tan(beta) at (rho, eta) = (1/6, sqrt(5)/6), mu = 99/100 (NOT protected)",
      diff_at_concrete != 0,
      detail=f"diff = {diff_at_concrete}")


# ----------------------------------------------------------------------------
section("Part 6: framework instance (rho, eta) = (1/6, sqrt(5)/6), mu in NLO band")
# ----------------------------------------------------------------------------
rho_val = Rational(1, 6)
eta_val = sqrt(Rational(5)) / 6
# At lambda^2 = alpha_s/2, mu = 1 - alpha_s/4
# Use a generic mu = 1 - x for x in (0, 1).
x = symbols('x', positive=True, real=True)
mu_NLO = 1 - x
rho_bar_NLO = mu_NLO * rho_val
eta_bar_NLO = mu_NLO * eta_val
ratio_NLO = simplify(eta_bar_NLO / rho_bar_NLO)
expected_ratio_NLO = sqrt(Rational(5))
check("framework instance (rho, eta) = (1/6, sqrt(5)/6) under mu = 1 - x: eta_bar/rho_bar = sqrt(5)",
      simplify(ratio_NLO - expected_ratio_NLO) == 0,
      detail=f"eta_bar/rho_bar = {ratio_NLO}")

# Doubled-angle: sin(2 gamma) = sqrt(5)/3, cos(2 gamma) = -2/3 with t = sqrt(5).
sin_2gamma_fw = simplify(2 * sqrt(Rational(5)) / (1 + Rational(5)))
cos_2gamma_fw = simplify((1 - Rational(5)) / (1 + Rational(5)))
expected_sin = sqrt(Rational(5)) / 3
expected_cos = -Rational(2, 3)
check("framework instance sin(2 gamma) = sqrt(5)/3 exact",
      simplify(sin_2gamma_fw - expected_sin) == 0,
      detail=f"sin = {sin_2gamma_fw}")
check("framework instance cos(2 gamma) = -2/3 exact",
      simplify(cos_2gamma_fw - expected_cos) == 0,
      detail=f"cos = {cos_2gamma_fw}")


# ----------------------------------------------------------------------------
section("Part 7: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")
print(f"    deps: {parent.get('deps')}")

check("parent row class-A load-bearing step (algebraic / geometric identity)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (rho, eta) be any point in the open first quadrant (rho > 0,
    eta > 0) and mu > 0 a positive scaling factor. Define the radial
    scaling
        (rho_bar, eta_bar)  =  (mu * rho, mu * eta).

  CONCLUSION:
    (i)   eta_bar / rho_bar = eta / rho exact (slope preserved);
    (ii)  arctan(eta_bar / rho_bar) = arctan(eta / rho) exact
          (origin-angle protected);
    (iii) sin(2 gamma_bar) = sin(2 gamma), cos(2 gamma_bar) = cos(2 gamma)
          exact (doubled-angle preserved);
    (iv)  sqrt(rho_bar^2 + eta_bar^2) = mu * sqrt(rho^2 + eta^2)
          (radial distance scales as mu);
    (v)   the angle at (1, 0), tan(beta_bar) = eta_bar / (1 - rho_bar),
          is NOT in general equal to tan(beta) = eta / (1 - rho)
          (counter-illustrates non-protection: only the origin-angle
          and radial distance behave canonically).

  Audit-lane class:
    (A) — pure plane geometry / similar-triangles identity. No CKM-
    specific input, no Wolfenstein / atlas-triangle / alpha_s / CP-phase
    authority. The framework instance (rho, eta) = (1/6, sqrt(5)/6) at
    NLO scaling mu = 1 - alpha_s/4 is one application; the algebra
    closes for any (rho, eta, mu) in the stated domain.

  This narrow theorem drops the parent's deps on Wolfenstein lambda^2/A^2,
  CP-phase rho/eta, atlas-triangle right-angle, and alpha_s(v) by stating
  (rho, eta, mu) as abstract symbols.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
