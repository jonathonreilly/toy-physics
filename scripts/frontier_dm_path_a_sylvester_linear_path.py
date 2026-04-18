"""
Frontier runner — Path A Sylvester Linear-Path Theorem.

Certifies the Sylvester-linear-path admissibility claim at the P3 pin:

    signature(H_base + J_*) = signature(H_base) = (2, 0, 1)

via an exact, theorem-grade 1D positivity argument on the cubic polynomial
det(H(t)) with H(t) = H_base + t * J_* and t in [0, 1].

This runner replaces the earlier sampled-evidence positivity argument
(11 grid points + 1107-point tube scan) with:

  1. Exact symbolic construction of H(t) via sympy from the retained affine
     generators T_m, T_delta, T_q (docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_
     AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md) and the retained
     base matrix H_base with gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3.
  2. Exact symbolic determinant: p(t) = det(H(t)), a cubic in t.
  3. Exact coefficient extraction p(t) = A0 + A1*t + A2*t^2 + A3*t^3.
  4. Exact cross-check: A0 == 32*sqrt(2)/9, matching the retained atlas.
  5. Exact cross-check: p(1) agrees with direct H_base + J_* determinant
     on the numerical P3 pin.
  6. Exact critical-point analysis of p: p'(t) = A1 + 2*A2*t + 3*A3*t^2 = 0
     is a quadratic; compute its real roots in closed form and filter to
     those in [0, 1].
  7. Theorem-grade minimum: min p over [0,1] is attained at one of
     {0, 1} union {critical points in [0,1]}.  Evaluate p exactly at each
     and take the smallest.
  8. PASS requires that smallest value to be > 0.

If the PASS condition holds, Sylvester's law of inertia forces
signature(H(t)) = signature(H(0)) = (2, 0, 1) for every t in [0, 1], in
particular at t = 1, i.e. at the P3 pin.

This is the certifying evidence surface for the Path A theorem note
`DM_FLAGSHIP_PATH_A_SYLVESTER_BRANCH_THEOREM_NOTE_2026-04-18.md`.

Scope caveat (retained from the theorem note):
    The argument is pointwise at the P3 pin along the linear baseline-
    connected segment.  It does NOT derive that the baseline-connected
    component of {det(H) != 0} is the physical live sheet.  That remains a
    separate input.
"""

from __future__ import annotations

import sys

import sympy as sp


# ---------------------------------------------------------------------------
# Retained constants and generators (exact)
# ---------------------------------------------------------------------------

# gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3.
gamma = sp.Rational(1, 2)
E1 = sp.sqrt(sp.Rational(8, 3))
E2 = sp.sqrt(8) / 3

# Retained base Hermitian matrix.
H_base = sp.Matrix(
    [
        [0,               E1,              -E1 - sp.I * gamma],
        [E1,              0,               -E2],
        [-E1 + sp.I * gamma, -E2,           0],
    ]
)

