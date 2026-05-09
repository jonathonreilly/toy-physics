#!/usr/bin/env python3
"""Pattern A narrow runner for `KOIDE_CIRCULANT_CHARACTER_BRIDGE_NARROW_THEOREM_NOTE_2026-05-09`.

Verifies the standalone polynomial-algebra identities relating, on abstract
symbols (a in R, b in C), the parameters of a C_3[111]-circulant Hermitian

    H = a I + b C + bbar C^2,

with C the 3x3 cyclic permutation matrix, to the C_3 character coefficients
(a_0, z) of the eigenvalue triple lambda = (lam_0, lam_1, lam_2):

    lam_k =  a + b w^k + bbar w^{-k},   k = 0, 1, 2,    where  w = e^{2 pi i / 3},

    a_0  =  (lam_0 + lam_1 + lam_2)         / sqrt(3),
    z    =  (lam_0 + wbar lam_1 + w lam_2)  / sqrt(3).

THEN the following identities are checked exactly (Pattern A, pure algebra):

  (T1)  a_0  =  sqrt(3) * a,
  (T2)  z    =  sqrt(3) * b,
  (T3)  a_0^2 - 2 |z|^2  =  3 a^2 - 6 |b|^2.

In particular,

      a_0^2 = 2 |z|^2   <==>   3 a^2 = 6 |b|^2,

as a fact of polynomial algebra on (a, b) in R x C.

This is class-A pure algebra over R x C (with the standard root-of-unity
identity 1 + w + w^2 = 0). No Koide / charged-lepton mass / sqrt(m)
physical identification, no spectral-to-readout law, and no selection
principle is consumed.
"""

from pathlib import Path
import sys

try:
    import sympy
    from sympy import (
        Rational,
        sqrt,
        simplify,
        expand,
        symbols,
        I,
        conjugate,
        Matrix,
        eye,
        exp,
        pi,
    )
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
section("Pattern A narrow theorem: Koide circulant / character bridge identities")
# ============================================================================

# Symbolic ingredients: a in R, b in C with b = x + i y, real x, y.
a, x, y = symbols("a x y", real=True)
b = x + I * y
bbar = conjugate(b)
# w = exp(2 pi i / 3) = -1/2 + i sqrt(3)/2.
w = Rational(-1, 2) + I * sqrt(Rational(3)) / 2
wbar = conjugate(w)

# Sanity: w^3 = 1 and 1 + w + w^2 = 0 (root-of-unity facts used in proof).
w3 = simplify(w**3)
sum_unity = simplify(1 + w + w**2)
check("w^3 = 1 (cube root of unity)", w3 == 1, detail=f"w^3 = {w3}")
check("1 + w + w^2 = 0 (sum of cube roots of unity)",
      sum_unity == 0, detail=f"1 + w + w^2 = {sum_unity}")

# 3x3 cyclic permutation C with C[i, (i+1) mod 3] = 1.
C = Matrix([
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
])
I3 = eye(3)
C2 = simplify(C * C)
check("C^3 = I (cyclic permutation cubes to identity)",
      simplify(C * C * C) == I3,
      detail="explicit matrix product")

# Hermitian circulant H = a I + b C + bbar C^2.
H = a * I3 + b * C + bbar * C2


# ----------------------------------------------------------------------------
section("Part 1: lam_k = a + b w^k + bbar w^{-k} agrees with eigenvalue computation of H")
# ----------------------------------------------------------------------------
# For each k, the (right) eigenvector of C with eigenvalue w^k is
# v_k = (1, w^k, w^{2k})^T, since (C v_k)_i = v_k[(i+1) mod 3] = w^{k(i+1)}
# = w^k * v_k[i].  Then H v_k = (a + b w^k + bbar w^{-k}) v_k because
# C^2 v_k = w^{2k} v_k and w^{2k} = w^{-k} (mod 3).
def lam_formula(k):
    return a + b * w**k + bbar * w**(-k)


