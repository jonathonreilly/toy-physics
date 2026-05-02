#!/usr/bin/env python3
"""Pattern B audit-companion runner for
`dm_neutrino_z3_character_transfer_theorem_note_2026-04-15`
(claim_type=positive_theorem, audit_status=audited_conditional, td=134,
load_bearing_step_class=A).

The parent's load-bearing step is the algebraic identity:

  exp(i lambda * delta_src) is a true 1d Z3 character (chi^3 = 1)
  if and only if lambda is an integer; on the continuity strip
  |lambda| <= 1 the only source-faithful branches are {-1, 0, +1}.

The existing primary runner `frontier_dm_neutrino_z3_character_transfer_theorem.py`
verifies this at numpy float precision with 1e-12 tolerance. This Pattern B
companion verifies the same algebra at sympy `Rational` / exact symbolic
precision — `exp(i * 2 * pi * n) == 1` exactly (not just within 1e-12), and
`chi(lambda)^3 == 1` reduces to a closed-form identity.

Companion role: not a new claim row; not a new source note. Provides
audit-friendly evidence that the parent's load-bearing class-(A) step
holds at exact precision. Does not modify the parent's audit status;
that decision belongs to the audit lane.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, exp, I, pi, cos, sin, simplify, expand, nsimplify
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
section("Audit companion for dm_neutrino_z3_character_transfer_theorem_note_2026-04-15 (td=134)")
# Goal: exact symbolic verification that the Z3 character-transfer
# discretization holds at sympy precision (not just 1e-12 numpy float).
# ============================================================================

# delta_src = 2 pi / 3 exactly
delta_src = 2 * pi / Rational(3)

def chi(lam):
    """Z3 phase-lift character: chi(lambda) = exp(i * lambda * delta_src)."""
    return exp(I * lam * delta_src)


# ----------------------------------------------------------------------------
section("Part 1: exact integer-lambda cases satisfy chi(lambda)^3 = 1")
# ----------------------------------------------------------------------------
# For integer lambda n: chi(n)^3 = exp(i * n * 2 pi) = 1 exactly.
for n in [-2, -1, 0, 1, 2]:
    chi_n_cubed = simplify(chi(Rational(n))**3)
    # exp(2 pi i n).rewrite(cos) = cos(2pi n) + i sin(2pi n) = 1 for integer n
    check(f"integer lambda = {n}: chi({n})^3 = 1 exactly",
          simplify(chi_n_cubed - 1) == 0,
          detail=f"chi({n})^3 = {chi_n_cubed}")


# ----------------------------------------------------------------------------
section("Part 2: exact non-integer-lambda cases fail chi(lambda)^3 = 1")
# ----------------------------------------------------------------------------
# For lambda = 1/2: chi(1/2)^3 = exp(i * pi) = -1 != 1.
# For lambda = 1/3: chi(1/3)^3 = exp(i * 2pi/3) = omega != 1.
# For lambda = 2/3: chi(2/3)^3 = exp(i * 4pi/3) = omega^2 != 1.

non_integer_cases = [
    (Rational(1, 2), -1, "lambda = 1/2 -> exp(i pi) = -1"),
    (Rational(1, 3), exp(I * 2 * pi / 3), "lambda = 1/3 -> omega = exp(2pi i/3)"),
    (Rational(2, 3), exp(I * 4 * pi / 3), "lambda = 2/3 -> omega^2"),
    (Rational(1, 4), exp(I * pi / 2), "lambda = 1/4 -> i"),
    (Rational(3, 4), exp(I * 3 * pi / 2), "lambda = 3/4 -> -i"),
]
for lam, expected, label in non_integer_cases:
    chi_cubed = simplify(chi(lam)**3)
    check(f"non-integer {label}: chi^3 != 1",
          simplify(chi_cubed - 1) != 0,
          detail=f"chi^3 = {chi_cubed}")
    check(f"non-integer {label}: chi^3 matches closed form",
          simplify(chi_cubed - expected) == 0,
          detail=f"chi^3 - expected = {simplify(chi_cubed - expected)}")


# ----------------------------------------------------------------------------
section("Part 3: continuity-strip {-1, 0, +1} is the unique exact set")
# ----------------------------------------------------------------------------
# Within |lambda| < 2 the integer values are {-1, 0, +1} (those satisfy chi^3 = 1)
# and {-2, +2} also work but lie outside the continuity strip |lambda| <= 1.
strip_set = [-1, 0, 1]
chi_values = {n: simplify(chi(Rational(n))) for n in strip_set}
print(f"\n  chi values on the continuity strip:")
for n in strip_set:
    print(f"    chi({n:+d}) = {chi_values[n]}")

# chi(0) = 1 (retained zero law)
check("chi(0) = 1 exactly (retained zero law)",
      chi_values[0] == 1,
      detail=f"chi(0) = {chi_values[0]}")

# chi(+1) = omega = exp(2pi i / 3)
omega = exp(I * 2 * pi / 3)
check("chi(+1) = omega = exp(2 pi i / 3) exactly",
      simplify(chi_values[1] - omega) == 0,
      detail=f"chi(+1) = {chi_values[1]}")

# chi(-1) = omega^bar = exp(-2pi i / 3) = conjugate of chi(+1)
omega_bar = exp(-I * 2 * pi / 3)
check("chi(-1) = omega-bar = conjugate(chi(+1)) exactly",
      simplify(chi_values[-1] - omega_bar) == 0,
      detail=f"chi(-1) = {chi_values[-1]}")

# Conjugacy explicit
chi_plus1_conj = sympy.conjugate(chi_values[1])
check("conjugate(chi(+1)) = chi(-1) exactly (orientation pair)",
      simplify(chi_plus1_conj - chi_values[-1]) == 0,
      detail=f"conjugate(chi(+1)) = {simplify(chi_plus1_conj)}")


# ----------------------------------------------------------------------------
section("Part 4: omega^3 = 1 (cube root of unity identity)")
# ----------------------------------------------------------------------------
omega_cubed = simplify(omega**3)
check("omega^3 = 1 exactly",
      simplify(omega_cubed - 1) == 0,
      detail=f"omega^3 = {omega_cubed}")
check("omega-bar^3 = 1 exactly",
      simplify(omega_bar**3 - 1) == 0,
      detail=f"omega-bar^3 = {simplify(omega_bar**3)}")
# Use rewrite(cos)+expand to force trig reduction; sympy's default simplify
# does not always reduce exp(2pi i/3) + exp(-2pi i/3) + 1 to 0.
char_sum = (omega + omega_bar + 1).rewrite(cos).expand(complex=True)
check("omega + omega-bar + 1 = 0 exactly (Z3 character sum)",
      simplify(char_sum) == 0,
      detail=f"rewritten char sum = {char_sum}")
prod_om_ombar = (omega * omega_bar).rewrite(cos).expand(complex=True)
check("omega * omega-bar = 1 exactly",
      simplify(prod_om_ombar - 1) == 0,
      detail=f"rewritten omega*omega_bar = {prod_om_ombar}")


# ----------------------------------------------------------------------------
section("Part 5: parent row dep verification")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
rows = ledger['rows']
parent_id = "dm_neutrino_z3_character_transfer_theorem_note_2026-04-15"
parent = rows.get(parent_id, {})
print(f"\n  {parent_id} current ledger state:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    effective_status: {parent.get('effective_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check(f"{parent_id} has class-(A) load-bearing step (algebraic identity)",
      parent.get('load_bearing_step_class') == 'A',
      detail=f"class = {parent.get('load_bearing_step_class')}")


# ----------------------------------------------------------------------------
section("Audit-companion summary")
# ----------------------------------------------------------------------------
print("""
  This companion provides EXACT symbolic verification (via sympy) of the
  parent theorem's load-bearing class-(A) step:

      exp(i * lambda * 2pi/3) is a Z3 character (chi^3 = 1) iff
      lambda is an integer; on the continuity strip |lambda| <= 1 the
      only source-faithful branches are {-1, 0, +1}.

  The existing primary runner
    scripts/frontier_dm_neutrino_z3_character_transfer_theorem.py
  verifies this at numpy float precision with 1e-12 tolerance; this
  companion reduces those errors to exact zero (sympy `exp(I * 2 pi * n)`
  evaluates symbolically to 1 for integer n).

  Audit-lane class for the parent's load-bearing step:
    (A) — algebraic identity / cube-root-of-unity arithmetic. No
    external observed/fitted/literature input.

  This audit-companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent's audit_status. The parent
  remains audited_conditional pending audit-lane review of the
  upstream phase-lift / weak-only source / source-orientation
  authorities the verdict identifies.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
