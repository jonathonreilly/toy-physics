#!/usr/bin/env python3
"""Audit-companion exact-symbolic runner for
`ckm_nlo_barred_triangle_protected_gamma_theorem_note_2026-04-25`.

The parent note's load-bearing structural claim is the **protection
identity**:

    at NLO Wolfenstein,   gamma_bar  ==  gamma_0,

i.e. the apex-from-origin angle of the barred unitarity triangle is
exactly preserved by the NLO multiplicative scaling
`(rho_bar + i eta_bar) = (rho + i eta)(1 - lambda^2/2)`.

The mechanism is structural: under the NLO multiplicative-scaling
premise, both `rho_bar` and `eta_bar` are rescaled by the SAME real
positive factor `(1 - lambda^2/2)`, so the ratio `eta_bar / rho_bar`
is invariant under the scaling, and the apex argument
`arg(rho_bar + i eta_bar)` is preserved.

This companion verifies the protection identity at sympy `Rational`
exact precision and also derives the closed-form NLO catalog
`(N1)`-`(N9)` symbolically. Concretely it shows:

  (P0)  the abstract structural protection identity
        tan(gamma_bar)(rho, eta, lambda^2) - tan(gamma_0)(rho, eta) == 0
        as a polynomial identity in symbolic (rho, eta, lambda^2);

  (P1)  the framework-counts protection identity with retained
        (rho, eta) = (1/6, sqrt(5)/6) and lambda^2 = alpha_s/2:
        tan(gamma_bar) - sqrt(5) == 0 as a Rational identity in alpha_s;

  (N1)-(N9)  the catalog closed forms in the parent's Statement
             section, all simplified to canonical form symbolically;

  (LO)  alpha_s -> 0 recovery of the atlas-leading right-angle triangle.

Companion role: exact-precision verification of the parent's
load-bearing protection identity and its closed-form NLO catalog.
This companion does NOT introduce a new claim row, a new source note,
or any modification of the parent row's status. It only verifies the
local algebraic content; independent audit retains responsibility for
the parent row and its upstream authorities.
"""

import sys

try:
    import sympy
    from sympy import (
        Rational,
        Symbol,
        sqrt,
        atan,
        sin,
        cos,
        tan,
        simplify,
        expand,
        cancel,
        together,
        factor,
        symbols,
        pi,
        series,
        limit,
        nsimplify,
        N,
        S,
    )
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{tag}] {label}{suffix}")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


print("=" * 88)
print("Audit companion (exact symbolic): ckm_nlo_barred_triangle_protected_gamma")
print("See docs/CKM_NLO_BARRED_TRIANGLE_PROTECTED_GAMMA_THEOREM_NOTE_2026-04-25.md")
print("=" * 88)


# ============================================================================
section("Part 0: structural protection identity in abstract (rho, eta, lam2)")
# Goal: show the protection identity holds in the most general form
# allowed by the parent's NLO multiplicative-scaling premise, with
# (rho, eta) and lambda^2 ('lam2') treated as free symbols. This is the
# CORE structural content of the protection theorem: NO substitution of
# specific apex coordinates or coupling values is required.
# ============================================================================

rho_s = Symbol('rho', real=True)
eta_s = Symbol('eta', real=True)
lam2 = Symbol('lam2', real=True, nonnegative=True)  # lambda^2

# NLO multiplicative-scaling map from parent note Statement and Cited Inputs:
#     rho_bar + i eta_bar = (rho + i eta) (1 - lam2/2)
# Splitting real/imaginary, with the scale factor being purely real:
nlo_scale = 1 - lam2 / 2
rho_bar_sym = rho_s * nlo_scale
eta_bar_sym = eta_s * nlo_scale

# Protection identity (P0): the apex argument is preserved.
# tan(gamma_bar) := eta_bar / rho_bar; tan(gamma_0) := eta / rho.
# The scaling factor cancels exactly because it is the same real factor
# in numerator and denominator.
tan_gamma_bar_abstract = simplify(eta_bar_sym / rho_bar_sym)
tan_gamma_0_abstract = eta_s / rho_s
diff_abstract = simplify(tan_gamma_bar_abstract - tan_gamma_0_abstract)

check(
    "(P0) abstract protection: tan(gamma_bar) == tan(gamma_0) for all (rho, eta, lam2)",
    diff_abstract == 0,
    detail=f"simplify(diff) = {diff_abstract}",
)