for k in (0, 1, 2):
    v_k = Matrix([1, w**k, w**(2 * k)])
    lhs = simplify(H * v_k)
    rhs = simplify(lam_formula(k) * v_k)
    diff = simplify(expand(lhs - rhs))
    check(f"H v_{k} = lam_{k} v_{k} with lam_{k} = a + b w^{k} + bbar w^{{-{k}}}",
          diff == Matrix([0, 0, 0]),
          detail=f"residual = {diff.T.tolist()[0]}")

# Also store the symbolic eigenvalues for later parts.
lam = [simplify(lam_formula(k)) for k in (0, 1, 2)]


# ----------------------------------------------------------------------------
section("Part 2 (T1): a_0 := (lam_0 + lam_1 + lam_2) / sqrt(3) = sqrt(3) * a")
# ----------------------------------------------------------------------------
a0_def = simplify((lam[0] + lam[1] + lam[2]) / sqrt(Rational(3)))
a0_expected = sqrt(Rational(3)) * a
check("a_0 = sqrt(3) * a symbolically",
      simplify(expand(a0_def - a0_expected)) == 0,
      detail=f"a_0 = {a0_def}, expected = {a0_expected}, "
             f"diff = {simplify(expand(a0_def - a0_expected))}")


# ----------------------------------------------------------------------------
section("Part 3 (T2): z := (lam_0 + wbar lam_1 + w lam_2) / sqrt(3) = sqrt(3) * b")
# ----------------------------------------------------------------------------
z_def = simplify((lam[0] + wbar * lam[1] + w * lam[2]) / sqrt(Rational(3)))
z_expected = sqrt(Rational(3)) * b
check("z = sqrt(3) * b symbolically",
      simplify(expand(z_def - z_expected)) == 0,
      detail=f"z = {z_def}, expected = {z_expected}, "
             f"diff = {simplify(expand(z_def - z_expected))}")


# ----------------------------------------------------------------------------
section("Part 4 (T3): a_0^2 - 2 |z|^2  =  3 a^2 - 6 |b|^2")
# ----------------------------------------------------------------------------
abs_b_sq = simplify(b * bbar)  # = x^2 + y^2
abs_z_sq = simplify(z_def * conjugate(z_def))
lhs_T3 = simplify(expand(a0_def**2 - 2 * abs_z_sq))
rhs_T3 = simplify(expand(3 * a**2 - 6 * abs_b_sq))
check("a_0^2 - 2 |z|^2 = 3 a^2 - 6 |b|^2 symbolically",
      simplify(expand(lhs_T3 - rhs_T3)) == 0,
      detail=f"diff = {simplify(expand(lhs_T3 - rhs_T3))}")

# Equational equivalence form: a_0^2 = 2 |z|^2  iff  3 a^2 = 6 |b|^2.
delta_chr = simplify(expand(a0_def**2 - 2 * abs_z_sq))
delta_op = simplify(expand(3 * a**2 - 6 * abs_b_sq))
check("(a_0^2 - 2 |z|^2) - (3 a^2 - 6 |b|^2) = 0 symbolically",
      simplify(expand(delta_chr - delta_op)) == 0,
      detail=f"diff = {simplify(expand(delta_chr - delta_op))}")


# ----------------------------------------------------------------------------
section("Part 5: numerical sanity at concrete (a, b)")
# ----------------------------------------------------------------------------
# Pick a = 2, b = 1 + 2 i  (off the cone:  3 a^2 = 12,  6 |b|^2 = 30).
a_val = Rational(2)
x_val = Rational(1)
y_val = Rational(2)
subs = {a: a_val, x: x_val, y: y_val}

a0_num = simplify(a0_def.subs(subs))
z_num = simplify(z_def.subs(subs))
abs_z_sq_num = simplify(z_num * conjugate(z_num))
abs_b_sq_num = x_val**2 + y_val**2

# a_0 should equal sqrt(3) * 2 = 2 sqrt(3).
check("at (a, b) = (2, 1 + 2 i): a_0 = 2 sqrt(3)",
      simplify(a0_num - 2 * sqrt(Rational(3))) == 0,
      detail=f"a_0 = {a0_num}")

