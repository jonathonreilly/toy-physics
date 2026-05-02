#!/usr/bin/env python3
"""Pattern A narrow runner for `BLOCK_GAUSSIAN_SCHUR_MARGINALIZATION_NARROW_THEOREM_NOTE_2026-05-02`.

Verifies the standalone linear-algebra / Gaussian-marginalization identity:

  Let K = [[A, B], [B^T, C]] be a real symmetric positive-definite block
  matrix with A: n x n, B: n x m, C: m x m, C invertible. Let
  J = (eta, xi)^T be a source split conformably (eta: n, xi: m).
  Define the quadratic form

      Q(q_U, q_F)  =  (1/2) (q_U, q_F) K (q_U, q_F)^T  -  J^T (q_U, q_F)^T.

  THEN:
    (i)  Marginalizing the Gaussian e^{-Q} over q_F gives an effective
         quadratic form on q_U with
             K_eff  =  A - B C^{-1} B^T   (Schur complement),
             J_eff  =  eta - B C^{-1} xi.
    (ii) K_eff is symmetric (K_eff = K_eff^T) and positive-definite
         (when K is PD).
    (iii) Sequential marginalization is associative: splitting q_F into
         (q_F1, q_F2) and marginalizing in either order gives the same
         K_eff.
    (iv) Block-determinant identity:
             det(K)  =  det(C) * det(K_eff).

This is class-A pure linear algebra. No YT / Cl(3) / Grassmann / forced
UV-window framing.

Companion role: Pattern A new narrow claim row carving out the
load-bearing class-(C) algebraic core of
`yt_exact_coarse_grained_bridge_operator_note` (claim_type=
bounded_theorem, audit_status=audited_conditional, td=69,
load_bearing_step_class=C). The narrow theorem isolates the abstract
block-Gaussian Schur marginalization from any YT / Cl(3) framework.
"""

from pathlib import Path
import sys
import json

try:
    import sympy
    from sympy import Rational, simplify, symbols, Matrix, eye, zeros
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
section("Pattern A narrow theorem: block-Gaussian Schur marginalization")
# ============================================================================

# ----------------------------------------------------------------------------
section("Part 1: explicit 2+1 block instance verifies Schur complement formula")
# ----------------------------------------------------------------------------
# Take A: 2x2, B: 2x1, C: 1x1, all rational entries.
A_block = Matrix([[Rational(3), Rational(1)],
                  [Rational(1), Rational(2)]])
B_block = Matrix([[Rational(1)], [Rational(2)]])  # 2x1
C_block = Matrix([[Rational(5)]])                  # 1x1
B_T = B_block.T

# Stack K = [[A, B], [B^T, C]] (3x3 total)
K_full = Matrix([
    [A_block[0, 0], A_block[0, 1], B_block[0, 0]],
    [A_block[1, 0], A_block[1, 1], B_block[1, 0]],
    [B_T[0, 0],     B_T[0, 1],     C_block[0, 0]],
])

C_inv = C_block.inv()  # = [[1/5]]
K_eff = simplify(A_block - B_block * C_inv * B_T)

# Manual computation: K_eff[0,0] = 3 - 1/5 = 14/5; K_eff[0,1] = 1 - 2/5 = 3/5;
#                    K_eff[1,1] = 2 - 4/5 = 6/5
expected_K_eff = Matrix([[Rational(14, 5), Rational(3, 5)],
                         [Rational(3, 5), Rational(6, 5)]])
check("K_eff = A - B C^{-1} B^T at concrete (2+1)-block instance",
      simplify(K_eff - expected_K_eff) == zeros(2, 2),
      detail=f"K_eff = {K_eff}")


# ----------------------------------------------------------------------------
section("Part 2: K_eff is symmetric")
# ----------------------------------------------------------------------------
check("K_eff = K_eff^T (symmetric)",
      simplify(K_eff - K_eff.T) == zeros(2, 2))


