#!/usr/bin/env python3
"""Pattern A narrow runner for `THALES_RIGHT_ANGLE_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone Euclidean / algebraic identity:

  For any (rho, eta) with eta^2 = rho * (1 - rho) (i.e., (rho, eta) lies
  on the Thales circle on diameter [0, 1]) and 0 < rho < 1, eta > 0:

      The triangle with vertices (0, 0), (1, 0), (rho, eta) has a right
      angle at (rho, eta).

This is pure Euclidean geometry / arctan algebra. No CKM-specific input,
no atlas/Wolfenstein values, no PDG/literature/fitted/admitted imports.

The narrow theorem applies in particular to the special instance
(rho, eta) = (1/6, sqrt(5)/6), but does not claim those values; the
Thales hypothesis is the only premise.

Companion role: not a new audit-companion; this is a Pattern A new
narrow claim row carving out the algebra-only core of the existing
`ckm_atlas_triangle_right_angle_theorem_note_2026-04-24`. The parent's
load-bearing step is class A, and the parent's `audited_conditional`
verdict is solely on the upstream supply of the (rho, eta) values; this
narrow rephrasing drops that dependency by hypothesis.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, atan, pi, simplify, symbols, Symbol
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
section("Pattern A narrow theorem: Thales right-angle on diameter [0, 1]")
# Statement: eta^2 = rho * (1 - rho), 0 < rho < 1, eta > 0
#   ==> triangle (0,0)-(1,0)-(rho,eta) has a right angle at (rho, eta).
# Pure Euclidean / arctan algebra. No CKM-specific input.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: symbolic Thales identity")
# ----------------------------------------------------------------------------
# Symbolic form: assume eta^2 = rho(1-rho). Show the angle at (rho, eta)
# in the triangle (0,0)-(1,0)-(rho,eta) is exactly pi/2.

rho, eta = symbols('rho eta', positive=True, real=True)

# Two edge vectors meeting at vertex (rho, eta):
# v_to_origin = (0,0) - (rho, eta) = (-rho, -eta)
# v_to_one    = (1,0) - (rho, eta) = (1 - rho, -eta)
v_to_origin = sympy.Matrix([-rho, -eta])
v_to_one = sympy.Matrix([1 - rho, -eta])

dot_product = (v_to_origin.T * v_to_one)[0, 0]
# Symbolic: dot = -rho(1-rho) + eta^2
dot_expanded = sympy.expand(dot_product)

print(f"\n  Edge dot product at (rho, eta) symbolically: {dot_expanded}")
# On Thales hypothesis eta^2 = rho(1-rho), substitute:
dot_under_thales = simplify(dot_expanded.subs(eta**2, rho * (1 - rho)))
print(f"  Under hypothesis eta^2 = rho(1-rho): dot = {dot_under_thales}")

check("symbolic dot product at (rho, eta) reduces to eta^2 - rho(1-rho)",
      simplify(dot_expanded - (eta**2 - rho * (1 - rho))) == 0,
      detail=f"dot = {dot_expanded}")
check("Thales hypothesis eta^2 = rho(1-rho) forces dot product to zero (pi/2 angle)",
      dot_under_thales == 0,
      detail="zero dot product <=> right angle")


# ----------------------------------------------------------------------------
section("Part 2: arctan-sum form of the identity")
# ----------------------------------------------------------------------------
# Equivalent form: arctan(eta/rho) + arctan(eta/(1-rho)) = pi/2 on the Thales
# circle (because tan(a) * tan(b) = eta^2 / (rho(1-rho)) = 1, so a + b = pi/2).

tan_a_times_tan_b = (eta / rho) * (eta / (1 - rho))
tan_a_times_tan_b_simplified = simplify(tan_a_times_tan_b)
print(f"\n  tan(arctan(eta/rho)) * tan(arctan(eta/(1-rho))) = {tan_a_times_tan_b_simplified}")
under_thales = simplify(tan_a_times_tan_b.subs(eta**2, rho * (1 - rho)))
print(f"  Under hypothesis eta^2 = rho(1-rho): product = {under_thales}")

check("tan-product on Thales circle equals 1",
      under_thales == 1,
      detail="tan(a) * tan(b) = 1 implies a + b = pi/2 for a, b in (0, pi/2)")


# ----------------------------------------------------------------------------
section("Part 3: concrete numerical verifications")
# ----------------------------------------------------------------------------
# Verify the identity at three independent Thales-circle points:
#   (rho, eta) = (1/6, sqrt(5)/6)        # the CKM atlas instance
#   (rho, eta) = (1/2, 1/2)              # midpoint case
#   (rho, eta) = (1/3, sqrt(2)/3)        # another rational instance

cases = [
    (Rational(1, 6), sqrt(5) / 6, "CKM atlas instance"),
    (Rational(1, 2), Rational(1, 2), "midpoint case"),
    (Rational(1, 3), sqrt(2) / 3, "rational point #2"),
    (Rational(1, 4), sqrt(3) / 4, "rational point #3"),
]

for rho_val, eta_val, label in cases:
    # Verify Thales hypothesis
    thales_holds = simplify(eta_val**2 - rho_val * (1 - rho_val)) == 0
    check(f"{label}: (rho, eta) = ({rho_val}, {eta_val}) satisfies eta^2 = rho(1-rho)",
          thales_holds,
          detail=f"eta^2 = {simplify(eta_val**2)}, rho(1-rho) = {simplify(rho_val * (1 - rho_val))}")
    # Verify dot product is zero
    dot = -rho_val * (1 - rho_val) + eta_val**2
    check(f"{label}: dot product zero (right angle at vertex)",
          simplify(dot) == 0,
          detail=f"dot = {simplify(dot)}")
    # Verify arctan sum equals pi/2 (numerical check at high precision;
    # sympy does not automatically simplify atan(x) + atan(1/x) = pi/2).
    angle_sum = atan(eta_val / rho_val) + atan(eta_val / (1 - rho_val))
    diff_numeric = sympy.N(angle_sum - pi / 2, 50)
    check(f"{label}: arctan(eta/rho) + arctan(eta/(1-rho)) = pi/2 (50-digit)",
          abs(diff_numeric) < sympy.Rational(1, 10**45),
          detail=f"angle_sum - pi/2 = {diff_numeric}")


# ----------------------------------------------------------------------------
section("Part 4: independence from any CKM-specific input")
# ----------------------------------------------------------------------------
# This narrow theorem holds for ANY (rho, eta) with 0 < rho < 1, eta > 0
# on the Thales circle eta^2 = rho(1-rho). The CKM atlas instance
# (rho, eta) = (1/6, sqrt(5)/6) is a SPECIAL CASE; the theorem does not
# depend on, derive, or claim those values.

# Demonstrate the identity at a non-CKM instance with irrational rho:
rho_irrational = Rational(7, 13)
eta_irrational = sqrt(rho_irrational * (1 - rho_irrational))
thales_check = simplify(eta_irrational**2 - rho_irrational * (1 - rho_irrational)) == 0
dot_irrational = simplify(-rho_irrational * (1 - rho_irrational) + eta_irrational**2)
check(f"non-CKM instance (rho, eta) = (7/13, sqrt(42)/13): right-angle holds",
      thales_check and dot_irrational == 0,
      detail="confirms no dependency on CKM-specific (rho, eta) values")


# ----------------------------------------------------------------------------
section("Part 5: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
# The narrow theorem carves out the load-bearing class-A geometric core of
# `ckm_atlas_triangle_right_angle_theorem_note_2026-04-24`, which currently
# sits at audited_conditional with td=116. The parent's verdict cites the
# unratified `ckm_cp_phase_structural_identity_theorem_note_2026-04-24`
# dep that supplies the specific (rho, eta) = (1/6, sqrt(5)/6) values.
# The narrow theorem here drops that dep entirely by stating only the
# geometric implication, conditioned on the Thales hypothesis as an
# explicit input.

LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('ckm_atlas_triangle_right_angle_theorem_note_2026-04-24', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")
print(f"    deps: {parent.get('deps')}")

check("parent row class-A load-bearing step (purely geometric)",
      parent.get('load_bearing_step_class') == 'A')
check("parent row is bounded_theorem or positive_theorem (carve-out applies)",
      parent.get('claim_type') in ('positive_theorem', 'bounded_theorem'))


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (rho, eta) be any pair of real numbers with
        0 < rho < 1, eta > 0, eta^2 = rho(1 - rho).
    (i.e., (rho, eta) lies on the upper half of the Thales circle on the
     diameter [0, 1].)

  CONCLUSION:
    The triangle with vertices (0, 0), (1, 0), (rho, eta) has a right
    angle at (rho, eta), i.e. the two edges meeting at (rho, eta) are
    orthogonal in the Euclidean plane.

  Audit-lane class:
    (A) — pure algebraic / Euclidean-geometric identity. No external
    observed/fitted/literature/CKM-specific input. Proof is one-line
    Pythagoras / dot-product calculation.

  This narrow theorem is independent of the parent's CKM-specific
  (rho, eta) = (1/6, sqrt(5)/6) supply. The CKM instance is just one
  point on the Thales circle; the right-angle conclusion holds for any
  such point by the same geometric identity.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