# Stronger restatement: the apex argument is preserved as a polynomial
# identity in the scale factor. We re-express by clearing denominators:
# tan(gamma_bar) * rho - eta == 0  identically.
poly_form = simplify(tan_gamma_bar_abstract * rho_s - eta_s)
check(
    "(P0') polynomial form: tan(gamma_bar) * rho - eta == 0 identically",
    poly_form == 0,
    detail=f"simplify = {poly_form}",
)

# Mechanism cross-check: the cancellation is exactly the (1 - lam2/2)
# factor in numerator and denominator. We display the unsimplified
# ratio (eta * factor) / (rho * factor) = eta/rho once factor cancels.
unsimpl = (eta_s * nlo_scale) / (rho_s * nlo_scale)
canceled = cancel(unsimpl)
check(
    "(P0'') mechanism: (eta * (1-lam2/2)) / (rho * (1-lam2/2)) cancels to eta/rho",
    simplify(canceled - eta_s / rho_s) == 0,
    detail=f"cancel = {canceled}",
)

# Independent argument-of-complex-product proof: arg(z * w) = arg(z) +
# arg(w) for any nonzero w; here w = (1 - lam2/2) is a positive real
# (for lam2 in (0, 2)), so arg(w) = 0. Therefore
# arg(rho_bar + i eta_bar) = arg(rho + i eta).
# We capture this algebraically: the imaginary parts and real parts
# scale by the SAME real factor, so any homogeneous-degree-zero
# function of (Re, Im) is invariant. tan(arg) = Im/Re is one such.
check(
    "(P0''') homogeneity: real positive scaling preserves Im/Re ratio",
    simplify(eta_bar_sym * rho_s - rho_bar_sym * eta_s) == 0,
    detail="Im(z')*Re(z) - Re(z')*Im(z) = 0 (the scaling factor commutes)",
)


# ============================================================================
section("Part 1: framework retained inputs and (P1) protection identity")
# Goal: instantiate the abstract protection identity with the retained
# atlas apex coordinates (rho, eta) = (1/6, sqrt(5)/6) and the retained
# Wolfenstein lambda^2 = alpha_s/2, then verify that
# tan(gamma_bar) - sqrt(5) == 0 holds as a Rational+sqrt identity in
# alpha_s.
# ============================================================================

alpha = Symbol('alpha_s', real=True, nonnegative=True)
rho_fw = Rational(1, 6)
eta_fw = sqrt(5) / 6
lam2_fw = alpha / 2

# Substitute into the abstract apex maps.
rho_bar_fw = simplify(rho_bar_sym.subs({rho_s: rho_fw, eta_s: eta_fw, lam2: lam2_fw}))
eta_bar_fw = simplify(eta_bar_sym.subs({rho_s: rho_fw, eta_s: eta_fw, lam2: lam2_fw}))

# (N1) closed form: rho_bar = (4 - alpha_s)/24
n1_target = (4 - alpha) / 24
check(
    "(N1) rho_bar = (4 - alpha_s)/24",
    simplify(rho_bar_fw - n1_target) == 0,
    detail=f"rho_bar = {rho_bar_fw}",
)

# (N2) closed form: eta_bar = sqrt(5)(4 - alpha_s)/24
n2_target = sqrt(5) * (4 - alpha) / 24
check(
    "(N2) eta_bar = sqrt(5)(4 - alpha_s)/24",
    simplify(eta_bar_fw - n2_target) == 0,
    detail=f"eta_bar = {eta_bar_fw}",
)

# (N3) closed form: rho_bar^2 + eta_bar^2 = (4 - alpha_s)^2 / 96
n3_target = (4 - alpha) ** 2 / 96
n3_lhs = simplify(rho_bar_fw ** 2 + eta_bar_fw ** 2)
check(
    "(N3) rho_bar^2 + eta_bar^2 = (4 - alpha_s)^2 / 96",
    simplify(n3_lhs - n3_target) == 0,
    detail=f"|apex|^2 = {n3_lhs}",
)

# (N4) PROTECTED protection identity at framework counts.
# tan(gamma_bar) = eta_bar / rho_bar should reduce to sqrt(5) as a
# Rational+sqrt identity in alpha_s.
tan_gamma_bar_fw = simplify(eta_bar_fw / rho_bar_fw)
check(
    "(N4) tan(gamma_bar) = sqrt(5) [PROTECTED identity at framework counts]",
    simplify(tan_gamma_bar_fw - sqrt(5)) == 0,
    detail=f"tan(gamma_bar) = {tan_gamma_bar_fw}",
)

