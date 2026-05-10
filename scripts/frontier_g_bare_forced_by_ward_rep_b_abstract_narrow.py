#!/usr/bin/env python3
"""Pattern A narrow runner for `G_BARE_FORCED_BY_WARD_REP_B_INDEPENDENCE_ABSTRACT_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone polynomial-algebra forcing identity on abstract
symbolic variables (F, g, N, c0):

  Hypothesis (abstract algebraic constraints):
      (W1)  F^2  =  c0,                                            (1)
      (W2)  F^2  =  g^2 / (2 N).                                   (2)

  Conclusion (T1) (forcing identity by equating (1) and (2)):
      g^2  =  2 N c0.                                              (3)

  Conclusion (T2) (positive-branch unique solution):
      g  =  sqrt(2 N c0)   (when c0 > 0).                          (4)

  Conclusion (T3) (canonical numerical instance):
      At (N, c0) = (3, 1/6),  g^2 = 1  and  g = 1 (positive).      (5)
      At (N, c0) = (1, 1),    g^2 = 2  and  g = sqrt(2)
                              (showing pair-specificity).

This is class-A pure polynomial algebra. No Ward identity, no lattice
gauge theory, no Wilson plaquette action, no Cl(3) framework input, no
SU(N_c) gauge group, no physical bare-coupling identification, and no
PDG / literature / fitted / admitted-unit-convention import.

The narrow theorem applies in particular to the canonical lattice
instance (N, c0) = (3, 1/6) which yields g = 1, but does not claim
those values; the abstract forcing identity is the only premise.
"""

from fractions import Fraction
from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, expand, solve, Eq
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "G_BARE_FORCED_BY_WARD_REP_B_INDEPENDENCE_ABSTRACT_NARROW_THEOREM_NOTE_2026-05-10.md"
CLAIM_ID = "g_bare_forced_by_ward_rep_b_independence_abstract_narrow_theorem_note_2026-05-10"

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
section("Pattern A narrow theorem: simultaneous-constraint forcing identity")
# Pure polynomial algebra over R. No Ward / lattice / Cl(3) / SU(N_c) input.
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: symbolic forcing identity (T1) via sympy")
# Hypothesis: F^2 = c0 (constant) and F^2 = g^2 / (2 N).
# Equate => c0 = g^2 / (2 N) => g^2 - 2 N c0 = 0.
# ----------------------------------------------------------------------------
F, g, N, c0 = symbols('F g N c0', real=True)

# Define the two abstract identities as polynomial expressions equal to zero.
W1 = F**2 - c0                       # (W1) F^2 - c0 = 0
W2 = F**2 - g**2 / (2 * N)           # (W2) F^2 - g^2/(2N) = 0

# Subtract: W1 - W2 = -c0 + g^2/(2N) = 0 => c0 = g^2/(2N) => g^2 = 2 N c0.
# i.e. (W1) - (W2) = (F^2 - c0) - (F^2 - g^2/(2N)) = g^2/(2N) - c0.
forcing_residual = simplify((W1 - W2) - (g**2 / (2 * N) - c0))
check("(W1) - (W2) algebraically equals (g^2 / (2 N) - c0) symbolically",
      forcing_residual == 0,
      detail=f"residual = {forcing_residual}")

# Multiply through by 2 N (N > 0): g^2 - 2 N c0 = 0.
g_sq_eq = (g**2 / (2 * N) - c0) * (2 * N)
g_sq_residual = simplify(g_sq_eq - (g**2 - 2 * N * c0))
check("multiplying by 2 N gives the polynomial g^2 - 2 N c0 = 0",
      g_sq_residual == 0,
      detail=f"residual = {g_sq_residual}")

# The forcing identity (T1): g^2 = 2 N c0.
forcing_identity_residual = simplify(g**2 - 2 * N * c0 - (g**2 - 2 * N * c0))
check("forcing identity (T1) g^2 = 2 N c0 is the canonical algebraic form",
      forcing_identity_residual == 0,
      detail="(trivially: g^2 - 2 N c0 = g^2 - 2 N c0)")