# z should equal sqrt(3) * (1 + 2 i).
check("at (a, b) = (2, 1 + 2 i): z = sqrt(3) * (1 + 2 i)",
      simplify(z_num - sqrt(Rational(3)) * (Rational(1) + I * Rational(2))) == 0,
      detail=f"z = {z_num}")

# |z|^2 = 3 |b|^2 = 3 * 5 = 15.
check("at (a, b) = (2, 1 + 2 i): |z|^2 = 15",
      simplify(abs_z_sq_num - Rational(15)) == 0,
      detail=f"|z|^2 = {abs_z_sq_num}, 3 |b|^2 = {3 * abs_b_sq_num}")

# Bridge: a_0^2 - 2 |z|^2 = 12 - 30 = -18, and 3 a^2 - 6 |b|^2 = 12 - 30 = -18.
lhs_num = simplify(a0_num**2 - 2 * abs_z_sq_num)
rhs_num = simplify(3 * a_val**2 - 6 * abs_b_sq_num)
check("at (a, b) = (2, 1 + 2 i): a_0^2 - 2 |z|^2 = 3 a^2 - 6 |b|^2 = -18",
      simplify(lhs_num - rhs_num) == 0 and simplify(lhs_num + 18) == 0,
      detail=f"a_0^2 - 2 |z|^2 = {lhs_num}, 3 a^2 - 6 |b|^2 = {rhs_num}")

# On-cone instance: pick a = sqrt(2), b = 1 (so 3 a^2 = 6 = 6 |b|^2).
# Use rational substitutes to verify exactly: a^2 = 2, |b|^2 = 1.
a2_val = Rational(2)
xc_val = Rational(1)
yc_val = Rational(0)
abs_b_sq_c = xc_val**2 + yc_val**2
# Substitute a^2 -> 2 in lhs/rhs by working symbolically with the formula.
# Easier: pick a = 1, b = 1/sqrt(2) so 3 a^2 = 3 = 6 |b|^2 (since |b|^2 = 1/2).
xc2 = sqrt(Rational(1, 2))
subs_cone = {a: Rational(1), x: xc2, y: Rational(0)}
delta_chr_cone = simplify(expand(delta_chr.subs(subs_cone)))
delta_op_cone = simplify(expand(delta_op.subs(subs_cone)))
check("on-cone instance (a=1, b=1/sqrt(2)): a_0^2 - 2 |z|^2 = 0",
      simplify(delta_chr_cone) == 0,
      detail=f"a_0^2 - 2 |z|^2 = {delta_chr_cone}")
check("on-cone instance (a=1, b=1/sqrt(2)): 3 a^2 - 6 |b|^2 = 0",
      simplify(delta_op_cone) == 0,
      detail=f"3 a^2 - 6 |b|^2 = {delta_op_cone}")


# ----------------------------------------------------------------------------
section("Narrow theorem summary")
# ----------------------------------------------------------------------------
print("""
  Narrow Pattern A theorem statement:

  HYPOTHESIS:
    Let (a, b) in R x C be abstract symbols. Let C be the 3 x 3 cyclic
    permutation matrix and w = exp(2 pi i / 3). Define
        H     = a I + b C + bbar C^2,
        lam_k = a + b w^k + bbar w^{-k}   (k = 0, 1, 2),
        a_0   = (lam_0 + lam_1 + lam_2)         / sqrt(3),
        z     = (lam_0 + wbar lam_1 + w lam_2)  / sqrt(3).

  CONCLUSION:
    (T1)  a_0 = sqrt(3) * a    symbolic identity.
    (T2)  z   = sqrt(3) * b    symbolic identity.
    (T3)  a_0^2 - 2 |z|^2  =  3 a^2 - 6 |b|^2,
          and equivalently
              a_0^2 = 2 |z|^2  iff  3 a^2 = 6 |b|^2.

  Audit-lane class:
    (A) - pure polynomial algebra over R x C with the standard
    root-of-unity identity 1 + w + w^2 = 0. No Koide / charged-lepton
    mass / sqrt(m) / Wilson-source / selection-principle physical
    identification.

  This narrow theorem isolates the algebraic character/operator
  identities from any physical Wilson / charged-lepton / spectral-readout
  framing.
""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
print(f"PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL > 0 else 0)