# (P1) the protection identity holds for ALL alpha_s in [0, 2]:
# tan(gamma_bar)(alpha_s) - tan(gamma_0) is the zero polynomial in alpha_s.
delta_protection = simplify(tan_gamma_bar_fw - sqrt(5))
check(
    "(P1) protection holds for all alpha_s: tan(gamma_bar) - sqrt(5) == 0",
    delta_protection == 0,
    detail=f"delta = {delta_protection}",
)


# ============================================================================
section("Part 2: (N5) closed form for tan(beta_bar)")
# Goal: tan(beta_bar) = eta_bar / (1 - rho_bar)
#                   = sqrt(5)(4 - alpha_s) / (20 + alpha_s)
# as a Rational+sqrt identity in alpha_s.
# ============================================================================

one_minus_rho_bar = simplify(1 - rho_bar_fw)
# Should equal (20 + alpha_s)/24
check(
    "1 - rho_bar = (20 + alpha_s)/24",
    simplify(one_minus_rho_bar - (20 + alpha) / 24) == 0,
    detail=f"1 - rho_bar = {one_minus_rho_bar}",
)

tan_beta_bar = simplify(eta_bar_fw / one_minus_rho_bar)
n5_target = sqrt(5) * (4 - alpha) / (20 + alpha)
check(
    "(N5) tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s)",
    simplify(tan_beta_bar - n5_target) == 0,
    detail=f"tan(beta_bar) = {tan_beta_bar}",
)


# ============================================================================
section("Part 3: (N6), (N7) alpha_bar and linear deviation")
# Goal: alpha_bar = pi - gamma_0 - beta_bar (triangle constraint with
# protection identity), and the linear-in-alpha_s deviation theorem
#   alpha_bar - pi/2 = (sqrt(5)/20) alpha_s + O(alpha_s^2).
# ============================================================================

# Define gamma_0 = arctan(sqrt(5)).  We treat gamma_0 as a sympy atan.
gamma_0 = atan(sqrt(5))
beta_0 = atan(1 / sqrt(5))

# Atlas right-angle: gamma_0 + beta_0 = pi/2.
# Algebraic mechanism: with t1 = sqrt(5), t2 = 1/sqrt(5), t1*t2 = 1, so
# tan(gamma_0 + beta_0) = (t1 + t2)/(1 - t1 t2) is undefined (division
# by zero). Both gamma_0 and beta_0 are in (0, pi/2), and the sum lies
# in (0, pi), so the only possibility is gamma_0 + beta_0 = pi/2.
# We capture the algebra via the cotangent identity: cot(gamma_0) =
# 1/sqrt(5) = tan(beta_0), so gamma_0 = pi/2 - beta_0.
cot_gamma_0 = 1 / tan(gamma_0)            # 1/sqrt(5)
tan_beta_0 = tan(beta_0)                  # 1/sqrt(5)
check(
    "cot(gamma_0) = tan(beta_0) (=> gamma_0 + beta_0 = pi/2 algebraically)",
    simplify(cot_gamma_0 - tan_beta_0) == 0,
    detail=f"cot(gamma_0) = {simplify(cot_gamma_0)}, tan(beta_0) = {simplify(tan_beta_0)}",
)
# Numerical confirmation as a finite-precision sanity check:
right_angle_num = float(N(gamma_0 + beta_0 - pi / 2, 50))
check(
    "gamma_0 + beta_0 = pi/2 (atlas right angle, numerical 50 digits)",
    abs(right_angle_num) < 1e-30,
    detail=f"|sum - pi/2|_num = {right_angle_num:.3e}",
)

# beta_bar from the closed-form tan via atan.
beta_bar = atan(n5_target)
alpha_bar = pi - gamma_0 - beta_bar  # (N6)

# (N7) Series in alpha_s about alpha_s = 0: leading term should be
# (sqrt(5)/20) alpha_s.
# Method: write alpha_bar - pi/2 = (pi/2 - gamma_0) - beta_bar, and
# then use that pi/2 - gamma_0 = beta_0 (proved above algebraically) to
# get alpha_bar - pi/2 = beta_0 - beta_bar. Since beta_bar(0) = beta_0
# at alpha_s = 0 (proved in Part 6 below), the constant term of the
# series in alpha_s is exactly 0, and the linear coefficient is
# d(beta_0 - beta_bar)/d alpha_s |_0 = -d beta_bar/d alpha_s |_0.
ab_minus_pi2_via_beta = beta_0 - beta_bar
ser_via_beta = series(ab_minus_pi2_via_beta, alpha, 0, 3).removeO()
linear_coeff_via_beta = simplify(ser_via_beta.coeff(alpha, 1))
const_coeff_via_beta = simplify(ser_via_beta.coeff(alpha, 0))

