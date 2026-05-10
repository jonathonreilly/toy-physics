#!/usr/bin/env python3
"""Pattern A narrow runner for `WOLFENSTEIN_LAMBDA_A_PRODUCT_CANCELLATION_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone symbolic-cancellation identity:

  GIVEN the two parametric input definitions on abstract positive symbols
      lambda^2  =  alpha_s / n_pair,                                   (W1)
      A^2       =  n_pair  / n_color,                                  (W2)
  THEN the following exact symbolic reductions hold:
      (T1) A^2 lambda^2     =  alpha_s / n_color,                      (W3)
      (T2) (n_pair / n_color) * (1 / n_pair)  =  1 / n_color           (R1)
           [pure rational lemma; underlies (T1) cancellation],
      (T3) |V_cb|^2 = A^2 lambda^4  =  alpha_s^2 / (n_pair * n_color)
                                  =  alpha_s^2 / n_quark,              (V1)
      (T4) the cancellation closes for arbitrary positive count tuples;
           the framework instance (n_pair, n_color, n_quark) = (2, 3, 6)
           and an alternative instance (5, 7, 35) both satisfy the same
           exact symbolic reductions.

This narrow theorem treats (alpha_s, n_pair, n_color) as ABSTRACT
POSITIVE SYMBOLS and (lambda, A) as derived positive symbols defined by
(W1)+(W2). It does not derive (W1) or (W2); it does not import any
specific value of alpha_s; it does not consume any Wolfenstein/atlas/
CP-phase/native-gauge/graph-first-SU3 authority; it does not claim any
physical-CKM identification, any PDG comparator, or any framework-
specific (n_pair, n_color) = (2, 3) assignment as load-bearing.

The narrow theorem can be applied to ANY abstract positive count tuple
satisfying the two input parametric identities; the framework instance
(2, 3, 6) and the alternative (5, 7, 35) are concrete sanity cases
shown for closure on arbitrary count tuples.

Companion role: not a new audit-companion; this is a Pattern A new narrow
claim row carving out the symbolic-cancellation core of the existing
`wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24`.
"""

from __future__ import annotations

from fractions import Fraction
import sys

try:
    import sympy
    from sympy import Rational, simplify, sqrt, symbols
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: Wolfenstein lambda-A product cancellation")
# Statement: (W1)+(W2) imply (W3) by pure symbolic algebra.
# Pure algebraic-cancellation lemma on abstract positive symbols.
# No CKM-physical claim, no upstream authority, no PDG comparator.
# ============================================================================

# Abstract positive symbols.
alpha_s, n_pair, n_color = symbols(
    "alpha_s n_pair n_color", positive=True, real=True
)

# Input parametric definitions (treated as hypotheses; not derived here).
lambda_sq = alpha_s / n_pair
a_sq = n_pair / n_color

# Derived positive amplitudes (positive square roots).
lambda_sym = sqrt(lambda_sq)
a_sym = sqrt(a_sq)

# Auxiliary count.
n_quark = n_pair * n_color


# ----------------------------------------------------------------------------
section("Part 0: input parametric identities (hypotheses, not derived)")
# ----------------------------------------------------------------------------
print(f"  lambda^2  =  {lambda_sq}    (W1; alpha_s / n_pair)")
print(f"  A^2       =  {a_sq}        (W2; n_pair / n_color)")
print(f"  n_quark   =  {n_quark}      (auxiliary; n_pair * n_color)")

check(
    "(W1) lambda^2 = alpha_s / n_pair as input parametric definition",
    simplify(lambda_sq - alpha_s / n_pair) == 0,
    detail="trivial accept of input identity",
)
check(
    "(W2) A^2 = n_pair / n_color as input parametric definition",
    simplify(a_sq - n_pair / n_color) == 0,
    detail="trivial accept of input identity",
)


# ----------------------------------------------------------------------------
section("Part 1: (T1) symbolic cancellation A^2 lambda^2 = alpha_s / n_color")
# ----------------------------------------------------------------------------
# A^2 * lambda^2 = (n_pair / n_color) * (alpha_s / n_pair)
#                = alpha_s * n_pair / (n_color * n_pair)
#                = alpha_s / n_color    [n_pair cancels exactly]
product = a_sq * lambda_sq
expected_T1 = alpha_s / n_color
residual_T1 = simplify(product - expected_T1)
print(f"\n  product simplified  =  {simplify(product)}")
print(f"  expected            =  {expected_T1}")

check(
    "(T1) A^2 lambda^2 = alpha_s / n_color  [n_pair cancels exactly]",
    residual_T1 == 0,
    detail=f"residual = {residual_T1}",
)


# ----------------------------------------------------------------------------
section("Part 2: (T2) rational-cancellation lemma (n_pair/n_color)*(1/n_pair) = 1/n_color")
# ----------------------------------------------------------------------------
# Symbolic statement on abstract positive (n_pair, n_color).
sym_lemma = (n_pair / n_color) * (1 / n_pair) - 1 / n_color
res_T2_sym = simplify(sym_lemma)
check(
    "(T2-sym) (n_pair/n_color)*(1/n_pair) - 1/n_color = 0 on abstract positive symbols",
    res_T2_sym == 0,
    detail=f"residual = {res_T2_sym}",
)

