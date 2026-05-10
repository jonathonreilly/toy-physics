#!/usr/bin/env python3
"""Pattern A narrow runner for
`CKM_CP_PHASE_RHO_ETA_TO_DELTA_NARROW_THEOREM_NOTE_2026-05-10`.

Verifies the standalone polynomial-algebra identities

  Given abstract real positive symbols (w_A1, w_perp, r^2) with
  partition (P)  w_A1 + w_perp = 1,
  and abstract integer k >= 2:

  (T1)  rho^2 + eta^2 = r^2          where rho^2 := r^2 * w_A1, eta^2 := r^2 * w_perp.
  (T2)  cos^2(delta)  = w_A1         where cos^2(delta) := rho^2 / (rho^2 + eta^2).
  (T3)  sin^2(delta)  = w_perp       where sin^2(delta) := eta^2 / (rho^2 + eta^2).
  (T4)  cos^2 + sin^2 = 1            (from (T2) + (T3) + (P)).
  (T5)  tan^2(delta)  = w_perp / w_A1.
  (T6)  Specialising w_A1 = 1/k, w_perp = (k-1)/k:
        cos^2 = 1/k, sin^2 = (k-1)/k, tan^2 = k-1,
        delta = arccos(1/sqrt(k)) = arctan(sqrt(k-1)).
  (T7)  k = 6 numerical instance: cos^2 = 1/6, tan = sqrt(5),
        delta = 65.905157447889... deg.
  (T8)  Abstract substitution lambda^2 := alpha/n_pair, A^2 := n_pair/n_color:
        J_0 := lambda^6 A^2 eta  =  alpha^3 * sqrt(r^2 * w_perp) / (n_pair^2 * n_color).
        (Substitution recorded explicitly; symbolic equality to substituted form.)
  (T9)  Numerical (n_pair, n_color, k) = (2, 3, 6), r^2 = 1/6, w_perp = 5/6:
        J_0 = alpha^3 * sqrt(5) / 72 (substitution-form match to parent's stated form).
  (T10) Numerical witness on an explicit Wolfenstein-shape 3x3 unitary V whose apex
        (rho, eta) = (1/6, sqrt(5)/6): arctan(eta/rho) = arctan(sqrt(5)).

This is class-A pure polynomial algebra. No CKM atlas authority, no
Wolfenstein structural identities, no alpha_s value, no projector-split
1+5 input, no quark-mass identification, no PDG comparator is consumed.
The k=6 integer specialisation is a substitution under abstract integer
hypothesis; the load-bearing physical input that picks out k=6 is an
upstream CKM atlas / center-excess-projector authority outside this
note's scope.
"""

from __future__ import annotations

from pathlib import Path
import math
import sys

try:
    import sympy
    from sympy import (
        Rational,
        Symbol,
        sqrt,
        simplify,
        symbols,
        expand,
        Eq,
        cos,
        sin,
        tan,
        acos,
        atan,
        pi,
        Matrix,
        I,
        exp,
        re,
        im,
        Abs,
        conjugate,
        nsimplify,
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
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title: str) -> None:
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A narrow theorem: CKM CP-phase rho-eta to delta algebraic core")
# ============================================================================

# Abstract positive symbols.
w_A1 = Symbol('w_A1', positive=True)
w_perp = Symbol('w_perp', positive=True)
r2 = Symbol('r^2', positive=True)
alpha = Symbol('alpha', positive=True)
n_pair = Symbol('n_pair', positive=True)
n_color = Symbol('n_color', positive=True)
k = Symbol('k', positive=True, integer=True)

# Definitions (D-rho), (D-eta), (D-cos), (D-sin), (D-tan).
rho2 = r2 * w_A1
eta2 = r2 * w_perp
# Use rho^2 + eta^2 (NOT r^2) in the denominator so the cos^2/sin^2 identity reads
# strictly off the algebraic definition, not a hypothesis-substituted form.
cos2_delta_def = rho2 / (rho2 + eta2)
sin2_delta_def = eta2 / (rho2 + eta2)
tan2_delta_def = sin2_delta_def / cos2_delta_def