n7_target_coeff = sqrt(5) / 20
check(
    "(N7) leading order of (alpha_bar - pi/2) in alpha_s = (sqrt(5)/20) alpha_s",
    simplify(linear_coeff_via_beta - n7_target_coeff) == 0,
    detail=f"coeff(alpha_s^1) = {linear_coeff_via_beta}",
)

# The constant term of (alpha_bar - pi/2) written as (beta_0 - beta_bar)
# is identically zero (no need for atan-sum identity simplification).
check(
    "(N7) constant term of (alpha_bar - pi/2) is 0 [via (beta_0 - beta_bar)]",
    simplify(const_coeff_via_beta) == 0,
    detail=f"coeff(alpha_s^0) = {const_coeff_via_beta}",
)

# Verify (N6) directly: alpha_bar = pi - gamma_0 - beta_bar.
check(
    "(N6) alpha_bar = pi - gamma_0 - beta_bar (definition)",
    simplify(alpha_bar - (pi - gamma_0 - beta_bar)) == 0,
)

# Direct cross-check of (N7) coefficient via differentiation of the
# closed form tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s):
# d tan(beta_bar) / d alpha_s = -sqrt(5) * 24 / (20 + alpha_s)^2
# at alpha_s = 0 this is -sqrt(5) * 24 / 400 = -3 sqrt(5)/50.
# d beta_bar / d alpha_s = (1/(1+t^2)) * dt/d alpha_s, at alpha_s = 0
# t = 1/sqrt(5), 1+t^2 = 6/5, so factor = 5/6.
# d beta_bar/d alpha_s |_0 = -3 sqrt(5)/50 * 5/6 = -sqrt(5)/20.
dt_dalpha = simplify(n5_target.diff(alpha))
dt_dalpha_at_0 = simplify(dt_dalpha.subs(alpha, 0))
check(
    "d tan(beta_bar)/d alpha_s |_{alpha_s=0} = -3 sqrt(5)/50",
    simplify(dt_dalpha_at_0 - (-3 * sqrt(5) / 50)) == 0,
    detail=f"dt/da|_0 = {dt_dalpha_at_0}",
)
dbeta_dalpha_at_0 = simplify(
    dt_dalpha_at_0 / (1 + n5_target.subs(alpha, 0) ** 2)
)
check(
    "d beta_bar/d alpha_s |_0 = -sqrt(5)/20  (=> alpha_bar - pi/2 has slope +sqrt(5)/20)",
    simplify(dbeta_dalpha_at_0 - (-sqrt(5) / 20)) == 0,
    detail=f"dbeta/da|_0 = {dbeta_dalpha_at_0}",
)


# ============================================================================
section("Part 4: (N8) PROTECTED doubled-angle catalog")
# Goal: sin(2 gamma_bar) = sqrt(5)/3, cos(2 gamma_bar) = -2/3, EXACTLY,
# as Rational+sqrt identities in alpha_s (independent of alpha_s by
# protection).
# ============================================================================

# Use the protection identity gamma_bar = arctan(sqrt(5)) directly, and
# evaluate sin(2 arctan(sqrt(5))) and cos(2 arctan(sqrt(5))) exactly.
# Standard identity: with t = tan(gamma), sin(2 gamma) = 2t/(1+t^2),
# cos(2 gamma) = (1-t^2)/(1+t^2).
t_gamma = sqrt(5)
sin_2g = simplify(2 * t_gamma / (1 + t_gamma ** 2))
cos_2g = simplify((1 - t_gamma ** 2) / (1 + t_gamma ** 2))

check(
    "(N8) sin(2 gamma_bar) = sqrt(5)/3 [PROTECTED]",
    simplify(sin_2g - sqrt(5) / 3) == 0,
    detail=f"sin(2 gamma_bar) = {sin_2g}",
)
check(
    "(N8) cos(2 gamma_bar) = -2/3 [PROTECTED]",
    simplify(cos_2g - Rational(-2, 3)) == 0,
    detail=f"cos(2 gamma_bar) = {cos_2g}",
)
check(
    "(N8) sin^2 + cos^2 = 1",
    simplify(sin_2g ** 2 + cos_2g ** 2 - 1) == 0,
)