# Pure rational instance check (Fraction): for several (p, c) pairs with p, c != 0.
for p_val, c_val in [(2, 3), (5, 7), (11, 13), (1, 2), (4, 9), (7, 11)]:
    rat_residual = Fraction(p_val, c_val) * Fraction(1, p_val) - Fraction(1, c_val)
    check(
        f"(T2-rational) (n_pair/n_color)*(1/n_pair) - 1/n_color = 0 at (n_pair, n_color) = ({p_val}, {c_val})",
        rat_residual == 0,
        detail=f"residual = {rat_residual}",
    )


# ----------------------------------------------------------------------------
section("Part 3: (T3) |V_cb|^2 = alpha_s^2 / n_quark squared-magnitude corollary")
# ----------------------------------------------------------------------------
# |V_cb|^2 = A^2 lambda^4 = (n_pair/n_color) * (alpha_s/n_pair)^2
#         = alpha_s^2 / (n_color * n_pair)
#         = alpha_s^2 / n_quark
v_cb_sq = a_sq * lambda_sq ** 2
v_cb_sq_clean = alpha_s ** 2 / n_quark
v_cb_sq_explicit = alpha_s ** 2 / (n_pair * n_color)
res_V1_general = simplify(v_cb_sq - v_cb_sq_clean)
res_V1_explicit = simplify(v_cb_sq - v_cb_sq_explicit)

print(f"\n  |V_cb|^2 simplified  =  {simplify(v_cb_sq)}")
print(f"  alpha_s^2 / n_quark  =  {v_cb_sq_clean}")

check(
    "(T3) |V_cb|^2 = A^2 lambda^4 = alpha_s^2 / n_quark  [squared identity, no radicals]",
    res_V1_general == 0,
    detail=f"residual = {res_V1_general}",
)
check(
    "(T3) |V_cb|^2 = alpha_s^2 / (n_pair * n_color) [explicit factorization]",
    res_V1_explicit == 0,
    detail=f"residual = {res_V1_explicit}",
)

# Positive-amplitude form: |V_cb| = A lambda^2 = alpha_s / sqrt(n_quark).
v_cb = a_sym * lambda_sq
v_cb_clean = alpha_s / sqrt(n_quark)
res_V1_amp = simplify(v_cb - v_cb_clean)
check(
    "(T3) |V_cb| = A lambda^2 = alpha_s / sqrt(n_quark)  [positive amplitude]",
    res_V1_amp == 0,
    detail=f"residual = {res_V1_amp}",
)


# ----------------------------------------------------------------------------
section("Part 4: (T4) closure on framework instance (n_pair, n_color, n_quark) = (2, 3, 6)")
# ----------------------------------------------------------------------------
# Special case shown for sanity, NOT load-bearing on the cancellation.
sub_framework = {n_pair: Rational(2), n_color: Rational(3)}

product_2_3 = simplify(product.subs(sub_framework))
expected_2_3 = alpha_s / 3
check(
    "(2, 3, 6) framework instance: A^2 lambda^2 = alpha_s / 3",
    simplify(product_2_3 - expected_2_3) == 0,
    detail=f"product = {product_2_3}",
)

v_cb_sq_2_3 = simplify(v_cb_sq.subs(sub_framework))
expected_v_cb_sq_2_3 = alpha_s ** 2 / 6
check(
    "(2, 3, 6) framework instance: |V_cb|^2 = alpha_s^2 / 6",
    simplify(v_cb_sq_2_3 - expected_v_cb_sq_2_3) == 0,
    detail=f"|V_cb|^2 = {v_cb_sq_2_3}",
)

v_cb_2_3 = simplify(v_cb.subs(sub_framework))
expected_v_cb_2_3 = alpha_s / sqrt(6)
check(
    "(2, 3, 6) framework instance: |V_cb| = alpha_s / sqrt(6)",
    simplify(v_cb_2_3 - expected_v_cb_2_3) == 0,
    detail=f"|V_cb| = {v_cb_2_3}",
)


# ----------------------------------------------------------------------------
section("Part 5: (T4) closure on alternative instance (n_pair, n_color, n_quark) = (5, 7, 35)")
# ----------------------------------------------------------------------------
# Alternative case showing the cancellation is independent of the framework's
# integer choice; the same algebra works for any positive (n_pair, n_color).
sub_alt = {n_pair: Rational(5), n_color: Rational(7)}

product_5_7 = simplify(product.subs(sub_alt))
expected_5_7 = alpha_s / 7
check(
    "(5, 7, 35) alternative instance: A^2 lambda^2 = alpha_s / 7",
    simplify(product_5_7 - expected_5_7) == 0,
    detail=f"product = {product_5_7}",
)