# Partition hypothesis (P): w_A1 + w_perp = 1.
# We enforce by substituting w_perp -> 1 - w_A1.
P_subs = {w_perp: 1 - w_A1}


# ----------------------------------------------------------------------------
section("Part 1: (T1) rho^2 + eta^2 = r^2 under (P)")
# ----------------------------------------------------------------------------
T1_lhs = rho2 + eta2
T1_rhs = r2
T1_check = simplify((T1_lhs - T1_rhs).subs(P_subs))
check("(T1) rho^2 + eta^2 - r^2 = 0 under (P)",
      T1_check == 0,
      detail=f"diff = {T1_check}")


# ----------------------------------------------------------------------------
section("Part 2: (T2) cos^2(delta) = w_A1")
# ----------------------------------------------------------------------------
T2_diff = simplify((cos2_delta_def - w_A1).subs(P_subs))
check("(T2) cos^2(delta) - w_A1 = 0 under (P)",
      T2_diff == 0,
      detail=f"diff = {T2_diff}")
# Also record the off-(P) form for transparency.
T2_offP = simplify(cos2_delta_def - w_A1 / (w_A1 + w_perp))
check("(T2-offP) cos^2(delta) = w_A1 / (w_A1 + w_perp) symbolically (no (P) needed)",
      T2_offP == 0,
      detail=f"diff = {T2_offP}")


# ----------------------------------------------------------------------------
section("Part 3: (T3) sin^2(delta) = w_perp")
# ----------------------------------------------------------------------------
T3_diff = simplify((sin2_delta_def - w_perp).subs(P_subs))
check("(T3) sin^2(delta) - w_perp = 0 under (P)",
      T3_diff == 0,
      detail=f"diff = {T3_diff}")
# Also record the off-(P) form for transparency.
T3_offP = simplify(sin2_delta_def - w_perp / (w_A1 + w_perp))
check("(T3-offP) sin^2(delta) = w_perp / (w_A1 + w_perp) symbolically (no (P) needed)",
      T3_offP == 0,
      detail=f"diff = {T3_offP}")


# ----------------------------------------------------------------------------
section("Part 4: (T4) Pythagorean identity cos^2 + sin^2 = 1 under (P)")
# ----------------------------------------------------------------------------
T4_diff = simplify((cos2_delta_def + sin2_delta_def - 1).subs(P_subs))
check("(T4) cos^2 + sin^2 - 1 = 0 under (P)",
      T4_diff == 0,
      detail=f"diff = {T4_diff}")


# ----------------------------------------------------------------------------
section("Part 5: (T5) tan^2(delta) = w_perp / w_A1")
# ----------------------------------------------------------------------------
T5_diff = simplify(tan2_delta_def - w_perp / w_A1)
check("(T5) tan^2(delta) - w_perp/w_A1 = 0 symbolically",
      T5_diff == 0,
      detail=f"diff = {T5_diff}")


# ----------------------------------------------------------------------------
section("Part 6: (T6) integer-k specialisation w_A1 = 1/k, w_perp = (k-1)/k")
# ----------------------------------------------------------------------------
k_subs = {w_A1: 1 / k, w_perp: (k - 1) / k}

T6a_diff = simplify((cos2_delta_def - 1 / k).subs(k_subs))
check("(T6a) cos^2(delta) = 1/k under k-specialisation",
      T6a_diff == 0,
      detail=f"diff = {T6a_diff}")

T6b_diff = simplify((sin2_delta_def - (k - 1) / k).subs(k_subs))
check("(T6b) sin^2(delta) = (k-1)/k under k-specialisation",
      T6b_diff == 0,
      detail=f"diff = {T6b_diff}")

T6c_diff = simplify((tan2_delta_def - (k - 1)).subs(k_subs))
check("(T6c) tan^2(delta) = k - 1 under k-specialisation",
      T6c_diff == 0,
      detail=f"diff = {T6c_diff}")

