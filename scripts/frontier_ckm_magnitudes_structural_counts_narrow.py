#!/usr/bin/env python3
"""Pattern A narrow runner for `CKM_MAGNITUDES_STRUCTURAL_COUNTS_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone algebraic-substitution implication:

  GIVEN the four parametric input identities
      lambda^2          =  alpha_s / n_pair,
      A^2               =  n_pair / n_color,
      rho^2 + eta^2     =  1 / n_quark,
      (1 - rho)^2 + eta^2  =  (n_quark - 1) / n_quark,
      n_quark           =  n_pair * n_color,
  THEN the five Wolfenstein-leading squared off-diagonal CKM-style
  magnitudes are the closed-form expressions
      |V_us|_0^2 = lambda^2                          = alpha_s / n_pair,
      |V_cb|_0^2 = A^2 lambda^4                      = alpha_s^2 / (n_pair n_color),
      |V_ts|_0^2 = A^2 lambda^4                      = alpha_s^2 / (n_pair n_color),
      |V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2)      = alpha_s^3 / (n_pair^3 n_color^2),
      |V_td|_0^2 = A^2 lambda^6 ((1-rho)^2 + eta^2)  = (n_quark - 1) alpha_s^3 / (n_pair^3 n_color^2).

This narrow theorem treats (alpha_s, lambda, A, rho, eta, n_pair, n_color,
n_quark) as ABSTRACT SYMBOLS satisfying the listed input identities. It
does not derive, claim, or import any specific value of alpha_s, any
Wolfenstein/atlas authority, any CP-phase identity, or any Thales/triangle
authority. It does not claim any physical-CKM identification, any PDG
comparator, or any framework-specific (n_pair, n_color, n_quark) = (2, 3, 6)
assignment.

The narrow theorem can be applied to ANY tuple satisfying the input
hypotheses; the framework-specific instance (n_pair, n_color, n_quark) =
(2, 3, 6) is a concrete special case shown for sanity, not a load-bearing
input.

Companion role: not a new audit-companion; this is a Pattern A new narrow
claim row carving out the algebra-only core of the existing
`ckm_magnitudes_structural_counts_theorem_note_2026-04-25` (claim_type=
positive_theorem, load_bearing_step_class=A).
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, expand, factor, cancel
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
section("Pattern A narrow theorem: structural-counts algebra (M1)-(M5)")
# Statement: under the four input parametric identities, the five
# Wolfenstein-leading squared off-diagonal CKM magnitudes are forced
# closed-form expressions in (alpha_s, n_pair, n_color, n_quark).
# Pure algebraic substitution. No CKM-physical claim, no PDG comparator.
# ============================================================================

# Abstract symbols
alpha_s, n_pair, n_color, n_quark = symbols(
    'alpha_s n_pair n_color n_quark', positive=True, real=True)

# Input identities (treated as definitions of lambda^2, A^2, rho^2 + eta^2, etc.)
lambda_sq = alpha_s / n_pair
A_sq = n_pair / n_color
rho_sq_plus_eta_sq = 1 / n_quark              # = rho when rho = 1/n_quark
one_minus_rho_sq_plus_eta_sq = (n_quark - 1) / n_quark

# Auxiliary: n_quark = n_pair * n_color (treated as a hypothesis)
n_quark_constraint = n_pair * n_color


# ----------------------------------------------------------------------------
section("Part 1: (M1) |V_us|_0^2 = lambda^2 -> alpha_s / n_pair")
# ----------------------------------------------------------------------------
V_us_sq = lambda_sq
V_us_sq_expected = alpha_s / n_pair
check("(M1) |V_us|_0^2 = alpha_s / n_pair (pure substitution from lambda^2 def)",
      simplify(V_us_sq - V_us_sq_expected) == 0,
      detail=f"|V_us|_0^2 = {V_us_sq}")


# ----------------------------------------------------------------------------
section("Part 2: (M2) |V_cb|_0^2 = A^2 lambda^4 -> alpha_s^2 / (n_pair n_color)")
# ----------------------------------------------------------------------------
V_cb_sq = A_sq * lambda_sq**2
V_cb_sq_simplified = simplify(V_cb_sq)
V_cb_sq_expected = alpha_s**2 / (n_pair * n_color)
check("(M2) |V_cb|_0^2 = alpha_s^2 / (n_pair * n_color)",
      simplify(V_cb_sq - V_cb_sq_expected) == 0,
      detail=f"|V_cb|_0^2 = {V_cb_sq_simplified}")


# ----------------------------------------------------------------------------
section("Part 3: (M3) |V_ts|_0^2 = |V_cb|_0^2 (atlas-leading equality)")
# ----------------------------------------------------------------------------
V_ts_sq = A_sq * lambda_sq**2  # same Wolfenstein leading expression
check("(M3) |V_ts|_0^2 = |V_cb|_0^2 = alpha_s^2 / (n_pair * n_color)",
      simplify(V_ts_sq - V_cb_sq_expected) == 0,
      detail=f"|V_ts|_0^2 = {simplify(V_ts_sq)}")


# ----------------------------------------------------------------------------
section("Part 4: (M4) |V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2) -> alpha_s^3 / (n_pair^3 n_color^2)")
# ----------------------------------------------------------------------------
V_ub_sq = A_sq * lambda_sq**3 * rho_sq_plus_eta_sq
V_ub_sq_simplified = simplify(V_ub_sq)
print(f"\n  |V_ub|_0^2 in (alpha_s, n_pair, n_color, n_quark) = {V_ub_sq_simplified}")

# Substitute n_quark = n_pair * n_color
V_ub_sq_with_constraint = simplify(V_ub_sq.subs(n_quark, n_quark_constraint))
V_ub_sq_expected = alpha_s**3 / (n_pair**3 * n_color**2)
check("(M4) |V_ub|_0^2 = alpha_s^3 / (n_pair^3 * n_color^2) under n_quark = n_pair * n_color",
      simplify(V_ub_sq_with_constraint - V_ub_sq_expected) == 0,
      detail=f"|V_ub|_0^2 = {V_ub_sq_with_constraint}")


# ----------------------------------------------------------------------------
section("Part 5: (M5) |V_td|_0^2 = A^2 lambda^6 ((1-rho)^2 + eta^2)")
# ----------------------------------------------------------------------------
V_td_sq = A_sq * lambda_sq**3 * one_minus_rho_sq_plus_eta_sq
V_td_sq_simplified = simplify(V_td_sq)
print(f"\n  |V_td|_0^2 in (alpha_s, n_pair, n_color, n_quark) = {V_td_sq_simplified}")

V_td_sq_with_constraint = simplify(V_td_sq.subs(n_quark, n_quark_constraint))
V_td_sq_expected = (n_quark_constraint - 1) * alpha_s**3 / (n_pair**3 * n_color**2)
V_td_sq_expected_simplified = simplify(V_td_sq_expected)
check("(M5) |V_td|_0^2 = (n_quark - 1) alpha_s^3 / (n_pair^3 * n_color^2) under n_quark = n_pair * n_color",
      simplify(V_td_sq_with_constraint - V_td_sq_expected_simplified) == 0,
      detail=f"|V_td|_0^2 = {V_td_sq_with_constraint}")


# ----------------------------------------------------------------------------
section("Part 6: ratio identities derivable from the structural-counts algebra")
# ----------------------------------------------------------------------------
# (M2) / (M1) = A^2 lambda^2 = alpha_s / n_color
ratio_cb_us = simplify(V_cb_sq_expected / (alpha_s / n_pair))
expected_cb_us = alpha_s / n_color
check("|V_cb|_0^2 / |V_us|_0^2 = alpha_s / n_color (= A^2 lambda^2)",
      simplify(ratio_cb_us - expected_cb_us) == 0,
      detail=f"|V_cb|^2 / |V_us|^2 = {ratio_cb_us}")

# (M5) / (M4) = (n_quark - 1)
ratio_td_ub = simplify(V_td_sq_expected_simplified / V_ub_sq_expected)
check("|V_td|_0^2 / |V_ub|_0^2 = n_quark - 1 (purely combinatorial ratio)",
      simplify(ratio_td_ub - (n_quark_constraint - 1)) == 0,
      detail=f"ratio = {ratio_td_ub}")


# ----------------------------------------------------------------------------
section("Part 7: framework-specific instance (n_pair, n_color, n_quark) = (2, 3, 6)")
# ----------------------------------------------------------------------------
# Special case shown for sanity, NOT load-bearing on the narrow theorem.
sub = {n_pair: Rational(2), n_color: Rational(3), n_quark: Rational(6)}
V_us_2_3 = simplify(V_us_sq.subs(sub))
V_cb_2_3 = simplify(V_cb_sq.subs(sub))
V_ub_2_3 = simplify(V_ub_sq.subs(sub))
V_td_2_3 = simplify(V_td_sq.subs(sub))

check("(2,3,6) instance: |V_us|_0^2 = alpha_s / 2",
      simplify(V_us_2_3 - alpha_s / 2) == 0,
      detail=f"|V_us|_0^2 = {V_us_2_3}")
check("(2,3,6) instance: |V_cb|_0^2 = alpha_s^2 / 6",
      simplify(V_cb_2_3 - alpha_s**2 / 6) == 0,
      detail=f"|V_cb|_0^2 = {V_cb_2_3}")
check("(2,3,6) instance: |V_ub|_0^2 = alpha_s^3 / 72",
      simplify(V_ub_2_3 - alpha_s**3 / 72) == 0,
      detail=f"|V_ub|_0^2 = {V_ub_2_3}")
check("(2,3,6) instance: |V_td|_0^2 = 5 alpha_s^3 / 72",
      simplify(V_td_2_3 - 5 * alpha_s**3 / 72) == 0,
      detail=f"|V_td|_0^2 = {V_td_2_3}")


# ----------------------------------------------------------------------------
section("Part 8: alternative non-(2,3,6) instance to confirm independence from framework counts")
# ----------------------------------------------------------------------------
# Instance: (n_pair, n_color, n_quark) = (3, 4, 12). Same algebra applies.
sub_alt = {n_pair: Rational(3), n_color: Rational(4), n_quark: Rational(12)}
V_us_alt = simplify(V_us_sq.subs(sub_alt))
V_cb_alt = simplify(V_cb_sq.subs(sub_alt))
V_ub_alt = simplify(V_ub_sq.subs(sub_alt))
V_td_alt = simplify(V_td_sq.subs(sub_alt))

check("(3,4,12) instance: |V_us|_0^2 = alpha_s / 3",
      simplify(V_us_alt - alpha_s / 3) == 0,
      detail=f"|V_us|_0^2 = {V_us_alt}")
check("(3,4,12) instance: |V_cb|_0^2 = alpha_s^2 / 12",
      simplify(V_cb_alt - alpha_s**2 / 12) == 0,
      detail=f"|V_cb|_0^2 = {V_cb_alt}")
check("(3,4,12) instance: |V_ub|_0^2 = alpha_s^3 / (27 * 16) = alpha_s^3 / 432",
      simplify(V_ub_alt - alpha_s**3 / 432) == 0,
      detail=f"|V_ub|_0^2 = {V_ub_alt}")
check("(3,4,12) instance: |V_td|_0^2 = 11 alpha_s^3 / 432",
      simplify(V_td_alt - 11 * alpha_s**3 / 432) == 0,
      detail=f"|V_td|_0^2 = {V_td_alt}")


# ----------------------------------------------------------------------------
section("Part 9: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('ckm_magnitudes_structural_counts_theorem_note_2026-04-25', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-A load-bearing step (algebraic substitution)",
      parent.get('load_bearing_step_class') == 'A')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESES (input parametric identities, NOT derived here):
      lambda^2                   = alpha_s / n_pair,
      A^2                        = n_pair / n_color,
      rho^2 + eta^2              = 1 / n_quark,
      (1 - rho)^2 + eta^2        = (n_quark - 1) / n_quark,
      n_quark                    = n_pair * n_color.

  CONCLUSION (algebraic-substitution forced):
      |V_us|_0^2  =  alpha_s / n_pair,
      |V_cb|_0^2  =  alpha_s^2 / (n_pair * n_color),
      |V_ts|_0^2  =  alpha_s^2 / (n_pair * n_color),
      |V_ub|_0^2  =  alpha_s^3 / (n_pair^3 * n_color^2),
      |V_td|_0^2  =  (n_quark - 1) * alpha_s^3 / (n_pair^3 * n_color^2).

  Audit-lane class:
    (A) — pure algebraic substitution. No external observed/fitted/literature
    input. No physical-CKM identification, no PDG comparator. The
    framework-specific instance (n_pair, n_color, n_quark) = (2, 3, 6) is a
    concrete sanity case, not a load-bearing input.

  The narrow theorem drops the parent row's dependencies on ALPHA_S_DERIVED,
  WOLFENSTEIN_LAMBDA_A, CKM_CP_PHASE, CKM_ATLAS_TRIANGLE_RIGHT_ANGLE by
  stating the four input parametric identities as hypotheses.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