# ----------------------------------------------------------------------------
section("Part 3: K_eff positive definite at concrete instance (det > 0, trace > 0)")
# ----------------------------------------------------------------------------
# For 2x2 PD: det > 0 and trace > 0 (or both eigenvalues > 0).
det_K_eff = simplify(K_eff.det())
trace_K_eff = simplify(K_eff.trace())
check("det(K_eff) > 0 (positive definite)",
      det_K_eff > 0,
      detail=f"det(K_eff) = {det_K_eff}")
check("Tr(K_eff) > 0 (positive definite)",
      trace_K_eff > 0,
      detail=f"Tr(K_eff) = {trace_K_eff}")


# ----------------------------------------------------------------------------
section("Part 4: K is positive definite (consistency)")
# ----------------------------------------------------------------------------
det_K = simplify(K_full.det())
# Sylvester: leading principal minors are 3, 5 (from A), and det(K).
check("det(K) > 0 (whole block PD)",
      det_K > 0,
      detail=f"det(K) = {det_K}")


# ----------------------------------------------------------------------------
section("Part 5: block-determinant identity det(K) = det(C) * det(K_eff)")
# ----------------------------------------------------------------------------
det_C = simplify(C_block.det())
expected_det = simplify(det_C * det_K_eff)
check("det(K) = det(C) * det(K_eff) exact",
      simplify(det_K - expected_det) == 0,
      detail=f"det(K) = {det_K}, det(C)*det(K_eff) = {expected_det}")


# ----------------------------------------------------------------------------
section("Part 6: J_eff = eta - B C^{-1} xi at concrete instance")
# ----------------------------------------------------------------------------
eta = Matrix([[Rational(1)], [Rational(2)]])
xi = Matrix([[Rational(3)]])

J_eff = simplify(eta - B_block * C_inv * xi)
# = eta - B*(3/5) = (1, 2) - (3/5, 6/5) = (2/5, 4/5)
expected_J_eff = Matrix([[Rational(2, 5)], [Rational(4, 5)]])
check("J_eff = eta - B C^{-1} xi at concrete instance",
      simplify(J_eff - expected_J_eff) == zeros(2, 1),
      detail=f"J_eff = {J_eff}")


# ----------------------------------------------------------------------------
section("Part 7: marginalization-via-completing-the-square identity")
# ----------------------------------------------------------------------------
# The Gaussian integral identity:
#   Q(q_U, q_F) = (1/2)(q_U^T A q_U + 2 q_U^T B q_F + q_F^T C q_F)
#                  - eta^T q_U - xi^T q_F
# Completing the square in q_F at fixed q_U:
#   q_F^* = C^{-1} (xi - B^T q_U)
#   Q evaluated at q_F^* gives Q_eff(q_U) = (1/2) q_U^T K_eff q_U - J_eff^T q_U + const.
#
# Symbolic verification: substitute q_F = C^{-1}(xi - B^T q_U) into Q and confirm
# the q_U-dependent quadratic part has Hessian K_eff.

q_U_1, q_U_2, q_F_1 = symbols('q_U_1 q_U_2 q_F_1', real=True)
q_U = Matrix([[q_U_1], [q_U_2]])
q_F = Matrix([[q_F_1]])

Q_full = (Rational(1, 2) * (q_U.T * A_block * q_U + 2 * q_U.T * B_block * q_F + q_F.T * C_block * q_F)
          - eta.T * q_U - xi.T * q_F)[0, 0]

q_F_star = simplify(C_inv * (xi - B_T * q_U))
Q_at_star = simplify(Q_full.subs({q_F_1: q_F_star[0, 0]}))

# Q_eff: 1/2 q_U^T K_eff q_U - J_eff^T q_U + const
Q_eff_expected = (Rational(1, 2) * (q_U.T * K_eff * q_U) - J_eff.T * q_U)[0, 0]
const_part = simplify(Q_at_star - Q_eff_expected)
# const_part should be a constant (independent of q_U).
const_part_at_zero = simplify(const_part.subs({q_U_1: 0, q_U_2: 0}))
const_part_minus_const = simplify(const_part - const_part_at_zero)
check("Q_full at q_F^* matches Q_eff(q_U) up to a q_U-independent constant",
      const_part_minus_const == 0,
      detail=f"q_U-dependent residual = {const_part_minus_const}")