# (T6d) trig identity: arccos(1/sqrt(k)) = arctan(sqrt(k-1))
# at abstract k this is the standard identity tan(arccos(x)) = sqrt(1-x^2)/x.
# Verify symbolically with a few concrete integer k's.
for k_val in [2, 3, 6, 12]:
    lhs = math.acos(1.0 / math.sqrt(k_val))
    rhs = math.atan(math.sqrt(k_val - 1))
    check(
        f"(T6d) arccos(1/sqrt(k)) = arctan(sqrt(k-1)) at k = {k_val}",
        abs(lhs - rhs) < 1e-14,
        detail=f"|lhs - rhs| = {abs(lhs - rhs):.3e}",
    )


# ----------------------------------------------------------------------------
section("Part 7: (T7) k = 6 numerical readout")
# ----------------------------------------------------------------------------
k_six = {w_A1: Rational(1, 6), w_perp: Rational(5, 6)}

T7a_val = simplify(cos2_delta_def.subs(k_six))
check("(T7a) cos^2(delta) = 1/6 exact at (w_A1, w_perp) = (1/6, 5/6)",
      T7a_val == Rational(1, 6),
      detail=f"cos^2 = {T7a_val}")

T7b_val = simplify(tan2_delta_def.subs(k_six))
check("(T7b) tan^2(delta) = 5 exact at (w_A1, w_perp) = (1/6, 5/6)",
      T7b_val == 5,
      detail=f"tan^2 = {T7b_val}")

# Numerical delta in degrees.
delta_rad = math.acos(1.0 / math.sqrt(6.0))
delta_deg = math.degrees(delta_rad)
expected_deg = 65.90515744788931
check(
    "(T7c) delta = arccos(1/sqrt(6)) = arctan(sqrt(5))",
    abs(math.acos(1.0 / math.sqrt(6.0)) - math.atan(math.sqrt(5.0))) < 1e-15,
    detail=f"diff = {abs(math.acos(1.0 / math.sqrt(6.0)) - math.atan(math.sqrt(5.0))):.3e}",
)
check(
    f"(T7d) delta = {expected_deg:.12f} deg numerical (within 1e-12)",
    abs(delta_deg - expected_deg) < 1e-12,
    detail=f"delta_deg = {delta_deg:.12f}",
)


# ----------------------------------------------------------------------------
section("Part 8: (T8) Jarlskog-shape symbolic substitution J_0 = lambda^6 A^2 eta")
# ----------------------------------------------------------------------------
# Definitions:
#   lambda^2 := alpha / n_pair,  A^2 := n_pair / n_color, eta := sqrt(r^2 * w_perp).
lambda2 = alpha / n_pair
A2 = n_pair / n_color
eta_sym = sqrt(r2 * w_perp)

J_def = lambda2**3 * A2 * eta_sym
# Substitution-derived form.
J_substituted = (alpha**3 / (n_pair**2 * n_color)) * sqrt(r2 * w_perp)
# Verify symbolic equality.
T8_diff = simplify(J_def - J_substituted)
check(
    "(T8) J_0 := lambda^6 A^2 eta = alpha^3 * sqrt(r^2 * w_perp) / (n_pair^2 * n_color)",
    T8_diff == 0,
    detail=f"diff = {T8_diff}",
)


# ----------------------------------------------------------------------------
section("Part 9: (T9) k = 6 numerical specialisation of (T8)")
# ----------------------------------------------------------------------------
# (n_pair, n_color, k) = (2, 3, 6), r^2 = 1/k = 1/6, w_perp = (k-1)/k = 5/6.
J_substituted_at_236 = J_substituted.subs({
    n_pair: 2,
    n_color: 3,
    r2: Rational(1, 6),
    w_perp: Rational(5, 6),
})
J_substituted_at_236 = simplify(J_substituted_at_236)
expected_form_T8 = alpha**3 * sqrt(Rational(5, 36)) / (4 * 3)  # = alpha^3 sqrt(5) / 72
# alpha^3 * sqrt(5/36) / 12 = alpha^3 * (sqrt(5)/6) / 12 = alpha^3 * sqrt(5) / 72
expected_T9_substituted = simplify(alpha**3 * sqrt(5) / 72)
T9_diff = simplify(J_substituted_at_236 - expected_T9_substituted)
check(
    "(T9) J_0 = alpha^3 * sqrt(5) / 72 at (n_pair, n_color, r^2, w_perp) = (2, 3, 1/6, 5/6)",
    T9_diff == 0,
    detail=f"J_substituted = {J_substituted_at_236}",
)