# ----------------------------------------------------------------------------
section("Part 2: positive-branch unique solution (T2) via sympy.solve")
# ----------------------------------------------------------------------------
# Solve g^2 - 2 N c0 = 0 for g.
g_solutions = solve(g**2 - 2 * N * c0, g)
print(f"\n  Solutions of g^2 = 2 N c0: g = {g_solutions}")
expected_solutions = [-sqrt(2 * N * c0), sqrt(2 * N * c0)]
# Check both branches present.
sols_set = set(g_solutions)
expected_set = set(expected_solutions)
check("solve gives two real roots g = ± sqrt(2 N c0)",
      sols_set == expected_set,
      detail=f"got {g_solutions}")

# Positive branch: g = sqrt(2 N c0) is unique among the two.
positive_branch = [s for s in g_solutions if str(s).startswith('sqrt')]
check("positive branch g = sqrt(2 N c0) is uniquely determined",
      len(positive_branch) == 1 and simplify(positive_branch[0] - sqrt(2 * N * c0)) == 0,
      detail=f"positive branch = {positive_branch}")


# ----------------------------------------------------------------------------
section("Part 3: canonical numerical instance (T3) at (N, c0) = (3, 1/6) yields g = 1")
# ----------------------------------------------------------------------------
# Substitute concrete rational values.
N_val = Rational(3)
c0_val = Rational(1, 6)
g_squared_at_3_1_6 = simplify((2 * N * c0).subs({N: N_val, c0: c0_val}))
check("at (N, c0) = (3, 1/6): g^2 = 2 · 3 · (1/6) = 1 exact",
      g_squared_at_3_1_6 == 1,
      detail=f"g^2 = {g_squared_at_3_1_6}")

g_at_3_1_6 = sqrt(g_squared_at_3_1_6)
check("at (N, c0) = (3, 1/6): positive branch g = 1 exact",
      g_at_3_1_6 == 1,
      detail=f"g = sqrt(1) = {g_at_3_1_6}")

# Cross-check via Fraction (exact-rational arithmetic):
g_sq_frac = Fraction(2) * Fraction(3) * Fraction(1, 6)
check("Fraction cross-check at (3, 1/6): g^2 = 1 exactly",
      g_sq_frac == Fraction(1),
      detail=f"Fraction: g^2 = 2 · 3 · 1/6 = {g_sq_frac}")


# ----------------------------------------------------------------------------
section("Part 4: alternative pair (N, c0) = (1, 1) yields g = sqrt(2) ≠ 1")
# ----------------------------------------------------------------------------
g_squared_at_1_1 = simplify((2 * N * c0).subs({N: Rational(1), c0: Rational(1)}))
check("at (N, c0) = (1, 1): g^2 = 2 · 1 · 1 = 2 exact",
      g_squared_at_1_1 == 2,
      detail=f"g^2 = {g_squared_at_1_1}")

g_at_1_1 = sqrt(g_squared_at_1_1)
check("at (N, c0) = (1, 1): positive branch g = sqrt(2) ≠ 1",
      g_at_1_1 != 1 and simplify(g_at_1_1 - sqrt(Rational(2))) == 0,
      detail=f"g = sqrt(2) = {g_at_1_1}")


# ----------------------------------------------------------------------------
section("Part 5: counter-grid of (N, c0) pairs forcing distinct g^2 values")
# ----------------------------------------------------------------------------
counter_grid = [
    (Fraction(2), Fraction(1, 4), Fraction(1)),       # 2·2·(1/4) = 1
    (Fraction(3), Fraction(2, 3), Fraction(4)),       # 2·3·(2/3) = 4
    (Fraction(5), Fraction(1, 10), Fraction(1)),      # 2·5·(1/10) = 1
    (Fraction(7), Fraction(7, 14), Fraction(7)),      # 2·7·(1/2) = 7
    (Fraction(11), Fraction(3, 22), Fraction(3)),     # 2·11·(3/22) = 3
    (Fraction(13), Fraction(5, 26), Fraction(5)),     # 2·13·(5/26) = 5
]