# Alternative protection cross-check: derive sin(2 gamma_bar) from the
# parent's apex map directly. Using the double-angle identity
# sin(2 theta) = 2 sin(theta) cos(theta), and that for theta = arctan(t)
# with t > 0, sin(theta) = t/sqrt(1+t^2), cos(theta) = 1/sqrt(1+t^2):
sin_2g_from_apex = simplify(2 * (eta_bar_fw / sqrt(rho_bar_fw ** 2 + eta_bar_fw ** 2))
                            * (rho_bar_fw / sqrt(rho_bar_fw ** 2 + eta_bar_fw ** 2)))
check(
    "(N8') alternative: sin(2 gamma_bar) from apex = 2 rho_bar eta_bar / |apex|^2 = sqrt(5)/3",
    simplify(sin_2g_from_apex - sqrt(5) / 3) == 0,
    detail=f"sin(2 gamma_bar) from apex = {simplify(sin_2g_from_apex)}",
)

cos_2g_from_apex = simplify((rho_bar_fw ** 2 - eta_bar_fw ** 2)
                            / (rho_bar_fw ** 2 + eta_bar_fw ** 2))
check(
    "(N8') alternative: cos(2 gamma_bar) from apex = (rho^2 - eta^2)/|apex|^2 = -2/3",
    simplify(cos_2g_from_apex - Rational(-2, 3)) == 0,
    detail=f"cos(2 gamma_bar) from apex = {simplify(cos_2g_from_apex)}",
)


# ============================================================================
section("Part 5: (N9) closed forms for sin/cos(2 beta_bar)")
# Goal: with t = tan(beta_bar) = sqrt(5)(4 - alpha_s)/(20 + alpha_s),
#   sin(2 beta_bar) = 2 sqrt(5)(4-alpha_s)(20+alpha_s) / D
#   cos(2 beta_bar) = ((20+alpha_s)^2 - 5(4-alpha_s)^2) / D
# where D = (20+alpha_s)^2 + 5(4-alpha_s)^2.
# ============================================================================

t_beta = n5_target  # sqrt(5)(4 - alpha_s)/(20 + alpha_s)
sin_2b_direct = simplify(2 * t_beta / (1 + t_beta ** 2))
cos_2b_direct = simplify((1 - t_beta ** 2) / (1 + t_beta ** 2))

D_target = (20 + alpha) ** 2 + 5 * (4 - alpha) ** 2
n9_sin_target = 2 * sqrt(5) * (4 - alpha) * (20 + alpha) / D_target
n9_cos_target = ((20 + alpha) ** 2 - 5 * (4 - alpha) ** 2) / D_target

check(
    "(N9) sin(2 beta_bar) closed form",
    simplify(sin_2b_direct - n9_sin_target) == 0,
    detail=f"diff = {simplify(sin_2b_direct - n9_sin_target)}",
)
check(
    "(N9) cos(2 beta_bar) closed form",
    simplify(cos_2b_direct - n9_cos_target) == 0,
    detail=f"diff = {simplify(cos_2b_direct - n9_cos_target)}",
)
check(
    "(N9) sin^2 + cos^2 = 1 (Pythagorean check)",
    simplify(sin_2b_direct ** 2 + cos_2b_direct ** 2 - 1) == 0,
)


# ============================================================================
section("Part 6: alpha_s -> 0 LO recovery (atlas right-angle triangle)")
# Goal: at alpha_s = 0, the closed forms reduce to the atlas-leading
# right-angle triangle: rho_bar = 1/6, eta_bar = sqrt(5)/6,
# tan(beta_bar) = 1/sqrt(5), alpha_bar = pi/2.
# ============================================================================

rho_bar_LO = simplify(rho_bar_fw.subs(alpha, 0))
eta_bar_LO = simplify(eta_bar_fw.subs(alpha, 0))
tan_beta_LO = simplify(t_beta.subs(alpha, 0))

check("rho_bar(0) = 1/6", simplify(rho_bar_LO - Rational(1, 6)) == 0,
      detail=f"rho_bar(0) = {rho_bar_LO}")
check("eta_bar(0) = sqrt(5)/6", simplify(eta_bar_LO - sqrt(5) / 6) == 0,
      detail=f"eta_bar(0) = {eta_bar_LO}")
check("tan(beta_bar)(0) = 1/sqrt(5) = sqrt(5)/5",
      simplify(tan_beta_LO - 1 / sqrt(5)) == 0,
      detail=f"tan(beta_bar)(0) = {tan_beta_LO}")