# ----------------------------------------------------------------------------
section("Part 10: (T10) Numerical 3x3 unitary witness with apex (rho, eta) = (1/6, sqrt(5)/6)")
# ----------------------------------------------------------------------------
# Construct a 3x3 unitary V whose Wolfenstein-leading apex is (1/6, sqrt(5)/6).
# Strategy: build V directly from the standard Wolfenstein parameterisation
# truncated at O(lambda^3) with lambda = 0.225 (chosen as small generic positive),
# A = sqrt(2/3), rho = 1/6, eta = sqrt(5)/6. Then verify:
#   (a) V is approximately unitary (to O(lambda^4) error),
#   (b) the apex angle arctan(eta/rho) matches arctan(sqrt(5)).
# This is a numerical witness; the algebraic content of (T1)-(T9) is independent
# of any particular unitary matrix.
lam_val = 0.225
A_val = math.sqrt(2.0 / 3.0)
rho_val = 1.0 / 6.0
eta_val = math.sqrt(5.0) / 6.0

# Standard Wolfenstein O(lambda^3) CKM matrix.
import cmath
V11 = 1.0 - 0.5 * lam_val**2
V12 = lam_val
V13 = A_val * lam_val**3 * (rho_val - 1j * eta_val)
V21 = -lam_val
V22 = 1.0 - 0.5 * lam_val**2
V23 = A_val * lam_val**2
V31 = A_val * lam_val**3 * (1.0 - rho_val - 1j * eta_val)
V32 = -A_val * lam_val**2
V33 = 1.0

# Apex angle from the Wolfenstein convention (rho, eta).
apex_angle_rad = math.atan2(eta_val, rho_val)
expected_apex_rad = math.atan(math.sqrt(5.0))
check(
    "(T10a) apex arctan(eta/rho) = arctan(sqrt(5)) at (rho, eta) = (1/6, sqrt(5)/6)",
    abs(apex_angle_rad - expected_apex_rad) < 1e-14,
    detail=f"diff = {abs(apex_angle_rad - expected_apex_rad):.3e}",
)
# Apex coordinates exact rational sanity check.
check(
    "(T10b) rho^2 + eta^2 = 1/6 exact at (1/6, sqrt(5)/6)",
    abs(rho_val**2 + eta_val**2 - 1.0 / 6.0) < 1e-15,
    detail=f"rho^2 + eta^2 = {rho_val**2 + eta_val**2:.15f}",
)
# Unitarity check at leading order (within O(lambda^4)).
row1 = [V11, V12, V13]
row2 = [V21, V22, V23]
row3 = [V31, V32, V33]
def row_norm_sq(row):
    return sum(abs(z)**2 for z in row)
n1, n2, n3 = row_norm_sq(row1), row_norm_sq(row2), row_norm_sq(row3)
# Each row should be 1 + O(lambda^4) ~ 1 + 6.4e-3.
check(
    "(T10c) row 1 norm^2 = 1 + O(lambda^4) within 1e-2",
    abs(n1 - 1.0) < 1e-2,
    detail=f"|row1|^2 = {n1:.6f}",
)
check(
    "(T10d) row 2 norm^2 = 1 + O(lambda^4) within 1e-2",
    abs(n2 - 1.0) < 1e-2,
    detail=f"|row2|^2 = {n2:.6f}",
)
check(
    "(T10e) row 3 norm^2 = 1 + O(lambda^4) within 1e-2",
    abs(n3 - 1.0) < 1e-2,
    detail=f"|row3|^2 = {n3:.6f}",
)
# Off-diagonal row dot products: row1.row2*, row1.row3*, row2.row3* should be ~0.
def row_dot(a, b):
    return sum(x * y.conjugate() for x, y in zip(a, b))