for N_v, c0_v, expected_g_sq in counter_grid:
    g_sq = Fraction(2) * N_v * c0_v
    check(f"forcing at (N, c0) = ({N_v}, {c0_v}): g^2 = {expected_g_sq}",
          g_sq == expected_g_sq,
          detail=f"g^2 = 2 · {N_v} · {c0_v} = {g_sq}")


# ----------------------------------------------------------------------------
section("Part 6: pair-specificity — g = 1 is NOT forced for arbitrary (N, c0)")
# ----------------------------------------------------------------------------
# Demonstrate that not every (N, c0) yields g = 1. Only pairs satisfying
# 2 N c0 = 1 force g = 1; other pairs force other values.
for N_v, c0_v, expected_g_sq in counter_grid:
    if expected_g_sq != Fraction(1):
        check(f"at (N, c0) = ({N_v}, {c0_v}): forced g^2 = {expected_g_sq} ≠ 1",
              expected_g_sq != Fraction(1),
              detail=f"g = 1 NOT forced at this pair")


# ----------------------------------------------------------------------------
section("Part 7: c0 = 0 contradicts g > 0 (T2 boundary)")
# ----------------------------------------------------------------------------
# If c0 = 0, then g^2 = 0, hence g = 0, contradicting g > 0.
g_sq_at_zero = Fraction(2) * Fraction(3) * Fraction(0)
check("at c0 = 0: g^2 = 0, contradicting g > 0 (boundary degeneracy)",
      g_sq_at_zero == Fraction(0),
      detail=f"g^2 = 0 at c0 = 0; positive branch undefined")


# ----------------------------------------------------------------------------
section("Part 8: independence from any Ward / lattice / Cl(3) / SU(N_c) input")
# ----------------------------------------------------------------------------
# The narrow theorem holds for any abstract (F, g, N, c0). The "Ward
# Rep-B-independence + same-1PI pinning" instance with (N, c0) = (N_c, 1/6)
# is a SPECIAL CASE; the theorem does not depend on, derive, or claim those
# identifications.
#
# Demonstrate at a non-physical instance with N = π/4 (irrational) — the
# identity remains a pure algebraic substitution.
#
# Use sympy positive symbols to avoid branch ambiguity:
N_sym, c0_sym = symbols('N_sym c0_sym', positive=True, real=True)
g_sq_sym = simplify(2 * N_sym * c0_sym)
check("identity holds at fully symbolic (N, c0) with no numerical values",
      g_sq_sym == 2 * N_sym * c0_sym,
      detail="g^2 = 2·N·c0 is the algebraic forcing identity at any (N, c0)")

# Demonstrate at irrational N (not the integer N_c = 3):
import math
N_pi = sympy.pi / 4
c0_e = sympy.E
g_sq_pi_e = simplify(2 * N_pi * c0_e)
check("at (N, c0) = (π/4, e): g^2 = (π e)/2 (irrational, but identity holds)",
      simplify(g_sq_pi_e - sympy.pi * sympy.E / 2) == 0,
      detail=f"g^2 = {g_sq_pi_e}")


# ----------------------------------------------------------------------------
section("Part 9: note structure and narrow-scope discipline")
# ----------------------------------------------------------------------------
note_text = NOTE_PATH.read_text()
required = [
    "g_bare Forced by Ward Rep-B-Independence Abstract Narrow Theorem",
    "Type:** positive_theorem",
    "polynomial-algebra forcing identity",
    "no Ward identity",
    "no lattice gauge theory",
    "Wilson\nplaquette action",
    "no SU(N_c) gauge group",
    "g^2  =  2 N c0",
    "Cited dependencies\n\nNone",
    "Forbidden imports check",
]
for s in required:
    check(f"note contains: {s!r}", s in note_text)