v_cb_sq_5_7 = simplify(v_cb_sq.subs(sub_alt))
expected_v_cb_sq_5_7 = alpha_s ** 2 / 35
check(
    "(5, 7, 35) alternative instance: |V_cb|^2 = alpha_s^2 / 35",
    simplify(v_cb_sq_5_7 - expected_v_cb_sq_5_7) == 0,
    detail=f"|V_cb|^2 = {v_cb_sq_5_7}",
)

v_cb_5_7 = simplify(v_cb.subs(sub_alt))
expected_v_cb_5_7 = alpha_s / sqrt(35)
check(
    "(5, 7, 35) alternative instance: |V_cb| = alpha_s / sqrt(35)",
    simplify(v_cb_5_7 - expected_v_cb_5_7) == 0,
    detail=f"|V_cb| = {v_cb_5_7}",
)


# ----------------------------------------------------------------------------
section("Part 6: alpha_s independence (cancellation is alpha_s-agnostic)")
# ----------------------------------------------------------------------------
# Substituting alpha_s -> any positive value preserves the cancellation
# structure. The cancellation is purely a fact of the (n_pair / n_color) *
# (alpha_s / n_pair) -> (alpha_s / n_color) reduction.

for alpha_s_val_label, alpha_s_val in [
    ("a_s", Rational(1, 10)),  # arbitrary positive rational
    ("a_s = 1", Rational(1)),
    ("a_s = 7/13", Rational(7, 13)),
]:
    # With a fixed alpha_s, the (W3) cancellation still holds symbolically
    # in (n_pair, n_color).
    product_a = simplify(product.subs(alpha_s, alpha_s_val))
    expected_a = alpha_s_val / n_color
    check(
        f"(T1) alpha_s independence: A^2 lambda^2 = {alpha_s_val} / n_color at alpha_s = {alpha_s_val}",
        simplify(product_a - expected_a) == 0,
        detail=f"product = {product_a}",
    )


# ----------------------------------------------------------------------------
section("Part 7: explicit demonstration that the cancellation is the n_pair factor")
# ----------------------------------------------------------------------------
# Show A^2 lambda^2 = alpha_s * (n_pair / (n_color * n_pair)) = alpha_s / n_color
# step-by-step, isolating the n_pair / n_pair = 1 cancellation.
intermediate = alpha_s * n_pair / (n_color * n_pair)
res_explicit = simplify(intermediate - alpha_s / n_color)
check(
    "explicit cancellation: alpha_s * n_pair / (n_color * n_pair) - alpha_s / n_color = 0",
    res_explicit == 0,
    detail=f"residual = {res_explicit}",
)

# Demonstrate that in a SINGLE simplify call, sympy reduces (n_pair/n_color)*(alpha_s/n_pair)
# to alpha_s / n_color, confirming the cancellation is a sympy-canonical reduction
# rather than an artifact of a specific manipulation order.
direct = (n_pair / n_color) * (alpha_s / n_pair)
direct_simplified = simplify(direct)
check(
    "direct reduction: simplify((n_pair/n_color)*(alpha_s/n_pair)) = alpha_s / n_color",
    simplify(direct_simplified - alpha_s / n_color) == 0,
    detail=f"simplified = {direct_simplified}",
)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESES (input parametric definitions on abstract positive symbols):
      lambda^2  =  alpha_s / n_pair                   (W1)
      A^2       =  n_pair  / n_color                  (W2)
      with (alpha_s, n_pair, n_color) abstract positive real symbols.

  CONCLUSION (symbolic cancellation):
      A^2 lambda^2  =  alpha_s / n_color              (W3, T1)
      [the n_pair factor cancels by pure rational algebra]

      Underlying lemma:
          (n_pair / n_color) * (1 / n_pair)  =  1 / n_color   (R1, T2)

      Squared-magnitude corollary:
          |V_cb|^2 = A^2 lambda^4  =  alpha_s^2 / n_quark     (V1, T3)
          where n_quark = n_pair * n_color.

      Closure on arbitrary count tuples (T4):
          (n_pair, n_color, n_quark) = (2, 3, 6) gives A^2 lambda^2 = alpha_s/3,
          (n_pair, n_color, n_quark) = (5, 7, 35) gives A^2 lambda^2 = alpha_s/7.

  Audit-lane class:
    (A) -- pure symbolic-cancellation algebra over abstract positive symbols.
    No external observed/fitted/literature input. No physical-CKM
    identification, no PDG comparator. The framework-specific
    (n_pair, n_color) = (2, 3) instance is a concrete sanity case, not a
    load-bearing input.

  The narrow theorem drops the parent row's dependencies on
  CKM_ATLAS_AXIOM_CLOSURE, NATIVE_GAUGE_CLOSURE, GRAPH_FIRST_SU3_INTEGRATION,
  ALPHA_S_DERIVED, and CKM_CP_PHASE_STRUCTURAL_IDENTITY by stating the two
  input parametric identities (W1) and (W2) as hypotheses on abstract
  positive symbols.
""")


print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
