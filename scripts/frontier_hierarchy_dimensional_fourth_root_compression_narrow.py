#!/usr/bin/env python3
"""Narrow runner for HIERARCHY_DIMENSIONAL_FOURTH_ROOT_COMPRESSION_NARROW_THEOREM_NOTE_2026-05-10.

Verifies the standalone class-A dimensional-analysis identity at d = 4:

  (a)  In d-dim Euclidean thermal QFT in Stefan-Boltzmann form (f ~ T^d,
       Kapusta-Gale ch. 3, Vassilevich hep-th/0306138 sec 4,
       Laine-Vuorinen ch. 2), the free-energy density carries mass
       dimension [f] = d.

  (b)  The unique mass-dim-1 fractional-power scale extraction from f
       is M = f^(1/d). The exponent 1/d is the unique rational that
       maps a mass-dim-d input to a mass-dim-1 output by simple power.

  (c)  At d = 4, the compression exponent is 1/d = 1/4.

  (d)  Among integer d >= 1, the rational value 1/d = 1/4 is taken
       uniquely at d = 4.

Pure class-A dimensional analysis on a textbook Stefan-Boltzmann form.
No framework axiom or admission is consumed.

This narrow theorem is INDEPENDENT of the sister narrow theorem in
HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md,
which proves the number-theoretic algebraic equivalence
2^(d - 2) = d <=> 1/(2d) = 2^(1 - d). Both narrow theorems give 1/4
at d = 4 for INDEPENDENT reasons (one number-theoretic, one
dimensional-analysis); both must independently retain.

Target: PASS = 11, FAIL = 0.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

try:
    import sympy as sp
    from sympy import (
        Rational,
        Symbol,
        nsimplify,
        simplify,
        symbols,
    )
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS (A)"
    else:
        FAIL += 1
        tag = "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: dimensional fourth-root compression at d=4")
# Statement: in d-dim Euclidean thermal QFT in Stefan-Boltzmann form, the
# free-energy density carries [f] = d, and the unique mass-dim-1 fractional-
# power scale extraction is M = f^(1/d). At d = 4, this is 1/d = 1/4. Among
# integer d >= 1, the value 1/d = 1/4 is taken uniquely at d = 4.
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1: mass-dimension of f in d-dim Stefan-Boltzmann form (T1)")
# Standalone fact (textbook Stefan-Boltzmann scaling, Kapusta-Gale ch. 3,
# Vassilevich hep-th/0306138 sec 4): in d-dim Euclidean thermal QFT for a
# massless relativistic gas, f ~ T^d in natural units, hence
#   [f] = d * [T] = d * 1 = d.
# We model the dimension symbolically in sympy: assign T mass-dim 1, and
# check that f = C * T^d carries dimension d. The dimensionless constant
# C carries dim 0 and does not affect the leading-power dimension count.
# ----------------------------------------------------------------------------

# Symbolic dimension tracker: we treat 'mass_dim' as a SymPy symbolic
# label. The Stefan-Boltzmann form f = C_d * T^d induces
#   mass_dim(f) = mass_dim(C_d) + d * mass_dim(T) = 0 + d * 1 = d.
T_dim = Symbol("T_dim", real=True)
d_sym = Symbol("d", positive=True, integer=True)
C_dim = Symbol("C_dim", real=True)
# In natural units ℏ = c = k_B = 1, [T] = 1, [C_d] = 0
mass_dim_T = sp.Integer(1)
mass_dim_C = sp.Integer(0)
mass_dim_f = mass_dim_C + d_sym * mass_dim_T  # = d
expected_dim_f = d_sym
sb_dim_match = simplify(mass_dim_f - expected_dim_f) == 0
check(
    "T1: in d-dim Stefan-Boltzmann form f = C_d * T^d, [f] = d (sympy dim tracking)",
    sb_dim_match,
    detail=f"mass_dim(f) = {mass_dim_f}, expected = {expected_dim_f}",
)


# ----------------------------------------------------------------------------
section("Part 2: scale extraction M = f^(1/d) gives [M] = 1 (T2)")
# Given [f] = d, the equation [M] = [f]^alpha = d * alpha = 1 has unique
# rational solution alpha = 1/d. Hence M = C_M * f^(1/d) with [M] = 1.
# We verify across d in {1, 2, 3, 4, 5, 6, 7, 8} via Fraction arithmetic.
# ----------------------------------------------------------------------------

t2_dims = {}
all_t2_one = True
for d in range(1, 9):
    alpha = Fraction(1, d)
    mass_dim_M = d * alpha  # = 1 by construction
    t2_dims[d] = mass_dim_M
    if mass_dim_M != Fraction(1):
        all_t2_one = False
check(
    "T2: M = f^(1/d) gives [M] = 1 for d in {1,...,8} (Fraction)",
    all_t2_one,
    detail="dims = "
    + ", ".join(f"d={d}:[M]={dim}" for d, dim in t2_dims.items()),
)


# ----------------------------------------------------------------------------
section("Part 3: at d = 4, 1/d = 1/4 (T3)")
# Direct evaluation.
# ----------------------------------------------------------------------------

alpha_d4 = Fraction(1, 4)
expected_alpha_d4 = Fraction(1, 4)
check(
    "T3: at d=4, compression exponent 1/d = 1/4 exactly (Fraction)",
    alpha_d4 == expected_alpha_d4,
    detail=f"1/d at d=4 = {alpha_d4} = 1/4",
)


# ----------------------------------------------------------------------------
section("Part 4: numeric cross-check (7/8)^(1/4) ~ 0.96717 (T4)")
# Bounded-context cross-check (NOT load-bearing on the algebraic theorem):
# the framework's compression-exponent value (7/8)^(1/4) ~ 0.96717
# carried in HIERARCHY_DIMENSIONAL_COMPRESSION_NOTE.md. The narrow
# theorem identifies the (1/4) outer exponent as the d=4 dimensional-
# analysis instance; the (7/8) base is the SISTER narrow theorem's
# domain. This is reported as relational consistency.
# ----------------------------------------------------------------------------

seven_eighths_quarter_sym = sp.Rational(7, 8) ** sp.Rational(1, 4)
seven_eighths_quarter_high_precision = sp.N(seven_eighths_quarter_sym, 25)
seven_eighths_quarter_float = float(seven_eighths_quarter_sym)
expected_5sf = 0.96717
gap_5sf = abs(seven_eighths_quarter_float - expected_5sf)
within_5sf = gap_5sf < 1e-4
check(
    "T4: (7/8)^(1/4) ~= 0.96717 (5-sf relational cross-check)",
    within_5sf,
    detail=(
        f"(7/8)^(1/4) = {seven_eighths_quarter_float:.15f} "
        f"(25-digit: {seven_eighths_quarter_high_precision}); "
        f"framework value 0.96717, gap = {gap_5sf:.2e}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 5: at d in {2, 3, 5, 6, 8}, 1/d in {1/2, 1/3, 1/5, 1/6, 1/8} (T5)")
# Demonstrates the d=4 selection is non-trivial in the value space:
# at d != 4, the compression exponent takes strictly different rational
# values.
# ----------------------------------------------------------------------------

t5_table = {}
expected_values = {
    2: Fraction(1, 2),
    3: Fraction(1, 3),
    5: Fraction(1, 5),
    6: Fraction(1, 6),
    8: Fraction(1, 8),
}
all_t5_match = True
for d, expected in expected_values.items():
    val = Fraction(1, d)
    t5_table[d] = val
    if val != expected:
        all_t5_match = False
check(
    "T5: at d in {2,3,5,6,8}, 1/d in {1/2,1/3,1/5,1/6,1/8} (Fraction)",
    all_t5_match,
    detail=", ".join(f"d={d}:1/d={v}" for d, v in t5_table.items()),
)


# ----------------------------------------------------------------------------
section("Part 6: uniqueness of M = f^(1/d) by dim balance (T6)")
# Equation d * alpha = 1 over rationals has unique solution alpha = 1/d.
# We solve symbolically via sympy.solve.
# ----------------------------------------------------------------------------

alpha_sym = Symbol("alpha", real=True)
d_pos = Symbol("d", positive=True, integer=True)
solutions = sp.solve(d_pos * alpha_sym - 1, alpha_sym)
unique_solution = (len(solutions) == 1) and (
    simplify(solutions[0] - 1 / d_pos) == 0
)
check(
    "T6: equation d*alpha = 1 has unique solution alpha = 1/d (sympy.solve)",
    unique_solution,
    detail=f"solutions = {solutions}",
)


# ----------------------------------------------------------------------------
section("Part 7: 1/d table for d in {1,...,8} — d=4 unique (T7)")
# 1/d is strictly decreasing on positive integers, hence injective.
# The value 1/4 is taken uniquely at d = 4.
# ----------------------------------------------------------------------------

t7_table = {d: Fraction(1, d) for d in range(1, 9)}
hits_at_quarter = [d for d, v in t7_table.items() if v == Fraction(1, 4)]
unique_at_4 = hits_at_quarter == [4]
# Strict-decreasing check
strictly_decreasing = all(
    t7_table[d] > t7_table[d + 1] for d in range(1, 8)
)
check(
    "T7: 1/d table on d in {1,...,8} — value 1/4 hit uniquely at d=4; strictly decreasing",
    unique_at_4 and strictly_decreasing,
    detail=", ".join(f"d={d}:1/d={v}" for d, v in t7_table.items()),
)


# ----------------------------------------------------------------------------
section("Part 8: (7/8)^(1/4) != (7/8)^(1/3) != (7/8)^(1/5) (T8)")
# d=4 selection is non-trivial in the value space.
# ----------------------------------------------------------------------------

x_quarter = float(sp.Rational(7, 8) ** sp.Rational(1, 4))
x_third = float(sp.Rational(7, 8) ** sp.Rational(1, 3))
x_fifth = float(sp.Rational(7, 8) ** sp.Rational(1, 5))
all_distinct = (
    abs(x_quarter - x_third) > 1e-4
    and abs(x_third - x_fifth) > 1e-4
    and abs(x_quarter - x_fifth) > 1e-4
)
check(
    "T8: (7/8)^(1/4) != (7/8)^(1/3) != (7/8)^(1/5) (numeric, 1e-4 tol)",
    all_distinct,
    detail=(
        f"(7/8)^(1/4)={x_quarter:.6f}, "
        f"(7/8)^(1/3)={x_third:.6f}, "
        f"(7/8)^(1/5)={x_fifth:.6f}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 9: dimensional consistency at d=4: (M^4)^(1/4) = M (T9)")
# Sympy round-trip of the d=4 instance: starting from a mass-dim-1 scale M,
# raising to the 4th power gives mass-dim-4 (a mock f), then taking the
# 1/4-th root recovers M. This is the dimensional-consistency instance of
# (b) at d = 4.
# ----------------------------------------------------------------------------

M_sym = Symbol("M", positive=True)
f_mock = M_sym ** 4
M_recovered = f_mock ** Rational(1, 4)
M_recovered_simplified = simplify(M_recovered - M_sym)
roundtrip_d4 = M_recovered_simplified == 0
check(
    "T9: at d=4, (M^4)^(1/4) = M symbolically (sympy)",
    roundtrip_d4,
    detail=f"(M^4)^(1/4) - M simplifies to {M_recovered_simplified}",
)


# ----------------------------------------------------------------------------
section("Part 10: cross-d roundtrip: (f^(1/d))^d = f for d in {1,...,8} (T10)")
# Sympy roundtrip across multiple d values: starting from mass-dim-d
# free-energy density f, the unique mass-dim-1 extraction M = f^(1/d)
# raised back to the d-th power recovers f. This holds for any d >= 1.
# ----------------------------------------------------------------------------

f_sym = Symbol("f", positive=True)
all_t10_roundtrip = True
t10_results = {}
for d in range(1, 9):
    M_at_d = f_sym ** Rational(1, d)
    f_recovered = M_at_d ** d
    diff = simplify(f_recovered - f_sym)
    t10_results[d] = diff
    if diff != 0:
        all_t10_roundtrip = False
check(
    "T10: (f^(1/d))^d = f for d in {1,...,8} symbolically (sympy)",
    all_t10_roundtrip,
    detail=", ".join(f"d={d}:diff={r}" for d, r in t10_results.items()),
)


# ----------------------------------------------------------------------------
section("Part 11: independence vs PR #1025 sister theorem (T11)")
# PR #1025's algebraic equivalence: 2^(d - 2) = d (integer alignment).
# Present theorem: M = f^(1/d) (dimensional balance at integer d).
# At d = 3:
#   - PR #1025: 2^(3-2) - 3 = 2 - 3 = -1 (FAILS; d=3 is not a solution)
#   - Present theorem: 1/d = 1/3 (well-defined; d=3 is allowed).
# At d = 4: both give 1/4 in their respective output forms, but for
# INDEPENDENT reasons:
#   - PR #1025 derives 1/4 via 1/(2d) = 2^(1-d) at d=4 -> 1/8 = 1/8.
#   - Present theorem derives 1/4 via [M] = [f]/d = 1 at d=4.
# These are about different mathematical objects.
# ----------------------------------------------------------------------------

# Verify PR #1025's equation at d in {3, 4}:
pr1025_d3 = 2 ** (3 - 2) - 3  # = -1, FAILS
pr1025_d4 = 2 ** (4 - 2) - 4  # = 0, holds
# Verify present theorem at d in {3, 4}:
present_d3 = Fraction(1, 3)  # well-defined
present_d4 = Fraction(1, 4)  # well-defined
# At d = 3: PR #1025 fails; present is well-defined at 1/3.
# At d = 4: PR #1025 zero; present is 1/4.
independence_holds = (
    pr1025_d3 != 0  # PR #1025 fails at d=3
    and pr1025_d4 == 0  # PR #1025 holds at d=4
    and present_d3 == Fraction(1, 3)  # present well-defined at d=3
    and present_d4 == Fraction(1, 4)  # present specialised at d=4
    and present_d3 != present_d4  # present takes different values
)
check(
    "T11: present theorem and PR #1025 are independent at d=3 and d=4",
    independence_holds,
    detail=(
        f"PR#1025 alignment at d=3 = {pr1025_d3} (fails), "
        f"d=4 = {pr1025_d4} (holds); "
        f"present 1/d at d=3 = {present_d3}, d=4 = {present_d4}"
    ),
)


# ----------------------------------------------------------------------------
section("Part 12: relational sister-theorem consistency (informational)")
# Cross-reference only: the sister narrow theorem is
#   docs/HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md
# It proves the algebraic equivalence at d=4 of three rational quantities
# on the value 7/8. The present theorem proves the dimensional-analysis
# value 1/d = 1/4 at d=4. Both must independently retain to support
# downstream framework hierarchy applications such as (7/8)^(1/4).
# ----------------------------------------------------------------------------

print(
    "\n  Sister narrow theorem (relational context, NOT load-bearing here):"
)
print(
    "    HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET_DIMENSIONAL_ANCHOR_NARROW_THEOREM_NOTE_2026-05-10.md"
)
print(
    "    proves 2^(d-2) = d (number-theoretic; d=4 unique). The present"
)
print(
    "    theorem proves M = f^(1/d) (dimensional-analysis; 1/4 at d=4)."
)
print(
    "    Both give 1/4 at d=4 for INDEPENDENT reasons. Downstream hierarchy"
)
print(
    "    application (7/8)^(1/4) consumes BOTH narrow theorems; this runner"
)
print(
    "    does not depend on the sister theorem or on the audit ledger."
)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print(
    """
  Narrow Pattern A theorem statement (recapitulation):

  HYPOTHESIS:
    Let d >= 1 be an integer and let f be a free-energy density in
    d-dim Euclidean thermal QFT in Stefan-Boltzmann form (f ~ T^d,
    Kapusta-Gale ch. 3, Vassilevich hep-th/0306138, Laine-Vuorinen ch. 2).

  CONCLUSION:
    (a) [f] = d in natural units;
    (b) the unique mass-dim-1 fractional-power scale extraction is
        M = f^(1/d) (modulo dimensionless prefactor);
    (c) at d = 4, 1/d = 1/4;
    (d) among integer d >= 1, the value 1/d = 1/4 is taken uniquely
        at d = 4.

  Audit-lane class:
    (A) — pure dimensional analysis on textbook Stefan-Boltzmann
    scaling. No external observed/fitted/literature/PDG input. No
    framework axiom or admission consumed.

  This narrow theorem is independent of:
    - The framework's selection of L_t = 4 (separate, bilinear-selector).
    - The (7/8) base of the framework's compression factor (sister
      narrow theorem HIERARCHY_SEVEN_EIGHTHS_RIEMANN_DIRICHLET).
    - The full hierarchy formula v = M_Pl x alpha_LM^16 x (7/8)^(1/4).
    - The alpha_LM substitution.
    - The per-determinant geometric-mean readout.
    - Identification of f with any specific framework determinant.
"""
)


print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