# alpha_bar(0) = pi/2 is established via the (beta_0 - beta_bar) series
# constant term being 0 in Part 3 (which used the algebraic right-angle
# mechanism cot(gamma_0) = tan(beta_0) without invoking sympy's
# atan-sum identity engine).
# Direct numerical confirmation as a finite-precision sanity check:
ab_LO_num = float(N(alpha_bar.subs(alpha, 0) - pi / 2, 50))
check("alpha_bar(0) = pi/2 (atlas right angle, numerical 50 digits)",
      abs(ab_LO_num) < 1e-30,
      detail=f"|alpha_bar(0) - pi/2|_num = {ab_LO_num:.3e}")
# Algebraic restatement: alpha_bar(0) = pi - gamma_0 - beta_0; from the
# right-angle mechanism above, gamma_0 + beta_0 = pi/2, hence
# alpha_bar(0) = pi - pi/2 = pi/2. We capture this by the chain of
# algebraic identities verified earlier rather than calling simplify on
# the atan-sum directly.
beta_bar_LO = simplify(beta_bar.subs(alpha, 0))
check("beta_bar(0) = beta_0 (recovers atlas-leading angle)",
      simplify(beta_bar_LO - beta_0) == 0,
      detail=f"beta_bar(0) = {beta_bar_LO}, beta_0 = {beta_0}")


# ============================================================================
section("Part 7: structural cross-check vs related theorems")
# Goal: verify retained sin(2 beta_0) = sqrt(5)/3 (atlas-LO) and
# cos(2 beta_0) = 2/3 from the (N9) closed form at alpha_s = 0.
# ============================================================================

sin_2b_LO = simplify(sin_2b_direct.subs(alpha, 0))
cos_2b_LO = simplify(cos_2b_direct.subs(alpha, 0))
check("sin(2 beta_0) = sqrt(5)/3 (atlas-LO recovery from (N9))",
      simplify(sin_2b_LO - sqrt(5) / 3) == 0,
      detail=f"sin(2 beta_0) = {sin_2b_LO}")
check("cos(2 beta_0) = 2/3 (atlas-LO recovery from (N9))",
      simplify(cos_2b_LO - Rational(2, 3)) == 0,
      detail=f"cos(2 beta_0) = {cos_2b_LO}")

# Atlas-LO doubled-angles equal protected NLO doubled-gamma:
check("atlas-LO sin(2 beta_0) == NLO-protected sin(2 gamma_bar) (= sqrt(5)/3)",
      simplify(sin_2b_LO - sin_2g) == 0)


# ============================================================================
section("Audit-companion summary")
# ============================================================================
print("""
  This companion provides EXACT symbolic verification (via sympy) of
  the parent theorem's load-bearing protection identity and its
  closed-form NLO catalog (N1)-(N9):

    PROTECTION IDENTITY (P0): for any (rho, eta, lam2), the NLO
      multiplicative scaling (rho, eta) -> (rho, eta)(1 - lam2/2)
      preserves the apex-from-origin angle exactly because the
      same real positive factor multiplies both real and imaginary
      parts. tan(gamma_bar) = eta_bar/rho_bar = eta/rho identically.

    PROTECTION IDENTITY (P1): substituting the retained
      (rho, eta) = (1/6, sqrt(5)/6) and lambda^2 = alpha_s/2 yields
      tan(gamma_bar) = sqrt(5) as an exact identity in alpha_s.

    CLOSED-FORM CATALOG (N1)-(N9): all parent-note expressions
      reduce to canonical Rational+sqrt form symbolically, and the
      linear deviation theorem (N7) is verified via sympy series
      expansion.

    LO RECOVERY: at alpha_s -> 0, closed forms reduce to the retained
      atlas-leading right-angle triangle (rho_bar = 1/6,
      eta_bar = sqrt(5)/6, tan(beta_bar) = 1/sqrt(5),
      alpha_bar = pi/2).

  Audit-lane class for the parent's load-bearing step:
    (A) -- algebraic identity over symbolic apex coordinates and the
    NLO multiplicative-scaling premise. No external observed/fitted
    input enters the protection identity.

  This companion does NOT introduce a new claim row, a new source
  note, or any modification of the parent row's status. It only
  verifies the local algebraic content; independent audit retains
  responsibility for the parent row and its upstream authorities
  (apex coordinates, lambda^2 = alpha_s/2, alpha_s(v)).
""")


print(f"\n{'=' * 88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'=' * 88}")
sys.exit(1 if FAIL > 0 else 0)