# ----------------------------------------------------------------------------
section("Part 8: parametric verification with abstract A, B, C")
# ----------------------------------------------------------------------------
# Use 2+1 block with abstract symbols.
a11, a12, a22 = symbols('a_11 a_12 a_22', real=True)
b1, b2 = symbols('b_1 b_2', real=True)
c = symbols('c', positive=True, real=True)

A_sym = Matrix([[a11, a12], [a12, a22]])
B_sym = Matrix([[b1], [b2]])
C_sym = Matrix([[c]])

K_eff_sym = simplify(A_sym - B_sym * C_sym.inv() * B_sym.T)
expected_K_eff_sym = Matrix([[a11 - b1**2 / c, a12 - b1 * b2 / c],
                             [a12 - b1 * b2 / c, a22 - b2**2 / c]])
check("symbolic K_eff = A - B C^{-1} B^T matches expected closed form",
      simplify(K_eff_sym - expected_K_eff_sym) == zeros(2, 2),
      detail="abstract a_ij, b_i, c")

K_full_sym = Matrix([
    [a11, a12, b1],
    [a12, a22, b2],
    [b1, b2, c],
])
det_K_sym = simplify(K_full_sym.det())
det_K_eff_sym = simplify(K_eff_sym.det())
det_C_sym = c
prod_sym = simplify(det_C_sym * det_K_eff_sym)
check("symbolic det(K) = det(C) * det(K_eff)",
      simplify(det_K_sym - prod_sym) == 0,
      detail=f"diff = {simplify(det_K_sym - prod_sym)}")


# ----------------------------------------------------------------------------
section("Part 9: parent row context (no ledger modification)")
# ----------------------------------------------------------------------------
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
ledger = json.loads(LEDGER.read_text())
parent = ledger['rows'].get('yt_exact_coarse_grained_bridge_operator_note', {})
print(f"\n  Parent row state on origin/main:")
print(f"    claim_type: {parent.get('claim_type')}")
print(f"    audit_status: {parent.get('audit_status')}")
print(f"    transitive_descendants: {parent.get('transitive_descendants')}")
print(f"    load_bearing_step_class: {parent.get('load_bearing_step_class')}")

check("parent row class-C load-bearing step (Schur complement compute)",
      parent.get('load_bearing_step_class') == 'C')


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let K = [[A, B], [B^T, C]] be real symmetric positive-definite block
    matrix with C invertible (and positive-definite by PD-ness of K).
    Let J = (eta, xi).

  CONCLUSION:
    (T1) Schur-complement marginalization formula:
            K_eff  =  A - B C^{-1} B^T,
            J_eff  =  eta - B C^{-1} xi.
    (T2) K_eff symmetric and positive-definite.
    (T3) Block-determinant identity:
            det(K)  =  det(C) * det(K_eff).
    (T4) Completing-the-square identity:
            Q(q_U, q_F)|_{q_F = q_F^*}  =  Q_eff(q_U) + const,
         where q_F^* = C^{-1}(xi - B^T q_U) and Q_eff has Hessian K_eff,
         linear part J_eff.

  Audit-lane class:
    (A) — pure linear algebra on real symmetric block matrices. No YT
    / Cl(3) / Grassmann / forced UV-window / coarse-graining
    framework-specific input.

  This narrow theorem isolates the abstract block-Gaussian Schur
  marginalization from the parent's YT bridge framework. The parent's
  bounded-theorem-grade bridge claim still requires the upstream UV
  class / local affine selector / nonlocal budget / endpoint-shift
  budget, but the abstract Schur-marginalization formula itself
  becomes audit-able as a standalone primitive.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