d12 = row_dot(row1, row2)
d13 = row_dot(row1, row3)
d23 = row_dot(row2, row3)
check(
    "(T10f) row1 . row2* ~ 0 to O(lambda^4)",
    abs(d12) < 1e-2,
    detail=f"|row1.row2*| = {abs(d12):.3e}",
)
check(
    "(T10g) row1 . row3* ~ 0 to O(lambda^4)",
    abs(d13) < 1e-2,
    detail=f"|row1.row3*| = {abs(d13):.3e}",
)
check(
    "(T10h) row2 . row3* ~ 0 to O(lambda^4)",
    abs(d23) < 1e-2,
    detail=f"|row2.row3*| = {abs(d23):.3e}",
)


# ----------------------------------------------------------------------------
section("Part 11: Off-cone sanity (uniform partition w_A1 = w_perp = 1/2)")
# ----------------------------------------------------------------------------
# At w_A1 = w_perp = 1/2: cos^2 = 1/2, tan^2 = 1, delta = pi/4 = 45 deg.
# This is the "balanced" partition and demonstrates the cone is non-trivial.
uniform_subs = {w_A1: Rational(1, 2), w_perp: Rational(1, 2)}
cos2_uniform = simplify(cos2_delta_def.subs(uniform_subs))
tan2_uniform = simplify(tan2_delta_def.subs(uniform_subs))
check(
    "uniform partition w_A1 = w_perp = 1/2 gives cos^2 = 1/2 (off the k=6 cone)",
    cos2_uniform == Rational(1, 2),
    detail=f"cos^2 = {cos2_uniform}",
)
check(
    "uniform partition gives tan^2 = 1 (off the k=6 cone, delta = pi/4)",
    tan2_uniform == 1,
    detail=f"tan^2 = {tan2_uniform}",
)


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Abstract real positive symbols (w_A1, w_perp, r^2) with partition
        (P)  w_A1 + w_perp = 1,  w_A1 > 0,  w_perp > 0,
    and definitions
        rho^2 := r^2 * w_A1,  eta^2 := r^2 * w_perp,
        cos^2(delta) := rho^2 / (rho^2 + eta^2),
        sin^2(delta) := eta^2 / (rho^2 + eta^2),
        tan^2(delta) := sin^2(delta) / cos^2(delta).

  CONCLUSION:
    (T1) rho^2 + eta^2 = r^2 under (P).
    (T2) cos^2(delta) = w_A1.
    (T3) sin^2(delta) = w_perp.
    (T4) cos^2 + sin^2 = 1 under (P).
    (T5) tan^2(delta) = w_perp / w_A1.
    (T6) k-specialisation w_A1 = 1/k, w_perp = (k-1)/k:
           cos^2 = 1/k, sin^2 = (k-1)/k, tan^2 = k-1,
           delta = arccos(1/sqrt(k)) = arctan(sqrt(k-1)).
    (T7) k = 6 instance: cos^2 = 1/6, tan = sqrt(5),
         delta = 65.905157447889... deg.
    (T8) Jarlskog-shape lambda^6 A^2 eta substitution reduces to
         alpha^3 * sqrt(r^2 * w_perp) / (n_pair^2 * n_color) under
         (J-l), (J-A), (D-eta).
    (T9) (n_pair, n_color, r^2, w_perp) = (2, 3, 1/6, 5/6) gives
         J_0 = alpha^3 * sqrt(5) / 72 (substitution form matches the
         parent atlas's stated factorisation).
    (T10) Numerical 3x3 unitary witness: an explicit Wolfenstein-shape
          V with apex (1/6, sqrt(5)/6) has arctan(eta/rho) = arctan(sqrt(5))
          and approximate unitarity at O(lambda^4) precision.

  Audit-lane class:
    (A) — pure polynomial algebra over abstract positive symbols
    (w_A1, w_perp, r^2, alpha, n_pair, n_color, k). No CKM atlas
    authority, no Wolfenstein structural identity, no projector-split
    1+5 input, no alpha_s value, no PDG comparator.

  This narrow theorem isolates the CP-plane-coordinate -> phase-angle
  algebraic transformation from the upstream physical CKM-atlas /
  Wolfenstein / alpha_s authorities that the parent bundles together.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