# Retained affine generators T_m, T_delta, T_q (real symmetric).
T_m = sp.Matrix(
    [
        [1, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
    ]
)
T_delta = sp.Matrix(
    [
        [0, -1,  1],
        [-1, 1,  0],
        [1,  0, -1],
    ]
)
T_q = sp.Matrix(
    [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
)

# P3 observational pin (retained by observational promotion).
m_star = sp.Rational(657061, 1000000)    # 0.657061
delta_star = sp.Rational(933806, 1000000)  # 0.933806
q_star = sp.Rational(715042, 1000000)    # 0.715042

J_star = m_star * T_m + delta_star * T_delta + q_star * T_q


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------

PASS = 0
FAIL = 0


def check(label, cond, detail=""):
    """Lightweight PASS/FAIL reporter."""
    global PASS, FAIL
    status = "PASS" if cond else "FAIL"
    if cond:
        PASS += 1
    else:
        FAIL += 1
    print(f"[{status}] {label}" + (f"  ({detail})" if detail else ""))


# ---------------------------------------------------------------------------
# Step 1 — Construct H(t) symbolically
# ---------------------------------------------------------------------------

t = sp.symbols("t", real=True)
H_of_t = H_base + t * J_star
check(
    "H(t) is 3x3 matrix",
    H_of_t.shape == (3, 3),
    f"shape={H_of_t.shape}",
)

# Hermiticity check: H(t) - H(t)^H = 0 for all t.
Hdag_minus_H = (H_of_t - H_of_t.H).applyfunc(sp.simplify)
check(
    "H(t) is Hermitian for all t",
    Hdag_minus_H == sp.zeros(3, 3),
    "H(t) = H(t)^H",
)

# ---------------------------------------------------------------------------
# Step 2 — Exact determinant as a polynomial in t
# ---------------------------------------------------------------------------

det_Ht = sp.expand(sp.simplify(H_of_t.det()))
# Extract coefficients.
poly = sp.Poly(det_Ht, t)
coeffs = poly.all_coeffs()  # highest degree first
# Pad if degree < 3
while len(coeffs) < 4:
    coeffs = [sp.Integer(0)] + coeffs
A3, A2, A1, A0 = coeffs  # p(t) = A3 t^3 + A2 t^2 + A1 t + A0
check(
    "det(H(t)) is cubic in t (degree <= 3)",
    poly.degree() <= 3,
    f"degree = {poly.degree()}",
)


# ---------------------------------------------------------------------------
# Step 3 — Atlas cross-check: A0 = det(H_base) = 32*sqrt(2)/9
# ---------------------------------------------------------------------------

A0_simplified = sp.simplify(A0)
atlas_value = 32 * sp.sqrt(2) / 9
check(
    "A0 = det(H_base) = 32*sqrt(2)/9  [atlas cross-check]",
    sp.simplify(A0_simplified - atlas_value) == 0,
    f"A0 = {A0_simplified}",
)


# ---------------------------------------------------------------------------
# Step 4 — Direct determinant cross-check at t = 1 (P3 pin)
# ---------------------------------------------------------------------------

p_at_1_from_poly = sp.simplify(A0 + A1 + A2 + A3)
p_at_1_direct = sp.simplify((H_base + J_star).det())
check(
    "p(1) from cubic == det(H_base + J_*) directly",
    sp.simplify(p_at_1_from_poly - p_at_1_direct) == 0,
    f"p(1) = {float(p_at_1_from_poly):.6f}",
)

# The retained atlas's recorded Basin 1 value is approximately 0.959.
p_at_1_num = float(p_at_1_from_poly)
check(
    "p(1) ~ 0.959 (matches retained Basin 1 value)",
    abs(p_at_1_num - 0.959) < 0.01,
    f"p(1) = {p_at_1_num:.6f}",
)


# ---------------------------------------------------------------------------
# Step 5 — Exact critical-point analysis of p(t)
# ---------------------------------------------------------------------------

# p'(t) = A1 + 2*A2*t + 3*A3*t^2
p_prime = sp.diff(poly.as_expr(), t)

# Solve p'(t) = 0 exactly.
critical_points_all = sp.solve(p_prime, t)
# Keep only real-valued roots in [0, 1].
critical_points_in_01 = []
for cp in critical_points_all:
    cp_simp = sp.nsimplify(sp.simplify(cp), rational=False)
    if cp_simp.is_real is False:
        continue
    try:
        cp_num = float(cp_simp)
    except (TypeError, ValueError):
        continue
    if 0 <= cp_num <= 1:
        critical_points_in_01.append(cp_simp)

check(
    "p'(t) = 0 solved exactly (quadratic in t)",
    len(critical_points_all) == 2,
    f"{len(critical_points_all)} critical points total",
)
print(f"        critical points (all): "
      f"{[float(sp.N(cp)) for cp in critical_points_all]}")
print(f"        critical points in [0,1]: "
      f"{[float(sp.N(cp)) for cp in critical_points_in_01]}")


# ---------------------------------------------------------------------------
# Step 6 — Theorem-grade min p over [0, 1]
# ---------------------------------------------------------------------------

# Extremum candidates are the closed-interval endpoints union the critical
# points inside (0, 1).
candidates = [sp.Integer(0), sp.Integer(1)] + critical_points_in_01
evaluations = [(c, sp.simplify(poly.as_expr().subs(t, c))) for c in candidates]

for c, val in evaluations:
    print(f"        p({float(c):.6f}) = {float(val):.6f}")

min_val = min(val for _, val in evaluations)
min_val_num = float(min_val)

check(
    "min_{t in [0,1]} p(t) > 0  [certifies det(H(t)) > 0]",
    min_val_num > 0,
    f"min = {min_val_num:.6f}",
)


# ---------------------------------------------------------------------------
# Step 7 — Retained atlas min cross-check (should be ~ 0.876)
# ---------------------------------------------------------------------------

check(
    "min p ~ 0.876 (matches retained atlas statement)",
    abs(min_val_num - 0.876) < 0.005,
    f"min = {min_val_num:.6f}",
)


# ---------------------------------------------------------------------------
# Step 8 — Sylvester signature conclusion
# ---------------------------------------------------------------------------

# Since det(H(t)) > 0 on [0, 1] (Step 6), H(t) is non-singular, and Sylvester's
# law of inertia gives signature(H(t)) = signature(H(0)).

# Compute signature(H_base) numerically to close the chain.
H_base_numeric = sp.Matrix(
    [[complex(H_base[i, j]) for j in range(3)] for i in range(3)]
)

import numpy as np

evals = np.linalg.eigvalsh(np.array(H_base_numeric.tolist(), dtype=complex))
n_pos = int(sum(1 for e in evals if e > 1e-12))
n_zero = int(sum(1 for e in evals if abs(e) <= 1e-12))
n_neg = int(sum(1 for e in evals if e < -1e-12))
# Retained atlas signature convention: (n_-, n_0, n_+).
signature_base = (n_neg, n_zero, n_pos)

check(
    "signature(H_base) = (2, 0, 1)  [convention (n_-, n_0, n_+)]",
    signature_base == (2, 0, 1),
    f"eigs = {sorted(float(e) for e in evals)}",
)

# At t=1 pin: direct eigenvalue check as independent cross-check.
H_pin_numeric = H_base_numeric + sp.Matrix(
    [[complex(J_star[i, j]) for j in range(3)] for i in range(3)]
)
evals_pin = np.linalg.eigvalsh(np.array(H_pin_numeric.tolist(), dtype=complex))
n_pos_pin = int(sum(1 for e in evals_pin if e > 1e-12))
n_zero_pin = int(sum(1 for e in evals_pin if abs(e) <= 1e-12))
n_neg_pin = int(sum(1 for e in evals_pin if e < -1e-12))
signature_pin = (n_neg_pin, n_zero_pin, n_pos_pin)

check(
    "signature(H_base + J_*) = (2, 0, 1)  [direct independent check]",
    signature_pin == (2, 0, 1),
    f"eigs = {sorted(float(e) for e in evals_pin)}",
)


# ---------------------------------------------------------------------------
# Interpretive summary
# ---------------------------------------------------------------------------

print()
print("=" * 72)
print("Sylvester Linear-Path Theorem — certification summary")
print("=" * 72)
print(
    "\n"
    "det(H(t)) is the exact cubic\n"
    "  p(t) = A3 t^3 + A2 t^2 + A1 t + A0\n"
    f"  A0 = {sp.simplify(A0)}\n"
    f"  A1 ~ {float(sp.N(sp.simplify(A1))):.6f}\n"
    f"  A2 ~ {float(sp.N(sp.simplify(A2))):.6f}\n"
    f"  A3 ~ {float(sp.N(sp.simplify(A3))):.6f}\n"
)
print(
    "Critical points of p(t) come from the quadratic p'(t) = 0, solved\n"
    "exactly.  The extremum of p on the closed interval [0, 1] is taken\n"
    "from the finite set {0, 1} union {critical points in (0, 1)}.\n"
)
print(
    f"min_{{t in [0,1]}} p(t) = {min_val_num:.6f}  >  0\n"
)
print(
    "By Sylvester's law of inertia, signature(H(t)) is constant on [0, 1],\n"
    "so signature(H_base + J_*) = signature(H_base) = (2, 0, 1).\n"
)
print(
    "Scope:\n"
    "  - Unconditional: H_pin lies on the same connected component of\n"
    "    {det(H) != 0} as H_base (the baseline-connected component), and\n"
    "    hence has signature (2, 0, 1).\n"
    "  - Still imposed: the identification of the baseline-connected\n"
    "    component as the physical live sheet.  Basin-2/X exclusion\n"
    "    remains conditional on this identification.\n"
)

print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(0 if FAIL == 0 else 1)