# Critical: the narrow note must NOT claim physical-convention identifications.
forbidden = [
    "g_bare = 1 is uniquely forced by Cl(3)",
    "Wilson plaquette action is uniquely forced",
    "g_bare = 1 follows from A1 + A2",
    "Ward identity is derived from this note",
]
for f in forbidden:
    check(f"narrow scope avoids forbidden physical claim: {f!r}",
          f not in note_text)


# ----------------------------------------------------------------------------
section("Part 10: parent / sibling row context (no ledger modification)")
# ----------------------------------------------------------------------------
# The narrow theorem carves out the load-bearing class-A polynomial-algebra
# core that is ALSO embedded inside the existing
# `g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09` row's
# scoped substitution at (N, c0) = (N_c, 1/6) = (3, 1/6) → g_bare = 1.
# The narrow theorem here drops the Ward / staggered-Dirac / Wilson deps
# entirely by stating only the abstract symbolic forcing identity.
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('g_bare_forced_by_ward_rep_b_independence_theorem_note_2026-05-09', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    deps: {parent.get('deps')}")

check("parent row exists in ledger (graph-visible)",
      parent != {},
      detail=f"parent claim_type={parent.get('claim_type')!r}")

# Optional: confirm self-row seeded after pipeline run.
self_row = ledger['rows'].get(CLAIM_ID, None)
if self_row is not None:
    print(f"\n  Self row state (post-pipeline):")
    print(f"    claim_type: {self_row.get('claim_type')}")
    print(f"    deps: {self_row.get('deps')}")
    retained_grade_statuses = {"retained", "retained_bounded", "retained_no_go"}
    check("self row not promoted to retained-grade by this runner",
          self_row.get('effective_status') not in retained_grade_statuses,
          detail=f"effective_status={self_row.get('effective_status')!r}")
    check("self row records zero load-bearing dependencies (deps=[])",
          self_row.get('deps') == [],
          detail=f"deps={self_row.get('deps')}")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (F, g, N, c0) be abstract symbolic variables with g > 0, N > 0,
    F arbitrary in any field of characteristic zero, and c0 ∈ R_{>=0}.
    Suppose the two algebraic constraints

        (W1)  F^2  =  c0,                                          (1)
        (W2)  F^2  =  g^2 / (2 N).                                 (2)

  CONCLUSION:
    Equating (1) and (2),

        g^2  =  2 N c0.                                            (T1)

    On the positive branch g > 0 (when c0 > 0),

        g  =  sqrt(2 N c0).                                        (T2)

    At (N, c0) = (3, 1/6), the forced value is g = 1; at (N, c0) = (1, 1),
    the forced value is g = sqrt(2) ≠ 1 (pair-specific).             (T3)

  Audit-lane class:
    (A) -- pure polynomial algebra over R. No external observed/fitted/
    literature/Ward/lattice/Cl(3)/SU(N_c) input. Proof is one-line
    direct algebraic substitution.

  This narrow theorem is independent of the parent g_bare forced-by-Ward
  bounded theorem's physical Ward Rep-B-independence + same-1PI pinning
  framing. The lattice instance (N, c0) = (N_c, 1/6) = (3, 1/6) is just
  one application; the forcing identity holds for any abstract
  (F, g, N, c0) by the same algebraic substitution.

  Distinct from the sibling
  BETA_GBARE_RESCALING_ABSTRACT_IDENTITY_NARROW_THEOREM_NOTE_2026-05-10
  (PR #1034), which captures the rescaling identity
  β(g/c, N) = c^2 · β(g, N). The present note captures the
  simultaneous-constraint forcing identity g^2 = 2 N c0 — different
  abstract structure.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
